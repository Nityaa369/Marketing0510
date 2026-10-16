#!/usr/bin/env python3
"""Creative call-out linter — run on every ad HTML before rendering/handoff.
Usage: python3 ads/ad_lint.py <ad.html> [...]

WHY THIS EXISTS (26 Jul 2026). Ramanuj has rejected cryptic call-outs three times in one
session — "this is shit not understandable at all", "this is also cryptic", "very bad call
out - almost mysterious", "omg again cryptic as fuck ... i thought we made rules against it".
The rule DID exist, in memory. Memory did not hold, because each new kit was written fresh
and the rule was never re-read. Same root cause as the LP sermons and the sticky CTA. So it
is a checker now.

THE DIAGNOSIS. Compare what passed and what failed:

  WORKED (plain, instantly decodable by a stranger):
    "HOW TO GET YOUR FIRST BOARD SEAT"          verb GET, names the prize
    "BOARD SEATS ARE NEVER ADVERTISED"          verb ARE, complete statement
    "5 REASONS SENIOR PROFESSIONALS JOIN BOARDS" verb JOIN, names who + what
    "ON THE IICA DATABANK?"                     a question the reader can answer

  FAILED (rejected as cryptic/mysterious):
    "FOR PROFESSIONALS WITH 15+ YEARS OF EXPERIENCE"   says WHO, never says WHAT
    "ONE PREPARATION. FIVE BOARD ROLES."               a riddle: no verb, no subject

The failures are all NOUN-PHRASE FRAGMENTS. The reader has to infer the missing verb, and on
a feed nobody does that work. So:

C1 FAIL  call-out has no verb and is not a question -> it is a fragment, i.e. a riddle
         (verb = an explicit list OR any -ed/-ing word; a fixed list always has holes)
C2 FAIL  call-out names no concrete thing the reader wants (board/seat/director/boardroom/...)
C3 WARN  call-out is only an audience descriptor ("for professionals with...") -> says who, not what
C4 WARN  call-out longer than ~48 chars -> stops being thumbnail-legible
C5 FAIL  call-out is about vague third parties ("they", "some people") instead of the
         reader or a usable fact -> a scene, not a promise. The reader must be in it.
C6 WARN  call-out contains insider vocabulary (databank/IICA/NRC/LODR) -> cryptic on broad
         delivery. ONLY acceptable as a deliberate shibboleth for an audience that already
         knows the term (e.g. the ₹100 "ON THE IICA DATABANK?" ad targeting registrants) —
         if that is the intent, the WARN is the record of the decision.
C7 FAIL  em-dash anywhere in creative copy (Ramanuj 27 Jul 2026: "too many emdashes -
         remove all emdashes"). Use periods, commas or colons.
C8 FAIL/WARN  call-out or kicker font too small to notice (Ramanuj 27 Jul 2026: made him
         ask twice for 2x/4x bigger). On a 1080px canvas: .callout >=44px (FAIL below),
         .elig kicker >=28px (FAIL below, WARN under 36px).

Eligibility/audience lines are fine — as a SUPPORTING line (.elig), never as the call-out.

ADDED 13 Aug 2026 — C10..C22. Every one of these was already a hard rule that lived only in
memory, and every one has been re-broken at least once because each new kit is written fresh.
Same root cause that produced C1..C9. Only rules a regex can decide reliably are here; C13
(brand by product line) belongs to check_claims.py, and C20 (4-step spine) needs the rendered
creative and is left to the vision gate rather than shipped as a noisy heuristic.

C10 FAIL/WARN earning figures on the ad (FAIL) or experience-year gates (WARN, 15+ allowed)
C11 FAIL  "not for you if" / negative-qualification block
C12 FAIL  distress positioning
C14 FAIL  Sandya Advani named as proof
C15 FAIL  promises a recording
C16 FAIL  product-line vocabulary gate ("AI" on SkillArbitrage skilling, "work for US/UK
          clients", bare "UK firms", "automatic exemption")
C17 FAIL  topic call-out on an HR creative (labour law / POSH — reads as Labour Law, ~10x cost)
C18 FAIL  targets or names freelancers
C19 WARN  scarcity framing on an exam product (abundance framing converts, scarcity backfires)
C22 WARN  no camp date on the creative
"""
import re, sys, os
import html as _html

VERBS = r"""\b(?:get|gets|getting|is|are|was|were|be|become|becomes|join|joins|joining|open|opens|
 need|needs|want|wants|can|could|will|make|makes|take|takes|start|starts|learn|learns|
 qualify|qualifies|earn|earns|land|lands|bag|bags|hire|hires|appoint|appoints|pay|pays|
 have|has|do|does|did|know|knows|find|finds|build|builds|turn|turns|work|works|
 sit|sits|clear|clears|cleared|prepare|prepares|run|runs|go|goes|come|comes|
 reach|reaches|break|breaks|broke|land|lands|secure|secures|choose|chooses|wait|waits|
 leave|leaves|walk|walks|send|sends|sent|keep|keeps|stay|stays|handle|handles|show|shows|
 fall|falls|fell|search|searches|vote|votes|step|steps|apply|applies|register|registers|
 belong|belongs|require|requires|deserve|deserves|retire|retires|end|ends|begin|begins|

 keep|keeps|spend|spends|treat|treats|ask|asks|give|gives|show|shows|help|helps|

 argue|argues|draft|drafts|file|files|move|moves|cross|crosses|appear|appears|
 defend|defends|handle|handles|stop|stops|send|sends|carry|carries|
 add|adds|become|becomes|step|steps|own|owns|run|runs|clear|clears|return|returns|
 manage|manages|supervise|supervises|instruct|instructs|assemble|assembles|
 understand|understands|report|reports|
 bring|brings|guide|guides|oversee|oversees|
 # 18 Sep 2026: C1 called seven corporate finance faces noun fragments when every one of them is
 # an imperative with an ordinary English verb ("Arrange the loan and value the business"). The
 # list already carries draft, file, supervise and oversee, so the omissions were arbitrary rather
 # than principled. Measured before and after on 39 shipped faces (US Accounting 10-12 Oct and
 # Independent Director 10-12 Oct): verdicts unchanged, 21 accept / 18 accept-with-changes.
 arrange|arranges|value|values|read|reads|restart|restarts|sign|signs|advise|advises|
 score|scores|invest|invests|forecast|forecasts|cost|costs|cover|covers|price|prices|
 pass|passes|close|closes|sell|sells|
 # 23 Sep 2026: same arbitrary omission, HR wave. C1 called "Recruit for startups abroad, paid in
 # dollars." a noun fragment - an imperative whose verb is the first word. The list already holds
 # hire, appoint and supervise, so recruit and source were holes rather than decisions. Measured
 # before and after on the 39 shipped faces of US Accounting 10-12 Oct and Independent Director
 # 10-12 Oct: verdicts unchanged, 21 accept / 18 accept-with-changes.
 recruit|recruits|source|sources|screen|screens|onboard|onboards|bill|bills|charge|charges|
 serve|serves|automate|automates|set|sets|


 never|now|why|how|what|when|who)\b"""

