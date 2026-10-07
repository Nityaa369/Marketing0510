# NCA "Dual-qualify" set. Frame from BARBRI SQE ("Dual-Qualify as a Solicitor"), offer from BARBRI
# Bar Prep Preview ("try the real thing"), one objection per face. Run: python3 build.py
import os, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
SERIF = "'Bitstream Charter',Caladea,serif"
BASE = """*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,'Noto Color Emoji',sans-serif;background:%(bg)s;color:#15130F;display:flex;flex-direction:column;padding:40px 54px 36px}
.rail{text-align:center;font-size:23px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:%(ac)s;margin-bottom:14px}
.callout{background:%(ac)s;color:#fff;font-size:62px;font-weight:900;line-height:1.04;letter-spacing:-.02em;text-transform:uppercase;text-align:center;padding:16px 22px 20px;border-radius:12px}
.head{font-size:66px;font-weight:900;line-height:1.06;letter-spacing:-.024em;margin-top:24px;text-align:center}
.head em{font-style:italic;color:%(ac)s}
.grow{flex:1;min-height:10px}
.rt{text-align:center;font-size:24px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:#2A2620;margin-bottom:10px}
.route{display:flex;align-items:center;gap:10px}
.route .s{flex:1;text-align:center;border:3px solid %(ac)s;border-radius:12px;padding:14px 6px;font-size:30px;font-weight:900;line-height:1.1;background:#fff}
.route .s.e{background:%(ac)s;color:#fff}.route .a{font-size:34px;font-weight:900;color:%(ac)s}
.gloss{text-align:center;font-size:25px;font-weight:700;color:#4A443B;margin-top:10px}
.bigbtn{background:%(ac)s;color:#fff;text-align:center;font-size:48px;font-weight:900;padding:22px 30px;border-radius:14px;margin-top:20px}
.foot{display:flex;justify-content:space-between;margin-top:14px;font-size:24px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3B352C}
"""
ROUTE = '<div class="rt">The route</div><div class="route"><div class="s">NCA exams, from India</div><div class="a">&#8594;</div><div class="s">Bar licensing</div><div class="a">&#8594;</div><div class="s e">Practise in Canada</div></div><div class="gloss">NCA: Canada&#39;s check on your Indian law degree.</div>'
FOOT = """<div class="bigbtn">Try the route for Rs 10</div>
<div class="foot"><div>3 live days · No recordings</div><div>Rs 10 incl. GST · Refundable</div></div>"""
RAIL = '<div class="rail">LawSikho · NCA and Canadian bar bootcamp</div>'
def page(css, body, pal):
    return "<!doctype html><html><head><meta charset='utf-8'><style>" + (BASE + css) % pal + "</style></head><body>" + body + "</body></html>"

# D1 TWO LICENCE CARDS: experienced lawyers. Objection: "I'd have to give up my practice"
def d1():
    pal = dict(bg="#EDF0F5", ac="#1F3B5C")
    css = """.cards{display:flex;flex-direction:column;gap:26px;margin-top:34px}
.card{border-radius:18px;padding:40px 34px;display:flex;align-items:center;gap:26px;box-shadow:0 12px 28px rgba(20,30,50,.14)}
.c1{background:#fff;border:4px solid #C9D1DD}.c2{background:%(ac)s;color:#fff}
.flag{font-size:96px;line-height:1;flex:none}
.ct{font-size:26px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;opacity:.8}
.cn{font-size:52px;font-weight:900;line-height:1.1;margin-top:4px}
.st{margin-left:auto;font-size:28px;font-weight:900;padding:8px 16px;border-radius:30px;white-space:nowrap}
.c1 .st{background:#E3F2E7;color:#1B6B3A}.c2 .st{background:#fff;color:%(ac)s}
.obj{text-align:center;font-size:37px;font-weight:700;margin-top:28px;line-height:1.3}"""
    body = RAIL + """<div class="callout">Practising law for 5+ years?</div>
<div class="head">Keep your Indian licence. <em>Add Canada's.</em></div>
<div class="cards">
<div class="card c1"><div class="flag">&#x1F1EE;&#x1F1F3;</div><div><div class="ct">Licence 1</div><div class="cn">Advocate, India</div></div><div class="st">&#10003; You have it</div></div>
<div class="card c2"><div class="flag">&#x1F1E8;&#x1F1E6;</div><div><div class="ct">Licence 2</div><div class="cn">Lawyer, Canada</div></div><div class="st">Add it</div></div></div>
<div class="obj">Keep your practice running. The NCA exams are written from India.</div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

# D2 MYTH / FACT: want to practise in Canada. Objection: "I'd need a Canadian degree"
def d2():
    pal = dict(bg="#E8F1EB", ac="#1E6A48")
    css = """.mf{margin-top:30px;display:flex;flex-direction:column;gap:20px}
