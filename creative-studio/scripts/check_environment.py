"""Inspect this machine before installing or generating anything. Changes nothing.

  python3 scripts/check_environment.py

Reports chip, macOS version, RAM, free disk, Python, installed packages, the mflux
command, fonts and whether the model weights are already downloaded, then says what to do.
"""
from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GB = 1024**3
MODEL_FULL = "Tongyi-MAI/Z-Image-Turbo"
MODEL_4BIT = "filipstrand/Z-Image-Turbo-mflux-4bit"

results: list[tuple[str, str, str]] = []


def add(status: str, item: str, detail: str) -> None:
    results.append((status, item, detail))


def sh(*cmd: str) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


def ram_bytes() -> int:
    if sys.platform == "darwin":
        out = sh("sysctl", "-n", "hw.memsize")
        return int(out) if out.isdigit() else 0
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal"):
                return int(line.split()[1]) * 1024
    except OSError:
        pass
    return 0


def hf_cache() -> Path:
    home = os.environ.get("HF_HOME")
    return Path(home) / "hub" if home else Path.home() / ".cache" / "huggingface" / "hub"


def model_downloaded(repo: str) -> tuple[bool, float]:
    folder = hf_cache() / f"models--{repo.replace('/', '--')}"
    if not folder.exists():
        return False, 0.0
    size = sum(f.stat().st_size for f in folder.rglob("*") if f.is_file() and not f.is_symlink())
    return size > 1 * GB, size / GB


def main() -> int:
    is_mac = sys.platform == "darwin"
    machine = platform.machine()
    apple_silicon = is_mac and machine == "arm64"

    # chip
    if is_mac:
        chip = sh("sysctl", "-n", "machdep.cpu.brand_string") or machine
        if apple_silicon:
            add("PASS", "Chip", f"{chip} (Apple Silicon, can run local image generation)")
        else:
            add("FAIL", "Chip", f"{chip} (Intel). MLX/MFLUX needs Apple Silicon: posters work, hero generation does not")
    else:
        add("INFO", "Chip", f"{platform.processor() or machine} on {platform.system()} (not a Mac: posters only)")

    # macOS
    if is_mac:
        ver = platform.mac_ver()[0]
        major = int(ver.split(".")[0]) if ver else 0
        add("PASS" if major >= 14 else "FAIL", "macOS", f"{ver} (MLX needs 14.0 or newer)")

    # RAM
    ram = ram_bytes() / GB
    if ram:
        if ram >= 24:
            add("PASS", "RAM", f"{ram:.0f} GB: 8-bit model is fine")
        elif ram >= 16:
            add("WARN", "RAM", f"{ram:.0f} GB: use STUDIO_QUANTIZE=4 and close other apps while generating")
        else:
            add("WARN", "RAM", f"{ram:.0f} GB: tight. Use the 4-bit model ({MODEL_4BIT}) and STUDIO_QUANTIZE=4; expect slow runs")

    # disk
    free = shutil.disk_usage(ROOT).free / GB
    need = 40
    add("PASS" if free >= need else "WARN", "Free disk", f"{free:.0f} GB free (full model download ~31 GB, 4-bit ~6 GB, plus outputs)")

    # python
    py = sys.version_info
    native = platform.processor() == "arm" if apple_silicon else True
    ok_py = py >= (3, 10)
    add("PASS" if ok_py else "FAIL", "Python", f"{platform.python_version()} at {sys.executable} (needs 3.10+)")
    if apple_silicon and not native:
        add("FAIL", "Python build", "Python is running under Rosetta (i386). Use a native arm64 Python (the setup script's uv venv is native)")
    in_venv = sys.prefix != sys.base_prefix
    add("PASS" if in_venv else "INFO", "Virtual env", sys.prefix if in_venv else "not active (run: source .venv/bin/activate)")

    # tools + packages
    add("PASS" if shutil.which("uv") else "INFO", "uv", shutil.which("uv") or "not installed (setup_mac.sh explains how)")
    for mod, pip_name in [("PIL", "pillow"), ("pandas", "pandas"), ("openpyxl", "openpyxl"), ("mflux", "mflux")]:
        found = importlib.util.find_spec(mod) is not None
        status = "PASS" if found else ("WARN" if mod == "mflux" else "FAIL")
        add(status, f"package {pip_name}", "installed" if found else "missing")

    cli = shutil.which("mflux-generate-z-image-turbo")
    if cli:
        help_text = sh(cli, "--help")
        has_output = "--output" in help_text
        add("PASS" if has_output else "WARN", "mflux command", f"{cli}" + ("" if has_output else " (no --output flag in --help: set STUDIO_MFLUX_COMMAND in .env)"))
    else:
        add("WARN" if apple_silicon else "INFO", "mflux command", "mflux-generate-z-image-turbo not on PATH")

    # fonts
    sys.path.insert(0, str(ROOT))
    try:
        from studio.config import fallback_fonts_in_use

        fb = fallback_fonts_in_use()
        add("PASS" if not fb else "WARN", "Fonts", "brand fonts found" if not fb else f"fallback used for {', '.join(fb)}: run scripts/fetch_fonts.sh")
    except Exception as exc:  # noqa: BLE001
        add("FAIL", "Fonts", str(exc))

    # model weights
    for repo in (MODEL_FULL, MODEL_4BIT):
        have, size = model_downloaded(repo)
        add("PASS" if have else "INFO", f"weights {repo}", f"downloaded ({size:.1f} GB)" if have else "not downloaded")

    width = max(len(i) for _, i, _ in results)
    for status, item, detail in results:
        print(f"[{status:4}] {item:<{width}}  {detail}")

    fails = [r for r in results if r[0] == "FAIL"]
    print()
    if is_mac and not apple_silicon:
        print("Intel Mac: run setup_mac.sh --posters-only, put your own hero photos in assets/hero_images/,")
        print("and fill the hero_image column. Local AI generation is not supported on Intel.")
    elif fails:
        print("Fix the FAIL lines above first.")
    else:
        print("Next: bash scripts/setup_mac.sh (if not done), then python scripts/download_model.py")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
