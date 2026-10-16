#!/usr/bin/env python3
"""Measure the approved ad-copy corpus and print the numbers SOP/07_AD_COPY.md is fitted to.

Every rule in SOP/07 carries a count. This script is where those counts come from, so the
SOP can be re-fitted after each approval batch instead of drifting into folklore.

Baseline, run 31 Aug 2026 over APPROVED/ (150 blocks, 16 kits):

    primary text words    p25 80  median 86  p75 97  p90 106   (93% <= 110)
    headline words        p25 6   median 7   p90 9    max 10   (no approved headline > 10)
    description words     median 13  max 23
    delivery sentence present            139/150   92%
      ... naming exactly three things    136/139   98%
      ... carrying "in 6 months"          99/150   66%
    em-dashes in copy blocks               0/150
    banned filler words                    0/150
    statistic present                     37/150   24%

The 100-150 word primary-text figure in AD_CREATION_DIRECTOR.md sec 7 predates this census
and is not supported by it; SOP/07 supersedes that figure.

Usage:  python SOP/tools/copy_census.py [corpus-dir]      (default: APPROVED)
"""
import collections
import glob
import os
import re
import statistics
import sys

BANNED = [
    "transform", "unlock", "discover", "elevate", "leverage", "empower", "journey",
    "dive into", "game-chang", "revolution", "seamless", "cutting-edge", "freelanc",
    "skyrocket", "unleash", "harness", "navigate", "landscape", "ever-evolving",
    "in today", "—",
]

DELIVERY_VERB = re.compile(r"\bwe (show|teach|check|map|give|take) ", re.I)


def load(root):
    blocks = []
    for path in glob.glob(os.path.join(root, "**", "ad_copy*.md"), recursive=True):
        kit = os.path.relpath(path, root).split(os.sep)[0]
        text = open(path, encoding="utf-8").read()
        # kits head each ad with "## " or "### " (both are in use); accept either, or
        # whole kits go silently uncounted and a zero reads as "clean".
        for chunk in re.split(r"\n#{2,4} ", text)[1:]:
            pt = re.search(r"\*\*Primary text:\*\*(.*?)(?=\n\*\*|\n#|\Z)", chunk, re.S)
            if not pt:
                continue
            hd = re.search(r"\*\*Headline:\*\*(.*)", chunk)
            ds = re.search(r"\*\*Description:\*\*(.*)", chunk)
            blocks.append({
                "kit": kit,
                "id": chunk.split("\n")[0].strip()[:48],
                "pt": " ".join(pt.group(1).split()),
                "hd": hd.group(1).strip() if hd else "",
                "ds": ds.group(1).strip() if ds else "",
            })
    return blocks


def pctile(values, p):
    values = sorted(values)
    return values[min(int(len(values) * p), len(values) - 1)]


def delivery_sentence(pt):
    for s in re.split(r"(?<=[.?!]) ", pt):
        if DELIVERY_VERB.search(s):
            return s
    return None


