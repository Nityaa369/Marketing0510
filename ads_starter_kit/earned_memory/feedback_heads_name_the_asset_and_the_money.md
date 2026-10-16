---
name: feedback-heads-name-the-asset-and-the-money
description: "22 Sep Academic Writing review - heads rewritten as \"your <asset> can earn you dollars\"; no \"No PhD needed\" to academics; \"language\" not \"English\" skills"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ede3d7bb-967e-4a12-b319-fa4569f4dabe
  modified: 2026-09-22T12:03:32.240Z
---

On the Academic Writing 24-26 Oct wave the reviewer rewrote 13 of the 30 heads in one pass, all to the same shape:
the reader's own asset plus the money, stated plainly. Examples: "Your PhD can still earn you money.",
"Your thesis skills can earn you dollars.", "Your subject expertise can pay you in dollars.",
"Your MSc can earn you more than lab work.", "Secure your next income before the grant ends."

- A clipped or implied head gets rejected: "Research writing pays while you wait" drew "wait for what? specify".
- Say "language skills", not "English skills", which "sounds weird".
- Never put "No PhD needed" on a face or page for assistant professors, lecturers or faculty, because they hold a PhD or are working towards one. build.py/build_lps.py now drop it for PHD|PROFESSOR|LECTURER|FACULTY callouts.
- The translate layout's .head had `text-wrap: balance`, which split 7-word heads into 3 short lines ("why is the heading entirely left aligned?"). It now uses `pretty`.

**Why:** a half-asleep reader has to see what they already own and that it pays. See [[feedback-half-asleep-callouts]].
**How to apply:** keep the reviewer's wording even when hook_rules H warns "money without work". The card below names the work. H is only a finding, not a block.
