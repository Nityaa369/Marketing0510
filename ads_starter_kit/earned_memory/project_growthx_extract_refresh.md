---
name: project-growthx-extract-refresh
description: "funnels_today.json is refreshed from the get_leads_report MCP tool, not a browser; reconcile to Meta by GrowthX `group` with Google funnels removed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6b3cc398-ae3d-4243-9d01-8ae42f98a796
  modified: 2026-09-21T05:54:33.997Z
---

**`funnels_today.json` is the GrowthX order data, and it is refreshed from the
`get_leads_report` MCP tool** (server `1a4ed2c1...`), which returns exactly the JSON
schema the file already uses — `total`, `paid`, `truncated`, `byFunnel[]`. No browser
is needed. `daily_report.py`'s own docstring says so: *"as saved from the
get_leads_report MCP tool."* Asked for via Chrome on 21 Sep 2026; the MCP path is
faster and exact, so it was used instead.

```
list_filter_options            # valid group / leadtype names, says if live
get_leads_report from=.. to=.. # max 1 month span; output lands in a tool-results file
```

The result exceeds the token cap and is auto-saved to a file — load that with
`json.load` and write it out; do not try to read it inline.

**Refreshed 21 Sep 2026 for 8–21 Sep: total 48,558, paid 17,475, 833 funnels,
revenue ₹5,99,630.** The file it replaced was dated **10 Sep — eleven days stale** while
named `today`, and `daily_report.py` read it without complaint. Now also written as
`funnels_2026-09-21.json`, with `_window` / `_pulled` / `_source` keys added
(`load_funnels` ignores unknown keys), and the stale one kept as `funnels_2026-09-10.json`.

## Reconciling GrowthX against Meta — join on `group`, not `leadtype`

Two joins were tried on 21 Sep and only the second works:

- **`leadtype` fails.** Many funnels carry `leadtype: None` — every
  `*_ID_Community` funnel does. Joining on it made Independent Director Community read
  as Meta +222% over GrowthX, which looked like a serious over-attribution finding and
  was entirely a join bug. Filtering to funnel names starting `meta` makes it worse,
  because plenty of Meta funnels are not named that way.
- **`group` works**, with Google-named funnels removed (`funnel.lower().startswith("google")`)
  and `funnelType` respected: a `lead` funnel's result is `total`, a `paid` funnel's is
  `paid`. Two groups need merging by hand: Academic Writing is split across
  `academic writing` + `ACW_Meta`, and `US Accounting and Bookkeeping` holds both the
  Sep and Oct camps, so split it by `leadtype` for a per-camp figure.

**The result: all 16 live campaigns agree within ±11%, most within 6%.** Meta's pixel
purchase counts are sound and the "Meta is inventing sales" failure mode is ruled out
for this window. Record this before chasing an attribution ghost.

Related: [[reference-growthx-funnel-checkout]], [[feedback-report-scripts-narrow-silently]],
[[feedback-contradiction-means-failed-test]], [[feedback-ads-reports-route-through-token]].

**22 Sep 2026: pull 7 days at a time, never 14.** On 22 Sep a 14-day query (8-21 Sep) returned
22,193 rows while 15-21 Sep alone returned 30,371, with `truncated: false` both times. Seven
single-day pulls summed exactly to the 7-day figure, so 7-day windows are sound. A window that
includes today can also come back as all zeros. The MCP server id changes between accounts
(1a4ed2c1 on one, f93af04a on the other); the tool name `get_leads_report` is the constant.
