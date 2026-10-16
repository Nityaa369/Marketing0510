#!/usr/bin/env python3
"""Re-render a face in a different visual style, and PROVE the copy did not move.

WHY THIS EXISTS (15 Sep 2026). Asked for directly:

    "past ads that worked - i share a sample of an ad visual that i like, and the
     ads are regenerated using that sample as reference without changing text.
     i have tried it in claude and it does not happen."

It did not happen for three reasons, and all three are fixed here:

  1. NO OPERATION. Restyling meant hand-editing `layout=` inside a kit's spec.py.
     A model sent in there to change one keyword will also tidy a headline on the
     way past, so the copy moves - the one thing the request said not to do. The
     override now lives OUTSIDE spec.py, in <kit>/.restyle.json, and spec.py is
     never edited.

  2. NO PROOF. Nothing checked that the words survived. This diffs every text node
     on the rendered face before and after, using the same extractor the blind
     reader uses, and REVERTS if a single character moved.

  3. NO MAP FROM A PICTURE TO A STYLE. adkit/layouts.py has carried a provenance
     line per layout all along - the real face each one came from, with its live
     cost - but nothing surfaced it. `--list` prints that table, so "the one that
     looks like this" becomes a layout name.

    python -m adkit.restyle <kit> --list
    python -m adkit.restyle <kit> --ad 03_school_teachers --to serif
    python -m adkit.restyle <kit> --revert            drop every override

WHAT THIS IS NOT. Changing the skeleton is not a finding from cost. Only two
styles in this account carry a measured number - pay chart at 2.34x par and
toon/chat at 1.22x, both worse - and neither says anything about which of the
eleven layouts is better. Restyle because the reviewer asked for variety (Rule 4b,
"make sure each have distinct colour palette"), not because a layout is known to
convert. It also cannot invent a new look: it can only reach the layouts
adkit/layouts.py already implements.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OVERRIDE = ".restyle.json"

# Ad copy carries the rupee sign, and the Windows console default is cp1252, which
# cannot encode it. check_all.py already forces PYTHONIOENCODING=utf-8 on the
# children it spawns; this module is also run directly, so it does it for itself.
# Without this the tool crashes exactly when it has something to report.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):                            # pragma: no cover
    pass


# The classes that carry SELLING COPY, as opposed to chrome. Measured 15 Sep 2026
# by rendering one ad through `notice` and `serif` and diffing by class:
#
#   identical: callout, head, def           renamed but identical: deliver -> quote
#   chrome, and different by design: nrail -> brand + eyebrow, the terms bar
#   (sm / sm r) -> fline + trust, nlabel dropped, barrier added
#
# So "without changing text" cannot mean every string on the face - the layouts
# consume different chrome field sets, and demanding byte-equality across all of
# them makes every restyle illegal, which is the first thing this tool did. It
# means the words that sell: the ICP line, the hook, the definition, the delivery
# sentence. Those must survive verbatim. Chrome is reported and not blocked.
#
# `nlabel` is deliberately NOT here. It is the section label on the notice
# device ("Call for reviewers") - content the writer chose, but content that
# exists only because that device has a slot for it. Leaving the device drops it,
# correctly. It shows up in the chrome diff so the loss is never silent.
COPY_CLASSES = ("callout", "head", "def", "deliver", "quote", "kicker", "elig",
                "barrier")


def _nodes(face):
    sys.path.insert(0, str(ROOT))
    import blind_reader
    return blind_reader.extract(face)


def _copy(face):
    """The selling-copy strings on a face, as a set."""
    return {t for t, _, cls in _nodes(face)
            if any(c in COPY_CLASSES for c in cls.split())}


def _all(face):
    return {t for t, _, _ in _nodes(face)}


def _faces(kit):
    return {p.stem: p for p in sorted((kit / "html").glob("*.html"))
            if not p.name.startswith("__fit_")}


def _render(kit):
    spec = kit / "spec.py"
    if not spec.is_file():
        return False, "no spec.py in %s - this kit was not built from a spec." % kit.name
    p = subprocess.run([sys.executable, str(spec)], cwd=str(kit.parent),
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if p.returncode != 0:
        return False, (p.stderr or p.stdout or "")[-800:]
    return True, ""


def show_list(kit):
    from . import layouts as _layouts
    # layout -> (source face, live cost, one line). Take the first three and
    # tolerate a shorter or longer tuple rather than unpacking blind.
    prov = getattr(_layouts, "PROVENANCE", {}) or {}

    print("\n  THE LAYOUTS, and the real face each one came from.")
    print("  This is the map from \"the one that looks like this\" to a layout "
          "name.\n")
    print("  %-12s %-40s %-16s %s"
          % ("layout", "reference face", "its live cost", "what it is"))
    print("  " + "-" * 110)
    for name in sorted(getattr(_layouts, "LAYOUTS", {})):
        row = list(prov.get(name, ()))
        ref = row[0] if len(row) > 0 else "-"
        cost = row[1] if len(row) > 1 else "-"
        what = row[2] if len(row) > 2 else ""
        print("  %-12s %-40s %-16s %s" % (name, ref[:40], cost[:16], what[:44]))

    used = {}
    ov = {}
    f = kit / OVERRIDE
    if f.is_file():
        ov = json.loads(f.read_text(encoding="utf-8"))
    spec = kit / "spec.py"
    if spec.is_file():
        import re
        src = spec.read_text(encoding="utf-8", errors="replace")
        names = re.findall(r'name\s*=\s*"([^"]+)"', src)
        lays = re.findall(r'layout\s*=\s*"([^"]+)"', src)
        for n, l in zip(names, lays):
            used[n] = ov.get(n, l)
    if used:
        print("\n  THIS KIT\n")
        for n, l in used.items():
            mark = "  <- overridden" if n in ov else ""
            print("    %-34s %s%s" % (n, l, mark))
        counts = {}
        for l in used.values():
            counts[l] = counts.get(l, 0) + 1
        top = max(counts.values()) if counts else 0
        if len(used) >= 4 and top > len(used) / 2.0:
            print("\n    %d of %d share one layout - Meta reads visually similar faces"
                  "\n    as one ad. Restyle one: --ad <name> --to <layout>"
                  % (top, len(used)))
    print("""
  To restyle without touching a word of the copy:
    python -m adkit.restyle %s --ad <name> --to <layout>
