"""NCA Canada skyline template (LawSikho). Fixed: header, maple leaf skyline art, three route
pillars, "We show you how" sticker, terms band, JOIN NOW button, footer. Variable per ad: the
hook (call-out question) and the prize line (value proposition). Everything else can be
overridden through the config dict but should not change between ads in a wave.

Canvas 1080 x 1350 (Meta 4:5). Fonts: Inter (installed). Assets are cut from the reference ad
in reference/original.webp.
"""
import html

DEFAULTS = dict(
    # VARIABLE PER AD. Wrap the red part in <em>...</em>.
    hook="A lawyer who keeps thinking <em>about Canada?</em>",
    prize="You could <em>practise law in Canada.</em>",
    # Max height the hook block may take before it is shrunk to fit (px).
    hook_max_height=290,
    hook_max_px=124,
    prize_max_height=150,
    prize_max_px=78,
    # FIXED FOR THE WAVE. Three route pillars: NCA exams, then bar licensing, then practise.
    pillars=[
        ("icon_nca.png", "NCA exams", "Canada's check on your Indian law degree. Written <em>online, from India.</em> Every month."),
        ("icon_bar.png", "Canadian bar", "Then bar licensing. You become eligible to apply."),
        ("icon_laptop.png", "Practise in Canada", "Same craft, Canadian clients and courts."),
    ],
    sticker="We show you how.",
    # Terms band. Left cell is the risk remover; right cell is the format.
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

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,sans-serif;background:%(bg)s;color:%(ink)s;position:relative;display:flex;flex-direction:column;padding:34px 44px 30px}
em{font-style:normal;color:%(red)s}
.hdr{display:flex;align-items:center;gap:26px;height:92px;flex:none}
.hdr img{height:92px;width:auto}
.hdr .div{width:3px;height:84px;background:#2B2A33;opacity:.75}
.art{position:absolute;right:0;top:118px;height:560px;width:auto;z-index:0}
.copy{position:relative;z-index:1;width:700px;margin-top:30px;flex:none}
.hook{font-size:86px;font-weight:900;line-height:.98;letter-spacing:-.045em;word-spacing:-.04em}
.prize{font-size:64px;font-weight:900;line-height:1.0;letter-spacing:-.04em;margin-top:26px;width:640px}
.grow{flex:1;min-height:8px}
.pillars{position:relative;z-index:1;display:flex;flex:none;margin-top:18px}
.pil{flex:1;text-align:center;padding:0 14px}
.pil+.pil{border-left:3px solid #E6E2DB}
.pil img{height:108px;width:auto}
.pt{font-size:32px;font-weight:900;letter-spacing:-.02em;margin-top:8px}
.pd{font-size:23px;font-weight:600;line-height:1.22;margin-top:5px;color:#2A2730}
.pd em{font-weight:800}
.sticker{position:relative;z-index:2;display:inline-block;align-self:flex-start;background:#FFF04A;font-size:34px;font-weight:900;letter-spacing:-.02em;padding:6px 20px 8px;border-radius:8px;transform:rotate(-2.5deg);margin:10px 0 0 12px;box-shadow:0 6px 14px rgba(0,0,0,.10)}
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
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:20px;flex:none;font-size:25px;font-weight:800;letter-spacing:.03em;text-transform:uppercase}
.foot div{display:flex;align-items:center;gap:16px}
.foot img{height:42px;width:auto}
"""

FIT_JS = """
<script>
// Grow the block until it would overflow its height budget, then step back. Short hooks get
// bigger type, long hooks get smaller, and the gap above the pillars stays closed.
function fit(sel,maxH,minPx,maxPx){var e=document.querySelector(sel);var s=maxPx;e.style.fontSize=s+'px';
while(e.scrollHeight>maxH&&s>minPx){s-=2;e.style.fontSize=s+'px';}}
fit('.hook',%(hook_max_height)d,56,%(hook_max_px)d);fit('.prize',%(prize_max_height)d,44,%(prize_max_px)d);
</script>"""


def render(cfg):
    c = dict(DEFAULTS); c.update(cfg)
    a = c["assets"]
    pil = "".join(
        f'<div class="pil"><img src="{a}/{ic}"><div class="pt">{t}</div><div class="pd">{d}</div></div>'
        for ic, t, d in c["pillars"])
    body = f"""
<div class="hdr"><img src="{a}/logo_lawsikho.png"><div class="div"></div><img src="{a}/brand_nca.png"></div>
<img class="art" src="{a}/art_leaf_skyline.png">
<div class="copy"><div class="hook">{c['hook']}</div><div class="prize">{c['prize']}</div></div>
<div class="grow"></div>
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
