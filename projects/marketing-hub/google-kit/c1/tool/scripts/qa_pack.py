#!/usr/bin/env python3
"""
qa_pack.py - Check the rendered set, build contact sheets for visual QA, zip it, pick WhatsApp samples.

Usage:
  python3 qa_pack.py OUT_DIR ZIP_PATH [--content content.json] [--flat] [--limit-mb 29.5]

Checks:
  * every ad folder holds exactly 12 JPGs: C1..C4 x landscape 1200x628, square 1200x1200, portrait 960x1200
  * every file's pixel size matches the size in its name
  * if --content is given: every ad in the JSON has a folder (none missing, none extra)
Makes:
  * OUT_DIR/../qa_sheets/<size>_C<n>.jpg contact sheets  -> LOOK AT EVERY SHEET before delivering
  * ZIP_PATH (stored, no recompression) containing OUT_DIR as its top folder
  * OUT_DIR/../whatsapp_samples/ with one C1 square and one C1 portrait from the first two ads
Fails (exit 1) if a check fails or the zip is over --limit-mb (re-render with a lower --quality, e.g. 76).
"""
import argparse, glob, json, os, re, shutil, sys, zipfile
from PIL import Image

EXPECT = {(f"C{c}", s, w, h) for c in range(1, 5) for s, w, h in [("landscape", 1200, 628), ("square", 1200, 1200), ("portrait", 960, 1200)]}
PAT = re.compile(r"^(?P<slug>.+)_(?P<c>C[1-4])_(?P<size>landscape|square|portrait)_(?P<w>\d+)x(?P<h>\d+)\.jpg$")

def sheet(files, out, cols=6, tw=300):
    if not files: return
    ims = [Image.open(f).convert("RGB") for f in files]
    th = int(tw * ims[0].height / ims[0].width)
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * (tw + 6) + 6, rows * (th + 6) + 6), "#9a9a9a")
    for i, im in enumerate(ims):
        canvas.paste(im.resize((tw, th)), (6 + (i % cols) * (tw + 6), 6 + (i // cols) * (th + 6)))
    canvas.save(out, quality=85)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("zip"); ap.add_argument("--content"); ap.add_argument("--flat", action="store_true")
    ap.add_argument("--limit-mb", type=float, default=29.5)
    a = ap.parse_args()
    out = os.path.abspath(a.out); bad = []
    depth = "*" if a.flat else "*/*"
    ads = sorted(d for d in glob.glob(os.path.join(out, depth)) if os.path.isdir(d))
    for d in ads:
        files = [f for f in os.listdir(d) if f.lower().endswith(".jpg")]
        got = set()
        for f in files:
            m = PAT.match(f)
            if not m or m["slug"] != os.path.basename(d): bad.append(f"bad name: {d}/{f}"); continue
            w, h = Image.open(os.path.join(d, f)).size
            if (w, h) != (int(m["w"]), int(m["h"])): bad.append(f"wrong pixels {w}x{h}: {f}")
            got.add((m["c"], m["size"], int(m["w"]), int(m["h"])))
        if got != EXPECT: bad.append(f"{os.path.relpath(d, out)}: has {len(files)} files, missing {sorted(EXPECT - got)}")
    if a.content:
        cfg = json.load(open(a.content))
        want = {(ad["slug"] if a.flat else os.path.join(ad["folder"], ad["slug"])) for ad in cfg["ads"]}
        have = {os.path.relpath(d, out) for d in ads}
        for x in sorted(want - have): bad.append(f"missing ad folder: {x}")
        for x in sorted(have - want): bad.append(f"extra folder not in content: {x}")
    print(f"{len(ads)} ad folders, {sum(len(os.listdir(d)) for d in ads)} files")
    parent = os.path.dirname(out)
    qa = os.path.join(parent, "qa_sheets"); os.makedirs(qa, exist_ok=True)
    for c in range(1, 5):
        for s in ("landscape", "square", "portrait"):
            sheet(sorted(glob.glob(os.path.join(out, depth, f"*_C{c}_{s}_*.jpg"))), os.path.join(qa, f"{s}_C{c}.jpg"))
    print(f"contact sheets: {qa}  (open and look at every one)")
    smp = os.path.join(parent, "whatsapp_samples"); os.makedirs(smp, exist_ok=True)
    for d, s in zip(ads[:2], ("square", "portrait")):
        for f in glob.glob(os.path.join(d, f"*_C1_{s}_*.jpg")): shutil.copy(f, smp)
    if os.path.exists(a.zip): os.remove(a.zip)
    with zipfile.ZipFile(a.zip, "w", zipfile.ZIP_STORED) as z:
        for root, _, files in os.walk(out):
            for f in sorted(files):
                if f.lower().endswith(".jpg"):
                    p = os.path.join(root, f); z.write(p, os.path.relpath(p, parent))
    with zipfile.ZipFile(a.zip) as z:
        if z.testzip() is not None: bad.append("zip test failed")
    mb = os.path.getsize(a.zip) / 1e6
    print(f"zip: {a.zip}  {mb:.1f} MB")
    if mb > a.limit_mb: bad.append(f"zip is {mb:.1f} MB, over {a.limit_mb} MB: re-render with --quality 76 (or 70), never split unless 912+ files make it impossible")
    if bad:
        print("\nFAILED:", *bad, sep="\n  "); sys.exit(1)
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
