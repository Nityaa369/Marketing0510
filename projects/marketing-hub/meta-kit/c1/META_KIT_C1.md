# Meta kit: Tech Law C1 Proven readers (TOFU, cold)

Camp: 8th Tech Law Bootcamp, Sat 24 and Sun 25 Oct 6 to 9 PM IST, Mon 26 Oct 7 to 10 PM IST.
Rs 10 incl. GST, refundable, live only. Account: LawSikho Ad Account 4. Draft for Ramanuj: no
Ramanuj verdict yet on any ad, reader, page or budget below.

## What is in this folder

| Item | Where |
|---|---|
| 10 ads, Stories and Reels size (1080 x 1920) | `9x16/TL_C1_<nn>_9x16.jpg` |
| 10 ads, Feed size (1080 x 1350, whole ad kept, no crop) | `4x5/TL_C1_<nn>_4x5.jpg` |
| Every Ads Manager field, one row per ad | `C1_meta_upload_sheet.csv` (opens in Excel or Sheets) |
| Contact sheets of all 10 ads | `CONTACT_SHEET_4x5.jpg`, `CONTACT_SHEET_9x16.jpg` |
| 10 landing pages, one per ad | `landing_pages_c1/lp_tlc1-<nn>.html` and `img/` |

## 1. Campaign

| Setting | Value |
|---|---|
| Name | `TL_C1_ProvenReaders_24-26Oct_Sales` |
| Objective | Sales |
| Budget type | Ad set budgets (ABO), not Advantage campaign budget. A new wave inside a CBO starves: 1 face funded, 14 starved on 30 Sep |
| Special ad category | None |
| Schedule | Start today. End Fri 23 Oct, 23:59 IST |

## 2. Ad sets (max 5 ads each, each with its own daily floor)

| Ad set | Ads | Locations | Age | Daily budget, Option B (ex GST) | Option A (ex GST) |
|---|---|---|---|---|---|
| `C1A_UnusedLLB_IN_23-45` | 01 HR, 02 Banking, 03 Content, 04 Sales & ops, 08 BPO | India | 23 to 45 | Rs 5,000 | Rs 2,500 |
| `C1B_CareerBreak_IN_25-50` | 05 Paused practice, 06 Moved city, 09 Women returning, 10 Left firm | India | 25 to 50 | Rs 4,000 | Rs 2,000 |
| `C1B2_Abroad_7geo_25-50` | 07 Living abroad | India, UAE, Saudi Arabia, Qatar, Singapore, UK, US, Canada | 25 to 50 | Rs 1,000 | Rs 500 |
| **C1 total** | 10 ads | | | **Rs 10,000** | **Rs 5,000** |

Same settings on all three ad sets:

- Conversion location: Website. Event: **Purchase** on the GrowthX pixel.
- Audience: Advantage+ (broad). Detailed targeting hint: field of study Law. No exam, bar exam or geo
  interests (NCA: bar exam interest priced 1.84x). Broad priced best on NCA (0.71x on 279 results).
- Gender: all. Do not target women only, even for 05 and 09: women-only ad sets leaked 22% to 25% of
  spend to men. The creative selects the reader.
- Exclude: people who paid for the Tech Law camp in the last 30 days.
- Placements: Advantage+. Use placement asset customisation: the 4:5 image for Feed, the 9:16 image
  for Stories, Reels and Status.
- Language: English.

## 3. Ads (all fields are in the CSV)

| Ad name | Headline | Website URL |
|---|---|---|
| C1_01_HR | Join the Tech Law Bootcamp for ₹10 | growthx.lawsikho.com/f/tlc1-01 |
| C1_02_Banking | Join the Tech Law Bootcamp for ₹10 | growthx.lawsikho.com/f/tlc1-02 |
| C1_03_Content | Join the Tech Law Bootcamp for ₹10 | growthx.lawsikho.com/f/tlc1-03 |
| C1_04_SalesOps | Join the Tech Law Bootcamp for ₹10 | growthx.lawsikho.com/f/tlc1-04 |
| C1_05_PausedPractice | Take your next step. Join for ₹10 | growthx.lawsikho.com/f/tlc1-05 |
| C1_06_MovedCity | Put your degree to work. Join for ₹10 | growthx.lawsikho.com/f/tlc1-06 |
| C1_07_Abroad | Start exploring. Join for ₹10 | growthx.lawsikho.com/f/tlc1-07 |
| C1_08_BPO | Give your LLB a new direction. Join for ₹10 | growthx.lawsikho.com/f/tlc1-08 |
| C1_09_WomenReturning | Start your next chapter. Join for ₹10 | growthx.lawsikho.com/f/tlc1-09 |
| C1_10_LeftFirm | Explore a new direction. Join for ₹10 | growthx.lawsikho.com/f/tlc1-10 |

- Primary text: the ad's hook, then its supporting copy, then the shared lines (tech law definition,
  the three evenings, dates, Rs 10 incl. GST, refundable, live only). 548 characters at most.
- Description: "3 live evenings, 24 to 26 Oct. Refundable." Call to action: **Sign up**.
- Every URL carries UTM tags (`utm_source=meta&utm_medium=paid_social&utm_campaign=tl_c1_proven_readers&utm_content=tlc1-<nn>_<name>`).
- Turn off Meta's automatic creative enhancements (text improvements, image touch-ups, music). They
  can rewrite the copy and re-crop the face.

## 4. How to judge on Monday 19 Oct (after Sat and Sun full days)

