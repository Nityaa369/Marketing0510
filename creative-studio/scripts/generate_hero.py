"""Generate ONE hero image (no text) for a scene.

  python scripts/generate_hero.py --id test01 --prompt "a young Indian woman lawyer in a black blazer, Toronto skyline behind"
  python scripts/generate_hero.py --sheet data/icps_template.xlsx --row nca01_new_grads
Add --backend placeholder to test without the model.
"""
import argparse
import sys
import time

import _bootstrap  # noqa: F401
from studio.config import load_brand, load_layout
from studio.hero import HeroError, build_prompt, generate_hero
from studio.sheet import load_rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--id", help="file name for the hero (assets/hero_images/<id>.png)")
    p.add_argument("--prompt", help="scene description: people and place, never text")
    p.add_argument("--sheet", help="take id + hero_prompt + seed from this spreadsheet")
    p.add_argument("--row", help="row id in --sheet")
    p.add_argument("--seed", type=int)
    p.add_argument("--template", default="ncacanada")
    p.add_argument("--backend", choices=["mflux", "hf_space", "placeholder"], help="default: STUDIO_HERO_BACKEND or mflux")
    p.add_argument("--force", action="store_true", help="regenerate even if an identical image exists")
    a = p.parse_args()

    layout = load_layout(a.template)
    seed = a.seed
    if a.sheet:
        program = load_brand()["programs"][layout["program"]]
        rows = {r.id: r for r in load_rows(a.sheet, program, layout)}
        if a.row not in rows:
            p.error(f"row '{a.row}' not in {a.sheet}. Ids: {', '.join(rows)}")
        row = rows[a.row]
        a.id, a.prompt = row.id, row.get("hero_prompt")
        seed = seed if seed is not None else row.get("seed") or None
    if not (a.id and a.prompt):
        p.error("give --id and --prompt, or --sheet and --row")

    print("prompt:", build_prompt(a.prompt, layout))
    t0 = time.time()
    try:
        out = generate_hero(a.id, a.prompt, layout, backend=a.backend, seed=seed, force=a.force)
    except HeroError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"hero saved: {out}  ({time.time() - t0:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
