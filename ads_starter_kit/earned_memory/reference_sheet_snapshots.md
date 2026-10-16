---
name: reference-sheet-snapshots
description: Dated raw reads of the bootcamp dates sheet sit in earlier sessions' tool-results; use them to prove when a camp's time changed
metadata:
  type: reference
---

The bootcamp sheet is view-only for Ruchika, so Google's cell edit history and version history are
not available. Earlier sessions saved raw reads of it (Drive connector `read_file_content`) under
`~/.claude/projects/C--Users-Ruchika-Claude-ads-tasks/<session>/tool-results/mcp-b99f1b26-...-read_file_content-<ms>.txt`;
the 13-digit number is the read time in ms since epoch. Reads exist for 10 Sep 16:52, 17 Sep 13:17
and 18 Sep 12:42 IST (2026). Rows are pipe-separated inside escaped text: match
`| name | month | date | day1 | day2 | day3 | ...` with a regex, not by line.

What they proved on 28 Sep 2026:
- Academic Writing 24-26 Oct: 6-9 PM on all three reads, 2-5pm by 28 Sep 12:51 (changed after 18 Sep).
- Academic Writing 26-28 Sep: 6-9 PM on 10 Sep, 2-5 PM "(scheduled for 2-5 pm)" by 17 Sep.
- Senior AI 3-5 Oct: 2-5 PM on every read since 10 Sep, so the ads' 6-9 PM never came from the sheet.
- NCA 31 Oct: 2-5 PM since it was added (17 Sep).

**Why:** "they changed the time without telling us" needs a before-and-after; the repo's cached
BOOTCAMP_CALENDAR.md alone looked wrong until these reads showed the sheet itself had moved.
**How to apply:** save each fresh sheet read (CSV export works: /export?format=csv&gid=9975817) with a
date in its name, and diff against the last one at the start of every wave.
Related: [[reference-bootcamp-dates-sheet]], [[project-lp-swaps-sep28]].
