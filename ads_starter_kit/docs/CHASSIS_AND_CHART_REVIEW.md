# The `cw_px_` chassis and the money-desk chart

Review of two families in [APPROVED/](../APPROVED/), 24 Aug 2026. Both were approved by
Ramanuj; both carry a defect that the shipped checkers did not test for. Every finding
below cites the principle it comes from, per the `visual-design` and `data-viz` skills.
Nothing here is unsourced opinion.

---

## Part 1 — the `cw_px_` chassis demotes its own evidence

### The defect

`cw_px_demand_board.png` sets its evidence line in grey micro-type:

> "17,000+ content strategy and 64,000+ AI strategy roles open on Naukri now."

Measured on the rendered pixels: **2.8:1**. It is the most persuasive fact on the ad and
the least readable thing on it. Directly beneath, *"You already own the hard half. The rest
is repackaging."* sits at 3.9:1.

### Why it happened, in doctrine terms

*Design for Hackers* ch.7, **Pattern 3, Isolated Factor Layering.** The five factors for
hierarchy are white space, type weight, type size, colour, and ornamentation, and the
prescribed order is:

> "Start with only white space. Then add weight (bold). Then add size. Then colour. Then
> ornamentation. At each step, evaluate whether the hierarchy is sufficient *before* adding
> the next factor."

This chassis skipped to **colour** to de-emphasise a line, and it reduced *value* to do it.
Ch.8 gives the reason that is the worst available choice: Munsell separates colour into hue,
**value** (how light or dark) and chroma, and value is the axis legibility rides on. Lowering
value does not rank a line below another line — it removes it from the page.

Ch.3 confirms it from the type side. The **squint test** asks a text block to read as an even
grey texture, where "light holes indicate poor visual weight management." Squint at
`demand_board` and the evidence line is a hole.

Ch.7's own red-flag table names the general error: hierarchy attempted with the wrong factor,
fix being "default to white space, then weight, then size before reaching for a new
[differentiator]".

### The fix

The de-emphasis this chassis wanted is available for free. The evidence line does not need to
compete with the payoff — it needs to sit **below** it in the reading order, which white space
and weight already achieve. So:

1. **Delete the value reduction.** Set the evidence line at the body ink colour.
2. **Get the separation from space instead.** Increase the gap above the line so proximity
   groups it with the table it summarises, not with the payoff.
3. **If it still competes, drop weight, not value.** Regular against the payoff's bold.

Measured targets, if the grey is kept for brand reasons. These are the darkest value that
clears WCAG 4.5:1 against each face's own ground, computed from the rendered pixels (colours
are histogram-quantised, so treat them as target values and set them properly in CSS):

| Face | y | now | ink → ground | change ink to | gives |
|---|---|---|---|---|---|
| `cw_px_demand_board` | 792–808 | **2.8:1** | `#909078` on `#f0f0d8` | `#6d6d5b` | 4.6:1 |
| `cw_px_demand_board` | 843–867 | 3.9:1 | `#787860` on `#f0f0d8` | `#6e6e58` | 4.5:1 |
| `cw_px_demand_board` | 1012–1031 | 3.8:1 | `#787878` on `#f0f0d8` | `#6c6c6c` | 4.5:1 |
| `cw_px_budget` | 811–866 | 3.6:1 | `#787890` on `#d8f0f0` | `#68687d` | 4.6:1 |
| `cw_px_india` | 1012–1031 | 3.5:1 | `#907878` on `#f0f0d8` | `#7b6767` | 4.6:1 |
| `cw_px_spec` | 760–776 | 3.5:1 | `#907890` on `#f0f0f0` | `#7b677b` | 4.5:1 |
| `cw_px_spec` | 1012–1031 | 3.8:1 | `#787890` on `#f0f0f0` | `#6a6a80` | 4.6:1 |

The y≈1012 row recurs on four faces at 3.5–3.9:1. **That is one chassis element, not four
page defects.** Fix it once.

### The blocker on fixing it

**The `cw_px_` chassis has no source in this repo.** A search for `cw_px*`, `demand_board`
and any generator that writes them returns nothing outside the rendered PNGs in `APPROVED/`.
The kit README says the copy is byte-identical to the superseded `cw_dir_` cells and only the
look changed, but the HTML and CSS that produced the look are not here.

So this family cannot be corrected, only re-created. It also means `ad_lint`'s C-rules — which
read the ad HTML — can never run on it, and `simplicity.py`'s text rules cannot either. Only
the pixel rules apply.

