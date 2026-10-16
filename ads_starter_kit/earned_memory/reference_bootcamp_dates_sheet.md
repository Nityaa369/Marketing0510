---
name: reference-bootcamp-dates-sheet
description: The live Google Sheet that is the source of record for every bootcamp date - read it before generating any ad, never trust the cached calendar
metadata:
  type: reference
---

**Bootcamp dates live here, and this sheet wins over anything in the repo:**

https://docs.google.com/spreadsheets/d/1vfTsS7b976HYpYW_xV2e31UkV9kr_--UCoAjDh24zss/edit?gid=9975817#gid=9975817

Given by Ruchika 10 Sep 2026, with the instruction to keep it for all future ad
generation. Readable through the Google Drive connector with
`read_file_content(fileId="1vfTsS7b976HYpYW_xV2e31UkV9kr_--UCoAjDh24zss")` - the
response is large and lands in a tool-results file, so parse it rather than reading
it whole.

**Shape:** one markdown table, ~461 rows. Columns are BOOTCAMP NAME, MONTH, DATE,
Day 1/2/3 timings, DAYS, BRAND, ZOOM ACCOUNT, LEADERS, WhatsApp joining link, RUNWAY,
WA FUNNEL DOC. Camp names carry the `MAIN -` / `RE -` prefix, matching
`BOOTCAMP_CALENDAR.md`. Note the dash in the October rows is an en dash, not a hyphen.

**Two traps:**

- **It is a rolling multi-year sheet.** The first rows are January and February and
  those have already passed. Never read from the top - filter to dates ahead of today.
- **There is a second block further down** with different camp names (webinar-style
  titles like *"How to kickstart your international IP law career today"*). The first
  block is the bootcamp calendar proper; the second is a different series. Do not mix
  them.

**October 2026, copied into `BOOTCAMP_CALENDAR.md` on 10 Sep 2026:** camps run Sat-Sun-Mon
on 3-5, 10-12, 17-19, 24-26 Oct and 31 Oct-2 Nov. Senior AI MAIN is **3-5 Oct**, and a
Senior AI RE closes the month on 31 Oct-2 Nov.

**How to apply:** re-read the sheet at the start of any wave rather than trusting the
cached copy, and update `BOOTCAMP_CALENDAR.md` when it has moved - the daily report's
coverage check reads that file, so a stale calendar produces false dark-camp findings.
See [[feedback-reruns-are-never-advertised]] for why only MAIN rows are checked.
