#!/usr/bin/env python3
r"""Hook rules, fitted against RAMANUJ'S approvals.

WHY THIS FILE WAS REFITTED, 31 Aug 2026
---------------------------------------
It used to be fitted on the Section A split: 24 pairs, 13 approved hooks and 7
rejects, same product and same week. That split is no longer usable as a label.

    "ignore the ones that i approved, they were finally not approved.
     only the ones ramanuj approved became the final ads"

Section A's verdicts are recorded in CAMPAIGN_MAP.md as a bare "APPROVED: pairs
01, 02, ..." with nobody's name against them. They were an in-house call and
those pairs did not ship. So the gate was fitted to labels that did not describe
what Ramanuj actually approves, and it showed:

    the shipped gate blocked 72% of the 123 headlines Ramanuj DID approve.

Rule E alone fired on 82 of 123 (67%). It was not measuring vagueness. It was
measuring the absence of a verb, and the dominant approved headline in this
account is a DESTINATION NOUN PHRASE with no verb at all -- "A global legal
career, from home", "A second innings in US accounting", "Your first US client,
at US rates". SOP/07_AD_COPY.md asks for exactly that: the headline "names the
destination role, never the pain". The rule was penalising the house shape, and
13 content-writing hooks written in one week by one hand could not reveal it.

THE NEW FIT BASIS
-----------------
123 headlines from faces Ramanuj approved or built himself, via `adkit.golden`
(APPROVED/, plus his own RID_BC and Accounting_BC kits). This is 9x the old
evidence and it is correctly labelled.

It is a ONE-CLASS fit, and that is a real limit, stated plainly: there is no
usable negative set. Every rejection recorded in CAMPAIGN_MAP.md is a LANDING
PAGE with no hook text in the corpus, and the only numbered rejections are
Section A's, whose labels are the ones that just failed. So these rules can be
measured for PRECISION -- do they block work Ramanuj approved? -- and cannot
currently be measured for recall. A rule that fires on approved work is noise;
a rule that stays quiet on approved work is merely not-yet-disproved.

    before refit:  72.4% of Ramanuj-approved headlines blocked
    after refit:    4.1%  (A 2.4%, H 1.6%, D 0.8%)

What changed to get there, all of it reported rather than quietly widened:
  * Rule E demoted from BLOCK to advisory (see its docstring for the evidence).
  * CONCRETE and WORK lexicons widened with nouns appearing in >=2 approved
    headlines. The old lists had no vocabulary for law, accounting or board
    work, which is most of what this account sells.
  * Rule A no longer treats `this/that/these/those` as a pronoun when a noun
    follows it. "You already run this meeting" is a determiner, not anaphora.

THE COST, because a refit that only reports its wins is not a fit:
On the OLD Section A split the gate now catches 3 of 7 rejects instead of 6, with
1 false alarm instead of 2. If you believe those labels, the gate got worse. The
whole point is that we no longer believe them.

WHAT PERFORMANCE SAYS, AND WHY IT IS NOT FITTED ON
--------------------------------------------------
Only 13 ads in the repo carry BOTH a hook and a live cost, 7 leads and 6
purchases. The gate flags 0 of the 13 -- it blocks nothing that actually ran,
including the expensive ones. So there is no evidence these rules predict cost,
and 13 points is far too few to fit six regexes without inventing a pattern.
Cost per lead lives in `adkit.corpus --winners` and stays a separate question
from "is this hook vague". Do not merge them until the Meta pull and the hook
corpus overlap on a few hundred ads.

THE CHECKLIST (this is the part that stops a vague hook being written)
----------------------------------------------------------------------
1. Name the thing she walks away with, in a word she already uses.
2. Put her in motion OR name the destination. A destination noun phrase with no
   verb is a first-class approved shape -- this is the correction of 31 Aug 2026.
3. Finish every clause. If the second clause borrows its verb from the first
   ("The reporting did not."), she has to complete the sentence to understand it.
4. If you use "they", "it" or a bare "that", the noun it stands for must appear
   earlier in the hook itself, not merely somewhere on the face.
5. If you set up a contrast, both sides must be things she can picture. "Not how
   much" and "not what you charge for" are variables, not things.
6. A hook may break 1 or 2 only if the device on the face answers it in the same
   glance. Not available to a hook sitting over a decorative device.
7. Both clauses must sit on ONE axis, and the second must correct or complete the
   first. A hook whose first clause is about newsrooms and whose second is about
   businesses is two facts glued together.
8a. RECOGNITION, NOT PROPOSITION. The first clause must be a moment she has lived,
   not a mechanism she has to work out. Point at the physical thing or the minute
   of her day it names. If you cannot point at anything, you have written a
   proposition and she has to decode it. NO rule here tests for this.
9. Name the work, not just the money. Rules G and H gate this.
10. Say whose. "The nap" - whose nap? Human test; approved hooks use bare
   definites freely where the noun is a category she can instantiate.
11. A JOB TITLE IS NOT A JOB. If the head names the destination as a title
   ("the ERP consultant", "the operations advisor", "your name and your subject"),
   a verb somewhere in the head must name work THE READER performs. A verb whose
   subject is the buyer does not count: "the operations advisor a plant brings in
   from outside" has a verb, but the plant is doing it, so the reader still cannot
   say what they would do all day. NO rule here tests for this - telling "the
   consultant who brings a company's cloud bill down" (reader's verb, CLEAR) from
   "the operations advisor a plant brings in" (buyer's verb, UNCLEAR) needs a human.

   Evidence, 23 Sep 2026, SeniorAI_Reach_31Oct-2Nov, blind read of 11 first folds
   (8 new + 3 blinded controls with live cost), one fresh reader each:
     UNCLEAR  01 "Become the ERP consultant mid-sized firms hire direct."
     UNCLEAR  07 "Become the operations advisor a plant brings in from outside."
     UNCLEAR  control si09 "Edtech companies will pay for your name and your subject."
                           (Rs 273/buyer, the dearest of the three controls)
   All three failures are title-only heads, and all three readers gave the same
   reason unprompted: "never says what the actual work is". The eight that passed
   all attach a reader-verb: "brings a company's cloud bill down", "advise them",
   "start a security practice for companies with no security team", "run other
   companies' programmes", "that startups book before they launch".
   Both rewrites were re-read blind and came back CLEAR:
     01 -> "Turn your SAP and Oracle rollouts into your own consulting business."
     07 -> "Start a consulting practice fixing downtime at other plants."
   NOTE the first 01 rewrite, "Run SAP and Oracle rollouts for your own clients",
   also failed: naming the work is necessary but not sufficient, because a bare
   work verb with no destination noun reads as the same job done elsewhere.
11. The second clause must not assert something she can falsify from her chair.

WHAT IS MECHANICAL AND WHAT IS NOT
----------------------------------
Items 7, 8a and 10 are NOT mechanical and are not gates. Both were found by a reader
asking "does that even make sense?", after the four fitted rules passed the hook
clean. A subject-sharing test for item 7 was tried and discarded: it flags the
approved "One-off work ends. Campaigns get renewed.", whose clauses share no
content word at all. Some of this stays a human reading the sentence out loud.

A, B, D, E, G and H ship as BLOCK: together they catch 6 of the 7 rejects (the
seventh, 16, is confounded by a separate faded-type defect) and raise 2 false
alarms on 13 approved hooks. G and H were added on 25 Aug 2026 after a reader
asked "paid to do what?" and "whose form?" of two hooks that every earlier rule
had passed; both fit with zero false alarms. C stays advisory. Rule F was fitted and deleted - see below.
Run this file to see the current fit.

    python hook_rules.py                 score every rule against the split
    python hook_rules.py "<hook text>"   check one or more candidate hooks
    python hook_rules.py --kit <folder>  read <folder>/hooks.md and print the approval table
"""
import pathlib
import re
import sys

