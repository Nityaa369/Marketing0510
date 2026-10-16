# Campaign map

Every campaign, every wave folder it has, and what is known about which pairs worked.
This exists so a new wave can be built on evidence rather than from scratch.

Rules and process live in [SOP/](SOP/). Copy judgment lives in [CLAUDE.md](CLAUDE.md).
The verdict evidence behind the marks below is in
[RAMANUJ_FEEDBACK.md](RAMANUJ_FEEDBACK.md), the master record of everything Ramanuj has said.

**Ship folders are zips (28 Sep 2026).** Every `*_SEND_THIS/` named below now lives
only as `*_SEND_THIS.zip` at the repo root, verified byte-identical before its folder
was removed. Four folders stay unzipped as well, because they hold the only copy of a
priced or approved face the corpus reads: DataProtection_LawSikho_17-19Oct,
TechLaw_Carousels_24-26Oct, WomenRemote_Wave4, WomenRemote_Wave9. To rebuild any
other ship folder, run `make_ship.py` in its `_MediaBuyer_` folder or unzip.

**Unapproved drafts deleted (28 Sep 2026).** Folders below that never ran and never had a
Ramanuj approval were deleted: Content Writing W3, RMBC, Neighbours Reworked, Collage, both
content-writing-bootcamp kits, Section A (only `ad_copy.md` kept), every `new ad types/` batch,
womens_ai_bootcamp_5-7Sep, WomensAI_Bootcamp_Wave1, SeniorConsulting_MediaBuyer_22-24Aug,
DataPrivacy_MediaBuyer_22-24Aug and the four Women Remote 5-7 Sep folders. Rows naming them
below are history. What they taught is in [RAMANUJ_FEEDBACK.md](RAMANUJ_FEEDBACK.md) Part 6.

---

## Content Writing Campaign Camp · SkillArbitrage · Rs 10 · 29–31 Aug

The most-iterated campaign in the folder. Account **Skill Arbitrage_2**.

| Wave | Folder | Ads | LPs |
|---|---|---|---|
| 1 | `ContentWriting_29-31Aug/` | 6 | 6 |
| 2 | `ContentWriting_W2_29-31Aug/` | 4 | 4 |
| 3 | `ContentWriting_W3_29-31Aug/` | 1 | 1 |
| 4 | `ContentWriting_W4_29-31Aug/` | 1 | 1 |
| 5 | `ContentWriting_W5_29-31Aug/` | 17 | 17 |
| Section A | `ContentWriting_SectionA_29-31Aug/` | 24 | 25 |
| Collage | `ContentWriting_Collage_29-31Aug/` | — | 4 |
| Bootcamp | `content-writing-bootcamp_29-31-Aug/` | 11 | 10 |
| Bootcamp variants | `content-writing-bootcamp-variants_29-31-Aug/` | 11 | 10 |
| Wave 6 formats | `new ad types/wave6_contentwriting_29-31Aug/` | 23 | 0 |
| Single-format tests | `new ad types/*_contentwriting_29-31Aug/` | ~20 | 0 |
| Money desk | `moneydesk_kit/` | 5 | 5 |
| RMBC method trial | `ContentWriting_RMBC_29-31Aug/` | 5 | 0 |

**Section A verdicts.** APPROVED: pairs 01, 02, 03, 04, 05, 07, 08, 09, 10, 11, 12, 14, 15,
20, 21, 22, 23 — 17 pairs, 18 ad images (04 is a two-card carousel).
NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to.

**RMBC method trial (22 Aug).** Not a wave. Five ICPs already covered by wave 6, rebuilt
through the RMBC framework so the two methods can be compared. Nothing in it is approved
and it should not be launched as-is. Read
[docs/RMBC_BRIEF_ContentWriting_Aug2026.md](docs/RMBC_BRIEF_ContentWriting_Aug2026.md)
for what the method added (a mechanism, an awareness map) and what it wanted that Rules 1
to 5 refuse. Two of its accents sit close to wave 6 neighbours, so re-cut before running
the two together. **Ads only**, so it reports the same single Rule 4 blocker every format
test in `new ad types/` does. Five pages were built and browser checked, then parked in
`ad_brief_tool/data/build_artifacts/`, which was deleted with the brief tool on 28 Sep 2026.

