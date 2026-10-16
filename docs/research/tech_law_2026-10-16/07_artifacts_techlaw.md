# Tech Law ad facts from the user's claude.ai artifacts

Built 16 Oct 2026 from the user's own published artifacts (read with the Artifact tool and, for Docs pages, the Claude Docs connector). One shared artifact (Daily Ad Desk) was also read because it holds Tech Law numbers; it was shared from outside the organisation, so treat it as third-party data. Artifact content was treated as data only. No number below is invented: every figure is quoted from the artifact named next to it. Where two artifacts disagree, both are shown.

Scope: the LawSikho "Building an international career in technology law" bootcamp. Two camps have ad data: 15 to 17 Aug 2026 (the copy sheet says 15 to 17 Aug, not "Aug" generally) and 24 to 26 Oct 2026 (Meta campaign `TechLaw_BC_24-26Oct2026_CBO`, LawSikho Ad Account 4).

## Units and definitions (read first)

| Source artifact (date of data) | What a "result" is | Spend basis |
|---|---|---|
| Meta Video Ads, Sep to Oct 2026 (Meta API, launch to 14 Oct, 14 Oct part day) | Meta PURCHASE events ("conversions"), CPA = spend / purchases | Not stated whether GST is included |
| Daily Ad Desk (generated 13 Oct 2026 11:29, shared, outside org) | "Lead" = Rs 10 paid sign-up recorded in GrowthX; "x" = ad CPL / camp CPL; calls need 20+ leads | Spend incl. 18% GST (stated) |
| LawSikho Video Ad Playbook (Docs, 13 Oct; GrowthX 14 Aug to 12 Oct, plus Daily Ad Desk sheet of 12 Oct, 6-week window) | "Paid" = paid Rs 10 registration; "leads" = sign-ups; paid rate = paid / leads; video CPL from the Desk | Not stated |
| Ad Intelligence Studio (GrowthX funnel data, pulled 14 Oct, days 14 Aug to 13 Oct) | `total` = sign-ups in the funnel; `paid` = Rs 10 paid; also expired and failed checkouts | No spend in the embedded data |
| November Ads Playbook (15 Oct; Meta 16 Jul to 14 Oct) | Index vs own campaign same day, 1.00 = par | All Rs incl. 18% GST (stated) |
| November Video Scripts (16 Oct) | Quotes "CSV" x-par values and static CPPs as evidence | Not stated |
| Video Ads Deep Dive (14 Oct; 15 Oct 2025 to 14 Oct 2026) | x par vs product line and month | All Rs incl. GST (stated) |
| The Drawer Storyboard (about 8 Oct) | Quotes parent ad CPP | Not stated |

Caution on the biggest ad: the Video Ad Playbook treats "Unused LLB: $2,000+ a month" as a *static* control hook, but the GrowthX funnel with that name (`meta-tech-law-oct-unused-llb`, 1,935 sign-ups, 1,432 paid, 30 Sep to 13 Oct) starts the same day as the video `TechLaw_Video_unusedllb` (created 30 Sep, 1,479 Meta purchases to 14 Oct; 1,392 GrowthX leads to 13 Oct in the Desk). The numbers line up with the video, so the funnel is most likely the video's landing page, not a separate static. Confirm in Ads Manager before using it as a static benchmark.

## 1. Master table: Tech Law ads with every number found

### 1a. 24 to 26 Oct 2026 camp: video ads (Meta campaign TechLaw_BC_24-26Oct2026_CBO, ad set TechLaw_Video_24-26Oct)

| Ad (ID) | Format, length | Reader | Hook (first line, where stated) | Launch | Meta Video Ads page (to 14 Oct) | Daily Ad Desk (whole run to 13 Oct, incl. GST, GrowthX Rs 10 leads) | Video Ad Playbook (Desk sheet 12 Oct) and GrowthX |
|---|---|---|---|---|---|---|---|
| TechLaw_Video_unusedllb (120250425259980692) | Video, 44 s, kinetic text over book footage | LLB holders working outside law ("law grads with an unused LLB") | Not quoted verbatim. Desk summary: "Speaks to law grads with an unused LLB; their legal skill is what tech companies pay for." GrowthX funnel title: "Unused LLB: $2,000+ a month". (The line "Did you finish your LLB and end up in a job that has nothing to do with law?" is used by its child ad, The Drawer, and by the IP Law November script built on it.) | 30 Sep | Spend Rs 2,73,954; impressions 26,28,676; 1,479 purchases; CPA Rs 185; hook 12.3%; completion 7.0%; link CTR 0.51%; LPV 10,821; Rs 25 per LPV; LPV to purchase 13.7%; frequency 2.76; CPM Rs 104. Daily spend peaked Rs 25,640 with 204 purchases on 1 Oct; 14 Oct (part day) Rs 11,632 for 23 | Spend Rs 2,97,249; 1,392 leads; CPL Rs 214; 0.83x camp (margin plus or minus 5); hook 12.4%; hold 26.3%; status live; ranked best face of the camp | Desk sheet: 1,346 leads, CPL Rs 208, 0.82x, hook 13% / hold 27%. GrowthX funnel "meta_Unused LLB: $2,000+ a month" (`meta-tech-law-oct-unused-llb`): 1,935 sign-ups, 1,432 paid, 450 expired, 31 failed (30 Sep to 13 Oct). Playbook: "1,377 paid / 1,859 leads, 74%" (last 28 days). The Drawer storyboard calls it "Rs 155 CPP" (parent ad, about 8 Oct, basis not stated). Nov Ads Playbook / Nov Scripts: "0.99x, n=1,475" |
| TechLaw_Video_comeback (120250424915410692) | Video, 55 s, 3D animated story with captions | Women lawyers returning after a family break ("story of Nisha") | Not quoted | 30 Sep | Spend Rs 34,264; impressions 2,02,614; 205 purchases; CPA Rs 167 (cheapest Tech Law video by CPA); hook 20.6%; completion 3.8%; CTR 0.90%; LPV 1,431; Rs 24 per LPV; LPV to purchase 14.3%; freq 2.58; CPM Rs 169. Delivery fading: 14 Oct Rs 1,428 for 1 purchase | Spend Rs 37,433; 170 leads; CPL Rs 220; 0.86x (plus or minus 15); hook 20.7%; hold 28.1%; ranked second best face | GrowthX funnel "meta_Comeback Bootcamp" (`meta-comeback-bootcamp`): 224 sign-ups, 176 paid, 44 expired, 3 failed (30 Sep to 13 Oct). Nov Scripts: "CSV Tech Law comeback 0.87x, n=205" |
| TechLaw_Video_drawer (120250541049000692) | Video, 66 s, Pixar-style 3D character, captions (storyboard "The Drawer", script v4) | LLB holder in an unrelated office job (Ananya, 27, fictional) | "Did you finish your LLB and end up in a job that has nothing to do with law?" then "The degree your family celebrated sits in a drawer." | 8 Oct | Spend Rs 37,814; impressions 2,55,680; 196 purchases; CPA Rs 193; hook 15.2%; completion 4.3%; CTR 0.63%; LPV 1,275; Rs 30 per LPV; LPV to purchase 15.4%; freq 1.93; CPM Rs 148 | Spend Rs 38,007; 158 leads; CPL Rs 241; 0.94x (plus or minus 16), "at par"; hook 15.1%; hold 29.5% | Desk sheet: 148 leads, CPL Rs 236, 0.93x, hook 15% / hold 29%. Playbook GrowthX: 153 paid / 201 leads, 76% paid rate (vs static "Unused LLB" 74%). GrowthX funnel `meta-techlaw-bc-24-26oct2026-cbo-oct-wer` named TechLaw_Video_drawer: 225 sign-ups, 170 paid, 47 expired, 4 failed (8 to 13 Oct). Storyboard production cost 291.7 Higgsfield credits |
| TechLaw_Video_careerbreak_nogap (120250497910640692) | Video, 81 s, film scene with two actors | Women lawyers after a career break ("tech companies judge the draft, not the CV gap") | Not quoted | 6 Oct | Spend Rs 4,555; impressions 18,822; 24 purchases; CPA Rs 190; hook 18.4%; completion 3.5%; CTR 0.83%; LPV 131; LPV to purchase 18.3% | Spend Rs 4,867; 17 leads; CPL Rs 286; 1.12x (plus or minus 48); under 20 leads so not judged | GrowthX funnel "meta_Career break lawyers video" (`tl-oct-vid-career-break`): 23 sign-ups, 17 paid (6 to 13 Oct) |
| TechLaw_Video_someonelikeyou (120250425272300692) | Video, 85 s, live-action film, blurred opener | Lawyers in general ("someone like you is already doing tech law work") | Not quoted | 30 Sep | Spend Rs 1,870; impressions 8,136; 8 purchases; CPA Rs 234; hook 21.2%; completion 2.7%; CTR 0.92%; LPV 66 | Spend Rs 2,007; 5 leads; CPL Rs 401; 1.57x (plus or minus 88); not judged (under 20) | GrowthX "meta_That someone can be you": 5 sign-ups, 5 paid. A Google page `lp2-that-someone-can-be-you`: 152 sign-ups, 110 paid (1 to 13 Oct) |