# HISTORY, NOT THE FIT. The Section A split, kept so the refit above can be
# re-checked and argued with. These 13 were approved IN-HOUSE and did not ship;
# do not treat them as evidence of what Ramanuj approves.
SECTIONA_INHOUSE_APPROVED = [
    ("01", "Get paid for the campaign, not the word count"),
    ("02", "Your output is already enough to run whole campaigns"),
    ("03", "Paid for your skill, not your word count"),
    ("04", "Learn the other three quarters of a campaign"),
    ("05", "One-off work ends. Campaigns get renewed."),
    ("07", "What you sell is the problem."),
    ("08", "You can own the next campaign"),
    ("09", "Deciding is the job that pays."),
    ("10", "Don't learn to write ads. Unless you want a skill that bills outside school."),
    ("11", "Most writers stop at line one."),
    ("12", "Four jobs. One title."),
    ("14", "Next time they ask what next, send them the link."),
    ("15", "Widen the retainer from posts to whole campaigns."),
]
SECTIONA_INHOUSE_REJECTED = [
    ("06", "They skip portfolios. They read results."),
    ("13", "A campaign has no word count to argue down."),
    ("16", "Graduate with a campaign, not a certificate."),
    ("17", "Three evenings from now, your writing has a number attached."),
    ("18", "You already do the campaign. Nobody calls it that."),
    ("19", "Change what you charge for, not how much."),
    ("24", "They pay you to fix pages."),
]
# 16 is a known confound: simplicity.py --why cites 16_will_you as the evidence for
# rule R1 (body text at .72 opacity, 22px). Its rejection is attributable to faded
# tiny type, so a hook rule that misses 16 is not thereby a worse rule.
CONFOUNDED = {"16"}

PRONOUNS = r"\b(they|them|their|it|its|that|this|those|these)\b"

