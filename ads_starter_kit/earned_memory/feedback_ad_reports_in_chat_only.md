---
name: feedback-ad-reports-in-chat-only
description: "Ad reports go in the chat reply only - never an Artifact, never a report file saved in the repo"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1b7804e8-15ad-49d0-b3a7-3ce658932436
  modified: 2026-09-28T07:32:56.567Z
---

Ad reports (daily, per-campaign, boards) are written into the chat reply. Do not publish them as Artifacts and do not leave HTML/MD report files in the repo. Past reports were deleted 28 Sep 2026.

**Why:** the user, 28 Sep 2026: "I only want to see ad reports in the chat itself, not created as artifacts". SOP/10 used to say "Full report as an Artifact"; that line was replaced.

**How to apply:** `daily_report.py` now writes its HTML to %TEMP%; `pull_ads.py` (Ramanuj's shared repo, left unmodified) still writes to `ad-analysis-shared/reports/`, so treat that as scratch and read numbers from it. The chat format itself is unchanged: [[feedback-daily-report-chat-style]], [[feedback-ads-report-columns]], [[feedback-ads-report-day-by-day]].
