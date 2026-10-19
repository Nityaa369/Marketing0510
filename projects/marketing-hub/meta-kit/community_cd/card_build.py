"""Render the 20 fixed cards (1080x1350) from cards.json + photos/ill_NN.png.

Self-contained so it can run in any sandbox with Python and node playwright:
  python3 card_build.py cards.json OUTDIR
"""
import json, os, subprocess, sys

W, H = 1080, 1350
BAR = 220


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def on(bg):
    l = lum(bg)
    return "#FFFFFF" if 1.05 / (l + 0.05) >= (l + 0.05) / 0.05 else "#111111"


def cutout(src, dst):
    """White background -> transparent (only white connected to the cell border, so white
    shirts and papers stay), soft edge, neighbour slivers dropped, trimmed to the figure."""
    import numpy as np
    from PIL import Image, ImageFilter
    from scipy import ndimage
    a = np.asarray(Image.open(src).convert("RGB")).astype(float)
    a = np.minimum(255, a * 255 / 236)
    white = a.min(axis=2) >= 244
    lab, _ = ndimage.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    alpha = Image.fromarray(np.where(bg, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    al = np.asarray(alpha).astype(float)
    # keep the figure, drop slivers of neighbouring cells: components smaller than 4% of the largest
    lab2, n2 = ndimage.label(al > 12)
    if n2 > 1:
        sizes = ndimage.sum(np.ones_like(al), lab2, range(1, n2 + 1))
        keep = [i + 1 for i, z in enumerate(sizes) if z >= 0.04 * sizes.max()]
        al = al * np.isin(lab2, keep)
    rgba = np.dstack([a, al]).astype("uint8")
    im = Image.fromarray(rgba, "RGBA")
    ys, xs = np.where(al > 12)
    im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).save(dst)


FONTS = ("https://fonts.googleapis.com/css2?family=Inter:wght@600;800;900"
         "&family=Caveat:wght@700&family=Kalam:wght@700&display=block")


def card(c, img):
    k1, k2 = c["head"]
    note = c["notes"][0].replace("\n", "<br>")
    hand = c["hand"]
    btn_t = on(c["button"])
    head_px = 76 if max(len(k1), len(k2)) <= 19 else 66
    top = 230 + 44 * (len(c['banner']) > 30)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{FONTS}"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:{c['paper']};font-family:Inter;color:{c['ink']};position:relative}}
.brand{{position:absolute;left:56px;top:44px;font:900 40px Inter;letter-spacing:-1px}}
.brand span{{color:{c['button']}}}
.tag{{position:absolute;right:56px;top:50px;font:800 22px Inter;letter-spacing:1.5px;border:3px solid {c['ink']};border-radius:30px;padding:6px 16px}}
.callout{{position:absolute;left:56px;top:128px;max-width:700px;background:{c['hi']};color:#111;font:800 34px/1.18 Inter;
  letter-spacing:.3px;padding:12px 18px;box-shadow:6px 6px 0 rgba(0,0,0,.12)}}
.img{{position:absolute;right:0;bottom:{BAR}px;width:620px;height:760px;object-fit:contain;object-position:right bottom}}
.copy{{position:absolute;left:56px;top:{top}px;width:540px;display:flex;flex-direction:column;gap:28px}}
.head{{font:900 {head_px}px/1.0 Inter;letter-spacing:-2.5px;text-wrap:balance}}
.head b{{display:block;color:{c['banner_bg']};font-weight:900}}
.body{{font:600 30px/1.32 Inter;text-wrap:pretty;max-width:470px}}
.note{{position:absolute;right:56px;top:228px;background:#FFF7C2;transform:rotate(5deg);padding:16px 18px;
  font-family:'{hand}';font-weight:700;font-size:{40 if hand == 'Caveat' else 32}px;line-height:1.05;color:#2a2a2a;
  box-shadow:0 8px 14px rgba(0,0,0,.15);text-align:center;min-width:170px}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:{BAR}px;background:#FFFFFF;border-top:4px solid {c['ink']};
  display:flex;align-items:center;justify-content:space-between;padding:0 56px}}
.bar h3{{font:900 33px Inter;letter-spacing:-.5px}}
.bar p{{font:600 24px/1.35 Inter;margin-top:6px;color:#333}}
.btn{{background:{c['button']};color:{btn_t};font:900 50px Inter;letter-spacing:-.5px;padding:30px 44px;border-radius:18px;white-space:nowrap;
  box-shadow:0 9px 0 rgba(0,0,0,.25)}}
</style></head><body>
<div class="brand">Law<span>Sikho</span></div>
<div class="tag">CONTRACT DRAFTING</div>
<img class="img" src="{img}">
<div class="callout">{c['banner']}</div>
<div class="copy"><div class="head">{k1}<b>{k2}</b></div>
<div class="body">{c['hook']}</div></div>
<div class="note">{note}</div>
<div class="bar"><div><h3>Contract Drafting Community</h3>
<p>21 days · Live online · From zero<br>₹200 incl. GST · Refundable</p></div>
<div class="btn">Join for ₹200 →</div></div>
</body></html>"""


JS = r"""
const pw = require(process.env.PW || 'playwright');
(async () => {
  const b = await pw.chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1350}});
  const [dir, out, ...ids] = process.argv.slice(2);
  for (const id of ids) {
    await p.goto('file://' + dir + '/card_' + id + '.html', {waitUntil:'networkidle'});
    await p.evaluate(() => document.fonts.ready);
    const bad = await p.evaluate(() => {
      const r = s => document.querySelector(s).getBoundingClientRect();
      const body = r('.body'), bar = r('.bar'), head = r('.head'), co = r('.callout'), note = r('.note');
      const out = [];
      if (body.bottom > bar.top - 10) out.push('body hits bar ' + Math.round(body.bottom));
      if (co.bottom > head.top - 8) out.push('callout hits head');
      if (head.right > note.left - 6 && head.top < note.bottom) out.push('head hits note');
      if (body.bottom > 830) out.push('body low ' + Math.round(body.bottom));
      return out;
    });
    if (bad.length) console.log('CHECK', id, bad.join('; '));
    await p.screenshot({path: out + '/cd_card_' + id + '.png'});
  }
  await b.close();
})();
"""

if __name__ == "__main__":
    cards = json.load(open(sys.argv[1]))
    out = os.path.abspath(sys.argv[2])
    here = os.path.dirname(os.path.abspath(sys.argv[1]))
    os.makedirs(out, exist_ok=True)
    for c in cards:
        src = os.path.join(here, "photos", f"ill_{c['id']}.png")
        img = os.path.join(here, "photos", f"cut_{c['id']}.png")
        cutout(src, img)
        open(os.path.join(here, f"card_{c['id']}.html"), "w").write(card(c, "file://" + img))
    open(os.path.join(here, "card_render.js"), "w").write(JS)
    subprocess.run(["node", os.path.join(here, "card_render.js"), here, out, *[c["id"] for c in cards]], check=True)