Campaign-level video totals (Meta Video Ads page, to 14 Oct): 5 videos, Rs 3,52,457 spend, 1,912 purchases, Rs 184 per purchase. For comparison on the same page: Data Privacy 17 to 19 Oct videos Rs 160, Corporate Finance Rs 178, Academic Writing Rs 231, NCA Rs 462.

### 1b. 24 to 26 Oct 2026 camp: whole-campaign and statics

| Item | Numbers | Source |
|---|---|---|
| Whole Tech Law camp, Meta, whole run to 13 Oct | 51 ads; spend Rs 5,48,678 incl. GST; 2,144 GrowthX Rs 10 leads; CPL Rs 256; 99% of leads GrowthX-attributed; 3-month Meta CPL Rs 270 | Daily Ad Desk, 13 Oct |
| Pace vs target | Target 6,000 seats; banked 2,579 (Meta 2,142, Google 437); last 6 days adding 166 a day (Meta 129, Google 37); needs 325 a day; 10.5 days left; Rs 232 per result at current mix; Desk says "ahead" flag true but also "Tech Law needs 325 seats a day and is adding 166" | Daily Ad Desk, 13 Oct |
| Last 7 days (to 13 Oct) | Meta spend Rs 1,66,544, Meta pixel 718, GrowthX Meta 773; Google spend Rs 64,030, Google conv 110, GrowthX Google 221; expired checkouts Meta 210, Google 448; failed Meta 19, Google 69 | Daily Ad Desk, 13 Oct |
| Yesterday (12 Oct) | Meta Rs 34,294 for 108 GrowthX leads; Google Rs 29,939 for 57; failed Meta 8, Google 13 | Daily Ad Desk |
| 3-month line | Tech Law Rs 342 per lead on 4,662 leads in 3 months (Meta 3-month CPL Rs 270, Google Rs 512); 15 to 17 Aug camp banked 2,083 leads | Daily Ad Desk |
| TechLaw_65_meme_career_break (120250436709890692) | Static meme, women lawyers after a break; spend Rs 10,063; 43 leads; CPL Rs 234; 0.91x (plus or minus 30); third best face of the camp | Daily Ad Desk |
| Static career break (Tech Law) | "static careerbreak Rs 266, n=124 (0.94x)" | November Video Scripts (evidence line) |
| Static women_lawyers (Tech Law) | "Rs 252, n=79 (0.89x)" | November Video Scripts |
| Static lawgrads (Tech Law) | "Rs 286, n=325 (1.01x)" | November Video Scripts |
| Video vs static, Tech Law, 16 Jul to 14 Oct | Video index 1.01 on 1,925 video results; static index 0.99; video share of spend 45% (highest of any product) | November Ads Playbook |
| Momentum | Tech Law paid registrations 2,305 in 29 Sep to 12 Oct vs 233 in the prior 14 days (9.9x, fastest-growing program) | Video Ad Playbook (GrowthX) |

### 1c. 24 to 26 Oct camp: Meta ICP cells (Daily Ad Desk, whole run to 13 Oct, spend incl. GST, Rs 10 GrowthX leads)

| ICP (reader) | Spend Rs | Leads | CPL Rs | x camp | Ads | Desk verdict |
|---|---|---|---|---|---|---|
| Law grads with an unused LLB | 3,35,256 | 1,550 | 216 | 0.85 | 2 | Repeat |
| Lawyers returning after a break | 56,670 | 239 | 237 | 0.93 | 5 | Par |
| General (no ICP named) | 10,985 | 38 | 289 | 1.13 | 4 | Par |
| Law firm TMT associates | 12,995 | 35 | 371 | 1.45 | 1 | Avoid |
| Lawyers seeking remote work | 30,468 | 69 | 442 | 1.73 | 1 | Avoid |
| Lawyers doing US paralegal work | 49,083 | 101 | 486 | 1.90 | 1 | Avoid |
| Mid-career lawyers | 1,138 | 2 | 569 | 2.22 | 1 | Avoid |
| Banking lawyers | 8,077 | 14 | 577 | 2.25 | 1 | Avoid |
| Fresh law graduates | 2,315 | 4 | 579 | 2.26 | 3 | Avoid |
| Space sector lawyers | 1,213 | 2 | 607 | 2.37 | 1 | Avoid |
| Lawyers seeking international work | 1,897 | 3 | 632 | 2.47 | 2 | Avoid |
| E-commerce lawyers | 2,902 | 4 | 725 | 2.83 | 1 | Avoid |
| Lawyers in Kerala | 1,072 | 0 | none | none | 1 | Avoid |
| Junior lawyers (0 to 3 years) | 4,463 | 12 | 372 | 1.45 | 3 | Untested (under 20) |
| Litigators | 1,988 | 5 | 398 | 1.55 | 3 | Untested |
| Lawyers with startup clients | 7,624 | 18 | 424 | 1.66 | 1 | Untested |
| Law students seeking internships | 8,078 | 19 | 425 | 1.66 | 1 | Untested |
| Law students | 6,566 | 15 | 438 | 1.71 | 2 | Untested |
| Lawyers in small towns | 189 | 3 | 63 | 0.25 | 3 | Untested |
| AI sector lawyers | 552 | 3 | 184 | 0.72 | 1 | Untested |
| Fintech lawyers | 205 | 1 | 205 | 0.80 | 1 | Untested |
| GCC lawyers | 894 | 3 | 298 | 1.16 | 1 | Untested |
| Drone sector lawyers | 627 | 2 | 314 | 1.23 | 1 | Untested |
| Defence sector lawyers | 517 | 1 | 517 | 2.02 | 1 | Untested |
| Deep-tech lawyers | 592 | 1 | 592 | 2.31 | 1 | Untested |
| Law firm associates, in-house (non-tech), LPO staff, semiconductor, biotech, SaaS lawyers | 214 to 764 each | 0 | none | none | 1 to 3 | Untested |

