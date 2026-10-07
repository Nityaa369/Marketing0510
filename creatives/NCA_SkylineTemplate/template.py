"""NCA Canada skyline template (LawSikho), layout v4: the reference format, exactly.

Mirrors reference/original.webp: header left; hook and prize on the left; the maple leaf
skyline art bleeding off the RIGHT EDGE (the reference's own crop); then the pillar row in
the reference order (NCA, Online Exams, Canadian Bar); the "We show you how." sticker; the
band with Canada's legal market on the left and 3 DAYS / 9 HOURS on the right; the JOIN NOW
button with the ONLY Rs 10 burst; and the footer. Variable per ad: hook and prize only.

Departures from the reference, all decided and recorded in the README:
- NCA pillar line is Ruchika's "A direct pathway toward Canadian bar eligibility."
- Market figure is the sourced ~CAD 22B (IBISWorld via docs/NCA_MARKET_FACTS_2026-10-07.md),
  not the unverified 38B. VERIFY before launch; swap to Rs 10 cell if Ramanuj flags stats.
- "31 Oct to 2 Nov" (no en dash, standing rule).
- Spelling: practice/practicing everywhere (Ruchika, 7 Oct).

Canvas 1080 x 1350 (Meta 4:5). Fonts: Inter (installed).
"""

