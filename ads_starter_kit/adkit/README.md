# adkit

The shared chassis, spine, corpus index and fit gate. Built 31 Aug 2026 because a kit
build was spending most of its tokens re-deriving things this repo already knew.

## What was measured

**20 per-kit generators, 9,890 lines, no shared library.**

| File | Lines | CSS declarations |
|---|---|---|
| `womens_ai_bootcamp/gen_formats.py` | 1,311 | 926 |
| `ContentWriting_SectionA/gen_lps.py` | 1,702 | — |
| `IndependentDirector/gen_lps.py` | 774 | — |
| `IndependentDirector/gen_ads.py` | 390 | 113 |
| `WomensRemoteWork_HiddenMarkets/gen_ads.py` | 327 | 159 |
| `ContentWriting_SectionA/gen_ads.py` | 213 | 143 |

Each re-derives the same 1080×1350 shell, the same Chrome screenshot call, the same
`.callout`/`.head` classes `ad_lint` C8 matches on. `HiddenMarkets`' own docstring says its
chassis was carried over from `womens_ai_bootcamp` — by copy-paste, so it was re-emitted in
full anyway.

Same for the page: SKILL.md says in bold *"Do not redesign the page spine. It is already
solved."* Independent Director's pages are **20 KB** each for the same ten sections
ContentWriting_SectionA shipped at **55–72 KB**, seventeen times over.

And **2,822 lines of prose plus 9 PNGs** were mandated reading before step 0 — about
55,000 tokens before the first hook.

## The four modules

| Module | Replaces | What it adds |
|---|---|---|
| `spec.py` | `value_props.md` + `hooks.md` + `ad_copy.md` + both generators | one string per fact; Rule 3 true by construction |
| `verdicts.py` | nothing — the rejections were never machine-read | the labelled negative set, with the reviewer's words |
| `golden.py` | 9 hand-picked images frozen in August | 199 Ramanuj-approved faces derived from the corpus, with live cost |
| `chassis.py` | every kit's `gen_ads.py` | auto-fit by measurement; identity type clamped at 64px; one palette per ad enforced |
| `lp_spine.py` | every kit's `gen_lps.py` | the fixed 10-section spine; L1–L5 lint (dead pay stub, banned qualifier, em-dash, fold, word count) |
| `fit.py` | nothing — this defect class had no gate | F1 clipped, F2 overlap, F3 computed size floor, F4 missing identity class |
| `corpus.py` | nothing — the evidence was never joined up | 472 shipped ads joined to live CPL and approval status, searchable |

## A kit is now data

39 lines for two ads, including imports:

```python
from adkit import Kit

kit = Kit(root=__file__,
          brand="Skill<i>Arbitrage</i>",
          eyebrow="Independent Director Bootcamp",
          takeaways=["IICA databank registration, done with you",
                     "A 50-question mock exam, with answers",
                     "Notes, templates and checklists",
                     "A 90-day plan to your first board seat"],
          cta="Save my seat &#8594;",
          terms="<b>Free &middot; 12 to 14 September &middot; on Zoom</b><br>"
                "9 hours live &middot; Sat, Sun 2-5 PM &middot; Mon 7-10 PM",
          trust="NSE Emerge-listed &middot; NSDC &middot; IIT Roorkee iHUB")

kit.face("01_company_secretaries", palette="clay",
         callout="A company secretary?",
         head="Boards need people who <em>know how a board works.</em>",
         card=("Sitting fee, per board meeting",
               "&#8377;25,000 to &#8377;1,00,000", "10 to 18 meetings a year"),
         definition="Every listed and large public company must have independent "
                    "directors, who are outside members reviewing the accounts "
                    "and the big decisions.",
         proof="No prior board seat needed &middot; the exam is open-book")

kit.render("01")   # build ONE face first, then the rest
```

`render()` writes `html/` and `ads/`, measures each face, and picks the largest scale that
actually fits. It prints the chosen scale when it is not 1.00.

## Why auto-fit replaces `tight=True`

The Independent Director generator carried a hand-written CSS override block per ad — a
human guessing a character budget. SKILL.md, 26 Aug 2026: *"a guessed budget cost two of
the five cycles here."*

