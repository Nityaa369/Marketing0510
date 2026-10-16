---
name: feedback_measure_every_colour_pair
description: reading one contrast pair proves nothing about the other - the pay button on 20 pages was 1.46:1 while I reported 7.1:1
metadata:
  type: feedback
---

I measured contrast on the wave 6 pages, reported *"the accent clause 7.1:1, past WCAG
AA"*, and called contrast a non-issue. That reading was of accent **text on the light page
ground**. The **pay button** was the inverse pair, `color:var(--ink)` on
`background:var(--acc)`, and measured **1.46:1 to 2.68:1** across all twenty palettes -
in-page and in the fixed bottom bar. The closing fold was white on a radial gradient whose
centre stop is the near-white page tint: **1.07:1**.

**Why:** a palette is not light or dark, it is a set of colours, and every PAIR has its own
ratio. Checking one and generalising is how the primary call to action on a twenty-page
wave shipped nearly unreadable. Twice in one day a light gradient stop collided with the
text on top of it.

**How to apply:** `L8` in `adkit/lp_spine.py` resolves the page's own `:root` custom
properties and checks every rule that declares both a background and a colour. A gradient
is checked against **every stop**, which is what catches the fold - it passed on its dark
end and failed on its light one. Blocks under 4.5:1, warns under 7, and fires 0 blockers on
the corpus that converted. Prefer a **solid** ground for any block carrying text: white on
accent is 6.26:1 worst case, white on ink 16.45:1. See [[feedback_lp_readability_is_not_contrast]].
