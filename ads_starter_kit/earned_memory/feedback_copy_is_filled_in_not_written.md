---
name: feedback-copy-is-filled-in-not-written
description: Approved ad copy is a fill-in-the-slots formula, not free writing; the delivery sentence is a per-kit constant and the length ceilings are measured
metadata:
  type: feedback
---

Ramanuj flagged on 31 Aug 2026 that ad copy was "still not up to the mark" even after the
director file and the mechanical gates. A census of the `APPROVED/` folder (150 approved copy
blocks, 16 kits) showed why: approved copy is far more formulaic than the drafts, and the
drafts were being creative in the slots that are meant to be constant.

The measured shape, now written up in `SOP/07_AD_COPY.md` and re-runnable with
`python SOP/tools/copy_census.py`:

- **Primary text is four moves**: situation (~12 words) → pivot (the asset is worth more
  elsewhere) → delivery sentence → terms. Median 86 words, 140 of 150 at or under 110.
  The old "100-150 words" figure in `AD_CREATION_DIRECTOR.md` §7 was never fitted to the
  corpus and was the direct cause of over-long drafts; it has been corrected.
- **The delivery sentence is a per-kit constant.** 139/150 carry one, 136 of those name
  exactly three things plus a horizon ("we show you the work, the skills and the plan that
  <OUTCOME>, in 6 months"). Only the outcome clause changes per ICP. 21 IP Law ads share one
  sentence; 7 Independent Director ads share it byte-identically.
- **Headlines: 4-10 words, median 7. No approved headline exceeds 10.** They name the
  destination role, never the pain.
- **Zero banned filler words and zero em-dashes across all 150 blocks** — the anti-voice list
  is empirically clean, not a style preference.
- **Only 24% carry a statistic.** Reaching for a number every ad is off-pattern.
- **The horizon ("in 6 months") is product-line specific**, not universal: 92-100% in camps
  selling a route to a first client or seat (ID, IP Law, US Accounting, USCL, Arbitration),
  0% in Women Remote, Content Writing and SQE, which promise a plan without a clock.

**The controlled test, 31 Aug 2026.** `IndependentDirector_Wave1_MediaBuyer_12-14Sep` is the
same product, camp and dates as three ID kits that were approved. Approved siblings: delivery
sentence 88-100%, plan 100%, horizon 100%, primary text median 72-74 words. Wave 1: delivery
**0 of 10**, plan 10%, horizon 0%, median 104 words. Its sentence is "The free bootcamp *is*
9 hours live over three days: <three lecture titles>" - product as subject, syllabus instead of
assets, no plan and no outcome. Wave 1's own blind-reader test caught the symptom and the fix
went onto the ad face as a promise block; the defect was in the sentence and survived.

**Why:** the rejections were not about ideas or ICPs, which were already being approved. They
were sentence-level: reinvented delivery sentences, headlines over the ceiling, and copy
running 140-160 words against a corpus median of 86.

**How to apply:** write the delivery sentence once per kit into `value_props.md` before the
first ad exists, then paste it into every block and change only the outcome clause. Run the
10-line copy check in `SOP/07_AD_COPY.md` §8 before the face is designed, not after.

Related: [[feedback-house-ad-formula]], [[feedback-ad-clarity-rules]],
[[feedback-simple-technical-english]], [[feedback-run-every-gate]].

**The limitation, refitted 28 Sep 2026.** The selftest first fitted against Section A, whose labels were in-house and never shipped; it then crashed for a month because hook_rules renamed that split. It now measures precision on the 146 GOLDEN copy blocks Ramanuj approved: headline>10 words 0%, bare pronoun 1.4%, primary>110 words 6.8%, no delivery sentence 7.5%, but no plan 17.8%, no horizon 31.5%, no negation strip 61.6% (style only). There is no labelled rejected set, so recall is unmeasured: SOP/07 is a *style guide fitted to approved output, not a rejection predictor*. What decides whether copy is good is CLAUDE.md Rules 1-5 and the blind-reader test.
Re-run with `python SOP/tools/copy_census.py --selftest`.
