#!/usr/bin/env python3
"""
simplicity.py - the anti-cleverness gate for ad faces.

preflight.py answers "is this compliant". This answers a different question:

    Can a stranger understand this in two seconds, without trying?

Every rule below was derived from a verdict that already happened in this folder, not
from taste. The evidence is named on each rule so it can be argued with.

    python simplicity.py <kit-folder>          # checks html/*.html + ads/*.png
    python simplicity.py <file.html> [...]     # checks named files
    python simplicity.py --why                 # print the rules and their evidence

Exit codes: 0 clean or notes only, 1 BLOCKER present, 2 bad usage.

THE VALIDATION SET - REFITTED 31 Aug 2026
-----------------------------------------
It used to be the Section A split: 24 pairs, 17 approved, 7 not. That split is no
longer usable. Its approvals were made in-house and did not stick:

    "ignore the ones that i approved, they were finally not approved.
     only the ones ramanuj approved became the final ads"

So the rules were fitted to labels that did not describe what Ramanuj approves,
and it showed. Measured against the faces he DID approve:

    blockers fired on 84% of Ramanuj-approved HTML faces (26 of 31)
    blockers fired on  4% of Ramanuj-approved PNGs      (6 of 150)
    and on `banker`, the cheapest Independent Director ad ever run (Rs 60.42)

THE NEW BASIS is two sets, and where they disagree with a rule, THEY WIN:

  1. Faces Ramanuj approved - the ads/src_*.html sources and every PNG under
     APPROVED/. Landing pages and index.html contact sheets are excluded; leaving
     them in made S1 report 1,100-word "faces".
  2. Ads that RAN, with their live cost from the Meta pull, via adkit.golden.
     Ramanuj's own kits are PNG-only, so performance reaches the pixel rules only.

    after the refit: 0% of approved HTML, 0% of approved PNGs, 0 of 10 priced ads.

What moved, all of it reported rather than quietly loosened:
  * S1 was a BLOCK at 100 words. Ramanuj-approved faces run 102 to 191 words,
    median 113 - a duty chart carries more words than a poster. BLOCK moved to
    195, above the heaviest he approved; 100 stays as a FIX, which is what it
    should always have been. The design target is still 40-45.
  * ink_bands, which feeds L3, now requires a band 24-110px tall. Every L3 blocker
    on approved work was a hairline or a tint-block edge, not type - `banker` was
    blocked by an 11px band at 1.1:1.
  * S2 exempts reassurance ("you do not NEED to move"), which is not deficiency
    framing. All three S2 hits on approved faces were of this shape.
  * R1 and R2 exempt CHROME_OWNED - the brand lockup, trust line, date chip and
    CTA. R2 was firing on 34 of 37 approved faces because it policed labels as if
    they were reading matter.

THIS IS A ONE-CLASS FIT, like hook_rules.py. It measures whether a rule blocks
work that was approved or performed. It cannot measure recall: there is no set of
faces Ramanuj rejected with sources in this repo. So --selftest also reports
LIVENESS - whether the blockers still fire anywhere at all - because a gate tuned
until it fires on nothing is not a gate.

    python simplicity.py --selftest
"""

import re
import sys
import pathlib
from collections import Counter
from html.parser import HTMLParser

try:
    from PIL import Image
except ImportError:
    Image = None

# ---------------------------------------------------------------------------
# thresholds - all of them arguable, none of them invented
# ---------------------------------------------------------------------------

# S1. REFITTED 31 Aug 2026 on faces RAMANUJ approved, not on the Section A split.
# The 100-word figure was fitted to Section A, whose approvals were in-house and did
# not stick. Measured against 31 Ramanuj-approved HTML faces, a 100-word BLOCK fired
# on 26 of them - 84%. Their real distribution is 102 to 191 words, median 113: a
# duty chart or a comparison table legitimately carries more words than a poster.
# So the BLOCK moves above the heaviest face he approved, and 100 stays as a FIX,
# which is what it always should have been. The design target is still 40-45.
FACE_WORD_CAP = 100     # S1 FIX. The design target; above this, check it earns the words.
FACE_WORD_BLOCK = 195   # S1 BLOCK. Above the heaviest Ramanuj-approved face (191).
MIN_FONT_RATIO = 0.024  # R2. 26px on a 1080 canvas. BODY text only - see C8_OWNED.

# Classes whose size is ad_lint C8's job, not this file's. C8 hard-fails a call-out or
# head under 64px and a kicker chip under 56px; re-checking them here at 26px would
# report a pass on something C8 rejects.
C8_OWNED = ("callout", "head", "elig", "kicker", "kick")
# Chrome, not body copy: the brand lockup, the trust line, the date chip, the CTA
# and the strapline. R2 fired on 34 of 37 Ramanuj-approved faces (92%) because it
# policed these as if they were reading matter. They are labels, and he approved
# them small. R1 likewise exempts footnote lines, which is where `.trust at .65`
# came from on an approved IP Law face.
CHROME_OWNED = ("brand", "trust", "cta", "datechip", "stamp", "chip", "logi",
                "strap", "pchip", "pt", "dd", "src", "source", "foot", "terms",
                "disclaimer", "logo")
MIN_TEXT_OPACITY = 0.85  # R1.
SAFE_EDGE = 0.035       # L2. Ink closer than this to an edge risks the 1:1 crop.
ALIGN_TOL = 0.012       # L1. Left edges within 1.2% of canvas width count as aligned.

SEV_BLOCK, SEV_FIX, SEV_WARN = "BLOCKER", "FIX", "WARN"


# ---------------------------------------------------------------------------
# rule catalogue - the docstring the team actually reads
# ---------------------------------------------------------------------------

