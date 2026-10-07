"""Render every ad in ads.json on the skyline template.
Usage: python3 build.py [ads.json]   (run from this folder; needs Chromium headless shell + Inter)
Writes html/<stem>.html and ads/<stem>.png (1080x1350 at 2x)."""
import glob, json, os, subprocess, sys
from template import render

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ads.json")
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
ads = json.load(open(SRC))
for ad in ads:
    stem = ad.pop("stem")
    h = os.path.join(HERE, "html", stem + ".html")
    open(h, "w").write(render(ad))
    png = os.path.join(HERE, "ads", stem + ".png")
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--screenshot=" + png, "file://" + h], check=True, capture_output=True)
    print("wrote", png)
