"""Download the image model and prove it works. Runs ONLY when you call it.

  python scripts/download_model.py            # z-image-turbo = Tongyi-MAI/Z-Image-Turbo, Apache-2.0, ~31 GB
  python scripts/download_model.py --small    # filipstrand/Z-Image-Turbo-mflux-4bit, ~6 GB (check its licence tag)

It asks first, then lets mflux fetch exactly the files (and the pinned revision) it needs by
making one tiny 256x256 test image. Weights land in the Hugging Face cache
(~/.cache/huggingface/hub), outside the repo, so Git never sees them.
"""
import argparse
import os
import shutil
import sys
import time
from pathlib import Path

import _bootstrap  # noqa: F401
from studio.config import OUTPUTS_DIR
from studio.hero import DEFAULT_MODEL, HeroError, _run_mflux

SMALL = "filipstrand/Z-Image-Turbo-mflux-4bit"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--small", action="store_true", help=f"use the pre-quantized 4-bit copy ({SMALL})")
    p.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    a = p.parse_args()

    if a.small:
        os.environ["STUDIO_MODEL"] = SMALL
        os.environ["STUDIO_QUANTIZE"] = "none"
    model = os.environ.get("STUDIO_MODEL", DEFAULT_MODEL)
    need_gb = 8 if model == SMALL else 35
    free = shutil.disk_usage(Path.home()).free / 1024**3
    print(f"Model: {model}")
    print(f"Free disk: {free:.0f} GB, need about {need_gb} GB")
    if free < need_gb:
        print("Not enough free disk space. Free some space or use --small.", file=sys.stderr)
        return 1
    if model == SMALL:
        print("Note: the upstream model is Apache-2.0, but this pre-quantized copy is tagged")
        print("'tongyi-qianwen-license' on Hugging Face. Read it before commercial use.")
    if not a.yes and input("Download now? [y/N] ").strip().lower() != "y":
        print("Cancelled.")
        return 1

    out = OUTPUTS_DIR / "logs" / "model_check.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    print("Downloading (first time only) and making a 256x256 test image...")
    try:
        _run_mflux(out, "a red maple leaf on a cream background", 256, 256, 1)
    except HeroError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"Model works. Test image: {out}  ({time.time() - t0:.0f}s including download)")
    if model == SMALL:
        print("Add these lines to .env so every run uses it:")
        print(f"  STUDIO_MODEL={SMALL}\n  STUDIO_QUANTIZE=none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