RULES = [
    ("S1", SEV_BLOCK, "More than %d words on the ad face (FIX above %d)."
     % (FACE_WORD_BLOCK, FACE_WORD_CAP),
     'Ramanuj, 21 Aug: "wayy too much text in the ads" / "simplify all, the message is '
     'too complex". Measured: of the six wordiest Section A faces, five were rejected '
     '(16:115, 18:114, 17:114, 24:107, 19:101 words). The one approved at that weight '
     'was 23 at 104.'),
    ("S2", SEV_BLOCK, "Deficiency framing - telling the reader what they have never done.",
     'CLAUDE.md Rule 1, and ad_copy_spec.py says it in the kit\'s own words: "The gap is '
     'always \'nobody has let you near this\', never \'you are deficient\'." Four of the '
     'seven Section A rejects opened with "You have never..." or "You write X. Not what '
     'sells it."'),
    ("S3", SEV_FIX, "The hook points at something that is not on the face.",
     'This is what "cryptic" means mechanically. "Own all four" - four what? "Learn the '
     'rest" - the rest of what? If the noun is not on the face, the reader has to guess, '
     'and they will not.'),
    ("S5", SEV_FIX, "Long or abstract vocabulary in the hook.",
     'Rule 2. Four-syllable words and consultant nouns force a decode step.'),
    ("S6", SEV_BLOCK, "No job title or identity call-out on the face.",
     'CLAUDE.md Rule 2 steps 1 and 2. The reader must recognise themselves in under two '
     'seconds. Memory note, 14 Aug: ICP call-out size is a standing rejection reason.'),
    ("S7", SEV_FIX, "No plain-words definition sentence on the face.",
     'CLAUDE.md Rule 2 step 4, "Never skip this". Not a veto: eye_test, founder_post, '
     'no_number and per_word_both_ways all shipped approved with no definition SENTENCE, '
     'because the hero device itself named the four parts. So this is a prompt to check '
     'that something on the face does the defining - not proof that nothing does.'),
    ("S8", SEV_WARN, "Wordplay, pun, paradox or idiom in the hook.",
     'Ramanuj, 07 Aug: "the flipping burger thing is not clear as a hook - who are you '
     'talking to and why". Cleverness costs the reader a beat they do not spend.'),
    ("S9", SEV_FIX, "More than three stacked text blocks under the hero device.",
     'ad_copy_spec.py, change 3: "those three carried four stacked text blocks under the '
     'device" - listed as a defect being removed.'),
    ("S10", SEV_FIX, "A possessive that points at an unnamed thing: \"the company's CFO\".",
     'User, 28 Sep 2026, on IndependentDirector_Calendar 01: "it says a call with the '
     "company's CFO - which company? which CFO? sounds vague\". S3 only reads the hook and "
     'had no token for it, so a calendar row carried it through all 11 gates and two blind '
     'reads. Possessive only, so a generic "outside the company" in a definition does not '
     'fire. Satisfied when the face first says "a/an/your/this/every ... company".'),
    ("R1", SEV_BLOCK, "Text set at reduced opacity.",
     'Memory note, 14 Aug: no blind-spot grey or small text. NOTE 31 Aug 2026: the '
     'evidence line here does not hold. 16_will_you.html does define '
     '.def{font-size:22px;opacity:.72}, but no element in that file carries '
     'class="def" - it is dead CSS, so R1 never fired on the case it cites and '
     'never could have. The rule is kept because faded body text is a real defect, '
     'but it has no confirmed catch. Do not cite it as fitted.'),
    ("R2", SEV_FIX, "BODY text below %.1f%% of canvas width." % (MIN_FONT_RATIO * 100),
     'A 1080px face renders around 500px in feed, so 26px on the canvas is about 12px in '
     'the eye. Below that it is decoration that costs clarity. SCOPED 24 Aug 2026: the '
     'headline, call-out and kicker are NOT checked here - ad_lint C8 owns those and its '
     'floors are much stricter (call-out and head hard-fail under 64px, kicker chips '
     'under 56px, after Ramanuj asked for "2x bigger" twice). This file had a single '
     '26px floor for everything, which would have passed a 52px headline that C8 fails.'),
    ("L3", SEV_BLOCK, "Measured text contrast below target on the rendered face.",
     'Measured on pixels, not CSS. The CSS version of this check was deleted: it called '
     'six approved ads unreadable because .mark and .pill sit on a dark strip drawn by an '
     'absolutely positioned sibling, which no ancestor walk can find. Gradients and '
     'z-order defeat it the same way. Under 3:1 blocks; 3 to 4.5 is a FIX.'),
    ("L1", SEV_FIX, "Text blocks do not share a left edge.",
     'Reported directly: "content is not properly aligned on the image". Ragged left '
     'edges read as unfinished even when nobody can say why.'),
    ("L2", SEV_FIX, "Text within %.1f%% of the left or right edge." % (SAFE_EDGE * 100),
     'Horizontal only. Top and bottom are deliberate on this chassis (full-bleed bars with '
     'text inside them), and the 1:1 crop question belongs to crop_qa.py - flagging it '
     'here as well fired on all 24 faces and said nothing.'),
]

RULE_BY_ID = {r[0]: r for r in RULES}


# ---------------------------------------------------------------------------
# lexicons
# ---------------------------------------------------------------------------

# S2 - deficiency framing. Second person plus a negated capability.
DEFICIT_RX = [
    re.compile(r"\byou(?:'ve| have)\s+never\b", re.I),
    re.compile(r"\byou\s+never\b", re.I),
    re.compile(r"\byou(?:'re| are)\s+(?:not|n[o']t)\b", re.I),
    # REFITTED 31 Aug 2026. "You do not NEED to move to use it" and "In the camp you
    # do not GUESS" are reassurance - they remove a barrier. Deficiency framing is
    # about what she LACKS. All three S2 hits on Ramanuj-approved faces were
    # reassurance, so the construction is exempted rather than the rule weakened.
    re.compile(r"\byou\s+(?:do\s?n[o']t|don't|cannot|can'?t|won'?t|couldn'?t)\b"
               r"(?!\s+(?:need|have\s+to|has\s+to|require|guess|wait|pay|risk|lose))",
               re.I),
    re.compile(r"\byou\s+lack\b", re.I),
    re.compile(r"\bnobody\s+(?:taught|showed|told)\s+you\b", re.I),
]