# Nouns a reader of THIS account can picture. Hand-kept and deliberately narrow:
# ad_lint's C2 carries the same caveat. Widen it when a real product word is
# missing, then re-run the fit and check the split still holds.
CONCRETE = r"""\b(campaign|campaigns|retainer|retainers|client|clients|brief|briefs|
 word\s+count|rate|rates|invoice|invoices|poster|posters|post|posts|piece|pieces|
 byline|portfolio|portfolios|certificate|page|pages|job|jobs|title|link|calendar|
 month|newsroom|newsrooms|desk|desks|salary|skill|skills|ads|ad|report|reports|
 reporter|reporters|reporting|deck|audit|pitch|business|businesses|employer|
 employers|editor|editors|writer|writers|designer|designers|source|sources|story|
 stories|seat|scope|output|work|
 nap|minutes|hour|hours|form|forms|interview|interviews|gap|cv|resume|salary|ctc|
 dietitian|dietitians|dietician|dieticians|nutritionist|nutritionists|practice|
 practices|
 shift|school|child|children|baby|
 draft|drafts|court|hearing|clause|contract|agreement|translation|language|
 design|designs|operations|relationship|relationships|inbox|admin|replies|
 languages|caption|captions|inbox|posting|campus|note|notes|
 # Added 31 Aug 2026, refitting against 123 RAMANUJ-approved headlines instead of
 # the 13 Section A hooks (whose approval was in-house and did not stick). Every
 # word below is a noun in at least two approved headlines. The old list had no
 # vocabulary for law, accounting or board work, which is most of what this
 # account sells, so rule A was firing on "From running companies to governing
 # them" purely because `companies` was missing.
 income|firm|firms|board|boards|director|directors|career|careers|profile|profiles|
 tax|arbitration|paralegal|paralegals|solicitor|solicitors|lawyer|lawyers|law|
 company|companies|team|teams|governance|duty|checklist|route|routes|
 office|offices|dollar|dollars|usd|america|india|people|women|men|
 strategist|strategists|accounting|bookkeeping|payroll|compliance|privacy|
 patent|patents|trademark|litigation|restart|innings|stream|line|lines|
 # Added 21 Sep 2026: 'A CFA candidate who has not built their ...' blocked as a dangling
 # 'their'. candidate is a person noun like director or lawyer, already in this list.
 candidate|candidates|
 # Added 25 Sep 2026: 'Accountants who have finished their day job ...' (us24_notice_evening,
 # Rs 40/lead on 3,463, Sep) blocked as a dangling 'their'. Same gap as candidate.
 accountant|accountants|
 meeting|meetings|city|cities|adviser|advisers|experience|qualification|
 qualifications|degree|degrees|licence|license|quickbooks|tally|xero|gcc|
 smb|smbs|startup|startups|fee|fees|signature|document|documents|filing|filings)\b"""

# A destination the reader cannot picture, because it is a variable rather than a value.
VARIABLE_TO = r"""(what\s+you\s+\w+|how\s+much|how\s+many|a\s+number|the\s+number|
 results|outcomes|value|impact|potential|the\s+difference|the\s+rest)"""

# Verbs that put the READER in motion or money in her hands. Excludes verbs that
# only describe someone else's behaviour, which is why "pay" is absent: "They pay
# you to fix pages" was rejected and describes nothing she does differently.
#
# "become|becomes" added 26 Aug 2026. AD_CREATION_DIRECTOR.md 3.5 fits the headline
# subject test against the DataPrivacy 9-headline split and records "BECOME the Data
# Protection Officer your hospital will need in 2027" and "...your platform will need
# in 2027" as APPROVED - twice - with "become" named as one of the three verbs that
# grammatically relocate the reader to the new role. Rule E was blocking the single
# most strongly evidenced approved shape in the repo. Selftest re-run after adding:
# catches 6/7 rejects, 2/13 false alarms - identical to before, so the fit did not move.
FORWARD = r"""\b(get|gets|learn|own|owns|widen|start|send|run|charge|bill|bills|
 can|will|sell|sells|paid|renewed|write|build|take|plan|price|set|make|keep|land|
 quote|decide|deciding|hire|hires|graduate|stop|become|becomes)\b"""


def r_a_dangling_pronoun(h):
    """A pronoun whose antecedent is not a noun earlier in the hook itself.

    `this`, `that`, `these` and `those` are only pronouns when they stand alone.
    Followed by a noun they are DETERMINERS ("this meeting", "that desk") and
    point at the thing right next to them, which is the opposite of dangling.
    Same for `that` used as a relativiser after a noun ("an income that is
    yours"). Both were false alarms on Ramanuj-approved headlines before this.
    """
    for m in re.finditer(PRONOUNS, h, re.I):
        word = m.group(0).lower()
        # An ALL-CAPS token is an initialism, not a pronoun: "IT", not "it".
        # English does not capitalise pronouns mid-sentence, so the only way this
        # fires is a field name. It blocked `SC_Oct3|w9_06_it_managers`, "Launch
        # your own IT consulting business" - Rs 92 per buyer on 235 buyers,
        # 0.66x its campaign par and one of the ten cheapest faces in the
        # product (measured 1 Oct 2026). The hook itself is skipped only when the
        # token is capitalised and the hook is not shouting in full caps.
        if m.group(0).isupper() and not h.isupper():
            continue
        if word in ("this", "that", "these", "those"):
            after = h[m.end():m.end() + 24]
            # determiner: followed by an optional adjective then a word
            if re.match(r"\s+[a-z]+", after, re.I):
                continue
        if not re.search(CONCRETE, h[:m.start()], re.I | re.X):
            return f'"{m.group(0)}" has no noun before it in the hook'
    return None