.row{border-radius:18px;padding:36px 38px}
.my{background:#fff;border:4px dashed #C25A4A}
.fa{background:%(ac)s;color:#fff;box-shadow:0 12px 28px rgba(20,60,40,.18)}
.lb{font-size:28px;font-weight:900;letter-spacing:.16em;text-transform:uppercase}
.my .lb{color:#C25A4A}.fa .lb{color:#BFE7CC}
.tx{font-size:56px;font-weight:900;line-height:1.14;margin-top:8px}
.my .tx{text-decoration:line-through;text-decoration-color:#C25A4A;text-decoration-thickness:5px;color:#5A5048}"""
    body = RAIL + """<div class="callout">Want to practise law in Canada?</div>
<div class="head">Practise law in Canada <em>with the LLB you already have.</em></div>
<div class="mf">
<div class="row my"><div class="lb">Myth</div><div class="tx">You need a Canadian law degree first.</div></div>
<div class="row fa"><div class="lb">Fact</div><div class="tx">The NCA assesses your Indian LLB and sets the exams.</div></div></div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

# D3 PREVIEW TICKET: newly enrolled. Objection: "it's too big a commitment to start"
def d3():
    pal = dict(bg="#F5ECE8", ac="#9E2328")
    css = """.tk{margin-top:30px;display:flex;border-radius:20px;overflow:hidden;box-shadow:0 14px 30px rgba(90,20,20,.18)}
.main{flex:1;background:#fff;padding:36px 34px;border-right:4px dashed #E2C9C3}
.stub{width:230px;background:%(ac)s;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.adm{font-size:26px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:%(ac)s}
.tt{font-size:50px;font-weight:900;line-height:1.1;margin-top:8px}
.li{font-size:36px;font-weight:700;line-height:1.35;margin-top:14px;color:#3A2E2A}
.li span{color:%(ac)s;font-weight:900;margin-right:10px}
.pr{font-size:76px;font-weight:900;line-height:1}.ps{font-size:24px;font-weight:800;margin-top:8px;letter-spacing:.06em}
.obj{text-align:center;font-size:37px;font-weight:700;margin-top:28px}"""
    body = RAIL + """<div class="callout">Newly enrolled advocate?</div>
<div class="head">Become a lawyer in Canada. <em>Try the route first, for Rs 10.</em></div>
<div class="tk"><div class="main"><div class="adm">Admit one · Live</div><div class="tt">3 days on the Canada route</div>
<div class="li"><span>&#10003;</span>Write an NCA-style answer</div><div class="li"><span>&#10003;</span>Your 12-month plan</div><div class="li"><span>&#10003;</span>About 2 hours a day, after court</div></div>
<div class="stub"><div class="pr">Rs 10</div><div class="ps">INCL. GST<br>REFUNDABLE</div></div></div>
<div class="obj">If it is not for you, ask for the Rs 10 back.</div>
<div class="grow"></div>""" + ROUTE + FOOT
    return page(css, body, pal)

# D4 SPLIT SCREEN: contract lawyers. Objection: "my skills only work in India"
def d4():
    pal = dict(bg="#E5EEF2", ac="#0E5A6C")
    css = """.split{margin-top:30px;display:flex;border-radius:18px;overflow:hidden;box-shadow:0 12px 28px rgba(10,50,70,.14)}
.col{flex:1;padding:24px 26px}
.l{background:#fff}.r{background:%(ac)s;color:#fff}
.ch{font-size:30px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;padding-bottom:12px;border-bottom:3px solid currentColor;margin-bottom:8px}
.l .ch{color:%(ac)s}
.it{font-size:35px;font-weight:800;padding:11px 0;border-bottom:1px solid rgba(0,0,0,.08)}
.r .it{border-color:rgba(255,255,255,.2)}
.it span{margin-right:10px}
.obj{text-align:center;font-size:37px;font-weight:700;margin-top:28px;line-height:1.3}"""
    rows = ["Shareholders' agreements", "Service contracts", "NDAs", "Privacy policies"]
    body = RAIL + """<div class="callout">Corporate or contract lawyer?</div>
<div class="head">Qualify in Canada. <em>Draft for Canadian clients too.</em></div>
<div class="split"><div class="col l"><div class="ch">India, today</div>%s</div><div class="col r"><div class="ch">Canada, next</div>%s</div></div>
<div class="obj">Canada is common law, like India. Your drafting carries over.</div>
<div class="grow"></div>""" % ("".join('<div class="it"><span>&#10003;</span>%s</div>' % x for x in rows),
                               "".join('<div class="it"><span>&#10003;</span>%s</div>' % x for x in rows)) + ROUTE + FOOT
    return page(css, body, pal)

ADS = [("nca_d_01_two_licences_5plus", d1), ("nca_d_02_myth_fact_canada", d2),
       ("nca_d_03_ticket_newly_enrolled", d3), ("nca_d_04_split_contract_lawyers", d4)]
if __name__ == "__main__":
    for stem, fn in ADS:
        h = os.path.join(HERE, "html", stem + ".html"); open(h, "w").write(fn())
        subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--window-size=1080,1350", "--screenshot=" + os.path.join(HERE, "ads", stem + ".png"), "file://" + h],
                       check=True, capture_output=True)
        print(stem)
