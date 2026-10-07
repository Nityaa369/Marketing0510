import os, subprocess, sys, glob
OUT = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
BASE = """*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,'Noto Color Emoji',sans-serif;background:%(bg)s;color:#16130E;display:flex;flex-direction:column;padding:40px 54px 38px}
.rail{text-align:center;font-size:23px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:%(ac)s;margin-bottom:14px}
.callout{background:%(ac)s;color:#fff;font-size:68px;font-weight:900;line-height:1.04;letter-spacing:-.02em;text-transform:uppercase;text-align:center;padding:16px 22px 20px;border-radius:10px}
.head{font-size:58px;font-weight:900;line-height:1.08;letter-spacing:-.02em;text-align:center;margin-top:24px;color:#16130E}
.gloss{font-size:27px;font-weight:700;text-align:center;margin-top:12px;color:#3B352C}
.chips{display:flex;align-items:center;gap:8px;margin-top:16px}
.chips .s{flex:1;background:#fff;color:%(ac)s;border:3px solid %(ac)s;border-radius:8px;text-align:center;font-size:27px;font-weight:900;padding:10px 4px;line-height:1.1}
.chips .a{font-weight:900;font-size:28px;color:%(ac)s}
.grow{flex:1;min-height:12px}
.bigbtn{margin-top:24px;background:%(ac)s;color:#fff;text-align:center;font-size:46px;font-weight:900;padding:20px 30px;border-radius:14px}
.foot{display:flex;justify-content:space-between;margin-top:14px;font-size:24px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3B352C}
.lbl{font-size:22px;font-weight:700;color:#5A5348;text-align:center;margin-top:10px}
"""
FOOT = """<div class="bigbtn">Join the Rs 10 bootcamp</div>
<div class="foot"><div>3 days · Live only</div><div>Rs 10 incl. GST · Refundable</div></div>"""
RAIL = '<div class="rail">LawSikho · Canada law bootcamp</div>'
GLOSS = '<div class="gloss">NCA: Canada\'s check on your Indian law degree.</div>'
CHIPS = '<div class="chips"><div class="s">NCA exams, from India</div><div class="a">&#8594;</div><div class="s">Bar licensing</div><div class="a">&#8594;</div><div class="s">Practise in Canada</div></div>'
def page(css, body, pal):
    return "<!doctype html><html><head><meta charset='utf-8'><style>" + (BASE + css) % pal + "</style></head><body>" + body + "</body></html>"

def chat():  # 1 experienced advocates
    pal = dict(bg="#F1ECE4", ac="#1D3A6B")
    css = """.phone{margin-top:22px;border-radius:22px;overflow:hidden;box-shadow:0 14px 34px rgba(0,0,0,.16)}
.top{background:#075E54;color:#fff;display:flex;align-items:center;gap:18px;padding:16px 24px}
.av{width:58px;height:58px;border-radius:50%%;background:#C9D8D3;color:#075E54;font-weight:900;font-size:28px;display:flex;align-items:center;justify-content:center}
.nm{font-size:31px;font-weight:800}.st{font-size:21px;opacity:.85}
.wall{background:#ECE5DD;padding:18px 22px 20px;display:flex;flex-direction:column;gap:12px}
.b{max-width:80%%;font-size:34px;line-height:1.22;padding:12px 20px 8px;border-radius:14px;box-shadow:0 1px 1px rgba(0,0,0,.12)}
.me{align-self:flex-end;background:#DCF8C6;border-top-right-radius:2px}
.fr{align-self:flex-start;background:#fff;border-top-left-radius:2px}
.t{display:block;text-align:right;font-size:19px;color:#6B7B74;margin-top:4px}"""
    body = RAIL + """<div class="callout">Experienced advocates?</div>
<div class="phone"><div class="top"><div class="av">A</div><div><div class="nm">Adv. Mehta</div><div class="st">online</div></div></div>
<div class="wall">
<div class="b fr">You can write Canada's exams from India?<span class="t">9:41 PM</span></div>
<div class="b me">Yes. Online. Every month.<span class="t">9:42 PM ✓✓</span></div>
<div class="b fr">And my chamber?<span class="t">9:42 PM</span></div>
<div class="b me">Stays open. You study around your cause list.<span class="t">9:43 PM ✓✓</span></div>
</div></div>
<div class="lbl">Dramatised chat. Not a real learner.</div>
<div class="head">Practise law in Canada too.</div>""" + GLOSS + CHIPS + '<div class="grow"></div>' + FOOT
    return page(css, body, pal)

