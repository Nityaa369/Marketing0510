#!/usr/bin/env python3
"""
preflight.py - hard gate for LawSikho / SkillArbitrage ad + landing page work.

Catches the mechanical failures that have actually reached Ramanuj:
dead pay buttons, hedge paragraphs above the CTA, banned copy patterns,
and ads shipped without a landing page.

Usage:
    python preflight.py <kit-folder>
    python preflight.py lp_one.html lp_two.html
    python preflight.py .

Exit code 0 = clean or warnings only. 1 = at least one BLOCKER.

Rules 1, 2 and 3 are gated through each kit's value_props.md: every ad must
name the better job it offers and define its field in one plain sentence, and
that sentence must appear in the first fold of the landing page it points at.
Write that file BEFORE the creative, from an ICP list, for a kit that does not
exist yet. Round one of approval is that file and nothing else:

    python preflight.py --scaffold-from <icp-list.md> <kit-folder>

Or, for a kit already built, scaffold it from the ads that are there:

    python preflight.py --scaffold <kit-folder>

Each block carries a pain_score, five dimensions at 1 to 5, so the ICP list can
be RANKED before anything is built. Print the ranked table - the round-one
deliverable, which needs no ads to exist:

    python preflight.py --shortlist <kit-folder>

The wording itself is still yours to judge. The gate only guarantees a value
proposition was written down and reached the page.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- patterns

# Dead pay buttons. Seen in 99 pages in this folder.
PAY_STUBS = [
    (r"PAYMENT_LINK_PENDING", "pay button is a PAYMENT_LINK_PENDING stub"),
    (r"TODO\(dev\)", "pay button is a TODO(dev) stub"),
    (r"TODO(?!\()", "unresolved TODO left in the page"),
    (r"growthx\.skillarbitra\.ge/f/<slug>", "literal <slug> placeholder never filled in"),
    (r"PAY_URL\s*=\s*[\"']\s*[\"']", "PAY_URL set to an empty string"),
    (r"PAY_URL\s*=\s*[\"']#", "PAY_URL set to a bare anchor"),
]

# Hedges that must never sit above the CTA.
HEDGE = [
    r"not a guarantee",
    r"individual results vary",
    r"results (?:may |can )?vary",
    r"not an independently verified",
    r"company'?s own stated benchmark",
    r"samples are small and the range is wide",
]

# Copy patterns banned outright by the shipped kits.
BANNED = [
    (r"not for you if", 'banned "this is not for you if..." block'),
]

# Legitimate disclaimer context - must never be flagged as a promise.
# "not for you if" is itself banned and reported separately; including it here
# stops one bad block being counted twice.
DISCLAIMER_CONTEXT = re.compile(
    r"what we will not promise|we do not promise|no guaranteed jobs"
    r"|not for you if|we cannot promise|not a promise of"
    # 23 Sep 2026: an FAQ that ASKS the question and answers no is the house position,
    # not a claim. "Does the bootcamp guarantee placements? No. It teaches the sourcing,
    # the pitch and the plan." (HR calendar wave, lp_18) was blocked as a guarantee.
    # CLAUDE.md says saying "no guaranteed jobs" plainly is correct and expected.
    r"|\?\s*(?:</h\d>)?\s*(?:<p>)?\s*(?:No\b|Never\b|We do not\b|We cannot\b)",
    re.I,
)

# Actual guarantee claims (only outside a disclaimer block).
GUARANTEE_CLAIM = re.compile(
    r"(?:we )?guarantee(?:d|s)?\s+(?:you\s+)?(?:a\s+)?(?:job|placement|income|salary)", re.I
)

CTA = re.compile(
    r"reserve my seat|join for\s*₹|sign up|enrol|enroll|book my seat|pay\s*₹",
    re.I,
)

# How far above a CTA a hedge is still "directly above the button".
#
# Calibrated against real pages, not guessed:
#   lp_09_coaching_admissions.html  gap 46   <- the page Ramanuj rejected
#   lp_66_opsmanager.html           gap 508  <- approved and live
#   lp_46_bpo.html                  gap 512  <- approved and live
#
# A hedge qualifying a salary figure is REQUIRED by the standing compliance
# rules. It only becomes a conversion problem when it is the last thing the
# reader sees before the button.
#
# REFITTED 31 Aug 2026 against Ramanuj's approvals and live cost. 250 was set
# from three pages. Measured across every landing page under APPROVED/, it fired
# 72 times, and EVERY false alarm sits at exactly gap 237 - one shared US
# Accounting template. One of those pages is lp_us05_evening.html, whose ad is
# the second-cheapest in the account at Rs 30.55 per lead. So both Ramanuj and
# the money say that page is fine and the rule was wrong.
#
#   gap  46   lp_09_coaching_admissions.html   <- the page Ramanuj REJECTED
#   gap 237   the US Accounting template       <- approved, and Rs 30.55 per lead
#   gap 508   lp_66_opsmanager.html            <- approved and live
#   gap 512   lp_46_bpo.html                   <- approved and live
#
# 120 sits between 46 and 237 with 74 characters of margin below and 117 above,
# which is a far wider separation than 250 ever had.
HEDGE_WINDOW = 120

# Not sales copy: contact sheets and research appendices ship alongside kits.
#
# NARROWED 31 Aug 2026. The pattern was `.*_evidence`, a wildcard whose only
# intended target was `evidence_bank.html` - already matched by its own literal
# alternative, so the wildcard protected nothing. What it did do was silently
# swallow any real landing page whose angle is named "evidence":
# WomenRemote_Wave9's `lp_A1_evidence.html` disappeared from the pairing check,
# which then reported "7 ads but only 6 landing pages" and would have blocked a
# complete kit for a defect that did not exist. A checker that sees fewer files
# than the kit contains is the failure mode check_all.py was written for.
# Repo-wide there is exactly one `evidence_bank.html` and no other `*_evidence`
# file that is not sales copy. Re-ran the selftest after narrowing: unchanged.
SKIP_FILE = re.compile(r"^(index|evidence_bank)\.html$", re.I)


def visible_text(html: str) -> str:
    """Strip script/style/tags so we analyse what a reader actually sees."""
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", html)


def check_page(path: Path):
    """Return (blockers, warnings) for a single HTML file."""
    blockers, warnings = [], []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [f"could not read file: {e}"], []

    text = visible_text(raw)

    # 1. Dead pay button - checked against raw HTML, stubs live in attrs/JS.
    # Embedded images are skipped first: on 30 Sep 2026 all seven Corporate Finance wave 3
    # faces blocked on "TODO" because the base64 of their collage PNG contains "tdoO", which
    # the case-insensitive pattern read as a stub. A stub never lives inside a data: URI.
    stub_scan = re.sub(r"data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=]+", "data:", raw)
    for pattern, msg in PAY_STUBS:
        if re.search(pattern, stub_scan, re.I):
            blockers.append(msg)

    # 2. Hedge paragraph above the CTA.
    cta_positions = [m.start() for m in CTA.finditer(text)]
    if cta_positions:
        for hedge in HEDGE:
            for hm in re.finditer(hedge, text, re.I):
                if any(0 < cta - hm.end() <= HEDGE_WINDOW for cta in cta_positions):
                    snippet = text[hm.start(): hm.start() + 60].strip()
                    snippet = snippet.encode("ascii", "replace").decode("ascii")
                    blockers.append(f'hedge above the CTA: "{snippet}..."')
                    break

    # 3. Banned copy patterns.
    for pattern, msg in BANNED:
        if re.search(pattern, text, re.I):
            blockers.append(msg)

    # 4. Guarantee claims, ignoring legitimate disclaimer blocks.
    for gm in GUARANTEE_CLAIM.finditer(text):
        window = text[max(0, gm.start() - 200): gm.end() + 60]
        if not DISCLAIMER_CONTEXT.search(window):
            blockers.append(f'possible guarantee claim: "{gm.group(0).strip()}"')

    # 5. Em-dashes in visible copy.
    if "—" in text:
        warnings.append(f"em-dash in copy ({text.count(chr(0x2014))}x) - banned in kit copy")

    # 6. Salary figures on the page - legal on an LP, never on an ad face.
    if re.search(r"₹\s*\d+\s*(?:L|Cr|lakh|crore)", text, re.I):
        warnings.append("salary/income figures present - LP only, never on an ad face")

    return blockers, warnings


# Rule 4b - one ad, one page, and the pages must ACTUALLY DIFFER.
#
# Added 31 Aug 2026, from the founder, on the women bootcamp kit he had just
# shipped:
#
#   "if i am showing ads to someone for the women bootcamp, they see different
#    ads, and then they click on it, but the lp is the same over and over again,
#    making them disinterested. so we have to come up with different lps in the
#    same kit"
#
# Rule 4 already said 1 ad = 1 LP, and every kit obeyed it - as separate FILES.
# What nothing measured was whether the files said anything different. Measured
# across every kit in this repo, as median pairwise overlap of whole sentences:
#
#   USParalegal_LawSikho_MediaBuyer_29-31Aug   7 LPs   93%
#   WomenRemote_Wave6_SEND_THIS                6 LPs   90%
#   WomenRemote_Wave8_SEND_THIS               10 LPs   84%   <- the reported kit
#   SeniorAI / ContentWriting / womens_ai     var      81-83%
#   WomenRemote_Wave4_SEND_THIS               28 LPs   77%
#   CorporateFinance_MediaBuyer_15-17Aug       7 LPs   74%
#   WomenRemote_Wave9_LPs_SEND_THIS            7 LPs    1%   <- the model
#
# Wave 8's ten pages carry an IDENTICAL H2 sequence and change only the H1. Wave 9
# gives each page its own argument - a Saturday walkthrough, the case in numbers,
# three career-break stories, a demand board - and overlaps by 1%.
#
# THIS DOES NOT CONTRADICT "do not redesign the page spine". The spine is the
# chassis: ten sections, 1,500-2,000 words, counted lists, sticky CTA. Corporate
# Finance sits at 74% and converts 9.3% to 20.7%, so a shared spine is not what
# costs conversion ON ONE PAGE. The defect is different and is about the READER,
# not the page: one person sees several ads from the same campaign, clicks more
# than one, and lands somewhere they have already read. Keep the spine, change
# the argument inside it.
#
# 80% blocks (the reported failure zone, 84-93%); 65% warns.
LP_SAME_BLOCK = 0.80
LP_SAME_WARN = 0.65


def _page_sentences(path: Path):
    text = visible_text(path.read_text(encoding="utf-8", errors="replace"))
    return {s.strip().lower()
            for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) >= 6}


def check_lp_diversity(folder: Path):
    """Do the landing pages in this kit actually say different things?"""
    findings = []
    lp_dir = folder / "landing_pages"
    if not lp_dir.is_dir():
        return findings
    pages = [p for p in sorted(lp_dir.glob("*.html")) if not SKIP_FILE.match(p.name)]
    if len(pages) < 3:
        return findings
    sets = [(p.name, _page_sentences(p)) for p in pages]
    sims, worst = [], (0.0, "", "")
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            a, b = sets[i][1], sets[j][1]
            if not a or not b:
                continue
            s = len(a & b) / float(len(a | b))
            sims.append(s)
            if s > worst[0]:
                worst = (s, sets[i][0], sets[j][0])
    if not sims:
        return findings
    sims.sort()
    med = sims[len(sims) // 2]
    if med >= LP_SAME_BLOCK:
        findings.append(
            "BLOCKER  the %d landing pages are %.0f%% the same, sentence for sentence "
            "(worst pair %.0f%%: %s / %s). A reader who clicks two ads from this "
            "campaign lands on a page she has already read. Keep the spine, change "
            "the argument: give each page its own case, the way "
            "WomenRemote_Wave9 does at 1%%."
            % (len(pages), 100 * med, 100 * worst[0], worst[1], worst[2]))
    elif med >= LP_SAME_WARN:
        findings.append(
            "WARNING  the %d landing pages are %.0f%% the same, sentence for sentence. "
            "Under 80%% so it does not block, but check the argument really differs "
            "per ad and not just the headline." % (len(pages), 100 * med))
    return findings


MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
          "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}

# Kit folders carry the camp dates: ..._17-19Oct, ..._5-7Sep, ..._22-24Aug.
# Not anchored to the end: the shipped copy is ..._17-19Oct_SEND_THIS, and that
# is the folder that actually gets sent, so it must be readable too.
CAMP_DATES = re.compile(r"(\d{1,2})-(\d{1,2})([A-Z][a-z]{2})(?![a-z])")


def camp_is_ahead(name: str, as_of: str) -> bool:
    """
    Is this kit's camp still in the future, as of the extract's own end date?

    Folder names carry no year, so the year is inferred by nearest wrap: a month
    more than six ahead of `as_of` is last year, more than six behind it is next
    year. Without that second half a January kit read as ten months past instead
    of two months ahead. Unparseable name means we do not know, and a rule that
    does not know says nothing - returns False.
    """
    matches = CAMP_DATES.findall(name)
    if not matches:
        return False
    try:
        y, mo, d = int(as_of[:4]), int(as_of[5:7]), int(as_of[8:10])
    except (ValueError, IndexError):
        return False
    _, last, mon = matches[-1]
    month = MONTHS.get(mon.lower())
    if not month:
        return False
    year = y
    if month - mo > 6:
        year -= 1
    elif mo - month > 6:
        year += 1
    return (year, month, int(last)) > (y, mo, d)


def check_funnel_slugs(folder: Path):
    """
    Rule 5 asks whether the page can actually take money. PAY_STUBS only answers
    the syntactic half - TODO, href="#", a literal <slug>. A slug that is spelled
    correctly but was never created in GrowthX passes every one of those and still
    cannot take a rupee.

    Measured 21 Sep 2026 on the CorporateFinance Notify 17-19 Oct wave: 19 pages,
    0 dead stubs, preflight clean - and 0 of the 19 cf-oct-* funnels existed. The
    browser returned "Funnel not found." for every one. The sibling October kits
    shipped the same week were not in that state (USAccounting_Search 18 of 21
    live, IndependentDirector_Chat 13 of 18), so this is a real gap in one wave,
    not the normal pre-launch condition.

    What the extract can and cannot say. funnels_*.json is a get_leads_report
    pull over a LEADS WINDOW (funnels_2026-09-21.json covers 8-21 Sep), not a
    registry of every funnel that exists. A funnel with no leads in that window
    is absent from it whether or not it exists, so absence is a HINT, never
    proof - the first cut of this rule ignored that and fired on 16 of 51 kits,
    most of them August and September camps whose funnels were live at the time.

    So the rule only speaks where absence is actually informative: a kit whose
    camp is still ahead, which by launch needs a funnel taking traffic. Past
    kits stay silent. WARNING, never BLOCKER - slugs are legitimately created
    after a kit is built, and the browser is the only test that settles it.

    Silent when no extract is on disk - absence of the file is not evidence.
    """
    findings = []
    lp_dir = folder / "landing_pages"
    if not lp_dir.is_dir():
        return findings

    extracts = sorted(Path(folder.parent).glob("funnels_2*.json"))
    if not extracts:
        return findings
    try:
        data = json.loads(extracts[-1].read_text(encoding="utf-8"))
        live = {r.get("slug") for r in data.get("byFunnel", []) if r.get("slug")}
        window_to = (data.get("_window") or {}).get("to", "")
    except Exception:
        return findings
    if not live or not window_to:
        return findings

    # Only speak about a camp that has not run yet. For anything already past,
    # absence from a 14-day leads window says nothing at all.
    if not camp_is_ahead(folder.name, window_to):
        return findings

    used = set()
    for p in sorted(lp_dir.glob("*.html")):
        if SKIP_FILE.match(p.name):
            continue
        used |= set(re.findall(r"growthx\.skillarbitra\.ge/f/([a-z0-9-]+)",
                               p.read_text(encoding="utf-8", errors="replace")))
    if not used:
        return findings

    missing = sorted(s for s in used if s not in live)
    if not missing:
        return findings

    shown = ", ".join(missing[:6]) + (" ..." if len(missing) > 6 else "")
    findings.append(
        "WARNING  this camp has not run yet and %d of %d funnel slug(s) took no "
        "leads in %s (window to %s): %s. The pay button is well formed, so no "
        "stub check can see this. It is a hint, not proof - a funnel with no "
        "traffic looks identical to one that was never created. Open one in a "
        "browser before any ad points here; curl gives false 404s."
        % (len(missing), len(used), extracts[-1].name, window_to, shown))
    return findings


def check_pairing(folder: Path):
    """
    Every ad needs its own landing page. "But where are the landing pages?"
    was asked twice in one week.

    Kits deliberately use different names on each side (cw_01_types_clients.png
    pairs with lp_cw_01_clients.html) and the authoritative mapping lives in the
    kit README table. So counts are a BLOCKER; name matching is only a hint.
    """
    findings = []
    ads_dir, lp_dir = folder / "ads", folder / "landing_pages"
    if not ads_dir.is_dir():
        return findings

    ads = [p.name for p in ads_dir.iterdir()
           if p.suffix.lower() in (".png", ".jpg", ".jpeg")]
    # A carousel is ONE ad and ONE page, however many cards it has. Added 23 Sep 2026:
    # the Tech Law carousel kit shipped 40 cards for 10 pages and this check read it as
    # "30 ads cannot be launched". Cards are named <stem>_c1..<stem>_cN (SOP/02 fixes
    # card order), so collapse that suffix before counting. A kit of single faces is
    # unaffected: nothing there ends in _c<digit>.
    ads = sorted({re.sub(r"_c\d+(?=\.[^.]+$)", "", n) for n in ads})
    if not ads:
        return findings

    lps = ([p.name for p in lp_dir.glob("*.html") if not SKIP_FILE.match(p.name)]
           if lp_dir.is_dir() else [])

    if not lps:
        findings.append(
            f"BLOCKER  {len(ads)} ads and no landing pages at all - do not hand over"
        )
        return findings

    if len(lps) < len(ads):
        findings.append(
            f"BLOCKER  {len(ads)} ads but only {len(lps)} landing pages - "
            f"{len(ads) - len(lps)} ad(s) cannot be launched"
        )

    def index(name: str):
        m = re.search(r"(\d+)", Path(name).stem)
        return m.group(1).lstrip("0") or "0" if m else None

    lp_index = {}
    for name in lps:
        lp_index.setdefault(index(name), []).append(name)

    for ad in sorted(ads):
        if index(ad) is not None and index(ad) not in lp_index:
            findings.append(
                f"warning  {ad} has no landing page with a matching number - "
                f"check the README mapping table"
            )
    return findings


# ---------------------------------------------------- value props (Rules 1-3)

# Rules 1 and 2 caused nearly every rejection, and until now nothing checked
# them: they were four sentences you were asked to write at handover. This
# turns them into a gate. Every kit carries a value_props.md, one block per ad:
#
#   ## 01
#   ad: ads/01_ai_discount_chat.png
#   lp: landing_pages/lp_01_ai_discount.html
#   better_job: Decide what the campaign says, and be paid for the number it moves.
#   field_definition: Campaign strategy is choosing what gets written, who it
#     targets and which number it has to move.
#   deliverables: A campaign brief written live | An AI content workflow end to
#     end | A one page results report clients pay for
#
# Run `python preflight.py --scaffold <kit-folder>` to generate the stub.

VALUE_PROPS = "value_props.md"

# Drop an empty .preflight-legacy file in a kit that shipped before this check
# existed. It suppresses the value-prop check for that folder and nothing else.
LEGACY_MARKER = ".preflight-legacy"

# Specs that predate a required field. PER FIELD, because the exempt sets differ:
# on 15 Sep 2026 twelve specs lacked `pain_score` and all THIRTEEN lacked
# `hypothesis`, so one flat list would have to exempt the wrong kit from the wrong
# rule. Format, one per line:
#
#     <kit folder>: pain_score, hypothesis      exempt from those fields
#     <kit folder>                              exempt from every legacy field
#
# NEVER add to this. Both scaffolds write both fields, so a kit that lacks one is a
# kit whose ICP list was never ranked or whose test was never stated.
# `preflight.py --selftest` fails if the entry count grows.
GRANDFATHER_FILE = ".preflight-grandfathered"
GRANDFATHER_BASELINE = 25          # total (kit, field) pairs on the day it landed
LEGACY_FIELDS = ("pain_score", "hypothesis")
SCRIPT_DIR = Path(__file__).resolve().parent


def grandfathered(root: Path, field: str = "pain_score"):
    """Kit folder names exempt from `field`."""
    f = Path(root) / GRANDFATHER_FILE
    if not f.is_file():
        return set()
    out = set()
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        name, _, fields = line.partition(":")
        name = name.strip().rstrip("/\\")
        want = [x.strip() for x in fields.split(",") if x.strip()] or list(LEGACY_FIELDS)
        if field in want:
            out.add(name)
    return out


def grandfather_entries(root: Path):
    """Every (kit, field) exemption, for the selftest's growth check."""
    pairs = set()
    for fld in LEGACY_FIELDS:
        for kit in grandfathered(root, fld):
            pairs.add((kit, fld))
    return pairs

