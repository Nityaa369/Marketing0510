---
name: feedback_a_title_is_not_a_job
description: "A head that names the destination as a job title reads as cryptic unless a verb in the head names work the READER does; the buyer's verb does not count"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dc1f1eba-6002-4592-b9b5-7fca7c2942e6
  modified: 2026-09-23T09:02:05.803Z
---

Measured 23 Sep 2026 on `SeniorAI_Reach_31Oct-2Nov`: 11 first folds blind-read, one fresh
reader each, 8 new faces plus 3 blinded controls with live cost. Three came back UNCLEAR
and all three are the same shape — **the head names the destination as a job title and
never names the work**:

- "Become the ERP consultant mid-sized firms hire direct."
- "Become the operations advisor a plant brings in from outside."
- "Edtech companies will pay for your name and your subject." (control, Rs 273/buyer)

Every reader gave the same reason unprompted: *"never says what the actual work is."*

The eight that passed all attach a **reader-verb**: "brings a company's cloud bill down",
"advise them", "start a security practice for companies with no security team", "run other
companies' programmes", "that startups book before they launch".

**Why:** a verb in the head is not enough — "the operations advisor a plant brings in from
outside" has a verb, but its subject is the *plant*. The reader still cannot say what they
would do all day. No regex separates "the consultant who brings a company's cloud bill
down" from "the operations advisor a plant brings in", so this is a human read every time.
Logged as checklist item 11 in `hook_rules.py`, marked NOT mechanical.

**How to apply:** if the head names a title, check whose verb is attached to it. If the
verb belongs to the buyer, rewrite so the reader is doing something. And naming the work is
necessary but **not sufficient** — the first rewrite, "Run SAP and Oracle rollouts for your
own clients", also failed blind, because a bare work verb with no destination noun reads as
the same job done elsewhere, which is [[feedback_offer_line_names_the_prize]] and Rule 1's
rejected shape in disguise. The verified fix carries both: *"Turn your SAP and Oracle
rollouts into your own consulting business."*

Also learned in the same run: because the delivery sentence is a per-kit constant
([[feedback_copy_is_filled_in_not_written]]), every reader's answer to "what will I have on
the last day" was identical across all eight faces. All the differentiation sits in the ICP
band and the head, so a head that does no work collapses that face into a generic camp ad.

Related: [[feedback_headline_names_job_not_buying]],
[[feedback_definition_belongs_on_the_page_not_the_face]],
[[feedback_blind_reader_is_a_script_with_controls]], [[project_seniorai_history]].
