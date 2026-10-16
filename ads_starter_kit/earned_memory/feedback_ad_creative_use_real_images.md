---
name: feedback-ad-creative-use-real-images
description: "When building ad creative devices/illustrations for LawSikho/SkillArbitrage, never hand-author graphics - crop and reuse the real reference images already in the project."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7683fe6f-af49-4571-9d73-80254c30bed3
  modified: 2026-08-18T13:19:57.151Z
---

Never hand-draw or CSS/SVG-mock-up illustration, icons, or app-chrome for ad creative in
this project (ads tasks). No drawn characters, no drawn UI (fake poll bars, fake notes-app
chrome, drawn avatars/circles-as-people). Instead, crop the actual illustration/photo bands
out of the real reference images already provided in the relevant folder (e.g. the
`WhatsApp Image *.jpeg` files in `new ad types/`) and place those crops directly into the
layout, typically with `object-fit:contain` so no baked-in dialogue text or timestamp gets
clipped.

**Why:** In the 18 Aug 2026 session building `new ad types/formats_v1_aug18/`, a first pass
built CSS-drawn mockups (fake Instagram poll UI, fake iOS Notes app, abstract circles for a
"Two Buttons" meme, plain text boxes standing in for a "This is Fine" dog scene) to avoid
reproducing third-party copyrighted meme material (film stills, Jake Clark's Two Buttons,
KC Green's This is Fine) in paid ad creative. The user rejected this outright: "where are
all the memes?", "just copy and add the image", "do not draw anything." The real reference
images already in the project are commissioned/generated illustration assets (not
third-party copyrighted memes) and look far more authentic than anything producible via
code in this session (no image-generation tool is available - only HTML/CSS/SVG rendering
via headless Chrome). The fix was `PIL`-based cropping (`crop.py`) of the illustration band
out of each real reference image, reused across ad layouts as plain `<img>` tags.

**How to apply:** Before building any new ad/meme-format creative here, check what
reference images already exist in the relevant folder first. Use PIL to crop clean
illustration-only bands (no ad's own baked-in headline/CTA text bleeding in) rather than
inventing new visual content. See also [[feedback_ad_clarity_rules]] for the broader
ad-quality bar this project holds creative to, and [[feedback_ad_creative_vary_composition]]
for why the layout around the photo also needs to vary, not just the photo itself.

**Update, same session, Content Writing batch:** no in-project reference photos exist for
every topic (Arbitration/SQE had a folder of commissioned illustrations; Content Writing had
none). Asked directly why I couldn't just source photos myself instead of waiting for the
user to supply them ("Can't you pick the reference photos from the internet? Why do I have
to supply them?"). Resolution: **licensed stock photography (Pexels/Unsplash, free for
commercial use, no attribution required) is a legitimate source and should be used by
default** when no in-project photo exists - don't fall back to drawn/CSS mockups and don't
make the user manually supply images that a licensed stock search can find. Generic web
image search results (not from an explicitly-licensed source) remain higher legal risk since
they're typically someone's copyrighted photography - flag that distinction if it comes up,
but the user has separately stated they're willing to accept broader image-sourcing risk
when asked directly, so don't block on it if they say so again. See
`new ad types/formats_v4_contentwriting_photoled/` for the working pattern: download via
`curl` from the Pexels/Unsplash CDN direct-image URL (extract from the page's `og:image`
meta tag if needed), save into a `stock_<topic>/` folder alongside the kit, cite the source
page in the kit README.
