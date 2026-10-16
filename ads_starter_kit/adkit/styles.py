#!/usr/bin/env python3
"""The design styles that have gone live, so a wave has variety in it.

WHY THIS EXISTS (31 Aug 2026). Asked for directly: "all of the different design
styles that have gone live, what have performed well so that there is a variety in
the ads designed." Nothing in the repo answered it. `GOLDEN` lists faces, the Meta
pull lists costs, and the kit generators describe their devices in their own
docstrings -- three vocabularies that were never joined, so every kit reinvented
its device list and several shipped ten faces in one shape.

WHERE THE TAXONOMY COMES FROM. It is read off the work, not invented:

  * 27 device names written by the kit generators themselves, in their docstrings
    ("a comparison table, a negotiation sheet and a floor plan"; "board minutes, a
    two-column list, a dialogue"; "ONE number in a plain card").
  * The six approved hook types in AD_CREATION_DIRECTOR.md section 4, which name
    devices too -- speech bubble, interrogated list, overheard dialogue, quoted-self
    mirror, data/quadrant.
  * `new ad types/candidates_*.md`, the formats that were explored deliberately.

HOW HONEST THE PERFORMANCE COLUMN IS. Thin, and labelled as such on every row.
Only about a dozen live ads can be matched to a face whose style is classifiable:
the Meta pull names ads the way the media buyer named them, and most kits ship
faces under different names. `CPL_WINNERS_31Aug2026.md` carries the same caveat --
"Format labels are inferred from ad names". So this file reports:

  * what is MEASURED, for the two styles where it is: the pay chart at index 2.34
    replicated across three product lines, and toon/chat at 1.22.
  * the individual priced ads it can place, with their real cost.
  * `-` everywhere else. An unpriced style is not a bad style; it is one nobody
    has spent enough on to have an opinion about, and this file will not invent one.

    python -m adkit.styles                 the catalogue
    python -m adkit.styles --kit <folder>  the style mix of one kit, and whether
                                           it is shipping the same shape ten times
    python -m adkit.styles --write         regenerate SOP/10_DESIGN_STYLES.md
"""
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent

