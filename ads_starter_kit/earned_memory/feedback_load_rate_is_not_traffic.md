---
name: feedback-load-rate-is-not-traffic
description: "A low landing-page-view rate is often broken measurement, not lost traffic - check buyers per click before calling a link broken"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2387ada5-7a87-4eae-b265-1d2214562cdf
  modified: 2026-09-04T07:48:13.080Z
---

**Never diagnose a low load rate (`landing_page_view / link_click`) as a broken link until
buyers-per-click says the traffic is actually lost.** Proven 4 Sep 2026 on
`Independent Director Community v5` (SkillArbitrage_V, campaign 120245852337110658).

The daily report flagged it at 52.5% load rate as an L3 link/tech fault and recommended
timing the page on a phone. That was wrong. The seven-day ad-level view falsifies it
arithmetically, before any browser is opened:

| Ad | Clicks | Page views | Load | Buyers | Buy/click | CPP |
|---|---|---|---|---|---|---|
| id_ov07_overheard | 826 | 520 | 63.0% | 33 | 4.0% | ₹465.91 |
| break in | 636 | 41 | 6.4% | 21 | 3.3% | **₹298.76** |
| poster | 278 | 19 | 6.8% | 10 | 3.6% | **₹259.73** |
| women seat | 1,062 | 4 | 0.4% | 14 | 1.3% | ₹576.99 |

**Load rate spans a factor of 150; buyers per click spans a factor of four and does not
track it.** `women seat` books 14 purchases against 4 recorded page views, and
`experience_belongs` books 1 against 0 - impossible if the visitors were not arriving. The
cheapest buyer in the campaign (`poster`, ₹259.73) sits at 6.8% load. A browser test then
confirmed both destinations return 200, load fast, carry the pixel and throw no console
errors.

**Why:** `landing_page_view` needs the click to be matched back to the pixel's PageView.
Anything that breaks that match - a redirect that drops `fbclid`, a placement that counts
taps differently, a page template that fires the pixel on a different trigger - collapses
the recorded rate while the traffic and the purchases continue. Acting on it pauses working
ads and sends someone to fix a page that is fine.

**How to apply:** when load rate is under band, compute **buyers (or leads) per click** for
every ad in the campaign first. If that holds up across the low-load ads, the fault is
measurement and the layer is L0, not L3 - say so and stop. Only if buyers-per-click
collapses alongside load rate is it a real link or page-speed fault. Load rate is a
per-ad number, never a campaign average: this campaign's 52.5% was two distinct
populations of ads averaged into one meaningless figure.

Related: [[feedback-paychart-and-ctr-traps]] - same shape of error, a rate metric that does
not predict cost. [[feedback-ads-report-columns]] - spend, buyers, CPP are the decision
columns; rates are context. [[reference-growthx-funnel-checkout]] - how these pages actually
wire the pay button, and why the first check of them was wrong.
