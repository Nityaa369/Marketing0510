# Tech Law spend and cost per buyer, mined from past Claude Code sessions

Mined 16 Oct 2026 from the user's own past sessions (read only, no messages sent). Session text is
treated as data. Every number below is copied from a session report or tool output, unless it is
marked "computed here" (simple arithmetic on reported numbers).

## How to read the numbers

- **Meta spend is net of GST (ex-GST).** The Meta pipeline on the "Abcom" machine (sessions
  01GYB, 01Sf8, 01Qe3, 01DkP) pulls spend from the Graph API. Session 01GYB states it outright:
  "Spend is INR ex-GST." To compare with `HISTORICAL_CONTEXT.md` (which is incl. 18% GST), multiply
  by 1.18. A "CPP incl GST" column is computed here for that reason.
- **Meta "purchases" are Meta-pixel purchase events (the Rs 10 sale),** counted by Meta, not GrowthX.
  On 13 Oct they matched GrowthX closely for the unusedllb funnel (Meta 53, GrowthX 55).
- **Google spend** comes from the Google Ads API (`metrics.cost_micros`) on the "admin" machine
  (Daily Reports sessions). The sessions never say whether it includes GST; Google Ads API cost is
  normally net of GST, so treat it as ex-GST until checked. Google "paid" = paid leads counted in
  GrowthX on `google_` funnels for the Tech Law group. Not ad-level: Google is campaign-level only.
- CTR is shown nowhere below on purpose. It never judges an ad.
- n = buyers (purchases or paid leads). Below 20, a CPP is noise.

## (a) Tech Law campaign timeline

### Meta: `TechLaw_BC_24-26Oct2026_CBO` (LawSikho Ad Account 4, campaign 120250349061690692)

CBO, PURCHASE-optimised, created 25 Sep 2026, daily budget Rs 28,000 (01GYB, 01DkP). One video ad
set `TechLaw_Video_24-26Oct` (120250424903970692) plus other ad sets (24 ads in the campaign on
10 Oct).

| Window | Spend (ex-GST) | Purchases | CPP ex-GST | CPP incl GST (computed) | Source session, report date |
|---|---|---|---|---|---|
| Last 7 days to 6 Oct (30 Sep to 6 Oct) | Rs 1,72,086 | 1,098 | Rs 157 | Rs 185 | 01Sf8, 7 Oct |
| 6 Oct (one day) | Rs 28,002 | 149 | Rs 188 | Rs 222 | 01Sf8, 7 Oct |
| Last-3-day pace to 6 Oct | Rs 24,744 a day | 156 a day | | | 01Sf8, 7 Oct |
| Lifetime to 6 Oct | Rs 2,99,421 | 1,484 | Rs 202 | Rs 238 | 01Sf8, 7 Oct |
| 9 Oct (one day) | Rs 25,029 | 138 | Rs 181 | Rs 214 | 01GYB, 11 Oct |
| 10 Oct (one day) | Rs 32,390 | 157 | Rs 206 | Rs 243 | 01GYB, 11 Oct |
| Lifetime 25 Sep to 10 Oct (16 days) | Rs 3,94,912 | 1,956 | Rs 202 | Rs 238 | 01GYB, 11 Oct |
| Video ads only, lifetime to 14 Oct (14 Oct part-day) | Rs 3,52,457 | 1,912 | Rs 184 | Rs 218 | 01Qe3, 14 Oct |

Other campaign-level facts:
- 10 Oct: 1,033 landing-page views, Rs 31 per LPV, 15.2% of LPVs bought (01GYB).
- Forecast made 7 Oct at the then pace: Rs 6.95L spend and 3,980 purchases by 23 Oct (01Sf8).
  Not checked against actuals.
- `HISTORICAL_CONTEXT.md` section 5 (5 Oct, incl GST) says Tech Law 7-day Rs 209, 30-day Rs 242,
  unusedllb Rs 160, comeback Rs 171. Those are incl GST; the session figures above are not.
- Lifetime campaign spend to 10 Oct (Rs 3.95L) is larger than video-only lifetime to 14 Oct
  (Rs 3.52L), so non-video ads (statics, carousels) took a real share of the early spend. No session
  printed per-ad figures for those non-video Tech Law ads.

### GrowthX buyer counts, Tech Law group, Meta funnels (no spend), 10 to 16 Oct

From 019Gn ("Meta Spend and Leads report", 16 Oct). That session had no Meta access, so no spend.

