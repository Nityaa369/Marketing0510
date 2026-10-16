# Tech Law camp: fact check of market claims (16 Oct 2026)

Scope: claims in `docs/TECH_LAW_CAMP_FACTS_2026-10-16.md` (sections 1, 2, 4, 7), the "List of Spaces"
brief and the deep tech warm-up email ("20 Skills ... AI, Drone and Space Law").

Method: WebSearch only (fetch blocked). Verdicts read from search-result summaries of the named
pages, not from full page reads, so re-open the URL before printing a number on a page.

**Coverage limit, read this first.** The shared web search budget for this turn (200 calls across
all agents) ran out partway through. Everything from the US claims onward (section F, most of G, H)
could not be searched. Those rows are marked UNVERIFIED with "not searched". Where I have
background knowledge I give it as a note, but a note is not a source and does not make a row TRUE.
A few rows rely on sibling research notes in this scratchpad (`research/06_notes.txt`); those are
marked "(sibling note)".

Verdict key: TRUE = a credible source gives the figure as written. TRUE WITH CORRECTION = true only
in the corrected form. UNVERIFIED = no credible source found or not searched. FALSE = a credible
source contradicts it, or it is outdated in a way that makes it wrong today.

---

## A. Regulation ("India rewrote its tech rulebook in 18 months")

