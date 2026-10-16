#!/usr/bin/env python3
"""One command that runs every gate in this repo against a kit, and refuses to
report success when a gate did not actually run.

Why this exists (25 Aug 2026). Two ads passed review three times and were still
wrong, because the checks were run partially and the partial run was reported as
"no blockers":

  * `simplicity.py` was run on `ads/*.png` only. Its copy rules (S1-S9, R1-R2)
    live on the HTML half, so a 196-word ad face - nearly double the 100-word cap
    - never got flagged.
  * `judging-static-ads/engine/creative_judge.py`, the repo's actual ship gate,
    was never run at all.
  * `ad_lint` C8 (call-out and headline size floors) matches CSS CLASS names.
    The kit generator emitted inline styles with no classes, so the strictest
    size gate in the repo silently matched nothing and reported a pass.
  * The judge crashed on Windows with a UnicodeEncodeError before printing its
    verdict, which looks exactly like a clean run if you are not reading closely.

So this runner reports three states per gate, never two: PASS, FINDINGS, or
ERROR. ERROR covers a crashed checker AND a checker that ran but saw zero files,
because both of those are the failure mode above. Exit code is non-zero for
either FINDINGS or ERROR.

    python check_all.py <kit-folder>
    python check_all.py <kit-folder> --selftest   # also run both engines' own tests
    python check_all.py --brief                   # what to read before building
"""
import os
import re
import subprocess
import sys
import pathlib

HERE = pathlib.Path(__file__).parent.resolve()
JUDGE = HERE / "judging-static-ads" / "engine" / "creative_judge.py"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

