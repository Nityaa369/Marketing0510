#!/usr/bin/env python3
"""
render_ads.py - Render every ad in a content JSON into 3 sizes x 4 colours = 12 JPGs per ad.

Sizes:   landscape 1200x628 · square 1200x1200 · portrait 960x1200
Colours: C1 = the ad's own accent, C2/C3/C4 = OKLab hue rotation +90 / +180 / +270
         (lightness and chroma are kept, so contrast stays the same in every colour).

Usage:
  python3 render_ads.py content.json OUT_DIR [--fonts /path/to/node_modules/@fontsource]
                        [--only slug1,slug2] [--quality 82] [--flat]

Output (default, categorised):  OUT_DIR/<folder>/<slug>/<slug>_C<n>_<size>_<W>x<H>.jpg
Output (--flat):                OUT_DIR/<slug>/<slug>_C<n>_<size>_<W>x<H>.jpg

Needs: pip install playwright pillow numpy  (and a Chromium that Playwright can launch)
Fonts: Poppins, Inter, Source Serif 4. Pass --fonts pointing at an @fontsource folder
       (npm i @fontsource/poppins @fontsource/inter @fontsource/source-serif-4),
       otherwise Google Fonts is linked (needs internet).
"""
import argparse, base64, html as H, json, os, sys
import numpy as np
from PIL import Image

SIZES = [("landscape", 1200, 628), ("square", 1200, 1200), ("portrait", 960, 1200)]
DELTAS = [0, 90, 180, 270]

# ---------------- colour: OKLab hue rotation ----------------
def _lin(c): return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def _gam(c): return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(np.clip(c, 0, None), 1 / 2.4) - 0.055)
M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])
def _to_lab(rgb): return np.cbrt(_lin(rgb) @ M1.T) @ M2.T
def _to_rgb(lab): return _gam(((lab @ np.linalg.inv(M2).T) ** 3) @ np.linalg.inv(M1).T)
def rot_hex(hx, deg):
    """Rotate a hex colour's hue by deg in OKLab, pulling chroma in until it fits sRGB."""
    hx = hx.lstrip('#'); rgb = np.array([[int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4)]])
    if deg:
        lab = _to_lab(rgb); C = np.hypot(lab[..., 1], lab[..., 2]); h = np.arctan2(lab[..., 2], lab[..., 1]) + np.radians(deg)
        for k in range(15):
            o = lab.copy(); f = 0.88 ** k
            o[..., 1] = C * f * np.cos(h); o[..., 2] = C * f * np.sin(h); r = _to_rgb(o)
            if not ((r < -0.002) | (r > 1.002)).any(): break
        rgb = np.clip(r, 0, 1)
    return '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in rgb[0])
def mix(a, b, t):
    a, b = a.lstrip('#'), b.lstrip('#'); ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))

# ---------------- html helpers ----------------
def px(n): return f"calc(var(--s)*{n}px)"
def e(t): return H.escape(str(t))
def uri(p):
    mt = "image/jpeg" if p.lower().endswith((".jpg", ".jpeg")) else "image/png"
    return f"data:{mt};base64," + base64.b64encode(open(p, "rb").read()).decode()

def font_css(fs):
    base = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'InterX',Inter,sans-serif;-webkit-font-smoothing:antialiased;position:relative;overflow:hidden}
