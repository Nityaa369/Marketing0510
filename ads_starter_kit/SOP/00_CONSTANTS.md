# The constants card

**Read this first, and read nothing else until a gate fires or a judgement call needs
the reasoning behind a rule.**

Measured 31 Aug 2026: the reading `generate-ad-kit` mandated before step 0 was
**2,822 lines of prose plus 9 GOLDEN PNGs** (AD_CREATION_DIRECTOR 762, SOP/07 500,
SKILL.md 440, CLAUDE.md 434, GOLDEN.md 218, SOP/05 158, SOP/08 136, CPL_WINNERS 174) —
roughly **55,000 tokens spent before a single hook was written**, re-paid every kit and
every session. Almost all of it is *reasoning about* rules whose *content* fits on this
page. The long files stay as the record; they are where you go when a gate fires and you
need to know why the rule exists, or when you are about to change one.

**The two things this card cannot replace, and you must still do:**

1. **`python -m adkit.corpus --like "<the ICP in your own words>"`** — the ads that
   already ran for a reader like this, with their live cost per lead and their shipped
   copy. Read five before writing a hook. Doctrine is a compression of those ads.
2. **The blind-reader test** (§9), now `python blind_reader.py --prepare <kit>` then
   `--score <kit>`, gated by `check_all.py`. It is the only thing that catches cryptic,
   and you cannot run it on yourself. Priced winners are blinded into every run as
   controls, so the verdict is relative: a face is blocked only when it reads worse than
   an ad that was approved or ran cheap. Measured 15 Sep 2026 on the first real run —
   `us05_evening` at **Rs 31/lead scores 2/3**, so any fixed "3 of 3" threshold would
   have blocked the second-cheapest ad in the account.

Precedence unchanged: **the kit's own README wins**, then `CLAUDE.md`, then the SOPs.

---

## 1. Order of approval — cheapest rejection first

| # | Approve this | A rejection here costs |
|---|---|---|
| 1 | The ICP list, **ranked** — `preflight.py --shortlist <kit>` | a paragraph |
| 2 | `value_props.md` | a paragraph |
| 3 | `hooks.md`, **as a printed table** | a line of text |
| 4 | ONE ad and its landing page | one pair |
| 5 | everything else | the wave |

Section A shipped 24 pairs and 7 were rejected — about 105,000 tokens of landing page
written for nothing. Hooks settled after layout cost **14.1 rebuild cycles per creative**;
hooks settled as text first cost **6.4**.

**Step 1 is a ranked table, not a list** (4 Sep 2026). Every block carries a `pain_score`:
`severity | frequency | activation | reachability | fit`, each 1 to 5. `preflight.py
--shortlist <kit>` prints them ranked, with no ads required. A flat list makes forty ICPs
look equally worth building; ranking puts the weak cells in front of the reviewer while
striking one is still free. **Not fitted against live cost** — no scored ICP has run yet,
so it decides what to *build*, never what will convert. Preflight blocks on a malformed or
missing score, never on a total, and warns when reachability or fit is 1 or 2.

## 2. Which ICPs earn an ad (SOP/08, fitted to 128 ads, ₹2,591,070)

| Archetype | Index (1.00 = par) | Verdict |
|---|---|---|
| **B** — a life situation (career break, fifties, mother, small city, free evenings) | 0.96 | build |
| **A** — an occupation, adding a line to what they already do | 0.98 | build |
| C — an aspiration or abstract state ("freedom", "switch", own firm) | 1.05 | rewrite into A or B |
| E — a broad population ("women", "global companies") | 1.15 | rewrite |
| **D** — device-led, no ICP named (pay chart, calendar, exam date) | **1.22** | **do not build** |

Every ad above ₹280 in the corpus is C or D.

**The strongest single rule: name the discipline they already trained in.** Own-discipline
ICPs index 0.95, generic or distant ones 1.18, replicated in 4 of 4 campaigns where both
ran. Patent camp: `biomedical_devices` ₹91, `semicon_vlsi` ₹121, `agri_foodsci` ₹131 —
against `Exam window — deadline urgency` ₹203, `Exam 2027 timeline` ₹251, `Calendar motif`
₹285. **Manufactured urgency is the expensive way to sell this; a named discipline is the
cheap way.** Split an occupation at the *degree people hold*, not at the sector.

Four tests, one line each: **Identity** (would they tick this box on a form about
themselves?) · **Pressure** (why pay and show up *now*?) · **Adjacency** (do they already do
a version of this work, in their own vocabulary?) · **Ceiling** (what named thing can they
not get where they are?).