NOUNS = [
    'board', 'seat', 'director', 'directorship', 'boardroom', 'iica', 'databank',
    'solicitor', 'lawyer', 'exam', 'sqe', 'practice', 'firm', 'company', 'career',
    'job', 'work', 'salary', 'client', 'course', 'community', 'bootcamp',
    'tax', 'taxes', 'licence', 'license', 'accountant', 'accounting', 'bookkeeper',
    'bookkeeping', 'irs', 'america', 'us ', 'dollar', 'freelance', 'income',
    'finance', 'deal', 'cfo', 'banking', 'valuation', 'modeling', 'modelling', 'ipo',
    # litigation practice (added 30 Jul 2026 for the criminal-litigation kit — the list
    # had no courtroom vocabulary at all, so complete call-outs naming a concrete prize
    # ("run a criminal case start to finish") were failing C2 as "abstractions").
    'case', 'cases', 'bail', 'brief', 'court', 'trial', 'advocate', 'skill', 'skills',
    'chamber', 'litigation', 'hearing', 'petition', 'chargesheet', 'cross examination',
    # arbitration practice (added 4 Aug 2026 for the arbitration_community_aug04 kit —
    # same gap as the 30 Jul litigation addition: no ADR vocabulary, so call-outs naming
    # the concrete prize ("Draft your first Statement of Claim") failed C2 as abstractions).
    'arbitration', 'tribunal', 'award', 'claim', 'dispute', 'disputes', 'clause',
    # contract drafting (added 5 Aug 2026 for the contract_drafting_aug05 kit — same
    # precedent: transactional vocabulary missing, concrete prizes failed C2).
    'contract', 'contracts', 'drafting',
    # senior-professionals consulting (added 5 Aug 2026 for the senior_ai_r10_aug21 kit —
    # same gap: the product's concrete prize IS the consulting practice and its clients,
    # so "start a consulting business" failed C2 as an abstraction).
    'consulting', 'consultant', 'client', 'clients',
    # data privacy / DPDP (added 10 Aug 2026 for the dp_icp40_aug29 kit — same precedent as
    # the 30 Jul litigation and 4 Aug arbitration additions: the list carried no privacy
    # vocabulary at all, so call-outs naming the concrete prize ("Your controls make you a
    # privacy officer", "Add DPDP audits to your audit clients") failed C2 as abstractions).
    'privacy', 'dpdp', 'gdpr', 'consent', 'data', 'breach', 'audit', 'audits', 'auditor',
    'officer', 'dpo', 'regulator', 'record', 'records', 'notice', 'file', 'files',
    'rulebook', 'processor', 'erasure', 'deletion', 'retention', 'profile', 'profiles',
    'compliance', 'questionnaire', 'review', 'governance',
]

# ---------------------------------------------------------------------------
# C10..C22 — product context + lexicons (added 13 Aug 2026)
# ---------------------------------------------------------------------------
# Product line is inferred from the path, same convention as check_claims.py. Several rules
# only apply to one product family, so a wrong inference costs a false positive: pass
# --product to override when a kit folder name is ambiguous.
HR_HINTS       = ('hr_', '_hr', 'hr/', 'strategic_hr', 'hrbp')
EXAM_HINTS     = ('patent', 'judiciary', 'sqe', 'ca_bar', 'cabar', 'ibps', 'clat')
# senior_ai was briefly removed from this list (15 Aug) on lp_41 evidence, then RESTORED
# 16 Aug: shown the flagged line, Ramanuj's fix was 'instead of AI say "agents you custom
# built"' — agents-language holds even on the senior-AI product. C16 was right.
SKILLING_HINTS = ('hr_', 'us_acc', 'usacc', 'acw', 'academic', 'women', 'content_writ',
                  'ai_automation', 'senior_ai', 'us_accounting')
UK_HINTS       = ('sqe', 'uk_', 'solicitor', 'uscl')
# Content-writing bootcamp carve-out (20 Aug 2026): on THIS product "AI" is the approved
# vocabulary — the 6 Aug VoC fixed "AI Content Strategist" as the aspiration label, and
# every shipped cell (cw_01..cw_10, waves 1-2, Ramanuj-approved) carries "AI" on the
# creative. The word ban stays for the rest of the skilling line (senior_ai included,
# per the 16 Aug restore above). Kit-dir judging never caught this because
# "ContentWriting_W2" does not contain the underscored hint; working-folder judging did.
CONTENTWRITING_HINTS = ('content_writ', 'contentwriting')

def product_of(path):
    p = path.lower()
    return {
        'hr':       any(h in p for h in HR_HINTS),
        'exam':     any(h in p for h in EXAM_HINTS),
        'skilling': any(h in p for h in SKILLING_HINTS),
        'uk':       any(h in p for h in UK_HINTS),
        'contentwriting': any(h in p for h in CONTENTWRITING_HINTS),
    }

# C10 — earnings/experience figures. The PRICE is fine (₹10, ₹100); an income claim is not.
# Upside ladders live on the LP. The 15+ years eligibility qualifier is a deliberate exception
# (ID funnel) and must not trip the check.
# BACKTEST CORRECTION (13 Aug 2026). C10 rejected 57 creatives that Ramanuj approved and
# shipped in media-buyer zips — more than any other rule. Two bugs, both mine:
#   (a) `₹\s?[\d,]{4,}` counted the COMMA toward the length test, so the price "₹100," matched
#       as a four-character figure. Twelve SQE statics were rejected for showing their price.
#   (b) lakh/crore fired on MARKET-SIZE stats ("387 cr in two record years", "963 cr IPO
#       pipeline"), which are not earnings claims at all.
# The rule bans EARNINGS figures. It now counts digits only, and only treats a big number as an
# earning claim when an earning word sits near it.
EARN_NEAR = r'(?:earn|salary|salaries|income|pay|package|ctc|stipend|fee|fees|charge|bill)'
MONEY_RX = [
    (r'₹\s?(?=[\d,]*\d{5})[\d,]+',           'a rupee figure of ₹10,000 or more'),
    (rf'\b\d+\s?(?:lakh|lakhs|lpa|cr|crore)\b[^.]{{0,40}}{EARN_NEAR}',
     'a lakh/crore/LPA earning figure'),
    (rf'{EARN_NEAR}[^.]{{0,40}}\b\d+\s?(?:lakh|lakhs|lpa|cr|crore)\b',
     'a lakh/crore/LPA earning figure'),
    (r'₹\s?\d+\s?(?:k|l)\b',                 'a ₹Nk / ₹NL figure'),
    (r'\b\d[\d,]*\s*(?:per month|/month|a month|per year|/year)\b', 'a per-month/per-year figure'),
]
EXP_RX = r'\b(\d+)\+?\s*(?:years|yrs)\b'

# C11 — negative qualification. Banned outright, any funnel.
NOTFORYOU_RX = [
    r'\bnot for you if\b', r'\bthis is not for\b', r'\bdo not (?:apply|join|buy) if\b',
    r"\bdon'?t (?:apply|join|buy) if\b", r'\bwho (?:should|must) not\b', r'\bskip this if\b',
]

