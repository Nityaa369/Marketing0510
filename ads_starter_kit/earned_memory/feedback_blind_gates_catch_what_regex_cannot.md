---
name: feedback_blind_gates_catch_what_regex_cannot
description: "Three defects on Senior AI wave 10 that passed every mechanical gate clean and were caught only by blind_reader / closing_reader"
metadata:
  node_type: memory
  type: feedback

Senior AI wave 10, 2 Oct 2026. Three real defects shipped past `preflight`, `simplicity`,
`hook_rules`, `creative_judge`, C8, fit, gaps and L5/L7/L8 **all clean**, and were caught
only by the two reader gates.

1. **A schedule a reader could not resolve.** The camp runs 2 to 5 PM on Sat and Sun and
   7 to 10 PM on Mon. The terms bar said `2 TO 5 PM IST . MONDAY 7 TO 10 PM` and never
   named the first two days, so **13 of 20 blind readers reported two conflicting
   schedules**. Fix: name both, `LIVE . SAT & SUN 2 TO 5 PM IST . MON 7 TO 10 PM`.
2. **A closing heading with no verb in it.** "Hospital administrators: your own hospital
   consulting business, started on the side" is a noun fragment, and a reader asked to
   restate it answered CANNOT ANSWER. Nine other readers passed the identical structure,
   so one 2/3 against a 3/3 control floor was the only signal. Fix: two plain clauses,
   reader named first, per [[feedback_closing_fold_names_the_reader_first]].
3. **`.capitalize()` destroying an initialism.** The fix for (2) built the heading with
   `role.capitalize()`, which lower-cases the rest: "IT manager" shipped as **"It
   managers"** and "ERP consultant" as **"Erp consultants"** on four pages. A reader
   called it a probable typo and scored the fold 0/3 on who it addresses. Use
   `role[0].upper() + role[1:]`. See [[feedback_allcaps_is_not_a_pronoun]] for the same
   class of bug in hook_rules.

**Why:** a regex cannot tell that a heading has no verb, that two times are ambiguous
about which day they belong to, or that "It managers" is wrong rather than merely
unusual. Every one of these is well-formed text. The relative, blinded, controlled read
is the only gate in the repo that sees them.

**How to apply:** when a face or a closing fold changes at all, re-run the reader gate -
`check_all` reports ERROR for a stale one and that is doing its job, not being pedantic.
Budget for it: each full re-run is 23 blind plus 23 closing subagents.
