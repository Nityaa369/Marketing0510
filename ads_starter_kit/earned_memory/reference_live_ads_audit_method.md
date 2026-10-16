---
name: reference-live-ads-audit-method
description: "How to audit every live Meta ad (links, wrong campaign, LP refresh, camp coverage) in one pass, and the traps hit doing it on 28 Sep 2026"
metadata:
  node_type: memory
  type: reference
  originSessionId: fa845281-08bd-45e2-9141-19982a7eb62d
  modified: 2026-09-29T07:00:58.648Z
---

First full live-ads audit ran 28 Sep 2026 for Ruchika (broken links, wrong campaigns, LP refresh,
camps needing ads, other issues). Method that worked:

- **Pull by ad, per account, in parallel**, using `pull_ads.token()`/`paged()`: `act_X/ads` with
  `creative{object_story_spec,asset_feed_spec,...}`, adset/campaign status, plus ad-level insights
  for 7/3/1 days. "Live" = spend in the last 3 days, not `effective_status` - about 4,200 ads show
  ACTIVE at every level but sit in 2023-25 campaigns whose ad sets ended (harmless clutter).
- **Skip the DISABLED Law Sikho account** - it has 2,163 switched-on ads and the call fails with
  "reduce the amount of data".
- **Skill Arbitrage rate-limits the `/ads` endpoint after one full pull** and stayed locked for
  over an hour; `paged()` returns a partial list silently. Cross-check campaign spend from
  `--list` against the ads you got. The `/insights` endpoint kept working, so ad names for a
  missing campaign come from `{campaign_id}/insights?level=ad`.
- **Python urllib with a browser UA fetches GrowthX pages fine** (200 + `__FUNNEL_DEPLOYER__`).
  A 404 "Funnel not found" is a real missing slug. Checkout is proven by the iframe-click test in
  [[reference-growthx-funnel-checkout]]; a text mismatch like "₹ 100" vs "₹100" is not a fault.
- **Built-but-unlaunched kits:** read slugs from each `*_SEND_THIS.zip` manifest.json (ship folders
  get deleted; zips stay) and diff against every ad link in Meta.
- **Tracking reconciles:** GrowthX paid vs Meta purchases matched within ~5% on 6 campaigns, so
  Meta purchase counts are trustworthy; LPV and frequency are not (WhatsApp Status, see
  [[feedback-whatsapp-status-fakes-frequency]]).

**Daily re-run (29 Sep 2026):** Ruchika asks for it as "today's ad quality audit like yesterday".
Pull **campaign-first** (campaigns with 3-day spend via act insights, then `{cid}/ads` +
`{cid}/insights`): 970 ads in ~2 min with no rate limit. Scripts kept in the session scratchpad
`aud29/` (pull29.py, an29.py, lp29.py). The report leads with what changed since the previous run:
fixed items, pages edited (diff words/dates per URL against the last links.json), new ads, kits
still unlaunched (manifest slugs vs Meta + whether the funnel slug 404s), and pages newly past 2x.

Related: [[feedback-launch-check-by-ad-not-campaign]], [[feedback-ads-reports-route-through-token]].