READING = """
================================================================================
BEFORE YOU BUILD - read two things, not 2,822 lines
================================================================================

  SOP/00_CONSTANTS.md   the constants card. Every rule that changes a decision on
                        one page: order of approval, the ICP archetype table and
                        what separates an approved wave from a rejected one, the
                        six hook types, the four copy moves and the length
                        ceilings, the first fold, the LP spine, the anti-voice
                        list, the handover lines.

  the ads that already ran for a reader like this:
      python -m adkit.corpus --like "<the ICP in your own words>" --quote 3
                        472 indexed ads joined to the Meta pull, with live cost,
                        the shipped copy, the face PNG, and the rejections nearest
                        that reader in the reviewer's own words. Read five before
                        writing a hook. The long files are a compression of these.

================================================================================
EVERY COMMAND, BY WHEN YOU RUN IT
================================================================================

  BEFORE YOU BUILD - what already exists
    python -m adkit.brief "<the ICP in your own words>"   START HERE. Past
                                                       performance for this reader,
                                                       the precedents, the
                                                       rejections, the order of
                                                       work. One command instead of
                                                       2,381 lines of MD.
    python -m adkit.brief --worked                     every ICP with a live cost
    python -m adkit.brief --styles                     every design style that ran
    python check_all.py --brief                        this
    python -m adkit.corpus --like "<ICP>" --quote 3    precedents + rejections
    python -m adkit.corpus --winners                   cheapest live ads, with copy
    python -m adkit.corpus --losers --family purchase  what actually costs money
    python -m adkit.corpus --ad us05_evening           one ad, everything known
    python -m adkit.icp --report                       rebuild SOP/ICP_INDEX.md
    python -m adkit.icp --situations                   life-situation ICPs
    python -m adkit.icp --rejected                     audiences already disproven
    python -m adkit.verdicts --rejected                every rejection and its reason
    python -m adkit.styles                            design styles that ran
    python -m adkit.styles --kit <kit>                is this wave all one shape?

  BUILDING
    python -m adkit.spec --template > <kit>/spec.py    the one file a kit is made of
    python -m adkit.restyle <kit> --list               the 11 layouts, each with the
                                                       real face it came from and
                                                       its cost. The map from "the
                                                       one that looks like this" to
                                                       a layout name.
    python -m adkit.restyle <kit> --ad <a> --to <lay>  re-skin one face. Proves the
                                                       selling copy did not move and
                                                       reverts if it would.
    python -m adkit.restyle <kit> --spread             BATCH visual refresh. Probes
                                                       every (ad, layout) pair with no
                                                       Chrome, then spreads the wave
                                                       over as many skeletons as its
                                                       copy allows. Add --apply.
    python <kit>/spec.py                               emits value_props, hooks,
                                                       ad_copy, faces and LPs
    python hook_rules.py --kit <kit>                   the hooks table, for approval
                                                       BEFORE anything is rendered
    python hook_rules.py "<a candidate hook>"          check one hook

  CHECKING - the only command you may report a result from
    python check_all.py <kit>
    python check_all.py <kit> --selftest               also re-run every checker's fit
    python blind_reader.py --prepare <kit>             the isolated read: blinded
                                                       packets, priced winners mixed
                                                       in as controls. Then one fresh
                                                       subagent per packet, answers
                                                       into .blind/answers.txt
    python blind_reader.py --score <kit>               unblind and score it
    python -m adkit.fit <kit>                          just the rendered-box gate
    python preflight.py <kit>                          compliance + LP diversity
    python simplicity.py <kit>                         the two-second-read gate
    python SOP/tools/copy_census.py APPROVED <kit>     copy vs the approved corpus

  AFTER A VERDICT - so the next kit starts from it. DO THIS EVERY ROUND.
    python -m adkit.verdict --pending                  which kits shipped faces and
                                                       recorded nothing. On 15 Sep
                                                       2026: 36 of 37
    python -m adkit.verdict <kit> --review             prefilled list, mark A or R
    python -m adkit.verdict <kit> --apply              record it, his words verbatim
    python -m adkit.verdict <kit> --approved a,b --rejected c --why "<what he said>"
    python -m adkit.golden                             rebuild GOLDEN from approvals

    538 built ads produced 7 recorded rows, which is why every checker here is a
    ONE-CLASS fit that can only show it does not block good work. The rejections
    arrive free with every round and were being thrown away.

  THE FITS - run after changing any rule, and report before/after
    python hook_rules.py       python simplicity.py --selftest
    python preflight.py --selftest    python -m adkit.selftest
    python SOP/tools/copy_census.py --selftest

================================================================================
WHAT A CLEAN RUN MEANS - all three checkers were refitted 31 Aug 2026
================================================================================

Fitted to the old in-house Section A labels they blocked most of the work Ramanuj
actually approved:

    hook_rules.py    72% of 123 approved headlines   ->   4.1%
    simplicity.py    84% of approved HTML faces      ->   0%
    preflight.py     72 hedge false alarms           ->   0

  * They are ONE-CLASS fits. They show a rule does not block good work. They
    cannot show what they catch - there is no set of faces Ramanuj rejected with
    sources in this repo. A clean run is weaker evidence than it looks.

  * Where a rule disagrees with a face Ramanuj approved, or with an ad that ran
    cheaply, THE FACE WINS. Fix the rule and report the before/after. That is how
    the 100-word cap became 195 and the hedge window became 120.

  * preflight.py is the exception: it checks wiring, not taste. A dead pay button
    on an approved page is still a real defect - 103 of them sit in APPROVED/
    right now, disclosed in CAMPAIGN_MAP.md.

  * An in-house APPROVED label is not evidence. Only Ramanuj's approval made an
    ad final.

Go to the long files when a gate fires and you need to know WHY a rule exists, or
when you are about to change one: AD_CREATION_DIRECTOR.md, CLAUDE.md (Rules 1-5),
SOP/07_AD_COPY.md, SOP/08_ICP_SELECTION.md, SOP/05_LANDING_PAGES.md,
SOP/09_EARNED_PLAYBOOK.md (population-specific), adkit/README.md.
GOLDEN/GOLDEN.md is generated - 199 faces Ramanuj approved, 47 of them his own,
with live cost. Load 2 or 3, never the set.

================================================================================
WHERE A NEW LEARNING GOES - write it down as part of finishing the job
================================================================================
  mechanically testable rule   a checker, WITH its evidence in the docstring,
                               then re-run its selftest and report before/after
  a judgement no regex makes   the checklist in hook_rules.py, marked NOT mechanical
  changes a DECISION           SOP/00_CONSTANTS.md, the card read every build
  explains why a rule exists   AD_CREATION_DIRECTOR.md, plus a memory note
  a change to the order of work    the Steps in the skill
  a standard for one artefact      the matching SOP/0N_*.md
  which ICP to pick            SOP/08_ICP_SELECTION.md
  how copy sentences are built SOP/07_AD_COPY.md, then copy_census.py --selftest
  population-specific          SOP/09_EARNED_PLAYBOOK.md
  a number from a Meta pull    ad-analysis-shared/CPL_WINNERS_*.md, dated, with the
                               account and window stated; then check corpus --winners
                               still joins (the money match is name-based)
  a verdict from Ramanuj       python -m adkit.verdict <kit> --approved ... --why ...
                               then adkit.golden, and a hand-written WHY IT PASSED
                               in GOLDEN/GOLDEN_NOTES.md if it is worth explaining
  a new source of approvals    SOURCES in adkit/golden.py, then rebuild
  chassis or LP spine          adkit/, then adkit.selftest, report before/after

================================================================================
ORDER OF WORK - the part that saves the most
================================================================================
  1. ICP list approved, RANKED    a rejection here costs a paragraph
     preflight.py --scaffold-from <icp-list.md> <kit>, then --shortlist <kit>.
     Ranked on pain_score so the weak cells are struck before they cost anything.
  2. value_props.md approved      a rejection here costs a paragraph
  3. hooks.md approved as a TABLE a rejection here costs a line of text
  4. ONE ad + its LP approved     a rejection here costs one pair
  5. then build the rest          a rejection here costs the wave
"""


