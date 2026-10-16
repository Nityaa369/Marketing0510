# Content Writing Bootcamp — ad playbook

**Self-contained handover, 22 Aug 2026.** Written after building 22 statics across the
19 target ICPs and having most of them rejected at least once. Everything below is a
rule that was earned by getting it wrong first, with the rejection quoted.

Read with, not instead of: `CLAUDE.md` (project rules) and
`D2C_VALUEPROP_AND_ICPS_HANDOFF.md` (offer, ICPs, evidence). Where those are stricter,
they win. This file is about **how to make the ad actually land**, which is where every
rejection in this project has come from.

---

## 0. The one-line version

> Someone at 20% brain function, scrolling in bed, must know **who it is for**, **what
> is wrong with their life**, and **what they get**, without assembling anything.

Ruchika, 22 Aug: *"if i look at it as someone with brain functionality at 20% due to
lack of sleep, i will not get it. optimise for a person in that state."*

Every rule below is downstream of that sentence.

---

## 1. The build pipeline

Each kit is a folder under `new ad types/<donor-slug>_29-31Aug/` containing:

```
gen_ad.py        the ad as an f-string of HTML, rendered by headless Chrome
html/            the generated source (written by gen_ad.py, do not hand-edit)
ads/             the 1080x1350 PNGs that ship
photos/          generated or cropped imagery, plus prep.py if any keying is needed
ad_copy.md       paste-ready primary text, headline, description
```

Render with `python gen_ad.py`. Non-negotiables in the Chrome call:

```python
subprocess.run([
    CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
    f"--screenshot={out}", f"--window-size=1080,1350",
    "--force-device-scale-factor=1",
    "--virtual-time-budget=25000",     # webfonts are fetched over the network
    src.as_uri(),
], check=True, capture_output=True)
```

**The `--virtual-time-budget` is load-bearing.** Anton and Archivo come from Google
Fonts. At 10000 on a loaded machine the screenshot fires before the fonts land and the
whole ad silently renders in Segoe UI, looking nothing like the house style. It happened
once and was nearly shipped. Use 25000.

### Imagery
No hand-drawn CSS illustration, no fake app chrome (memory
`feedback_ad_creative_use_real_images`). Options in order of preference:
1. Crop a real reference image already in the project.
2. Generate one (`nano_banana_pro` via the Higgsfield MCP), then `remove_background`
   and bbox-crop, or alpha-key by darkness in a `photos/prep.py`.
3. Licensed stock (Pexels/Unsplash) with the source page cited in the kit README.

**Plain geometry is not illustration.** Diagrams, cards, switches, gauges, calculators
and charts built in CSS are fine and always have been — the approved `cw_14` two-path
diagram is exactly that. The ban is on drawn characters and fake UI.

**Recolour generated art if it resembles a trademark.** One hero came back in
blue/red/yellow with a cape; it was recoloured to the cell's palette before going
anywhere near a paid ad.

---

## 2. The house system

Copy this furniture exactly. It is on every shipped ad in
`ContentWriting_W5_29-31Aug/ads/` and it is not optional.

| Element | Spec |
|---|---|
| Kicker | `SKILLARBITRAGE`, ~21px, weight 800, letter-spacing .19em, accent colour, with a 44x4 accent rule before it |
| Price badge | 142–148px circle, top right, accent fill, `₹10` in Anton over `TO JOIN` |
| ICP slab | Solid near-black block, **Anton caps 78–86px**, full width, sitting tight under the badge row (`margin-top:-14px`) |
| Qualifier | 22–24px, weight 900, letter-spacing .09em, one line, sibling identities only |
| Device | The joke. Should occupy 35–50% of the canvas |
| Payoff | Anton caps, 55–62px, two lines, line one ink and line two accent |
| Invitation | Bordered box, 23–25px, weight 800 |
| Terms bar | **One line**, 18–19px: `29 TO 31 AUGUST · 9 HOURS LIVE, NO RECORDINGS` / `₹10 INCLUDING GST, REFUNDABLE ANYTIME`, with the CTA pill left |

