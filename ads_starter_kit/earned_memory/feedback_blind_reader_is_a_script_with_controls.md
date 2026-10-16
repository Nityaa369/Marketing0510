---
name: feedback-blind-reader-is-a-script-with-controls
description: "The blind-reader test is blind_reader.py with priced winners blinded in as controls; the verdict is relative, never a fixed 3-of-3 bar"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8aa53e3e-85fb-4783-9c48-c46acdf94f1d
  modified: 2026-09-15T06:00:03.417Z
---

The blind-reader test is now `python blind_reader.py --prepare <kit>` → one fresh subagent
per `packet_F*.txt` → `--score <kit>`, and `check_all.py` gates on it (ERROR for a kit that
never ran one, or whose faces were re-rendered after it — the result is mtime-aware).

Candidates AND three faces that demonstrably worked are copied into `.blind/` as
`F01.png, F02.png…`, shuffled. The reader cannot tell which face is under test, and neither
can the session spawning the agents, so a bad verdict cannot be discounted after the fact.

**Why:** the instruction to run this in isolation sat in 30 files and zero scripts (grepped
15 Sep 2026), which made it the last check in the repo on the honour system — while pixel
gaps, type floors and hedge windows all had real gates. And the director's "run the control
before acting on a bad verdict" only ever fired *after* bad news, by which point four rebuild
passes had already gone into chasing a broken ruler (the Patent faces, 3 Sep).

**The verdict is relative and this is measured, not a preference.** First real run,
AcademicWriting Wave 1, 8 isolated Explore subagents, 15 Sep 2026: `us05_evening` — Rs 31 per
lead, the second-cheapest ad in the account — scored **2/3**, failing "what will I be able to
do on the last day". All five candidates scored 3/3. A fixed "three clean answers or it is
cryptic" bar would have condemned a priced winner. Controls at 0 report ERROR and block
nothing, because then the instrument failed, not the ads.

**How to apply:** never re-introduce an absolute threshold. Where the gate disagrees with an
approved or cheap face, the face wins and the rule gets refitted — see
[[feedback-checkers-refit-basis]]. The reader gets the rendered PNG, not extracted text:
only one of the nine priced-or-approved winners still had an html/ source in the repo, so a
text-only test cannot assemble a control set at all ([[feedback-blind-reader-needs-the-whole-face]]).
It measures comprehension and never desire — a face can pass every question and still sell the
buying decision rather than a job ([[feedback-headline-names-job-not-buying]]).

**Control bug fixed 17 Sep 2026.** corpus.match_live joins ad names on shared words, so every
refresh of a reader inherited its predecessor's cost: `us43_search_small_town` (never run) and
`us04_small_town` both carried us25's Rs 40 and were used as "priced" controls. blind_reader.py
now requires one name to contain the other before a live cost counts. The US Accounting verdicts
still stood (their 2/3 floor came from us05_evening, a real priced face).
