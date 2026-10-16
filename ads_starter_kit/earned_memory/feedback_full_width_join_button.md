---
name: feedback-full-width-join-button
description: The join button on every ad face fills the full line; the notice layout's small footer button was rejected - use extra big_cta=True
metadata:
  type: feedback
---

29 Sep 2026, on US Accounting wave 2: "the join now button is small in half of them, expand it to fill
the full line". The six notice faces carried the default notice footer (small button between
"Free · Live online" and "No CA or CPA needed"); the search faces already had a full-width button.

**Why:** the button is the one action on the face; a small pill between two text blocks reads as
fine print next to a full-width button on the sibling faces.

**How to apply:** on the `notice` layout always pass `extra=dict(..., big_cta=True)` (adkit/layouts.py,
added 22 Sep for "make the join button bigger"); on any layout, check the button spans the text
column before handover. Re-rendering a face makes the blind read stale - re-read only the changed
faces and reuse the rest by ad name. Related: [[feedback-notify-layout]], [[feedback-broadsheet-layout]].
