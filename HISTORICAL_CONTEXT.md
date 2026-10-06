# Marketing historical context (LawSikho / SkillArbitrage Meta ads)

Built 6 Oct 2026 from `ads_starter_kit_2026-10-05.zip`, which is Ruchika's handover of her
Claude Code ad-kit project. It was packed on 5 Oct 2026 and is 23 MB in 424 files. Everything
here is dated. Numbers are as of the pull dates given, and the live Google Sheet and Meta
account win over this file.

---

## 1. The business

- **Product:** 3-day live online bootcamps (Sat, Sun, Mon) at **Rs 10 incl. GST**, refundable
  anytime, **live only with no recordings**. A few camps are free: Women AI 3-5 Oct, US
  Accounting and the ID lead camps. Each camp is the top of the funnel into a paid course.
- **Two brands, never co-branded:**
  - **LawSikho** (legal careers): data protection, arbitration, patents, IP, Tech Law, US
    Corporate Law, NCA Canada, SQE.
  - **SkillArbitrage** (non-legal careers): content writing, corporate finance, US accounting,
    HR, academic writing, Senior AI/consulting, Women AI remote work, Independent Director.
- **Reader:** an Indian professional, student or woman returning from a break. They are on a
  phone and half asleep. Ruchika's test: *"someone with brain functionality at 20%."*
- **People:**
  - **Ruchika** builds and reviews the kits. She is "the user" in the notes.
  - **Ramanuj** is the founder and the **only approver whose verdict counts**.
  - Her approval is not his. In-house "APPROVED" labels are not evidence.
- **Unit of work:** a **kit** is a wave of 5 to 20 ad + landing page pairs. Each pair targets
  one ICP and has its own palette and its own page. It ships to the media buyer as a
  `_SEND_THIS.zip` with six items: README, `ad_copy_wN.md`, `ads/`, `landing_pages/`,
  `manifest.json` and `kit_meta.json`. A `source/` folder can be added on request.
- **Checkout:** GrowthX funnels (`/f/<slug>`). The pay button opens `/modal/<slug>` in the
  page. Always test it in a real browser, because curl gives false 404s.

## 2. Approval order (cheapest rejection first)

1. Ranked ICP table (pain_score: severity, frequency, activation, reachability, fit).
2. `value_props.md`: better_job, field_definition, 3+ deliverables, buying_pressure,
   awareness.
3. `hooks.md` as a table. Hooks settled as text took 6.4 rebuilds per creative; hooks settled
   after layout took 14.1.
4. ONE ad + its LP.
5. The rest of the wave.

Section A is the cautionary tale: 24 pairs shipped, 7 were rejected, and about 105k tokens of
LP were wasted. Tech Law non-lawyers is another: 20 faces and 10 LPs passed every gate, then
the ICP was struck.

## 3. The rules that cause nearly every rejection

**Rule 1: offer a better career, never threaten.**
- The reader's current work is an asset to trade up with.
- Three framings are always rejected: regulator or liability fear, more work at the same
  desk, and "get named the person who fixed it".
- Sell the same craft to a better payer. Ownership beats assistance.
- Approved example: *"Your domain knowledge is the part consultants cannot buy."*

**Rule 2: no assumed knowledge ("cryptic").**
- Every face and page defines the field in one plain sentence.
- First-fold order:
  1. Who-question.
  2. Qualifier row.
  3. Plain offer.
  4. Field definition.
  5. 3-4 deliverables.
  6. Price, dates, live-only, refundable.
- The template is the CF 15-17 Aug kit (7 of 7, "Excellent now").

**Rule 3:** the LP first fold repeats the ad's promise in the ad's own words.

**Rule 4:** 1 ad = 1 LP, a distinct palette per ad (CIELAB dE >= 12), and no A/B split.
**Rule 4b:** LPs in one kit must argue differently. Preflight blocks at 80% sentence overlap.

**Rule 5:** the page must take money. It needs a real funnel URL, a browser test buy, and no
hedge paragraph above the CTA.

**Standing rules:**
- No placement or job guarantee.
- No income figures on the face. Salary is page-only and must be sourced.
- No em or en dashes. Write "3 to 5 Oct".
- No "this is not for you if" block.
- No AI-fear framing.
- Freelancers do not convert, so exclude them.
- Every claim must trace to the bootcamp script. No false "be early" or newness claims.
- Indian faces only.
- Max 5 ads per ad set.