# (style, regex over the face name + kit name, one-line note)
# Ordered: the first match wins, so put the specific before the generic.
STYLES = [
    ("pay chart", r"paychart|pay_chart|salary_?(chart|ladder|table)",
     "A salary figure as the hero. MEASURED WORST IN THE ACCOUNT, index 2.34 "
     "against a par of 1.00, replicated across three product lines. Also banned "
     "from the face on compliance grounds. Do not build one."),
    ("toon / cartoon", r"toon|cartoon|comic|duocartoon",
     "Drawn characters, usually two, with a caption. Format index 1.22. The "
     "account's highest-CTR ad is one of these and it costs more than its "
     "campaign median - the clearest case that CTR does not defend an ad."),
    ("chat / messaging", r"\bchat\b|whatsapp|dm_|inbox_|message",
     "A messaging thread as the artefact. Indexes with toon at 1.22. Reads fast, "
     "converts unremarkably."),
    ("notice / letter", r"notice|letter|memo|circular",
     "An official-looking notice. The shape behind us22_notice_fifties (Rs 29.65) "
     "and us25/us24 - three of the four cheapest lead ads in the account."),
    ("quote card", r"quote|said|voice|bubble|talk",
     "The reader's own sentence, set large. Hook type 2 and 5. mh01_corridor is "
     "the GOLDEN reference."),
    ("comparison table", r"compar|versus|_vs_|two_?column|both_ways|duo\b",
     "Two columns the reader can put herself in. Hook type 3."),
    # Added 18 Sep 2026 with the Corporate Finance 17-19 Oct wave, built from a DTC supplement
    # static. Its nineteen faces matched nothing and reported as "no device". No live cost yet.
    ("venn / overlap", r"venn|overlap|intersect|both_?circles",
     "Two outlined circles: the work the reader does now in one, the work the camp adds in the "
     "other, and the offer in the intersection. Only honest when the two sides really are "
     "separate today. No live cost yet, so judge it inside its own campaign."),
    # Added 21 Sep 2026 with the Corporate Finance 17-19 Oct notify wave, built from a DTC
    # sunscreen static. Replaced `venn`, which was a category error, and `alert`, which
    # carried almost none of the information. No live cost yet.
    ("notification card", r"notify|notification|alert|push_?card|lock_?screen",
     "One white notification card on a flat ground, with two more peeking behind it: app row, "
     "the ICP as a question, qualifier chips, the offer, the definition, an attachment card "
     "carrying the take-aways, and ONE filled action. Meta disallows creative that imitates "
     "platform UI misleadingly, so no status bar, no platform glyphs, no fake close control, "
     "and the only control-looking element is the real CTA. No live cost yet."),
    # Added 21 Sep 2026 with the LawSikho Data Protection 17-19 Oct wave, built from an AG1
    # "incoming call" static. The idea: a better opportunity is calling. No live cost yet.
    ("incoming call", r"(^|_)call(_|$)|incoming|is_?calling|ringing",
     "A dark accent-to-ink call screen, everything centred: the ICP question with the "
     "reader's title in full white, qualifier chips, a brand monogram as the caller, the "
     "winning headline as the caller's name over 'is calling...', a white caller card "
     "carrying the definition and take-aways, and ONE slide-to-act pill whose label is the "
     "real CTA. Behind SOP/10: brand colours, an arrow knob not a phone glyph, no status "
     "bar, no Decline. First face blind-read 3/3 against a 2/3 control floor. No live "
     "cost yet."),
    ("chart / quadrant", r"chart|quadrant|graph|percentile|curve|axis",
     "A simple plot with her current and target bucket both visible. Hook type 6. "
     "Numeric axis ticks MUST cite a source on the face."),
    ("duty / rota / checklist", r"duty|rota|checklist|task_?list|dutychart",
     "A list of the actual work, as an artefact. SQE_DutyChart is the reference."),
    ("board / minutes / agenda", r"minutes|agenda|board_?(paper|pack)|needs_?board",
     "A document from the room she wants to be in."),
    ("receipt / invoice / form", r"receipt|invoice|form|payslip|payout",
     "A financial artefact. Carries money without putting a figure in the headline."),
    ("calendar / timeline", r"calendar|timeline|schedule|exam_?window|dayone|day_?1",
     "Time as the device. CAUTION: calendar and exam-window motifs are the "
     "device-led archetype D, which indexes 1.22 and is the most expensive "
     "archetype measured. Name the reader, never the date."),
    ("ladder / progression", r"ladder|progress|step_?up|rung|route",
     "Where the work leads, in stages. hoc_02_ladder is the GOLDEN reference."),
    ("collage / sticker", r"collage|sticker|scrap|pastel",
     "Assembled fragments. Built for Content Writing wave 6."),
    ("photo-led", r"photo|portrait|scene|corridor|office|chamber|canteen|shot",
     "A real photograph as the hero. Most approved ads in this account carry NO "
     "photograph - the director says default to a device instead."),
    ("poster / type-only", r"poster|slab|headline_?only|type_?only|typographic",
     "Type and colour, no artefact. The RID poster chassis."),
    ("carousel", r"carousel|swipe|slide|_0[1-9]_of_",
     "Multi-frame. Counted as one cell."),
    # Added 1 Sep 2026 with adkit/layouts_social.py. Neither carries a live cost.
    ("object + paper slip", r"fortune|slip_?card|cookie",
     "A drawn object holding a paper slip that carries the promise, under a "
     "sans-plus-script headline. Reference set 1 Sep 2026, sheet 2. No live "
     "cost yet."),
    ("pixel art", r"pixel|8bit|8_?bit|arcade|retro_?game",
     "A pixel-grid device on a flat bright ground. Reference set 1 Sep 2026, "
     "sheet 5. No live cost yet."),
]

MEASURED = {
    "pay chart": ("2.34", "worst in the account, replicated 3 product lines"),
    "toon / cartoon": ("1.22", "high CTR, unremarkable cost"),
    "chat / messaging": ("1.22", "indexes with toon"),
}


_SRC_CACHE = {}


def _sources():
    """{face stem: html source}. A face's own markup is a better witness to its
    device than its filename, and 37% of faces have one."""
    if _SRC_CACHE:
        return _SRC_CACHE
    for f in ROOT.rglob("*.html"):
        p = f.as_posix()
        if "landing_page" in p or f.name.startswith("lp_") or f.name == "index.html":
            continue
        if "/html/" in p or f.name.startswith("src_"):
            _SRC_CACHE[f.stem.lower().replace("src_", "")] = f
    return _SRC_CACHE