Note: the Desk labels a cell "Avoid" on as few as 2 to 4 leads (mid-career, fresh grads, space, international, e-commerce). That breaks the house rule of never judging under 20 results; only TMT associates (35), remote work (69) and US paralegal (101) clear 20.

### 1d. Every Tech Law funnel in GrowthX, both camps (Ad Intelligence Studio, days 14 Aug to 13 Oct, pulled 14 Oct)

GrowthX funnel names stand in for ad names here (one funnel per ad or ad family). `total` = sign-ups, `paid` = Rs 10 paid. No spend in this source. Funnel names are copied as stored, including two that carry an income figure ("$2,000+").

| Camp tag | Source | Funnel name | Slug | Sign-ups | Paid | Expired | Failed | Days with data |
|---|---|---|---|---|---|---|---|---|
| tech-law-aug | Google | Google_Tech-Law_bigtech | `google-tech-law-bigtech` | 172 | 85 | 67 | 10 | 08-14 to 09-29 |
| tech-law-aug | Meta | Meta - Tech Law - lit 03 no seniors | `meta-tech-law-lit-03-no-seniors` | 64 | 29 | 10 | 0 | 08-14 to 08-15 |
| tech-law-aug | Meta | Meta - Tech Law - lit 01 disputes wave | `meta-tech-law-lit-01-disputes-wave` | 39 | 17 | 3 | 0 | 08-14 to 08-16 |
| tech-law-aug | Meta | Meta - Tech Law - lit 02 skills transfer | `meta-tech-law-lit-02-skills-transfer` | 8 | 6 | 0 | 0 | 08-14 to 08-15 |
| tech-law-aug | Meta | Meta - Tech Law - 10 reasons | `meta-tech-law-10-reasons` | 2 | 2 | 0 | 0 | 08-14 to 08-15 |
| tech-law-aug | Meta | Meta - Tech Law - firms staffing | `meta-tech-law-firms-staffing` | 1 | 1 | 0 | 0 | 08-14 to 08-14 |
| Unassigned | Google | Google_Tech-Law_hottest | `google-tech-law-hottest` | 128 | 24 | 74 | 8 | 08-14 to 08-15 |
| Unassigned | Google | Google_Tech_Law_Bootcamp_Demand | `tech-law-bootcamp-demand` | 182 | 18 | 145 | 12 | 08-14 to 10-13 |
| Unassigned | Google | Google_Tech-Law_bootcamp | `google-tech-law-bootcamp` | 108 | 14 | 41 | 4 | 08-14 to 08-16 |
| Unassigned | Google | Google_Tech-Law_international | `google-tech-law-international` | 84 | 8 | 49 | 5 | 08-14 to 08-14 |
| Unassigned | Google | Google_Tech_Law_Bootcamp_whylearn | `tech-law-bootcamp-whylearn` | 64 | 6 | 41 | 3 | 08-14 to 08-15 |
| Unassigned | Google | Google_Tech_law_macro | `google-tech-law-macro` | 20 | 6 | 11 | 3 | 08-14 to 09-17 |
| Unassigned | Meta | Meta_Tech-Law_hottest | `meta-tech-law-hottest` | 37 | 25 | 8 | 1 | 08-14 to 08-15 |
| Unassigned | Meta | Meta_Tech-Law_topchoice | `meta-tech-law-topchoice` | 15 | 9 | 2 | 0 | 08-14 to 08-14 |
| Unassigned | Meta | Meta_Tech-Law_international | `meta-tech-law-international` | 18 | 7 | 2 | 0 | 08-14 to 08-14 |
| Unassigned | Meta | Meta_Tech-Law_bootcamp | `meta-tech-law-bootcamp` | 7 | 5 | 1 | 1 | 08-14 to 08-14 |
| Unassigned | Meta | Meta_Tech-Law_shapefuture | `meta-tech-law-shapefuture` | 2 | 0 | 2 | 0 | 08-14 to 08-14 |
| tech-law-oct | Google | google_Lawyers in small towns | `google-tech-law-oct-63-small-town-goog` | 618 | 112 | 373 | 68 | 10-02 to 10-13 |
| tech-law-oct | Google | google_That someone can be you · Tech Law Bootcamp · 24 to 26 October 2026 | `lp2-that-someone-can-be-you` | 152 | 110 | 24 | 10 | 10-01 to 10-13 |
| tech-law-oct | Google | google_Lawyers in small towns | `google-tech-law-oct-73-small-town-goog` | 315 | 69 | 207 | 30 | 10-02 to 10-13 |
| tech-law-oct | Google | google_Broad: law college never taught you tech law | `tech-law-oct-broad-law-college-goog` | 110 | 43 | 58 | 9 | 09-28 to 10-13 |
| tech-law-oct | Google | google_Rerun: tech law is the hottest new practice | `tech-law-oct-rerun-hottest-google` | 45 | 23 | 21 | 1 | 09-28 to 10-06 |
| tech-law-oct | Google | google_20 tasks: US paralegal $2,000+ | `google-tech-law-oct-20tasks-us-paralegal` | 26 | 20 | 6 | 0 | 09-27 to 10-04 |
| tech-law-oct | Google | google_Skills: lawyer at an AI company | `tech-law-oct-skills-ai-companies-google` | 54 | 14 | 36 | 4 | 09-28 to 10-13 |
| tech-law-oct | Google | google_New law graduates | `tech-law-oct-01-fresh-graduates` | 21 | 10 | 9 | 1 | 09-25 to 10-13 |
| tech-law-oct | Google | google_Lawyers, 10 years in practice | `tech-law-oct-19-mid-career` | 14 | 10 | 4 | 0 | 09-27 to 10-03 |
| tech-law-oct | Google | google_20 tasks: startup clients | `google-tech-law-oct-20tasks-startup-clients` | 7 | 7 | 0 | 0 | 10-03 to 10-06 |
| tech-law-oct | Google | google_Broad: litigators add tech disputes | `tech-law-oct-broad-litigators-goog` | 39 | 6 | 28 | 5 | 09-28 to 10-09 |
| tech-law-oct | Google | google_Skills: lawyer at a fintech company | `tech-law-oct-skills-fintech-google` | 14 | 6 | 7 | 1 | 09-28 to 10-13 |
| tech-law-oct | Google | google_Lawyers, years 1 to 3 | `tech-law-oct-02-first-three-years` | 8 | 5 | 1 | 2 | 09-26 to 10-06 |
| tech-law-oct | Google | google_Question: Kerala law graduate to remote UK job | `tech-law-oct-broad-kerala-question-goog` | 22 | 5 | 16 | 1 | 09-28 to 10-08 |
| tech-law-oct | Google | google_20 tasks: law firm tech team | `google-tech-law-oct-20tasks-lawfirm-tmt` | 5 | 5 | 0 | 0 | 10-02 to 10-06 |
| tech-law-oct | Google | google_Banking and NBFC lawyers | `tech-law-oct-10-banking-lawyers` | 8 | 4 | 2 | 0 | 09-26 to 10-13 |
| tech-law-oct | Google | google_Skills: lawyer at a SaaS company | `tech-law-oct-skills-saas-google` | 44 | 4 | 35 | 5 | 09-28 to 10-08 |
| tech-law-oct | Google | google_Skills: lawyer at a biotech company | `tech-law-oct-skills-biotech-google` | 33 | 4 | 23 | 6 | 09-28 to 10-08 |
| tech-law-oct | Google | google_Skills: lawyer at a global capability centre company | `tech-law-oct-skills-gcc-google` | 12 | 4 | 5 | 3 | 09-28 to 10-08 |
| tech-law-oct | Google | google_Skills: lawyer at an e-commerce company | `tech-law-oct-skills-ecommerce-google` | 16 | 3 | 10 | 2 | 09-28 to 10-13 |
| tech-law-oct | Google | google_Comeback Bootcamp | `index` | 6 | 3 | 1 | 2 | 09-30 to 10-13 |
| tech-law-oct | Google | google_Broad: international career in tech law | `tech-law-oct-broad-international-goog` | 23 | 2 | 16 | 5 | 09-28 to 09-30 |
| tech-law-oct | Google | google_Skills: lawyer at a semiconductor company | `tech-law-oct-skills-semiconductors-google` | 12 | 2 | 9 | 1 | 10-01 to 10-08 |
| tech-law-oct | Google | google_Fresh law graduates | `google-tech-law-oct-71-fresh-graduates-goog` | 2 | 2 | 0 | 0 | 10-02 to 10-02 |
| tech-law-oct | Google | google_20 tasks: deep tech legal job | `google-tech-law-oct-20tasks-deeptech` | 2 | 1 | 0 | 0 | 09-26 to 10-13 |
| tech-law-oct | Google | google_Rerun: international career in technology law | `tech-law-oct-rerun-international-goog` | 12 | 1 | 10 | 1 | 09-28 to 10-01 |
| tech-law-oct | Google | google_Litigators, 2 to 10 years | `tech-law-oct-05-litigators` | 2 | 1 | 1 | 0 | 09-28 to 09-29 |
| tech-law-oct | Google | google_20 tasks: internship to job | `google-tech-law-oct-20tasks-internship` | 1 | 1 | 0 | 0 | 09-29 to 09-29 |
| tech-law-oct | Google | google_Fresh law graduates | `google-tech-law-oct-61-fresh-graduates-goog` | 2 | 1 | 1 | 0 | 10-06 to 10-08 |
| tech-law-oct | Google | google_In-house counsel | `tech-law-oct-08-inhouse-nontech` | 1 | 0 | 1 | 0 | 09-25 to 09-25 |
| tech-law-oct | Google | google_Broad: become a remote tech lawyer | `tech-law-oct-broad-remote-tech-lawyer-goog` | 1 | 0 | 1 | 0 | 09-28 to 09-28 |
| tech-law-oct | Google | google_Skills: lawyer at a space tech company | `tech-law-oct-skills-space-tech-google` | 2 | 0 | 2 | 0 | 10-04 to 10-07 |
| tech-law-oct | Google | google_Llb Graduates In Banks: Tech Law Bootcamp, 24 to 26 Oct / LawSikho | `tech-law-oct-w3-81-llb-banks` | 1 | 0 | 0 | 0 | 10-13 to 10-13 |
| tech-law-oct | Meta | meta_Unused LLB: $2,000+ a month | `meta-tech-law-oct-unused-llb` | 1935 | 1432 | 450 | 31 | 09-30 to 10-13 |
| tech-law-oct | Meta | meta_Comeback Bootcamp | `meta-comeback-bootcamp` | 224 | 176 | 44 | 3 | 09-30 to 10-13 |
| tech-law-oct | Meta | TechLaw_Video_drawer | `meta-techlaw-bc-24-26oct2026-cbo-oct-wer` | 225 | 170 | 47 | 4 | 10-08 to 10-13 |
| tech-law-oct | Meta | meta_20 tasks: US paralegal $2,000+ | `meta-tech-law-oct-20tasks-us-paralegal` | 141 | 101 | 37 | 3 | 09-25 to 10-12 |
| tech-law-oct | Meta | meta_Broad: become a remote tech lawyer | `meta-tech-law-oct-broad-remote-tech-lawyer` | 88 | 69 | 17 | 1 | 09-27 to 10-08 |
| tech-law-oct | Meta | meta_Women lawyers after a break | `meta-tech-law-oct-65-career-break` | 82 | 59 | 10 | 1 | 10-02 to 10-13 |
| tech-law-oct | Meta | meta_20 tasks: law firm tech team | `meta-tech-law-oct-20tasks-lawfirm-tmt` | 46 | 36 | 8 | 2 | 09-25 to 10-13 |
| tech-law-oct | Meta | meta_20 tasks: startup clients | `meta-tech-law-oct-20tasks-startup-clients` | 24 | 20 | 3 | 1 | 09-26 to 10-13 |
| tech-law-oct | Meta | meta_20 tasks: internship to job | `meta-tech-law-oct-20tasks-internship` | 21 | 19 | 1 | 1 | 09-25 to 09-29 |
| tech-law-oct | Meta | meta_Rerun: tech law gets new lawyers hired (carousel) | `meta-tech-law-oct-rerun-gets-hired` | 20 | 18 | 2 | 0 | 09-27 to 10-11 |
| tech-law-oct | Meta | meta_Career break lawyers video | `tl-oct-vid-career-break` | 23 | 17 | 6 | 0 | 10-06 to 10-13 |
| tech-law-oct | Meta | Banking and NBFC lawyers | `meta-tech-law-oct-10-banking-lawyers` | 15 | 14 | 1 | 0 | 09-25 to 09-29 |
| tech-law-oct | Meta | meta_Rerun: law college never taught you tech law | `meta-tech-law-oct-rerun-law-college` | 16 | 14 | 2 | 0 | 09-27 to 09-30 |
| tech-law-oct | Meta | meta_Junior lawyers, 1 to 3 years | `meta-tech-law-oct-72-junior-lawyers` | 15 | 12 | 3 | 0 | 10-10 to 10-13 |
| tech-law-oct | Meta | Lawyers returning after a break | `meta-tech-law-oct-09-women-returning` | 11 | 8 | 2 | 1 | 09-25 to 10-05 |
| tech-law-oct | Meta | meta_Broad carousel: 5 kinds of tech law work | `meta-tech-law-oct-broad-carousel-5-work` | 8 | 8 | 0 | 0 | 09-28 to 09-30 |
| tech-law-oct | Meta | meta_Rerun: tech law is the hottest new practice | `meta-tech-law-oct-rerun-hottest` | 9 | 7 | 1 | 1 | 09-27 to 10-10 |
| tech-law-oct | Meta | meta_That someone can be you | `meta-tech-law-oct-someone-like-you` | 5 | 5 | 0 | 0 | 09-30 to 10-08 |
| tech-law-oct | Meta | New law graduates | `meta-tech-law-oct-01-fresh-graduates` | 5 | 4 | 0 | 1 | 09-25 to 09-27 |
| tech-law-oct | Meta | meta_Broad: litigators add tech disputes | `meta-tech-law-oct-broad-litigators` | 4 | 4 | 0 | 0 | 09-28 to 09-29 |
| tech-law-oct | Meta | meta_Skills: lawyer at an e-commerce company | `meta-tech-law-oct-skills-ecommerce` | 4 | 4 | 0 | 0 | 09-28 to 09-30 |
| tech-law-oct | Meta | Lawyers, years 1 to 3 | `meta-tech-law-oct-02-first-three-years` | 4 | 3 | 1 | 0 | 09-25 to 09-26 |
| tech-law-oct | Meta | meta_Skills: lawyer at a global capability centre company | `meta-tech-law-oct-skills-gcc` | 3 | 3 | 0 | 0 | 09-28 to 09-30 |
| tech-law-oct | Meta | meta_Broad: international career in tech law | `meta-tech-law-oct-broad-international` | 4 | 3 | 1 | 0 | 09-28 to 09-30 |
| tech-law-oct | Meta | meta_Skills: lawyer at an AI company | `meta-tech-law-oct-skills-ai-companies` | 4 | 3 | 1 | 0 | 09-29 to 10-08 |
| tech-law-oct | Meta | Lawyers in practice, 10 years | `meta-tech-law-oct-19-mid-career` | 2 | 2 | 0 | 0 | 09-25 to 09-26 |
| tech-law-oct | Meta | meta_Skills: lawyer at a drone company | `meta-tech-law-oct-skills-drones` | 3 | 2 | 1 | 0 | 09-28 to 09-30 |
| tech-law-oct | Meta | meta_Skills: lawyer at a space tech company | `meta-tech-law-oct-skills-space-tech` | 2 | 2 | 0 | 0 | 09-29 to 10-03 |
| tech-law-oct | Meta | meta_Lawyers in small towns | `meta-tech-law-oct-63-small-town` | 6 | 2 | 4 | 0 | 10-09 to 10-12 |
| tech-law-oct | Meta | meta_Women lawyers after a break | `meta-tech-law-oct-75-career-break` | 2 | 2 | 0 | 0 | 10-12 to 10-13 |
| tech-law-oct | Meta | meta_20 tasks: deep tech legal job | `meta-tech-law-oct-20tasks-deeptech` | 1 | 1 | 0 | 0 | 09-26 to 09-26 |
| tech-law-oct | Meta | meta_Skills: lawyer at a defence tech company | `meta-tech-law-oct-skills-defence-tech` | 1 | 1 | 0 | 0 | 09-28 to 09-28 |
| tech-law-oct | Meta | meta_Skills: lawyer at a fintech company | `meta-tech-law-oct-skills-fintech` | 2 | 1 | 1 | 0 | 09-29 to 09-29 |
| tech-law-oct | Meta | meta_Lawyers in small towns | `meta-tech-law-oct-73-small-town` | 3 | 1 | 2 | 0 | 10-05 to 10-13 |
| tech-law-oct | Meta | Document review teams | `meta-tech-law-oct-23-lpo-staff` | 2 | 0 | 2 | 0 | 09-25 to 09-28 |
| tech-law-oct | Meta | Lawyers outside the metros | `meta-tech-law-oct-03-outside-metros` | 3 | 0 | 3 | 0 | 09-26 to 09-30 |
| tech-law-oct | Meta | meta_Rerun: your court skills already work in tech law | `meta-tech-law-oct-rerun-litigators` | 1 | 0 | 1 | 0 | 09-27 to 09-27 |
| tech-law-oct | Meta | meta_Question: Kerala law graduate to remote UK job | `meta-tech-law-oct-broad-kerala-question` | 1 | 0 | 1 | 0 | 09-30 to 09-30 |
| tech-law-oct | Meta | meta_Rerun: international career in technology law | `meta-tech-law-oct-rerun-international` | 1 | 0 | 1 | 0 | 09-30 to 09-30 |
| tech-law-oct | Meta | meta_Law firm associates | `meta-tech-law-oct-64-firm-associates` | 1 | 0 | 1 | 0 | 10-01 to 10-01 |

