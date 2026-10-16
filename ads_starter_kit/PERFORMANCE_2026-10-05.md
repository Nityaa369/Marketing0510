# Meta and Google performance, as pulled 5 Oct 2026

This file is a **dated snapshot**, not a live view. It exists so a new person can see what
the account actually costs before writing an ad, instead of guessing from doctrine. Re-pull
it rather than trusting it after a week: `python ad-analysis-shared/pull_ads.py --list`,
then `python daily_report.py`.

**How these numbers were made.** Meta Graph API v21.0 at ad level, through the System User
token in `ad-analysis-shared/.env` (SOP/03: the token, never the Ads MCP, because the MCP
cannot read LawSikho Ad Account 4, which carries live bootcamp spend). All rupee figures
**include 18% GST** - Meta returns net and the puller grosses it up. Windows are the last
7 days and the last 30 days to 2026-10-05.

**How to read a cost column.** Each campaign is judged on one result type and never a blend:
**buyers** where the camp sells and **leads/registrations** where it registers (the rule in
`daily_report.py`: buyers if buyers >= leads, else leads). A Rs 10 camp still counts a buyer.
SOP/03: **never judge an ad on fewer than 20 results** - every per-ad table below prints n,
and thin rows are left out of the ranking rather than quietly averaged in.

Coverage: 19 ad accounts read, 14 with no spend in the window. Five carry everything:
Skill Arbitrage, Skill Arbitrage_2, Community (ASHWIN), LawSikho Ad Account 4,
SkillArbitrage_V.

---

## 1. Day by day, all rupee accounts, last 7 days

| Day | Spend (incl GST) | Buyers | CPP | Leads | CPL |
|---|---|---|---|---|---|
| 2026-09-28 | Rs 379,573 | 1,239 | Rs 306 | 2,580 | Rs 147 |
| 2026-09-29 | Rs 350,537 | 1,115 | Rs 314 | 2,005 | Rs 175 |
| 2026-09-30 | Rs 411,579 | 1,350 | Rs 305 | 2,044 | Rs 201 |
| 2026-10-01 | Rs 387,310 | 1,414 | Rs 274 | 1,790 | Rs 216 |
| 2026-10-02 | Rs 405,913 | 1,320 | Rs 308 | 2,030 | Rs 200 |
| 2026-10-03 | Rs 312,817 | 1,247 | Rs 251 | 1,173 | Rs 267 |
| 2026-10-04 | Rs 339,286 | 1,055 | Rs 322 | 1,160 | Rs 292 |
| 2026-10-05 | Rs 133,416 | 396 | Rs 337 | 414 | Rs 322 |
| **7-day total** | **Rs 2,720,431** | **9,136** | **Rs 298** | **13,196** | **Rs 206** |

The last row is a **part day** - the pull ran mid-day on 5 Oct, so its spend and its cost
are both incomplete. Never judge an ad or a day on a part-day row.

Buyers and leads sit side by side here only to show the shape of the week. Do not divide one
total by the other: free-registration camps and selling camps are both in it.

---

## 2. Campaign par, last 7 days against last 30 days

`Cost` is the campaign's own cost per result - the number a new ad in that campaign has to
beat. A campaign thin in the 7-day column but heavy in the 30-day one is winding down.

