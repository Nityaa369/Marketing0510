"""Hero image generation. The model only paints the scene; posters add every word.

Backends
  mflux        Local, free. Runs the MFLUX command line tool on an Apple Silicon Mac.
  placeholder  Draws a labelled stand-in with Pillow, so the pipeline can be tested
               anywhere. Never ship a placeholder poster.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from .config import HERO_DIR, color, font

DEFAULT_MODEL = "z-image-turbo"  # mflux alias for Tongyi-MAI/Z-Image-Turbo (Apache-2.0)
DEFAULT_COMMAND = (
    "mflux-generate-z-image-turbo --model {model} --prompt {prompt} --width {width} --height {height}"
    " --seed {seed} --steps {steps} {quantize_flag} --output {output}"
)


class HeroError(RuntimeError):
    pass


def build_prompt(scene: str, layout: dict) -> str:
    gen = layout["hero_generation"]
    return f"{gen['style_prefix']}{scene.strip().rstrip('.')}{gen['style_suffix']}"


def seed_for(row_id: str, seed: str | int | None = None) -> int:
    if seed not in (None, ""):
        return int(float(seed))
    return int(hashlib.sha256(row_id.encode()).hexdigest()[:8], 16) % 2_000_000_000


def sidecar(path: Path) -> Path:
    return path.with_suffix(".json")


def read_meta(path: Path) -> dict:
    meta = sidecar(Path(path))
    return json.loads(meta.read_text()) if meta.exists() else {}


def _write_meta(path: Path, meta: dict) -> None:
    sidecar(path).write_text(json.dumps(meta, indent=2, ensure_ascii=False))


def backend_from_env() -> str:
    return os.environ.get("STUDIO_HERO_BACKEND", "mflux")


def generate_hero(
    row_id: str,
    scene: str,
    layout: dict,
    *,
    backend: str | None = None,
    seed: int | str | None = None,
    out_dir: Path = HERO_DIR,
    force: bool = False,
) -> Path:
    """Create (or reuse) the hero image for one row and return its path."""
    backend = backend or backend_from_env()
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{row_id}.png"
    prompt = build_prompt(scene, layout)
    seed_value = seed_for(row_id, seed)
    gen = layout["hero_generation"]

    if out.exists() and not force:
        meta = read_meta(out)
        if meta.get("prompt") == prompt and meta.get("seed") == seed_value and meta.get("backend") == backend:
            return out

    started = time.time()
    if backend == "placeholder":
        _placeholder(out, row_id, gen["width"], gen["height"], seed_value)
    elif backend == "mflux":
        _run_mflux(out, prompt, gen["width"], gen["height"], seed_value)
    else:
        raise HeroError(f"Unknown hero backend '{backend}' (use mflux or placeholder)")

    if not out.exists():
        raise HeroError(f"{backend} finished but wrote no image at {out}")
    with Image.open(out) as im:
        size = im.size
    _write_meta(
        out,
        {
            "row_id": row_id,
            "backend": backend,
            "model": os.environ.get("STUDIO_MODEL", DEFAULT_MODEL) if backend == "mflux" else None,
            "prompt": prompt,
            "seed": seed_value,
            "size": size,
            "seconds": round(time.time() - started, 1),
            "placeholder": backend == "placeholder",
        },
    )
    return out


def _run_mflux(out: Path, prompt: str, width: int, height: int, seed: int) -> None:
    template = os.environ.get("STUDIO_MFLUX_COMMAND", DEFAULT_COMMAND)
    exe = template.split()[0]
    if not shutil.which(exe):
        raise HeroError(
            f"'{exe}' not found. On your Mac run scripts/setup_mac.sh and `source .venv/bin/activate`, "
            "or set STUDIO_HERO_BACKEND=placeholder to test without a model."
        )
    quantize = os.environ.get("STUDIO_QUANTIZE", "8").strip()
    values = {
        "model": shlex.quote(os.environ.get("STUDIO_MODEL", DEFAULT_MODEL)),
        "prompt": shlex.quote(prompt),
        "width": width,
        "height": height,
        "seed": seed,
        "steps": int(os.environ.get("STUDIO_STEPS", "9")),
        "quantize_flag": f"-q {int(quantize)}" if quantize not in ("", "0", "none") else "",
        "output": shlex.quote(str(out)),
    }
    cmd = shlex.split(template.format(**values))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-15:]
        raise HeroError("mflux failed:\n" + "\n".join(tail))


def _placeholder(out: Path, row_id: str, width: int, height: int, seed: int) -> None:
    """A clearly labelled stand-in scene: sky gradient, skyline, maple leaf, figure."""
    import random

    rnd = random.Random(seed)
    top = (250, 238 - rnd.randint(0, 30), 220 - rnd.randint(0, 40))
    bottom = (200 + rnd.randint(0, 40), 40 + rnd.randint(0, 40), 50 + rnd.randint(0, 30))
    im = Image.new("RGB", (width, height))
    px = ImageDraw.Draw(im)
    for y in range(height):
        t = y / height
        px.line([(0, y), (width, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bottom)))
    # skyline
    x = 0
    while x < width:
        w = rnd.randint(40, 110)
        h = rnd.randint(height // 6, height // 2)
        px.rectangle([x, height - h, x + w, height], fill=(60, 30, 35))
        x += w + rnd.randint(4, 18)
    tower_x = int(width * rnd.uniform(0.55, 0.8))
    px.rectangle([tower_x - 8, int(height * 0.12), tower_x + 8, height], fill=(60, 30, 35))
    px.ellipse([tower_x - 26, int(height * 0.32), tower_x + 26, int(height * 0.38)], fill=(60, 30, 35))
    # figure in court dress
    cx, base = int(width * rnd.uniform(0.22, 0.4)), height
    px.ellipse([cx - 55, base - 430, cx + 55, base - 310], fill=(150, 100, 75))
    px.polygon([(cx - 150, base), (cx - 110, base - 300), (cx + 110, base - 300), (cx + 150, base)], fill=(20, 20, 20))
    px.polygon([(cx - 22, base - 300), (cx + 22, base - 300), (cx, base - 230)], fill=(250, 250, 250))
    draw_maple_leaf(px, (int(width * 0.88), int(height * 0.2)), int(height * 0.12), color("red"))
    im = im.filter(ImageFilter.GaussianBlur(1.2))
    d = ImageDraw.Draw(im)
    label = f"PLACEHOLDER HERO · {row_id}"
    f = font("body", max(18, height // 24))
    top = height // 3
    d.rectangle([0, top, d.textlength(label, font=f) + 40, top + f.size + 24], fill=(255, 255, 255))
    d.text((20, top + 12), label, font=f, fill=(0, 0, 0))
    im.save(out)


def draw_maple_leaf(draw: ImageDraw.ImageDraw, center: tuple[int, int], size: int, fill) -> None:
    """Stylised 11-point maple leaf drawn as a polygon (no image asset needed)."""
    pts = [
        (0, -1.0), (0.12, -0.72), (0.3, -0.8), (0.24, -0.38), (0.6, -0.62), (0.52, -0.45), (0.92, -0.42),
        (0.78, -0.22), (0.9, -0.12), (0.4, 0.2), (0.48, 0.38), (0.06, 0.32), (0.06, 0.75), (-0.06, 0.75),
        (-0.06, 0.32), (-0.48, 0.38), (-0.4, 0.2), (-0.9, -0.12), (-0.78, -0.22), (-0.92, -0.42),
        (-0.52, -0.45), (-0.6, -0.62), (-0.24, -0.38), (-0.3, -0.8), (-0.12, -0.72),
    ]
    cx, cy = center
    draw.polygon([(cx + x * size, cy + y * size) for x, y in pts], fill=fill)
