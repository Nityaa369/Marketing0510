#!/usr/bin/env python3
"""The pre-build packet: what already worked for this reader, in one command.

WHY THIS EXISTS (15 Sep 2026). Asked directly: "if i ask for ads to be generated,
1/ past ad performances are pulled and analysed 2/ all the mds are put in action
right away". Both halves were manual. The repo holds 2,381 lines of MD across
CLAUDE.md, AD_CREATION_DIRECTOR.md and the constants card, plus a Meta pull, plus
473 labelled ICPs, and the build step that reads them was "remember to".

So this is the one command to run BEFORE writing anything. It prints the evidence,
not the doctrine - the MDs stay as the record of WHY, and this answers WHAT.

    python -m adkit.brief "women on a career break, content writing"
    python -m adkit.brief --worked        every ICP that has a live cost, ranked
    python -m adkit.brief --styles        every design style that ran, with cost

HOW STRONG IS THIS EVIDENCE. Weak, and the output says so on every run. Of 538
built ads, 20 carry a live cost - the pull is a 31 Aug snapshot and most ads never
got enough budget to have an opinion attached. That is not a ranking of ICPs; it
is the handful that were measured. Read it as "these are known to have worked",
never as "these are the best" and never as "the absent ones failed".

The count was 14 until 15 Sep 2026, when load_live() was found to be reading two
of the three priced tables in the pull - a whole product line's ICP-level costs
were invisible with no error. See corpus.load_live.__doc__.
"""
import pathlib
import re
import sys

from . import corpus as _corpus
from . import verdicts as _verdicts

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABELS = pathlib.Path(__file__).resolve().parent / "data" / "icp_labels.json"


def _labels():
    import json
    if not LABELS.exists():
        return {}
    raw = json.load(open(LABELS, encoding="utf-8"))
    out = {}
    for key, v in raw.items():
        stem = key.split("·")[-1].strip().lower()
        out[stem] = v
    return out


def _label_for(ad, labels):
    a = ad.lower()
    if a in labels:
        return labels[a]
    for k, v in labels.items():
        if len(k) >= 5 and (k in a or a in k):
            return v
    return None


def priced_icps():
    """[(cost, family, ad, kit, archetype, icp text)] for every priced ad we can
    attach an audience to."""
    labels = _labels()
    rows = []
    for r in _corpus.index():
        live = r.get("live")
        if not live:
            continue
        lab = _label_for(r["ad"], labels) or {}
        rows.append((live["cost"], live["family"], r["ad"], r["kit"],
                     lab.get("archetype", "?"), lab.get("icp", "")))
    rows.sort(key=lambda x: (x[1], x[0]))
    return rows


CAVEAT = """
  HOW TO READ THIS. {n} of {total} built ads carry a live cost; the rest never got
  enough budget to have an opinion attached. An ICP missing from this table was
  NOT measured and did not fail. Cost per lead and cost per purchase are different
  families and are never compared. Meta reports net of GST; gross up 18% before
  judging against SOP/02."""


