import os, subprocess, sys, glob
OUT = sys.argv[1]
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
DELIVER = ("In our 3-day live bootcamp, we show you how to clear the NCA exams from India, how to find "
           "Canadian legal work while you prepare, and your 12-month plan to the Canadian bar.")
BASE = """*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,sans-serif;background:%(bg)s;color:#16130E;display:flex;flex-direction:column;padding:40px 54px 38px}
.rail{text-align:center;font-size:23px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:%(ac)s;margin-bottom:14px}
.callout{background:%(ac)s;color:#fff;font-size:62px;font-weight:900;line-height:1.04;letter-spacing:-.02em;text-transform:uppercase;text-align:center;padding:16px 22px 20px;border-radius:10px}
.head{font-size:62px;font-weight:900;line-height:1.08;letter-spacing:-.024em}
.head em{font-style:italic;color:%(ac)s}
.grow{flex:1;min-height:12px}
.offer{background:#fff;border:3px solid %(ac)s;border-radius:14px;padding:16px 28px 18px}
.ot{font-size:29px;font-weight:900;color:%(ac)s;margin-bottom:6px}
.tk{font-size:32px;font-weight:800;line-height:1.26;padding:4px 0}
.tk span{color:%(ac)s;margin-right:12px}
.bigbtn{background:%(ac)s;color:#fff;text-align:center;font-size:46px;font-weight:900;padding:20px 30px;border-radius:14px}
.foot{display:flex;justify-content:space-between;margin-top:14px;font-size:24px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3B352C}
"""
OFFER = """<div class="offer"><div class="ot">In 3 live days, we show you:</div>
<div class="tk"><span>&#10003;</span>Clear the NCA exams from India</div>
<div class="tk"><span>&#10003;</span>Find Canadian clients who pay in dollars</div>
<div class="tk"><span>&#10003;</span>Your 12-month plan to the Canadian bar</div></div>"""
FOOT = """<div class="bigbtn">Join the Rs 10 bootcamp</div>
<div class="foot"><div>Live only, no recordings</div><div>Rs 10 incl. GST · Refundable</div></div>"""

def page(css, body, pal):
    return "<!doctype html><html><head><meta charset='utf-8'><style>" + (BASE + css) % pal + "</style></head><body>" + body + "</body></html>"

# 01 SEARCH: the question they already typed, then the answer
def ad1():
    pal = dict(bg="#EEF1F6", ac="#1D3A6B")
    css = """.lab{font-size:26px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:%(ac)s;margin:24px 0 10px}
.bar{background:#fff;border:3px solid #C9D2E0;border-radius:60px;padding:22px 30px;display:flex;align-items:center;gap:20px;box-shadow:0 8px 22px rgba(20,40,80,.10)}
.mag{width:40px;height:40px;border:6px solid %(ac)s;border-radius:50%%;position:relative;flex:none}
.mag:after{content:'';position:absolute;width:6px;height:20px;background:%(ac)s;right:-10px;bottom:-16px;transform:rotate(-45deg);border-radius:3px}
.q{font-size:38px;font-weight:700;line-height:1.2;color:#1E2430}
.card{background:#fff;border-radius:18px;padding:28px 36px 30px;box-shadow:0 12px 30px rgba(20,40,80,.12);border-left:12px solid %(ac)s}
.chips{display:flex;align-items:center;gap:10px;margin-top:24px}
.card .head{font-size:70px}
.chip{flex:1;text-align:center;border:3px solid %(ac)s;border-radius:12px;padding:10px 6px;font-size:28px;font-weight:900;line-height:1.1}
.chip.end{background:%(ac)s;color:#fff}
.ar{font-size:34px;font-weight:900;color:%(ac)s}
.gloss{font-size:28px;font-weight:700;color:#3A4150;margin-top:14px}"""
    body = """<div class="rail">LawSikho · Canada law bootcamp</div>
<div class="callout">Final-year law students?</div>
<div class="lab">The search:</div>
<div class="bar"><div class="mag"></div><div class="q">practise law in canada with indian llb</div></div>
<div class="lab">The answer:</div>
<div class="card"><div class="head">Graduate in India. <em>Practise law in Canada.</em></div>
<div class="chips"><div class="chip">NCA exams</div><div class="ar">&#8594;</div><div class="chip">Bar licensing</div><div class="ar">&#8594;</div><div class="chip end">Licensed in Canada</div></div>
<div class="gloss">NCA: Canada's check on your Indian law degree.</div></div>
<div class="grow"></div>""" + OFFER + """<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

# 02 NAMEPLATES: the plate you have, the plate you add
def ad2():
    pal = dict(bg="#F4EDE6", ac="#9E2328")
    css = """.head{text-align:center;margin-top:26px;font-size:60px}