REQUIRED_KEYS = ("better_job", "field_definition", "deliverables", "buying_pressure",
                 "awareness")

# hypothesis is required too, but is checked separately so it can be grandfathered
# per kit - see grandfathered(). Added 15 Sep 2026.
#
# WHY. The account records WHO an ad is for (icp, archetype), WHAT it offers
# (better_job, field_definition), HOW HARD the audience is pressed (buying_pressure,
# pain_score) and WHAT THE READER ALREADY BELIEVES (awareness). It recorded nothing
# about WHAT THE AD IS TESTING. So a verdict came back attached to a face and not to
# a belief, and the wave taught the next wave nothing beyond "that one was rejected".
#
# This is the one idea worth taking from the Meta static-ads doctrine reviewed on
# 15 Sep 2026 (pre-tag every concept: Avatar / Desire / Awareness / Hypothesis).
# Three of its four tags already existed here under other names; Hypothesis did not,
# and it is the one that compounds - a rejection recorded against a stated
# hypothesis is evidence about a belief, which transfers to the next kit. A bare
# REJECTED is not. It pairs directly with `python -m adkit.verdict <kit> --review`.
#
# The rest of that doctrine was rejected: its formats (stat callouts, comparison
# tables) are the pay-chart family at 2.34x par across four product lines, and its
# "Us vs Them" / "stop scrolling if" shapes break Rule 1 and the banned
# disqualification block. Take the scoring, not the shape.
HYPOTHESIS_KEY = "hypothesis"

