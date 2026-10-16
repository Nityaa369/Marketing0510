---
name: project-folder-cleanup-sep28
description: 28 Sep 2026 cleanup - ship folders now live as zips; kit working folders are the corpus and must not be bulk-deleted
metadata:
  node_type: memory
  type: project
  originSessionId: 1b7804e8-15ad-49d0-b3a7-3ce658932436
  modified: 2026-09-28T07:19:01.057Z
---

On 28 Sep 2026 the user asked to delete duplicates and keep only final zips. Done via Recycle Bin: 24 `_SEND_THIS/` folders that were byte-identical to their `.zip`, session exports, `__pycache__`, `lp_shots`, `*_SAMPLE` layout samples, and `.blind/F*.png` copies in kits that had already been scored. `ad-analysis-shared/reports/DAILY_*.md` merged into `DAILY_REPORTS_Sep2026.md`.

Four ship folders stay unzipped too (DataProtection_LawSikho_17-19Oct, TechLaw_Carousels_24-26Oct, WomenRemote_Wave4, WomenRemote_Wave9) because they hold the only copy of a priced or approved face.

**Why:** `adkit.corpus` rglobs every `ad_copy*.md` live, and `blind_reader`/`closing_reader` draw their blinded controls from it. Kit folders are the corpus, not clutter. Deleting old `_MediaBuyer_` folders silently weakens `adkit.brief` and the gates.

**How to apply:** before any cleanup, hash-check against corpus priced/approved rows. A future `make_ship.py` recreates `_SEND_THIS/`, so after zipping, the folder can go. Related: [[project-adkit-and-corpus]], [[feedback-blind-reader-is-a-script-with-controls]].

**Second pass, same day (user approved):** unapproved drafts that never ran were deleted: CW W3/RMBC/Neighbours/Collage, both content-writing-bootcamp kits, Section A (ad_copy.md kept), all `new ad types/` batches, womens_ai_bootcamp, WomensAI_Wave1, SeniorConsulting 22-24Aug, DataPrivacy 22-24Aug, four Women Remote 5-7 Sep folders. Their lessons are in RAMANUJ_FEEDBACK.md Part 6. Kept because they ran or he approved: CW 29-31Aug/W2/W4/W5, ConsultingGrowthCamp, HR Wave 9, and every kit he sent to plug in. Folder now ~530 MB. Rule for any future cleanup: a folder stays if a GrowthX funnel, a live cost, a Ramanuj approval or his own "plug in" message ties to it.

