#!/usr/bin/env python3
"""Static creative judge — accept / accept-with-changes / reject, one entry point.

Usage:
    python3 engine/creative_judge.py <kit_dir>            # judge a whole kit
    python3 engine/creative_judge.py <ad.html> [...]      # judge specific creatives
    python3 engine/creative_judge.py <kit_dir> --json     # machine-readable verdicts
    python3 engine/creative_judge.py <kit_dir> --quiet    # verdict lines only
    python3 engine/creative_judge.py <kit_dir> --no-log   # don't append to the verdict log

WHY THIS EXISTS (13 Aug 2026). The rules were already enforced by four separate scripts that
nobody ran as a set, so a creative could pass ad_lint.py and still ship with clipped text, a
banned claim, or a 2.15x-cost wall of primary text. This runs Gate 0 in one call, applies one
decision procedure, and writes every verdict to a log so the rubric can eventually be measured
instead of remembered. Rulebook: reference/gate-rules.md, plus reference/house-rules.md for the judgement layer.

GATE 0 (this script, deterministic — no model):
    ad_lint.py       C1..C22  copy + call-out, on the ad HTML
    ad_render_qa.py  E1..E4   clipping / crop band / dead band, on the rendered PNG
    crop_qa.py       X1       ink inside the discarded square-crop bands
    check_claims.py  T1       trust-claim accuracy, brand by product line, negative-sell
    (this file)      C21      primary text length, on the kit's ad_copy*.md
                     K1       every creative has an anchor-text entry

GATE 1 (vision, not yet built) and GATE 2 (novelty vs kit + past ads) are described in the
rulebook. A creative that passes Gate 0 is NOT accepted outright — it is "pending vision".

DECISION PROCEDURE
    any BLOCK                 -> REJECT
    2 or more FIX             -> REJECT
    exactly 1 FIX             -> ACCEPT WITH CHANGES
    0 FIX, any number of WARN -> ACCEPT (each WARN is a decision that must be stated)

Tier mapping: a FAIL from a checker is a BLOCK unless its rule id is in SOFT_RULES, which
holds the rules where a failure is real but cheap to correct rather than disqualifying.
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, 'creative_verdicts.jsonl')

# Rules whose FAIL is a FIX rather than a BLOCK. Everything else that FAILs is a BLOCK.
#
# BACKTEST CORRECTION (13 Aug 2026). C7 (em-dash) and C8 (font size) were BLOCK and between
# them killed the two cheapest ads in the whole backtest: rid_poster_vote at ₹38 and
# rid_poster_databank at ₹45, index 0.45 and 0.54, both with clean call-outs. They are HOUSE
# STYLE, not performance: an em-dash has never been shown to cost anything, and C8's size floor
# assumes `.head` is a giant call-out when in several design families it is body copy. A rule
# with no cost evidence behind it may ask for a change; it may not block a launch.
#
# Only two kinds of rule BLOCK now:
#   (a) measured cost evidence  — C17 (HR topic ~10x), C18 (never converts), V1, V3
#   (b) compliance or brand     — C13/C14/C15/C16/T1, where the cost of being wrong is not CPL
# C1 is a FIX, not a BLOCK. It is a real signal — cryptic call-outs were rejected on sight four
# times in one session — but it decides "does this line have a verb" from a hand-maintained word
# list, and a closed list always has holes ("coach" is not in it). On the backtest it blocked 25
# creatives that were approved and shipped, and two ads that beat their campaign median. One C1
# alone now reads as accept-with-changes; C1 plus any other substantive defect still rejects.
# C23 (no identity call-out) is a FIX. It discriminates well — it fires on 14.9% of approved
# work against 27.1% of unshipped — but it matches identity by keyword, and an ad can name its
# audience without using the word: "School hours" (index 0.80) targets mothers, "cw 06 types
# promotion" (0.67) targets working writers. As a blocker it rejected both. Gate 1 answers
# "who is this for" from the thumbnail and settles it properly.
SOFT_RULES = {'C1', 'C3', 'C4', 'C6', 'C7', 'C8', 'C9', 'C10', 'C19', 'C21', 'C22', 'C23',
              'C24', 'C25', 'C26', 'C27', 'E3', 'K1'}

# C10 also never accumulates into a rejection. A monetary figure on an ad is worth a look, not a
# spike: these products sell income, and the rule fired on 16.8% of approved work against 6.0%
# of unshipped. Ramanuj, 13 Aug 2026: "suspect but not necessarily a reject outright".
STYLE_RULES_EXTRA = {'C10'}

# Rules carry an effective date; a creative OLDER than the rule is noted, never
# failed. This has been stated policy since judging-static-ads ("rules postdating
# an approved creative are noted, not retro-enforced") but nothing enforced it, so
# on 16 Aug 2026 the judge was rejecting 5 of 84 approved creatives, four of them
# through C26 — a rule Ramanuj dictated the day before, fired at ads approved weeks
# earlier. Dates come from each rule's own provenance comment; only rules with a
# sourced date appear here.
RULE_EFFECTIVE = {
    'C1': '2026-07-26',    # no-riddle call-out (feedback_no_cryptic_callouts)
    'C21': '2026-08-13',   # primary-text length (this file's own founding date)
    'C23': '2026-08-13',   # identity call-out required
    'C26': '2026-08-15',   # ₹10 CTA must state the total value
}


def retro_downgrade(issues, path):
    """FAILs from rules newer than the creative become notes."""
    try:
        born = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(path)))
    except OSError:
        return issues
    out = []
    for lvl, code, msg in issues:
        if lvl == 'FAIL' and RULE_EFFECTIVE.get(code, '0') > born:
            out.append(('WARN', code, msg + f' [rule effective {RULE_EFFECTIVE[code]}, '
                        f'creative predates it — noted, not enforced]'))
        else:
            out.append((lvl, code, msg))
    return out

# STYLE rules are house preference with no cost evidence. They are reported so the creative can
# be tidied, but they NEVER accumulate into a rejection — the first re-tier still killed
# rid_poster_vote (index 0.45) and rid_poster_databank (0.54) purely by stacking an em-dash on
# top of a font size. Two taste notes are not a reason to spike the cheapest ad in the account.
STYLE_RULES = {'C4', 'C6', 'C7', 'C8', 'C10', 'C19', 'C22'}

# Pixel rules that are NOT calibrated for full-bleed 4:5 statics (measured 13 Aug 2026 over
# 600 rendered creatives): E1 fired on 77%, E2 on 162% (multiple hits per file), and E2 hit
# 919 non-carousel creatives against 55 carousel ones. Both assume a padded canvas whose
# corner pixel is the true background, which is false for edge-to-edge designs with a brand
# bar or a full-width footer. The 1:1 centre crop they protect against is real for CAROUSEL
# cards, so they stay BLOCK there and drop to WARN elsewhere until someone calibrates them
# against creatives that actually shipped. Judging every static on them rejects 100% of kits,
# which is the same as having no judge at all.
CAROUSEL_ONLY = {'E1', 'E2', 'X1'}

# Kit-directory keywords that mean a LawSikho product. Deliberately narrower than the hint list
# in check_claims.py: this is matched against the kit folder only, never a creative filename.
LAWSIKHO_KITS = ('lawsikho', 'ip_law', 'iplaw', 'patent', 'judiciary', 'uscl', 'litigation',
                 'sqe', 'ca_bar', 'cabar', 'arbitration', 'contract_drafting', 'legal_ai',
                 'legalai', 'criminal_lit', 'corp_lit', 'techlaw', 'tech_law')

VERDICT_ACCEPT = 'ACCEPT'
VERDICT_CHANGES = 'ACCEPT WITH CHANGES'
VERDICT_REJECT = 'REJECT'


# --------------------------------------------------------------------------- helpers
def run(cmd):
    """Run a checker; return (stdout, exit_code). Never raises."""
    try:
        # encoding is explicit: text=True alone decodes with the Windows ANSI codepage, so a
        # checker that echoes an emoji from the face (the chat layout's call-outs do) killed
        # the reader thread with UnicodeDecodeError and the judge reported as ERROR in
        # check_all while every face was in fact fine. 18 Sep 2026.
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120,
                           encoding="utf-8", errors="replace")
        return p.stdout + p.stderr, p.returncode
    except Exception as exc:                                  # checker missing / crashed
        return f'[judge] could not run {cmd[1]}: {exc}\n', -1


ISSUE_RX = re.compile(r'\[(FAIL|WARN)\s+([A-Z]\d+)\]\s*(.*)')


def parse_issues(out):
    """Pull [LEVEL CODE] message lines out of a checker's stdout."""
    found = []
    for line in out.splitlines():
        m = ISSUE_RX.search(line)
        if m:
            found.append((m.group(1), m.group(2), m.group(3).strip()))
    return found


