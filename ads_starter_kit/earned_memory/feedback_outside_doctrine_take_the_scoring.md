---
name: feedback_outside_doctrine_take_the_scoring
description: "Outside marketing doctrine (RMBC, offer-to-campaign) is a draft — take its scoring and diagnosis, never its output shape"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b145a477-8850-4707-aac4-535843c82971
  modified: 2026-09-04T10:14:27.396Z
---

When an outside marketing framework is circulated for adoption, take the part that
**ranks or diagnoses** and reject the part that **shapes the deliverable**.

Evaluated 4 Sep 2026: the `offer-to-campaign` algo Uday Wagh circulated on 21 Aug 2026.
Judged not adoptable as a process, and one piece of it adopted — the scored ICP rubric,
now `pain_score` in `preflight.py` and `pain=` in `adkit/spec.py`.

**Why:** the back-and-forth on this account is not caused by missing strategy. It is
caused by rejections on Rule 1 (threat framing), Rule 2 (cryptic), ICPs nobody
self-identifies as, and identical LPs. US direct-response doctrine pushes *toward* the
first two: it asks for "cost of inaction" framing, and its `pain → hidden diagnosis →
mechanism` sequence is a curiosity gap by construction. It also delivers seven artefacts
at once (5 short ads, 3 long, 10 hooks, hero, retargeting, funnel, test plan), which is
the opposite of cheapest-rejection-first and gives seven surfaces to reject in one pass.

This is not a prediction — `ContentWriting_RMBC_29-31Aug/` ran the experiment and
`VERDICT_v1.md` returned REJECT-rethink on all five, with the same three conflicts
resolved against the outside doctrine (mandatory numbers, fear hooks, invented urgency).

**How to apply:** when one of these arrives, ask which of the two halves it is. Scoring,
ranking, awareness mapping and mechanism tests are portable and worth taking. Hook shape,
CTA patterns, urgency, qualification blocks and deliverable lists are not — they are
fitted to a different market and this account's rejection record is mostly them. Adopt the
portable half into the existing tooling rather than adding a parallel process, and say in
the docstring which dimensions were dropped and why. See [[feedback_checkers_refit_basis]]
and [[feedback_icp_is_the_biggest_lever]].