def classify_html(path):
    """Read the device off the markup. Only returns a style it can actually see."""
    try:
        t = path.read_text(encoding="utf-8", errors="replace").lower()
    except OSError:
        return None
    # The borrowed-format layouts are read off their own class names FIRST.
    # Before 1 Sep 2026 the generic `<svg>` branch below caught every one of them
    # and reported "chart / quadrant", because that branch assumes any inline SVG
    # on a face is a plot. It is not: a stick figure and a fortune cookie are
    # both SVG and neither is a chart. Measured on
    # AcademicWriting_Wave2_MediaBuyer_26-28Sep, 11 faces built from 5 distinct
    # skeletons: BEFORE 7 chart / quadrant + 4 unclassified, and a false 60%
    # single-style WARNING. AFTER 5 toon / 2 chat / 2 object+slip / 2 pixel, no
    # warning. Re-checked on IndependentDirector_Wave1 (7 photo-led, 2
    # unclassified, 1 chart), GlobalPatent_Wave1 and AcademicWriting_Wave1: all
    # three unchanged.
    if re.search(r'class="pix"|class="[^"]*pix', t):
        return "pixel art"
    if re.search(r'class="half|class="[^"]*slip', t):
        return "object + paper slip"
    if re.search(r'class="askrow|class="inbar', t):
        return "chat / messaging"
    if re.search(r'class="[^"]*fig|class="panels', t):
        return "toon / cartoon"
    if re.search(r'class="[^"]*(bubble|msg|chatline|thread)', t):
        return "chat / messaging"
    if re.search(r"<svg", t):
        return "chart / quadrant"
    if re.search(r'class="[^"]*(quote|said|voice)', t):
        return "quote card"
    # a repeated row class 4+ times is a table or a list artefact
    for cls in re.findall(r'class="([a-z][a-z0-9_-]*)"', t):
        if t.count('class="%s"' % cls) >= 4 and cls not in (
                "tk", "chip", "pill", "tag", "k", "row"):
            return "duty / rota / checklist"
    if re.search(r"<img[^>]+photos/", t):
        return "photo-led"
    if re.search(r"<img", t):
        return "collage / sticker"
    return None


def classify(name, kit="", use_html=True):
    hay = ("%s %s" % (name, kit)).lower()
    for style, rx, _ in STYLES:
        if re.search(rx, hay):
            return style
    if use_html:
        src = _sources().get(name.lower())
        if src is not None:
            got = classify_html(src)
            if got:
                return got
    return "unclassified"


def faces():
    """Every ad face PNG in the repo, with its kit."""
    out = []
    for f in ROOT.rglob("*.png"):
        p = f.as_posix()
        if "/ads/" not in p or "landing" in p or "__pycache__" in p:
            continue
        try:
            kit = f.relative_to(ROOT).parts[0]
        except ValueError:
            continue
        out.append((f.stem, kit, f.relative_to(ROOT)))
    return out


def priced():
    """{style: [(cost, family, ad name)]} for the few live ads we can place."""
    try:
        from . import corpus, golden
    except Exception:                                   # noqa: BLE001
        return {}
    out = {}
    for e in golden.collect():
        if not e.get("live"):
            continue
        s = classify(e["name"], e.get("source", ""))
        out.setdefault(s, []).append(
            (e["live"]["cost"], e["live"]["family"], e["name"]))
    for v in out.values():
        v.sort()
    return out


def catalogue():
    counts, examples, kits = Counter(), {}, {}
    for stem, kit, rel in faces():
        s = classify(stem, kit)
        counts[s] += 1
        examples.setdefault(s, []).append(rel.as_posix())
        kits.setdefault(s, set()).add(kit)
    return counts, examples, kits


