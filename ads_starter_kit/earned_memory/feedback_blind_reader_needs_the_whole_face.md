---
name: feedback_blind_reader_needs_the_whole_face
description: "Give the blind reader the complete rendered face, never a three-line fold - a truncated fold makes question 3 unanswerable by construction"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 096e1a6f-e024-4ecb-a1df-f569d2b43add
  modified: 2026-09-03T07:01:42.210Z
---

When running the blind-reader check, extract **every text node in the rendered face**,
not just the call-out, head and definition. On Global Patent wave 2 (3 Sep 2026) I handed
two isolated readers a three-line fold. Both returned CANNOT TELL on *"what will I be able
to do on the last day"* for 9 of 10 faces, which looked like a damning copy defect. It was
my extraction: the delivery sentence and the terms strip sit lower on the face and I had
cut them off. Re-run on complete faces, all five questions were answerable and nothing
read as a step down.

**Why:** a truncated fold makes question 3 unanswerable by construction, so the test
returns a false positive that costs a rebuild cycle. A wrong verdict also discredits the
one check that actually catches cryptic.

**How to apply:** dump the face with a regex over the `<body>` of the generated HTML, one
line per text node, and hand that to the subagent. Split the faces across two agents so
one reader does not anchor the other. Their non-Q3 findings stayed valid even on the
truncated fold and were worth acting on: one face named no buyer and no money at all,
and another ranked the reader's current job below the new one, which is a Rule 1 defect
no gate catches. Related: [[feedback_blind_reader_value_prop]],
[[feedback_same_copy_different_face_10x]].
