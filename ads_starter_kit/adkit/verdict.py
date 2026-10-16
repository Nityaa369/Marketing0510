"""Record what the reviewer said, so the next kit starts from it.

WHY THIS EXISTS (31 Aug 2026). `corpus.py` and `icp.py` only know what
`CAMPAIGN_MAP.md` happens to say in prose, parsed conservatively by
`verdicts.py`. That parse is lossy by design -- a verdict attached to the wrong
ad is worse than no verdict -- so most reviews never reach the index at all.

The measured consequence: a blind test of the ICP method re-proposed a
practising-credential audience that had already produced 5 ads and 0 approved,
then 3 and 0, then a kit halted at spec. The method has no memory; only the
archive does. An archive that is only updated when somebody remembers to write a
paragraph is an archive that drifts out of date exactly when a wave is busiest.

So this is the deliberately cheap way to record a verdict at the moment it is
given, in the reviewer's own words:

    python -m adkit.verdict WomenRemote_Wave9_SEND_THIS \\
        --approved X31_evidence,X32_story,X33_demand,X34_method,X36_room \\
        --rejected X35_dayone --why "cryptic, we can drop it"

It appends to `adkit/data/verdicts.jsonl`, which `verdicts.load()` merges OVER
the CAMPAIGN_MAP parse -- an explicit record always beats an inferred one.

THE LOOP THIS CLOSES. After a wave is reviewed:

    1. python -m adkit.verdict <kit> --approved ... --rejected ... --why "..."
    2. python -m adkit.icp --extract      # pick up the new ads
    3. python -m adkit.icp --unlabelled   # what still needs an ICP label
    4. label those, then: python -m adkit.icp --report

Step 3 is the only part that needs a person or a model: an ICP label is a
judgement, not a regex. Everything else regenerates.
"""
import json
import re
import pathlib
import sys
import time

DATA = pathlib.Path(__file__).resolve().parent / "data"
STORE = DATA / "verdicts.jsonl"

APPROVED, REJECTED = "APPROVED", "REJECTED"


