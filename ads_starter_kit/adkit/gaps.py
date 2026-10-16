"""Measure the vertical whitespace between blocks on a rendered ad face.

Written 4 Sep 2026, after the third round of *"there are a lot of empty gaps,
especially above the footer, space it out properly so that it doesn't look
awkward"* / *"make sure everything is aligned properly, no weird spaces"*.

Nothing in this repo could see this. `adkit.fit` measures the box model but only
asks whether anything CLIPS or OVERLAPS -- a face with a 300px void in the middle
passes it, because a void is the opposite of an overlap. `simplicity.py` checks
that text blocks share a left edge, which is the horizontal half of the same
question and was already covered. `ad_lint` reads source CSS and never renders.
So every gap complaint so far arrived from a human looking at a PNG, three times,
and each time I fixed the one face I was shown.

WHY IT MEASURES THE PNG AND NOT THE DOM

The first version drove a DOM probe. It ran, and it was useless as a gate,
because the corpus this repo fits its checkers on -- GOLDEN, the faces Ramanuj
approved or built himself -- is **PNG only**. A rule that can only be measured on
faces we generated ourselves can never be fitted against approved work, which is
the one thing this repo asks of a checker. Reading pixels measures both classes
on the same ruler, and it measures what the reader actually sees rather than what
the box model intended.

WHAT IT MEASURES

Rows of the image within tolerance of the page background, in one uninterrupted
run, lying strictly between the first and last row that carry content. Top and
bottom page margins are excluded by construction. The longest such run is the
face's worst gap.

THE THRESHOLD IS FITTED, NOT CHOSEN

Run `python -m adkit.gaps --fit` to re-measure the corpus and print the numbers
the ceiling is set from. Measured 4 Sep 2026:

    9 GOLDEN faces        largest 178px   median  63px
    10 priced faces       largest 151px   median 100px
      (us22_notice_fifties Rs 29.65 = 66px; 03_law_firm_associates Rs 82 = 150px;
       icp_28_biomedical_devices Rs 91.36 = 1px)

So no face that was approved, and no face that ran cheaply, pools more than 178px
of background in one place. CEILING = 200 sits just above that: it blocks 0 of 19,
and it blocks the 207px US Corporate Law face that was reported. On a 1350px
canvas 200px is under an eighth of the height.

It is a one-class fit, like `simplicity.py`: it can show that the ceiling does not
block work that was approved. It cannot prove that everything it passes looks
good. A human still opens the PNG. Aim for the priced range (under about 150px)
rather than for the ceiling.
"""

import glob
import os
import pathlib
import sys

CEILING = 200      # px of uninterrupted background between blocks, 1350px canvas
TOL = 10           # per-channel distance from background that still counts empty
INK = 0.004        # fraction of a row that must differ from bg for it to be content


def _rows(png):
    """Return (height, [is_content per row]) for one PNG."""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    px = im.load()
    # background = whichever corner colour the four corners agree on. Faces in
    # this repo are flat-ground, so this is exact rather than a guess.
    corners = [px[0, 0], px[w - 1, 0], px[0, h - 1], px[w - 1, h - 1]]
    bg = max(set(corners), key=corners.count)
    step = max(1, w // 400)          # sample columns; 400 is ample at 1080 wide
    need = max(1, int((w / step) * INK))
    out = []
    for y in range(h):
        n = 0
        for x in range(0, w, step):
            r, g, b = px[x, y]
            if abs(r - bg[0]) > TOL or abs(g - bg[1]) > TOL or abs(b - bg[2]) > TOL:
                n += 1
                if n >= need:
                    break
        out.append(n >= need)
    return h, out


def measure(png):
    """Return (worst_interior_gap_px, y_of_that_gap) for one face."""
    _, content = _rows(png)
    idx = [i for i, c in enumerate(content) if c]
    if not idx:
        return (0, 0)
    first, last = idx[0], idx[-1]
    worst, at, run, start = 0, 0, 0, None
    for y in range(first, last + 1):
        if not content[y]:
            if start is None:
                start = y
            run += 1
            if run > worst:
                worst, at = run, start
        else:
            run, start = 0, None
    return (worst, at)


def check_dir(d, pattern="*.png"):
    """Yield (name, worst_gap, y) for every PNG in a directory."""
    for f in sorted(glob.glob(os.path.join(d, pattern))):
        gap, at = measure(f)
        yield (pathlib.Path(f).stem, gap, at)


def _fit():
    """Re-measure the approved corpus and print what the ceiling should be."""
    here = pathlib.Path(__file__).resolve().parent.parent
    rows = [(gap, "GOLDEN/" + name)
            for name, gap, _ in check_dir(str(here / "GOLDEN"))]
    if not rows:
        print("  ERROR: no faces found in GOLDEN; cannot fit.")
        return 1
    rows.sort(reverse=True)
    print("approved faces, largest interior background run:\n")
    for gap, name in rows[:12]:
        print("    %5dpx  %s" % (gap, name))
    if len(rows) > 12:
        print("    ... %d more" % (len(rows) - 12))
    med = rows[len(rows) // 2][0]
    print("\n    faces: %d   largest: %dpx   median: %dpx   current ceiling: %dpx"
          % (len(rows), rows[0][0], med, CEILING))
    print("\n    the ceiling must sit ABOVE %dpx or it blocks approved work."
          % rows[0][0])
    return 0


def main(argv):
    if "--fit" in argv:
        return _fit()
    kits = [a for a in argv if not a.startswith("-")]
    worst_overall, bad, seen = 0, 0, 0
    for kit in kits:
        d = kit if os.path.basename(kit) == "ads" else os.path.join(kit, "ads")
        print("%s" % kit)
        for name, gap, at in check_dir(d):
            seen += 1
            worst_overall = max(worst_overall, gap)
            ok = gap <= CEILING
            bad += not ok
            print("    %-38s %4dpx  at y=%-5d%s"
                  % (name, gap, at, "" if ok else "   <-- over %dpx" % CEILING))
        print("")
    if not seen:
        print("ERROR: no faces measured.")
        return 1
    print("faces: %d   worst gap: %dpx   ceiling: %dpx   over: %d"
          % (seen, worst_overall, CEILING, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