DEFAULTS = dict(
    # VARIABLE PER AD. Wrap the red part in <em>...</em>.
    hook="A lawyer who keeps thinking <em>about Canada?</em>",
    prize="You could <em>practice law in Canada.</em>",
    # Height budgets before the fitter shrinks the type (px).
    hook_max_height=350, hook_max_px=100,
    prize_max_height=200, prize_max_px=68,
    # FIXED FOR THE WAVE. Reference pillar order: NCA, Online Exams, Canadian Bar.
    pillars=[
        ("icon_nca.png", "NCA", "A direct pathway toward Canadian bar eligibility."),
        ("icon_laptop.png", "Online Exams", "Give the NCA exams <em>from the comfort of your home.</em> Sessions 12 times a year."),
        ("icon_bar.png", "Canadian Bar", "You become eligible for the Canadian bar exam."),
    ],
    sticker="We show you how.",
    band_left_label="Canada's<br>legal market",
    band_left_big="~CAD 22B",
    band_left_small="(about &#8377;1.4 lakh crore)",
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
body{font-family:Inter,sans-serif;background:%(bg)s;color:%(ink)s;position:relative;display:flex;flex-direction:column;padding:34px 48px 24px}
em{font-style:normal;color:%(red)s}
.hdr{display:flex;align-items:center;gap:26px;height:94px;flex:none}
.hdr img{height:94px;width:auto}
.hdr .div{width:3px;height:84px;background:#2B2A33;opacity:.75}
.art{position:absolute;right:0;top:112px;height:524px;width:auto;z-index:0}
.copy{position:relative;z-index:1;width:712px;margin-top:30px;flex:none}
.hook{font-size:%(hook_max_px)dpx;font-weight:900;line-height:.98;letter-spacing:-.045em;word-spacing:-.04em}
.prize{font-size:%(prize_max_px)dpx;font-weight:900;line-height:1.02;letter-spacing:-.04em;margin-top:26px;width:660px}
.grow{flex:1;min-height:0}
.pillars{position:relative;z-index:1;display:flex;flex:none;margin-top:12px}
.pil{flex:1;text-align:center;padding:0 12px}
.pil+.pil{border-left:3px solid #E6E2DB}
.pil img{height:128px;width:auto}
.pt{font-size:38px;font-weight:900;letter-spacing:-.02em;margin-top:8px}
.pd{font-size:24px;font-weight:600;line-height:1.22;margin-top:5px;color:#2A2730}
.pd em{font-weight:800}
.sticker{position:relative;z-index:2;align-self:flex-start;background:#FFF04A;font-size:36px;font-weight:900;letter-spacing:-.02em;padding:7px 22px 9px;border-radius:8px;transform:rotate(-2.5deg);margin:10px 0 0 8px;box-shadow:0 6px 14px rgba(0,0,0,.10)}
.band{display:flex;flex:none;background:#FEECE7;border-radius:16px;margin-top:12px;padding:15px 30px}
.cell{flex:1;display:flex;align-items:center;gap:24px}
.cell+.cell{border-left:3px solid #E9CFC7;padding-left:30px}
.cell img{height:100px;width:auto}
.clabel{font-size:30px;font-weight:900;line-height:1.08;letter-spacing:-.02em}
.cbig{font-size:58px;font-weight:900;letter-spacing:-.03em;color:%(red)s;line-height:1.02}
.csmall{font-size:24px;font-weight:600;color:#4A443C;margin-top:2px}
.cb{font-size:42px;font-weight:900;line-height:1.04;letter-spacing:-.03em;color:%(red)s;text-transform:uppercase}
.cs{font-size:26px;font-weight:800;letter-spacing:.02em;text-transform:uppercase;margin-top:5px}
.btnrow{position:relative;flex:none;margin-top:18px}
.btn{background:%(red)s;color:#fff;border-radius:60px;height:104px;display:flex;align-items:center;padding:0 44px;box-shadow:0 10px 24px rgba(242,55,29,.35)}
.bt{font-size:56px;font-weight:900;letter-spacing:-.02em;flex:1;text-align:center;padding-right:140px}
.arrow{font-size:70px;font-weight:900;margin-left:auto}
.burst{position:absolute;right:160px;top:-36px;width:216px;height:178px;background:url('data:image/svg+xml;utf8,<svg xmlns=%%22http://www.w3.org/2000/svg%%22 viewBox=%%220 0 230 190%%22><polygon fill=%%22%%23FFE64A%%22 stroke=%%22%%23F2371D%%22 stroke-width=%%226%%22 points=%%22115,6 135,30 165,14 172,44 206,40 198,72 228,88 206,112 224,142 190,148 190,182 158,168 140,186 115,160 88,186 70,168 38,182 38,148 6,142 24,112 2,88 32,72 24,40 58,44 65,14 95,30%%22/></svg>') no-repeat center/contain;display:flex;align-items:center;justify-content:center;text-align:center;font-size:42px;font-weight:900;line-height:.95;color:%(ink)s;transform:rotate(6deg)}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:14px;flex:none;font-size:26px;font-weight:800;letter-spacing:.03em;text-transform:uppercase}
.foot div{display:flex;align-items:center;gap:16px}
.foot img{height:44px;width:auto}
"""

FIT_JS = """
<script>
// Fit hook and prize to their budgets, then shrink both until the whole column fits the
// canvas, so no face ever clips the button or footer.
function size(e){return parseFloat(getComputedStyle(e).fontSize)}
function fit(sel,maxH,minPx,maxPx){var e=document.querySelector(sel);var s=maxPx;e.style.fontSize=s+'px';
while(e.scrollHeight>maxH&&s>minPx){s-=2;e.style.fontSize=s+'px';}}
fit('.hook',%(hook_max_height)d,52,%(hook_max_px)d);fit('.prize',%(prize_max_height)d,40,%(prize_max_px)d);
// Keep the pillar row clear of the leaf art (art bottom = 112 + 524).
(function(){var pil=document.querySelector('.pillars'),g=document.querySelector('.grow');
var need=648-pil.getBoundingClientRect().top;if(need>0)g.style.minHeight=need+'px';})();
(function(){var h=document.querySelector('.hook'),p=document.querySelector('.prize');
for(var i=0;i<40&&document.body.scrollHeight>1350;i++){
 if(size(h)<=52&&size(p)<=40)break;
 if(size(h)>52)h.style.fontSize=(size(h)-2)+'px';
 if(size(p)>40)p.style.fontSize=(size(p)-2)+'px';}})();
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
 <div class="cell"><img src="{a}/icon_chart.png"><div><div class="clabel">{c['band_left_label']}</div><div class="cbig">{c['band_left_big']}</div><div class="csmall">{c['band_left_small']}</div></div></div>
 <div class="cell"><img src="{a}/icon_calendar.png"><div><div class="cb">{c['band_right_big']}</div><div class="cs">{c['band_right_small']}</div></div></div>
</div>
<div class="btnrow"><div class="btn"><div class="bt">{c['button']}</div><div class="arrow">&#10140;</div></div><div class="burst">{c['burst']}</div></div>
<div class="foot"><div><img src="{a}/foot_calendar.png">{c['dates']}</div><div><img src="{a}/foot_laptop.png">{c['foot_mid']}</div><div><img src="{a}/foot_card.png">{c['foot_right']}</div></div>
"""
    return ("<!doctype html><html><head><meta charset='utf-8'><style>" + CSS % c + "</style></head><body>"
            + body + FIT_JS % c + "</body></html>")
