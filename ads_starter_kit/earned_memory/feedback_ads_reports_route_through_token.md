---
name: feedback-ads-reports-route-through-token
description: Every ads report goes through the System User token and pull_ads.py, never the Meta Ads MCP alone - the MCP is blind to a live-spending account
metadata:
  type: feedback
---

**Asked directly by Ruchika, 9 Sep 2026:** *"ensure that any time i ask for an ads
report it uses this new access token ... so that I get an overview into all campaigns
live."*

So: **an ads report runs `python ad-analysis-shared/pull_ads.py`, on the System User
token in `ad-analysis-shared/.env`.** The Meta Ads MCP is for quick interactive
lookups only, never for a report.

**Why: coverage, not preference.** The token reads **19** ad accounts. The MCP sees 21
but is refused server-side on two of them, and one of those, `LawSikho Ad Account 4`
(458577609606074), was carrying about Rs 4.5L over 14 days across IP law (Main Bootcamp)
and US_Corporate_Law_BC_19-21Sep2026. Every MCP-based report to date silently excluded
it. The token misses only the personal "Ruchika Lalla" account and unnamed
`452865377044057`. Both were checked at campaign level over `maximum` and hold
**zero campaigns, ever** - so the token's blind spots cost nothing. Ruchika confirmed
the same day that neither is relevant.

There was never an "old token" to avoid - the old path was the MCP, which uses no token.
`.env` had held the placeholder `paste-token-here` since it was written. System User
tokens do not expire, so this path should stay good without maintenance.

**Five accounts carry all live spend** as of 9 Sep 2026: Skill Arbitrage, Skill
Arbitrage_2, Community (ASHWIN), LawSikho Ad Account 4, SkillArbitrage_V. The other
fourteen are at zero over 14 days.

**How to apply:** run `--list` first; it now ends with a coverage line naming every
account read and every account with no spend, so carry that into the report rather
than implying full coverage. See [[project-meta-data-pull-path]],
[[feedback-ads-report-day-by-day]] and [[feedback-ads-report-columns]] for the shape
of the report itself.