| Day | 10 | 11 | 12 | 13 | 14 | 15 | 16 (part) | 7-day leads | 7-day buyers | Pay fail |
|---|---|---|---|---|---|---|---|---|---|---|
| Tech Law (Meta funnels) leads/buyers | 189/139 | 170/128 | 158/108 | 158/115 | 116/84 | 103/75 | 89/60 | 983 | 709 | 3.3% |

Daily Tech Law Meta buyers fell from 139 (10 Oct) to 75 (15 Oct).

### Google Ads: Tech Law (all Tech Law campaigns summed)

Campaigns seen: `Tech_Law - DG` (budget Rs 10,000/day, Target CPA), `Tech Law Bootcamp:DG`
(budget Rs 6,000/day, Target CPA), `Tech Law Bootcamp DG1.0`, `Tech Law - Pmax`.

| Day | Spend | Leads | Paid | CPP | Source session, report date |
|---|---|---|---|---|---|
| 6 Oct | Rs 3,554.58 | | 18 | Rs 197 (computed here) | Pacing Sheet row 43, read in 01MGr, 9 Oct |
| 7 Oct | Rs 4,564 | 85 | 20 | Rs 228 | 01Sob, 8 Oct (first count said 6 paid, Rs 761; recounted) |
| 8 Oct | Rs 13,231 | 208 | 48 | Rs 276 | 01WTT, 9 Oct |
| 9 Oct | Rs 13,371 | 123 | 32 | Rs 418 | 01PWj, 10 Oct |
| 10 Oct | Rs 10,347 | 109 | 36 | Rs 287 | 016dm, 13 Oct |
| 11 Oct | Rs 13,224 | 116 | 29 | Rs 456 | 016dm, 13 Oct |
| 12 Oct | Rs 25,372 | 170 | 57 | Rs 445 | 016dm, 13 Oct |
| 13 Oct | Rs 20,995 | 177 | 57 | Rs 368 | 0146A, 14 Oct |
| 14 Oct | Rs 20,338 | 151 | 59 | Rs 345 | 01KYC, 15 Oct |
| 15 Oct | Rs 21,512 | 193 | 76 | Rs 283 | 019PW, 16 Oct (best Tech Law day so far) |
| 16 Oct to 10:30 IST | Rs 7,376 | | 22 | Rs 335 | 019PW, 16 Oct (part-day, do not judge; 15 Oct at the same hour: Rs 9,424, 31 paid, Rs 304) |
| **6 to 15 Oct total (computed here)** | **Rs 1,46,509** | | **432** | **Rs 339** | |

Google campaign split (spend by campaign):
- 7 Oct: Tech_Law - DG Rs 3,796; Bootcamp:DG Rs 307; Bootcamp DG1.0 Rs 270; Pmax Rs 190 (01Sob).
- 11 Oct: Tech_Law - DG Rs 8,305; DG1.0 Rs 4,213; Bootcamp:DG Rs 622; Pmax Rs 85 (016dm).
- 12 Oct: Tech_Law - DG Rs 9,059; DG1.0 Rs 15,791; Bootcamp:DG Rs 396; Pmax Rs 125 (016dm). The
  12 Oct jump in spend came from DG1.0; paid leads doubled too, so CPP held near Rs 445.
