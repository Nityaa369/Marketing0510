# Ad approval system — static creative judge

A skill plus a deterministic checker that decides whether a static ad is ready to run:
**ACCEPT**, **ACCEPT WITH CHANGES**, or **REJECT — rethink**.

It exists because the rules were spread across four scripts nobody ran as a set, so a creative
could pass the copy linter and still ship with clipped text, a banned claim, or a wall of
primary text that ran at 2.15× median cost.

## What's in here

```
SKILL.md                    the protocol Claude follows when an ad arrives
reference/house-rules.md    the standing rules a linter can't see (the judgement layer)
reference/gate-rules.md     the backtested rulebook: fire rates, tiers, calibration notes
engine/creative_judge.py    one entry point — runs everything, logs every verdict
engine/ad_lint.py           C1–C27  copy and call-out rules, reads the ad HTML
engine/ad_render_qa.py      E1–E4   clipping, crop line, dead band, reads the PNG
engine/crop_qa.py           X1      ink inside the bands a square crop discards
engine/check_claims.py      T1      trust-claim accuracy, brand by product line
engine/verdict_log.py       reads/writes the verdict log; enforces verdict freshness
engine/package_check.py     the ship gate — run before zipping a kit for a media buyer
engine/make_manifest.py     writes the manifest.json the kit importer expects
engine/test_verdict_gate.py 18 regression tests for the decision procedure
```

## Setup

Python 3.9+ and Pillow. Pillow is required — without it the two pixel checkers cannot run and
you lose the crop gate, which is where the expensive mistakes are.

```bash
python3 -m pip install --user Pillow
```

If your system Python refuses (`externally-managed-environment` on recent macOS), use a venv:

```bash
python3 -m venv ~/.venvs/adjudge && ~/.venvs/adjudge/bin/pip install Pillow
```

and call `~/.venvs/adjudge/bin/python` instead of `python3` below.

Verify:

```bash
python3 engine/test_verdict_gate.py
```

18 tests should pass.

## Using it

Judge one creative, or a whole kit directory:

```bash
python3 engine/creative_judge.py path/to/ad.html
```

```bash
python3 engine/creative_judge.py path/to/kit_dir
```

Useful flags: `--json` (machine-readable), `--quiet` (verdict lines only), `--no-log` (don't
append to `engine/creative_verdicts.jsonl`), `--vision` (render 236px thumbnails and a contact
sheet for the vision pass).

### The one gotcha that costs you the pixel gate

`creative_judge.py` looks for the rendered PNG **in the same directory as the HTML**. Most kits
keep `html/` and `ads/` as siblings, so the pixel checks silently skip and you get `[WARN E0]`.
Copy the pair into one folder first:

```bash
mkdir -p /tmp/judge && cp kit/html/01_foo.html kit/ads/01_foo.png /tmp/judge/ && python3 engine/creative_judge.py /tmp/judge/01_foo.html
```

If a checker can't run at all you get `[WARN E9] … the check was NOT performed`. That is not a
pass — fix the cause and run again.

### Rendering a PNG from ad HTML

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1350 --virtual-time-budget=5000 --screenshot=out.png "file:///absolute/path/to/ad.html"
```

## Installing the skill in Claude Code

Copy the whole folder into your skills directory:

```bash
cp -R judging-static-ads ~/.claude/skills/
```

Claude picks it up from `SKILL.md` and will run the protocol whenever you paste an ad image or
point at ad HTML. It works fine without Claude Code too — the engine is plain Python and the
two reference files are readable on their own.

## How the verdict is decided

```
any BLOCK                 -> REJECT
2 or more FIX             -> REJECT
exactly 1 FIX             -> ACCEPT WITH CHANGES
0 FIX, any number of WARN -> ACCEPT   (each WARN is a decision that must be stated)
```

A clean Gate 0 pass means **"no known defect", not "good ad"**. Gate 0 separates the bad tail;
it does not pick winners. The vision pass in `SKILL.md` and the teardown questions in
`gate-rules.md` are what decide whether an ad is actually good.

Judging from an image with no source is a degraded verdict and must say so — Gate 0 never ran.
A 44px kicker shipped once exactly this way.

## The ship gate

Judging one ad is half the system. `package_check.py` is the other half: run it on a kit
folder before you zip it for a media buyer and it refuses to ship a kit whose creatives were
REJECTed, whose anchor text is missing, whose landing pages don't exist, or whose verdicts are
**stale** — a verdict older than the PNG it names authorises nothing, because someone edited
the creative after it was judged.

```bash
python3 engine/package_check.py path/to/kit_dir
```

To ship a creative with a known defect anyway, the override is deliberately awkward and always
logged, because the point is to make it attributable rather than impossible:

```bash
python3 engine/package_check.py path/to/kit_dir --accept-defects C21 --reason "owner approved, dated creative is intentional"
```

## Adding a rule

New mechanical rules must pass the backtest discipline in `gate-rules.md`: **never reject what
was approved and shipped, never reject ads that beat their campaign median.** Check the fire
rate on approved vs unshipped kits before letting a rule block anything. A change that only
lowers a rule's fire rate is safe by construction.
