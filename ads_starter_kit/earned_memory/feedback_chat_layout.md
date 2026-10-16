---
name: feedback-chat-layout
description: "The `chat` layout and the five copy rules it took to get right - the reader's own text, a forwarded flyer with the agenda and a register button, and a friend's nudge as the last bubble"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4d1fca80-c9d7-436b-8c41-3000397bc5e2
  modified: 2026-09-18T06:06:13.072Z
---

Built from a DTC chat-thread static Ruchika supplied ("Girl! My skin is breaking out, what
should I do?" / product picture / "Try this"). adkit/layouts_custom.py `chat`. Five rounds of
review on 17-18 Sep 2026 changed the COPY every time and the skeleton never. What they settled:

1. **Message 1 is the reader's own message, first person.** v1 put an ad call-out in the grey
   bubble ("A banker, retired after 30 years?"). *"the first message and the second message are
   not cohesive... the problem statement and solution are too obvious [in the reference]. That
   is what we want."*
2. **The register is texting, not headline.** *"is this how people text?"* Lower case, a
   fragment, one emoji, no full stops in the middle: "30 yrs a banker, retiring in March. no
   idea what after". It is message 1 that does the recognising, never message 2 - *"people
   should either instantly recognize or reject it"* - so message 1 names the job and the
   situation and nothing else.
3. **The flyer carries what happens in the camp.** *"in the original ads, there is more
   information around what happens in the bootcamp. currently it is all lost."* The poster is
   an event flyer: accent band (FREE + brand), headline, date, the three sessions by date with
   one line each, a "You keep:" line, then a register button.
4. **A real button, and the bubble fills its width.** *"there is no button where people can
   click to buy"* -> the flyer gets the button (a chat bubble is a person talking, not a
   control). *"why is it so left aligned?"* -> `text-wrap: balance` on a message bubble evens
   the lines and costs a whole line of height. Removed; bubble at 92%.
5. **The last bubble nudges, never sells.** *"can it be something like why don't you explore
   this? OR Have you thought about this?"* FREE is already on the flyer band and the button, so
   the closing line is free to be "Have you thought about this? / Why don't you look into this /
   Worth a look", varied per face like the emoji.

**Shapes.** B (message -> flyer -> nudge) is the default and the reference's own. A adds one
friend's line between them, and only where it carries a fact the reader does not know (the
10-year practice exemption from the IICA test). At the 0.80 fit floor, A costs about one line.

**Gates it trips.** S6/C23 want a job word in the message: "in the bank", "ran my own company",
"in internal audit" all failed - write "a banker", "founder", "an internal auditor". S1 runs
~110 words because of the agenda, which is a FIX, not a blocker, and the words are the point.
`fit` cannot see text clipped INSIDE a box, so every thread item is `flex: none`.

**Evidence warning:** SOP/10 prices chat faces at 1.22x par; nothing on this layout has a live
cost. Related: [[feedback-search-layout]], [[feedback-every-statement-must-be-sourced]].