Fonts: **Anton** display, **Archivo** body. Serif (Playfair Display) and mono (VT323)
only where a donor format demands it.

Canvas 1080x1350, padding `34px 44px 0`.

### Dark grounds
Invert the slab (white or accent block, dark text) and give any panel a light
translucent fill with a border — a near-black panel on a near-black ground has no edge
and disappears.

---

## 3. The copy formula

Six blocks, in this order, and nothing else:

```
1. SLAB          who they are, one or two words
2. QUALIFIER     sibling identities, one line
3. DEVICE        the joke, carrying the situation
4. PAYOFF        line 1 = the pain, line 2 = the D2C fact with its consequence
5. INVITATION    "In 3 live evenings we show you ... Come and we will show you how."
6. TERMS BAR     one line
```

**Target ~45 words on the face.** A rejected build ran 96.

### The payoff is the whole ad
Two lines of Anton. Line one names **the pain in the reader's own words**. Line two
names **who pays and how many**. Both must stand alone.

Good:
```
FOUR JOBS. ONE TITLE.
4,300 FOUNDERS PAY FOR ALL FOUR.
```
```
YOUR FEE WILL NOT MOVE.
4,300 FOUNDERS PAY PER CAMPAIGN.
```
```
80,000 WORDS FOR SOMEBODY ELSE.
4,300 FOUNDERS PAY FOR CAMPAIGNS.
```

### The definition
`CLAUDE.md` Rule 2 requires the field defined in plain words. The sentence is:

> A campaign is the ad, the landing page, the follow up emails and the tracking that
> shows what it sold.

**Drop it entirely when the device already names the four parts** (an eye chart whose
rows are WORDS / THE PAGE / THE EMAILS / THE TRACKING, a flowchart whose questions are
the four, a card with four numbered tiles). Otherwise the ad says the same thing twice
and that is where the text bloat comes from.

---

## 4. The D2C angle — the part most often missed

Ruchika, 22 Aug: *"the entire d2c research that we have is not showing up in the ads.
the d2c angle has to be a part of the ads."*

Then, on a first attempt that bolted a stat underneath the payoff:

> *"you have added a fact from the lp, okay so what? what does it mean for the viewer?"*

### The three rules

**A. A statistic is not a benefit.** Put the fact IN the payoff at payoff size with its
consequence attached. `11,000 Indian brands sell straight off their own website` in a
strip underneath is trivia. `11,000 BRANDS NEED CAMPAIGNS RUN` as the second half of the
punchline is a reason to act.

**B. Show the expanse.** *"make sure that expanse of demand in d2c is visible across
brands."* Every D2C line carries a brand count or a growth figure. "Brands buy campaigns"
without a number does not convey scale.

**C. Never lean on one figure.** *"do not use the same 11000 stat in all."* One
distinct fact per ad, matched to the ICP. Grep the pack before shipping.

### The evidence, and what it is good for

| Figure | Use it for |
|---|---|
| 11,000 brands selling straight off their own website | Scale, the default |
| 6,000 transacting on a single platform | Scale, second string |
| 3,700 D2C companies | Scale, third string |
| 4,300 founders | When the buyer is a person, not a company |
| 30 to 40% of revenue into advertising | When the point is that spend is continuous |
| Orders +34%, FMCG +32%, health and beauty +48%/41% | When the point is growth |
| Two thirds of order growth from Tier 2 and 3 | Reach and where traffic comes from |
| Marketing hiring +12%, media production +24% | When the point is that the work exists |
| Only ~1% of Indian LinkedIn users post consistently | Ghostwriting and personal brand |
| Mamaearth, boAt, Minimalist | Named proof when a statistic feels abstract |

**Never**: "D2C is booming" (funding fell 54% from 2022), any salary ladder on an ad
face, any "you will earn X".

**Say "need it run", never "are hiring".** 11,000 is scale, not demand — there were only
~805 creative strategist listings on Glassdoor India in March 2026. A sector-literate
reader will catch a hiring claim.

**Say "D2C" only with the definition attached** — it is jargon a writer in Indore may
never have used. Prefer "brands that sell straight off their own website".

---

## 5. Relatability — the bar that fails most ads

