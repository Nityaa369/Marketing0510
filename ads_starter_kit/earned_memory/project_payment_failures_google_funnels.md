---
name: project-payment-failures-google-funnels
description: "Google-sourced funnels fail payments far more than Meta ones; Senior AI and US Corporate Law duplicate slugs are the outliers at 30-40%, measured 23 Sep 2026"
metadata:
  node_type: memory
  type: project
  originSessionId: ede3d7bb-967e-4a12-b319-fa4569f4dabe
  modified: 2026-09-23T17:53:56.933Z
---

Measured 23 Sep 2026 from the GrowthX `get_leads_report` MCP, which carries a per-lead
`byStatus` with **Failed** as a state distinct from Expired (never attempted) and Paid. The
honest denominator for a failure rate is **Paid + Failed**, everyone who reached payment.
Expired belongs to a traffic or intent question, not a payment one.

**Baseline, all funnels, 9 to 22 Sep 2026:** Meta 2.5% failed (246 of 10,039 attempts),
Google 11.6% (393 of 3,382), other 3.3%. Meta sits at 1.1 to 2.8% in every camp, so it is
the control.

**Google carries a real but modest penalty everywhere** (AI for Women 3.5%, academic writing
3.8%, Legal AI 6.1%, Contract Drafting 6.5%, Patent 7.3%, Independent Director 8.5%,
IP Law 10.4%). **Two camps are far outside it: Senior AI 27.8% and US Corporate Law 20.5%.**

**Inside those two the failures sit on DUPLICATED funnel slugs** (suffix -2, -3, r2), against
their own original Google funnels in the same camp and week:

| camp | duplicate slug | original slug |
|---|---|---|
| Senior AI | 39.6% on 333 attempts | 6.9% on 189 |
| US Corporate Law | 30.8% on 234 | 10.5% on 239 |
| Patent Law | 5.9% on 304 | 8.8% on 295 |
| academic writing | 2.4% on 41 | 3.9% on 855 |

So "duplicated funnels are broken" is NOT a general rule - Patent and Academic Writing
duplicates are fine. It is these two batches: `senior-ai-*-2/-3`,
`senior-consulting-sc-01-rented-executives-2`, and the `sep19-uscl-*-2` set.

**Not new.** The August Senior AI camp, on entirely different funnel pages, shows the same
split: Google about 22% (321 failed against 1,106 paid), Meta about 2.5%.

**What is NOT established:** the gateway's reason. The platform reports the status; it does
not expose the decline code. Two explanations still fit - a checkout misconfiguration on
those pages, or lower-quality Google traffic (those pages also expire at 66% against 22% on
Meta). Only the Razorpay or GrowthX error codes for those slugs settle it.

**How to re-run:** `get_leads_report` with no group filter for a fortnight saves to a
tool-results file; tally Paid and Failed per funnel, split by whether the funnel name starts
with google/meta and whether the slug ends in -2/-3/r2. Scripts in the 23 Sep session.
See [[feedback-load-rate-is-not-traffic]] and [[feedback-contradiction-means-failed-test]].
