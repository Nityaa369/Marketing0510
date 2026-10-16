# SOP 08 — Choosing the ICP

`AD_CREATION_DIRECTOR.md` §2 settles **how an ICP is phrased** on the face: a real self-recognised
job title, un-checkable situation, identity in the band and situation in the headline, widen
laterally never upward. All of that still holds and this file does not repeat it.

This file settles the question before that one: **which ICPs are worth an ad at all.** It is
fitted to the last three months of live spend — 128 ads, ₹2,591,070, Skill Arbitrage account,
pulled 31 Aug 2026 — plus the approval record in `CAMPAIGN_MAP.md`.

The short answer: **ICP choice is the largest single lever we have measured.** It moves cost per
result more than format, more than copy shape, and more than anything on the ad face. It also
turns out to move landing-page conversion by 2–3× with the page itself held constant (`SOP/05`).

---

## 1. The five archetypes, ranked by what they cost

Every ad in the last three months resolves to one of five ICP archetypes. Normalised against
each ad's **own campaign median** (1.00 = par, so product, objective and period are controlled):

| Archetype | n | Index | Median cost/purchase | Median cost/lead |
|---|---|---|---|---|
| **B — a life situation** (career break, in their fifties, mother, small town, free evenings) | 15 | **0.96** | ₹127 | **₹42** |
| **A — an occupation, adding a line to what they already do** | 69 | **0.98** | **₹145** | ₹59 |
| C — an aspiration or abstract state (freedom, "switch", own firm, IPO) | 18 | 1.05 | ₹188 | — |
| E — a broad population ("women", "global companies") | 5 | 1.15 | ₹170 | ₹67 |
| **D — device-led, no ICP named at all** (pay chart, calendar, exam date) | 21 | **1.22** | **₹224** | ₹134 |

**Only A and B are worth building.** C, E and D are 7% to 25% worse at the median and carry the
tail: every ad above ₹280 in the corpus is C or D.

**D is not an ICP.** A pay chart, a calendar motif, an exam deadline and a lab notebook are
devices in search of a reader. They cost **55% more per purchase than a named occupation** and
they are also the format finding in `SOP/07` §9. If you cannot name who the ad is for before you
pick the device, you are building a D.

## 2. The strongest single rule — name the discipline they already trained in

Inside archetypes A and D, split by whether the ICP names the reader's **own trained discipline
or existing practice**, versus a generic or distant occupation:

| | n | Index |
|---|---|---|
| Names the reader's own discipline / practice | 64 | **0.95** |
| Generic, distant, or no ICP | 26 | **1.18** |

Replicated in **4 of 4 campaigns** where both kinds ran side by side:

| Campaign | Own discipline | Generic / distant | Penalty |
|---|---|---|---|
| Patent 19 Sep | ₹121.53 | ₹263.95 | **2.17×** |
| Patent 15 Aug | ₹140.09 | ₹213.27 | **1.52×** |
| Senior AI | ₹191.65 | ₹234.71 | 1.22× |
| Corporate Finance | ₹193.93 | ₹213.24 | 1.10× |

The clearest case is one Patent camp: `icp_28_biomedical_devices` ₹91.36, `icp_27_semicon_vlsi`
₹120.68, `icp_18_agri_foodsci` ₹131.49, `icp_26_ayurveda_bams` ₹135.30 — against
`Exam window — deadline urgency` ₹203.28, `Exam 2027 timeline` ₹250.89, `Calendar motif` ₹284.95.

**Manufactured urgency is the expensive way to sell this product. A named discipline is the cheap
way.** A deadline is a reason to hurry; it is not a reason to believe the work is for you.

## 3. The four tests an ICP must pass before it earns an ad

Adapted from the D/S/G/N test in `docs/RemoteWomen_ICP_MARKET_RESEARCH_26Aug.md`, which was
built for the remote-work product and generalises. Score each candidate; **miss one and strike
the block.**