def record(kit, approved=(), rejected=(), why="", when=None):
    """Append one review. Returns the number of ads recorded."""
    DATA.mkdir(parents=True, exist_ok=True)
    stamp = when or time.strftime("%Y-%m-%d")
    rows = []
    for ad in approved:
        rows.append(dict(ad=ad, kit=kit, verdict=APPROVED, reason="", date=stamp))
    for ad in rejected:
        rows.append(dict(ad=ad, kit=kit, verdict=REJECTED, reason=why, date=stamp))
    with STORE.open("a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


def load():
    """{lowercased ad name: dict(verdict, reason, how)} from the explicit store.

    Later lines win, so a re-review supersedes an earlier one rather than
    needing the file edited.
    """
    out = {}
    if not STORE.exists():
        return out
    for line in STORE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("ad") and r.get("verdict"):
            out[r["ad"].lower()] = dict(verdict=r["verdict"],
                                        reason=r.get("reason", ""),
                                        how="recorded")
    return out


def _split(s):
    return [x.strip() for x in (s or "").replace(",", " ").split() if x.strip()]


# --------------------------------------------------------- the two-step review
#
# WHY THIS EXISTS (15 Sep 2026). The flag form below is correct and was used
# exactly once, on the day it was written. The census that day: 538 built ads in
# the corpus, 7 rows in this store. So every checker in the repo is a ONE-CLASS
# fit - check_all.py --brief says so outright: "They show a rule does not block
# good work. They cannot show what they catch - there is no set of faces Ramanuj
# rejected with sources in this repo."
#
# The back-and-forth IS the missing training data, and it was being thrown away
# after every round.
#
# The friction was never the append. It was that a review arrives as prose on
# WhatsApp - "these are fine, drop 3 and 7, the second one is cryptic" - and the
# flag form makes you translate that into ad names before you can record it. So
# do not parse the prose. Pre-fill the ad list and let a person mark it:
#
#     python -m adkit.verdict <kit> --review    writes <kit>/.review.md, prefilled
#     (change each ? to A or R, put his words on the R lines)
#     python -m adkit.verdict <kit> --apply     reads it back and records
#
# Five keystrokes per ad, and the reviewer's own sentence is kept verbatim, which
# is the part worth having.

REVIEW_FILE = ".review.md"

REVIEW_HEADER = """# Review: {kit}
#
# Mark each ad below. Change the leading ? to:
#     A   approved
#     R   rejected  - put HIS OWN WORDS after the ad name, on the same line
#     ?   no verdict yet (left alone, not recorded)
#
# A rejection with no reason is refused. That sentence is the most useful thing
# in the archive - it is what turns these checkers from one-class into two-class.
#
# quote: <optional - one sentence covering the whole batch. Used as the reason
#         for any R line that has no reason of its own.>
#
# Then: python -m adkit.verdict "{kit}" --apply

"""


def _ads_in(kit_dir):
    ads = pathlib.Path(kit_dir) / "ads"
    if not ads.is_dir():
        return []
    skip = ("index", "contact", "review", "sheet", "thumb", "_grid")
    return sorted(p.stem for p in ads.glob("*.png")
                  if not any(s in p.name.lower() for s in skip))


def write_review(kit):
    kit_dir = pathlib.Path(kit)
    ads = _ads_in(kit_dir)
    if not ads:
        print("no ads/*.png in %s - nothing to review." % kit_dir)
        return 2
    known = load()
    out = [REVIEW_HEADER.format(kit=kit_dir.name)]
    for ad in ads:
        prev = known.get(ad.lower())
        note = ""
        if prev:
            note = "    # already recorded: %s %s" % (prev["verdict"],
                                                      prev["reason"][:40])
        out.append("?  %-34s%s" % (ad, note))
    path = kit_dir / REVIEW_FILE
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n  wrote %s with %d ad(s).\n" % (path, len(ads)))
    print("  Mark each line A or R, put his words on the R lines, then:")
    print('    python -m adkit.verdict "%s" --apply\n' % kit)
    return 0


def parse_review(text):
    """-> (approved, [(ad, reason)], batch_quote)."""
    approved, rejected, quote = [], [], ""
    for line in text.splitlines():
        m = re.match(r"^\s*#\s*quote:\s*(.+)", line, re.I)
        if m and "<optional" not in m.group(1):
            quote = m.group(1).strip()
            continue
        if line.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*([ARar?])\s+(\S+)\s*(.*)$", line)
        if not m:
            continue
        mark, ad, rest = m.group(1).upper(), m.group(2), m.group(3).strip()
        rest = re.sub(r"\s*#.*$", "", rest).strip()
        if mark == "A":
            approved.append(ad)
        elif mark == "R":
            rejected.append((ad, rest))
    return approved, rejected, quote


def apply_review(kit):
    kit_dir = pathlib.Path(kit)
    path = kit_dir / REVIEW_FILE
    if not path.is_file():
        print("no %s - run --review first." % path)
        return 2
    approved, rejected, quote = parse_review(path.read_text(encoding="utf-8"))
    if not approved and not rejected:
        print("every line is still '?' in %s - nothing marked, nothing recorded."
              % path)
        return 2

    blank = [ad for ad, why in rejected if not why and not quote]
    if blank:
        print("\n  REFUSED. %d rejection(s) carry no reason: %s\n"
              % (len(blank), ", ".join(blank)))
        print("  Put his own words after the ad name, or add a batch-wide")
        print("  '# quote: ...' line. A bare REJECTED teaches the next kit")
        print("  nothing, which is how 538 built ads produced 7 usable rows.\n")
        return 2

    print("\n  about to record for %s:\n" % kit_dir.name)
    for ad in approved:
        print("    APPROVED  %s" % ad)
    for ad, why in rejected:
        print("    REJECTED  %-30s %s" % (ad, why or quote))
    n = 0
    for ad, why in rejected:
        n += record(kit_dir.name, (), [ad], why or quote)
    if approved:
        n += record(kit_dir.name, approved, (), "")
    print("\n  recorded %d verdict(s) -> %s" % (n, STORE))
    print("\n  now refresh the index:")
    print("    python -m adkit.icp --extract")
    print("    python -m adkit.icp --unlabelled")
    print("    python -m adkit.icp --report")
    return 0


def pending(root=None):
    """Kits that shipped faces and have no verdict recorded against any of them.

    This is the number that matters: an unrecorded review is a review that
    happened and taught the repo nothing."""
    root = pathlib.Path(root or pathlib.Path(__file__).resolve().parent.parent)
    known = load()
    rows = []
    for d in sorted(root.glob("*/")):
        if d.name.startswith((".", "_")) or d.name in ("adkit", "SOP", "GOLDEN",
                                                       "APPROVED", "docs"):
            continue
        ads = _ads_in(d)
        if not ads:
            continue
        have = sum(1 for a in ads if a.lower() in known)
        rows.append((d.name, len(ads), have))
    unrecorded = [r for r in rows if r[2] == 0]
    print("\n  %d kit(s) with shipped faces; %d have NO recorded verdict.\n"
          % (len(rows), len(unrecorded)))
    for name, n, have in rows:
        flag = "  " if have else "->"
        print("  %s %-52s %2d face(s), %2d recorded" % (flag, name[:52], n, have))
    if unrecorded:
        print("\n  For each '->', after the review comes back:")
        print('    python -m adkit.verdict "<kit>" --review')
        print('    python -m adkit.verdict "<kit>" --apply')
    print("\n  Every checker here is fitted on approvals only. Rejections are the")
    print("  half that is missing, and they arrive free with every round.\n")
    return 0


def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0

    if args[0] == "--pending":
        return pending()

    if args[0] == "--list":
        rows = load()
        print("\n  %d ads with a recorded verdict\n" % len(rows))
        for ad, v in sorted(rows.items()):
            print("   %-10s %-34s %s" % (v["verdict"], ad, v["reason"][:60]))
        return 0

    kit = args[0]

    if "--review" in args:
        return write_review(kit)
    if "--apply" in args:
        return apply_review(kit)

    def opt(flag):
        return args[args.index(flag) + 1] if flag in args else ""

    approved = _split(opt("--approved"))
    rejected = _split(opt("--rejected"))
    why = opt("--why")
    if not approved and not rejected:
        print("nothing to record: pass --approved and/or --rejected")
        return 2
    if rejected and not why:
        print("a rejection needs --why, in the reviewer's own words. "
              "That sentence is the most useful thing in the archive.")
        return 2
    n = record(kit, approved, rejected, why)
    print("recorded %d verdict(s) for %s -> %s"
          % (n, kit, STORE.relative_to(DATA.parent.parent)))
    print("\nnow refresh the index:\n"
          "  python -m adkit.icp --extract\n"
          "  python -m adkit.icp --unlabelled\n"
          "  python -m adkit.icp --report")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