def causelist():  # 2 litigators
    pal = dict(bg="#EEF2EA", ac="#2F5D3A")
    css = """.paper{margin-top:22px;flex:1;background:#FFFEF8;border:3px solid #2A2A20;padding:30px 30px;display:flex;flex-direction:column;font-family:'Bitstream Charter',Caladea,serif}
.ttl{text-align:center;font-size:36px;font-weight:700;letter-spacing:.08em;border-bottom:2px solid #2A2A20;padding-bottom:10px}
.sub{text-align:center;font-family:Inter,sans-serif;font-size:22px;font-weight:700;color:#5A5A48;margin:8px 0 12px}
table{width:100%%;flex:1;border-collapse:collapse;font-size:38px}
td,th{border:2px solid #2A2A20;padding:10px 16px;text-align:left}
th{font-family:Inter,sans-serif;font-size:22px;letter-spacing:.1em;text-transform:uppercase;background:#E8E8D8}
tr.hi td{background:%(ac)s;color:#fff;font-weight:700;font-size:42px}"""
    body = RAIL + """<div class="callout">In court every week?</div>
<div class="paper"><div class="ttl">CAUSE LIST</div><div class="sub">A dramatised list. Issued by LawSikho.</div>
<table><tr><th>Item</th><th>Matter</th><th>Status</th></tr>
<tr><td>11</td><td>Stay application</td><td>Listed</td></tr>
<tr><td>12</td><td>Bail application</td><td>Listed</td></tr>
<tr><td>13</td><td>Written statement</td><td>Listed</td></tr>
<tr class="hi"><td>14</td><td>Canada qualification</td><td>Pick your exam month</td></tr>
<tr><td>15</td><td>Final arguments</td><td>Listed</td></tr>
<tr><td>16</td><td>Evidence</td><td>Listed</td></tr></table></div>
<div class="head">Add Canada to your cause list.</div>""" + GLOSS + CHIPS + '<div class="grow"></div>' + FOOT
    return page(css, body, pal)

def card():  # 4 fresh graduates
    pal = dict(bg="#FBEFE6", ac="#B2451E")
    css = """.card{margin:34px auto 0;width:930px;flex:1;margin-bottom:10px;background:#fff;border-radius:18px;box-shadow:0 18px 40px rgba(120,60,20,.22);border-left:22px solid %(ac)s;padding:44px 52px;display:flex;flex-direction:column;justify-content:center;transform:rotate(-2deg)}
.n{font-size:92px;font-weight:900;letter-spacing:-.02em}
.d{font-size:44px;font-weight:700;color:#5A5348;margin-top:6px}
.q{font-size:68px;font-weight:900;color:%(ac)s;line-height:1.1;margin-top:28px}
.ip{font-size:36px;font-weight:700;color:#5A5348;margin-top:10px}"""
    body = RAIL + """<div class="callout">Fresh out of law school?</div>
<div class="card"><div class="n">Your Name</div><div class="d">LLB (India)</div>
<div class="q">Canada-qualified lawyer</div><div class="ip">In progress. One exam at a time, from India.</div></div>
<div class="lbl">Sample card</div>
<div class="head">Qualify as a lawyer in Canada.</div>""" + GLOSS + CHIPS  + FOOT
    return page(css, body, pal)

def route():  # 6 planning to move
    pal = dict(bg="#EAF1F6", ac="#1F5C7A")
    css = """.map{margin-top:26px;flex:1;display:flex;flex-direction:column;gap:0;position:relative}
.st{flex:1;display:flex;align-items:center;gap:30px;background:#fff;border:3px solid %(ac)s;border-radius:16px;padding:20px 30px}
.no{flex:none;width:110px;height:110px;border-radius:50%%;background:%(ac)s;color:#fff;font-size:64px;font-weight:900;display:flex;align-items:center;justify-content:center}
.tt{font-size:58px;font-weight:900;line-height:1.1}
.ss{font-size:34px;font-weight:700;color:#4A5A62;margin-top:4px}
.ln{height:30px;width:6px;background:%(ac)s;margin-left:80px}"""
    body = RAIL + """<div class="callout">Planning to move to Canada?</div>
<div class="map">
<div class="st"><div class="no">1</div><div><div class="tt">NCA exams</div><div class="ss">Written online, from India, before you move</div></div></div><div class="ln"></div>
<div class="st"><div class="no">2</div><div><div class="tt">Bar licensing</div><div class="ss">Province by province</div></div></div><div class="ln"></div>
<div class="st"><div class="no">3</div><div><div class="tt">Practise in Canada</div><div class="ss">With a Canadian qualification</div></div></div></div>
<div class="head">Start Canada's exams from India.</div>""" + GLOSS  + FOOT
    return page(css, body, pal)

def calendar():  # 8 associates
    pal = dict(bg="#F4EEFA", ac="#5B2C83")
    css = """.cal{margin-top:24px;flex:1;grid-auto-rows:1fr;background:#fff;border:3px solid %(ac)s;border-radius:16px;padding:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.m{border:2px solid #CFC3DD;border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-size:52px;font-weight:800;color:#4A3B5C}
.m.on{background:%(ac)s;color:#fff;border-color:%(ac)s;font-size:40px;line-height:1.1;padding:8px 4px;box-shadow:0 0 0 6px #fff,0 0 0 10px %(ac)s}
.sm{font-size:22px;font-weight:700;display:block;margin-top:4px}"""
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    cells = "".join('<div class="m on">Your exam month<span class="sm">%s</span></div>' % m if m=="Mar" else '<div class="m">%s</div>' % m for m in months)
    body = RAIL + """<div class="callout">Law firm associates?</div>
<div class="cal">""" + cells + """</div>
<div class="lbl">Sample calendar</div>
<div class="head">Pick the month. Qualify in Canada.</div><div class="gloss">The exams are online, from India. Choose them around your billable hours.</div>""" + GLOSS.replace('margin-top:12px','')  + FOOT
    return page(css, body, pal)

for stem, fn in [("nca_c_01_chat_advocates", chat), ("nca_c_02_causelist_litigators", causelist), ("nca_c_04_card_fresh_grads", card),
                 ("nca_c_06_route_movers", route), ("nca_c_08_calendar_associates", calendar)]:
    h = os.path.join(OUT, "html", stem + ".html"); open(h, "w").write(fn())
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--screenshot=" + os.path.join(OUT, "ads", stem + ".png"), "file://" + h],
                   check=True, capture_output=True)