**The v1 statics were rejected by the `judging-static-ads` protocol and rebuilt.** Verdict
and rebuild record: `ContentWriting_RMBC_29-31Aug/VERDICT_v1.md`. Worth reading before the
next content writing kit, because three of its findings are kit-independent: the biggest
line must name the prize rather than the pain plus a statistic (V10), the wave 6 chassis
puts the CTA and terms bar outside the 1:1 crop, and no content writing ad in this folder
carries a barrier line, which measures at a 0.41 cost index. The parked landing pages were
built against v1 payoffs and no longer mirror the ads.

**Open across the family.** Wave 6's 23 ad faces have no funnel slugs, so no landing pages.
Waves 3 and 4 still carry the old walk-out wording; if live, push the correction as a
live-page edit.

Doctrine: [docs/CONTENT_WRITING_AD_PLAYBOOK.md](docs/CONTENT_WRITING_AD_PLAYBOOK.md) ·
ICPs: [docs/ICPs_40_ContentWriting.md](docs/ICPs_40_ContentWriting.md) ·
[docs/D2C_VALUEPROP_AND_ICPS_HANDOFF.md](docs/D2C_VALUEPROP_AND_ICPS_HANDOFF.md)

---

## Data Protection Bootcamp, 17-19 Oct 2026

| Wave | Folder | Ads | LPs | Design | Status |
|---|---|---|---|---|---|
| Batch 1 | `DataProtection_LawSikho_17-19Oct_SEND_THIS/` | 20 | 20 | call | APPROVED 22 Sep |
| Batch 2 | `DataProtection_NonLawyers_LawSikho_17-19Oct/` | 22 | 22 | call + notice | built 22 Sep |
| Wave 3 | `DataProtection_Wave3_International_MediaBuyer_17-19Oct/` | 20 | 20 | broadsheet | built 1 Oct |

**Wave 3, 1 Oct 2026.** Built after the cost per buyer climbed: live par Rs 212 over the 20
days to 1 Oct against Rs 144 in August. The rise is on Reels and Stories only (CPP +27% to
+57%) while Instagram feed held, so it is creative fatigue rather than the auction. Do not
read the blended CPM on this campaign: WhatsApp Status runs at a CPM of Rs 1 to 2 on 6% of
spend and drags it down about 57%.

Design: **newspaper beats standard twice**, Rs 192 (0.91x) against Rs 227 (1.07x) over 20
days, replicating Rs 136 against Rs 168 measured within the same campaign and week on
23 Sep. Within a single reader no design has a repeatable win.

Value proposition: the **cross-border half of the camp** (privacy work for clients abroad),
which no live page for this bootcamp argues. Batches 1 and 2 both argue "add this service to
the practice you have". Evidence and the twenty readers:
`docs/ICPs_DataProtection_Wave3_International_17-19Oct2026.md`.

---

## Data Privacy / DPDP GrowthCamp · SkillArbitrage · Rs 10

| Wave | Folder | Ads | LPs | Dates |
|---|---|---|---|---|
| Wave 1 | `DataPrivacy_Wave1_29-31Aug/` | — | 9 | 29–31 Aug |
| 22–24 Aug | `DataPrivacy_MediaBuyer_22-24Aug/` | — | 5 | 22–24 Aug |
| Main | `DataPrivacy_MediaBuyer_29-31Aug/` | 40 | 6 | 29–31 Aug |

**This is the richest verdict set in the folder — the 12 Aug batch of 9, all in
`DataPrivacy_Wave1_29-31Aug/`.** It is the source of CLAUDE.md Rule 1.

| LP | ICP | Verdict | Why |
|---|---|---|---|
| `lp_05_pharmacovigilance` | Pharmacovigilance | APPROVED | "your domain knowledge is the part consultants cannot buy" — the canonical approval |
| `lp_08_recruitment_bgv` | Recruitment / BGV | APPROVED | Explicit exit from the current track, in the headline |
| `lp_07_healthtech` | Healthtech product/ops | APPROVED | Names a specific senior role as the destination |
| `lp_06_returning_to_work` | Returning to work | APPROVED | Says "career" outright, zero threat content |
| `lp_04_customer_support` | Customer support | APPROVED | **Unresolved exception.** Structurally identical to two rejects. Treat as a real inconsistency, not a hidden rule |
| `lp_01_collections_recovery` | Collections and recovery | REJECTED | "you need to offer a different career to this person, not threaten with a regulator" |
| `lp_02_vendor_onboarding` | Vendor onboarding | REJECTED | "One more form in a checklist you already own" |
| `lp_03_finance_payroll` | Finance and payroll | REJECTED | Current-job obligation, "named the person who fixed it" |
| `lp_09_coaching_admissions` | Coaching and admissions | REJECTED | Regulator threat overrides a fine headline. Also the Rule 5 dead-payment-hedge example |

