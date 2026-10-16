---
name: feedback-never-judge-an-ad-on-a-part-day
description: Ad-level cut/scale calls need a 7-day window and 20+ buyers - every part-day call made on 4 Sep 2026 collapsed when re-measured
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2387ada5-7a87-4eae-b265-1d2214562cdf
  modified: 2026-09-04T08:58:57.064Z
---

**No ad-level judgement off a part-day. 7-day window, and no call under 20 buyers.**

On 4 Sep 2026 I marked six ads *cut* or *pause now* using that day's partial numbers. Every
single one was wrong when re-measured over seven days:

| Ad | Buyers the call rested on | Part-day CPP | 7-day CPP | Campaign avg |
|---|---|---|---|---|
| acwr_03_research_scholars | 4 | ₹468.61 | **₹162.10** | ₹167.30 |
| cd_Route 21 | 0 | — | **₹368.32** | ₹442.16 |
| sqe_l_l_gulf | 0 | — | **₹385.69** | ₹442.16 |
| sqr_j_parmeet | 1 | ₹1,081.45 | **₹425.19** | ₹442.16 |
| cd_contracts_grid | 2 | ₹753.43 | **₹354.15** | ₹442.16 |
| W9_X33_demand | 6 | ₹249.09 | ₹159.37 | ₹126.60 |

The founder's question was *"why are you retracting the analysis later after i push?"* The
answer is not stubbornness on either side - the calls were never supported. A cost per buyer
built on *n* buyers carries roughly **±196/√n percent**: ±98% at n=4, ±62% at n=10, ±44% at
n=20, ±20% at n=100. At four buyers the number carries no information at all.

**How to apply:**

- **Ad and creative level: `date_preset: last_7d`, always.** Today's part-day answers exactly
  one question - is it delivering. Use it for L0 checks and nothing else.
- **Print the buyer count in every row**, next to the CPP, so thinness is visible rather than
  inferred. Add the ±196/√n margin; it makes a bad row self-evidently bad.
- **Under 20 buyers, write "no call - n too small".** Do not soften it to "watch"; a watch is
  still a claim.
- **Campaign level tolerates a shorter window** because n is large - Academic Writing's rise
  to ₹212 on 3 Sep rested on 136 buyers and was real. The error was attributing it to one ad.
- **Zero buyers is only evidence with enough clicks behind it.** `rf02_women_science` at 334
  clicks and 0 buyers is a genuine kill; an ad with 6 clicks and 0 buyers is not.
- When a campaign's ads are *uniformly* dear (SQE community: every ad above the half average),
  the fault is ICP or offer, not creative. Do not go creative-hunting - that is SOP/08 work.

Related: [[feedback-contradiction-means-failed-test]], [[feedback-ads-report-columns]],
[[feedback-ads-report-day-by-day]].