""" % kit.name)
    return 0


def restyle(kit, ad, to):
    from . import layouts as _layouts
    known = set(getattr(_layouts, "LAYOUTS", {}))
    if to not in known:
        print("unknown layout '%s'. Known: %s" % (to, ", ".join(sorted(known))))
        return 2

    faces = _faces(kit)
    if ad not in faces:
        print("no face named '%s' in %s/html. Found: %s"
              % (ad, kit.name, ", ".join(sorted(faces)[:8])))
        return 2

    before_copy, before_all = _copy(faces[ad]), _all(faces[ad])
    f = kit / OVERRIDE
    prev = json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
    new = dict(prev, **{ad: to})
    f.write_text(json.dumps(new, indent=2), encoding="utf-8")

    ok, err = _render(kit)
    if not ok:
        f.write_text(json.dumps(prev, indent=2), encoding="utf-8") if prev \
            else f.unlink(missing_ok=True)
        print("render failed, override reverted:\n%s" % err)
        return 2

    face = _faces(kit)[ad]
    after_copy, after_all = _copy(face), _all(face)

    lost = sorted(s for s in before_copy if s not in after_all)
    if lost:
        f.write_text(json.dumps(prev, indent=2), encoding="utf-8") if prev \
            else f.unlink(missing_ok=True)
        _render(kit)
        print("\n  REVERTED. '%s' cannot carry this ad's copy - %d line(s) would have"
              "\n  been dropped:\n" % (to, len(lost)))
        for s in lost:
            print("    lost: %s" % s[:72])
        print("\n  Pick another layout, or move that line into a field '%s' renders."
              "\n  Nothing was changed.\n" % to)
        return 1

    print("\n  %s is now '%s'." % (ad, to))
    print("  Every selling line survived verbatim: %d copy field(s) checked "
          "(ICP line,\n  hook, definition, delivery sentence).\n" % len(before_copy))

    gained = sorted(s for s in after_all if s not in before_all)
    dropped = sorted(s for s in before_all if s not in after_all)
    if gained or dropped:
        print("  Chrome differs, as layouts do. This is not copy and was not blocked:")
        for s in dropped:
            print("    - %s" % s[:72])
        for s in gained:
            print("    + %s" % s[:72])
        print("")
    print("  spec.py was not edited; the override is in %s.\n" % (kit / OVERRIDE))
    print("  Re-run the gates - a new skeleton changes the box model, not the words:")
    print("    python check_all.py %s" % kit.name)
    print("    python blind_reader.py --prepare %s\n" % kit.name)
    return 0


def _probe(kit):
    """{ad: {layout: [copy strings]}} with no Chrome and no files touched."""
    import os
    spec = kit / "spec.py"
    if not spec.is_file():
        return None, "no spec.py in %s - only spec-built kits can be spread." % kit.name
    env = dict(os.environ, ADKIT_PROBE_LAYOUTS="1", PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, str(spec)], cwd=str(kit.parent), env=env,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    for line in (p.stdout or "").splitlines():
        if line.startswith("ADKIT_PROBE_JSON "):
            raw = json.loads(line[len("ADKIT_PROBE_JSON "):])
            return {ad: {lay: v.get("text", []) for lay, v in per.items()}
                    for ad, per in raw.items()}, ""
    return None, (p.stderr or p.stdout or "probe produced no output")[-600:]


def spread(kit, apply=False):
    """Give a wave as many distinct skeletons as its copy allows.

    WHY. Meta treats visually similar faces as one ad, so ten faces in one
    skeleton is one ad with the widget swapped - the reviewer's Rule 4b point
    about landing pages, applied to the creative. Doing it by hand means editing
    spec.py ten times and re-rendering after each, and a model in there to change
    a keyword also tidies the copy.

    HOW. One Chrome-free probe builds every (ad, layout) face in memory and
    reports the copy each would carry. A layout is legal for an ad only if every
    selling line survives. Then a greedy pass hands each ad the legal layout that
    is least used so far, so the wave spreads as wide as the copy permits.

    It never invents a look - it can only reach the layouts adkit/layouts.py
    already implements - and it never rewrites a word.
    """
    probe, err = _probe(kit)
    if probe is None:
        print("ERROR  %s" % err)
        return 2

    ov = {}
    f = kit / OVERRIDE
    if f.is_file():
        ov = json.loads(f.read_text(encoding="utf-8"))
    current = {}
    import re as _re
    src = (kit / "spec.py").read_text(encoding="utf-8", errors="replace")
    names = _re.findall(r'name\s*=\s*"([^"]+)"', src)
    lays = _re.findall(r'layout\s*=\s*"([^"]+)"', src)
    for n, l in zip(names, lays):
        current[n] = ov.get(n, l)

    legal = {}
    for ad, per in probe.items():
        base = set(per.get(current.get(ad, "default"), []))
        if not base:
            base = set(max(per.values(), key=len)) if per else set()
        legal[ad] = sorted(lay for lay, txt in per.items()
                           if base and base.issubset(set(txt)))

    # `photo` needs a supplied hero image (PROVENANCE: "supplied hero"), and with
    # no shot it renders a hole that the auto-fitter then cannot close - measured
    # 15 Sep 2026: 09_ev_battery_solar moved to `photo` and DID NOT FIT at any
    # scale down to 0.80. The copy probe cannot see this, because the text is all
    # present; it is the box model that fails. So never propose it for an ad that
    # is not already using it.
    for ad in legal:
        if current.get(ad) != "photo" and "photo" in legal[ad]:
            legal[ad] = [l for l in legal[ad] if l != "photo"]

    order = sorted(probe, key=lambda a: len(legal[a]))     # most constrained first
    used, plan = {}, {}
    for ad in order:
        options = list(legal[ad]) or [current.get(ad, "default")]
        options.sort(key=lambda l: (used.get(l, 0), l != current.get(ad), l))
        pick = options[0]
        plan[ad] = pick
        used[pick] = used.get(pick, 0) + 1

    width = max(len(a) for a in probe)
    print("\n  %s - %d face(s)\n" % (kit.name, len(probe)))
    print("  %-*s %-12s %-12s %s" % (width, "ad", "now", "proposed", "legal layouts"))
    print("  " + "-" * (width + 46))
    for ad in sorted(probe):
        mark = "" if plan[ad] == current.get(ad) else "  <- change"
        print("  %-*s %-12s %-12s %d of %d%s"
              % (width, ad, current.get(ad, "?"), plan[ad],
                 len(legal[ad]), len(probe[ad]), mark))

    print("\n  distinct skeletons: %d now -> %d proposed (of %d implemented)"
          % (len(set(current.values())), len(set(plan.values())), len(probe[order[0]])))
    tight = [a for a in probe if len(legal[a]) <= 2]
    if tight:
        print("\n  %d face(s) can only take 1-2 layouts - their copy uses fields most"
              "\n  skeletons do not carry: %s" % (len(tight), ", ".join(tight[:4])))

    if not apply:
        print("\n  Nothing changed. To apply:"
              "\n    python -m adkit.restyle %s --spread --apply\n" % kit.name)
        return 0

    # A layout can be legal on copy and still not FIT - the probe reads text, the
    # chassis auto-fitter reads the box model. When that happens, drop only the
    # face that failed back to its current layout and re-render. Aborting the whole
    # batch for one face would throw away the other improvements, which is how a
    # batch tool stops being used.
    dropped = []
    for _ in range(4):
        f.write_text(json.dumps(plan, indent=2), encoding="utf-8")
        ok, err = _render(kit)
        if ok:
            break
        stuck = re.findall(r"^\s*(\S+)\s+DOES NOT FIT", err, re.M)
        stuck = [s for s in stuck if plan.get(s) != current.get(s)]
        if not stuck:
            f.write_text(json.dumps(ov, indent=2), encoding="utf-8") if ov \
                else f.unlink(missing_ok=True)
            _render(kit)
            print("\n  render failed for a reason that is not a fit problem. "
                  "Reverted:\n%s" % err[-600:])
            return 2
        for s in stuck:
            dropped.append((s, plan[s]))
            plan[s] = current.get(s, "default")
    else:
        f.write_text(json.dumps(ov, indent=2), encoding="utf-8") if ov \
            else f.unlink(missing_ok=True)
        _render(kit)
        print("\n  could not settle after 4 passes. Reverted, nothing changed.")
        return 2

    bad = []
    for ad, face in _faces(kit).items():
        want = set(probe[ad].get(current.get(ad, "default"), []))
        if want and not want.issubset(_all(face)):
            bad.append(ad)
    if bad:
        f.write_text(json.dumps(ov, indent=2), encoding="utf-8") if ov \
            else f.unlink(missing_ok=True)
        _render(kit)
        print("\n  REVERTED - copy moved on %s despite the probe. That is a probe bug,"
              "\n  not a layout you should work around. Nothing was changed."
              % ", ".join(bad))
        return 1

    print("\n  applied. %d distinct skeletons, every selling line intact."
          % len(set(plan.values())))
    for ad, want in dropped:
        print("  %s stayed on '%s' - '%s' does not fit its copy at any scale."
              % (ad, plan[ad], want))
    print("  spec.py was not edited; the plan is in %s\n" % (kit / OVERRIDE))
    print("  Re-run the gates - new skeletons change the box model:")
    print("    python check_all.py %s" % kit.name)
    print("    python blind_reader.py --prepare %s\n" % kit.name)
    return 0


def revert(kit):
    f = kit / OVERRIDE
    if not f.is_file():
        print("no overrides in %s." % kit.name)
        return 0
    f.unlink()
    ok, err = _render(kit)
    print("overrides dropped and re-rendered." if ok else "re-render failed:\n%s" % err)
    return 0 if ok else 2


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    kit = pathlib.Path(args[0])
    if not kit.is_dir():
        kit = ROOT / args[0]
    if not kit.is_dir():
        print("not a kit folder: %s" % args[0])
        return 2

    def opt(flag):
        return args[args.index(flag) + 1] if flag in args and \
            args.index(flag) + 1 < len(args) else ""

    if "--revert" in args:
        return revert(kit)
    if "--spread" in args:
        return spread(kit, apply="--apply" in args)
    if "--ad" in args or "--to" in args:
        ad, to = opt("--ad"), opt("--to")
        if not ad or not to:
            print("need both --ad <name> and --to <layout>")
            return 2
        return restyle(kit, ad, to)
    return show_list(kit)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
