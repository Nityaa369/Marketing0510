---
name: feedback_funnels_json_is_a_window
description: "funnels_*.json is a leads window, not a registry of funnels - absence of a slug is a hint, never proof it was never created"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cf343ba6-b495-4564-9e6a-d31fe2da3de5
  modified: 2026-09-21T09:32:09.854Z
---

`funnels_2026-09-21.json` and its siblings at the repo root are a `get_leads_report`
pull over a **leads window** (that one covers 8-21 Sep), not a list of every funnel
that exists. A funnel with no leads in the window is absent from the file whether or
not it was ever created.

**Why:** on 21 Sep 2026 I wrote `check_funnel_slugs` in `preflight.py` treating
absence as non-existence. It fired on 16 of 51 kits, most of them August and
September camps whose funnels were demonstrably live when they ran. Reading
`_window` showed the mistake. Refitted to speak only about camps that have not run
yet, it fires on 9 of 51 - five future waves, their MediaBuyer and SEND_THIS copies
- and is silent on all 42 past kits.

**How to apply:** read `_window`, `_pulled` and `_source` before drawing any
conclusion from one of these files. Absence within the window is a *hint* worth
flagging, never a finding worth asserting. The browser is the only thing that
settles whether a funnel exists - `curl` gives false 404s on GrowthX, per
[[reference_growthx_funnel_checkout]]. Run a known-live slug as a control before
believing a "not found", the way [[feedback_contradiction_means_failed_test]] asks.
Same family as [[feedback_report_scripts_narrow_silently]]: the file answers a
narrower question than its name suggests, and says so only in a metadata key.

Two regex traps the selftest now pins, both from folder-name camp dates: `_` is a
word character, so `\b` after `Oct` never matched the shipped `_SEND_THIS` folder;
and a January kit read as ten months past instead of two months ahead.
