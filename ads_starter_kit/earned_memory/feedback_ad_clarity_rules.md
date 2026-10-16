---
name: feedback-ad-clarity-rules
description: "Eight-point ad legibility/clarity bar Ramanuj/Ruchika gave on 14 Aug 2026, plus the 21 Aug bed-and-bathroom callout test - applies to all ad creative in this project, on top of CLAUDE.md Rules 1/2."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7683fe6f-af49-4571-9d73-80254c30bed3
  modified: 2026-08-25T11:22:25.531Z
---

Standing ad-creative quality bar for LawSikho/SkillArbitrage work, given 14 Aug 2026,
additive to the Rule 1 (better career, never threaten) and Rule 2 (no assumed knowledge)
judgment calls already in the project's `CLAUDE.md`:

1. **ICP callout must be unmissable.** Big font, high contrast, no doubt about "is this for
   me." Not a small caption.
2. **No wordplay in the main heading.** The reader may be sleepy, distracted, or scrolling
   in the washroom - the heading must decode in microseconds, not require decoding at all.
   No clever double-meanings.
3. **Value proposition visible at first glance.** First look must tell the reader what is
   being offered concretely (e.g. "earn a second income as a teacher," not an abstract
   promise).
4. **Nothing important goes in a blind spot.** No grey color, no micro font, and nothing
   placed *above* the heading expecting to be read - readers read the heading then look
   below it, never above it.
5. **ICP must be a real, self-recognized identity**, not an invented demographic label.
   Rejected example: "women looking to learn AI skills" (nobody identifies that way).
6. **Good heading pattern (approved example):** "5 AI skills for women who want to finish
   their work faster" - literal, numbered/concrete, names the audience and the outcome.
7. Reiterates 2/3: value proposition clarity is non-negotiable, checked explicitly before
   handoff.
8. Reiterates 4: good content must never be buried in a blind spot by styling it small/grey.

## The bed-and-bathroom test (21 Aug 2026) - RUN ON EVERY AD, EVERY TIME

Asked to be made a **baseline check for any ad generated in this project**: *"for someone
scrolling in bed or the bathroom - can they immediately identify if this is for them or
not?"* Apply it to the ICP callout specifically, before anything else is judged. Two
failure modes surfaced on the same batch, both now disqualifying:

- **The callout must name WHO they are, not only their situation.** A callout that is
  purely circumstantial ("WRITING 20 ARTICLES A MONTH", "THREE YEARS. SAME RATE PER WORD")
  has no identity anchor, and on a fast scroll the identity lands before the circumstance.
  Fixed to "CONTENT WRITERS PAID PER ARTICLE" / "CONTENT WRITERS WHOSE RATE NEVER MOVES".
- **Any situation attached to the identity must be UN-CHECKABLE.** A specific number is a
  checkable claim, and a checkable claim gets checked and failed - a writer doing 8 or 40
  articles a month reads "20 articles a month" and thinks *not me*. The approved senior
  ads never do this: "SENIOR PROFESSIONALS", "RETIRING IN THE NEXT 5 YEARS" both have
  generous edges that let a wide band self-identify.
- Related: **passive/elided grammar flips the meaning.** "Content writers asked for an
  'AI discount'" parses as *the writers are asking*, because the reader will not supply
  the elided "who were". And coined terms in scare quotes are a decode instruction.
- **Widen laterally, never upward.** Qualifier rows may add sibling identities at the same
  rung (CONTENT WRITERS · COPYWRITERS · SEO WRITERS). They must NOT include the aspiration
  label - putting "strategist" in a content-writing ICP band names the destination as the
  starting identity and collapses the ladder the ad is selling.

Structural consequence: when a callout is being asked to name the audience *and* describe
the situation at once, it does neither. Split them - identity in the callout band, situation
in the headline directly below. See `ContentWriting_SectionA_29-31Aug/gen_ads.py`.

