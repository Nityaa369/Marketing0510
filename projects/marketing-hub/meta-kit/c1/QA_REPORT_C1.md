# QA report, Meta kit C1 (16 Oct 2026)

Rule followed: no words on any creative image were changed. The 10 supplied ads were only resized. Nothing was redrawn, retyped or cropped.

| Check | Result |
|---|---|
| 20 ad images exist, all 1080x1920 (9x16) or 1080x1350 (4x5) | Pass |
| Supplied ad is intact inside each file (pixel compare against the supplied PNG, mean difference 1.3 to 2.0 out of 255, which is resizing and JPEG only) | Pass, all 20 |
| Native shape (no padding): 01, 02, 03 in 9x16; 04 to 09 in 4x5. Other shape = whole ad on a colour wash from its own edges, no crop | As designed |
| Upload sheet: 10 rows, every image path and page path exists, image number matches the ad | Pass |
| Primary text 509 to 548 characters (limit 548); price, refund, live only and dates present in every ad; no dashes; no arrows | Pass |
| URLs: slug, utm_source=meta and utm_content match the ad number | Pass |
| Call to action "Sign up" on all 10 | Pass |
| Headline length (Meta shows about 40 before cutting) | **C1_08_BPO is 43 characters**; left unchanged. Meta may cut "₹10". |
| Landing pages: 10 files, hero picture loads, pay link goes to the right funnel, no dashes, no arrows, first fold repeats the ad's hook | Pass (08's hook uses "Hello..." with three dots in both places) |
| Layout at 360, 390 and 768 px wide, picture loads, no sideways scroll, no script errors, sticky pay button present | Pass, 30 of 30 |
| Hero picture on each page matches its ad | Pass for all 10 after a fix: page 05 had the other 05 picture; now the same as the ad. The other 05 picture is kept as `img/alt/TL_C1_05_desk_laptop.jpg` |

Not tested here: a real Rs 10 purchase, the GrowthX pixel, or Ads Manager preview (Stories safe zone for 01 to 03 still needs a look).
Script: `../qa_meta.py` (run from this folder).