**Copy shape:**
- Call-out names the ICP in 2-6 words at 64px or more.
- The gain is stated in about 10 words, with the field named.
- Headline is 4-10 words (target 7) and names the destination role, never the pain.
- Face copy is 40-45 words, with a hard ceiling of 100.
- Primary text is 80-110 words.
- Body uses four moves: situation, pivot, delivery sentence (written once per kit; only the
  work object varies), terms.

**Landing pages:**
- Since 25-28 Sep 2026, **the 21-step spine is the standard**, at about 1,800-2,000 words.
- Close by naming the reader first, with a self-contained lede.
- Sentences run 34 words or fewer.
- Every colour pair is measured.

## 4. What the money says (evidence, not doctrine)

- **The ICP is the biggest lever.** Naming the discipline the reader already trained in
  indexes 0.95; generic ICPs index 1.18. This replicated in 4 of 4 campaigns.
  - Archetype B (life situation) indexes 0.96 and A (occupation) 0.98. Build these.
  - C (aspiration) indexes 1.05 and E (broad population) 1.15. Rewrite these.
  - D (device-led, no ICP) indexes 1.22. Do not build it.
- **Every ad above Rs 280 in the corpus is C or D.**
- **Credential-anchored ICPs fail.** A practising credential cannot be the identity for these
  products. This was proven three ways on Women Remote: USRoles got 0 of 5, Verticals was
  halted after 6 of 6 blind reads came back "step DOWN", and an earlier ICP cut was made on
  the same grounds.
- **Pay charts never win:** 2.3-3.2x worse in ID, Patent, US Acc and ACW. The 23 Sep style
  index softens this to "about par, with one 5.05x disaster", but it is still never a winner.
- **CTR does not predict cost.** It runs backwards in Senior AI (+0.61) and ACW (+0.52). Never
  defend an ad on CTR.
- **Same copy, different face, 10x cost:** the two Patent medrep ads, with byte-identical copy,
  ran at Rs 1,700 and Rs 160 per buyer. Pull ad-level data before rewriting copy.
- **The `notice` layout** is the only static under par twice (0.81x). Newspaper/broadsheet
  beat standard twice on DPDP. The CF wave 3 collage face `cfw3_loan_consultant`, at Rs 136,
  is the cleanest design win: the design moved the number, not the reader.
- **LP length does not predict conversion** (330 pages, about 0 correlation). Benchmarks:
  - A free camp converts about 30.5% of LP views; a paid Rs 10 camp about 9.6%.
  - About 22% of clicks never reach the page.
- **Budget routing:** a new wave inside a CBO starves. Give it its own ad set with a floor, or
  it is not tested (CF waves 3-4 on 30 Sep: 1 face was funded, 14 were starved).
- **Judging an ad:** use a 7-day window with 20+ results, print n and the ±1.96/√n margin, and
  never judge on a part-day. Compare only within a campaign, and never blend free-lead with
  Rs 10 purchase camps, or MAIN with RE.
- **Reruns (RE) are never advertised.**
- Women-only ad sets leak 22-25% of spend to men.
- WhatsApp Status fakes frequency and drags blended CPM down. Never report blended CPM there.
- Payment failures run about 2.5% on Meta and 11.6% on Google. Senior AI and USCL Google
  duplicate slugs (`-2`, `-3`, `r2`) fail at 30-40%, so check the slug before blaming the
  creative.

## 5. Performance snapshot, 5 Oct 2026 (Meta, incl. 18% GST)

7-day totals: **Rs 27.2L spend, 9,136 buyers (Rs 298 CPP), 13,196 leads (Rs 206 CPL).**