PASS, FINDINGS, ERROR = "PASS", "FINDINGS", "ERROR"


def run(cmd, cwd=None):
    p = subprocess.run([sys.executable] + cmd, cwd=str(cwd or HERE), env=ENV,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or ""), (p.stderr or "")


def crashed(err, out):
    return "Traceback (most recent call last)" in err or "Traceback (most recent call last)" in out


class Gate(object):
    def __init__(self, name, state, seen, detail, body=""):
        self.name, self.state, self.seen, self.detail, self.body = name, state, seen, detail, body


def gate_preflight(kit):
    rc, out, err = run(["preflight.py", str(kit)])
    if crashed(err, out):
        return Gate("preflight.py", ERROR, 0, "checker crashed", err.strip()[-1200:])
    m = re.search(r"(\d+) pages checked", out)
    seen = int(m.group(1)) if m else 0
    if not m:
        return Gate("preflight.py", ERROR, 0, "no 'pages checked' line - did it see the kit?", out[-800:])
    n_block = sum(1 for l in out.splitlines() if l.strip().startswith("BLOCKER"))
    state = FINDINGS if n_block else PASS
    return Gate("preflight.py", state, seen, f"{n_block} blocker(s)",
                "\n".join(l for l in out.splitlines() if "BLOCKER" in l))


def kit_word_cap(kit):
    """A kit may declare its on-face word cap in a `.word-cap` file holding just the
    number. Default stays 100.

    Why this exists (26 Aug 2026). AD_CREATION_DIRECTOR.md 5.5 records TWO real budgets:
    100 words for the four-element template ContentWriting_SectionA was fitted against,
    and 130 for the seven-element template (call-out, qualifier row, italic definition
    sentence, three named deliverables, terms bar), which structurally runs 125-130 and
    was measured at 126 and 130 on a two-ad test. 5.5 says to run
    `simplicity.py --word-cap 130` for such a kit and to SAY SO in the kit.

    check_all could not express that: it always ran the 100 cap, so a seven-element kit
    reported a BLOCKER that the director says is not one. The two ways out of that are
    both bad - trim the definition sentence or a deliverable to hit 100 (5.5 explicitly
    warns this "erodes the exact specificity that makes the template work"), or read past
    a red gate by hand, which is how the 25 Aug three-times-passed failure happened.

    So the cap is declared per kit, in the kit, and printed in the gate line. It is not a
    global loosening: no `.word-cap` file means 100, exactly as before."""
    f = kit / ".word-cap"
    if not f.exists():
        return 100, False
    try:
        return int(f.read_text(encoding="utf-8").split("#")[0].strip()), True
    except ValueError:
        return 100, False


