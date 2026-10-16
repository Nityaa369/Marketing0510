"""The ICP index — every audience this account has ever pointed an ad at.

WHY THIS EXISTS (31 Aug 2026). A blind test ran the documented ICP method against
three product lines with no repo access. Coverage of the audiences that actually
shipped tracked how occupation-heavy the line was:

    Independent Director   ~85% of live ICPs found   (live set is occupations)
    Content Writing        ~71%                      (occupations)
    Women Remote           ~32%                      (live set is life situations)

Two failure modes, both fixable with evidence rather than instruction:

  1. **Life-stage blindness.** The method reliably produces occupations and
     systematically misses situations — small city, empty nest, retired, single
     mother, own health, school fees. Three of those four are among the best
     converting segments this account has run.
  2. **No memory.** One blind run in four proposed a practising-credential ICP
     (nurses) for the women's camp -- the exact idea that produced 5 ads and 0
     approved, then 3 and 0, then a kit halted at spec on 6-of-6 step-DOWN blind
     reads. Nothing in the method prevents it; only the archive does.

So this module turns 477 shipped ads into a queryable list of AUDIENCES, carrying
the archetype, the verdict, and the live cost per result where one exists. It is
the ICP-level companion to `corpus.py`, which is ad-level.

    python -m adkit.icp                      # the index, grouped by archetype
    python -m adkit.icp --line women         # one product line
    python -m adkit.icp --situations         # the situation vocabulary only
    python -m adkit.icp --rejected           # audiences that failed, and why
    python -m adkit.icp --report             # regenerate SOP/ICP_INDEX.md
    python -m adkit.icp --extract            # rebuild the evidence file for labelling

HOW AN ICP IS RECOVERED, in priority order. Only the first two are stated by a
human; the rest are inferred, and the index says which.

    1. `**ICP:**` in the kit's ad_copy.md          (54 ads -- waves 6/7/8 style)
    2. the `value_props.md` block for that ad       (33 ads)
    3. the call-out band read off html/<stem>.html  (62 ads)
    4. the ad name + headline + the opening of the primary text

Source 4 covers most of the corpus and is not a guess in this repo: the naming
convention IS the ICP label (`X27_career_gap`, `i2_cfo`, `icp_27_semicon_vlsi`,
`N20_small_city`). The normalised phrase and the archetype for those are written
into `adkit/data/icp_labels.json` by a labelling pass and committed, so the index
is reproducible and reviewable rather than re-derived differently every run.
"""
import json
import pathlib
import re
import sys

from adkit import corpus

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = pathlib.Path(__file__).resolve().parent / "data"
RAW = DATA / "icp_raw.json"
LABELS = DATA / "icp_labels.json"
SITUATIONS = DATA / "situations.json"
REPORT = ROOT / "SOP" / "ICP_INDEX.md"

ARCHETYPES = {
    "A": "an occupation, adding a line to what they already do",
    "B": "a life situation they are living in and can point at",
    "C": "an aspiration or abstract state",
    "D": "device-led, no ICP named",
    "E": "a broad population",
}
INDEX = {"A": 0.98, "B": 0.96, "C": 1.05, "D": 1.22, "E": 1.15}

# Product line from the kit folder. Order matters: first hit wins.
LINES = [
    ("women-remote", r"womenremote|womensremotework|women_?remote|womenfreelance|handoff_women"),
    ("women-ai", r"womens?_?ai"),
    ("content-writing", r"contentwriting|content-writing|moneydesk"),
    ("independent-director", r"independentdirector|id_|paychart_independent"),
    ("us-accounting", r"us_accounting|usacc|accounting_bc"),
    ("data-privacy", r"dataprivacy"),
    ("patent", r"patent"),
    ("ip-law", r"iplaw"),
    ("corporate-finance", r"corporatefinance"),
    ("us-corporate-law", r"uscl"),
    ("hr", r"hr_growthcamp"),
    ("senior-ai", r"seniorai"),
    ("consulting", r"consulting"),
    ("arbitration", r"arbitration"),
    ("tech-law", r"techlaw"),
    ("paralegal", r"paralegal"),
    ("sqe", r"sqe"),
    ("academic-writing", r"acw|academic"),
]