def compare(roots):
    """One row per corpus. Use to score an unbuilt kit against the APPROVED baseline."""
    cols = ("kit", "n", "pt med", "hl max", "delivery", "plan", "horizon", "negation", "over")
    print("%-44s %4s %7s %7s %9s %6s %8s %9s %5s" % cols)
    print("-" * 108)
    for root in roots:
        blocks = load(root)
        name = os.path.basename(os.path.normpath(root))[:44]
        if not blocks:
            print("%-44s %4d  (no ad_copy blocks found)" % (name, 0))
            continue
        n = len(blocks)
        ptw = [len(b["pt"].split()) for b in blocks]
        hw = [len(b["hd"].split()) for b in blocks if b["hd"]]
        have = sum(1 for b in blocks if delivery_sentence(b["pt"]))
        plan = sum(1 for b in blocks if re.search(r"\bthe (plan|method|route)\b|plan that|plan to", b["pt"]))
        hor = sum(1 for b in blocks if re.search(r"\bin \d+ (months|days|weeks)\b", b["pt"]))
        neg = sum(1 for b in blocks if re.search(r"\bNo [A-Za-z][^.,]{0,24}[.,]\s*[Nn]o\b", b["pt"]))
        over = sum(1 for w in ptw if w > 110) + sum(1 for w in hw if w > 10)
        print("%-44s %4d %7.1f %7d %8d%% %5d%% %7d%% %8d%% %5d" % (
            name, n, statistics.median(ptw), max(hw) if hw else 0,
            100 * have // n, 100 * plan // n, 100 * hor // n, 100 * neg // n, over))
    print("\nAPPROVED baseline (31 Aug 2026): pt med 86 | hl max 10 | delivery 92% | plan 82%")
    print("horizon 69% overall, but 92-100% in route-to-a-client camps (ID, IP Law, US Accounting,")
    print("USCL, Arbitration) and 0% in Women Remote / Content Writing / SQE -- read it per product line.")


def copy_rules():
    """The SOP/07 rules, each a predicate that returns True when a block BREAKS the rule."""
    return {
        "headline > 10 words": lambda b: len(b["hd"].split()) > 10,
        "primary text > 110 words": lambda b: len(b["pt"].split()) > 110,
        "no delivery sentence": lambda b: not delivery_sentence(b["pt"]),
        "delivery names < 3 things": lambda b: (
            lambda d: not d or not (d.count(",") >= 2 or ", and" in d))(delivery_sentence(b["pt"])),
        "no horizon": lambda b: not re.search(r"\bin \d+ (months|days|weeks)\b", b["pt"]),
        "no plan/method/route": lambda b: not re.search(
            r"\bthe (plan|method|route)\b|plan that|plan to", b["pt"]),
        "no negation strip": lambda b: not re.search(
            r"\bNo [A-Za-z][^.,]{0,24}[.,]\s*[Nn]o\b", b["pt"]),
        "headline title-case": lambda b: (lambda w: len(w) >= 3 and all(x[0].isupper() for x in w))(
            [x for x in b["hd"].split() if x.isalpha() and len(x) > 3]),
        "bare pronoun in headline": lambda b: bool(re.search(
            r"\b(They|Them|Their|It|That|This|Those|These)\b", b["hd"])),
        "opening sentence > 25 words": lambda b: len(
            re.split(r"(?<=[.?!]) ", b["pt"])[0].split()) > 25,
    }


def ramanuj_blocks():
    """Every copy block from a face Ramanuj approved or built himself, via adkit.golden.

    Same basis hook_rules.py was refitted on (31 Aug 2026), so the two checkers move
    together: record a verdict in CAMPAIGN_MAP.md, rebuild GOLDEN, and both refit."""
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, root)
    try:
        from adkit import golden
    except Exception:                                  # noqa: BLE001
        return []
    out = []
    for e in golden.collect():
        pt = " ".join((e.get("primary") or "").split())
        if pt:
            out.append({"id": e.get("name", ""), "hd": (e.get("headline") or "").strip(),
                        "pt": pt})
    return out


def selftest():
    """Fit every SOP/07 rule against copy Ramanuj actually approved.

    Until 28 Sep 2026 this scored the rules against the Section A split (13 approved,
    7 rejected). Those labels were in-house and never shipped, so hook_rules.py and
    simplicity.py were refitted away from them on 31 Aug; this selftest kept importing
    names hook_rules had renamed and crashed on every run. It now uses the same basis
    they do: the approved copy blocks in GOLDEN.

    What it measures is PRECISION: how often a rule fires on approved work. A rule
    that fires on more than 10% of approved blocks cannot be used to reject copy. There
    is no labelled negative set, so recall (what a rule catches) is not measured; the
    old Section A split is printed after the fit for reference only.

    SOP/07 is a style guide fitted to approved output, NOT a rejection predictor. This
    function is how we know which of its rules could ever be a gate.
    """
    blocks = ramanuj_blocks()
    if not blocks:
        print("ERROR: could not load Ramanuj-approved copy via adkit.golden.")
        print("A fit that cannot see its evidence is not a pass. Run from the repo root.")
        return 2
    rules = copy_rules()
    print("FIT: false alarms on %d copy blocks Ramanuj approved or built himself.\n" % len(blocks))
    print("%-28s %-22s %s" % ("rule", "fires on approved", "verdict"))
    print("-" * 78)
    usable = []
    for name, fn in rules.items():
        hits = [b for b in blocks if fn(b)]
        pct = 100.0 * len(hits) / len(blocks)
        if pct > 10:
            verdict = "style only, never a gate"
        elif hits:
            verdict = "low noise, may gate with a human read"
            usable.append(name)
        else:
            verdict = "never fires on approved work"
            usable.append(name)
        print("%-28s %4d / %-4d (%4.1f%%)  %s" % (name, len(hits), len(blocks), pct, verdict))
    print("\nRules that could gate (<= 10%% false alarms): %s" % (", ".join(usable) or "none"))
    print("Recall is NOT measured: there is no labelled set of copy Ramanuj rejected.")

    # Reference only: the in-house Section A split this selftest used to fit against.
    try:
        from hook_rules import SECTIONA_INHOUSE_APPROVED, SECTIONA_INHOUSE_REJECTED
    except ImportError:
        return 0
    by_id = {}
    for b in load("ContentWriting_SectionA_29-31Aug"):
        m = re.match(r"(\d\d)", b["id"])
        if m:
            by_id[m.group(1)] = b
    app = [n for n, _ in SECTIONA_INHOUSE_APPROVED if n in by_id]
    rej = [n for n, _ in SECTIONA_INHOUSE_REJECTED if n in by_id]
    if app and rej:
        print("\nOLD Section A split, for reference only (in-house labels, never shipped):")
        for name, fn in rules.items():
            tp = [n for n in rej if fn(by_id[n])]
            fp = [n for n in app if fn(by_id[n])]
            print("  %-28s catches %d/%d, false alarms %d/%d" % (
                name, len(tp), len(rej), len(fp), len(app)))
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    if len(sys.argv) > 2 or (len(sys.argv) > 1 and sys.argv[1] == "--vs"):
        roots = [a for a in sys.argv[1:] if a != "--vs"]
        return compare(roots)
    root = sys.argv[1] if len(sys.argv) > 1 else "APPROVED"
    blocks = load(root)
    if not blocks:
        print("no ad_copy*.md blocks found under %s" % root)
        return 1
    n = len(blocks)
    print("corpus: %s  |  %d blocks  |  %d kits\n" % (root, n, len(set(b["kit"] for b in blocks))))

    ptw = [len(b["pt"].split()) for b in blocks]
    print("primary text words    p25 %d  median %d  p75 %d  p90 %d  max %d   (<=110: %d/%d)" % (
        pctile(ptw, .25), statistics.median(ptw), pctile(ptw, .75), pctile(ptw, .90),
        max(ptw), sum(1 for w in ptw if w <= 110), n))

    hw = [len(b["hd"].split()) for b in blocks if b["hd"]]
    print("headline words        p25 %d  median %d  p90 %d  max %d" % (
        pctile(hw, .25), statistics.median(hw), pctile(hw, .90), max(hw)))

    dsw = [len(b["ds"].split()) for b in blocks if b["ds"]]
    if dsw:
        print("description words     median %d  max %d" % (statistics.median(dsw), max(dsw)))

    sents = [len(s.split()) for b in blocks for s in re.split(r"(?<=[.?!]) ", b["pt"]) if s.strip()]
    print("sentence words        median %d  p90 %d" % (statistics.median(sents), pctile(sents, .90)))
    opens = [len(re.split(r"(?<=[.?!]) ", b["pt"])[0].split()) for b in blocks]
    print("opening sentence      median %d  p90 %d" % (statistics.median(opens), pctile(opens, .90)))

    dels = [delivery_sentence(b["pt"]) for b in blocks]
    have = [d for d in dels if d]
    three = [d for d in have if d.count(",") >= 2 or ", and" in d]
    print("\ndelivery sentence present          %3d/%d  %d%%" % (len(have), n, 100 * len(have) // n))
    print("  ... naming exactly three things  %3d/%d  %d%%" % (
        len(three), len(have), 100 * len(three) // max(len(have), 1)))
    for phrase in ("the plan", "in 6 months", "we show you"):
        c = sum(1 for b in blocks if phrase in b["pt"].lower())
        print("  ... %-28s %3d/%d  %d%%" % ('"%s"' % phrase, c, n, 100 * c // n))

    neg = sum(1 for b in blocks if re.search(r"\bNo [A-Za-z][^.,]{0,24}[.,]\s*[Nn]o\b", b["pt"]))
    stat = sum(1 for b in blocks if re.search(r"\b\d[\d,]{2,}\b|\b\d+ percent\b", b["pt"]))
    print("\nnegation strip (>=2 'No X')        %3d/%d  %d%%" % (neg, n, 100 * neg // n))
    print("statistic present                  %3d/%d  %d%%" % (stat, n, 100 * stat // n))

    print("\nbanned words / em-dashes:")
    hits = 0
    for w in BANNED:
        c = sum(1 for b in blocks if w in (b["pt"] + " " + b["hd"]).lower())
        if c:
            hits += c
            print("  PRESENT  %-16s x%d" % (w.replace("—", "em-dash"), c))
    if not hits:
        print("  none present (0 across the whole corpus)")

    over = [b for b in blocks if len(b["hd"].split()) > 10]
    long_pt = [b for b in blocks if len(b["pt"].split()) > 110]
    if over or long_pt:
        print("\noutside the SOP/07 limits:")
        for b in over:
            print("  headline %d words   %s | %s" % (len(b["hd"].split()), b["kit"][:28], b["hd"]))
        for b in long_pt:
            print("  primary  %d words   %s | %s" % (len(b["pt"].split()), b["kit"][:28], b["id"]))

    print("\nheadline opening words:", collections.Counter(
        b["hd"].split()[0] for b in blocks if b["hd"]).most_common(10))
    return 0


if __name__ == "__main__":
    sys.exit(main())
