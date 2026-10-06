import os, subprocess, sys, glob
OUT = sys.argv[1]
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
SERIF = "'Bitstream Charter',Caladea,serif"
BASE = """*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,sans-serif;background:%(bg)s;color:#16130E;display:flex;flex-direction:column;padding:40px 54px 38px}
.rail{text-align:center;font-size:23px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:%(ac)s;margin-bottom:14px}
.callout{background:%(ac)s;color:#fff;font-size:64px;font-weight:900;line-height:1.04;letter-spacing:-.02em;text-transform:uppercase;text-align:center;padding:16px 22px 20px;border-radius:10px}
.head{font-size:62px;font-weight:900;line-height:1.08;letter-spacing:-.022em;margin-top:24px}
.head em{font-style:italic;color:%(ac)s}
.grow{flex:1;min-height:12px}
.route{display:flex;align-items:center;gap:10px}
.st{flex:1;text-align:center;border:3px solid %(ac)s;border-radius:12px;padding:12px 6px;font-size:29px;font-weight:900;line-height:1.1;background:#fff}
.st.end{background:%(ac)s;color:#fff}
.ar{font-size:34px;font-weight:900;color:%(ac)s}
.strip{text-align:center;font-size:30px;font-weight:800;margin-top:16px;color:#2A2620}
.bigbtn{background:%(ac)s;color:#fff;text-align:center;font-size:46px;font-weight:900;padding:20px 30px;border-radius:14px;margin-top:18px}
.foot{display:flex;justify-content:space-between;margin-top:14px;font-size:24px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3B352C}
"""
ROUTE = """<div class="route"><div class="st">NCA exams, from India</div><div class="ar">&#8594;</div><div class="st">Bar licensing</div><div class="ar">&#8594;</div><div class="st end">Practise in Canada</div></div>
<div class="strip">3 live days: each step explained, with your 12-month plan</div>"""
FOOT = """<div class="bigbtn">Join the Rs 10 bootcamp</div>
<div class="foot"><div>Live only, no recordings</div><div>Rs 10 incl. GST · Refundable anytime</div></div>"""
RAIL = '<div class="rail">LawSikho · Canada law bootcamp</div>'
def page(css, body, pal):
    return "<!doctype html><html><head><meta charset='utf-8'><style>" + (BASE + css) % pal + "</style></head><body>" + body + "</body></html>"