# A hypothesis is a claim that could turn out to be WRONG. "This will work" and
# "good ad for teachers" cannot fail, so they are not hypotheses and are blocked.
# The shape wanted is: this reader believes X, so showing Y should beat Z.
HYPOTHESIS_MIN_WORDS = 8
HYPOTHESIS_EMPTY = (
    "this will work", "good ad", "should work", "test this", "see how it goes",
    "brand awareness", "general awareness", "tbd", "n/a",
)
HYPOTHESIS_EXAMPLE = ("hypothesis: She reads 'virtual assistant' as junior work, so "
                      "naming the duties she already does should beat naming the title.")

# awareness comes from the RMBC trial in docs/RMBC_BRIEF_ContentWriting_Aug2026.md,
# which is the one thing that comparison found the playbook has no answer for:
# "The awareness spectrum. Three of five ads are structured differently because of it.
# The playbook has no equivalent and TREATS EVERY ICP AS PROBLEM AWARE."
#
# It decides the shape of the ad, not just its words. An unaware reader has to be shown
# the problem before any offer means anything; a solution-aware reader is bored by the
# problem and wants the different unit. Writing hooks before settling this is what
# produces ten variations of one opener.
AWARENESS_LEVELS = ("unaware", "problem", "solution", "product", "most")

AWARENESS_HELP = ("unaware | problem aware | solution aware | product aware | "
                  "most aware")

# buying_pressure answers the question that decides whether an ICP is worth an ad
# at all: why would THIS person spend money and three evenings, now? An ICP with
# no pressure behind it produces a technically compliant ad nobody buys.
# ContentWriting_Neighbours_Reworked_29-31Aug got there first and called the field
# better_job_check, so that name is accepted as an alias rather than orphaned.
PRESSURE_ALIASES = ("buying_pressure", "better_job_check", "pressure")

# A pressure line has to name a force, not a preference. "would like to earn more"
# is not pressure; "paid per filed story by a shrinking employer" is.
PRESSURE_HINTS = (
    r"shrink|declin|contract|freelanc|laid off|layoff|redundan|notice period|"
    r"capped|flat|stagnat|plateau|frozen|no raise|halve|discount|undercut|"
    r"automat|replac|obsolet|last job|no job|unemploy|between jobs|career break|"
    r"returning|maternity|relocat|visa|retir|pension|bench|no growth|"
    r"ceiling|dead end|no promotion|priced out|rate cut|per piece|per word|"
    r"per article|hourly|overtime|night shift|attrition|churn"
    # Legal-practice forces, added 21 Sep 2026 on the LawSikho Data Protection kit.
    # The list above was fitted on non-legal kits and read "fees follow the cause list,
    # so every adjournment moves the income" as naming no force. Each term below is a
    # squeeze in a lawyer's own economics, not a preference.
    # Household and shift-work forces, added 1 Oct 2026 on the Women AI wave 10 kit.
    # The list above was fitted on professional and legal kits: it knows "notice period"
    # and "cause list" and does not know "one salary", "roster" or "unpaid". It flagged
    # 19 of 20 buying_pressure lines on that kit as naming no force, including "A salary
    # stopped and the gap has to be covered now" - which names a force precisely. Every
    # term below is a squeeze in this reader's own economics, not a preference.
    r"|one salary|one income|single income|salary stopped|income stopped|unpaid|"
    r"roster|shift|posting|transfer|drop.?off|pick.?up|school hours|caring|carer|"
    r"return.?to.?office|return date|no second earner|fixed scale|salary scale|"
    r"local rate|one town|no local|left a job|out of work|exam|preparation"
    r"|adjourn|cause list|per form|per filing|per matter|matter at a time|\bcaps\b|"
    r"rises slowly|builds slowly|dries up|irregular|\bthin\b|low[- ]fee|\bqueue\b|"
    r"walks? in|takes? it elsewhere|go(?:es)? elsewhere"
)
# FIT, measured 21 Sep 2026 over all 357 scored pressure lines in the repo: the warning
# fired on 170 (48%) before these terms and 153 (43%) after, and still catches all five
# deliberately weak control lines ("wants to grow", "would like to earn more", "keen to
# upskill"). It is STRUCTURALLY NOISY, not merely under-fitted: most lines that still
# fire name a real force in words this list does not hold - "the stipend is set by a
# circular", "renewed one semester at a time", "the school pay scale is fixed", "the
# wait pays nothing". Every product brings new vocabulary for pressure, so a keyword
# list cannot converge. Whether a line names a force is a judgement, and per CLAUDE.md
# belongs in a checklist marked NOT mechanical. Read a firing warning; do not reword a
# line to satisfy it.

