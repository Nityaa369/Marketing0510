---
name: feedback-worklist-layout
description: The worklist layout, built from a reference image; take the skeleton, never the rate card
metadata:
  type: feedback
---

`worklist` (adkit/layouts_custom.py, 15 Sep 2026) is the first layout built through
`python -m adkit.layouts --new`, from `reference_images/IMG-20260806-WA0057.jpg` — the
LawSikho practising-lawyers face. Accent band carrying the ICP, serif head with one coloured
clause, a kicker, then **rows of named work on thick left accent bars**, each a small-caps
label over an ordinary-words line. Brand sits bottom-right, not top-left.

**Take the skeleton, not the rate card.** Every row in the reference ends in a price
("$300-400 per filing"). That is the pay-chart shape — index 2.34 vs par across four product
lines — and the standing compliance list keeps such figures on the LP, never the face. The
row's emphasis slot carries a concrete detail of the work instead. Same ruling as
[[feedback-outside-doctrine-take-the-scoring]].

**How to apply:** supply `extra["rows"]` as `"LABEL | what it is"` strings. Without them it
falls back to `kit.takeaways` and renders as a plain bullet list, which loses the whole point
of the layout — the labels are what make it different from `ladder`.

**Two things the build taught, both already paid for:**
- `simplicity.py` R1 blocked the first render: I muted `.def` and the footer with
  `opacity`, and faded text is banned ([[feedback-ad-clarity-rules]]). Hierarchy comes from
  size and weight. Never reach for opacity in a layout.
- A module-level `__getattr__` does not resolve bare globals inside that module's own
  functions (PEP 562 covers attribute access only), so lazily imported chassis constants like
  `SERIF` must be fetched by a call, not a name.
