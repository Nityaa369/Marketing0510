---
name: feedback-daily-report-chat-style
description: "The daily ad report she likes - GrowthX funnel numbers per camp/community vs yesterday, free vs paid split, then plain \"What stands out\" bullets; not a list of 81 flags"
metadata:
  node_type: memory
  type: feedback
  originSessionId: ca6c6075-c746-4476-a92c-4c0a0b45026d
  modified: 2026-09-25T07:14:07.154Z
---

Asked on 24 Sep 2026: write the daily report the way the 21-24 Sep "Campaigns Daily Reports"
chat did (a Google report, pasted in). She liked it over the 81-item `daily_report.py` output.

The shape:
1. Time stamp + "part day" note, then a **headline**: spend, leads, paid, CPL, CPP, against yesterday.
2. A two-row box: **free-registration funnels** (spend, leads, CPL) and **paid funnels** (spend, paid, CPP), today vs yesterday.
3. **Report 1: Bootcamps**, split into free-registration and Rs 10 camps. **Report 2: Communities**, with Rs collected.
   Columns: spend, leads, paid, at checkout, CPL or CPP, and the same figure yesterday.
4. **What stands out**: 5-8 plain-English bullets with the numbers inside them - open checkouts,
   failed payments, ad-level winners/losers, new campaigns, a camp behind pace.
5. One reconciliation line: campaign spend adds up to the account total.

Leads/paid/checkout/failed come from GrowthX `get_leads_report` (one day per call), joined to
Meta spend by `group` [[project-growthx-extract-refresh]]. `daily_report.py` rows already include
GST - do not multiply again.

**Then combine** (asked same day, "COMBINE BOTH REPORT FORMATS"): after the bullets add the
SOP/10 parts in short form: dark camps, top pause calls, ads to scale, spread-thin ad sets, day by day.

**"Full detailed report"** (asked 25 Sep): add a camp-by-camp section. For each camp, list its Meta
landing pages (ads, spend, leads, paid, checkout, CPP) and its Google funnels from GrowthX. Join
ad to funnel with `daily_report.fetch_links` + `lp_slug`. Publish it as an Artifact, and update
the same URL during the day. Google spend needs a signed-in Google Ads session; the in-app browser
is not signed in, and the earlier chat used her Chrome.

**How to apply:** use this shape for chat replies; keep the HTML report as the attachment.
Still include the day-by-day table [[feedback-ads-report-day-by-day]].
