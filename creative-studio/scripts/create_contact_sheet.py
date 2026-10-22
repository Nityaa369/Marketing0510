"""Contact sheet from a folder of posters (the batch makes one automatically).

  python scripts/create_contact_sheet.py
  python scripts/create_contact_sheet.py --folder outputs/individual_ads --out outputs/contact_sheets/review.png
"""
import argparse
import sys
import time
from pathlib import Path

import _bootstrap  # noqa: F401
from studio.config import OUTPUTS_DIR
from studio.contact_sheet import create_contact_sheet


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--folder", default=str(OUTPUTS_DIR / "individual_ads"))
    p.add_argument("--out", default=str(OUTPUTS_DIR / "contact_sheets" / f"sheet_{time.strftime('%Y%m%d_%H%M')}.png"))
    p.add_argument("--title", default="Contact sheet")
    p.add_argument("--columns", type=int)
    a = p.parse_args()
    posters = sorted(Path(a.folder).glob("*.png"))
    if not posters:
        print(f"no PNG posters in {a.folder}", file=sys.stderr)
        return 1
    out = create_contact_sheet([(x, x.stem) for x in posters], a.out, a.title, columns=a.columns)
    print(f"contact sheet: {out} ({len(posters)} posters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
