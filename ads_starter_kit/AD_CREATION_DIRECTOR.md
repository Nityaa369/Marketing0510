# The Ad Creation Director

**This is the sole director for generating a static ad + landing page pair in this repo.**
Read this file, and only this file, before writing a single line of creative. It folds in
Ramanuj's compliance rules (`CLAUDE.md`), the launch/kit SOPs, the earned lessons in
`docs/CONTENT_WRITING_AD_PLAYBOOK.md`, the visual doctrine in `docs/CHASSIS_AND_CHART_REVIEW.md`,
and every standing feedback note in project memory — reconciled into one process, in the order
you actually use them.

It exists because five specific complaints kept recurring: **content not aligned on the image,
the image trying to be too clever, the hook trying to be too clever, ICPs that nobody would
actually buy for, and readability being off.** Every section below is designed against one or
more of those five. Where a section fixes a specific complaint, it says so.

If a kit's own README sets a stricter rule than this file, the README wins for that kit. Nothing
else outranks this file for how an ad gets built.

---

## 0. The one test everything else serves

> *"If I look at it as someone with brain functionality at 20% due to lack of sleep, I will not
> get it. Optimise for a person in that state."* — Ruchika, 22 Aug 2026

> *"For someone scrolling in bed or the bathroom — can they immediately identify if this is for
> them or not?"*

Run this before anything else is judged, on the ICP callout first:

**Would someone scrolling Instagram half-asleep, on the toilet, paying zero attention,
understand this in under 3 seconds without re-reading? If no, simplify — don't add anything to
compensate, remove.**

Everything below exists to make that test pass by construction, not by luck.

---

## 1. THE SPEC — write this before any creative exists

*Fixes: irrelevant ICPs, and the general waste of building a whole ad before finding out the
idea was wrong.*

One block per ad, filled in and approved **before a single pixel or headline is drawn**:

```
## <ad-id>
ad:  ads/<file>.png                (leave as TODO until built)
lp:  landing_pages/<file>.html     (leave as TODO until built)

better_job:       What different, better job is this person being offered? One line.
                  Never "the same job, done more carefully" or "the same job, plus a
                  new obligation" — if that's the honest answer, the idea isn't ready.

field_definition: The plain-words "X is / X means" sentence for whatever field or role
                  is being sold. Must survive to the ad face AND the landing page's
                  first fold, in the same words.

deliverables:     Three or four named, concrete things the reader leaves with.
                  Not benefits — nameable objects ("a landing page you built",
                  "a one page results report"), not adjectives.

buying_pressure:  Why does THIS person pay and show up NOW? Name a force: a shrinking
                  employer, a frozen rate, a career break, a notice period, a ceiling.
                  Never "wants to grow" — that has no urgency and describes everyone.

awareness:        unaware | problem aware | solution aware | product aware | most aware
                  Plus one line on what it changes about the hook (see Section 4).

pain_score:       Five dimensions, each 1 to 5, so the shortlist can be RANKED instead
                  of every ICP on a list quietly getting an ad:
                    severity      what it costs them — money, standing or time
                    frequency     how often it bites
                    activation    is something forcing the decision NOW, and when
                    reachability  can this exact person be targeted on Meta
                    fit           does this camp change the outcome for them
                  Written: severity 4 | frequency 5 | activation 4 | reachability 5 | fit 4
```

Scaffold a whole kit's spec from an ICP list, before any ad exists, then print the ranked
shortlist — which needs no ads, no palette and no pages to exist:
```bash
python preflight.py --scaffold-from <icp-list.md> <kit-folder>
python preflight.py --shortlist <kit-folder>
```
That table is round one of approval. Send it, nothing else — no ad face, no palette, no
landing page. Strike whatever is wrong. **Only build what survives.** A rejection here costs a
paragraph; the same rejection after the kit is built costs the kit.

**`pain_score` exists because a flat ICP list makes every ICP look equal.** Forty arrive, twenty
get an ad, and nothing on the page says which twenty or why. Ranking them puts the weak cells
in front of the person approving them, at the point where striking one is free. It is
**not fitted against live cost** — no scored ICP has run yet — so it decides what to *build*,
never what will convert. `preflight.py` blocks on a malformed or missing score and never on a
total; it warns when reachability or fit is 1 or 2, because an ICP that cannot be targeted, or
that this camp does not serve, wastes a cell whatever the other three columns say.

*(Adapted from the offer-to-campaign algo, Uday Wagh, 21 Aug 2026. Two of its seven dimensions
are deliberately dropped: `recognition` is the `awareness` field under another name, and
`differentiation` is a property of the ad rather than the ICP, so it cannot honestly be scored
before the ad exists — kit-level sameness is already gated by Rule 4b and V9.)*

**The `buying_pressure` field is what stops an irrelevant ICP.** An ICP with no named force
behind it produces an ad that can pass every other rule in this file and still sell nothing.
"Content writer who wants to grow" is not a buyer. "Content writer whose per-word rate hasn't
moved in three years" is.

---

## 2. THE ICP RULE

*Fixes: irrelevant ICPs, and the bed-and-bathroom failure.*

**The ICP must be a real, self-recognized job title — never an invented demographic or
psychographic label.** Rejected outright: "women looking to learn AI skills" (nobody identifies
that way). Approved, every time: the reader's actual job title — CONTENT WRITERS, SENIOR CONTENT
WRITERS WHO WANT TO EARN MORE, AGENCY COPYWRITERS ON INDIAN RETAINERS, COURT LITIGATORS, COMPANY
SECRETARIES.

**Any situation attached to the identity must be un-checkable.** A specific number is a checkable
claim, and a checkable claim gets checked and fails: "20 articles a month" loses the writer doing
8 or 40. "SENIOR PROFESSIONALS", "RETIRING IN THE NEXT 5 YEARS" work because their edges are
generous.

**The callout must name WHO they are, not only their situation.** A purely circumstantial callout
("WRITING 20 ARTICLES A MONTH") has no identity anchor. Split it: **identity in the callout
band, situation in the headline directly below.** Never ask one element to do both.

