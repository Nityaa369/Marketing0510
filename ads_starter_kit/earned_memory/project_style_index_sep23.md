---
name: project-style-index-sep23
description: "Measured 23 Sep 2026 across 12 campaigns: no static design style has a repeatable win; notice is the only one under par twice, and pay chart is bad but not 2.34x"
metadata: 
  node_type: memory
  type: project
  originSessionId: 72d8a971-d1c7-4903-b4a2-5bd535dd4e4b
  modified: 2026-09-23T08:04:01.758Z
---

Ad-level pull, 30 days to 23 Sep 2026, 12 campaigns, ~940 rows, every ad indexed against
**its own campaign's par** and filtered to 20+ results (the part-day rule).

| style | ads at the bar | index | note |
|---|---|---|---|
| video | 9 | 0.80 | range 0.37 to 1.63, not a static style |
| notice | 2 | 0.81 | both at 0.81; us24_notice_evening 78 buyers, us22_notice_fifties 25 |
| chat/thread | 1 | 0.85 | one ad |
| unclassified | 118 | 0.99 | the bulk; ICP-named, no style signal |
| pay chart | 3 | 1.04 | 13 rows all-in: 0.49 to 5.05, worst is pc_patent_paychart at 5.05 |
| grid/table, meme, toon/duo | 4/3/8 | 1.06-1.09 | at or above par |
| search, quote, ladder, worklist | 0 | - | no ad reached 20 results |

**Every one of the 18 best high-volume ads is named by ICP, not by style** (veterinary 0.57,
medical_researchers 0.73, cs_inhouse_mnc 0.75, wfh_lawyers at 1,505 buyers 0.83). This is
[[feedback-icp-is-the-biggest-lever]] measured again on a bigger pull.

**Two corrections to earlier notes.** Pay chart's "2.34x in four product lines" is too harsh
as a single number: across 13 rows it is roughly par, with one 5.05 disaster in Patent. It is
still never a winner. And `^pc_` is NOT a pay-chart signal - in Global Patent it is the
campaign's own ad prefix, which misclassified 62 ads on the first pass. Match `paychart`
only.

**The one untested opening:** notice has run in exactly one campaign, US Accounting, 17 ads.
Nowhere else. It is the only static style under par twice. Related: [[feedback-vary-the-design-style]],
[[project-search-layout-oct-rollout]].
