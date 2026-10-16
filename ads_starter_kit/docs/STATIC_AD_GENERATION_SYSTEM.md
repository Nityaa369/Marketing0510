# Static Ad Generation System

Built from every instruction MD in this repo (`CLAUDE.md`, `SOP/`, `docs/CONTENT_WRITING_AD_PLAYBOOK.md`,
`docs/D2C_VALUEPROP_AND_ICPS_HANDOFF.md`, `docs/CHASSIS_AND_CHART_REVIEW.md`,
`judging-static-ads/SKILL.md`, the auto-memory feedback files) plus every ad and landing page in
`APPROVED/` — the 21 pairs actually cleared by Ramanuj (13 in `ContentWriting_Ready13_29-31Aug`,
5 in `LawSikho-Arbitration-MassHysteria-22Aug2026`, 3 in `ContentWriting_HeadOfContent_29-31Aug`).

Where the MDs and the approved ads agreed, that's a rule below with no flag. Where they disagreed
or the MDs only implied something, it's flagged **[Inferred from approved ads — verify this
matches your intent]**. This document does not override `CLAUDE.md` or the SOPs — it is the
operational layer that sits on top of them for going from brief to shippable ad.

---

## SECTION 1 — THE RULES (Anti-Patterns & Constraints)

### The six known LLM failure modes, checked against the evidence