**Widen laterally, never upward.** A qualifier row may add sibling identities at the same rung
(CONTENT WRITERS · COPYWRITERS · SEO WRITERS). It must never include the aspiration label —
putting "strategist" in a content-writer's ICP band names the destination as the starting
identity and collapses the ladder the ad is selling.

**The band must not promise a wider audience than the line under it serves.** Check that the
callout and the situation line name the *same population*. A `CONTENT WRITERS` slab over an
appraisal-based setup line lost every client-side writer, because only salaried writers get
appraisals.

**Use the reader's own vocabulary, never invented shorthand or a borrowed-industry word.**
Rejected: "PIECES RUN OUT" (no writer calls their output a "piece"), "BOOKED / NOT BOOKED" (a
salon word). Fixed to "WORK / NO WORK".

**Default population for a SkillArbitrage / content-writing brief**, unless told otherwise: a
person paid per word, per piece, or per project for writing, whose rate hasn't moved. For a
LawSikho / arbitration brief: a lawyer, company secretary, or law student who has never run an
arbitration matter but is about to be asked to. Do not invent a third population or a niche
cross-section of either without an explicit brief asking for it.

---

## 3. THE TWO COMPLIANCE RULES

*Ramanuj's own words. These are not mechanical — no script can see them. Judge every ad against
both before anything else.*

### Rule 1 — Offer a better career. Never threaten.

The reader's current work is an asset they trade up with, **never** a liability they're exposed
on. Three things get rejected every time:

1. **Regulator / liability framing** — telling the reader a law now applies to them, or that
   something they do is now prohibited.
2. **More work at the same desk** — selling extra admin, an extra form, an extra process to own,
   in the job they already have.
3. **"Get named the person who fixed it"** — internal credit for unpaid extra work is a chore
   with a compliment attached, not a career.

**Worked example — identical template, opposite verdicts, same night:**

> **APPROVED:** *"You handle named patient information every single day. Health data is the most
> sensitive category there is, and healthcare is the least prepared sector in the country.
> Your domain knowledge is the part consultants cannot buy."*

> **REJECTED:** *"Your lead database is full of students, and many of them are children.
> Targeted advertising to children is banned outright and parental consent cannot cure it."*

The first says *you already own something rare*. The second says *you are in breach*. That is the
whole difference.

> *"You need to offer a different career to this person, not threaten with a regulator."*
> — Ramanuj

**Your check, before handing over:** for each ad, answer in one line — what better job is this
person being offered? If the answer is "the same job, done more carefully" or "the same job,
plus a new obligation", rewrite it.

### Rule 2 — No assumed knowledge

**Cryptic = the ad only makes sense to someone who already knows what the field is.** This is
the single most repeated rejection in this project's history, and it is missing 9 times out of
10 for the same reason: the one-sentence plain-words definition of the field or role got skipped.

> **REJECTED as cryptic:** *"Turn what you already know into a freelance-ready privacy
> certification, recognised outside India."* — never says what the certification leads to, or
> what "what you already know" refers to.

> **APPROVED:** *"A company secretary who handles the paperwork of a deal but never the deal?
> … Do corporate finance work on the deal itself, not only the filings around it. Deal work
> means valuing the company, building the model and reading the term sheet before anyone
> signs it."*

**Required first-fold structure**, exactly this order:

1. **Who you are, as a question.** *"A final-year B.Com student with no finance job in sight?"*
2. **Qualifier row.** Concrete titles/credentials — `B.COM · BBA · M.COM · FINAL YEAR ·
   FRESHERS`.
3. **The offer, in plain words.** What they will be able to *do*.
4. **One sentence defining the field.** No jargon, no assumed knowledge. **Never skip this.**
5. **Three or four named deliverables.** Concrete and nameable, not benefits.
6. **Price, dates, live-only, and a risk reversal.**

**Your check, before handing over:** could someone who has never heard of this field tell you
what job they would be doing, from the field-definition line alone? If not, it's cryptic — and
the fix is almost always to write step 4.

---

## 3.5 THE HEADLINE SUBJECT TEST — a mechanical rule, not a taste call

Derived from `DataPrivacy_Wave1_29-31Aug/` (12 Aug 2026, the batch `CAMPAIGN_MAP.md` calls
"the source of CLAUDE.md Rule 1") — 9 headlines, 5 approved, 4 rejected, read side by side:

| Headline pattern | Verdict |
|---|---|
| *"...every call you make to a borrower **is now** data processing."* | REJECTED |
| *"...the PAN and bank details you collect **now need** a data agreement."* (subhead: *"One more form in a checklist you already own."*) | REJECTED |
| *"...your payroll vendor **is now** a data processor..."* (promise: *"...named the person who fixed it."*) | REJECTED |
| *"**Become the** Data Protection Officer your hospital will need in 2027."* | APPROVED |
| *"**Become the** Data Protection Officer your platform will need in 2027."* | APPROVED |
| *"**Start a** privacy analyst career from home."* | APPROVED |
| *"Tired of targets? **Move into** data privacy instead."* | APPROVED |
| *"...a complaint has to be routed differently..."* (promise: *"...named the person who built it."*) | **APPROVED anyway** — logged as a known exception, not a hidden rule (`CAMPAIGN_MAP.md`) |

**The test: does the sentence's grammatical subject change to a new destination role
("become," "start a ___ career," "move into"), or does it stay the reader's current job with
a new clause attached to it ("is now," "now needs," "already own")?** Four of five approvals
pass this test; three of four rejections fail it. Run every headline through it explicitly,
as a sentence-structure check, not a vibe check:
- Rewrite the headline with the job title as the grammatical subject if it currently isn't.
- If the subject is still the current job and something is happening *to* it, that's the
  rejected shape — rewrite so the subject is the new role instead.
- **One exception is on record** (customer support, approved despite matching the rejected
  shape). Don't treat 4/5 as 5/5 — flag a headline that matches the rejected pattern as a risk
  even if you can point to one precedent that got through anyway.

