# 10 · The daily ad report

Generated every day, in two halves: **Community** and **Bootcamps**. The halves are never
blended, because SOP/03 forbids blending funnel types and because the two are judged on
different questions — Community on cost per buyer at steady state, Bootcamps on whether a
dated camp fills before its date.

This file is the spec. It says what to pull, what counts as a problem, and what the report
must contain. It does not replace SOP/02 (thresholds) or SOP/03 (how to judge a cell); it
applies them daily.

---

## Two conventions that override everything below

- **All rupee figures include 18% GST.** Meta returns net. Multiply by 1.18 before any
  number reaches the report or gets compared to a threshold. SOP/03 has said this since
  before this file existed; reports written straight off the API have been understating
  CPP by 18% against the standard the account is judged on.
- **Never blend funnel types.** A ₹10 camp, a ₹100 community, a free registration and a
  full-price campaign go in separate tables. The Community/Bootcamp split is the first cut,
  not the last one: within Bootcamps, lead-objective campaigns are reported separately from
  purchase-objective ones.

---

## The failure taxonomy

Money moves along a chain, and each link fails in its own way with its own detector. The
report's job is to say **which link broke**, because that decides who fixes it — a media
buyer, a copywriter, or a developer.

```
budget → impressions → clicks → landing page views → purchases
         [audience]    [creative]  [link/tech]        [page/offer]
```

### L0 · Account and delivery

| Failure | Detector | Source |
|---|---|---|
| Account disabled or flagged | `account_status` != ACTIVE | `ads_get_ad_accounts` |
| No payment method / unsettled | `has_payment_method`, status UNSETTLED | `ads_get_ad_accounts` |
| Delivery-blocking error | any error returned | `ads_get_errors` |
| Campaign ACTIVE but ₹0 spend | `effective_status` ACTIVE, spend 0 | entities |
| Account dark that should be live | spend 0 vs its own 7-day norm | entities |
| Someone changed something | budget/status/targeting edits | `ads_account_get_activity_logs` |

SOP/03: report LIVE vs PAUSED vs ₹0 explicitly. Never let ₹0 read as a result.

### L1 · Audience

| Failure | Detector | Threshold |
|---|---|---|
| Audience too narrow | anomaly signal | est. audience under ~10k |
| Frequency runaway | `frequency` over 7d | over 3.5 = fatigue (SOP/03), over 5 = act |

**Frequency is judged on Instagram + Facebook only** (24 Sep 2026). WhatsApp Status took 76-85%
of impressions at 3-6% of spend on six campaigns, with frequency 20-262, and produced every
blended "fatigue" reading over 7. Pull `breakdowns=publisher_platform` first. Ad-set-level
`reach` from the API is unreliable (994k claimed vs 125k across its own ads); use ad or campaign level.
| Auction overlap with own ad sets | anomaly signal / ranking benchmarks | any flag |
| CPM inflation | CPM vs own 7-day median | +30% |
| Reach saturated | reach flat while spend climbs | reach +<10% on spend +>30% |

Two of our own campaigns must never target the same audience (SOP/02).

### L2 · Creative

| Failure | Detector | Threshold |
|---|---|---|
| Hook not working | CTR vs half median | under 0.6× |
| Perceived as low quality | Quality Ranking | Below Average; Bottom 20% = act |
| Not spurring interest | Engagement Rate Ranking | Below Average |
| Creative fatigue | CTR decaying at flat frequency over 3 days | −25% |
| Too few creatives | ads carrying 80% of campaign spend | under 3 |
| Complaints on the ad | comments per ₹1,000 spend vs half median | over 2× |

Fatigue is a refresh, not a kill (SOP/03). Max 5 ads per ad set (SOP/02).

### L3 · Link and technical

**The load rate is `landing_page_view / link_click`.** This is the direct detector for
"the link in the ad is not working" and for a page too slow to load.

| Failure | Detector | Threshold |
|---|---|---|
| Link broken / page too slow | load rate | under 60% investigate, under 40% act |
| Pixel stopped firing | LPVs steady, purchases → 0 | any campaign, 1 day |
| Dead payment stub on the LP | LPVs healthy, purchases 0 | see Rule 5, CLAUDE.md |
| Wrong destination | load rate normal, LP conversion near 0 | conversion under 1% |