**Why:** Recurring rejection pattern named directly by the user (quoting Ramanuj) as
"problems in ads" that keep recurring and need to be "simplified greatly." Distinct from,
and additive to, the Rule 1/Rule 2 content judgment calls already documented in
`CLAUDE.md` - those are about *what* the ad offers/how cryptic it is; this set is about
*visual hierarchy and legibility* of whatever copy is chosen.

**How to apply:** Treat as a mechanical layout checklist for every ad face going forward,
same spirit as `preflight.py` for the compliance rules: callout huge and solid, heading
literal, value prop stated plainly and again in an offer block, nothing meaningful under
24px or in grey, and the bed-and-bathroom test passed on the callout before anything else
is reviewed. Worth proposing as a formal addition to `CLAUDE.md` (a "Rule 6") if it keeps
recurring across kits, since CLAUDE.md is checked into the repo and this is not yet written
down anywhere durable. See also [[feedback_ad_creative_use_real_images]] and
[[feedback_ad_creative_vary_composition]].

## Vocabulary and audience-width failures (21 Aug 2026)

Three rejections in one session, all the same root cause: the ad was written in my
words rather than the reader's, or the callout promised a wider audience than the
line under it served.

- **Use the reader's own vocabulary, never invented shorthand.** Rejected: "PIECES RUN
  OUT" (no writer calls their own output a "piece") and "BOOKED / NOT BOOKED" (a salon
  and studio word; a content writer says they have work or they do not). Fixed to
  "WORK / NO WORK" and "ONE-OFF WORK ENDS." The user's words: *"this is still vague -
  what pieces are running out? the booked not booked idea is also not landing."*
- **The ICP band must not promise a wider audience than the situation line serves.**
  Rejected: slab "CONTENT WRITERS" plus qualifier row over the setup "GOOD REVIEW. NO
  INCREMENT." An appraisal only happens to salaried writers, so every client-side
  writer read the band as "me" and the setup as "not me", and scrolled. Fixed by
  changing the ICP to one whose situation is universal across salaried, agency and
  client-side writers.
- **A meme/format pun must be visual in one step, not conceptual.** A SKIP card next to
  an appraisal line makes the reader build the bridge themselves, which is the
  definition of cryptic in CLAUDE.md Rule 2. The donor formats work because the card's
  symbol IS the thing being talked about (Kakaji: "+4" card holding four snack packs).
  Fix: put the thing being skipped ON the card. Also check the fallback read for anyone
  who does not know the format.
- **Word budget.** Rejected: *"there is wayyy too much text... the joke or pun or idea
  of the ad is not clear immediately because you have filled it with text."* The shape
  that passed is setup line, device, punchline, ONE sentence (the Rule 2 definition),
  terms bar. Everything else - cap lines above the device, a punch sentence inside it, a
  second explainer line, a deliverables strip - gets cut. Roughly 40-45 words on the
  face, against 96 on the rejected build.

**How to apply:** before rendering, read every phrase back and ask whether the reader
would use that word about themselves. Then check the band and the situation line name
the same population. Then count the words.

## Evidence on an ad face (22 Aug 2026)

Two rules, both given after a full 16-ad rework had to be redone.

- **A statistic is not a benefit.** Ruchika: *"you have added a fact from the lp, okay so
  what? what does it mean for the viewer?"* A number parked in its own strip under the
  payoff reads as trivia. The fix is to move the fact INTO the payoff, at payoff size,
  with its consequence attached: not "11,000 Indian brands sell straight off their own
  website" but "11,000 INDIAN BRANDS NEED IT RUN." The reader has to be told what the
  number means for them, in the same breath.
- **Never repeat the same statistic across a pack.** *"do not use the same 11000 stat in
  all - remember that."* Rotate the handoff's ad-face-safe evidence one fact per cell,
  matched to the ICP: 11,000 brands selling direct, 6,000 on one platform, 3,700
  companies, 4,300 founders, 30-40% of revenue into advertising, orders +34%, FMCG +32%,
  health and beauty +48%/41%, two thirds of growth from Tier 2 and 3, marketing hiring
  +12%, media production +24%, only ~1% of Indian LinkedIn users posting, and the named
  brands (Mamaearth, boAt, Minimalist). Audit with a grep across the pack before shipping.