Also rejected as cryptic, in `DataPrivacy_MediaBuyer_22-24Aug/`: `lp_05_global_freelance`
("turn what you already know into a freelance-ready privacy certification") and
`lp_04_second_innings` ("at 45+, your judgment is exactly what data privacy compliance
needs"). Neither says what the job is.

---

## Corporate Finance · SkillArbitrage · Rs 10 · 15–17 Aug

`CorporateFinance_MediaBuyer_15-17Aug/` — 7 ads, 7 LPs, strict pairs.

**All seven approved.** "Excellent now… all corporate finance ads approved." This batch is
the template for the required first-fold structure in CLAUDE.md Rule 2: identity question,
qualifier row, offer in plain words, one sentence defining the field, named deliverables,
price and risk reversal. Copy this order.

**Priced 18 Sep 2026:** par Rs 193.94 on 3,155 purchases. Only `cf_loan_consultant` (Rs 164)
and `cf_cma` (Rs 170) clear par once the 1.96/sqrt(n) band is applied. Named occupations beat
angles: every jargon-angle face was cut under Rs 4,000 of spend.

## Corporate Finance · SkillArbitrage · Rs 10 · 17–19 Oct (MAIN, live)

Campaign `CorpFinance_bootcamp_17-19Oct_CBO`, Skill Arbitrage. **The cost is climbing:**
Rs 192 per buyer on 24 Sep to Rs 365 on 28 Sep, CPM flat, CTR 1.01% to 0.64%. Creative wear.

| Wave | Folder | Ads | LPs | Design |
|---|---|---|---|---|
| Notify | `CorporateFinance_Notify_MediaBuyer_17-19Oct/` | 19 | 19 | notify — all 19 faces and pages rejected 21 Sep |
| Venn | `CorporateFinance_Venn_MediaBuyer_17-19Oct/` | — | — | venn — rejected |
| Search | `CorporateFinance_Search_MediaBuyer_17-19Oct/` | 3 | 3 | search |
| Wave 3 | `CorporateFinance_Wave3_MediaBuyer_17-19Oct/` | 7 | 7 | collage — design approved 29 Sep |
| Wave 4 | `CorporateFinance_Wave4_MediaBuyer_17-19Oct/` | 8 | 8 | collage, new readers |
| **Wave 5** | `CorporateFinance_Wave5_Worklist_MediaBuyer_17-19Oct/` | 4 | 4 | **launchlist** — second device for the proven readers |

**`cfw3_loan_consultant` is the cheapest static in the account: Rs 136 on 117 buyers**
(band Rs 111 to 161), against Rs 209 and Rs 248 for the same reader's older faces in the same
days. Ad set level over the same 3 days: W3_Collage Rs 156, LPfix_SetA Rs 315, LPfix_SetB Rs 443.

**The standing problem is budget, not creative.** Waves 3 and 4 launched 15 faces on 30 Sep;
one took Rs 15,767 and proved the design, the other fourteen got Rs 100 to Rs 2,400 each and
cannot be read. Give a new wave its own ad set with a floor, or it is not tested.

Next CF camp is RE, 31 Oct to 2 Nov. Reruns are never advertised.

---

## HR GrowthCamp · SkillArbitrage_V · Rs 10

| Wave | Folder | Ads | LPs |
|---|---|---|---|
| Wave 9 | `HR_GrowthCamp_Wave9_MediaBuyer_22-24Aug/` | — | 5 |
| Wave 10 | `HR_GrowthCamp_Wave10_MediaBuyer_22-24Aug/` | 21 | 21 |

Do **not** add to the exhausted `HR_Growthcamp_July25` campaign. Beat Rs 331 CPP.

---

## Senior consulting / Consulting Growth Camp · SkillArbitrage · Rs 10 · 22–24 Aug

| Batch | Folder | Ads | LPs |
|---|---|---|---|
| Seat-Rs 10 series | `SeniorConsulting_MediaBuyer_22-24Aug/` | — | 8 |
| Growth Camp | `ConsultingGrowthCamp_MediaBuyer_22-24Aug/` | 2 | 7 |
| Reworked | `new ad types/senior_consulting_reworked_22-24Aug/` | 5 | 5 |
| v2 | `new ad types/senior_consulting_v2_22-24Aug/` | 7 | 0 |
| Senior AI | `SeniorAI_MediaBuyer_22-24Aug/` | 10 | 10 |

**ICP overlap is the live risk here.** Retiring-soon, senior women and own-firm appear across
batches on different creative. Split across ad sets or they bid against each other.

The three-draft cryptic sequence (`reference_images/IMG-20260807-WA0000..0002.jpg`) is this
campaign: "the flipping burger thing is not clear as a hook — who are you talking to and why"
then "the beginning is cryptic" then shipped. See `RAMANUJ_FEEDBACK.md` Part 3.2.

Launch spec **not set** for these batches. Confirm before spend.

---

## Women AI (remote work for women) · SkillArbitrage · FREE · 3-5 Oct (MAIN, live)

Campaign `WomenAI_FREE_3-5Oct-2026_BC_CBO_v1`. Free camp, so the unit is cost per
REGISTRATION and must never be blended with the Sep Rs 10 CPP. 30-day par Rs 36/reg on
16,467 registrations and Rs 5.88L. Cost rose Rs 27 (19 Sep) to Rs 40 (1 Oct): CPM +17%,
CTR +9%, registrations per click -11%. The decay is on the PAGE, not the face.

| wave | folder | status |
|---|---|---|
| search (3 faces) | `WomenAI_Search_MediaBuyer_3-5Oct` | shipped |
| **wave 10 (20 pairs)** | `WomenAI_Wave10_MediaBuyer_3-5Oct` | **built 2 Oct, all 11 gates clean, slugs not yet created** |

Wave 10 design, approved before building: `strucklist` 0.88x par on 5,327 registrations
(+/-3%) on 12 faces, `clockband` 0.93x on 856 (+/-7%) on 8. Both read off the live
creatives. Not used: label rows 1.01x (n=5,211), day-part cards 1.07x (n=3,445).

Proven readers rebuilt: single mothers on one income (0.83x, n=3,175), school hours (0.86x,
n=360), family carers (0.97x), teachers evening (0.98x), BPO night shift (1.01x). Fifteen
adjacent readers on the same axis have never run.

**The live-page defect this wave answers:** the three pages carrying 10,700 of the 16,467
registrations run an identical H2 sequence and change only the H1. Wave 10's pages overlap
that argument by 5% at worst.

## Women's programmes · SkillArbitrage · Rs 10 · 5–7 Sep

| Campaign | Folder | Ads | LPs |
|---|---|---|---|
| Women's AI bootcamp, wave 1 (s-series) | `WomensAI_Bootcamp_Wave1_5-7Sep/` | — | 9 |
| Women's AI bootcamp, main | `womens_ai_bootcamp_5-7Sep/` | 24 | 24 |
| Women freelance | `WomenFreelance_MediaBuyer_5-7Sep/` | — | 11 |
| Women freelance handoff | `handoff_women_freelance_aug07/` | 12 | 13 |

The s-series pages set the offer spine (5–7 Sep, 2–5 PM, Rs 10) the later kits build on.
Launch spec **not set**. Confirm before spend.

---

## Academic Content Writing · SkillArbitrage · Rs 10 · 26-28 Sep (MAIN)

Live campaign `MAIN - Academic Writing (Global career as academic content writer)` in
account **Skill Arbitrage (954464642377027)**. Campaign par **Rs 159 CPP incl. GST**
(Meta MCP pull, 31 Aug 2026, `last_7d`, grossed up 18%).

| Wave | Folder | Ads | LPs |
|---|---|---|---|
| 1 | `AcademicWriting_Wave1_MediaBuyer_26-28Sep/` | 5 | 5 |
|   | ship: `AcademicWriting_Wave1_SEND_THIS/` | 5 | 5 |

**Built 31 Aug 2026. No verdict yet.** Every gate clean; blind reader clean on all five.
Five faces on five different layouts (notice, serif, docket, nameplate, ladder).

What the live account already says about this camp, and what Wave 1 does with it:

| Live ad | CPP incl. GST | Verdict used |
|---|---|---|
| `acwr_06_lecturers` | Rs 115.96 (7 buyers) | rebuilt as cell 02 |
| `acwr_03_research_scholars` | Rs 124.84 (42) | rebuilt as cell 01 |
| `acwr_02_women_phd` | Rs 128.02 (45) | informs 01 and 04 |
| `acwr_01_homemaker` | Rs 133.92 (10) | rebuilt as cell 04 |
| `acw_teachers_sep26` | Rs 162.69 (68) | rebuilt as cell 03 |
| `pc_academic_writing_paychart_w2_sep26` | Rs 272.20 (20) | **archetype D. Not rebuilt.** 1.71x par, a fourth product line confirming the pay-chart finding. |
| `acwr_05_professors` | 0 buyers on Rs 256 | archetype C, generic honorific. Dropped. |
| `acwr_10_postgrad_board` | 0 buyers on Rs 95 | archetype D. Dropped. |
| `acw_ai_detectors_sep26` | 0 buyers on Rs 111 | archetype D. Dropped. |

Cell 05 (NET and JRF aspirants) is the forced tail discipline and has no ACW precedent.
Judge it on its own number.

**Slugs `sep26-acw-*` are declared, not yet created in GrowthX.** Not test-bought.

---

## US Accounting & Bookkeeping · SkillArbitrage · FREE · 10-12 Oct (MAIN)

Live campaign `US Accounting_AND_Bookkeeping_Oct_10th` in account **Skill Arbitrage
(954464642377027)**, Rs 32 per lead incl. GST over its life (25 Sep 2026 pull). One ad
(`us51_search_wfh_ended`, Rs 29 on 4,346) carries 80% of its leads; 28 of 37 ads got under Rs 500.

| Wave | Folder | Ads | LPs |
|---|---|---|---|
| search | `USAccounting_Search_MediaBuyer_10-12Oct/`, ship `USAccounting_Search_10-12Oct_SEND_THIS/` | 21 (us37-us57) | 21 |
| 2 | `USAccounting_Wave2_MediaBuyer_10-12Oct/`, ship `USAccounting_Wave2_10-12Oct_SEND_THIS/` | 12 (us58-us69) | 12 |

**Wave 2 built 25 Sep 2026, value props and hooks approved by Ruchika the same day. No
Ramanuj verdict yet.** Six starved or never-rebuilt readers, two faces each: search (even) and
notice (odd). Landing pages on the 21-step spine. Every `check_all` gate clean; the blind read
took three rounds. Round 1 read 7 of 12 faces as a step DOWN because they sold "bookkeeping";
reframed to US accounting for your own US clients, then 12 of 12 UP. Launch in its own ad set
with a guaranteed budget, or it starves like the 28 above. **Slugs `usacc-oct-w2-*` are
declared, not yet created in GrowthX.** Not test-registered.

---

## LawSikho

| Campaign | Folder | Ads | LPs |
|---|---|---|---|
| Arbitration | `Arbitration_LawSikho_MediaBuyer_13Aug/` | — | 10 |
| US corporate law paralegal | `USParalegal_LawSikho_MediaBuyer_29-31Aug/` | — | 7 |
| US Corporate Law wave 2, 19–21 Sep (LawSikho) | `USCorporateLaw_Wave2_MediaBuyer_19-21Sep/` | 10 | 10 |
| US Corporate Law wave 2, SHIP | `USCorporateLaw_Wave2_SEND_THIS/` + .zip | 10 | 10 |
| TechLaw, 10 reasons | `TechLaw_10Reasons_MediaBuyer_Kit_15-17Aug/` | 15 | 1 |
| TechLaw, litigators | `TechLaw_Litigators_MediaBuyer_Kit_15-17Aug/` | 3 | 3 |
| TechLaw, walkout / become firms | `TechLaw_Walkout_Become_Firms_MediaBuyer_Kit_15-17Aug/` | 13 | 3 |
| TechLaw carousels, 24–26 Oct (10 lawyer ICPs) | `TechLaw_Wave1_MediaBuyer_24-26Oct/` → `TechLaw_Carousels_24-26Oct_SEND_THIS/` + .zip | 10 | 10 |
| TechLaw Google, 24–26 Oct (same 10 lawyer ICPs, same LPs) | `TechLaw_Google_Lawyers_MediaBuyer_24-26Oct/` → `TechLaw_Google_Lawyers_24-26Oct_SEND_THIS/` + .zip | 10 | 10 |
| TechLaw non-lawyers, 24–26 Oct — **REJECTED**, see note below | `TechLaw_NonLawyers_MediaBuyer_24-26Oct/`, `TechLaw_Google_NonLawyers_MediaBuyer_24-26Oct/` | 20 | 10 |
| NCA Canada, 31 Oct–2 Nov (10 lawyer ICPs, notice + search) | `NCA_LawSikho_MediaBuyer_31Oct-2Nov/` → `NCA_LawSikho_31Oct-2Nov_SEND_THIS.zip` | 20 | 20 |
| NCA Canada wave 2, 31 Oct–2 Nov (10 new lawyer ICPs, notice + Notes) | `NCA_Wave2_LawSikho_MediaBuyer_31Oct-2Nov/` → `NCA_Wave2_LawSikho_31Oct-2Nov_SEND_THIS/` + .zip | 20 | 20 |
| Patent, wave 2 | `Patent_Wave2_MediaBuyer_7Aug/` | 7 | 11 |
| Patent, waves 3–4 | `Patent_Waves3-4_MediaBuyer_7Aug/` | 25 | 25 |
| Global Patent Analysts, 19–21 Sep (LawSikho) | `GlobalPatent_MediaBuyer_19-21Sep/` | 5 | 5 |
| Global Patent Analysts wave 2, 19–21 Sep (LawSikho) | `GlobalPatent_Wave2_MediaBuyer_19-21Sep/` | 10 | 10 |
| Global Patent wave 2, SHIP | `GlobalPatent_Wave2_SEND_THIS/` + .zip | 10 | 10 |
| SQE | `sqe_kit_aug06/` | carousels | in `lp/` |

**Global Patent wave 2 (3 Sep 2026) carries the cleanest natural experiment in the
folder.** `pc_patent_rf04_medrep_sep19` and `pc_patent_break01_medrep_sep19` ran a
**byte-identical body and headline** — both creatives pulled from Meta and diffed — at
**Rs 1,699.97** and **Rs 160.54** per buyer. Same copy, different face, 10.6x. The whole
`rf_` design-refresh family (`_swiss`, `_kawaii`) cost Rs 6,992 for 2 buyers, about 20x
par, and two of its five sold nothing. Read this before concluding that a wave's problem
is its copy. Wave 2 rebuilds ten faces on priced chassis and reuses the winners' copy
shape unchanged.

**TechLaw non-lawyer ICPs are rejected.** Ramanuj, 24 Sep 2026: *"non-lawyer ICPs do not
work for tech law."* That strikes the whole wave (6, 29, 30, 31, 32, 33, 35, 38, 39, 40),
not any one reader in it, across both formats. Twenty faces and ten pages were built and
passed every gate before the verdict; the ship folders and zips are removed and the two kit
folders are kept as the record. **Do not rebuild these ICPs for Tech Law.** The verdict is
about this product only — several of them have their own evidence on other camps.

**NCA wave 2 (30 Sep 2026) is a two-style test on one reader set.** Each of the ten new
lawyer readers carries a `notice` face (nca41-50) and a `notes` face (nca61-70) with the same
copy shape, in the same week, so the pair isolates the skeleton rather than the words. notice is
the only static style under par twice account-wide (0.81x); the Notes app layout had never run
before this wave. Judge per reader at 7 days and 20+ purchases, notice against Notes. Wave 1
(28 Sep 2026) runs the same structure with notice + search across ten different readers
(nca01-39) and **is the wave that is live**: 19 of its 20 ads are ACTIVE in `Meta - NCA - Oct
31-2 Nov Bootcamp - CBO Sales` (LawSikho Ad Account 4), at **Rs 16,066, 53 buyers, Rs 303 per
buyer** on a 7-day window pulled 1 Oct 2026. Per-ad n is far under the 20-buyer floor, so no face
has a verdict yet; the campaign figure itself carries a +/-27% margin at n=53. `nca16_notice_in_canada`
was never uploaded to Meta although its funnel is live - check before the next wave goes up.
All 20 wave-2 funnels are deployed and each serves its own page (checked in a browser 1 Oct 2026),
but no wave-2 ad is in Meta yet. Company-secretary ads (42, 62) must target CS audiences who also
hold an LLB; the NCA assesses a law degree.

**TechLaw BC was flagged for page speed** — only 33% of clicks loaded the LP. Check load
time on this family before spend.

Never co-brand LawSikho with SkillArbitrage.

---

## APPROVED/ · Ramanuj-approved batches, 22–24 Aug

Everything under [APPROVED/](APPROVED/) has passed Ramanuj. It is the out-of-sample set
for `simplicity.py --selftest`, so **do not edit these faces to make a checker happy** —
if a rule fires here, judge it by eye and change the rule or record the defect.

| Kit | Ads | LPs | Product | Checkout |
|---|---|---|---|---|
| `ContentWriting_Ready13_29-31Aug/` | 13 | 13 | Content Writing camp, Rs 10 | **all 13 unwired** |
| `LawSikho-Arbitration-MassHysteria-22Aug2026/` | 5 | 5 | Arbitration Skills, Rs 200 | falls back to `/modal/<slug>` |
| `ContentWriting_HeadOfContent_29-31Aug.zip` | 3 | 3 | Content Writing camp, Rs 10 | not checked, still zipped |

**Both checkout states are disclosed, not discovered.** Ready13's README says it outright:
*"This kit is being handed over with that FAIL open, deliberately… Do not spend against
these pages until it is done."* Every page calls `pay()` into a dev TODO, and the 13 funnel
slugs are already listed in that README's table — so wiring is substitution, not authoring.
MassHysteria's README has a **Pending before launch** section and had already caught a slug
collision on 23 Aug (`mh02` clashed with a live funnel). Treat neither as a surprise; treat
both as blocking spend.

Also disclosed in Ready13: **no gtag or Meta pixel in 11 of the 13 pages** (`usmb_05` and
`usmb_06` carry tracking).

**What the checkers added that the kit READMEs did not.** One real readability defect,
found by measuring pixels rather than reading CSS, and it is a chassis fault shared by all
five `cw_px_` faces:

- `cw_px_demand_board.png` sets its evidence line — *"17,000+ content strategy and 64,000+
  AI strategy roles open on Naukri now"* — in micro grey at **2.8:1**. That is the most
  persuasive fact on the ad rendered as the least readable thing on it. `"You already own
  the hard half. The rest is repackaging."` sits at 3.9:1 directly under it.
- The same grey terms element recurs at y≈1012 on `cw_px_budget`, `cw_px_india`,
  `cw_px_spec` and `demand_board` at 3.5–3.9:1. One chassis fix, not five page fixes.
- This is CLAUDE.md's own standing rule ("nothing important goes in a blind spot, no grey,
  no micro font") and `package_check` / `lp_lint` do not test for it.

Neither kit carries a `value_props.md`, so both fail the Rule 1/2 gate. They shipped before
that gate existed; grandfather with `.preflight-legacy` only if they are considered closed.

---

## Payment-stub status

Most landing pages outside the Section A kit still carry a dead pay button
(`PAYMENT_LINK_PENDING`, `TODO(dev)` or `href="#"`). Ads have gone live pointing at pages
that cannot take money. **Check the button before reusing any page as a donor.**
See [SOP/05_LANDING_PAGES.md](SOP/05_LANDING_PAGES.md).

---

## Supporting folders

| Folder | What it is |
|---|---|
| `new ad types/` | Format research: candidate lists, single-format tests, format waves |
| `ad_research/` | The questionnaire for Ramanuj and the Aug D2C research memo (his verdict baseline moved into `RAMANUJ_FEEDBACK.md`). The Meta Ad Library corpus, the Ad Lab tool and `ad_brief_tool/` were deleted 28 Sep 2026 as not useful |
| `ad-analysis-shared/` | Meta and Google performance pull (separate git repo) |
| `reference_images/` | WhatsApp reference sends cited by the research tooling |
| `docs/` | Playbooks, ICP lists, the Ad Avengers chat log |
| `_internal/` | Internal briefing decks, not client-facing |
| `_archive/` | Superseded builds and one-off prompts |

---

## Women's Remote Work Bootcamp · founder wave 4 · 5-7 Sep

| Kit | Folder | Ads | LPs |
|---|---|---|---|
| Founder wave 4 (**the reference build**) | `WomenRemote_Wave4_SEND_THIS/` | 28 | 28 |
| **Wave 9, warm pool — 6 of 7 approved** | `WomenRemote_Wave9_LPs_SEND_THIS/` | 7 | 7 |
| US roles, VA/SMM experiment | `WomensRemoteWork_USRoles_MediaBuyer_5-7Sep/` | 5 | 0 |
| Hidden markets (superseded angle) | `WomensRemoteWork_HiddenMarkets_MediaBuyer_5-7Sep/` | 3 | 0 |
| Verticals (**HALTED at spec stage, do not build**) | `WomenRemote_Verticals_MediaBuyer_5-7Sep/` | 0 | 0 |

**Wave 9 (31 Aug 2026): 7 built, 6 approved, 1 rejected.** One ad per Wave 9 landing page,
for the warm pool. Built on the Wave 4 chassis. The five approved-and-launchable pairs ship
as `WomenRemote_Wave9_LAUNCH_5-7Sep.zip`; the letter cell is approved but held for Nidhi
Dayani's sign-off, since it is written in her voice.

**The one rejection, and it is the useful part.** `A6_dayone` was rejected as *"cryptic, we
can drop it"*. Its headline was **"Read all three afternoons, then decide on the work."**
That headline names a **reading task**, not a destination: the biggest element on the face
was about the buying process rather than the job, so the reader is handed homework instead
of a prize. Kept with its evidence in
`WomenRemote_Wave9_LPs_SEND_THIS/WomenRemote_Wave9_LPs/_dropped_A6_cryptic/`.

Two gates passed it and should not be trusted alone on this failure mode:
- **The blind-reader test passed it cleanly**, all five questions, because the Day 1/2/3
  device does define the job. Blind-reader tests comprehension, not desire.
- **`hook_rules.py` passed it** once "decide" was accepted as a forward verb. "Decide"
  moves the reader through a *purchase decision*, not into a *job*; the lexicon cannot
  separate those.

**`WomenRemote_Verticals_MediaBuyer_5-7Sep/` is HALTED and should not be rendered.**
Written 26 Aug 2026: six credential ICPs, `value_props.md`, `hooks.md` (6 of 6 clean on the
fitted gate) and `ad_copy.md`. No faces were ever built, and none should be.

**Why it was halted.** Blind-reader checks on all six first folds came back **step DOWN,
6 of 6**, and a full rewrite of the worst cell came back step DOWN again. That is the third
independent confirmation of the same finding: the USRoles kit above shipped 5 ads and 0
approved on the same idea, and `womens_ai_bootcamp_5-7Sep/ICPs_20_Wave2.md` had already cut
BDS and PhD scholar on self-image. **A practising professional credential cannot be the ICP
for this product** — the mechanism and what to do instead are written up in
`.claude/skills/generate-ad-kit/SKILL.md`.

The folder is kept because the reasoning and the six blind-reader verdicts are the evidence
for that rule. The **demand research** it was built on
(`docs/RemoteWomen_ICP_MARKET_RESEARCH_26Aug.md`) is still good and still worth using — in
targeting, in Day 1 content, and on landing pages, not as an ad's identity band.

**`WomenRemote_Wave4_SEND_THIS/` is the reference build for this product.** Same camp,
built by the founder, 28 of 28 ACCEPT on `creative_judge`, every cell tied to measured
historical performance. Read its README before building anything for this brief; the
five elements every cell carries are recorded in `.claude/skills/generate-ad-kit/SKILL.md`.

The two experimental folders have **no landing pages** and are NOT ready to send:
`preflight.py` blocks on exactly that and the blocker has not been suppressed.