def r_b_gapped_clause(h):
    """A clause that borrows its complement from the previous one, so the reader
    has to finish the sentence herself: "The reporting did not." """
    m = re.search(r"\b(did|does|do|is|are|was|were|has|have|had|will|can)\s+not\s*[.!?]",
                  h, re.I)
    return f'"{m.group(0).strip()}" ends the clause with nothing after it' if m else None


def r_c_no_concrete_noun(h):
    if not re.search(CONCRETE, h, re.I | re.X):
        return "no noun the reader can picture"
    return None


def r_d_variable_destination(h):
    """A contrast whose better side is a variable, not a thing."""
    if re.search(r"(,\s*not\b|\binstead of\b|\brather than\b)", h, re.I) \
            or re.match(r"\s*change\b", h, re.I):
        head = re.split(r"(,\s*not\b|\binstead of\b|\brather than\b)", h, flags=re.I)[0]
        if re.search(VARIABLE_TO, head, re.I | re.X):
            return "the better side of the contrast is a variable, not a thing"
    return None


# Nouns that name WORK. A hook may mention money only if it also names the work the
# money is for. This is CONCRETE minus the money words and minus the life-stage words.
WORK = r"""\b(campaign|campaigns|brief|briefs|poster|posters|post|posts|piece|pieces|
 byline|portfolio|portfolios|page|pages|job|jobs|link|report|reports|reporting|deck|
 audit|pitch|story|stories|skill|skills|ads|ad|output|work|calendar|research|
 operations|admin|replies|captions|inbox|design|designs|
 client\s+work|task|tasks|draft|drafts|copy|content|
 # Added 31 Aug 2026, same refit. H fired on 12 of 123 approved headlines, every
 # one of which DOES name the work, in vocabulary this list did not carry:
 # "Your CA-firm experience pays in dollars", "QuickBooks pays more than Tally",
 # "Governance support for US boards, at dollar rates", "Earn in USD after your B.Com".
 # Added 31 Aug 2026 (Academic Writing Wave 1). Rule H blocked
 # "Journals and labs commission systematic reviews from outside writers", which
 # names the work as explicitly as any approved headline does. The lexicon simply
 # carried no academic-writing vocabulary: it had never seen this product line.
 # Same class of gap, and same fix, as the 31 Aug widening recorded above.
 review|reviews|paper|papers|manuscript|manuscripts|writing|writer|writers|
 editing|edit|edits|proofreading|dissertation|dissertations|thesis|theses|
 citation|citations|reference|references|search|searches|summary|summaries|
 syllabus|curriculum|lesson|question|questions|material|materials|module|
 modules|chapter|chapters|proposal|proposals|grant|grants|
 practice|practices|client|clients|firm|firms|board|boards|governance|tax|
 arbitration|law|legal|career|careers|income|paralegal|solicitors|lawyers|
 director|directors|duty|checklist|route|teams|company|companies|business|
 businesses|experience|profile|seat|desk|office|accounting|bookkeeping|payroll|
 compliance|privacy|patent|trademark|litigation|document|documents|filing|
 filings|signature|quickbooks|tally|xero|meeting|meetings|hours|
 com|bcom|ca|cs|cma|llb)\b"""
MONEY = r"\b(paid|pay|pays|rate|rates|charge|charges|price|prices|ctc|salary|earn|earns|fee|fees)\b"


def r_g_promise_with_no_object(h):
    """"Long enough to get paid." Paid to do WHAT? A bare get-paid promise leaves the
    reader holding the question. Approved hooks always attach the object: "Get paid FOR
    the campaign", "Paid FOR your skill". Note this deliberately does not fire on an
    intransitive "the job that pays", which is approved hook 09.
    22 Sep 2026: a currency phrase may sit between "paid" and its object - "Get paid in
    dollars to work on your research specialty" (Academic Writing 08, the reviewer's own
    wording) names the work and was blocked as if it did not."""
    for m in re.finditer(r"\b(?:get|gets|getting|be|being)\s+paid\b", h, re.I):
        after = h[m.end():m.end() + 40]
        if not re.match(r"\s*(?:in\s+(?:dollars|usd|rupees|foreign\s+currency)\s+)?(for|to)\b", after, re.I):
            return '"get paid" with nothing after it - paid to do what?'
    return None


def r_h_money_without_work(h):
    """The hook names a payment but never names the work the payment is for. "Set your
    own rate instead" - a rate to do what? "The nap is ninety minutes. Long enough to
    get paid." - paid for what? Every approved hook that mentions money also names the
    work: campaign, skill, job, posts, retainer-and-campaigns."""
    if re.search(MONEY, h, re.I) and not re.search(WORK, h, re.I | re.X):
        return "names the money but never the work it is for"
    return None


