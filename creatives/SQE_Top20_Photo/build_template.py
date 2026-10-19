"""SQE Community: 20 posters on the supplied template, unchanged. Only the photo, the banner,
the hook and the CTA are filled per ICP. Run: python3 build_template.py"""
import os, glob, subprocess
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
exec(open(os.path.join(HERE, "..", "SQE_Top20_Heroes", "build.py")).read().split("def lum")[0])  # R, PRICE

T = Image.open(os.path.join(HERE, "source", "poster_template.webp")).convert("RGB")
W, H = T.size
a = np.asarray(T).astype(float)

# --- top cover: template sky with the placeholder text removed ---
col = np.median(a[:, 893:905, :], axis=1)
for y0, y1 in [(118, 220), (486, 580)]:           # rows hidden by the "Edit" callouts
    for y in range(y0, y1):
        f = (y - y0) / (y1 - y0)
        col[y] = col[y0 - 1] * (1 - f) + col[y1] * f
sky = Image.fromarray(np.repeat(col[:, None, :], W, axis=1).astype(np.uint8))
cover = T.copy()
for box in [(255, 100, 1015, 225), (140, 195, 1015, 455), (220, 440, 1015, 585)]:
    cover.paste(sky.crop(box), box)
cover = cover.filter(ImageFilter.GaussianBlur(6))
for box in [(10, 10, 340, 100), (830, 10, 1015, 100)]:   # logo and social icons stay sharp
    cover.paste(T.crop(box), box)
cover = cover.crop((0, 0, W, 640))
cover.save(os.path.join(HERE, "source", "top_cover.png"))

# --- bottom chrome: CTA and USP strip with the placeholders removed ---
bot = T.crop((0, 1200, W, H)).copy()
ground = T.crop((850, 1500, 1010, 1536)).resize((175, 300)).filter(ImageFilter.GaussianBlur(8))
bot.paste(ground, (840, 1240 - 1200))              # right callouts, button is redrawn in CSS
red = T.crop((135, 1248, 150, 1392)).resize((760, 144))
bot.paste(red, (120, 1248 - 1200))                 # button interior
dark = T.crop((322, 1430, 338, 1500))
for x0, x1 in ((170, 305), (420, 540), (648, 845)):
    bot.paste(dark.resize((x1 - x0, 70)), (x0, 1430 - 1200))
bot.save(os.path.join(HERE, "source", "bottom_chrome.png"))

ICON = [
 '<circle cx="24" cy="24" r="17" fill="none" stroke="#FFD21F" stroke-width="4"/><ellipse cx="24" cy="24" rx="7" ry="17" fill="none" stroke="#FFD21F" stroke-width="3"/><path d="M7 24H41M10 15H38M10 33H38" stroke="#FFD21F" stroke-width="3"/>',
 '<rect x="10" y="5" width="28" height="38" rx="4" fill="none" stroke="#FFD21F" stroke-width="4"/><path d="M16 17H32M16 25H32M16 33H26" stroke="#FFD21F" stroke-width="4" stroke-linecap="round"/>',
 '<path d="M4 28L44 14L40 20L26 26L28 40L22 42L16 29L8 33Z" fill="#FFD21F"/>',
 '<path d="M24 4L40 10V24C40 34 33 41 24 45C15 41 8 34 8 24V10Z" fill="none" stroke="#FFD21F" stroke-width="4"/><path d="M16 24L22 30L33 18" fill="none" stroke="#FFD21F" stroke-width="4" stroke-linecap="round"/>']