**Do not invent the situation list — read it.** [SOP/ICP_INDEX.md](ICP_INDEX.md) §2 holds
the **35 canonical life situations** this account has run, occupation stripped off, with
the pressure that makes each one buy. §2.1 shows which have never been tried on your line.

Measured 31 Aug 2026, blind test on three product lines: the method alone finds ~85% of
the live audiences on an occupation-heavy line (Independent Director) but only **~32% on a
situation-heavy one** (Women Remote). Handed the situation vocabulary, the same test went
**32% → 45%** and recovered the four biggest previously-missed converters — small city,
single mother, employed-with-free-evenings, own health. **The method generates occupations;
the index supplies the situations.** Use both.

Check `CAMPAIGN_MAP.md` for a proven relaunch before inventing an ICP —
`icp04_fifties_RELAUNCH` ₹46.21 and `indian_mom_RELAUNCH` ₹60.73 both re-ran winners.

**Never build a pay chart.** Independent Director ₹195.36 vs ₹60.42 (3.2x worse), Patent
₹380.20 vs ₹121.53 (3.1x), US Accounting ₹72.65 vs ₹29.65 (2.5x), and Academic Writing
₹230.68 against a camp par of ₹134.84 (1.71x, added 31 Aug 2026). **Four product lines, four
times.** Index 2.34 against a par of 1.00.

**A high CTR is not a good ad and must never be used to defend one.** CTR vs cost per
result across 90 ads: r = +0.17 (leads), +0.08 (purchases). Inside Senior AI it is +0.61
and Academic Writing +0.52 — higher CTR, *more* expensive.

## 2a. Screening an ICP list — the full evidence

