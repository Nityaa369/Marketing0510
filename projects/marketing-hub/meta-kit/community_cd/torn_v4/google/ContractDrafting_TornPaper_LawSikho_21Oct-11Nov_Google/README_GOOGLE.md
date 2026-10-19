# Google kit: LawSikho · Contract Drafting Community · torn-paper set

20 ads for Performance Max or Demand Gen, the same readers, design and landing pages as the Meta kit.
Camp: 21 Oct to 11 Nov 2026, live online, ₹200 incl. GST, refundable. Draft for Ramanuj: no verdict
on any ad, reader, page or budget yet.

## What is here

| Item | Where |
|---|---|
| 20 ads x 3 sizes = 60 JPGs | `images/cd_NN_<reader>/` |
| Sizes | landscape 1200x628, square 1200x1200, portrait 960x1200 |
| Text assets per ad (5 headlines, long headline, 4 descriptions, business name, CTA, URL) | `GOOGLE_COPY_CD.csv` |
| Landing pages, one per ad (same files as Meta) | `landing_pages/lp_cd_NN.html` |
| Contact sheets, one per size | `contact_sheets/` |
| QA results | `QA_REPORT.md` |

## Design: same as Meta, by default

Per divyanshu's 16 Oct rule, the Google images are the Meta design, not a rebuild. Each ad is fitted
whole into the Google size and the spare space is a wash from the ad's own paper edge. No word on any
ad was changed. **Google policy risks in that art, flagged and not altered:**

1. **Arrow and button shape.** The red button with "→" is the pattern Google disapproved 7 times on
   this account (misleading ad design: an image that looks clickable).
2. **Trademark on the face:** "LinkedIn" in the support line of ads 07, 19 and 20.
3. **Personal situation on the face:** ads 08 ("women lawyers returning after a family break"),
   09 ("moved cities after marriage") and 20 ("left a law firm for family") name a personal situation.
   Google's personalised-ads policy can limit these. The text assets use neutral wording instead.
4. **All-caps tape** (the ICP line) reads as shouting to Google's reviewers on some placements.
5. **Landscape is small.** At 1200x628 the whole 2:3 ad is 419 px wide, so the hook and support line
   are small. Google requires a landscape image for PMax and Demand Gen, so it is included.

If Google disapproves any of these, ask for the policy-safe version: no arrow, button as plain text on
a band, sentence-case audience, no trademark.

## How to set up in Google Ads

1. Four campaigns (Performance Max or Demand Gen), conversion goal Purchase on the GrowthX pixel:
   `CD_G_A_StudentsAndNewLawyers` (01, 02, 03, 04, 19), `CD_G_B_LawyersNearContracts` (05, 06, 16, 17, 18),
   `CD_G_C_LawyersWorkingRemotely` (07, 08, 09, 10, 20), `CD_G_D_LLBHoldersInOtherJobs` (11, 12, 13, 14, 15).
2. One asset group per ad: its 3 images, the 5 headlines, long headline, 4 descriptions, business name
   "LawSikho", call to action "Sign up" and the Final URL from `GOOGLE_COPY_CD.csv`.
3. Audience signal: the "Audience signal" column, in the reader's own words. No age or gender targeting.
4. Final URLs point at the same GrowthX funnels as Meta (`cdtp-01` to `cdtp-20`) with
   `utm_source=google&utm_medium=cpc`. Create those funnels first, with `ctaLabels` set to
   "Join the Contract Drafting Community for ₹200" and "Join for ₹200 · 21 days, live online".
   Do not duplicate the funnels for Google: duplicated slugs failed payments at 30 to 40% (measured 23 Sep).
5. Test-buy every page in a real browser before launch. Google reviews the landing page too.
6. Routing, budgets and audiences are Ramanuj's call. No Google cost per buyer exists for this
   account yet; judge on GrowthX paid seats over 7 full days, never on CTR or a part day.

## Landing page notes for Google review

The pages name WhatsApp, LinkedIn, Y Combinator and Apollo in the body (how the camp runs and what
it teaches). Body-text mentions are normally allowed; they are not in any ad text.