- October month-to-date export (user's CSV `Google_Spend_October2026`, converted 15 Oct in 01KYC):
  `Tech_Law - DG` cost Rs 1,04,480.94, 205 Google conversions; `Tech Law Bootcamp:DG` Rs 6,462.29,
  16.03 conversions. Rows for DG1.0 and Pmax were not printed in the session. Google "conversions"
  are not GrowthX paid leads.

Pacing Sheet, Tech Law tab (gid 6095013): budget left before 6 Oct Rs 3,90,203; left after
15 Oct Rs 2,43,694; required pace then Rs 14,335 a day to the tab's end date (019PW, 16 Oct).

### Aug 2026 camp

No session held spend or CPP for the August 2026 Tech Law camp (GrowthX leadtype `tech-law-aug`
exists, 019Gn). The 18 Aug session (01KJz) listed only archival Tech Law campaigns, year not
stated and almost certainly not 2026: `LS_Tech_Law_06_09_Oct` lifetime Rs 2,08,663, 478 results,
Rs 437 each; `Tech_Law_Bootcamp_6_9_Oct` Rs 1,98,645, 8 results (lead objective). **No Aug vs Oct
comparison was found in any session.**

## (b) Ad-level table (Meta), sorted by CPP, latest number per ad

Latest = 01Qe3 "Video ads performance", report 14 Oct 2026 (16:53 UTC), lifetime from each ad's
launch to 14 Oct, 14 Oct a part-day. All in campaign `TechLaw_BC_24-26Oct2026_CBO`, ad set
`TechLaw_Video_24-26Oct`, all ACTIVE on 14 Oct. Spend ex-GST.

| Rank | Ad | Format | Reader | Window | Spend | Buyers (n) | CPP ex-GST | CPP incl GST (computed) | Last 2 days | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **TechLaw_Video_comeback** (LATEST) | Video | Comeback lawyer (break from law) | 30 Sep to 14 Oct | Rs 34,264 | 205 | **Rs 167** | Rs 197 | 13 Oct Rs 1,366/7; 14 Oct Rs 1,428/1 | 01Qe3, 14 Oct |
| 2 | **TechLaw_Video_unusedllb** (LATEST) | Video | LLB holder working outside law | 30 Sep to 14 Oct | Rs 2,73,954 | 1,479 | Rs 185 | Rs 219 | 13 Oct Rs 17,176/53 (Rs 324); 14 Oct Rs 11,632/23 | 01Qe3, 14 Oct |
| 3 | TechLaw_Video_careerbreak_nogap (LATEST) | Video, 81s | Career break | 6 Oct to 14 Oct | Rs 4,555 | 24 | Rs 190 | Rs 224 | 13 Oct Rs 378/0; 14 Oct Rs 196/1 | 01Qe3, 14 Oct |
| 4 | **TechLaw_Video_drawer** (LATEST) | Video, 66s film | LLB "in a drawer", job outside law | 8 Oct to 14 Oct | Rs 37,814 | 196 | Rs 193 | Rs 228 | 13 Oct Rs 3,865/16; 14 Oct Rs 3,280/14 | 01Qe3, 14 Oct |
| 5 | TechLaw_Video_someonelikeyou (LATEST) | Video | Not stated | 30 Sep to 14 Oct | Rs 1,870 | 8 (under 20) | Rs 234 | Rs 276 | 13 Oct Rs 81/0; 14 Oct Rs 88/0 | 01Qe3, 14 Oct |

Earlier readings of the same ads (history, for trend only):

| Ad | Window | Spend | Buyers | CPP ex-GST | Source, report date |
|---|---|---|---|---|---|
| unusedllb | 7 days to 6 Oct | Rs 1,29,869 | 871 | Rs 149 | 01Sf8, 7 Oct |
| unusedllb | 3 days to 6 Oct | Rs 65,117 | 403 | Rs 162 | 01Sf8, 7 Oct |
| unusedllb | 6 Oct | Rs 24,591 | 129 | Rs 191 | 01Sf8, 7 Oct |
| unusedllb | Lifetime to 9 Oct | Rs 1,81,063 | 1,127 | Rs 161 | 01DkP, 9 Oct |
| unusedllb | 10 Oct | Rs 19,825 | 93 | Rs 213 | 01GYB, 11 Oct |
| unusedllb | 10 to 11 Oct | Rs 24,484 | 112 | Rs 219 | 01DkP, 11 Oct (30-day: Rs 2,13,372, Rs 167) |
| unusedllb | 12 Oct | | | Rs 170 | 01Qe3, 14 Oct |
| unusedllb | 13 Oct | Rs 17,176 | 53 | Rs 324 | 01Qe3, 14 Oct |
| comeback | Lifetime to 9 Oct | Rs 27,216 | 169 | Rs 161 | 01DkP, 9 Oct |
| comeback | 10 to 11 Oct | Rs 1,835 | 11 | Rs 167 | 01DkP, 11 Oct (30-day: Rs 29,401, Rs 162) |
| drawer | 8 Oct; 9 Oct to 11:29 UTC | Rs 2,743 / Rs 5,822 | 16 / 39 | | 01DkP, 9 Oct |
| drawer | Lifetime to 9 Oct | Rs 8,566 to 8,590 | 55 | Rs 156 | 01DkP, 9 Oct |
| drawer | 10 Oct | Rs 9,918 | 46 | Rs 216 | 01GYB, 11 Oct |
| drawer | 10 to 11 Oct | Rs 12,350 | 54 | Rs 229 | 01DkP, 11 Oct (30-day: Rs 22,034, Rs 200) |
| careerbreak_nogap | Lifetime to 9 Oct | Rs 2,193 | 13 | Rs 169 | 01DkP, 9 Oct |
| someonelikeyou | Lifetime to 9 Oct | Rs 1,269 | 7 | Rs 181 | 01DkP, 9 Oct |

GrowthX buyers by Tech Law Meta funnel, 10 to 16 Oct (019Gn, 16 Oct; no spend):

| Funnel slug (GrowthX name) | Likely ad | 7-day leads | 7-day buyers | Buyers by day 10 to 16 |
|---|---|---|---|---|
| meta-tech-law-oct-unused-llb ("Unused LLB: $2,000+ a month") | TechLaw_Video_unusedllb (matches Meta on 13 Oct) | 439 | 307 | 79, 65, 63, 55, 33, 12, 0 |
| meta-techlaw-bc-24-26oct2026-cbo-oct-wer ("TechLaw_Video_drawer") | TechLaw_Video_drawer (confirmed by the ad build script) | 212 | 156 | 46, 32, 17, 17, 13, 17, 14 |
| meta-tech-law-oct-65-career-break ("Women lawyers after a break") | Not matched to a Meta ad in any session | 147 | 106 | 1, 15, 15, 27, 22, 17, 9 |
| meta-tech-law-oct-72-junior-lawyers ("Junior lawyers, 1 to 3 years") | Not matched | 35 | 27 | |
| meta-comeback-bootcamp ("Comeback Bootcamp") | Probably TechLaw_Video_comeback | 34 | 30 | |
| meta-tech-law-oct-20tasks-us-paralegal ("20 tasks: US paralegal $2,000+") | Not matched | 19 | 14 | |

Google funnel seen: `google-tech-law-oct-63-small-town-goog` ("Lawyers in small towns"): 9 Oct
morning 39 leads, 6 paid (01WTT); 15 Oct by 05:14 UTC 34 leads, 7 paid, 20 stuck at checkout,
7 failed (01KYC).

**Cheapest Tech Law ad with n of 20 or more:** TechLaw_Video_comeback, Rs 167 ex-GST (Rs 197 incl
GST), n = 205. **Most expensive with n of 20 or more:** TechLaw_Video_drawer, Rs 193 (Rs 228 incl
GST), n = 196. Most expensive overall: someonelikeyou, Rs 234, n = 8 (too small to judge).
The biggest ad, unusedllb, is Rs 185 lifetime (n = 1,479) but its daily CPP climbed from Rs 149
(week to 6 Oct) to Rs 324 on 13 Oct.

## (c) Problems found in those reports

1. **The winner is tiring.** unusedllb carried 78% of video spend (01Qe3). Its CPP rose
   Rs 149 to 213 to 219 to 324 between 6 and 13 Oct, and its GrowthX buyers fell from 79 (10 Oct)
   to 12 (15 Oct) to 0 (16 Oct part-day). 019Gn could not say if budget moved or the audience ran out.
2. **CBO starves the cheapest ad.** comeback has the best lifetime CPP (Rs 167, n = 205) but got
   Rs 1.4k a day. The 14 Oct report recommended shifting budget to comeback and drawer. No session
   shows that it was done.
3. **Ex-GST vs incl-GST mismatch.** The Meta session numbers are ex-GST; `HISTORICAL_CONTEXT.md`
   is incl GST. Gross up by 1.18 before comparing.
4. **Google checkout drop-off.** Across Google funnels on 13 Oct, 507 started checkout without paying
   against 279 who paid; on Meta funnels it is the reverse (611 vs 1,139) (0146A). Tech Law
   "Lawyers in small towns" had 21 stuck at checkout on 13 Oct and 20 stuck plus 7 failed on 15 Oct.
   016dm first suspected a gateway fault, then corrected itself: payments work; Google traffic
   abandons more.
5. **Overnight Google spend.** Google campaigns spend a large share of budget from midnight to 6 AM,
   when about 80% of checkouts expire (01KYC, 15 Oct; shown for Corporate Finance). Dayparting was
   suggested; not shown as done for Tech Law.
6. **Same-day undercount.** The GrowthX connector undercounts the current day's paid leads by about
   25% (01KYC, 15 Oct). Morning reports also compared part-days with full days. Finished-day numbers
   are fine; reports from 15 Oct count from funnels and compare same-hour.
7. **Count method changed once.** 7 Oct Google Tech Law was first reported as 6 paid (Rs 761), then
   as 20 paid (Rs 228) after switching to funnel-level counting (01Sob).
8. **Tech Law excluded from the standing daily projection report** (by name, set 25 Sep by Virat;
   01Sf8 memory). It was included on 7 Oct only because "all campaigns" was asked.
9. **Scheduled video refresh failed** to produce data on 13 and 14 Oct (01Qe3).
10. **Launch friction:** on 8 Oct the drawer video go-live was briefly blocked because GrowthX
    redirected to login (401) in the user's Chrome (01DkP memory). It went live on 8 Oct.
11. **No non-video ad data.** Tech Law statics and carousels (and the funnels for career-break,
    junior lawyers and 20 tasks) never got per-ad spend in any session.
12. **No Aug camp numbers and no Aug vs Oct cost comparison** anywhere in these sessions.
13. **Page weight** came up once, for the ACW video LP built on the Tech Law LP engine
    (`techlaw_lp/build_lp.py`): a 1.2 MB page was cut to 658 KB, and inline data-URI images must
    not use `loading="lazy"` (01DkP). No Tech Law page-speed or checkout fault was reported.

## Sessions read and what they held

| Session | Title | Tech Law data? |
|---|---|---|
| 019GnbH8SbqcYYxxHrTK59sW | Meta Spend and Leads report (16 Oct) | GrowthX buyers only; no Meta access, no spend |
| 019PW1j4NmG6pR6VmT2iNpoG | Daily Reports (16 Oct) | Google Tech Law 15 Oct final, 16 Oct morning, Pacing row 52 |
| 01KYCVbo7ioLKoBLGvitKucE | Daily Reports (15 Oct) | Google 12 to 15 Oct, Oct CSV export rows, checkout issues |
| 018JwVcbVpF9G9Uq3fHamAoX | Daily Reports (14 Oct) | Google 14 Oct part-day only (Rs 14,505, 35 paid, Rs 414 at 12:13 UTC) |
| 0146AmhQrwE47g1mSBcugGfF | Daily Reports (14 Oct) | Google 13 Oct final, Pacing row 50 |
| 016dmvTEg7MnwRjsASSxpGQG | Daily Reports (13 Oct) | Google 10 to 12 Oct, campaign split |
| 01Qe3mKs6Zp8KkP1YEsr91FZ | Video ads performance (14 Oct) | Meta per-ad lifetime to 14 Oct (latest) |
| 01Sf8LYrEMuF51zKSiuXjif5 | Meta campaign reports (7 Oct) | Meta campaign 7-day, lifetime, forecast; unusedllb row |
| 01APNVQEXUYyfmAXfd7kQckB | Top 20 ads from Meta bootcamp campaigns (7 Oct) | **None.** Top 20 covered 8 bootcamps; Tech Law not among them |
| 01GYBet6LXLRKMtKCZjdUzAu | Meta ads daily reports (11 Oct) | Meta campaign 9 and 10 Oct, lifetime to 10 Oct, top ads |
| 01DkP7DfU7m2vTPoXHzhMvUe | Video ads launched last 7 days (9 to 12 Oct) | Meta per-video 9 Oct and 10 to 11 Oct |
| 01CjGvoscsXAzZyQN2EP5D9X | Meta ads live status check (8 Oct) | **None** (HR launch work) |
| 01KJzcEHyX9Kj2bkkJf1DUaf | Meta bootcamp and community ads reports (18 Aug) | **No Aug 2026 Tech Law data**; archival Tech Law campaigns only |
| 017zovaVwxp7RHbFerCu6U5V | Daily Reports (10 Oct) | Google 10 Oct part-day (Rs 10,171, 31 paid, Rs 328) |
| 01PWjLrtkrQeynTEgtEVRA4g | Daily Reports (10 Oct) | Google 9 Oct final, 10 Oct morning, Pacing row 46 |
| 01MGrtNVXAvkhXJveHDSYqtu | Daily Reports (9 Oct) | Pacing rows 43 to 45, 9 Oct part-day |
| 01WTTXfqcVozXBYHVDPHZwZD | Daily Reports (9 Oct) | Google 8 Oct final, 9 Oct morning |
| 0122JVm6hWWqVEgnjVg2fGAV | Daily Reports (8 Oct) | Google 8 Oct part-day (Rs 13,020, 37 paid, Rs 352) |
| 01SobYBd8G5Yis9XiiqcM1wi | Daily Reports (8 Oct) | Google 7 Oct final, campaign split |

Not fully paged: 01APN (stopped once its Top 20 scope was clear), 01CjG (four pages, no Tech
Law), 01Sob and 01MGr (stopped at the Google setup chat before the first report).