**Screen the ICP list before anything else. This step decides the wave.** ICP choice
   moves cost per result and landing-page conversion more than format, copy or design does,
   measured over 128 ads — and in the one controlled comparison in this repo (six kits, one
   product, one fortnight) it is the *only* variable that separates the three kits that
   shipped from the three that got zero approvals: **credential-anchored ICPs, 13 of 17 in
   the rejected kits against 0 of 21 in the approved ones.** See "What actually separates an
   approved wave from a rejected one" below before you spend effort anywhere else; nothing
   downstream recovers a wrong choice here.

   Classify every candidate against the archetype table on the card (§2) and **strike
   anything that is not A or B**; then write the four tests, one line each — Identity,
   Pressure, Adjacency, Ceiling. Every ad above ₹280 in the corpus is a C or a D.

   **You are measurably good at one half of this and bad at the other.** Blind-tested on
   31 Aug 2026, three product lines, no repo access: the method alone found **~85%** of
   the live audiences on Independent Director and **~71%** on Content Writing — both
   occupation-heavy lines — but only **~32%** on Women Remote, whose live audiences are
   life situations. Generating occupations is the part that works. The four things below
   are the parts that do not, in the order they cost the most.

   - **Read the situation vocabulary. Do not invent it.**

     ```bash
     python -m adkit.icp --situations        # or SOP/ICP_INDEX.md §2
     ```

     35 canonical life situations, occupation stripped off, each with its pressure, plus
     a matrix (§2.1) of which have never been tried on your line. Handed this vocabulary,
     the same blind test went **32% → 45%** and recovered small city, single mother,
     employed-with-free-evenings and own health — three of which are among the
     best-converting segments this account has run. The situations recur across product
     lines because *a career break is a career break* whatever the destination is; the
     occupations do not.

   - **Then force three tail disciplines.** After listing the obvious occupations for the
     field, name three more from adjacent fields nobody would think of first. **The index
     cannot help you here and it was checked**: the two audiences the ID blind run missed
     were `i6_professor` and `i7_forces` (₹65/lead, near the top of that campaign), and
     both appear in the corpus on the Independent Director line and *nowhere else*. Tail
     disciplines are line-specific, so a cross-line list can never surface them. This one
     is on you.

   - **Check whether this ICP has already been rejected**, and why:

     ```bash
     python -m adkit.corpus --like "<the ICP in your own words>"
     python -m adkit.icp --rejected
     ```

     The method has **no memory** — one blind run in four proposed a practising-credential
     audience (nurses) for the women's camp, the exact idea behind 5 ads and 0 approved,
     then 3 and 0, then a kit halted at spec on 6-of-6 step-DOWN blind reads. Nothing in
     the method prevents that. Only this check does.

   - **Check `CAMPAIGN_MAP.md` for a proven relaunch before inventing an ICP.**
     `icp04_fifties_RELAUNCH` ₹46.21 and `indian_mom_RELAUNCH` ₹60.73 both re-ran winners.

   **One caveat on the archetype table.** It calls anything that is neither an occupation
   nor a situation a C and says rewrite — but `W4_not_too_late` and `W6_whatsapp_level`
   are **objection-led** ICPs ("women who think it is too late", "…who think they are not
   technical") and both shipped in the founder's own Wave 4, which gated 28 of 28 ACCEPT.
   Do not mechanically rewrite an objection-led ICP into an A or a B; you would be
   deleting a pattern that keeps passing review. See `SOP/ICP_INDEX.md` §6, including the
   honest limit that none of them carries a live cost yet.


## 2b. What actually separates an approved wave from a rejected one

Audited 31 Aug 2026. Six kits, **one product, one camp, the same fortnight** — the closest
thing to a controlled experiment in this repo. Three shipped (Waves 6, 7, 8: 21 ads, 21
pages). Three got zero approvals (`USRoles`, `HiddenMarkets`, `Verticals`).

| | rejected kits | approved kits |
|---|---|---|
| **Credential-anchored ICP** | **13 of 17 cells** | **0 of 21 cells** |
| Ad : landing page | 8→2, 3→0, 0→0 | 6:6, 5:5, 10:10 |
| Carries a constant delivery sentence | 3 of 3 kits | 3 of 3 kits |
| `value_props.md` + `hooks.md` present | **3 of 3 kits** | **0 of 3 kits** |
| Definition names concrete daily tasks | **15 of 17 (88%)** | **7 of 21 (33%)** |

**The ICP is the whole story.** Every other column either fails to separate the groups or
separates them backwards.

### Two intuitions that are wrong, and cost time every wave

1. **The spec files are not what makes an ad approvable.** `value_props.md` and `hooks.md`
   are present in *every* kit that got zero approvals and *absent* from every kit that
   shipped. They are good defect-catchers and worth writing — but producing them is not
   progress toward approval, and a kit is not closer to shipping because the paperwork is
   thorough. **Do not let spec completeness stand in for ICP judgement.**
2. **A more concrete job definition does not drive approval.** The rejected kits define the
   work far *more* specifically (88% name real duties) than the approved ones (33%). Writing
   a sharper definition fixes a real comprehension failure when the blind reader reports one
   — it did in Wave 9 — but it will not rescue a wrong ICP, and its absence did not stop 14
   approved faces from shipping on "the work US small business owners buy."

### The delivery sentence: constant frame, *varying* work object

Both groups repeat one sentence. The difference is what moves inside it. Approved kits swap
the **work object** per cell — *"the evening work they buy"* · *"the work that fits school
hours"* · *"the admin work they buy"* · *"the customer work they hand over"*. The rejected
kits held the object constant too: `Verticals` ran one byte-identical sentence across all
six cells. **Vary the object, not just the outcome clause.**

### Half the rejected kits could not have shipped at any quality

`USRoles` had 2 pages for 8 faces; `HiddenMarkets` and `Verticals` had none. Rule 4's 1:1 is
not bookkeeping — a kit without a page per ad is not a late kit, it is not a kit.

---

## 3. Rule 1 — offer a better career, never threaten

Their current work is **an asset they trade up with**, never a liability they are exposed
on. Three things get rejected every time: regulator/liability framing · more work at the
same desk · "get named the person who fixed it".

> **APPROVED:** "Your domain knowledge is the part consultants cannot buy."
> **REJECTED:** "Targeted advertising to children is banned outright."

The general form: **the ad must offer the SAME CRAFT to a better payer.** A lesser or
different craft reads as a demotion however it is worded. **Ownership beats assistance** —
"an income that is yours", "your own list", not "assistant to a US advisor".

**A practising credential cannot be the ICP for this product. Proven three ways; do not
propose it a fourth.** Keep the identity band a SITUATION. Put credential research into
targeting, Day 1 content, and the landing page instead.

## 4. Rule 2 — no assumed knowledge. Required first fold

1. **Who you are, as a question.** *"A final-year B.Com student with no finance job in sight?"*
2. **Qualifier row.** `B.COM · BBA · M.COM · FINAL YEAR · FRESHERS`
3. **The offer in plain words.** What they will be able to *do*.
4. **One sentence defining the field.** **Never skip this** — it is the missing piece in
   nine of ten cryptic rejections. *"Corporate finance is valuation, forecasting, market
   sizing and investor reporting."*
5. **Three or four named deliverables.** Concrete, not benefits.
6. **Price, dates, live-only, and a risk reversal.**

## 5. Hooks — pick ONE of six. Do not free-associate a seventh

1. **Grievance-as-headline** — the reader's exact complaint, flat declarative, 5–12 words.
2. **Reader's-own-voice speech bubble** — the caption never explains the joke.
3. **Interrogated-list / self-audit device** — max 4 rows, every row already true of them.
4. **Overheard-dialogue / interview exchange** — 3 lines max, ending on the unanswerable question.
5. **Quoted-self / "your week probably" mirror** — their actual voice, code-switching kept.
6. **Data/quadrant device** — max 4 zones; numeric axis ticks **must cite a source on the
   face**, or relabel the axis ends qualitatively.

**The universal test:** would someone scrolling half-asleep understand this in under 3
seconds without re-reading?

**Five filters after picking:** one job per hook · facts not adjectives · no decode step
(no pun, no riddle) · no throat-clearing · **name the prize, not the pain, in the biggest
element**.

**A destination noun phrase with no verb is a first-class approved shape** — "A global
legal career, from home", "A second innings in US accounting". Corrected 31 Aug 2026:
`hook_rules.py` used to block these and was rejecting 72% of the headlines Ramanuj
approved. It is now refitted on 123 of his approvals and blocks 4%.

A census of 171 faces found the mechanical anti-cryptic rule fired **zero times**, and two
headlines predicted to be rejects were both approved. **Your own read of "does this sound
clever" is not reliable.** Only the corpus and the blind-reader test catch it.

`hook_rules.py` is a **precision** tool, not a cost predictor: it flags 0 of the 13 ads
that carry both a hook and a live cost, so it says nothing about what an ad will cost.

## 6. Copy — the four moves, and the sentence you write once

```
MOVE 1  SITUATION   the reader's present tense, concrete nouns, no adjectives   ~12 words
MOVE 2  PIVOT       the asset they already have is worth more somewhere else    ~25 words
MOVE 3  DELIVERY    the constant sentence: three named things plus a horizon     ~30 words
MOVE 4  TERMS       price, format, live-only, and the negation strip            ~15 words
```

**Write the delivery sentence ONCE per kit, into `value_props.md`, before the first ad.**
It is a constant, not a creative surface: 139 of 150 approved blocks carry one, 136 name
exactly three things. Paste it into every block and change **only the outcome clause**.

> "In our free 3-day live bootcamp, **we show you** the eligibility route, the IICA
> registration steps, and **the networking plan that gets your profile in front of boards
> in 6 months**."

The three things are **assets the reader leaves holding**, never lecture titles, and the
third is always the plan. The horizon belongs to the route-selling camps (ID, IP Law, US
Accounting, USCL, Arbitration) and **not** to Women Remote, Content Writing or SQE.

| Measure | Value |
|---|---|
| Face copy | 40–45 words target, **100 hard ceiling** (counts everything on the face) |
| Primary text | **80–110 words** (150 approved blocks: median 86, 140 of 150 ≤110) |
| Headline | **4–10 words, target 7.** No approved headline of 11 words exists |

Headline names the **destination role**, never the pain. Reference build: `us05_evening`,
₹30.55 per lead, this formula with nothing added.

**Anti-voice list — never generate these.** Em-dashes · "this is not for you if…" ·
"freelancer"/"freelance", "adapt", "content marketing" as an audience label, "AI content
writer" · insider jargon (organic/inorganic, CRM, lifecycle, retention, performance
creative, funnel, ROAS, UGC) · filler (transform, discover, unlock, elevate, leverage) ·
deficiency framing ("you have never…") · salary/per-word/earnings figures on an ad face ·
an acronym without its plain-words definition in the same breath · regulator/liability/
threat framing · any placement or income promise. Every word on this list measures **zero**
occurrences across the approved corpus, so a hit means the draft is off-corpus.

