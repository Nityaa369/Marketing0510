---
name: feedback_blind_reader_unit_is_the_first_fold
description: Run the blind-reader check on the whole first fold including the definition sentence - on call-out plus head alone the four cheapest patent ads score 0 CLEAR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 096e1a6f-e024-4ecb-a1df-f569d2b43add
  modified: 2026-09-03T08:02:55.816Z
---

The blind-reader unit is the **first fold**: call-out, head AND the plain-words
definition sentence. Not the head alone, and not call-out plus head. Measured 3 Sep
2026 by running the identical test on the four Patent ads that carry a live cost:

| face | live | verdict on call-out + head only |
|---|---|---|
| `icp_28_biomedical_devices` | **Rs 91.36** | SLIGHTLY VAGUE |
| `icp_27_semicon_vlsi` | Rs 120.68 | VAGUE |
| `icp_26_ayurveda_bams` | Rs 121.53 | VAGUE |
| `icp_18_agri_foodsci` | Rs 131.49 | VAGUE |

**0 of 4 CLEAR on the cheapest ads in the product line**, and the reader called them
"a fill-in-the-blank, the same line swapped for whatever course I did". A test that
fails every ad that actually ran cheaply does not discriminate, and optimising
against it is wasted money. I spent four rebuild passes on it before checking.

**Why:** the definition sentence sits directly under the head and answers the exact
question the reader keeps asking ("what would I be doing?"). Removing it from the
test makes the head look like it failed when the fold did not. On the complete face
the same wave came back with all five questions answerable and no fold reading as a
step down.

**How to apply:** hand over the whole first fold, per CLAUDE.md. If a sub-unit test
produces a bad verdict, **run the same test on the priced winners before acting on
it** - that is the cheap control and it takes one subagent. The general rule the
repo already states: a check that fires on work that ran cheaply is noise, and the
face wins. Related: [[feedback_blind_reader_needs_the_whole_face]],
[[feedback_checkers_refit_basis]], [[feedback_only_ramanuj_approval_counts]].
