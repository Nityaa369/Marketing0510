---
name: feedback-en-dash-counts-as-em-dash
description: "The no-em-dash rule covers en dashes too: write date ranges as '3 to 5 Oct', never '3–5 Oct'"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72d8a971-d1c7-4903-b4a2-5bd535dd4e4b
  modified: 2026-09-21T13:35:02.053Z
---

Ruchika, 21 Sep 2026, on 19 search faces reading "3&ndash;5 Oct": *"i can see em dashes in
between the dates."* To the reader an en dash is an em dash. Write every range in words:
"3 to 5 Oct", "31 Oct to 2 Nov".

**Why no gate caught it:** ad_lint C7 counted only a literal U+2014 and never decoded
entities, so `&ndash;`/`&mdash;` in face HTML passed; lp_spine L3 checked em only. Both
widened the same day (C7 now fires on 126 of 355 repo faces, was 0), so older kits re-run
through check_all will now flag their dates.

**How to apply:** never emit `&ndash;` or `–` in copy, faces, pages or ad_copy. Related:
[[feedback-run-every-gate]], [[feedback-c8-reads-first-css-rule]] (same class of gate that
reads the source instead of what renders).
