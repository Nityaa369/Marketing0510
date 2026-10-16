---
name: feedback_darkobject_layout
description: "The dark spotlit face (adkit layout `darkobject`) - second cheapest design on Senior Consulting at Rs 108 / 0.78x par, built 1 Oct 2026 from the live dos_* faces"
metadata:
  node_type: memory
  type: feedback
---

Built 1 Oct 2026 for Senior AI wave 10, from the twenty-four live `SC_Oct3|dos_*` faces of
Senior Consulting 3-5 Oct: **Rs 108 against a Rs 139 campaign par (0.78x) on 904 buyers**,
while the same campaign's verb-headline faces ran 1.53x on 1,547. Second only to
[[feedback_launchlist_is_the_measured_design]] (0.68x), and the only measured winner on this
product that is not a list, so a wave can carry both without the faces reading the same.

The shape, read off `dos_erp_chair`: near-black ground (#07070A) with one warm radial pool of
light low in the frame, a small centred brand lockup (sans over serif), the ICP in large
letter-spaced cream caps on nothing, a serif destination headline with the second clause in
the accent, two quiet lines, the object, then two pill rows at the foot (price, then dates).

**Two things the implementation had to solve, both reusable:**
1. Every palette in the register is built for a light page, so its accent vanishes on black.
   `_lift()` raises LIGHTNESS in HLS and holds saturation; blending towards white instead
   desaturates and ten dark faces become ten greys (#A8231C went to #BE5D58, not carmine).
2. `simplicity.py` R1 blocks text set at reduced opacity. On a dark ground the softening has
   to be solid hex, not `opacity`, or the whole kit blocks.

**It takes a photographed object in `extra["object"]`; without one the lit panel carries the
named work instead**, which is what shipped on 1 Oct because the image generator was out of
credits. `adkit.gaps` would otherwise block the empty lower half.