def kit_mix(folder):
    """The style mix inside one kit. Ten faces in one shape is the defect."""
    d = pathlib.Path(folder)
    pngs = sorted((d / "ads").glob("*.png")) if (d / "ads").is_dir() else []
    if not pngs:
        pngs = sorted(d.rglob("ads/*.png"))
    mix = Counter(classify(p.stem, d.name) for p in pngs)
    return len(pngs), mix


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    if "--kit" in argv:
        i = argv.index("--kit")
        folder = argv[i + 1] if len(argv) > i + 1 else "."
        n, mix = kit_mix(folder)
        if not n:
            print("  no ad faces found under %s" % folder)
            return 2
        print("\n  %s - %d faces\n" % (pathlib.Path(folder).name, n))
        for s, c in mix.most_common():
            bar = "#" * c
            print("    %-26s %2d  %s" % (s, c, bar))
        top = mix.most_common(1)[0]
        unclass = mix.get("unclassified", 0)
        print("")
        if top[0] != "unclassified" and top[1] >= max(3, 0.6 * n):
            print("  WARNING  %d of %d faces are the same style (%s). A reader who "
                  "sees\n           several of these ads sees one idea. Vary the device."
                  % (top[1], n, top[0]))
        elif unclass >= 0.6 * n:
            print("  %d of %d faces did not match a known style. Either this kit is "
                  "doing\n  something new - worth adding to STYLES - or the names carry "
                  "no device." % (unclass, n))
        else:
            print("  %d distinct styles across %d faces." % (len(mix), n))
        return 0

    counts, examples, kits = catalogue()
    pr = priced()
    total = sum(counts.values())
    known = total - counts.get("unclassified", 0)
    print("")
    print("  %d ad faces in the repo. %d carry a device signal in their name or their"
          % (total, known))
    print("  markup and are classified below; %d do not. That is a limit of how faces were"
          % counts.get("unclassified", 0))
    print("  named, not a finding about them - do not read the counts as a census. The")
    print("  value here is the CATALOGUE and the examples, not the totals.")
    print("")
    print("  %-26s %5s %6s  %s" % ("style", "faces", "index", "live cost where known"))
    print("  " + "-" * 92)
    for style, _, _note in STYLES:
        n = counts.get(style, 0)
        if not n:
            continue
        idx = MEASURED.get(style, ("-", ""))[0]
        p = pr.get(style, [])
        cost = ", ".join("Rs %.0f %s" % (c, f[:4]) for c, f, _ in p[:3]) or "-"
        print("  %-26s %5d %6s  %s" % (style, n, idx, cost))
    if counts.get("unclassified"):
        print("  %-26s %5d %6s  %s" % ("(no device signal)", counts["unclassified"], "-",
                                       "not a style - unreadable from name or markup"))
    print("")
    print("  index: cost per result normalised to campaign par 1.00. Only two styles")
    print("  have a measured index; the rest print `-` because the Meta pull names ads")
    print("  the way the buyer named them and most faces cannot be matched to a row.")
    print("  An unpriced style is not a bad style - it is one nobody has spent enough")
    print("  on to have an opinion about.")
    if "--write" in argv:
        write_doc(counts, examples, kits, pr)
        print("\n  wrote SOP/10_DESIGN_STYLES.md")
    return 0


def write_doc(counts, examples, kits, pr):
    out = ["""# Design styles that have gone live

**Generated — run `python -m adkit.styles --write`.** The taxonomy is read off the
work: the device names the kit generators write in their own docstrings, the six
approved hook types in `AD_CREATION_DIRECTOR.md` §4, and the formats explored in
`new ad types/`.

**Why this file exists:** so a wave has variety in it. Check a kit with
`python -m adkit.styles --kit <folder>` — it warns when most of the faces are the
same shape, which is the visual version of the landing-page problem in Rule 4b: a
reader who sees several ads from one campaign should not see one idea.

**How honest the index column is.** Only two styles have a measured cost index. The
Meta pull names ads the way the media buyer named them, and most faces cannot be
matched to a row — `CPL_WINNERS_31Aug2026.md` carries the same caveat. `-` means
nobody has spent enough on that style to have an opinion about it. It does not mean
the style is bad, and it must not be quoted as if it did.

**Coverage, stated plainly:** most faces in this repo cannot be classified from
their filename or their markup, so the **Faces** column counts only the ones that
carry a device signal. It is not a census, and the totals should not be quoted as
one. The value of this file is the catalogue and the named examples.

| Style | Faces | Index | Live cost where known |
|---|---|---|---|
"""]
    for style, _, _note in STYLES:
        n = counts.get(style, 0)
        if not n:
            continue
        idx = MEASURED.get(style, ("—", ""))[0]
        p = pr.get(style, [])
        cost = ", ".join("₹%.0f/%s" % (c, f) for c, f, _ in p[:2]) or "—"
        out.append("| %s | %d | %s | %s |\n" % (style, n, idx, cost))
    out.append("\n## What each style is, and when it earns its place\n\n")
    for style, _, note in STYLES:
        n = counts.get(style, 0)
        if not n:
            continue
        ex = examples.get(style, [])[:3]
        out.append("### %s — %d faces, %d kits\n\n%s\n\n"
                   % (style, n, len(kits.get(style, [])), note))
        for e in ex:
            out.append("- `%s`\n" % e)
        out.append("\n")
    out.append("""## The two rules this file exists to serve

1. **Vary the device across a wave.** `python -m adkit.styles --kit <folder>` warns
   when 60% or more of a kit's faces are one style.
2. **Never build a pay chart**, and treat calendar/exam-window motifs as the
   device-led archetype D — 1.22 against par, the most expensive archetype measured.
   If you cannot name who the ad is for before you pick the device, you are building
   a D.
""")
    (ROOT / "SOP" / "10_DESIGN_STYLES.md").write_text("".join(out), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
