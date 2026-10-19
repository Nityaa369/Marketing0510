"""Render the 20 torn-paper Contract Drafting ads to out/cd_art_NN.png (1080x1350).

python3 build.py            # all ads
python3 build.py 01 07      # some ads
Photos are read from photos/cd_NN.jpg; a missing photo renders a labelled placeholder.
"""
import math, os, random, subprocess, sys
from ads import ADS, CTA, FOOTER

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1350
HOLE = (190, 205, 890, 735)  # x0, y0, x1, y1


def lum(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def on(bg):
    """White or near-black text, whichever contrasts more with bg."""
    l = lum(bg)
    return "#FFFFFF" if (1.05 / (l + 0.05)) >= ((l + 0.05) / 0.05) else "#111111"


def bright(hexc):
    """Vivid version of the ad's accent: same hue, saturation 95%, lightness 50%."""
    import colorsys
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.15:  # near-black accents get the house red-orange
        return "#FF4F1F"
    r, g, b = colorsys.hls_to_rgb(h, 0.50, 0.95)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


def torn_path(rng, x0, y0, x1, y1, step=14, amp=13):
    """Jagged closed path around a rounded blob inside the box."""
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    n = int(2 * math.pi * max(rx, ry) / step)
    wob = [rng.uniform(-1, 1) for _ in range(6)]
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        # squarish superellipse so the hole fills its box like the reference
        c, s = math.cos(t), math.sin(t)
        e = 0.38
        px = rx * math.copysign(abs(c) ** e, c)
        py = ry * math.copysign(abs(s) ** e, s)
        slow = sum(w * math.sin((k + 2) * t + k) for k, w in enumerate(wob)) * 9
        j = rng.uniform(-amp, amp) + slow
        nx, ny = (px / rx if rx else 0), (py / ry if ry else 0)
        norm = math.hypot(nx, ny) or 1
        pts.append((cx + px + j * nx / norm, cy + py + j * ny / norm))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def strip_clip(rng, n=26, amp=5):
    """Polygon clip-path (percent) for a torn paper strip."""
    top = [(i * 100 / n, rng.uniform(0, amp)) for i in range(n + 1)]
    bot = [(100 - i * 100 / n, 100 - rng.uniform(0, amp)) for i in range(n + 1)]
    return "polygon(" + ",".join(f"{x:.1f}% {y:.1f}%" for x, y in top + bot) + ")"


NOISE = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .09 0'/></filter>"
         "<rect width='100%25' height='100%25' filter='url(%23n)'/></svg>")


