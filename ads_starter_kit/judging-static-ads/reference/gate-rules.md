# Static Creative Judge — Rulebook v1

Accept/reject rubric for 1080×1350 statics. Every rule traces to a measured cost delta or a
recorded rejection.

**Status (13 Aug 2026).** Gate 0 is built and runs: `python3 ads/creative_judge.py <kit_dir>`.
C1–C22 are implemented in `ads/ad_lint.py` (C13 is delegated to `check_claims.py`, C20 is left
to Gate 1). Gates 1 and 2 are not built — a creative that clears Gate 0 is "pending vision",
never "approved".

## Backtest — the gate is validated against ads that ran, not against taste

`python3 ads/judge_backtest.py` (ads) · `judge_backtest.lp_backtest()` (landing pages).

**Test 1 — performance.** Join running ads to their local creative, normalise cost within
campaign, compare. A rule that rejects a winner is a broken rule.

| | before correction | after |
|---|---|---|
| ACCEPT | 0.95 | **0.98** |
| ACCEPT-WITH-CHANGES | — | 1.00 |
| REJECT | 1.02 | **1.03** |
| ads that beat their median and were rejected | **7** | **0** |

**Test 2 — your own approvals.** What goes into a media-buyer zip is what you approved. 48 zips
yield **714 approved creatives**; everything else generated locally is unshipped. (Unshipped is
a NOISY negative — some were simply never sent, not rejected — so the binding constraint is
one-sided: the gate must not reject what you approved.)

| | before correction | after |
|---|---|---|
| REJECT rate on APPROVED | **22.9%** | **3.9%** |
| REJECT rate on unshipped | 18.1% | 5.2% |

The gate was **inverted** — rejecting more of what you approved than of what you never sent.

**What the backtest changed, and why:**

- **C10 (earnings figures) was the single worst rule — it rejected 57 approved creatives.** Two
  bugs, both introduced with the rule: `₹\s?[\d,]{4,}` counted the comma, so the *price*
  "₹100," matched (twelve SQE statics rejected for showing their price); and lakh/crore fired
  on market-size stats ("963 cr IPO pipeline"). Now counts digits only, and needs an earning
  word nearby.
- **C7 (em-dash) and C8 (font size) are HOUSE STYLE, not performance.** Between them they killed
  the two cheapest ads in the account (₹38 and ₹45, index 0.45 and 0.54, both with clean
  call-outs). They are FIX-tier now and live in `STYLE_RULES`, which never accumulate into a
  rejection: two taste notes may not spike a winner.
- **C1 (fragment call-out) is FIX, not BLOCK.** It decides "has a verb" from a hand-maintained
  word list, and a closed list always has holes ("coach" is not in it). It blocked 25 approved
  creatives and 2 winners.
- **C2 (names nothing concrete) is WARN.** Its noun list has needed hand-extension for every new
  product and still rejected "Law college never taught you tech law."
- **Identity call-outs are no longer blocked.** "WOMEN IN ACADEMIA" (0.77) and "INDIA'S
  PROFESSORS" (0.82) both beat their campaign median. Naming the audience in the giant line is
  a proven winning pattern; a verbless call-out that names a person now routes to C3 (WARN).