def tier(level, code, carousel=False):
    if level == 'WARN':
        return 'WARN'
    if code in CAROUSEL_ONLY and not carousel:
        return 'WARN'
    return 'FIX' if code in SOFT_RULES else 'BLOCK'


def stem_variants(name):
    """Every plausible spelling of a creative's stem.

    Kits are not consistent: the source may be `src_01_it_security.html` while the render is
    `01_it_security.png` and the anchor heading is `01_it_security.png`. Matching only the
    literal stem made K1 fire on all 39 ads of a kit whose anchor text was in fact complete.
    """
    stem = os.path.splitext(os.path.basename(name))[0]
    out = [stem]
    for rx in (r'^src_', r'^_+', r'^ad_', r'_1080x1350$'):
        out += [re.sub(rx, '', s) for s in list(out)]
    return list(dict.fromkeys(s for s in out if s))


RENDER_DIRS = ('ads', 'previews', 'renders', 'png', 'out')


def _tail(stem):
    """The descriptive part of a stem, with any leading index dropped.

    Kits renumber between source and render: `html/cw_29_eye_test.html` is rendered as
    `ads/11_eye_test.png`. Both reduce to `eye_test`.
    """
    return re.sub(r'^(?:cw_|src_|ad_)?\d+[a-z]?_', '', stem)


