---
name: project-google-ads-access-path
description: Google's own read-only google-ads-mcp is the preferred route (verified installing 31 Aug 2026); Adspirer is the write-capable, quota-metered fallback
metadata:
  type: project
---

**Updated 31 Aug 2026.** The earlier note here said no Google Ads MCP existed. That
was wrong about first-party servers: it is true there is none in the *MCP registry*,
but Google publishes one on GitHub at `googleads/google-ads-mcp`. Prefer it.

**Verified working on this machine 31 Aug 2026**, installed and probed over stdio:

```
uvx --from git+https://github.com/googleads/google-ads-mcp.git google-ads-mcp
```

Builds in ~15s (90 packages, `google-ads` is 22MB), reports as "Google Ads Server"
on FastMCP 4.0.0b5, and exposes exactly three **read-only** tools:
`customers_list_accessible_customers`, `metadata_get_resource_metadata`,
`search_search` (raw GAQL). No mutation tools at all - which is what
`ad-analysis-shared/README.md` actually asked for, unlike Adspirer.

`uvx` works even though the README says `pipx`; pipx is not installed here, uv is.

**What it still needs, and why it is not same-session:**

- A **developer token** from `ads.google.com/aw/apicenter`, which is only visible
  when signed in as a **manager (MCC)** account. Explorer access is often granted
  automatically and does reach production accounts at 2,880 ops/day; Basic (15,000)
  is a ~5 business day review. A token stuck at "Test account access" connects fine
  and returns nothing for real accounts, which reads as a bug but is not one.
- A Google Cloud project with `googleads.googleapis.com` enabled and an **OAuth
  desktop client**.
- Application Default Credentials. The README's route is `gcloud auth
  application-default login --scopes .../adwords,.../cloud-platform
  --client-id-file=...`, but **gcloud is not installed here and does not need to be**:
  `~/.google-ads-mcp/make_adc.py` writes the identical `authorized_user` ADC JSON via
  `InstalledAppFlow`, run with `uv run --with google-auth-oauthlib`.

Credentials live in `~/.google-ads-mcp/`, deliberately outside the ads-tasks tree.

**Adspirer** (`plugin:adspirer-ads-agent:adspirer`) remains installed and unauthorized.
It is now the fallback, not the route: it is write-capable across every platform it
touches (Meta included) and quota-metered per call (Free 15/month up to Max 3,000).
Only reach for it if the Google server cannot be used.

**Why:** the write access and the quota were the two objections to Adspirer, and the
first-party server answers both. The multi-day blocker is the developer token, not the
software, so start the token application before doing anything else.

**How to apply:** when asked to connect Google Ads, install the first-party server and
send them to the API Center first. See [[project-meta-data-pull-path]] for the Meta
equivalent and [[feedback-ads-report-columns]] for what to query once it is live.
