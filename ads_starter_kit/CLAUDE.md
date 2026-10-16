# Ad and landing page generation — LawSikho / SkillArbitrage

**For the ad/LP creation process, read [AD_CREATION_DIRECTOR.md](AD_CREATION_DIRECTOR.md)
first — it is the sole director for building a static ad + landing page pair, and it folds
in everything below plus the SOPs and the earned playbooks.** This file remains the source
of record for Rule 1 / Rule 2 (cited by name elsewhere in the repo) and for the mechanical
check; nothing here contradicts the director file. Media-buying/account/CPP rules stay in
`SOP/02` and `SOP/03`, which the director file does not cover.

**This is a supplement, not a replacement.** It does not change how a kit is put together
— folder structure, the ad-copy file, the per-drop README with its launch spec, account
routing, ABO/CBO rules, circuit breakers, GrowthX slugs. Keep doing all of that exactly as
before, per whatever that drop's README specifies. This file adds two things on top: the
two judgment calls that account for nearly every rejection, and a mechanical check to run
before anything is sent. Nothing here overrides a kit README — if one sets a stricter or
different rule, the kit README wins.

This exists so the work is right the first time, and Ramanuj does not have to explain the
same two rejections again.

**Read this before generating anything. Run the check before handing anything back.**

## Where the rest of it lives

- **[RAMANUJ_FEEDBACK.md](RAMANUJ_FEEDBACK.md)** - every piece of feedback and every verdict
  Ramanuj has given, in his own words, by theme, with a kit-by-kit ledger. Merged 28 Sep 2026.
  New feedback from him goes there, not into a new file.
- **[SOP/00_CONSTANTS.md](SOP/00_CONSTANTS.md)** - the constants card, added 31 Aug 2026.
  Every rule that changes a decision, on one page. Read it instead of the 2,822 lines the
  skill used to mandate; come back to the long files when a gate fires or you are changing
  a rule.
- **`python -m adkit.brief "<the ICP in your own words>"`** - START HERE, before writing
  anything. Past performance for this reader, the nearest precedents with their live cost,
  the rejections nearest them, and the order of work. One command instead of reading the
  MDs. `--worked` lists every ICP that has a live cost (20 of 538 built ads; the rest were
  never measured and did not fail). `--styles` lists the design styles that have run.
  `python -m adkit.corpus --like "..."` is the lower-level view underneath it.
- **`python -m adkit.restyle <kit> --list`** - the 11 layouts, each with the real face it
  came from and that face's cost, which is the map from "make it look like this one" to a
  layout name. `--ad <name> --to <layout>` re-skins one face, proves the selling copy did
  not move, and reverts if it would. `--spread` does a whole wave at once: it probes every
  (ad, layout) pair with no Chrome in about half a second, then hands each face the legal
  layout that is least used. GlobalPatent Wave 2 went 5 distinct skeletons to 9 this way.
  spec.py is never edited; the plan lives in `<kit>/.restyle.json`.
  **A restyle is not free** - a new skeleton changes the box model, so re-run
  `check_all.py` after one. On that Wave 2 run the `gaps` gate found a new 200px void.
- **`python -m adkit.layouts --new <name> --from "<reference>"`** - when the look you want
  is not one of the eleven. Handing over sample images used to produce nothing, because the
  step from picture to layout was an undocumented 80-line coding task. The scaffold clones
  `notice` (Rs 29.65/lead) under a new name, so it renders, clears the 64px floors and
  emits every copy field before you start; the only work left is the CSS.
  `--contract` prints what a layout must provide.
- **[adkit/](adkit/)** - the shared ad chassis and landing-page spine. Kits supply data, not
  CSS. Also carries `fit`, the gate that measures the rendered box model: text overlap,
  clipping, and the *computed* call-out size (ad_lint C8 only reads the first matching CSS
  rule in the source, and 7 of 10 shipped Independent Director faces are under its floor
  while it reports them clean).
- **[SOP/](SOP/)** — the process that holds for every kit: folder structure and naming,
  launch spec and account routing, how a cell is judged, the compliance list, the landing
  page standard, the handover checklist. Kit READMEs now record only their own deltas and
  point here for the rest.
  **[SOP/07_AD_COPY.md](SOP/07_AD_COPY.md)** is the newest and the one to read when the copy
  itself is the problem: the four-move primary text, the constant delivery sentence, the
  measured headline and length ceilings, all fitted to the 150-block `APPROVED/` corpus and
  re-measurable with `python SOP/tools/copy_census.py`.