**Money on the face: name the payoff, never the figure.** Not one approved face carries a
rupee or dollar figure except the ticket price. Rate tables belong on the landing page,
sourced line by line.

## 7. The hero

Default to a **device hero** (table/chart/chat/quote-box), not a photo — most approved ads
carry no photograph. **One-sentence rule:** if the hero needs "and" to describe it, split or
simplify.

**Pick from the catalogue and vary it across the wave** — `SOP/10_DESIGN_STYLES.md`, and
`python -m adkit.styles --kit <folder>` warns when 60%+ of a kit's faces are one shape.
Only two styles have a measured cost and both are worse than par: **never a pay chart**
(2.34, replicated in three product lines) and toon/chat at 1.22. Everything else has no
cost recorded, which is not the same as being safe.

**The skeleton is a field now, not a fact of the chassis.** Until 31 Aug 2026 `adkit.chassis`
emitted exactly one shape, so a wave of five ads was one template with the middle widget
swapped, however varied the copy was. Rejected on sight on the first GlobalPatent wave:
*"I don't like the designs, look through the design styles of past best performing ads and
redo the designs."* `adkit.styles --kit` had scored that kit **4 of 5 faces unclassified**,
which is the same finding by machine.

Pass `layout=` on `spec.ad(...)`. Five skeletons, each lifted from a face that was approved
and priced, listed with its source and cost by `python -m adkit.layouts`:

