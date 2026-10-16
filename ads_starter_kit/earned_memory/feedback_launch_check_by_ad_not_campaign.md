---
name: feedback-launch-check-by-ad-not-campaign
description: "To check whether a camp is launched, search ads by created_time and funnel slug, not campaign names; the Oct Tech Law ads went into the paused Aug campaign"
metadata:
  node_type: memory
  type: feedback
  originSessionId: ca6c6075-c746-4476-a92c-4c0a0b45026d
  modified: 2026-09-25T06:39:10.769Z
---

On 25 Sep 2026 I told Ruchika that no Tech Law ads for 24-26 Oct were live. I had searched
campaign names and spend, and GrowthX showed 0 leads on `tech-law-oct`. The team said the camp
was launched. What had actually happened:
- A new ad set `TechLaw_Oct_Wave1_24-26Oct` with 10 ads (links `growthx.lawsikho.com/f/meta-tech-law-oct-*`)
  was created at 00:17 on 25 Sep.
- It was created **inside the old paused campaign `Techlaw_BC_15AUG`** (LawSikho Ad Account 4).
- The ad set and ads are ACTIVE, but the campaign is PAUSED, so they had 0 impressions.
- The campaign still holds two old August ad sets (20 ads, still ACTIVE). Unpausing the campaign
  restarts those too.

**Why:** "launched" to the team means the ads were created. Delivery needs every level switched
on. A campaign reused under an old name also hides from the daily report's coverage check,
which matches campaign names to camp dates.

**How to apply:** for "is X live?", list ads with `filtering created_time > date` in every
account, and read the ad, ad set and campaign `effective_status` plus the creative's link slug.
Report the delivery state ("created, not delivering because the campaign is paused"), not just
whether it exists. `pull_ads.paged` prints API errors to stderr and returns partial lists, so
never filter out stderr when counting.

Related: [[feedback-daily-report-chat-style]], [[feedback-contradiction-means-failed-test]]