.safe{position:absolute;display:flex;flex-direction:column} .safe div{flex-shrink:0} div{text-wrap:pretty} .bal{text-wrap:balance}"""
    if fs and os.path.isdir(fs):
        def ff(n, pkg, ws, st="normal"):
            return "".join(f"@font-face{{font-family:'{n}';font-weight:{w};font-style:{st};src:url('file://{fs}/{pkg}/files/{pkg}-latin-{w}-{st}.woff2')}}" for w in ws)
        css = ff("PoppinsX", "poppins", [600, 700, 800]) + ff("SSerif", "source-serif-4", [700, 800]) + ff("SSerif", "source-serif-4", [700, 800], "italic")
        if os.path.isdir(f"{fs}/inter"): css += ff("InterX", "inter", [500, 600, 700, 800])
        return "", css + base
    link = ('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@500;600;700;800'
            '&family=Source+Serif+4:ital,wght@0,700;0,800;1,700;1,800&display=block" rel="stylesheet">')
    return link, base

GOOGLE_ALIAS = {"PoppinsX": "Poppins", "SSerif": "'Source Serif 4'", "InterX,Inter": "Inter", "'InterX',": ""}

# ---------------- blocks ----------------
def brand_block(brand, acc, base_dir):
    def side(b):
        if not b: return "<span></span>"
        if b.get("type") == "image":
            return f'<img src="{uri(os.path.join(base_dir, b["path"]))}" style="height:{px(40)};width:auto">'
        if b.get("type") == "label":
            return f'<span style="font:800 {px(19)} InterX,Inter;color:{acc}">{e(b["text"])}</span>'
        t, a = b["text"], b.get("accent_part", "")
        inner = e(t[:len(t) - len(a)]) + (f'<span style="color:{b.get("accent_color", acc)}">{e(a)}</span>' if a else "")
        return f'<span style="font:800 {px(30)} PoppinsX;color:#141414">{inner}</span>'
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;gap:{px(16)}">'
            f'{side(brand.get("left"))}{side(brand.get("right"))}</div>')

def icp_block(acc, title, sit):
    return (f'<div style="background:{acc};color:#fff;padding:{px(13)} {px(20)};border-radius:{px(8)};align-self:flex-start">'
            f'<div class="bal" style="font:800 {px(34)} PoppinsX;line-height:1.12">{e(title)}</div>'
            + (f'<div class="bal" style="font:600 {px(22)} InterX,Inter;line-height:1.3;margin-top:{px(4)}">{e(sit)}</div>' if sit else "") + '</div>')

def head_block(ad, acc, size=56):
    serif = ad.get("headline_font") == "serif"
    fam = "SSerif" if serif else "PoppinsX"
    accent = ad.get("headline_accent", "")
    acc_span = (f'<span style="color:{acc};{"font-style:italic;" if serif else ""}">{e(accent)}</span>' if accent else "")
    return (f'<div class="bal" style="font:800 {px(size)} {fam};line-height:1.07;letter-spacing:{"0" if serif else "-.015em"};color:#141414">'
            f'{e(ad["headline"])}{acc_span}</div>')

def expl_block(acc, t, fs=26):
    return f'<div style="border-left:{px(8)} solid {acc};padding-left:{px(18)};font:800 {px(fs)} InterX,Inter;line-height:1.3;color:#141414">{e(t)}</div>'

def bullets_block(acc, dark, items, title=None, card=False):
    its = "".join(f'<div style="display:flex;gap:{px(12)};align-items:center;font:600 {px(23)} InterX,Inter;color:#1f2328;line-height:1.3">'
                  f'<span style="flex:none;width:{px(11)};height:{px(11)};background:{acc};border-radius:50%"></span>{e(t)}</div>' for t in items)
    ttl = f'<div style="font:800 {px(23)} PoppinsX;color:{dark}">{e(title)}</div>' if title else ""
    box = (f"background:#fff;border-radius:{px(12)};padding:{px(16)} {px(20)};box-shadow:0 {px(4)} {px(16)} rgba(0,0,0,.08);" if card else "")
    return f'<div style="{box}display:flex;flex-direction:column;gap:{px(9)}">{ttl}{its}</div>'

def cta_block(cta, fine, note=None):
    return (f'<div id="cta" style="margin-top:{px(30)}"><div style="font:800 {px(44)} PoppinsX;color:#fff;line-height:1.06">{e(cta)}</div>'
            f'<div style="font:600 {px(16)} InterX,Inter;color:#fff;opacity:.95;margin-top:{px(7)}">{e(fine)}</div>'
            + (f'<div style="font:500 {px(13)} InterX,Inter;color:#fff;opacity:.85;margin-top:{px(3)}">{e(note)}</div>' if note else "") + '</div>')

def page(link, css, W, Hh, acc, bg, dark, inner, gap, extra=""):
    tex = f"background-color:{bg};background-image:radial-gradient({mix(acc, bg, .78)} 1.4px,transparent 1.5px);background-size:24px 24px;"
    sx, sy = W * .1, Hh * .1
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8">{link}<style>{css}html,body{{width:{W}px;height:{Hh}px}}</style></head>'
            f'<body style="--s:1;{tex}">{extra}<div id="band" style="position:absolute;left:0;right:0;bottom:0;background:{dark}"></div>'
            f'<div class="safe" style="left:{sx}px;top:{sy}px;width:{W * .8}px;height:{Hh * .8}px;gap:{px(gap)}">{inner}</div></body></html>')

# ---------------- templates ----------------
def build(cfg, ad, size, W, Hh, deg, link, css, base_dir):
    acc = rot_hex(ad["accent"], deg); bg = mix(acc, "#ffffff", 0.88); dark = mix(acc, "#000000", 0.28)
    brand = ad.get("brand", cfg.get("brand", {}))
    top = brand_block(brand, acc, base_dir)
    icp = icp_block(acc, ad["icp_title"], ad.get("icp_situation"))
    cta = cta_block(ad.get("cta", cfg["cta"]), ad.get("fine", cfg["fine"]), ad.get("note", cfg.get("note")))
    land = size == "landscape"; tpl = ad.get("template", "list")
    value = (f'<div class="bal" style="font:800 {px(30)} InterX,Inter;line-height:1.25;color:{acc}">{e(ad["value_line"])}</div>'
             if ad.get("value_line") else "")
    expl = expl_block(acc, ad["explanation"]) if ad.get("explanation") else ""

    if tpl == "photo":
        photo = uri(os.path.join(base_dir, ad["photo"]))
        head = head_block(ad, acc, 50)
        if land:
            extra = f'<div style="position:absolute;left:0;top:0;bottom:0;width:{W * .42}px;background:url({photo}) center/cover"></div>'
            inner = (f'<div style="margin-left:{W * .36}px;display:flex;flex-direction:column;gap:{px(12)};flex:1 0 auto;justify-content:center">'
                     f'{top}{icp}{head}</div>{cta}')
            return page(link, css, W, Hh, acc, bg, dark, inner, 10, extra)
        ph = f'<div data-photo="1" style="flex:1 1 0;min-height:{px(420)};border-radius:{px(14)};background:url({photo}) center 25%/cover"></div>'
        inner = f'{top}{icp}{head}{ph}{expl_block(acc, ad["explanation"], 24) if ad.get("explanation") else ""}{cta}'
        return page(link, css, W, Hh, acc, bg, dark, inner, 18)

    if tpl == "numbered":
        items = ad["items"]; head = head_block(ad, acc, 46)
        def item(i, it, show_d=True):
            t, d = (it if isinstance(it, (list, tuple)) else (it, ""))
            return (f'<div style="display:flex;gap:{px(14)};align-items:flex-start;min-width:0">'
                    f'<span style="flex:none;width:{px(36)};height:{px(36)};border-radius:50%;background:{acc};color:#fff;font:800 {px(18)} InterX,Inter;display:flex;align-items:center;justify-content:center">{i}</span>'
                    f'<div style="line-height:1.25;min-width:0;flex:1"><div style="font:800 {px(23)} InterX,Inter;color:#141414">{e(t)}</div>'
                    + (f'<div style="font:500 {px(18)} InterX,Inter;color:#374151;margin-top:{px(2)}">{e(d)}</div>' if (show_d and d) else '') + '</div></div>')
        if land:
            lst = "".join(item(i + 1, it, False) for i, it in enumerate(items))
            inner = (f'{top}<div style="display:flex;gap:{px(32)};flex:1 0 auto;align-items:center">'
                     f'<div style="flex:0 0 46%;display:flex;flex-direction:column;gap:{px(12)}">{icp}{head}</div>'
                     f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:{px(8)}">{lst}</div></div>{cta}')
            return page(link, css, W, Hh, acc, bg, dark, inner, 10)
        cols = 2 if (len(items) > 5 and size == "square") or len(items) > 8 else 1
        lst = "".join(item(i + 1, it) for i, it in enumerate(items))
        grid = f'<div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:{px(14)} {px(26)}">{lst}</div>'
        inner = f'{top}{icp}{head}{value}{grid}{expl_block(acc, ad["explanation"], 23) if ad.get("explanation") else ""}<div style="flex:1 0 0"></div>{cta}'
        return page(link, css, W, Hh, acc, bg, dark, inner, 18)

    # default "list" template
    head = head_block(ad, acc, 56)
    bl = bullets_block(acc, dark, ad.get("bullets", []), ad.get("bullets_title"), ad.get("bullets_card", False)) if ad.get("bullets") else ""
    if land:
        right = value or bullets_block(acc, dark, ad.get("bullets", [])[:3], ad.get("bullets_title"), ad.get("bullets_card", False))
        inner = (f'{top}<div style="display:flex;gap:{px(36)};flex:1 0 auto;align-items:center">'
                 f'<div style="flex:0 0 52%;display:flex;flex-direction:column;gap:{px(14)}">{icp}{head}</div>'
                 f'<div style="flex:1;min-width:0;display:flex;flex-direction:column;gap:{px(14)}">{right}</div></div>{cta}')
        return page(link, css, W, Hh, acc, bg, dark, inner, 12)
    inner = f'{top}{icp}{head}{value}{expl}{bl}<div style="flex:1 0 0"></div>{cta}'
    return page(link, css, W, Hh, acc, bg, dark, inner, 22)

# Shrinks the --s scale until everything fits inside the safe box (centre 80%), then
# puts the full-bleed bottom band 22px (scaled) above the CTA.
FIT = """() => {
  const safe=document.querySelector('.safe'); let s=1.7;
  const ok=()=>{ if(safe.scrollHeight>safe.clientHeight+0.5) return false; const r=safe.getBoundingClientRect();
    for(const el of safe.querySelectorAll('div,span,img,svg')){const b=el.getBoundingClientRect(); if(b.width&&(b.right>r.right+1||b.left<r.left-1||b.bottom>r.bottom+1||b.top<r.top-1)) return false;}
    const ph=safe.querySelector('[data-photo]'); if(ph && ph.getBoundingClientRect().height < parseFloat(getComputedStyle(ph).minHeight)-1) return false;
    return true;};
  document.body.style.setProperty('--s',s);
  while(!ok() && s>0.4){ s-=0.01; document.body.style.setProperty('--s',s.toFixed(3)); }
  const c=document.getElementById('cta').getBoundingClientRect(); document.getElementById('band').style.top=Math.round(c.top-22*s)+'px';
  return s; }"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content"); ap.add_argument("out")
    ap.add_argument("--fonts", default=os.environ.get("FONTSOURCE_DIR", ""))
    ap.add_argument("--only", default=""); ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--flat", action="store_true")
    a = ap.parse_args()
    cfg = json.load(open(a.content)); base_dir = os.path.dirname(os.path.abspath(a.content))
    only = set(filter(None, a.only.split(",")))
    link, css = font_css(a.fonts)
    from playwright.sync_api import sync_playwright
    tmp_html = os.path.join(a.out, "_page.html"); tmp_png = os.path.join(a.out, "_shot.png"); os.makedirs(a.out, exist_ok=True)
    low = []
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        for ad in cfg["ads"]:
            if only and ad["slug"] not in only: continue
            od = os.path.join(a.out, ad["slug"]) if a.flat else os.path.join(a.out, ad["folder"], ad["slug"])
            os.makedirs(od, exist_ok=True)
            for ci, deg in enumerate(DELTAS):
                for size, W, Hh in SIZES:
                    html = build(cfg, ad, size, W, Hh, deg, link, css, base_dir)
                    if link:                                   # no local fonts: map to Google Fonts family names
                        for k, v in GOOGLE_ALIAS.items(): html = html.replace(k, v)
                    open(tmp_html, "w").write(html)
                    pg.set_viewport_size({"width": W, "height": Hh}); pg.goto("file://" + os.path.abspath(tmp_html))
                    pg.evaluate("document.fonts.ready"); s = pg.evaluate(FIT); pg.screenshot(path=tmp_png)
                    fn = os.path.join(od, f"{ad['slug']}_C{ci + 1}_{size}_{W}x{Hh}.jpg")
                    Image.open(tmp_png).convert("RGB").save(fn, "JPEG", quality=a.quality, optimize=True, progressive=True)
                    print(f"{os.path.basename(fn)}  scale={s:.2f}", flush=True)
                    if s < 0.7: low.append((os.path.basename(fn), round(s, 2)))
        br.close()
    for f in (tmp_html, tmp_png):
        if os.path.exists(f): os.remove(f)
    if low:
        print("\nWARNING: text scaled below 0.70 (copy too long for the frame, shorten it):", *low, sep="\n  ")

if __name__ == "__main__":
    main()
