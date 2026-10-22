"""Whole spreadsheet -> hero images -> posters -> contact sheet.

  python scripts/generate_batch.py --sheet data/icps_template.xlsx
  python scripts/generate_batch.py --sheet data/icps_template.xlsx --limit 1        # try one first
  python scripts/generate_batch.py --sheet data/icps_template.xlsx --only nca03_canadian_clients nca07_punjab_lawyers
Re-running skips rows that already succeeded with the same inputs, so after a failure just run it again.
"""
import argparse
import sys

import _bootstrap  # noqa: F401
from studio.batch import run_batch


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--sheet", required=True)
    p.add_argument("--template", default="ncacanada")
    p.add_argument("--backend", choices=["mflux", "hf_space", "placeholder"], help="default: STUDIO_HERO_BACKEND or mflux")
    p.add_argument("--only", nargs="+", help="only these row ids")
    p.add_argument("--limit", type=int, help="only the first N rows")
    p.add_argument("--force", action="store_true", help="redo posters even if unchanged (heroes are reused unless prompt/seed changed)")
    p.add_argument("--no-contact-sheet", action="store_true")
    a = p.parse_args()

    r = run_batch(
        a.sheet, a.template, backend=a.backend, force=a.force, only=a.only, limit=a.limit,
        contact_sheet=not a.no_contact_sheet,
    )
    print(f"\nmade {len(r.done)} · skipped (unchanged) {len(r.skipped)} · failed {len(r.failed)} · invalid {len(r.invalid)}")
    for rid, errs in r.invalid.items():
        print(f"  INVALID {rid}: {'; '.join(errs)}")
    for rid, err in r.failed.items():
        print(f"  FAILED  {rid}: {err}")
    for rid, ws in r.warnings.items():
        print(f"  warn    {rid}: {'; '.join(ws)}")
    print(f"report: {r.report}")
    if r.contact_sheet:
        print(f"contact sheet: {r.contact_sheet}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    sys.exit(main())
