---
name: project_dpdp_history_and_icps
description: DPDP/data-protection ad history across 37 months - only the Aug 2026 Rs10 camp is rankable; lawyers adding a practice line won; LawSikho Ad Accounts 2-4 are ACTIVE and carry the lawyer-segment evidence
metadata: 
  node_type: memory
  type: project
  originSessionId: cf343ba6-b495-4564-9e6a-d31fe2da3de5
  modified: 2026-09-21T12:59:51.740Z
---

Pulled 21 Sep 2026 for the **MAIN – Data Protection camp, 17-19 Oct 2026, LawSikho**
(confirmed by Ruchika). Kit: `DataProtection_LawSikho_MediaBuyer_17-19Oct/`. ICP list:
`docs/ICPs_DataProtection_LawSikho_17-19Oct2026.md`. Raw pull:
`ad-analysis-shared/reports/dpdp_family_37mo_2026-09-21.json` (GST INCLUDED).

**37 months, four efforts, only one comparable.** 135 ads, Rs 8.68 L incl. GST.
- DataPrivacy bootcamp Aug 2026 (Skill Arbitrage) - Rs10 purchase camp, par Rs144 gross
  (Rs122 net). **The only rankable history.**
- DPO bootcamp Sep 2025 (SkillArbitrage_V) - free LEAD camp; a vertical video drew 1,465
  leads at Rs60. Different family from a Rs10 purchase.
- CIPP crash course Oct-Nov 2025 (Brihaspati_AI_2) - high-ticket, Rs2.7-4.7k per sale on
  n=2-6. Different product. One ad claimed "earn 15 LPA" - an income claim, never reuse.
- Data Protection bootcamp Oct 2025 (Funnel Ashwin) - same product name as the Oct 2026
  camp, but 46 leads total. Too thin to rank.

**Proven cheap in Aug (winning FACE, top of 95% band under par):** firm_associates Rs97
(0.67x), side_practice 115, litigators 116, data_analysts 117, transcription_rcm 122.
Per READER only three hold across every face (litigators, transcription_rcm,
firm_associates) - side practice and data analysts win on one face only, so the refresh
unit is the winning face.

**Why:** three of the five winners are lawyers adding a data-protection line to a
practice they already run. That is Rule 1 done right on the product line Rule 1 was
written about. 32 of 50 Aug readers were UNMEASURED (never got budget), including most
lawyer readers - untested, not failed.

**How to apply:** frame every DPDP reader as a practice line to add, never "the Act now
applies to you". Every priced DPDP ad ran SkillArbitrage-side, so the brand transfer is a
real risk. **Correction, same day:** I first reported LawSikho history as invisible because
the ORIGINAL "Law Sikho" account 164485738329334 is DISABLED. It is the only one. LawSikho
Ad Accounts 2, 3 and 4 are ACTIVE (~Rs 9.4 Cr, 493 campaigns, 15,685 ads) and US Corporate
Law ran on Account 4 that week. I had only searched them for the word "privacy".

**LawSikho lawyer-segment evidence** (legal campaigns only, cost relative to each ad's own
campaign par, n>=5 cells; `reports/lawsikho_active_37mo_2026-09-21.json`):
CHEAPER - company secretaries (0.69x on n=529 in the `cs` ad sets; 0.88x n=2,280 broadly),
law-university audiences aged 22-34 (0.82x / 0.93x), labour/employment ad sets (0.94x,
n=1,242, only 2 camps),
banking/SEBI (0.88-0.95x), law firm audiences (0.85x), women lawyers restarting (0.90x once
the non-legal women funnels are excluded). DEARER - law students (1.10x, n=1,973) and
contract law (1.54x). My pain_score ranked law students FIRST; the money says dearer.
Tagging traps that inflated the first pass: "copyright" matched the copywriting product,
"hospital" matched hospitality, "women" matched the women-remote funnels, and an `LL`
ad-set group I first read as labour law spans CA/CS, SQE and USCL campaigns - it is
Meta's lookalike-audience shorthand. Read the campaigns behind a segment before naming it. For the
5 refreshes, live cost overrides pain_score (data_analysts scores 16/25 on paper and is
proven cheap). Winning faces for wave2/wave5 are NOT in the repo - only on Meta via the
pull's fb/ig links.

**Pull technique:** `pull_ads.py` fetches every ad in every account and filters by name
client-side; over 1,100 days that did not finish in 20 min. A server-side
`filtering=[{field:"campaign.name",operator:"CONTAIN",value:kw}]` on only the accounts
`pull_ads.py --list --days 1100` shows carrying the campaign ran in under a minute and
matched the full pull to the rupee. Script: scratchpad `dpdp_targeted_pull.py`.

**22 Sep 2026: batch 1 APPROVED by Ramanuj** (20 call-layout ads + 20 LPs, zip
`DataProtection_LawSikho_17-19Oct_SEND_THIS.zip`). His note: "why just mostly lawyers?" - batch 2
is 20 NON-lawyer readers taken from the Aug camp's own ad list (August non-lawyer evidence:
bfsi_ops n=475 Rs140, pharmacovigilance n=486 Rs148, returning_soft n=426 ~Rs151, logistics
n=118 Rs170, it_security n=144 Rs174; all ran SkillArbitrage-side, so LawSikho brand transfer is
untested for non-lawyers).

**Batch 2 built 22 Sep** (`DataProtection_NonLawyers_LawSikho_17-19Oct`, zip `..._SEND_THIS.zip`,
stems 21-42): readers 1-11 of the non-lawyer list, two ads each. A = call layout, step up. B = notice
layout after three rounds of Ruchika's feedback: no "invited to" sentence, no delivery paragraph
("text heavy"), a ticked list of the 3 evenings ("too empty"), a full-width CTA ("make the join
button bigger"), and a bridge line "Turn your <current work> into a better-paid data privacy
career" ("how does that connect to their current role?"). adkit notice layout gained optional
`ticks` and `big_cta`; palettes gained terracotta and violet; simplicity S6 learned
professional/staff/broker/agent (selftest unchanged).

Related: [[project_corporate_finance_live_cost]], [[feedback_icp_is_the_biggest_lever]],
[[feedback_split_occupation_by_sector]], [[feedback_report_scripts_narrow_silently]],
[[feedback_same_copy_different_face_10x]].