### The slab names WHO, the line under it names the situation
Never both in one element. `CONTENT WRITERS` in the slab, the situation in the headline
below.

### The situation must be un-checkable
No number the reader can fail. "20 articles a month" loses the writer who does 8 or 40.
"SENIOR PROFESSIONALS" and "RETIRING IN THE NEXT 5 YEARS" work because their edges are
generous.

### The band must not promise a wider audience than the situation serves
A build ran `CONTENT WRITERS` over "GOOD REVIEW. NO INCREMENT." An appraisal only happens
to salaried writers, so every client-side writer read the band as "me" and the setup as
"not me", and scrolled. **Check that the slab and the situation name the same
population.**

### Use the reader's own vocabulary
Rejected: "PIECES RUN OUT" (no writer calls their output a piece) and "BOOKED / NOT
BOOKED" (a salon word). Fixed to "WORK / NO WORK" and "ONE-OFF WORK ENDS".

### No pronouns in the payoff
*It, that, this, one, them, those* each cost a lookup and a tired reader will not spend
one. Eleven of twenty-two payoffs were failing this. Replace every pronoun with the
actual noun and check both lines stand alone.

Counting words are fine: "one person", "all four", "line one", "one page".

### The payoff must contain a pain and a takeaway
"You already do the whole job" is a compliment, not a pain. "Send a page you built" is an
instruction, not a takeaway. Ruchika: *"the pain point we are addressing is still not
clear. the takeaway is not clear."*

---

## 6. Matching a format to an ICP

**This is where most rebuilds came from.** A donor format has a shape. If the ICP's
situation is not that shape, no amount of rewording rescues it.

| Format shape | Needs an ICP whose situation is | Failed on |
|---|---|---|
| Gauge (E to F) | A level that **depletes and refills** | "Work you can show" only accumulates. Two ICPs failed before the format was dropped |
| Magnifier | A **claim** you can look behind | A headcount is a fact you can print, so the glass had nothing to do |
| Converging flowchart | Every path genuinely ending in **the same place** | Worked first time: the only writer in a company |
| Toggle | A genuine **two-state** switch | Worked, but the two labels must be far apart. "Filling the brief / writing the brief" differ by one word and read as the same label twice |
| Reverse psychology ("don't buy") | Something the reader **already wants**, so refusing it costs something | "Don't learn to write ads" refuses something nobody was planning to do |
| Numbered list landing on item 3 | Items 1 and 2 **predictable**, item 3 the punchline | Items must be two or three words or the gag is a four-beat read |
| Eye test / perceptual gag | Something perceived **without reading** | A typo is textual, not perceptual. An optician's chart is recognised before a word is read |
| Emoji equation | A question the reader is **actually asked, often** | Worked: the notice-period "so what next?" |
| Arithmetic device (calculator) | A problem on the **axis the product moves** | An appraisal is decided by someone else and the camp does not touch it, so the ad could never answer its own joke |

**The chain test.** Both approved cells hold one axis end to end:
- cw_25: *writing what you are told* → *deciding what gets written* → *the person who
  decides owns the campaign*.
- cw_28: *nobody owns the campaign* → *three evenings from now, you* → *you can own the
  next campaign*.

If the problem is on one axis and the solution on another, the reader has to build a
bridge that is not there. That is what "vague" means every time it has been said here.

---

## 7. Borrowing from a donor format

The reference images are **brand ads with nothing to explain**. They can spend their
biggest type on framing. These ads cannot — the same space has to carry who, what and
the offer.

**Cut any donor block that carries no information, on the first pass.** "ACCORDING TO MY
calculations" survived three rebuilds before being cut, and it was the reason that ad
kept reading as vague. "Fuel It Up!" was cut on the first pass of the next ad, which is
the correct instinct.

**Keep**: the ground treatment, the composition, the device, the type contrast.
**Replace**: the framing copy, with the reader's situation.

---

## 8. Compliance, non-negotiable

- **Rule 1** — offer a better job, never threaten. The reader's current work is an asset
  they trade up with. Watch for: a payoff that lands on the job they already have (an ad
  telling a ghostwriter to become a ghostwriter collapses the ladder), and any line that
  frames existing work as worthless.