That override also set `.callout` to **58px** and `.head` to **52px**, both under C8's 64px
hard floor. It shipped clean, because **`ad_lint` C8 uses `re.search` for the FIRST
`.callout{...font-size:Npx}` in the source**, and a later override wins in the browser
while staying invisible to the linter.

Measured 31 Aug 2026 with `python -m adkit.fit IndependentDirector_Wave1_MediaBuyer_12-14Sep`:
**7 of 10 shipped faces** render under the floor, and C8 reports all ten clean.

So here, identity type is clamped: `.callout` and `.head` never go under 64px whatever the
scale, and only body elements absorb a tight fit. A face that still will not fit is
reported as *does not fit* — the fix is cutting words, which is the actual lesson
(*"Lengthening a definition sentence or a role name is never free."*).

## The fit gate discriminates

`python -m adkit.selftest` — three cases through real Chrome:

```
PASS A shipped face, scale 1.00                 expected clean     got clean
PASS B over-long definition, scale 1.00         expected FINDINGS  got FINDINGS
         F1 CLIPPED  .def runs 51px past the canvas
         F1 CLIPPED  .proof runs 105px past the canvas
PASS C .callout overridden to 40px              expected FINDINGS  got FINDINGS
         F3 FLOOR    .callout computed 40px, floor 64px
```

Case B is the 26 Aug 2026 defect that passed `simplicity` (both halves), `hook_rules`,
`ad_lint` C8 and `creative_judge` — 3 accept, 0 reject. Wired into `check_all.py` as the
`fit (rendered)` gate.

## The corpus

```bash
python -m adkit.corpus --like "chartered accountant board seat" --quote 3
python -m adkit.corpus --winners                    # cheapest live, with their copy
python -m adkit.corpus --losers --family purchase   # what actually costs money
python -m adkit.corpus --ad us05_evening
```

472 indexed ads, joined to the Meta pull (90 ads, ₹4,275,135) and to `APPROVED/` and
`GOLDEN/` membership. Relevance is token overlap — a finding aid. **The judgement columns
are live cost and APPROVED**; an ad with no CPL was never given budget, which is not the
same as being bad, so the table prints `-` rather than guessing.

Money joins are deliberately conservative: an unguarded version joined the ad named `01` to
`01_static_earn-in-usd` and reported someone else's ₹69 CPL on it. A wrong cost per lead
attached to an ad is worse than no cost at all.

## Rendering

Chrome is found automatically; override with `ADKIT_CHROME`. All output is ASCII-sanitised
before printing — `check_all.py`'s own docstring records the judge crashing on Windows with
a `UnicodeEncodeError` before printing its verdict, *"which looks exactly like a clean run
if you are not reading closely"*.


## The spec path (new kits only)

```bash
python -m adkit.spec --template > <kit>/spec.py
```

Measured on `IndependentDirector_Wave1`: `value_props.md` 127 lines + `hooks.md` 59 +
`ad_copy.md` 480 = **666 lines of hand-typed markdown**, plus the face data, plus the page
data — all the same content. `field_definition` is typed verbatim three times; `statement`
and `turn` twice; the deliverables twice.

A spec holds each string once and emits `value_props.md`, `hooks.md`, `ad_copy.md`, the
faces and the pages. Verified against the existing gates: `preflight.py` parses the
generated `value_props.md` at **0 BLOCKER** and reports *"every ad states a better job and
defines its field on the page it points at"*; `hook_rules.py` parses the generated
`hooks.md` and prints its table.

**Rule 3 becomes structural.** `field_definition` is one string that reaches the face and
the page. `lp_spine`'s L4 check and preflight's fold check still run, but on this path they
cannot fire — which is the point.

**The delivery sentence is a kit constant with one `{outcome}` slot**, and `Spec()` raises
if it has no slot. 139 of 150 approved blocks carry a delivery sentence and 136 name exactly
three things; `IndependentDirector_Wave1` wrote a fresh one per ad, carried 0 of 10, and
reads flat. On this path that is not writable.

Existing kits are untouched.

## Rejections: `verdicts.py`

`CAMPAIGN_MAP.md` records verdicts in three shapes — verdict tables, numbered wave lines
(`NOT APPROVED: 06, 13, ...`), and prose. All three are parsed, and `corpus.py --like` ends
by naming the rejections nearest your ICP **in the reviewer's own words**:

