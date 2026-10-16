---
name: feedback_closing_fold_is_ungated
description: "every clarity gate points at the ad face; the LP's closing fold above the pay button had none, and shipped 19 riddles through a clean check_all"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cf343ba6-b495-4564-9e6a-d31fe2da3de5
  modified: 2026-09-21T10:01:58.092Z
---

The landing page's **closing fold** - the last call-to-action plus the heading above it -
is the final argument before the money, and until 21 Sep 2026 nothing in the repo looked
at it. `simplicity.py`'s dangling-reference rule and `blind_reader.py` both take the AD's
first fold as their unit.

**Why:** CorporateFinance_Notify_17-19Oct passed all ten gates of `check_all.py` clean
with all 19 pages carrying the same riddle above the pay button - two clauses, an implied
contrast, the referent withheld. One had no verb in its first clause; two opened on "that
conversation" and "the file" with no antecedent on the page. Ramanuj: *"These type of
lines that have been added - none of them make any sense."*

**How to apply:** write the closing line as two plain clauses - name the work the reader
already does, then what this adds ("You already work out whether a company can repay.
This is how you work out what it is worth."). Run `closing_reader.py --prepare/--score`;
`check_all.py` now gates on it as `closing read`, same contract as the ad blind read
(never run is ERROR, a rebuilt page reads STALE, verdict relative to three blinded
controls whose face priced cheap). Standard in SOP/05.

Two things this cost that are worth remembering. **The instrument needs its own controls
checked first**: the first run returned a registration *form* ("Full name Email Mobile
+91") as all three controls, because the control pages end in a hidden modal - it would
have set the floor from a form rather than from copy that worked. Strip sticky bars,
modals and forms before locating the fold, and define the fold by POSITION not class
(269 of 534 pages use `div.close`, 265 do not - the [[feedback_c8_reads_first_css_rule]]
trap). **And it catches my own writing**: two of my replacement lines failed it, one
because "a company valued and a model to open" does not take its object, which is
[[feedback_demand_clause_must_take_the_object]] again.

Related: [[feedback_blind_reader_unit_is_the_first_fold]],
[[feedback_definition_belongs_on_the_page_not_the_face]], [[feedback_run_every_gate]].