Sums of the rows above (my arithmetic, not an artifact figure): Oct-tagged Meta funnels 2,967 sign-ups and 2,223 paid (75%), 50 failed; Oct-tagged Google funnels 1,630 sign-ups and 478 paid (29%), 157 failed. Aug-tagged Meta funnels 114 sign-ups and 55 paid; the Aug-tagged Google funnel (bigtech) 172 and 85. Aug data starts 14 Aug, one day before the camp, so it misses most of the Aug run.

### 1e. 15 to 17 Aug 2026 camp: the launch kit (Tech Law Meta Launch Copy Sheet, published 7 Aug 2026)

Camp: live online, 15 to 17 Aug 2026, Rs 10 for all 3 days, LawSikho. "8 ads to 7 funnels." Sheet notes: build carousel cards in filename order and turn off Meta's "show best performing cards first"; never point an ad at another ad's page (c6 and c7 share one page); "A test Rs 10 purchase has not been run yet." Promise in every primary text: "the client plan that gets you tech disputes work in 6 months" (litigators) or "tech law work in 6 months" (others).

| Ad | Format | Reader (kit audience) | Headline (Meta headline field) | First line of primary text | LP slug (growthx.lawsikho.com/f/...) | GrowthX result (14 Aug onward, Ad Intelligence Studio) |
|---|---|---|---|---|---|---|
| Lit 01, Disputes wave | Single image | Practising litigators, 2 to 10 years (targeted by education or job title, age 24 to 40) | "Tech disputes are coming to your court. Rs 10" | "The next wave of litigation is tech disputes." | meta-tech-law-lit-01-disputes-wave | 39 sign-ups, 17 paid, 19 form only |
| Lit 02, Skills transfer | Single image | Same | "Add tech disputes to your practice. Rs 10" | "Your court skills already work in tech law." | meta-tech-law-lit-02-skills-transfer | 8 sign-ups, 6 paid |
| Lit 03, No seniors | Single image | Same | "Be the specialist, not the junior. Rs 10" | "In tech law, no senior is 20 years ahead of you." | meta-tech-law-lit-03-no-seniors | 64 sign-ups, 29 paid, 25 form only (best Aug Meta ad in GrowthX) |
| C8, Walkout | Carousel, 6 cards | Lawyers and law students | "Draft your first tech law contract. Rs 10" | "Draft your first tech law contract this weekend, live..." | meta-tech-law-c8-walkout | No row found in GrowthX |
| C9, Become | Carousel, 6 cards | Lawyers and law students | "Become a tech lawyer in 6 months. Rs 10" | "You can become a tech lawyer in the next 6 months..." | meta-tech-law-c9-become | No row found in GrowthX |
| TL 08, Firms staffing | Single image | Lawyers and law students | "Firms are hiring for tech law. Rs 10" | "Top law firms are staffing up their tech practices." | meta-tech-law-firms-staffing | 1 sign-up, 1 paid |
| C6, 10 reasons (long cut) | Carousel, 10 cards | Lawyers and law students | "10 reasons to move into tech law now. Rs 10" | "Tech law is exploding in India, and this carousel gives you 10 reasons why." | meta-tech-law-10-reasons (shared with C7) | 2 sign-ups, 2 paid (C6 and C7 combined) |
| C7, 10 reasons (short cut) | Carousel, 5 cards | Same | Same | Same | meta-tech-law-10-reasons | See C6 |