- **Chrome is not a call-out.** Separators ("·"), logistics bands ("FREE · LIVE · NO
  RECORDINGS"), slide labels ("Days 8-14") and "A note from SkillArbitrage" were all being
  judged as the giant line on creatives that shipped.

**Landing pages — `lp_lint.py` has NOT been corrected and currently fails its backtest.**
32 LPs joined from `lp_rank_2026-08-10.json`: ACCEPT median index **1.00**, REJECT median index
**1.00** — zero discrimination. It rejects 61% of ranked LPs including four that beat median
CPP (`women-remote-corporate-litigation` 0.84, `meta-lp-v4-transition-dark` 0.85, and two more
at 0.89), on R1/R2/R3/R6/S1. Those rules need the same house-style vs performance split the ad
rules just got. Until then LP lint is advisory only.

### Per-rule audit — every rule scored against both labels

For each rule: how often it fires on approved work vs unshipped, and the cost index of the ads
it fires on vs the ads it does not. A rule that fires MORE on approved work, or fires on ads
that beat their median, is a broken rule.

| rule | fires on approved | fires on unshipped | idx fired | idx clean | verdict |
|---|---|---|---|---|---|
| C22 no camp date | 50.7% | 38.4% | **0.96** | 1.00 | **WITHDRAWN — sign reversed** |
| C0 no call-out found | 30.0% | 3.9% | 1.03 | 1.00 | **reclassified: parser gap, not a defect** |
| C10 earnings figures | 16.8% | 6.0% | 1.02 | 1.00 | **experience-gate half removed** |
| C8 font size | 48.3% | 27.7% | 1.00 | 1.00 | house style (STYLE_RULES) |
| C2 names nothing | 6.6% | 22.8% | 1.01 | 1.00 | healthy — WARN |
| C9 no promise | 27.3% | 47.6% | 1.01 | 1.00 | healthy |
| C23 no identity | 14.9% | 27.1% | 1.04 | 1.00 | healthy — FIX |

**C22 was withdrawn outright.** It was added on a pooled-copy reading that dated ads ran ~31%
cheaper. On the creatives themselves the sign reverses: dateless creatives ran at **0.96** vs
1.00, and it fired on half of all approved work. The original number came from primary text
pooled across products and did not survive per-creative data. Confirm dates from the schedule,
but their absence is not a defect.

**C0 is a coverage signal.** It fires on 30% of approved creatives against 3.9% of unshipped —
not because approved work is worse, but because a third of approved kits use markup `ad_lint`
cannot read, so C1–C6 never ran on them at all. It now reports as INFO and says so.

**C10 lost its experience-gate half.** "7+ years" on the judiciary statics is the statutory
eligibility requirement; "2+ years" likewise. It fired on 60+ approved creatives. The rule
conflated "no earning figures on an ad" with "no exclusionary seniority gates" (a separate
finding from the women ID autopsy, about excluding buyers rather than stating an eligibility
fact). A year-count regex cannot tell them apart.

**C23 — the identity call-out — is now inverted from how it started.** C1 used to block
verbless identity lines as riddles. Presence of an identity call-out is never a defect; its
ABSENCE is, and that is C23 (FIX tier, because keyword matching cannot see implied identity:
"School hours" targets mothers at index 0.80 without using the word).

### The two badly-named rules, in plain terms

**C9 "no promise" = the ad never says what the reader GETS.** This is the rule that enforces
"promise value or nobody joins". It was too narrow to be useful: it accepted only "We show you
…" and "in 6 months", so it flagged the legal-AI kit — which promises "30 SKILLS · 14 DAYS",
"Build 30 AI Skills From One System", "Finish a day's drafting by lunch" — as promise-less. It
now recognises four shapes of promise: a we-verb commitment, an outcome with a timeframe, a
**counted deliverable** ("30 skills in 14 days"), or an **outcome verb** ("build", "draft your
first…"). Fire rate went from 27.3% of approved work to **6.6%, against 23.8% of unshipped** —
a 3.6× discrimination, now the strongest single rule in the set.

**C2 "names nothing" = the giant line does not name the PRIZE.** It means the call-out contains
no concrete thing the reader wants: no board seat, no bail application, no privacy audit, just
an abstraction. It reads a hand-kept vocabulary list that cannot know every product's words, so
it is advisory (WARN) only.

### Dates go on the landing page, not the ad

Ramanuj, 13 Aug 2026: "we should put dates into landing pages not ad creatives." The backtest
agreed independently — dateless creatives ran at **0.96** cost index against 1.00 for dated
ones, and the old "no date on the ad" rule fired on 50.7% of approved work. So the pair is now:

- **C22 (ad)** — WARN when a camp date IS printed on the creative. It goes stale the moment the
  camp moves, and it measured worse.
- **P7 (LP)** — WARN when the landing page carries NO date. The page is where the buyer checks
  logistics before paying, so a missing date there is a lost conversion asset.

### Monetary outcomes are suspect, not disqualifying

Ramanuj, 13 Aug 2026: "if an ad promises very clear monetary outcomes that can be suspect but
not necessarily a reject outright - most of our ads are about how to increase income."

C10 is a flag now, and never accumulates into a rejection. Note the distinction it draws:
income **framing** ("add a second income", "increase what you charge") is the product's core
promise and is never touched. Only a specific monetary **figure** is flagged — that is the point
where a claim gets concrete enough to need backing, and where the upside ladder belongs on the
LP so it can be qualified.

### The five-point teardown (13 Aug 2026) — what a passing ad must still survive

Ramanuj tore down a women-remote static the gates had passed: "This ad sucks but the gates
caught no real issues. It is a total fail." Two lessons, then the five rules.

Lesson one: the ad arrived as an IMAGE, so Gate 0 never ran — the kicker was ~44px and C8
would have failed it on sight. **An image-only verdict is a degraded verdict and must say so;
judge the kit source.** Lesson two: after the backtest de-fanging, a clean pass means "no
known defect", never "good ad" — the teardown questions below are what decide.

| ID | Rule | Enforced by |
|---|---|---|
| C24/V10 | The BIGGEST line names the prize the TG wants, never the product. "6 things this bootcamp teaches that help you get one" fails (product as subject, prize as pronoun); "6 things that land you your first well-paid remote job" passes. | ad_lint C24 (pronoun form = FAIL) + vision V10 |
| C25/V12 | Barrier/eligibility lines are conversion assets, never fine print (<30px fails). 0.41 backtest index — the cheapest pattern in the account deserves legible type. | ad_lint C25 + vision V12 |
| V13 | Kicker looks 2× too big on desktop AND clears the 1:1 crop line with real margin, not technical clearance. | vision |
| V11 | No filler support copy. Delete-test every subtitle: what does a buyer lose if it goes? | vision |
| V14 | List items are mined from the camp's own delivery script — specific, surprising, worth ₹10 each. "Write short, clear emails" is filler; "a chatbot you build yourself, live" is real. | vision |

Fire rates on the archive: C24 0.2% approved / 0.0% unshipped; C25 2.2% / 2.4% — low and
sane. Both FIX-tier: individually accept-with-changes, two together (or with any other
substantive defect) a reject, which is exactly how the torn-down ad scores: V10 + V11 + V12 +
V13 + V14 → rethink, not tweak.

### Second teardown (15 Aug 2026, DPDP returner ad) — vision-judge calibration

Ramanuj's five points vs the judge's: caught #4 fully and #3's diagnosis (with the wrong
prescription), agreed on #2, missed #1 and #5. What changed:

- **C23 override ban (V16).** The kicker "BACK AFTER A BREAK?" fired mechanical C23 (no
  identity noun) and the vision pass waved it through as "situation-framing". Ramanuj: "no
  clear call out … strange." A bare situation names nobody; winners are person-IN-situation.
  When C23 fires, the vision judge may not override without a person-noun in the frame.
- **C26 (new): CTA full-exchange rule.** "Reserve my seat for ₹10" reads as a deposit with a
  balance due. Cure: "9 hours of training just for ₹10" / "₹10 gets you all 3 days".
  Prevalence: 132 approved ads use reserve/book CTAs, 67 uncured — so FIX-tier on the uncured
  form only; the rule postdates those approvals.
- **V13 widened: blind spots are positional.** A small top-corner chip is skipped even when
  legible; nothing that must be read may sit below the CTA — the CTA is the scan terminus.
- **V13 corollary (16 Aug, dp_icp40 data-analysts cell): a redundant footer strip below the
  CTA is a deliberate pattern, not a defect.** Ramanuj on the "Live online · dates · ₹10 ·
  refund" line sitting outside the 1:1 crop: "i am actually fine with this — even if that gets
  cropped it will show in landing page — same reason why date is ok there." When the below-CTA
  ink only restates what the LP carries (dates, price recap, refund policy), C22 and X1 stay
  WARN and the vision judge must not escalate the verdict to ACCEPT WITH CHANGES on their
  account. The strip is bonus ink for 4:5 placements; the LP is the source of truth. Escalate
  only when NON-redundant, must-read copy (a barrier line, a value claim) sits below the CTA
  or outside the crop.
- **V14 widened: value prop must match the ICP's goal type.** Job-seeker ICPs get the route to
  the job (N skills → land it → clear the interview → network); practice ICPs get deliverables
  and clients. The judge prescribed artifacts to a job-seeker — right diagnosis, wrong fix.

### What Gate 0 is and is not

Final state: ACCEPT 1.00 · CHANGES 1.00 · REJECT 1.03, and approved work is rejected 4.1% of
the time against 8.5% for unshipped. Gate 0 separates the bad tail; it does NOT pick winners —
accepted and accept-with-changes creatives perform identically. Treat it as a floor, not a
ranker. Picking winners is what Gate 1 and the novelty gate are for.

**Not yet used as a signal: chat transcripts.** Edits made to a creative between generation and
approval are a correction record, and nothing in this rulebook draws on them.

## Calibration notes

All measured over the 1,373 creatives in `ads/`:

- **E1/E2/X1 are carousel rules.** They assume a padded canvas whose corner pixel is the true
  background. On full-bleed 4:5 statics E1 fired on 77% and E2 on 162% (multiple hits/file),
  and E2 hit 919 non-carousel creatives against 55 carousel ones. They stay BLOCK on carousels
  and drop to WARN elsewhere until someone calibrates them against creatives that shipped.
- **The call-out bug was not cosmetic.** Re-linting the archive with the fixed parser against
  the old one: call-out text changed on **524 of 1,373 creatives (38%)**; **193 creatives newly
  FAIL** on C1/C2 having silently passed before, and **126 clear** as false rejects (mostly C8
  size checks on brand chips). Worst-affected kits: `techlaw_r10_jul27` (23), `style_matrix_jul15`
  (20), `judiciary_ctr` (14), `techlaw_freshwave_aug15` (14), `women_ai_r10_sep05` (13).
- **Two real `ad_lint.py` bugs were found and fixed while wiring this up.** (a) The call-out
  regex always closed on `</span>`, so `<div class=callout>PHD<br><span>SCHOLARS</span></div>`
  was read as the call-out "SCHOLARS" — every div-based kit had been linted against fragments.
  (b) Brand chips (`SKILLARBITRAGE`) were judged as call-outs and size-gated, which alone
  rejected 32 of 32 creatives in one kit.

Severity tiers:

| Tier | Meaning | Effect on verdict |
|---|---|---|
| **BLOCK** | Ships a known-costly or previously-rejected defect | REJECT, no discussion |
| **FIX** | Materially weakens the ad, cheap to correct | 1 → ACCEPT WITH CHANGES · 2+ → REJECT |
| **WARN** | May be deliberate | Accept, but the WARN must be stated as a decision |

---

## Decision procedure

```
1. Gate 0 — deterministic (HTML + PNG, no model):
     ad_lint.py · ad_render_qa.py · crop_qa.py · check_claims.py
     any FAIL -> REJECT immediately, return the failing line + the fix. Do not invoke the model.
2. Gate 1 — vision judge on the RENDERED PNG, viewed at 236px thumbnail first, then full size.
     Rules V1-V9 below. This gate catches most of what has historically been rejected.
3. Gate 2 — portfolio judge: novelty vs the rest of the kit, and vs ads already run
     for this product. Rules N1-N3.
4. Verdict = worst tier fired. Every verdict logs one JSONL row (see "Closing the loop").
```

---

## A. Copy rules (Gate 0, `ad_lint.py`)

### Implemented today

| ID | Tier | Rule |
|---|---|---|
| C1 | BLOCK | Call-out is a noun-phrase fragment (no verb, not a question). Rejected four times in one session: "this is shit not understandable at all". |
| C2 | BLOCK | Call-out names nothing concrete the reader wants. Name the prize, not an abstraction. |
| C3 | FIX | Call-out is only an audience descriptor ("For professionals with 15+ years"). Says who, never what. Demote to the supporting line. |
| C4 | WARN | Call-out over ~48 chars, stops being thumbnail-legible. |
| C5 | BLOCK | Call-out is about vague third parties ("they", "some people"). The reader must be in it. |
| C6 | WARN | Insider vocabulary (databank/IICA/NRC/LODR/DRHP). Only acceptable as a deliberate shibboleth. |
| C7 | BLOCK | Any em-dash in creative copy. |
| C8 | BLOCK | Call-out < 64px or kicker < 56px on the 1080 canvas (targets 80 / 64). |
| C9 | FIX | No concrete promise: no "We show/give you…" line and no outcome-with-timeframe. |

### Added 13 Aug 2026 (implemented — fire rates over the 1,373-creative archive in brackets)

| ID | Tier | Rule | Origin |
|---|---|---|---|
| **C10** | BLOCK | **No earning or experience figures on the ad.** Price (₹10, ₹100) is fine. Upside ladders belong on the LP only. | standing rule, never linted |
| **C11** | BLOCK | **No "not for you if…" / negative-qualification block**, any funnel. Qualify positively. Lint exists on LPs (P4), not on ads. | "i hate this never do this", 19 Jul |
| **C12** | BLOCK | **No distress positioning.** Positive capability framing only. Never "stuck", "left behind", "your career is over". | standing |
| **C13** | BLOCK | **Brand matches product line.** SkillArbitrage products (HR, US accounting, skilling) → "SkillArbitrage". LawSikho products (USCL, litigation, judiciary, patent, SQE) → "LawSikho". Never "BY LAWSIKHO" on a SkillArbitrage ad. | standing |
| **C14** | BLOCK | **Proof names: Garima Pandey, Amaresh Kumar only. Never Sandya Advani.** | standing |
| **C15** | BLOCK | **Never promise recordings.** Camps are live-only; substitutes are notes, templates, WhatsApp group, certificate. | standing |
| **C16** | BLOCK | **Vocabulary gates by product.** HR/SkillArbitrage skilling: never the word "AI" (use "agents"/"systems"). Global-work legal: "paralegal support for US/UK firms", never "work for US/UK clients". UK products: "UK law firms and lawyers", never bare "UK firms". SQE: "eligible to apply", never "automatic". | four separate corrections |
| **C17** | BLOCK | **No topic call-outs on HR creative** (labour law, POSH). They read as Labour Law and cost ~10× — `strategic_hr_aug22` was rejected entirely on this. | measured |
| **C18** | BLOCK | **Never target or name freelancers.** Has never converted. | standing |
| **C19** | FIX | **Exam products (patent, judiciary, SQE) use abundance framing** — shortage of supply, huge demand. Never "only N cleared" scarcity; it backfires. | measured |
| **C20** | FIX | **4-step spine present:** identity → problem → value → CTA. Step 2 (the problem) is the step that goes missing. Name a big, recognisable buyer where proof is used. | recurring |
| **C21** | FIX | **Primary text under ~600 characters.** In the pooled 320-ad sample below, >600 chars ran at **2.15× product-median cost** — the single strongest text signal in the data. | measured, this folder |
| **C22** | WARN | Camp dates present on the ad and sourced from the schedule, never inferred from a campaign name. | recurring defect |

Age call-outs ("in your 50s") are **allowed** — do not let C12 or C3 flag them.

Fire rates on the existing archive: C10 6.1% FAIL / 9.1% WARN · C16 3.8% · C12 0.7% · C17 0.4%
· C18 0.3% · C15 0.1% · C11 0% · C19 0.1% · C22 41% WARN. Most of these creatives predate the
rules, so these are the historical violation rates, not a false-positive rate. C22's 41% is
worth a look on its own: two in five statics carry no camp date.

**Known Gate 0 limit.** Some kits (`acw_r10_aug1`) put the identity in `.callout` and the
promise in classes `ad_lint.py` does not scan, so C1/C2 read a bare audience descriptor and
reject the whole kit. That is the case Gate 1 exists for — do not solve it with more regex.

---

## B. Vision rules (Gate 1 — rendered PNG, the model actually looks)

This gate does not exist yet and is the biggest single gap. Most historical rejections were
visual, and `ad_lint.py` reads HTML so it is structurally blind to all of them.

| ID | Tier | Rule | Evidence |
|---|---|---|---|
| **V1** | BLOCK | **The identity call-out must be readable at 236px.** Render the thumbnail and read it back. If the judge cannot state who the ad is for from the thumbnail alone, reject. | the CPL lever |
| **V2** | BLOCK | **Every human in the image is Indian.** | standing, hard |
| **V3** | FIX | **Light background.** Dark statics cost 10–40% more. At most one dark cell per kit, labelled as the test cell. | measured |
| **V4** | BLOCK | **No invisible, cropped, or clipped text.** Includes text outside the 1:1 centre crop (y 135–1215) — `crop_qa.py` covers carousels, extend it to every static. | four render defects in one session |
| **V5** | BLOCK | **No dark-on-dark or low-contrast text.** Body-size text ≥4.5:1. | shipped once, 27 Jul |
| **V6** | FIX | **Call-out sits in the optical centre**, not floating above a dead band ≥180px (`ad_render_qa.py` E3). | implemented, unused on statics |
| **V7** | FIX | **Captions/hooks at the TOP of frame**, never lower third. | hard rule |
| **V8** | WARN | Canvas is exactly 1080×1350. | E4 |
| **V9** | FIX | **The kit varies aesthetically.** One aesthetic × N headlines is a rejection, not a kit. Distinct ICPs get distinct looks; offer anchors (price, dates, brand) stay constant. | recurring |
| **V20** | FIX | **The 4-step spine is visible:** identity → problem → value → CTA. Step 2 is the one that goes missing. Moved here from C20 — it needs the rendered creative, not a regex. | recurring |

**Running Gate 1.** `creative_judge.py <kit> --vision` renders 236px thumbnails plus a numbered
contact sheet and writes `vision_worklist.json`. Judge from the contact sheet first, fill in
`verdicts`, then re-run with `--vision-verdicts <path>` to merge and re-decide.

First real run (`dp_icp40_aug29`, 39 creatives): Gate 0 returned 38 accept / 1 reject; Gate 1
returned **39 reject**, on V9 (one template × 39 headlines, only the kicker accent colour
changes, 20 cells share the headline formula "Become the Data Protection Officer your X will
need in 2027") and V20 (the line under the headline states the reader's situation but never
names what it costs them). Neither defect is visible to any text linter.

---

## C. Novelty / portfolio rules (Gate 2)

| ID | Tier | Rule |
|---|---|---|
| **N1** | WARN | The creative is a near-duplicate of another cell in the same kit (same layout + same palette + swapped headline). **Never a rejection.** |
| **N2** | FIX | The angle was already run for this product and landed above 1.3× product-median cost. Do not re-ship a known loser with new art. |
| **N3** | WARN | The angle has no prior art for this product at all. Fine as a deliberate experiment; say so. Quiet days are the right days to run experiments. |

**N1 was downgraded from BLOCK to WARN (13 Aug 2026).** It shipped on the claim that two
near-identical cells "split delivery against each other". That is wrong. Ramanuj: "if we run
this meta will pick the winner - also you can reject one why will you reject both here?"
Inside an ad set Meta explores across creatives and concentrates spend on the better one, so a
duplicate costs nothing in delivery — the auction sorts it out. What a duplicate actually costs
is a **cell slot**: real estate that could have carried a different angle. That is an
opportunity-cost note for the person building the kit, not grounds for rejecting a creative
that is otherwise fine.

The one case where duplicates DO cost money is across separate ad sets or campaigns aimed at
the same audience, where the two creatives bid against each other in the auction. N1 should say
so specifically rather than flagging every within-kit variant.

N2 requires the creative→performance join described below. Until that join works, N2 can only
be run manually.

---

## D. Angle selection — what the data says

Measured, product-specific, and these beat design instinct every time:

**Works**
- **Identity call-out × earning promise.** HR: identity-led **₹31/buyer** vs capability-led **₹421** — a 10× gap on the same product.
- **Carousel on explanation-heavy camps.** Tech Law: **₹114** vs **₹375** for statics, 3.3×.
- **Barrier removal.** "No degree / no experience / no relocation" framing. Pooled sample: **0.41× cost index** (n=10, weak but directionally consistent with the ID and women findings).
- **Inclusive language, no seniority gates.** Women ID: exclusionary cells **₹633–1,800** vs **₹446** inclusive. ID inclusive LP **₹225** vs **₹400+**.
- **Light editorial aesthetic.**
- **Live dates present.** Pooled sample: **0.76** vs **1.10** index, 31% cheaper.
- **"Break into X"** beats market-opportunity framing; personal beats market.

**Does not work**
- Long primary text (>600 chars): **2.15× cost**.
- Cryptic or noun-fragment call-outs; small call-outs.
- Dark backgrounds (+10–40%).
- Negative qualification, distress framing, "honest" money hedging.
- Topic call-outs on HR (~10×).
- Freelancer targeting.
- One template with a swapped accent colour, ad or LP.

**Caveat on the pooled numbers:** n=320 ads with >₹3k spend across 4 products, normalised to
each product's median cost. Confounded by ICP and by budget allocation (winners accumulate
spend). Treat as corroboration of the rules above, not as independent proof.

