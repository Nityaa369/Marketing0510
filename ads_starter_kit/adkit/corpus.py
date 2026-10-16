#!/usr/bin/env python3
"""Find the ads that already ran, so the next one is written from evidence.

Why this exists. Everything needed to answer "what has worked for a reader like
this?" is already in this repo, and none of it is joined up:

    APPROVED/                        28 folders of approved kits
    GOLDEN/GOLDEN.md + 9 PNGs        the exemplar faces, with WHY IT PASSED
    ad-analysis-shared/CPL_WINNERS_31Aug2026.md   90 ads, Rs 4,275,135, real CPL
    CAMPAIGN_MAP.md                  which pairs were approved and which rejected
    <kit>/ad_copy.md                 the actual shipped primary text and headline
    <kit>/ads/*.png                  the actual shipped face

So a build starts by reading 2,822 lines of doctrine about what a good ad is,
when five real ads for a near-identical reader are sitting on disk with their
cost per lead attached. Doctrine is a compression of those ads; reading the ads
is both faster and better, and it is the only way to answer "what does NOT work"
with a number rather than a rule.

    python -m adkit.corpus --like "chartered accountant board seat"
    python -m adkit.corpus --like "women remote work virtual assistant" --quote 3
    python -m adkit.corpus --winners            what is live and cheap, with copy
    python -m adkit.corpus --losers             what is live and expensive
    python -m adkit.corpus --ad us05_evening    everything known about one ad

WHAT THE RANKING MEANS. Relevance is token overlap against the kit name, the ad
name, the headline and the primary text -- it is a finding aid, not a judgement.
The columns that carry judgement are CPL/CPP (live money) and APPROVED (a human
verdict). An ad with no CPL was never given enough budget to have an opinion
about; that is not the same as it being bad, and the table says `-` rather than
guessing.
"""
import pathlib
import re
import sys

from . import verdicts as _verdicts

ROOT = pathlib.Path(__file__).resolve().parent.parent
CPL_FILE = ROOT / "ad-analysis-shared" / "CPL_WINNERS_31Aug2026.md"
GOLDEN = ROOT / "GOLDEN"
APPROVED = ROOT / "APPROVED"

SKIP_DIRS = {"_archive", "_internal", "__pycache__", "node_modules", "ad_brief_tool",
             "ad_research", "judging-static-ads", "SOP", "docs", ".claude", ".git"}

STOP = set("a an the and or of for to in on at is are was were be been this that with "
           "you your my our their they it its as by from not no do does did who whom "
           "what which when where how why can could will would should i we he she".split())


def _tok(s):
    """Short tokens are dropped EXCEPT ones carrying a digit. `v4`, `w5`, `us05`
    and `i7` are ad identifiers and the most discriminative thing in a name; a
    plain len>2 filter threw them away and cost every live-money join on the
    Independent Director and US Accounting waves."""
    return [w for w in re.findall(r"[a-z0-9]+", (s or "").lower())
            if w not in STOP and (len(w) > 2 or any(c.isdigit() for c in w))]


# ------------------------------------------------------------------ live money

