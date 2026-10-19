"""Contract Drafting torn-paper set v4: divyanshu's supplied ad (src/template_01.webp) with the
hero swapped per ICP from his supplied grid (src/heroes_grid.webp), and the text layer re-set.

python3 build.py            # all 20 -> out/cd_torn_NN.png (1024x1536, the template's size)
python3 build.py 01 04      # some
Kept from the template: paper, torn hole and fringe, LawSikho logo, the two title strips.
Changed per ICP: hero, ICP tape (bigger), hook, supporting line, button (bigger) + pop-up line.
"""
import json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
HOOKS = os.path.join(ROOT, "docs", "COMMUNITY_HOOKS_CD_LEGALAI_20each_2026-10-19.md")
W, H = 1024, 1536

# grid cell (row, col) for each ICP, matched by the character descriptions
HERO_CELL = {"01": (0, 0), "02": (0, 1), "03": (0, 2), "04": (0, 3), "05": (0, 4),
             "06": (1, 0), "07": (1, 1), "08": (1, 3), "09": (2, 0), "10": (2, 1),
             "11": (2, 2), "12": (1, 4), "13": (3, 0), "14": (3, 1), "15": (2, 3),
             "16": (2, 4), "17": (3, 2), "18": (3, 3), "19": (3, 4), "20": (3, 5)}

# pop-up line on the button: the CTA lead-in from the hooks file, or a calendar-true one
POPUP = {"03": "Build your first practice.", "05": "Draft it yourself.", "06": "Add startup clients.",
         "07": "Work from your own city.", "10": "Work from anywhere.", "11": "Draft for companies.",
         "12": "Draft the deal papers.", "13": "Write the contracts.", "14": "Draft the deals you close.",
         "16": "From review to drafting.", "17": "Draft for founders.", "18": "Go beyond sale deeds.",
         "19": "Start while in college."}


def load_icps():
    txt = open(HOOKS, encoding="utf-8").read()
    cd = txt.split("## LAWSIKHO · CONTRACT DRAFTING COMMUNITY")[1].split("## LAWSIKHO · LEGAL AI PROGRAM")[0]
    out = {}
    for block in re.split(r"\n(?=\d\d\. )", cd):
        m = re.match(r"(\d\d)\. ", block)
        if not m:
            continue
        g = lambda k: re.search(rf"{k}: (.+)", block).group(1).strip()
        cta = g("CTA")
        lead = cta.split("Join the Contract Drafting Community")[0].strip()
        out[m.group(1)] = dict(id=m.group(1), banner=g("Audience banner"), hook=g("HOOK"),
                               support=g("Supporting copy"), popup=lead or POPUP[m.group(1)])
    return out


def grid_cells():
    g = np.asarray(Image.open(os.path.join(HERE, "src", "heroes_grid.webp")).convert("RGB")).astype(int)
    white = g.min(axis=2) > 232

    def runs(frac):
        r, s = [], None
        for i, v in enumerate(frac > 0.9):
            if v and s is None: s = i
            if not v and s is not None: r.append((s, i - 1)); s = None
        if s is not None: r.append((s, len(frac) - 1))
        return r

    def spans(gutters, size):
        cuts = [0] + [x for a, b in gutters for x in (a, b + 1)] + [size]
        return [(cuts[i], cuts[i + 1]) for i in range(0, len(cuts), 2) if cuts[i + 1] - cuts[i] > 100]

    rows = spans(runs(white.mean(axis=1)), g.shape[0])
    return [[(x0, y0, x1, y1) for x0, x1 in spans(runs(white[y0:y1].mean(axis=0)), g.shape[1])] for y0, y1 in rows]