def gate_simplicity(kit, half):
    """half is 'html' or 'ads' - both must be run; running one and calling it done
    is the exact mistake this file exists to stop."""
    files = sorted((kit / half).glob("*.html" if half == "html" else "*.png"))
    if not files:
        return Gate(f"simplicity.py ({half})", ERROR, 0, f"no {half} files found in the kit")
    cap, declared = kit_word_cap(kit)
    argv = ["simplicity.py"] + (["--word-cap", str(cap)] if declared else [])
    rc, out, err = run(argv + [str(f) for f in files])
    if crashed(err, out):
        return Gate(f"simplicity.py ({half})", ERROR, len(files), "checker crashed", err.strip()[-1200:])
    n_block = sum(1 for l in out.splitlines() if l.strip().startswith("BLOCKER"))
    state = FINDINGS if n_block else PASS
    note = f"{n_block} blocker(s)" + (f", word cap {cap} (declared)" if declared else "")
    return Gate(f"simplicity.py ({half})", state, len(files), note,
                "\n".join(l for l in out.splitlines() if "BLOCKER" in l or "FIX " in l))


def gate_judge(kit):
    if not JUDGE.exists():
        return Gate("creative_judge.py", ERROR, 0, f"not found at {JUDGE}")
    htmls = sorted((kit / "html").glob("*.html"))
    if not htmls:
        return Gate("creative_judge.py", ERROR, 0, "no html/ sources to judge")
    rc, out, err = run([str(JUDGE)] + [str(f) for f in htmls])
    if crashed(err, out):
        return Gate("creative_judge.py", ERROR, len(htmls), "checker crashed", err.strip()[-1200:])
    m = re.search(r"(\d+) creative\(s\): (\d+) accept, (\d+) accept-with-changes, (\d+) reject", out)
    if not m:
        return Gate("creative_judge.py", ERROR, 0, "no verdict line - the judge did not finish", out[-800:])
    total, acc, awc, rej = (int(g) for g in m.groups())
    if total != len(htmls):
        return Gate("creative_judge.py", ERROR, total,
                    f"judged {total} of {len(htmls)} creatives - some were skipped")
    state = FINDINGS if rej else PASS
    return Gate("creative_judge.py", state, total, f"{acc} accept, {awc} with-changes, {rej} reject",
                "\n".join(l for l in out.splitlines() if "BLOCK " in l or "FAIL " in l))


def gate_classes(kit):
    """ad_lint C8 reads CSS class names. A kit whose generator emits inline styles
    only is invisible to it, which reads as a pass. Verify the classes exist."""
    htmls = sorted((kit / "html").glob("*.html"))
    if not htmls:
        return Gate("C8 reachability", ERROR, 0, "no html/ sources")
    blind = []
    for f in htmls:
        h = f.read_text(encoding="utf-8")
        if not any(re.search(r"\.%s\s*{[^}]*?font-size:\s*[\d.]+px" % c, h, re.S)
                   for c in ("callout", "head", "kicker", "elig", "kick")):
            blind.append(f.name)
    if blind:
        return Gate("C8 reachability", ERROR, len(htmls),
                    f"{len(blind)} face(s) carry no sized .callout/.head class - "
                    "ad_lint's size floor cannot see them",
                    "\n".join("    " + b for b in blind[:12]))
    return Gate("C8 reachability", PASS, len(htmls), "every face exposes a sized call-out class")


