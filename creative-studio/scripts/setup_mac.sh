#!/usr/bin/env bash
# One-time setup on your Mac. Checks first, installs only into ./.venv, never uses sudo,
# never downloads model weights (that is scripts/download_model.py, run separately).
#
#   bash scripts/setup_mac.sh                # Apple Silicon: posters + local AI generation
#   bash scripts/setup_mac.sh --posters-only # Intel Mac or no AI: posters from your own photos
set -euo pipefail
cd "$(dirname "$0")/.."

POSTERS_ONLY=0
[ "${1:-}" = "--posters-only" ] && POSTERS_ONLY=1

say()  { printf "\n== %s\n" "$1"; }
fail() { printf "\nSTOP: %s\n" "$1"; exit 1; }

say "Checking this Mac"
if [ "$(uname -s)" != "Darwin" ]; then
  echo "Not macOS: continuing in posters-only mode."
  POSTERS_ONLY=1
fi
if [ "$(uname -s)" = "Darwin" ]; then
  ARCH="$(uname -m)"
  MACOS="$(sw_vers -productVersion)"
  echo "chip: $(sysctl -n machdep.cpu.brand_string)  arch: $ARCH  macOS: $MACOS"
  if [ "$ARCH" != "arm64" ] && [ $POSTERS_ONLY -eq 0 ]; then
    if [ "$(sysctl -in sysctl.proc_translated)" = "1" ]; then
      fail "This Terminal runs under Rosetta. Open Terminal without 'Open using Rosetta' and run again."
    fi
    echo "Intel Mac: local AI generation (MLX) is not supported. Switching to posters-only."
    POSTERS_ONLY=1
  fi
  if [ $POSTERS_ONLY -eq 0 ] && [ "${MACOS%%.*}" -lt 14 ]; then
    fail "MLX needs macOS 14 or newer (you have $MACOS). Update macOS, or run with --posters-only."
  fi
fi

say "Checking uv (Python manager, installs to your home folder, no sudo)"
if ! command -v uv >/dev/null 2>&1; then
  cat <<'MSG'
uv is not installed. Install it with ONE of these, then open a new Terminal and run this script again:
  brew install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh
MSG
  exit 1
fi
uv --version

say "Creating the isolated environment in .venv (Python 3.12, native)"
[ -d .venv ] || uv venv --python 3.12 .venv
# shellcheck disable=SC1091
source .venv/bin/activate

say "Installing packages into .venv only"
if [ $POSTERS_ONLY -eq 1 ]; then
  uv pip install -e ".[dev]"
else
  uv pip install -e ".[mac,dev]"
fi

say "Fonts"
bash scripts/fetch_fonts.sh

say "Config"
[ -f .env ] || { cp .env.example .env; echo "created .env from .env.example"; }
if [ $POSTERS_ONLY -eq 1 ]; then
  grep -q '^STUDIO_HERO_BACKEND=' .env && sed -i '' 's/^STUDIO_HERO_BACKEND=.*/STUDIO_HERO_BACKEND=placeholder/' .env 2>/dev/null || true
fi

say "Environment report"
python scripts/check_environment.py || true

cat <<MSG

Setup finished. Every new Terminal: cd into this folder, then  source .venv/bin/activate
$( [ $POSTERS_ONLY -eq 1 ] && echo "Posters-only: put photos in assets/hero_images/ and fill the hero_image column." || echo "Next: python scripts/download_model.py   (downloads the model, asks first)" )
MSG
