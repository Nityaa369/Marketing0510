"""Fit each 1024x1536 ad into Meta's 4:5, 1:1 and 9:16 without cropping or touching its words.

The whole ad is scaled to fit; the spare canvas is a wash made from the ad's own outer edge
(edge pixels extended, then blurred), per the 16 Oct rule "resize only, keep the whole ad".
9:16 sits a little high so the button clears the bottom 250 px Stories keep for the reply bar.
"""
import numpy as np
from PIL import Image, ImageFilter

SIZES = {"4x5": (1080, 1350), "1x1": (1080, 1080), "9x16": (1080, 1920)}


def fit(ad, W, H, top_bias=0.5):
    ad = ad.convert("RGB")
    s = min(W / ad.width, H / ad.height)
    if W == 1080 and H == 1920:
        s = 1500 / ad.height  # leave room above and below in Stories and Reels
    w, h = round(ad.width * s), round(ad.height * s)
    small = ad.resize((w, h), Image.LANCZOS)
    x = (W - w) // 2
    y = round((H - h) * top_bias)
    a = np.asarray(small)[4:-4, 4:-4]  # skip the outermost pixels (JPEG edge artefacts)
    pad = ((y + 4, H - y - h + 4), (x + 4, W - x - w + 4), (0, 0))
    bg = Image.fromarray(np.pad(a, pad, mode="edge")).filter(ImageFilter.GaussianBlur(28))
    bg.paste(small, (x, y))
    return bg, (x, y, w, h)


def make(src, out_base):
    ad = Image.open(src)
    boxes = {}
    for k, (W, H) in SIZES.items():
        im, box = fit(ad, W, H, 0.42 if k == "9x16" else 0.5)
        im.save(f"{out_base}_{k}.jpg", quality=84, optimize=True, progressive=True)
        boxes[k] = box
    return boxes
