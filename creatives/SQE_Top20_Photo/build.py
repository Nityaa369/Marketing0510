"""SQE Community: 20 photo posters in the supplied poster template layout.
Photos are cropped from source/photo_grid.webp (5 x 4). Run: python3 build.py"""
import os, glob, subprocess
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
src = open(os.path.join(HERE, "..", "SQE_Top20_Heroes", "build.py")).read().split("def lum")[0]
exec(src)  # gives R (20 rows), PRICE

COLS = [(0, 299), (308, 615), (623, 913), (924, 1229), (1236, 1536)]
ROWS = [(0, 257), (265, 508), (515, 759), (767, 1024)]
grid = Image.open(os.path.join(HERE, "source", "photo_grid.webp")).convert("RGB")
for i in range(20):
    x0, x1 = COLS[i % 5]; y0, y1 = ROWS[i // 5]
    c = grid.crop((x0, y0, x1, y1)).resize((1080, round(1080 * (y1 - y0) / (x1 - x0))), Image.LANCZOS)
    c = c.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    c.save(os.path.join(HERE, "photos", f"{i+1:02d}.jpg"), quality=95)

F = ["Live 7 evenings", "SQE2 exemption route", "Exams written in India", "Mock SQE1 and MCQs"]
OVR = {3: {1: "SQE1 study plan"}, 4: {1: "Criminal law in SQE1"}, 6: {1: "Land law in SQE1"},
       8: {1: "English-law arbitration"}, 9: {1: "Where UK law is recognised"}, 10: {1: "Gulf and DIFC session"},
       11: {1: "Exam to admission route"}, 12: {1: "Singapore session"}, 13: {2: "Nearest test centre"},
       14: {1: "LLM route explained"}, 15: {1: "Build your profile"}, 16: {1: "Business law in SQE1"},
       17: {1: "In-house pathways"}, 18: {1: "Live Q&A on Day 7"}, 19: {1: "IP and tech pathways"}}
ICONS = [
 '<circle cx="24" cy="24" r="17" fill="none" stroke="#FFD21F" stroke-width="4"/><ellipse cx="24" cy="24" rx="7" ry="17" fill="none" stroke="#FFD21F" stroke-width="3"/><path d="M7 24H41M10 15H38M10 33H38" stroke="#FFD21F" stroke-width="3"/>',
 '<rect x="10" y="5" width="28" height="38" rx="4" fill="none" stroke="#FFD21F" stroke-width="4"/><path d="M16 17H32M16 25H32M16 33H26" stroke="#FFD21F" stroke-width="4" stroke-linecap="round"/>',
 '<path d="M4 28L44 14L40 20L26 26L28 40L22 42L16 29L8 33Z" fill="#FFD21F"/>',
 '<path d="M24 4L40 10V24C40 34 33 41 24 45C15 41 8 34 8 24V10Z" fill="none" stroke="#FFD21F" stroke-width="4"/><path d="M16 24L22 30L33 18" fill="none" stroke="#FFD21F" stroke-width="4" stroke-linecap="round"/>']

def card(r):
    n, stem, banner, hook = r[0], r[1], r[2], r[3]
    l1, l2 = hook.split(". ", 1)
    l1 += "."
    feats = list(F)
    for k, v in OVR.get(n, {}).items(): feats[k] = v
    fh = "".join(f'<div class="f"><svg viewBox="0 0 48 48" width="52" height="52">{ICONS[i]}</svg><span>{feats[i]}</span></div>' for i in range(4))
    return f'''<div class="card">
<div class="photo" style="background-image:url(../photos/{n:02d}.jpg)"></div>
<div class="shade"></div>
<div class="logo"><div class="dot"><svg viewBox="0 0 40 40" width="40" height="40"><path d="M20 6C11 6 6 13 6 20S11 34 20 34 34 28 34 22 28 14 22 14 15 17 15 21 18 26 22 26" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/></svg></div><span>LawSikho</span></div>
<div class="ban"><span id="b">{banner}</span></div>
<div class="hook" id="hk"><div class="l1">{l1}</div><div class="l2">{l2}</div></div>
<div class="feats">{fh}</div>
<div class="cta"><span>Join the SQE Community for {PRICE}</span><b>&#8594;</b></div>
<div class="usp"><div><i>&#9679;</i> Live evening sessions<br><small>no recordings</small></div><div><i>&#9679;</i> 7 days<br><small>one session a day</small></div><div><i>&#9679;</i> Refundable<br><small>incl. GST</small></div></div>
</div>
<script>
function fit(el,max,min){{let s=max;el.style.fontSize=s+'px';while(el.scrollHeight>el.clientHeight+1&&s>min){{s-=2;el.style.fontSize=s+'px';}}}}
const hk=document.getElementById('hk');const l1=hk.querySelector('.l1'),l2=hk.querySelector('.l2');
let s=70;function ap(){{l1.style.fontSize=(s*0.78)+'px';l2.style.fontSize=s+'px';}}ap();
while(hk.scrollHeight>hk.clientHeight+1&&s>34){{s-=2;ap();}}
const b=document.getElementById('b');let t=50;b.style.fontSize=t+'px';
while(b.parentElement.scrollHeight>b.parentElement.clientHeight+1&&t>28){{t-=2;b.style.fontSize=t+'px';}}
</script>'''

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter','Noto Sans',sans-serif;background:#0B1F4D}
.card{width:1080px;height:1350px;position:relative;overflow:hidden;background:linear-gradient(180deg,#0A1B45 0%,#112C66 45%,#0A1B45 100%)}
.photo{position:absolute;left:0;top:560px;width:1080px;height:900px;background-size:cover;background-position:center}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,#0A1B45 0%,#0A1B45 47%,rgba(10,27,69,0) 62%,rgba(10,27,69,0) 78%,rgba(6,14,38,.92) 100%)}
.logo{position:absolute;left:36px;top:26px;display:flex;align-items:center;gap:12px;z-index:5}
.dot{width:58px;height:58px;border-radius:50%;background:#E2262B;display:flex;align-items:center;justify-content:center}
.logo span{font-family:'Bitstream Charter',Caladea,serif;font-size:50px;color:#fff;font-weight:700}
.ban{position:absolute;left:150px;right:150px;top:96px;height:112px;background:#FFD21F;color:#101828;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;text-transform:uppercase;line-height:1.02;padding:6px 22px;transform:rotate(-1.4deg);z-index:5;overflow:hidden}
.hook{position:absolute;left:44px;right:44px;top:228px;height:340px;text-align:center;font-weight:900;line-height:1.04;overflow:hidden;z-index:5;text-transform:none}
.l1{color:#fff}.l2{color:#FF2D3A;margin-top:8px;text-shadow:0 2px 0 rgba(0,0,0,.25)}
.feats{position:absolute;left:30px;right:30px;top:586px;display:flex;z-index:5}
.f{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;color:#fff;font-weight:800;font-size:25px;text-align:center;line-height:1.1;padding:0 8px;border-right:2px solid rgba(255,255,255,.35)}
.f:last-child{border:0}
.cta{position:absolute;left:46px;right:46px;top:1166px;height:96px;background:linear-gradient(180deg,#F23A3A,#C81620);border-radius:48px;color:#fff;display:flex;align-items:center;justify-content:center;gap:18px;font-weight:900;font-size:43px;box-shadow:0 8px 24px rgba(0,0,0,.45);z-index:6}
.cta b{font-size:50px}
.usp{position:absolute;left:30px;right:30px;top:1280px;display:flex;color:#fff;font-weight:800;font-size:25px;line-height:1.15;z-index:6}
.usp div{flex:1;text-align:center}.usp small{font-size:22px;font-weight:600;opacity:.95}.usp i{color:#FFD21F;font-style:normal;font-size:20px}
"""
os.makedirs(f"{HERE}/ads", exist_ok=True); os.makedirs(f"{HERE}/html", exist_ok=True)
def shot(html, out, w, h):
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", f"--screenshot={out}", "file://" + html], check=True, capture_output=True)
for r in R:
    p = f"{HERE}/html/sqe_p_{r[0]:02d}_{r[1]}.html"
    open(p, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{card(r)}</body></html>")
    shot(p, f"{HERE}/ads/sqe_p_{r[0]:02d}_{r[1]}.png", 1080, 1350)
# contact sheet, 5 x 4
sheet = Image.new("RGB", (5 * 540 + 6 * 16, 4 * 675 + 5 * 16), (225, 225, 225))
for i, r in enumerate(R):
    im = Image.open(f"{HERE}/ads/sqe_p_{r[0]:02d}_{r[1]}.png").convert("RGB").resize((540, 675), Image.LANCZOS)
    sheet.paste(im, (16 + (i % 5) * 556, 16 + (i // 5) * 691))
sheet.save(f"{HERE}/sheet.png")
print("done")
