#!/usr/bin/env python3
"""Derive GOLDEN from the approved corpus instead of hand-picking it.

Why this exists. GOLDEN was 9 images chosen by hand in August and frozen there.
It is the single most load-bearing artefact in the account -- AD_CREATION_DIRECTOR
§13 says "load these, don't just cite them", and SKILL.md says examples change
what gets written where rules only argue with what is already written. Freezing it
in August means every kit since has been imitating a nine-image snapshot while the
repo accumulated hundreds of approved faces and a full Meta pull.

WHAT COUNTS AS GOLDEN HERE. ONLY WHAT RAMANUJ APPROVED. Corrected 31 Aug 2026,
and it is the whole selection rule:

    "ignore the ones that i approved, they were finally not approved.
     only the ones ramanuj approved became the final ads"

So an in-house approval is not evidence of anything and does not admit a face to
this set. `ContentWriting_SectionA_APPROVED_29-31Aug.zip` was a source here for
exactly one build and was removed: CAMPAIGN_MAP.md records its verdicts as a bare
"APPROVED: pairs 01, 02, ..." with no attribution, those 17 pairs were approved
in-house, and they did not become final ads. `APPROVED/` stays, because
CAMPAIGN_MAP.md attributes it explicitly -- "Ramanuj-approved batches ...
Everything under APPROVED/ has passed Ramanuj."

Two kinds of source survive:

  1. `APPROVED/` -- the batches that passed Ramanuj.

  2. The faces Ramanuj made himself, which were never generated in this repo:
     `RID_BC_8Aug_Ads (1)` and `Accounting_BC_8Aug_Ads (1)` -- the kits that ran
     on the 8 Aug instances. These matter more than their approval status: they
     hold the cheapest ads in the whole account. `banker` at Rs 60.42 is the
     best Independent Director ad ever run, and four of the six cheapest US
     Accounting ads by cost per lead are in the Accounting_BC creatives.

EXCLUDED, deliberately, and each for a stated reason -- see EXCLUDED below. They
are listed in the output rather than silently dropped, because "why is X not in
GOLDEN" should be answerable without reading this file.

The index carries live cost per lead or purchase where the Meta pull knows it, so
"what does good look like" and "what was cheap" are the same table rather than two.

    python -m adkit.golden            rebuild GOLDEN/GOLDEN.md
    python -m adkit.golden --dry      show what would be included, write nothing
"""
import pathlib
import re
import shutil
import sys
import zipfile

from . import corpus as _corpus
from . import verdicts as _verdicts

ROOT = pathlib.Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "GOLDEN"
NOTES = GOLDEN / "GOLDEN_NOTES.md"

# (label, path, provenance) -- provenance is printed against every face
SOURCES = [
    # Listed FIRST so it claims its own faces before the APPROVED sweep does --
    # dedup keeps the first source that names a face. These are images Ramanuj
    # sent rather than anything built here, and their filenames carry no ad name,
    # so they are worth labelling rather than burying in the batch folder.
    ("Ramanuj's own, sent 29 Aug", "APPROVED/WhatsApp Unknown 2026-08-31 at 1.03.57 PM",
     "ramanuj"),
    ("Ramanuj-approved batches", "APPROVED", "approved"),
    ("Ramanuj's own, Independent Director 8 Aug", "RID_BC_8Aug_Ads (1)", "ramanuj"),
    ("Ramanuj's own, US Accounting 8 Aug", "Accounting_BC_8Aug_Ads (1)", "ramanuj"),
]

EXCLUDED = [
    ("reference_images/", 138,
     "Reference MATERIAL, not our ads -- WhatsApp photos and meme templates used as "
     "donors. Keep using them (see the memory note on cropping real reference images); "
     "they are not examples of an approved face."),
    ("ContentWriting_SectionA_APPROVED_29-31Aug.zip", 18,
     "Approved IN-HOUSE, not by Ramanuj, and those pairs did not become final ads. "
     "An in-house APPROVED label is not evidence and never admits a face here."),
]

