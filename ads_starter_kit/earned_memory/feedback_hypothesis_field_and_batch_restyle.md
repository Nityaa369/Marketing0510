---
name: feedback-hypothesis-field-and-batch-restyle
description: value_props carries a falsifiable hypothesis per ad, and adkit.restyle --spread does a whole-wave visual refresh from a Chrome-free probe
metadata:
  type: feedback
---

**`hypothesis` is a required `value_props.md` field** (15 Sep 2026). One line per ad saying
what it TESTS, as a claim that could turn out wrong. "This will work", "good ad for
teachers", "TBD" are blocked — they cannot fail, so they are not hypotheses. Under 8 words
warns. Exemptions are per-field in `.preflight-grandfathered` (`<kit>: pain_score,
hypothesis`), 25 pairs across 13 kits, and `preflight.py --selftest` fails if that count
grows.

**Why:** the account recorded who an ad is for, what it offers, how hard the reader is
pressed and what they already believe — and nothing about what it was testing. So a verdict
attached to a face, not to a belief, and the wave taught the next wave nothing beyond "that
one was rejected". It pairs directly with `adkit.verdict --review`: a rejection against a
stated hypothesis is evidence about a reader that transfers.

**`python -m adkit.restyle <kit> --spread`** re-skins a whole wave. `ADKIT_PROBE_LAYOUTS=1`
makes `Spec.write()` build every (ad, layout) face in memory and dump the copy each would
carry — no Chrome, no files, ~0.5s, versus ~19s per real render (about 16 minutes by trial
for 5 ads x 11 layouts). Then a greedy pass hands each face the legal layout least used.
GlobalPatent Wave 2 went **5 distinct skeletons to 9** across 10 faces.

**How to apply:** a copy probe is necessary but NOT sufficient — `photo` passed on text and
then DID NOT FIT at any scale, because it needs a supplied hero. `photo` is never proposed
for an ad that is not already using it, and any face that fails to fit drops back to its
current layout instead of aborting the batch. **Always re-run `check_all.py` after a
restyle**: on that Wave 2 run the `gaps` gate found a new 200px void. Two faces were locked
to `serif` because their copy uses the `barrier` field most skeletons do not carry — see
[[feedback-restyle-layouts-are-not-interchangeable]].
