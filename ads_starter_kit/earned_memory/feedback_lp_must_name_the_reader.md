---
name: feedback-lp-must-name-the-reader
description: Rule 4b measures whether pages differ; lint L6 measures whether a page speaks to the person who clicked
metadata:
  type: feedback
---

*"For the LPs, make sure there is at least 1 role-specific section, so it relates to the ICP
clicking on it."* Rule 4b ([[feedback-lps-in-a-kit-must-differ]]) already blocks pages that
are copies of each other, but a page can overlap by 1% and still never name the reader - it
just argues something different, generically.

**Why:** measured 4 Sep 2026 across 41 pages in 5 kits, 7 had no section heading naming their
ICP at all, including three where the whole page was otherwise ICP-specific. The reader lands
from an ad whose call-out band says TRADE FINANCE OFFICERS and meets ten headings that could
belong to anybody.

**How to apply:** `lp_spine` lint **L6** now checks that at least one `<h2>` contains a content
word from that ad's own ICP line, stemmed. The kit passes `icp=` through `Camp.page()`; it is
never rendered. Tokenise at 3 characters, not 4 - at 4, "LLB HOLDERS WORKING OUTSIDE LAW" lost
"law" and a heading that plainly named her read as a miss. A shorter floor gives the page more
ways to match, so it lowers false alarms. Two selftest cases in `adkit/selftest.py` keep it
honest.
