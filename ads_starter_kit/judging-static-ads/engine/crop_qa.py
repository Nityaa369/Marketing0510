#!/usr/bin/env python3
"""Crop-safety QA for carousel cards.

Meta renders carousel cards square. A 1080x1350 card is centre-cropped to 1080x1080, which
discards the top 135px and the bottom 135px. The 25 Jul 2026 rule ("labels/cues/CTAs must be
prominent AND inside the ~140px crop-safe zone; QA the render") exists because of exactly this.

This does not guess from CSS geometry. It reads the rendered PNG and reports how much INK
(non-background pixels) falls in the two bands that a square crop throws away, so a sliced CTA
cannot ship unnoticed.

Usage:  python3 ads/crop_qa.py <png> [png ...]
Exit 1 if any card has ink in a discarded band above the tolerance.
"""
import sys, os
from collections import Counter

try:
    from PIL import Image
except ImportError:
    Image = None


def load_rgb(path):
    """Return (w, h, getpixel-like callable). Falls back to `sips`+raw if Pillow is absent."""
    if Image is not None:
        im = Image.open(path).convert("RGB")
        return im.width, im.height, im.load()
    # Exit 2, not 1. Exit 1 means "a card loses its CTA to the crop"; a missing dependency is
    # not a defect in the card. creative_judge.py read the two as the same thing and reported a
    # spurious X1 BLOCK on every creative whenever Pillow was absent. Matches ad_render_qa.py.
    print("crop_qa needs Pillow: python3 -m pip install --user Pillow", file=sys.stderr)
    raise SystemExit(2)


"""CALIBRATION (1 Aug 2026). Thresholds are set against a known-good card, not invented:
`ads/wave3_jul31/techlaw_carousels/c1_s5_cta.png` is the ₹114/buyer Tech Law carousel, the best
carousel result on record, and it is also 1080x1350. It measures 3.7% top / 0.0% bottom. Its top
band holds only the brand header, which is cosmetic to lose. So:
  bottom band  -> the CTA and the payoff line live here. Anything above BOTTOM_TOL is a real defect.
  top band     -> reported for information only; the proven winner fails a strict top-band test.
Cards drawn as a "sheet on a desk" inflate both numbers, because the desk margin reads as ink
against a sheet-coloured background. Always confirm a flagged card by eye with an actual crop.
"""
BOTTOM_TOL = 0.03
TOP_REPORT_ONLY = True


def analyse(path, tol=BOTTOM_TOL):
    w, h, px = load_rgb(path)
    if h <= w:
        return path, None, "already square or wider, no crop applied"
    band = (h - w) // 2                      # discarded at top and at bottom

    # background = most common colour in the card, sampled on a grid
    c = Counter()
    for y in range(0, h, 7):
        for x in range(0, w, 7):
            c[px[x, y]] += 1
    bg = c.most_common(1)[0][0]

    def ink_frac(y0, y1):
        n = hit = 0
        for y in range(y0, y1, 2):
            for x in range(0, w, 2):
                r, g, b = px[x, y]
                n += 1
                if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 60:
                    hit += 1
        return hit / max(n, 1)

    top = ink_frac(0, band)
    bot = ink_frac(h - band, h)
    # Only the bottom band is a launch blocker: that is where the CTA and the payoff line sit.
    # The top band carries the brand header, which the proven ₹114 winner also loses.
    return path, (top, bot, band, bot > tol), None


def main(paths):
    bad = []
    print(f"{'card':<52} {'top band':>9} {'bottom band':>12}   verdict")
    for p in paths:
        path, res, note = analyse(p)
        if res is None:
            print(f"{os.path.basename(path)[:52]:<52} {note}")
            continue
        top, bot, band, fail = res
        v = "CTA/PAYOFF CUT" if fail else "safe"
        if fail:
            bad.append(path)
        print(f"{os.path.basename(path)[:52]:<52} {top*100:>8.1f}% {bot*100:>11.1f}%   {v}")
    print(f"\n{len(bad)} card(s) lose the CTA or payoff line to the square crop.")
    for b in bad:
        print("   ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a.endswith(".png") and not os.path.basename(a).startswith("_")]
    if not args:
        raise SystemExit("usage: python3 ads/crop_qa.py <card.png> [...]")
    sys.exit(main(sorted(args)))
