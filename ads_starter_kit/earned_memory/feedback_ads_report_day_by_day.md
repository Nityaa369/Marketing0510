---
name: feedback-ads-report-day-by-day
description: Every ads performance report must include a day-by-day table - day, spend, buyers, CPP - not just today vs yesterday
metadata:
  type: feedback
---

Any ads performance report includes a **day-by-day table** as a standard section: one row
per day with **day, spend, buyers (purchases), CPP (cost per purchase)**. Asked for on
31 Aug 2026 after a report that only carried today-vs-yesterday.

**Why:** a single day-over-day comparison cannot separate a real trend from noise. Two
points make every move look like a signal. The daily series is how you see whether a CPP
move is drift, a step change, or the usual weekday shape - and it is the view the account
is actually judged on.

**How to apply:** default to the last 14 days. Pull it with `ads_get_ad_entities` at
campaign level with `time_increment: "1"` and `date_preset: "last_14d"`, then aggregate
spend and purchases per day across purchase-objective campaigns; CPP is spend over buyers,
recomputed per day, never averaged from the per-campaign CPPs. Account level does not
support `cost_per_result`, so campaign level is the level to pull. Keep lead campaigns out
of the CPP maths and report leads separately. Mark the current day as partial - it is a
part-day number sitting next to full days and will read as a collapse in spend otherwise.

Related: [[project-meta-data-pull-path]], [[feedback-ads-report-columns]] - the per-ad half of the same report is ad, spend, buyers, CPP, link to the ad.
