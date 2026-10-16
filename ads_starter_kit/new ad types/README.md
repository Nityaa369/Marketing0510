# New ad types

Non-standard creative — meme formats, dialogue/comic panels, movie-still templates —
as an addition to the standard headline-first static ads shipped elsewhere in this repo.
Same compliance bar as everything else: [../CLAUDE.md](../CLAUDE.md) governs all of it,
this folder does not get a lighter rule set.

## The workflow

This folder is fed by two skills (`.claude/skills/`):

1. **`discover-ad-formats`** — run on demand, whenever you want a fresh batch of
   candidates (no automatic schedule is set up — this project folder isn't a git repo, so
   there's no durable way to run a cloud routine against it; ask for a run whenever you
   want one). Searches the web for trending meme templates / ad-creative formats worth
   adapting, and writes a dated candidate list to `candidates_<YYYY-MM-DD>.md` in this
   folder. Discovery only — it does not generate any ad or landing page.
2. **`build-new-ad-type-kit`** — run once you've picked candidate numbers from a
   `candidates_*.md` file (or handed over a reference image directly, like the seven
   `WhatsApp Image *.jpeg` files already sitting here). Builds a full kit: ad creative(s),
   matching landing page(s), `ad_copy.md`, a `README.md` with a launch spec, a
   `preflight.py` pass, and the four compliance lines CLAUDE.md requires before handoff.

## Folder layout once a kit is built

Each picked batch gets its own subfolder here, structured like every other kit in this
repo (see `../DataPrivacy_MediaBuyer_29-31Aug/` or `../ContentWriting_29-31Aug/` for the
pattern):

```
new ad types/
  candidates_2026-08-18.md        <- discovery output, dated, one per run
  <batch-slug>_<dates>/
    ad_copy.md
    README.md                     <- launch spec: account, dates, price, CPP baseline, circuit breaker
    ads/
    landing_pages/
```

## Reference images already here

The seven `WhatsApp Image 2026-08-18 *.jpeg` files are approved-style examples of the
target look (Bollywood-still dialogue format, illustrated-panel dialogue format) — use
them to calibrate tone when generating meme-format creative, they are not themselves a
kit.
