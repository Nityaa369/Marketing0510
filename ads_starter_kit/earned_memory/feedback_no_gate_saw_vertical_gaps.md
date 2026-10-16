---
name: feedback-no-gate-saw-vertical-gaps
description: adkit/gaps.py measures background runs on the rendered PNG; fitted at 200px against GOLDEN (max 178) and the priced faces (max 151)
metadata:
  type: feedback
---

Three separate reports of *"a lot of empty gaps, especially above the footer"* /
*"make sure everything is aligned properly, no weird spaces"* all arrived from a human
looking at a PNG, because **no gate in the repo could see a void**. `adkit.fit` asks only
whether anything clips or overlaps, and a void is the opposite of an overlap.
`simplicity.py` covers the horizontal half (shared left edge). `ad_lint` never renders.

**Why:** each time, only the one face that was shown got fixed, so the next wave shipped the
same defect. `adkit/gaps.py` (4 Sep 2026, wired into `check_all.py`) measures the longest
uninterrupted run of background rows between the first and last content row.

**How to apply:** it reads **pixels, not the DOM**, and that is deliberate - GOLDEN is PNG
only, so a DOM rule could never be fitted against approved work, which is what this repo
requires of a checker (see [[feedback-checkers-refit-basis]]). Ceiling 200px: GOLDEN's worst
is 178px, the priced faces' worst is 151px, so it blocks 0 of 19 and blocked the 207px face
that was reported. Aim for the priced range, under about 150px, not for the ceiling. Re-fit
with `python -m adkit.gaps --fit`.