# Leading tokens that are a filing code rather than part of the audience label.
# Two classes only, so that a real short word survives: a token containing a digit
# (x27, i2, 10d, 05, us05), and a known kit prefix. Stripping every short token
# turned `icp_30_research_fellows` into "cp 30 research fellows" and would have
# eaten `cfo` and `banker`, which ARE the audience.
CODE_TOKEN = re.compile(r"^[a-z]{0,6}\d+[a-z]?$", re.I)
KIT_PREFIX = {"icp", "lp", "ad", "pc", "paychart", "usmb", "cw", "px", "wrw",
              "rid", "hoc", "acw", "dpdp", "mh", "st", "sc", "usacc", "uscl"}
TRAIL = re.compile(r"_(v\d+|cag|r\d+|final|new)$", re.I)


def line_of(kit):
    k = kit.lower().replace("\\", "/")
    for name, pat in LINES:
        if re.search(pat, k):
            return name
    return "other"


def name_to_phrase(ad):
    """`X27_career_gap` -> 'career gap'. The repo's naming convention is the label."""
    s = TRAIL.sub("", ad)
    toks = [t for t in re.split(r"[_\-\s]+", s) if t]
    while toks and (CODE_TOKEN.match(toks[0]) or toks[0].lower() in KIT_PREFIX
                    or not re.search(r"[a-z0-9]", toks[0], re.I)):
        toks.pop(0)
    return " ".join(toks).strip()


def _face_callout(kit_dir, ad):
    """The ICP band as it renders, read off the face source."""
    h = kit_dir / "html" / (ad + ".html")
    if not h.exists():
        cands = list((kit_dir / "html").glob("*.html")) if (kit_dir / "html").is_dir() else []
        h = next((c for c in cands if c.stem.lower() in ad.lower()
                  or ad.lower() in c.stem.lower()), None)
        if h is None:
            return ""
    t = h.read_text(encoding="utf-8", errors="replace")
    for cls in ("callout", "elig", "kicker", "kick", "band", "icp"):
        m = re.search(r'class="[^"]*\b%s\b[^"]*"[^>]*>(.*?)</' % cls, t, re.S | re.I)
        if m:
            txt = re.sub(r"<[^>]+>", " ", m.group(1))
            txt = " ".join(txt.replace("&middot;", "·").split())
            if txt and not re.fullmatch(r"(by\s+)?(skillarbitrage|lawsikho)", txt, re.I):
                return txt[:120]
    return ""


def _value_prop(kit_dir, ad):
    vp = kit_dir / "value_props.md"
    if not vp.exists():
        return ""
    text = vp.read_text(encoding="utf-8", errors="replace")
    idx = re.search(r"(\d+)", ad)
    if not idx:
        return ""
    n = idx.group(1).lstrip("0") or "0"
    m = re.search(r"^## %s\s*$\n(.*?)(?=^## |\Z)" % re.escape(n), text, re.S | re.M)
    if not m:
        return ""
    blk = m.group(1)
    out = []
    for f in ("better_job", "buying_pressure", "pressure"):
        g = re.search(r"%s:\s*(.+?)(?=\n\w+:|\n##|\Z)" % f, blk, re.S)
        if g:
            out.append(" ".join(g.group(1).split())[:200])
    return " | ".join(out)


def _adcopy_icp(kit_dir, ad):
    cf = next(kit_dir.glob("ad_copy*.md"), None)
    if not cf:
        return ""
    text = cf.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^##\s*%s\b.*?\n(.*?)(?=^## |\Z)" % re.escape(ad), text, re.S | re.M | re.I)
    if not m:
        return ""
    g = re.search(r"\*\*ICP:?\*\*\s*(.+)", m.group(1))
    return " ".join(g.group(1).split()) if g else ""


