# What is in this copy, what is not, and which gates that affects

Packed 5 Oct 2026 from the working repo, which is 901 MB and 170 top-level folders. This copy
is 23 MB in 423 files. Everything that decides how an ad gets built is here. What was left out is
**the history**: 538 past ad faces across 100+ kit folders, the 78 MB `APPROVED/` corpus, and
40 MB of reference images.

Read this before you trust a gate result, because two gates fit themselves against that
history and one of them cannot do it here.

---

## Gate by gate, measured in this folder on 5 Oct 2026

| Gate | State here | Why |
|---|---|---|
| `preflight.py --selftest` | **passes** | Carries its own fixtures. |
| `judging-static-ads` verdict tests | **passes** | 18 unit tests, self-contained. |
| `hook_rules.py` | **passes** | The approved and rejected headlines are listed in the file itself. |
| `blind_reader.py --selftest` | **passes** | Needs three control faces that demonstrably worked. They are shipped: `us22_notice_fifties` at Rs 30/lead, `us05_evening` at Rs 31, `us25_notice_small_town` at Rs 40. These are the same three the full repo picks. |
| `closing_reader.py --selftest` | **passes** | Reads 60 of 60 pages in `reference_pages/`, 30 with `div.close` and 30 without, which is what its fold finder has to prove. |
| `simplicity.py --selftest` | **passes, both halves** | It blocks none of the approved faces and none of the five ads that ran, and its liveness probe still fires: `18 PNGs across the repo: {'L3': 4}`. The four it fires on are shipped on purpose in `examples_that_fail/`, because a gate tuned until it catches nothing is not a gate, and with only clean faces on disk you cannot tell a clean corpus from a dead rule. |
| `adkit.selftest` | **2 failures that are also in the full repo, 2 that are not** | See below. This one needs care. |

### `adkit.selftest`, honestly

Running it here reports four failures and `fit gate discriminates: NO`.

**Two of them are not caused by this bundle.** `LP clean page` and `LP L6 quiet when a heading
names her` fail identically in the full working repo as of 5 Oct 2026. They are a live issue
in the landing page lint fixtures, not something missing from this copy. Ruchika knows.

**Two of them are caused by this bundle.** The `G` tests check that `GOLDEN` can be rebuilt
from every source it is meant to draw on, and those sources are the 28 approved kit folders
and 138 reference images that were left out. `GOLDEN/` itself is shipped complete, with its
notes, so the exemplars are all here to read. Only the rebuild is unavailable.

**What this means in practice:** `python check_all.py <kit>` will report **ERROR** on the
`adkit fit + LP lint fit` line. That is expected in this copy, and it is not a verdict on
your kit. Every other gate in `check_all.py` runs properly and does judge your kit. Do not
let a kit through on the strength of that one line being red for a known reason, and do not
treat it as a reason to ignore the others.

---

## To turn the last two green

Ask Ruchika for two folders out of the working repo and drop them in at the top level:

- `APPROVED/` (78 MB, 28 kits the reviewer approved). This restores the `simplicity.py` fit
  basis and most of the `G` tests.
- `reference_images/` (40 MB, 138 images). This restores the rest.

Nothing needs reconfiguring. Both are found by path.

---

## Deliberately not included

| Left out | Why |
|---|---|
| 100+ past kit folders, 538 ad faces | Size. The corpus index (`python -m adkit.corpus`) therefore sees 36 ads rather than 472, and `adkit.brief` has far less precedent to show you. The *numbers* those ads earned are preserved in `PERFORMANCE_2026-10-05.md`, `ad-analysis-shared/CPL_WINNERS_31Aug2026.md` and `CAMPAIGN_MAP.md`. |
| The Meta access token | It is a credential. `ad-analysis-shared/.env.example` is here; ask Ruchika for the token and paste it into `.env`, which must never be committed or shared. |
| Google Ads credentials | There are none to share. The API is not connected yet; `PERFORMANCE_2026-10-05.md` section 4 says exactly what is missing and what to apply for. |
| `ad-analysis-shared/.git` and `.env` | Credentials and history. The scripts and the CPL evidence are here without them. |
| The WhatsApp group chat export in `docs/` | A raw chat log of other people. Everything in it that became a rule is in `RAMANUJ_FEEDBACK.md`, attributed. |
| Dated GrowthX funnel extracts (`funnels_*.json`) | They are a window on one day, never a registry: a slug missing from one is a hint, never proof it does not exist. Re-pull rather than inherit. |
| `_internal/team_briefing.html`, `_archive/` | Internal and superseded. |

---

## Two things to know about the tooling before you lean on it

**A checker that sees zero files reads as a pass.** That is why `check_all.py` has three
states and not two, and why ERROR covers "ran and saw nothing" as well as "crashed". On
25 Aug 2026 a pair of ads passed review three times because the pixel rules had been run on
the wrong file type and the judge had never been run at all.

**The fits are one-class.** `simplicity.py` and both blind readers can show that a rule does
not block work that was approved or that ran cheap. They cannot show what they catch. They
are useful, not oracular, and the blind readers are relative: a face fails when it reads
worse than a control that actually worked, not against a fixed bar.

---

## If you change a rule

Re-run that rule's selftest and report the before and after fit. Never widen a word list or
loosen a threshold without it. Anything learned in a build that would change the next build
goes into the tooling the same day: a mechanically testable rule into a checker with its
evidence in the docstring, a judgement no regex can make into the `hook_rules.py` checklist
marked NOT mechanical, a change in the order of work into the skill, a standard for one
artefact into the matching `SOP/0N_*.md`.