1. **Hook as riddle.** CONFIRMED as a real risk, and the approved set is almost entirely direct.
   Every approved headline states its claim in one pass: *"They pay you for the typing."* ·
   *"Write the same ads for clients who pay more."* · *"Get past the rung where writers stall."*
   · *"One question decides who gets the job."* None require solving anything. The two
   counter-examples that were approved despite looking clever — *"Own all four"*, *"Own the
   campaign nobody owns"* — are not actually riddles: both are resolved **in the same glance** by
   an adjacent device (a four-row list, a plain "AI can write the words, it cannot decide what
   they are for" line right above). A repo-wide census of 171 ad faces found the rule written to
   catch dangling references (no antecedent on the face) **fired zero times** — cleverness is
   semantic, and it cannot be caught mechanically or predicted reliably by re-reading it yourself.
   **Rule: NEVER leave a phrase for the reader to decode. A clever line is only safe when something
   else on the same face resolves it within the same 3-second look — never rely on your own
   judgment that a line "still works," check it against the golden examples in Section 7 instead.**

2. **Overcomplicated ICP.** CONFIRMED as the single most common failure named in the MDs, and the
   approved ICP bands prove the fix: every one is a real, literal, self-recognized job title —
   *"SENIOR CONTENT WRITERS WHO WANT TO EARN MORE"* · *"WRITERS LOOKING FOR JOBS"* · *"AGENCY
   COPYWRITERS ON INDIAN RETAINERS"* · *"CONTENT CREATORS"* · *"WRITERS AIMING AT HEAD OF
   CONTENT"* · *"COURT LITIGATORS"* · *"COMPANY SECRETARIES"* · *"LITIGATION JUNIORS"*. None are
   invented psychographic segments ("ambitious creatives," "growth-minded writers"). **Rule:
   NEVER invent a demographic or psychographic label. ALWAYS use the job title the reader already
   uses about themselves.**

3. **Busy hero image.** CONFIRMED, with a finding the prompt didn't anticipate: **most approved
   ads in this account have no photograph at all.** Of the 21 approved ads, only the 5-ad MH
   (arbitration) kit uses a photographic/illustrated scene; the other 16 use a plain data or text
   device — a checklist, a 2-column table, a chat exchange, a quote box, a quadrant chart — in
   the space a "hero image" would normally occupy. Where a photo scene IS used, it is always one
   subject, one moment, one reaction — never a layered metaphor-plus-product-plus-context
   composite. See Section 4.

4. **Benefit stacking.** CONFIRMED as banned, with a nuance: a device (list/table/chart) may show
   3–4 rows, but every approved example resolves those rows to **one argument**, never to three
   or four separate reasons to buy. `cw_px_demand_board`'s four-row table ("you work out who is
   reading → targeting" etc.) is one claim — *you already do this job, it just has different
   names* — not four benefits. **Rule: a device may have multiple rows; the ad may only have one
   takeaway.**

5. **Polished/corporate tone.** CONFIRMED as the wrong register. The approved copy is plain,
   direct-address, frequently code-switched Hindi-English where that's how the ICP actually talks
   (*"Client ka budget kam hai. Revision rounds khatam nahi hote."* · *"Ghar se ho jayega na."* ·
   *"Ek reel bana do."*). `docs/CONTENT_WRITING_AD_PLAYBOOK.md` bans a specific insider-jargon
   list outright: organic/inorganic content, CRM, lifecycle, retention, performance creative,
   funnel, ROAS, UGC.

6. **Filler language.** CONFIRMED absent. "Transform," "discover," "unlock," "elevate," "leverage"
   do not appear anywhere in the ~30 approved copy blocks read for this document. **Rule: treat
   any of those five words as an automatic rewrite trigger.**

### Full NEVER / ALWAYS list

- **NEVER** use regulator, liability, or threat framing — because the single most common
  rejection in this account's whole history is exactly this (`CLAUDE.md` Rule 1).
- **NEVER** sell "more work at the same desk" or "get named the person who fixed it" — same
  rejection pattern, Rule 1.
- **ALWAYS** frame the reader's current work as an asset they trade up with, never a liability.
- **NEVER** skip the one-sentence plain-words definition of the field/role being sold — the
  single most repeated rejection word in this project's history is "cryptic," and it is missing
  9 times out of 10 (`CLAUDE.md` Rule 2).
- **ALWAYS** put that definition sentence in the first fold of the ad AND the landing page, in
  the same words.
- **NEVER** attach a checkable number to a situation ("20 articles a month") — a reader who does
  8 or 40 reads it as *not me* and scrolls. **ALWAYS** use un-checkable, generous-edged situations
  ("senior professionals," "retiring in the next 5 years").
- **NEVER** let the ICP band promise a wider audience than the line under it serves (an
  appraisal-based callout over a `CONTENT WRITERS` slab lost every client-side writer who has no
  appraisal cycle).
- **NEVER** use invented shorthand or a borrowed-industry word the reader wouldn't use about
  themselves ("PIECES RUN OUT," "BOOKED / NOT BOOKED") — use their actual vocabulary.
- **NEVER** leave a bare pronoun (*it, that, this, one, them, those*) in the payoff/headline
  with no noun beside it — eleven of twenty-two payoffs failed this in one earlier batch.
  Counting words are fine ("one person," "all four," "line one").
- **NEVER** park a statistic on its own — a number with no consequence attached reads as trivia.
  **ALWAYS** fold the fact into the payoff at payoff size with what it means for the reader in
  the same breath.
- **NEVER** repeat the same statistic across a pack — rotate one fact per ad, matched to the ICP.
- **NEVER** use salary, per-word rupee, or earnings figures on an ad face (LP-only, and even
  there labelled as market data with source and date).
- **NEVER** promise a job or placement guarantee.
- **NEVER** frame AI as a threat — it's a ladder ("AI took the production floor, which raised the
  price of the judgment that decides what gets produced"), never fear.
- **NEVER** use em-dashes anywhere in shipped copy.
- **NEVER** use a "this is not for you if…" block — qualify positively instead.
- **NEVER** exceed ~100 words on the ad face (hard ceiling); **target 40–45** for the main copy
  blocks (design target — a rejected build ran 96 words and was called out by name: *"wayy too
  much text in the ads."*).
- **NEVER** set anything the reader must read below 2.4% of canvas width, in reduced opacity, or
  in grey on a light ground — an approved ad still shipped a genuinely defective 2.8:1-contrast
  evidence line because nothing checked pixel contrast at the time. Measure contrast on the
  rendered PNG, never trust the CSS.
- **ALWAYS** run `python preflight.py` and `python simplicity.py` before calling anything ready,
  but **do not mistake a clean run for "simple enough."** The repo-wide census found the rule
  built specifically to catch cryptic hooks never fires. These tools catch volume, legibility,
  and compliance — not cleverness. Use the golden examples (Section 7) and the 3-second test
  (Section 3) for that.

---

## SECTION 2 — THE ICP DEFAULTS

The approved set spans two product families with two ICP populations, but the same shape of
person in both:

### Primary ICP — the content-writing population (SkillArbitrage camp)

**One sentence, in their language:** *A person who gets paid per word, per piece, or per project
for writing — and the rate has not moved.*

- **What they care about:** proof that the work they already do has a version that pays properly;
  a concrete next step, not inspiration.
- **Language they use:** rate, per word, per article, client, retainer, brief, budget — not
  "content marketing," "organic," "funnel," or any agency-side term.
- **Scroll-stopping trigger:** a specific, nameable moment of stagnation — the rate hasn't moved
  in three years, the appraisal came with no increment, the client cancelled a retainer for a
  tool, the notice period has started and there's no next thing decided yet. Never vague ambition
  ("wants to grow").

### Secondary ICP — the legal-practice population (LawSikho arbitration)

**One sentence:** *A lawyer, company secretary, or law student who has never run an arbitration
matter but is about to be asked to.*

- **What they care about:** being ready for a specific procedural moment (a notice arriving, a
  senior asking for a draft with no template, graduating with no practical exposure).
- **Language they use:** notice, tribunal, statement of claim, brief, matter, board.
- **Scroll-stopping trigger:** an imminent or just-happened specific event, not a general career
  goal — the notice landed on their desk, the senior asked for a draft by Monday, the client just
  mentioned an arbitration clause.

**Rule: always default to the primary ICP for a SkillArbitrage/content-writing brief unless the
product is explicitly the legal one. Do not invent a third population or a niche cross-section of
either. The pattern that generalizes to a new product: find the population's own job title, and
find the one concrete moment that is squeezing them right now — never "wants to improve."**

---

## SECTION 3 — THE HOOK SYSTEM

Five hook/device types actually got approved. Riddle-hooks and pure-curiosity-gap hooks did not
appear in the approved set at all.

### 1. Grievance-as-headline
The payoff states the reader's exact complaint, in their own words, as a flat declarative.
- *"They pay you for the typing."*
- *"Write the same ads for clients who pay more."*
- *"Get past the rung where writers stall."*

**Constraint:** 5–12 words. Must be sayable by the reader about themselves, no metaphor standing
in for the complaint. Never a compliment ("you already do the whole job" is not a pain).

### 2. Reader's-own-voice speech bubble
A line the ICP would plausibly say out loud, in a bubble over a photographic/illustrated scene,
with a flat caption underneath naming the effect — never a second joke.
- *"Sir, I will call you back. I think I will just get into arbitration instead of waiting in the
  corridor all day for matters to be called."* — caption: *"How to create mass hysteria in a
  court corridor."*

**Constraint:** first person, present tense, something a real person in that job would actually
say out loud. The caption only describes what's happening — it never explains the joke.

### 3. Interrogated-list / self-audit device
A short table or checklist mapping what the reader already does to what it's actually called or
what's still missing.
- `cw_px_demand_board`: *"You work out who is reading → Targeting. You write the value
  proposition → The offer."* (4 rows)
- `hoc_01_gap`: a checklist of 3 things "you already have" against 3 things "the job turns on."

**Constraint:** every row must be something the reader indisputably already does — no aspirational
rows. Max 4 rows, each ≤6 words per side.

### 4. Overheard-dialogue / interview exchange
A short back-and-forth (chat bubbles or quoted dialogue) landing on the question the reader can't
currently answer.
- *"Tell me about your best piece of content." / "It ranked, and it got shared a lot." / "And
  what was the ROI on it?"*

**Constraint:** 3 lines max. The final line is the gap. Never resolve it inside the bubble — the
paragraph underneath explains it once.

### 5. Quoted-self / "your week probably" mirror
A short bulleted quote box in the reader's actual voice — including code-switched language if
that's how the ICP talks — naming 2–3 recognizable frustrations, no argument yet.
- *"YOUR WEEK, PROBABLY — Client ka budget kam hai · Revision rounds khatam nahi hote · Retainer
  renew nahi hua."*

**Constraint:** use the reader's real vocabulary, not an English paraphrase of it.

### 6. Data/quadrant device
A simple chart where the reader's current bucket and the target bucket are both visible in one
face, with a one-line gloss.
- `cw_10d_senior`'s "what content work actually pays" quadrant chart.

**Constraint:** ≤4 labeled zones. **[Confirmed defect, not a style note]** — if the axes carry
numeric ticks, they must cite a source on the face. The approved money-desk chart shipped
unsourced 0–100 "percentile" ticks; `docs/CHASSIS_AND_CHART_REVIEW.md` flags this as a real
defect that slipped through, and the fix (drop the ticks, relabel the axis ends qualitatively —
"pays little" to "pays a lot") costs nothing and should be the default for any new chart hook.

### The universal hook test

> Would someone scrolling Instagram half-asleep, on the toilet, paying zero attention, understand
> this in under 3 seconds without re-reading? If no, simplify.

This is the same test the project's own docs call **the bed-and-bathroom test** — apply it to the
ICP callout first, before anything else is judged.

---

## SECTION 4 — THE HERO IMAGE BRIEF SYSTEM

**[Inferred from approved ads — verify this matches your intent]** The prompt assumes "hero
image" means a photograph. In this account's approved set, **16 of 21 ads use no photograph at
all** — the space a hero image would occupy is a data/text device instead (a table, a chart, a
chat exchange, a quote box). Only the 5-ad arbitration kit uses actual photographic/illustrated
imagery. Both patterns are approved; treat "device-only" as equally valid, not a fallback.

### What the photographic heroes actually show (literal subjects)
- A lawyer mid-sentence on a phone call in a court corridor, with a small crowd of colleagues
  reacting behind her.
- A junior advocate on the phone at a desk, colleagues in the room reacting.

One subject speaking, one small reactive crowd, one moment, one shared emotion (surprise/shock at
what's being said). Never a montage, never more than one location, never a metaphor layered on
top of the literal scene.

### The complexity ceiling
- **Photo hero:** one speaker + one reacting group, one moment, one emotion. No props beyond what
  the scene naturally contains (files, a phone, office furniture).
- **Device hero:** one table/chart/chat/list, max 4 rows or zones, one gloss line underneath.
  Never two devices stacked on one face.

### The one-sentence rule
*If you can't describe the hero (image or device) in one sentence without the word "and," it's
too complex. Simplify.*

### Template

For a photo hero: `[One subject] + [One action or state] + [One emotion/mood]`
> A court litigator + announcing on the phone that she's leaving corridor practice for
> arbitration + calm resolve, with colleagues behind her showing shock.

For a device hero (this account's more common case), the same discipline maps to:
`[One reader-recognizable device] + [One thing it maps or reveals] + [One flat gloss line]`
> A four-row "what you do → what it's called" table + mapping the reader's daily tasks onto
> campaign-strategist vocabulary + "You already own the hard half. The rest is repackaging."

---

## SECTION 5 — THE COPY SYSTEM

### Word counts
- **On-image (face) copy:** design target **40–45 words**, hard ceiling **100 words** (the
  `simplicity.py` S1 backstop, which counts everything on the face including the terms bar,
  brand row and price — treat 40–45 as the real target and 100 as the point of no return, not a
  goal to approach).
- **Primary text (off-image caption):** approved examples run roughly **100–150 words** — longer
  than the face copy is allowed to be, since it isn't fighting an image for attention the same
  way. Structure is consistent across every approved example: one paragraph naming the reader's
  situation → one paragraph naming what the offer actually is → one line stating format, price,
  and live-only.

### Sentence structure
Short, declarative, mostly one clause. Direct second-person address ("You already…", "You work
out…"). No pronoun stands in for a noun in a headline or payoff line — replace *it/that/this* with
the actual thing. Counting words are fine ("one person," "all four," "line one").

### CTA patterns
- SkillArbitrage (content writing): **"Book my seat"**, always.
- LawSikho (arbitration): **"Join for ₹200 →"**, exact wording, every cell.
- Every CTA states the full exchange (price + what it buys), never a bare "reserve my seat."

### Anti-voice list — never generate these
- Em-dashes.
- "This is not for you if…"
- "Freelancer" / "freelance," "adapt," "content marketing" as an audience label, "AI content
  writer" (the label is *AI Content Strategist* / *campaign strategist*, and it never goes in the
  ICP band — putting the destination label in the starting-identity slot collapses the ladder the
  ad is selling).
- Insider jargon: organic/inorganic content, CRM, lifecycle, retention, performance creative,
  funnel, ROAS, UGC.
- Filler words: transform, discover, unlock, elevate, leverage — none appear in any approved ad.
- Deficiency framing: "you have never…" — four of the seven Section A rejections shared this
  construction.
- Salary, per-word rupee, or "you will earn X" constructions on an ad face.
- "D2C" without its plain-words definition attached in the same breath.
- Regulator/liability/threat framing, and any placement or job guarantee.

---

## SECTION 6 — THE GENERATION WORKFLOW

```
STEP 0: SPEC FIRST — write it before any creative exists
- better_job: what different, better job is this person being offered? (one line)
- field_definition: the plain-words "X is / X means" sentence for whatever field/role
  is being sold — must survive to the ad face AND the landing page's first fold
- buying_pressure: why does THIS person pay and show up now? Name a shrinking employer, a
  frozen rate, a career break, a notice period, a ceiling — never "wants to grow"
- awareness: unaware | problem aware | solution aware | product aware | most aware
  (changes which hook type in Section 3 is appropriate — an unaware reader needs the
  field_definition first; a problem-aware reader wants their grievance named directly)
Get this one paragraph approved before building anything. A rejection here costs a
paragraph; the same rejection after the ad and landing page exist costs the whole kit.

STEP 1: BRIEF INTAKE
- What is the product/offer, price, format, dates?
- Who is the ICP? Default to Section 2's primary population unless told otherwise.
- What is the ONE message? (not two, not three)
- What is the proof point? (a stat with its consequence attached, or a named example)

STEP 2: HOOK GENERATION
- Pick ONE hook type from Section 3 based on the awareness level from Step 0 — do not
  write the hook before deciding this
- Generate up to 5 hooks in that type
- Each hook must pass the 3-second scroll test
- Check every hook against Section 1's NEVER list

STEP 3: HERO BRIEF
- Decide photo or device (Section 4) — device is the more common, equally valid default
  for this account, not a fallback
- Write the one-sentence brief using the Section 4 template
- If it needs "and," split or simplify

STEP 4: COPY DRAFT
- Face copy: 40–45 words, 100 hard ceiling
- Primary text: ~100–150 words, situation paragraph → offer paragraph → format/price line
- Apply the anti-voice list
- Check every line for a bare pronoun

STEP 5: SELF-CHECK — before showing any output
- [ ] Would someone scrolling half-asleep understand this in under 3 seconds?
- [ ] Is the hook one of the five types in Section 3, not an invented riddle?
- [ ] Does the ICP band name a real job title, not a psychographic label?
- [ ] Does the hero (image or device) reduce to one sentence with no "and"?
- [ ] Is face copy within 40–45 words (100 hard ceiling)?
- [ ] Does anything on the anti-voice list appear? If yes, rewrite.
- [ ] Is there a bare pronoun with no noun beside it?
- [ ] Am I benefit-stacking — does the device's rows resolve to ONE takeaway?
- [ ] Does the field_definition sentence from Step 0 appear on the face (or is it
      resolved by the device, per Section 3's dangling-reference exception)?
If any check fails, revise before showing output.

STEP 6: MECHANICAL GATE (this account has code for this — use it)
- python preflight.py <kit-folder>       — compliance, must be zero blockers
- python simplicity.py <kit-folder>      — volume/legibility, must be zero blockers
Neither tool can judge whether the hook is actually clever/cryptic — that's Step 2 and
the golden examples in Section 7, not a script.
```

---

## SECTION 7 — REFERENCE EXAMPLES

Five approved ads, one per hook type where possible, chosen to anchor structure and simplicity
level — not content, which changes per product.

### 1. `mh01_corridor` — reader's-own-voice speech bubble
- **Hook:** *"Sir, I will call you back. I think I will just get into arbitration instead of
  waiting in the corridor all day for matters to be called."* Type: reader's-own-voice speech
  bubble.
- **Hero image:** a litigator on the phone in a court corridor, a small crowd of colleagues behind
  her reacting with visible shock. One subject, one moment, one emotion.
- **Copy:** Callout "COURT LITIGATORS." Caption "How to create mass hysteria in a court
  corridor." Offer block: "Join our 21 day arbitration training for ₹200." Explainer: "We give
  you the 21 skills, a drafting template for every one, and the method to run an arbitration from
  notice to award, in 21 days." Terms bar: "21 DAYS · 21 SKILLS · 10 LIVE WEBINARS." CTA: "Join
  for ₹200 →."
- **ICP:** Court litigators whose commercial-dispute clients are increasingly routed to
  arbitration instead of court.
- **Why it works:** the hook is something this exact person would say out loud, in their own
  voice, with zero decoding required — the "cleverness" (the mass-hysteria framing) is only a
  caption sitting on top of a literal, plain statement, never the hook itself. This is the
  approved kit's cleanest example and scored zero findings on every mechanical check run against
  it.

### 2. `hoc_01_gap` — interrogated-list / self-audit device
- **Hook:** *"Open any Head of Content listing and read it line by line. You will find you
  already have half of it."* Headline: "Build the skills the top content job asks for." Type:
  interrogated-list device.
- **Hero image:** none — a two-part checklist in place of an image: "YOU ALREADY HAVE" (writing
  and editing, research and interviewing, managing a calendar) against "THE JOB TURNS ON THESE"
  (calculating ROI, mapping content to funnel stage, reporting ROI in finance language).
- **Copy:** Full primary text builds the half-you-have / half-you-need argument, names ROI as the
  single missing skill, states the offer (9 hours, 3 evenings, landing page + email sequence +
  tracking dashboard + results note), closes on price and format.
- **ICP:** Writers aiming at a Head of Content role.
- **Why it works:** the device does the defining — the reader sees their own daily work laid
  against the job's real requirements in one glance, so the ad never has to explain the gap in
  prose. One argument (you're halfway there) carried by four short list rows, not four separate
  benefits.

### 3. `hoc_03_question` — overheard-dialogue / interview exchange
- **Hook:** a three-line chat exchange — *"Tell me about your best piece of content." / "It
  ranked, and it got shared a lot." / "And what was the ROI on it?"* Headline: "One question
  decides who gets the job." Type: overheard-dialogue.
- **Hero image:** none — a chat-bubble mockup of the exchange itself is the entire visual.
- **Copy:** primary text names the interview moment as the actual test, states the three-evening
  offer and what's kept afterward (a results note "to open in the interview"), closes on
  price/format.
- **ICP:** Writers who want to move into running content, not just producing it.
- **Why it works:** the gap (ROI) is never explained inside the bubble — it's just the third
  question, unanswered, and the paragraph underneath is the only place it's resolved. The reader
  supplies their own dread at not having an answer; the ad doesn't have to state it.

### 4. `usmb_05_agency_copy` — quoted-self mirror + direct headline
- **Hook:** quote box "YOUR WEEK, PROBABLY" — "Client ka budget kam hai / Revision rounds khatam
  nahi hote / Retainer renew nahi hua." Headline: "Write the same ads for clients who pay more."
  Type: quoted-self mirror, paired with a grievance-as-headline payoff.
- **Hero image:** none — the quote box and the two-tone headline are the entire visual.
- **Copy:** primary text names the US-remote-hiring mechanism directly, states the offer (raise
  output with AI agents, land US clients, three evenings, ₹10), CTA "Book my seat."
- **ICP:** Agency copywriters working Indian retainers.
- **Why it works:** the quote box uses the reader's actual code-switched language rather than an
  English paraphrase, so recognition is instant; the headline states the exact trade (same work,
  better-paying clients) with no metaphor standing between the reader and the claim.

### 5. `cw_10d_senior` — data/quadrant device
- **Hook:** a 2×2 quadrant chart, "What Content Work Actually Pays" — how often clients need a
  type of work vs. what it pays, four labeled zones (Volume Work, The Money Desk, Small Jobs,
  Specialist Work). Headline: "What Content Work Actually Pays." Type: data/quadrant device.
- **Hero image:** the chart itself is the entire visual — no photograph.
- **Copy:** minimal — the chart carries the argument; a short closing line states the offer
  (build one whole campaign live, over one weekend) and price.
- **ICP:** Senior content writers who want to earn more.
- **Why it works:** the reader sees their current bucket (Volume Work) and the target bucket (The
  Money Desk) on one face with no prose needed to explain the move. **Caution when copying this
  one:** the axis ticks are unsourced 0–100 "percentile" numbers, which `docs/
  CHASSIS_AND_CHART_REVIEW.md` flags as a real defect that slipped through review — copy the
  *structure* (qualitative zones, position-encoding), not the numeric ticks. Relabel axis ends
  qualitatively instead.

---

## Where the MDs and the approved ads disagree, or the MDs risk causing the problem

- **"Own all four" / "Own the campaign nobody owns" were approved despite matching the exact
  shape ("dangling reference, no antecedent on the face") that every anti-cleverness rule in this
  repo is written to catch.** Resolution: the rule isn't wrong, it's incomplete — both lines are
  resolved by an adjacent device in the same glance. Treat "no dangling references" as the
  default, and the one exception as: only safe when something else on the same face closes the
  loop within the same look, never left to be inferred from memory of the rest of the ad.
- **The "vary composition" memory file instructs building each ad in a batch with a genuinely
  different visual skeleton and leaning into named meme formats.** This is correctly scoped to
  layout variety, not content complexity — but read carelessly it could be taken as license to
  make each ad conceptually cleverer to feel "different." It shouldn't be: vary the *skeleton*
  (device type, composition), never the amount of decoding required.
- **SOP's "borrowing from a donor format" table (gauge, magnifier, flowchart, toggle, etc.)
  requires the ICP's real situation to match the format's shape exactly, or "no amount of
  rewording rescues it."** This is a good anti-complexity discipline in principle, but it invites
  choosing a donor format *before* the plain hook is settled. Follow Section 3 first — decide the
  hook type from the awareness level — and only reach for a donor meme format if it demonstrably
  matches that hook's shape, never as the starting point.
- **No MD instruction found that explicitly tells the model to "be creative" or "think outside the
  box" without a constraint attached** — every instance of "experimentation" in the memory files
  is scoped to layout/composition variety specifically, with the content-simplicity rules held
  constant. So there's no smoking-gun instruction causing the overcomplication; the failure mode
  in the record consistently comes from the model's own untethered instinct about what reads as
  "interesting," not from any line in these files. Section 3's five hook types, chosen from what
  was actually approved, are the fix — pick from the list rather than free-associating.