| layout | lifted from | live cost |
|---|---|---|
| `notice` | `us22_notice_fifties` | **Rs 29.65/lead, cheapest ad in the account** |
| `serif` | `03_law_firm_associates` | **Rs 82.00/purchase, cheapest paid ad, LawSikho** |
| `ladder` | `hoc_02_ladder` | GOLDEN, unpriced |
| `nameplate` | Ramanuj's own Academic Writing face, 29 Aug | unpriced, but his own design |
| `docket` | new | the document the reader would be paid to produce |

`spec.report()` now prints the layout per ad and **warns when every face in a wave uses one**.

Two things the redesign proved, both worth keeping:

1. **A layout that drops the deliverables costs you the third blind-reader question.** The
   `notice` and `ladder` faces first shipped without the delivery sentence, and both blind
   readers answered *"what will I be able to do on the last day"* **by inference, and said
   so unprompted**. The three faces carrying it answered from the page. `Spec` now injects
   the delivery sentence into every face, so this cannot recur.
2. **`simplicity.py` R1 catches faded type in a new layout immediately.** Four `opacity`
   declarations written for visual hierarchy blocked the kit on the first run. Use a solid
   colour; never dial type back with opacity.

## 8. The landing page (SOP/05)

**Do not redesign the spine.** All seven Corporate Finance pages are structurally identical
and convert 9.3% to 20.7%; within-kit spread is 2.1x–2.9x in every kit measured and it
tracks the **ICP**, not the page. Use `adkit.lp_spine`.

- **9 or 10 sections, 1,500–2,000 words.**
- **Two sections are counted lists** — "8 sectors creating a flood of privacy work". Counts
  real and specific, never round-number filler. This is what makes it an argument, not a brochure.
- First fold repeats the ad's promise **in the same words** (Rule 3).
- Qualify with **"You are in the right room if…"**, never "Is this for you?".
- **1 ad = 1 LP, own palette** (Rule 4).
- **The pages must actually DIFFER from each other** (Rule 4b, 31 Aug 2026). Separate
  files is not enough. The women kit that prompted this had 10 pages sharing an identical
  H2 sequence with only the H1 changed — 84% the same sentence for sentence. A reader who
  clicks two ads from one campaign lands where she has already been.
  **Keep the spine, change the argument.** `WomenRemote_Wave9` is the model at 1%: each
  page carries its own case — a walkthrough, the numbers, the stories, the demand board.
  preflight blocks at 80%.
- **The pay button carries a real funnel URL.** 153 pages in this folder ship a dead stub.
  **Never put a hedge above the CTA.** Test-buy in a real browser; curl returns false 404s.
- Benchmarks: free bootcamp ≈ **30.5%** of LP views, paid ₹10 camp ≈ **9.6%**. About 22% of
  clicks never reach the page — a deploy-pipeline loss, not a copy problem.

## 9. Before handing over — the gates and the five lines

```bash
python check_all.py <kit-folder>
```

The only command you may report a result from. Three states per gate, never two: PASS,
FINDINGS, **ERROR** — where ERROR means a gate crashed *or ran and saw zero files*.

**Zero blockers is necessary and not sufficient.** No gate reliably catches a cryptic or
over-clever hook. Open the PNG, every render, every time.

**`simplicity.py` and `hook_rules.py` were both refitted on Ramanuj's approvals, 31 Aug
2026.** Against the old in-house Section A labels they were blocking 84% and 72% of the
work he actually approved. Both are now **one-class fits**: they show a rule does not
block good work, and cannot show what they catch. **Where a rule disagrees with a face
Ramanuj approved or with an ad that ran cheaply, the face wins — fix the rule.**