| Campaign | Judged on | 7d cost | 30d cost | Best faces (30d, n>=20) |
|---|---|---|---|---|
| SeniorConsulting 3-5 Oct | buyers | Rs 112 | Rs 136 | telecom, IT managers, hospital admin, construction PM (Rs 84-92) |
| US Accounting 10 Oct | leads | Rs 40 | Rs 36 | us51 search wfh_ended Rs 34 on 10,125 leads; us63 notice fifties |
| CorpFinance 17-19 Oct | buyers | Rs 259 | Rs 249 | cfw3_loan_consultant Rs 207, cf_cma Rs 219 |
| RID + ID 10-12 Oct | leads | Rs 95 | Rs 74 | C4_banker Rs 57, V3_educator_retired Rs 66 on 4,784 |
| TechLaw 24-26 Oct | buyers | Rs 209 | Rs 242 | videos unusedllb Rs 160, comeback Rs 171 |
| WomenAI FREE 3-5 Oct | leads | Rs 37 | Rs 36 | school_hours Rs 22, caregiver Rs 28, stop_waiting Rs 30 on 3,518 |
| Academic Writing 24-26 Oct | buyers | Rs 182 | Rs 182 | economics PGs Rs 152, medical researchers Rs 161 |
| DataPrivacy 17-19 Oct | buyers | Rs 188 | Rs 198 | pharmacovigilance Rs 94-128, firm associates Rs 136 |
| StrategicHR 31 Oct-2 Nov | buyers | Rs 156 | Rs 157 | retired Rs 138, women Rs 147 |
| NCA 31 Oct-2 Nov | buyers | Rs 334 | Rs 334 | spouse Rs 310, final year Rs 316 (only 2 cleared n=20) |
| Community camps (ASHWIN) | buyers | Rs 318-923 | | Contract Drafting, Legal AI, Crim Lit, M&A, SQE, Arbitration, Women AI June |

**Google Ads:** the API is not connected. The developer token on the MCC is not issued, so
there is no Google CPP/CPL. Google creative uses one `search` face per reader (no carousels),
puts the field definition on the face, and has authored headlines of 40 characters or fewer
and descriptions of 90 or fewer.

## 6. Campaign histories, by product

**US Accounting (SkillArbitrage, free lead camp)**
- CPL has fallen every month: Rs 140-230 (Jan-Jun), Rs 82 (Jul), Rs 60 (Aug), Rs 42 (Sep),
  about Rs 36 (Oct).
- "Same Work, Global Clients" was cheapest in Apr, May and Jun, and was never rebuilt.
- The Sep notice faces (us22 fifties Rs 29.65 net, us05 evening Rs 30.55) are the cheapest
  ads in the account. They are the blind-reader controls.
- "Bookkeeping" reads as a step down. Frame it as US accounting for your own US clients.
- The Oct search + Wave 2 kits are built; Wave 2 has no Ramanuj verdict yet.

**Independent Director (SkillArbitrage, free lead camp)**
- Lead cost by month: Jul Rs 62, Aug 69, Sep 77, Oct 63.
- The general "retired" frame has the highest ceiling: rid_quote_ 0.69x, Boardroom_Retirement
  0.78x.
- Named occupations give the higher floor.
- "15+ years experience" ads and women cells lose every time. Do not propose a women cell
  again.
- Facts:
  - The IICA exemption for ex-directors/KMP is 3 years.
  - The October script teaches a 6-month plan, **not 90-day**.
- The calendar face was rejected 28 Sep ("second innings, not a step down").

**Corporate Finance (SkillArbitrage, Rs 10)**
- Aug par was Rs 194. That kit is the 7-of-7 approved template.
- Proven readers: loan consultants/DSAs, CMA, equity research, aspiring IB.
- Losers: commerce grads, final-year students, career break, retired bankers.
- Oct cost climbed from Rs 192 to Rs 365 from creative wear.
- Wave outcomes:
  - Notify (19) and Venn were rejected 21 Sep: "where does it say build a career in corporate
    finance", and "CF work is not valuation, read the script".
  - Collage W3 was approved and won.
  - Launchlist W5 was built.
- The next camp is an RE run (31 Oct), so it is not advertised.

**Data Protection / DPDP**
- Over 37 months, only the Aug 2026 Rs 10 camp is rankable (par Rs 144).
- Winners are lawyers adding a practice line: firm associates Rs 97, side practice, litigators,
  data analysts, transcription/RCM.
- 17-19 Oct (LawSikho):
  - Batch 1: 20 call-layout ads, **approved 22 Sep** ("why just mostly lawyers?").
  - Batch 2: 22 non-lawyer ads.
  - Wave 3: International, broadsheet, cross-border angle.