def evidence():
    """One record per shipped ad: everything known that points at its audience."""
    out = []
    for r in corpus.index():
        kd = r["kit_dir"]
        ad = r["ad"]
        stated = _adcopy_icp(kd, ad)
        source = "ad_copy"
        if not stated:
            stated, source = _value_prop(kd, ad), "value_props"
        if not stated:
            stated, source = _face_callout(kd, ad), "face"
        if not stated:
            stated, source = "", "inferred"
        out.append(dict(
            ad=ad, kit=r["kit"], line=line_of(r["kit"]),
            stated=stated, source=source,
            name_phrase=name_to_phrase(ad),
            headline=r["headline"][:120],
            opener=" ".join(r["primary"].split()[:28]),
            approved=bool(r["approved"]), rejected=bool(r["rejected"]),
            why=r.get("why", "")[:200],
            golden=bool(r["golden"]), live=r.get("live") or None,
        ))
    return out


def load_situations():
    """The canonical life-situation vocabulary, occupation stripped off."""
    if not SITUATIONS.exists():
        return []
    return json.loads(SITUATIONS.read_text(encoding="utf-8"))


def load_labels():
    if not LABELS.exists():
        return {}
    return json.loads(LABELS.read_text(encoding="utf-8"))


def index():
    """Evidence joined to the committed normalised labels."""
    labels = load_labels()
    rows = []
    for e in evidence():
        lab = labels.get(e["ad"]) or labels.get(e["ad"].lower()) or {}
        e["icp"] = lab.get("icp") or e["stated"] or e["name_phrase"]
        e["archetype"] = lab.get("archetype", "")
        e["note"] = lab.get("note", "")
        e["labelled"] = bool(lab)
        e["approved"] = _really_approved(e)
        rows.append(e)
    return rows


# An in-house APPROVED label is not an approval. Ramanuj, 31 Aug 2026: "ignore the
# ones that i approved, they were finally not approved. only the ones ramanuj
# approved became the final ads." `adkit/golden.py` excludes the Section A pairs
# for exactly this reason; the ICP index has to agree with it or its verdict
# column overstates. These kits keep their ICPs -- who an ad was aimed at is still
# real evidence -- but they do not get to say "approved".
NOT_FINAL = re.compile(r"contentwriting_sectiona", re.I)


def _really_approved(row):
    return bool(row["approved"]) and not NOT_FINAL.search(row["kit"])


def _cost(e):
    lv = e.get("live") or {}
    for k in ("cpl", "cpp", "cost"):
        if lv.get(k):
            return lv[k]
    return None


def _dedupe(rows):
    """Collapse to distinct audiences per product line, keeping the best evidence."""
    best = {}
    for r in rows:
        key = (r["line"], re.sub(r"[^a-z0-9 ]", "", r["icp"].lower()).strip())
        cur = best.get(key)
        rank = (bool(_cost(r)), r["golden"], r["approved"], not r["rejected"])
        if cur is None or rank > cur["_rank"]:
            r = dict(r, _rank=rank, _n=(cur or {}).get("_n", 0) + 1)
            best[key] = r
        else:
            cur["_n"] += 1
    return sorted(best.values(), key=lambda r: (r["line"], r["archetype"], r["icp"].lower()))


