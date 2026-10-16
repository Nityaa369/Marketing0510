---
name: feedback-airdrop-layout
description: "The AirDrop share-sheet face: radar icon, 'X wants to share: <file>.pdf', a ticked checklist of the camp's real deliverables, Decline/Accept; the reader goes in .callout and the turn in .head"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-10-01T07:16:36.150Z
  originSessionId: f1085e60-b1db-41dd-952a-195f5347d203
---

Built 1 Oct 2026 from a reference Ruchika sent (a skincare AirDrop meme), as Tech Law
`TechLaw_Meme_24-26Oct` stems 71-75. Scaffolded with
`python -m adkit.layouts --new airdrop`, which clones `notice` so it renders and clears the
64px floors before any CSS is written.

**What makes it argue instead of decorate: the checklist rows are the camp's named
deliverables.** The inspo's rows were a mood ("drink more water"). Ours are the documents you
leave with, which is also how Rule 2's three-named-deliverables test gets satisfied on the face.

**The slot mapping that satisfies the gates.** The inspo has no audience band, so:
`.callout` = the reader, `.head` = the turn as the sheet's own highlighted line, and the
filename carries the promise per reader ("what to do with your LLB.pdf"). Both identity classes
use `_idpx`, so auto-fit (0.80 to 0.88 on these) cannot push them under 64px.

**Order, corrected by Ruchika 1 Oct on first look:** *"put the heading (icp) at the top, then
the airdrop bit"*. The ICP band had been under the filename and read as an afterthought on a
device whose own chrome is the loudest thing in the frame. It goes at the very top of the card,
above the radar.

**It also needs a real join button:** *"there is no clear join now button"*. Decline / Accept is
the device's chrome and reads as iOS, not as a CTA, so a full-width `.bigbtn` on the accent goes
below the sheet with the delivery sentence above it and the terms under it. Same lesson as the
notice faces on 29 Sep, where a small footer pill was rejected - see
[[feedback-full-width-join-button]].

**On the landing page the hero drops the head banner**, because the page already carries the
head as its h1 and showing it twice in one screen reads as a stutter. Keep the radar, the
sender line, the filename and the rows.

Palette note: `pal` has `page/accent/ink/card/line/soft` and **no `tint`** - use `soft` for a
tinted bar. Related: [[feedback-film-still-layout]], [[feedback-notify-layout]],
[[feedback-notes-layout]], [[project-techlaw-oct-cpm-diagnosis]].