| Campaign | Account | Judged on | 7d spend | 7d n | 7d cost | 30d n | 30d cost |
|---|---|---|---|---|---|---|---|
| SeniorConsulting_BC_3-5Oct2026_CBO_v1 | Skill Arbitrage | buyers | Rs 234,466 | 2,092 | **Rs 112** | 5,222 | Rs 136 |
| US Accounting_AND_Bookkeeping_Oct_10th | Skill Arbitrage | leads | Rs 214,512 | 5,391 | **Rs 40** | 12,943 | Rs 36 |
| CorpFinance_bootcamp_17-19Oct_CBO | Skill Arbitrage | buyers | Rs 213,485 | 823 | **Rs 259** | 1,507 | Rs 249 |
| RID + ID BC 10-12 Oct 2026_CBO_LEAD | Skill Arbitrage | leads | Rs 212,167 | 2,233 | **Rs 95** | 6,219 | Rs 74 |
| TechLaw_BC_24-26Oct2026_CBO | LawSikho Ad Account 4 | buyers | Rs 209,295 | 1,001 | **Rs 209** | 1,181 | Rs 242 |
| WomenAI_FREE_3-5Oct-2026_BC_CBO_v1 | Skill Arbitrage_2 | leads | Rs 205,512 | 5,559 | **Rs 37** | 17,850 | Rs 36 |
| Academic_Writing_BC_24-26Oct2026_CBO | Skill Arbitrage | buyers | Rs 198,236 | 1,090 | **Rs 182** | 1,090 | Rs 182 |
| DataPrivacy_bootcamp_17-19Oct_CBO | Skill Arbitrage | buyers | Rs 166,821 | 888 | **Rs 188** | 1,611 | Rs 198 |
| StrategicHR_bootcamp_31Oct-2Nov_CBO | Skill Arbitrage | buyers | Rs 162,832 | 1,044 | **Rs 156** | 1,298 | Rs 157 |
| SA[Community]_ContractDrafting_2nd_July_2026 | Community (ASHWIN) | buyers | Rs 130,181 | 245 | **Rs 531** | 1,115 | Rs 480 |
| Sa_community_Legalai_13th_june | Community (ASHWIN) | buyers | Rs 115,420 | 318 | **Rs 363** | 1,133 | Rs 396 |
| PK_[21day_Community]_CriminalLitigation_9/May | Community (ASHWIN) | buyers | Rs 113,461 | 326 | **Rs 348** | 1,492 | Rs 309 |
| Independent Director Community v5 13 July | SkillArbitrage_V | buyers | Rs 112,425 | 353 | **Rs 318** | 1,384 | Rs 336 |
| M&A_14day[Community]_4june | Community (ASHWIN) | buyers | Rs 101,047 | 157 | **Rs 644** | 643 | Rs 657 |
| SA_SQE community_JULY | Community (ASHWIN) | buyers | Rs 94,178 | 149 | **Rs 632** | 525 | Rs 751 |
| [Community]_14Day_Arbitration_12Sep | Community (ASHWIN) | buyers | Rs 87,711 | 95 | **Rs 923** | 325 | Rs 831 |
| Community_Women _AI_June | Community (ASHWIN) | buyers | Rs 87,432 | 168 | **Rs 520** | 805 | Rs 447 |
| Meta - NCA - Oct 31-2 Nov Bootcamp - CBO Sales | LawSikho Ad Account 4 | buyers | Rs 59,078 | 177 | **Rs 334** | 177 | Rs 334 |

### Non-rupee accounts

None spent in this window. Never gross a USD or GBP figure up by 18% or add it into
a rupee total - `pull_ads.py` warns when a match spans currencies.

---

## 3. Which creatives are carrying it, last 30 days

Per campaign, the ads that cleared 20 results, cheapest first. This is the table that should
decide what the next ad looks like: the reader and the layout in the cheap rows are the ones
to build from, and `python -m adkit.corpus --like "<reader>"` pulls their copy. Ads that
never cleared 20 results are counted in the header line, not ranked - they were starved, not
beaten.

### MAIN - Academic Writing (Global career as academic content writer)

*Par: Rs 170 per buyer over 30 days. 25 of 138 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| acw_sep26_w2_14_medical_researchers | Rs 91,057 | 688 | **Rs 132** | 0.78x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249647794400716) |
| acw_sep26_09_assistant_professors | Rs 27,861 | 189 | **Rs 147** | 0.87x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249599811800716) |
| acw_sep26_socsci_01_social_science_researchers | Rs 8,407 | 57 | **Rs 147** | 0.87x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249600124250716) |
| acwr_01_homemaker | Rs 27,982 | 182 | **Rs 154** | 0.90x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249338866760716) |
| acw_sep26_w2_30_teachers_upskilling | Rs 18,461 | 113 | **Rs 163** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249647806490716) |
| acw_obj_teachers_masters_a05 | Rs 48,866 | 299 | **Rs 163** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448864160716) |
| *(16 mid-table ads omitted)* | | | | | |
| acw_sep26_ten_14_medical_researchers | Rs 8,279 | 40 | **Rs 207** | 1.22x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249647831100716) |
| acw_obj_women_phd_w_a14 | Rs 12,228 | 58 | **Rs 211** | 1.24x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448869900716) |
| acw_sep26_33_quiz_women_academia | Rs 6,424 | 26 | **Rs 247** | 1.45x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249599813620716) |

### IP law (Main Bootcamp)

*Par: Rs 253 per buyer over 30 days. 10 of 67 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| IPWR_R3_women_lawyers | Rs 8,635 | 43 | **Rs 201** | 0.79x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915480270692) |
| IPWR_R3_lawgrads | Rs 19,134 | 88 | **Rs 217** | 0.86x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915476850692) |
| IPWR_R1_women_lawyers | Rs 56,712 | 243 | **Rs 233** | 0.92x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915452350692) |
| IPWR_R1_lawgrads | Rs 286,194 | 1,163 | **Rs 246** | 0.97x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915450350692) |
| IPWR_R1_become_paralegal | Rs 51,446 | 209 | **Rs 246** | 0.97x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915459320692) |
| IPWR_R3_careerbreak | Rs 100,072 | 403 | **Rs 248** | 0.98x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915487830692) |
| IPWR_R1_lawyer_moms | Rs 45,710 | 183 | **Rs 250** | 0.99x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249915453710692) |
| iplaw_sep26_meme_mm02_lawgrads_2016 | Rs 76,602 | 299 | **Rs 256** | 1.01x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250239961680692) |
| iplaw_sep26_toon_pt04_lawyer_moms | Rs 47,670 | 172 | **Rs 277** | 1.10x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250197372850692) |
| iplaw_sep26_toon_pt03_careerbreak | Rs 16,423 | 58 | **Rs 283** | 1.12x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250197372320692) |