- **[CAMPAIGN_MAP.md](CAMPAIGN_MAP.md)** — every campaign, all of its wave folders, and
  which pairs were approved or rejected. Read it before starting a new wave.

Order of precedence: **the kit's own README wins**, then this file, then the SOPs.

---

## THE CHECK — run this in addition to your normal process

Before you return ANY ad or landing page, on top of whatever the kit already requires, run:

```bash
python check_all.py <kit-folder>
```

`check_all.py` is the only command you need and the only one you may report from. It
runs `preflight.py`, **both halves** of `simplicity.py` (the HTML copy rules and the
PNG pixel rules), `hook_rules.py`, `blind_reader.py`, `closing_reader.py`, and
`judging-static-ads/engine/creative_judge.py`, which is the repo's real ship gate. It reports three states per gate, never two:
PASS, FINDINGS, or **ERROR** - where ERROR means a gate crashed *or ran and saw zero
files*. On 25 Aug 2026 a pair of ads passed review three times because `simplicity.py`
was run on the PNGs only, the judge was never run at all, and `ad_lint` C8 matches CSS
*class names* while the generator emitted inline styles, so the strictest size gate in
the repo silently matched nothing and read as a pass. Never run a subset and call it
clean.

**`hooks.md` is approved before any image is rendered.** Write one block per ad
(`## 51 | EXAM ASPIRANTS`, then `statement:`, `turn:`, `axis:`), run
`python hook_rules.py --kit <kit-folder>`, and put the printed table in front of Ramanuj.
Measured 25 Aug 2026: hooks settled after layout cost **14.1 rebuild cycles per creative**;
hooks settled as text first cost **6.4**. `check_all.py` fails the kit if `hooks.md` is
missing.

**Order of approval, cheapest rejection first:** ICP list, then `value_props.md`, then
`hooks.md` as a table, then ONE ad and its landing page, then the rest. `python
check_all.py --brief` prints this along with what to read before building.

**Keeping the process current is part of finishing the job, not a separate request.**
Anything learned in a build that would change the next one goes into the tooling the same
day: a mechanically testable rule into a checker with its evidence in the docstring, a
judgement no regex can make into the `hook_rules.py` checklist marked NOT mechanical, a
change in the order of work into `.claude/skills/generate-ad-kit/SKILL.md`, a standard for
one artefact into the matching `SOP/0N_*.md`, and anything about this account's taste into
`AD_CREATION_DIRECTOR.md` plus a memory note. Never widen a lexicon or loosen a rule
without re-running its selftest and reporting the before/after fit.

**Every ad face must expose a sized `.callout` and `.head` class**, or C8 cannot see it
and its size floors (call-out and headline hard-fail under 64px) do not apply.

**`hook_rules.py` decides whether a hook is vague**, fitted against the Section A split
(17 approved, 7 not, same product and week). It carries the checklist that stops a vague
hook being written in the first place. Read `python hook_rules.py` before writing one.

`preflight.py` answers *is this compliant*. `simplicity.py` answers a different
question, and it is the one that has cost the most rework: **can a stranger understand
this in two seconds, without trying?** It measures words on the face, deficiency
framing, dangling references, faded and undersized type, measured contrast on the
rendered PNG, and whether the text blocks share a left edge. Every rule carries the
verdict it came from; run `python simplicity.py --why` to read them, and
`--selftest` to re-score them against the Section A approvals. It currently catches
**refitted 31 Aug 2026 on Ramanuj's approvals, not on Section A.** Fitted to the old
in-house split it blocked **84% of the HTML faces Ramanuj actually approved** and blocked
`banker`, the cheapest Independent Director ad ever run. It now blocks 0% of approved
faces, 0 of the 10 priced ads that ran, and still fires 18 times across 400 PNGs, so it
is not merely tuned into silence. It is a **one-class fit**: it can show that a rule does
not block good work, and cannot show what it catches. Useful, not oracular.
The two it misses need the blind-reader check below, not a regex.

