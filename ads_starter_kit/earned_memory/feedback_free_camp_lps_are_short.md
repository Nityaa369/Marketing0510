---
name: feedback-free-camp-lps-are-short
description: "Page length and section count do not predict LP conversion across 330 pages; short US Accounting pages did slightly better within campaign, but it is confounded - test it, do not assert it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4d1fca80-c9d7-436b-8c41-3000397bc5e2
  modified: 2026-09-17T11:33:59.379Z
---

17 Sep 2026. I built two ~1,000-word US Accounting pages and told Ruchika "free-camp pages win
when short", from about ten pages. She pushed back: the pages that do well across campaigns
have more sections and offer more value. Measured properly the same day:

Meta, 180 days, results / landing page views, every live page with 1,000+ views, words and
h2 counted on the page as it is deployed today (it may have been edited since it ran).

- **Free, 84 pages:** Spearman words~conversion -0.09, h2~conversion -0.13. Medians by words:
  <800 23.6%, 800-1,200 15.0%, 1,200-1,600 14.2%, 1,600-2,200 20.0%, 2,200+ 21.2%. No trend.
- **Paid, 246 pages:** words +0.02, h2 +0.12. 8-11 sections median 9.4% vs 5-8 at 6.3%, a
  slight lean towards more sections.
- **Within one campaign (same product, same week):** free -0.29 over 55 pages; paid +0.05
  over 215. US Accounting Aug: 530-548-word pages 31-32%, the 1,889-word 10-section page 24%
  and 20%. Sep: 758-863 words 24-28%, 1,889 words 22%. WomenAI Apr ran 2,600-word 14-section
  pages at 21-29%, so long pages also win.

**Why:** the claim was stronger than the evidence, and the user's instinct was not refuted.
Length does not decide conversion either way; the reader does (same template 16% vs 28%).

**How to apply:** never tell a reviewer a length "wins" without this table. When length is
disputed, offer a split test (same ad, duplicated ad set, short vs full page) instead of
arguing. Script: scratchpad lp_pull.py + the length pass; `lp_spine` L5 band stays a paid fit.
Related: [[feedback_landing_page_standard]], [[feedback-contradiction-means-failed-test]].