# S3 - references that need an antecedent. token -> the nouns that would satisfy it.
DANGLE_TOKENS = [
    (re.compile(r"\ball\s+(two|three|four|five|\d+)\b", re.I), "a list of that many named things"),
    (re.compile(r"\bthe\s+rest\b", re.I), "what the first part was"),
    (re.compile(r"\bline\s+(one|two|1|2)\b", re.I), "the thing that has lines"),
    (re.compile(r"\ba\s+(quarter|third|half)\s+of\s+it\b", re.I), "what 'it' is"),
    (re.compile(r"\bboth\b", re.I), "the two things"),
    (re.compile(r"\bthe\s+other\s+(one|half|side)\b", re.I), "the first one"),
]

# S10 - "the company's CFO": a possessive whose owner the face never introduced.
POSSESSIVE_RX = re.compile(r"\bthe\s+(company|client|firm|startup|business|employer|bank|"
                           r"organisation|organization|fund)(?:'s|’s)\s+\w+", re.I)

# S5 - vocabulary that forces a decode step.
JARGON = {
    "leverage", "leveraging", "optimise", "optimize", "optimisation", "optimization",
    "framework", "frameworks", "ecosystem", "synergy", "holistic", "paradigm",
    "methodology", "utilise", "utilize", "actionable", "scalable", "robust",
    "seamless", "bandwidth", "alignment", "ideate", "operationalise", "monetise",
    "monetize", "disrupt", "disruption", "transformative", "empower", "empowerment",
    "unlock", "unlocking", "delve", "landscape", "journey", "curated", "bespoke",
}

# S8 - decode-step constructions.
DECODE_RX = [
    (re.compile(r"\b(\w+)\s+(?:that\s+)?nobody\s+\1s?\b", re.I), "paradox"),
    (re.compile(r"\bthe\s+(\w+)\s+\1\b", re.I), "word echo"),
    (re.compile(r"\b(?:think|read|guess)\s+again\b", re.I), "riddle"),
    (re.compile(r"\?\s*$"), "rhetorical question with no answer on the face"),
    (re.compile(r"\b(?:tip|top|edge|game|table|ladder|boat|ship|race|door)\s+"
                r"(?:of\s+the\s+iceberg|game|changer)\b", re.I), "idiom"),
    (re.compile(r"\b(?:flip|flipping|burger|hamster\s+wheel|treadmill|rat\s+race)\b", re.I),
     "metaphor the reader must unpack"),
]