**The blind-reader test, on every first fold, in a context-isolated subagent.** All five
questions, every time:

1. Who is this addressed to?
2. What job would I be doing?
3. What will I be able to do on the last day that I cannot do today?
4. **What is this ad offering you that you do not have now?**
5. **Would this feel like a step UP or a step DOWN from the career you trained for?**

**The five handover lines**, plus two added 31 Aug 2026 — the **ICP archetype of every
cell** with confirmation no cell is C, D or E, and the **delivery sentence quoted once**
with confirmation every block uses it unchanged but for the outcome clause. The original
five: preflight result · simplicity result · the better job each ad offers plus your honest
read of it · the field-definition sentence per ad quoted plus blind-reader confirmation ·
confirmation every pay button carries a real URL.

---

## 10. The ship zip — leaner than the working kit, not richer

```
<Kit>_SEND_THIS/
  README.md  ad_copy_wN.md  ads/  landing_pages/  manifest.json  kit_meta.json
```

**Those six, and nothing else.** No `html/`, `previews/`, `photos/`, `value_props.md`,
`hooks.md`, `.word-cap`, `*.py` or contact sheet — working files stay in the working
folder. Read `APPROVED/WomenRemote_Wave6/7/8_SEND_THIS/` before zipping: that is the
founder's own format and the three are consistent.

- **`manifest.json` is the deployment contract.** A kit without one cannot ship. Its
  `slug` carries **no `/f/` prefix**, though the page's line-1 comment and the README both
  write `/f/<slug>` — verify the two agree.
- **Ad stems continue one X-series across waves**, never restarting per wave: W6 `X1`–`X6`,
  W7 `X7`–`X11`, W8 `X21`–`X30`, W9 `X31`–`X36`. The page is `lp_` + the ad's exact stem.
- **A pending sign-off is a launch gate, not an approval verdict.** An approved ad still
  goes in the kit; note the sign-off in the README's launch note.

Full detail: [SOP/01_KIT_STRUCTURE.md](01_KIT_STRUCTURE.md), "The SHIP format".

---

## Where to go when this card is not enough

| You need | Read |
|---|---|
| Precedents for this exact ICP | `python -m adkit.corpus --like "..."` |
| What is live and cheap, with copy | `python -m adkit.corpus --winners` |
| Why a rule exists / this account's taste | `AD_CREATION_DIRECTOR.md` |
| Rules 1–5 as cited by name | `CLAUDE.md` |
| Sentence-level copy formula in full | `SOP/07_AD_COPY.md` |
| Which ICPs earn an ad, in full | `SOP/08_ICP_SELECTION.md` |
| LP standard in full | `SOP/05_LANDING_PAGES.md` |
| Approved faces to imitate | `GOLDEN/GOLDEN.md` — 199 faces **Ramanuj approved**, generated, with live cost. Load **2 or 3**, never the set |
| Why a specific face passed | `GOLDEN/GOLDEN_NOTES.md` — the hand-written WHY IT PASSED entries |
| Which pairs were approved or rejected | `CAMPAIGN_MAP.md` |
| Live money, by ad | `ad-analysis-shared/CPL_WINNERS_31Aug2026.md` |

---

## Recording the verdict — do this every round, not when you remember

Added 15 Sep 2026. Census that day: **538 built ads in the corpus, 7 recorded rows** in
`adkit/data/verdicts.jsonl`; 36 of 37 kits with shipped faces had recorded nothing. That
is why every checker here is a **one-class fit** — `check_all.py --brief` says it plainly:
they show a rule does not block good work, they cannot show what they catch, because there
is no set of faces Ramanuj rejected with sources in this repo.

**The back-and-forth is the missing training data.** It arrives free with every round and
was being thrown away.

```bash
python -m adkit.verdict --pending           # which kits recorded nothing
python -m adkit.verdict <kit> --review      # prefilled ad list, mark A or R
python -m adkit.verdict <kit> --apply       # record it, in his own words
```

The flag form (`--approved a,b --rejected c --why "..."`) still works and is correct. It
was used exactly once, on the day it was written, because a review arrives as prose on
WhatsApp and the flag form makes you translate it first. `--review` removes that step: it
prints the kit's ads pre-filled, you change `?` to `A` or `R` and put his sentence on the
`R` lines. **A rejection with no reason is refused** — that sentence is the whole value.