F = ["Live 7 evenings", "SQE2 exemption route", "Exams written in India", "Mock SQE1 and MCQs"]
OVR = {3: {1: "SQE1 study plan"}, 4: {1: "Criminal law in SQE1"}, 6: {1: "Land law in SQE1"}, 8: {1: "English-law arbitration"},
       9: {1: "Where UK law counts"}, 10: {1: "Gulf and DIFC session"}, 11: {1: "Exam to admission"}, 12: {1: "Singapore session"},
       13: {2: "Nearest test centre"}, 14: {1: "LLM route explained"}, 15: {1: "Build your profile"}, 16: {1: "Business law in SQE1"},
       17: {1: "In-house pathways"}, 18: {1: "Live Q&amp;A on Day 7"}, 19: {1: "IP and tech pathways"}}

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{width:1024px;height:1536px;overflow:hidden;font-family:'Inter Display','Inter',sans-serif}
.card{position:relative;width:1024px;height:1536px;background:#0b1430}
.photo{position:absolute;left:0;top:600px;width:1024px;height:800px;background-size:cover;background-position:center top}
.top{position:absolute;left:0;top:0;width:1024px;height:640px;background:url(../source/top_cover.png);
 -webkit-mask-image:linear-gradient(#000 0,#000 596px,transparent 640px);mask-image:linear-gradient(#000 0,#000 596px,transparent 640px)}
.bot{position:absolute;left:0;top:1200px;width:1024px;height:336px;background:url(../source/bottom_chrome.png);-webkit-mask-image:linear-gradient(transparent 0,transparent 40px,#000 44px);mask-image:linear-gradient(transparent 0,transparent 40px,#000 44px)}
.btn{position:absolute;left:96px;top:1243px;width:814px;height:150px;border-radius:42px;background:linear-gradient(180deg,#FF4A4A 0%,#E5141F 55%,#B30D16 100%);box-shadow:0 10px 26px rgba(0,0,0,.55),inset 0 3px 0 rgba(255,255,255,.35)}
.ban{position:absolute;left:0;right:0;top:112px;display:flex;justify-content:center}
.ban span{display:inline-block;background:#FFD21F;color:#0E0E12;font-weight:900;text-transform:uppercase;line-height:1;padding:14px 26px 12px;transform:rotate(-1.6deg);font-size:46px;letter-spacing:-.01em;max-width:780px;text-align:center}
.hook{position:absolute;left:60px;right:60px;top:215px;height:238px;text-align:center;font-weight:900;text-transform:uppercase;line-height:.98;letter-spacing:-.025em;overflow:hidden}
.l1{color:#fff;text-shadow:0 3px 0 #0a1230,0 0 14px rgba(0,0,0,.55)}
.l2{color:#FF1F2E;margin-top:6px;-webkit-text-stroke:1.5px #fff;text-shadow:0 3px 0 #1a0a0a,0 0 14px rgba(0,0,0,.5)}
.feats{position:absolute;left:150px;right:150px;top:470px;display:flex}
.f{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;color:#fff;font-weight:800;font-size:19px;text-align:center;line-height:1.1;padding:0 6px;border-right:2px solid rgba(255,255,255,.5)}
.f:last-child{border:0}
.cta{position:absolute;left:96px;width:814px;top:1243px;height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:900;text-transform:uppercase;line-height:1;letter-spacing:-.015em}
.cta .a{font-size:54px}.cta .b{font-size:50px;margin-top:6px}
.usp{position:absolute;top:1432px;color:#fff;font-weight:800;font-size:22px;line-height:1.25}
.usp small{display:block;font-weight:600;font-size:20px}
"""

def card(r):
    n, banner, hook = r[0], r[2], r[3]
    l1, l2 = hook.split(". ", 1); l1 += "."
    feats = list(F)
    for k, v in OVR.get(n, {}).items(): feats[k] = v
    fh = "".join(f'<div class="f"><svg viewBox="0 0 48 48" width="46" height="46">{ICON[i]}</svg><span>{feats[i]}</span></div>' for i in range(4))
    return f'''<div class="card">
<div class="photo" style="background-image:url(../photos/{n:02d}.jpg)"></div>
<div class="top"></div>
<div class="bot"></div>
<div class="btn"></div>
<div class="ban"><span id="b">{banner}</span></div>
<div class="hook" id="hk"><div class="l1">{l1}</div><div class="l2">{l2}</div></div>
<div class="feats">{fh}</div>
<div class="cta"><div class="a">Join the SQE Community</div><div class="b">for {PRICE} &#8594;</div></div>
<div class="usp" style="left:178px">Format<small>Live online</small></div>
<div class="usp" style="left:428px">Duration<small>7 days</small></div>
<div class="usp" style="left:662px">USP<small>Refundable (incl. GST)</small></div>
</div>
<script>
const hk=document.getElementById('hk'),l1=hk.querySelector('.l1'),l2=hk.querySelector('.l2');
let s=74;function ap(){{l1.style.fontSize=(s*.8)+'px';l2.style.fontSize=s+'px';}}ap();
while(hk.scrollHeight>hk.clientHeight+1&&s>34){{s-=2;ap();}}
const b=document.getElementById('b');let t=46;while(b.getBoundingClientRect().width>790&&t>26){{t-=2;b.style.fontSize=t+'px';}}
const bb=b.getBoundingClientRect().bottom+14;hk.style.top=bb+'px';hk.style.height=(458-bb)+'px';
s=74;ap();while(hk.scrollHeight>hk.clientHeight+1&&s>30){{s-=2;ap();}}
</script>'''

os.makedirs(f"{HERE}/ads_template", exist_ok=True); os.makedirs(f"{HERE}/html_template", exist_ok=True)
def shot(html, out):
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={W},{H}", f"--screenshot={out}", "file://" + html], check=True, capture_output=True)
for r in R:
    p = f"{HERE}/html_template/sqe_t_{r[0]:02d}_{r[1]}.html"
    open(p, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{card(r)}</body></html>")
    shot(p, f"{HERE}/ads_template/sqe_t_{r[0]:02d}_{r[1]}.png")
sheet = Image.new("RGB", (5 * 512 + 6 * 14, 4 * 768 + 5 * 14), (225, 225, 225))
for i, r in enumerate(R):
    im = Image.open(f"{HERE}/ads_template/sqe_t_{r[0]:02d}_{r[1]}.png").convert("RGB").resize((512, 768), Image.LANCZOS)
    sheet.paste(im, (14 + (i % 5) * 526, 14 + (i // 5) * 782))
sheet.save(f"{HERE}/sheet_template.png"); print("done")