### SeniorConsulting_BC_3-5Oct2026_CBO_v1

*Par: Rs 136 per buyer over 30 days. 39 of 152 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| SC_Oct3|w9_21_telecom | Rs 5,722 | 68 | **Rs 84** | 0.62x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249765221080716) |
| SC_Oct3|dos_quality_stamp | Rs 4,560 | 54 | **Rs 84** | 0.62x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249761730270716) |
| SC_Oct3|w9_06_it_managers | Rs 25,535 | 282 | **Rs 91** | 0.67x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249761783780716) |
| SC_Oct3|w9_20_hospital_admin | Rs 70,112 | 773 | **Rs 91** | 0.67x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249764178320716) |
| SC_Oct3|w9_17_construction_pm | Rs 36,663 | 399 | **Rs 92** | 0.68x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249764172220716) |
| SC_Oct3|w9_22_freight_shipping | Rs 17,907 | 192 | **Rs 93** | 0.69x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249765223930716) |
| *(30 mid-table ads omitted)* | | | | | |
| SC_Oct3|flm_02_banker_farewell | Rs 11,594 | 36 | **Rs 322** | 2.38x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249787331000716) |
| SC_Oct3|sc3_01_ca_startup | Rs 13,281 | 41 | **Rs 324** | 2.39x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249572656960716) |
| SC_Oct3|sc8_12_factory_labour | Rs 24,312 | 69 | **Rs 352** | 2.60x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249646977080716) |

### US_Corporate_Law_BC_19-21Sep2026

*Par: Rs 258 per buyer over 30 days. 12 of 94 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| pc_us_corporate_law_paychart_sep19 | Rs 11,870 | 66 | **Rs 180** | 0.70x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249808420290692) |
| uscl_sep19_icp28_law_lecturers | Rs 5,767 | 28 | **Rs 206** | 0.80x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249931436330692) |
| uscl_sep19_legal_stacked | Rs 8,186 | 38 | **Rs 215** | 0.84x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249917733140692) |
| uscl_sep19_icp38_cs_inhouse_mnc_compliance | Rs 35,132 | 161 | **Rs 218** | 0.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249931439500692) |
| uscl_sep19_icp44_wfh_lawyers | Rs 233,709 | 1,067 | **Rs 219** | 0.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249949493120692) |
| uscl_sep19_prestige_calbar | Rs 49,468 | 199 | **Rs 249** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250143686320692) |
| *(3 mid-table ads omitted)* | | | | | |
| uscl_sep19_icp39_ca_gcc_profile | Rs 27,643 | 88 | **Rs 314** | 1.22x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120249931440960692) |
| uscl_sep19_vs_photo_v2_inhouse_cs_mnc | Rs 11,090 | 29 | **Rs 382** | 1.48x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250186451590692) |
| uscl_sep19_video_growth_flexible_sideincome | Rs 45,041 | 117 | **Rs 385** | 1.49x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250143362520692) |

### WomenAI_FREE_3-5Oct-2026_BC_CBO_v1

*Par: Rs 36 per lead over 30 days. 19 of 45 ads that spent cleared 20 leads.*

| Ad | Spend | Leads | Cost | vs par | Link |
|---|---|---|---|---|---|
| WF_04_CPP90_R2_school_hours | Rs 1,157 | 53 | **Rs 22** | 0.61x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251892783460568) |
| WF_03_CPP89_N18_caregiver | Rs 1,403 | 51 | **Rs 28** | 0.77x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251892782260568) |
| WF_11_CPP112_R3_stop_waiting | Rs 105,352 | 3,518 | **Rs 30** | 0.83x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251892786670568) |
| WF_VID_03_two_hours | Rs 7,785 | 254 | **Rs 31** | 0.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251949617330568) |
| WF_ALT_03_N18_caregiver | Rs 1,802 | 57 | **Rs 32** | 0.88x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251892790080568) |
| WF_ALT_11_R3_stop_waiting | Rs 83,213 | 2,377 | **Rs 35** | 0.98x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251892792910568) |
| *(10 mid-table ads omitted)* | | | | | |
| WF_05_CPP91_W9_toon_freelance | Rs 1,011 | 21 | **Rs 48** | 1.34x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251892796020568) |
| WF_t1c_own_health | Rs 5,982 | 124 | **Rs 48** | 1.34x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251857692430568) |
| WF_t2a_commute | Rs 1,505 | 28 | **Rs 54** | 1.50x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251857725690568) |

### SA[Community]_ContractDrafting_2nd_July_2026

