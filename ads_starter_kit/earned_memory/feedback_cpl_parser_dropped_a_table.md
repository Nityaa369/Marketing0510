---
name: feedback-cpl-parser-dropped-a-table
description: corpus.load_live read two of three priced tables in the Meta pull, hiding a whole product line's costs with no error
metadata:
  type: feedback
---

`corpus.load_live()` recognised exactly two headings (`## Free bootcamps`, `## Paid camps`)
and read cost at a fixed column index. The pull had since grown a third priced table —
`## Academic Writing, 26-28 Sep camp` — under an unrecognised heading AND five columns wide
instead of six. Both failures were silent.

**Cost: 12 priced ads, a whole product line's ICP-level costs, invisible to `corpus`,
`--winners`, `--losers` and every ICP rollup.** Fixed 15 Sep 2026 by reading each table's own
header row (CPL -> lead, CPP -> purchase) and locating columns by name. Priced rows went
31 -> 47, corpus ads with a live cost 14 -> 20, and it recovered three US Accounting winners
(`us04_small_town`, `us25_notice_small_town`, `us24_notice_evening`, all ~Rs 40/lead).

**Why:** this is [[feedback-report-scripts-narrow-silently]] happening again in a different
file. A hardcoded heading or column index shrinks a total with no error, and the number still
looks plausible.

**How to apply:** when a parser reads a human-maintained Markdown table, derive the shape from
the table's own header, never from position or from a heading whitelist. And whenever a number
looks small, check the parser before concluding the data is missing — "only 14 of 538 ads are
priced" was half a parser bug. `python -m adkit.brief --worked` now prints n on every run so
the denominator is never invisible.
