# SOP — the rules that hold for every kit

These files hold what used to be copy-pasted into all 25-odd kit READMEs: the launch
spec, how a cell is judged, the compliance list, the landing page standard and the
handover checklist. They are the **default**. A kit README now only has to record what
is different about that drop.

## Order of precedence

1. **The kit's own README.** If it sets a stricter or different rule, it wins. Always.
2. **`../CLAUDE.md`.** The two judgment calls (Rule 1 offer a better career, Rule 2 no
   assumed knowledge) and the standing compliance rules.
3. **These SOPs.** The default when the kit README is silent.

Nothing here replaces `CLAUDE.md`. That file is about whether the copy is any good.
These files are about how a kit is assembled, launched and judged — with one exception:
`07_AD_COPY.md` **is** about the copy, at the sentence level, and it is measured rather than
argued. Re-measure it with `python SOP/tools/copy_census.py` after each approval batch.

## The files

| File | What it settles |
|---|---|
| [01_KIT_STRUCTURE.md](01_KIT_STRUCTURE.md) | Folder layout, naming, what ships, the README template |
| [02_LAUNCH_SPEC.md](02_LAUNCH_SPEC.md) | Accounts, objective, ad set rules, CPP targets, circuit breakers |
| [03_JUDGING_PERFORMANCE.md](03_JUDGING_PERFORMANCE.md) | How to read a cell without fooling yourself |
| [04_COMPLIANCE.md](04_COMPLIANCE.md) | The non-negotiable list, in one place |
| [05_LANDING_PAGES.md](05_LANDING_PAGES.md) | First fold, section spine, the pay button |
| [06_HANDOVER_CHECKLIST.md](06_HANDOVER_CHECKLIST.md) | What must be true before anything is sent |
| [07_AD_COPY.md](07_AD_COPY.md) | The sentence-level copy formula, fitted to the 150-block `APPROVED/` corpus |
| [08_ICP_SELECTION.md](08_ICP_SELECTION.md) | Which ICPs earn an ad, fitted to 128 ads of live spend |
| [10_DAILY_AD_REPORT.md](10_DAILY_AD_REPORT.md) | The daily Community/Bootcamps report: failure taxonomy by funnel layer, thresholds, what to pull |

## Where things live now

- **Campaign history** — [../CAMPAIGN_MAP.md](../CAMPAIGN_MAP.md) lists every campaign,
  every wave folder it has, and what was approved or rejected in each.
- **Reference images** — `../reference_images/` (the WhatsApp sends the research tooling cites).
- **Research and doctrine** — `../ad_research/`, `../docs/`.
- **Superseded builds** — `../_archive/`.


## 00_CONSTANTS.md

Added 31 Aug 2026. The card that gets read every build:
every rule that changes a decision, on one page. The other files here are the
record and the reasoning; this one is the briefing. When they disagree, they
should not - fix the card.
