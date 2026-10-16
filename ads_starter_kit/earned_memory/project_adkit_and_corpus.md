---
name: project-adkit-and-corpus
description: Ad kits build from the shared adkit/ chassis, the SOP/00 constants card and the corpus index, not from a per-kit generator and 2,822 lines of doctrine
metadata:
  type: project
---

Built 31 Aug 2026 after "the skill is taking way too long to generate ads". Three
measured cost centres, all now addressed:

1. **2,822 lines of prose + 9 GOLDEN PNGs (~55k tokens) read before step 0.**
   Replaced by `SOP/00_CONSTANTS.md`, the one-page card. Long files are the record,
   read when a gate fires or a rule is being changed.
2. **20 per-kit generators, 9,890 lines, no shared library.** Replaced by `adkit/`
   (`chassis.py`, `lp_spine.py`). A kit is now ~10 lines of data per ad.
3. **No gate could see text overlap or the computed type size.** `adkit/fit.py`,
   wired into `check_all.py` as `fit (rendered)`.

Plus `adkit/corpus.py`: 472 shipped ads joined to the Meta pull and to APPROVED/GOLDEN
membership. `--like "<icp>"`, `--winners`, `--losers`, `--ad <name>`. Read five real
precedents (copy AND the face PNGs) before writing a hook. `adkit/verdicts.py` adds the
labelled NEGATIVE set from CAMPAIGN_MAP.md, so `--like` ends by naming the rejections
nearest that ICP in the reviewer's own words.

Second pass, same day, after "is this as optimised as it can be":

4. **`adkit/spec.py` — one spec per kit, everything generated.** value_props.md +
   hooks.md + ad_copy.md were 666 hand-typed lines on one kit, and the same strings
   again in both generators. `field_definition` was typed verbatim three times. Now
   written once; Rule 3 is true by construction rather than checked by a linter.
   New kits only, opt-in; shipped kits untouched.
5. **`adkit/golden.py` — GOLDEN is generated, not hand-picked.** Was 9 images frozen
   in Aug; now 217 approved faces from `APPROVED/`, the SectionA APPROVED zip, and
   Ramanuj's own `RID_BC_8Aug_Ads (1)` + `Accounting_BC_8Aug_Ads (1)` (47 faces are
   his). Those two hold the account's cheapest ads. Recorded rejects are dropped
   automatically. Hand-written WHY IT PASSED notes preserved in GOLDEN_NOTES.md.
6. **SKILL.md 548 -> 399 lines**, with the population-specific playbook moved to
   `SOP/09_EARNED_PLAYBOOK.md` (conditional reading) and every rule the card already
   carries removed rather than restated.

`python -m adkit.selftest` is the evidence, 8/8, and runs inside
`check_all.py --selftest`.

Related: [[feedback-run-every-gate]], [[feedback-copy-is-filled-in-not-written]],
[[feedback-icp-is-the-biggest-lever]]
