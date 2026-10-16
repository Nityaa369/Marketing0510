---
name: feedback_house_ad_formula
description: "The account's approved ad formula - two-part serif hook (statement + italic turn) plus a believable artefact as the hero, not an abstract diagram and not a bare quote card"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9742c7f3-53d5-44d3-8a58-72139a29d390
  modified: 2026-08-25T14:25:51.337Z
---

Read off ~40 approved ads in `reference_images/` (clearest single example:
`IMG-20260812-WA0134.jpg`). The house formula, top to bottom:

1. Brand row + camp label
2. ICP band - solid filled block, headline scale
3. **Two-part serif headline: a flat statement, then an italic accent clause that turns
   it.** "Companies in 2026 are not hiring. *They are renting your judgement.*" /
   "The code got cheap. *Your judgement did not.*" / "Fully booked *is not a business.*"
4. Small-caps qualifier row (offer attributes, not the ICP again)
5. **Hero = a believable artefact from the better job** - a job board with real-looking
   listings, a booked calendar, a client screen. Something that could be a screenshot.
6. One bold plain-words definition line + an italic gloss, inside the artefact card
7. DAY 1 / DAY 2 / DAY 3 chips with named deliverables
8. Price, terms, CTA

**Why:** the creativity belongs in the *turn* and in the *artefact*; the words themselves
stay flat. Two failure modes cost three rebuilds on one pair of ads (25 Aug 2026):
putting the creativity into an abstract layout device (circles, bars, an SVG diagram that
just restates the headline), and then over-correcting by deleting the hero entirely and
shipping a bare typographic quote card. Both read as flat. The approved corpus is almost
entirely photo-free, so "add a photo" is not the fix either - the fix is an artefact.

**How to apply:** before writing a hook, write the statement and the turn as two separate
sentences and check the second one genuinely reframes the first. Before building a hero,
ask "could this be a screenshot of something from the job I am selling?" If it is a chart,
a bubble diagram or a bar comparison, it is decoration and it will read flat. Never quote
a statistic in the artefact unless a real source exists - WA0134 carries a sourced one,
and an unsourced imitation is the defect that got `cw_10d_senior` excluded from GOLDEN.

**The hook rule is now mechanical.** `hook_rules.py` at the repo root is fitted against
the Section A split (17 approved, 7 rejected, same product and week) and blocks four
defects: a pronoun with no noun before it, a clause that borrows its verb from the
previous one ("The reporting did not."), a contrast whose better side is a variable
("not how much"), and a hook with no verb that moves the reader. Ten of thirteen approved
hooks name the thing she walks away with; six of seven rejects name nothing. Note what
the data did NOT support: second person is not required, since eight of the thirteen
approved hooks never say "you".

Related: [[feedback_ad_creative_vary_composition]] (the artefact shape must differ between
sibling ads even when the chassis repeats), [[feedback_ad_clarity_rules]],
[[feedback_ad_creative_use_real_images]].
