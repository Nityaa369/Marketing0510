"""Paths, brand config, template layout and font lookup."""
from __future__ import annotations

import json
import os
import sys
from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
HERO_DIR = ASSETS_DIR / "hero_images"
OUTPUTS_DIR = ROOT / "outputs"

SYSTEM_FONT_DIRS = [
    Path.home() / "Library/Fonts",
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path("/System/Library/Fonts/Supplemental"),
    Path("/usr/share/fonts"),
]


def load_env(path: Path | None = None) -> None:
    """Read KEY=VALUE lines from .env into os.environ (no extra dependency)."""
    path = path or ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@lru_cache(maxsize=None)
def load_brand(path: str | None = None) -> dict:
    return json.loads(Path(path or CONFIG_DIR / "brand.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def load_layout(template: str = "ncacanada") -> dict:
    path = TEMPLATES_DIR / template / "layout.json"
    if not path.exists():
        raise FileNotFoundError(f"No template called '{template}' (looked for {path})")
    return json.loads(path.read_text(encoding="utf-8"))


def color(name_or_hex: str, brand: dict | None = None) -> str:
    brand = brand or load_brand()
    return brand["colors"].get(name_or_hex, name_or_hex)


def _find_font_file(filename: str) -> Path | None:
    direct = FONTS_DIR / filename
    if direct.exists():
        return direct
    for folder in SYSTEM_FONT_DIRS:
        if not folder.exists():
            continue
        hit = next(folder.rglob(filename), None)
        if hit:
            return hit
    return None


@lru_cache(maxsize=None)
def resolve_font(role: str) -> tuple[str, str | None, bool]:
    """Return (path, variation, is_fallback) for a font role in brand.json."""
    fonts = load_brand()["fonts"]
    spec = fonts[role]
    for filename in spec["files"]:
        path = _find_font_file(filename)
        if path:
            return str(path), spec.get("variation"), False
    for filename in fonts.get("fallback", []):
        path = _find_font_file(filename)
        if path:
            return str(path), None, True
    raise FileNotFoundError(
        f"No font found for '{role}'. Run scripts/fetch_fonts.sh or put {spec['files'][0]} in {FONTS_DIR}"
    )


@lru_cache(maxsize=512)
def font(role: str, size: int) -> ImageFont.FreeTypeFont:
    path, variation, _ = resolve_font(role)
    f = ImageFont.truetype(path, size)
    if variation:
        try:
            f.set_variation_by_name(variation)
        except (OSError, ValueError):
            pass  # static font: the file itself is already the right weight
    return f


def fallback_fonts_in_use() -> list[str]:
    roles = [r for r in load_brand()["fonts"] if r not in ("fallback", "_note")]
    return [r for r in roles if resolve_font(r)[2]]


def is_apple_silicon() -> bool:
    import platform

    return sys.platform == "darwin" and platform.machine() == "arm64"
