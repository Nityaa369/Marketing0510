---
name: feedback_run_every_gate
description: Run check_all.py on the kit - never a subset of the checkers, and never treat a crashed or blind checker as a pass
metadata:
  type: feedback
---

`python check_all.py <kit-folder>` at the repo root runs every gate and reports PASS /
FINDINGS / **ERROR**, where ERROR means a gate crashed or saw zero files. Use it. Do not
hand-run one checker and report "no blockers".

**Why:** on 25 Aug 2026 two ads passed review three times and were still wrong.
`simplicity.py` was run on `ads/*.png` only, so its copy rules never ran and a 196-word ad
face (cap is 100) went unflagged. `judging-static-ads/engine/creative_judge.py`, the repo's
actual ship gate, was never run at all. `ad_lint` C8 matches CSS **class names**, and the
kit generator emitted inline styles with no classes, so the strictest size gate in the repo
silently matched nothing and looked like a pass. The judge also crashes on Windows with a
UnicodeEncodeError unless `PYTHONIOENCODING=utf-8` is set, and a crash reads exactly like a
clean run if you are not looking.

**How to apply:** every ad face must expose a sized `.callout` and `.head` class or C8
cannot see it. Set `PYTHONIOENCODING=utf-8` before the judge. When a gate fires on the
approved set too (E2/X1 crop-line warnings fire on mh01, hoc_02 and usmb_05), say so and
do not chase it. When a gate blocks on something only the user can decide (C16 bans the
word "AI" on SkillArbitrage skilling creatives, but the Women AI Bootcamp is named for it,
exactly like the content-writing carve-out of 20 Aug), raise it rather than silently
rewriting the product's name.

**Two more gates were found not running, 25 Aug 2026.** `creative_judge.py` K1 (every ad
has anchor text) and C21 (primary text length) look for `ad_copy*.md` beside the ad HTML.
Kits that keep render sources in `html/` resolve the kit dir to that subfolder, so both
checks reported "could not be checked" - which reads like a clean run. Fixed in the judge
by looking one level up. C21 then measured every ad as ~12,990 chars, because `ad_copy.md`
was a single markdown table: C21 splits per ad on markdown headings, so one table means one
block. **Ship `ad_copy.md` as one `###` section per ad with Headline, Primary text and
Description**, the way ContentWriting_SectionA does. The Description field was missing
entirely from the table format, and it is one of the three paste-ready fields every ad owes
the media buyer.

**Primary text is an argument, not a summary.** Approved Section A primary texts run
~500-590 chars against C21's 600 flag: a lived scene, the correction, a definition of the
new unit, then a standing close ("Across three live evenings we show you how to build one
end to end, and how to land the clients who buy it"). Summarising the ad face instead wastes
the field.

Related: [[feedback_house_ad_formula]], [[feedback_ad_clarity_rules]].