# S6 - identity tokens. Anything that names a person by what they do.
ROLE_RX = re.compile(
    r"\b(writer|writers|copywriter|copywriters|journalist|journalists|teacher|teachers|"
    r"lawyer|lawyers|advocate|advocates|secretary|secretaries|engineer|engineers|"
    r"analyst|analysts|consultant|consultants|manager|managers|officer|officers|"
    r"paralegal|paralegals|student|students|graduate|graduates|fresher|freshers|"
    r"freelancer|freelancers|editor|editors|designer|designers|marketer|marketers|"
    r"recruiter|recruiters|accountant|accountants|auditor|auditors|nurse|nurses|"
    r"pharmacist|pharmacists|blogger|bloggers|intern|interns|founder|founders|"
    # dietitian/nutritionist added 26 Aug 2026: real, self-recognised job titles in
    # exactly the same class as nurse and pharmacist, which were already here. The list
    # simply had not met this ICP yet. Re-ran --selftest after adding: unchanged.
    r"dietitian|dietitians|dietician|dieticians|nutritionist|nutritionists|"
    r"translator|translators|interpreter|interpreters|architect|architects|"
    # Added 31 Aug 2026 (Academic Writing Wave 1). S6 blocked "A lecturer on a
    # guest appointment?" - a job title in exactly the same class as teacher,
    # which was already here. The list had never met an academic camp. NOTE the
    # word "academic" is deliberately NOT added: it appears in every face on this
    # product line and would let S6 pass on a face that names no ICP at all.
    r"lecturer|lecturers|professor|professors|scholar|scholars|researcher|"
    r"researchers|tutor|tutors|faculty|librarian|librarians|postgraduate|"
    r"postgraduates|phd|"
    r"aspirant|aspirants|assistant|assistants|associate|associates|"
    r"b\.?com|bba|m\.?com|mba|llb|ca\b|cs\b|hr\b|seo\b|"
    # C-suite and senior titles, added 27 Aug 2026 for the Independent Director
    # bootcamp. Same case the dietitian note above makes: CFO, CHRO, CXO and general
    # counsel are real, self-recognised job titles in the same class as the ones
    # already here; the list had simply never met a camp whose ICPs are senior. Two
    # already-built faces named their reader perfectly ("A CFO or finance head?",
    # "A general counsel or legal head?") and still failed S6.
    # DELIBERATELY NOT ADDED: "director". It is the product's own word and sits in the
    # definition sentence of every ad in this kit, so adding it would make S6 pass
    # vacuously on any face that defines the role.
    # Re-ran --selftest after adding: 1 of 18 before, 1 of 18 after, unchanged.
    r"cfo|cfos|chro|chros|cxo|cxos|coo|cto|counsel|banker|bankers|"
    # Added 17 Sep 2026 (Independent Director chat wave). Same case as the C-suite note
    # above: "A doctor or hospital administrator?", "A CEO or CXO who has run the
    # business?" and "Just retired after a 30-year career" name their reader as plainly
    # as "A CFO or finance head?", and S6 blocked them. `retired` is a life-stage
    # identity in the same class as `homemaker` below, not this product's own word
    # (the product word is "director", still deliberately absent).
    r"ceo|ceos|ctos|doctor|doctors|administrator|administrators|executive|executives|"
    r"retired|retiree|retirees|veteran|veterans|"
    r"professor|professors|principal|principals|"
    # Added 21 Sep 2026 (Tech Law search wave). S6 blocked "A litigator, 2 to 10 years
    # in court?", which names its reader as plainly as "lawyer" and "advocate", already
    # here. Same case as the dietitian note: the list had never met the word.
    r"litigator|litigators|"
    # Added 22 Sep 2026 (Data Protection non-lawyer batch). S6 blocked 16 of 22 faces that
    # name their reader plainly: "A pharmacovigilance professional?", "For logistics and
    # supply chain professionals", "For banking and NBFC operations staff", "An insurance
    # broker or agent?". Same case as the dietitian note: "<field> professional" and
    # "<field> staff" are how these readers describe themselves, and broker and agent are
    # job titles in the same class as banker, already here. None of the four appears in
    # this product's shared definition or take-away rows, so none passes a face vacuously.
    r"professional|professionals|staff|broker|brokers|agent|agents|"
    # Added 24 Sep 2026 (Senior AI "reach" wave). S6 blocked 5 of 8 faces that name
    # their reader in the reader's own words: "ERP and SAP implementation leads",
    # "QA and testing leads", "IT and information security heads", "Plant, power and
    # process operations heads", "Finance and accounts controllers". Same case as the
    # dietitian note: the list had never met an enterprise-IT or plant-operations camp.
    # `controller` goes in bare - it is only ever a job title. `lead` and `head` do NOT,
    # because a bare "leads to" or "the head of the table" would pass a face that names
    # nobody; they are admitted only in the compound forms these readers actually use.
    r"controller|controllers|"
    r"(?:implementation|testing|qa|delivery|technical|team|tech|project|module|"
    r"practice|engineering)\s+leads?|"
    r"(?:security|operations|finance|delivery|practice|technology|engineering|plant|"
    r"project|programme|program|department)\s+heads?|"
    # LABORATORY AND FIELD SCIENCE TITLES, added 3 Sep 2026 (Global Patent wave 2).
    # Exactly the case the dietitian note above makes. `pharmacist`, `nurse` and
    # `dietitian` were already here; the list had simply never met a camp whose ICPs
    # are laboratory scientists. S6 blocked "An M.Sc microbiologist on a QC bench?",
    # which names its reader as precisely as any face in the repo.
    # DELIBERATELY NOT ADDED: "scientist" and "researcher" as bare words are the
    # product line's own vocabulary and appear in the definition sentence of several
    # patent faces, so adding them would let S6 pass on a face naming no ICP at all.
    # (`researcher` is already in the list from the academic-writing addition; that is
    # a different product line, where it is the ICP rather than the product's word.)
    # Re-ran --selftest after adding: ads that ran 10, blocked 0 before and after;
    # liveness 400 PNGs {'L3': 18} before and after. Unchanged.
    # `drafter` added 3 Sep 2026 (US Corporate Law wave 2). It is a real, self-
    # described occupation in exactly the same class as `writer` and `editor`,
    # both of which were already here. S6 blocked "FREELANCE LEGAL DRAFTERS",
    # which names its reader as plainly as any call-out in the repo.
    r"drafter|drafters|"
    r"microbiologist|microbiologists|biologist|biologists|chemist|chemists|"
    r"physicist|physicists|veterinarian|veterinarians|technologist|technologists|"
    r"metallurgist|metallurgists|pharmacologist|pharmacologists|"
    # LIFE-STAGE IDENTITIES, added 25 Aug 2026. The rule's own text says "job title OR
    # identity call-out", but the list only knew job titles, so S6 blocked every ad on a
    # product whose ICPs are life stages rather than occupations: 01_maternity and
    # 08_schoolhours, already built, both failed it while naming their reader perfectly
    # ("ON MATERNITY BREAK, YEAR TWO"). A woman reading "YOUNG MOTHERS" recognises
    # herself in well under two seconds, which is the thing S6 exists to protect.
    # Re-run --selftest after touching this list.
    r"mother|mothers|mum|mums|homemaker|homemakers|housewife|housewives|"
    r"parent|parents|wife|wives|widow|widows|grandmother|grandmothers|"
    r"maternity|career\s+break|back\s+after\s+a\s+break|on\s+a\s+break|"
    r"returning\s+to\s+work|"
    # SHIFT, CARE AND SELF-EMPLOYMENT IDENTITIES, added 2 Oct 2026 (Women AI wave 10).
    # Exactly the case the dietitian and retired notes above make. Run against the
    # call-outs of the ads that ACTUALLY RAN on WomenAI_FREE_3-5Oct, S6 blocked five of
    # eight, including WF_06 "WOMEN ON NIGHT SHIFTS WITH A HEADSET" (825 registrations,
    # 1.07x) and WF_03 "WOMEN CARING FOR FAMILY ALL DAY" (0.80x par). Each term below is
    # how this reader describes herself, and none is this product line's own vocabulary.
    # DELIBERATELY NOT ADDED: "women". It is on every face on this product line and
    # would let S6 pass on a face that names no ICP at all - the same reasoning as
    # "director", "academic" and "scientist" above.
    # Re-ran --selftest after adding; before/after reported in the handover.
    r"carer|carers|caregiver|caregivers|caring\s+for|"
    r"night\s+shifts?|rotating\s+shifts?|roster|rosters|bpo|call\s*cent(?:re|er)s?|"
    r"tuition|salon|salons|beautician|beauticians|"
    r"freelancing|freelance\s+work|showroom|showrooms|"
    r"back\s+to\s+work|left\s+a\s+job|"
    r"stay.at.home)", re.I)

# S7 - the field-definition sentence. "X is ...", "X means ...", "An X is ...".
DEF_RX = re.compile(
    r"\b(?:an?\s+|the\s+)?[a-z][a-z \-]{2,40}?\s+(?:is|are|means)\s+(?:the\s+|a\s+|an\s+)?"
    r"[a-z][a-z]", re.I)

VOWEL_GROUPS = re.compile(r"[aeiouy]+")