def report():
    """Regenerate SOP/ICP_INDEX.md — the knowledge base."""
    rows = index()
    uniq = _dedupe(rows)
    by_arch = {}
    for r in rows:
        by_arch.setdefault(r["archetype"] or "?", []).append(r)

    out = []
    w = out.append
    w("# The ICP index — every audience this account has pointed an ad at")
    w("")
    w("**Generated. Do not hand-edit — run `python -m adkit.icp --report`.**")
    w("")
    w("%d shipped ads across %d product lines, reduced to **%d distinct audiences**, "
      "each carrying its archetype, its verdict, and its live cost per result where one "
      "exists." % (len(rows), len({r['line'] for r in rows}), len(uniq)))
    w("")
    w("## Why this file exists")
    w("")
    w("A blind test on 31 Aug 2026 ran the documented ICP method against three product")
    w("lines with no repo access. It found ~85% of the live audiences on Independent")
    w("Director and ~71% on Content Writing — both occupation-heavy lines — but only")
    w("**~32% on Women Remote**, whose live audiences are life situations. It also")
    w("re-proposed a practising-credential ICP that had already killed three kits.")
    w("")
    w("The method generates occupations well. It is blind to **life situations** and to")
    w("**tail disciplines**, and it has no memory of what has been rejected. Those are")
    w("evidence problems, not instruction problems, which is what this index supplies.")
    w("")
    w("**Read §2 (the situation vocabulary) and §4 (what has already failed) before")
    w("writing an ICP list.** Those two sections are the ones the method cannot generate.")
    w("")
    w("**What \"approved\" means here.** Only Ramanuj's approvals count. Ramanuj, 31 Aug")
    w("2026: *\"ignore the ones that i approved, they were finally not approved. only the")
    w("ones ramanuj approved became the final ads.\"* The 24 `ContentWriting_SectionA` ads")
    w("carry an in-house APPROVED label and are excluded from the verdict column for that")
    w("reason, matching `adkit/golden.py`. Their **audiences** are still indexed — who an")
    w("ad was aimed at is real evidence either way — they simply do not get to say")
    w("approved. A blank verdict means unknown, not bad: most ads were never given budget.")
    w("")

    counts = {k: len(v) for k, v in sorted(by_arch.items())}
    w("## 1. The shape of what has been built")
    w("")
    w("| Archetype | | Ads | Index (1.00 = par) |")
    w("|---|---|---|---|")
    for k in ("A", "B", "C", "D", "E", "?"):
        if k in counts:
            w("| **%s** | %s | %d | %s |" % (
                k, ARCHETYPES.get(k, "unlabelled"), counts[k],
                ("%.2f" % INDEX[k]) if k in INDEX else "-"))
    w("")
    nD = counts.get("D", 0) + counts.get("E", 0)
    if nD:
        w("**%d of %d ads (%.0f%%) are D or E** — device-led or a broad population. Those "
          "index 1.15 to 1.22 against a par of 1.00, so a meaningful share of everything "
          "ever built here was aimed at nobody in particular." % (
              nD, len(rows), 100.0 * nD / len(rows)))
        w("")

    sits = load_situations()
    lines = sorted({r["line"] for r in rows if r["line"] != "other"})
    w("## 2. The situation vocabulary — %d canonical life situations" % len(sits))
    w("")
    w("**This is the section the method cannot produce from first principles**, and the")
    w("one to read before writing an ICP list. These are every life situation this account")
    w("has pointed an ad at, with the occupation stripped off: 88 shipped phrasings")
    w("collapse to %d situations, because the same situation keeps being reused with a" % len(sits))
    w("different profession glued to the front (*lawyers* / *M.Sc holders* / *mothers*")
    w("restarting after a career break are one situation, not three).")
    w("")
    w("**They travel across product lines far better than occupations do.** That is what")
    w("makes §2.1 useful: a situation proven on one line is a candidate for every other.")
    w("")
    for s in sits:
        w("**%s** — used on: %s" % (s["situation"], ", ".join(s["lines_used"]) or "-"))
        w("")
        w("> %s" % s["definition"])
        w(">")
        w("> **Pressure:** %s" % s["pressure"])
        w("")

    w("### 2.1 Coverage — which situations have never been tried on which line")
    w("")
    w("`+` means an ad has run for that situation on that line. A blank is an untested")
    w("combination, and the cheapest place to look for the next ICP: the situation is")
    w("already proven to be a real audience, it has simply never been pointed at this")
    w("offer. Check the offer genuinely fits before building — not every pairing makes")
    w("sense, and a situation with no plausible route to the product is still a no.")
    w("")
    w("| Situation | " + " | ".join(l.replace("-", " ") for l in lines) + " |")
    w("|---" * (len(lines) + 1) + "|")
    for s in sits:
        used = set(s["lines_used"])
        w("| %s | %s |" % (s["situation"],
                           " | ".join("+" if l in used else "" for l in lines)))
    w("")
    gaps = sum(len(lines) - len(set(s["lines_used"])) for s in sits)
    w("**%d untested situation-by-line combinations.** Most are wrong for their offer; the"
      % gaps)
    w("point is that the list of candidates is finite, written down, and no longer has to")
    w("be re-invented from scratch every wave.")
    w("")

    w("## 3. Occupations and disciplines (archetype A)")
    w("")
    w("Grouped by line. **Split an occupation at the degree people actually hold**, not at")
    w("the sector — that rule is why `semicon_vlsi` and `agri_foodsci` beat a generic")
    w("science ICP by 1.5x to 2.4x.")
    w("")
    line = None
    for r in [x for x in uniq if x["archetype"] == "A"]:
        if r["line"] != line:
            line = r["line"]
            w("")
            w("**%s**" % line)
            w("")
            w("| Occupation | Verdict | Live |")
            w("|---|---|---|")
        w("| %s | %s | %s |" % (r["icp"], _verdict_word(r), _cost_word(r)))
    w("")

    rej = [r for r in rows if r["rejected"]]
    w("## 4. What has already failed — read before proposing anything")
    w("")
    if rej:
        w("| Audience | Line | Why |")
        w("|---|---|---|")
        for r in sorted(rej, key=lambda r: r["line"]):
            w("| %s | %s | %s |" % (r["icp"], r["line"], (r["why"] or "-")[:120]))
        w("")
    w("**The standing rule this account paid three kits to learn:** a *practising")
    w("professional credential* cannot be the ICP for a general remote-work product. A")
    w("dietitian does not want to become a dietitian's assistant. Use the credential for")
    w("targeting and for landing-page proof; keep the ad's identity band a **situation**.")
    w("")

    w("## 5. Priced audiences — the only ones that settle an argument")
    w("")
    priced = [r for r in uniq if _cost(r)]
    if priced:
        w("| Audience | Line | Archetype | Live |")
        w("|---|---|---|---|")
        for r in sorted(priced, key=lambda r: _cost_num(r)):
            w("| %s | %s | %s | %s |" % (r["icp"], r["line"], r["archetype"], _cost_word(r)))
    else:
        w("_No audience in the index currently carries a live cost._")
    w("")
    belief = re.compile(r"\b(think|thinks|believe|believes|not for (her|them)|too late)\b", re.I)
    obj = [r for r in rows if r["archetype"] == "C"
           and (belief.search(r["icp"]) or "objection" in r["note"].lower()
                or "belief" in r["note"].lower())]
    if obj:
        w("## 6. An open question: objection-led ICPs")
        w("")
        w("The archetype table calls anything that is neither an occupation nor a situation")
        w("a **C**, indexes it at 1.05, and says rewrite. But this account has shipped ads")
        w("whose audience is neither — it is a *belief the reader holds about herself*:")
        w("")
        for icp_, ad_, kit_ in sorted({(r["icp"], r["ad"], r["kit"]) for r in obj}):
            w("- *%s* — `%s` (%s)" % (icp_, ad_, kit_.split("\\")[0].split("/")[0]))
        w("")
        w("These are not sloppiness. `W4_not_too_late` and `W6_whatsapp_level` are cells of")
        w("`WomenRemote_Wave4_SEND_THIS`, the founder's own kit, which gated **28 of 28")
        w("ACCEPT**; `X2_myth_truth` shipped in the approved Wave 6. So the taxonomy has no")
        w("name for a pattern that keeps passing review: the ICP is an **objection**, and")
        w("the ad exists to answer it. It behaves like a situation — she can point at the")
        w("belief — but carries no occupation and no life circumstance.")
        w("")
        w("**Do not \"fix\" these by rewriting them into an A or a B.** That is what the")
        w("table would tell you to do, and it would delete a working pattern. Treat")
        w("objection-led as a fourth buildable shape, and note the honest limit: **none of")
        w("them carries a live cost**, so the case for it is approval, not money. If one")
        w("ever gets budget, price it before promoting the pattern.")
        w("")

    w("---")
    w("")
    w("Regenerate with `python -m adkit.icp --report`. Labels live in")
    w("`adkit/data/icp_labels.json` and are committed, so the index is reviewable and")
    w("stable rather than re-derived differently on every run.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    return len(rows), len(uniq)


def _verdict_word(r):
    if r["golden"]:
        return "GOLDEN"
    if r["rejected"]:
        return "rejected"
    if r["approved"]:
        return "approved"
    return "-"


def _cost_num(r):
    c = _cost(r)
    try:
        return float(re.sub(r"[^\d.]", "", str(c)))
    except (TypeError, ValueError):
        return 1e9


def _cost_word(r):
    c = _cost(r)
    return ("Rs %s" % c) if c else "-"


def main(argv):
    args = argv[1:]

    def flag(f):
        return f in args

    if flag("--unlabelled"):
        rows = [r for r in index() if not r["labelled"]]
        if not rows:
            print("\n  every indexed ad carries an ICP label. Nothing to do.\n")
            return 0
        print("\n  %d ad(s) need an ICP label before --report is current:\n" % len(rows))
        for r in rows:
            print("   %-30s %-22s %s" % (r["ad"][:30], r["line"], r["headline"][:44]))
        print("\n  Label them into adkit/data/icp_labels.json as")
        print('   "<ad>": {"icp": "<audience, 3-8 words>", '
              '"archetype": "A|B|C|D|E", "note": ""}')
        print("  then re-run --report. An ICP label is a judgement, not a regex:")
        print("  read the headline and the opener, and write who the ad is FOR.\n")
        return 0

    if flag("--report"):
        n, u = report()
        print("wrote %s: %d ads -> %d distinct audiences"
              % (REPORT.relative_to(ROOT), n, u))
        return 0

    if flag("--extract"):
        DATA.mkdir(parents=True, exist_ok=True)
        ev = evidence()
        RAW.write_text(json.dumps(ev, indent=1, ensure_ascii=False), encoding="utf-8")
        stated = sum(1 for e in ev if e["source"] != "inferred")
        print("wrote %s: %d ads, %d with a stated ICP, %d to label"
              % (RAW.relative_to(ROOT), len(ev), stated, len(ev) - stated))
        return 0

    rows = index()
    if flag("--line"):
        want = args[args.index("--line") + 1]
        rows = [r for r in rows if want in r["line"]]
    if flag("--rejected"):
        rows = [r for r in rows if r["rejected"]]
    if flag("--situations"):
        rows = [r for r in rows if r["archetype"] == "B"]

    seen, uniq = set(), []
    for r in sorted(rows, key=lambda r: (r["line"], r["archetype"], r["icp"].lower())):
        key = (r["line"], r["icp"].lower())
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)

    print("\n  %d ads -> %d distinct audiences\n" % (len(rows), len(uniq)))
    line = None
    for r in uniq:
        if r["line"] != line:
            line = r["line"]
            print("\n  == %s" % line.upper())
        mark = "GOLD" if r["golden"] else ("ok" if r["approved"] else
                                           ("REJ" if r["rejected"] else "-"))
        cost = _cost(r)
        print("   %-1s %-4s %-46s %-9s %s" % (
            r["archetype"] or "?", mark, r["icp"][:46],
            ("Rs%s" % cost) if cost else "", r["ad"][:24]))
        if r["rejected"] and r["why"]:
            print("        why: %s" % r["why"][:100])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