# C12 — distress positioning. Sell positive capability, never fear.
# Two tiers. The hard list is unambiguous distress-coaching and stays a FAIL. The
# soft list is stock direct-response pain vocabulary that appears in APPROVED work
# ('stuck in' blocked acw_27_stuck_brick, an ad Ramanuj shipped) — those phrases
# get a WARN so a human looks at the framing, which is what the rule is actually
# about.
DISTRESS_RX = [
    r'\byour career is over\b',
    r'\btoo late for you\b', r'\bnobody wants\b', r'\bno one will hire\b',
    r'\bwasting your (?:life|career|years)\b', r'\bobsolete\b', r'\breplaced by\b',
]
DISTRESS_SOFT_RX = [
    r'\bleft behind\b', r'\bfalling behind\b', r'\bstuck in\b', r'\bdead[- ]end\b',
]

# C15 — camps are live-only by design. Match a PROMISE of a recording, not the bare word:
# on a 2,303-creative sweep the bare word fired on 14% of files, almost all of them talking
# about recording something rather than offering one.
RECORDING_RX = (r'\b(?:get|receive|access)\s+the\s+recording|\brecordings?\s+(?:will be|are|'
                r'included|available|provided)|\bwatch\s+(?:it\s+)?later|\bwatch\s+anytime|'
                r'\breplay\b|\blifetime access\b|\brecorded sessions?\b')

# C18 — has never converted.
FREELANCER_RX = r'\bfreelancer|\bfreelancers\b'

# C19 — scarcity backfires on exam products; abundance framing converts.
SCARCITY_RX = [
    r'\bonly \d+ (?:cleared|passed|qualified|made it)\b', r'\bfewer than \d+\b',
    r'\bjust \d+ people\b', r'\bless than \d+% (?:clear|pass)\b',
]

DATE_RX = r'\b\d{1,2}\s?(?:st|nd|rd|th)?\s?(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'

# C24 — mechanism-led headline (Ramanuj, 13 Aug 2026, tearing down a women-remote static the
# gates had passed: "the large most big header does not talk about what the TG wants i.e remote
# work - mine would be '6 things this bootcamp will teach you so you can land your first well
# paid remote job'"). The failing shape: the giant line makes the PRODUCT the subject ("6 things
# this bootcamp teaches that help you get one.") and parks the prize in a pronoun whose
# antecedent lives up in the kicker. The reader's want must be IN the headline, not referenced
# by it. Same lesson as feedback_ad_formula_audience_aspiration: kicker = who, headline = what
# they become/get.
MECHANISM_RX = re.compile(
    r'\b(this|the|our)\s+(bootcamp|growth\s?camp|course|program|programme|community|'
    r'masterclass|workshop|training)\b', re.I)
PRONOUN_PRIZE_RX = re.compile(r'\b(get|land|find|have)\s+(one|it|that)\b[.!]?\s*$', re.I)

# C25 — conversion assets styled as fine print (same teardown: "no degree etc part is too
# small - not readable"). Barrier-removal lines are the single cheapest-performing pattern in
# the backtest (0.41 index) and eligibility is a conversion asset, not a disclaimer. The LP
# linter has had this rule for weeks (R4); the ad side never did. Fails when a barrier phrase
# renders below 30px on the 1080 canvas.
BARRIER_RX = re.compile(
    r'no (degree|experience|coding|office|law degree|cpa|relocation)\b|'
    r'without (a )?(degree|experience)\b|simple english is enough|no experience letter', re.I)

# C26 — CTA price semantics (Ramanuj, 15 Aug 2026, DPDP returner teardown): "reserve my seat
# for Rs 10 sounds like you may have to pay more later - should say 9 hour of training just for
# Rs 10." Reserve/book language carries deposit semantics: pay now, balance due later. The cure
# is a total-value line stating the full exchange ("₹10 gets you all 3 days", "9 hours of live
# training just for ₹10"). 132 approved ads carry the pattern, 67 uncured, so this is FIX-tier
# on the uncured form only — the rule postdates those approvals.
RESERVE_CTA_RX = re.compile(r'(reserve|book|hold|grab|claim)\s+(my|your|a)\s+(seat|spot|place)', re.I)
TOTAL_VALUE_RX = re.compile(
    r'all\s+3\s+days|all\s+three\s+(days|evenings)|\d+\s*hours?\s+(of\s+)?(live|training)|'
    r'gets you all|everything|full\s+(camp|bootcamp)|just\s+for\s+.?10|pay once|one[- ]time|'
    r'nothing (more|else) to pay|no (further|extra) (payment|charges)', re.I)

# C27 — kicker chip in a visual blind spot (Ramanuj, 15 Aug 2026, refining the DPDP teardown):
# "back after a break was in a visual blind spot - same colour kicker as a background above
# large fonts - in much smaller font." Three compounding mechanisms: (a) the chip's background
# is nearly the CANVAS colour, so it never registers as a block — the neumorphic pink-on-pink
# chip was held only by a soft shadow; (b) it sits in much smaller type than the huge headline
# directly below, so the headline eats the eye; (c) top-corner position. The fix that worked:
# "in the new one the font is much larger so it draws the eye." Mechanical form: chip bg vs
# canvas bg luminance ratio — a working kicker is a contrast BLOCK (dark chip on teal, navy bar
# on cream); a blending one fails.
def _lum(hexstr):
    h = hexstr.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    try:
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return None
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def kicker_blend(html):
    """Return (ratio, chip_hex, canvas_hex) when the kicker chip blends into the canvas."""
    # canvas = the page ground only. Matching .card here made white-panel kits false-fire
    # (chip legitimately sits ON a card; chip-vs-card is a different question).
    m = re.search(r'\bbody\s*{[^}]*?background(?:-color)?:\s*(#[0-9a-fA-F]{3,6})', html, re.S) \
        or re.search(r':root\s*{[^}]*?--bg:\s*(#[0-9a-fA-F]{3,6})', html, re.S)
    if not m:
        return None
    canvas = m.group(1)
    for cls in ('kicker', 'chip', 'kick', 'elig'):
        k = re.search(rf'\.{cls}\s*{{[^}}]*?background(?:-color)?:\s*(#[0-9a-fA-F]{{3,6}})', html, re.S)
        if k:
            l1, l2 = _lum(canvas), _lum(k.group(1))
            if l1 is None or l2 is None:
                return None
            ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
            return (ratio, k.group(1), canvas)
    return None


