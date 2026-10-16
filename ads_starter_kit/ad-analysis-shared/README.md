# Ad analysis — shared access

Ask questions like *"what ads are working in remote work for women?"* and get
ad-by-ad answers with clickable FB/IG links, GST-inclusive costs, and the same
judgment rules Ramanuj uses.

## One-time setup

1. **Get the token.** Ask Ramanuj for the read-only Meta reporting token
   (it grants `ads_read` + `read_insights` only — you can see everything,
   change nothing).

2. **Connect this repo to your Claude.**
   - **claude.ai/code (web):** connect this GitHub repo, then add an environment
     secret named `META_ACCESS_TOKEN` with the token value.
   - **Claude Code on your laptop:** clone the repo, then copy `.env.example`
     to `.env` and paste the token in. `.env` is git-ignored — never commit it.

3. That's it. No Python packages to install (standard library only, Python 3.9+).

## Using it

Open a Claude session in this repo and just ask — Claude reads `CLAUDE.md`
and knows the house rules. Or run the puller directly:

```bash
python3 pull_ads.py --list
```

lists every active campaign by account with 14-day spend (use this to find
campaign names), and

```bash
python3 pull_ads.py women --days 14
```

pulls every campaign matching "women", ad by ad, and writes a JSON + HTML
report into `reports/` with FB ↗ / IG ↗ buttons per ad.

## What the numbers mean

- All ₹ figures **include 18% GST** (Meta returns net; the scripts gross it up).
- Campaigns are judged on **cost per result** — per buyer where the campaign
  sells, per lead/registration where it registers. The tables never mix the two.
- CTR is reported but never used as the verdict — click→buy % is what matters.

## Google Ads

Separate system, no token here. Ask Ramanuj for a read-only invite to the
Google Ads accounts (email invite, no password sharing) and use the Google Ads
UI. Never blend Google and Meta costs into one number.
