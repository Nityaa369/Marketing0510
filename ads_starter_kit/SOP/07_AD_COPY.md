# SOP 07 — Ad copy: the sentence-level formula

**Read this before writing a single line of ad copy.** `AD_CREATION_DIRECTOR.md` settles what
the ad is *about* — the ICP, the hook type, the device, the value proposition. This file settles
how the sentences are actually built, because that is where the copy has kept missing.

Every rule below is fitted against the **`APPROVED/` corpus: 150 approved copy blocks across
16 kits** (Independent Director, US Accounting, US Corporate Law, IP Law, SQE, Content Writing,
Women Remote Work, Arbitration), plus **21 approved ad faces** read from their source HTML and
6 read from the rendered PNGs. Counts in brackets are measured, not estimated. Re-run
`python SOP/tools/copy_census.py` to re-measure after the next approval batch, and

```
python SOP/tools/copy_census.py APPROVED <your-kit-folder>
```

to score a kit you are about to build against the baseline, one row each. **Run it on
`ad_copy.md` before any face is rendered** — every deviation below costs a paragraph to fix at
that point and a kit to fix after.

The one-line summary: **approved copy is not written, it is filled in.** Read §0 first for
what this buys you and what it does not. The corpus is far more
formulaic than the drafts we keep producing. Most of what reads as "not up to the mark" is a
writer being creative in the four slots that are supposed to be constant, and lazy in the one
slot that is supposed to carry all the work.

---

## 0. WHAT IS VALIDATED, AND WHAT IS NOT — read this before treating anything here as a gate

Refitted 28 Sep 2026. `python SOP/tools/copy_census.py --selftest` re-runs it.

**The basis is copy Ramanuj approved, not Section A.** This section was first fitted (31 Aug)
against the Section A split, 13 "approved" and 7 rejected. Those labels were in-house and the
pairs never shipped, so `hook_rules.py` and `simplicity.py` were refitted away from them the
same day. The selftest now uses their basis: the **146 copy blocks in GOLDEN** that Ramanuj
approved or wrote. It measures how often each rule fires on approved work. There is no labelled
set of copy he rejected, so what a rule *catches* is not measured.

| Rule | Fires on Ramanuj-approved copy | Use |
|---|---|---|
| headline > 10 words | 0/146 (0%) | may gate |
| bare pronoun in headline | 2/146 (1.4%) | may gate |
| headline title-case | 6/146 (4.1%) | may gate |
| opening sentence > 25 words | 6/146 (4.1%) | may gate |
| primary text > 110 words | 10/146 (6.8%) | may gate, with a human read |
| no delivery sentence | 11/146 (7.5%) | may gate, with a human read |
| delivery names < 3 things | 14/146 (9.6%) | may gate, with a human read |
| no plan / method / route | 26/146 (17.8%) | **style only, never a gate** |
| no horizon ("in 6 months") | 46/146 (31.5%) | **style only, never a gate** |
| no negation strip | 90/146 (61.6%) | **style only, never a gate** |

"May gate" means the rule rarely fires on work he approved. It does not mean the rule predicts
a rejection: nothing here has been shown to. On the old Section A split only *bare pronoun in
headline* separated the groups cleanly (2/7 caught, 0/13 false alarms); the selftest still
prints that split for reference.

**So: this file is a style guide fitted to approved output. It is not a rejection predictor.**

- **Use it to draft.** Filling the slots gets you copy that looks like the approved corpus, in
  one pass instead of five. That is its real value and it is a large one.
- **Gate only on the low-noise rules, and read the copy when one fires.** Ten percent of
  approved work breaks the noisiest of them.
- **Horizon, plan and negation strip are constants of the route-selling product lines** (ID, IP
  Law, US Accounting, USCL, Arbitration) and absent elsewhere. Outside their line they fire on
  approved work, so they produce false alarms, not quality.
- **What still decides whether copy is good** is `CLAUDE.md` Rules 1–5 and the blind-reader test
  in `AD_CREATION_DIRECTOR.md` §12.5. Nothing measured here replaces either.

### Known limits of the evidence

1. **No labelled rejections.** The fit above is precision on 146 approved blocks. A set of copy
   Ramanuj actually rejected, with the blocks, would be worth more than any further work on this
   file: it is the only way to measure what a rule catches.