IMG = (".png", ".jpg", ".jpeg")
# carousel frames, contact sheets and review grids are not single faces to imitate
# 22 Sep 2026: anchored, as in blind_reader._candidates - "review" anywhere in a name dropped
# a real face (05_woman_phd_litreview) from the blind read. Match sheets by prefix or suffix only.
SKIP_NAME = re.compile(r"^(index|contact|review|sheet|thumbs?|grid)(_|$)|_(sheet|grid|thumbs?)$", re.I)


def _faces_in(path):
    """Every ad face under a source. Zips are read without extracting."""
    p = ROOT / path
    out = []
    if not p.exists():
        return out
    if p.suffix == ".zip":
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.lower().endswith(IMG) and "/ads/" in n.replace("\\", "/"):
                    out.append((pathlib.PurePosixPath(n).stem, "%s!%s" % (path, n)))
        return out
    for f in sorted(p.rglob("*")):
        if f.suffix.lower() not in IMG:
            continue
        rel = f.relative_to(ROOT).as_posix()
        # only faces, not photos/ donors or landing-page assets
        if "/photos/" in rel or "/reference" in rel:
            continue
        if SKIP_NAME.search(f.stem):
            continue
        out.append((f.stem, rel))
    return out


def collect():
    live = _corpus.load_live()
    by_name, by_number = _verdicts.load()
    copy_by_ad = {}
    for row in _corpus.index():
        copy_by_ad.setdefault(row["ad"].lower(), row)

    entries, seen = [], set()
    for label, path, prov in SOURCES:
        for stem, rel in _faces_in(path):
            key = stem.lower()
            if key in seen:
                continue
            seen.add(key)
            c = copy_by_ad.get(key)
            v = _verdicts.for_ad(stem, path, by_name, by_number)
            if v and v["verdict"] == _verdicts.REJECTED:
                continue          # a recorded reject never belongs in GOLDEN
            entries.append(dict(
                name=stem, path=rel, source=label, provenance=prov,
                live=_corpus.match_live(stem, live),
                headline=(c or {}).get("headline", ""),
                primary=(c or {}).get("primary", "")))
    return entries


def _cost(e):
    if not e["live"]:
        return None
    fam = "lead" if e["live"]["family"] == "lead" else "purchase"
    return (e["live"]["cost"], fam)


def preserved_notes():
    """The hand-written WHY IT PASSED blocks are earned judgement and are never
    regenerated. They are moved to GOLDEN_NOTES.md the first time this runs, and
    linked from the generated index afterwards."""
    if NOTES.exists():
        return NOTES.read_text(encoding="utf-8")
    old = GOLDEN / "GOLDEN.md"
    if not old.exists():
        return ""
    text = old.read_text(encoding="utf-8")
    i = text.find("### GOLD-01")
    body = text[i:] if i > 0 else text
    NOTES.write_text(
        "# GOLDEN notes — the hand-written WHY IT PASSED entries\n\n"
        "Written by hand in August 2026 and **kept verbatim**. `GOLDEN.md` is now\n"
        "generated (`python -m adkit.golden`); this file is not, because these are\n"
        "judgements no script can re-derive. Add to it by hand when a new face is\n"
        "worth explaining rather than just listing.\n\n---\n\n" + body,
        encoding="utf-8")
    return body


