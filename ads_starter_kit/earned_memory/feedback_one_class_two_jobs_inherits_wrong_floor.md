---
name: feedback-one-class-two-jobs-inherits-wrong-floor
description: The barrier line wore .kicker and inherited C8's 56px identity floor; a class must follow its content, not its slot
metadata:
  type: feedback
---

On the serif chassis `.kicker` carried the **tension line** on the Rs 82 winner ("The work is
already here. The trained people are not.") and, on any kit where the tension line was
dropped, silently fell back to the **barrier line** ("no law degree, no US bar exam, no
visa"). Two different jobs, one class, so each inherited the other's size rule: C8 hard-fails
`.kicker` under 56px because it is an identity call-out floor, while the barrier line's own
rule is C25, whose measured floor is 30px.

**Why:** at 56px in the accent colour the barrier line sat within 10px of the 66px head and
wrapped to two ragged lines, so the face had three competing primary elements and no
hierarchy - reported as *"the no law degree required can be designed better"*. Demoting
`.kicker` itself was the wrong fix: it dropped the tension line under C8 too, and
creative_judge caught it on another kit within one run. US Corporate Law did NOT catch it,
because C8 reads the first matching CSS rule - see [[feedback-c8-reads-first-css-rule]].

**How to apply:** `.kicker` (tension line, 56px floor) and `.barrier` (qualifier row, 38px)
are now separate, and `_serif_shell` picks by what the slot actually holds. When a shared
element starts carrying a second kind of content, give it its own class before restyling it -
otherwise the restyle silently moves another kit under a rule it was passing. And set a
chassis floor EQUAL to the checker's floor: `floor=52` against C8's 56 let 54px through.