Precedent: TechLaw BC ran at **33% of clicks loading the LP** (SOP/02). Page speed is a
launch criterion, checked before spend, not after. Measured Community band is 69–85%.

### L4 · Landing page and offer

**The page conversion is `purchases / landing_page_view`.**

| Failure | Detector | Threshold |
|---|---|---|
| LP needs a refresh | page conversion vs half median | under 0.6× |
| Meta agrees | Conversion Rate Ranking | Below Average |
| LP does not match the ad | manual, on any flagged page | Rule 3, CLAUDE.md |
| LP going stale | page conversion decaying at flat traffic | −25% over 7 days |

A campaign whose ads are fine and whose page is weak must be reported as a **page**
problem. Pausing its creatives is the wrong fix and wastes working ads.

### L5 · ICP fit

| Failure | Detector |
|---|---|
| Wrong people clicking | CTR at or above median **and** page conversion under 0.6× median |
| Expensive niche with no depth | CPM over 2× median, CPP over 1.5× median, reach small |
| A segment that never buys | age / gender / placement breakdown, spend with no purchases |
| ICP had no buying pressure | every creative in the campaign underperforms alike |

The last one is a `value_props.md` failure, not a media failure. It goes back to ICP
selection (SOP/08), not to the media buyer.

### L6 · Budget allocation

| Failure | Detector |
|---|---|
| A bad ad eating the allocation | spend share ÷ buyer share over 1.4 |
| The good ad starved | CPP under 0.7× half blended **and** spend share under 5% |
| Campaign past its circuit breaker still funded | CPP over 1.5× its baseline |

### L7 · Outcome — parked until the GrowthX MCP lands

Buyers are not attendees. Show-up rate, refunds, revenue per buyer and true ROAS live in
GrowthX and the payment bridge (Cashfree / Razorpay), not the Meta API.

**A GrowthX MCP is being built (noted 31 Aug 2026). Until it is connected, the report says
plainly that it cannot see outcome data** rather than letting Meta purchases read as the
business result. When it lands, this layer opens up and the fill-target columns below stop
being a manual input. SOP/02 still requires reconciling the payment bridge against Meta
against the CRM at 100 purchases.

---

## Thresholds are dynamic, not absolute

*Settled 31 Aug 2026: "keep this dynamic based on past averages."*

No rupee figure is hard-coded. Every threshold is a **ratio to a trailing baseline**, so the
report keeps working when costs drift, when a new product line launches with no history, and
when a ₹100 community sits next to a ₹10 camp.

### The ratios

Taken from SOP/02's own documented ₹10-camp numbers, so that applying this system to a ₹10
camp reproduces existing policy exactly rather than inventing a second standard:

| Band | Ratio to baseline | Derivation |
|---|---|---|
| Scale | at or below **0.83×** | ₹250 / ₹300 |
| On target | around **1.0×** | ₹300 / ₹300 |
| Watch | **1.3×** and above | midpoint |
| Circuit breaker | **1.5×** and above | ₹450 / ₹300 |

### The baseline

Trailing **28-day median CPP, GST-inclusive**, computed at the narrowest level that has at
least **30 buyers** of history. Fall back up this ladder and always state which level was used:

1. This product line, same type (MAIN or RE), last 3 camps
2. This product line, both types
3. This funnel type within the half (₹10 camp / ₹100 community / lead)
4. The half overall

MAIN and RE are never averaged together at level 1 — a rerun sells to a thinner remaining
audience and costs more, and blending the two hides both.

### Indexing by days to camp

A bootcamp's CPP is not flat across its sales window: traffic 20 days out is cold and traffic
3 days out is buying on a deadline. So a camp at T-5 is compared against **what other camps
cost at T-5**, not against their whole-run average.

This needs a few camp cycles of history before it is trustworthy. Until then use the flat
trailing median and say so in the report. Build the day-indexed curve as camps complete.

### Everything else scales the same way

Load rate, page conversion, CTR, CPM and comment density are all judged against the trailing
28-day median for the same half, using the band ratios above. The only fixed number in this
file is **frequency 3.5**, which is a Meta-side fatigue threshold from SOP/03 and not a cost.

## Classification: Community vs Bootcamp

By campaign name first, account as fallback. Flag anything unclassified rather than
bucketing it silently.

- **Community** — name contains `Community`, `21day`, `21 Day`, `14day`. Default for
  accounts `1132073781843015` (Community ASHWIN) and `708740732041378` (SkillArbitrage_V).
