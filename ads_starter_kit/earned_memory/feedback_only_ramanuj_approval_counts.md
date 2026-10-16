---
name: feedback-only-ramanuj-approval-counts
description: Only Ramanuj's approval makes an ad final; an in-house APPROVED label is not evidence and must never be used as a precedent
metadata:
  type: feedback
---

An ad approved in-house is not approved. Only what Ramanuj approved became a final,
running ad.

**Why:** stated 31 Aug 2026 — *"ignore the ones that i approved, they were finally not
approved. only the ones ramanuj approved became the final ads."* The 17
`ContentWriting_SectionA` pairs are recorded in `CAMPAIGN_MAP.md` as a bare
"APPROVED: pairs 01, 02, ..." with no attribution. They were an in-house call and did
not ship.

**How to apply:** when reading any APPROVED marker, check who made the call.
`CAMPAIGN_MAP.md` attributes `APPROVED/` explicitly ("Ramanuj-approved batches ...
Everything under APPROVED/ has passed Ramanuj") — that one counts. A bare "APPROVED"
line with no name does not. `GOLDEN` is built on this rule: `adkit/golden.py` SOURCES
carries only Ramanuj-approved and Ramanuj-authored faces, and excludes the Section A
zip by name with the reason attached. Never cite your own earlier approval as a
precedent for a new face.

Related: [[project-adkit-and-corpus]], [[feedback-blind-reader-value-prop]]