def png_for(html_path):
    """Find the rendered PNG that belongs to an ad HTML, if it has been rendered.

    FIXED 24 Aug 2026. This used to look only in the HTML's own directory. Every kit in
    this repo keeps sources in `html/` and renders in a SIBLING `ads/`, so it returned
    None for all of them and the entire pixel gate - ad_render_qa (E1..E4) and crop_qa
    (X1) - was silently skipped on every creative ever judged. SKILL.md documented the
    manual workaround ("copy the pair into one folder"), which nobody did. Verified by
    `png_for('ContentWriting_SectionA_29-31Aug/html/16_will_you.html') -> None` while
    `ads/16_will_you.png` sat right there.
    """
    d = os.path.dirname(html_path) or '.'
    parent = os.path.dirname(d) or '.'
    search = [d] + [os.path.join(parent, s) for s in RENDER_DIRS]
    # Carousels are rendered into a subfolder of ads/ (e.g. ads/cw_22_carousel/), so
    # walk one level down as well. One level only: deeper is archive, not renders.
    for base in list(search):
        if os.path.isdir(base):
            search += [os.path.join(base, s) for s in sorted(os.listdir(base))
                       if os.path.isdir(os.path.join(base, s))]

    # 1. exact stem, in the HTML's directory then the usual render directories
    for dd in search:
        if not os.path.isdir(dd):
            continue
        for v in stem_variants(html_path):
            for cand in (v + '.png', v + '_1080x1350.png'):
                p = os.path.join(dd, cand)
                if os.path.exists(p):
                    return p

    # 2. renumbered render: match on the descriptive tail, but ONLY when exactly one
    #    candidate matches. An ambiguous match is worse than no match, because it would
    #    judge one creative's pixels against another's rules.
    want = _tail(os.path.splitext(os.path.basename(html_path))[0])
    if want:
        for dd in search:
            if not os.path.isdir(dd):
                continue
            hits = [os.path.join(dd, f) for f in sorted(os.listdir(dd))
                    if f.lower().endswith('.png')
                    and _tail(os.path.splitext(f)[0]) == want]
            if len(hits) == 1:
                return hits[0]
    return None


def is_creative(path):
    """Ad HTMLs only.

    Landing pages, contact sheets, scraped research pages and QA scratch files all live in the
    same kit folders and must not be judged as creatives — on a 1,251-file sweep they were what
    produced most of the C10/C11/C12/C15/C18 hits, because an LP is *allowed* to carry the
    money ladder that an ad is not. The filter is deliberately conservative: a file that is not
    clearly a creative is skipped rather than judged.
    """
    b = os.path.basename(path).lower()
    if not b.endswith('.html'):
        return False
    stem = b[:-5].lstrip('_')
    # landing pages: lp_x, x_lp, lp1_main, lpshot_, *_lp_v2
    if re.match(r'^lp[\d_]', stem) or re.search(r'(^|_)lp(\d+)?(_|$)', stem):
        return False
    if stem.startswith(('index', 'preview', 'qa', 'readme', 'contact', 'sheet', 'grid')):
        return False
    if any(k in stem for k in ('landing', 'lpshot', 'review', 'report', 'pack', 'handoff',
                               'audit', 'dashboard', 'checkout')):
        return False
    # scraped/research captures keep their source domain in the filename
    if re.search(r'(_com_|_in_|https?_|www_|ambitionbox|glassdoor|naukri|indeed)', stem):
        return False
    # Structural test — the filename heuristics above still let ad_copy / anchor-text /
    # evidence-bank documents through. A hand-built static always has a call-out element and a
    # 1080-wide canvas; a document has neither. This is what actually separates them.
    try:
        head = open(path, encoding='utf-8', errors='ignore').read(20000)
    except OSError:
        return False
    has_callout = re.search(r'class=["\']?(callout|band|kicker|kick|elig|head)\b', head, re.I)
    has_canvas = re.search(r'\b1080(px)?\b', head)
    return bool(has_callout and has_canvas)


