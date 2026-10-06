import os, subprocess, sys, glob
OUT = sys.argv[1]
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
BASE = """*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,'Noto Color Emoji',sans-serif;background:%(bg)s;color:#16130E;display:flex;flex-direction:column;padding:40px 54px 38px}
.rail{text-align:center;font-size:23px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:%(ac)s;margin-bottom:14px}
.callout{background:%(ac)s;color:#fff;font-size:64px;font-weight:900;line-height:1.04;letter-spacing:-.02em;text-transform:uppercase;text-align:center;padding:16px 22px 20px;border-radius:10px}
.grow{flex:1;min-height:12px}
.bigbtn{background:%(ac)s;color:#fff;text-align:center;font-size:46px;font-weight:900;padding:20px 30px;border-radius:14px}
.foot{display:flex;justify-content:space-between;margin-top:14px;font-size:24px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3B352C}
"""
FOOT = """<div class="bigbtn">Join the Rs 10 bootcamp</div>
<div class="foot"><div>3 days · Live only, no recordings</div><div>Rs 10 incl. GST · Refundable</div></div>"""
RAIL = '<div class="rail">LawSikho · Canada law bootcamp</div>'
def page(css, body, pal):
    return "<!doctype html><html><head><meta charset='utf-8'><style>" + (BASE + css) % pal + "</style></head><body>" + body + "</body></html>"

