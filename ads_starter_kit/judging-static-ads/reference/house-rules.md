# House rules for static ads

These are the standing rules the vision pass applies. They come from Ramanuj's corrections on
real creatives between June and August 2026, with the date and the reason kept so you can tell
a hard ban from a preference. `engine/ad_lint.py` enforces some of them mechanically; the rest
only a reader can catch, which is why they are written down here.

Rule of thumb: a rule postdating a creative's build date is **noted, not retro-enforced**.

---

## 1. The ad formula (HARD)

**(1) Clearly call out the audience. (2) Tell them what to aspire to. (3) The rest can vary.**

7 Jul 2026 — a full 5-static kit was rejected: *"all of this sucks and will never work because
the value prop is not clear."* The kit had strong narratives but not one headline named the
aspiration. Mechanism without aspiration = no value prop.

- Kicker = who it is for. Headline = what they become or get, named explicitly and legible at
  thumbnail size. Narrative, mechanism and aesthetic are the support layer, never the headline.
- If the headline could belong to any product, rewrite before building.
- Applies at the **angle-proposal stage** too (27 Jul): every proposed angle leads with the WHO
  line; the hook moves to the headline slot.
- Prefer want/aspiration phrasing on the image over tested pain phrasing (18 Jul): "WANT to
  break into the patent industry?" beat "STRUGGLING to…". Worry is allowed on-image only when
  it pivots to qualification and action in the same breath. Never let the reader self-label as
  failing.

## 2. The four-step spine (HARD)

Every ad carries all four: **identity call-out → problem → value proposition → CTA.**
Step 2, the problem, is the one that goes missing. Order is medium-specific; presence is not
optional.

## 3. Call-out size and clarity

- **Size floor on a 1080px canvas:** kicker identity chips ≥64px (hard floor 56px, 2-line wrap
  fine); giant call-outs ≥80px (hard floor 64px). Enforced by ad_lint C8. Below ~56px reads as
  body text in feed.
- **One dominant call-out**, legible at 150–240px thumbnail width. Information-richness below
  it is good, but must never compete with or shrink it.
- **The call-out must self-identify the audience in its own words** — it may not lean on a
  small kicker or corner tag to supply the category.
- **Never cryptic.** Rejected four times, three in one session (25–26 Jul): *"omg again cryptic
  as fuck … why do you keep making cryptic ads."* Every failure was a noun-phrase fragment with
  no verb and no reader in it. Every success was a complete sentence or question that named the
  prize. "HOW TO GET YOUR FIRST BOARD SEAT" works; "ONE PREPARATION. FIVE BOARD ROLES." does not.
- **On eligibility-gated products the gate word lives IN the big call-out** (17 Jul): "SCIENCE
  POSTGRADS & PHDs", never bare "POSTGRADS & PHDs" — thumbnail readers see only the big line and
  out-of-gate clicks are targeting waste the creative created. Never bare "ALL STREAMS" on a
  gated product.

## 4. Nothing invisible, nothing cropped (HARD)

- Every element carrying meaning must be legible: labels ≥~24px bold, scroll cues ≥~30px bold,
  high contrast, not tucked in a corner blind spot. *"you write small texts in blind spots that
  is practically invisible and then think you did something."*
- **Crop-safe zone:** Meta centre-crops a 1080×1350 toward square in feed, eating the top and
  bottom ~135px. Keep everything that must be read inside y 135–1215. Decorative ink can sit
  outside; anything the buyer must read cannot.
- **Blessed exception (16 Aug):** a redundant footer strip below the CTA — dates, price recap,
  refund policy, all of which the landing page also carries — is a deliberate pattern, not a
  defect. *"i am actually fine with this — even if that gets cropped it will show in landing
  page."* Escalate only when NON-redundant must-read copy (a barrier line, a value claim) sits
  outside the crop.
- After every render, **open the PNG and look**. Never claim an element is present from the
  code alone.

## 5. Plain English (HARD)

- No poetic, clever, paradox or inversion constructions. 27 Jul: *"can you write normal easy to
  understand english and not try to be too clever or poetic."* Every line should parse on first
  read by a distracted skimmer. Prefer subject-verb-object statements of the plain fact.
