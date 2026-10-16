# Ad analysis — house rules

You are helping analyze Meta/Google ad performance for LawSikho / SkillArbitrage.
These rules are non-negotiable — they encode months of decisions. Follow them exactly.

## Money

- **Every ₹ figure shown to the user must include 18% GST.** Meta and Google APIs
  return net values — multiply by 1.18 and label "incl. GST". Never show net.
- Indian comma grouping: ₹1,00,000. Round CPL/CPP to the nearest rupee.
- **Never blend Meta and Google prices** in one number — always separate columns/sections.

## Every ad-level report

- **Every ad mentioned must carry its public links**: FB link built from
  `creative.effective_object_story_id` as `https://www.facebook.com/{page_id}/posts/{post_id}`
  (split the story id at `_`), IG link from `creative.instagram_permalink_url`.
  If missing, show `—` explicitly — never silently omit.
- More than ~10 ads → also generate a self-contained HTML view with FB ↗ / IG ↗
  buttons per row (pull_ads.py does this) and open it.

## How to judge performance

- **Judge on cost-per-result** (CPP for paid products, CPL for free/₹10 registrations),
  never on CTR. CTR is a liar; **click→buy %** is what discriminates good ads.
- **Never blend funnel types.** Free-registration, ₹10 tripwire, ₹100 community and
  full-price campaigns have incomparable costs — always separate tables first.
- Judge settled performance on the **last 3 full days**; before calling anything
  dead or broken, also check **today + yesterday fresh** — recent fixes show there first.
- **Frequency > 3.5** over 7 days = creative fatigue → flag "refresh needed".
- A campaign that is ACTIVE but spending ₹0 may be intentionally paused-by-budget —
  report status (LIVE vs PAUSED vs ₹0) explicitly, up front.
- Judge trends against the monthly baseline, not against yesterday.

## Which data path (decided 9 Sep 2026)

- **Every ads report runs through `pull_ads.py` and the System User token.** Not the
  Meta Ads MCP. The token reads 19 ad accounts including `LawSikho Ad Account 4`,
  which the MCP refuses server-side and which carries live bootcamp spend. An
  MCP-only report is missing that account without saying so.
- The Ads MCP is fine for a one-off interactive lookup. It is not the reporting path.
- **Always state which accounts the report covers.** `--list` prints a coverage line
  naming every account read and every account with no spend. Never write "nothing is
  running" without naming what you checked.
- **GST is INR-only.** Two accounts bill in USD and one in GBP. Never gross those up
  by 1.18 and never add them into a rupee total.

## Tools in this repo

- `python3 pull_ads.py --list` — see every active campaign (by account) with 14-day spend.
  Use this first when you don't know exact campaign names.
- `python3 pull_ads.py <keyword> [--days N]` — ad-by-ad report for every campaign
  whose name matches the keyword. E.g. `python3 pull_ads.py women --days 14` for the
  remote-work-for-women funnels. Writes JSON + HTML into `reports/`.
- The raw JSON in `reports/` is already GST-inclusive — do not multiply again.
- Cache discipline: before pulling, check `reports/` for a same-day file and reuse it.

## Token

- The token comes from the `META_ACCESS_TOKEN` env var or a local `.env` file
  (never committed — `.gitignore` covers it). It is **read-only** (`ads_read` +
  `read_insights`): you can analyze everything but cannot pause, edit or create ads.
  If an edit is needed, tell Ramanuj what to change and why.
- Google Ads has no API token here — use read-only access in the Google Ads UI
  and keep Google numbers in their own section.

## Style

- Answer in chat, plain English, conclusions first. HTML reports are a companion,
  not a substitute for the chat answer.