This is the same underlying instinct as Rule 1, made mechanical enough to check without
judgment: "is now" / "now needs" grammatically keeps the burden attached to the current job;
"become" / "start" / "move into" grammatically relocates the reader to the new one.

## 4. THE HOOK SYSTEM

*Fixes: the hook trying to be too clever.*

**Classify before you write.** A hook is only good relative to what the reader already believes.
Deciding this first is what stops "give me 10 hooks" from producing ten variants of one opener.

| Decision | Options |
|---|---|
| Awareness level | unaware → problem aware → solution aware → product aware → most aware |
| Strategy | sell the click vs. sell the solution |

- **Unaware** → curiosity is allowed, but the field-definition line (Rule 2, step 4) must follow
  immediately — this is where "cryptic" lives.
- **Problem-aware (the usual default)** → name their grievance in their own words. *"They pay you
  for the typing."*
- **Solution-aware** → contrarian or proof.
- **Product-aware** → offer and price, stated plainly.

### The six hook types that actually got approved

Pick ONE. Do not free-associate a seventh.

1. **Grievance-as-headline.** The payoff states the reader's exact complaint as a flat
   declarative. *"They pay you for the typing."* · *"Get past the rung where writers stall."*
   5–12 words. Never a compliment ("you already do the whole job" is not a pain).
2. **Reader's-own-voice speech bubble.** A line the ICP would plausibly say out loud, over a
   scene, with a flat caption underneath naming the effect — the caption never explains the
   joke. *"Sir, I will call you back. I think I will just get into arbitration instead of
   waiting in the corridor all day."*
3. **Interrogated-list / self-audit device.** A short table mapping what the reader already does
   to what it's actually called. Max 4 rows, every row indisputably true of the reader already —
   no aspirational rows.
4. **Overheard-dialogue / interview exchange.** 3 lines max, ending on the question the reader
   can't currently answer. Never resolve it inside the bubble.
5. **Quoted-self / "your week probably" mirror.** A bulleted quote box in the reader's actual
   voice, including code-switched language if that's how the ICP talks. Never an English
   paraphrase of a Hindi complaint.