def paper_fill(base, y0, y1):
    """Repaint rows y0..y1 as plain paper: colour from the row's clean margins, plus grain."""
    a = np.asarray(base).astype(float)
    rng = np.random.default_rng(7)
    for y in range(y0, y1):
        L = a[y, 4:30].mean(axis=0); R = a[y, W - 30:W - 4].mean(axis=0)
        t = np.linspace(0, 1, W)[:, None]
        a[y] = L * (1 - t) + R * t
    grain = ndimage.gaussian_filter(rng.normal(0, 5.5, (y1 - y0, W)), 0.8)
    blot = ndimage.gaussian_filter(rng.normal(0, 14, (y1 - y0, W)), 18)
    a[y0:y1] += (grain + blot)[:, :, None]
    # blend the seam over 12 px so no hard line
    out = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))
    m = np.zeros((H, W)); m[y0 + 12:y1 - 12] = 1
    m = ndimage.gaussian_filter(m, 6)
    return Image.composite(out, base, Image.fromarray((m * 255).astype("uint8")))


def compose(icp, cells, tmpl, mask):
    r, c = HERO_CELL[icp]
    x0, y0, x1, y1 = cells[r][c]
    hero = Image.open(os.path.join(HERE, "src", "heroes_grid.webp")).convert("RGB").crop((x0 + 2, y0 + 2, x1 - 2, y1 - 2))
    m = np.asarray(mask) > 127
    ys, xs = np.where(m)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    bw, bh = bx1 - bx0, by1 - by0
    s = max(bw / hero.width, (bh + 140) / hero.height) * 1.02
    hero = hero.resize((round(hero.width * s), round(hero.height * s)), Image.LANCZOS)
    hero = hero.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    hx, hy = int(bx0 + bw / 2 - hero.width / 2), int(by0 + 120)
    # backdrop: the hero's own top band stretched up and blurred, so the shifted hero leaves no gap
    band = hero.crop((0, 0, hero.width, 140)).resize((hero.width, hy - by0 + 160), Image.BILINEAR)
    canvas = Image.new("RGB", (W, H))
    canvas.paste(band.filter(ImageFilter.GaussianBlur(14)), (hx, by0 - 20))
    # hero top sits below the ICP tape so the face is never covered; desk and hands go behind the title strip
    fade = Image.new("L", hero.size, 255)
    fade.paste(Image.linear_gradient("L").resize((hero.width, 70)), (0, 0))
    canvas.paste(hero, (hx, hy), fade)
    # soft inner shadow under the torn edge
    d = ndimage.distance_transform_edt(m)
    shade = 1 - 0.45 * np.exp(-d / 16)
    ca = np.asarray(canvas).astype(float) * shade[:, :, None]
    canvas = Image.fromarray(np.clip(ca, 0, 255).astype("uint8"))
    base = Image.composite(canvas, tmpl, mask)
    return paper_fill(base, 1018, 1500)


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def page(d):
    words = d["banner"].split(" ")
    # two-line tape like the template: break near the middle
    half, acc, cut = len(d["banner"]) / 2, 0, 1
    for i, w in enumerate(words):
        acc += len(w) + 1
        if acc >= half: cut = i + 1; break
    tape = " ".join(words[:cut]) + "<br>" + " ".join(words[cut:])
    tape_px = 50 if len(d["banner"]) <= 30 else 44 if len(d["banner"]) <= 40 else 39
    hook_px = 44 if len(d["hook"]) <= 88 else 39
    sup_px = 28 if len(d["support"]) <= 95 else 25
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Caslon;font-weight:400;src:url('fonts/LibreCaslonText-400.ttf')}}
@font-face{{font-family:Caslon;font-weight:700;src:url('fonts/LibreCaslonText-700.ttf')}}
@font-face{{font-family:Archivo;src:url('fonts/ArchivoBlack-400.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;position:relative;background:url('base/base_{d['id']}.png');color:#111}}
.tape{{position:absolute;left:22px;top:84px;transform:rotate(-3deg);background:#FFE135;padding:16px 26px 14px;
  font:{tape_px}px/1.05 Archivo;color:#151515;letter-spacing:.3px;box-shadow:0 6px 12px rgba(0,0,0,.22);
  clip-path:polygon(1% 4%,8% 0,22% 3%,40% 0,58% 4%,76% 0,92% 3%,100% 0,98% 30%,100% 55%,97% 78%,100% 100%,84% 97%,66% 100%,48% 96%,30% 100%,12% 97%,0 100%,2% 70%,0 45%,3% 22%)}}
.copy{{position:absolute;left:52px;right:52px;top:1020px;height:272px;display:flex;flex-direction:column;justify-content:center;gap:16px;text-align:center}}
.hook{{font:700 {hook_px}px/1.16 Caslon;letter-spacing:-.4px;text-wrap:balance}}
.sup{{font:400 {sup_px}px/1.3 Caslon;color:#222;text-wrap:balance;padding:0 14px}}
.btn{{position:absolute;left:36px;right:36px;top:1346px;height:150px;background:#E31B23;border-radius:22px;
  display:flex;align-items:center;justify-content:center;text-align:center;font:700 46px/1.12 Caslon;color:#fff;letter-spacing:-.3px;white-space:nowrap;
  box-shadow:0 10px 0 #9E0F15,0 16px 26px rgba(0,0,0,.28)}}
.pop{{position:absolute;left:58px;top:1294px;transform:rotate(-4deg);background:#FFE135;color:#111;font:31px Archivo;
  padding:12px 22px;border-radius:14px;box-shadow:0 6px 12px rgba(0,0,0,.25);z-index:2;white-space:nowrap}}
.pop:after{{content:"";position:absolute;left:46px;bottom:-16px;border:9px solid transparent;border-top:12px solid #FFE135;border-left:14px solid #FFE135}}
.foot{{position:absolute;left:0;right:0;top:1505px;text-align:center;font:700 22px Caslon;letter-spacing:1px;color:#2a2a2a}}
</style></head><body>
<div class="tape">{tape}</div>
<div class="copy"><div class="hook">{d['hook']}</div><div class="sup">{d['support']}</div></div>
<div class="pop">{d['popup']}</div>
<div class="btn">Join the Contract Drafting<br>Community for ₹200 &rarr;</div>
<div class="foot">21 days · Live online · ₹200 incl. GST · Refundable</div>
</body></html>"""


JS = r"""
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1024,height:1536}});
  for (const id of process.argv.slice(2)) {
    await p.goto('file://' + __dirname + '/html_' + id + '.html'); await p.evaluate(() => document.fonts.ready);
    const bad = await p.evaluate(() => {
      const r = s => document.querySelector(s).getBoundingClientRect(); const o = [];
      const c = document.querySelector('.copy'); const kids = [...c.children].reduce((a,e)=>a+e.getBoundingClientRect().height,0) + 16;
      if (kids > 272) o.push('copy too tall ' + Math.round(kids));
      if (r('.sup').bottom > r('.pop').top - 4) o.push('support hits popup');
      if (r('.tape').right > 1010) o.push('tape too wide');
      const bt = document.querySelector('.btn'); if (bt.scrollWidth > bt.clientWidth + 2) o.push('btn text too wide');
      return o; });
    if (bad.length) console.log('CHECK', id, bad.join('; '));
    await p.screenshot({path: __dirname + '/out/cd_torn_' + id + '.png'});
  }
  await b.close(); })();
"""

if __name__ == "__main__":
    icps = load_icps()
    ids = sys.argv[1:] or sorted(icps)
    cells = grid_cells()
    tmpl = Image.open(os.path.join(HERE, "src", "template_01.webp")).convert("RGB")
    mask = Image.open(os.path.join(HERE, "src", "hole_mask.png")).convert("L")
    os.makedirs(os.path.join(HERE, "base"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for i in ids:
        compose(i, cells, tmpl, mask).save(os.path.join(HERE, "base", f"base_{i}.png"))
        open(os.path.join(HERE, f"html_{i}.html"), "w", encoding="utf-8").write(page(icps[i]))
    open(os.path.join(HERE, "render.js"), "w").write(JS)
    subprocess.run(["node", os.path.join(HERE, "render.js"), *ids], check=True)
    json.dump(icps, open(os.path.join(HERE, "icps.json"), "w"), ensure_ascii=False, indent=1)
    print("rendered", len(ids))
