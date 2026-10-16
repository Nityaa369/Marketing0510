#!/usr/bin/env python3
"""Rendered-creative QA — catches what a copy linter cannot see.
Usage: python3 ads/ad_render_qa.py <creative.png> [...]

WHY THIS EXISTS (26 Jul 2026). Four separate times in one session a call-out was wrong in the
RENDER while the copy was fine: `<br>` breaks silently re-wrapped and orphaned a word, and
`white-space:nowrap` let an oversized font run straight off the right edge (76px needed 1028px
of a 924px usable width — the last two letters were simply gone). ads/ad_lint.py reads the HTML
and cannot see any of that. Ramanuj caught all four; this checker exists so he does not have to.

Checks, all from the pixels:
  E1 FAIL  content clipped at a canvas edge -> something overflowed and was cut off
  E2 FAIL  a critical element sits outside the 1:1 centre crop (y 135..1215 of 1350)
  E3 WARN  large dead band (>=180px) of pure background above the bottom element ->
           top-heavy composition, call-out drifts out of the optical centre
  E4 WARN  canvas is not 1080x1350 (Meta 4:5)

NOT DETECTABLE FROM PIXELS — do this in the browser instead. Text clipped at the CALL-OUT BOX's
own inner edge (as opposed to the canvas edge) cannot be found reliably by colour heuristics: an
attempt on 26 Jul flagged three good creatives and still missed the bad one, so it was removed
rather than shipped as noise. The reliable check is a measurement, via the puppeteer MCP:

    const card=document.querySelector('.card'), co=document.querySelector('.callout');
    const cs=getComputedStyle(card);
    const usable=card.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
    const r=document.createRange(); r.selectNodeContents(co);
    const widest=Math.max(...[...r.getClientRects()].map(x=>x.width));
    const pad=parseFloat(getComputedStyle(co).paddingLeft)*2;
    ({widest, usable, fits: widest+pad<=usable})

Run it after ANY change to call-out text or font-size when the call-out uses white-space:nowrap.
It is how the 76px overflow (needed 1028px of 924px) was found and fixed at 66px.

No dependencies beyond Pillow.
"""
import sys
try:
    from PIL import Image
except ImportError:
    print("Pillow not installed — pip3 install --user Pillow"); sys.exit(2)

W, H = 1080, 1350
CROP_TOP, CROP_BOT = 135, 1215          # Meta's 1:1 centre crop of a 4:5 canvas
TOL = 18                                 # per-channel tolerance vs background


def near(a, b, tol=TOL):
    return all(abs(x - y) <= tol for x, y in zip(a[:3], b[:3]))


def qa(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    issues = []
    if (w, h) != (W, H):
        issues.append(("WARN", "E4", f"canvas is {w}x{h}, not {W}x{H} (Meta 4:5)"))
    px = im.load()
    bg = px[3, 3]                        # top-left corner is always page background

    def row_has_ink(y):
        return any(not near(px[x, y], bg) for x in range(0, w, 3))

    def col_has_ink(x):
        return any(not near(px[x, y], bg) for y in range(0, h, 3))

    # E1 — ink touching an edge means content ran off and was cut
    for x, side in ((0, "left"), (w - 1, "right")):
        if col_has_ink(x):
            issues.append(("FAIL", "E1", f"content is clipped at the {side} edge — an element "
                                         "overflowed the canvas. If the call-out uses white-space:nowrap, "
                                         "its font-size is too large for the line."))
    for y, side in ((0, "top"), (h - 1, "bottom")):
        if row_has_ink(y):
            issues.append(("FAIL", "E1", f"content is clipped at the {side} edge — an element overflowed the canvas"))

    # E2 — anything above/below the 1:1 crop band is lost in square placements
    for y in range(0, min(CROP_TOP, h), 4):
        if row_has_ink(y):
            issues.append(("FAIL", "E2", f"ink at y={y}, above the 1:1 crop line (y={CROP_TOP}) — "
                                         "it disappears in square placements"))
            break
    for y in range(min(CROP_BOT, h - 1), h, 4):
        if row_has_ink(y):
            issues.append(("FAIL", "E2", f"ink at y={y}, below the 1:1 crop line (y={CROP_BOT}) — "
                                         "it disappears in square placements"))
            break

    # E3 — a big empty band means the composition is top-heavy and the call-out
    #      has drifted out of the strongest part of the frame
    inked = [y for y in range(0, h, 3) if row_has_ink(y)]
    if inked:
        gap, run, start = 0, 0, None
        best = (0, None)
        for y in range(inked[0], inked[-1], 3):
            if row_has_ink(y):
                if run > best[0]:
                    best = (run, start)
                run, start = 0, None
            else:
                if start is None:
                    start = y
                run += 3
        if run > best[0]:
            best = (run, start)
        if best[0] >= 180:
            issues.append(("WARN", "E3", f"{best[0]}px dead band starting at y={best[1]} — composition is "
                                         "unbalanced; centre the content block so the call-out sits in the "
                                         "optical centre rather than the top edge"))
    return issues


if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        print(__doc__); sys.exit(2)
    total = 0
    for p in paths:
        iss = qa(p)
        fails = [i for i in iss if i[0] == "FAIL"]
        total += len(fails)
        print(f"{'✗' if fails else '✓'} {p.split('/')[-1]}: {len(fails)} FAIL, {len(iss)-len(fails)} WARN")
        for lvl, code, msg in iss:
            print(f"   [{lvl} {code}] {msg}")
    sys.exit(1 if total else 0)