2. **"Unapproved" is not "rejected for copy."** The kits in the comparison table died for
   different reasons: `WomenRemote_Verticals` / `USRoles` / `HiddenMarkets` were killed at the
   **ICP** stage (a practising credential cannot be the ICP), and
   `IndependentDirector_Wave1` says "Nothing here is built" — it was never submitted. Their
   deviations from the corpus are suggestive, not verdicts.
3. **Performance data is now joined in — partly.** See §9 and
   [ad-analysis-shared/CPL_WINNERS_31Aug2026.md](../ad-analysis-shared/CPL_WINNERS_31Aug2026.md)
   (90 ads, ₹4.28M spend, pulled 31 Aug 2026). The four cheapest lead ads in the account are
   textbook four-movers, which is the first evidence tying this file to money rather than to
   approval. It is four ads in one product line with the format confounded, so it supports the
   pattern; it does not license using this file as a gate.
4. **Face coverage is thin.** The 10-slot face order in §3 is generalised from 21 near-identical
   source files in one kit plus 6 rendered PNGs, against 400+ PNGs in `APPROVED/`.
5. **Duplicate inflation was checked and is small.** 150 blocks contain 129 unique primary texts
   (the three Independent Director kits share one delivery sentence 19 times). Deduplicated, the
   numbers barely move: median 86 → 88 words, delivery 92% → 91%, headline max 10 unchanged. The
   descriptive stats are robust; it is the *diagnostic* claim that is weak, not the measurement.

---

## 0.1 The two errors that account for most off-corpus copy

1. **Reinventing the delivery sentence.** 92% of approved blocks carry one, 97% of those are
   the same sentence shape, and inside a kit it is very nearly byte-identical. It is not a creative surface.
   Writing a fresh one per ad is the single most common way approved-looking copy goes wrong.
2. **Writing long.** Approved primary text has a **median of 86 words**. Drafts routinely run
   140–160 because `AD_CREATION_DIRECTOR.md` §7 said "100–150 words" — a figure the corpus does
   not support and which is corrected here. 93% of approved blocks are ≤110 words.

---

## 1. THE FOUR-MOVE PRIMARY TEXT

Every approved primary text is the same four moves in the same order. Median 6 sentences,
80–100 words. Write the moves in order; do not blend them.

```
MOVE 1  SITUATION    The reader's present tense, in concrete nouns.        ~12 words
MOVE 2  PIVOT        The same asset, valued somewhere else.                ~25 words
MOVE 3  DELIVERY     The constant sentence. Three named things + horizon.  ~30 words
MOVE 4  TERMS        Price, format, live-only, eligibility removed.        ~15 words
```

### Move 1 — Situation

One or two sentences. Present tense, second person, concrete nouns, **zero adjectives**.
It states what is true of this reader today, in a way they would not dispute.

> "You reach court by ten. The board moves, the other side asks for a date, and by one o'clock
> you are outside with a fresh date two months away."

> "The whole colony negotiates your tuition fee."

> "You raise the bills, chase the suppliers, keep the stock list true and answer every customer.
> The family shop runs because you run it, and nobody pays you for it."

Median opening sentence: **12 words** (p90 = 22). If the first sentence is over 25 words, the
ad opens slow and nothing downstream recovers it.

