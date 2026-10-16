---
name: feedback-ads-report-columns
description: The five columns Ramanuj wants in any ads performance report - ad, spend, buyers, CPP, link to the ad
metadata:
  type: feedback
---

When asked for an ads report or "how are X ads doing", report these five data points per ad:
**ad name, spend, buyers (purchases), CPP (cost per purchase), and a link to the ad itself.**

Stated 31 Aug 2026 after a Global Patent Analysts report that led with spend, impressions,
clicks, CTR and CPM. Impressions/clicks/CTR/CPM are not the requested columns - they can be
added as context underneath, but they are not the report.

**Why:** the decision being made is which creative to fund and which to cut. That needs the
money in, the buyers out, the cost of each, and the ability to actually look at the creative
being judged. CTR is explicitly not decision-grade here - see [[feedback_paychart_and_ctr_traps]],
where CTR ran backwards against CPL.

**How to apply:** default table is `Ad | Spend | Buyers | CPP | Link`. Report every ad in the
campaign, not just the ones with meaningful spend - say which are starved rather than omitting
them. Ad link format that works: `https://adsmanager.facebook.com/adsmanager/manage/ads?act=<account_id>&selected_ad_ids=<ad_id>`.
Meta calls the conversion "Website purchases"; call it buyers.

Reaffirmed 31 Aug 2026: link every ad, ad set and campaign named anywhere in a report, in
recommendations as well as tables, and link the name itself rather than appending a bare URL.
Ad set and campaign patterns, confirmed against the deeplink `ads_insights_anomaly_signal`
returns: `.../manage/adsets?act=<account_id>&selected_adset_ids=<id>` and
`.../manage/campaigns?act=<account_id>&selected_campaign_ids=<id>`. Several ids join with
`%2C`; the account id carries no `act_` prefix. At ad level request `campaign_id` - the field
`campaign_name` is not supported there, so `campaign_id` is the only correct way to group ads
by campaign instead of guessing from name prefixes. For the rendered creative rather than the
row, use `ads_get_ad_preview`.

Related: [[feedback-ads-report-day-by-day]] - the same report also carries a day-by-day table (day, spend, buyers, CPP, last 14 days). The two together are the full report: the daily series first, then the per-ad table.