# C23 — the identity call-out. Ramanuj, 13 Aug 2026: "why is there a rule that blocks identity
# call outs that is crazy - there must be identity call outs for every ad."
#
# REFINED 15 Aug 2026 (DPDP returner teardown): a bare SITUATION with no person in it is not an
# identity call-out. "BACK AFTER A BREAK?" fired C23 mechanically and the vision pass overrode
# it as "situation-framed" — Ramanuj rejected it: "no clear call out - the current call out is
# strange". The winners are person-IN-situation ("WOMEN RETURNING TO WORK", "Indian woman
# lawyer - career on hold for family"). When C23 fires, do NOT wave it through as
# situation-framing unless a person-noun is present somewhere in the frame.
#
# He is right, and the original rule had it backwards. C1 treated any verbless noun phrase as a
# riddle, which swept up the identity line along with the genuine riddles. The evidence is on
# his side twice over: HR identity-led ran ₹31 per buyer against ₹421 capability-led, and on the
# joined backtest set creatives with the identity IN the call-out ran at 0.98 index against 1.01
# without it. "WOMEN IN ACADEMIA" (0.77) and "INDIA'S PROFESSORS" (0.82) both beat their
# campaign median while C1 was rejecting them.
#
# So identity in the call-out is never a defect. Its ABSENCE is. C23 fires when no audience is
# named anywhere on the creative.
IDENTITY_RX = re.compile(
    r'\b(women|men|mothers?|housewi(?:fe|ves)|homemakers?|professors?|lecturers?|teachers?|'
    r'scholars?|researchers?|graduates?|students?|professionals?|lawyers?|advocates?|'
    r'solicitors?|engineers?|doctors?|nurses?|pharmacists?|accountants?|auditors?|bankers?|'
    r'founders?|managers?|officers?|analysts?|consultants?|freshers?|retirees?|paralegals?|'
    r'coders?|transcriptionists?|'
    # 2 Oct 2026 (Women AI wave 10). The vocabulary already carries `women`, `mothers`
    # and `housewives`, and had no word for the rest of how this audience names itself:
    # C23 and C1 rejected five faces whose call-out is as plain as any here - "Daughters
    # and wives in a family business", "Bank and insurance branch staff", "Government
    # exam aspirants at home", "Salon and beauty workers with quiet weekdays". Same fix
    # and same reason as the BPO and dietitian notes below. `workers?` carries its word
    # boundary deliberately, so the kit's constant "client work" does not satisfy it,
    # and none of these appears anywhere in this product's shared chrome.
    r'wi(?:fe|ves)|daughters?|staff|aspirants?|workers?|carers?|caregivers?|'
    r'academia|academics?|phds?|mbas?|mtechs?|ca|cs|cma|llb|llm|hr|recruiters?|'
    r'secretaries|examiners?|litigators?|associates?|interns?|'
    # 13 Aug 2026: BPO / call-centre ICP named the audience but the vocabulary
    # had no word for it, so C23 false-failed a compliant kit.
    r'bpo|call\s*cent(?:re|er)|contact\s*cent(?:re|er)|voice\s*process|'
    # 24 Sep 2026: the Senior AI "reach" wave names its reader in the reader's own
    # words - "ERP and SAP implementation leads", "QA and testing leads", "IT and
    # information security heads", "Plant, power and process operations heads",
    # "Finance and accounts controllers", "Cloud and infrastructure architects" - and
    # C23/C1 false-failed 6 of 8 faces. Same fix and same reason as BPO and dietitian
    # above: the vocabulary had never met an enterprise-IT or plant-operations camp.
    # `controller` and `architect` go in bare, they are only ever job titles. `lead`
    # and `head` go in ONLY as the compounds these readers use, because a bare
    # "leads to" or "head of the table" would let C23 pass a face that names nobody.
    r'controllers?|architects?|'
    r'(?:implementation|testing|qa|delivery|technical|team|tech|project|module|'
    r'practice|engineering)\s+leads?|'
    r'(?:security|operations|finance|delivery|practice|technology|engineering|plant|'
    r'project|programme|program|department)\s+heads?|'
    # 14 Aug 2026: "IN-HOUSE COUNSEL" kicker false-failed the dpdp lawyer cells.
    r'counsel|'
    # 26 Aug 2026: "TRAINED AS A DIETITIAN?" false-failed C23 - the vocabulary had no
    # word for the nutrition occupations, exactly as it had none for BPO or for the
    # writing occupations before them. Same fix, same reason.
    r'dietit(?:ian|ians)|dietic(?:ian|ians)|nutritionists?|'
    # 3 Sep 2026: LABORATORY AND FIELD SCIENCE OCCUPATIONS, plus the clipped
    # "GRADS". Same fix and same reason again, and this time it false-failed a
    # PRICED WINNER: C1 fired on "AGRI & FOOD SCIENCE GRADS", which is
    # icp_18_agri_foodsci at Rs 131.49, one of only four patent faces in the repo
    # carrying a live cost. It also fired on "INDUSTRIAL & ANALYTICAL CHEMISTS".
    # The vocabulary knew `engineers` and `graduates` but not `grads`, and knew
    # `pharmacists` but no bench-science occupation at all. C1's own docstring
    # already settles the principle - "an identity call-out is the TARGET, not a
    # defect" - so this is the lexicon catching up with the rule, not a loosening.
    # `drafter` added 3 Sep 2026, same reason as in simplicity.py ROLE_RX: it is
    # the same class as `writer`, and C1/C23 both read "FREELANCE LEGAL DRAFTERS"
    # as naming nobody.
    r'drafters?|'
    # 24 Sep 2026 (Tech Law Google wave): "A VIRTUAL ASSISTANT?" fired C23 and REJECTED a
    # face that names its reader in the reader's own words. The vocabulary knew
    # `secretaries`, `paralegals` and `administrators` but had no word for the assistant
    # occupations, exactly as it had none for BPO, dietitians, grads or writers before them.
    # Measured over every call-out in this repo (296 distinct): C23 fires on 60 before and
    # 58 after, and the only two that change are "A virtual assistant?" and
    # "STORE ASSISTANTS", both of which name a real occupation. So this is the lexicon
    # catching up with the rule, not a loosening: it cannot wave through a face that names
    # nobody, because no face in the corpus uses "assistant" for anything but a person.
    r'assistants?|'
    # 1 Oct 2026 (DPDP wave 3): `coders` and `transcriptionists`. Both are unambiguous
    # occupation nouns and both are live DPDP readers - transcription and RCM is the
    # largest cell in that campaign at 254 buyers. Measured before adding them: across
    # the 592 ad HTML files in this folder the two words change the C23 verdict on
    # exactly 2, both of them the faces that prompted it. Adding a word to this lexicon
    # is monotonic: it can only remove a C23 finding, never create one, so the only risk
    # is wrongly accepting, and a face whose giant line says "Medical coders" is naming
    # an audience by any reading.
    # 17 Sep 2026 (Independent Director chat wave): senior titles and the retired. "A CFO or
    # finance head?", "A CEO or CXO?", "A practising Company Secretary?" and "Just retired
    # after a 30-year career" all fired C23 while naming their reader. Same fix as above.
    r'cfos?|ceos?|cxos?|ctos?|chros?|executives?|principals?|administrators?|'
    r'secretary|retired|veterans?|'
    r'grads?|chemists?|microbiologists?|biologists?|physicists?|'
    r'veterinar(?:ian|ians|y)|technologists?|metallurgists?|pharmacologists?|'
    # 14 Aug 2026: "DIGITAL AGENCIES" / "LEGAL PROCESS AND TRANSLATION FIRMS" kickers
    # false-failed — firm/agency-audience cells name the WHO at company level.
    r'agenc(?:y|ies)|firms?|'
    # 20 Aug 2026: "CONTENT WRITERS" / "SOCIAL MEDIA WRITERS" kickers false-failed the
    # content-writing camp cells — the vocabulary had no word for the writing occupations.
    r'writers?|copywriters?|ghostwriters?|editors?|bloggers?|'
    # 20 Aug 2026: "MARKETERS IN INDIA RUNNING THE SHOW" false-failed the usmb wave.
    # The writing occupations went in earlier the same day but the marketing ones did
    # not, and half this product's ICPs are named as marketers, not writers.
    r'marketers?|marketing\s+managers?|strategists?|media\s+buyers?)\b', re.I)