| # | Claim as written | Verdict | Correct version | Source | Source date |
|---|---|---|---|---|---|
| A1 | DPDP deadlines "November 2026 and May 2027" | TRUE WITH CORRECTION | DPDP Rules notified 13 Nov 2025 (G.S.R. 846(E)). Board provisions in force at once. **13 Nov 2026 starts only the consent manager provisions.** Almost every duty a business has (notice, consent, security safeguards, breach reporting, rights, retention) starts **13 May 2027**. | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf ; https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014 | 13 to 17 Nov 2025 |
| A2 | Spaces brief: "The DPDP deadline in November 2026 is weeks away. Companies need help now" | FALSE as written | The Nov 2026 date applies to consent managers, not to ordinary companies. MeitY proposed (Jan 2026) cutting the window to 12 months for Significant Data Fiduciaries, but no amendment was notified as of Sept 2026. Say "most duties start 13 May 2027". | https://www.business-standard.com/technology/tech-news/meity-may-cut-compliance-timeline-for-key-dpdp-rules-to-12-months-126012201293_1.html ; https://www.mirvolegal.com/insights/dpdp-rules-2025-compliance-timeline/ | 22 Jan 2026 ; Sept 2026 |
| A3 | DPDP penalties up to Rs 250 crore | TRUE WITH CORRECTION | Up to Rs 250 crore per breach for failing to take reasonable security safeguards. The cap comes from the DPDP **Act 2023** Schedule, not the 2025 Rules, so it is not "new in 18 months". Other caps: Rs 200 crore (breach notice, children's data), Rs 150 crore (SDF duties), Rs 50 crore (residual). | https://www.storyboard18.com/advertising/dpdp-enforcement-begins-penalties-up-to-%E2%82%B9250-cr-breach-put-entire-digital-ecosystem-on-high-alert-84226.htm | Nov 2025 |
| A4 | Any SME relief under DPDP | No relief found | Searches found no size-based exemption or lower penalty for startups or MSMEs in the Rules; commentary says the same caps apply to all. Background (unverified): Act s.17(3) lets the government exempt classes such as startups from some duties; no such notification found. | https://www.storyboard18.com/digital/dpdp-final-rules-set-off-a-compliance-stress-test-for-indias-msmes-and-startups-84254.htm | Nov 2025 |
| A5 | Takedowns "cut from 36 hours to 3", with AI content labelling | TRUE WITH CORRECTION | IT Amendment Rules 2026 (G.S.R. 120(E)) notified 10 Feb 2026, in force 20 Feb 2026. The 3-hour window applies to removal on a government or court order (it was 36 hours). Non-consensual intimate imagery: 2 hours. AI (synthetically generated) audio and video must be labelled and carry metadata. Grievance acknowledgement cut from 15 to 7 days. | https://www.livelaw.in/top-stories/centre-notifies-it-rules-amendment-to-regulate-ai-generated-and-synthetic-content-522623 ; https://www.legal500.com/intelligence/india/technology/it-rules-2026-deepfake-regulation-three-hour-takedowns-and-ai-labelling-obligations | Feb 2026 |
| A6 | "A national AI governance framework" | TRUE WITH CORRECTION | MeitY released the India AI Governance Guidelines on 5 Nov 2025. They are **voluntary guidelines**, not a statute. Do not call them "a new AI law". | https://ssrana.in/articles/meity-unveils-indias-approach-towards-regulating-artificial-intelligence/ ; https://lexplosion.in/meity-issues-india-ai-governance-guidelines-introducing-a-coordinated-oversight-structure/ | Nov 2025 |
| A7 | "Three new AI institutions" | TRUE WITH CORRECTION | The guidelines name three bodies: AI Governance Group (AIGG, proposed), Technology and Policy Expert Committee (TPEC, proposed) and the AI Safety Institute (AISI, already set up under the IndiaAI Mission). So two are proposed and one already existed; "three new" is loose. | https://lexplosion.in/meity-issues-india-ai-governance-guidelines-introducing-a-coordinated-oversight-structure/ | Nov 2025 |
| A8 | "Even the Supreme Court has a draft AI policy" | TRUE WITH CORRECTION | The Supreme Court published draft regulations on AI use in courts on 3 Jun 2026; comments closed 20 Jun 2026. AI may assist; judges decide; lawyers must disclose AI use in filings. Not shown as final. | https://www.livelaw.in/top-stories/supreme-court-publishes-draft-regulations-on-ai-use-in-judiciary-invites-feedback-536746 ; https://www.scconline.com/blog/post/2026/06/05/sc-issues-draft-ai-regulations-for-courts/ | 3 to 5 Jun 2026 |
| A9 | "RBI replaced its rulebook in one day: 244 Master Directions, 9,445 circulars withdrawn" | TRUE WITH CORRECTION | On 28 Nov 2025 RBI issued 244 Master Directions and withdrew 9,445 circulars (3,809 folded in, 5,673 repealed as obsolete). Deputy Governor Murmu: "from a regulatory standpoint, nothing has changed ... the repetition is gone." So it is a **consolidation**, not new rules. Say "consolidated", not "replaced" or "rewrote". | https://www.newsonair.gov.in/rbi-repeals-9000-circulars-consolidates-rules-into-244-master-directions-to-ease-compliance/ ; https://www.taxmann.com/post/blog/rbi-withdraws-9445-circulars-following-consolidation-into-244-master-directions | 28 Nov 2025 |
| A10 | Payment Aggregator rules: net worth Rs 25 crore | TRUE WITH CORRECTION | RBI (Regulation of Payment Aggregators) Directions 2025, 15 Sep 2025: Rs 15 crore at application, Rs 25 crore by the end of the third financial year after authorisation (existing PAs: by 31 Mar 2028 under the earlier circular). | https://www.outlookbusiness.com/news/rbi-issues-new-master-directions-for-payment-aggregators-rules-take-effect-immediately ; https://hdfcsky.com/news/rbi-tightens-rules-for-payment-aggregators-set-rs-25-crore | Sep 2025 |
| A11 | Digital Lending Directions: KFS before signing, DLG capped at 5% | TRUE WITH CORRECTION | RBI (Digital Lending) Directions 2025, 8 May 2025 (RBI/2025-26/36), replace the 2022 guidelines and 2023 DLG guidelines. KFS before the loan is finalised: confirmed. DLG cap of 5% of the loan portfolio: given by one secondary source; check the RBI text before printing. | https://www.mondaq.com/india/fin-tech/1636908/digital-lending-directions-2025 ; https://knallp.com/?p=6652 | May 2025 |
| A12 | "28% GST on gaming upheld, with Rs 1 lakh crore in disputes" | TRUE | Supreme Court (Pardiwala and Mahadevan JJ.) upheld 28% GST on online money gaming on 27 May 2026 and let past demands proceed (the 2023 change was treated as clarificatory). Demands: "over Rs 1 lakh crore" (estimates run to Rs 1.5 lakh crore). | https://www.businesstoday.in/latest/corporate/story/supreme-court-upholds-28-gst-on-online-gaming-rs1-lakh-cr-tax-burden-looms-533671-2026-05-27 ; https://entrackr.com/news/gaming-firms-to-face-over-rs-1-lakh-cr-tax-blow-as-supreme-court-backs-28-gst-11880150 | 27 May 2026 |
| A13 | Promotion and Regulation of Online Gaming Act 2025 "banned real-money games" | TRUE WITH CORRECTION | Act passed Aug 2025, but it and the Online Gaming Rules 2026 (notified 22 Apr 2026) came into force on **1 May 2026**, not Oct 2025. Bans online money games of skill or chance, their ads and payment processing; e-sports and social games allowed. | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2256973 ; https://www.scconline.com/blog/post/2026/04/23/meity-notified-enforcement-of-promotion-regulation-online-gaming-act-2025/ | Apr 2026 |
| A14 | A High Court held Section 79 is "not a free for all safe harbour" | UNVERIFIED | Phrase not found in any searched source. Closest real ruling: Karnataka High Court, X Corp v. Union of India (Sahyog portal), Justice M. Nagaprasanna, 24 Sep 2025: safe harbour is conditional on due diligence; "social media can't be left in anarchic freedom" (headline). X Corp's appeal is pending before a Division Bench. Use the case and the paraphrase, not the quote. | https://www.business-standard.com/india-news/karnataka-hc-dismisses-x-plea-sahyog-portal-social-media-regulation-125092401218_1.html ; https://www.medianama.com/2026/03/223-karnataka-hc-centre-response-x-challenge-sahyog-portal/ | 24 Sep 2025 ; Mar 2026 |
| A15 | "Rules that are 18 months old" | TRUE WITH CORRECTION | Most items fall between May 2025 and Jun 2026 (lending May 2025, PA Sep 2025, AI guidelines and RBI and DPDP Rules Nov 2025, IT Rules Feb 2026, gaming May 2026, SC AI draft Jun 2026). The DPDP Act itself is from Aug 2023. "In the last 18 months" is fair as a framing; "nobody has experience" is opinion. | (rows above) | |

## B. Market size and demand

| # | Claim as written | Verdict | Correct version | Source | Source date |
|---|---|---|---|---|---|
| B1 | Digital economy 11.74% of national income (Rs 31.64 lakh crore), nearly one-fifth of GDP by 2030 (MeitY) | TRUE WITH CORRECTION | Correct figures, but they are for **2022-23**, and "one-fifth by 2030" is a projection. MeitY report "Estimation and Measurement of India's Digital Economy", Jan 2025. Write "in 2022-23". | https://inc42.com/?p=496288 ; https://www.storyboard18.com/digital/by-2030-digital-economy-to-fuel-20-of-indias-national-income-meity-54346.htm | Jan 2025 |
| B2 | Indian legal market about USD 27.95 billion heading to USD 42 billion by 2034, "with tech law and data privacy named as new practice areas" | TRUE WITH CORRECTION | One paid market report (IMARC): USD 27.95 bn (2025) to USD 42.09 bn (2034), only 4.66% a year. Mordor Intelligence puts the same market at USD 2.49 bn, so the size is contested. IMARC's named drivers are digital transformation, AI legal tech, Tele-Law and regulatory complexity; "tech law and data privacy named" was **not confirmed**. Weak claim; avoid. | https://www.imarcgroup.com/india-legal-services-market | 2026 edition |
| B3 | "Rs 314 lakh crore moved through UPI last year"; 24,000 crore transactions | TRUE | FY 2025-26: 24,161.69 crore transactions worth Rs 314.23 lakh crore (Lok Sabha answer), up from Rs 260.56 lakh crore in FY25. Say "in 2025-26". | https://www.tribuneindia.com/news/business/upi-user-base-reaches-55-49-crore-fy26-transactions-rise-to-24162-crore-worth-rs-314-lakh-crore/ | 2026 |
| B4 | "Over a thousand fintech legal roles are open"; DMI Finance role with 200+ applicants | UNVERIFIED | Likely from a job-board screenshot (not read). No source found. Page only with a dated screenshot. | not searched | |
| B5 | Tech industry "about USD 315 billion (Nasscom FY26)" | UNVERIFIED | Not searched (budget). | not searched | |
| B6 | Fintechs raised USD 2 billion Jan to Jun 2026, up 42%; e-commerce USD 90 bn to 250 bn by 2030 | UNVERIFIED | Not searched. | not searched | |

## C. Startups, deep tech and government money

| # | Claim as written | Verdict | Correct version | Source | Source date |
|---|---|---|---|---|---|
| C1 | India has "3,600+ deep tech startups" | TRUE WITH CORRECTION | Nasscom-Zinnov, Jun 2024 (data to 2023): about 3,600, 6th globally. Later reports say about 4,000 (2024). Date it: "3,600 (Nasscom, 2024)". | https://www.angelone.in/news/economy/india-ranks-sixth-globally-deeptech-startup-ecosystems ; https://www.siasat.com/india-has-3600-deeptech-startups-ranks-sixth-globally-nasscom-3047824/amp/ | Jun 2024 |
| C2 | "A Rs 1 lakh crore fund, soft long-term loans at just 3 to 4% interest for 12 to 15 years, and even equity investment of up to 25%" | TRUE WITH CORRECTION | Cabinet approved the RDI Scheme (Rs 1 lakh crore) on 1 Jul 2025. Terms via the Technology Development Board as fund manager: loans at 3 to 4% for 12 to 15 years, up to 50% of project cost, no collateral; equity "up to 25% of assistance sought", not 25% of the company. Conditions: IP stays in India, Indian control. | https://www.pmindia.gov.in/en/news_updates/cabinet-approves-research-development-and-innovation-rdi-scheme-to-scale-up-research-development-and-innovation-in-strategic-and-sunrise-domains/ ; https://tdb.gov.in/rdi_slfm ; https://www.businesstoday.in/latest/economy/story/indias-deep-tech-moment-22-projects-get-backing-under-rs1-lakh-crore-rdi-fund-558642-2026-09-29 | Jul 2025 ; 29 Sep 2026 |
| C3 | Warm-up: "the first 22 projects are now backed" under RDI | TRUE | TDB approved 22 projects, total project cost Rs 4,744 crore, RDI funding Rs 2,192 crore; 14 are startups. | https://www.businesstoday.in/latest/economy/story/indias-deep-tech-moment-22-projects-get-backing-under-rs1-lakh-crore-rdi-fund-558642-2026-09-29 | 29 Sep 2026 |
| C4 | "A record 55,200 startups were recognised in FY 2025-26" | TRUE | More than 55,200 in FY26, the highest since 2016, up about 52% from about 36,400 in FY25. | https://inc42.com/buzz/centre-recognises-record-55200-startups-in-fy26/ | Apr 2026 |
| C5 | "India's 2 lakh+ startups" | TRUE WITH CORRECTION | 2,40,092 DPIIT-recognised by 30 Jun 2026 (Lok Sabha). Say "2.4 lakh". | https://inc42.com/buzz/centre-recognises-record-55200-startups-in-fy26/ ; https://influence360.co.uk/dpiit-recognised-startups-cross-2-4-lakh-as-india-adds-16334-in-q1/ | Apr to Aug 2026 |
| C6 | "92,000 recognised startups" | FALSE (outdated) | That count is from about early 2023. Current: 2.4 lakh (Jun 2026). | as C5 | |
| C7 | "About 50% of startups are in Tier 2 and 3 cities" | UNVERIFIED | Not searched. Background: DPIIT has said "nearly half"; check before use. | not searched | |

## D. Legal tech, GCCs, ESOPs

| # | Claim as written | Verdict | Correct version | Source | Source date |
|---|---|---|---|---|---|
| D1 | "1,000+ Indian legal tech startups" | TRUE | Tracxn lists 1,215 legal tech startups in India (94 funded, 1 unicorn). | https://tracxn.com/d/explore/legal-tech-startups-in-india/__E1QQRMw4NEjHwC6iLnpj5s5God9ZktQAeqwocPbdMfk | Sep 2026 |
| D2 | "3,800+ in the US" | UNVERIFIED | No source found for the figure. | (searched, none) | |
| D3 | "USD 6 billion raised last year" | TRUE WITH CORRECTION | LegalComplex: USD 5.99 bn, global, 2025 (a record). Crunchbase says USD 4.08 bn, Tracxn USD 4.44 bn. Write "about USD 4 to 6 billion worldwide in 2025, a record" or cite LegalComplex by name. | https://www.artificiallawyer.com/2026/01/06/legal-tech-raised-6bn-in-2025-as-ai-boom-shows-divisions/ ; https://news.crunchbase.com/venture/ai-legal-tech-investment-all-time-high-filevine/ | 6 Jan 2026 |
| D4 | "Sirion is India's first legal tech unicorn" | UNVERIFIED (likely FALSE) | Sirion (founded Delhi 2012, now US-headquartered) was valued at about USD 1 bn in 2024 and in Haveli's 2026 buyout. No source calls it India's first legal tech unicorn. Background: Icertis (Pune-founded contract software) passed USD 1 bn in 2019, earlier. Do not use "first". | https://www.globallegalpost.com/news/us-private-equity-firm-haveli-buys-majority-stake-in-legaltech-business-sirion-1089060174 | 2026 |
| D5 | Harvey: 2,400+ customers in 70+ countries; "Legal Engineer" roles are lawyers, not coders | TRUE WITH CORRECTION | Harvey's own site: 200,000+ lawyers at 2,400+ organisations in 70 countries (another source says 3,000+ by Sep 2026). Harvey's Legal Engineer role in Bengaluru asks for a qualified Indian advocate with 3+ years at a top-tier firm (sibling note). Self-reported figures. | https://www.harvey.ai/company ; https://www.harvey.ai/company/careers/35f57b4f-2c57-4060-9a32-d53273d6ce7e | 2026 |
| D6 | "2,117 GCCs employing 23.6 lakh" | TRUE | Nasscom-Zinnov, FY26: 2,117 GCCs, about 2.36 million people. | https://www.businesstoday.in/technology/news/story/the-big-boom-how-indias-gcc-story-hits-2030-target-4-years-early-530265-2026-05-07 ; https://flexiple.com/gcc/statistics | May 2026 |
| D7 | "5,000 GCCs by 2030" | FALSE (unsupported) | Published 2030 projections: 2,100 to 2,200 (Nasscom-Zinnov), 2,400+ (ANSR), 2,500+ (JLL). None says 5,000. | https://www.businessofgcc.com/gcc-data/reports/india-gcc-compensation-pulse-2026 ; https://wework.co.in/blogs/global-capability-centres-india-setup-guide/ | 2026 |
| D8 | GCC "legal roles pay 25 to 30% above market" | TRUE WITH CORRECTION | TeamLease (Nov 2025): GCC **average salaries across all roles** are 25 to 30% above the national average. Not a legal-role figure. No legal-specific premium found. | https://caalley.com/news-updates/indian-news/gccs-in-india-drive-10-4-mn-jobs-30-higher-pay-2-000-legal-obligations (sibling note) | Nov 2025 |
| D9 | GCCs face "500+ legal obligations" | TRUE WITH CORRECTION | Same TeamLease report (sibling note says 500+ per GCC; the URL slug says 2,000). Re-open and quote the exact figure before use. | as D8 | Nov 2025 |
| D10 | "Coinbase's legal chief made USD 18 million in a year" | TRUE WITH CORRECTION | Paul Grewal's 2020 total compensation in Coinbase's S-1: USD 18,017,579, almost all stock and options at grant-date accounting value, not cash. Say "was granted pay valued at about USD 18 million in 2020". Page only. | https://www.sec.gov/Archives/edgar/data/1679788/000162828021003168/coinbaseglobalincs-1.htm ; https://news.bloomberglaw.com/us-law-week/coinbase-ipo-reveals-payday-for-legal-chief-hired-from-facebook | 2021 filing |
| D11 | "Swiggy's IPO made 500 employees crorepatis" (Rs 9,000 crore ESOPs) | TRUE WITH CORRECTION | Nov 2024 IPO. Reports: about 500 of 5,000 ESOP holders (current and former) worth Rs 1 crore+ at the upper price band; ESOP pool about Rs 9,000 crore. These were estimates at the price band, not a count. Not lawyer-specific. Page only. | https://www.outlookmoney.com/news/500-swiggy-employees-become-crorepati-as-ipo-unlocks-rs-9000-crore-worth-of-esops ; https://inc42.com/buzz/swiggy-ipo-500-employees-to-join-the-crorepati-club/amp | Nov 2024 |
| D12 | "Groww, Lenskart, Meesho, PhysicsWallah and Urban Company all listed in 2025" | TRUE | All five listed in 2025 (Urban Company Sep; Groww, Lenskart, PhysicsWallah Nov; Meesho Dec, per background). | https://globalventuring.com/corporate/asia/corporate-backed-indian-startups-waiting-to-ipo/ ; https://www.kotaksecurities.com/news/market-news/physics-wallah-ipo-growth-story-or-competitive-gamble | Nov 2025 |
| D13 | Lawyers holding ESOPs at Zomato, Paytm, PolicyBazaar "made more at IPO than top partners" | UNVERIFIED | Not searched; no named lawyer or figure given. Do not use. | not searched | |
| D14 | BW Legal World (Sep 2025): firms face "a shortage of professionals who combine legal and technical expertise" | TRUE WITH CORRECTION | Article "Tech And Data Experts Redefine Law Firms Hiring In India", late Sep 2025, quotes Cyril Shroff and Sahil Arora on the shortage (sibling note). Exact quoted wording not re-checked; paraphrase it. | https://www.bwlegalworld.com/article/tech-and-data-experts-redefine-law-firms-hiring-in-india-573255 | Sep 2025 |

## E. Jobs data

| # | Claim as written | Verdict | Correct version | Source | Source date |
|---|---|---|---|---|---|
| E1 | "Legal jobs grew 9% in August 2026 while overall hiring fell 10% (foundit)" | UNVERIFIED | Not searched. Sibling note: Naukri JobSpeak Sept 2026 shows white-collar hiring +2%, which sits oddly with "overall fell 10%". | https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-September-2026.pdf (context only) | Sep 2026 |
| E2 | "Legal specialist is #12 on LinkedIn's Jobs on the Rise 2026 list for India" | UNVERIFIED (likely FALSE) | Sibling research found no legal or privacy title on the India 2026 list (AI roles lead). Do not use. | (sibling note) | 2026 |
| E3 | "Tech startups have the highest fresher hiring outlook (93%, TeamLease EdTech)" | UNVERIFIED | Not searched. | not searched | |

## F. United States claims (none searched: budget ran out)

| # | Claim as written | Verdict | Background note (not a source) |
|---|---|---|---|
| F1 | 418,000 US law firms; 160,000 (1.6 lakh) with 0 to 20 staff | UNVERIFIED | Not searched. Check US Census County Business Patterns (NAICS 541110) for the firm count. |
| F2 | "1.6 lakh small law firms that each need 2 to 10 remote paralegals ... about 8 lakh paralegals. Only about 10,000 Indian lawyers do this work" | UNVERIFIED | The "need" is the brief's own multiplication, not a published figure. Do not use. |
| F3 | US legal market USD 380 to 422 billion in 2026; "USD 400 billion US legal market" | UNVERIFIED | Not searched. Market-research estimates vary widely. |
| F4 | "ABA Opinion 08-451 allows US lawyers to outsource work abroad if they supervise it" | UNVERIFIED | Background: ABA Formal Opinion 08-451 (Aug 2008) does permit outsourcing, including abroad, with competence, supervision, confidentiality and, in some cases, client consent. Very likely correct; cite the ABA text after checking. |
| F5 | "An Indian law graduate can sit the California Bar without a US LLM" | UNVERIFIED (likely needs correction) | Background: California lets a foreign-educated applicant sit without extra US study **only if admitted to practise in good standing** in the foreign jurisdiction (an enrolled advocate in India). A graduate not enrolled needs a year of study (usually an LLM) at a US law school. Check the State Bar of California rules before stating it. |
| F6 | "1,428 US court rulings flagged AI-made-up cases or quotes" | UNVERIFIED | Likely from Damien Charlotin's AI Hallucination Cases database, which counts decisions **worldwide**, not US only, and grows weekly. Quote it with the database name and date. |
| F7 | "79% of US legal staff use AI, but 53% have no AI policy" | UNVERIFIED | Not searched; source survey not named in the brief. |
| F8 | "USD 10 an hour is below what a US burger flipper earns" | UNVERIFIED (needs correction) | Background: the federal minimum wage is USD 7.25; many states and cities are higher (California fast food USD 20). True only for higher-wage states. Avoid. |
| F9 | Upwork "was free in 2020 and now charges for proposals" | UNVERIFIED (likely FALSE) | Background: Upwork began charging for Connects in 2019, before 2020. Check before use. |

## G. Deep tech warm-up email claims

The email names a source and date for each figure, which is good practice, but I could not open or
search them (budget). Re-check each against the named source before reuse on a page.

| # | Claim as written | Verdict | Note |
|---|---|---|---|
| G1 | Defence exports Rs 38,424 crore in 2025-26, up 62.66%; exporters 128 to 145 (ETV Bharat, 2 Apr 2026) | UNVERIFIED | Internally consistent: background FY25 figure Rs 23,622 crore x 1.6266 = Rs 38,424 crore. Likely correct; check PIB. |
| G2 | Army drone buying may exceed Rs 20,000 crore; 600+ drone makers (WION/Reuters, 3 Jun 2026) | UNVERIFIED | Email already labels it a projection. Keep that label. |
| G3 | IN-SPACe 113 authorisations to 52 non-government entities; about 440 space startups (News On AIR, 12 Aug 2026) | UNVERIFIED | Spaces brief says "113 licences to 52 private companies": use the email's wording ("authorisations", "non-government entities"). |
| G4 | Skyroot raised USD 60 million at USD 1.1 billion (Free Press Journal, May 2026) | UNVERIFIED | Not searched. |
| G5 | 12 chip projects approved, 3 in commercial production (Business Today, 17 Sep 2026) | UNVERIFIED | Spaces brief says only "12 projects approved"; consistent. |
| G6 | Tonbo Imaging DRHP filed 4 Aug 2026; 28,000+ systems in 24 countries (Groww) | UNVERIFIED | Check on SEBI's DRHP list; a broker blog is a weak source. |
| G7 | Deep tech funding USD 2.3 billion in 2025, up 37%, AI 91% (People Matters on Nasscom-Zinnov) | UNVERIFIED | Not searched. |
| G8 | National Quantum Mission cohort 17 startups (Business Today, 9 Apr 2026) | UNVERIFIED | Not searched. |
| G9 | RDI Rs 1 lakh crore approved Jul 2025; first 22 projects backed | TRUE | See C2 and C3. |
| G10 | IndiaAI compute portal 38,000+ GPUs from Rs 65 an hour (Inc42, Sep 2025) | UNVERIFIED | Background: consistent with IndiaAI Mission statements in 2025. Dated; check for a 2026 count. |

## H. Other script and brief claims

| # | Claim as written | Verdict | Correct version or note |
|---|---|---|---|
| H1 | Criminal cases instituted 81.6 lakh (2018) to 62.4 lakh (2025), "People's Archive of Rural India's annual report" | UNVERIFIED, attribution almost certainly wrong | PARI is a rural journalism archive and publishes no court statistics. The table repeats 62,41,569 for 2023 and 2025, a copy error. A real series would come from the National Judicial Data Grid (cases instituted) or NCRB "Crime in India" (cases registered, which is a different measure). Not searched (budget). Do not use until rebuilt from NJDG or NCRB. |
| H2 | "MP High Court had to direct a minimum stipend for junior advocates" | UNVERIFIED | Not searched. |
| H3 | 99.9% uptime allows about 43 minutes of downtime a month; 99.99% about 4 minutes | TRUE (arithmetic) | 0.1% of a 30-day month = 43.2 minutes; 0.01% = 4.3 minutes. |
| H4 | 13 banned dark patterns (2023 guidelines) | UNVERIFIED | Background: the CCPA Guidelines for Prevention and Regulation of Dark Patterns, 2023 list 13 specified patterns. Likely correct; not searched. |
| H5 | 1 million+ Shopify stores in the US | UNVERIFIED | Not searched. |
| H6 | "Tech industry ... can be expected to employ more lawyers than the entire bar does today" | UNVERIFIED (opinion) | No data. Do not use. |
| H7 | "A 30-year veteran and a fresh graduate start on the same line" | Opinion | Defensible as framing because the rules date from 2025 and 2026 (see A15), but it is not a fact. |

---

## Safe to use on a landing page (15 strongest verified facts)

Each one in the corrected wording, with its source. All are page-level facts (dates and figures stay
off the ad face per house rules).

1. **DPDP timeline.** The DPDP Rules were notified on 13 Nov 2025. Consent managers come under the
   rules from 13 Nov 2026, and most duties for every business (notice, consent, security, breach
   reporting) start on 13 May 2027.
   PIB, 17 Nov 2025: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf
2. **DPDP penalty.** Under the DPDP Act, failing to protect personal data can cost a company up to
   Rs 250 crore per breach.
   Storyboard18, Nov 2025: https://www.storyboard18.com/advertising/dpdp-enforcement-begins-penalties-up-to-%E2%82%B9250-cr-breach-put-entire-digital-ecosystem-on-high-alert-84226.htm
3. **IT Rules 2026.** From 20 Feb 2026, platforms must remove content within 3 hours of a government
   or court order (it was 36 hours) and must label AI-generated audio and video.
   LiveLaw, Feb 2026: https://www.livelaw.in/top-stories/centre-notifies-it-rules-amendment-to-regulate-ai-generated-and-synthetic-content-522623
4. **AI governance.** MeitY released the India AI Governance Guidelines on 5 Nov 2025 (voluntary).
   S.S. Rana, Nov 2025: https://ssrana.in/articles/meity-unveils-indias-approach-towards-regulating-artificial-intelligence/
5. **Courts and AI.** The Supreme Court published draft rules on AI use in courts on 3 Jun 2026;
   they require lawyers to disclose AI use in filings.
   LiveLaw, Jun 2026: https://www.livelaw.in/top-stories/supreme-court-publishes-draft-regulations-on-ai-use-in-judiciary-invites-feedback-536746
6. **RBI consolidation.** On 28 Nov 2025 the RBI consolidated its rules into 244 Master Directions
   and withdrew 9,445 circulars.
   News On AIR, 28 Nov 2025: https://www.newsonair.gov.in/rbi-repeals-9000-circulars-consolidates-rules-into-244-master-directions-to-ease-compliance/
7. **Gaming GST.** On 27 May 2026 the Supreme Court upheld 28% GST on online money gaming, which
   revives tax demands of over Rs 1 lakh crore.
   Business Today, 27 May 2026: https://www.businesstoday.in/latest/corporate/story/supreme-court-upholds-28-gst-on-online-gaming-rs1-lakh-cr-tax-burden-looms-533671-2026-05-27
8. **Gaming law.** The Promotion and Regulation of Online Gaming Act 2025 and its Rules came into
   force on 1 May 2026, banning online money games.
   PIB: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2256973 ; SCC Online, 23 Apr 2026: https://www.scconline.com/blog/post/2026/04/23/meity-notified-enforcement-of-promotion-regulation-online-gaming-act-2025/
9. **Fintech scale.** UPI carried 24,162 crore payments worth Rs 314 lakh crore in 2025-26.
   The Tribune (Lok Sabha data), 2026: https://www.tribuneindia.com/news/business/upi-user-base-reaches-55-49-crore-fy26-transactions-rise-to-24162-crore-worth-rs-314-lakh-crore/
10. **Digital economy.** MeitY estimates the digital economy at 11.74% of national income in 2022-23
    (Rs 31.64 lakh crore) and projects nearly one-fifth by 2030.
    Inc42, Jan 2025: https://inc42.com/?p=496288
11. **Startups.** A record 55,200 startups were recognised in 2025-26; India had 2.4 lakh recognised
    startups by 30 Jun 2026.
    Inc42, 2026: https://inc42.com/buzz/centre-recognises-record-55200-startups-in-fy26/
12. **GCCs.** India has 2,117 global capability centres employing about 23.6 lakh people (FY26).
    Business Today, May 2026: https://www.businesstoday.in/technology/news/story/the-big-boom-how-indias-gcc-story-hits-2030-target-4-years-early-530265-2026-05-07
13. **Legal tech in India.** Tracxn tracks 1,215 legal tech startups in India.
    Tracxn, Sep 2026: https://tracxn.com/d/explore/legal-tech-startups-in-india/__E1QQRMw4NEjHwC6iLnpj5s5God9ZktQAeqwocPbdMfk
14. **Legal engineers are lawyers.** Harvey (used by 2,400+ organisations in 70 countries, by its own
    count) hires Legal Engineers in Bengaluru who must be qualified Indian advocates.
    Harvey: https://www.harvey.ai/company ; https://www.harvey.ai/company/careers/35f57b4f-2c57-4060-9a32-d53273d6ce7e
15. **Deep tech money with legal strings.** The Rs 1 lakh crore RDI Fund (approved Jul 2025) has
    backed its first 22 projects with loans at 3 to 4% for up to 15 years, on condition the IP stays
    in India.
    Business Today, 29 Sep 2026: https://www.businesstoday.in/latest/economy/story/indias-deep-tech-moment-22-projects-get-backing-under-rs1-lakh-crore-rdi-fund-558642-2026-09-29

Also usable with care (page only, corrected wording): Payment Aggregator net worth (A10), Digital
Lending KFS (A11), Coinbase USD 18 million as 2020 grant-date pay (D10), Swiggy ESOP estimate (D11),
3,600 deep tech startups dated 2024 (C1), BW Legal World shortage as a paraphrase (D14), uptime maths
(H3).

## Do not use

False, outdated or unverifiable. Each needs a real source before it goes anywhere.

- "The DPDP deadline in November 2026 is weeks away" for ordinary companies (A2). Nov 2026 is
  consent managers only; most duties start 13 May 2027.
- "RBI replaced / rewrote its rulebook" (A9). RBI says nothing changed in substance. Say "consolidated".
- "Section 79 is not a free for all safe harbour" as a quote (A14). Not found. Cite Karnataka HC,
  X Corp v. Union of India, 24 Sep 2025, as a paraphrase.
- "Three new AI institutions" (A7). Two are proposed; the AI Safety Institute already existed.
- Online Gaming Act "in force from Oct 2025" (A13). It came into force 1 May 2026.
- Legal market USD 27.95 bn to 42 bn "with tech law and data privacy named" (B2). One contested
  estimate; the tech law naming was not confirmed.
- "5,000 GCCs by 2030" (D7). No projection says this.
- GCC "legal roles pay 25 to 30% above market" (D8). The figure is for all GCC roles.
- "Sirion is India's first legal tech unicorn" (D4). Unconfirmed; Icertis was earlier.
- "3,800+ US legal tech startups" (D2). No source.
- "92,000 recognised startups" (C6). Outdated; 2.4 lakh now.
- "Legal specialist #12 on LinkedIn Jobs on the Rise 2026" (E2). Not found on the list.
- Foundit "+9% legal jobs" (E1), TeamLease "93%" (E3), Nasscom "USD 315 bn" (B5), fintech funding
  and e-commerce projections (B6), "1,000+ fintech legal roles" (B4): unverified.
- Criminal cases table credited to "People's Archive of Rural India" (H1). Wrong source and a
  duplicated figure. Rebuild from NJDG or NCRB.
- ESOP "lawyers made more than top partners" (D13); "tech will employ more lawyers than the bar"
  (H6): no data.
- All US figures (F1 to F9): unverified this session. In particular, "8 lakh paralegals needed" is
  the brief's own arithmetic; "USD 10 is below a burger flipper" is false against the USD 7.25 federal
  minimum; "Upwork was free in 2020" is likely false; the California Bar line must say "enrolled
  advocates", not "law graduates".
- Deep tech email figures G1 to G8 and G10: plausible and sourced by name in the email, but not
  checked here. Re-verify before reuse.

## Still to check (needs a fresh search budget)

US: law firm count (Census NAICS 541110), US legal market size, ABA 08-451 text, State Bar of
California foreign-applicant rule, Charlotin database count, the 79% / 53% survey, Upwork Connects
date. India: Foundit Aug 2026, LinkedIn Jobs on the Rise India 2026, TeamLease 93%, Nasscom FY26,
NJDG criminal institution series, MP High Court stipend order, 50% Tier 2/3 startups, dark patterns
count. Deep tech: G1 to G8, G10.