*Par: Rs 480 per buyer over 30 days. 10 of 43 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| cd_sprint – v1 | Rs 100,128 | 262 | **Rs 382** | 0.80x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247536152420605) |
| cd_sprint – v2 | Rs 13,858 | 33 | **Rs 420** | 0.87x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247537278040605) |
| cd_student pad | Rs 10,435 | 23 | **Rs 454** | 0.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247570733720605) |
| cd_contracts_grid | Rs 60,669 | 131 | **Rs 463** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246583529390605) |
| cd_women restart | Rs 35,281 | 69 | **Rs 511** | 1.07x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247570827940605) |
| cd_women remote | Rs 97,444 | 189 | **Rs 516** | 1.07x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247570905630605) |
| cd_structure_ad | Rs 117,083 | 225 | **Rs 520** | 1.08x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246584995200605) |
| cd_Route 21 | Rs 52,519 | 100 | **Rs 525** | 1.09x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247571900660605) |
| cd_notebook_yellow | Rs 12,795 | 24 | **Rs 533** | 1.11x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246583740120605) |
| cd_notebook | Rs 21,162 | 36 | **Rs 588** | 1.22x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246583739440605) |

### Global_Patent_Analysts_BC_19-21Sep2026

*Par: Rs 118 per buyer over 30 days. 24 of 54 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| pc_patent_w1_veterinary_s38 | Rs 15,755 | 207 | **Rs 76** | 0.65x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448889200716) |
| pc_patent_w1_microbiologists_s35 | Rs 32,341 | 333 | **Rs 97** | 0.82x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448886610716) |
| pc_patent_w1_food_technologists_s39 | Rs 31,276 | 311 | **Rs 101** | 0.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448889890716) |
| pc_patent_w2_chemical_process_e24 | Rs 7,356 | 73 | **Rs 101** | 0.86x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448900620716) |
| pc_patent_w2_biomedical_devices_e11 | Rs 13,025 | 125 | **Rs 104** | 0.88x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448895070716) |
| pc_patent_w1_chemistry_phd_s41 | Rs 8,505 | 81 | **Rs 105** | 0.89x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249448891830716) |
| *(15 mid-table ads omitted)* | | | | | |
| pc_patent_w3_women_msc_52 | Rs 54,305 | 352 | **Rs 154** | 1.31x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249449916040716) |
| pc_patent_mm01_govtexam_sep19 | Rs 16,032 | 91 | **Rs 176** | 1.50x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249280939980716) |
| pc_patent_break01_medrep_sep19 | Rs 6,496 | 25 | **Rs 260** | 2.21x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249284278970716) |

### US Accounting_AND_Bookkeeping_Oct_10th

*Par: Rs 36 per lead over 30 days. 9 of 49 ads that spent cleared 20 leads.*

| Ad | Spend | Leads | Cost | vs par | Link |
|---|---|---|---|---|---|
| usacc_oct10_search_us51_wfh_ended | Rs 345,581 | 10,125 | **Rs 34** | 0.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249677019660716) |
| usacc_oct10_w2_notice_us63_fifties | Rs 14,786 | 411 | **Rs 36** | 1.00x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249824796150716) |
| usacc_oct10_07_bcom_meme | Rs 36,201 | 871 | **Rs 42** | 1.15x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249675117320716) |
| usacc_oct10_search_us53_payroll | Rs 15,533 | 369 | **Rs 42** | 1.17x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249677022200716) |
| usacc_oct10_07_bcom_static | Rs 33,047 | 763 | **Rs 43** | 1.20x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249675118000716) |
| usacc_oct10_w2_notice_us67_wfh_ended | Rs 3,390 | 74 | **Rs 46** | 1.27x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249824800090716) |
| usacc_oct10_search_us49_ca_firm_staff | Rs 4,077 | 87 | **Rs 47** | 1.30x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249677019000716) |
| usacc_oct10_search_us43_small_town | Rs 3,164 | 66 | **Rs 48** | 1.33x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249677023850716) |
| usacc_oct10_search_us46_restarting | Rs 3,351 | 51 | **Rs 66** | 1.82x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249677013450716) |

### Independent Director Community v5 13 July

*Par: Rs 336 per buyer over 30 days. 13 of 33 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| Sortlist_test | Rs 15,603 | 75 | **Rs 208** | 0.62x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246498078320658) |
| Orange | Rs 11,212 | 51 | **Rs 220** | 0.65x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246498078410658) |
| poster | Rs 18,942 | 86 | **Rs 220** | 0.65x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246498078400658) |
| static_every_seat_v2 | Rs 24,187 | 94 | **Rs 257** | 0.76x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246498078310658) |
| experience_belongs | Rs 5,959 | 23 | **Rs 259** | 0.77x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246498078290658) |
| break in | Rs 22,060 | 72 | **Rs 306** | 0.91x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120245853594670658) |
| *(4 mid-table ads omitted)* | | | | | |
| Orange – Copy | Rs 83,969 | 218 | **Rs 385** | 1.15x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246498078380658) |
| id_ov07_overheard_independentofwhom | Rs 12,635 | 32 | **Rs 395** | 1.17x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120246788841510658) |
| women seat | Rs 43,684 | 99 | **Rs 441** | 1.31x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=708740732041378&selected_ad_ids=120245852780460658) |

