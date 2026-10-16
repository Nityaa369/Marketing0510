# Start here

This folder is everything needed to build **static Meta ads and their landing pages** for
LawSikho and SkillArbitrage, handed over so you can start without being told the same two
rejections twice.

It is a **working Claude Code project**, not a reading pack. Unzip it, open the folder in
Claude Code (terminal or the desktop Code tab), and Claude picks up `CLAUDE.md` on its own.
Then say what you want built. The rules, the checkers and the worked examples are all in
here and they run.

```
Unzip  ->  open the folder in Claude Code  ->  "build an ad kit for <camp>, ICPs <list>"
```

---

## 1. Fifteen minutes of setup

```bash
python --version          # 3.9 or newer
pip install Pillow        # the only Python dependency, used by the image gates
```

**Chrome or Chromium must be installed.** Ad faces are HTML rendered headless by Chrome, and
the gate that measures text overlap and clipping drives the same browser. If it is somewhere
unusual, set `ADKIT_CHROME` to the executable path.

Check it all works:

```bash
python check_all.py --brief          # prints every command, grouped by when you run it
python -m adkit.layouts --list       # the 11 ad layouts, with the real cost each one earned
python blind_reader.py --selftest    # should end "every check passed"
```

**Optional, for performance data.** Copy `ad-analysis-shared/.env.example` to
`ad-analysis-shared/.env` and paste the read-only Meta reporting token. Ask Ruchika for it.
It grants `ads_read` and `read_insights` only. Without it you can still build everything;
you just cannot re-pull the numbers in `PERFORMANCE_2026-10-05.md`.

---

## 2. What the work is

3-day live online bootcamps at **Rs 10**, price including GST, refundable anytime, **live
only with no recordings**. Each camp is the top of a funnel into a paid course. One ad speaks
to exactly one reader and points at exactly one landing page written for that reader.

**Two brands, never co-branded.** LawSikho sells legal careers (data protection, arbitration,
patents, US paralegal, independent director). SkillArbitrage sells non-legal careers (content
writing, corporate finance, US accounting, HR, academic writing, AI for senior professionals,
remote work for women, consulting).

The reader is an Indian working professional, student, or a woman returning from a career
break, scrolling on a phone and paying almost no attention.

---

## 3. Read these four, in this order

| | File | Why |
|---|---|---|
| 1 | [MY_WORK_SUMMARY.md](MY_WORK_SUMMARY.md) | The job in two pages. It was written as a briefing for another Claude, so it is the fastest way in for both of you. |
| 2 | [SOP/00_CONSTANTS.md](SOP/00_CONSTANTS.md) | Every rule that changes a decision, on one page. Read this instead of the long files. |
| 3 | [AD_CREATION_DIRECTOR.md](AD_CREATION_DIRECTOR.md) | The sole director for building an ad and page pair. Fourteen sections, each one aimed at a complaint that actually recurred. |
| 4 | [PERFORMANCE_2026-10-05.md](PERFORMANCE_2026-10-05.md) | What the account costs right now: 7-day and 30-day cost per buyer and per lead, by campaign and by ad, pulled 5 Oct 2026. Build against these numbers, not against doctrine alone. |

Then, before writing a single hook, read the ads that already ran for your reader:

```bash
python -m adkit.brief "chartered accountant who wants a board seat"
python -m adkit.corpus --like "<your ICP in your own words>" --quote 3
```

The doctrine in the long files is a compression of those ads. The ads are faster to read,
they carry the live cost, and they are the only way to answer "what does not work" with a
number instead of a rule.

---

## 4. The two rules that cause nearly every rejection

Both are stated in full in [CLAUDE.md](CLAUDE.md) with the worked examples. In short:

**Rule 1. Offer a better career. Never threaten.** Every ad offers the reader a different and
better job than the one they have. Their current work is an asset they trade up with, never a
liability they are exposed on. Three things get rejected every time: telling them a law now
applies to them, selling them more work at the same desk, and offering internal credit for
unpaid extra work.

**Rule 2. No assumed knowledge.** "Cryptic" means the ad only makes sense to someone who
already knows what the field is. The fix is almost always one missing sentence: a plain-words
definition of the field, on the face and again in the page's first fold.

> The test behind both, from Ruchika: *"If I look at it as someone with brain functionality at
> 20% due to lack of sleep, I will not get it. Optimise for a person in that state."*

---

## 5. Building your first kit

Approval runs **cheapest rejection first**. Do not build the kit and then ask.

1. **The ICP list.** Ranked, as a table, with nothing else. A rejection here costs a
   paragraph; the same rejection after the kit is built costs the kit. Section A once shipped
   24 pairs and 7 were rejected, which was about 105,000 tokens of landing page written for
   nothing.

   ```bash
   python preflight.py --scaffold-from docs/ICPs_<your list>.md <kit-folder>
   python preflight.py --shortlist <kit-folder>
   ```