```
REJECTED near this ICP - the cheaper lesson, in the reviewer's own words:
  lp_01_collections_recovery   "you need to offer a different career to this person,
                                not threaten with a regulator"
```

The rejected set is ranked over the verdict records themselves, not over the ad index,
because the richest verdict set in the repo — the 12 Aug batch of 9 that CLAUDE.md Rule 1
is derived from — is **landing pages**, which never appear in an `ad_copy.md`.

Scoping is conservative for the same reason the money join is. Three bugs found and fixed
while fitting it, each of which would have attached a verdict to the wrong ad:

- Word-set overlap picked `content-writing-bootcamp` for "Section A verdicts", because the
  folder spells it `SectionA` and shares no *word* with the sentence. Scored on substrings now.
- The `NOT APPROVED:` line does not itself name the kit — the line above it does. Scoring the
  single line filed all seven Section A rejections against the wrong kit.
- `re.match(r"^(\d{1,2})")` never fires on `06_wheres_the_work`, because `_` is a word
  character. The numbered verdicts matched **nothing at all** until that was found.

The index now reproduces CAMPAIGN_MAP's own count exactly: 24 Section A pairs, 17 approved,
7 rejected.


## GOLDEN, derived

```bash
python -m adkit.golden          # rebuild GOLDEN/GOLDEN.md
python -m adkit.golden --dry    # show what would be included
```

GOLDEN was nine images hand-picked in August and frozen there, while the repo accumulated
hundreds of approved faces and a full Meta pull. It is now generated from sources declared in
`SOURCES`:

| Source | Faces | |
|---|---|---|
| `APPROVED/WhatsApp Unknown 2026-08-31...` | 10 | Ramanuj's own, sent 29 Aug |
| `APPROVED/` | 152 | Ramanuj-approved batches |
| `RID_BC_8Aug_Ads (1)` | 16 | **Ramanuj's own**, Independent Director 8 Aug |
| `Accounting_BC_8Aug_Ads (1)` | 21 | **Ramanuj's own**, US Accounting 8 Aug |

**199 faces, 47 of them Ramanuj's own.** The selection rule, corrected 31 Aug 2026: *"ignore
the ones that i approved, they were finally not approved. only the ones ramanuj approved
became the final ads."* An in-house APPROVED label is not evidence. The 17 Section A pairs
marked approved in `CAMPAIGN_MAP.md` carry no attribution, were approved in-house, and are
excluded by name. The two `_BC_8Aug` kits earn their place on more
than provenance: they hold the cheapest ads in the account. Four of the six lowest-CPL faces
are Accounting_BC creatives (₹39.93, ₹40.11, ₹41.21, ₹42.93) and `banker` (₹60.42) is the
best Independent Director ad ever run.

A face with a REJECTED verdict in `CAMPAIGN_MAP.md` is dropped automatically, so recording a
verdict there is enough to change the set. Two sources are excluded on purpose and the output
says why: `reference_images/` (donor material, not our ads) and `ads to be tested/` (no
verdict recorded).

**The hand-written WHY IT PASSED entries are never regenerated.** They move to
`GOLDEN/GOLDEN_NOTES.md` on first run and stay there verbatim — they are judgements no script
can re-derive.


## What the refit did to `hook_rules.py`

`hook_rules.py` was fitted on the Section A split — 13 approved hooks, 7 rejects — whose
approvals were in-house and did not stick. Measured against 123 headlines Ramanuj actually
approved (loaded through `adkit.golden`):

| | blocked, of 123 Ramanuj-approved headlines |
|---|---|
| before | **89 (72.4%)** |
| after | **5 (4.1%)** |

Rule E alone fired on 82 of 123. It required a verb, and the dominant approved headline here
is a destination noun phrase with no verb — "A global legal career, from home" — which is
what `SOP/07_AD_COPY.md` asks for. E is now advisory, on the same disposal rule that removed
Rule F for firing on 8 of 13.

Also: `CONCRETE` and `WORK` widened with nouns from ≥2 approved headlines (the old lists had
no vocabulary for law, accounting or board work), and rule A no longer reads `this/that`
followed by a noun as a dangling pronoun.

**It is a one-class fit and the file says so.** Every rejection in `CAMPAIGN_MAP.md` is a
landing page with no hook text, so precision is measurable and recall is not. The cost of the
refit is reported too: on the old split it now catches 3 of 7 rejects instead of 6.