def show_worked():
    rows = priced_icps()
    total = len(_corpus.index())
    print("\n  EVERY ICP WITH A LIVE COST, cheapest first, within family\n")
    fam = None
    for cost, family, ad, kit, arch, icp in rows:
        if family != fam:
            fam = family
            unit = "cost per lead" if family == "lead" else "cost per purchase"
            print("  --- %s ---" % unit)
            print("  %-34s %-7s %-3s %s" % ("ad", "cost", "typ", "audience"))
        print("  %-34s Rs%-5.0f %-3s %s"
              % (ad[:34], cost, arch, (icp or "(unlabelled)")[:44]))
    print(CAVEAT.format(n=len(rows), total=total))
    # Split by family. A median over both is meaningless - a Rs 30 lead and a
    # Rs 98 purchase are not the same number, which this file says two lines up.
    # The first version of this rollup broke its own rule.
    arch = {}
    for cost, family, ad, kit, a, icp in rows:
        arch.setdefault((family, a), []).append(cost)
    print("\n  by archetype, WITHIN family (SOP/08: A=occupation, B=life situation,")
    print("  C=aspiration, D=device-led, E=broad)")
    for family in ("lead", "purchase"):
        keys = sorted(k for k in arch if k[0] == family)
        if not keys:
            continue
        unit = "per lead" if family == "lead" else "per purchase"
        print("    --- %s ---" % unit)
        for k in keys:
            v = sorted(arch[k])
            print("    %-3s %d ad(s), median Rs%.0f" % (k[1], len(v), v[len(v) // 2]))
    print("    n is far too small to rank archetypes from this. SOP/08's table is")
    print("    fitted on 128 ads and stays the source for that judgement.\n")
    return 0


def show_styles():
    try:
        from . import styles as _styles
    except Exception as exc:                                    # noqa: BLE001
        print("could not load adkit.styles: %s" % exc)
        return 2
    print("\n  DESIGN STYLES THAT HAVE RUN\n")
    fn = getattr(_styles, "main", None)
    if fn:
        fn(["styles"])
    print("\n  Only two styles carry a measured cost, and both are worse than par:")
    print("    pay chart  2.34x   (four product lines, never build one)")
    print("    toon/chat  1.22x")
    print("  Every other style is unpriced. Variety is a rule from the reviewer")
    print("  (Rule 4b, and 'make sure each have distinct colour palette'), not a")
    print("  finding from cost.\n")
    return 0


def show_like(query):
    terms = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    labels = _labels()

    print("\n  WHAT ALREADY RAN FOR A READER LIKE THIS")
    print("  query: %s\n" % query)

    rows = _corpus.index()
    scored = sorted(rows, key=lambda r: _corpus.score(r, terms), reverse=True)
    top = [r for r in scored if _corpus.score(r, terms) > 0][:8]
    if not top:
        print("  nothing in the corpus matches those words. Widen the query, or")
        print("  this is a genuinely new audience - say so when you hand it over.\n")
    else:
        print("  %-30s %-11s %-9s %s" % ("ad", "live", "verdict", "headline"))
        print("  " + "-" * 96)
        for r in top:
            live = ("Rs%.0f/%s" % (r["live"]["cost"],
                                   "lead" if r["live"]["family"] == "lead" else "buy")) \
                if r.get("live") else "-"
            verdict = "APPROVED" if r.get("approved") else (
                "REJECTED" if r.get("rejected") else "")
            print("  %-30s %-11s %-9s %s"
                  % (r["ad"][:30], live, verdict, r["headline"][:44]))

    priced = [r for r in top if r.get("live")]
    if priced:
        print("\n  Of those, the ones with money attached:")
        for r in sorted(priced, key=lambda x: x["live"]["cost"]):
            lab = _label_for(r["ad"], labels) or {}
            print("    Rs%-5.0f %-28s %s" % (r["live"]["cost"], r["ad"][:28],
                                             lab.get("icp", "")[:44]))

    print("\n  REJECTIONS NEAREST THIS READER - read these before writing a hook")
    try:
        _corpus.show_rejections(terms, query)
    except Exception:                                           # noqa: BLE001
        by_name, _ = _verdicts.load()
        shown = 0
        for ad, v in (by_name or {}).items():
            if v.get("verdict") == _verdicts.REJECTED and v.get("reason"):
                print("    %-28s %s" % (ad[:28], v["reason"][:60]))
                shown += 1
        if not shown:
            print("    none recorded. python -m adkit.verdict --pending")

    print("""
  THEN, IN THIS ORDER (a rejection costs less the earlier it lands):
    1  ICP list, RANKED     preflight.py --scaffold-from <icps.md> <kit>
                            preflight.py --shortlist <kit>          ~a paragraph
    2  value_props.md                                               ~a paragraph
    3  hooks.md as a TABLE  hook_rules.py --kit <kit>               ~a line
    4  ONE ad + its LP                                              ~one pair
    5  the rest                                                     ~the wave

  AND BEFORE HANDOVER:
    python check_all.py <kit>
    python blind_reader.py --prepare <kit>   (then --score)
""")
    return 0


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if args[0] == "--worked":
        return show_worked()
    if args[0] == "--styles":
        return show_styles()
    return show_like(" ".join(args))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