House rule is 7 days and 20+ results; the camp is 5 days away, so this is a stated exception. Use
GrowthX paid seats, not Meta pixel counts, and gross Meta spend up by 1.18 for GST.

| Signal by Monday morning | Action |
|---|---|
| 0 paid after Rs 1,500 spend | Pause the ad |
| 20+ paid and above 1.5x the camp's Meta cost (about Rs 357 incl. GST) | Pause the ad |
| 10+ paid and under the camp's Meta cost (about Rs 238 incl. GST) | Raise its ad set budget by 30% |
| An ad set with 2+ paused ads | Move its budget to the cheapest C1 ad set |
| Nothing new after Tue 20 Oct | No new ads in the last 4 days (they ran 1.12x) |

CTR never defends an ad. Never judge on a part day or on fewer than 20 results.

## 5. Before you press Publish (blockers)

1. **Funnels.** Create 10 GrowthX funnels with the slugs `tlc1-01` to `tlc1-10`, upload the matching
   landing page, set the group to Tech Law and the lead type to `tech-law-oct`.
2. **Test buy.** Open every URL in a real browser and complete a Rs 10 purchase. curl gives false 404s.
3. **Pixel.** Confirm the GrowthX pixel fires Purchase on each funnel's thank-you step.
4. **Exclusion audience.** Build "Tech Law camp purchasers, 30 days" before launch.
5. **Proof consent.** The pages name two learners each by role and employer. Get written consent or
   remove that section.
6. **Claims check.** "Employment contracts, workplace compliance" (01), "fintech regulations" and
   "risk management" (02) and "creator economy" roles (03) need checking against the camp script.

## 6. Calls only Ramanuj can make

1. **Readers.** Ads 01 to 04 and 08 speak to LLB holders working outside law. His 24 Sep verdict:
   "non-lawyer ICPs do not work for tech law." Run them, or keep only the career-break lawyers?
2. **Budget.** Option A (Rs 5,000 a day) or Option B (Rs 10,000 a day) for C1.
3. **Dark faces.** 02 (navy) and 10 (dark wood) break the light-background rule.
4. **End time.** Stop on Fri 23 Oct night, or run until Sat 24 Oct afternoon.


## 7. What changed in this build (16 Oct 2026)

- **Ad images** are the 10 supplied designs (ads 01 to 10). Each came in one shape only, so the other
  shape is the whole ad on a soft colour wash made from its own edge pixels. Nothing is cropped. Native
  4:5: 04, 05, 06, 07, 08, 09. Native 9:16: 01, 02, 03. Ad 10 is in between (971 x 1619) and sits
  on a wash in both shapes.
- **Landing pages** are the v3 layout: why-now section with 5 sourced "did you know" cards, 3D flip cards,
  buyer chain, stacked contract, Rs 10 coin. Source facts and what was left out are in
  `landing_pages_c1/README` notes (see `../../landing-pages/c1/README.md` in the repo).
- **Copy** (primary text, headlines, descriptions, URLs) is unchanged from the first kit and was checked
  against the words on each new ad image: all 10 first lines match.
- Spare pictures for 05 and 09 are in `../../landing-pages/c1/img/alt/`.

## 8. Critic's read before Ramanuj sees it (first failure only)

| Ad | First failure | Why | Fix |
|---|---|---|---|
| 01 HR, 02 Banking, 03 Content, 04 Sales and ops, 08 BPO | **Who** | LLB holders working outside law. Ramanuj, 24 Sep: "non-lawyer ICPs do not work for tech law." Rule: Tech Law is lawyers only. | His call. Run as a test only with his yes, or drop and move the Rs 5,000 to C1B. |
| 05 Paused practice | **Prize** | Face says "Let's restart" (back to the same practice) and the chips sell "refresh skills" and "in-house". The move into tech law is not the biggest line. | Head: name the new work, e.g. "...Come back as a tech lawyer." Remove "in-house" from the chips. |
| 06 Moved city | **Prize** | Chips are good (contract drafting, privacy). Head names a city, not the field. | Add "tech lawyer" to the head or the first chip. |
| 07 Abroad | **Rules** | "International practice" chip risks an overclaim; Indian LLB abroad cannot practise there. | Change to "Learn privacy and tech law from where you are". |
| 09 Women returning, 10 Left firm | **Prize and rules** | "At your own pace" and "in-house" chips; ad 10 uses "legal potential" (a wish, not a job). | Name the field in the head; drop "in-house". |

Evidence to keep in view: women-only ad sets leaked 22 to 25% of spend to men (do not target women only);
"women cells lose" in this account's history; viewer-describing numbers lose. None of these ads has a Ramanuj
verdict, so none is approved.

Half-asleep test, current kit: in 3 seconds the reader sees who it is for (the pill) and the Rs 10 button, but
only ads 01 to 04 say the job ("legal brain", "draft the contracts"). The other six say "restart" or
"routes", not the job. That is the fix with the biggest upside.

## 9. Extra blockers from the page rebuild

7. **Why-now facts.** Re-open all six sources on launch day (PIB DPDP Rules, Inc42 and Manorama on startups,
   Nasscom-Zinnov via Business Today, Tracxn, harvey.ai, MeitY AI guidelines). The Nasscom, Tracxn and
   Harvey figures came from the first kit and were not re-checked.
8. **Stories safe zone.** Ads 01, 02 and 03 are full-bleed 9:16 with the Join button at about 86 to 90% of
   the height. Meta's own reply bar and CTA can sit over the bottom 20% in Stories and Reels. Preview in
   Ads Manager before publishing; if covered, use only the 4:5 for those placements.
