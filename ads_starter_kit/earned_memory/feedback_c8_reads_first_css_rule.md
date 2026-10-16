---
name: feedback-c8-reads-first-css-rule
description: ad_lint C8 matches the FIRST .callout font-size in source, so a later CSS override is invisible to it and ships under the size floor
metadata:
  type: feedback
---

`ad_lint` C8 uses `re.search` for the first `.callout{...font-size:Npx}` in the HTML
source. A later rule wins in the browser and C8 never sees it.

**Why:** measured 31 Aug 2026, 7 of 10 shipped `IndependentDirector_Wave1` faces render
`.callout` at 58px and `.head` at 52px, both under C8's 64px hard floor, because the
generator appended a hand-written `tight=True` override block. C8 reported all ten clean.
This is the same class of silent pass as the 25 Aug inline-styles failure.

**How to apply:** never write a per-ad CSS override to make copy fit. Use
`adkit.chassis`, which clamps identity type at 64px and scales only body elements, and
trust `check_all.py`'s `fit (rendered)` gate, which reads the *computed* value. If a face
does not fit, cut words. The ten ID faces are shipped and were not regenerated.

Related: [[feedback-run-every-gate]], [[project-adkit-and-corpus]]