# --------------------------------------------------------------------------- kit-level
def kit_copy_checks(kit_dir, creatives):
    """C21 (primary text length) and K1 (anchor entry present) from ad_copy*.md.

    Returns {creative_stem: [(level, code, msg)]} plus a list of kit-wide issues.
    """
    per_ad, kit_wide = {}, []
    copies = [f for f in os.listdir(kit_dir)
              if re.match(r'ad_copy.*\.md$', f, re.I)] if os.path.isdir(kit_dir) else []
    # Kits that keep their render sources in html/ resolve kit_dir to that subfolder, so
    # ad_copy.md sits one level up and K1/C21 never ran at all — they reported the WARN
    # below, which reads like "checked, nothing to say". Look up one level before giving
    # up. Found 25 Aug 2026 on womens_ai_bootcamp_5-7Sep, whose 32 ads had never been
    # anchor-checked. This can only make the two checks run where they previously did
    # not; it cannot reject anything the archive approved.
    if not copies and os.path.isdir(kit_dir):
        up = os.path.dirname(os.path.abspath(kit_dir))
        if os.path.isdir(up):
            found = [f for f in os.listdir(up) if re.match(r'ad_copy.*\.md$', f, re.I)]
            if found:
                kit_dir, copies = up, found
    if not copies:
        kit_wide.append(('WARN', 'K1',
                         'no ad_copy*.md in the kit — anchor text could not be checked. '
                         'Every ad ships with paste-ready primary text, headline and description.'))
        return per_ad, kit_wide

    text = ''
    for c in copies:
        text += open(os.path.join(kit_dir, c), encoding='utf-8').read() + '\n'

    # Split into per-ad blocks on markdown headings, then match blocks to creative stems.
    blocks = re.split(r'\n(?=#{1,4}\s)', text)
    for stem in creatives:
        keys = [re.sub(r'[^a-z0-9]+', '', v.lower()) for v in stem_variants(stem)]
        keys = [k for k in keys if len(k) >= 4]
        block = next((b for b in blocks
                      if any(k in re.sub(r'[^a-z0-9]+', '', b.lower()) for k in keys)), None)
        if block is None:
            per_ad.setdefault(stem, []).append(
                ('FAIL', 'K1', f'no anchor-text entry found for "{stem}" in ad_copy*.md — '
                               'every ad ships with primary text, headline and description.'))
            continue
        # C21 — primary text length. >600 chars ran at 2.15x product-median cost.
        body = re.sub(r'^#{1,4}.*$', '', block, flags=re.M)
        # The colon sits INSIDE the bold in every kit we ship ("**Headline:** ..."), so the old
        # `\*\*(headline|description)\*\*` never matched and C21 measured primary text PLUS the
        # headline, the description and the landing-page path — roughly 150 chars of overcount,
        # enough to push a compliant 519-char primary over the 600 line. A page path is not
        # primary text either. This only ever lowers the fire rate, so it cannot reject
        # anything the archive approved.
        body = re.sub(r'\*\*(headline|description|page):?\*\*.*$', '', body,
                      flags=re.M | re.I)
        n = len(body.strip())
        if n > 900:
            per_ad.setdefault(stem, []).append(
                ('FAIL', 'C21', f'anchor copy for "{stem}" is ~{n} chars. Primary text over 600 '
                                'chars ran at 2.15x product-median cost in the pooled sample.'))
        elif n > 600:
            per_ad.setdefault(stem, []).append(
                ('WARN', 'C21', f'anchor copy for "{stem}" is ~{n} chars — trim toward 600.'))
    return per_ad, kit_wide