def r_e_no_forward_move(h):
    """DELETED AS A GATE 31 Aug 2026. Kept as an advisory only.

    Refit against 123 Ramanuj-approved headlines: this rule fired on 82 of them,
    67%. It is not measuring vagueness, it is measuring a grammatical shape that
    the house style actively prefers. The dominant approved headline in this
    account is a DESTINATION NOUN PHRASE with no verb at all:

        "A global legal career, from home"
        "A second innings in US accounting"
        "A new revenue stream from the clients you already have"
        "Your first US client, at US rates"

    and SOP/07_AD_COPY.md says exactly that -- the headline "names the destination
    role, never the pain". Rule E was penalising the house shape.

    This is the same disposal rule that removed Rule F, which fired on 8 of 13
    approved hooks: a rule that rejects most of the approved set is worse than no
    rule. The 13-hook Section A split it was fitted on could not see this, because
    all 13 were content-writing hooks written in one week by one hand.
    """
    if not re.search(FORWARD, h, re.I | re.X):
        return "no verb putting the reader in motion (advisory: a destination noun phrase is fine)"
    return None


def r_f_reader_absent(h):
    """The sentence is about somebody else and she is not in it."""
    if re.search(r"\b(you|your)\b", h, re.I):
        return None
    return "the reader is not in the sentence"


# Rule F ("the reader is not in the sentence") was fitted and DELETED: it fired on
# eight of the thirteen approved hooks. Second person is not what separates the two
# groups, and a rule that rejects most of the approved set is worse than no rule.
AUX = ("is", "are", "was", "were", "has", "have", "had", "will", "can",
       "do", "does", "did", "never", "actually", "only", "still")


def r_i_orphan_demonstrative(h):
    """Demonstrative + noun whose noun never appears earlier in the HOOK itself.

    Rule A deliberately skips `that`/`those` + noun, and it is right to: followed
    by a noun they are determiners pointing at the thing beside them, and treating
    them as dangling produced false alarms on Ramanuj-approved headlines. This is a
    narrower case that A cannot see, and it is ADVISORY for exactly that reason.

    Found 3 Sep 2026 by Ramanuj on GlobalPatent wave 2 face 01: *"the molecule on
    the box.... - vague line"*. The head read "The molecule on THAT BOX was searched
    by somebody with your degree." The antecedent lived in the `statement`, which is
    the first move of the PRIMARY TEXT and never appears on the face -- so a scroller
    met a demonstrative pointing at a box nobody had shown her. Nine of ten heads in
    that wave had the same defect, and a blind reader had already said it about one
    of them ("'that reading' points at nothing") without me generalising it.

    The mechanical statement: the `turn` renders ALONE as the big line, so it must be
    readable by somebody who has seen nothing else. If it says "that X" and X is not
    named earlier in the same hook, the reader has to supply X herself.

    Advisory, never blocking: "that desk", "those hours" and similar point at things
    the reader independently owns, and a regex cannot tell those from "that box".
    Read the row and decide.

    MEASURED FIT, 3 Sep 2026, against the same 123 Ramanuj-approved headlines the
    rest of this file is fitted on:

        fires on 1 of 123 approved headlines = 0.8%
        catches 5 of 5 of the wave 2 defect heads

    The single false alarm is "You already run this meeting", which is the exact
    case the module docstring already names as a determiner rather than anaphora --
    she owns the meeting. That is the irreducible limit of a regex here and the
    reason this rule is advisory rather than blocking.

    A first draft fired on 5 of 123 because the relativiser guard only skipped
    auxiliaries: "legal work THAT FITS your schedule" and "a finance seat THAT
    ACTUALLY HIRES" read as orphans. Scoping the verb test to the singular `that`
    and `this` -- `those`/`these` can never be relativisers -- took it to 1, without
    going blind on "those filings", which is the case the rule exists for. The
    SHIPPED GATE (A, B, D, G, H) is unchanged at 4.1%, because this rule is
    advisory and does not enter it.
    """
    for m in re.finditer(r"\b(that|those|these|this)\s+([a-z]+(?:\s+[a-z]+)?)\b", h, re.I):
        dem = m.group(1).lower()
        words = m.group(2).lower().split()
        noun = words[-1]
        before = h[:m.start()].lower()
        # A COMPLETE SENTENCE EARLIER IN THE HEAD IS AN ANTECEDENT. Corrected
        # 3 Sep 2026 after this rule fired on `icp_28_biomedical_devices`,
        # Rs 91.36 -- the cheapest patent ad ever run in this account:
        #     "Medical devices file patents. Learn that work."
        # "that work" points back at the whole preceding sentence, which the
        # reader HAS been given. The standing rule is that where a checker
        # disagrees with an ad that ran cheaply, the ad wins and the checker
        # gets fixed. So the rule now only fires on a demonstrative in the
        # head's FIRST sentence, where nothing precedes it.
        if re.search(r"[.!?]", before):
            continue
        # Relativiser, not a determiner: "an income that is yours", "legal work
        # that fits your schedule", "a seat that actually hires". Only `that` and
        # `this` can do this, never `those`/`these`, so the verb test is scoped to
        # them -- otherwise "those filings" reads as a verb and the rule goes
        # blind on the exact case it was written for.
        if dem in ("that", "this"):
            head_word = words[0]
            nxt = words[1] if len(words) > 1 else ""
            verbish = (head_word in AUX
                       or head_word.endswith("s")
                       or (head_word.endswith("ly") and nxt.endswith("s")))
            if verbish:
                continue
        if noun[:5] and noun[:5] not in before and noun.rstrip("s")[:5] not in before:
            return ('"%s" points at something the head never named'
                    % m.group(0).strip())
    return None


