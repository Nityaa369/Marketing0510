---
name: feedback-notes-layout
description: "The Notes-app layout (adkit `notes`), built 30 Sep 2026 from a DTC niacinamide reference: reader's question small, offer large with the key phrase as selected text, drawn eyes peeking; Ruchika approved it for NCA wave 2"
metadata:
  type: feedback
---

Built 30 Sep 2026 in `adkit/layouts_custom.py` (`notes`) from a skincare Notes-app static Ruchika supplied ("do one notice format and one Notes app style ad"). She saw the sample pair and asked for the whole wave.

**The face:** amber "‹ Notes" bar and •••, the reader's question as the smaller line (`.callout`, still >= 64px), the offer as the large line (`.head`), the head's `<em>` part rendered as SELECTED TEXT with blue drag handles, two drawn eyes peeking over the card, delivery line + one full-width button + terms below. The LP hero mirrors it as a small Notes card (`device()` in the kit's build_lps.py).

**Why the eyes are drawn:** the eyes emoji renders as purple Fluent eyes in headless Chrome on Windows, not the Apple eyes in the reference, and the PNG is what Meta shows.

**How to apply:** put the `<em>` so the selection starts at a line start or mid-line, never with a lone handle dangling at a line end (62's "Use your LLB to |" had to move "to" inside the em). Never priced yet: first run is NCA wave 2 (nca61-nca70), paired against notice faces on the same readers. Related: [[feedback-vary-the-design-style]], [[project-nca-history]].

**Descender clipping (30 Sep 2026, Ruchika: "The q is getting cut" on ad 62).** At head line-height 1.14 the next line's full-height selection background painted over the descenders of the line above. Fix in adkit/layouts_custom.py `_notes`: line-height 1.3 and the `.sel` highlight as a gradient band (transparent 0-14%, colour 14-96%). The fit gate passed the broken faces: it checks box overlap, not a background painting over glyph ink. Look at any highlighted multi-line head at full size before shipping.