def gate_fit(kit):
    """adkit.fit -- the rendered box model. Measures what NO other gate here can:
    text overlap and clipping (invisible to all five, per SKILL.md 26 Aug 2026),
    and the COMPUTED call-out/headline size rather than the first matching CSS
    rule in the source.

    That last distinction is not academic. ad_lint C8 uses re.search for the
    first `.callout{...font-size:Npx}`, so a later override wins in the browser
    and is invisible to it. Measured 31 Aug 2026: 7 of 10 shipped
    IndependentDirector_Wave1 faces render .callout at 58px and .head at 52px,
    both under C8's 64px hard floor, and C8 reports all ten clean.
    """
    htmls = [f for f in sorted((kit / "html").glob("*.html"))
             if not f.name.startswith("__fit_")]
    if not htmls:
        return Gate("fit (rendered)", ERROR, 0, "no html/ sources to measure")
    try:
        sys.path.insert(0, str(HERE))
        from adkit import fit as _fit
        chrome = _fit.find_chrome()
    except Exception as e:                        # noqa: BLE001
        return Gate("fit (rendered)", ERROR, 0, "could not start: %s" % e)
    lines, n_bad = [], 0
    for f in htmls:
        try:
            found = _fit.check(f, chrome)
        except Exception as e:                    # noqa: BLE001
            n_bad += 1
            lines.append("    %s  ERROR %s" % (f.name, e))
            continue
        if found:
            n_bad += 1
            lines.append("    " + f.name)
            lines += ["      " + x for x in found]
    if n_bad:
        return Gate("fit (rendered)", FINDINGS, len(htmls),
                    "%d of %d face(s) clip, overlap or sit under the 64px floor"
                    % (n_bad, len(htmls)), chr(10).join(lines))
    return Gate("fit (rendered)", PASS, len(htmls),
                "no clipping, no overlap, identity type at or above 64px")


def gate_gaps(kit):
    """adkit.gaps -- vertical whitespace on the RENDERED PNG.

    Added 4 Sep 2026, after the third round of "a lot of empty gaps" / "make sure
    everything is aligned properly, no weird spaces". No gate here could see it:
    `adkit.fit` asks only whether anything CLIPS or OVERLAPS, and a void is the
    opposite of an overlap; `simplicity.py` checks the horizontal half (do the
    text blocks share a left edge); `ad_lint` never renders. So every gap report
    so far arrived from a human looking at a PNG, and each time only the one face
    that was shown got fixed.

    Ceiling is fitted, not chosen: no GOLDEN face pools more than 178px of
    background in one place and no priced face more than 151px, so 200px blocks
    0 of 19 and blocks the 207px face that was reported. `python -m adkit.gaps
    --fit` re-measures.
    """
    pngs = sorted((kit / "ads").glob("*.png"))
    if not pngs:
        return Gate("gaps (rendered)", ERROR, 0, "no ads/*.png to measure")
    try:
        sys.path.insert(0, str(HERE))
        from adkit import gaps as _gaps
    except Exception as e:                        # noqa: BLE001
        return Gate("gaps (rendered)", ERROR, 0, "could not start: %s" % e)
    lines, n_bad, worst = [], 0, 0
    for f in pngs:
        try:
            gap, at = _gaps.measure(f)
        except Exception as e:                    # noqa: BLE001
            n_bad += 1
            lines.append("    %s  ERROR %s" % (f.name, e))
            continue
        worst = max(worst, gap)
        if gap > _gaps.CEILING:
            n_bad += 1
            lines.append("    %s  %dpx of background at y=%d, ceiling %dpx"
                         % (f.name, gap, at, _gaps.CEILING))
    if n_bad:
        return Gate("gaps (rendered)", FINDINGS, len(pngs),
                    "%d of %d face(s) pool more than %dpx of background in one place"
                    % (n_bad, len(pngs), _gaps.CEILING), chr(10).join(lines))
    return Gate("gaps (rendered)", PASS, len(pngs),
                "worst gap %dpx, under the %dpx ceiling on every face"
                % (worst, _gaps.CEILING))


def gate_hooks(kit):
    """hook_rules.py, fitted against the Section A approved/rejected split. Reads the
    largest .head line off each face, which is the hook by construction."""
    sys.path.insert(0, str(HERE))
    try:
        import hook_rules
    except Exception as exc:
        return Gate("hook_rules.py", ERROR, 0, f"could not import: {exc}")
    htmls = sorted((kit / "html").glob("*.html"))
    if not htmls:
        return Gate("hook_rules.py", ERROR, 0, "no html/ sources")
    seen, bad = 0, []
    for f in htmls:
        h = f.read_text(encoding="utf-8")
        m = re.search(r'class="head"[^>]*>(.*?)</div>', h, re.S)
        if not m:
            continue
        seen += 1
        hook = re.sub(r"<[^>]+>", " ", m.group(1))
        hook = re.sub(r"\s+", " ", hook).strip()
        blockers, _ = hook_rules.check_hook(hook)
        for name, reason in blockers:
            bad.append(f"    {f.stem}: {name} - {reason}")
    if not seen:
        return Gate("hook_rules.py", ERROR, 0,
                    "no face exposes a .head hook - the gate could not read anything")
    state = FINDINGS if bad else PASS
    return Gate("hook_rules.py", state, seen, f"{len(bad)} vague hook(s)", "\n".join(bad))