# A. WHATSAPP CHAT: final-year law students
def chat():
    pal = dict(bg="#F1ECE4", ac="#1D3A6B")
    css = """.phone{margin-top:22px;border-radius:22px;overflow:hidden;box-shadow:0 14px 34px rgba(0,0,0,.16);display:flex;flex-direction:column}
.top{background:#075E54;color:#fff;display:flex;align-items:center;gap:18px;padding:16px 24px}
.av{width:58px;height:58px;border-radius:50%%;background:#C9D8D3;color:#075E54;font-weight:900;font-size:28px;display:flex;align-items:center;justify-content:center}
.nm{font-size:31px;font-weight:800}.st{font-size:21px;opacity:.85}
.wall{background:#ECE5DD;padding:20px 22px 22px;display:flex;flex-direction:column;gap:14px}
.b{max-width:84%%;font-size:34px;line-height:1.28;padding:14px 20px 10px;border-radius:14px;box-shadow:0 1px 1px rgba(0,0,0,.12)}
.me{align-self:flex-end;background:#DCF8C6;border-top-right-radius:2px}
.fr{align-self:flex-start;background:#fff;border-top-left-radius:2px}
.t{display:block;text-align:right;font-size:19px;color:#6B7B74;margin-top:4px}
.fwd{font-size:21px;font-style:italic;color:#6B7B74;margin-bottom:6px}
.fly{background:%(ac)s;color:#fff;border-radius:10px;padding:16px 20px;margin-top:4px}
.fh{font-size:34px;font-weight:900;line-height:1.15}
.fr2{display:flex;align-items:center;gap:8px;margin-top:12px}
.s{flex:1;background:#fff;color:%(ac)s;border-radius:8px;text-align:center;font-size:26px;font-weight:900;padding:8px 4px;line-height:1.1}
.a{font-weight:900;font-size:24px}
.fl{font-size:27px;font-weight:700;margin-top:10px;opacity:.95}"""
    body = RAIL + """<div class="callout">Final-year law students?</div>
<div class="phone"><div class="top"><div class="av">R</div><div><div class="nm">Riya (law school)</div><div class="st">online</div></div></div>
<div class="wall">
<div class="b me">Final year is almost done. I really want to practise law in Canada. No idea where to start 😕<span class="t">9:41 PM ✓✓</span></div>
<div class="b fr"><div class="fwd">Forwarded</div><div class="fly"><div class="fh">Practise law in Canada with your Indian LLB</div>
<div class="fr2"><div class="s">NCA exams, from India</div><div class="a">&#8594;</div><div class="s">Bar licensing</div><div class="a">&#8594;</div><div class="s">Practise in Canada</div></div>
<div class="fl">3 live days · each step explained · your 12-month plan</div></div><span class="t">9:43 PM</span></div>
<div class="b fr">Have you thought about this? The NCA exams can be written from India.<span class="t">9:43 PM</span></div>
</div></div>
<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

# B. NOTICE (gazette style, issued by LawSikho, no state emblem)
def notice():
    pal = dict(bg="#EDE6D6", ac="#7A1F1F")
    css = """.paper{margin-top:24px;background:#FBF8EF;border:3px solid #2A2015;outline:2px solid #2A2015;outline-offset:-12px;padding:40px 50px 34px;font-family:'Bitstream Charter',Caladea,serif;position:relative;box-shadow:0 12px 30px rgba(60,40,10,.16)}
.iss{text-align:center;font-family:Inter,sans-serif;font-size:22px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#4A3B28}
.pt{text-align:center;font-size:58px;font-weight:700;letter-spacing:.08em;margin-top:6px;border-bottom:2px solid #2A2015;padding-bottom:10px}
.subj{font-size:38px;font-weight:700;margin-top:18px;line-height:1.25}
.bd{font-size:35px;line-height:1.36;margin-top:12px}
ol{margin:14px 0 0 48px;font-size:42px;line-height:1.4;font-weight:700}
ol li span{font-weight:400;font-size:31px;color:#3B3024}
.stamp{flex:none;width:170px;height:170px;border:5px solid %(ac)s;border-radius:50%%;color:%(ac)s;display:flex;align-items:center;justify-content:center;text-align:center;font-family:Inter,sans-serif;font-weight:900;font-size:22px;letter-spacing:.06em;line-height:1.15;transform:rotate(-14deg);opacity:.9}
.sig{font-size:28px;font-style:italic;color:#3B3024}
.sigrow{display:flex;justify-content:space-between;align-items:center;margin-top:16px}"""
    body = RAIL + """<div class="callout">Lawyers who want to practise in Canada?</div>
<div class="paper"><div class="iss">Issued by LawSikho</div><div class="pt">NOTICE</div>
<div class="subj">For Indian lawyers: your route to practise in Canada</div>
<ol><li>Clear the NCA exams<br><span>Canada's check on your Indian law degree, written from India</span></li>
<li>Pass the bar licensing</li><li>Practise law in Canada</li></ol>
<div class="bd">Each step is explained in a 3-day live bootcamp, with your 12-month plan.</div>
<div class="sigrow"><div class="sig">By order, LawSikho</div><div class="stamp">LAWSIKHO<br>CANADA<br>BOOTCAMP</div></div></div>
<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

# C. MEME: young lawyers, two-panel before / after
def meme():
    pal = dict(bg="#EFEAF3", ac="#5A2A6C")
    css = """.memebox{margin-top:22px;border:4px solid #111;background:#fff;display:flex;flex-direction:column}
.pn{display:flex;align-items:center;gap:26px;padding:30px 30px;min-height:385px}
.pn+.pn{border-top:4px solid #111}
.face{font-size:170px;line-height:1;flex:none}
.cap{font-size:27px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:#6A6070}
.say{font-size:52px;font-weight:900;line-height:1.14;margin-top:8px}
.p2{background:#F6F0FA}.p2 .say{color:%(ac)s}
.route{display:flex;gap:10px;align-items:center;margin-top:14px}
.s{background:%(ac)s;color:#fff;border-radius:8px;font-size:27px;font-weight:900;padding:8px 12px}
.ar{font-weight:900;color:%(ac)s;font-size:26px}
.wm{font-size:30px;font-weight:900;color:#fff;background:#111;text-align:center;padding:14px}"""
    body = RAIL + """<div class="callout">Lawyers with 0 to 2 years of practice?</div>
<div class="memebox">
<div class="pn"><div class="face">😩</div><div><div class="cap">Me, a year ago</div><div class="say">"Practise in Canada? I would need a foreign law degree."</div></div></div>
<div class="pn p2"><div class="face">😎</div><div><div class="cap">Me, after the bootcamp</div><div class="say">"My Indian LLB is enough to start."</div>
<div class="route"><div class="s">NCA exams</div><div class="ar">&#8594;</div><div class="s">Bar licensing</div><div class="ar">&#8594;</div><div class="s">Practise in Canada</div></div></div></div>
<div class="wm">3 live days · each step explained · your 12-month plan</div>
</div>
<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

for stem, fn in [("nca_f_01_chat_final_year", chat), ("nca_f_02_notice_canada_lawyers", notice), ("nca_f_03_meme_lawyers_0to2yrs", meme)]:
    h = os.path.join(OUT, "html", stem + ".html"); open(h, "w").write(fn())
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--screenshot=" + os.path.join(OUT, "ads", stem + ".png"), "file://" + h],
                   check=True, capture_output=True)