# ---------------------------------------------------------------- rule J data
#
# A demand clause folded into a head is almost always a REDUCED RELATIVE:
#     "draft the contracts US firms outsource"
#      verb  ^--- object ---^  ^subj^  ^demand verb^
# which unpacks to "US firms outsource the contracts". The head reads as English
# only if the demand verb can actually take that object. Twice in one session it
# could not, and every other gate in this repo passed both:
#
#   3 Sep 2026  "draft the contracts US firms CANNOT STAFF"
#               -> "and draft the contracts US firms cannot staff? what does this
#                  sentence even mean?"   You staff a ROLE. Not a contract.
#   4 Sep 2026  "register the companies US firms OUTSOURCE"
#               -> "how do you outsource a firm??"
#               The first repair moved the defect one word over instead of fixing
#               it: OUTSOURCE takes WORK as its object, never an entity, and only
#               loosely an artefact.
#
# So the table below is by object CLASS, not by word:
#
#   entity    a company, a firm, a client -- something with a legal existence
#   artefact  a contract, a filing, a set of papers -- something you hand over
#   work      drafting, registration, research -- an activity
#   role      a seat, a desk, a team -- something a person occupies
#
_OBJ_CLASS = {
    "entity": ("company companies firm firms entity entities subsidiary "
               "subsidiaries corporation corporations client clients startup "
               "startups business businesses"),
    "artefact": ("contract contracts agreement agreements paper papers filing "
                 "filings document documents resolution resolutions form forms "
                 "application applications deed deeds brief briefs draft drafts "
                 "note notes report reports memo memos patent patents"),
    "work": ("work drafting registration filing research review compliance "
             "diligence bookkeeping admin drafting job jobs task tasks"),
    "role": ("seat seats desk desks team teams role roles post posts position "
             "positions chair chairs"),
}
NOUN_CLASS = {w: cls for cls, words in _OBJ_CLASS.items() for w in words.split()}

# What each demand verb can take. Absent from this table = not checked.
VERB_TAKES = {
    "staff":     {"role", "work"},
    "outsource": {"work"},
    "offshore":  {"work"},
    "subcontract": {"work"},
    "send":      {"artefact", "work"},
    "file":      {"artefact"},
    "sign":      {"artefact"},
    "draft":     {"artefact"},
    "register":  {"entity"},
    "incorporate": {"entity"},
    "hire":      {"role"},
}
_VERB_HUMAN = {"entity": "a company", "artefact": "a document",
               "work": "work", "role": "a role"}