def load_live():
    """Parse the Meta pull into {normalised ad name: dict}. Free camps report cost
    per LEAD and paid camps cost per PURCHASE; the two are never mixed, so the
    family is carried on every row."""
    """Read EVERY priced table in the pull, by reading each table's own header row
    rather than a hardcoded heading and fixed column numbers.

    Why it changed (15 Sep 2026). The old version recognised exactly two headings,
    `## Free bootcamps` and `## Paid camps`, set family=None for any other `## `,
    and indexed cost at cells[4] and CTR at cells[5]. The pull has since grown a
    third priced table - `## Academic Writing, 26-28 Sep camp` - which is both
    under an unrecognised heading AND five columns wide instead of six. Both
    failures are silent: 12 priced ads, a whole product line's ICP-level costs,
    were invisible to corpus, --winners, --losers and every ICP rollup, with no
    error anywhere. Exactly the failure in the memory note
    `report_scripts_narrow_silently`.

    So: family comes from the cost column's own label (CPL -> lead, CPP ->
    purchase), and the cost and CTR columns are located by name. A table whose
    header names neither is skipped rather than guessed at, because a WRONG cost
    attached to an ad is worse than no cost - the same rule match_live() follows.
    """
    out = {}
    if not CPL_FILE.exists():
        return out
    family = i_cost = i_ctr = i_camp = i_spend = None
    for line in CPL_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("## "):
            family = None                      # every table declares its own shape
            continue
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        head = [c.strip("`* ").lower() for c in cells]

        if head and head[0] == "ad":           # a header row: learn this table
            family = i_cost = None
            for i, h in enumerate(head):
                if "cpl" in h:
                    family, i_cost = "lead", i
                elif "cpp" in h:
                    family, i_cost = "purchase", i
            i_ctr = next((i for i, h in enumerate(head) if "ctr" in h), None)
            i_camp = next((i for i, h in enumerate(head) if "camp" in h), None)
            i_spend = next((i for i, h in enumerate(head) if "spend" in h), None)
            continue

        if not family or i_cost is None or i_cost >= len(cells):
            continue
        name = cells[0].strip("`* ")
        cost = re.sub(r"[^0-9.]", "", cells[i_cost])
        if not name or not cost:               # "-" means it sold nothing: no cost
            continue
        ctr = re.sub(r"[^0-9.]", "", cells[i_ctr]) if i_ctr is not None \
            and i_ctr < len(cells) else ""
        out[name.lower()] = dict(
            name=name, family=family, cost=float(cost),
            ctr=float(ctr) if ctr else None,
            camp=cells[i_camp] if i_camp is not None and i_camp < len(cells) else "",
            spend=cells[i_spend] if i_spend is not None and i_spend < len(cells) else "")
    return out


def match_live(ad_name, live):
    """Meta ad names and kit file names are not the same string. Match on shared
    stems -- but conservatively, because a WRONG cost per lead attached to an ad
    is worse than no cost at all. The containment bonus is gated on both names
    being long enough to mean something: an unguarded version joined the ad named
    `01` to `01_static_earn-in-usd` and reported someone else's Rs 69 CPL on it."""
    a = ad_name.lower()
    ta = set(_tok(a))
    if not ta:
        return None
    best, score = None, 0
    for key, row in live.items():
        k = key.split("|")[-1]
        shared = ta & set(_tok(k))
        common = len(shared)
        if len(a) >= 6 and len(k) >= 6 and (k in a or a in k):
            common += 3
        # at least one shared token has to be a real word, not just an index
        if not any(len(s) >= 4 for s in shared):
            continue
        if common > score:
            best, score = row, common
    return best if score >= 2 else None


# ------------------------------------------------------------------ the corpus

BLOCK = re.compile(r"^##\s+(?P<name>[^\n*(]+)", re.M)