### RID + ID BC 10-12 Oct 2026_CBO_LEAD

*Par: Rs 74 per lead over 30 days. 11 of 77 ads that spent cleared 20 leads.*

| Ad | Spend | Leads | Cost | vs par | Link |
|---|---|---|---|---|---|
| C4_banker_finance_minds | Rs 25,694 | 452 | **Rs 57** | 0.76x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249675334550716) |
| V3_educator_retired | Rs 317,637 | 4,784 | **Rs 66** | 0.89x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249705185320716) |
| id19_f20_social_sector | Rs 16,952 | 233 | **Rs 73** | 0.98x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249834507830716) |
| C5_corporate_25yrs_qualifies | Rs 5,072 | 58 | **Rs 87** | 1.18x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249675334990716) |
| 25_chat_civil_servant | Rs 12,025 | 125 | **Rs 96** | 1.29x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249676721460716) |
| id19_f16_age_proof | Rs 4,961 | 51 | **Rs 97** | 1.31x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249834503690716) |
| *(2 mid-table ads omitted)* | | | | | |
| D2_RID_i7_forces | Rs 11,012 | 76 | **Rs 145** | 1.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249673382150716) |
| W1_women | Rs 3,921 | 25 | **Rs 157** | 2.11x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249673370090716) |
| V1_construction_desk | Rs 30,230 | 163 | **Rs 185** | 2.50x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249710029340716) |

### PK_[21day_Community]_CriminalLitigation_9/May

*Par: Rs 309 per buyer over 30 days. 7 of 35 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| crimlit_sep26_04_full-calendar | Rs 253,226 | 943 | **Rs 269** | 0.87x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248348577250605) |
| weekly calendar | Rs 40,368 | 134 | **Rs 301** | 0.97x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120242708469350605) |
| 21 skills calendar light | Rs 27,750 | 82 | **Rs 338** | 1.09x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120242709029620605) |
| cr15_crimlit_sketch | Rs 11,761 | 30 | **Rs 392** | 1.27x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247961643240605) |
| cr07_crimlit_nameplate | Rs 42,087 | 99 | **Rs 425** | 1.37x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247961641320605) |
| du07_crimlit_junior | Rs 55,073 | 121 | **Rs 455** | 1.47x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248040743590605) |
| 21 skills calendar black yellow | Rs 16,406 | 32 | **Rs 513** | 1.66x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120242709050220605) |

### Sa_community_Legalai_13th_june

*Par: Rs 396 per buyer over 30 days. 4 of 24 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| cr03_legalai_toon | Rs 138,702 | 421 | **Rs 329** | 0.83x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247961632520605) |
| cr11_legalai_toolbox | Rs 111,844 | 264 | **Rs 424** | 1.07x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247961633570605) |
| blueprint_curriculum | Rs 33,209 | 75 | **Rs 443** | 1.12x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246980236210605) |
| One lawyer every ai | Rs 152,039 | 340 | **Rs 447** | 1.13x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246979361290605) |

### M&A_14day[Community]_4june

*Par: Rs 657 per buyer over 30 days. 4 of 23 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| ma_students_14day_calendar | Rs 21,043 | 43 | **Rs 489** | 0.74x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248255778930605) |
| ma_professionals_4documents | Rs 42,289 | 69 | **Rs 613** | 0.93x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248255816600605) |
| ma_freshgrads_first_year | Rs 119,850 | 180 | **Rs 666** | 1.01x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248208153030605) |
| ma_litigators_full_syllabus | Rs 217,950 | 323 | **Rs 675** | 1.03x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248255805050605) |

### SA_SQE community_JULY

*Par: Rs 751 per buyer over 30 days. 9 of 75 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| sqe_h_h_secondact | Rs 21,655 | 46 | **Rs 471** | 0.63x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247668333310605) |
| Sqe_ondemand | Rs 14,653 | 30 | **Rs 488** | 0.65x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247297079740605) |
| sqr_c_editorial | Rs 15,621 | 31 | **Rs 504** | 0.67x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248075227900605) |
| sqe_l_l_gulf | Rs 54,353 | 81 | **Rs 671** | 0.89x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247668333270605) |
| sqe_k_k_associates | Rs 67,738 | 88 | **Rs 770** | 1.02x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247668333250605) |
| sqd_c_tsl_shortagelist | Rs 72,443 | 93 | **Rs 779** | 1.04x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248141108600605) |
| sqe_f_f_paralegal | Rs 17,802 | 21 | **Rs 848** | 1.13x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247668333280605) |
| sqx_l_family_home | Rs 44,890 | 47 | **Rs 955** | 1.27x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248381994270605) |
| sqx_g2_seniors_15plus | Rs 22,294 | 23 | **Rs 969** | 1.29x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248381975090605) |

