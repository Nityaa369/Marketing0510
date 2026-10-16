---
name: feedback_clip_can_come_from_an_ancestor
description: "fit F1 compares every leaf with the canvas, so an element clipped by a nearer overflow:hidden ancestor passes clean - added F8"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cf343ba6-b495-4564-9e6a-d31fe2da3de5
  modified: 2026-09-21T11:07:35.052Z
---

`adkit/fit.py` F1 asks "does this leaf extend past the **canvas**?". A card chassis
usually has an inner container with `overflow:hidden`, and an element cut off by
*that* sits comfortably inside the canvas and reports clean.

**Why:** 21 Sep 2026, the CF notify wave. `.note` is `overflow:hidden` inside a
fixed canvas, so on 3 of 19 faces a taller content block pushed the CTA band down
and the card ate its lower padding: the band rendered **78px instead of 108px**
and "Join for Rs10" sat almost on the bottom edge. `fit.check` returned clean at
scale 1.00, so the auto-fitter had no reason to shrink anything, and the kit
passed all eleven gates. Ramanuj caught it by eye, twice.

**How to apply:** F8 now walks up to the nearest ancestor whose overflow is not
visible and compares against its padding box (border sits outside it). With F8
live the auto-fitter shrank those three to 0.96/0.92/0.92 and every label is now
centred within 3px. Same family as the F7 note already in that file - F1 is a
canvas-only ruler, and every new clipping surface needs its own check.

**Two process lessons, both expensive:**

- **Measure before believing, then sanity-check the ruler.** My first pass
  detected the band as "rows that are mostly accent", which splits the band in two
  at the text; it reported `below = 1px` on all 19 faces. A number identical
  across every face is a broken ruler, not a finding. The band is identified by
  its LEFT AND RIGHT MARGINS, where the label never reaches.
- **A neighbouring fix is not the fix.** Earlier the same day "alignment for the
  button text is off" was read as the delivery line ABOVE the button (`.meta` was
  `display:flex`, splitting one sentence into two flex items). That was a real
  defect and fixing it was right, but it was not what was being pointed at. When
  a complaint repeats with "still", re-measure the exact element named rather
  than assuming the previous fix missed.

Related: [[feedback_no_gate_saw_vertical_gaps]], [[feedback_c8_reads_first_css_rule]],
[[feedback_run_every_gate]].