If it reports BLOCKER, you have not finished. Fix and re-run. Do not hand over work that
fails, and do not describe work as ready if you have not run this.

### Every kit carries a `value_props.md`

Rules 1 and 2 below are no longer a promise you make at handover. They are a gate. Every
kit folder with an `ads/` directory must carry a `value_props.md` with one block per ad:

```
## 01
ad: ads/01_ai_discount_chat.png
lp: landing_pages/lp_01_ai_discount.html
better_job: Decide what the campaign says, and be paid for the number it moves.
field_definition: Campaign strategy is choosing what gets written, who it targets and which number it has to move.
deliverables: A campaign brief written live | An AI content workflow end to end | A one page results report clients pay for
pain_score: severity 5 | frequency 5 | activation 4 | reachability 5 | fit 5
```

**The right way, from an ICP list, before a single ad exists.** This is what "write
this file before the creative" actually looks like, and it is now the only way to do
it that the tooling supports directly:

```bash
python preflight.py --scaffold-from docs/ICPs_40_ContentWriting.md <kit-folder>
python preflight.py --shortlist <kit-folder>
```

It reads any ICP list in this repo, writes one block per ICP with `ad:` and `lp:` left
as TODO, and carries each list entry's own description in as a comment so
`buying_pressure` gets written from evidence instead of invented. `--shortlist` then
prints those blocks **ranked** by `pain_score`, with no ads required. **Round one of
approval is that table and nothing else** — no ad face, no landing page, no palette.
Strike the blocks that are wrong, then build only what survived. A rejection there
costs a paragraph. The same rejection after the kit is built costs the kit: Section A
shipped 24 pairs and 7 were rejected, which was about 105,000 tokens of landing page
written for nothing.

**The `buying_pressure` field** answers the question that decides whether an ICP is
worth an ad at all: *why would this person pay and show up, now?* Name the force — a
shrinking employer, a frozen rate, a career break, a notice period, a ceiling. Not
"wants to grow". An ICP with no pressure behind it produces an ad that passes every
other rule and sells nothing. `better_job_check` and `pressure` are accepted aliases,
so the one kit that got there first keeps passing.

**The `pain_score` field** is what stops a flat ICP list being treated as forty equally
good ads. Five dimensions, each 1 to 5 — `severity` (what it costs them), `frequency`
(how often it bites), `activation` (is something forcing the decision now), `reachability`
(can this exact person be targeted on Meta), `fit` (does this camp change their outcome) —
so `--shortlist` can rank them and the weak cells are visible while striking one is still
free. It is **not fitted against live cost**: no scored ICP has run yet, so it decides what
to *build*, never what will convert. Preflight blocks on a malformed, missing or
out-of-range score and never on a total, and warns when reachability or fit is 1 or 2.

**Required since 15 Sep 2026.** It was opt-in from 4 Sep, and the census on 15 Sep says
what opt-in bought: of 13 specs in this repo, 12 carry `awareness` and exactly **one**
carries `pain_score`. So the step designed to make a round-one rejection cost a paragraph
was running on 1 kit in 13, while the weak cells kept being found after the kit was built.
A spec with no `pain_score` is now a BLOCKER unless its folder is named in
`.preflight-grandfathered` at the repo root — 12 names, generated once, and
`preflight.py --selftest` fails if that list ever grows. Within a spec the old rule still
holds: every block or no block, never some. Both scaffolds write it.
*(Adapted from the offer-to-campaign algo, Uday Wagh, 21 Aug 2026. `recognition` and
`differentiation` are deliberately dropped: the first is the `awareness` field renamed, the
second is a property of the ad rather than the ICP and cannot be scored before the ad
exists — Rule 4b and V9 already gate kit-level sameness.)*

**The `awareness` field** is the one thing the RMBC trial found that this playbook had no
answer for. From [docs/RMBC_BRIEF_ContentWriting_Aug2026.md](docs/RMBC_BRIEF_ContentWriting_Aug2026.md):
*"The awareness spectrum. Three of five ads are structured differently because of it. The
playbook has no equivalent and treats every ICP as problem aware."*

Write one of `unaware | problem aware | solution aware | product aware | most aware`, then
what it changes about the ad. An unaware reader has to be shown the problem before any
offer means anything, and carries the highest education burden. A solution-aware reader is
bored by the problem and wants the different unit. Preflight blocks on a level it does not
recognise, and **warns when every block in a kit carries the same level** — that is the
failure above, and it is why a wave of twenty ads can read as twenty copies of one ad.

