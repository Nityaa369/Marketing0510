---
name: feedback-ad-report-standing-requirements
description: "Every ad report must carry five things: GA + GrowthX, blended then Meta then Google, lead-target pace, live ICP/value-prop performance with a double-down call, and a quality check"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e73dfe4f-601b-4c48-9079-7afa2d33dc8b
  modified: 2026-10-05T07:36:05.363Z
---

Asked 5 Oct 2026, as a standing spec for **every** future "today's ad report". This extends
[[feedback-daily-report-chat-style]] (the chat shape) and [[feedback-ads-report-columns]] /
[[feedback-ads-report-day-by-day]] (the tables); none of those are replaced.

1. **Google Analytics and GrowthX numbers are part of the report, not an optional extra.**
   Refresh both every time. A stale `funnels_today.json` is not acceptable as a substitute.
2. **Three views, in this order: Meta + Google combined, then Meta alone, then Google alone.**
3. **Pace against the lead target per bootcamp** in the blended view, and again in the Meta
   view, because Meta supplies most of the leads. State whether the current run rate reaches
   the target before the camp date.
4. **ICPs and value props of all live ads, with their performance**, and an explicit call per
   ICP: double down, add more value props, or leave it. Not just a list — a recommendation.
5. **A full quality check**: broken links, ads needing a refresh, LPs needing a refresh,
   incorrect text.

**Why:** the report is used to decide where money goes next and what to build next, and a
Meta-only cost table answers neither. Points 3 and 4 are the decision; 1 and 2 are the inputs;
5 is what stops spend running at a broken page.

**State of the plumbing as of 5 Oct 2026 — three of the five need wiring:**

- **GrowthX**: `get_leads_report` MCP is NOT connected to this session (connectors present:
  Higgsfield, Claude Docs, visualize, scheduled-tasks). The tool name is the constant; the
  server id varies by account. See [[project-growthx-extract-refresh]]. Until it is enabled,
  say the funnel half is missing — never fall back on the stale file.
- **Google Ads**: no connector. First-party `googleads/google-ads-mcp` runs via uvx but needs
  a developer token from the MCC API Center, which is a multi-day approval.
  See [[project-google-ads-access-path]].
- **Google Analytics**: nothing exists anywhere — no connector, no property id in the repo,
  no reference in any SOP. This is a from-scratch setup, not a reconnect.
- **Meta**: fine, via the System User token [[feedback-ads-reports-route-through-token]].
- **Lead targets per bootcamp**: DO NOT EXIST. `SOP/10_DAILY_AD_REPORT.md` lists "Fill targets
  per camp" as still open and says explicitly *"Until the GrowthX MCP lands there is no fill
  target to measure against ... Do not invent one."* The only settled targets are cost ones
  (SOP/02: CPP Rs 300 or better incl. GST, plus dynamic trailing baselines). Ask her for the
  per-camp numbers; do not derive one and present it as the target.

**How to apply:** run the parts that are wired, and name the missing parts in the report
itself rather than quietly omitting them. Reports still go in the chat reply only
[[feedback-ad-reports-in-chat-only]].