- **Bootcamp** — name contains `BC`, `Bootcamp`, `Growthcamp`, or a camp date range.
  Default for `954464642377027` (Skill Arbitrage) and `915514346476600` (Skill Arbitrage_2).

Campaigns move between accounts, so the name rule wins.

---

## What to pull

All via the connected Meta Ads MCP. Account level does not support `cost_per_result`, so
per-result numbers come from campaign or ad level.

1. `ads_get_ad_accounts` — status, payment, which accounts are readable.
2. Account level, `time_increment: "1"`, `last_14d` — the daily series.
   Fields: `amount_spent`, `offsite_conversion_fb_pixel_purchase`, `lead`.
3. Campaign level, `last_7d` and `yesterday` and `today` — the campaign board.
   Fields: `name`, `amount_spent`, `offsite_conversion_fb_pixel_purchase`, `link_click`,
   `landing_page_view`, `ctr`, `cpm`, `frequency`, `reach`, `comment`, `effective_status`,
   `objective`.
4. Ad level, `last_7d` — the creative board. Same fields plus `campaign_id` and
   `effective_status`. **`campaign_name` is not a supported field at ad level; group by
   `campaign_id`.**
5. `ads_get_errors` on each live account — delivery blockers.
6. `ads_insights_auction_ranking_benchmarks` — quality / engagement / conversion rankings.
7. `ads_insights_anomaly_signal` — narrow audiences, overlap, fatigue.
8. `ads_account_get_activity_logs`, last 24h — what changed.

Today is always a partial day. Label it. Judge settled performance on the last 3 full days
and check today and yesterday before calling anything dead (SOP/03).

---

## Report structure

Same skeleton for each half. Community first, Bootcamps second.

0. **Verdict** — one sentence. Is this half healthy, drifting, or on fire.
1. **Act today** — at most 5, ranked by money at stake. Each item carries: the finding, the
   layer it sits in (L0–L6), the evidence, the rupees committed, the fix, and a link.
2. **Day by day** — day, spend, buyers, CPP, 14 days, current day marked partial.
   *(Standing requirement — see the memory note `feedback-ads-report-day-by-day`.)*
3. **Campaign board** — spend, buyers, CPP vs yesterday and 7-day, plus the three funnel
   rates (CTR, load rate, page conversion) so the failing layer is visible per row.
4. **Funnel diagnosis** — only the campaigns with a rate outside its band, and which layer.
5. **Creative board** — every ad: spend, buyers, CPP, frequency, quality flags, link.
   Starved ads are listed and named as starved, never omitted.
6. **Money in the wrong place** — spend share against buyer share.
7. **Headed the wrong way** — deteriorating over 3 days, not yet critical.
8. **Working** — scale these.
9. **Housekeeping** — errors, ₹0-spend live campaigns, changes in the last 24h, audience
   warnings, dark accounts.

### The Bootcamps half carries three extra things

**1. The coverage check, and it runs first.** Read [BOOTCAMP_CALENDAR.md](../BOOTCAMP_CALENDAR.md),
list every camp whose date has not passed, and name the live campaign behind each. **A camp
with a date and no campaign is the most urgent thing this report can contain** — no CPP
number will ever surface it, because there is no spend to have a CPP. Order dark camps by
days remaining. Two accounts are not MCP-readable and one is disabled, so state that a dark
camp may be running somewhere unseen rather than asserting it is not running at all.

**2. Days to camp**, from the calendar, on every row.

**3. Pace against the fill target**, once targets exist. Until the GrowthX MCP lands there is
no fill target to measure against, so report buyers-to-date and the CPP trend by days-to-camp
and say the target is not yet available. Do not invent one.

Every ad, ad set and campaign named anywhere is a clickable Ads Manager deep link — in the
recommendations as well as the tables (`feedback-ads-report-columns`).

---

## Delivery

