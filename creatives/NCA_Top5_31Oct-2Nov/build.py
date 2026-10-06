import os, subprocess, sys
OUT = sys.argv[1]
ADS = [
 dict(stem="nca_t5_01_final_year", accent="#1D3A6B", bg="#EFEBE1", line="#C9C1AE",
      callout="Final-year law students?", hs=78, qual="LLB · BA LLB · BBA LLB · FINAL YEAR",
      head="Start building a Canadian law career <em>in your final year.</em>"),
 dict(stem="nca_t5_02_young_lawyers", accent="#9E2328", bg="#F3ECE6", line="#D8C3B8",
      callout="A young lawyer with big plans?", qual="ADVOCATES · ASSOCIATES · IN-HOUSE",
      head="Your Indian LLB can take you to <em>an international law career in Canada.</em>"),
 dict(stem="nca_t5_03_canadian_qualification", accent="#1E6A48", bg="#EAF0EA", line="#BCCDBF",
      callout="Want to practise law in Canada?", qual="LLB HOLDERS · ADVOCATES · ANY PRACTICE AREA",
      head="Qualify through the NCA from India, <em>then make the move.</em>"),
 dict(stem="nca_t5_04_corporate_lawyers", accent="#0E5A6C", bg="#E6EEF1", line="#B5CAD2",
      callout="Corporate lawyers and associates?", qual="CORPORATE · M&amp;A · CONTRACTS · IN-HOUSE",
      head="Add a Canadian qualification <em>to the contracts you already draft.</em>"),
 dict(stem="nca_t5_05_practise_abroad", accent="#5A2A6C", bg="#F0EAF2", line="#CDBCD4",
      callout="Ever thought of practising law abroad?", hs=74, qual="LAW STUDENTS · ADVOCATES · ASSOCIATES",
      head="Canada has a set route <em>for your Indian law degree.</em>"),
]
DELIVER = "In our 3-day live bootcamp, we show you the route to become a Canada-qualified lawyer:"
TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,sans-serif;background:%(bg)s;color:#16130E;display:flex;flex-direction:column;padding:44px 54px 46px}
.rail{text-align:center;font-size:24px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:%(accent)s;margin-bottom:18px}
.callout{background:%(accent)s;color:#fff;font-size:60px;font-weight:900;line-height:1.05;letter-spacing:-.02em;text-transform:uppercase;text-align:center;padding:18px 22px 22px;border-radius:10px}
.qual{text-align:center;font-size:25px;font-weight:800;letter-spacing:.1em;color:%(accent)s;margin-top:18px}
.paper{background:#FCFBF7;margin-top:26px;padding:30px 50px 38px;transform:rotate(-0.7deg);box-shadow:0 18px 40px rgba(0,0,0,.16)}
.tape{width:150px;height:15px;background:%(line)s;margin:0 auto 16px;border-radius:3px}
.nlabel{font-size:28px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:%(accent)s;margin-bottom:16px}
.head{font-size:%(hs)spx;font-weight:900;line-height:1.1;letter-spacing:-.024em}
.head em{font-style:italic;color:%(accent)s}
.grow{flex:1;min-height:18px}
.ticks{margin-top:22px;background:#fff;border:2px solid %(line)s;border-radius:12px;padding:14px 28px}
.tk{font-size:31px;font-weight:800;line-height:1.3;padding:4px 0}
.tk span{color:%(accent)s;margin-right:14px}
.deliver{font-size:33px;font-weight:700;line-height:1.36;text-align:center;padding:0 10px;color:#2A2620}
.bigbtn{background:%(accent)s;color:#fff;text-align:center;font-size:46px;font-weight:900;padding:22px 30px;border-radius:14px;margin-top:20px}
.foot{display:flex;justify-content:space-between;margin-top:20px;font-size:25px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3B352C}
</style></head><body>
<div class="rail">LawSikho · NCA Canada bootcamp</div>
<div class="callout">%(callout)s</div>
<div class="qual">%(qual)s</div>
<div class="paper"><div class="tape"></div><div class="nlabel">Notice</div><div class="head">%(head)s</div></div>
<div class="grow"></div>
<div class="deliver">%(deliver)s</div>
<div class="ticks"><div class="tk"><span>&#10003;</span>How the NCA assesses your LLB</div><div class="tk"><span>&#10003;</span>How to prepare for its exams from India</div><div class="tk"><span>&#10003;</span>The 12-month plan to qualify in Canada</div></div>
<div class="grow"></div>
<div class="bigbtn">Join the Rs 10 bootcamp</div>
<div class="foot"><div>3 days · Live only, no recordings</div><div>Rs 10 incl. GST · Refundable</div></div>
</body></html>"""
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
for a in ADS:
    h = os.path.join(OUT, "html", a["stem"] + ".html")
    open(h, "w").write(TPL % dict(a, deliver=DELIVER, hs=a.get("hs", 64)))
    png = os.path.join(OUT, "ads", a["stem"] + ".png")
    subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1080,1350",
                    "--screenshot=" + png, "file://" + h], check=True, capture_output=True)
    print(png)
