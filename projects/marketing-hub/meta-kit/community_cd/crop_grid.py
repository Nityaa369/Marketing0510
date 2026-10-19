"""Cut the 4x5 grid image into photos/cd_01.jpg .. cd_20.jpg.

python3 crop_grid.py grid.png [prefix] [ext]   (default cd jpg)
Finds the white gutters; falls back to equal cells if it cannot find 3 and 4 of them.
"""
import sys
import numpy as np
from PIL import Image

COLS, ROWS = 4, 5


def bands(white_frac, n_needed):
    """Centres of runs where the line is mostly white, excluding the outer border."""
    runs, start = [], None
    for i, w in enumerate(white_frac > 0.97):
        if w and start is None:
            start = i
        if not w and start is not None:
            runs.append((start, i - 1)); start = None
    if start is not None:
        runs.append((start, len(white_frac) - 1))
    inner = [r for r in runs if r[0] > 0 and r[1] < len(white_frac) - 1]
    return runs, inner if len(inner) == n_needed else None


im = Image.open(sys.argv[1]).convert("RGB")
PREFIX = sys.argv[2] if len(sys.argv) > 2 else "cd"
EXT = sys.argv[3] if len(sys.argv) > 3 else "jpg"
a = np.asarray(im).astype(int)
white = (a.min(axis=2) > 238)
W, H = im.size
col_runs, cg = bands(white.mean(axis=0), COLS - 1)
row_runs, rg = bands(white.mean(axis=1), ROWS - 1)


def edges(runs, gutters, size, n):
    if gutters is None:
        step = size / n
        return [(round(i * step), round((i + 1) * step)) for i in range(n)]
    lo = runs[0][1] + 1 if runs and runs[0][0] == 0 else 0
    hi = runs[-1][0] if runs and runs[-1][1] == size - 1 else size
    cuts = [lo] + [x for g in gutters for x in (g[0], g[1] + 1)] + [hi]
    return [(cuts[2 * i], cuts[2 * i + 1]) for i in range(n)]


xs = edges(col_runs, cg, W, COLS)
ys = edges(row_runs, rg, H, ROWS)
print("gutters found:", cg is not None and rg is not None)
k = 0
for y0, y1 in ys:
    for x0, x1 in xs:
        k += 1
        cell = im.crop((x0 + 6, y0 + 6, x1 - 6, y1 - 6))
        cell.save(f"photos/{PREFIX}_{k:02d}.{EXT}", quality=92)
        print(f"{PREFIX}_{k:02d}", cell.size)
