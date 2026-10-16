---
name: feedback-film-still-layout
description: "The film-still meme face: generated B&W Hindi film still, two caption boxes, one line the family would really say and one plain answer; its LP hero lays the exchange UNDER the still because the face's px positions do not survive a 680px column"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-10-01T06:07:41.074Z
  originSessionId: f1085e60-b1db-41dd-952a-195f5347d203
---

Format from a reference Ruchika sent 30 Sep 2026. Built as `TechLaw_Meme_24-26Oct`, faces 61 to
65, on the existing `photo` layout plus a `bubbles` extra added to `adkit/layouts.py` the same
day. Face 61 approved same day: *"Love this"*.

**The joke must not need decoding.** Ruchika: *"the meme joke should not be hard to understand."*
One line the family, a colleague or a boss would really say, and one plain answer that names the
better job. No wordplay. The reader is named in the call-out, so the exchange carries the turn.

**The stills are generated** (GPT Image 2.5 on Higgsfield), never real film frames: a real still
is copyrighted and its actors imply endorsement. Keep rejected takes in `photos/_unused/` and
check none is close to a real actor's styling. The LP footer says the stills are illustrations
created for the campaign.

**The LP hero cannot reuse the face's geometry.** The face positions its caption boxes in px on a
1080x1350 canvas; those offsets break in a 680px column. Rebuild the hero as a `.still` figure
(the photo, grayscaled) with the two lines underneath as an `.exchange`, second line right-aligned
in the accent colour. The words stay the ad's words, which is what Rule 3 actually asks for.
Blind read 3/3 on all five faces; closing folds 3/3.

**Why the wave existed**, which is the part worth copying: it was a CPM fix, not new ICPs. See
[[project-techlaw-oct-cpm-diagnosis]]. Related: [[feedback-ad-creative-use-real-images]],
[[feedback-house-ad-formula]], [[project-21-step-lp-spine]].
