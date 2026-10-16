---
name: feedback-one-lp-per-ad-no-ab-split
description: "Never ship two landing pages for one ad as an A/B split unless Ruchika asks for a split test by name; an ambiguous 'keep X, rebuild as Y' means replace"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72d8a971-d1c7-4903-b4a2-5bd535dd4e4b
  modified: 2026-09-22T06:20:05.423Z
---

On 21 Sep 2026 I read "keep the current pages, rebuild them as near-exact copies. They should be
the highest converting lps" as "keep both" and shipped 19 ads with an A page and a B page each.
Ruchika: *"only 1 lp per ad, why are there 2?"* Rule 4 is 1 ad = 1 LP, and it applies to the
count of pages per ad as well as the other direction.

**Why:** a doubled page set doubles funnel setup and splits the ad's traffic, and she never
asked for a test. The second sentence of her message said which one she wanted.

**How to apply:** when an instruction could mean "both", choose the reading that keeps 1 ad =
1 LP and say which you chose in one line, or ask. A split test only when she names one. Donor-copy
pages then still have to clear Rule 4b (under 80% overlap); she chose "vary 1-2 sections per
reader" as the way to do that.

**A donor copy still wears its ad's design.** I briefed the copies as "colours stay the donor's
own" and she asked *"why is the lp design not matching the ad?"* Copy the donor's structure and
words; take palette and hero device (for the search layout: call-out band, search bar, headline
with the accent turn) from the ad. Rule 4 is not suspended by "near-exact copy".
Recolouring the donor was still wrong: *"pick the content of the best performing lps and tweak
that to match the ad. The lp layout and design should match the ad and look like a set."*
And the hero must be the ad's own component, not a re-drawing: seven kits each hand-drew the
search bar as a thin pill and she asked "what is unclear about my instruction??" (22 Sep). Use
`adkit/search_hero.py` (the ad's CSS scaled to the page) for any search-layout page.
"Based on the best LP" means its CONTENT (sections, copy, order) poured into the house page
design that matches the ad; never the donor's layout, fonts or CSS. Related: [[feedback-lps-in-a-kit-must-differ]],
[[project-search-layout-oct-rollout]].
