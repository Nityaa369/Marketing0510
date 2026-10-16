---
name: feedback-definition-belongs-on-the-page-not-the-face
description: The one-sentence field definition lives in the LP first fold; on the face it reads as clutter when the head already names the job
metadata:
  type: feedback
---

Rule 2 step 4 requires a one-sentence field definition. It belongs in the **landing page
first fold**, where lint L4 checks it. On the **face** it is a third block of body copy
under a head that already names the job, and it reads as padding: *"the us corporate law
support line can be removed from all ads since it is just adding text but not a value and
the ad is looking too hotch potch"* (4 Sep 2026, US Corporate Law Wave 2).

**Why:** none of the four approved USCL faces carries a definition sentence. When the head
is concrete - verb plus a nameable object - it already answers the blind reader's "what job
would I be doing", so the definition adds length without adding an answer. The definition is
load-bearing only when the head is abstract, and an abstract head is the actual defect.

**How to apply:** pass `extra=dict(face_definition="")` in the kit spec. `field_definition`
stays set, so `value_props.md`, the page and lint L4 are unaffected; the serif shell drops
the empty div rather than rendering its margins. Then confirm the head alone still answers
question 2 of [[feedback-blind-reader-value-prop]] - if it does not, fix the head, do not
put the definition back.
