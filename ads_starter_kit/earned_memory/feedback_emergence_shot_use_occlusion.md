---
name: feedback_emergence_shot_use_occlusion
description: "To generate someone emerging from a screen, describe occlusion; asking for part of the body to be inside the screen reliably produces a second copy of the person"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dc1f1eba-6002-4592-b9b5-7fca7c2942e6
  modified: 2026-09-23T16:38:41.424Z
---

Learned 23 Sep 2026 building the Senior AI "reach out of the screen" wave
(`SeniorAI_Reach_31Oct-2Nov`), adapted from `10_freedom`. Three prompt versions failed
before the cause was clear:

| Version | Instruction | Result |
|---|---|---|
| v1 | "mid-stride, stepping out" + "glass ripples like water" | Man fully outside the phone, vapour trail, no sense of where he came from |
| v2 | "his torso is still inside the screen, in black and white" | Overlap worked, but a **second copy of him** appeared inside the screen: shrunken trailing arm, body rescaled at the bezel |
| v3 | v2 plus an explicit anatomy lock (one head, two arms, exactly two legs, five fingers, no duplicated limbs) | **Still a third leg.** An anatomy lock cannot beat an instruction that literally says to draw a person inside the screen |
| **v4** | **Nothing of him is inside the screen.** The phone's edge "passes IN FRONT OF his trailing shoulder and leg and HIDES them completely, the way a door frame hides part of a person walking through a doorway." Screen shows the empty room, nobody in it | Clean on the first attempt, both variants |

**The rule: describe OCCLUSION, never a body rendered across two media.** "Half of him is
inside the screen" is read as "there is a person in the screen", so the model draws one.

Supporting lines that also earned their place in v4: "EXACTLY ONE PERSON EXISTS IN THIS
ENTIRE PICTURE", and naming the failure explicitly in the negatives ("no second figure, no
reflection of him, no silhouette of him, no grey copy of him anywhere").

**Two other things the same run settled:**
- **Ban text on surfaces, not just signage.** A generic "no text, no logos" still produced a
  fully legible whiteboard ("Migration Plan", a numbered list). The ban has to name
  whiteboards, monitors, documents, notebooks and planners as "blank or illegible".
- **Size from the chassis, not by feel.** The face is 1080x1350 and the hero band is
  1080x660 (1.64:1), so ask for landscape 3:2, never portrait - a 4:5 portrait cropped to
  the band throws away ~60% of the pixels. The chassis veils the bottom 56% and prints the
  headline there, so the prompt must reserve the bottom 40% for plain floor.

Prompts are generated from `gen_prompts.py`, not hand-edited, so all eight stay identical in
structure. Images can be generated in-session with the Higgsfield `generate_image` tool
(`gpt_image_2_5`, aspect_ratio 3:2, which returns 1024x688 and needs a ~5% upscale to reach
the 1080 band).

Related: [[feedback_ad_creative_use_real_images]], [[feedback_house_ad_formula]],
[[project_seniorai_history]].
