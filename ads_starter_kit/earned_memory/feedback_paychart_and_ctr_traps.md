---
name: feedback-paychart-and-ctr-traps
description: Pay-chart ads cost 2.3x their campaign median in three product lines, and CTR does not predict CPL - two measured traps in how we pick creative
metadata:
  type: feedback
---

Measured 31 Aug 2026 from the Meta Ads MCP: 90 ads, Rs 4,275,135 spend, account
954464642377027. Tables in `ad-analysis-shared/CPL_WINNERS_31Aug2026.md`, doctrine in
`SOP/07_AD_COPY.md` section 9.

**Stop building pay charts.** Replicated in three campaigns across three product lines,
each against the best ad in its own campaign: Independent Director Rs 195.36 vs Rs 60.42
(3.2x worse), Patent Rs 380.20 vs Rs 121.53 (3.1x), US Accounting Rs 72.65 vs Rs 29.65
(2.5x). Normalised index 2.34 against a campaign par of 1.00; every other format sits
between 0.64 and 1.22. A pay chart makes a salary figure the hero, which CLAUDE.md already
bans from the ad face on compliance grounds - so performance and compliance agree here.

**A high CTR is not a good ad.** CTR vs cost per result across 90 ads: r = +0.17 (leads),
+0.08 (purchases). Inside Senior AI r = +0.61 and Academic Writing r = +0.52 - higher CTR,
MORE expensive. The account's highest-CTR ad (SeniorICP|Toon|st02_canteen, 4.12%) costs
Rs 234.71; cf_cma at 0.61% CTR costs Rs 170.17. Toon/chat formats index 1.22.

**Name the ICP, do not manufacture urgency.** In one Patent camp the named-occupation cells
(semicon/VLSI Rs 120.68, agri-food Rs 131.49, ayurveda Rs 135.30) beat the deadline cells
(Rs 203.28, Rs 250.89, Rs 284.95) by 1.5x to 2.4x.

**Why:** we had no way to tell a creative that wins attention from one that wins leads, and
the pay chart kept getting rebuilt because a salary number looks like a value proposition.

**How to apply:** never defend an ad on clicks. Keep the three-second comprehension test -
it is about being understood, not about CTR. Pull fresh numbers via [[project-meta-data-pull-path]]
before repeating a format. Related: [[feedback-copy-is-filled-in-not-written]].