6. **Data/quadrant device.** A simple chart with the reader's current bucket and target bucket
   both visible. Max 4 labeled zones. **If it carries numeric axis ticks, they must cite a
   source on the face** — an approved chart shipped with unsourced 0–100 "percentile" ticks and
   it was a real defect. Default to relabeling the axis ends qualitatively instead ("pays
   little" → "pays a lot").

### The seventh failure mode: a headline that names a TASK FOR THE READER

Added 31 Aug 2026, from the one rejection in `WomenRemote_Wave9` (6 of 7 approved).

> **REJECTED as cryptic:** *"Read all three afternoons, then decide on the work."*

The headline instructs the reader to **evaluate the product**. Its grammatical subject is
a chore she has to perform before she gets anything. Compare the five approved siblings in
the same wave, each of which names a destination or a prize: *"The work is real. Decide
from the numbers."* (decide FROM evidence already on the face) · *"Twelve years at home.
Then her first paid work."* · *"Become the assistant US owners cannot find."* · *"Your
first client. Not luck, a route you can walk."* · *"Whatever your hours, you can take the
same route."*

**The test: is the biggest line on the face about the JOB, or about BUYING?** A headline
whose verb asks her to read, compare, check, consider or decide-whether is selling the
purchase process. Section 3.5's subject test does not catch this, because the subject did
move off her current job; it just moved onto a task instead of a destination.

**Two gates passed this face, so do not lean on either for it.** The blind-reader test in
12.5 passed it on all five questions, because the device underneath defined the job
perfectly well — blind-reader measures *comprehension*, never *desire*. And
`hook_rules.py` passed it once "decide" was in the forward-verb lexicon; "decide" moves
the reader through a purchase decision, not into a job, and no regex separates those. This
one is a human read of the biggest line, every time.

### The universal hook test

> Would someone scrolling Instagram half-asleep, on the toilet, paying zero attention,
> understand this in under 3 seconds without re-reading? If no, simplify.

### Five mechanical filters, after picking the type

1. **One job per hook.** One promise, or one proof point, or one objection removed. Not two.
2. **Facts, not adjectives.** "Twenty pieces a month, and the income sits flat" beats
   "frustrating rate stagnation."
3. **No decode step.** If understanding it requires solving anything — wordplay, a pun, a riddle
   — cut it. *"the flipping burger thing is not clear as a hook — who are you talking to and
   why."*
4. **No throat-clearing.** "In today's fast-paced world", "Have you ever wondered."
5. **Name the prize, not the pain, in the biggest element.** Pain earns recognition in the
   headline; the prize belongs in the single biggest line on the face.

### Why this can't be judged by feel, or by a script

A repo-wide census of 171 shipped ad faces found the mechanical rule built specifically to catch
dangling/cryptic references **fired zero times** — and two headlines predicted to be rejects for
sounding clever (*"Own all four"*, *"Own the campaign nobody owns"*) were both **approved**,
because each is resolved in the same glance by an adjacent device (a four-row list, a plain line
right above it). Your own read of "does this sound clever" is not reliable, and `simplicity.py`
cannot see semantic cleverness either — it only catches volume, deficiency framing, and dangling
references with zero antecedent anywhere on the face. **The two things that actually catch
"too clever" are Section 8 (Golden Examples) and the blind-reader test in Section 12.5. Run both,
every time — a clean mechanical gate is not evidence the hook is simple enough.**

---

## 5. THE HERO / DEVICE SYSTEM

*Fixes: the image trying to be too clever, and busy/layered visuals.*

**Default to a device, not a photo, unless the brief specifically calls for a scene.** Most
shipped, approved ads in this account carry no photograph at all — the space a "hero image"
would occupy is a plain data or text device: a table, a chart, a chat exchange, a quote box. This
is a stronger default than photography for most content-writing creative, not a fallback.

**But device-vs-photo is not what makes a hero catch attention — specificity is.** Confirmed
live: a first build used an abstract device (a bare risk comparison, a generic "0 openings"
line) and it was mechanically clean and completely flat. Rebuilding with the *exact same
device type* but concrete, named, quoted detail — three specific quoted worries in the
reader's real voice, named cities instead of a generic count — was the actual fix, not
switching to a photo. Every entry in `GOLDEN/GOLDEN.md` confirms this: real quoted dialogue,
named job-ladder rungs, a real interview exchange. A device filled with generic labels is not
simpler than one filled with specifics — it's just emptier. When a hero reads as flat, the fix
is almost never "make it a photo instead"; it's "make the words in it name a real, specific
thing" (a real line someone would say, a real place, a real number), the same discipline
Section 7 already applies to statistics ("facts, not adjectives").

**No hand-drawn CSS illustration, no fake app chrome.** Never invent UI, icons, or avatars in
CSS/SVG. Options, in order:
1. Crop a real reference image already in the project.
2. Generate one (image model), then background-remove and crop.
3. Licensed stock (Pexels/Unsplash) with the source cited in the kit README.

Plain geometry — diagrams, cards, switches, gauges, calculators, charts built in CSS — is not
illustration and is always fine. The ban is on drawn characters and fake UI.

### The complexity ceiling

- **Photo/scene hero:** one subject or speaker + one small reacting group at most, one moment,
  one shared emotion. No montage, no second location, no metaphor layered on top of the literal
  scene.
- **Device hero:** one table/chart/chat/list, max 4 rows or zones, one flat gloss line
  underneath. Never two devices stacked on one face.

### The one-sentence rule

**If you can't describe the hero — image or device — in one sentence without the word "and," it
is too complex. Simplify.**

### The brief template

- Photo hero: `[One subject] + [One action or state] + [One emotion/mood]`
  > A court litigator + announcing on the phone that she's leaving corridor practice for
  > arbitration + calm resolve, colleagues behind her showing shock.
- Device hero: `[One reader-recognizable device] + [One thing it maps or reveals] + [One flat
  gloss line]`
  > A four-row "what you do → what it's called" table + mapping daily tasks onto
  > campaign-strategist vocabulary + "You already own the hard half. The rest is repackaging."

### Matching a device to an ICP — check the shape, not just the availability

A borrowed device has a shape. If the ICP's situation isn't that shape, no amount of rewording
rescues it:

| Device shape | Needs an ICP whose situation is | Fails when |
|---|---|---|
| Gauge (E to F) | A level that **depletes and refills** | The thing only accumulates |
| Converging flowchart | Every path genuinely ending in the **same place** | Paths don't converge |
| Toggle | A genuine **two-state** switch, labels far apart | Labels differ by one word |
| Numbered list landing on item 3 | Items 1–2 predictable, item 3 the punchline | Items run long |
| Eye test / perceptual gag | Something perceived **without reading** | The gag is textual, not visual |
| Arithmetic device | A problem on the **axis the product moves** | The camp can't answer its own joke |

**Cut any borrowed block that carries no information, on the first pass.** If a line survives
three rebuilds and the ad still reads as vague, that line is usually why.

---

## 5.5 THE SEVEN-ELEMENT TEMPLATE — validated at volume, 7/7, one build

`CorporateFinance_MediaBuyer_15-17Aug/` is the best evidence in this repo of low-revision
output at batch size: 7 ads, one build date (13 Aug), **all seven approved** — no rejected
sibling to rebuild against. Same seven elements, in the same order, every time; only the
identity, the situation, the deliverables, and the diagram change per ICP.

1. **Question headline naming the identity**: *"A [ROLE] who [limitation/aspiration]?"* —
   *"A cost accountant who wants to do more than cost sheets?"* · *"An accounting firm owner
   whose clients are all within 50km?"* Note the clause attached to the identity is always a
   **ceiling or an aspiration** ("wants to do more," "whose clients are all within X"), never
   an **added burden** ("is now," "now needs") — the same direction Section 3.5's headline
   test checks for, just inside a question instead of a declarative sentence. Both shapes are
   validated; a burden-clause shape is not, in either form.
2. **Qualifier row**: real credentials/titles, small caps — `CMA · CMA INTER · COST
   ACCOUNTANTS · B.COM`.
3. **Declarative payoff line**, two-tone (identity phrase in accent colour, rest in ink):
   *"Do corporate finance work that shapes the decision, not just the report."*
4. **Italic serif definition sentence** — a distinct typeface from everything else on the
   face signals "this is the plain-words definition," satisfying Rule 2 visually as well as
   verbally: *"Costing, budgeting and variance analysis are the base of all financial
   planning work..."*
5. **A bespoke diagram specific to this exact role** — never a generic icon with swapped
   labels. See Section 12.6.
6. **3-4 "key takeaways"** with a repeated checkmark icon, each a **named, concrete
   deliverable**, never a benefit adjective: *"A written 6-month plan to your first client"*,
   never "confidence" or "growth."
7. **Terms bar**: price + dates + CTA, one line, consistent across the whole batch.

**Use this as the default skeleton for a new batch of 30-40.** Fill elements 1-4 and 6 from
the spec (Section 1) per ICP, design element 5 fresh per ICP (Section 12.6's test: could this
diagram be relabeled onto a different ICP? If yes, redesign it), keep element 7 fixed batch-wide.
Holding six of seven elements constant and changing only the identity/situation/diagram is
what kept this batch to one round.

**Word budget: 130, not 100, for this template — confirmed by building against it.** Section
7's 100-word cap was fitted against `ContentWriting_SectionA_29-31Aug`'s four-element
template; ported faithfully, this seven-element one structurally runs 125-130 words (a
qualifier row, an italic definition sentence, and three named checklist items are each real
content, not bloat) and a two-ad test came in at 126 and 130 before any trimming. Don't
silently cut the qualifier row or thin the checklist to force the old cap — that erodes the
exact specificity that makes the template work. Run `python simplicity.py --word-cap 130
<folder-or-files>` for anything built on this template, and say so in the kit's `value_props.md`
or README so the number isn't mistaken for a silent rule change. The two-element budgets are
both real, for different templates — check which one a kit is using before applying either.

## 6. THE VISUAL HOUSE SYSTEM

*Fixes: alignment and readability.*

Canvas **1080×1350**, padding `34px 44px 0`. Fonts: **Anton** (display), **Archivo** (body).
Serif/mono only when a borrowed format demands it.

| Element | Spec |
|---|---|
| Kicker | brand mark, ~21px, weight 800, letter-spacing .19em, accent colour, small accent rule before it |
| Price badge | 142–148px circle, top right, accent fill |
| ICP slab | solid near-black block, **Anton caps 78–86px**, full width |
| Qualifier | 22–24px, weight 900, letter-spacing .09em, one line, sibling identities only |
| Device | the hook. 35–50% of the canvas |
| Payoff | Anton caps, 55–62px, two lines, line one ink / line two accent |
| Invitation | bordered box, 23–25px, weight 800 |
| Terms bar | one line, 18–19px |

**Dark grounds:** invert the slab (white or accent block, dark text). A near-black panel on a
near-black ground has no edge and disappears.

### Alignment

- **Spacing and type sizes trace back to a scale, never an arbitrary pixel value.** Offsets like
  34px, 44px, 51px, 70px that don't derive from anything are how three competing left edges
  happen.
- **An edge only counts as competing when two or more text blocks share it.** A chart's axis
  number row and axis title legitimately don't align to the body margin — that's not a defect,
  don't flag it as one.
- Use the *invisible axis* technique: align edges or centres of elements to shared vertical/
  horizontal lines; use those as anchor points rather than eyeballing offsets per element.
- Check every string length against the actual content width before shipping — a qualifier row
  or headline that wraps to two lines reads as a typo.

### Readability — measured, not eyeballed

- **Type-size floors on identity elements: 64px minimum for a call-out, 56px minimum for a chip.**
  A 52px headline reads as "barely visible" against this floor — do not trust a looser rule.
- **Body copy floor: nothing meaningful under 2.4% of canvas width**, and never in reduced
  opacity.
- **Measure contrast on the rendered PNG, never estimate from CSS.** Text frequently sits on a
  strip drawn by an absolutely-positioned sibling that no CSS-level check can see — six approved
  ads were nearly miscalled this way. **Nothing the reader must read may sit below 4.5:1
  contrast** against its actual rendered background. One approved ad shipped a defect exactly
  here: its single most persuasive line sat at 2.8:1, in grey, under its own headline — the most
  important fact on the ad was the least readable thing on it.
- **Nothing important goes in a blind spot.** No grey colour, no micro font, and nothing placed
  *above* the heading expecting to be read — readers read the heading then look below it, never
  above it.
- To de-emphasise a line without killing it: use white space and weight first, colour only as a
  last resort, and never lower a line's *value* (light/dark) as the only differentiator — that
  doesn't rank it below another line, it removes it from the page.
- On any chart: use position/size encoding over colour where possible; if colour is the only
  channel in a legend, add a shape or text cue too (colourblind safety).

---

## 7. THE COPY SYSTEM

*Fixes: word volume, and the general "too much to read" complaint.*

### Word counts

- **On-face copy:** design target **40–45 words**. Hard ceiling **100 words** (counts everything
  on the face — terms bar, brand row, price included). Treat 40–45 as the real target; 100 is the
  point of no return, not something to approach.
- **Primary text (off-image caption):** **80–100 words, hard ceiling 110.** Corrected 31 Aug 2026
  against the `APPROVED/` corpus: 150 approved blocks measure p25 80, median 86, p75 97, and 140
  of 150 sit at or under 110. The earlier "100–150 words" figure here was never fitted to the
  corpus and was making drafts run long. Structure: situation → pivot → delivery sentence → terms.
- **The sentence-level formula for all of this lives in [SOP/07_AD_COPY.md](SOP/07_AD_COPY.md)** —
  the four moves, the constant delivery sentence (92% of approved blocks, three named things and a
  horizon), the headline ceiling of 10 words, the negation strip, and the comparison-table row
  grammar. Read it before writing copy; this section is the summary, that file is the rule.

### Sentence rules

- Short, declarative, mostly one clause. Direct second-person address.
- **No bare pronoun** (*it, that, this, one, them, those*) standing in for a noun in a headline
  or payoff — replace with the actual noun. Counting words are fine ("one person," "all four,"
  "line one").
- **A statistic is not a benefit.** Fold the fact into the payoff at payoff size, with its
  consequence attached in the same breath — not "11,000 brands sell direct" but "11,000 brands
  need it run."
- **Never repeat the same statistic across a pack.** One distinct fact per ad, matched to the
  ICP. Grep the pack before shipping.
- **A statistic proves scale, not demand** — don't let a big number imply hiring volume it
  doesn't support.

### CTA

States the full exchange (price + what it buys), never a bare "reserve my seat." Use the exact
wording the product line specifies (e.g. "Book my seat", "Join for ₹200 →") — check the kit
README for the product's fixed CTA string.

### Anti-voice list — never generate these

Em-dashes · "this is not for you if…" (qualify positively instead) · "freelancer"/"freelance",
"adapt", "content marketing" as an audience label, "AI content writer" (aspiration label is *AI
Content Strategist* / *campaign strategist*, and it never goes in the ICP band) · insider jargon
(organic/inorganic content, CRM, lifecycle, retention, performance creative, funnel, ROAS, UGC) ·
filler words (transform, discover, unlock, elevate, leverage — none appear in any approved ad) ·
deficiency framing ("you have never…") · salary/per-word rupee/earnings figures on an ad face ·
an acronym (e.g. "D2C") without its plain-words definition attached in the same breath ·
regulator/liability/threat framing · any placement or job guarantee · any income promise.

---

## 8. THE LANDING PAGE

*Fixes: the drop-off between what the ad promises and what the page says.*

- **The page spine is the 21-step framework since 25 Sep 2026** (SOP/05). Build from the newest
  kit that used it; see SOP/05 for the list and the house adaptations.

- **The first fold repeats the ad's promise in the same words as the ad.** The page `h1` should
  appear verbatim on its own ad face — check it mechanically, not by eye.
- The Rule 2 field-definition sentence belongs in the first fold too, not only on the ad.
- **One ad, one landing page. Always.** Never point two ads at one page. The page mirrors its
  ad's colours, headline wording, and hero device. Every ad gets its own palette; keep a
  `PALETTE_REGISTER.md` past six pairs.
- **The pay button carries a real funnel URL.** No `TODO`, `PAYMENT_LINK_PENDING`, `href="#"`, or
  literal `<slug>`.
- **Never put a hedge or disclaimer paragraph above the CTA.** If a figure needs that much
  qualification, remove the figure, don't caveat it.
- **Test-buy in a real browser, every page, not a spot check.** `curl` returns false 404s on
  GrowthX funnels and proves nothing.
- Money data is matched per page — a student page never quotes a strategist salary band.
- Self-contained, hero embedded, no sibling folders. Typically 36–90 KB, 2,800–3,000 words.

---

## 9. THE STANDING COMPLIANCE LIST

Not up for renegotiation per pack. A kit README may be stricter, never looser.

- **No placement or job guarantee, ever.**
- **No income promise.** Market data must be labelled as market data, with source and date.
- **No earning, salary, or per-word rupee figures on any ad face.** LP-only, and even there
  labelled.
- **No AI-fear framing.** The argument is a ladder — AI took the production floor, which raised
  the price of the judgment that decides what gets produced.
- **Live only, no recordings.** Never promise a recording. Substitutes: session notes, templates,
  the WhatsApp group, a certificate.
- **Price labelled including GST**, refundable anytime, stated plainly wherever price appears.
- **Brand separation** — SkillArbitrage and the legal-products brand are never co-branded.
- **No em-dashes** anywhere in shipped copy.
- **No "this is not for you if…" block.**
- **No third-party trade dress** — recolour any generated art that resembles a trademark.

---

## 10. THE GENERATION WORKFLOW

```
STEP 0: SPEC (Section 1) — write and get it approved before anything else exists.

STEP 1: BRIEF INTAKE
- Product/offer, price, format, dates
- ICP (Section 2) — default to the primary population unless told otherwise
- The ONE message — not two, not three
- The proof point — a stat with its consequence attached, or a named example

STEP 2: HOOK
- Classify awareness level (Section 4) BEFORE writing a word
- Pick ONE hook type from the six in Section 4
- Generate up to 5, each passing the 3-second test
- Run the five mechanical filters

STEP 3: HERO / DEVICE (Section 5)
- Decide device or photo — device is the stronger default
- Write the one-sentence brief; if it needs "and," split or simplify
- Check the device-shape table if borrowing a format

STEP 4: LAYOUT (Section 6)
- Use the house element spec table, or the kit's documented equivalent
- Anchor every offset to a shared line, never an arbitrary pixel value
- Check every string length against content width

STEP 5: COPY (Section 7)
- Face copy 40–45 words, 100 hard ceiling; primary text ~100–150 words
- Apply the anti-voice list
- Check every line for a bare pronoun

STEP 6: LANDING PAGE (Section 8)
- First fold repeats the ad's exact words
- Real pay URL, no hedge above the CTA
- Own palette

STEP 7: SELF-CHECK (Section 11) — every box, before showing output

STEP 8: MECHANICAL GATE (Section 12)
python preflight.py <kit-folder>
python simplicity.py <kit-folder>
Zero blockers on both, or it is not ready.

STEP 9: BLIND-READER TEST (Section 12.5) — mandatory, not optional.
        THE UNIT IS THE WHOLE FIRST FOLD: call-out, head AND the plain-words
        definition sentence. Not the head alone, and not call-out plus head.
        Measured 3 Sep 2026: on call-out + head only, the four Patent faces that
        carry a live cost score 0 of 4 CLEAR and three of them VAGUE, including
        icp_28_biomedical_devices at Rs 91.36, the cheapest patent ad in the
        account. A test that fails every ad that ran cheaply does not
        discriminate. Four rebuild passes were spent chasing it.
        SO: IF A BLIND READ COMES BACK BAD, RUN THE SAME TEST ON THE PRICED
        WINNERS BEFORE ACTING ON IT. That control costs one subagent and it is
        the difference between a real defect and a broken ruler.
        THIS IS NOW AUTOMATIC AND YOU DO NOT HAVE TO REMEMBER IT:
            python blind_reader.py --prepare <kit>
            (one fresh subagent per packet_F*.txt, all in one message)
            python blind_reader.py --score <kit>
        The controls are mixed in blinded BEFORE the read, and check_all.py
        reports ERROR for a kit that never ran one or whose faces changed since.

STEP 10: HANDOVER (Section 13) — state the five lines.
```

---

## 11. THE SELF-CHECK

Mapped directly to the five recurring complaints. Every box, before showing anything.

- [ ] **Alignment** — do every two-or-more text blocks that should share a left edge actually
      share it? Does every offset trace to a scale, not an eyeballed pixel value?
- [ ] **Image not too clever** — does the hero (photo or device) reduce to one sentence with no
      "and"? Is it one subject/one device, not a layered composite?
- [ ] **Hook not too clever** — is it one of the six named types, not an invented riddle? Does it
      pass the 3-second half-asleep test? Would it survive the blind-reader test in Section 12.5?
- [ ] **ICP actually relevant** — is `buying_pressure` a named force, not "wants to grow"? Is the
      identity real and self-recognized, not invented? Is the situation attached un-checkable?
- [ ] **Readability** — does every meaningful text block clear 4.5:1 measured contrast on the
      rendered PNG? Are identity elements at or above the 64px/56px floors? Nothing in reduced
      opacity or grey?
- [ ] Face copy within 40–45 words (100 hard ceiling)?
- [ ] Anything on the anti-voice list present? Rewrite if yes.
- [ ] Bare pronoun with no noun beside it, anywhere?
- [ ] Benefit-stacking — does the device's rows resolve to ONE takeaway, not three?
- [ ] Does the field-definition sentence appear on the face, or is it resolved by the device?
- [ ] Rule 1 — is the better job actually better, not "the same job, plus an obligation"?

If any box fails, revise before showing output.

---

## 12. THE MECHANICAL GATE — what it catches and what it can't

```bash
python preflight.py <folder-or-files>     # compliance: banned words, missing value_props
                                           # fields, dead pay buttons, missing landing pages
python simplicity.py <folder-or-files>    # volume, deficiency framing, dangling references,
                                           # alignment, measured contrast, type-size floors
```

Both must report zero blockers before anything ships. **Neither can judge Rules 1 or 2, and
neither reliably catches "too clever."** A repo-wide census found the rule built specifically for
cryptic hooks has never fired once across 171 ad faces. A clean gate means volume, legibility,
and compliance are fine — it does not mean the ad is simple enough.

### 12.5 — The blind-reader test (a required tool call, not a line you read and move past)

You cannot run this test on your own writing. You wrote the brief, so your brain fills the gap
and the fold reads fine to you — that's not carelessness, it's contamination, and it's why
cryptic ads survive to Ramanuj even from a session that had every rule in this file in front of
it. **This has to be an actual isolated read by something with no access to the brief, not a
box you tick from memory of what you just wrote.**

**This is now a script, and check_all.py gates on it.** Added 15 Sep 2026, because the
instruction below sat in 30 files and in zero checkers, which made it the last gate in the
repo running on the honour system:

```bash
python blind_reader.py --prepare <kit>     # blinded packets + priced winners as controls
# spawn ONE fresh subagent per packet_F*.txt, all in one message, prompt = the packet body
python blind_reader.py --score <kit>       # unblind, score against the control floor
```

It copies every candidate face AND three faces that demonstrably worked into `.blind/` as
`F01.png, F02.png…`, shuffled, so neither the reader nor you can tell which is under test.
**The controls go in before the read, not after a bad one** — that is Step 9's instruction
made automatic. The verdict is relative: a face is blocked only when it reads *worse than a
face that was approved or ran cheap*.

That relative floor is not a nicety. On the first real run (AcademicWriting Wave 1, 8 isolated
subagents, 15 Sep 2026) **`us05_evening` — Rs 31/lead, the second-cheapest ad in the account —
scored 2/3**, failing question 3. A fixed "3 of 3 or it is cryptic" threshold would have
blocked it. All five candidates scored 3/3 and the kit passed at a floor of 2.

`--status` is mtime-aware: re-render a face after its read and the result reads as stale,
because rebuilding after a read is the ordinary way of working, not a dodge.

**What the script does not do is the reading.** That part is unchanged and is below.

Spawn a fresh subagent (the `Agent` tool, a plain `Explore` or `general-purpose` type) with a
prompt that contains **only**:
- the literal text and device description of the first fold (what a reader would see — ICP
  band, headline, device copy, **and the field-definition box, if the chassis has one** —
  for a single-image static ad, "the first fold" is the whole rendered face, not a partial
  crop of it. Leaving out the definition box produced a false "cannot answer" on the job
  question the first time this was run for real; the definition text is what a viewer
  actually sees, so it belongs in the test)
- the three questions below
- an explicit instruction that it has no other context and must not ask for or assume any

```
Here is the first fold of an ad. You have no other context — do not guess at a product,
company, or brief beyond what's below. Answer all three questions in one line each, or
say "cannot answer" if you genuinely cannot.

[paste ICP band + headline + device copy, verbatim, nothing else]

1. Who is this addressed to?
2. What job would I be doing?
3. What will I be able to do on the last day that I cannot do today?
```

Fewer than three clean answers means cryptic, by definition, and the ad does not get shown to
the user until it's fixed and re-tested — this is a hard stop in the workflow (Step 9), the same
weight as a `preflight.py` blocker. Nine times out of ten the missing piece is the
field-definition sentence (Section 4, Rule 2 step 4). Do not substitute your own prediction of
what the subagent would say — run it. A model reading its own output back knows what it meant to
say; a fresh subagent only knows what's actually on the page, which is the entire point.

---

## 12.6 — Matching the actual creative bar, not just clearing the gate

Passing every rule in this file and the blind-reader test is necessary and **still not
sufficient**. Confirmed live: two ads cleared every mechanical check and a full blind-reader
pass using flat devices (a bare risk comparison, a generic "0 openings" line; then, one
revision later, plain quoted text in colored rectangles) and still read as template filler
next to `CorporateFinance_MediaBuyer_15-17Aug/` — 7 ads, all approved, built 13 Aug 2026. That
kit's actual bar: **a bespoke small diagram per ICP** — a cost-sheet with a variance slider, a
client-location map with a 50km dashed radius and lines out to distant markers, a document
mid-transformation into stacked value cards — never a generic swapped-icon template. Every
hero still reduces to one sentence (Section 5's rule holds), but that sentence describes a
real, literal artifact from the reader's own world, built as an honest, labelled diagram
(plain geometry — circles, bars, connector lines, callouts — never a fake app or a drawn
character, per Section 5's existing ban).

**Before calling a hero finished, check it against this bar, not just against the rules:**
could this exact diagram be swapped into a different ICP's ad by only changing the labels? If
yes, it's still a template with new words in it, not a bespoke illustration of *this* reader's
actual situation — go back to Section 5's specificity rule and design a literal artifact (a
map, a gauge, a ledger, a bar chart of their actual budget or workload) instead of reusing a
generic shape. `GOLDEN/GOLDEN.md` shows the copy-only version of this bar; the corporate
finance kit is the citation for the visual-craft version of it.

## 13. GOLDEN EXAMPLES — load these, don't just cite them

**[GOLDEN/GOLDEN.md](GOLDEN/GOLDEN.md) exists and holds 8 approved, mechanically-clean ads —
images included — spanning all three hook types with real photography, and the two device-based
types, across both product lines.** This is not optional background reading. Rules stop the
worst output; only examples change what gets written in the first place, which is the entire
reason the ads needed this many rounds of correction before this file existed. **Paste the whole
`GOLDEN.md` file into context, with its 8 images, before writing a single hook or device brief —
not a summary of it, the actual file.**

When retiring/adding to it: keep the WHY-IT-PASSED discipline, date every entry, and never
silently delete a superseded pattern — mark it superseded so the disagreement stays visible.

---

## 14. HANDOVER — state these five lines, every time

1. `preflight.py` run and result.
2. The better job each ad offers (Rule 1) — one line per ad — and your own honest read: would
   that person actually want it?
3. The sentence that defines the field on each ad (Rule 2 step 4), quoted, plus confirmation a
   context-isolated reader could name the job from it alone.
4. Confirmation you opened each landing page and the pay button carries a real URL.
5. `simplicity.py` run and result, and the blind-reader check per ad face.

If you cannot fill one in, the work is not ready to send.

---

## Where this sits relative to the rest of the repo

This file supersedes the day-to-day *process* previously split across `CLAUDE.md` and
`SOP/01`–`06` — read this one file, not those, when building an ad. `CLAUDE.md` and the SOPs
remain the underlying record (skills and tooling still cite Rule 1 / Rule 2 by name from
`CLAUDE.md`, and account routing / CPP / circuit-breaker media-buying rules live in `SOP/02` and
`SOP/03`, which this file deliberately excludes — that's post-creation media ops, not ad
creation). `docs/CONTENT_WRITING_AD_PLAYBOOK.md`, `docs/D2C_VALUEPROP_AND_ICPS_HANDOFF.md`, and
`docs/STATIC_AD_GENERATION_SYSTEM.md` are the fuller research/evidence versions this file was
distilled from — go there for more worked examples and the full reasoning, not for a rule that
contradicts what's written here.

## Two things no gate can see (added 4 Sep 2026, US Corporate Law Wave 2)

Both of these shipped through all eight gates clean, on ten faces at once.

**1. The demand clause must be grammatical with its object.** "Draft the contracts US
firms cannot staff" is not English - you staff a role, not a contract. The first repair
moved the defect one word over rather than fixing it: "register the companies US firms
**outsource**" drew *"how do you outsource a firm??"*, because outsource takes WORK as its
object and never an entity. What works is `send` for documents ("the contracts US firms
send to India") and a possessive tie to the reader's own world for entities ("the US
companies your visa clients need").

This is now mechanical: **`hook_rules.py` rule J**, blocking, 0 of 123 approved headlines,
caught 8 of 8 defective heads. It knows four object classes (entity, artefact, work, role)
and what each demand verb can take. Extend the tables when a new verb or noun shows up
rather than working around it.

**2. The field definition goes on the page, not the face.** Rule 2 step 4 is satisfied by
the landing page first fold, which lint L4 checks. On a face whose head already names the
job with a concrete verb and a nameable object, the definition sentence is a third body
block that adds length and no answer, and it reads as clutter. Pass
`extra=dict(face_definition="")`; `field_definition` stays set for the page and
`value_props.md`. If removing it makes the head unable to answer "what job would I be
doing", the head is the defect - fix the head, do not put the definition back.

**Face geometry that follows from this.** With the definition gone there is real slack, and
two `.grow` spacers at equal flex split it into two visible voids. `.grow2` (flex 0.6)
below the delivery block keeps the larger gap after the barrier line without letting it
pool. Call-out bands over about 40 characters wrap to three lines at the 64px floor; keep
them at or under it.

**And this is now mechanical too: `adkit/gaps.py`, wired into `check_all.py`.** It measures
the longest run of background rows on the rendered PNG, between the first and last row that
carry content. Ceiling 200px, fitted: no GOLDEN face pools more than 178px and no priced
face more than 151px, so it blocks 0 of 19 and blocks the 207px face that was reported.
It reads pixels rather than the DOM precisely so it can be measured on GOLDEN, which is
PNG only. Aim for the priced range, under about 150px, not for the ceiling.

## Hierarchy on the face (added 4 Sep 2026)

The Rs 82 `03_law_firm_associates` face runs **five distinct sizes**: band, head, tension
line, question paragraph, then a small barred note. A face that runs band 64 / head 66 /
barrier 56 / body 37 has three competing primaries and reads flat, which is what *"the no
law degree required can be designed better"* and *"the ad is looking too hotch potch"* are
both pointing at.

- **The barrier line is a qualifier row, not a second headline.** Uppercase, letterspaced,
  ONE line, clearly subordinate. It has its own class, `.barrier`, and its own rule, C25,
  whose floor is 30px. Do not put it in `.kicker`, which is the tension line and carries
  C8's 56px identity floor - one class doing both jobs means each inherits the other's rule.
- **The left bar is an aside device.** It needs something to be an aside FROM. With the
  definition and the tension line gone, the delivery sentence is the only body copy on the
  face, and a bar on the only paragraph is decoration. Body copy, set as body copy.
- **Spend slack on margin and on the size of the value proposition**, not on flex spacers.
  Flex pools whatever is left into one void; fixed margins absorb it as rhythm.
- **Set a chassis floor EQUAL to the checker's floor.** `floor=52` against C8's 56 let a
  54px kicker through on a face fitted at s=0.97.

## The landing page (added 4 Sep 2026)

- **The number goes beside the point, not above it.** `.day` is a two-column grid: number in
  a narrow gutter, heading on the SAME line, body under the heading and aligned to it. As a
  block div the number cost a whole line per item, on lists of ten.
- **At least one section must name the reader** — lint **L6**, which checks that some `<h2>`
  carries a content word from that ad's own ICP line. Rule 4b measures whether the pages in a
  kit DIFFER; L6 measures whether a page speaks to the person who clicked. Measured across 41
  pages in 5 kits, 7 failed it while otherwise being fully ICP-specific.
