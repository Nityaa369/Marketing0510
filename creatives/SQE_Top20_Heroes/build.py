"""SQE Community: 20 hero creatives, rendered from code onto one sheet plus 20 single faces.
Run: python3 build.py   (writes ads/*.png, sheet.png, html/*.html)
Figures are flat illustrations, placeholders for licensed Indian photos."""
import os, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
PRICE = "₹[PRICE]"

SK = ["#C98F64", "#A8704A", "#D9A679", "#8E5B3C", "#B97F57"]
# n, stem, banner, hook, bg, ink, accent, coat, prop, shape, side, gender, bands, skin
R = [
 (1,"litigating_advocates","FOR LITIGATING ADVOCATES","You argue in court every week. Now become a UK solicitor without pausing your practice.","#FBF4E4","#14213D","#F28C0F","#1B1B1F","court","arch","R","m",1,0),
 (2,"experienced_advocates","FOR EXPERIENCED ADVOCATES","You have built a practice in India. Now add a UK solicitor qualification and keep the practice running.","#F7F3E3","#0F3D2E","#B8892B","#1B1B1F","books","rect","L","m",1,3),
 (3,"newly_enrolled","FOR NEWLY ENROLLED ADVOCATES","You have just enrolled. Start your UK solicitor qualification in your first years of practice.","#F2FAFA","#0B4F5C","#F0615A","#1B1B1F","cert","circle","R","f",1,2),
 (4,"criminal_lawyers","FOR CRIMINAL LAWYERS","Your weeks run on bail and trial dates. Now become a solicitor of England and Wales and work beyond one court.","#F6EBDD","#5B1425","#2B2B2B","#1B1B1F","file","window","L","m",1,1),
 (5,"civil_consumer","FOR CIVIL AND CONSUMER COURT LAWYERS","You argue contract and tort cases every month. Now become a UK solicitor for clients abroad.","#E8EEF9","#1B3A8C","#FFC400","#1B3A8C","laptop","rect","R","f",0,0),
 (6,"property_conveyancing","FOR PROPERTY AND CONVEYANCING LAWYERS","You already work on titles and deeds. Now become a solicitor of England and Wales.","#FBF0E6","#3E5C2A","#C8553D","#3E5C2A","deed","arch","L","m",0,4),
 (7,"nclt_banking","FOR NCLT AND BANKING LAWYERS","You appear before the tribunal. Now become the lawyer for cross-border finance disputes.","#FAF7F2","#4A1D5C","#D4A017","#4A1D5C","board","circle","R","m",1,1),
 (8,"arbitration","FOR ARBITRATION LAWYERS","You do arbitration in India. Now become an international arbitration lawyer.","#F5F7F8","#2F3E4E","#F26A21","#2F3E4E","bundle","rect","L","f",0,2),
 (9,"international_career","FOR LAWYERS WHO WANT AN INTERNATIONAL CAREER","You have thought about working abroad for years. Now find out if a UK solicitor qualification is your way in.","#E3F2FD","#0D3B66","#E63946","#0D3B66","passport","window","R","f",0,4),
 (10,"dubai_gulf","FOR LAWYERS WHO WANT TO WORK IN DUBAI OR THE GULF","You want legal work in the Gulf. Now qualify in the English law its courts and contracts run on.","#F8EEDB","#0E5A5A","#0E5A5A","#0E5A5A","dubai","window","L","m",0,0),
 (11,"england","FOR LAWYERS WHO WANT TO PRACTISE IN ENGLAND","You want to practise law in England. Start the qualification now, from India.","#F8EFE6","#1F2A5A","#B3412D","#1F2A5A","london","window","R","m",0,3),
 (12,"singapore_hk","FOR LAWYERS WHO WANT TO WORK IN SINGAPORE OR HONG KONG","You want an Asian legal hub. Now become an English-law lawyer those hubs hire.","#E1F5F4","#25313A","#25313A","#25313A","harbour","window","L","f",0,1),
 (13,"living_abroad","FOR INDIAN LAWYERS LIVING ABROAD","You moved abroad. Now qualify as a UK solicitor from where you live.","#FDEBDD","#5A3A22","#8A5A33","#8A5A33","home","arch","R","f",0,2),
 (14,"llm_abroad","FOR LAWYERS WITH AN LLM FROM ABROAD","You studied law abroad. Now turn that degree into a UK solicitor qualification.","#FBF3E6","#5C1A33","#C9962B","#5C1A33","scroll","arch","L","m",0,4),
 (15,"associates","FOR LAW FIRM ASSOCIATES","You are good at your job, and the cross-border work goes elsewhere. Now qualify to do it yourself.","#F4F7FF","#12307A","#B5E61D","#12307A","folder","rect","R","f",0,0),
 (16,"corporate_ma","FOR CORPORATE AND M&A LAWYERS","You work on deals every day. Now become the English-law deal lawyer global clients hire.","#FAF5E8","#22303C","#F5A300","#22303C","termsheet","circle","L","m",0,3),
 (17,"in_house","FOR IN-HOUSE COUNSEL","You advise one company. Now become counsel that global companies hire.","#EFF8F2","#0B5D3B","#111111","#0B5D3B","laptop","rect","R","m",0,1),
 (18,"practice_owners","FOR LAWYERS WHO OWN A PRACTICE","You built your own practice. Now add a UK arm to it.","#F8F1E4","#4A3320","#B58A2E","#4A3320","nameplate","arch","L","f",0,2),
 (19,"ip_data_privacy","FOR IP AND DATA PRIVACY LAWYERS","You advise on rules that cross borders. Now qualify in the English law behind much of it.","#F4F0FB","#4B2C8F","#3DDC97","#4B2C8F","lock","circle","R","f",0,4),
 (20,"smaller_cities","FOR LAWYERS IN SMALLER CITIES","You practise in a smaller city. Now qualify as a UK solicitor without moving anywhere.","#F9F3E3","#4D5A1E","#EE7B22","#4D5A1E","street","window","L","m",0,0),
]