def syllables(word):
    w = word.lower().strip(".,;:!?'\"()")
    if not w:
        return 0
    n = len(VOWEL_GROUPS.findall(w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


# ---------------------------------------------------------------------------
# a very small DOM, enough to answer "what colour is this text on"
# ---------------------------------------------------------------------------

class Node(object):
    __slots__ = ("tag", "classes", "style", "parent", "kids", "text")

    def __init__(self, tag, classes, style, parent):
        self.tag, self.classes, self.style = tag, classes, style
        self.parent, self.kids, self.text = parent, [], ""


VOID = {"br", "img", "hr", "meta", "link", "input", "source"}


class Tree(HTMLParser):
    """Builds a node tree and keeps the <style> block."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("root", [], "", None)
        self.cur = self.root
        self.css = []
        self._skip = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip = tag
            return
        if tag == "br":
            # A <br> is a word break. Dropping it silently glued the words on either
            # side together, so a call-out written "ERP and SAP<br>implementation leads"
            # flattened to "SAPimplementation leads" and S6's compound job titles could
            # never match (24 Sep 2026). Every kit that wraps a call-out is affected.
            self.cur.text += " "
            return
        if tag in VOID:
            return
        cls = a.get("class", "").split()
        n = Node(tag, cls, a.get("style", ""), self.cur)
        self.cur.kids.append(n)
        self.cur = n

    def handle_endtag(self, tag):
        if self._skip == tag:
            self._skip = None
            return
        if tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        if self._skip == "style":
            self.css.append(data)
        elif self._skip is None:
            self.cur.text += data


CSS_RULE_RX = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
DECL_RX = re.compile(r"([a-z\-]+)\s*:\s*([^;]+)")
HEX_RX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")


def parse_css(css_text):
    """selector-class -> {prop: value}. Only simple .class and tag selectors."""
    out = {}
    for sel_blob, body in CSS_RULE_RX.findall(css_text):
        decls = {}
        for prop, val in DECL_RX.findall(body):
            decls[prop.strip()] = val.strip()
        if not decls:
            continue
        for sel in sel_blob.split(","):
            sel = sel.strip()
            if not sel or " " in sel or ":" in sel:
                continue
            out.setdefault(sel, {}).update(decls)
    return out


def props_for(node, css):
    p = {}
    p.update(css.get(node.tag, {}))
    for c in node.classes:
        p.update(css.get("." + c, {}))
    if node.style:
        for prop, val in DECL_RX.findall(node.style):
            p[prop.strip()] = val.strip()
    return p


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def first_hex(val):
    m = HEX_RX.search(val or "")
    return hex_to_rgb(m.group(0)) if m else None


def effective_bg(node, css, default):
    n = node
    while n is not None:
        p = props_for(n, css)
        for key in ("background-color", "background"):
            c = first_hex(p.get(key, ""))
            if c:
                return c
        n = n.parent
    return default


def px(val):
    m = re.match(r"\s*(\d+(?:\.\d+)?)\s*px", val or "")
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# finding on the face
# ---------------------------------------------------------------------------

FOOT_CLASSES = ("foot", "footrow", "brandrow", "terms", "fterm", "legal", "src", "source")


def in_footer(node):
    n = node
    while n is not None:
        for c in getattr(n, "classes", []):
            if c in FOOT_CLASSES:
                return True
        n = n.parent
    return False


def iter_nodes(n):
    yield n
    for k in n.kids:
        for d in iter_nodes(k):
            yield d


def visible_text(node):
    return " ".join(n.text for n in iter_nodes(node)).split()


def canvas_width(css):
    for sel in (".canvas", "body", "html"):
        w = px(css.get(sel, {}).get("width", ""))
        if w:
            return w
    return 1080.0


def pick_hook(root, css, cw):
    """The biggest run of text on the face is the hook."""
    best, best_size = None, -1.0
    for n in iter_nodes(root):
        own = n.text.strip()
        if len(own) < 4:
            own = " ".join(k.text for k in n.kids).strip()
        if len(own) < 4:
            continue
        size = px(props_for(n, css).get("font-size", "")) or 0.0
        if size > best_size:
            best, best_size = n, size
    if best is None:
        return "", 0.0
    txt = " ".join(" ".join(x.text for x in iter_nodes(best)).split())
    return txt, best_size


# ---------------------------------------------------------------------------
# the checks
# ---------------------------------------------------------------------------

def check_html(path):
    """Returns a list of (rule_id, severity, detail)."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    t = Tree()
    t.feed(raw)
    css = parse_css("\n".join(t.css))
    cw = canvas_width(css)
    body_bg = first_hex(css.get("body", {}).get("background", "")) \
        or first_hex(css.get("body", {}).get("background-color", "")) \
        or (255, 255, 255)

    words = visible_text(t.root)
    face = " ".join(words)
    hook, hook_size = pick_hook(t.root, css, cw)
    out = []

    # ---- S1 volume
    if len(words) > FACE_WORD_BLOCK:
        out.append(("S1", SEV_BLOCK,
                    "%d words on the face, hard limit is %d. Cut %d. No face Ramanuj "
                    "approved is this heavy - the heaviest is 191."
                    % (len(words), FACE_WORD_BLOCK, len(words) - FACE_WORD_BLOCK)))
    elif len(words) > FACE_WORD_CAP:
        out.append(("S1", SEV_FIX,
                    "%d words on the face, design target is %d and 40-45 is the aim. "
                    "Ramanuj-approved faces run to 191, but every one of those is a "
                    "chart or a table. Check this one earns the words."
                    % (len(words), FACE_WORD_CAP)))

    # ---- S2 deficiency framing
    for rx in DEFICIT_RX:
        m = rx.search(face)
        if m:
            out.append(("S2", SEV_BLOCK,
                        'reads "%s" - that tells the reader what they lack. '
                        "Say what nobody has let them near instead." % m.group(0)))
            break

    # ---- S3 dangling reference in the hook
    for rx, wants in DANGLE_TOKENS:
        m = rx.search(hook)
        if not m:
            continue
        rest = face.replace(hook, " ")
        # satisfied if the face names 2+ concrete nouns after the hook
        nouns = re.findall(r"\b(ad|ads|page|pages|email|emails|tracking|brief|briefs|"
                           r"campaign|campaigns|landing page|report|reports|invoice|"
                           r"rate|rates|client|clients)\b", rest, re.I)
        if len(set(n.lower() for n in nouns)) < 2:
            out.append(("S3", SEV_FIX,
                        '"%s" in the hook, but the face never names %s.'
                        % (m.group(0), wants)))
            break

    # ---- S10 a possessive that points at something the face never named
    for m in POSSESSIVE_RX.finditer(face):
        noun = m.group(1).lower()
        intro = re.compile(r"\b(?:a|an|one|your|this|that|every|each|any|their)\s+"
                           r"(?:[\w'-]+\s+){0,2}%ss?\b" % re.escape(noun), re.I)
        if not intro.search(face[:m.start()]):
            out.append(("S10", SEV_FIX,
                        'reads "%s" but the face never says which %s. Anchor it to '
                        "something on the face, or name the kind." % (m.group(0), noun)))
            break

    # S4 (hook length) was removed 24 Aug 2026. ad_lint C4 already fails a call-out
    # over ~48 chars, which is tighter than the 65 this used, and it is the rule the
    # team already argues with. Two checkers reporting the same defect at different
    # numbers is worse than one.

    # ---- S5 vocabulary
    hard = [w for w in hook.split()
            if w.lower().strip(".,;:!?'\"()") in JARGON or syllables(w) >= 4]
    if hard:
        out.append(("S5", SEV_FIX, "hard words in the hook: %s" % ", ".join(sorted(set(hard)))))

    # ---- S6 identity
    if not ROLE_RX.search(face):
        out.append(("S6", SEV_BLOCK,
                    "no job title anywhere on the face. The reader cannot recognise "
                    "themselves."))

    # ---- S7 field definition
    if not DEF_RX.search(face):
        out.append(("S7", SEV_FIX,
                    "no plain 'X is ...' sentence on the face. Either add one, or "
                    "confirm the hero device itself names the parts of the job."))

    # ---- S8 decode step
    for rx, what in DECODE_RX:
        if rx.search(hook):
            out.append(("S8", SEV_WARN, "%s in the hook: %r" % (what, hook[:70])))
            break

    # ---- S9 stacked text blocks
    stage = [n for n in iter_nodes(t.root) if "stage" in n.classes]
    if stage:
        after, seen = 0, False
        for n in iter_nodes(t.root):
            if n is stage[0]:
                seen = True
                continue
            if not seen or in_footer(n):
                continue
            if len(n.text.strip()) > 12 and n.tag in ("div", "p", "h1", "h2", "span"):
                after += 1
        if after > 3:
            out.append(("S9", SEV_FIX,
                        "%d text blocks under the hero device, cap is 3." % after))

    # ---- R1 / R2 / R3 per text element
    faded, small = [], []
    for n in iter_nodes(t.root):
        txt = n.text.strip()
        if len(txt) < 3:
            continue
        p = props_for(n, css)
        label = ("." + n.classes[0]) if n.classes else n.tag

        op = p.get("opacity")
        if op:
            try:
                if float(op) < MIN_TEXT_OPACITY and not any(
                        c in CHROME_OWNED for c in n.classes):
                    faded.append("%s at %s" % (label, op))
            except ValueError:
                pass

        size = px(p.get("font-size", ""))
        if (size and size < MIN_FONT_RATIO * cw and not in_footer(n)
                and not any(c in C8_OWNED for c in n.classes)
                and not any(c in CHROME_OWNED for c in n.classes)):
            small.append("%s at %dpx" % (label, int(size)))

    if faded:
        out.append(("R1", SEV_BLOCK, "; ".join(sorted(set(faded))[:4])))
    if small:
        out.append(("R2", SEV_FIX, "; ".join(sorted(set(small))[:5])))

    return out


# ---------------------------------------------------------------------------
# pixel checks
# ---------------------------------------------------------------------------

def ink_bands(img, tol=26):
    """Rows of the image that contain ink, grouped into blocks."""
    w, h = img.size
    px_ = img.load()
    bg = Counter(px_[x, y] for x in range(0, w, 7) for y in range(0, h, 7)).most_common(1)[0][0]

    rows = []
    for y in range(h):
        left, right = None, None
        for x in range(w):
            if abs(px_[x, y] - bg) > tol:
                if left is None:
                    left = x
                right = x
        rows.append((left, right))

    bands, cur = [], None
    gap = 0
    for y, (l, r) in enumerate(rows):
        if l is None:
            gap += 1
            if cur and gap > 7:
                bands.append(cur)
                cur = None
            continue
        gap = 0
        if cur is None:
            cur = [y, y, l, r]
        else:
            cur[1] = y
            cur[2] = min(cur[2], l)
            cur[3] = max(cur[3], r)
    if cur:
        bands.append(cur)
    # A band must be a plausible LINE OF TYPE. Refitted 31 Aug 2026: every L3
    # BLOCKER on Ramanuj-approved work was a band that is not text - hairlines and
    # tint-block edges at 11, 16, 16, 21 and 22 px, and two 119/120px slabs of
    # near-uniform colour. `banker`, the cheapest Independent Director ad ever run
    # at Rs 60.42, was blocked by an 11px band at 1.1:1. Ramanuj and live cost win
    # over the rule, so the rule learns what a line of type looks like: at least
    # 24px (below the 26px body floor nothing readable exists) and at most 110px
    # (taller than that on a 1350px canvas is a panel, not a line).
    return [b for b in bands if 24 <= (b[1] - b[0]) <= 110]


def band_contrast(rgb, band, w):
    """Modal colour in the band is the background; the most distant frequent colour is
    the ink. Returns None for anything that looks like artwork rather than type."""
    y0, y1, x0, x1 = band
    box = rgb.crop((x0, y0, min(x1 + 1, w), y1 + 1))
    box = box.resize((max(1, box.width // 2), max(1, box.height // 2)))
    try:
        pixels = list(box.get_flattened_data())
    except AttributeError:                  # Pillow < 12
        pixels = list(box.getdata())
    quant = [(r // 24 * 24, g // 24 * 24, b // 24 * 24) for r, g, b in pixels]
    hist = Counter(quant)
    if len(hist) > 48:                       # a photograph, not a text block
        return None
    bg, bg_n = hist.most_common(1)[0]
    total = sum(hist.values())
    if bg_n / float(total) < 0.35:           # no dominant ground: not type on a field
        return None
    ink, best = None, -1.0
    for col, n in hist.items():
        if n / float(total) < 0.015:
            continue
        d = abs(luminance(col) - luminance(bg))
        if d > best:
            ink, best = col, d
    if ink is None or best < 0.02:
        return None
    return contrast(ink, bg), ink, bg


def check_png(path):
    if Image is None:
        return []
    out = []
    src = Image.open(path).convert("RGB")
    img = src.convert("L")
    w, h = img.size
    bands = ink_bands(img)
    if not bands:
        return out

    # Full-bleed bands are chassis - dark strips, rules, hero art. Only the narrower
    # bands are type, and only type has to respect the margin or share an edge.
    text_bands = [b for b in bands
                  if (b[3] - b[2]) < 0.94 * w and (b[3] - b[2]) > 0.12 * w]

    # ---- L2 horizontal bleed only. Vertical is deliberate here: this chassis runs
    #      full-bleed bars top and bottom with their text inside them, and the 1:1 crop
    #      question belongs to judging-static-ads/engine/crop_qa.py, which owns it.
    mx = SAFE_EDGE * w
    hits = []
    if any(b[2] < mx for b in text_bands):
        hits.append("left (x=%d)" % min(b[2] for b in text_bands))
    if any(b[3] > w - mx for b in text_bands):
        hits.append("right (x=%d of %d)" % (max(b[3] for b in text_bands), int(w)))
    if hits:
        out.append(("L2", SEV_FIX, "text bleeds to the edge on: %s" % ", ".join(hits)))
    if len(text_bands) >= 3:
        lefts = sorted(b[2] for b in text_bands)
        clusters, tol = [], ALIGN_TOL * w
        for v in lefts:
            if clusters and v - clusters[-1][-1] <= tol:
                clusters[-1].append(v)
            else:
                clusters.append([v])
        centred = sum(1 for b in text_bands
                      if abs(b[2] - (w - b[3])) < 0.02 * w)
        # A single stray block on its own edge is not a misalignment pattern - on the
        # chart-based faces (cw_10b/c/d/e, all approved) those two strays are the axis
        # number row and the axis title, which are not body text and never line up with
        # it. Only an edge that two or more blocks share counts as a competing edge.
        clusters = [c for c in clusters if len(c) >= 2]

        if len(clusters) > 2 and centred < len(text_bands) - 1:
            by_edge = []
            for c in clusters:
                ys = [b for b in text_bands if c[0] <= b[2] <= c[-1]]
                by_edge.append("x=%d (%d block%s: %s)"
                               % (int(c[0]), len(ys), "" if len(ys) == 1 else "s",
                                  " ".join("y%d" % b[0] for b in ys[:4])))
            out.append(("L1", SEV_FIX,
                        "%d text blocks on %d left edges. %s. Snap them to one."
                        % (len(text_bands), len(clusters), "; ".join(by_edge))))

    # ---- L3 measured contrast, per text band
    bad, dim = [], []
    for b in text_bands:
        r = band_contrast(src, b, w)
        if r is None:
            continue
        ratio, ink, bg = r
        where = "y=%d-%d" % (b[0], b[1])
        if ratio < 3.0:
            bad.append("%s %.1f:1 %s on %s" % (where, ratio, ink, bg))
        elif ratio < 4.5:
            dim.append("%s %.1f:1" % (where, ratio))
    if bad:
        out.append(("L3", SEV_BLOCK, "; ".join(bad[:4])))
    if dim:
        out.append(("L3", SEV_FIX, "; ".join(dim[:5])))
    return out


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------

SKIP = re.compile(r"^(index|contact|preview|_)", re.I)


def collect(target):
    p = pathlib.Path(target)
    if p.is_file():
        return [p]
    jobs = []
    for sub in ("html", "ads", "."):
        d = p / sub if sub != "." else p
        if not d.is_dir():
            continue
        for f in sorted(list(d.glob("*.html")) + list(d.glob("*.png"))):
            if not SKIP.match(f.name):
                jobs.append(f)
        if jobs:
            break
    return jobs


def stem_key(p):
    m = re.match(r"(?:cw_)?(\d+)", p.stem)
    return m.group(1).zfill(2) if m else p.stem


def run(targets):
    findings = {}
    for t in targets:
        for f in collect(t):
            try:
                res = check_html(f) if f.suffix == ".html" else check_png(f)
            except Exception as exc:                      # a broken file is a finding
                res = [("!!", SEV_WARN, "could not read: %s" % exc)]
            if res:
                findings.setdefault(stem_key(f), []).append((f, res))

    n_block = 0
    for key in sorted(findings):
        for f, res in findings[key]:
            print("\n%s" % f)
            for rid, sev, detail in res:
                if sev == SEV_BLOCK:
                    n_block += 1
                title = RULE_BY_ID[rid][2] if rid in RULE_BY_ID else ""
                print("  %-7s %s  %s" % (sev, rid, title))
                print("          %s" % detail)

    print("\n%s" % ("-" * 70))
    if n_block:
        print("%d BLOCKER(s). Not ready to send." % n_block)
        print("Run  python simplicity.py --why  for the evidence behind each rule.")
        return 1
    print("No blockers.")
    return 0


def why():
    print(__doc__)
    for rid, sev, title, evidence in RULES:
        print("%s  %-8s %s" % (rid, sev, title))
        for line in re.findall(r".{1,74}(?:\s|$)", evidence):
            print("            %s" % line.strip())
        print("")
    return 0


def approved_faces():
    """Faces RAMANUJ approved: the HTML sources shipped inside APPROVED/ as
    ads/src_*.html, and every PNG under APPROVED/**/ads/.

    Landing pages and index.html contact sheets are excluded - they are not ad
    faces, and including them made S1 report 1,100-word "faces".
    """
    root = pathlib.Path(__file__).parent / "APPROVED"
    html, png = [], []
    if not root.is_dir():
        return html, png
    for f in root.rglob("*.html"):
        if f.name.startswith("lp_") or f.name == "index.html":
            continue
        if "landing_pages" in f.parts:
            continue
        html.append(f)
    png = sorted(root.rglob("ads/*.png"))
    return sorted(html), png


def performing_ads():
    """Faces that RAN, with their live cost. Ramanuj's own kits are PNG-only, so
    only the pixel rules reach them - which is the half that matters here, since
    `banker` at Rs 60.42 was being blocked by a contrast rule."""
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).parent))
        from adkit import golden
    except Exception:                                     # noqa: BLE001
        return []
    out = []
    for e in golden.collect():
        if not e.get("live"):
            continue
        q = pathlib.Path(e["path"])
        if q.suffix.lower() == ".png" and q.exists():
            out.append((e["live"]["cost"], e["live"]["family"], e["name"], q))
    return sorted(out)


def selftest():
    """Fit against RAMANUJ'S APPROVALS and against ads that actually ran.

    THE RULE THAT DECIDES CONFLICTS, stated 31 Aug 2026: Ramanuj and past
    performance win. A blocker that fires on a face he approved, or on an ad that
    ran cheaply, is a defect in the rule - not in the face.
    """
    html, png = approved_faces()
    if not html and not png:
        print("  ERROR: APPROVED/ not found. A fit that cannot see its evidence")
        print("  is not a pass.")
        return 2

    print("  FIT BASIS 1 - faces Ramanuj approved. Expect ZERO blockers.")
    hb = Counter()
    nh = 0
    for f in html:
        blk = [r for r in check_html(f) if r[1] == SEV_BLOCK]
        if blk:
            nh += 1
            print("    BLOCKED  %-40s %s" % (f.name[:40], blk[0][0]))
        for r in blk:
            hb[r[0]] += 1
    print("    html faces: %d, blocked %d (%.0f%%). Was 84%% before the 31 Aug refit."
          % (len(html), nh, 100.0 * nh / max(1, len(html))))

    pb = Counter()
    npg = 0
    for q in png:
        blk = [r for r in check_png(q) if r[1] == SEV_BLOCK]
        if blk:
            npg += 1
            print("    BLOCKED  %-40s %s" % (q.name[:40], blk[0][0]))
        for r in blk:
            pb[r[0]] += 1
    print("    png faces:  %d, blocked %d (%.0f%%). Was 4%% before the refit."
          % (len(png), npg, 100.0 * npg / max(1, len(png))))

    print("")
    print("  FIT BASIS 2 - ads that RAN, cheapest first. Expect ZERO blockers.")
    perf = performing_ads()
    nperf = 0
    for cost, fam, name, q in perf:
        blk = [r for r in check_png(q) if r[1] == SEV_BLOCK]
        if blk:
            nperf += 1
        print("    Rs %-8.2f %-9s %-34s %s"
              % (cost, fam, name[:34], ",".join(r[0] for r in blk) or "clean"))
    print("    ads that ran: %d, blocked %d. `banker` at Rs 60.42 was blocked by L3"
          % (len(perf), nperf))
    print("    before the refit - an 11px hairline read as low-contrast type.")

    print("")
    print("  LIVENESS - a gate tuned until it fires on nothing is not a gate.")
    live = Counter()
    scanned = 0
    for q in list((pathlib.Path(__file__).parent).rglob("ads/*.png"))[:400]:
        scanned += 1
        for r in check_png(q):
            if r[1] == SEV_BLOCK:
                live[r[0]] += 1
    print("    %d PNGs across the repo: %s"
          % (scanned, dict(live) if live else "NOTHING - the rules are dead, fix them"))

    bad = nh + npg + nperf
    print("")
    if bad:
        print("  %d conflict(s) with Ramanuj or with live performance. Those win:" % bad)
        print("  fix the rule, not the face.")
    else:
        print("  No blocker fires on approved work or on an ad that ran, and the")
        print("  blockers still fire elsewhere in the repo.")

    print("")
    print("  Section A, the OLD basis, is no longer used: its approvals were made")
    print("  in-house and did not stick. See hook_rules.py for the same correction.")
    return 1 if bad else 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == "--why":
        return why()
    if argv[1] == "--selftest":
        return selftest()
    args = argv[1:]
    if args and args[0] == "--word-cap":
        # Sets the FIX threshold only. Since the 31 Aug 2026 refit the BLOCK lives at
        # FACE_WORD_BLOCK (195, above the heaviest face Ramanuj approved), so this
        # flag no longer decides whether a kit passes - it decides when the advisory
        # appears. The per-kit `.word-cap` escape hatch check_all.py carries is
        # therefore mostly redundant now; it stays because a kit that has argued for
        # a richer template should still be able to silence the advisory rather than
        # read past it. Pass it only when you can name which template earned the
        # number, and record that in the kit's value_props.md or README.
        if len(args) < 2:
            print("Usage: python simplicity.py --word-cap <n> <folder-or-files>")
            return 2
        global FACE_WORD_CAP
        FACE_WORD_CAP = int(args[1])
        old = RULE_BY_ID["S1"]
        RULE_BY_ID["S1"] = (old[0], old[1],
                             "More than %d words on the ad face." % FACE_WORD_CAP, old[3])
        args = args[2:]
    return run(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