def r_j_demand_clause_object(h):
    """Demand verb applied to an object it cannot grammatically take.

    See the table above for the two reports this rule comes from. Both shipped
    on TEN faces at once through all eight gates clean, because nothing in this
    repo asked whether a verb can take its noun -- `hook_rules`, `simplicity`,
    `ad_lint` and `creative_judge` all read the heads as fine.

    BLOCKING. Unlike vagueness, this is not a judgement call: "how do you
    outsource a firm" has one answer and it is "you do not". A head that is not
    a sentence is not a head.

    MEASURED FIT, 4 Sep 2026, against the same 123 Ramanuj-approved headlines
    the rest of this file is fitted on:

        fires on 0 of 123 approved headlines = 0%
        catches 8 of the 10 US Corporate Law wave 2 heads

    The two it does not catch are "register the US companies nobody here is
    trained for" and "draft the US contracts nobody here is trained for". Those
    are not this defect -- "contracts nobody is trained for" is grammatical -- so
    8 of 8 is the honest score, not 8 of 10. It caught both reported heads:
    "draft the contracts US firms cannot staff" and "register the companies US
    firms outsource".

    Deliberately narrow. It only fires when BOTH the object noun and the demand
    verb are in the tables, so an unknown noun or an unlisted verb is silence,
    not a guess. That is why it can be blocking at 0% false alarms.
    """
    # ANCHOR ON THE VERB, NOT ON THE DETERMINER. A first draft matched
    # "<the> <np> <subj> <verb>" left to right and missed
    # "register the companies US firms outsource" entirely: the greedy noun
    # phrase ate "companies US", left "firms" as the subject, read the object as
    # "US", found no class for it and moved on -- and because finditer had
    # already consumed the span, the correct parse was never tried. Anchoring on
    # the demand verb and scanning BACK to the nearest determiner has one parse
    # per verb and no backtracking to lose.
    low = h.lower()
    for m in re.finditer(r"\b([a-z]+)\b", low):
        verb = m.group(1)
        takes = VERB_TAKES.get(verb)
        if not takes:
            continue
        before = low[:m.start()]
        # a sentence boundary means this verb belongs to a different clause
        det = None
        for d in re.finditer(r"\b(?:the|these|those)\b", before):
            det = d
        if det is None or re.search(r"[.!?]", before[det.end():]):
            continue
        span = before[det.end():m.start()].split()
        # the reduced relative is short by construction: object phrase plus a
        # subject of one to three words. Anything longer is a different sentence
        # shape and this rule stays quiet rather than guessing.
        if not span or len(span) > 5:
            continue
        # THE HEAD OF A COMPOUND NOUN IS ITS LAST WORD, not its first. Taking the
        # first known noun read "the COMPANY papers US firms send here" as sending
        # a company, and blocked a head that is fine: the object is "company
        # papers", head "papers", and you can certainly send papers. So group the
        # consecutive known nouns, take the FIRST group -- that is the object
        # phrase, everything after it is the subject -- and use its last word.
        known = [i for i, w in enumerate(span) if w.strip(",") in NOUN_CLASS]
        if not known:
            continue
        group = [known[0]]
        for i in known[1:]:
            if i == group[-1] + 1:
                group.append(i)
            else:
                break
        at = group[-1]
        # the object must actually be followed by a SUBJECT, or this is a plain
        # verb phrase ("register the companies") and not a relative clause
        if at >= len(span) - 1:
            continue
        noun = span[at].strip(",")
        cls = NOUN_CLASS[noun]
        if cls in takes:
            continue
        return ('"the %s ... %s" is not English: you %s %s, not %s'
                % (noun, verb, verb,
                   " or ".join(sorted(_VERB_HUMAN[c] for c in takes)),
                   _VERB_HUMAN[cls]))
    return None


BLOCKING = [("A  dangling pronoun", r_a_dangling_pronoun),
            ("B  gapped clause", r_b_gapped_clause),
            ("D  variable destination", r_d_variable_destination),
            ("G  promise with no object", r_g_promise_with_no_object),
            ("H  money without work", r_h_money_without_work),
            ("J  demand clause object", r_j_demand_clause_object)]
ADVISORY = [("C  no concrete noun", r_c_no_concrete_noun),
            ("E  no forward move", r_e_no_forward_move),
            ("I  orphan demonstrative", r_i_orphan_demonstrative)]
RULES = BLOCKING + ADVISORY


def check_hook(hook):
    """Public entry. Returns (blockers, advisories), each a list of (rule, reason)."""
    b = [(n, r) for n, f in BLOCKING for r in [f(hook)] if r]
    a = [(n, r) for n, f in ADVISORY for r in [f(hook)] if r]
    return b, a



# ---------------------------------------------------------------------------
# Kit mode: hooks are approved as TEXT, in a table, before any image is rendered.
# ---------------------------------------------------------------------------
# Wave 1 of womens_ai_bootcamp averaged 14.1 judge cycles per creative because the hooks
# were settled AFTER layout: two ads were rebuilt on three different chassis before the
# hook was right. Wave 2 gate-tested every hook as plain text first and averaged 6.4.
# This turns that step into an artefact instead of a habit.
#
#     python hook_rules.py --kit <kit-folder>
#
# reads <kit>/hooks.md, runs the shipped gate on every hook and prints the table to put in
# front of the reviewer. One block per ad, order irrelevant:
#
#     ## 51 | EXAM ASPIRANTS
#     statement: Your exam attempt is in March.
#     turn: Take high-paying client work now.
#     axis: the calendar, March against now
#
# `axis` is the human column. Item 7 asks what the two clauses share, and being made to
# write it down is what stops "two facts glued together" reaching a render.
HOOKS_TEMPLATE = (
    "## 51 | EXAM ASPIRANTS\n"
    "statement: Your exam attempt is in March.\n"
    "turn: Take high-paying client work now.\n"
    "axis: the calendar, March against now\n"
)