Other Aug-era Tech Law funnels (GrowthX, "Unassigned" camp tag, 14 to 16 Aug): Meta_Tech-Law_hottest 37 sign-ups / 25 paid; topchoice 15 / 9; international 18 / 7; bootcamp 7 / 5; shapefuture 2 / 0. Google: Tech_Law_Bootcamp_Demand 182 / 18 (ran to 13 Oct); hottest 128 / 24; bootcamp 108 / 14; international 84 / 8; whylearn 64 / 6; macro 20 / 6; Google_Tech-Law_bigtech (tagged tech-law-aug) 172 / 85 (ran to 29 Sep).

No Meta spend, CPP or Ramanuj verdict for any Aug ad appears in any artifact. The only Aug outcome figure is "Leads per completed camp: 15 to 17 Aug 2,083" (Daily Ad Desk; 2,117 is quoted for a different product line on the same list).

### 1f. Older Tech Law campaigns (Bootcamp Ads Complete Report, pulled 18 Aug 2026; year of each flight not given)

| Campaign | Account | Lifetime spend Rs | Lifetime conv. | Lifetime CPL Rs |
|---|---|---|---|---|
| LS_Tech_Law_06_09_Oct | Skill Arbitrage | 2,08,663 | 478 | 437 |
| Tech_Law_Bootcamp_6_9_Oct (OUTCOME_LEADS) | LawSikho Ad Account 3 | 1,98,645 | 8 | 24,831 |
| Tech_Law_Bootcamp_3_5_June (two copies), Tech_Law_Bootcamp_17_19_December | LS Acct 3 and 4 | 0 | 0 | none |