# --------------------------------------------------------------------------- judging
def judge_one(html, extra=(), product_flags=()):
    """Run every Gate 0 checker against one creative. Returns a verdict dict."""
    issues = []

    out, _ = run([sys.executable, os.path.join(HERE, 'ad_lint.py'),
                  *product_flags, html])
    issues += parse_issues(out)

    png = png_for(html)
    if png:
        # Exit-code contract for the pixel checkers: 0 = clean, 1 = real defect, anything else
        # (2 = missing Pillow, -1 = checker absent or crashed) = the check never ran. Those are
        # different facts and must not share a verdict. Before this split, no-Pillow made
        # crop_qa exit 1 and every creative picked up a phantom X1 BLOCK, while ad_render_qa
        # exited 2 and vanished without a word — a silent hole exactly where the pixel gate is.
        out, code = run([sys.executable, os.path.join(HERE, 'ad_render_qa.py'), png])
        if code in (0, 1):
            issues += parse_issues(out)
        else:
            issues.append(('WARN', 'E9', f'ad_render_qa.py could not run (exit {code}) — '
                                         'clipping and crop-line checks were NOT performed. '
                                         f'{out.strip().splitlines()[-1] if out.strip() else ""}'))
        out, code = run([sys.executable, os.path.join(HERE, 'crop_qa.py'), png])
        if code == 1:
            issues.append(('FAIL', 'X1',
                           'ink falls inside a band that Meta discards when it centre-crops '
                           'the card to 1:1. Move it inside the crop-safe zone.'))
        elif code != 0:
            issues.append(('WARN', 'E9', f'crop_qa.py could not run (exit {code}) — the '
                                         'square-crop check was NOT performed. '
                                         f'{out.strip().splitlines()[-1] if out.strip() else ""}'))
    else:
        issues.append(('WARN', 'E0',
                       'no rendered PNG found — pixel checks (clipping, crop band, dead band) '
                       'were skipped. Render before handoff.'))

    # Brand is a property of the KIT, not of the file. check_claims.py infers it from the path,
    # and an ICP-named creative inside a SkillArbitrage kit (src_05_lawyers.html in the data
    # privacy kit) trips the "lawyer" hint and gets rejected for correct branding. Resolve it
    # once from the kit directory and pass it explicitly.
    kit_path = os.path.dirname(os.path.abspath(html))
    brand = 'lawsikho' if any(h in kit_path.lower() for h in LAWSIKHO_KITS) else 'skillarbitrage'
    out, code = run([sys.executable, os.path.join(HERE, 'check_claims.py'),
                     '--brand', brand, html])
    if code == 1:
        for line in out.splitlines():
            m = re.search(r'L(\d+):\s*(.*?)\s*->\s*(.*)', line)
            if m:
                issues.append(('FAIL', 'T1', f'{m.group(2)} at line {m.group(1)}: {m.group(3)}'))

    issues += list(extra)
    issues = retro_downgrade(issues, html)

    carousel = 'carousel' in html.lower()
    graded = [(tier(lvl, code, carousel), code, msg) for lvl, code, msg in issues]
    blocks = [g for g in graded if g[0] == 'BLOCK']
    fixes = [g for g in graded if g[0] == 'FIX']
    warns = [g for g in graded if g[0] == 'WARN']

    substantive = [f for f in fixes if f[1] not in STYLE_RULES]
    if blocks:
        verdict, why = VERDICT_REJECT, f'{len(blocks)} blocking defect(s)'
    elif len(substantive) >= 2:
        verdict, why = VERDICT_REJECT, f'{len(substantive)} fixable defects — too many to wave through'
    elif fixes:
        verdict, why = VERDICT_CHANGES, (f'{len(fixes)} fix note(s)' if substantive
                                         else f'{len(fixes)} house-style note(s)')
    else:
        verdict, why = VERDICT_ACCEPT, 'clean on Gate 0'

    return {
        'file': html,
        'png': png,
        'verdict': verdict,
        'reason': why,
        'gate': 0,
        'pending': ['vision (Gate 1)', 'novelty (Gate 2)'] if verdict != VERDICT_REJECT else [],
        'blocks': blocks, 'fixes': fixes, 'warns': warns,
        'rules_fired': sorted({g[1] for g in graded}),
    }