def context_rules(path, body_text, product=None):
    """C10..C22 — the rules that need product context or full-copy scanning."""
    issues = []
    low = body_text.lower()
    prod = product if product is not None else product_of(path)

    # C10 — earnings figures FAIL; experience gates WARN (15+ is an allowed ID qualifier)
    # C10 IS A FLAG, NOT A REJECTION (Ramanuj, 13 Aug 2026: "if an ad promises very clear
    # monetary outcomes - that can be suspect but not necessarily a reject outright - most of
    # our ads are about how to increase income or add income etc"). The backtest said the same
    # thing first: C10 fired on 16.8% of approved work against 6.0% of unshipped, which is the
    # signature of a blocker pointed the wrong way.
    #
    # Note what this does and does not catch. Income FRAMING — "add a second income", "increase
    # what you charge" — is the product's core promise and is never flagged; only a specific
    # monetary FIGURE is. That is the line worth reviewing: the claim gets concrete enough to
    # need backing, and the upside ladder belongs on the LP where it can be qualified.
    for rx, what in MONEY_RX:
        m = re.search(rx, low)
        if m:
            issues.append(('FAIL', 'C10',
                f'creative carries {what} ("{m.group(0).strip()}"). Income framing is fine and is '
                'what these products sell; a specific figure on the ad is the suspect part. '
                'Check it is backed, or move the ladder to the LP. Not a rejection on its own.'))
            break
    # The experience-gate WARN was REMOVED (13 Aug 2026). It fired on 60+ creatives Ramanuj
    # approved and shipped — "7+ years" on the judiciary statics is the statutory eligibility
    # requirement, "2+ years" likewise. It conflated two unrelated rules: "no earning figures on
    # an ad" (this one) and "no exclusionary seniority gates", which came from the women ID
    # autopsy and is about excluding buyers, not about stating an eligibility fact. A blanket
    # year-count check cannot tell those apart, so it does not belong here.

    for rx in NOTFORYOU_RX:
        m = re.search(rx, low)
        if m:
            issues.append(('FAIL', 'C11',
                f'negative-qualification block ("{m.group(0)}") — banned in every funnel. '
                'Qualify positively ("you likely qualify if…") and let the refund line de-risk.'))
            break

    for rx in DISTRESS_RX:
        m = re.search(rx, low)
        if m:
            issues.append(('FAIL', 'C12',
                f'distress positioning ("{m.group(0)}") — sell positive capability, never fear.'))
            break
    else:
        for rx in DISTRESS_SOFT_RX:
            m = re.search(rx, low)
            if m:
                issues.append(('WARN', 'C12',
                    f'pain phrase ("{m.group(0)}") — fine as a pain line, a defect if the whole '
                    f'frame is fear. Check the framing, not the phrase.'))
                break

    if re.search(r'sandya\s+advani', low):
        issues.append(('FAIL', 'C14',
            'Sandya Advani named as proof — use Garima Pandey or Amaresh Kumar.'))

    m = re.search(RECORDING_RX, low)
    if m:
        issues.append(('FAIL', 'C15',
            f'promises a recording ("{m.group(0)}") — camps are live-only by design. '
            'The value substitutes are notes, templates, WhatsApp group, certificate.'))

    # C16 — vocabulary gates, per product line
    if prod['skilling'] and not prod.get('contentwriting') and re.search(r'\bA\.?I\.?\b', body_text):
        issues.append(('FAIL', 'C16',
            'the word "AI" on a SkillArbitrage skilling creative — use "agents" or "systems".'))
    m = re.search(r'work (?:for|with) (?:us|uk|american|british) clients', low)
    if m:
        issues.append(('FAIL', 'C16',
            f'"{m.group(0)}" — the compliant framing is "paralegal support for US/UK firms".'))
    if prod['uk']:
        if re.search(r'\buk firms\b', low) and not re.search(r'uk law firms and lawyers', low):
            issues.append(('FAIL', 'C16',
                'bare "UK firms" — the required phrasing is "UK law firms and lawyers".'))
        if re.search(r'automatic(?:ally)? (?:exempt|qualify)', low):
            issues.append(('FAIL', 'C16',
                'implies an automatic SQE exemption — the compliant claim is "eligible to apply".'))

    if prod['hr'] and re.search(r'\blabour law\b|\blabor law\b|\bposh\b', low):
        issues.append(('FAIL', 'C17',
            'topic call-out on an HR creative (labour law / POSH) — it reads as a Labour Law ad '
            'and costs roughly 10x. Lead with the HR identity and the earning promise.'))

    m = re.search(FREELANCER_RX, low)
    if m:
        issues.append(('FAIL', 'C18',
            f'"{m.group(0)}" — freelancer targeting has never converted on any product.'))

    if prod['exam']:
        for rx in SCARCITY_RX:
            m = re.search(rx, low)
            if m:
                issues.append(('WARN', 'C19',
                    f'scarcity framing ("{m.group(0)}") on an exam product — abundance framing '
                    '(shortage of supply, huge demand) converts; scarcity backfires.'))
                break

    if RESERVE_CTA_RX.search(low) and not TOTAL_VALUE_RX.search(low):
        issues.append(('FAIL', 'C26',
            '"reserve/book my seat for ₹10" with no total-value line — reads like a deposit '
            'with a balance due later. State the full exchange: "9 hours of live training just '
            'for ₹10" or "₹10 gets you all 3 days" (Ramanuj, 15 Aug 2026).'))

    if not IDENTITY_RX.search(low):
        issues.append(('FAIL', 'C23',
            'no identity call-out: the creative never names WHO it is for. Every ad leads with '
            'one big line naming the audience. HR identity-led ran ₹31 per buyer against ₹421 '
            'capability-led, and on the backtest identity-in-the-call-out ran 0.98 vs 1.01.'))

    # C22 INVERTED (13 Aug 2026). It shipped as "no camp date on the creative" on a pooled-copy
    # reading that dated ads ran ~31% cheaper. The per-creative backtest reversed the sign:
    # DATELESS creatives ran at 0.96 index against 1.00 for dated ones, and the old rule fired
    # on 50.7% of approved work against 38.4% of unshipped. Ramanuj then set the rule directly
    # (13 Aug 2026): "we should put dates into landing pages not ad creatives." Both agree, so
    # the check now runs the other way: a date on the AD is the thing worth flagging, and the
    # LP is where it belongs. lp_lint carries the matching P7 that wants the date ON the page.
    m = re.search(DATE_RX, low)
    if m:
        issues.append(('WARN', 'C22',
            f'camp date on the ad creative ("{m.group(0).strip()}"). Dates belong on the landing '
            'page, not the ad. Dateless creatives ran at 0.96 cost index against 1.00 for dated '
            'ones, and a dated creative goes stale the moment the camp moves.'))

    return issues


