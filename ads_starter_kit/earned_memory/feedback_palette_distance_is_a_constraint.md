---
name: feedback_palette_distance_is_a_constraint
description: "one palette per ad means perceptually distinct, not just a different hex; and dE is a constraint to satisfy, never a quantity to maximise"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cf343ba6-b495-4564-9e6a-d31fe2da3de5
  modified: 2026-09-21T10:53:38.252Z
---

Rule 4's "every ad gets its own colour palette" was being satisfied as *no two
accents share a hex*. `adkit.palettes` even refuses two faces on the same palette,
so it looked enforced. It was not: the CF notify wave shipped 19 distinct hexes
with three pairs under **CIELAB dE 12**, roughly where two colours stop being told
apart at a glance in a feed - rust/brick 9.0, pine/forest 9.8, slate/ink 10.0.

**Measure it as dE, not as string equality.** Sample the CTA band of each rendered
face and compute pairwise CIELAB distance; under ~12 is a repeat.

**The register can run out.** An exhaustive swap search over every assignment of
19 of the then-21 palettes topped out at min dE 9.8. The pool was crowded in the
red-brown, green and slate families, so it needed *widening*, not reshuffling.
Added fern (hue 95), iris (272) and brass (50) into the register's own hue gaps.

**Why the two attempts:** maximising dE is the wrong objective. It drove every
pick to the saturation ceiling and produced `#068006`, `#068031` and `#991299` -
electric greens and vivid magenta that cleared the floor and looked like a
different brand beside `#96331F` rust. The fix was to treat **dE >= 12 as a
constraint** and then pick the colour closest to the register's own centre of
gravity (sat 0.71, val 0.47, measured over the existing 21). The three that
shipped sit at sat 0.70, val 0.46-0.48 and look like they belong.

**When a pair is too close, the face with measured history keeps its colour** and
the new or unproven ICP moves. rust stayed on loan_consultant (Rs164, proven
cheap); brick moved off career_break (a new ICP).

Cost note: a recolour re-renders, so `blind_reader` goes stale - but rendering is
deterministic, so only the faces that actually changed bytes need a fresh reader
(3, not 22). `closing_reader` hashes fold TEXT, so a palette change leaves it
valid. Related: [[feedback_closing_fold_is_ungated]],
[[project_corporate_finance_live_cost]].
