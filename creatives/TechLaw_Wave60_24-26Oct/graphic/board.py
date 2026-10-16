# One board per campaign: every single and every carousel card, captioned. Run: python3 board.py c1 "title"
import sys, importlib, html
camp, title = sys.argv[1], sys.argv[2]
ADS = importlib.import_module("copy_" + camp).ADS
singles = [a for a in ADS if a["kind"] == "single"]; cars = [a for a in ADS if a["kind"] == "carousel"]
def cap(a): return '<div class="cap"><b>%s</b> %s</div>' % (a["id"], html.escape(a["reader"]))
h = ['<div class="t">%s</div><div class="s">%d singles (4:5) and %d carousels (1:1, swipe left to right). Every ad has its own picture, palette, typeface and layout.</div>' % (html.escape(title), len(singles), len(cars))]
h.append('<div class="row">' + "".join('<div class="cell"><img src="out/tlg_%s_single.jpg" style="width:330px;height:412px">%s</div>' % (a["id"], cap(a)) for a in singles) + '</div>')
for a in cars:
    h.append('<div class="car"><div class="cl">CAROUSEL %s<br><span>%s</span></div>' % (a["id"], html.escape(a["reader"])) +
             "".join('<img src="out/tlg_%s_card%d.jpg" style="width:400px;height:400px">' % (a["id"], i) for i in range(1, len(a["cards"]) + 1)) + '</div>')
css = ("@font-face{font-family:P;font-weight:800;src:url('fonts/poppins-latin-800-normal.woff2')}@font-face{font-family:I;font-weight:600;src:url('fonts/inter-latin-600-normal.woff2')}"
       "body{margin:0;padding:50px;background:#F4F1EA;font-family:I;width:2550px}.t{font-family:P;font-weight:800;font-size:58px;color:#1b1b1b}"
       ".s{font-size:26px;color:#333;margin:8px 0 34px}.row{display:flex;gap:20px;flex-wrap:wrap}.cell{width:330px}"
       ".cell img,.car img{display:block;border-radius:10px;box-shadow:0 4px 14px rgba(0,0,0,.12)}.cap{font-size:20px;line-height:1.3;margin-top:10px;color:#222}"
       ".cap b{font-family:P;font-weight:800}.car{display:flex;gap:16px;align-items:center;margin-top:34px}"
       ".cl{width:300px;font-family:P;font-weight:800;font-size:28px;color:#1b1b1b}.cl span{font-family:I;font-weight:600;font-size:21px;color:#333}")
open("board_%s.html" % camp, "w").write('<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (css, "".join(h)))