def parse_ad_copy(path):
    """Pull one block per ad out of a kit's ad_copy.md. Tolerant on purpose --
    sixteen kits wrote this file by hand and no two agree on the extras."""
    text = path.read_text(encoding="utf-8", errors="replace")
    blocks, marks = [], list(BLOCK.finditer(text))
    for i, m in enumerate(marks):
        chunk = text[m.end():marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        raw = m.group("name").strip()
        # Headings come in three shapes across sixteen hand-written files:
        #   ## cw_13_wheres_the_work                      the identifier alone
        #   ## 09 | CHROs AND HR HEADS | `09_chro_hr_heads`   backticked at the end
        #   ## v3_year_on_board - another year at work    identifier then a gloss
        # A backticked token is always the identifier; otherwise take the text
        # before the first gloss dash. Splitting on `|` alone reduced the second
        # shape to "09", which is not an ad name and joined to the wrong money.
        tick = re.findall(r"`([^`]+)`", raw)
        if tick:
            name = tick[-1]
        else:
            name = re.split(r"\s+[—-]\s+", raw)[0]
            name = name.split("|")[-1] if "|" in name else name
        name = name.strip().strip("`*_ ")
        name = re.sub(r"\.(png|jpg|html)$", "", name, flags=re.I)
        if not name or len(name) > 80 or not re.search(r"[a-z]", name, re.I):
            continue

        def field(label):
            f = re.search(r"\*\*%s:?\*\*\s*(.+?)(?=\n\*\*|\n##|\Z)" % label, chunk,
                          re.S | re.I)
            return " ".join(f.group(1).split()) if f else ""
        primary = field("Primary text")
        headline = field("Headline")
        if not (primary or headline):
            continue
        # A 900-character "headline" means this file is prose, not the block
        # format, and the parse is not trustworthy. Keep the block, drop the
        # field, rather than quoting nonsense as if it were shipped copy.
        if len(headline) > 200:
            headline = ""
        blocks.append(dict(ad=name, primary=primary, headline=headline,
                           description=field("Description"), page=field("Page")))
    return blocks


def index():
    """Every shipped ad this repo can see, joined to money and verdicts."""
    live = load_live()
    by_name, by_number = _verdicts.load()
    golden = {p.stem.lower() for p in GOLDEN.glob("*.png")} if GOLDEN.exists() else set()
    rows = []
    for copy_file in ROOT.rglob("ad_copy*.md"):
        rel = copy_file.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        kit_dir = copy_file.parent
        kit = str(kit_dir.relative_to(ROOT))
        approved = "APPROVED" in rel.parts
        pngs = {p.stem.lower(): p for p in (kit_dir / "ads").glob("*.png")} \
            if (kit_dir / "ads").is_dir() else {}
        for b in parse_ad_copy(copy_file):
            stem = b["ad"].lower()
            png = pngs.get(stem)
            if png is None:
                for k, p in pngs.items():
                    if stem in k or k in stem:
                        png = p
                        break
            v = _verdicts.for_ad(b["ad"], kit, by_name, by_number)
            b.update(kit=kit, kit_dir=kit_dir, png=png,
                     approved=approved or (v or {}).get("verdict") == _verdicts.APPROVED,
                     rejected=(v or {}).get("verdict") == _verdicts.REJECTED,
                     why=(v or {}).get("reason", ""),
                     golden=any(stem in g or g in stem for g in golden),
                     live=match_live(b["ad"], live))
            rows.append(b)
    seen, unique = set(), []
    for r in rows:
        key = (r["ad"].lower(), r["headline"].lower()[:60])
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)
    return unique


def score(row, terms):
    hay = _tok(row["kit"]) + _tok(row["ad"]) * 3 + _tok(row["headline"]) * 2 \
        + _tok(row["primary"])
    if not hay:
        return 0.0
    hits = sum(hay.count(t) for t in terms)
    s = hits / (len(hay) ** 0.5)
    if row["approved"]:
        s *= 1.35
    if row.get("rejected"):
        s *= 0.85
    if row["golden"]:
        s *= 1.5
    if row["live"]:
        s *= 1.25
    return s


def _cost(row):
    if not row["live"]:
        return "-"
    return "Rs%.0f/%s" % (row["live"]["cost"],
                          "lead" if row["live"]["family"] == "lead" else "buy")


def show(rows, quote=0, width=34):
    print("\n  %-34s %-30s %-11s %s" % ("ad", "kit", "live", "flags"))
    print("  " + "-" * 96)
    for r in rows:
        flags = " ".join(f for f, on in (("GOLDEN", r["golden"]),
                                         ("REJECTED", r.get("rejected")),
                                         ("APPROVED", r["approved"] and
                                          not r.get("rejected"))) if on)
        print("  %-34s %-30s %-11s %s"
              % (r["ad"][:34], r["kit"].split("/")[-1][:30], _cost(r), flags))
    for r in rows[:quote]:
        print("\n  --- %s   (%s)" % (r["ad"], r["kit"]))
        if r["png"]:
            print("      face: %s" % r["png"].relative_to(ROOT))
        if r["live"]:
            print("      live: %s, %s spend, CTR %s%%"
                  % (_cost(r), r["live"]["spend"], r["live"]["ctr"]))
        if r.get("rejected"):
            print("      REJECTED: %s" % (r.get("why") or "no reason recorded")[:200])
        elif r.get("why"):
            print("      approved: %s" % r["why"][:200])
        if r["headline"]:
            print("      headline: %s" % r["headline"])
        if r["primary"]:
            words = len(r["primary"].split())
            print("      primary (%d words): %s" % (words, r["primary"]))