**Not fitted on performance.** Only 13 ads carry both a hook and a live cost, and the gate
flags none of them — no evidence it predicts CPL, and far too few points to fit six regexes.


## What the refit did to `simplicity.py`

Same correction as `hook_rules.py`, and the same governing rule: **where a rule disagrees
with a face Ramanuj approved or an ad that ran cheaply, the face wins.**

| | before | after |
|---|---|---|
| blockers on Ramanuj-approved HTML faces | **26 of 31 (84%)** | **0 of 28** |
| blockers on Ramanuj-approved PNGs | 6 of 150 (4%) | **0 of 150** |
| ads that ran, blocked | 1 of 10 — including `banker`, Rs 60.42 | **0 of 10** |
| still fires elsewhere (liveness) | — | **18 L3 blockers across 400 PNGs** |

What moved:

- **S1** was a BLOCK at 100 words. Ramanuj-approved faces run **102 to 191 words, median
  113** — a duty chart carries more words than a poster. BLOCK moved to 195, above the
  heaviest he approved; 100 stays as a FIX, which is what it should always have been.
- **`ink_bands`** (feeding L3) now needs a band 24–110px tall. Every L3 blocker on approved
  work was a hairline or tint-block edge, not type. `banker` was blocked by an **11px band
  at 1.1:1**.
- **S2** exempts reassurance — "you do not NEED to move to use it" removes a barrier, it is
  not deficiency framing. All three S2 hits on approved faces were this shape.
- **R1/R2** exempt `CHROME_OWNED` (brand lockup, trust line, date chip, CTA). R2 was firing
  on 34 of 37 approved faces because it policed labels as reading matter.

Two things found while fitting, both reported rather than papered over:

- The fit set initially included `landing_pages/` and `index.html` contact sheets, which
  made S1 report 1,100-word "faces". Excluded.
- **R1's cited evidence does not hold.** It claims `16_will_you.html` sets
  `.def{font-size:22px;opacity:.72}` — the CSS rule exists, but no element in that file
  carries `class="def"`. It is dead CSS, so R1 never fired on the case it cites and never
  could have. The rule is kept, with that noted in its evidence line; it has no confirmed
  catch.

`--selftest` reports **liveness** as well as precision, because a gate tuned until it fires
on nothing is not a gate.


## What the refit did to `preflight.py`

Same basis, but preflight is different in kind and the refit reflects that: **it checks
wiring and compliance, not taste.** Ramanuj approving a creative says nothing about whether
its pay button works, so most of its blockers on approved pages are correct and were kept.

| blocker on approved pages | before | after | why |
|---|---|---|---|
| dead pay button (`TODO(dev)`, `PAYMENT_LINK_PENDING`, bare anchor) | 103 | **103, kept** | real defects; CAMPAIGN_MAP records them as disclosed |
| hedge above the CTA | **72** | **0** | rule was wrong |
| missing `value_props.md` | 16 | **0** | legacy kits, grandfathered with the documented `.preflight-legacy` marker |

**The hedge window was the false positive.** It blocked a hedge within 250 characters of a
CTA, calibrated on three pages. Measured across every approved landing page it fired 72
times, and **every single one sat at gap 237** — one shared US Accounting template, one of
whose pages carries `us05_evening`, the second-cheapest ad in the account at ₹30.55. The
page Ramanuj actually rejected sat at gap **46**. The window moved to **120**, which
separates 46 from 237 far more widely than 250 ever did.

## Rule 4b — landing pages in one kit must differ

New rule, from the founder, on the women bootcamp kit he had just shipped: a reader sees
several ads from one campaign, clicks more than one, and lands on the same page each time.

Measured as median pairwise sentence overlap: `USParalegal` 93%, `WomenRemote_Wave6` 90%,
`WomenRemote_Wave8` **84%** (the reported kit), `CorporateFinance` 74%,
`WomenRemote_Wave9` **1%** (the model). Wave 8's ten pages share an identical H2 sequence
and change only the H1; Wave 9 gives each page its own argument.

**It does not contradict "reuse the spine".** Corporate Finance is at 74% and converts
9.3–20.7%, so a shared spine does not cost conversion *on one page*. The defect is about
the reader, not the page. Keep the spine, change the argument. `preflight.py` blocks at
80%, warns at 65%, and currently flags **14 kits**.