**In the chat reply only.** No Artifact, no published page, no report file saved in this
repo (the user, 28 Sep 2026: *"I only want to see ad reports in the chat itself, not
created as artifacts"*). `daily_report.py` and `pull_ads.py` still render HTML/JSON as
working files; `daily_report.py` now writes to the system temp folder, and whatever
`pull_ads.py` leaves in `ad-analysis-shared/reports/` is scratch, not a deliverable. Read
the numbers from them and write the report into the chat.

---

## Inputs — status

| Input | Status |
|---|---|
| Target / circuit-breaker CPP | **Settled.** No fixed targets; dynamic trailing baselines, ratios above. |
| Camp dates | **Settled.** [BOOTCAMP_CALENDAR.md](../BOOTCAMP_CALENDAR.md), refresh when the schedule changes. |
| Attendance, refunds, revenue | **Parked.** GrowthX MCP in build; L7 stays closed until it connects. |
| Fill targets per camp | Still open. Needed for the pace column; expected to arrive with GrowthX. |
| Launch lead time for a rerun | **Settled 9 Sep 2026 — there is none.** Reruns are never advertised on this account; no RE camp has ever had a campaign. The coverage check skips `RE` rows entirely. Checking them produced five false alarms on the first run, one of them a CRITICAL. |

---

## The chat summary — the shape that was asked for (24 Sep 2026)

The chat reply is the whole report. It follows the format of the 21-24 Sep "Campaigns
Daily Reports" chat, which the team preferred to an 81-item Act-today list:

1. Time stamp, part-day note, and a **headline**: spend, leads, paid, CPL, CPP, against yesterday.
2. **Free-registration funnels** (spend, leads, CPL) and **paid funnels** (spend, paid, CPP), today vs yesterday.
3. **Report 1: Bootcamps** (free-registration table, then ₹10 table) and **Report 2: Communities**
   (with ₹ collected). Columns: spend, leads, paid, at checkout, CPL/CPP, same figure yesterday.
4. **What stands out**: 5-8 plain bullets carrying their numbers: open checkouts, failed
   payments, winners and losers, new campaigns, pace.
5. A reconciliation line: campaign spend sums to the account total.

**Combined with the SOP report (asked the same day):** after the bullets, carry the SOP's own
sections in short form: dark camps from the coverage check, the top pause calls, the ads to
scale, the spread-thin ad sets, and the day-by-day table.

Leads, paid, checkout and failed come from GrowthX `get_leads_report`, one day per call,
joined to Meta spend by `group` with Google funnels removed. `daily_report.fetch()` rows are
already GST-inclusive.

---

## Standing requirements, added 5 Oct 2026

Asked by Ruchika as a spec for **every** future ad report, not a one-off. These sit on top of
everything above; nothing above is withdrawn.

1. **Google Analytics and GrowthX are part of the report.** Refresh both on every run. A stale
   `funnels_today.json` is never a substitute — if the GrowthX MCP is not connected, say the
   funnel half is missing and name it in the report body.
2. **Three views, in this order: Meta + Google combined, then Meta alone, then Google alone.**
   The combined view is the only place the two blend; within it the Community/Bootcamp split
   and the free/paid split still hold.
3. **Pace against the lead target per bootcamp**, in the blended view and again in the Meta
   view, because Meta supplies most of the leads. State whether the current run rate reaches
   the target before the camp date.
4. **ICPs and value props of every live ad, with their performance**, and a call per ICP:
   double down, add value props, or leave it. Judge an ICP against **its own campaign's** cost,
   never a cross-campaign median, and print `n` with the ±196/√n margin; under n=20 write
   "no call". The ICP library is the `value_props.md` blocks across all kit folders, joined to
   the live ad list by ad-name stem.
5. **A quality check on what is live**: broken or stubbed pay links, ads due a refresh
   (cost decaying faster than their campaign), LPs due a refresh, incorrect text.

### What this needs that does not exist yet

| Requirement | State on 5 Oct 2026 |
|---|---|
| GrowthX `get_leads_report` | MCP **not connected** to the session. Enable it in Connectors. |
| Google Ads | **No connector.** `googleads/google-ads-mcp` runs via uvx but needs an MCC developer token (multi-day approval). See the Google Ads access memory. |
| Google Analytics | **Nothing exists** — no connector, no GA4 property id anywhere in this repo. From-scratch setup. |
| **Lead target per bootcamp** | **Still does not exist**, as the Inputs table above already records. Requirement 3 cannot be met until the numbers are supplied. Ask for them; never derive one and present it as the target. |
| Live-LP quality check | **No script.** The gates (`check_all.py`, `preflight.py`) run against kit folders before ship, not against live URLs. Requirement 5 needs a live-URL checker that walks every live ad's landing page. |

Until each row is closed, run the parts that are wired and name the missing parts in the
report itself rather than quietly omitting them.