def gate_hooks_table(kit):
    """hooks.md is the approval artefact: the hooks are read as a table BEFORE any image
    is rendered. Wave 1 averaged 14.1 rebuild cycles per creative with the hook settled
    after layout; wave 2 averaged 6.4 with it settled first."""
    f = kit / "hooks.md"
    if not f.is_file():
        return Gate("hooks.md table", ERROR, 0,
                    "no hooks.md - hooks were never approved as text before rendering. "
                    "Run: python hook_rules.py --kit <kit>")
    rc, out, err = run(["hook_rules.py", "--kit", str(kit)])
    if crashed(err, out):
        return Gate("hooks.md table", ERROR, 0, "hook_rules crashed", err.strip()[-800:])
    n = sum(1 for l in out.splitlines() if l.startswith("| ")) - 1  # minus the header row
    blocked = 0
    for line in out.splitlines():
        if line.startswith("| ") and "| BLOCK " in line:
            blocked += 1
    missing = "axis not stated" in out
    if blocked:
        return Gate("hooks.md table", FINDINGS, max(n, 0), f"{blocked} hook(s) blocked",
                    "\n".join(l for l in out.splitlines() if "| BLOCK " in l))
    if missing:
        return Gate("hooks.md table", FINDINGS, max(n, 0),
                    "a hook has no shared axis stated - item 7 is the human check")
    return Gate("hooks.md table", PASS, max(n, 0), "every hook approved as text first")


def gate_blind(kit):
    """blind_reader.py -- the isolated read, which until 15 Sep 2026 was the only
    check in this repo running on the honour system.

    AD_CREATION_DIRECTOR 12.5 says the session that wrote the brief cannot
    administer this test, and 30 files repeated that instruction while zero scripts
    enforced it. The gate is deliberately as strict as gate_hooks_table: a kit that
    never ran a blind read is an ERROR, not a pass, because "we did not check" and
    "it is fine" are the two states check_all exists to keep apart.

    It is also mtime-aware. Re-rendering a face after its read is the ordinary way
    of working, not a dodge, so a stale result reads as ERROR rather than as the
    green tick it was yesterday."""
    if not (HERE / "blind_reader.py").is_file():
        return Gate("blind read", ERROR, 0, "blind_reader.py not found")
    rc, out, err = run(["blind_reader.py", "--status", str(kit)])
    if crashed(err, out):
        return Gate("blind read", ERROR, 0, "checker crashed", err.strip()[-1200:])
    body = (out + err).strip()
    n = 0
    m = re.search(r"(\d+) candidate", body)
    if m:
        n = int(m.group(1))
    if rc == 0:
        m = re.search(r"control floor (\d)/3", body)
        return Gate("blind read", PASS, n,
                    "every face read at least as clearly as a priced winner"
                    + (", floor %s/3" % m.group(1) if m else ""))
    state = FINDINGS if rc == 1 else ERROR
    first = body.splitlines()[0].strip() if body else "no output"
    return Gate("blind read", state, n, first[:90], body[-900:])


