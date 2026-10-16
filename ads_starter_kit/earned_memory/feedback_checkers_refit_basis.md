---
name: feedback-checkers-refit-basis
description: hook_rules.py and simplicity.py are fitted on Ramanuj's approvals plus live performance as one-class precision tests; where a rule disagrees with an approved or cheap ad, the face wins
metadata:
  type: feedback
---

`hook_rules.py` is fitted against **123 headlines Ramanuj approved or built himself**
(loaded via `adkit.golden`), not the old Section A 13-vs-7 split.

**Why:** the Section A verdicts were an in-house call that did not stick, so the gate
was fitted to bad labels. Measured 31 Aug 2026, it blocked **72.4% of the headlines
Ramanuj actually approved**. Rule E alone fired on 67%, because it required a verb and
the dominant approved headline in this account is a destination noun phrase with no
verb ("A global legal career, from home") — which is exactly what SOP/07 asks for.
After the refit: **4.1%**.

**How to apply:** this is a ONE-CLASS fit. It measures precision (does the rule block
work Ramanuj approved?) and cannot measure recall — every recorded rejection in
CAMPAIGN_MAP.md is a landing page with no hook text. A rule firing on >10% of approved
headlines is noise and must be demoted or deleted, the way E and F were. Do not fit on
cost: only 13 ads carry both a hook and a live cost, and the gate flags 0 of them, so
there is no evidence these rules predict CPL. Keep "is this hook vague" and "what did
it cost" as separate questions until the two corpora overlap on a few hundred ads.

`simplicity.py` was refitted the same day, on the same basis plus live cost. It was
blocking **84% of the HTML faces Ramanuj approved** and blocking `banker` (Rs 60.42,
the cheapest Independent Director ad ever run) via an 11px hairline read as
low-contrast type. Now 0% of approved faces, 0 of 10 priced ads, and still 18 L3
blockers across 400 PNGs so it is not tuned into silence. Its S1 word BLOCK moved
from 100 to 195, because approved faces run 102-191 words; 100 is now a FIX.

**The conflict rule, stated 31 Aug 2026: Ramanuj and past ads win.** A blocker firing
on a face he approved or an ad that ran cheaply is a defect in the RULE.

Always report liveness alongside precision - a gate tuned until it fires on nothing
is not a gate.

Related: [[feedback-only-ramanuj-approval-counts]], [[project-adkit-and-corpus]]