- **Watch the demand claim.** 11,000 is scale, not demand: there were only ~805 creative
  strategist listings on Glassdoor India in March 2026. Say brands "need it run", never
  that they "are hiring".

**How to apply:** one distinct fact per ad, phrased as a consequence for the reader, in
the payoff rather than in a block of its own.

## The two mechanical gates now exist (24 Aug 2026)

Restated as the single biggest problem: *"the tool tries to be too clever with the image
and the hook - it has to be simple and instantly understandable."* Plus two new items:
**content not properly aligned on the image**, and **ICP relevance** - *"who would buy
that course, ie would be willing to learn a new skill or are desperate in some way?"*

Everything above is now enforced by `simplicity.py` in the repo root, run alongside
`preflight.py` before any handover:

- word volume on the face, deficiency framing ("you have never..."), dangling references
  ("own all four" - four what), hook length, jargon, missing identity band, missing
  definition sentence, wordplay, stacked text blocks
- faded and undersized type, **measured contrast on the rendered PNG** (not from CSS -
  the CSS version was wrong on 6 of 15 approved ads because text sits on strips drawn by
  absolutely positioned siblings), text bleeding to the edge, and whether text blocks
  share a left edge
- `python simplicity.py --why` prints the verdict behind each rule; `--selftest`
  re-scores against the Section A split (currently 5 of 7 rejections, 2 false alarms
  on 15 approvals)

Note the two word-count scales are not the same denominator: the 40-45 word target above
counts main copy blocks; `simplicity.py` S1 counts everything on the face including the
terms bar, brand row and price, and blocks over 100. Treat 40-45 as the design target and
S1 as the backstop.

ICP relevance is now a required `value_props.md` field, `buying_pressure`: why THIS person
pays and shows up *now* - a shrinking employer, a frozen rate, a career break, a notice
period, a ceiling. Never "wants to grow". Scaffold a whole kit's spec from an ICP list
**before any creative exists** with
`python preflight.py --scaffold-from docs/ICPs_40_ContentWriting.md <kit-folder>`, and
send that file alone for round-one approval.

## The mechanical gates don't solve "too clever" - a repo-wide census proved it (24 Aug 2026)

Running every `simplicity.py` rule against all 171 ad HTMLs / 380 PNGs in the repo, not just
the 22-ad set it was fitted on: `S3` (dangling-hook-reference, the rule written specifically
to catch cryptic hooks) fired **zero times**. `R2` (type-size floor) fired on **100%** of
files - a rule that always fires carries no information. Two clever headlines predicted as
rejects ("Own all four", "Own the campaign nobody owns") were both approved - cleverness is
semantic and isn't reliably catchable from text by regex or by the model's own read.

**Why:** `simplicity.py` and `preflight.py` catch volume/legibility/compliance - real
problems, now measurable - but the stated core problem ("too clever," has to be instantly
understandable) is adjacent to those, not caught by them. A 40-word ad can be perfectly
cryptic and pass every rule.

**How to apply:** don't treat a clean `simplicity.py`/`preflight.py` run as proof an ad is
simple enough - it only means volume/legibility/compliance are fine. The two fixes identified
as the ones that would actually work, neither built yet: a `GOLDEN/` bank of 6-8 approved
ads (verdict + why-it-passed) quoted at the front of every generation run, since imitation
shapes what gets written and a gate only argues after the fact; and running the blind-reader
check (CLAUDE.md's three-question test) as actual code with a context-isolated subagent,
not just as a handover checklist item a writer applies to their own work.

Separately: `creative_judge.py`'s `png_for()` only looked beside the HTML file for a
render, and every kit in this repo stores `html/` and `ads/` as siblings - so the pixel-level
checks (`E1`-`E4` clipping/crop-band, `X1`) had **never actually run on any kit** until this
was fixed same day. Anything in `creative_verdicts.jsonl` logged before 24 Aug 2026 is
copy-only verified, not visually verified - its silence on clipping/crop means "never
checked," not "passed."
