---
name: feedback-calendar-layout
description: "The calendar layout - the reader's own week with the paid work already in it; four rows only, one accent event, no fake controls"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ede3d7bb-967e-4a12-b319-fa4569f4dabe
  modified: 2026-09-23T08:47:44.097Z
---

Built 23 Sep 2026 from a calendar-UI static Ruchika supplied (day strip, hour rows, one coloured event, plus a food photo and stickers). Chosen for the whole Strategic HR 31 Oct wave after a side-by-side against the priced `serif` block on the same offer: "go with the calendar, generate that for all icps".

**The skeleton:** day strip with one day circled, a one line date caption, then FOUR rows and no more. Two rows are the life she has now, one accent row is where the client abroad appears, the last row is being paid. The reference's photo, stickers and twelve empty hours are decoration and were dropped; twelve rows would shrink the event line below reading size.

**Only for readers whose story is time** - evenings, school hours, an empty week after a break, a week split across four clients. For anyone else the device says nothing the headline does not.

Gotchas found on the first wave:
- The time column is ~120px. A label like "The rest of the week" wraps to three lines; keep it to one word ("Weekend").
- `ad_lint` C1's verb list had no "recruit", so an imperative headline read as a noun fragment. Widened with recruit, source, screen, onboard, bill, charge, serve, automate, set; C1 fires the same 4 times on 98 shipped faces before and after.
- C26 fires on "Book my seat" unless the price line states the whole exchange: "Rs 10 gets you all 3 evenings".
- `python build.py <name>` silently renders nothing if the name filter does not match; the old face stayed on disk and the judge kept rejecting it. Re-run the whole build when in doubt.
- For the page screenshots, the sticky pay bar is fixed to the bottom of the CAPTURE, so every shot came out full height with nothing trimmed. Crop that band before looking for the end of the page.

**No live cost yet.** The only two fake-UI formats this account has measured went opposite ways: the tweet card at Rs 126 (cheapest static in the HR account) and chat at 1.22x par. See [[feedback_vary_the_design_style]] and [[feedback_chat_layout]].

**Page hero, 28 Sep 2026:** `adkit/calendar_hero.py` is the calendar ad's own CSS scaled to a 600px
column (same idea as `search_hero`); use it for every calendar LP so the first screen is the ad.
The rail stacks under 480px. `chassis.render(*only)` filters by ad NUMBER ("01"), not name; it now
prints NOTHING RENDERED instead of silently skipping. First ID face (01_cal_recently_retired) passed
all 11 gates, blind read 3/3 and UP.

**Approved face, 28 Sep 2026 (ID 01_cal_recently_retired), after five rounds:** every row must point at
something on the card ("Preparing for Thursday's board meeting", not "the company's CFO" or "papers");
the line under the calendar is ~18 words ("3 free live sessions, 10 to 12 Oct: what the job is, how to
qualify, and the 6-month plan to get there") set large with `extra["deliver_big"]=True` (38px bold,
opt-in so HR faces do not move); the terms strip carries the session TIMES, not a repeat of free/dates.

**Wave lessons, 28 Sep 2026 (ID calendar, all 9 faces through every gate):** (1) the line under the
calendar must say what the reader LEAVES WITH, not list topics - "what the job is, how to qualify, and the
6-month plan" failed blind Q3 on 2 of 9; "learn the job and how to qualify, and leave with your 6-month plan
to join a board" passed 9 of 9. (2) A situation call-out still needs a word S6 counts as identity:
"Took VRS or early retirement?" and "Handed the business to the next generation?" blocked; "Took VRS, or
retired early?" and "Business owner, retired from the day-to-day?" pass. (3) The page's closing FAQ heading
must name the subject ("... about board seats") or closing readers say the page never names the role.

**28 Sep, fill:** a short headline left an empty band between the delivery line and the offer (id36, id39
beside seven fuller faces; the gaps gate passed at 137px, so only a side-by-side sheet showed it). Fix is
extra["fill"]=True: the calendar rows take 4/5 of the spare height. Always review a wave as one contact
sheet before calling spacing done. Also: never let the accent row repeat the headline (id38 did).