- Par rose to Rs 212, from Reels and Stories fatigue.
- The 12 Aug Data Privacy batch of 9 is the origin of Rule 1:
  - Approved: pharmacovigilance, recruitment/BGV, healthtech, returning to work, customer
    support.
  - Rejected: collections, vendor onboarding, payroll, coaching.

**Tech Law (LawSikho)**
- Ramanuj, 24 Sep: *"non-lawyer ICPs do not work for tech law"*. The whole wave is struck;
  do not rebuild it.
- 10 lawyer ICPs survive, as Meta carousels plus a Google search wave.
- The Oct cost rise (Rs 424 vs Aug 288) is CPM, not conversion.
- Page speed was flagged earlier: only 33% of clicks loaded the page.

**NCA Canada (LawSikho, Rs 10 confirmed 30 Sep)**
- Past runs: free lead camps in 2023-24 (Rs 220-831/lead) and Rs 99 webinars.
- Geo targeting never won; bar-exam hooks run dear.
- Wave 1 (notice + search, 20) is live at about Rs 303 per buyer. Wave 2 (notice vs Notes app,
  20) is shipped.
- Days 1-2 run 2-5 PM, so never write "three evenings".

**Senior AI / Senior Consulting (SkillArbitrage)**
- Four generations:
  - Mar 2026: free camp, Rs 356 per lead.
  - Jun 2026: Rs 581 per buyer.
  - Aug 2026: Rs 220 per buyer.
  - Oct 2026: Rs 112-136 per buyer.
- Sell consulting, not AI. Name the trained discipline (ERP, credit officer, QA, security head).
- Strong angles: rented executive, banker-to-small-business, and the side of the 9-to-5.
- Live pages say 6-9 PM, but the sheet and script say 2-5 PM. This was unresolved at 28 Sep.
- "First paying client in 30 days" is not in any script.

**Women AI / Remote Women (SkillArbitrage)**
- The founder's Wave 4 (28 of 28) is the reference build. Wave 9 got 6 of 7 (A6_dayone "cryptic").
- ICP test is D/S/G/N: demand, solo, gap, and a trained Indian neighbour.
- The 3-5 Oct FREE camp has par Rs 36 per registration.
  - The cost rise is on the page: 3 live LPs share one H2 sequence.
  - The struck-list layout ran 0.88x and clockband 0.93x.
  - Best readers: single mothers on one income (0.83x) and school-hours mothers (0.86x).
- Wave 10 (20 pairs) is built; its slugs still need creating.

**Academic Writing (SkillArbitrage, Rs 10)**
- Winners: medical researchers, assistant professors, social science researchers, homemakers,
  teachers with a master's.
- The paychart ran 1.71x and was dropped.
- The Oct 24-26 time is 2-5 PM per the sheet; the scripts still say 6-9.

**Arbitration (LawSikho community)**
- The audience is worn out, not the faces. The June pages fell from 13-17% to 4-9%
  conversion, and cost went from Rs 228 to Rs 600-800.
- No ad has ever named the lawyer's existing practice. A new list of 11 practice-split ICPs
  exists.
- The Mass Hysteria speech-bubble faces (mh01-03) are GOLDEN.

**Content Writing (29-31 Aug)** was the most iterated campaign. Section A got 17 of 24
approved, and there is a 40-ICP list. The LP funnel slugs were the standing blocker.

**Others:**
- Patent: named-discipline faces won. Veterinary ran Rs 76 and microbiologists Rs 97, against
  "exam deadline" hooks at Rs 203-285.
- USCL: wfh_lawyers carried 1,067 buyers at Rs 219.
- HR: hospital HR ran 0.77x.
- Strategic HR: the 21-step LP spine was first used here.

## 7. Bootcamp calendar ahead (from the 28 Sep sheet copy; re-read the sheet)

| Dates | Camps |
|---|---|
| 10-12 Oct | US Accounting MAIN (free), Independent Director MAIN, Academic Writing RE |
| 17-19 Oct | Corporate Finance MAIN, Data Protection MAIN (LawSikho), IP Law RE, Women AI RE |
| 24-26 Oct | Academic Writing MAIN, Tech Law MAIN, ID RE, US Accounting RE |
| 31 Oct-2 Nov | Strategic HR MAIN, NCA MAIN, Corporate Finance RE, Senior AI RE |

