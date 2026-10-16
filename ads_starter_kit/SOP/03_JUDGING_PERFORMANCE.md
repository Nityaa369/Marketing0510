# 03 · Judging a cell

- **Judge on cost per result, never on CTR.** CTR is a liar. Click-to-buy is what
  discriminates a good ad from a busy one.
- **Never blend funnel types.** A ₹10 tripwire's cost per result is not comparable with a
  free registration, a ₹100 community or a full-price campaign. Separate tables first.
  Historical free-registration CPL of ₹96 including GST is not comparable to a ₹10 purchase.
- **Judge settled performance on the last 3 full days**, and check **today and yesterday**
  before calling anything dead. A recent fix shows up there first.
- **Frequency above 3.5 over 7 days is creative fatigue, not a bad ad.** Refresh rather
  than kill. That is what the alternate primary text variants in `ad_copy.md` are for.
- **All rupee figures reported back include 18% GST.** Meta returns net, so multiply by 1.18.
- **A cell that is ACTIVE but spending ₹0 may be paused by budget.** Report LIVE vs PAUSED
  vs ₹0 explicitly. Never let ₹0 read as a result.
- Two ads on overlapping ICPs are fine to run in one CBO for creative testing, but **do not
  read them as independent audiences**.
- When a cell aimed at a different audience from the rest of the pack delivers differently,
  **check the audience before blaming the creative**.

## Pulling the numbers

**Route every ads report through the System User token, not the Ads MCP.** Settled
9 Sep 2026, when the token was first generated and pasted into
`ad-analysis-shared/.env`. The reason is coverage, not preference:

| | accounts it can read | blind to |
|---|---|---|
| System User token (REST) | **19** | the personal "Ruchika Lalla" account and unnamed `452865377044057` — both hold **zero campaigns over all time**, verified 9 Sep 2026 |
| Meta Ads MCP | 19 of 21 | **`LawSikho Ad Account 4`** and `SkillArbitrage_21`, refused server-side |

`LawSikho Ad Account 4` is the one that matters: it was carrying IP law (Main Bootcamp)
and US_Corporate_Law_BC_19-21Sep2026 at about Rs 4.5L over 14 days while being invisible
to every MCP-based report. The MCP rollout gate does not apply to the Graph API.

The Ads MCP is still fine for a quick interactive lookup, and it reaches the two
zero-spend accounts the token cannot. But **a report goes through `pull_ads.py`.**

Two commands. Neither needs a Supermetrics subscription; both read the Meta Marketing
API directly with a read-only token (`ads_read` + `read_insights`) held in
`ad-analysis-shared/.env` as `META_ACCESS_TOKEN`. The token is git-ignored and grants
no write access - you can analyse everything and change nothing. System User tokens do
not expire, so this should stay good without maintenance.

```bash
python ad-analysis-shared/pull_ads.py --list                 # active campaigns + 14d spend
python ad-analysis-shared/pull_ads.py <keyword> --days 14    # ad-by-ad, JSON + HTML report
python campaign_map_sync.py --write                          # join it back onto the kits
```

`pull_ads.py` grosses every rupee up by 18% and groups by campaign, so the tables
never blend funnel types. Its JSON in `ad-analysis-shared/reports/` is already
GST-inclusive - never multiply again.

**`--list` ends with a coverage line naming every account it read and every account
with no spend. Carry that into the report.** Added 9 Sep 2026 with two fixes that
had been silently narrowing the numbers: the account list dropped anything not
`account_status == 1`, so UNSETTLED and DISABLED accounts vanished with no mention;
and every figure was multiplied by 1.18 and printed behind a rupee sign, including
the two USD accounts and the GBP one. Both were harmless only because those accounts
happened to be at zero. GST is now applied to INR alone, each account prints its own
currency, and a keyword pull spanning two currencies warns instead of adding them up.

`campaign_map_sync.py` matches each live ad name back to the `.png` in a kit's `ads/`
folder and applies the SOP/02 thresholds per cell (scale at Rs 250, target Rs 300,
circuit breaker Rs 450, frequency 3.5). `--write` updates the block between the
`AUTO PERFORMANCE` markers in `CAMPAIGN_MAP.md` and nothing else.

**The match is a guess.** Nothing forces a media buyer to name a Meta ad after the
file it came from, so every run prints a match rate and lists what it could not
place. A low rate means the naming convention is not being followed - not that those
ads did not run. Name ads in Meta after the `.png` stem and this stays near 100%.
Duplicated creative across kit folders is flagged `(ambiguous)`, which is real
information: two kits shipped the same face.