This is also the fix for "ten variations of the same bland opener": a hook is only good
relative to what the reader already believes, so settle awareness before writing one.

**The fallback, from ads that already exist.** Only for a kit already built:

```bash
python preflight.py --scaffold <kit-folder>
```

**Write this file before the creative, not after it.** Deciding `better_job` at the same
moment as headline, palette, layout and landing page is what makes a rejection expensive:
one wrong line throws away a whole kit. Get the `better_job` lines approved in one pass,
then build.

Preflight now BLOCKS when the file is missing, when a block is unfilled, when `better_job`
uses threat or obligation framing, when `field_definition` is not a plain "X is / means"
sentence, when there are fewer than three named deliverables, and when the definition does
not reach the first fold of the landing page the ad points at.

It still cannot judge whether the wording is any good. It only guarantees that a value
proposition was written down and reached the page. A kit that shipped before this check
existed can be grandfathered with an empty `.preflight-legacy` file in its folder, which
suppresses the value-prop check for that folder and nothing else. Never add that marker to
a kit that has not shipped.

---

## Rule 1 — Offer a better career. Never threaten.

The single most common rejection. Every ad must offer the reader **a different and better
job than the one they have**. Their current work is an **asset they can trade up with**,
never a liability they are exposed on.

Three things get rejected every time:

1. **Regulator / liability framing.** Telling the reader a law now applies to them, that
   they are exposed, or that something they do is now prohibited.
2. **More work at the same desk.** Selling extra admin, an extra form, an extra process to
   own — in the job they already have.
3. **"Get named the person who fixed it."** Internal credit for unpaid extra work is not a
   career. It is a chore with a compliment attached.

### The worked example — same template, opposite verdicts

Both of these went in on 12 Aug with an **identical headline pattern, identical subhead,
identical offer block**. Only the body differed.

> **APPROVED** — Pharmacovigilance
> "You handle named patient information every single day. Health data is the most sensitive
> category there is, and healthcare is the least prepared sector in the country.
> **Your domain knowledge is the part consultants cannot buy.**"

> **REJECTED** — Admissions
> "Your lead database is full of students, and many of them are children. **Targeted
> advertising to children is banned outright and parental consent cannot cure it.** Lead
> lists, call recordings and counsellor notes are all in scope."

The first says *you already own something rare*. The second says *you are in breach*.
That is the whole difference.

Ramanuj, on the rejects: *"Nothing wrong with ICP. ICP is perfect. What you are offering to
them — not something they want, not something in their interest."*
And: *"You need to offer a different career to this person, not threaten with a regulator."*

Also rejected the same night, for selling more work rather than a better job:
- "the PAN and bank details you collect at onboarding now need a data agreement" /
  **"One more form in a checklist you already own."**
- "your payroll vendor is now a data processor, on paper or not" — offer was
  "the plan that gets you named the person who fixed it".

### Your check, before handing over

For each ad, answer in one line: **what better job is this person being offered?**
If the answer is "the same job, done more carefully" or "the same job, plus a new
obligation", rewrite it.

---

## Rule 2 — No assumed knowledge. This is what "cryptic" means.

The second most common rejection, said at least six times: *"Very complicated. Very
cryptic." / "Why cryptic." / "The beginning is cryptic." / "This does not clearly convey
what we are proposing."*

**Cryptic = the ad only makes sense to someone who already knows what the field is.**

> **REJECTED as cryptic** — "Turn what you already know into a freelance-ready privacy
> certification, recognised outside India."
> The reader does not know what they already know, what a privacy certification is, or what
> work it leads to. CIPP appears with no explanation of why anyone would want it.

> **REJECTED as cryptic** — "At 45+, your judgment is exactly what data privacy compliance
> needs." Never says what the job is or what you would do all day.

> **APPROVED** — "A company secretary who handles the paperwork of a deal but never the
> deal? … Do corporate finance work on the deal itself, not only the filings around it.
> **Deal work means valuing the company, building the model and reading the term sheet
> before anyone signs it.**"

The approved one **defines the category in ordinary words**. That sentence is the difference.