# ---- the scored ICP shortlist (added 4 Sep 2026) --------------------------
#
# Source: the offer-to-campaign algo circulated by Uday Wagh, 21 Aug 2026, which
# scores every candidate pain 1-5 across seven dimensions and RANKS them before a
# word of copy is written. Adopted because ICP selection is the biggest lever in
# this account and buying_pressure - the field carrying it - is one prose line
# with no comparison in it. Forty ICPs arrive as a flat list, twenty get an ad,
# and nothing on the page says which twenty or why.
#
# FIVE of the seven dimensions are kept. The two dropped, and why:
#   recognition      DROPPED - it is the awareness field. Two fields for one
#                    judgement is two places to contradict yourself.
#   differentiation  DROPPED - it is a property of the ad, not of the ICP, so it
#                    cannot honestly be scored before the ad exists. Kit-level
#                    sameness is already gated by LP diversity (Rule 4b) and V9.
#
# NOT FITTED, and it says so in the output. No ICP in this repo has ever been
# scored, so there is no threshold to derive from live cost per lead. The gate is
# therefore mechanical only: it blocks on a malformed, missing or out-of-range
# score and NEVER on a total. The one judgement it makes - warn when reachability
# or fit is 1 or 2 - is from first principles rather than data: an ICP that
# cannot be targeted on Meta, or that this camp does not actually serve, wastes a
# cell whatever the other three columns say. Revisit once scored ICPs have run.
#
# REQUIRED, as of 15 Sep 2026. It was opt-in from 4 Sep, and the census on
# 15 Sep says what opt-in bought: of 13 specs in this repo, 12 carry `awareness`
# and exactly ONE carries `pain_score`. So the step designed to make a round-one
# rejection cost a paragraph was running on 1 kit in 13, while the weak cells kept
# being discovered after the kit was built - which CLAUDE.md prices at ~105,000
# tokens of landing page written for nothing.
#
# Grandfathering is an explicit, auditable LIST rather than a silent absence:
# .preflight-grandfathered at the repo root names the specs that predate the
# requirement. A missing pain_score in any kit NOT on that list is a BLOCKER.
# `--selftest` fails if the list ever grows, so the only way to add a kit to it is
# deliberately, with the selftest baseline moved in the same commit.
#
# Within a spec the old rule still holds: every block or no block, never some.
PAIN_DIMS = ("severity", "frequency", "activation", "reachability", "fit")

PAIN_ABBREV = {
    "severity": "sev(?:erity)?",
    "frequency": "freq(?:uency)?",
    "activation": "act(?:ivation)?",
    "reachability": "reach(?:ability)?",
    "fit": "fit",
}

PAIN_HELP = {
    "severity": "what it costs them - money, standing or time",
    "frequency": "how often it bites - daily, monthly, once a year",
    "activation": "is something forcing the decision NOW, and when",
    "reachability": "can this exact person be targeted on Meta",
    "fit": "does this camp credibly change the outcome for them",
}

PAIN_MAX = 5

# Below this on reachability or fit, the cell is probably wasted. Not fitted.
PAIN_WEAK = 2

PAIN_EXAMPLE = ("pain_score: severity 4 | frequency 5 | activation 4 | "
                "reachability 5 | fit 4")


def parse_pain_score(value: str):
    """Parse 'severity 4 | frequency 5 | ...' into {dim: int}.

    Returns (scores, errors). Forgiving about separators and abbreviations,
    strict about the range, because a 7 out of 5 is a typo that would otherwise
    quietly change a ranking.
    """
    v = re.sub(r"\s+", " ", (value or "").strip())
    if not v or v.upper().startswith("TODO"):
        return {}, ["is missing or still TODO - once one block in a spec is "
                    "scored they all must be, so the ranking is honest"]
    scores, errors = {}, []
    for dim in PAIN_DIMS:
        m = re.search(r"\b" + PAIN_ABBREV[dim] + r"\b\s*[:=]?\s*(\d+)",
                      v, re.I)
        if not m:
            errors.append("has no {} score ({})".format(dim, PAIN_HELP[dim]))
            continue
        n = int(m.group(1))
        if not 1 <= n <= PAIN_MAX:
            errors.append("scores {} at {}, must be 1 to {}".format(
                dim, n, PAIN_MAX))
            continue
        scores[dim] = n
    return scores, errors


# Rule 1. Threat and obligation framing in better_job. Deliberately narrow:
# these fire on one short line the writer composed, so precision beats recall.
# "regulator" on its own is NOT here - an approved DataPrivacy ad used it well
# ("the regulator is still being staffed, everyone starts level").
THREAT = [
    (r"\bnow (?:applies|apply|needs?|requires?|must|have to)\b",
     "tells the reader a rule now lands on them (Rule 1, regulator framing)"),
    (r"\b(?:in breach|non-?compliant|non-?compliance|out of compliance)\b",
     "tells the reader they are in breach (Rule 1)"),
    (r"\byou (?:are|could be|may be|might be|will be) (?:exposed|liable|at risk)\b",
     "puts the reader at risk instead of offering a job (Rule 1)"),
    (r"\b(?:banned|prohibited|illegal|unlawful|penalt(?:y|ies)|fined?|prosecut)\b",
     "leans on penalty or prohibition (Rule 1)"),
    (r"\b(?:one more|another|an extra) (?:form|process|checklist|register|policy)\b",
     "sells more work at the same desk, not a better job (Rule 1)"),
    (r"\b(?:get|gets|getting|be) named\b|\bnamed the person who\b",
     "internal credit for unpaid extra work is a chore, not a career (Rule 1)"),
    (r"\bbefore it(?:'| i)s too late\b|\bdon'?t get caught\b",
     "fear close (Rule 1)"),
    (r"\bAI (?:will|is going to) (?:take|replace|kill)\b|\breplaced by AI\b",
     "AI-fear framing - the argument is a ladder, not a threat"),
]

# Softer Rule 1 case: the same job, done more carefully.
SAME_DESK = [
    r"\bin your current (?:role|job|position)\b",
    r"\bthe same (?:role|job|desk|seat)\b",
    r"\bown the (?:process|form|checklist|policy)\b",
    r"\badd (?:it )?to your (?:existing )?(?:role|remit|responsibilities)\b",
]

# Rule 2 step 4: one sentence defining the field, in ordinary words.
# The approved pattern is definitional - "X is a, b and c" / "X means doing y".
DEFINES = re.compile(r"\b(?:is|are|means|involves)\b", re.I)

STOPWORDS = {
    "that", "this", "with", "from", "your", "what", "when", "they", "them",
    "then", "than", "into", "have", "has", "had", "been", "being", "does",
    "will", "would", "which", "there", "their", "about", "before", "after",
    "you", "and", "the", "for", "not", "but", "are", "its", "own",
}

# How much of the landing page counts as the first fold. LP visible text runs
# to many thousands of characters; the hero is comfortably inside 1500.
FOLD = 1500

# Fraction of the definition's content words that must appear in the fold.
FOLD_OVERLAP = 0.7


def content_words(s: str):
    """Lowercase words of 4+ characters, minus stopwords. Used for fuzzy match."""
    return {w for w in re.findall(r"[a-z]+", s.lower())
            if len(w) > 3 and w not in STOPWORDS}