def calls_out(html):
    """Return every call-out-ish string on the creative.

    FIXED 13 Aug 2026. A call-out is very often split across several spans of the SAME class so
    that individual words can be coloured or highlighted: "PAID RESEARCH WORK FOR <span
    class=k>SCHOLARS</span>". Evaluating each span on its own made C1/C2 fire on every fragment
    — the acw_r10_aug1 kit rejected 32 of 32 creatives on call-outs like "SCHOLARS", "WITH
    PHDs" and "ON YOUR HOURS", none of which is a real call-out. When a class appears more than
    once the pieces are joined and judged as the single line the reader actually sees.

    The pattern must also close on the element's OWN tag. The previous one always closed on
    </span>, so <div class=callout>PHD<br><span class=two>SCHOLARS</span></div> was read as the
    call-out "SCHOLARS" and the first half of the line was invisible to every check. Every
    div-based kit was being linted against fragments.
    """
    out = []
    # 21 Sep 2026: `elig` is dropped from this list. It is the QUALIFIER ROW - "DSA · LOAN
    # CONSULTANTS · CREDIT ADVISORS · B.COM" - which CLAUDE.md Rule 2 requires as step 2 of the
    # first fold, and which by construction is a run of credentials with no verb. Judged as a
    # call-out it fails C1 as a fragment on every face that obeys the rule, including
    # CorporateFinance_MediaBuyer_15-17Aug 4_loan-consultant (Rs 164 on n=396) and
    # 1_cost-accountant (Rs 170 on n=281), the only two ads in that campaign whose confidence
    # band clears par, and both approved by Ramanuj. Where a rule disagrees with a face that was
    # approved or ran cheap, the face wins. The row's words still reach C23's identity check,
    # which reads the whole creative, so nothing about naming the audience is weakened.
    for cls in ('callout', 'band', 'k', 'head', 'kick', 'kicker', 'chip'):
        # class attribute may be unquoted (class=head) — the old pattern required quotes and
        # therefore silently matched nothing on every hand-built carousel kit.
        parts = []
        # `[^>]*>` cannot cross the opening tag's own `>`, so the capture starts exactly at the
        # element's content. The lookahead keeps `callout` from matching `calloutbig`.
        rx = (rf'<(div|span|p|h1|h2|h3)\b[^>]*\bclass=["\']?{cls}(?=["\'\s>])["\']?[^>]*>'
              r'(.*?)</\1>')
        for m in re.finditer(rx, html, re.S | re.I):
            txt = re.sub(r'<br\s*/?>', ' ', m.group(2))
            txt = re.sub(r'<[^>]+>', '', txt)
            # entities must be decoded or the CTA-band skip below never sees its ₹ (&#8377;)
            txt = _html.unescape(txt)
            txt = re.sub(r'\s+', ' ', txt).strip()
            if txt:
                parts.append(txt)
        if not parts:
            continue
        out.append((cls, parts[0] if len(parts) == 1 else ' '.join(parts)))
    return out

