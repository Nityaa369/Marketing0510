---
name: feedback_allcaps_is_not_a_pronoun
description: "hook_rules' dangling-pronoun rule matched case-insensitively, so the field name 'IT' read as the pronoun 'it' and blocked a measured winner"
metadata:
  node_type: memory
  type: feedback
---

Found 1 Oct 2026 on Senior AI wave 10. `hook_rules.r_a_dangling_pronoun` ran `PRONOUNS` with
`re.I`, so **"IT" (information technology) matched the pronoun "it"** and the rule reported
"\"IT\" has no noun before it in the hook".

It was blocking `SC_Oct3|w9_06_it_managers`, "Launch your own IT consulting business" -
**Rs 92 per buyer on 235 buyers, 0.66x its campaign par**, one of the ten cheapest faces in
the product. A measured winner, blocked by a false alarm.

**Fix:** skip the match when the matched token is ALL CAPS and the hook is not entirely caps.
English does not capitalise pronouns mid-sentence, so the only way that fires is a field name
(IT, HR, QA). Selftest re-run before and after: **3 of 7 rejects caught, 1 of 13 false alarms,
identical both ways** - the narrowing did not move the fit.

**Why:** a lexicon fitted on prose will misread an initialism, and the cost lands on exactly
the faces that earned their place. See [[feedback_checkers_refit_basis]] for the rule that any
change to a checker re-runs its selftest and reports the before/after fit.