| Test | Question | Why |
|---|---|---|
| **Identity** | Would this person tick this box on a form about themselves? | "Women looking to learn AI skills" is not an identity. "Company secretaries" is. Rejected ICPs are almost always failures here. |
| **Pressure** | Why would they pay *and show up*, now? | Name the force: a frozen rate, a shrinking employer, a notice period, a ceiling, a career break, a retirement. "Wants to grow" is not a pressure. This is the `buying_pressure` field `preflight.py` already blocks on. |
| **Adjacency** | Do they already do a version of this work, in their own vocabulary? | §2. The reader must recognise the job as a step, not a leap. A litigator hearing "privacy law" is adjacent; a schoolteacher hearing "patents" is not. |
| **Ceiling** | Is there a named thing they cannot get where they are? | `cf_loan_consultant` (20.7% LP conversion) is *"a loan consultant whose every conversation ends at a loan"* — the ceiling is in the sentence. `cf_retired_banker` (9.3%) is *"still wants to work, from home"* — an aspiration with no ceiling. Same page, same week, **2.2× apart**. |

## 4. Two rules the repo already paid for

**A practising professional credential cannot be the ICP for a general remote-work product.**
Proven three independent ways and recorded in `CAMPAIGN_MAP.md`: `WomensRemoteWork_USRoles` shipped
5 ads and 0 approved; `WomensRemoteWork_HiddenMarkets` 3 ads and 0 approved;
`WomenRemote_Verticals` returned **step DOWN on 6 of 6 blind-reader checks** and was halted before
any face was built. A dietitian does not want to become a dietitian's assistant. Use the
credential for *targeting*, and make the ICP the **situation** she is in.

**Do not give a whole wave one awareness level.** `preflight.py` warns when every block in a kit
carries the same `awareness` value. A wave of twenty ads at one awareness level reads as twenty
copies of one ad, which is the failure the RMBC trial found and this playbook had no answer for.

## 5. How many, and in what order

- **Round one of approval is the ICP list and `value_props.md`, nothing else.** No faces, no
  pages, no palettes. Section A shipped 24 pairs and 7 were rejected — roughly 105,000 tokens of
  landing page written for nothing. A rejection at the list stage costs a paragraph.
- **Scaffold from a real list, never from imagination:**
  ```bash
  python preflight.py --scaffold-from docs/<ICP list>.md <kit-folder>
  ```
  It carries each entry's own description in as a comment, so `buying_pressure` gets written from
  evidence rather than invented.
- **Cover an occupation at the discipline level, not the sector level.** The Patent camp got
  `agri_foodsci`, `semicon_vlsi`, `biomedical_devices`, `ayurveda_bams` — four cheap cells — by
  splitting "science graduates" into the degrees people actually hold.
- **A relaunch of a proven ICP beats a new one.** `icp04_fifties_RELAUNCH` ₹46.21 and
  `indian_mom_RELAUNCH` ₹60.73 both re-ran measured winners. Check `CAMPAIGN_MAP.md` before
  inventing.

## 6. The check, before the list goes to Ramanuj

Per candidate ICP, one line each:

1. Which archetype — **A or B?** If C, D or E, strike it or rewrite it into A or B.
2. Does it name a discipline or practice the reader **already trained in**?
3. `buying_pressure`: what is the force, in the reader's own terms?
4. What is the **named ceiling** they cannot pass where they are?
5. Would they tick this box on a form about themselves?
6. Is this ICP's `awareness` different from at least some others in the wave?

Then run the list through `preflight.py` and put it in front of Ramanuj **before** anything is
built.

---

## Limits of the evidence

1. **One account, one quarter.** Skill Arbitrage `954464642377027`, last 30 days for the
   normalised figures. LawSikho `164485738329334` is DISABLED and contributes nothing.
2. **Archetype labels are mine**, assigned from ad names and kit copy after seeing the costs.
   That is a real risk of hindsight fitting. The two findings replicated across independent
   campaigns — D being worst, and own-discipline beating generic — are the ones to trust; the
   A-vs-B ordering (0.98 vs 0.96) is well inside noise and should **not** be used to prefer one
   over the other.
3. **Cost per lead is not revenue.** None of this says who showed up to the camp or bought after.
4. **Creative is confounded with ICP** — an ICP cell is also a specific face and a specific page.
   The `SOP/05` finding that the page spine is constant within a kit is what lets us attribute
   most of the within-kit variance to the ICP, but it does not fully separate them.