# --------------------------------------------------------------------------- gate 1 (vision)
# Tiering for the vision rules. See ads/creative_judge_rules.md section B.
V_TIERS = {
    'V1': 'BLOCK',   # identity call-out unreadable at 236px
    'V2': 'BLOCK',   # a human in the image is not Indian
    'V3': 'FIX',     # dark background (10-40% costlier)
    'V4': 'BLOCK',   # invisible / cropped / clipped text
    'V5': 'BLOCK',   # dark-on-dark or <4.5:1 body text
    'V6': 'FIX',     # call-out off the optical centre
    'V7': 'FIX',     # caption or hook below the top of frame
    'V8': 'WARN',    # canvas not 1080x1350
    'V9': 'FIX',     # kit does not vary aesthetically
    'V20': 'FIX',    # C20 spine: identity -> problem -> value -> CTA, judged visually
    # V10-V14 added 13 Aug 2026 from Ramanuj's five-point teardown of a women-remote static
    # that the gates had passed ("This ad sucks but the gates caught no real issues").
    'V10': 'FIX',    # headline names the product, not the prize the TG wants
    'V11': 'FIX',    # filler support copy — subtitle adds nothing a buyer needs
    'V12': 'FIX',    # conversion assets (barrier lines, eligibility) styled as fine print
    'V13': 'FIX',    # kicker too small or too close to the 1:1 crop line
    'V14': 'FIX',    # list items are generic filler, not mined from the delivery script
    'V15': 'FIX',    # CTA reads like a deposit; state the full exchange
    'V16': 'FIX',    # call-out is a bare situation, no person in it
}
V_ASKS = {
    'V1': 'Reading ONLY this thumbnail, who is this ad for? If you cannot say, V1 fails.',
    'V2': 'Is every human shown Indian? If there are no humans, V2 passes.',
    'V3': 'Is the background light? A dark background fails V3.',
    'V4': 'Is any text clipped, cut off at an edge, or hidden behind another element?',
    'V5': 'Is any text low-contrast against what sits behind it (dark on dark, grey on cream)?',
    'V6': 'Does the call-out sit in the optical centre, or is it stranded at the top edge?',
    'V7': 'Are the hook and captions at the TOP of the frame rather than the lower third?',
    'V8': 'Is the canvas 4:5 (1080x1350)?',
    'V9': 'Does this look meaningfully different from the other cells in this kit?',
    'V20': 'Does the ad carry all four steps: who it is for, the problem, the value, the CTA? '
           'Step 2, the problem, is the one that usually goes missing.',
    'V10': 'Does the BIGGEST line name the thing the audience wants (the job, the client, the '
           'seat) — or does it name the product ("this bootcamp teaches…")? The prize must be '
           'in the headline itself, never a pronoun pointing back at the kicker.',
    'V11': 'Read every support line and ask what a buyer loses if it is deleted. A subtitle '
           'that restates the obvious ("Remote work means real tasks for real companies") is '
           'filler — conversion-first: every element needs a conversion case.',
    'V12': 'Are the barrier-removal and eligibility lines ("No degree. No experience letter.") '
           'set large enough to read on a phone — or are they styled as grey fine print? They '
           'are the cheapest-performing pattern in the backtest; they must be legible.',
    'V13': 'Is the kicker LARGE (it should look 2x too big on desktop) and comfortably below '
           'the 1:1 crop line (top ~10% of the frame is discarded in square placements, so it '
           'needs clear margin, not just technical clearance)? Position matters as much as '
           'size: a small top-corner chip is a BLIND SPOT even when legible, and NOTHING that '
           'must be read may sit below the CTA — the CTA is where the scan stops (15 Aug: the '
           'barrier line below the CTA was called a blind spot, not a crop problem). Colour '
           'matters too: a chip whose background is nearly the canvas colour never registers '
           'as a block — and a kicker in much smaller type than the headline directly below it '
           'loses the eye to the headline regardless of contrast (mechanical form: C27).',
    'V14': 'Do the list items read like they came from THIS camp\'s delivery script — specific, '
           'surprising, worth ₹10 each — or could they be pasted into any bootcamp ad? '
           '"Write short, clear emails" is filler; "a chatbot you build yourself, live — your '
           'first work sample" is real. Generic lists fail. AND the list must match the ICP\'s '
           'GOAL TYPE: a job-seeker ICP wants the route to the job ("the 20 skills that land '
           'your first privacy-analyst job, how to clear the interview, how to network"); a '
           'practice-builder ICP wants deliverables and clients. Prescribing artifacts to a '
           'job-seeker is the wrong fix even when the diagnosis (generic list) is right.',
    'V15': 'Does the CTA state the FULL exchange? "Reserve my seat for ₹10" reads like a '
           'deposit with more to pay later. The cure is total-value: "9 hours of training just '
           'for ₹10", "₹10 gets you all 3 days".',
    'V16': 'Is the identity call-out a PERSON in a situation, or a bare situation? "BACK AFTER '
           'A BREAK?" names nobody and was rejected as strange; "WOMEN RETURNING TO WORK" '
           'names the person. If mechanical C23 fired, do not override it as situation-framing '
           'unless a person-noun is in the frame.',
}
THUMB_W = 236          # the size the identity call-out actually has to survive