def lum(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return (0.299*r + 0.587*g + 0.114*b) / 255


def person(skin, coat, gender, bands, ink):
    hair = "#1A1412"
    s = f'<ellipse cx="200" cy="470" rx="190" ry="120" fill="{coat}"/>'  # shoulders
    s += f'<path d="M150 330 L250 330 L262 372 Q200 420 138 372 Z" fill="{skin}"/>'  # neck
    if bands:
        s += '<path d="M168 372 L200 430 L232 372 L212 366 L200 392 L188 366 Z" fill="#fff"/>'
        s += '<rect x="186" y="400" width="12" height="46" fill="#fff"/><rect x="204" y="400" width="12" height="46" fill="#fff"/>'
    else:
        s += f'<path d="M160 372 L200 410 L240 372 L224 366 L200 388 L176 366 Z" fill="#fff"/>'
    if gender == "f":
        s += f'<path d="M108 230 Q108 90 200 90 Q292 90 292 230 L300 420 Q250 400 250 330 L150 330 Q150 400 100 420 Z" fill="{hair}"/>'
    s += f'<ellipse cx="200" cy="245" rx="82" ry="98" fill="{skin}"/>'
    if gender == "m":
        s += f'<path d="M118 235 Q112 120 200 118 Q288 120 282 235 Q268 170 200 168 Q132 170 118 235Z" fill="{hair}"/>'
    else:
        s += f'<path d="M118 240 Q118 130 200 128 Q282 130 282 240 Q260 170 200 176 Q160 180 118 240Z" fill="{hair}"/>'
    s += '<circle cx="168" cy="250" r="7" fill="#1A1412"/><circle cx="232" cy="250" r="7" fill="#1A1412"/>'
    s += '<path d="M150 228 Q168 216 186 226 M214 226 Q232 216 250 228" stroke="#1A1412" stroke-width="6" fill="none" stroke-linecap="round"/>'
    s += '<path d="M170 296 Q200 322 230 296" stroke="#6B2B22" stroke-width="7" fill="none" stroke-linecap="round"/>'
    if gender == "f":
        s += '<circle cx="200" cy="210" r="5" fill="#C0392B"/>'
    return f'<svg viewBox="0 0 400 520" width="100%" height="100%">{s}</svg>'


def prop(kind, ac, ink):
    P = {
     "court": f'<rect x="20" y="150" width="360" height="26" fill="{ink}"/><g fill="{ink}">' + "".join(f'<rect x="{40+i*68}" y="60" width="26" height="90"/>' for i in range(5)) + f'</g><path d="M10 60 L200 0 L390 60Z" fill="{ink}"/>',
     "books": "".join(f'<rect x="{30+i*52}" y="{40+(i%2)*14}" width="40" height="{120-(i%2)*14}" fill="{[ac,ink,ac,ink,ac,ink][i]}" opacity=".9"/>' for i in range(6)),
     "cert": f'<rect x="60" y="30" width="280" height="190" rx="10" fill="#fff" stroke="{ink}" stroke-width="8"/><rect x="90" y="70" width="220" height="14" fill="{ink}"/><rect x="90" y="106" width="170" height="12" fill="{ac}"/><circle cx="290" cy="180" r="24" fill="{ac}"/>',
     "file": f'<rect x="50" y="30" width="300" height="200" rx="8" fill="{ac}"/><rect x="50" y="30" width="110" height="26" rx="6" fill="{ink}"/><rect x="90" y="90" width="220" height="12" fill="#fff"/><rect x="90" y="124" width="180" height="12" fill="#fff"/>',
     "laptop": f'<rect x="70" y="30" width="260" height="170" rx="10" fill="{ink}"/><rect x="86" y="46" width="228" height="138" fill="#fff"/><rect x="104" y="66" width="150" height="12" fill="{ac}"/><rect x="104" y="96" width="190" height="10" fill="{ink}" opacity=".5"/><rect x="40" y="200" width="320" height="18" rx="9" fill="{ink}"/>',
     "deed": f'<rect x="60" y="20" width="280" height="200" fill="#fff" stroke="{ink}" stroke-width="6"/><path d="M120 150 L120 100 L200 60 L280 100 L280 150Z" fill="{ac}"/><rect x="180" y="110" width="40" height="40" fill="#fff"/><circle cx="300" cy="190" r="20" fill="{ink}"/>',
     "board": f'<rect x="40" y="20" width="320" height="200" rx="8" fill="{ink}"/>' + "".join(f'<rect x="64" y="{44+i*44}" width="{150+i*30}" height="14" fill="{ac}"/><rect x="64" y="{64+i*44}" width="110" height="10" fill="#fff" opacity=".7"/>' for i in range(4)),
     "bundle": f'<rect x="60" y="150" width="280" height="40" rx="6" fill="{ink}"/><rect x="60" y="102" width="280" height="40" rx="6" fill="{ac}"/><rect x="60" y="54" width="280" height="40" rx="6" fill="{ink}" opacity=".85"/>',
     "passport": f'<rect x="110" y="20" width="180" height="230" rx="12" fill="{ink}"/><circle cx="200" cy="110" r="42" fill="none" stroke="{ac}" stroke-width="6"/><rect x="140" y="180" width="120" height="12" fill="{ac}"/>',
     "dubai": f'<rect x="0" y="230" width="400" height="30" fill="{ink}" opacity=".3"/><path d="M200 0 L214 120 L216 260 L184 260 L186 120Z" fill="{ink}"/><rect x="70" y="110" width="50" height="150" fill="{ink}" opacity=".7"/><rect x="280" y="140" width="56" height="120" fill="{ink}" opacity=".55"/><rect x="130" y="170" width="40" height="90" fill="{ink}" opacity=".5"/>',
     "london": f'<rect x="170" y="40" width="60" height="220" fill="{ink}"/><path d="M165 40 L200 0 L235 40Z" fill="{ink}"/><circle cx="200" cy="90" r="20" fill="#fff"/><rect x="40" y="170" width="90" height="90" fill="{ink}" opacity=".6"/><rect x="270" y="150" width="90" height="110" fill="{ink}" opacity=".6"/>',
     "harbour": f'<path d="M0 230 Q100 200 200 230 T400 230 L400 270 L0 270Z" fill="{ink}" opacity=".35"/><rect x="60" y="80" width="46" height="150" fill="{ink}"/><rect x="130" y="40" width="50" height="190" fill="{ink}" opacity=".8"/><rect x="210" y="110" width="44" height="120" fill="{ink}" opacity=".65"/><rect x="280" y="60" width="52" height="170" fill="{ink}" opacity=".9"/>',
     "home": f'<path d="M40 130 L200 20 L360 130Z" fill="{ac}"/><rect x="70" y="130" width="260" height="110" fill="#fff" stroke="{ink}" stroke-width="6"/><rect x="170" y="170" width="60" height="70" fill="{ink}"/><rect x="95" y="155" width="50" height="40" fill="{ac}" opacity=".5"/>',
     "scroll": f'<rect x="60" y="40" width="280" height="170" fill="#fff" stroke="{ink}" stroke-width="6"/><circle cx="60" cy="125" r="26" fill="{ac}"/><circle cx="340" cy="125" r="26" fill="{ac}"/><rect x="110" y="90" width="180" height="12" fill="{ink}"/><rect x="110" y="124" width="140" height="10" fill="{ink}" opacity=".5"/>',
     "folder": f'<rect x="60" y="50" width="280" height="190" rx="10" fill="{ink}"/><rect x="60" y="30" width="120" height="30" rx="8" fill="{ac}"/><rect x="100" y="110" width="200" height="14" fill="#fff"/><rect x="100" y="146" width="150" height="12" fill="#fff" opacity=".7"/>',
     "termsheet": f'<rect x="80" y="20" width="240" height="230" fill="#fff" stroke="{ink}" stroke-width="6"/>' + "".join(f'<rect x="108" y="{50+i*34}" width="{190-(i%2)*50}" height="12" fill="{ink if i%2==0 else ac}"/>' for i in range(5)),
     "nameplate": f'<rect x="60" y="80" width="280" height="110" rx="10" fill="{ink}"/><rect x="90" y="110" width="220" height="16" fill="{ac}"/><rect x="90" y="144" width="150" height="12" fill="#fff" opacity=".8"/>',
     "lock": f'<path d="M130 110 Q130 30 200 30 Q270 30 270 110" fill="none" stroke="{ink}" stroke-width="22"/><rect x="100" y="100" width="200" height="150" rx="18" fill="{ink}"/><circle cx="200" cy="160" r="20" fill="{ac}"/><rect x="192" y="166" width="16" height="50" fill="{ac}"/>',
     "street": f'<rect x="20" y="110" width="110" height="140" fill="{ink}" opacity=".8"/><rect x="140" y="70" width="120" height="180" fill="{ac}"/><rect x="270" y="130" width="110" height="120" fill="{ink}" opacity=".65"/>' + "".join(f'<rect x="{160+(i%2)*50}" y="{95+(i//2)*44}" width="28" height="28" fill="#fff"/>' for i in range(6)),
    }
    return f'<svg viewBox="0 0 400 270" width="100%" height="100%">{P[kind]}</svg>'


def shape(kind, ac):
    c = ac
    if kind == "circle":
        return f'<div class="shp" style="width:700px;height:700px;border-radius:50%;background:{c};opacity:.22;"></div>'
    if kind == "arch":
        return f'<div class="shp" style="width:640px;height:820px;border-radius:320px 320px 0 0;background:{c};opacity:.22;"></div>'
    if kind == "window":
        return f'<div class="shp" style="width:700px;height:680px;background:{c};opacity:.2;border-radius:14px;"></div>'
    return f'<div class="shp" style="width:680px;height:760px;background:{c};opacity:.2;transform:rotate(-4deg);border-radius:18px;"></div>'


def card(row):
    n, stem, banner, hook, bg, ink, ac, coat, pr, shp, side, g, bands, sk = row
    btn_ink = "#14181F" if lum(ac) > 0.55 else "#FFFFFF"
    fig_side = "right:-30px" if side == "R" else "left:-30px"
    prop_side = "left:34px" if side == "R" else "right:34px"
    banner_sz = 66 if len(banner) < 36 else 56
    return f'''<div class="card" style="background:{bg};color:{ink}">
<div class="banner" style="background:{ink};color:{bg};font-size:{banner_sz}px">{banner}</div>
<div class="hook">{hook}</div>
<div class="stage">
 <div class="shpwrap" style="{fig_side}">{shape(shp, ac)}</div>
 <div class="prop" style="{prop_side}">{prop(pr, ac, ink)}</div>
 <div class="fig" style="{fig_side}">{person(SK[sk], coat, g, bands, ink)}</div>
</div>
<div class="btn" style="background:{ac};color:{btn_ink}">Join the SQE Community for {PRICE}</div>
</div>'''


CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,'Noto Sans',sans-serif;background:#ECECEC}
.card{width:1080px;height:1350px;position:relative;overflow:hidden;padding:48px 54px 44px;display:flex;flex-direction:column}
.banner{font-weight:900;letter-spacing:-.01em;line-height:1.04;text-transform:uppercase;text-align:center;padding:20px 22px 24px;border-radius:12px}
.hook{font-size:64px;font-weight:900;line-height:1.1;letter-spacing:-.02em;margin-top:30px}
.stage{position:relative;flex:1;margin-top:10px;min-height:0}
.shpwrap{position:absolute;bottom:-20px;width:700px;display:flex;justify-content:center;align-items:flex-end}
.shp{position:relative}
.fig{position:absolute;bottom:-40px;width:640px;height:800px}
.prop{position:absolute;bottom:30px;width:470px;height:320px}
.btn{font-size:48px;font-weight:900;text-align:center;padding:26px 24px;border-radius:16px;margin-top:14px;position:relative;z-index:3}
"""

os.makedirs(f"{HERE}/ads", exist_ok=True)
os.makedirs(f"{HERE}/html", exist_ok=True)


def shot(html, out, w, h, scale=1):
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={scale}",
                    f"--window-size={w},{h}", f"--screenshot={out}", "file://" + html], check=True, capture_output=True)


for r in R:
    p = f"{HERE}/html/sqe_h_{r[0]:02d}_{r[1]}.html"
    open(p, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}body{{background:#fff}}</style></head><body>{card(r)}</body></html>")
    shot(p, f"{HERE}/ads/sqe_h_{r[0]:02d}_{r[1]}.png", 1080, 1350, 1)

# single plane: 5 x 4 grid, each card shown at 0.5 size
cells = "".join(f'<div class="cell"><div class="num">{r[0]:02d}</div><div class="scaled">{card(r)}</div></div>' for r in R)
sheet = f"""<!doctype html><html><head><meta charset='utf-8'><style>{CSS}
body{{background:#D9D9D9;padding:30px;width:2900px}}
.grid{{display:grid;grid-template-columns:repeat(5,540px);gap:24px}}
.cell{{position:relative;width:540px;height:675px;overflow:hidden;border-radius:10px;box-shadow:0 4px 14px rgba(0,0,0,.25)}}
.scaled{{transform:scale(.5);transform-origin:0 0;width:1080px;height:1350px}}
.num{{position:absolute;top:8px;left:8px;z-index:9;background:#111;color:#fff;font:800 22px Inter,sans-serif;padding:4px 10px;border-radius:6px}}
h1{{font:900 40px Inter,sans-serif;margin-bottom:6px}} p{{font:600 24px Inter,sans-serif;margin-bottom:22px}}
</style></head><body><h1>SQE Community: 20 hero creatives</h1>
<p>Draft for Ramanuj. Illustrated placeholders for licensed Indian photos. Price line open: {PRICE}.</p>
<div class="grid">{cells}</div></body></html>"""
sp = f"{HERE}/html/sheet.html"
open(sp, "w").write(sheet)
shot(sp, f"{HERE}/sheet.png", 2900, 3000, 1)
print("done")