## 8. Tooling and data access

- **`check_all.py <kit>`** is the only result you may report. Its states are PASS, FINDINGS
  and ERROR, where ERROR includes "saw zero files".
- It wraps:
  - `preflight.py`
  - `simplicity.py`
  - `hook_rules.py`
  - `adkit` fit and gaps
  - the blind readers, `blind_reader.py` and `closing_reader.py`, which use fresh subagents
    against priced controls
  - `creative_judge.py`
- The checkers are one-class fits on Ramanuj's approvals: they show a rule does not block good
  work, and cannot show what it catches. When a rule disagrees with an approved or cheap ad,
  fix the rule.
- `adkit/` is the shared chassis.
  - It has 11+ layouts: notice, serif, ladder, nameplate, docket, search, chat, venn, notify,
    call, worklist, strucklist, clockband, collage, notes, broadsheet, airdrop, darkobject and
    others.
  - It also holds `spec.py`, `corpus.py` and `brief.py`.
- **Known red line in this bundle:** `adkit fit + LP lint fit` reports ERROR.
  - Two of its failures exist upstream too.
  - Two come from the omitted `APPROVED/` (78 MB) and `reference_images/` (40 MB) folders.
    Ask Ruchika for them to turn it green.
- **Meta data** comes from `ad-analysis-shared/pull_ads.py` on a read-only System User token in
  `.env`, which is not in the zip; ask Ruchika for it.
  - Use the token, not the Ads MCP, because the MCP cannot read LawSikho Ad Account 4.
  - Spend comes back net and is grossed up 18% GST.
  - The old Law Sikho account is DISABLED.
  - Supermetrics' trial has expired.
- **GrowthX:** use `get_leads_report` in 7-day pulls; 14-day pulls truncate silently. Join to
  Meta on `group`, not `leadtype`. Meta and GrowthX agree within ±11%.
- **Report format:** reports go in chat only. Always day by day, with the columns ad, spend,
  buyers, CPP and a link to the ad. No impressions, CTR or CPM.

## 9. Open items and contradictions at handover

1. **Times disagree across sources:**
   - ACW 24-26 Oct: sheet 2-5 PM vs scripts 6-9.
   - Senior AI 3-5 Oct: pages 6-9 PM vs sheet 2-5 PM.
   - NCA Day 3: sheet vs scripts.
2. Free vs paid for US Acc 10-12 Oct: undecided in the relaunch shortlist, "free" in the ICP doc.
3. Proven faces that break current rules:
   - banker: a sitting-fee figure and an em dash.
   - RID_i7_forces: a "first board appointment in 6 months" outcome claim.
   - rid_quote_: em dashes.
4. Declared slugs not yet created in GrowthX: `sep26-acw-*`, `usacc-oct-w2-*`, `dp-oct-w3-*`,
   `wai-oct-w10-*`. Also, nca16 was never uploaded to Meta.
5. Many current waves carry only Ruchika's approval: Women AI W10, NCA W2, US Acc W2, ACW W1.
6. Several ICP lists still include freelancers, against the ban.
7. About 25 "CONFIRM WITH RAMANUJ" placeholders are open, and ABO vs CBO (70/30) is unsettled.
8. Unsourced claims were found on live pages: "Recognised NSDC Training Partner", "first
   paying client in 30 days", and "90-day" ID plans.
9. Data Privacy customer support was approved despite having a rejected shape. It is an
   unresolved inconsistency, not a hidden rule.

## 10. Where to look in the kit

| Need | File |
|---|---|
| One-page rules | `SOP/00_CONSTANTS.md` |
| Rules 1-5 + handover lines | `CLAUDE.md` |
| Full build guide | `AD_CREATION_DIRECTOR.md` |
| Every Ramanuj verdict | `RAMANUJ_FEEDBACK.md` |
| Every campaign/wave + verdicts | `CAMPAIGN_MAP.md` |
| Live cost by ad | `PERFORMANCE_2026-10-05.md`, `ad-analysis-shared/CPL_WINNERS_31Aug2026.md` |
| Lessons with evidence | `earned_memory/` (134 notes, index `MEMORY.md`) |
| Approved exemplars | `GOLDEN/`, `APPROVED/`, `reference_pages/` |
| ICP lists, scripts, research | `docs/` |
