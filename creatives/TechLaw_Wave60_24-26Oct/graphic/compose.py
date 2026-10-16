# Graphic wave composer. Every ad: reader call-out band on the top 10%, a big buy button on the
# bottom 15%, the picture between them (scaled to keep the person whole), and the hook set by hand
# per ad so no two ads share a layout. Run: python3 compose.py c1  then  node shoot.js c1
# Images (img/<id>.png) are Higgsfield gpt_image_2_5 outputs; job ids in jobs_c1.json.
import os, sys, json, html, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FOOT = "LawSikho Tech Law Bootcamp · Rs 10 incl. GST · 3 live evenings · Refundable"
FONTS = {"Poppins": "poppins", "Bebas Neue": "bebas-neue", "Anton": "anton", "Playfair Display": "playfair-display",
         "DM Serif Display": "dm-serif-display", "Archivo Black": "archivo-black", "Montserrat": "montserrat",
         "Oswald": "oswald", "Fraunces": "fraunces", "Space Grotesk": "space-grotesk", "League Spartan": "league-spartan", "Inter": "inter"}
FIT = ("<script>document.fonts.ready.then(()=>{document.querySelectorAll('[data-fit]').forEach(e=>{let s=parseFloat(getComputedStyle(e).fontSize);"
       "const H=e.parentElement.clientHeight-8,Wd=e.parentElement.clientWidth-8;while((e.scrollHeight>H||e.scrollWidth>Wd)&&s>20){s-=1;e.style.fontSize=s+'px'}})})</script>")

def face_css():
    return "".join("@font-face{font-family:'%s';font-weight:%d;src:url('../fonts/%s-latin-%d-normal.woff2')}" % (f, w, st, w)
                   for f, st in FONTS.items() for w in range(400, 1000, 100)
                   if os.path.exists(os.path.join(HERE, "fonts", "%s-latin-%d-normal.woff2" % (st, w))))

def hi(text, words, color):
    t = html.escape(text)
    for w in words or []:
        t = t.replace(html.escape(w), '<span style="color:%s">%s</span>' % (color, html.escape(w)), 1)
    return t

def card(a, c, idx, size):
    W, H = size; sq = W == H
    s = dict(a["style"]); s.update(c.get("style", {}))
    ac, ink, font = s["accent"], s["ink"], s["font"]
    band_h, btn_h = round(H * .10), round(H * .15)
    sc, top = s.get("place", (1.0, 0))
    iw = W * sc; mask = "" if sc >= 1 else ("-webkit-mask-image:linear-gradient(to right,transparent,#000 7%,#000 93%,transparent),"
                                              "linear-gradient(to bottom,transparent,#000 8%,#000 92%,transparent);-webkit-mask-composite:source-in;")
    p = ['<img class="bg" src="../img/%s.png" style="left:%dpx;top:%dpx;width:%dpx;%s">' % (c["img"], (W - iw) / 2, top, iw, mask)]
    band = a["cards"][0]["label"]
    p.append('<div class="band" style="height:%dpx;background:%s"><div data-fit style="font-family:\'%s\';font-size:%dpx;color:%s">%s</div></div>'
             % (band_h, s.get("band_bg", ac), s.get("band_font", "Inter"), 46 if sq else 56, s.get("band_ink", "#fff"), html.escape(band)))
    b = []
    if idx > 0 and c.get("label"):
        b.append('<div class="kick" style="color:%s">%s</div>' % (ac, html.escape(c["label"])))
    if c.get("head"):
        b.append('<div class="head" style="font-family:\'%s\';color:%s;%s">%s</div>' % (font, ink, s.get("head_css", ""), hi(c["head"], c.get("hi"), ac)))
    if c.get("sub"):
        b.append('<div class="sub" style="color:%s;%s">%s</div>' % (ink, s.get("sub_css", ""), html.escape(c["sub"])))
    if c.get("define"):
        b.append('<div class="define" style="border-color:%s;color:%s;%s">Tech law is the legal work tech companies need: contracts, privacy, compliance and disputes.</div>' % (ac, ink, s.get("define_css", "")))
    if c.get("swipe"):
        b.append('<div class="swipe" style="color:%s">%s &rarr;</div>' % (ac, html.escape(c["swipe"])))
    p.append('<div class="box" style="%s">%s</div>' % (s["box"], "".join(b)))
    p.append('<div class="btn" style="height:%dpx;background:%s;%s"><div class="bt" style="font-family:\'%s\';font-size:%dpx">%s &rarr;</div><div class="bf">%s</div></div>'
             % (btn_h - 28, s.get("btn_bg", ac), s.get("btn_css", ""), s.get("btn_font", font), 62 if sq else 76, html.escape(c.get("btn", "Join for Rs 10")), FOOT))
    p += c.get("extra", [])
    css = (face_css() + "*{margin:0;padding:0;box-sizing:border-box}"
           "body{width:%dpx;height:%dpx;overflow:hidden;position:relative;font-family:Inter,sans-serif;background:%s}"
           ".bg{position:absolute;height:auto}.band{position:absolute;top:0;left:0;right:0;z-index:3;display:flex;align-items:center;padding:0 44px}"
           ".band div{font-weight:800;line-height:1.08;letter-spacing:-.005em;width:100%%}"
           ".box{position:absolute;z-index:2}.kick{font-size:32px;font-weight:800;margin-bottom:12px}"
           ".head{line-height:1.02;letter-spacing:-.01em}.sub{font-size:30px;line-height:1.32;font-weight:600;margin-top:18px}"
           ".define{margin-top:20px;font-size:26px;line-height:1.35;font-weight:600;border-left:6px solid;padding:4px 0 4px 16px}"
           ".swipe{margin-top:22px;font-size:29px;font-weight:800}"
           ".btn{position:absolute;left:28px;right:28px;bottom:28px;z-index:3;border-radius:26px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;box-shadow:0 12px 30px rgba(0,0,0,.22)}"
           ".bt{font-weight:800;line-height:1}.bf{margin-top:12px;font-size:21px;font-weight:700;letter-spacing:.01em}" % (W, H, s.get("bg", "#fff")))
    return '<!doctype html><html><head><meta charset="utf-8"><style>%s%s</style></head><body>%s%s</body></html>' % (css, s.get("css", ""), "".join(p), FIT)

if __name__ == "__main__":
    camp = sys.argv[1]; ADS = importlib.import_module("copy_" + camp).ADS
    os.makedirs(os.path.join(HERE, "html"), exist_ok=True); jobs = []
    for a in ADS:
        size = (1080, 1080) if a["kind"] == "carousel" else (1080, 1350)
        for i, c in enumerate(a["cards"]):
            name = "tlg_%s_%s" % (a["id"], "card%d" % (i + 1) if a["kind"] == "carousel" else "single")
            open(os.path.join(HERE, "html", name + ".html"), "w").write(card(a, c, i, size))
            jobs.append({"name": name, "w": size[0], "h": size[1]})
    json.dump(jobs, open(os.path.join(HERE, "html", "jobs_%s.json" % camp), "w")); print("wrote", len(jobs))