def gate_closing(kit):
    """closing_reader.py -- the same isolated read, aimed at the LANDING PAGE.

    Added 21 Sep 2026. Every other clarity gate here points at the ad face:
    simplicity.py's dangling-reference rule and blind_reader.py both take the ad's
    first fold as their unit. So CorporateFinance_Notify_17-19Oct passed all ten
    gates clean while all 19 of its pages carried a riddling heading directly above
    the pay button, one of them with no verb in its first clause. Ramanuj read them
    and said "none of them make any sense".

    Same contract as gate_blind: never run is an ERROR, and a page rebuilt after
    its read reads STALE rather than keeping yesterday's tick. Staleness is
    measured on the FOLD, not the file, so an unrelated FAQ edit does not cry wolf.

    Skips silently for a kit with no landing pages."""
    if not (HERE / "closing_reader.py").is_file():
        return Gate("closing read", ERROR, 0, "closing_reader.py not found")
    if not (pathlib.Path(kit) / "landing_pages").is_dir():
        return None
    rc, out, err = run(["closing_reader.py", "--status", str(kit)])
    if crashed(err, out):
        return Gate("closing read", ERROR, 0, "checker crashed", err.strip()[-1200:])
    body = (out + err).strip()
    if body.startswith("SKIP"):
        return None
    m = re.search(r"(\d+) closing fold", body)
    n = int(m.group(1)) if m else 0
    if rc == 0:
        f = re.search(r"control floor of (\d)/3", body)
        return Gate("closing read", PASS, n,
                    "every closing fold read at least as clearly as one that worked"
                    + (", floor %s/3" % f.group(1) if f else ""))
    state = FINDINGS if rc == 1 else ERROR
    first = body.splitlines()[0].strip() if body else "no output"
    return Gate("closing read", state, n, first[:90], body[-900:])


def gate_selftests():
    out = []
    rc, o, e = run([str(HERE / "judging-static-ads" / "engine" / "test_verdict_gate.py")])
    ok = "OK" in (o + e)
    out.append(("verdict gate tests", ok, (o + e).strip().splitlines()[-1] if (o + e).strip() else ""))
    rc, o, e = run(["simplicity.py", "--selftest"])
    out.append(("simplicity fit", not crashed(e, o), o.strip().splitlines()[-1] if o.strip() else ""))
    rc, o, e = run(["hook_rules.py"])
    ok = "SHIPPED GATE" in o and not crashed(e, o)
    line = next((l.strip() for l in o.splitlines() if "SHIPPED GATE" in l), "")
    out.append(("hook rules fit", ok, line))
    rc, o, e = run(["preflight.py", "--selftest"])
    ok = "BLOCKERS on landing pages Ramanuj approved" in o and not crashed(e, o)
    line = next((l.strip() for l in o.splitlines() if "kit(s) flagged" in l), "")
    out.append(("preflight fit", ok, line))
    rc, o, e = run(["-m", "adkit.selftest"])
    ok = "discriminates: yes" in o and not crashed(e, o)
    line = next((l.strip() for l in o.splitlines() if "discriminates" in l), "")
    n_fail = sum(1 for l in o.splitlines() if l.strip().startswith("FAIL"))
    out.append(("adkit fit + LP lint fit", ok and not n_fail, line))
    gates = []
    for name, ok, line in out:
        gates.append(Gate(name, PASS if ok else ERROR, 1, line))
    return gates


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    if "--brief" in argv:
        print(READING)
        return 0
    kit = pathlib.Path(argv[1]).resolve()
    if not kit.is_dir():
        print(f"not a kit folder: {kit}")
        return 2

    gates = [gate_hooks_table(kit), gate_classes(kit), gate_fit(kit), gate_gaps(kit),
             gate_hooks(kit), gate_preflight(kit),
             gate_simplicity(kit, "html"), gate_simplicity(kit, "ads"),
             gate_judge(kit), gate_blind(kit), gate_closing(kit)]
    gates = [g for g in gates if g is not None]   # gate_closing skips a kit with no LPs
    if "--selftest" in argv:
        gates += gate_selftests()

    width = max(len(g.name) for g in gates)
    print(f"\nkit: {kit.name}\n")
    print(f"  {'gate'.ljust(width)}  {'state':9} {'files':>5}  detail")
    print("  " + "-" * (width + 42))
    for g in gates:
        print(f"  {g.name.ljust(width)}  {g.state:9} {g.seen:>5}  {g.detail}")
    for g in gates:
        if g.body and g.state != PASS:
            print(f"\n  --- {g.name} ---")
            for line in g.body.splitlines():
                print("  " + line.rstrip())

    n_err = sum(1 for g in gates if g.state == ERROR)
    n_find = sum(1 for g in gates if g.state == FINDINGS)
    print()
    if n_err:
        print(f"  {n_err} gate(s) did not actually run. That is not a pass - fix the gate, then re-run.")
    if n_find:
        print(f"  {n_find} gate(s) reported findings.")
    if not n_err and not n_find:
        print("  every gate ran and every gate is clean.")
    return 1 if (n_err or n_find) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