def build_thumbs(results, kit_dir):
    """Write 236px thumbnails plus a numbered contact sheet for the vision pass."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None, None, 'Pillow not installed — pip3 install --user Pillow'
    out_dir = os.path.join(kit_dir, '.judge_thumbs')
    os.makedirs(out_dir, exist_ok=True)
    thumbs = []
    for r in results:
        if not r['png']:
            continue
        im = Image.open(r['png']).convert('RGB')
        im.thumbnail((THUMB_W, THUMB_W * 4), Image.LANCZOS)
        p = os.path.join(out_dir, os.path.basename(r['png']))
        im.save(p)
        thumbs.append((r['file'], p, im))
    if not thumbs:
        return out_dir, None, 'no rendered PNGs to judge'
    cols = 6
    cw, ch = THUMB_W + 12, max(i.height for _, _, i in thumbs) + 30
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * cw, rows * ch), 'white')
    d = ImageDraw.Draw(sheet)
    for i, (_, _, im) in enumerate(thumbs):
        x, y = (i % cols) * cw + 6, (i // cols) * ch + 24
        sheet.paste(im, (x, y))
        d.text((x, y - 18), f'#{i + 1}', fill='black')
    sheet_path = os.path.join(out_dir, '_contact_sheet.png')
    sheet.save(sheet_path)
    return out_dir, sheet_path, None


def vision_worklist(results, kit_dir):
    """Emit the Gate 1 worklist. The model fills in `verdicts` and feeds it back via
    --vision-verdicts, which merges the answers into the final verdict."""
    out_dir, sheet, err = build_thumbs(results, kit_dir)
    items = []
    for i, r in enumerate(results):
        if not r['png']:
            continue
        items.append({
            'index': len(items) + 1,
            'file': os.path.basename(r['file']),
            'thumb': os.path.join(out_dir, os.path.basename(r['png'])) if out_dir else None,
            'full': r['png'],
        })
    return {
        'kit': os.path.basename(os.path.normpath(kit_dir)),
        'contact_sheet': sheet,
        'error': err,
        'instructions': (
            'Look at the contact sheet at thumbnail size FIRST, then open individual thumbs '
            'only where a call is unclear. For each item answer every V rule with pass/fail '
            'and give who_is_it_for from the thumbnail alone. Do not read the HTML.'),
        'rules': V_ASKS,
        'items': items,
        'verdicts': [],           # <- model fills: [{"file":..., "V1":"pass", ..., "notes":...}]
    }


def merge_vision(results, verdicts):
    """Fold Gate 1 answers into the Gate 0 results and recompute each verdict."""
    by_file = {os.path.basename(r['file']): r for r in results}
    for v in verdicts:
        r = by_file.get(os.path.basename(v.get('file', '')))
        if not r:
            continue
        for code, tier_ in V_TIERS.items():
            if str(v.get(code, 'pass')).lower().startswith('fail'):
                msg = v.get(f'{code}_note') or V_ASKS[code]
                r[{'BLOCK': 'blocks', 'FIX': 'fixes', 'WARN': 'warns'}[tier_]].append(
                    (tier_, code, msg))
        if v.get('who_is_it_for'):
            r['who_is_it_for'] = v['who_is_it_for']
        r['gate'] = 1
        r['pending'] = ['novelty (Gate 2)']
        if r['blocks']:
            r['verdict'], r['reason'] = VERDICT_REJECT, f"{len(r['blocks'])} blocking defect(s)"
        elif len(r['fixes']) >= 2:
            r['verdict'], r['reason'] = VERDICT_REJECT, f"{len(r['fixes'])} fixable defects"
        elif r['fixes']:
            r['verdict'], r['reason'] = VERDICT_CHANGES, '1 fixable defect'
        else:
            r['verdict'], r['reason'] = VERDICT_ACCEPT, 'clean on Gate 0 + Gate 1'
        r['rules_fired'] = sorted({g[1] for g in r['blocks'] + r['fixes'] + r['warns']})
    return results


def log_verdicts(results, kit):
    ts = time.strftime('%Y-%m-%dT%H:%M:%S')
    with open(LOG, 'a', encoding='utf-8') as fh:
        for r in results:
            fh.write(json.dumps({
                'ts': ts, 'kit': kit, 'file': os.path.basename(r['file']),
                'gate': 0, 'verdict': r['verdict'], 'reason': r['reason'],
                'rules_fired': r['rules_fired'],
                'n_block': len(r['blocks']), 'n_fix': len(r['fixes']),
                'n_warn': len(r['warns']),
            }, ensure_ascii=False) + '\n')


# --------------------------------------------------------------------------- cli
MARK = {VERDICT_ACCEPT: '✓', VERDICT_CHANGES: '~', VERDICT_REJECT: '✗'}


def main():
    argv = sys.argv[1:]
    as_json = '--json' in argv
    quiet = '--quiet' in argv
    no_log = '--no-log' in argv
    want_vision = '--vision' in argv
    vision_file = None
    if '--vision-verdicts' in argv:
        i = argv.index('--vision-verdicts')
        vision_file = argv[i + 1] if i + 1 < len(argv) else None
        del argv[i:i + 2]
    product_flags = []
    while '--product' in argv:
        i = argv.index('--product')
        product_flags += argv[i:i + 2]
        del argv[i:i + 2]
    argv = [a for a in argv if not a.startswith('--')]
    if not argv:
        print(__doc__)
        return 2

    targets, kit = [], argv[0]
    if len(argv) == 1 and os.path.isdir(argv[0]):
        for f in sorted(os.listdir(argv[0])):
            p = os.path.join(argv[0], f)
            if is_creative(p):
                targets.append(p)
    else:
        targets = [a for a in argv if a.endswith('.html')]
        kit = os.path.dirname(os.path.abspath(targets[0])) if targets else '.'

    if not targets:
        print('no ad HTML found — pass a kit directory or specific .html files')
        return 2

    stems = [os.path.splitext(os.path.basename(t))[0] for t in targets]
    per_ad, kit_wide = kit_copy_checks(kit if os.path.isdir(kit) else os.path.dirname(kit), stems)

    results = []
    for t in targets:
        stem = os.path.splitext(os.path.basename(t))[0]
        results.append(judge_one(t, per_ad.get(stem, []), product_flags))

    kit_dir = kit if os.path.isdir(kit) else os.path.dirname(os.path.abspath(kit))

    if vision_file:
        with open(vision_file, encoding='utf-8') as fh:
            payload = json.load(fh)
        results = merge_vision(results, payload.get('verdicts', payload))

    if want_vision:
        work = vision_worklist(results, kit_dir)
        path = os.path.join(kit_dir, '.judge_thumbs', 'vision_worklist.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(work, fh, ensure_ascii=False, indent=2)
        print(f"Gate 1 worklist: {path}")
        if work['contact_sheet']:
            print(f"Contact sheet:   {work['contact_sheet']}  ({len(work['items'])} creatives)")
        if work['error']:
            print(f"  note: {work['error']}")
        print('Fill in "verdicts" and re-run with '
              f'--vision-verdicts {os.path.relpath(path)}')
        return 0

    if not no_log:
        log_verdicts(results, os.path.basename(os.path.normpath(kit)))

    if as_json:
        print(json.dumps({'kit': kit, 'kit_issues': kit_wide, 'results': results},
                         ensure_ascii=False, indent=2))
    else:
        for lvl, code, msg in kit_wide:
            print(f'[{lvl} {code}] {msg}')
        if kit_wide:
            print()
        for r in results:
            print(f"{MARK[r['verdict']]} {os.path.basename(r['file']):42} {r['verdict']}"
                  f"  ({r['reason']})")
            if not quiet:
                for grp, label in ((r['blocks'], 'BLOCK'), (r['fixes'], 'FIX'), (r['warns'], 'WARN')):
                    for _, code, msg in grp:
                        print(f'     [{label} {code}] {msg}')
        n_rej = sum(1 for r in results if r['verdict'] == VERDICT_REJECT)
        n_chg = sum(1 for r in results if r['verdict'] == VERDICT_CHANGES)
        n_acc = len(results) - n_rej - n_chg
        print(f'\n{len(results)} creative(s): {n_acc} accept, {n_chg} accept-with-changes, '
              f'{n_rej} reject.')
        if n_acc or n_chg:
            print('Gate 0 only. Vision (Gate 1) and novelty (Gate 2) still pending — '
                  'nothing here has been looked at.')
        if not no_log:
            print(f'Logged to {os.path.relpath(LOG)}')

    return 1 if any(r['verdict'] == VERDICT_REJECT for r in results) else 0


if __name__ == '__main__':
    sys.exit(main())
