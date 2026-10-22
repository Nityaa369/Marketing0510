"""Render ONE poster from a spreadsheet row (hero must exist or be given).

  python scripts/render_poster.py --sheet data/icps_template.xlsx --row nca01_new_grads
  python scripts/render_poster.py --sheet data/icps_template.xlsx --row nca01_new_grads --hero ~/Desktop/photo.jpg
"""
import argparse
import sys
from pathlib import Path

import _bootstrap  # noqa: F401
from studio.config import HERO_DIR, OUTPUTS_DIR, load_brand, load_layout
from studio.poster import PosterError, render_poster
from studio.sheet import load_rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sheet", required=True)
    p.add_argument("--row", required=True)
    p.add_argument("--hero", help="hero image path (default: hero_image column, then assets/hero_images/<id>.png)")
    p.add_argument("--template", default="ncacanada")
    p.add_argument("--out", help="output PNG (default outputs/individual_ads/<id>.png)")
    a = p.parse_args()

    layout = load_layout(a.template)
    program = load_brand()["programs"][layout["program"]]
    rows = {r.id: r for r in load_rows(a.sheet, program, layout)}
    if a.row not in rows:
        p.error(f"row '{a.row}' not in {a.sheet}. Ids: {', '.join(rows)}")
    row = rows[a.row]
    if not row.ok:
        print("Row is invalid:\n  " + "\n  ".join(row.errors), file=sys.stderr)
        return 1
    hero = Path(a.hero or row.get("hero_image") or HERO_DIR / f"{row.id}.png").expanduser()
    out = Path(a.out) if a.out else OUTPUTS_DIR / "individual_ads" / f"{row.id}.png"
    try:
        rep = render_poster(row.data, hero, out, a.template)
    except PosterError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"poster saved: {rep.path}  {rep.size[0]}x{rep.size[1]}  JOIN NOW bar {rep.cta_share:.1%} of poster")
    print("font sizes:", rep.font_sizes)
    for w in rep.warnings:
        print("WARNING:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