def show_rejections(terms, query=""):
    """Rejected work near this ICP, ranked over the VERDICT RECORDS themselves
    rather than over the ad index.

    This is deliberate. The richest verdict set in CAMPAIGN_MAP.md -- the 12 Aug
    batch of 9 that CLAUDE.md Rule 1 is derived from -- is a set of LANDING PAGES,
    and the ad index is built from `ad_copy.md` blocks, so none of them appear in
    it. Ranking the ad index alone silently drops the most important rejections
    in the repo. Ranking the verdicts directly finds them, and the reason text is
    itself worth matching on: "not threaten with a regulator" is the lesson.
    """
    by_name, by_number = _verdicts.load()
    scored = []
    for name, rec in by_name.items():
        if rec["verdict"] != _verdicts.REJECTED:
            continue
        hay = _tok(name) * 2 + _tok(rec["reason"])
        hits = sum(hay.count(t) for t in terms)
        if hits:
            scored.append((hits / (len(hay) ** 0.5), name, rec))
    scored.sort(reverse=True)
    print("\n  REJECTED near this ICP - the cheaper lesson, in the reviewer's own words:")
    if not scored:
        print("    nothing recorded near %r. That is NOT evidence of safety: "
              "CAMPAIGN_MAP.md\n    only holds verdicts somebody wrote down." % query)
        return
    for _, name, rec in scored[:5]:
        print("    %-30s %s" % (name[:30], (rec["reason"] or "no reason recorded")[:86]))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2

    def opt(flag, default=None):
        return args[args.index(flag) + 1] if flag in args and \
            args.index(flag) + 1 < len(args) else default

    rows = index()
    quote = int(opt("--quote", 0) or 0)
    n = int(opt("-n", 12) or 12)

    if "--ad" in args:
        want = (opt("--ad") or "").lower()
        hit = [r for r in rows if want in r["ad"].lower()]
        if not hit:
            print("  no ad matching %r in %d indexed blocks." % (want, len(rows)))
            return 1
        show(hit[:n], quote=len(hit[:n]))
        return 0

    if "--winners" in args or "--losers" in args:
        have = [r for r in rows if r["live"]]
        fam = opt("--family", "lead")
        have = [r for r in have if r["live"]["family"] == fam]
        have.sort(key=lambda r: r["live"]["cost"], reverse="--losers" in args)
        label = "cheapest" if "--winners" in args else "most expensive"
        print("\n  The %s live ads, cost per %s. Source: %s"
              % (label, fam, CPL_FILE.relative_to(ROOT)))
        show(have[:n], quote=quote or 3)
        print("\n  Cost per lead and cost per purchase are different families and "
              "are never compared. Use --family purchase for the paid camps.")
        return 0

    if "--like" in args:
        terms = _tok(opt("--like", ""))
        if not terms:
            print("  --like needs something to match on.")
            return 2
        ranked = sorted(rows, key=lambda r: score(r, terms), reverse=True)
        ranked = [r for r in ranked if score(r, terms) > 0][:n]
        if not ranked:
            print("  nothing in the corpus matched %r." % opt("--like"))
            return 1
        print("\n  %d indexed ads. Closest precedents for %r:"
              % (len(rows), opt("--like")))
        show(ranked, quote=quote or 3)
        show_rejections(terms, opt("--like"))
        print("\n  Read the faces before writing a hook. Relevance here is token "
              "overlap; the judgement columns are live cost, APPROVED and REJECTED.")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