def lint(path, product=None):
    html = open(path, encoding='utf-8').read()
    issues = []

    # C7 — em-dash ban (27 Jul 2026). Check rendered text only (not CSS/comments).
    body = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', html, flags=re.S)
    body_text = re.sub(r'<[^>]+>', ' ', body)
    # Widened 21 Sep 2026. Ruchika: "i can see em dashes in between the dates" on
    # "3&ndash;5 Oct". The old count read only a literal U+2014, so an &ndash;/&mdash;
    # entity or an en dash (which reads as the same mark on a face) passed silently.
    # Decode entities and count both. Before: fired on 0 of 355 repo faces; after: 126.
    import html as _html
    body_text = _html.unescape(body_text)
    n_dash = body_text.count('—') + body_text.count('–')
    if n_dash:
        issues.append(('FAIL', 'C7',
            f'{n_dash} em-dash(es) in creative copy — banned (Ramanuj 27 Jul 2026); '
            'rewrite with periods, commas or colons'))

    # C8 — call-outs/kickers must be LARGE (27 Jul 2026: "large call outs never small
    # ones that are barely visible"). Thresholds assume the 1080px kit canvas.
    # RAISED 27 Jul 2026 (evening): Ramanuj asked "2x bigger" a SECOND time on a 36px
    # kicker chip ("we need call outs to be prominent and large"). New floors: kicker
    # chips (any of .elig/.kicker) hard-fail below 56px, target >=64px; giant call-out
    # hard-fail below 64px, target >=80px. Also checks .kicker, which the old rule missed.
    # 'head' is the giant line on carousel slides, 'kick' the chip on hand-built kits; both
    # were invisible to this check until 1 Aug 2026, so carousel kits were never size-linted.
    # A kicker class that carries only the BRAND (SKILLARBITRAGE / LAWSIKHO) is a brand chip,
    # not the identity call-out, and is meant to be small — acw_r10_aug1 rejected 32 of 32
    # creatives on a 25px `.kick` that reads "SKILLARBITRAGE". The size floor exists for the
    # identity kicker; exempt the brand chip rather than force a 56px logo line.
    brandish = {cls for cls, txt in calls_out(html)
                if re.fullmatch(r'(by\s+)?(skillarbitrage|lawsikho)', txt.strip(), re.I)}
    # BARRIER-REMOVAL LINES are exempt from C1/C2/C3, added 4 Sep 2026. C25 in this same
    # file REWARDS this exact element -- "no degree / no experience" runs at a 0.41 cost
    # index, the cheapest-performing pattern in the backtest -- while C1 was rejecting it
    # as "a noun-phrase fragment that names nobody". Both cannot be right about one line.
    # It is a reassurance strip, not the identity call-out, exactly as the brand chip
    # above is a signature rather than a call-out. Fired on 10 of 10 US Corporate Law
    # faces carrying "No US bar exam - no visa - no relocation".
    barrier = {cls for cls, txt in calls_out(html)
               if len(re.findall(r"\bno\b", txt, re.I)) >= 2
               and re.match(r"\s*no\b", txt, re.I)}
    for cls, hard, soft in (('callout', 64, 80), ('head', 64, 80), ('elig', 56, 64),
                            ('kicker', 56, 64), ('kick', 56, 64)):
        if cls in brandish or cls in barrier:
            continue
        m = re.search(rf'\.{cls}\s*{{[^}}]*?font-size:\s*([\d.]+)px', html, re.S)
        if m:
            sz = float(m.group(1))
            if sz < hard:
                issues.append(('FAIL', 'C8',
                    f'.{cls} font-size {sz:.0f}px is barely visible — minimum {hard}px on a 1080px canvas'))
            elif soft and sz < soft:
                issues.append(('WARN', 'C8',
                    f'.{cls} font-size {sz:.0f}px — kickers read best at >={soft}px (Ramanuj asked for 2x on 27 Jul)'))

    # C9 — concrete promise presence (Ramanuj 29 Jul 2026: "check if there are any strong
    # promises on ads or landing pages"). Origin: the patent_aug14 kit shipped 16 ads whose
    # only forward-looking line was "Learn how: 9-hour live training"; he had to ask for the
    # promise twice. A strong promise = a we-verb commitment ("We show you …") and/or a
    # concrete outcome-with-timeframe ("… in 6 months", "by 14 August"). Heuristic + WARN
    # (not FAIL) because retargeting/teaser cells may legitimately omit it — the WARN is the
    # record of that decision.
    # WIDENED 13 Aug 2026. C9 fired on 27.3% of approved, shipped creatives — and they were not
    # promise-less. The legal-AI kit promises "30 SKILLS · 14 DAYS", "Build 30 AI Skills From One
    # System", "14 stops. One destination: AI-trained lawyer", "Finish a day's drafting by
    # lunch". The old detector accepted exactly two shapes ("we show you …" and "in 6 months"),
    # so it read a deliverable-plus-duration promise as no promise at all. A promise is: a
    # we-verb commitment, OR an outcome with a timeframe, OR a counted deliverable, OR an
    # outcome verb naming what the buyer walks out able to do.
    low_all = body_text.lower()
    has_we_verb = bool(re.search(
        r'\bwe (show|give|teach|hand|walk|take|get|build|map) you\b', low_all))
    has_timeframe = bool(re.search(
        r'\bin \d+\s+(day|week|month|year)s?\b'
        r'|\bby \d{1,2} (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)'
        r'|\bby (lunch|monday|tuesday|wednesday|thursday|friday|saturday|sunday|tonight)\b'
        r'|\b\d+[- ]day\b', low_all))
    # a counted deliverable: "30 skills", "14 sessions", "20 templates", "14 stops"
    has_deliverable = bool(re.search(
        r'\b\d+\s+(skills?|sessions?|templates?|tools?|stops?|steps?|modules?|drafts?|'
        r'documents?|clauses?|cases?|checklists?|playbooks?|routes?|projects?)\b', low_all))
    # an outcome verb: what the buyer walks out able to do
    has_outcome = bool(re.search(
        r'\b(build|builds|finish|finishes|draft|drafts|land|lands|master|masters|complete|'
        r'completes|walk out with|leave with|start|starts|run|runs|add|adds|become|becomes)\b',
        low_all))
    if not (has_we_verb or has_timeframe or has_deliverable or has_outcome):
        issues.append(('WARN', 'C9',
            'no promise of value found. The ad never says what the reader GETS: no "We show you"'
            ' commitment, no outcome with a timeframe, no counted deliverable ("30 skills in 14 '
            'days"), no outcome verb ("build", "draft your first…"). Nobody joins for a topic; '
            'they join for a result (Ramanuj 29 Jul 2026).'))

    # C10..C22 — context rules (13 Aug 2026)
    issues += context_rules(path, body_text, product)

    # C27 — kicker chip blends into the canvas (15 Aug 2026). Ratio < 1.35 means the chip is
    # essentially the background colour and only a shadow separates them.
    kb = kicker_blend(html)
    if kb and kb[0] < 1.35:
        issues.append(('FAIL', 'C27',
            f'kicker chip background {kb[1]} is nearly the canvas colour {kb[2]} '
            f'(contrast {kb[0]:.2f}:1) — a visual blind spot. The chip must read as a colour '
            'BLOCK (dark chip on teal, navy bar on cream), or the headline below eats the eye.'))

    # C25 — barrier-removal copy must be readable, not fine print (13 Aug 2026 teardown).
    # Find every barrier phrase, locate the font-size of the class it renders in, and fail if
    # its LARGEST rendering is under 30px on the 1080 canvas.
    sizes = {m.group(1): float(m.group(2)) for m in
             re.finditer(r'\.([\w-]+)\s*{[^}]*?font-size:\s*([\d.]+)px', html, re.S)}
    best_barrier = None
    for m in re.finditer(r'<(\w+)\b[^>]*class=["\']?([\w-]+)[^>]*>([^<]{0,300})', html):
        if BARRIER_RX.search(m.group(3)):
            sz = sizes.get(m.group(2))
            if sz and (best_barrier is None or sz > best_barrier):
                best_barrier = sz
    if best_barrier is not None and best_barrier < 30:
        issues.append(('FAIL', 'C25',
            f'barrier-removal line ("no degree / no experience…") renders at {best_barrier:.0f}px '
            '— fine print. It is the cheapest-performing pattern in the backtest (0.41 index) '
            'and a conversion asset: style it to be read, >=30px, near the CTA.'))

    found = calls_out(html)
    if not found:
        # C0 is a PARSER-COVERAGE signal, not a quality defect. It fires on 30.0% of the
        # creatives Ramanuj approved and shipped against 3.9% of the unshipped, which does not
        # mean approved work is worse — it means a third of his approved kits use markup this
        # linter cannot read, so C1..C6 never ran on them at all. That is a gap in the checker,
        # and it is reported as one.
        issues.append(('INFO', 'C0',
            'no .callout/.band/.head element found — this creative uses markup ad_lint cannot '
            'read, so the call-out rules C1..C6 did NOT run on it. Judge it at Gate 1 instead.'))
        return issues

    for cls, txt in found:
        low = txt.lower()
        # a CTA band ("JOIN FOR ₹100", "START FOR ₹100") is an offer, not a call-out
        if re.match(r'^(join|start|get started|enrol|enroll)\b', txt, re.I) or '₹' in txt:
            continue
        # Separators and slide labels are not call-outs. C1 was rejecting approved judiciary
        # statics on a bare "·" and carousel statics on "Days 8-14" — both are chrome, not the
        # line the reader decodes. Anything under three words with no verb is not a call-out
        # worth judging; the giant line always has more in it than that.
        if len(re.findall(r'[A-Za-z]{2,}', txt)) < 3:
            continue
        # Logistics bands and labels are chrome too. "FREE · LIVE · NO RECORDINGS", "FREE LIVE
        # BOOTCAMP", "District Judiciary · Direct recruitment" and "A note from SkillArbitrage"
        # were all rejected on approved, shipped creatives. None is the line the reader decodes.
        if re.fullmatch(r'[\s·|/,&-]*(?:free|live|online|offline|bootcamp|growth ?camp|webinar|'
                        r'workshop|masterclass|no recordings?|seats? filling|limited|new batch|'
                        r'day \d+|days? \d+[-–]\d+|week \d+|starts?|register|\d{1,2} ?[-–] ?\d{1,2}'
                        r'|[a-z]+ \d{1,2}|202\d)[\s·|/,&-]*', low.strip(), re.I):
            continue
        if re.match(r'^(a )?(note|message|word) from\b', low):
            continue
        # a brand chip is a signature, not a call-out — it has no verb and names no prize by
        # design, so C1/C2 fired on it 25 times in one kit
        if cls in brandish or cls in barrier:
            continue

        has_verb = bool(re.search(VERBS, low, re.X)) or bool(re.search(r'\b[a-z]{3,}(?:ed|ing)\b', low))
        # BACKTEST CORRECTION (13 Aug 2026). C1 was blocking pure IDENTITY call-outs — "WOMEN IN
        # ACADEMIA" (index 0.77) and "INDIA'S PROFESSORS" (index 0.82) both beat their campaign
        # median and both were rejected. Naming the audience in the giant line is a PROVEN
        # winning pattern (HR identity-led ₹31 vs capability-led ₹421), so it cannot be a
        # blocker. A verbless call-out that names a person or audience is routed to C3, which is
        # the WARN that already exists for exactly this. C1 keeps only the true riddles: verbless
        # lines that name nobody ("ONE PREPARATION. FIVE BOARD ROLES.").
        is_identity = bool(IDENTITY_RX.search(low))
        if not has_verb and '?' not in txt:
            if is_identity:
                pass    # an identity call-out is the TARGET, not a defect. See C23.
            else:
                issues.append(('FAIL', 'C1',
                    f'call-out "{txt}" is a noun-phrase FRAGMENT — no verb, not a question, and '
                    'it names nobody. A stranger cannot decode it on a feed. Write a complete '
                    'sentence or a question: "Board seats are never advertised".'))

        # C2 DEMOTED TO WARN (13 Aug 2026). It runs off a closed noun list that has needed
        # hand-extension for every new product (litigation 30 Jul, arbitration 4 Aug, contracts
        # and consulting 5 Aug, privacy 10 Aug) and still rejected "Law college never taught you
        # tech law." — a complete sentence naming the subject — because "tech law" was not in the
        # list. A rule that fails open on vocabulary it has not met yet must not block a launch.
        if not any(n in low for n in NOUNS):
            issues.append(('WARN', 'C2',
                f'call-out "{txt}" may not name the PRIZE. "Names nothing" means the giant line '
                'contains no concrete thing the reader wants — no board seat, no bail '
                'application, no privacy audit, just an abstraction. Name the thing they walk '
                'away able to do. (This check reads a hand-kept vocabulary list that does not '
                "know every product's words, so a single WARN here is advisory.)"))

        if re.match(r'^\s*(for|to)\s+(professionals|lawyers|people|anyone|those)\b', low):
            issues.append(('WARN', 'C3',
                f'call-out "{txt}" is an AUDIENCE descriptor — it says who, never what they get. '
                'Demote it to the supporting .elig line and give the call-out the destination.'))

        # C5 — a call-out about undefined third parties is a scene, not a promise.
        # "THEY RETIRED. THEN THEY JOINED A BOARD." passes C1/C2 and is still cryptic:
        # the reader is nowhere in it and nothing is offered. Working call-outs either
        # address the reader (you/your, a question, a how-to) or state a usable fact
        # about the prize ("board seats are never advertised").
        vague = re.match(r'^\s*(they|them|some people|some|others|people)\b', low) \
                or re.match(r'^\s*one of\b', low)
        addresses_reader = (re.search(r'\b(you|your|yours)\b', low) or '?' in txt
                            or re.match(r'^\s*how to\b', low))
        if vague and not addresses_reader:
            issues.append(('FAIL', 'C5',
                f'call-out "{txt}" is about vague third parties — the reader is not in it and '
                'nothing is offered. Address the reader ("How to …", "Want …?", "your …") or '
                'state a usable fact about the prize ("Board seats are never advertised").'))

        # C6 — insider vocabulary is cryptic to a cold reader. "NOBODY SEARCHES THE DATABANK
        # FOR YOU" passed C1-C5 and Ramanuj still called it cryptic (27 Jul): a broad-delivery
        # retiree has never heard of the databank. Jargon in a call-out is only right when the
        # ad deliberately targets people who recognise it.
        if re.search(r'\b(databank|iica|nrc|lodr|drhp)\b', low):
            issues.append(('WARN', 'C6',
                f'call-out "{txt}" uses insider vocabulary — cryptic on broad delivery. Keep only if '
                'this ad is a deliberate shibboleth for an audience that already knows the term.'))


        # C28 — kicker describes the reader via their CLIENTS, with no want (15 Aug 2026).
        if cls in ('kicker', 'kick', 'chip', 'elig'):
            if re.search(r'\b(advocates?|lawyers?|accountants?|professionals?|consultants?|'
                         r'engineers?|managers?|secretaries|auditors?|writers?|paralegals?)\s+'
                         r'(for|serving|acting\s+for|working\s+(for|with))\s+\w+', low) \
               and not re.search(r'\bwant|looking\s+(to|for)|ready\s+to|break(ing)?\s+into|'
                                 r'get\s+into|tired\s+of|stuck|\?', low):
                issues.append(('WARN', 'C28',
                    f'kicker "{txt[:60]}" defines the reader through their CLIENTS, not their '
                    'WANT. "Advocates for contractors and employers" reads as a descriptor and '
                    'the want is unclear. Want-frame it: "Advocates who want to get into '
                    'construction arbitration" (Ramanuj, 15 Aug 2026).'))

        # C24 — mechanism-led headline: the product is the subject, the prize is a pronoun.
        if cls in ('callout', 'head') and MECHANISM_RX.search(txt):
            pronoun = bool(PRONOUN_PRIZE_RX.search(txt))
            issues.append(('FAIL' if pronoun else 'WARN', 'C24',
                f'headline "{txt[:70]}" makes the PRODUCT the subject'
                + (' and parks the prize in a pronoun ("…get one")' if pronoun else '')
                + '. The giant line must name what the reader gets: not "6 things this bootcamp '
                  'teaches that help you get one" but "6 things that land you your first '
                  'well-paid remote job".'))

        if len(txt) > 48:
            issues.append(('WARN', 'C4',
                f'call-out is {len(txt)} chars — over ~48 it stops being legible at thumbnail size'))

    return issues

if __name__ == '__main__':
    argv = sys.argv[1:]
    # --product hr|exam|skilling|uk (repeatable) overrides path inference for C16/C17/C19
    forced = None
    while '--product' in argv:
        i = argv.index('--product')
        if i + 1 >= len(argv) or argv[i + 1] not in ('hr', 'exam', 'skilling', 'uk'):
            print('--product needs one of: hr exam skilling uk'); sys.exit(2)
        forced = forced or {'hr': False, 'exam': False, 'skilling': False, 'uk': False}
        forced[argv[i + 1]] = True
        del argv[i:i + 2]
    paths = argv
    if not paths:
        print(__doc__); sys.exit(2)
    total = 0
    for p in paths:
        issues = lint(p, forced)
        fails = [i for i in issues if i[0] == 'FAIL']
        total += len(fails)
        print(f"{'✗' if fails else '✓'} {p}: {len(fails)} FAIL, {len(issues)-len(fails)} WARN")
        for lvl, code, msg in issues:
            print(f'   [{lvl} {code}] {msg}')
    sys.exit(1 if total else 0)