.plate{border-radius:10px;padding:28px 30px;text-align:center;position:relative}
.p1{background:linear-gradient(#8A6A3A,#6F5530);color:#FBF3DF;margin-top:28px;box-shadow:0 10px 24px rgba(60,40,10,.25)}
.p2{background:#fff;border:5px solid %(ac)s;color:%(ac)s;box-shadow:0 14px 30px rgba(120,20,20,.18)}
.nm{font-size:56px;font-weight:900;letter-spacing:.04em}
.tt{font-size:30px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin-top:6px}
.screw{position:absolute;top:50%%;width:16px;height:16px;border-radius:50%%;background:rgba(0,0,0,.25);margin-top:-8px}
.l{left:16px}.r{right:16px}
.mid{display:flex;align-items:center;justify-content:center;gap:16px;margin:16px 0;font-size:29px;font-weight:900;color:#2A2620}
.mid b{font-size:44px;color:%(ac)s}
.gloss{text-align:center;font-size:26px;font-weight:700;color:#4A3F36;margin-top:14px}"""
    body = """<div class="rail">LawSikho · Canada law bootcamp</div>
<div class="callout">Young lawyers with big plans?</div>
<div class="head">Practise in India today. <em>Get licensed in Canada next.</em></div>
<div class="plate p1"><span class="screw l"></span><span class="screw r"></span><div class="nm">ADV. YOUR NAME</div><div class="tt">Advocate · India</div></div>
<div class="mid"><b>&#8595;</b>NCA exams from India, then bar licensing<b>&#8595;</b></div>
<div class="plate p2"><div class="nm">YOUR NAME</div><div class="tt">Barrister and Solicitor · Canada</div></div>
<div class="gloss">NCA: Canada's check on your Indian law degree.</div>
<div class="grow"></div>""" + OFFER + """<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

# 03 ROUTE MAP: transit line from the LLB they hold to the licence
def ad3():
    pal = dict(bg="#E9F1EB", ac="#1E6A48")
    css = """.head{margin-top:24px;font-size:58px}
.map{background:#fff;border-radius:18px;margin-top:24px;padding:26px 34px;box-shadow:0 10px 26px rgba(20,60,40,.12);position:relative}
.map:before{content:'';position:absolute;left:64px;top:52px;bottom:60px;width:12px;background:%(ac)s;border-radius:6px}
.stn{display:flex;gap:30px;align-items:flex-start;padding:14px 0;position:relative}
.dot{width:42px;height:42px;border-radius:50%%;background:#fff;border:8px solid %(ac)s;flex:none;margin-left:3px;z-index:1}
.dot.done{background:%(ac)s}
.dot.end{width:56px;height:56px;margin-left:-4px;background:%(ac)s;border-color:#0F3D29}
.sn{font-size:40px;font-weight:900;line-height:1.1}
.sd{font-size:26px;font-weight:700;color:#3F4A43;margin-top:4px;line-height:1.25}
.end .sn{font-size:42px;color:%(ac)s}
.side{display:inline-block;margin-top:8px;background:#FFF6D6;border:2px dashed #B79A2E;border-radius:10px;padding:6px 14px;font-size:25px;font-weight:800;color:#5B4A10}"""
    body = """<div class="rail">LawSikho · Canada law bootcamp</div>
<div class="callout">Want to practise law in Canada?</div>
<div class="head">Qualify from India first. <em>Move once you are licensed.</em></div>
<div class="map">
<div class="stn"><div class="dot done"></div><div><div class="sn">Your Indian LLB</div></div></div>
<div class="stn"><div class="dot"></div><div><div class="sn">NCA exams</div><div class="sd">Canada's check on your degree, from India</div><div class="side">Meanwhile: Canadian legal work from India</div></div></div>
<div class="stn"><div class="dot"></div><div><div class="sn">Bar licensing</div></div></div>
<div class="stn end"><div class="dot end"></div><div><div class="sn">Practise law in Canada</div></div></div>
</div>
<div class="grow"></div>""" + OFFER + """<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

# 04 CALENDAR: their own week, with the Canadian work already in it
def ad4():
    pal = dict(bg="#E5EEF2", ac="#0E5A6C")
    css = """.head{margin-top:24px;font-size:56px}
.cal{background:#fff;border-radius:18px;margin-top:22px;overflow:hidden;box-shadow:0 10px 26px rgba(10,50,70,.12)}
.ct{background:#20343B;color:#fff;font-size:27px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;padding:14px 28px}
.row{display:flex;align-items:center;border-top:2px solid #DCE5E8;padding:20px 28px;gap:24px}
.d{width:96px;font-size:28px;font-weight:900;color:#5A6A70;letter-spacing:.06em}
.e{font-size:34px;font-weight:800;line-height:1.2}
.row.hi{background:%(ac)s}.row.hi .d,.row.hi .e{color:#fff}
.tag{font-size:22px;font-weight:900;background:#FFD54A;color:#2B2300;border-radius:6px;padding:3px 10px;margin-left:10px;letter-spacing:.06em}"""
    body = """<div class="rail">LawSikho · Canada law bootcamp</div>
<div class="callout">Corporate lawyers and associates?</div>
<div class="head">Work on Canadian matters from India, <em>while you qualify for the Canadian bar.</em></div>
<div class="cal"><div class="ct">Your week, from India</div>
<div class="row"><div class="d">MON</div><div class="e">Contracts for your Indian clients</div></div>
<div class="row"><div class="d">WED</div><div class="e">NCA exam prep, 2 hours</div></div>
<div class="row hi"><div class="d">THU</div><div class="e">Canadian startup: privacy policy <span class="tag">NEW CLIENT</span></div></div>
<div class="row"><div class="d">SAT</div><div class="e">Next step on your plan to the bar</div></div></div>
<div class="grow"></div>""" + OFFER + """<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

# 05 BROADSHEET: the news they have been waiting for
def ad5():
    pal = dict(bg="#F3EFE6", ac="#5A2A6C")
    css = """.mast{text-align:center;font-family:'Bitstream Charter',Caladea,serif;font-size:64px;font-weight:700;border-top:4px solid #16130E;border-bottom:4px solid #16130E;padding:6px 0 8px;margin-top:18px;letter-spacing:.02em}
.sub{display:flex;justify-content:space-between;font-size:21px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;border-bottom:2px solid #16130E;padding:6px 0;color:#3B352C}
.nh{font-family:'Bitstream Charter',Caladea,serif;font-size:76px;font-weight:700;line-height:1.06;margin-top:18px;text-align:center}
.nh em{color:%(ac)s}
.cols{display:flex;gap:26px;margin-top:20px}
.col{flex:1;border-top:4px solid %(ac)s;padding-top:10px}
.ck{font-size:25px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:%(ac)s;margin-bottom:6px}
.cl{font-size:33px;font-weight:700;line-height:1.3}
.cl b{font-weight:900}"""
    body = """<div class="rail">LawSikho · Canada law bootcamp</div>
<div class="callout">Ever thought of practising law abroad?</div>
<div class="mast">The LawSikho Brief</div>

<div class="nh">Your Indian LLB can get you <em>licensed in Canada.</em></div>
<div class="cols">
<div class="col"><div class="ck">The route</div><div class="cl"><b>1.</b> NCA exams, written from India<br><b>2.</b> Bar licensing<br><b>3.</b> Practise law in Canada</div></div>
<div class="col"><div class="ck">New since 1 March 2026</div><div class="cl">An English test and an Indigenous law course. We explain both.</div></div>
</div>
<div class="grow"></div>""" + OFFER + """<div class="grow"></div>""" + FOOT
    return page(css, body, pal)

ADS = [("nca_t5_01_final_year", ad1), ("nca_t5_02_young_lawyers", ad2), ("nca_t5_03_canadian_qualification", ad3),
       ("nca_t5_04_corporate_lawyers", ad4), ("nca_t5_05_practise_abroad", ad5)]
for stem, fn in ADS:
    h = os.path.join(OUT, "html", stem + ".html"); open(h, "w").write(fn())
    png = os.path.join(OUT, "ads", stem + ".png")
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--screenshot=" + png, "file://" + h], check=True, capture_output=True)