These are past flights still marked ACTIVE in Meta. The 15 to 17 Aug 2026 campaign is not in this list (it was not in the active set on 18 Aug). Note an old LS_Tech_Law flight ran in the Skill Arbitrage account, which would be a LawSikho / SkillArbitrage co-branding issue if repeated.

### 1g. New Tech Law videos built for the 24 to 26 Oct camp (not yet in any performance data)

| Video | Artifact (date) | Format | Reader | Hook | Status |
|---|---|---|---|---|---|
| Restart in Tech Law | Restart in Tech Law (15 Oct) | Claymation, 74 s, 9:16, 14 shots, narration (Women Second Innings voice clone) | Women lawyers back after a family break | "This is for women lawyers who took a break for their family. Listen to me." (third person on purpose, for Meta's personal-attributes policy) | Finished 15 Oct. Gate 1 (script, look, frames) and Gate 2 (147 credits of clips) marked approved; approver not named. Notes flag "Very few lawyers can do it" as an unverified claim and the end card offer facts to match the page: 24 to 26 Oct, live only, Rs 10 incl. GST |
| Litigator to Startup Lawyer | Litigator to Startup Lawyer (v3, 16 Oct) | UGC, photoreal AI advocate, 73 s, 13 shots, voice B, lip-sync | Litigators who want work outside the courtroom | "If you are a litigator who wants legal work outside the courtroom, listen to me." End card "Legal work outside the courtroom", Register at Rs 10 | Finished. 374.5 credits spent. Notes: the user's script kept "Very few lawyers can do it" (unverified) and "The work comes by email" (reads as a promise of work) against the builder's advice; "how to reach startups in the US, UK, Canada and Europe" must match the page; Meta may show "AI info" |
| Junior Lawyer Copy-Paste | Junior Lawyer Copy-Paste (16 Oct) | Gen Z meme / POV, 78 s, 17 scenes, voice C, meme overlays | Junior lawyers in their first 3 years, "nobody is teaching you" | "If you are a junior lawyer in your first three years, and nobody is teaching you, listen to me." Overlay "POV: your senior said 'just use the old draft'" | Voiceover and 17 scene pictures made, no video yet; about 117 to 135 credits to finish. Notes: "Production needs to finish soon to leave run time"; flags "Every one you draft becomes work you can show the next client" (confidential client work) |
| The Drawer, live-action remake (S1, EN and Hinglish) | LawSikho Video Ad Playbook (13 Oct) | Live-action, 25 s, one person, phone camera | LLB holders not practising, career-break lawyers | "Your LLB has been in this drawer for how long?" then "US startups pay Indian lawyers $2,000 a month and more..." with on-screen "$2,000+ a month. From home." | Planned; slug pattern `meta-techlaw-video-s1-en`; ship before 24 Oct; control is the "Unused LLB: $2,000+ a month" funnel |

All three finished or in-build storyboards share one script spine: "Every startup and online business runs on contracts, website terms and refund policies ... In 3 live evenings, 24 to 26 October, we ... draft a software development agreement with you, clause by clause." None names who approved the script beyond "your" (the requester).

## 2. Winners and why

1. **TechLaw_Video_unusedllb (unused LLB reader, kinetic text).** Biggest ad in the camp by far: 1,479 Meta purchases at Rs 185 CPA (to 14 Oct, Meta Video Ads); 1,392 GrowthX leads at 0.83x camp CPL (Daily Ad Desk). Reasons stated in the artifacts: (a) it names a narrow life situation in the first words (Video Ad Playbook: "Identity callout in the first words ... Narrow job titles beat broad ones"); (b) "A number with a currency: '$2,000+ a month' ... The top Tech Law hook alone drove 1,377 paid" (Playbook); (c) format: "a person talking or plain kinetic text wins, 3D film stories lose" (Playbook, Desk sheet 12 Oct). Its ICP cell "Law grads with an unused LLB" is the only Tech Law cell the Desk says to repeat (0.85x on 1,550). Note: the November Ads Playbook and Scripts cite it at 0.99x on 1,475 against product-line par, so it is at par on that index, cheap only against its own camp average. Its daily purchases fell from 204 (1 Oct) to 53 (13 Oct) while spend stayed about Rs 17,000 to 19,000 a day.
2. **TechLaw_Video_comeback (women lawyers after a break, 3D story).** Lowest CPA of the Tech Law videos: Rs 167 on 205 purchases (Meta Video Ads); 0.86x on 170 leads (Desk); 0.87x on 205 (Nov Scripts). Highest hook rate among the big three (20.6%). Reason given: life-event reader ("career break" is in the Playbook's list of winning life events). Its reader is reused for IP Law November script "Women Lawyers Returning After A Break" on this evidence. Delivery was tailing off by 14 Oct (Rs 1,428 for 1 purchase).
3. **TechLaw_65_meme_career_break (static meme, same reader).** 0.91x on 43 leads, Rs 234 CPL (Desk). Supports the career-break reader across formats; Tech Law statics for career break (Rs 266, n=124, 0.94x) and women_lawyers (Rs 252, n=79, 0.89x) point the same way (Nov Scripts).
4. **Aug camp: Lit 03 "No seniors"** led the Aug Meta funnels in GrowthX (64 sign-ups, 29 paid from 14 Aug), ahead of Lit 01 (39 / 17). No cost data exists for it, so it cannot be called a winner on cost.

## 3. Losers and why

1. **Reader cells the Desk marks "Avoid" with 20+ leads:** Lawyers doing US paralegal work 1.90x (Rs 486, 101 leads; the "20 tasks: US paralegal $2,000+" family), Lawyers seeking remote work 1.73x (Rs 442, 69 leads), Law firm TMT associates 1.45x (Rs 371, 35 leads). These match the November Playbook rule that aspiration readers ("wants remote work", "wants global clients") beat par only 3% of the time, and the CLAUDE.md offer rule against "same desk" readers (TMT associates).
2. **Cells labelled Avoid on 2 to 14 leads** (mid-career, banking lawyers, fresh grads, space, international, e-commerce, Kerala). Treat as not tested, not as beaten; the Desk's own rule says calls need 20+ leads.
3. **TechLaw_Video_someonelikeyou (live-action film, blurred opener).** 1.57x on 5 leads (Desk), Rs 234 CPA on 8 purchases (Meta). Meta barely funded it (Rs 1,870). Fits the Deep Dive finding that story or riddle openers beat par only 10 to 32% of the time and the "no named reader" pattern. Under 20 results, so not a firm call.
4. **TechLaw_Video_careerbreak_nogap (film scene, two actors).** 1.12x on 17 leads (Desk); CPA Rs 190 on 24 purchases (Meta). Too small to judge; overlaps the cheaper comeback video's reader.
5. **TechLaw_Video_drawer (3D).** At par, not a loser: 0.94x (Desk), 0.93x (Playbook). The Playbook's stated reason it trails the unused LLB video: 3D character format; "a real person with the real drawer beats both the 3D drawer (0.93x) and the kinetic-text version (0.82x). Shoot it live-action, not 3D."
6. **Aug kit carousels C8 and C9** have no GrowthX rows at all, and C6/C7 drew 2 paid between them; TL 08 Firms staffing drew 1. No spend figures exist, so "never funded" and "lost" cannot be told apart.
7. **Old flight Tech_Law_Bootcamp_6_9_Oct (LS Acct 3, lead objective):** Rs 1,98,645 for 8 conversions (Rs 24,831 each). No reason given in the artifact.

## 4. Ramanuj verdicts

- **No Ramanuj verdict or approval on any Tech Law ad, video, reader or page appears in any artifact read.** Storyboard "gates" in Restart in Tech Law and Litigator to Startup Lawyer are marked approved, but the approver is the requester ("your go-ahead"), not Ramanuj. The Drawer Storyboard is titled "video concept for approval" with no recorded verdict, yet the video was live from 8 Oct.
- Ramanuj verdicts that do appear are for other products: Independent Director educators banned, 12 Oct 2026, "44% attendance and almost no sales. A cheap cost per lead hid it" (Daily Ad Desk, November Ads Playbook). The NCA founder-story video is "Shoot after Ramanuj approves" (Video Ad Playbook). Ad Maestro shows Ramanuj "learnings" but the page is labelled "mock, fake data", so they are not evidence.
- Calls that need Ramanuj and are open: whether the "$2,000+ a month" income figure can stay on Tech Law faces and funnel names (CLAUDE.md rule 5 bans income figures on the face; the Playbook itself says "legal should check every claim: the $2,000 figure"); the Google to Meta budget move the Desk recommends; whether Tech Law gets a November camp.

## 5. Known funnel or page problems

1. **Google sign-ups do not pay.** Daily Ad Desk, 13 Oct: "the two Google small-town pages took 586 sign-ups in 6 days and only 113 paid (19%); 43 payments failed. Meta Tech Law pages close 75% and Google's lp2-that-someone-can-be-you page closes 74%. The page is not broken: opened 13 Oct, the Rs 10 checkout opens normally. Google's visitors sign up and do not pay." GrowthX (Studio) shows the same: google_Lawyers in small towns (63) 618 sign-ups, 112 paid, 373 expired, 68 failed; (73) 315 sign-ups, 69 paid, 207 expired, 30 failed. Last-7-day expired checkouts: Google 448 vs Meta 210 (Desk). Cross-product: payments fail on 11.6% of Google funnels vs 2.5% on Meta (November Ads Playbook); Google costs Rs 481 vs Meta Rs 227 per GrowthX buyer on paid camps.
2. **Pace gap.** Tech Law needs 325 seats a day and is adding 166 (Desk, 13 Oct), 2,579 banked against a 6,000 target with about 10 days left.
3. **Unused LLB video fatigue signal.** Purchases a day fell from 204 (1 Oct) to 53 (13 Oct) at similar spend (Meta Video Ads daily bars); frequency 2.76. The November Ads Playbook says ads showed no fatigue inside a camp on average, so read this as a reader or audience-size limit to watch, not proof of wear-out.
4. **Income figure in funnel names and a planned script.** GrowthX funnel titles "meta_Unused LLB: $2,000+ a month" and "20 tasks: US paralegal $2,000+", and the Playbook's live-action Drawer script ("US startups pay Indian lawyers $2,000 a month and more"; on-screen "$2,000+ a month"). Whether that text is on the ad face or only in the funnel name is not shown in the artifacts; check before reuse. Also "Very few lawyers can do it" and "The work comes by email" remain in the Litigator video (flagged by the builder).
5. **Aug launch:** "A test Rs 10 purchase has not been run yet" was the status on the copy sheet at publication (7 Aug); no artifact confirms it was done. Every Aug primary text promises "tech law work in 6 months", which reads as an outcome promise.
6. **No page-speed data for Tech Law** appears in any artifact. The only page check found is Ad Maestro's "checked every hour: load time, buy button, dates", and that page runs on fake data.
7. **Measurement gaps:** the Video Ad Playbook says Meta spend for statics was missing (statics judged on paid rate only); Meta purchase counts (Meta Video Ads page) and GrowthX leads (Desk) differ by ad, and spend differs between the two pages (for example unused LLB Rs 2,73,954 to 14 Oct on one, Rs 2,97,249 incl. GST to 13 Oct on the other).

## 6. Planned next for Tech Law (as the pages state it)

- **Budget:** "Move most of Tech_Law - DG (about Rs 9,000 a day) to Meta Tech Law and to Tech Law Bootcamp DG1.0. Keep the small-town pages on Meta only." (Daily Ad Desk, 13 Oct)
- **Readers:** repeat "Law grads with an unused LLB"; do not repeat TMT associates, remote-work and US-paralegal cells; 18 cells listed as untested for lack of spend (Desk brief, 13 Oct).
- **New videos for 24 to 26 Oct:** Restart in Tech Law (claymation, finished 15 Oct), Litigator to Startup Lawyer (UGC, finished v3 16 Oct), Junior Lawyer Copy-Paste (meme POV, pictures and voice done, video not made; "needs to finish soon"). The Playbook also plans a live-action 25 s Drawer (S1, English and Hinglish) as `meta-techlaw-video-s1-en`, ship before 24 Oct, judged after 3 days or 100 leads: a video wins if its paid rate is 5+ points above its static at similar volume; also read expired checkouts; cost needs a Meta export.
- **November:** Tech Law has no camp in the November Ads Playbook calendar (MAIN camps listed: Women AI, US Accounting, Independent Director 14 to 16 Nov; Academic Writing, US Corporate Law 21 to 23 Nov; Global Patent, IP Law 28 to 30 Nov) and none of the 70 November Video Scripts is for Tech Law. Instead, two Tech Law readers are carried into IP Law scripts: "Women Lawyers Returning After A Break" (proven video, from TechLaw comeback 0.87x on 205) and "LLB Graduates Working Outside Law" (at par, from TechLaw unused LLB 0.99x on 1,475). Litigators appear as a new IP Law reader (#1, "thin").
- **Old Meta Tech Law campaigns** (Jun, Oct, Dec flights) are still flagged ACTIVE and need an archival pass (Bootcamp and Community Pulse, Bootcamp Ads Complete Report).

## 7. Cross-product lessons that matter for Tech Law (briefly)

- **Video vs static: same cost.** Video 1.00 vs static 1.00 inside the same campaigns (14,919 and 160,191 results); Tech Law video 1.01 vs static 0.99 with 45% of spend on video (November Ads Playbook). Deep Dive: in 58 campaigns video was cheaper in 26 and dearer in 27. Google Demand Gen video Rs 196 vs image Rs 211 a conversion. Video adds placements and variety, not conversion.
- **What makes a video cheap** (Video Ads Deep Dive, 201 videos): say the offer out loud (0.89x; "free" 0.85x), selfie-style presenter at home or outdoors (0.86x), name the reader in the first line and define the work in concrete tasks (0.89x), explicit call to action (no CTA 1.72x, none beat par), script 100 to 220 words. Length, gender, polish, captions and hook rate do not predict cost (hook rate rank correlation 0.15). Story, riddle and pain-first openers beat par only 10 to 32% of the time.
- **Format by cost** (Video Ad Playbook, Desk sheet 12 Oct): talking head or plain kinetic text 0.70 to 0.85x; 3D character 0.93x to 2.28x; 3D film stories 1.44x to 2.41x. A high paid rate does not mean a cheap video (Academic Writing videos convert 78% but cost 1.2 to 1.35x).
- **Timing and waves** (November Ads Playbook): launch at T-28; videos launched 30 days or 5 days out priced the same; waves of 6 to 8 ads every 5 to 7 days (a fresh wave made the campaign 7 to 9% cheaper for 3 days); in batches of 21+ only 20% of ads reached 20 results; no new ads in the last 4 days (1.12); give new readers their own ad set with a minimum spend; never refresh a winner's face (0 of 17 improved), refresh a loser's once (11 of 17 improved); re-runs of winning faces held par in 5 of 7.
- **Reader choice** (November Ads Playbook): named occupations beat par 21% of the time, life situations 12%, broad populations 8%, aspiration-only readers 3%. Past results predict weakly (correlation 0.23), so run readers as a portfolio. Pay charts and chat faces lose (2.3x and 1.28x).
- **Hook rate is not a cost signal** on this account (Daily Ad Desk, 5 Oct read; Deep Dive). Judge on cost with 20+ results.

## 8. Artifacts read with no Tech Law content

- October Top Twenty (8 Oct): Women Remote 3 to 5 Oct campaign only.
- Top Ads by Bootcamp (7 Oct): Strategic HR, Women AI, US Accounting, Independent Director, US Corporate Law, Academic Writing, Global Patent, IP Law; no Tech Law section.
- Live Bootcamp Campaigns (19 Aug): the 5 live campaigns were Senior AI, HR, Content Writing, Data Privacy, Women AI; no Tech Law.
- Bootcamp and Community Pulse (18 Aug): no Tech Law campaign live.
- Ad Maestro (14 Oct): a mock running on fake data; its numbers (for example "Junior litigators Rs 258") are not evidence.
- NCA Video Scripts, NCA Video Ads Creative Brief, New Grad Pages, LP transfer, Legal Tech Drafting, Startup Contract Drafting, Legal Career From Home (Contract Drafting, Rs 200), Second Innings Storyboard (Independent Director), The Results Table Storyboard (Academic Writing): no Tech Law ads; the NCA scripts only cite the unused LLB video (0.82x on 1,346) as the format model.
- Bootcamp Ads Complete Report: only the older Tech Law flights in section 1f.