**This is the argument for shipping `html/` inside every kit.** Two of the three approved kits
ship `ads/` and `landing_pages/` and no source, which puts most of both checkers out of reach.

### Note on alignment

The "three competing left edges" I reported earlier was a **false alarm on the chart ads**, not
a `cw_px_` fault, and the rule has been corrected (see Part 2). The genuine alignment finding
in this repo is on `01_ai_discount_chat` in Section A. Ch.6's remedy applies there: the
**invisible axis alignment** technique — "align edges or centers of elements along invisible
vertical or horizontal lines; use grid-line intersections as anchor points" — against ch.6's
named mistake of "relying solely on grid placement without directional forces." Ch.7's review
criterion is the test to apply: spacing and type sizes must trace back to a scale rather than
**arbitrary pixel values**. The Section A chassis uses 34px, 44px, 51px and 70px offsets that
trace back to nothing.

---

## Part 2 — the money-desk chart

Four of the 13 approved Ready13 ads are one chart in four kicker variants: `cw_10b_socialmedia`,
`cw_10c_perword`, `cw_10d_senior`, `cw_10e_women`. A scatter plot with a 2×2 quadrant overlay,
`x = "What one piece of work pays, percentile →"`, `y = "How often clients need it ↑"`, both
axes ticked **0 to 100**, points labelled by job type, hue by client category.

### What is right about it

**The chart type is the correct one.** Cleveland & McGill (1984) rank position on a common
scale as the most perceptually accurate encoding available, and this chart uses position for
both variables. The quadrant fills earn their ink under Tufte's "every element earns its place"
qualifier, because naming the four zones — VOLUME WORK, THE MONEY DESK, SMALL JOBS, SPECIALIST
WORK — *is* the message.

Hue for the three client categories is also safe here despite green/orange being the risky
deuteranopia pair, because every point carries its own adjacent text label. Hue is redundant
encoding, not the sole channel. The **legend** does rely on hue alone; that is the one place to
add a shape or a text cue.

### What is wrong about it

**Numeric axes on judgement placements.** Cairo's *How Charts Lie* taxonomy has two entries
that apply. "Missing baseline / context" is the softer one. The harder one is that a 0–100
axis labelled **"percentile"** asserts a measured distribution. Nothing on the face cites a
source for either axis, and no dataset behind it exists in this repo. So the ticks claim a
precision the data does not have.

This is the same discipline the house rules already apply to prose. `CLAUDE.md`: *"Market data
must be labelled as market data."* And the 22 Aug note on evidence: *"11,000 is scale, not
demand"* — a figure can be sourced and still be misused. A chart is a claim in exactly the
same way, and this one is unsourced.

**Redundant axis ink.** No reader of a feed ad decodes a point's coordinate. Under Tufte's
data-ink ratio the 0/20/40/60/80/100 tick numbers on both axes encode nothing that the reader
will use, while competing with the labels that carry the message.

### The fix

Both problems have one fix, and it costs the ad nothing:

1. **Remove the numeric ticks from both axes.** Relabel the ends qualitatively — y from
   "rarely needed" to "needed constantly", x from "pays little per piece" to "pays a lot per
   piece". The quadrant story survives intact; the false precision goes away.
2. **If the numbers stay, cite the source on the face**, in the same style the other approved
   ads cite theirs, and make it legible (Part 1 applies).
3. **Add a non-hue cue to the legend.**

Option 1 is the recommendation. The ad's argument is *which quadrant the work sits in*, and
that argument is qualitative already.

---

## What changed in the checkers because of this review

- `simplicity.py` **L1** now requires two or more blocks to share an edge before calling it a
  competing edge. The four chart ads were flagged because a scatter plot's axis number row and
  axis title do not align to the body margin, and never should.
- `simplicity.py` **R2** no longer checks `.callout .head .elig .kicker .kick` — `ad_lint` C8
  owns those, at 64px/56px floors far stricter than the 26px this file was using. **S4** was
  deleted outright; `ad_lint` C4 already caps the call-out, tighter.
- `judging-static-ads/engine/creative_judge.py` **`png_for()`** was fixed. It looked only
  beside the HTML, so on every kit in this repo — sources in `html/`, renders in a sibling
  `ads/` — it returned `None` and the whole pixel gate silently skipped. `ad_render_qa`
  (E1–E4) and `crop_qa` (X1) had never run on any creative. They now do.
