---
name: feedback-demand-clause-must-take-the-object
description: A demand clause folded into a head must be grammatical with the object it attaches to - "the contracts US firms cannot staff" is not English
metadata:
  type: feedback
---

When demand is folded into the head (see [[feedback-headline-names-job-not-buying]]), the
demand clause has to take the object it is attached to. On US Corporate Law Wave 2 all ten
heads ran "<verb> the <document> US firms cannot staff". You staff a role or a team. You do
not staff a contract, a set of papers or an agreement. Reported as: *"and draft the
contracts US firms cannot staff? what does this sentence even mean?"* It does not mean
anything.

**Why:** every gate passed. `hook_rules`, `simplicity`, `ad_lint` and `creative_judge` all
read the head as clean, because none of them checks whether the verb can take the noun.
This is a class of defect no checker in the repo can see, and it survived ten faces.

The first repair moved the defect one word over instead of fixing it. "Register the
companies US firms **outsource**" drew *"how do you outsource a firm??"* - outsource takes
WORK as its object, never an entity and only loosely a document.

**How to apply:** `send` takes documents ("the contracts US firms send to India"); a
possessive tie to the reader's own world takes entities ("the US companies your visa
clients need"). This is now enforced by **`hook_rules.py` rule J** - blocking, 0 of 123
approved headlines, caught 8 of 8 defective heads - which knows four object classes
(entity, artefact, work, role) and what each demand verb can take. Extend its tables rather
than working around it. Note the noun-phrase HEAD is its last word: "company papers" is
papers, and you can send papers. Related: [[feedback-blind-reader-needs-the-whole-face]].