- **NO EM-DASHES** in ad or LP copy. Periods, commas or colons instead. ad_lint C7 fails on any.
- Section headers too, not just body lines. When deriving from a donor file, re-read every
  header against this rule instead of trusting that the donor passed.

## 6. Promise and framing

- **Every ad and LP carries a concrete promise** (29 Jul): a we-verb commitment ("We show you
  …") naming the deliverables, a concrete outcome, and a timeframe. "9-hour live training · ₹10"
  states the product, not the outcome. Adapt the outcome per ICP; never promise a government
  post or a specific income — promise the route, the plan, the skills.
- **Never anti-promise framing** (20 Jul): no "an agenda, not a promise", "a plan, not a
  lecture", "no hype, just…". Headers state what the buyer gets or builds.
- **Never "not for you if" blocks** (19 Jul, HARD BAN): *"i hate this never do this."* No lists
  of who should not buy, on any ad or LP, any funnel. Qualify positively — "you likely qualify
  if…", persona lists, identity call-outs. The de-risking job belongs to the refund promise.
- **Never coach distress.** Positive capability framing only.
- **Value prop per ICP outcome** — never one-size across a kit.

## 7. Numbers on ads (HARD)

Never put a **viewer-describing** figure on an ad: earnings ("₹40,000/month"), experience
duration ("18 years"), a hard single age, or price anchors and MRP ("₹14,999", "99% OFF"). The
worst form is a giant hero number as the focal point. *"this disqualifies people and KILLS AD
PERFORMANCE."*

Replace the number with an identity or emotional hero phrase: "18 years running a home" becomes
"You ran a home."

**Allowed on ads** (these describe the OFFER, not the viewer): program duration ("21 days"),
the entry price ("₹10"), program structure ("Week 1", "Day 21"), a count of steps. Market-fact
stats (market size, shortage) are fine — they are not the viewer's earnings or experience.
Income ladders stay on the landing page.

## 8. The four campaign pieces (HARD, 20 Aug 2026)

A campaign strategist owns: **the ad · the page · the warm up · the tracking.**

Piece 3 is **the warm up** — the email warm up campaign, retargeting campaigns, and warm up
assets such as ebooks and blog posts. *"dont say the emails - say the warm up."* "The emails"
names one channel and undersells the piece. Use the phrase in ads, LPs, anchor text and section
copy.

## 9. Brand, cast and palette

- **Brand by product line**, not by ad account: SkillArbitrage for HR, US accounting and the
  skilling products; LawSikho for USCL, litigation, the lawyer camps, CA Bar / SQE, judiciary.
- **Every human in a creative is an Indian person** (4 Aug, HARD). Non-Indian faces break
  self-identification, which is the whole mechanism. Applies to generated images, stock, and
  illustrations, including watermarked placeholders.
- **Default to light backgrounds.** Matched-pair data across 4 products: dark statics cost
  10–41% more per acquisition, and Meta's optimizer starves them of budget. At most one dark
  cell per kit, labelled as the test cell.
- **Vary the aesthetic across a kit.** One aesthetic × N headlines is a rejection, not a kit.
  Offer anchors (price, dates, brand) stay constant; distinct ICPs get distinct looks.

## 10. Audience and topic bans (HARD)

- **Never target freelancers**, any product. *"this audience does not convert - always remember
  to exclude them."* Cheap front-end volume, junk downstream. (Content writers "niching up" is a
  distinct, approved idea — the ban is the generic freelancer identity.)
- **No labour-law / POSH HR ads** — reads as Labour Law and costs ~10×.
- **Banned proof names** — check the product's proof-asset file before putting a person's name
  or a customer quote on a creative.
- **Persona cards by situation, not job title.** Title lists disqualify.

## 11. Outcomes and proof

- **Outcomes at bootcamp exit** (HARD): promise what they walk out with, never a six-month
  future state.
- **Name the judgment, not the database** — the skill at each step; tools are demoted.
- **Brand-name companies in proof** (HARD) where proof is used at all.
- **Abundance framing for exam products** — scarcity backfires.

---

## What this file is not

It is not the backtested mechanical rulebook — that is `gate-rules.md`, which carries fire
rates against a 1,373-creative archive and the discipline for adding new blocking rules. This
file is the judgement layer. When the two disagree, the mechanical gate is a floor and the
house rule decides.
