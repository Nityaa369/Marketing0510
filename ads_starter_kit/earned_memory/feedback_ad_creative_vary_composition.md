---
name: feedback-ad-creative-vary-composition
description: "New ad types" work must use genuinely different visual layouts per format, not one template with a different widget swapped in each time - and should lean into actual recognizable meme formats.
metadata:
  type: feedback
---

When building a batch of "new ad type" statics, each one needs its own visual skeleton
(different composition, different proportions, different placement of brand/chrome vs
content) - not a shared six-block stack (brand row / callout / heading / device-in-a-box /
define-sentence / offer-bar / CTA) with only the widget inside the "device" box changed
each time. That reads as one template, not experimentation.

**Why:** In the 18 Aug 2026 session, two batches in a row (Arbitration/SQE statics, then a
first Content Writing batch) used identical page structure across all 10 ads per batch,
varying only the small "device" widget in the middle. Rejected: *"The samples in the
folder... experimented with different visuals. This is the same static format with
different UIs over and over again. I want experimentation. I want memes."* The fix was a
third rebuild using 10 actually distinct, recognizable meme formats (Drake, Expanding
Brain, Two Buttons, Bell Curve, This Is Fine, Stonks, a conspiracy-board string diagram, a
chat exchange, Waiting Skeleton, a scoreboard) - each with its own layout skeleton. Only a
small brand mark/price badge (top corner) and a slim compliance bar (bottom) repeated
across all ten; everything in between was bespoke per ad, matching the proportion of the
real reference images already in the project (meme/photo fills ~80% of the canvas, chrome
is minimal).

**How to apply:** When asked for a batch of varied/experimental ad statics:
1. Actually use well-known meme formats by name (Drake, Two Buttons, Expanding Brain, Bell
   Curve, This Is Fine, Stonks, etc.) as the starting structural reference, not invented
   generic "callout + box" layouts.
2. Give each ad in the batch a genuinely different layout, not a shared template.
3. Keep brand/price/compliance chrome small and in a corner/edge, so the meme itself
   dominates the canvas - do not let a big uniform header block eat the top third of every
   ad.
4. Watch for dead/empty space: a `flex:1` container with `justify-content:center` around a
   small text/icon cluster leaves large unintentional-looking blank margins on a 1080x1350
   canvas. Either make the content fill the space (bigger elements, more rows) or give it a
   full-bleed colored background panel so the empty margin reads as designed breathing room
   rather than a bug.
5. Per [[feedback_ad_creative_use_real_images]], when real reference photos exist for the
   topic, crop and use those instead of any of the above - this note applies specifically
   when no such photo library exists and original graphics are the only option.

See also [[feedback_ad_clarity_rules]] for the underlying legibility bar these layouts
still need to satisfy regardless of format.
