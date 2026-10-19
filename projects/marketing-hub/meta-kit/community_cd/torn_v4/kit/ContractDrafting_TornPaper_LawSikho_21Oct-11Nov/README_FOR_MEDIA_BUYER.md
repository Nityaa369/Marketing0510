# README for the media buyer: LawSikho · Contract Drafting Community · torn-paper set (Meta)

20 static ads, 20 landing pages (1 ad = 1 page), one campaign, 4 ad sets of 5.
Camp: 21 Oct to 11 Nov 2026, live online, ₹200 incl. GST, refundable.

## What is in the folder

| Path | What |
|---|---|
| `ads/cd_01.jpg` to `cd_20.jpg` | The ads, 1024x1536 (2:3). Brand LawSikho only. |
| `landing_pages/lp_cd_01.html` to `lp_cd_20.html` | One page per ad, same number. Hero = the ad image in `landing_pages/img/`. |
| `CD_meta_upload_sheet.csv` | One row per ad: campaign, ad set, primary text, headline, description, CTA, URL, page, slug. |
| `ad_copy.md` | The same copy, readable. |
| `manifest.json` | Machine-readable map of ad, page, slug, URL and copy. |
| `value_props.md`, `hooks.md` | The approval records for each ad (better job, field definition, pressure, hypothesis). |
| `CONTACT_SHEET.jpg` | All 20 ads on one sheet. |

## Before launch (blocking)

1. **Create the 20 GrowthX funnels** `cdtp-01` to `cdtp-20` on growthx.lawsikho.com, each with
   its own page from `landing_pages/`, and set each funnel's `ctaLabels` to exactly
   **"Join the Contract Drafting Community for ₹200"**. If the button text and `ctaLabels`
   differ, the payment modal does not open. The sticky bar reads "Join for ₹200 · 21 days, live
   online": add it to `ctaLabels` too.
2. **Test-buy every page in a real browser** (curl gives false 404s on GrowthX).
3. **Re-open the why-now sources on launch day:** DPDP Rules 2025 (MeitY, notified 14 Nov 2025,
   PIB); startup counts (Inc42, Manorama Yearbook Apr 2026); UK Business population estimates 2025
   (Department for Business and Trade, Oct 2025).
4. **Exclude past Contract Drafting buyers** in every ad set (the funnel review found none excluded).

## Launch spec

- Campaign `CD_Community_TornPaper_21Oct-11Nov_Sales`, objective Sales, purchase event.
- Ad sets, at most 5 ads each (Ramanuj rule 12):
  - `A_StudentsAndNewLawyers`: 01, 02, 03, 04, 19
  - `B_LawyersNearContracts`: 05, 06, 16, 17, 18
  - `C_LawyersWhoseLifeMoved`: 07, 08, 09, 10, 20 (ad 10 targets Indians living abroad)
  - `D_LLBHoldersInOtherJobs`: 11, 12, 13, 14, 15
- Meta CTA: **Sign up**. Headline "Contract Drafting Community, ₹200". Brand LawSikho, never co-branded.
- **Routing, budgets and audiences are Ramanuj's call.** The grouping above is a proposal. Do not let
  this campaign bid against another live Contract Drafting campaign.
- Judge on cost per buyer over 7 full days and 20+ buyers per ad. Never on a part day, never on CTR.
  Budget moves of 20% a day or less.
- Placements: the ads are 2:3. Feed crops to 4:5, so preview each ad in Ads Manager and check the
  ICP tape (top) and the red button (bottom) stay visible. Ask for a 4:5 or 9:16 cut if they do not.

## Rules these files keep (do not edit them out)

- No dates on the ads; dates appear on the pages only, as plain text.
- No countdown, timer, "seats left" or "closes today" anywhere.
- No income figures, no job, client or income promise, no mention of any paid course.
- The only disclaimer is at the very bottom of each page; nothing hedges above a button.
- Pages work with JavaScript off and contain no analytics: GrowthX adds the pixel and gtag.

## Open items (owner: divyanshu)

- Camp script: every page claim traces to the CD 64-65 calendar; re-check against the script.
- Refund terms: pages say "refundable" only, with no process, until the script words it.
- Testimonials: none on the pages (none supplied with consent). Add two real ones under step 16 if available.
- Palette: all 20 ads share the template's red and yellow (Ramanuj rule 9 asks for one palette per
  ad). Pages keep the red button and vary their accent colour per page.