**Never** open on the company, the course, the industry, or a trend. 37% open literally on
"You"/"Your"/"If you"; the rest open on the reader's situation stated in the third person
(*"The last bell can end the earning day"*, *"Retirement is when independent directors get
appointed"*). None open on us.

### Move 2 — Pivot

The engine of the whole ad. It says: **the thing you already have is worth more somewhere
else.** It is never "here is what you lack."

Three approved pivot shapes, in order of frequency:

| Shape | Skeleton | Example |
|---|---|---|
| **Same asset, better payer** | *X is what Y is short of / pays for* | "US small business owners pay for finished work, and the income carries your name." |
| **Same skill, new name** | *What you do is called Z over there* | "On a campaign brief those four things have different names: targeting, the offer, the hook and the close." |
| **Same side, other side of the table** | *You do A; the seat does A with B attached* | "You already draft the resolutions, brief the directors and flag the risks. The independent director's seat uses the same skills, with a vote attached." |

The `"you already"` stem appears verbatim in 13% of blocks and is the corpus's clearest tell of
a correct pivot. If you cannot write the pivot without telling the reader something is wrong
with them, the ICP or the angle is wrong — go back, do not push through. (This is Rule 1 made
into a sentence.)

### Move 3 — The delivery sentence · **THE CONSTANT**

**92% of approved blocks carry one (139/150). 97% of those name exactly three things (136/139).**

```
[WHEN/FORMAT], we show you [THING 1], [THING 2], and [THE PLAN THAT <OUTCOME>], in [HORIZON].
```

- **Verb: `we show you`** — 117/150. `we teach you` 13/150. `we give you` / `we check` for
  programme formats. Nothing else appears.
- **Exactly three things.** 136/139 (97%). Not two, not four, not a list.
- **The third thing is always the plan.** "the plan" 73/150 — and where the literal word is
  absent it is "the method", "the application plan", "the setup plan", "your first client plan",
  "the route". The first two are knowledge; the third is the bridge to money.
- **A horizon — in route-selling camps.** "in 6 months" 99/150 overall, but read this per
  product line, not as a blanket rule: it runs **92–100% in the camps that sell a route to a
  first client or a first seat** (Independent Director, IP Law, US Accounting, US Corporate Law,
  Arbitration, which used "in 21 days") and **0% in Women Remote, Content Writing and SQE**,
  which promise a plan without a clock ("the plan to reach your first client"). Match the
  product line you are building for. Never open-ended, never "overnight".
- **The outcome clause is the only part that changes per ICP.** Everything else in the sentence
  is fixed for the whole kit.

Worked, from `IPLaw_GrowthCamp_WinnerRefresh` — 21 approved ads, one sentence:

> "We show you the work, the skills and the plan that **lands your first assignment from a US
> or UK law firm**, in 6 months."
> "We show you the work, the skills and the plan that **restarts your legal career from home**,
> in 6 months."
> "We show you the work, the skills and the plan that **builds you work that fits school
> hours**, in 6 months."

From `ID_FreeBootcamp` — 7 ads, byte-identical delivery sentence, zero variation:

> "In our free 3-day live bootcamp (12 to 14 Sep), we show you the eligibility route, the IICA
> registration steps, and the networking plan that gets your profile in front of boards in 6
> months."

**Write this sentence once per kit, in `value_props.md`, before the first ad.** Then paste it
into every block and change only the outcome clause. If you find yourself writing a different
delivery sentence for ad 7 than for ad 1, you have made an error, not a variation.

### The worked failure — `IndependentDirector_Wave1_MediaBuyer_12-14Sep`, 27 Aug 2026

Same product, same camp, same dates as three kits that **were** approved. Censused 31 Aug:

| | approved ID kits | Wave 1, unapproved |
|---|---|---|
| delivery sentence present | 88–100% | **0 of 10** |
| names the plan | 100% | 10% |
| carries a horizon | 100% | **0%** |
| primary text, median words | 72–74 | **104** |

Its delivery block reads:

> "The free bootcamp **is** 9 hours live over three days: what a board actually expects, the
> IICA databank and its open-book exam, and how appointments really happen."

Its approved sibling reads:

> "In our free 3-day live bootcamp, **we show you** the eligibility route, the IICA registration
> steps, and **the networking plan that gets your profile in front of boards in 6 months**."

Three defects, all in one sentence:

1. **The subject is the product, not us acting for the reader.** "The bootcamp *is* 9 hours"
   describes a thing for sale. "We show you" performs a service. Every approved kit does the
   second.
2. **The three things are lecture titles, not assets.** "What a board expects / the databank /
   how appointments happen" is a syllabus. "The eligibility route / the registration steps / the
   networking plan" is what the reader leaves holding.
3. **The third slot is not a plan and has no outcome.** The sentence stops at curriculum and
   never reaches what the reader can do afterwards.

The kit's own blind-reader test had already caught the symptom — two of four readers answered
"cannot answer" to *what will I be able to do on the last day* — and the fix applied was a
promise block bolted onto the **face**. The defect was in the **sentence**, and it stayed.

### Move 4 — Terms

Price (96/150 state it), format, live-only, and the **negation strip**.

The negation strip removes the reasons this reader will say "not for me." Always parallel,
always 3–4, always the shortest sentences on the page. It appears in 37% of primary texts and
on nearly every ad face.

> "No visa. No relocation. No LL.M. No bar exam."
> "No CA, no CPA, no office."
> "No coding. No paid tools. No experience needed."
> "No experience needed. If you can use WhatsApp, you can do this."

Pick the objections this specific ICP actually holds. A career-break ICP gets "the gap does not
count"; a small-city ICP gets "no relocation"; a non-CA gets "no CA, no CPA."

---

## 2. THE HEADLINE — measured limits

Across 150 approved headlines: **min 4 words, median 7, max 10.** There is no approved headline
of 11 words. Treat 10 as a hard ceiling and 7 as the target.

**It names the destination, not the pain.** The pain lives in Move 1 of the primary text and in
the ICP band on the face. The headline is where the reader sees the new job.

Of the 150, the opening word is `Your` (14), `The` (11), `Become` (9), `Add` (9), `Start` (6),
`Get` (5), `Learn` (4), `Work` / `Restart` / `Move into` / `Do`. Note what dominates: verbs of
*relocation into a new role*, and possessives that hand the reader an asset.

Six approved headline shapes:

| Shape | Approved examples |
|---|---|
| **Become the ___** | "Become a remote IP paralegal" · "Become the accountant US firms want" · "Become the strategist who owns the campaign" |
| **Your ___ [is wanted / belongs / still pays]** | "Your experience belongs on a board" · "Your CA-firm experience pays in dollars" · "Your guest skills still pay, from home" |
| **Add a ___ to your ___** | "Add a US tax desk to your CA practice" · "Add a second income after the last bell" |
| **The ___ that ___** (the named prize) | "The desk with no seniors" · "The restart that does not ask about the gap" · "The profile GCC legal teams hire for" |
| **They / it does not ___** (objection killed) | "They never ask which city you live in" · "US clients check the books, not the gap" |
| **A vs B, stated flat** | "Get paid for outcomes, not word counts" · "QuickBooks pays more than Tally" · "Same skills. Better hours. Better pay." |

Run the §3.5 headline subject test from `AD_CREATION_DIRECTOR.md` on every one: the grammatical
subject must move to a new destination role, not stay the current job with a clause bolted on.

---

## 3. THE AD FACE — the slot order that got approved

Read off 21 source files. Two chassis, one slot order. Only slots 2, 3, 4 and the outcome
clause of 6 change between ads in a kit. Everything else is fixed.

```
1  BRAND ROW      LawSikho · IP Law Growth Camp          [constant]
2  ICP BAND       WOMEN LAWYERS ON A CAREER BREAK        [varies — all caps, first thing read]
3  HOOK A         Your law degree didn't expire.         [varies — statement, or the doubt as a question]
4  HOOK B         You can restart your career from home. [varies — the turn, italic/colour, ≤7 words]
5  FIELD LINE     IP paralegal work, assisting US and UK law firms. Paid in dollars.  [near-constant]
6  DELIVERY       We show you the work, the skills and the plan that restarts your
                  legal career from home, in 6 months.   [constant but the outcome clause]
7  NEGATION       No visa. No relocation. No LL.M. No bar exam.  [constant]
8  CTA            Reserve my seat · ₹10 gets you all 3 days, live.  [constant]
9  LOGISTICS      3 DAYS LIVE, ONLINE · 26 TO 28 SEPTEMBER · 6 TO 9 PM  [constant]
10 CREDIBILITY    By LawSikho · NSE Emerge-listed · Recognised NSDC Training Partner  [constant]
```

### The two-part hook (slots 3 + 4)

Always two lines, and the second answers the first. The first is the reader's doubt; the second
resolves it in five words or fewer. Never one long line, never three.

| Hook A (the doubt) | Hook B (the turn) |
|---|---|
| "Legal work that fits school hours?" | "It exists. It is remote." |
| "Feeling stuck where you are?" | "There is a remote route up." |
| "The best paid work from home for lawyers?" | "Remote IP paralegal work" |
| "Your law degree didn't expire." | "You can restart your career from home." |
| "Your degree still counts." | "Start in global IP law." |

On the notice/serif chassis the same two parts appear as **roman statement, then italic turn**:

> "Accountants on a career break who have already been asked about the gap are requested to
> show US clients the books. *US clients check the books, not the gap.*"

### The field-definition line (slot 5) is not optional

This is Rule 2, step 4, and it is present on every single approved face. It says in ordinary
words what the job is and who pays.

> "Assist US and UK law firms on trademark, patent and copyright matters. From home, on your
> terms, paid in dollars."

If a stranger cannot name the job from this line alone, the ad is cryptic regardless of how good
the hook is.

---

## 4. THE COMPARISON DEVICE — row grammar

The comparison table is the account's most-used device. Its rows are copy, and they follow rules.

- **Two columns, one axis.** Name the axis in the title: *"Differences between Unpaid work &
  Paid work"*. Never a third column.
- **5 rows maximum**, 3–4 preferred.
- **Every row parallel.** Same grammatical shape left and right, same length, so the eye reads
  the swap and not the sentence.
- **Every left-hand row is indisputably true of the reader today.** No aspirational rows on the
  left, nothing they would argue with.
- **Every right-hand row is a concrete, nameable deliverable** — "Invoices and payment reminders,
  paid work", not "financial freedom".
- **The last row is the identity payoff.** Not money — what they get *called*.

> 5. "Called just a homemaker."  →  "Called a professional again."

That final row is the reason the device works. If the table ends on a task, it has no ending.

The self-audit variant uses ticks against a job listing, with **two ticks and one open circle** —
you already have two of three, and the camp closes the one gap:

> ✓ Own the campaign, not just the copy — *You already plan a piece end to end*
> ✓ Know the audience and make them act — *You do both in everything you write*
> ○ Read the numbers and say what to change — *This is the one gap. Three evenings.*

---

## 5. FACTS AND NUMBERS

**Only 24% of approved blocks carry a statistic at all.** A stat is a device for one ad in four,
not a default opener. Copy that reaches for a number every time is off-pattern.

When a number is used:

- **It is sourced on the face.** "Source: The Law Society" · "Semrush study of 8,000 marketing
  job listings, Feb 2026" · "UK Immigration Rules · in force since 22 July 2025".
- **Its consequence is attached in the same breath.** "Down by 1,771 since 2017, a 32 percent
  drop" is followed immediately by "Police are releasing suspects because interviews cannot go
  ahead without one." A bare number is not a benefit.
- **One distinct fact per ad, never repeated across a pack.** Grep the pack before shipping.
- **It proves scale, not demand.** A big number must not be allowed to imply hiring volume it
  does not support.

Salary ladders, per-word rupee figures and earnings numbers stay off the ad face entirely —
LP only, labelled as market data.

---

## 6. VOICE

### Code-switching

Hindi/Hinglish is used only as **the reader's own quoted voice**, always as the opening line,
never translated, never in our voice.

> "Client ka budget kam hai. Revisions khatam nahi hote."
> "Ghar se ho jayega na. Pocket money to mil hi jayega."
> "Ek reel bana do. Aaj kuch post nahi hua?"

Never write our offer, our field line or our CTA in Hinglish.

### The banned list is empirically clean

Across all 150 approved blocks, these appear **zero times**: *transform · unlock · discover ·
elevate · leverage · empower · journey · dive into · game-changing · revolutionary · seamless ·
cutting-edge · freelance/freelancer · skyrocket · unleash · harness · navigate · landscape ·
ever-evolving · "in today's…"*. Also zero em-dashes in any approved copy block.

That is not a style preference we imposed; it is what the approved corpus measures. If a draft
contains one of these words, it is off-corpus.

### Sentence discipline

- Median sentence: **10 words**. p90: 30. Mostly one clause.
- No bare pronoun (*it, that, this, one, them*) standing in for a noun in a headline or payoff.
- Direct second person throughout.
- No throat-clearing, no rhetorical wind-up, no "have you ever wondered".

---

## 7. THE DESCRIPTION FIELD IS LOGISTICS, NOT COPY

Median 13 words, max 23. Within a kit it is near-identical across every ad. Two approved shapes:

- **Pure logistics** (most kits): *"Live 3 day US Corporate Law camp by LawSikho. 19 to 21
  September, Rs 10. Notes, templates, WhatsApp group and certificate included."*
- **Four-word differentiator, then logistics** (Women Remote, Content Writing): *"Dollar rates,
  not lane rates. ₹10 for 3 days."* · *"Hired on skill, not resume. ₹10 for 3 days."*

Do not put the ad's argument here. It is read after the decision, not before it.

---

## 8. THE COPY CHECK — run before the face is designed

Per ad, answer in one line each. **These are drafting checks, not a gate** — see §0. A "no"
means the copy is off the approved house pattern and you should have a reason, not that it
would be rejected.

1. Is the headline **≤10 words** and does it name the destination role, not the pain?
2. Is the primary text **80–110 words**, in the four moves, in order?
3. Is the delivery sentence **identical to the rest of the kit** except its outcome clause, and
   does it name **exactly three things** and a **horizon**?
4. Does Move 2 say *the thing you already have is worth more elsewhere* — with no sentence
   anywhere saying something is wrong with the reader? (Rule 1)
5. Is the **field-definition line** on the face, in ordinary words? (Rule 2, step 4)
6. Is there a **negation strip** of 3–4 parallel objections this ICP actually holds?
7. If a table: 5 rows or fewer, all parallel, every left row indisputably true today, last row
   the identity payoff?
8. If a number: sourced on the face, consequence attached, unique in the pack?
9. Zero banned words, zero em-dashes, zero bare pronouns in the headline?
10. Is the description a logistics line under 23 words?

Then run the blind-reader check from `AD_CREATION_DIRECTOR.md` §12.5 — the mechanical list above
cannot see "cryptic", and never could.

---

---

## 9. WHAT THE MONEY SAYS — CPL pull, 31 Aug 2026

Full tables and method: [ad-analysis-shared/CPL_WINNERS_31Aug2026.md](../ad-analysis-shared/CPL_WINNERS_31Aug2026.md).
90 ads, ₹4,275,135 spend, Skill Arbitrage account, ad level, last 30 and 90 days.

**Free camps report cost per lead, paid camps cost per purchase. Never put them in one column.**
Meta reports spend net of GST; gross up 18% before judging against `SOP/02`.

### Stop building pay charts

Replicated across three campaigns and three product lines, each against the best ad in its own
campaign: Independent Director ₹195.36 vs ₹60.42 (**3.2× worse**), Patent ₹380.20 vs ₹121.53
(**3.1×**), US Accounting ₹72.65 vs ₹29.65 (**2.5×**). Normalised, the pay chart indexes **2.34**
against a campaign par of 1.00; every other format sits between 0.64 and 1.22. A pay chart makes
a salary figure the hero, which `CLAUDE.md` already bans from the face on compliance grounds.
Performance and compliance agree here.

### A high CTR is not a good ad

CTR vs cost per result across all 90 ads: **r = +0.17 (leads), +0.08 (purchases)**. Inside Senior
AI it is **+0.61** and inside Academic Writing **+0.52** — higher CTR, *more* expensive. The
highest-CTR ad in the account (`SeniorICP|Toon|st02_canteen`, 4.12%) costs ₹234.71, worse than its
campaign median; `cf_cma` at 0.61% CTR costs ₹170.17.

Keep the three-second comprehension test in `AD_CREATION_DIRECTOR.md` §4 — it is about being
understood. But **never defend an ad on the grounds that it got clicks**, and treat toon/chat
formats as attention that has not yet been shown to convert.

### Name the ICP; do not manufacture urgency

Inside one Patent camp: `icp_27_semicon_vlsi` ₹120.68, `icp_18_agri_foodsci` ₹131.49,
`icp_26_ayurveda_bams` ₹135.30 — against `Exam window — deadline urgency` ₹203.28,
`Exam 2027 timeline` ₹250.89, `Calendar motif` ₹284.95. **1.5× to 2.4×.** The same holds in Data
Privacy, where the three cheapest ads in the entire paid corpus all name an existing practice and
offer to add a line to it (₹81.90, ₹97.69, ₹97.91).

### Destination in the headline, pressure in the body

Data Privacy is the cheapest paid camp in the account (₹122.02) and is also the line that produced
four Rule 1 rejections. Its shipped body copy still names regulatory pressure; what changed after
those rejections is the **headline**, now pure destination: *"Add data privacy. Grow faster."*
For a regulation-driven product that is the working shape — never pressure in the biggest element.

### The reference build

`us05_evening`, ₹30.55 per lead, second-cheapest ad in the account, is this file's §1 with nothing
added: 6-word destination headline, 77 words, situation → pivot → three-thing delivery sentence
with a plan → negation strip. Read it before writing a camp's first block.

## Precedence

The kit README wins, then `CLAUDE.md` Rules 1–5, then `AD_CREATION_DIRECTOR.md`, then this file.
Where `AD_CREATION_DIRECTOR.md` §7 gives a primary-text length of 100–150 words, **this file
supersedes it** — that figure was never fitted against the approved corpus and the corpus
measures 80–110.

One known exception on record: the Academic Writing GrowthCamp face *"Your research experience
can lead to paid work — in dollars"* shipped with an em-dash and was approved. It is logged as an
exception, not a licence. Do not widen the rule on the strength of one face.