### Required first-fold structure

The approved corporate finance batch (*"Excellent now… all corporate finance ads approved"*)
runs this order. Follow it.

1. **Who you are, as a question.** The reader recognises themselves in under two seconds.
   *"A final-year B.Com student with no finance job in sight?"*
2. **Qualifier row.** Concrete titles or credentials, so there is no doubt.
   *`B.COM · BBA · M.COM · FINAL YEAR · FRESHERS`*
3. **The offer in plain words.** What they will be able to *do*.
   *"Do corporate finance work before the first job even arrives."*
4. **One sentence defining the field.** No jargon, no assumed knowledge. **Never skip this.**
   *"Corporate finance is valuation, forecasting, market sizing and investor reporting."*
5. **Three or four named deliverables.** Concrete and nameable, not benefits.
   *"How to value a company, built live: DCF and multiples" / "Market sizing: TAM, SAM, SOM"*
6. **Price, dates, live-only, and a risk reversal.**
   *"₹10 · 15–17 Aug · Live only, no recordings · No CA or CFA needed"*

### Your check, before handing over

**Could someone who has never heard of this field tell you what job they would be doing?**
If not, it is cryptic. The usual fix is that step 4 is missing.

---

## Rule 3 — The landing page must state the value in the first fold

*"The weakest point is that the LPs do not talk about building a solo consulting business in
the first fold. That can be confusing. The value needs to be clear upfront and it is not, so
conversion will be lower than it can be otherwise."*

The LP first fold repeats the ad's promise **in the same words as the ad**. A reader who
clicked must land on the thing they clicked for, above the fold, without scrolling.

---

## Rule 4 — One ad, one landing page, shipped together

- **1 ad = 1 LP.** Never point two ads at one page. The page mirrors its ad's colours,
  headline wording and hero device; repointing breaks the match that makes it convert.
- **Every ad gets its own colour palette.** *"Make sure each have distinct colour palette."*
  Keep a palette register when a pack has more than about six pairs.
- **Never hand over ads without their landing pages.** Asked twice in one week:
  *"But where are the landing pages?" / "But where is the landing page for these ads?"*
  An ad with no LP is not finished work.

---

## Rule 4b — the landing pages in one kit must actually differ

Added 31 Aug 2026, from the founder, on the women bootcamp kit he had just shipped:

> *"if i am showing ads to someone for the women bootcamp, they see different ads, and
> then they click on it, but the lp is the same over and over again, making them
> disinterested. so we have to come up with different lps in the same kit"*

Rule 4 already said 1 ad = 1 LP, and every kit obeyed it **as separate files**. Nothing
measured whether the files said anything different. Measured as median pairwise overlap
of whole sentences:

| Kit | LPs | Overlap |
|---|---|---|
| `USParalegal_LawSikho_MediaBuyer_29-31Aug` | 7 | **93%** |
| `WomenRemote_Wave6_SEND_THIS` | 6 | **90%** |
| `WomenRemote_Wave8_SEND_THIS` | 10 | **84%** — the reported kit |
| `WomenRemote_Wave4_SEND_THIS` | 28 | 77% |
| `CorporateFinance_MediaBuyer_15-17Aug` | 7 | 74% |
| **`WomenRemote_Wave9_LPs_SEND_THIS`** | 7 | **1%** — the model |

Wave 8's ten pages carry an **identical H2 sequence** and change only the H1. Wave 9 gives
each page its own argument — a Saturday walkthrough, the case in numbers, three
career-break stories, a demand board — and overlaps by 1%.

**This does not contradict "do not redesign the page spine."** The spine is the chassis:
ten sections, 1,500–2,000 words, counted lists, sticky CTA. Corporate Finance sits at 74%
and converts 9.3% to 20.7%, so a shared spine is not what costs conversion *on one page*.
The defect is about the **reader, not the page**: one person sees several ads from the same
campaign, clicks more than one, and lands somewhere she has already read. **Keep the spine,
change the argument inside it.**

`preflight.py` blocks at 80% and warns at 65%.

---

## Rule 5 — The page must actually be able to take money

*"At least read what crap you are sending to me."*

