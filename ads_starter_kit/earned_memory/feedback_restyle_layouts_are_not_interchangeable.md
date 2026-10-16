---
name: feedback-restyle-layouts-are-not-interchangeable
description: "Re-skinning a face keeps the selling copy but never the chrome; layouts consume different field sets, which is why \"same text, new look\" failed when asked in chat"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8aa53e3e-85fb-4783-9c48-c46acdf94f1d
  modified: 2026-09-15T07:07:28.599Z
---

`python -m adkit.restyle <kit> --list` maps "make it look like this one" to a layout name
(all 11 layouts carry the real face they came from and its live cost, in
`adkit/layouts.PROVENANCE`). `--ad <name> --to <layout>` re-skins one face via
`<kit>/.restyle.json`; **spec.py is never edited**, which is the point — a model sent in to
change one keyword also tidies a headline on the way past.

**Layouts are not interchangeable skins over a fixed content model.** Measured 15 Sep 2026,
one ad through `notice` then `serif`: only 5 of 9 strings survived. `callout`, `head` and
`def` were identical and `deliver` was renamed to `quote` — but `notice` has a section label
(`nlabel`) and a terms bar, while `serif` has a barrier line, a `fline` and a trust row. Each
layout consumes a different chrome field set.

**Why:** this is why "I share a sample I like and the ads are regenerated without changing
text" did not work when asked in chat. It was not a prompting failure — the underlying system
could not express the operation, and a naive restyle silently dropped fields.

**How to apply:** the guarantee is over *selling copy* (ICP line, hook, definition, delivery
sentence — `COPY_CLASSES`), never over every string. Demanding byte-equality across all nodes
makes every restyle illegal, which is what the first version did. A lost copy line reverts and
reports; chrome differences are printed, never blocked. Re-run `check_all.py` after a restyle:
a new skeleton changes the box model, so [[feedback-no-gate-saw-vertical-gaps]] and the fit
gate both apply again. Blind-read staleness is hashed, not mtimed, so an applied-then-reverted
restyle does not falsely invalidate a good read.

Related: [[feedback-vary-the-design-style]], [[feedback-same-copy-different-face-10x]] — the
face alone moved CPL 10x, so restyling is not cosmetic.

**Generation IS a bottleneck, and this was pushed back on directly (15 Sep 2026):** "i had
once given a few samples and you could not generate ads using that." Correct. Every visual
the account can make comes from ~11 hand-written layouts; the step from a reference image to
a usable one was an undocumented 80-line coding task. `python -m adkit.layouts --new <name>
--from "<ref>"` now clones `notice` under a new name so it renders and passes the floors
immediately, and `--contract` writes the requirement down. The scaffold does not remove the
design work; it removes the contract archaeology.