### CorpFinance_bootcamp_17-19Oct_CBO

*Par: Rs 249 per buyer over 30 days. 13 of 45 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| cfw3_loan_consultant | Rs 78,713 | 381 | **Rs 207** | 0.83x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249838521100716) |
| cf_cma | Rs 61,266 | 280 | **Rs 219** | 0.88x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249737875810716) |
| cf_loan_consultant | Rs 20,600 | 92 | **Rs 224** | 0.90x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249737872550716) |
| cfw2_loan_consultant | Rs 26,461 | 114 | **Rs 232** | 0.93x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249741081730716) |
| cfw4_tax_consultant | Rs 7,851 | 33 | **Rs 238** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249841195670716) |
| cf_equity_research | Rs 40,894 | 165 | **Rs 248** | 1.00x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249737881040716) |
| *(4 mid-table ads omitted)* | | | | | |
| cf_us_remote | Rs 18,939 | 64 | **Rs 296** | 1.19x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249737890090716) |
| cfw2_retired_banker | Rs 8,684 | 23 | **Rs 378** | 1.52x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249741075380716) |
| cf_commerce_grad | Rs 21,112 | 46 | **Rs 459** | 1.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249737888850716) |

### Community_Women _AI_June

*Par: Rs 447 per buyer over 30 days. 6 of 17 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| myth | Rs 52,706 | 130 | **Rs 405** | 0.91x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246183341080605) |
| classic 21 days | Rs 19,809 | 47 | **Rs 421** | 0.94x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120246184201560605) |
| cr04_women_polaroid | Rs 136,153 | 319 | **Rs 427** | 0.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120247961962710605) |
| du04_women_hiring | Rs 71,106 | 158 | **Rs 450** | 1.01x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248040767470605) |
| ov08_women_neighbour | Rs 26,586 | 52 | **Rs 511** | 1.14x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248013339950605) |
| th04_women_fromtomorrow | Rs 28,189 | 54 | **Rs 522** | 1.17x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248040772970605) |

### Retired_Independent_Director_BC_12-Sep-2026_LEAD

*Par: Rs 70 per lead over 30 days. 9 of 29 ads that spent cleared 20 leads.*

| Ad | Spend | Leads | Cost | vs par | Link |
|---|---|---|---|---|---|
| RID_vid6_educator | Rs 146,057 | 2,211 | **Rs 66** | 0.94x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249436215780716) |
| banker | Rs 76,713 | 1,104 | **Rs 69** | 0.99x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249231107030716) |
| RID_vid2_infra | Rs 17,372 | 247 | **Rs 70** | 1.00x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249405365250716) |
| RID_vid4_banker | Rs 22,597 | 311 | **Rs 73** | 1.03x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249405368170716) |
| RID_sim_v4_women_directors | Rs 16,857 | 231 | **Rs 73** | 1.04x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249310256140716) |
| educator | Rs 7,793 | 103 | **Rs 76** | 1.08x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249234323570716) |
| RID_i7_forces | Rs 7,317 | 91 | **Rs 80** | 1.14x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249320743130716) |
| freebootcamp | Rs 7,674 | 95 | **Rs 81** | 1.15x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249234330730716) |
| RID_vid1_armedforces | Rs 26,962 | 311 | **Rs 87** | 1.23x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249405364200716) |

### DataPrivacy_bootcamp_17-19Oct_CBO

*Par: Rs 198 per buyer over 30 days. 19 of 80 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| re_dpdp_pharmacovigilance | Rs 4,626 | 49 | **Rs 94** | 0.48x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249882531590716) |
| dpdp_pharmacovigilance | Rs 12,283 | 96 | **Rs 128** | 0.65x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249850679080716) |
| dpdp_firm_associates | Rs 6,776 | 50 | **Rs 136** | 0.69x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249850689130716) |
| octSA_19_cyber_lawyers | Rs 21,704 | 130 | **Rs 167** | 0.84x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249737752910716) |
| oct_01_dpdp_firm_associates_newspaper | Rs 34,899 | 209 | **Rs 167** | 0.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249717956200716) |
| oct_12_dpdp_data_analysts_standard | Rs 7,168 | 38 | **Rs 189** | 0.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249717986980716) |
| *(10 mid-table ads omitted)* | | | | | |
| oct_06_dpdp_clinical_research_standard | Rs 14,768 | 56 | **Rs 264** | 1.33x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249717967660716) |
| re_dpdp_branch_ops | Rs 6,614 | 22 | **Rs 301** | 1.52x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249882538040716) |
| oct_10_dpdp_insurance_standard | Rs 12,321 | 38 | **Rs 324** | 1.64x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249717979300716) |

### US Accounting_AND_Bookkeeping_Sep_12th

*Par: Rs 44 per lead over 30 days. 11 of 41 ads that spent cleared 20 leads.*