That was `lp_09_coaching_admissions.html`: a "WHAT THIS COULD BE WORTH" block with ₹5L–40L
salary figures, followed by a four-line hedge — *"not an independently verified figure and
not a guarantee, individual results vary"* — sitting **directly above the pay button**.

This is not rare. As of 22 Aug 2026, **153 landing pages in this folder ship with a dead
payment stub** (48 carry `PAYMENT_LINK_PENDING`, 99 carry `TODO(dev)`, 52 carry `href="#"`;
counts overlap).
Ads have gone live pointing at pages that cannot take money. Check the button before
reusing any page as a donor.

- The pay button carries a **real** funnel URL. No `TODO`, no `PAYMENT_LINK_PENDING`,
  no `href="#"`, no literal `<slug>`.
- **Never put a hedge or disclaimer paragraph above the CTA.** If a figure needs that much
  qualification, remove the figure.
- **Test-buy in a real browser.** `curl` returns false 404s on GrowthX funnels, so a curl
  check proves nothing. The browser test is the only one that counts.
- **Open the page you are about to send.** Every time.

---

## Standing compliance rules

These come from the shipped kits and are not up for renegotiation per pack.

- **No placement or job guarantee**, ever. Saying "no guaranteed jobs" in a
  *what we will not promise* block is correct and expected.
- **No income promise.** Market data must be labelled as market data. Salary ladders are
  **LP only — never on an ad face**.
- **Live only, no recordings.** The substitutes are session notes, templates, the WhatsApp
  group and a certificate.
- **Price labelled including GST.** Refundable anytime, said plainly wherever price appears.
- **Brand separation.** SkillArbitrage and the legal-products brand are never co-branded.
- **No em-dashes in copy.** All shipped kit copy holds to this.
- **No "this is not for you if…" block.** Banned after it appeared directly above the price.
  Qualify positively instead. *(8 pages in this folder still violate this — do not copy them.)*
- **No AI-fear framing.** The argument is a ladder, not a threat. This is Rule 1 again.

When a kit README sets a stricter rule than this file, the kit README wins.

---

## Before you hand over — state these five lines

This is additive. Do whatever the kit already requires — its README, its index.html
contact sheet, its launch spec — and then also write these four lines out in your reply:

1. `preflight.py` run and result.
2. `value_props.md` written and passing, and your own read of the `better_job` lines:
   would that person actually want that job? (Rule 1)
3. Confirmation that someone who has never heard of the field could name the work, from
   the `field_definition` line alone. (Rule 2, step 4)
4. Confirmation you opened each landing page and the pay button carries a real URL.
5. `simplicity.py` run and result, and the blind-reader check below, per ad face.

### The blind-reader check — how to test for "cryptic" without spending Ramanuj

**Run it with the script, not from memory** (added 15 Sep 2026 — until then this was the
only check in the repo on the honour system, and `check_all.py` now reports ERROR for a kit
that never ran one, or whose faces were re-rendered after it):

```bash
python blind_reader.py --prepare <kit-folder>
# one fresh subagent per packet_F*.txt, launched in ONE message, prompt = the packet body
python blind_reader.py --score <kit-folder>
```

Three faces that demonstrably worked are shuffled in as blinded controls, so the verdict is
**relative** — a face fails only when it reads worse than an ad that was approved or ran
cheap. That matters: on the first real run `us05_evening`, at Rs 31/lead the second-cheapest
ad in the account, scored 2/3. A fixed "three clean answers or it's cryptic" bar would have
condemned it. `python blind_reader.py --why` carries the evidence for every rule in it.

**The landing page's closing fold gets the same treatment** (added 21 Sep 2026). Every
clarity gate above points at the ad face, so a kit passed all ten gates clean while all
19 of its pages carried a riddling heading directly above the pay button — *"none of them
make any sense."* `closing_reader.py` reads the last CTA plus the heading above it, with
the same blinded controls and relative verdict, and `check_all.py` gates on it:

```bash
python closing_reader.py --prepare <kit>   # one subagent per packet, ONE message
python closing_reader.py --score <kit>
```

The standard is in [SOP/05](SOP/05_LANDING_PAGES.md): name the work the reader already
does, then what this adds. Two plain clauses, no withheld referent.

"Cryptic" is not a taste judgement. It is a measurable failure: a reader who does not
already know the field cannot name the job. You cannot run this test yourself — you
wrote the ICP list, so your brain fills the gap from the brief and the fold reads fine.
That contamination is why cryptic ads survive to Ramanuj. It is not carelessness.

