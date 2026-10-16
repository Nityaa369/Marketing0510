---
name: feedback-closing-fold-names-person
description: "A closing fold that describes the reader's work but never puts a noun on the reader fails closing_reader question 1; name the person in the first three words"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-10-01T07:16:50.614Z
  originSessionId: f1085e60-b1db-41dd-952a-195f5347d203
---

Measured 1 Oct 2026 on `TechLaw_Meme_24-26Oct`. Four of ten closing folds scored 2/3, and
**all four failed question 1 (*who is this addressed to*), never question 3**. Each described
the work and never named the person:

- "You already draft and appear on your senior's matters." -> CANNOT ANSWER
- "You have the law degree and no first matter yet." -> CANNOT ANSWER
- "You are a junior lawyer, and every matter you touch is your senior's." -> clear

**Why:** SOP/05's standard was *name the work the reader already does, then what this adds*.
That is necessary and not sufficient. "You already draft..." describes an activity that several
different people do, so a reader with no context cannot say who is being spoken to.

**How to apply:** put the reader into the first three words of `close_h2` ("You are a junior
lawyer...", "You are a lawyer in a smaller town..."). It is the same defect C23 catches on an
ad face, one slot later.

**The gate samples this noisily.** The identical opening clause passed on one page and failed
on another in the same run, and the control floor moved from 3/3 to 2/3 between runs, which
changes the verdict on a borderline fold. So a PASS does not prove the fold names anybody -
fix the pattern across every page, not only the ones the run happened to catch. Written into
SOP/05. Related: [[feedback-closing-fold-is-ungated]], [[feedback-lp-must-name-the-reader]],
[[feedback-blind-reader-is-a-script-with-controls]].