| Ad | Spend | Leads | Cost | vs par | Link |
|---|---|---|---|---|---|
| USACC_us28_notice_ca_inter | Rs 3,723 | 123 | **Rs 30** | 0.69x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337440620716) |
| USACC_us35_notice_cs | Rs 977 | 30 | **Rs 33** | 0.75x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337446470716) |
| icp04_fifties_RELAUNCH | Rs 1,754 | 47 | **Rs 37** | 0.86x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249234470510716) |
| USACC_us24_notice_evening | Rs 96,511 | 2,315 | **Rs 42** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337385830716) |
| USACC_us22_notice_fifties | Rs 22,403 | 523 | **Rs 43** | 0.98x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337383180716) |
| USACC_us21_notice_bcom | Rs 21,938 | 500 | **Rs 44** | 1.01x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337382640716) |
| *(2 mid-table ads omitted)* | | | | | |
| USACC_us25_notice_small_town | Rs 1,026 | 20 | **Rs 51** | 1.18x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337387310716) |
| USACC_us27_notice_xero | Rs 1,624 | 30 | **Rs 54** | 1.24x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249337439150716) |
| USACC_us03_mom | Rs 1,397 | 24 | **Rs 58** | 1.34x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249315529530716) |

### TechLaw_BC_24-26Oct2026_CBO

*Par: Rs 242 per buyer over 30 days. 7 of 49 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| TechLaw_Video_unusedllb | Rs 109,000 | 680 | **Rs 160** | 0.66x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250425259980692) |
| TechLaw_Video_comeback | Rs 20,003 | 117 | **Rs 171** | 0.71x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250424915410692) |
| TechLaw_20T_04_lawfirm_tmt | Rs 12,971 | 45 | **Rs 288** | 1.19x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250356383040692) |
| TechLaw_20T_05_startup_clients | Rs 7,471 | 23 | **Rs 325** | 1.34x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250356383590692) |
| TechLaw_20T_03_internship | Rs 8,054 | 22 | **Rs 366** | 1.51x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250356382740692) |
| TechLaw_20T_02_usparalegal | Rs 47,818 | 120 | **Rs 398** | 1.65x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250356382000692) |
| TechLaw_Broad_tb01_remote_lawyer | Rs 30,453 | 68 | **Rs 448** | 1.85x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250378201350692) |

### [Community]_14Day_Arbitration_12Sep

*Par: Rs 831 per buyer over 30 days. 2 of 48 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| arb14_Ad01_court-order | Rs 159,474 | 204 | **Rs 782** | 0.94x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248347871740605) |
| arb14_Ad04_40-60-lakh | Rs 17,489 | 20 | **Rs 874** | 1.05x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=1132073781843015&selected_ad_ids=120248347873470605) |

### StrategicHR_bootcamp_31Oct-2Nov_CBO

*Par: Rs 157 per buyer over 30 days. 6 of 26 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| HR31Oct_87_retired | Rs 14,876 | 108 | **Rs 138** | 0.88x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249791764100716) |
| HR31Oct_79_women | Rs 77,710 | 528 | **Rs 147** | 0.94x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249791751840716) |
| HR31Oct_73_fresher | Rs 7,033 | 45 | **Rs 156** | 1.00x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249791742490716) |
| HR31Oct_75_side_income | Rs 60,116 | 381 | **Rs 158** | 1.01x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249791745220716) |
| HR31Oct_71_agency | Rs 27,015 | 153 | **Rs 177** | 1.12x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249791739390716) |
| HR31Oct_67_own_firm | Rs 6,857 | 37 | **Rs 185** | 1.18x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249791734340716) |

### Academic_Writing_BC_24-26Oct2026_CBO

*Par: Rs 182 per buyer over 30 days. 10 of 42 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| ACW_Oct24_economics_postgraduates_n44 | Rs 6,976 | 46 | **Rs 152** | 0.83x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826765040716) |
| ACW_Oct24_medical_researchers_papers_n21 | Rs 41,957 | 261 | **Rs 161** | 0.88x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826503070716) |
| ACW_Oct24_life_science_n43 | Rs 17,812 | 108 | **Rs 165** | 0.91x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826513060716) |
| ACW_Oct24_english_literature_n40 | Rs 27,778 | 166 | **Rs 167** | 0.92x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826756370716) |
| ACW_Oct24_msc_graduates_n48 | Rs 8,670 | 50 | **Rs 173** | 0.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826768180716) |
| ACW_Oct24_refresh_medical_researchers_r08 | Rs 4,013 | 23 | **Rs 174** | 0.96x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249827294110716) |
| ACW_Oct24_teachers_masters_n31 | Rs 18,771 | 100 | **Rs 188** | 1.03x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826740400716) |
| ACW_Oct24_ma_english_n41 | Rs 14,522 | 73 | **Rs 199** | 1.09x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826758830716) |
| ACW_Oct24_school_teachers_n36 | Rs 29,453 | 145 | **Rs 203** | 1.12x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249826746100716) |
| ACW_Oct24_refresh_teachers_content_writer_r07 | Rs 9,432 | 40 | **Rs 236** | 1.30x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=954464642377027&selected_ad_ids=120249827291140716) |