def parse_value_props(path: Path):
    """Parse value_props.md into {block id: {key: value}}. Values may wrap."""
    blocks, current, key = {}, None, None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        head = re.match(r"^##\s+(\S+)", line)
        if head:
            ident = head.group(1).strip().lstrip("0") or "0"
            current, key = {}, None
            blocks[ident] = current
            continue
        if current is None or line.lstrip().startswith("#"):
            continue
        kv = re.match(r"^\s*([a-z_]+)\s*:\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            current[key] = kv.group(2).strip()
        elif key and line.strip():
            # A wrapped continuation of the previous value.
            current[key] = (current[key] + " " + line.strip()).strip()
    return blocks


def ad_index(name: str):
    m = re.search(r"(\d+)", Path(name).stem)
    return (m.group(1).lstrip("0") or "0") if m else None


AD_SUFFIX = (".png", ".jpg", ".jpeg", ".html")


def ad_files(ads_dir: Path):
    """Ad faces in a kit. Some kits ship PNGs, others HTML rendered later."""
    return sorted(p.name for p in ads_dir.iterdir()
                  if p.suffix.lower() in AD_SUFFIX and not SKIP_FILE.match(p.name))


def value_props_enforced(folder: Path) -> bool:
    """True if the value-prop gate actually applies to this folder."""
    ads_dir = folder / "ads"
    if not ads_dir.is_dir() or (folder / LEGACY_MARKER).exists():
        return False
    return bool(ad_files(ads_dir))


def check_value_props(folder: Path):
    """
    Rules 1, 2 and 3 as a gate rather than a promise.

    Returns a list of finding strings, each prefixed BLOCKER or warning.
    """
    findings = []
    ads_dir = folder / "ads"
    if not value_props_enforced(folder):
        return findings

    ads = ad_files(ads_dir)

    vp_path = folder / VALUE_PROPS
    if not vp_path.is_file():
        return [
            "BLOCKER  no {} - every ad must state the better job it offers "
            "(Rule 1) and the sentence that defines the field (Rule 2). "
            "Run: python preflight.py --scaffold {}".format(VALUE_PROPS, folder)
        ]

    blocks = parse_value_props(vp_path)
    lp_dir = folder / "landing_pages"
    lps = ([p for p in lp_dir.glob("*.html") if not SKIP_FILE.match(p.name)]
           if lp_dir.is_dir() else [])
    lp_by_index = {}
    for p in lps:
        lp_by_index.setdefault(ad_index(p.name), []).append(p)

    levels_seen = []
    # Required since 15 Sep 2026, except for the named specs that predate it.
    # See the PAIN_DIMS comment block for the census that forced the change.
    uses_pain = any(b.get("pain_score") for b in blocks.values())
    exempt = folder.name in grandfathered(SCRIPT_DIR, "pain_score")
    hyp_exempt = folder.name in grandfathered(SCRIPT_DIR, HYPOTHESIS_KEY)
    if not uses_pain and not exempt:
        findings.append(
            "BLOCKER  value_props.md carries no pain_score. The ICP list was never "
            "ranked, so the weak cells only become visible after the kit is built. "
            "Add one line per block: {}  (or scaffold it: python preflight.py "
            "--scaffold-from <icp-list.md> {})".format(PAIN_EXAMPLE, folder.name))
    scored = []

    for ad in ads:
        idx = ad_index(ad)
        if idx is None:
            continue
        block = blocks.get(idx)
        if block is None:
            findings.append("BLOCKER  {} has no block in {}".format(ad, VALUE_PROPS))
            continue

        # accept whichever pressure alias the kit used
        for alias in PRESSURE_ALIASES:
            if block.get(alias) and not block[alias].strip().upper().startswith("TODO"):
                block["buying_pressure"] = block[alias]
                break

        missing = [k for k in REQUIRED_KEYS
                   if not block.get(k) or block[k].strip().upper().startswith("TODO")]
        if missing:
            findings.append(
                "BLOCKER  {} block {} still unfilled: {}".format(
                    VALUE_PROPS, idx, ", ".join(missing))
            )
            continue

        job = block["better_job"]
        definition = block["field_definition"]

        # --- Rule 1: a better job, never a threat and never more of the same.
        if len(job.split()) < 6:
            findings.append(
                'BLOCKER  block {} better_job is too thin to be a job offer: '
                '"{}"'.format(idx, job)
            )
        for pattern, why in THREAT:
            m = re.search(pattern, job, re.I)
            if m:
                findings.append(
                    'BLOCKER  block {} better_job {}: "{}"'.format(idx, why, m.group(0))
                )
        for pattern in SAME_DESK:
            m = re.search(pattern, job, re.I)
            if m:
                findings.append(
                    'warning  block {} better_job reads as the same job done more '
                    'carefully: "{}" (Rule 1)'.format(idx, m.group(0))
                )

        # --- Rule 2 step 4: one plain sentence defining the field.
        if len(definition.split()) < 6:
            findings.append(
                'BLOCKER  block {} field_definition is not a sentence: "{}"'.format(
                    idx, definition)
            )
        elif not DEFINES.search(definition):
            findings.append(
                'BLOCKER  block {} field_definition does not define anything - it '
                'needs an "X is / means ..." sentence: "{}"'.format(idx, definition)
            )

        # --- ICP relevance. Reported directly: "the icps are not that relevant -
        #     who would buy that course, ie would be willing to learn a new skill
        #     or are desperate in some way?" An ad can pass every other rule and
        #     still be aimed at someone with no reason to buy.
        pressure = block["buying_pressure"].strip()
        if len(pressure.split()) < 8:
            findings.append(
                'BLOCKER  block {} buying_pressure is too thin to be a reason to '
                'buy: "{}"'.format(idx, pressure))
        elif not re.search(PRESSURE_HINTS, pressure, re.I):
            findings.append(
                'warning  block {} buying_pressure names no force acting on this '
                'person - what is squeezing them right now? "{}"'.format(
                    idx, pressure[:70]))

        # --- the hypothesis: what this ad is testing, in a form that can be wrong.
        if not hyp_exempt:
            hyp = (block.get(HYPOTHESIS_KEY) or "").strip()
            low = hyp.lower().rstrip(".")
            if not hyp or low.upper().startswith("TODO"):
                findings.append(
                    "BLOCKER  block {} has no {}. Say what this ad is testing, as a "
                    "claim that could be wrong. Example: {}".format(
                        idx, HYPOTHESIS_KEY, HYPOTHESIS_EXAMPLE))
            elif any(low.startswith(e) or low == e for e in HYPOTHESIS_EMPTY):
                findings.append(
                    'BLOCKER  block {} hypothesis "{}" cannot be wrong, so it is not a '
                    'hypothesis. Name the belief you are betting against.'.format(
                        idx, hyp[:50]))
            elif len(hyp.split()) < HYPOTHESIS_MIN_WORDS:
                findings.append(
                    'warning  block {} hypothesis is {} words. A testable one names '
                    'the reader\'s belief AND what you are showing instead: "{}"'
                    .format(idx, len(hyp.split()), hyp[:60]))

        # --- awareness level, and what it forces about the ad's shape.
        aw = block["awareness"].strip()
        level = None
        for cand in AWARENESS_LEVELS:
            if re.match(r"\s*" + cand + r"\b", aw, re.I):
                level = cand
                break
        if level is None:
            findings.append(
                'BLOCKER  block {} awareness must start with one of: {}. Got: "{}"'
                .format(idx, AWARENESS_HELP, aw[:60]))
        else:
            levels_seen.append((idx, level))
            if len(aw.split()) < 6:
                findings.append(
                    'warning  block {} awareness names a level but not what it changes '
                    'about the ad. Say what has to be shown first.'.format(idx))

        # --- the scored ICP row. Ranks the shortlist so the weak cells are
        #     visible in round one, when striking one costs a paragraph.
        if uses_pain:
            pain, pain_errs = parse_pain_score(block.get("pain_score", ""))
            for e in pain_errs:
                findings.append(
                    "BLOCKER  block {} pain_score {}. Format: {}".format(
                        idx, e, PAIN_EXAMPLE))
            if not pain_errs:
                scored.append((idx, sum(pain.values()), pain))
                for dim in ("reachability", "fit"):
                    if pain[dim] <= PAIN_WEAK:
                        findings.append(
                            'warning  block {} scores {} at {}/{} - {}. A cell '
                            'this ICP cannot receive or the camp cannot serve is '
                            'spent whatever the rest of the row says.'.format(
                                idx, dim, pain[dim], PAIN_MAX, PAIN_HELP[dim]))

        # --- Rule 2 step 5: three or four named deliverables.
        items = [d.strip() for d in block["deliverables"].split("|") if d.strip()]
        if len(items) < 3:
            findings.append(
                "BLOCKER  block {} lists {} deliverable(s), needs 3 or 4 named "
                "ones (Rule 2, step 5)".format(idx, len(items))
            )

        # --- Rule 3: the LP first fold repeats the definition, in the same words.
        lp_path = None
        if block.get("lp") and not block["lp"].strip().upper().startswith("TODO"):
            candidate = folder / block["lp"]
            if candidate.is_file():
                lp_path = candidate
            else:
                findings.append(
                    "BLOCKER  block {} names lp: {} - no such file".format(
                        idx, block["lp"])
                )
                continue
        else:
            matches = lp_by_index.get(idx, [])
            if len(matches) == 1:
                lp_path = matches[0]
            elif not matches:
                continue  # the pairing check already blocks on a missing LP
            else:
                findings.append(
                    "warning  block {} matches {} landing pages - add an explicit "
                    "lp: line so Rule 3 can be checked".format(idx, len(matches))
                )
                continue

        page = visible_text(lp_path.read_text(encoding="utf-8", errors="replace"))
        fold, whole = page[:FOLD].lower(), page.lower()
        want = re.sub(r"\s+", " ", definition.strip().rstrip(".")).lower()

        if want in fold:
            continue

        words = content_words(definition)
        if not words:
            continue
        in_fold = len(words & content_words(fold)) / len(words)
        in_page = len(words & content_words(whole)) / len(words)

        if in_fold >= FOLD_OVERLAP:
            findings.append(
                "warning  {} first fold paraphrases the definition instead of "
                "repeating it - Rule 3 asks for the same words".format(lp_path.name)
            )
        elif want in whole or in_page >= FOLD_OVERLAP:
            findings.append(
                "BLOCKER  {} defines the field further down the page, not in the "
                "first fold - a reader who clicked must land on it (Rule 3)".format(
                    lp_path.name)
            )
        else:
            findings.append(
                "BLOCKER  {} never states what the field is - the value "
                "proposition is missing from the page (Rules 2 and 3)".format(
                    lp_path.name)
            )

    stray = set(blocks) - {ad_index(a) for a in ads}
    for idx in sorted(stray):
        findings.append(
            "warning  {} block {} has no matching ad in ads/".format(VALUE_PROPS, idx)
        )

    # --- the aggregate. One kit, one awareness level, is the failure the RMBC trial
    #     diagnosed: "the playbook has no equivalent and treats every ICP as problem
    #     aware." Twenty ads all pitched at problem-aware readers is twenty ads with
    #     the same shape, which is what makes a wave feel repetitive at review.
    if len(levels_seen) >= 4:
        distinct = {lv for _, lv in levels_seen}
        if len(distinct) == 1:
            findings.append(
                "warning  all {} blocks are '{}' aware. That is the failure the RMBC "
                "comparison named - every ad ends up the same shape. An unaware reader "
                "needs the problem shown before any offer lands; a solution-aware "
                "reader is bored by the problem and wants the different unit.".format(
                    len(levels_seen), levels_seen[0][1]))

    # --- the ranking itself. Advisory, never a blocker: no scored ICP has run
    #     yet, so a total has no fitted meaning. What it does is make the bottom
    #     of the shortlist visible instead of letting every ICP on a list get an
    #     ad by default.
    if len(scored) >= 3:
        ranked = sorted(scored, key=lambda r: (-r[1], r[0]))
        cut = ranked[(len(ranked) * 2 + 2) // 3:]
        if cut and cut[0][1] < ranked[0][1]:
            findings.append(
                "warning  weakest {} of {} scored ICPs: {}. Strike these first if "
                "the wave has to shrink - see python preflight.py --shortlist {}"
                .format(len(cut), len(ranked),
                        ", ".join("{} ({}/{})".format(
                            i, t, PAIN_MAX * len(PAIN_DIMS)) for i, t, _ in cut),
                        folder))

    return findings


def shortlist(folder: Path):
    """Print the ranked ICP shortlist for a spec - the round-one deliverable.

    Runs on value_props.md alone, so it works the moment --scaffold-from has
    written the spec and BEFORE any ad, palette or landing page exists. That is
    the point: this is the table Ramanuj strikes lines from, and a rejection
    here costs a paragraph rather than a kit.
    """
    path = folder / VALUE_PROPS
    if not path.is_file():
        print("{} has no {}. Run: python preflight.py --scaffold-from "
              "<icp-list.md> {}".format(folder, VALUE_PROPS, folder))
        return 1

    blocks = parse_value_props(path)
    rows, unscored = [], []
    for idx, block in blocks.items():
        label = block.get("icp") or block.get("better_job", "")
        pain, errs = parse_pain_score(block.get("pain_score", ""))
        if errs:
            unscored.append((idx, label, errs[0]))
        else:
            rows.append((idx, label, sum(pain.values()), pain))

    if not rows and not unscored:
        print("{} carries no pain_score lines. This spec predates the scored "
              "shortlist, so there is nothing to rank.".format(path))
        return 0

    width = min(max(max([len(r[1]) for r in rows + unscored] or [12]), 12), 44)
    head = "  ".join(d[:4].upper().ljust(4) for d in PAIN_DIMS)
    top = PAIN_MAX * len(PAIN_DIMS)
    print("\nScored ICP shortlist - {}".format(folder.name))
    print("Ranked on severity + frequency + activation + reachability + fit,")
    print("each 1 to {}. NOT fitted against live cost: no scored ICP has run yet."
          .format(PAIN_MAX))
    print("Use it to decide what to BUILD, not to predict what will convert.\n")
    print("  {}  {}  {}  {}".format("ID".ljust(4), "ICP".ljust(width),
                                    "TOT".rjust(5), head))
    print("  " + "-" * (4 + 2 + width + 2 + 5 + 2 + len(head)))
    for idx, label, total, pain in sorted(rows, key=lambda r: (-r[2], r[0])):
        weak = [d for d in ("reachability", "fit") if pain[d] <= PAIN_WEAK]
        print("  {}  {}  {}  {}{}".format(
            idx.ljust(4), label[:width].ljust(width),
            "{}/{}".format(total, top).rjust(5),
            "  ".join(str(pain[d]).ljust(4) for d in PAIN_DIMS),
            "  <- weak " + "/".join(weak) if weak else ""))
    for idx, label, why in unscored:
        print("  {}  {}  {}  {}".format(
            idx.ljust(4), label[:width].ljust(width), "-".rjust(5), why))
    if unscored:
        print("\n  {} block(s) unscored. Format: {}".format(
            len(unscored), PAIN_EXAMPLE))
    print("\nSend THIS TABLE for round one. Strike the rows that are wrong, then")
    print("build only what survived.")
    return 0


def scaffold(folder: Path):
    """Write a value_props.md stub from whatever is already in the kit."""
    ads_dir, lp_dir = folder / "ads", folder / "landing_pages"
    if not ads_dir.is_dir():
        print("{} has no ads/ - nothing to scaffold.".format(folder))
        return 1
    out = folder / VALUE_PROPS
    if out.exists():
        print("{} already exists - not overwriting.".format(out))
        return 1

    lp_by_index = {}
    if lp_dir.is_dir():
        for p in sorted(lp_dir.glob("*.html")):
            if not SKIP_FILE.match(p.name):
                lp_by_index.setdefault(ad_index(p.name), []).append(p)

    lines = [
        "# Value props - {}".format(folder.name),
        "",
        "One block per ad. preflight.py BLOCKS on anything left as TODO.",
        "",
        "  better_job        the different and better job this ad offers (Rule 1).",
        "                    Never a rule that now applies to them, never one more",
        "                    form, never internal credit for unpaid extra work.",
        "  field_definition  one sentence, ordinary words, saying what the field IS",
        "                    (Rule 2 step 4). This same sentence must appear in the",
        "                    landing page first fold (Rule 3).",
        "  deliverables      three or four named, concrete things, separated by |",
        "  buying_pressure   why THIS person pays and shows up, now. Name the force:",
        "                    a shrinking employer, a frozen rate, a career break, a",
        "                    notice period, a ceiling. Not 'wants to grow'.",
        "  hypothesis        what this ad TESTS, as a claim that could be wrong.",
        "                    Name the belief you are betting against.",
        "  awareness         one of: unaware | problem aware | solution aware |",
        "                    product aware | most aware, THEN what it changes about",
        "                    the ad. Unaware readers must be shown the problem before",
        "                    any offer lands. Solution aware readers are bored by the",
        "                    problem and want the different unit. From the RMBC trial:",
        "                    treating every ICP as problem aware gives a kit one shape.",
        "  pain_score        five dimensions, each 1 to 5, so the shortlist can be",
        "                    RANKED instead of every ICP on a list getting an ad:",
        "                      severity      what it costs them - money, standing, time",
        "                      frequency     how often it bites",
        "                      activation    is something forcing the decision NOW",
        "                      reachability  can this exact person be targeted on Meta",
        "                      fit           does this camp change the outcome for them",
        "                    Not fitted against live cost - it decides what to BUILD,",
        "                    not what will convert. See --shortlist.",
        "",
    ]
    ads = ad_files(ads_dir)
    for ad in ads:
        idx = ad_index(ad) or "?"
        matches = lp_by_index.get(idx, [])
        lp = "landing_pages/" + matches[0].name if len(matches) == 1 else "TODO"
        lines += [
            "## " + idx.zfill(2),
            "ad: ads/" + ad,
            "lp: " + lp,
            "better_job: TODO",
            "field_definition: TODO",
            "deliverables: TODO | TODO | TODO",
            "buying_pressure: TODO",
            "hypothesis: TODO - what is this ad testing? A claim that could be wrong.",
            "awareness: TODO",
            "pain_score: severity ? | frequency ? | activation ? | "
            "reachability ? | fit ?",
            "",
        ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote {} with {} blocks. Fill every TODO, then re-run preflight.".format(
        out, len(ads)))
    return 0


# ---------------------------------------------------------------------------
# scaffold-from: the spec BEFORE the creative
# ---------------------------------------------------------------------------
#
# scaffold() reads a value_props.md out of ads that already exist, which makes
# the wrong order the easy one. CLAUDE.md asks for the opposite: "Write this
# file before the creative, not after it... one wrong line throws away a whole
# kit." This does that. Point it at any list of ICPs and it writes the spec for
# a kit that has not been built yet, so round one of approval costs a paragraph
# per ICP instead of an ad plus a landing page per ICP.
#
#   python preflight.py --scaffold-from docs/ICPs_40_ContentWriting.md MyKit_5Sep
#
# It accepts any of these as an ICP line, which covers every list in this repo:
#   ## 12 Technical writers        | - Technical writers
#   12. Technical writers          | | 12 | Technical writers | ... |
# Everything else is ignored.

# Form 1, the house format, and the one to prefer. docs/ICPs_40_ContentWriting.md:
#   1. **rate-frozen-three-years** - Rs 1.50 a word in 2023, Rs 1.50 a word today.
# The trailing description is the gold. It usually already states the pressure, so it
# is carried into the block as a source note rather than thrown away.
ICP_BOLD = re.compile(
    r"^\s*(\d{1,3})[.)]\s*\*\*(.+?)\*\*\s*(?:[-—–:]\s*(.*))?$")

# Form 2, plainer lists: "- Technical writers", "12. Technical writers",
# "## 12 Technical writers", "| 12 | Technical writers | ... |"
ICP_PLAIN = re.compile(
    r"^\s*(?:\|\s*)?(?:#{2,}\s*)?(?:(\d{1,3})[.)\s|]+)?"
    r"(?:[-*+]\s*)?\*{0,2}([A-Za-z][^|]{2,60}?)\*{0,2}\s*(?:\||$)")

# Section headers, prose and table furniture that would otherwise read as ICPs.
ICP_NOISE = re.compile(
    r"^(?:the |a |an )?(?:icp|icps|role|roles|segment|segments|audience|name|"
    r"notes?|status|wave|waves|total|summary|contents|table|column|index|"
    r"offer|family|families|existing|sharpens|built|funnel|rule)", re.I)

# "A - The unit of sale is the problem (1-8)" is a family header, not an ICP.
ICP_FAMILY = re.compile(r"^[A-Z]\s*[·•\-—]\s")


def parse_icps(path: Path):
    """Returns [(index, label, source_note)] in file order. Deliberately forgiving,
    because every ICP list in this repo is formatted a little differently."""
    out, seen = [], set()
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    # One pass for the house format. If the file uses it at all, trust it alone:
    # letting the loose parser near these files only ever adds prose.
    bold = []
    for raw in lines:
        m = ICP_BOLD.match(raw.rstrip())
        if not m:
            continue
        label = re.sub(r"\s+", " ", m.group(2)).strip()
        if label.lower() in seen:
            continue
        seen.add(label.lower())
        note = re.sub(r"\s+", " ", (m.group(3) or "")).strip()
        bold.append((m.group(1), label, note))
    if bold:
        return bold

    for raw in lines:
        line = raw.rstrip()
        if not line or line.lstrip().startswith(("#!", "```", "---", "===", ">")):
            continue
        if line.lstrip().startswith("#") and not re.match(r"^\s*#{2,}\s*\d", line):
            continue
        m = ICP_PLAIN.match(line)
        if not m:
            continue
        label = re.sub(r"\s+", " ", m.group(2)).strip(" .:-*")
        if not label or ICP_NOISE.match(label) or ICP_FAMILY.match(label):
            continue
        if label.lower() in seen or len(label.split()) > 9:
            continue
        seen.add(label.lower())
        out.append((m.group(1), label, ""))
    return out


def scaffold_from(icp_file: Path, folder: Path):
    if not icp_file.is_file():
        print("No such ICP list: {}".format(icp_file))
        return 1
    icps = parse_icps(icp_file)
    if not icps:
        print("Found no ICP lines in {}. Expected '## 12 Technical writers', "
              "'- Technical writers', '12. Technical writers' or a table row."
              .format(icp_file))
        return 1

    out = folder / VALUE_PROPS
    if out.exists():
        print("{} already exists - not overwriting.".format(out))
        return 1
    folder.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Value props - {}".format(folder.name),
        "",
        "Written BEFORE the creative, per CLAUDE.md. {} ICPs read from {}."
        .format(len(icps), icp_file.name),
        "",
        "Round one of approval is THIS FILE and nothing else. No ad face, no",
        "landing page, no palette. Strike the blocks that are wrong, then build",
        "only what survived. A rejection here costs a paragraph; the same",
        "rejection after the kit is built costs the kit.",
        "",
        "  better_job        the different and better job this ad offers (Rule 1).",
        "                    Never a rule that now applies to them, never one more",
        "                    form, never internal credit for unpaid extra work.",
        "  field_definition  one sentence, ordinary words, saying what the field IS",
        "                    (Rule 2 step 4). This same sentence must appear in the",
        "                    landing page first fold (Rule 3).",
        "  deliverables      three or four named, concrete things, separated by |",
        "  buying_pressure   why THIS person pays and shows up, now. Name the force:",
        "                    a shrinking employer, a frozen rate, a career break, a",
        "                    notice period, a ceiling. Not 'wants to grow'.",
        "  hypothesis        what this ad TESTS, as a claim that could be wrong.",
        "                    Name the belief you are betting against.",
        "  awareness         one of: unaware | problem aware | solution aware |",
        "                    product aware | most aware, THEN what it changes about",
        "                    the ad. Unaware readers must be shown the problem before",
        "                    any offer lands. Solution aware readers are bored by the",
        "                    problem and want the different unit. From the RMBC trial:",
        "                    treating every ICP as problem aware gives a kit one shape.",
        "  pain_score        five dimensions, each 1 to 5, so the shortlist can be",
        "                    RANKED instead of every ICP on a list getting an ad:",
        "                      severity      what it costs them - money, standing, time",
        "                      frequency     how often it bites",
        "                      activation    is something forcing the decision NOW",
        "                      reachability  can this exact person be targeted on Meta",
        "                      fit           does this camp change the outcome for them",
        "                    Not fitted against live cost - it decides what to BUILD,",
        "                    not what will convert. See --shortlist.",
        "",
        "ad: and lp: stay TODO until the spec is approved. That is the point.",
        "",
    ]
    for n, (idx, label, note) in enumerate(icps, start=1):
        lines += [
            "## {}".format((idx or str(n)).zfill(2)),
            # A real key, not a comment: --shortlist prints it as the row label,
            # so the ranked table names the ICP rather than an index.
            "icp: {}".format(label),
        ]
        if note:
            # The list's own description is usually where the pressure already is.
            # Left in as a comment so buying_pressure gets written from evidence
            # rather than invented at the keyboard.
            lines.append("# from the list: {}".format(note))
        lines += [
            "ad: TODO",
            "lp: TODO",
            "better_job: TODO",
            "field_definition: TODO",
            "deliverables: TODO | TODO | TODO",
            "buying_pressure: TODO",
            "hypothesis: TODO - what is this ad testing? A claim that could be wrong.",
            "awareness: TODO",
            "pain_score: severity ? | frequency ? | activation ? | "
            "reachability ? | fit ?",
            "",
        ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote {} with {} ICP blocks, no ads required.".format(out, len(icps)))
    print("Fill every TODO, send THIS FILE for approval, then build what survives.")
    return 0


def selftest():
    """Fit against RAMANUJ'S APPROVALS and against live cost, 31 Aug 2026.

    Same basis and same conflict rule as hook_rules.py and simplicity.py: where a
    rule disagrees with a face Ramanuj approved or an ad that ran cheaply, the
    face wins.

    preflight differs from those two in one important way, and it is why most of
    its blockers on approved work are KEPT: it checks WIRING and COMPLIANCE, not
    taste. Ramanuj approving a creative says nothing about whether its pay button
    works. A dead button on an approved page is a real defect, and CAMPAIGN_MAP.md
    records those as disclosed, not discovered.
    """
    root = Path(__file__).parent / "APPROVED"
    if not root.is_dir():
        print("  APPROVED/ not found - nothing to fit against.")
        return 2
    kits = [d for d in sorted(root.iterdir()) if d.is_dir()]
    counts = {}
    for k in kits:
        found = []
        for f in sorted(k.rglob("lp_*.html")):
            if SKIP_FILE.match(f.name):
                continue
            b, _ = check_page(f)
            found += b
        for b in found:
            key = re.sub(r"[\"'].*", "", b).strip()[:46]
            counts[key] = counts.get(key, 0) + 1
    print("  BLOCKERS on landing pages Ramanuj approved:")
    for k in sorted(counts, key=lambda x: -counts[x]):
        verdict = ("REAL - approving a creative does not wire its button"
                   if "pay" in k.lower() or "TODO" in k or "PAY_URL" in k
                   else "CHECK - a rule firing on approved work is suspect")
        print("    %4d  %-46s %s" % (counts[k], k, verdict))
    if not counts:
        print("    none")
    print("")
    print("  The hedge rule was refitted here: it fired 72 times on approved pages,")
    print("  every one at gap 237 - a single US Accounting template, one of whose")
    print("  pages carries the Rs 30.55 ad. The rejected page sat at gap 46, so the")
    print("  window moved from 250 to 120 and those 72 are gone.")
    print("")
    print("  LP DIVERSITY across every kit in the repo (Rule 4b, added 31 Aug 2026):")
    rows = []
    for d in sorted(Path(__file__).parent.glob("*/")):
        f = check_lp_diversity(d)
        if f:
            rows.append((d.name, f[0].split()[0], f[0]))
    for name, sev, msg in rows[:14]:
        pct = re.search(r"are (\d+)% the same", msg)
        print("    %-8s %-46s %s" % (sev, name[:46], pct.group(0) if pct else ""))
    print("    %d kit(s) flagged. WomenRemote_Wave9 is the model at 1%%." % len(rows))

    # The scored shortlist was opt-in from 4 Sep and REQUIRED from 15 Sep. The fit
    # to report is now two numbers: it still costs the grandfathered specs nothing,
    # and the exemption list has not grown.
    print("")
    print("  SCORED ICP SHORTLIST (4 Sep 2026, REQUIRED since 15 Sep 2026)")
    specs = sorted(Path(__file__).parent.glob("*/" + VALUE_PROPS))
    exempt = grandfathered(SCRIPT_DIR, "pain_score")
    hits = 0
    for s in specs:
        blocks = parse_value_props(s)
        if not any(b.get("pain_score") for b in blocks.values()):
            continue
        hits += 1
        bad = sum(1 for b in blocks.values()
                  if parse_pain_score(b.get("pain_score", ""))[1])
        print("    %-46s %d/%d block(s) unscored" % (s.parent.name[:46],
                                                     bad, len(blocks)))
    print("    %d of %d specs carry pain_score; %d are grandfathered by name in %s."
          % (hits, len(specs), len(exempt), GRANDFATHER_FILE))

    unlisted = [s.parent.name for s in specs
                if s.parent.name not in exempt
                and not any(b.get("pain_score")
                            for b in parse_value_props(s).values())]
    pairs = grandfather_entries(SCRIPT_DIR)
    grew = len(pairs) > GRANDFATHER_BASELINE
    print("    %s exemption list holds %d (kit, field) pair(s), baseline %d%s"
          % ("FAIL " if grew else "ok   ", len(pairs), GRANDFATHER_BASELINE,
             " - IT GREW. A kit with no ranked ICP list, or no stated test, is a "
             "blocker, not an exemption." if grew else ""))
    print("    %s %d spec(s) would now BLOCK on a missing pain_score%s"
          % ("ok   " if not unlisted else "note ", len(unlisted),
             "" if not unlisted else ": " + ", ".join(unlisted[:4])))

    # --- the hypothesis fit. Same one-class shape as everything else here: it must
    #     cost the shipped specs nothing, and it must still reject an empty claim.
    hyp_exempt = grandfathered(SCRIPT_DIR, HYPOTHESIS_KEY)
    hyp_unlisted = [s.parent.name for s in specs
                    if s.parent.name not in hyp_exempt
                    and not any(b.get(HYPOTHESIS_KEY)
                                for b in parse_value_props(s).values())]
    print("    %s %d spec(s) would now BLOCK on a missing hypothesis%s"
          % ("ok   " if not hyp_unlisted else "note ", len(hyp_unlisted),
             "" if not hyp_unlisted else ": " + ", ".join(hyp_unlisted[:4])))
    bad = [h for h in ("This will work", "good ad for teachers", "TBD")
           if not any(h.lower().rstrip(".").startswith(e) or
                      h.lower().rstrip(".") == e for e in HYPOTHESIS_EMPTY)]
    print("    %s the empty-claim list rejects 'This will work', 'good ad for "
          "teachers', 'TBD'" % ("ok   " if not bad else "FAIL "))
    good = HYPOTHESIS_EXAMPLE.split(":", 1)[1].strip()
    ok_good = (len(good.split()) >= HYPOTHESIS_MIN_WORDS
               and not any(good.lower().startswith(e) for e in HYPOTHESIS_EMPTY))
    print("    %s the documented example passes its own check"
          % ("ok   " if ok_good else "FAIL "))
    grew = grew or bool(bad) or not ok_good

    # check_funnel_slugs only speaks about a camp that has not run yet, because
    # funnels_*.json is a leads window and absence proves nothing for a past
    # camp. The first cut of the rule missed that and fired on 16 of 51 kits.
    # These pin the two traps: "_" is a word character so \b after "Oct" never
    # matched the shipped _SEND_THIS folder, and a January kit read as ten
    # months past instead of two ahead.
    camp_cases = [
        ("CorporateFinance_Notify_17-19Oct", True),
        ("CorporateFinance_Notify_17-19Oct_SEND_THIS", True),   # the shipped copy
        ("USAccounting_Search_10-12Oct_SEND_THIS", True),
        ("SomeKit_3-5Jan", True),                               # wraps to next year
        ("SomeKit_20-22Sep", True),                             # still running
        ("SomeKit_18-20Sep", False),                            # finished
        ("HR_GrowthCamp_Wave10_MediaBuyer_22-24Aug", False),
        ("ContentWriting_SectionA_29-31Aug", False),
        ("NoDates_Kit", False),                                 # unknown says nothing
    ]
    camp_bad = [n for n, want in camp_cases
                if camp_is_ahead(n, "2026-09-21") != want]
    print("    %s camp_is_ahead reads %d folder-name date(s) correctly%s"
          % ("ok   " if not camp_bad else "FAIL ", len(camp_cases),
             "" if not camp_bad else ": " + ", ".join(camp_bad[:3])))
    grew = grew or bool(camp_bad)

    print("    Not fitted against live cost: no scored ICP has run yet. It ranks")
    print("    what to BUILD, and blocks only on a malformed or missing score.")
    print("    check_funnel_slugs is a HINT, not proof: a funnel with no traffic")
    print("    looks identical to one never created. Only a browser settles it.")
    return 1 if grew else 0


def kit_folders(root: Path):
    """The folder itself if it is a kit, else the immediate subfolders that are."""
    if (root / "ads").is_dir():
        return [root]
    return sorted(d for d in root.iterdir() if d.is_dir() and (d / "ads").is_dir())


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    if argv[1] == "--selftest":
        return selftest()
    if argv[1] == "--scaffold-from":
        if len(argv) < 4:
            print("Usage: python preflight.py --scaffold-from <icp-list> <kit-folder>")
            return 1
        return scaffold_from(Path(argv[2]), Path(argv[3]))

    if argv[1] == "--scaffold":
        if len(argv) < 3:
            print("Usage: python preflight.py --scaffold <kit-folder>")
            return 1
        return max(scaffold(Path(a)) for a in argv[2:])

    if argv[1] == "--shortlist":
        if len(argv) < 3:
            print("Usage: python preflight.py --shortlist <kit-folder>")
            return 1
        return max(shortlist(Path(a)) for a in argv[2:])

    targets, roots = [], []
    for arg in argv[1:]:
        p = Path(arg)
        if p.is_dir():
            roots.append(p)
            targets += [f for f in p.rglob("*.html") if not SKIP_FILE.match(f.name)]
        elif p.suffix.lower() == ".html":
            targets.append(p)

    if not targets:
        print("No HTML files found.")
        return 1

    total_block = total_warn = 0
    bad_pages = 0

    for path in sorted(set(targets)):
        blockers, warnings = check_page(path)
        blockers = list(dict.fromkeys(blockers))
        warnings = list(dict.fromkeys(warnings))
        if not (blockers or warnings):
            continue
        if blockers:
            bad_pages += 1
        try:
            label = path.relative_to(Path.cwd())
        except ValueError:
            label = path
        print(f"\n{label}")
        for b in blockers:
            print(f"  BLOCKER  {b}")
        for w in warnings:
            print(f"  warning  {w}")
        total_block += len(blockers)
        total_warn += len(warnings)

    def report(header, findings):
        nonlocal total_block, total_warn
        if not findings:
            return
        print(f"\n{header}")
        for f in findings:
            print(f"  {f}")
            if f.startswith("BLOCKER"):
                total_block += 1
            else:
                total_warn += 1

    gated = 0
    for root in roots:
        for kit in kit_folders(root):
            report(f"{kit} - ad to landing page pairing", check_pairing(kit))
            report(f"{kit} - landing pages differ from each other",
                   check_lp_diversity(kit))
            report(f"{kit} - funnel slugs exist in GrowthX (Rule 5)",
                   check_funnel_slugs(kit))
            report(f"{kit} - value proposition (Rules 1, 2, 3)",
                   check_value_props(kit))
            gated += value_props_enforced(kit)

    print("\n" + "-" * 64)
    print(f"{len(set(targets))} pages checked - "
          f"{total_block} BLOCKER, {total_warn} warning "
          f"({bad_pages} pages blocked)")

    if total_block:
        print("\nNOT READY TO SEND. Fix every BLOCKER and re-run.")
        return 1

    if gated:
        print("\nMechanical checks pass, and every ad states a better job and")
        print("defines its field on the page it points at.")
    else:
        print("\nMechanical checks pass.")
        print("The value-prop gate did NOT run here - no kit folder with ads/,")
        print("or the folder is marked legacy. Rules 1, 2 and 3 are unchecked.")
    print("Still to confirm by hand before sending:")
    print("  1. Read each better_job line - would that person want that job?")
    print("  2. Could someone who never heard of the field name the work?")
    print("  3. Did you open each page in a browser and test the pay button?")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