def html(ad):
    rng = random.Random(int(ad["id"]) * 7919)
    x0, y0, x1, y1 = HOLE
    outer = torn_path(rng, x0 - 24, y0 - 24, x1 + 24, y1 + 24, step=11, amp=16)
    inner = torn_path(rng, x0, y0, x1, y1, step=12, amp=10)
    photo = f"photos/cd_{ad['id']}.jpg"
    cut = f"photos/cut_{ad['id']}.png"
    has_photo = os.path.exists(os.path.join(HERE, photo))
    if os.path.exists(os.path.join(HERE, cut)):
        from PIL import Image
        cw, ch = Image.open(os.path.join(HERE, cut)).size
        fh = 500; fw = fh * cw / ch
        if fw > 600: fw = 600; fh = fw * ch / cw
        fx = (x0 + x1) / 2 - fw / 2; fy = 712 - fh
        img = (f"<defs><radialGradient id='bd' cx='50%' cy='38%' r='70%'><stop offset='0' stop-color='#FFFFFF'/>"
               f"<stop offset='1' stop-color='{ad['hi']}'/></radialGradient></defs>"
               f"<path d='{inner}' fill='url(#bd)'/>"
               f"<image href='../{cut}' x='{fx:.0f}' y='{fy:.0f}' width='{fw:.0f}' height='{fh:.0f}' clip-path='url(#hole)'/>")
    else:
      img = (f"<image href='../{photo}' x='{x0-40}' y='{y0-40}' width='{x1-x0+80}' height='{y1-y0+80}' "
           f"preserveAspectRatio='xMidYMid slice' clip-path='url(#hole)'/>") if has_photo else (
           f"<path d='{inner}' fill='#d8d2c8'/><text x='{(x0+x1)/2}' y='{(y0+y1)/2}' text-anchor='middle' "
             f"font-family='Inter' font-weight='800' font-size='34' fill='#8a8378'>PHOTO {ad['id']} PENDING</text>")
    s1, s2 = strip_clip(rng), strip_clip(rng)
    cta_bg = bright(ad["button"])
    bt, btn = on(ad["banner_bg"]), on(cta_bg)
    notes = [n.replace("\n", "<br>") for n in ad["notes"]]
    hand = ad["hand"]
    hsz = 38 if hand == "Caveat" else 31
    hook_px = 43 if len(ad["hook"]) <= 92 else 39
    ban_px = 33 if len(ad["banner"]) <= 42 else 29
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=DM+Serif+Display&family=Fraunces:opsz,wght@144,900&family=Abril+Fatface&family=Caveat:wght@600&family=Kalam&family=Inter:wght@600;800;900&display=block');
@font-face{{font-family:'Playfair Display';font-weight:900;src:url('../fonts/PlayfairDisplay-900.ttf')}}
@font-face{{font-family:'DM Serif Display';font-weight:400;src:url('../fonts/DMSerifDisplay-400.ttf')}}
@font-face{{font-family:'Fraunces';font-weight:900;src:url('../fonts/Fraunces-900.ttf')}}
@font-face{{font-family:'Abril Fatface';font-weight:400;src:url('../fonts/AbrilFatface-400.ttf')}}
@font-face{{font-family:'Caveat';font-weight:600;src:url('../fonts/Caveat-600.ttf')}}
@font-face{{font-family:'Kalam';font-weight:400;src:url('../fonts/Kalam-400.ttf')}}
@font-face{{font-family:'Inter';font-weight:600;src:url('../fonts/Inter-600.ttf')}}
@font-face{{font-family:'Inter';font-weight:800;src:url('../fonts/Inter-800.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden;background:{ad['paper']} url("{NOISE}");font-family:Inter;color:{ad['ink']};position:relative}}
.brand{{position:absolute;left:44px;top:34px;font:800 34px Inter;letter-spacing:-.5px}}
.brand b{{color:{ad['button']}}}
.pill{{position:absolute;right:44px;top:36px;border:3px solid {ad['ink']};border-radius:40px;padding:6px 18px;font:800 22px Inter;letter-spacing:1px}}
.banner{{position:absolute;left:50%;top:104px;transform:translateX(-50%) rotate({ad['tilt']*-0.6}deg);background:{ad['banner_bg']};color:{bt};
  font:800 {ban_px}px Inter;letter-spacing:.3px;padding:14px 26px;white-space:nowrap;box-shadow:0 6px 14px rgba(0,0,0,.18);max-width:1010px;text-align:center}}
svg.hole{{position:absolute;left:0;top:0}}
.title{{position:absolute;left:0;right:0;top:640px;text-align:center;transform:rotate({ad['tilt']}deg)}}
.strip{{display:inline-block;background:#FBF8F2;padding:8px 34px 16px;clip-path:var(--c);font-family:'{ad['title_font']}';font-weight:900;line-height:1.02;
  filter:drop-shadow(0 4px 6px rgba(0,0,0,.25))}}
.l1{{font-size:62px;--c:{s1}}}
.l2{{font-size:96px;margin-top:-6px;--c:{s2};background:linear-gradient(transparent 14%,{ad['hi']} 14%,{ad['hi']} 92%,transparent 92%),#FBF8F2}}
.copy{{position:absolute;left:64px;right:64px;top:858px;height:268px;display:flex;flex-direction:column;justify-content:center;gap:16px;text-align:center}}
.hook{{font:800 {hook_px}px/1.18 Inter;letter-spacing:-.6px;text-wrap:balance}}
.support{{font:600 27px/1.3 Inter;opacity:.86;padding:0 20px;text-wrap:balance}}
.cta{{position:absolute;left:50%;top:1136px;transform:translateX(-50%);background:{cta_bg};color:{btn};font:900 38px Inter;padding:26px 36px;border-radius:18px;
  white-space:nowrap;box-shadow:0 10px 0 rgba(0,0,0,.25),0 0 0 6px {cta_bg}33}}
.foot{{position:absolute;left:0;right:0;top:1272px;text-align:center;font:600 24px Inter;letter-spacing:1.5px}}
.note{{position:absolute;font-family:'{hand}';font-weight:{600 if hand=='Caveat' else 400};font-size:{hsz}px;line-height:1.05;color:{ad['note']};width:150px}}
.note:after{{content:"";display:block;width:110px;height:3px;background:{ad['note']};margin-top:8px;border-radius:3px;transform:rotate(-4deg)}}
.n1{{left:16px;top:260px;transform:rotate(-7deg)}} .n2{{right:16px;top:300px;transform:rotate(6deg);text-align:right}} .n2:after{{margin-left:auto}}
.n3{{left:16px;top:560px;transform:rotate(-5deg)}}
</style></head><body>
<div class="brand">Law<b>Sikho</b></div>
<div class="pill">CONTRACT DRAFTING COMMUNITY</div>
<svg class="hole" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
 <defs><clipPath id="hole"><path d="{inner}"/></clipPath>
  <filter id="sh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="6" stdDeviation="9" flood-opacity=".28"/></filter>
  <filter id="in"><feGaussianBlur stdDeviation="10"/></filter></defs>
 <path d="{outer}" fill="#FFFDF8" filter="url(#sh)"/>
 <path d="{outer}" fill="none" stroke="rgba(0,0,0,.08)" stroke-width="2"/>
 {img}
 <path d="{inner}" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="14" filter="url(#in)" clip-path="url(#hole)"/>
 <path d="{inner}" fill="none" stroke="#FFFDF8" stroke-width="3"/>
</svg>
<div class="banner">{ad['banner']}</div>
<div class="note n1">{notes[0]}</div><div class="note n2">{notes[1]}</div><div class="note n3">{notes[2]}</div>
<div class="title"><span class="strip l1">Learning the Art of</span><br><span class="strip l2">Contract Drafting</span></div>
<div class="copy"><div class="hook">{ad['hook']}</div>
<div class="support">{ad['support']}</div></div>
<div class="cta">{CTA}</div>
<div class="foot">{FOOTER}</div>
</body></html>"""


RENDER_JS = r"""
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const id of process.argv.slice(2)) {
    await p.goto('file://' + __dirname + '/html/cd_art_' + id + '.html', {waitUntil:'networkidle'});
    await p.evaluate(() => document.fonts.ready);
    const over = await p.evaluate(() => [...document.querySelectorAll('.copy,.banner,.cta,.note')]
      .filter(e => { const r = e.getBoundingClientRect(); return r.right > 1080 || r.left < 0 || r.bottom > 1350; })
      .map(e => e.className));
    if (over.length) console.log('OVERFLOW', id, over.join(','));
    await p.screenshot({ path: __dirname + '/out/cd_art_' + id + '.png' });
  }
  await b.close();
})();
"""

if __name__ == "__main__":
    want = set(sys.argv[1:])
    ids = []
    for ad in ADS:
        if want and ad["id"] not in want:
            continue
        open(os.path.join(HERE, "html", f"cd_art_{ad['id']}.html"), "w").write(html(ad))
        ids.append(ad["id"])
    js = os.path.join(HERE, "render.js")
    open(js, "w").write(RENDER_JS)
    subprocess.run(["node", js, *ids], check=True, env=dict(os.environ))
    print("rendered", len(ids))
