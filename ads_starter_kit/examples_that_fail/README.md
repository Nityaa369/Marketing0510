# examples_that_fail

Four faces from the archive that **a gate blocks today**. They are here for two reasons.

**They keep the pixel gate honest.** `simplicity.py --selftest` ends with a liveness probe:
*"a gate tuned until it fires on nothing is not a gate."* It scans the faces on disk and
reports what still fires. Without something that genuinely trips a rule, the probe reports
`NOTHING - the rules are dead, fix them`, and you cannot tell a clean corpus from a dead
rule. All four of these trip **L3**, measured contrast on the rendered PNG: type that is
faded or hairline-thin enough that a reader on a phone in daylight does not read it.

```bash
python simplicity.py --selftest     # the LIVENESS line should report {'L3': 4}
```

**They are negative examples.** Look at them next to `GOLDEN/`.

| Face | From | Why it is here |
|---|---|---|
| `cw_01_types_clients.png` | ContentWriting, 29-31 Aug | L3. Content writing wave one. |
| `icp_11_freshgrads.png` | Patent waves 3-4, 7 Aug | L3. |
| `pc_independent_director.png` | Independent Director pay chart, 12-14 Sep | L3, and the format itself is the lesson: **pay-chart faces cost about 2.3x campaign par in three separate product lines.** A salary ladder belongs on the landing page and never on an ad face, which is also a standing compliance rule. |
| `c6_s1.png` | Tech Law "10 reasons", 15-17 Aug | L3. |

These four are not in `ad_copy.md` form, so they stay out of the corpus index and can never
be picked as a blind-reader control. Nothing else from their kits travelled with them.

**L3 firing is not the same as a rejection by the reviewer.** It is one mechanical rule
reading one property of the image. Several of these faces shipped. Read it as "this would be
caught today", not as "this was rejected then".
