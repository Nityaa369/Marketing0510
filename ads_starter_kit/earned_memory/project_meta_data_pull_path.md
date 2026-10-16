---
name: project-meta-data-pull-path
description: How live Meta ad data reaches Claude for this account - a connected Meta Ads MCP server, not Supermetrics and not pull_ads.py
metadata:
  type: project
---

**Confirmed working 31 Aug 2026:** a **Meta Ads MCP server is connected and
authenticated directly** (server id prefix `5827be30-`). No token, no setup. It sees
21 ad accounts. `ads_get_ad_accounts` lists them with `is_queryable`;
`ads_get_ad_entities` pulls campaign/adset/ad rows with spend, impressions, clicks,
ctr, cpc, results and cost_per_result against a `date_preset` or `time_range`.
Every call needs a `client_conversation_id` (20 random alphanumerics, same value
reused for the whole conversation).

**A Meta System User token now exists and `pull_ads.py` is LIVE — 9 Sep 2026.**
Ramanuj generated a System User token in Business Suite and it is pasted into
`ad-analysis-shared/.env` as `META_ACCESS_TOKEN`. `python ad-analysis-shared/pull_ads.py
--list` works. System User tokens do not expire, so this should stay good.

**The REST token reads accounts the Ads MCP refuses.** This is the reason to use it.
`LawSikho Ad Account 4` (458577609606074) returns full insights over REST while every
Ads MCP call against it is refused server-side. It was carrying two live camps that
were invisible to every prior report: IP law (Main Bootcamp) and
US_Corporate_Law_BC_19-21Sep2026, about Rs 2.9L and Rs 2.6L over 14 days. The MCP
rollout gate is MCP-specific and the Graph API does not enforce it.

**`SkillArbitrage_21` is readable and genuinely empty.** Over REST it returns OK with
zero spend in 90 days. Its old "unreadable" status was the MCP gate, not an access
problem — do not keep citing it as a blind spot.

**So use both paths, and know which answers what:** the Ads MCP for quick interactive
questions (no setup, richer entity fields), `pull_ads.py` for full coverage and for the
repeatable JSON + HTML ad-by-ad reports that `campaign_map_sync.py` joins onto kit
folders. The token sees **19 ad accounts**; the MCP sees 21 but cannot read 2 of them.

Supermetrics MCP is authenticated but Team lawsikho's trial expired 2026-07-21;
discovery works, every `data_query` returns `TRIAL_EXPIRED`. Do not re-test.

**Account notes as of 31 Aug 2026:** `954464642377027` (Skill Arbitrage) is where the
live bootcamp spend is. `164485738329334` (Law Sikho) is DISABLED - flagged for
unusual activity, all ads paused, needs a Meta appeal. `3997767230350546` (LawSikho
Ad Account 3) has no spend since Nov 2025. LawSikho Ad Account 4, SkillArbitrage_21,
UK SkillArbitrage and BrihaspatiAi cannot be queried.

**Two corrections to apply to every pull:** Meta returns spend NET, so gross up by
18% GST before judging against SOP/02 thresholds; and never put purchase-optimised
and lead-optimised campaigns in one cost-per-result column.

**Why:** three sessions could otherwise be spent rediscovering that the two
documented paths are both blocked, when a live one exists that needs no setup.

**How to apply:** for any "what is working" question, go straight to the Meta Ads
MCP. `campaign_map_sync.py` (repo root) still joins a report back onto kit folders
and applies the SOP/02 thresholds. See also [[feedback-run-every-gate]].

**Two accounts are unreadable *over MCP*, tested 2 Sep 2026, still true 9 Sep.**
`SkillArbitrage_21` (1758160708403281) and `LawSikho Ad Account 4` (458577609606074)
refuse every Ads MCP call server-side: *"not enabled for the Ads MCP ... gradually being
rolled out."* They report `is_queryable: true`, which is misleading — the MCP gate is
enforced independently, so do not treat that field as permission. **Both are readable
over REST with the System User token**, which is now the fix: route those two through
`pull_ads.py` rather than reporting them as a blind spot.

**Supermetrics is connected but paywalled.** Facebook Ads is AUTHENTICATED (via Hirenn
Javeri) and both blocked accounts are visible to `accounts_discovery`, but `data_query`
returns `[TRIAL_EXPIRED]` — team "Team lawsikho", expired 2026-07-21, ID 1825387.
Discovery works, data does not.

**Always state which accounts a report covers.** The 1 Sep report initially implied full
coverage while missing two unreadable accounts and the whole Community (ASHWIN) account
(~Rs 75k/day on a different product line).

**Never state "no ads are running" as fact.** Corrected by the founder 4 Sep 2026, on a
report claiming two camps opening the next day had no ads. Three accounts are unreadable,
so the only defensible claim is *"I cannot find a live campaign in the sixteen accounts I
can read, and these three are closed to me."* Name the blind spot in the sentence itself,
not in a footnote further down - the founder reads the claim, not the caveat.

**Two method faults found the same day, both worth avoiding:**

- `ads_get_ad_entities` at campaign level **must be sorted** (`amount_spent_descending`).
  Unsorted it returns roughly by recency and paginates, so a spending campaign can sit past
  the cursor and read as absent. The first sweep that day missed a live campaign this way.
- **"MAIN" in a campaign name is not the calendar's MAIN.** In campaign names it means the
  main prospecting campaign as against retargeting; in BOOTCAMP_CALENDAR.md it means a first
  run as against a rerun (RE). Date the camp from the **ad set names**, which carry it
  explicitly (`ACW_Refresh_26-28Sep_set1`), never from the campaign name.