2. **`value_props.md`.** One block per ad: `better_job`, `field_definition`, `deliverables`,
   `buying_pressure`, `awareness`, `pain_score`. Written before any pixel exists.

3. **`hooks.md` as a table.** Hooks settled as text cost 6.4 rebuild cycles per creative.
   Hooks settled after the layout cost 14.1.

   ```bash
   python hook_rules.py --kit <kit-folder>
   ```

4. **ONE ad and its landing page.** Get that pair approved before building the other nine.

5. **The rest of the kit.**

The kit itself is one file. `spec.py` holds each string once and emits `value_props.md`,
`hooks.md`, `ad_copy.md`, the faces and the pages, so the ad and its page cannot drift apart:

```bash
python -m adkit.spec --template > <kit-folder>/spec.py
```

In Claude Code you can simply ask for the kit and the `generate-ad-kit` skill in
`.claude/skills/` walks the whole path. `build-new-ad-type-kit` is the variant that starts
from a borrowed format or a reference image.

---

## 6. Before you hand anything over

```bash
python check_all.py <kit-folder>
```

This is the only command to report from, and never a subset of it. It runs preflight, both
halves of the simplicity gate, the hook rules, the two blind readers, the fit and gap
measurements, and the creative judge. It reports **PASS**, **FINDINGS** or **ERROR** per
gate, where ERROR means a gate crashed *or* ran and saw zero files. On 25 Aug 2026 a pair of
ads passed review three times because a gate had silently matched nothing and read as a pass.

The two blind readers need subagents, so they are two steps rather than one:

```bash
python blind_reader.py --prepare <kit>     # then one fresh subagent per packet, in ONE message
python blind_reader.py --score <kit>
python closing_reader.py --prepare <kit>   # same, for the page's closing fold
python closing_reader.py --score <kit>
```

A reader who shares your context will always pass your own work, which is why the isolation
is the whole trick: you wrote the ICP list, so your brain fills the gap and the fold reads
fine to you.

Then state the five handover lines in your reply. They are listed at the end of
[CLAUDE.md](CLAUDE.md) and in [SOP/06_HANDOVER_CHECKLIST.md](SOP/06_HANDOVER_CHECKLIST.md).

---

## 7. What else is in here

| Path | What it is |
|---|---|
| `SOP/` | The process that holds for every kit: structure, launch spec, how a cell is judged, compliance, the landing page standard, the ad copy standard, ICP selection, design styles. |
| `adkit/` | The shared ad chassis and page spine. Kits supply data, not CSS. Also the corpus index, the brief tool, the restyle tool and the measurement gates. |
| `earned_memory/` | 132 notes recording what was learned from specific builds and what Ruchika and Ramanuj said about them, in their own words. Start at `earned_memory/MEMORY.md`. |
| `RAMANUJ_FEEDBACK.md` | Every piece of feedback and every verdict from the reviewer, by theme, with a kit-by-kit ledger. |
| `CAMPAIGN_MAP.md` | Every campaign, its wave folders, and which pairs were approved or rejected. Read it before starting a new wave. |
| `GOLDEN/` | The exemplar faces with a note on why each one passed. Load them, do not just cite them. |
| `APPROVED/` | A complete worked kit that the reviewer approved, plus three control faces. See `BUNDLE_NOTES.md`. |
| `reference_pages/` | 60 landing pages from kits that earned their money, as donors. |
| `examples_that_fail/` | Four faces a gate blocks today, as negative examples and to keep the pixel gate's liveness check honest. |
| `docs/` | The ICP lists, the bootcamp scripts, the playbooks and the research behind them. |
| `judging-static-ads/` | The creative judge and the lint rules it runs. |
| `new ad types/` | The format candidate lists and their reference images. |

**[BUNDLE_NOTES.md](BUNDLE_NOTES.md) says what was deliberately left out of this copy, which
two gates that affects, and how to turn them green.** Read it before you trust a gate result.

---

## 8. The standing rules, in brief

No placement or job guarantee, ever. No income promise: market data must be labelled as
market data, and salary ladders are page-only and never on an ad face. Live only, no
recordings. Price labelled including GST, refundable anytime, wherever price appears. The two
brands are never co-branded. No em dashes or en dashes in copy. No "this is not for you if"
block. No AI-fear framing: the argument is a ladder, not a threat.

Every ad ships with its own landing page and its own colour palette. Never point two ads at
one page. The page must actually be able to take money: a real funnel URL on the pay button,
checked in a browser, because curl returns false 404s on these funnels.
