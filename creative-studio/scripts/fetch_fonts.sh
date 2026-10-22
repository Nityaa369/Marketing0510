#!/usr/bin/env bash
# Download the open-licence brand fonts (SIL Open Font License) into assets/fonts/.
# Playfair Display (headlines), Anton (banner + JOIN NOW), Inter (body). No sudo.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p assets/fonts
base="https://raw.githubusercontent.com/google/fonts/main/ofl"
get() {  # url-path  local-name
  if [ -s "assets/fonts/$2" ]; then echo "have  $2"; return; fi
  curl -fsSL "$base/$1" -o "assets/fonts/$2" && echo "got   $2"
}
get "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf"        "PlayfairDisplay[wght].ttf"
get "playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf" "PlayfairDisplay-Italic[wght].ttf"
get "anton/Anton-Regular.ttf"                               "Anton-Regular.ttf"
get "inter/Inter%5Bopsz,wght%5D.ttf"                        "Inter[opsz,wght].ttf"
echo "Fonts ready in assets/fonts/ (licence: SIL OFL 1.1, free for commercial use)."