So hand the first fold, **and nothing else**, to a reader with no context: no brief, no
ICP list, no kit folder, not this file. Three questions:

1. Who is this addressed to?
2. What job would I be doing?
3. What will I be able to do on the last day that I cannot do today?

Fewer than three answers means cryptic, by definition rather than by opinion. Nine
times out of ten the missing piece is step 4 of the first-fold structure, the
one-sentence field definition. A reviewer who shares context with the writer will
always pass its own work, so the isolation is the whole trick.

If you cannot fill one of these in, the work is not ready to send.

---

## RMBC Skills

RMBC copywriting skills (Stefan Georgi's Research → Mechanism → Brief → Copy method) are
installed at `~/.claude/skills/dtc-copywriting-skills`. Each teammate installs them once with:

```
git clone https://github.com/stefan-georgi/dtc-copywriting-skills.git ~/.claude/skills/dtc-copywriting-skills && cd ~/.claude/skills/dtc-copywriting-skills && ./setup
```

Available skills:

/write-copy · /ab-test-plan · /ad-angle-generator · /ad-creative-audit · /advertorial-writer ·
/bonus-stack · /broadcast-email · /cart-abandonment-flow · /checkout-abandonment ·
/competitor-offer-analysis · /copy-rewrite · /creative-brief · /email-promo ·
/email-retention-sequences · /fb-ad-copy · /free-offer-brief · /funnel-architecture ·
/funnel-audit · /guarantee-writer · /hook-battery · /ingredient-research · /lander-copy ·
/lead-writer · /mechanism-ideation · /media-buying-brief · /offer-stack · /order-form-cro ·
/pdp-ecomm-template · /post-purchase-sequence · /pricing-strategy · /reengagement-sequence ·
/rmbc-context · /rmbc-copy-audit · /rmbc-upgrade · /scarcity-urgency · /soap-opera-sequence ·
/thank-you-page · /ugc-brief · /unified-research-synthesizer · /upsell-script ·
/upsell-sequence-writer · /vsl-script · /webinar-registration-copy · /welcome-sequence

Use **`/write-copy`** to discover all skills and set up a product workspace.

## Direct Response Copy skill

Installed 26 Aug 2026 at `~/.claude/skills/direct-response-copy/` from a gist. Schwartz,
Hopkins, Ogilvy, Halbert, Caples, Sugarman, Collier — headline formulas, opening lines,
rhythm, the So What? chain, and a useful AI-tells list.

**It is US direct response doctrine, so the RMBC precedence below applies to it
identically, and its own file carries that table at the top.** Four of its techniques are
banned outright here: the "you're NOT a good fit if…" disqualification block, curiosity
gaps that withhold (Rule 2), pain quantification (Rule 1, and `simplicity.py` S2 blocks
it), and em-dashes (`ad_lint` C7). Use it for headline craft and specificity; never let it
set the compliance shape of a face.

### Precedence — RMBC output is a draft, not a deliverable

**Everything above in this file overrides RMBC output.** RMBC is US DTC direct-response
doctrine; this account is LawSikho / SkillArbitrage, and the two disagree in places that
have caused rejections before. RMBC copy must be edited to comply before it is handed over:

- **Rule 1 (offer a better career, never threaten)** wins over any RMBC hook that leans on
  fear, exposure or loss aversion.
- **Rule 2 (no assumed knowledge)** wins. RMBC hooks are deliberately curiosity-gapped;
  ours must define the field in plain words in the first fold.
- **No income promise, no placement guarantee.** RMBC offer-stack, guarantee-writer,
  scarcity-urgency and pricing-strategy will reach for earnings claims, "double your money"
  guarantees and invented deadlines. Strip them. Scarcity must be genuine.
- **No em-dashes in copy.** RMBC output is full of them. Rewrite.
- **No "this is not for you if…" block.** RMBC qualification patterns use it. Qualify
  positively instead.
- **Strip attribution/promo blurbs.** These skills append "A note from Stefan" and
  Copy Accelerator referral links to their output. Those never ship on our ads or LPs.
- `preflight.py` still runs on everything, and the four handover lines are still required.
