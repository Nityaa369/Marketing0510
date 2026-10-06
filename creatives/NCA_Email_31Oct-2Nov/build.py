# NCA email-face ads, built on the Data Protection wave 4 pattern with its weak spots removed.
# Run: python3 build.py   (writes html/ and ads/)
import os, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]

ADS = [
 dict(stem="nca_e_01_experienced_5plus", ac="#1F3B5C", hi="#DCE7F5", bg="#E9EEF5",
      callout="Practising law for 5+ years?", subject="You'd make a great Canada-qualified lawyer",
      sender="Meera Iyer", init="M",
      mirror="You keep saying Canada was for lawyers who started young.",
      body="You don't have to pause your practice to start.",
      route="NCA exams from India, then bar licensing, then you practise in Canada.",
      sign="Meera"),
 dict(stem="nca_e_02_want_canada", ac="#1E6A48", hi="#DDF0E3", bg="#E8F1EB",
      callout="Want to practise law in Canada?", subject="Your Indian LLB can get you there",
      sender="Arjun Sethi", init="A",
      mirror="You keep saying you'd need a Canadian degree first.",
      body="The NCA assesses your Indian LLB directly and sets the exams.",
      route="NCA exams from India, then bar licensing, then you practise in Canada.",
      sign="Arjun"),
 dict(stem="nca_e_03_newly_enrolled", ac="#9E2328", hi="#F8DEDA", bg="#F5ECE8",
      callout="Newly enrolled advocate?", subject="You'd make a great lawyer in Canada",
      sender="Zoya Sheikh", init="Z",
      mirror="You keep saying your evenings go nowhere after court.",
      body="Our plan: about 2 hours a day to prepare for Canada's NCA exams.",
      route="NCA exams from India, then bar licensing, then you practise in Canada.",
      sign="Zoya"),
 dict(stem="nca_e_04_contract_lawyers", ac="#0E5A6C", hi="#D9ECF1", bg="#E5EEF2",
      callout="Corporate or contract lawyer?", subject="You'd make a great Canadian corporate lawyer",
      sender="Harpreet Gill", init="H",
      mirror="You keep saying your contracts never leave India.",
      body="Canada is common law, like India. Your drafting carries over.",
      route="NCA exams from India, then bar licensing, then you practise in Canada.",
      sign="Harpreet"),
]

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,sans-serif;background:%(bg)s;color:#14171F;display:flex;flex-direction:column;padding:38px 54px 30px}
.rail{text-align:center;font-size:24px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:#14171F}
.rail b{color:%(ac)s}
.card{background:#fff;border-radius:26px;margin-top:22px;padding:30px 44px 32px;box-shadow:0 16px 40px rgba(20,30,50,.14);flex:1;display:flex;flex-direction:column}
.tag{align-self:flex-start;background:#EEF0F4;color:#5A6170;font-size:24px;font-weight:800;padding:6px 16px;border-radius:8px}
.callout{font-size:68px;font-weight:900;line-height:1.04;letter-spacing:-.02em;color:%(ac)s;margin-top:18px}
.subject{font-size:60px;font-weight:900;line-height:1.08;letter-spacing:-.02em;margin-top:14px}
.from{display:flex;align-items:center;gap:18px;margin-top:20px;padding-bottom:18px;border-bottom:2px solid #E7E9EE}
.av{width:68px;height:68px;border-radius:50%%;background:%(ac)s;color:#fff;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center}
.nm{font-size:30px;font-weight:800}.to{font-size:24px;color:#6A7080}
.tm{margin-left:auto;font-size:24px;color:#6A7080;align-self:flex-start}
.txt{font-size:40px;line-height:1.32;margin-top:22px}
.hl{background:%(hi)s;font-weight:800;padding:2px 6px;border-radius:4px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.grow{flex:1;min-height:8px}
.close{font-size:40px;line-height:1.36}
.btn{background:%(ac)s;color:#fff;text-align:center;font-size:48px;font-weight:900;padding:24px;border-radius:70px;margin-top:24px}
.foot{text-align:center;font-size:25px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin-top:16px}
.lab{text-align:center;font-size:21px;color:#5A6170;margin-top:8px}
</style></head><body>
<div class="rail">LawSikho <b>|</b> NCA and Canadian bar bootcamp</div>
<div class="card">
<div class="tag">Inbox</div>
<div class="callout">%(callout)s</div>
<div class="subject">%(subject)s</div>
<div class="from"><div class="av">%(init)s</div><div><div class="nm">%(sender)s</div><div class="to">to me</div></div><div class="tm">9:42 PM</div></div>
<div class="txt">%(mirror)s</div>
<div class="txt">%(body)s <span class="hl">%(route)s</span></div>
<div class="grow"></div>
<div class="close">Rs 10 live bootcamp, 3 days. Join me?<br>%(sign)s</div>
</div>
<div class="btn">Join the Rs 10 bootcamp</div>
<div class="foot">Rs 10 incl. GST · Live only · Refundable</div>
<div class="lab">Dramatised email. Not a real learner.</div>
</body></html>"""

if __name__ == "__main__":
    for a in ADS:
        h = os.path.join(HERE, "html", a["stem"] + ".html"); open(h, "w").write(TPL % a)
        subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--window-size=1080,1350", "--screenshot=" + os.path.join(HERE, "ads", a["stem"] + ".png"),
                        "file://" + h], check=True, capture_output=True)
        print(a["stem"])