# S1 EDITORIAL, from sqe_h_secondact (0.63x, cheapest SQE ad) + sqr_c_editorial (0.67x)
def s1():
    pal = dict(bg="#F5F1E8", ac="#1F3B5C")
    css = """.ed{background:#FFFDF8;margin-top:28px;padding:44px 48px 48px;border-top:8px solid %(ac)s;box-shadow:0 10px 26px rgba(0,0,0,.10)}
.kick{font-size:24px;font-weight:900;letter-spacing:.16em;text-transform:uppercase;color:%(ac)s}
.eh{font-family:""" + SERIF + """;font-size:92px;font-weight:700;line-height:1.06;margin-top:12px}
.eh em{color:%(ac)s}
.dek{font-family:""" + SERIF + """;font-size:40px;line-height:1.35;margin-top:18px;color:#3A3328;border-left:6px solid %(ac)s;padding-left:20px}"""
    body = RAIL + """<div class="callout">Lawyers practising for 5+ years?</div>
<div class="ed"><div class="kick">For experienced advocates</div>
<div class="eh">Start your Canadian qualification <em>without pausing your practice.</em></div>
<div class="dek">The NCA exams, Canada's check on your Indian law degree, are written from India.</div></div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

# S2 ELIGIBILITY CHECK, from Ramanuj-approved sqd_routes "Are you eligible to migrate to the UK?"
def s2():
    pal = dict(bg="#EAF1EC", ac="#1E6A48")
    css = """.clip{background:#fff;margin-top:30px;border-radius:16px;padding:40px 42px 40px;box-shadow:0 10px 26px rgba(20,60,40,.12);position:relative}
.clip:before{content:'';position:absolute;top:-16px;left:50%%;margin-left:-90px;width:180px;height:32px;background:#7C8A80;border-radius:8px}
.ct{font-size:27px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:%(ac)s;text-align:center}
.q{font-size:64px;font-weight:900;line-height:1.08;text-align:center;margin-top:8px}
.row{display:flex;align-items:flex-start;gap:22px;margin-top:30px}
.bx{width:52px;height:52px;border:4px solid %(ac)s;border-radius:8px;flex:none;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:900;color:#fff;background:%(ac)s}
.bx.o{background:#fff;color:%(ac)s}
.rt{font-size:40px;font-weight:800;line-height:1.2}
.rt span{display:block;font-size:29px;font-weight:700;color:#4A564E;margin-top:4px}"""
    body = RAIL + """<div class="callout">Lawyers who want to practise in Canada?</div>
<div class="clip"><div class="ct">Eligibility check</div><div class="q">Are you eligible to apply?</div>
<div class="row"><div class="bx">&#10003;</div><div class="rt">An Indian LLB from a recognised university</div></div>
<div class="row"><div class="bx">&#10003;</div><div class="rt">An English test<span>Required for every applicant since 1 March 2026</span></div></div>
<div class="row"><div class="bx o">?</div><div class="rt">The NCA exams<span>Canada's check on your Indian law degree, written from India</span></div></div></div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

# S3 DAY PLANNER, from sqe_r_newadvocates "Become a UK solicitor in two hours a day"
def s3():
    pal = dict(bg="#F4ECE6", ac="#9E2328")
    css = """.day{background:#fff;margin-top:30px;border-radius:16px;padding:32px 32px;box-shadow:0 10px 26px rgba(90,20,20,.12)}
.dt{font-size:26px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:#5A4A44;margin-bottom:14px}
.bar{display:flex;height:230px;border-radius:12px;overflow:hidden;border:3px solid #2A2015}
.sg{display:flex;align-items:center;justify-content:center;text-align:center;font-size:33px;font-weight:900;line-height:1.1;padding:0 6px;border-right:3px solid #2A2015}
.sg:last-child{border-right:0}
.c1{flex:7;background:#E9E2D8}.c2{flex:2;background:#F6F1EA}.c3{flex:2;background:%(ac)s;color:#fff}
.tl{display:flex;justify-content:space-between;font-size:26px;font-weight:800;color:#7A6A62;margin-top:8px}"""
    body = RAIL + """<div class="callout">Newly enrolled advocates?</div>
<div class="head">Prepare for Canada's NCA exams <em>in 2 hours a day.</em></div>
<div class="day"><div class="dt">Your day, from India</div>
<div class="bar"><div class="sg c1">Court and your practice</div><div class="sg c2">Family</div><div class="sg c3">NCA prep</div></div>
<div class="tl"><span>10 AM</span><span>6 PM</span><span>9 PM</span><span>11 PM</span></div></div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

# S4 REDLINED CONTRACT, from sqe_e_contracts "You already draft under English law. Qualify in it."
def s4():
    pal = dict(bg="#E6EEF2", ac="#0E5A6C")
    css = """.doc{background:#fff;margin-top:28px;padding:40px 44px;box-shadow:0 10px 26px rgba(10,50,70,.14);font-family:""" + SERIF + """;position:relative}
.dh{font-size:36px;font-weight:700;text-align:center;letter-spacing:.06em}
.cl{font-size:38px;line-height:1.4;margin-top:18px;color:#2B2B2B}
.cl b{font-weight:700}
.hl{background:#FFE58A;padding:0 4px}
.cm{font-family:Inter,sans-serif;margin-top:22px;margin-left:auto;width:78%%;background:#EAF4F7;border-left:6px solid %(ac)s;padding:12px 18px;font-size:31px;font-weight:800;color:%(ac)s}"""
    body = RAIL + """<div class="callout">Corporate and contract lawyers?</div>
<div class="head">You already draft under common law. <em>Qualify to practise it in Canada.</em></div>
<div class="doc"><div class="dh">SERVICES AGREEMENT</div>
<div class="cl"><b>18. Governing law.</b> <span class="hl">This Agreement is governed by the laws of the Province of Ontario and the federal laws of Canada.</span></div>
<div class="cm">Review a Canadian contract, live, on Day 3</div></div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

for stem, fn in [("nca_s_01_editorial_5plus_years", s1), ("nca_s_02_eligibility_check", s2),
                 ("nca_s_03_planner_newly_enrolled", s3), ("nca_s_04_redline_contract_lawyers", s4)]:
    h = os.path.join(OUT, "html", stem + ".html"); open(h, "w").write(fn())
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--screenshot=" + os.path.join(OUT, "ads", stem + ".png"), "file://" + h],
                   check=True, capture_output=True)