def render(entries):
    priced = sorted([e for e in entries if _cost(e)], key=lambda e: _cost(e)[0])
    leads = [e for e in priced if _cost(e)[1] == "lead"][:12]
    buys = [e for e in priced if _cost(e)[1] == "purchase"][:12]

    def row(e):
        c = _cost(e)
        return "| `%s` | %s | %s | %s |" % (
            e["name"][:40], e["source"], "Rs %.0f" % c[0] if c else "—",
            (e["headline"] or "")[:60] or "—")

    n_ram = sum(1 for e in entries if e["provenance"] == "ramanuj")
    out = ["""# GOLDEN — the approved faces, derived from the corpus

**Generated. Do not hand-edit — run `python -m adkit.golden` instead.** The
hand-written WHY IT PASSED entries live in
[GOLDEN_NOTES.md](GOLDEN_NOTES.md) and are never regenerated.

This is an examples document, not a rules document. Rules stop the worst output;
examples change what gets written. Copy the **structure and simplicity level**,
never the content — the product, ICP and numbers change every time.

**Load two or three faces, not the whole set.** The point is a shape to imitate,
not a survey. Start with the priced tables below: those are the faces that were
both approved and cheap, which is the only combination that settles an argument.

""",
           "**%d faces**, from %d sources. **%d are Ramanuj's own**, built outside "
           "this repo.\n\n" % (len(entries), len(SOURCES), n_ram),
           "## The cheapest approved faces — free camps, cost per lead\n\n",
           "| Face | Source | CPL | Headline |\n|---|---|---|---|\n"]
    out += [row(e) + "\n" for e in leads]
    out.append("\n## The cheapest approved faces — paid camps, cost per purchase\n\n")
    out.append("| Face | Source | CPP | Headline |\n|---|---|---|---|\n")
    out += [row(e) + "\n" for e in buys]
    out.append("""
**Cost per lead and cost per purchase are different families and are never
compared.** A Rs 30 lead and a Rs 98 purchase are not the same number. Meta reports
spend net of GST; gross up 18% before judging against `SOP/02`.

**An unpriced face is not a worse face.** Most of the set below never got enough
budget to have an opinion attached. Approval and cost are two separate columns and
this file keeps them separate.

## Every approved face, by source

""")
    for label, path, prov in SOURCES:
        mine = [e for e in entries if e["source"] == label]
        if not mine:
            continue
        tag = " · **Ramanuj's own, not generated here**" if prov == "ramanuj" else ""
        out.append("### %s — %d faces%s\n\n`%s`\n\n" % (label, len(mine), tag, path))
        for e in sorted(mine, key=lambda x: x["name"]):
            c = _cost(e)
            bits = [e["path"]]
            if c:
                bits.append("**Rs %.0f per %s**" % (c[0], c[1]))
            if e["headline"]:
                bits.append('"%s"' % e["headline"][:70])
            out.append("- `%s` — %s\n" % (e["name"], " · ".join(bits)))
        out.append("\n")

    out.append("## Deliberately not in GOLDEN\n\n")
    for name, n, why in EXCLUDED:
        out.append("- **`%s`** (%d images) — %s\n" % (name, n, why))
    out.append("""
## How this is built

`python -m adkit.golden`. Sources are declared in `adkit/golden.py`; add one there
rather than copying images into this folder. A face with a REJECTED verdict in
`CAMPAIGN_MAP.md` is dropped automatically, so approving or rejecting work in that
file is enough to change this set.

Live cost comes from the Meta pull via `adkit.corpus`, matched on ad name and
deliberately conservative — a face shows no cost rather than someone else's.
""")
    return "".join(out)


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    entries = collect()
    priced = [e for e in entries if e["live"]]
    print("\n  %d faces collected" % len(entries))
    for label, path, prov in SOURCES:
        n = sum(1 for e in entries if e["source"] == label)
        print("    %-46s %3d  %s" % (label[:46], n,
                                     "(Ramanuj's own)" if prov == "ramanuj" else ""))
    print("  %d carry a live cost" % len(priced))
    for name, n, _ in EXCLUDED:
        print("    excluded: %-30s %d images" % (name, n))
    if "--dry" in argv:
        print("\n  --dry: nothing written.")
        return 0
    GOLDEN.mkdir(exist_ok=True)
    preserved_notes()
    (GOLDEN / "GOLDEN.md").write_text(render(entries), encoding="utf-8")
    print("\n  wrote GOLDEN/GOLDEN.md and preserved GOLDEN/GOLDEN_NOTES.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
