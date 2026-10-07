"""NCA Canada skyline template (LawSikho), layout v2: centered.

Fixed: header, the complete maple leaf skyscape (a full leaf silhouette filled with the
reference ad's sunset skyline photo), three route pillars, "We show you how" sticker, terms
band, JOIN NOW button, footer. Variable per ad: the hook (call-out question) and the prize
line (value proposition). Hook and prize sit centered above the leaf, so the face stays
balanced for any hook length.

Spelling: "practice"/"practicing" everywhere, on Ruchika's instruction of 7 Oct 2026 (the
Indian-English verb form "practise" was flagged and overruled; see README).

Canvas 1080 x 1350 (Meta 4:5). Fonts: Inter (installed). Assets in assets/ are cut from the
reference ad in reference/original.webp.
"""

DEFAULTS = dict(
    # VARIABLE PER AD. Wrap the red part in <em>...</em>.
    hook="A lawyer who keeps thinking <em>about Canada?</em>",
    prize="You could <em>practice law in Canada.</em>",
    # Height budgets before the fitter shrinks the type (px).
    hook_max_height=196, hook_max_px=100,
    prize_max_height=108, prize_max_px=68,
    # FIXED FOR THE WAVE. Three route pillars: NCA exams, then bar licensing, then practice.
    pillars=[
        ("icon_nca.png", "NCA exams", "A direct pathway toward Canadian bar eligibility. <em>Open book, written online from India.</em> A session every month."),
        ("icon_bar.png", "Canadian bar", "Then bar licensing. You become eligible to apply."),
        ("icon_laptop.png", "Practice in Canada", "Same craft, Canadian clients and courts."),
    ],
    sticker="We show you how.",
    band_left_big="Rs 10. Refundable.",
    band_left_small="Rs 10 incl. GST. Refund anytime.",
    band_right_big="3 DAYS.<br>9 HOURS.",
    band_right_small="LIVE ONLINE",
    button="JOIN NOW",
    burst="ONLY<br>&#8377;10 !!",
    dates="31 Oct to 2 Nov",
    foot_mid="LIVE ONLINE",
    foot_right="&#8377;10 INCL. GST",
    bg="#FEFDF7",
    red="#F2371D",
    ink="#15121A",
    assets="../assets",
)