---

## E. Closing the loop (the change that makes the agent improve)

Today the agent can only enforce rules. It cannot learn, because a rendered creative cannot be
matched to its own performance:

- 6,253 local PNGs · 4,275 distinct creative slugs
- 5,389 ads with spend > 0 · 2,135 with > ₹5,000
- **exact name join: 112 ads (0.5% of spend). Fuzzy substring join: 863 ads (5.0% of spend).**

Fix, in order of value:

1. **Pull `creative{image_hash,image_url,thumbnail_url}` in the daily ad-level pull** and store
   `image_hash` per `ad_id`. Only `patent_history_pull.py` and a few others fetch
   `thumbnail_url` today; nothing stores a stable image key.
2. **Write the kit slug into the ad name and into `manifest.json`**, and make
   `package_check.py` FAIL when a kit PNG has no matching anchor entry keyed by that slug.
   This alone takes the join from 5% to ~100% for everything shipped from now on.
3. **Backfill** by perceptual-hashing local PNGs against downloaded `image_url`s for the ~2,100
   ads with >₹5k spend.
4. **Log every verdict** as JSONL: `{ts, kit, file, gate, rules_fired, verdict, reviewer}` —
   then a nightly job appends realised CPP/CPL. After ~200 rows this rulebook stops being a
   list of remembered corrections and becomes a measured one.