def kit_table(folder):
    import pathlib
    f = pathlib.Path(folder) / "hooks.md"
    if not f.is_file():
        print("No {}. Write the hooks first, then render.\n".format(f))
        print(HOOKS_TEMPLATE)
        return 2
    blocks, cur = [], None
    for line in f.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s*(\S+)\s*\|\s*(.+?)\s*$", line)
        if m:
            cur = {"n": m.group(1), "icp": m.group(2), "statement": "", "turn": "", "axis": ""}
            blocks.append(cur)
            continue
        kv = re.match(r"^\s*(statement|turn|axis)\s*:\s*(.*)$", line, re.I)
        if kv and cur is not None:
            cur[kv.group(1).lower()] = kv.group(2).strip()
    if not blocks:
        print("{} has no '## <n> | <ICP>' blocks.".format(f))
        return 2

    rows, bad = [], 0
    for b in blocks:
        hook = (b["statement"] + " " + b["turn"]).strip()
        blockers, advisories = check_hook(hook)
        if blockers:
            bad += 1
            note = "; ".join(r for _, r in blockers)
        elif advisories:
            note = "advisory: " + "; ".join(r for _, r in advisories)
        else:
            note = "clean"
        rows.append([b["n"], b["icp"], b["statement"], b["turn"],
                     b["axis"] or "NOT STATED", "BLOCK" if blockers else "ok", note])

    hdr = ["#", "ICP", "Statement", "Turn", "Shared axis", "Gate", "Note"]
    wid = [max(len(str(r[i])) for r in rows + [hdr]) for i in range(len(hdr))]
    line = lambda cells: "| " + " | ".join(str(c).ljust(wid[i]) for i, c in enumerate(cells)) + " |"
    print(line(hdr))
    print("|" + "|".join("-" * (w + 2) for w in wid) + "|")
    for r in rows:
        print(line(r))

    missing = [r[0] for r in rows if r[4] == "NOT STATED"]
    print("\n{} hooks | {} blocked by the fitted rules".format(len(rows), bad))
    if missing:
        print("axis not stated for: " + ", ".join(missing)
              + " - item 7 is a human check and it is the one that catches two facts "
                "glued together")
    print("\nThe gate cannot see items 7, 8a and 10. Read every row out loud before "
          "approving:")
    print("  does the turn answer the statement, is the statement a moment she has lived,")
    print("  and is every 'the X' something she has already been given?")
    return 1 if bad else 0


def ramanuj_headlines(max_words=14):
    """Every headline from a face Ramanuj approved or built himself.

    Sourced through adkit.golden, so the fit basis moves when the approval record
    moves: record a verdict in CAMPAIGN_MAP.md, rebuild GOLDEN, and this refits.
    Headlines longer than `max_words` are dropped -- those rows are prose that the
    corpus parser picked up from a hand-written ad_copy.md, not hooks.
    """
    try:
        sys.path.insert(0, str(pathlib.Path(__file__).parent))
        from adkit import golden
    except Exception:                                  # noqa: BLE001
        return []
    out = set()
    for e in golden.collect():
        h = (e.get("headline") or "").strip()
        if h and len(h.split()) <= max_words:
            out.add(h)
    return sorted(out)


def main():
    if "--kit" in sys.argv:
        i = sys.argv.index("--kit")
        return kit_table(sys.argv[i + 1] if len(sys.argv) > i + 1 else ".")
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        bad = 0
        for h in args:
            b, a = check_hook(h)
            print(f'\n"{h}"')
            for n, r in b:
                print(f"   BLOCK    {n}: {r}")
            for n, r in a:
                print(f"   advisory {n}: {r}")
            if not b and not a:
                print("   clean on every fitted rule")
            bad += len(b)
        return 1 if bad else 0

    print(__doc__)

    heads = ramanuj_headlines()
    if not heads:
        print("  ERROR: could not load Ramanuj-approved headlines via adkit.golden.")
        print("  A fit that cannot see its evidence is not a pass. Fix the import.")
        return 2

    print("FIT: precision against %d headlines Ramanuj approved or built himself."
          % len(heads))
    print("There is no usable negative set, so recall is NOT measured here. See the")
    print("docstring for why, and adkit.corpus --winners for the money question.")
    print("")
    print(f"{'rule':30} {'fires on approved work':26} verdict")
    print("-" * 78)
    for name, fn in RULES:
        hits = [h for h in heads if fn(h)]
        pct = 100.0 * len(hits) / len(heads)
        tag = "BLOCK   " if (name, fn) in BLOCKING else "advisory"
        note = "noise - fix or demote" if (pct > 10 and tag.strip() == "BLOCK") else "ok"
        print(f"{tag} {name:21} {len(hits):4} / {len(heads)}  ({pct:4.1f}%)      {note}")

    blocked = [h for h in heads if check_hook(h)[0]]
    pct = 100.0 * len(blocked) / len(heads)
    print("")
    print(f"SHIPPED GATE (A, B, D, G, H): blocks {len(blocked)}/{len(heads)} "
          f"= {pct:.1f}% of Ramanuj-approved headlines")
    print("  (was 72.4% before the 31 Aug 2026 refit; rule E alone was 67%)")
    for h in blocked:
        print("    still blocked: %s" % h[:70])

    tp = [n for n, h in SECTIONA_INHOUSE_REJECTED if check_hook(h)[0]]
    fp = [n for n, h in SECTIONA_INHOUSE_APPROVED if check_hook(h)[0]]
    print("")
    print(f"OLD Section A split, for reference only (its labels are in-house and did")
    print(f"not stick): catches {len(tp)}/7 rejects {tp}, {len(fp)}/13 false alarms {fp}")
    print("Before the refit that read 6/7 and 2/13. If you trust those labels the gate")
    print("got worse; the refit exists because we do not.")
    print("")
    print("Items 7, 8a and 10 of the checklist are NOT mechanical and no rule tests")
    print("them. A human still has to read the hook out loud.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