# Complete 11-point maple leaf with stem, drawn once, filled with the skyline photo.
LEAF_PATH = "M383.8 351.7c2.5-2.5 105.2-92.4 105.2-92.4l-17.5-7.5c-10-4.9-7.4-11.5-5-17.4 2.4-7.6 20.1-67.3 20.1-67.3s-47.7 10-57.7 12.5c-7.5 2.4-10-2.5-12.5-7.5s-15-32.4-15-32.4-52.6 59.9-55.1 62.3c-10 7.5-20.1 0-17.6-10 0-10 27.6-129.6 27.6-129.6s-30.1 17.4-40.1 22.4c-7.5 5-12.6 5-17.6-5C293.5 72.3 255.9 0 255.9 0s-37.5 72.3-42.5 79.8c-5 10-10 10-17.6 5-10-5-40.1-22.4-40.1-22.4s27.6 119.6 27.6 129.6c2.5 10-7.5 17.5-17.5 10-2.5-2.5-55.1-62.3-55.1-62.3s-12.5 27.5-15 32.4c-2.5 5.1-5 10-12.5 7.5-10-2.5-57.7-12.5-57.7-12.5s17.7 59.7 20.1 67.3c2.4 6 5 12.5-5 17.4L23 259.3s102.6 89.9 105.2 92.4c5.1 5 10 7.5 5.1 22.5-5.1 15-10.1 35.1-10.1 35.1s95.2-20.1 105.3-22.6c8.7-.9 18.3 2.5 18.3 12.5S241 512 241 512h30s-5.8-102.7-5.8-112.8 9.5-13.4 18.3-12.5c10 2.5 105.3 22.6 105.3 22.6s-5-20.1-10.1-35.1c-4.9-15 0-17.5 5.1-22.5z"

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,sans-serif;background:%(bg)s;color:%(ink)s;display:flex;flex-direction:column;padding:34px 44px 30px}
em{font-style:normal;color:%(red)s}
.hdr{display:flex;align-items:center;justify-content:center;gap:26px;height:92px;flex:none}
.hdr img{height:92px;width:auto}
.hdr .div{width:3px;height:84px;background:#2B2A33;opacity:.75}
.copy{flex:none;text-align:center;margin-top:20px}
.hook{font-size:%(hook_max_px)dpx;font-weight:900;line-height:1.0;letter-spacing:-.04em;word-spacing:-.03em;margin:0 auto;max-width:980px}
.prize{font-size:%(prize_max_px)dpx;font-weight:900;line-height:1.04;letter-spacing:-.035em;margin:18px auto 0;max-width:920px}
.leafbox{flex:1;min-height:140px;display:flex;align-items:center;gap:34px;margin-top:10px}
.rule{flex:1;height:4px;border-radius:2px}
.rule.l{background:linear-gradient(90deg,rgba(242,55,29,0),rgba(242,55,29,.5))}
.rule.r{background:linear-gradient(90deg,rgba(242,55,29,.5),rgba(242,55,29,0))}
.leafwrap{height:100%%;aspect-ratio:1/1;position:relative}
.leafwrap svg{position:absolute;inset:0;width:100%%;height:100%%;filter:drop-shadow(0 10px 22px rgba(242,55,29,.22))}
.pillars{display:flex;flex:none;margin-top:10px}
.pil{flex:1;text-align:center;padding:0 14px}
.pil+.pil{border-left:3px solid #E6E2DB}
.pil img{height:104px;width:auto}
.pt{font-size:32px;font-weight:900;letter-spacing:-.02em;margin-top:6px}
.pd{font-size:23px;font-weight:600;line-height:1.22;margin-top:4px;color:#2A2730}
.pd em{font-weight:800}
.sticker{align-self:center;background:#FFF04A;font-size:34px;font-weight:900;letter-spacing:-.02em;padding:6px 22px 8px;border-radius:8px;transform:rotate(-2deg);margin-top:12px;box-shadow:0 6px 14px rgba(0,0,0,.10)}
.band{display:flex;flex:none;background:#FEECE7;border-radius:16px;margin-top:12px;padding:16px 28px}
.cell{flex:1;display:flex;align-items:center;gap:22px}
.cell+.cell{border-left:3px solid #E9CFC7;padding-left:30px}
.cell img{height:84px;width:auto}
.cb{font-size:38px;font-weight:900;line-height:1.02;letter-spacing:-.03em}
.cb.red{color:%(red)s;text-transform:uppercase}
.cs{font-size:23px;font-weight:600;color:#2A2730;margin-top:6px;line-height:1.2}
.cs.caps{font-weight:800;letter-spacing:.02em;text-transform:uppercase;color:%(ink)s;font-size:25px}
.btnrow{position:relative;flex:none;margin-top:18px}
.btn{background:%(red)s;color:#fff;border-radius:60px;height:104px;display:flex;align-items:center;padding:0 44px;box-shadow:0 10px 24px rgba(242,55,29,.35)}
.bt{font-size:56px;font-weight:900;letter-spacing:-.02em;flex:1;text-align:center;padding-right:140px}
.arrow{font-size:70px;font-weight:900;margin-left:auto}
.burst{position:absolute;right:160px;top:-34px;width:210px;height:172px;background:url('data:image/svg+xml;utf8,<svg xmlns=%%22http://www.w3.org/2000/svg%%22 viewBox=%%220 0 230 190%%22><polygon fill=%%22%%23FFE64A%%22 stroke=%%22%%23F2371D%%22 stroke-width=%%226%%22 points=%%22115,6 135,30 165,14 172,44 206,40 198,72 228,88 206,112 224,142 190,148 190,182 158,168 140,186 115,160 88,186 70,168 38,182 38,148 6,142 24,112 2,88 32,72 24,40 58,44 65,14 95,30%%22/></svg>') no-repeat center/contain;display:flex;align-items:center;justify-content:center;text-align:center;font-size:40px;font-weight:900;line-height:.95;color:%(ink)s;transform:rotate(6deg)}
.burst b{color:%(red)s}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:18px;flex:none;font-size:25px;font-weight:800;letter-spacing:.03em;text-transform:uppercase}
.foot div{display:flex;align-items:center;gap:16px}
.foot img{height:42px;width:auto}
"""

FIT_JS = """
<script>
// Grow or shrink the block to its height budget: short hooks get bigger type, long hooks
// smaller, and the leaf keeps the leftover space, so the face stays balanced.
function fit(sel,maxH,minPx,maxPx){var e=document.querySelector(sel);var s=maxPx;e.style.fontSize=s+'px';
while(e.scrollHeight>maxH&&s>minPx){s-=2;e.style.fontSize=s+'px';}}
fit('.hook',%(hook_max_height)d,52,%(hook_max_px)d);fit('.prize',%(prize_max_height)d,40,%(prize_max_px)d);
</script>"""


def render(cfg):
    c = dict(DEFAULTS); c.update(cfg)
    a = c["assets"]
    pil = "".join(
        f'<div class="pil"><img src="{a}/{ic}"><div class="pt">{t}</div><div class="pd">{d}</div></div>'
        for ic, t, d in c["pillars"])
    leaf = f"""<svg viewBox="0 0 512 512" preserveAspectRatio="xMidYMid meet"><defs><clipPath id="leaf"><path d="{LEAF_PATH}"/></clipPath></defs>
<image href="{a}/skyline_fill.png" x="0" y="0" width="512" height="512" preserveAspectRatio="xMidYMid slice" clip-path="url(#leaf)"/>
<path d="{LEAF_PATH}" fill="none" stroke="{c['red']}" stroke-width="6" stroke-linejoin="round"/></svg>"""
    body = f"""
<div class="hdr"><img src="{a}/logo_lawsikho.png"><div class="div"></div><img src="{a}/brand_nca.png"></div>
<div class="copy"><div class="hook">{c['hook']}</div><div class="prize">{c['prize']}</div></div>
<div class="leafbox"><div class="rule l"></div><div class="leafwrap">{leaf}</div><div class="rule r"></div></div>
<div class="pillars">{pil}</div>
<div class="sticker">{c['sticker']}</div>
<div class="band">
 <div class="cell"><img src="{a}/foot_card.png"><div><div class="cb">{c['band_left_big']}</div><div class="cs">{c['band_left_small']}</div></div></div>
 <div class="cell"><img src="{a}/icon_calendar.png"><div><div class="cb red">{c['band_right_big']}</div><div class="cs caps">{c['band_right_small']}</div></div></div>
</div>
<div class="btnrow"><div class="btn"><div class="bt">{c['button']}</div><div class="arrow">&#10140;</div></div><div class="burst">{c['burst']}</div></div>
<div class="foot"><div><img src="{a}/foot_calendar.png">{c['dates']}</div><div><img src="{a}/foot_laptop.png">{c['foot_mid']}</div><div><img src="{a}/foot_card.png">{c['foot_right']}</div></div>
"""
    return ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS % c + "</style></head><body>"
            + body + FIT_JS % c + "</body></html>")