- **Rule 2** — the campaign definition in plain words, unless the device carries it.
- **No income promise.** Cut lines like "that one gets paid most" and "the same
  reporting, for buyers who pay better". Claims about the **unit of sale** are fine:
  "Get paid for sales, not word count" is shipped and approved.
- **No placement or job guarantee.**
- **Banned words**: "freelancer" / "freelance", "adapt", "content marketing" as an
  audience label, "AI content writer". Aspiration label is **AI Content Strategist** or
  **campaign strategist**, and it never goes in the ICP band.
- **Banned insider words on an ad face**: organic/inorganic content, CRM, lifecycle,
  retention, performance creative, funnel, ROAS, UGC. Say "posts people find on their
  own", "the emails that bring a customer back".
- **No em-dashes.** No "this is not for you if" block.
- **No third-party trade dress.** A Google search box was rebuilt unbranded; a hero was
  recoloured off Superman's palette.
- CTA wording: **"Book my seat"**.

---

## 9. Layout faults that recur

Check every render, do not assume. These all shipped at least once:

1. **Dead band.** A `flex:1` container centring a content-sized device leaves 100–200px
   of empty ground. Either grow the device or pin the container.
2. **`margin-top:auto` on the bar.** Resolves to zero once a sibling absorbs the slack,
   jamming the body copy onto the rule. Resolves to a hole when nothing else grows.
3. **Overflow.** Spending reclaimed height on the device pushes the CTA off the canvas.
4. **`flex:none` on an image container** sizes from the image's *intrinsic* width, not
   its scaled width. Pin the column instead.
5. **Wrapping.** A qualifier row or headline that wraps to two lines reads as a typo.
   Check every string length against the 992px content width.
6. **Contrast.** Amber on vermilion measures ~2.5:1; white on vermilion ~4:1. Anything
   the reader must read goes on a panel or in near-black/white. Only display type can
   carry 4:1.

---

## 10. Before you send

1. `python preflight.py "new ad types/<kit>"` — zero blockers. It cannot judge Rules 1
   and 2.
2. **Open every PNG and look at it.** Copy audits do not catch clipping.
3. Extract the payoffs as text and read them as a list — that is how eight broken chains
   surfaced at once.
4. Grep the pack for repeated statistics.
5. State the four lines `CLAUDE.md` requires: preflight result, the better job each ad
   offers, the sentence defining the field, and the landing page status.

---

## 11. Where the pack stands

22 statics, all 19 target ICPs, in `new ad types/*_contentwriting_29-31Aug/`.

| Kit | ICP |
|---|---|
| two_moods | feast-famine |
| swipe_reveal (2-card carousel) | email-newsletter-writer |
| uno_skip | portfolio-not-working |
| fixmylife | never-raised-rates |
| toggle | agency-junior-brief-taker |
| dontbuy | teacher-explaining-for-a-living |
| closerlook | marketing-team-of-one |
| dialogue | startup-content-hire |
| eyetest | seo-blog-writer |
| equation | notice-period-thinking |
| listof3 | linkedin-ghostwriter |
| plans | writer-in-name-only |
| calculator | ecommerce-catalogue-writer |
| didyoumean | journalist-newsroom |
| gauge (rebuilt, no gauge) | pr-comms-executive |
| flowchart | only-writer-in-company |
| remaining6 | technical-writer, script-video-writer, ux-microcopy-writer, translator-subtitler, proofreader-editor, academic-thesis-writer |

**Open item: no landing pages.** Rule 4 is 1 ad = 1 LP with its own palette and the ad's
promise repeated in the first fold. Every kit reports that single preflight blocker, and
it is the gap between this pack and anything shippable.

The two clearest ads in the pack, worth copying when a format is not working, are the
**dialogue** cell and the rebuilt **gauge** cell. Both follow the shape of the approved
Senior Professionals ad: device, slab, a plain sentence-case promise naming the camp and
the price, a subhead naming what the reader will be able to do, an explainer box with the
invitation, and the terms strip. When in doubt, use that.