### Meta - NCA - Oct 31-2 Nov Bootcamp - CBO Sales

*Par: Rs 334 per buyer over 30 days. 2 of 39 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| Meta - NCA - nca02_notice_spouse | Rs 21,401 | 69 | **Rs 310** | 0.93x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250418468890692) |
| Meta - NCA - nca39_notice_final_year | Rs 14,857 | 47 | **Rs 316** | 0.95x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=458577609606074&selected_ad_ids=120250418477580692) |

### WomenAI_5-7Sep-2026_BC_CBO_v1

*Par: Rs 36 per buyer over 30 days. 6 of 53 ads that spent cleared 20 buyers.*

| Ad | Spend | Buyers | Cost | vs par | Link |
|---|---|---|---|---|---|
| W1_night_shift_cag | Rs 1,739 | 73 | **Rs 24** | 0.67x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251521606380568) |
| W8_V3_three_hours | Rs 918 | 35 | **Rs 26** | 0.73x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251567642840568) |
| N18_caregiver | Rs 553 | 21 | **Rs 26** | 0.74x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251521580090568) |
| N02_teacher_evening | Rs 1,826 | 63 | **Rs 29** | 0.81x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251322098050568) |
| W9_toon_freelance | Rs 1,938 | 60 | **Rs 32** | 0.90x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251588762810568) |
| R2_school_hours | Rs 2,321 | 62 | **Rs 37** | 1.05x | [open](https://adsmanager.facebook.com/adsmanager/manage/ads?act=915514346476600&selected_ad_ids=120251322078220568) |

---

## 4. Google Ads

**There is no cost per purchase or cost per lead for Google in this snapshot, and that is a
fact about access, not an oversight.** The Google Ads API is not connected:
`python ~/.google-ads-mcp/status.py` reports 4 of 6 setup steps outstanding, and the one with
a waiting period - a **developer token** from `ads.google.com/aw/apicenter`, visible only on
the manager (MCC) account - has not been issued. Until it is, Google cost exists only in the
Google Ads UI, and it must not be retyped into a rupee table beside Meta's.

What is known about Google traffic from the funnel side, measured 23 Sep 2026 on GrowthX
`get_leads_report` (payment outcomes, not cost), with Paid + Failed as the denominator:

- **Meta 2.5% payment failures** (246 of 10,039 attempts), **Google 11.6%** (393 of 3,382),
  other sources 3.3%. Meta sits at 1.1 to 2.8% in every camp, so it is the control.
- Google carries a modest penalty nearly everywhere (AI for Women 3.5%, academic writing
  3.8%, Legal AI 6.1%, Contract Drafting 6.5%, Patent 7.3%, Independent Director 8.5%,
  IP Law 10.4%) and two camps sit far outside it: **Senior AI 27.8%**, **US Corporate Law
  20.5%**.
- Inside those two, the failures concentrate on **duplicated funnel slugs** (`-2`, `-3`,
  `r2`): Senior AI 39.6% on 333 attempts against 6.9% on the original 189 in the same camp
  and week. It is not a general rule about duplicates - Patent and Academic Writing
  duplicates are fine.

So when a Google wave underperforms, check the funnel slug before blaming the creative. The
gateway's decline reason is not exposed, so lower-quality traffic and a broken checkout both
still fit.

**Google creative is built differently, and that part is settled.** Google cannot run
carousels, so a Meta carousel wave gets a twin wave of single faces in `adkit`'s `search`
layout - same readers, same landing pages, same slugs, nothing selling re-decided. Two
deltas against a Meta face: the **field definition goes on the face** (a Google reader has
not seen the account before), and each ad needs **authored** headlines of 40 characters or
fewer and descriptions of 90 or fewer in `ad_copy.md` - authored, never the face's copy cut
to length, which ends a line mid-phrase and produces the riddle the face was built to avoid.

**To get Google numbers:** apply for the developer token on the MCC account, then
`uvx --from git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp`. It is
read-only - account listing, resource metadata and raw GAQL search, no mutation tools.
Credentials live in `~/.google-ads-mcp/`, deliberately outside this folder.

---

## 5. What this snapshot cannot tell you

- **A cost with n under 20 is noise.** SOP/03: a 7-day window, 20+ results, and print the
  margin. Most ads in any wave are starved rather than beaten.
- **Cheap does not always mean the face is good.** A refresh of a reader inherits that
  reader's audience, and `adkit.corpus` joins live cost on shared words, so confirm a cost
  belongs to that exact ad before copying its layout.
- **CTR is absent on purpose.** It has run backwards against cost in three product lines.
  The decision columns are spend, results, cost per result, and a link to look at the
  creative.
- **An ICP with no row has no evidence either way.** Never read a missing reader as a
  rejected one.
