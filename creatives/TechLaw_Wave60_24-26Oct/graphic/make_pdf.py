# Builds C1_Graphic_Ads.pdf from final_c1/*.jpg and copy_c1.py. Run: python3 make_pdf.py
import os, html, glob, subprocess
from copy_c1 import ADS
HERE = os.path.dirname(os.path.abspath(__file__))
e = html.escape
F = "".join("@font-face{font-family:'%s';font-weight:%d;src:url('fonts/%s-latin-%d-normal.woff2')}" % (n, w, s, w)
            for n, s in (("Poppins", "poppins"), ("Inter", "inter")) for w in (500, 600, 700, 800))

def copy_rows(c, first):
    rows = []
    if first: rows.append(("Call-out band", c["label"]))
    elif c.get("label"): rows.append(("Kicker", c["label"]))
    rows.append(("Hook", c["head"]))
    for k in ("sub", "sub2"):
        if c.get(k): rows.append(("Reason", c[k]))
    if c.get("define"): rows.append(("Definition", "Tech law is the legal work tech companies need: contracts, privacy, compliance and disputes."))
    return "".join('<tr><th>%s</th><td>%s</td></tr>' % (e(a), e(b)) for a, b in rows)

pages = []
pages.append('''<section class="cover"><div class="kick">LawSikho · Tech Law Bootcamp · 24 to 26 Oct 2026</div>
<h1>C1 Proven readers: graphic ads</h1>
<p class="lead">10 ads for cold LLB holders and lawyers back after a break: 7 single images (4:5) and 3 carousels (1:1, four cards each).
Draft for Ramanuj. No Ramanuj verdict yet.</p><img class="board" src="BOARD_C1.jpg"></section>''')
pages.append('''<section><h2>How every ad is built</h2>
<ul>
<li><b>Top 10%:</b> a solid band that names the reader in full plain words ("For LLB holders working in HR").</li>
<li><b>Middle:</b> one picture that acts out the hook, one hook sentence that names the move into tech law, one reason.</li>
<li><b>Bottom 15%:</b> a big "Join for Rs 10" button with the price line: Rs 10 incl. GST, 3 live evenings, refundable.</li>
<li><b>Different on purpose:</b> each ad has its own picture, colour, typeface and layout. Only a carousel keeps one person across its cards.</li>
<li><b>Pictures:</b> Indian faces, light studio backdrops, one surreal idea each, in the style of the 7 reference posters you sent.</li>
<li><b>Rules held:</b> lawyers and LLB holders only; no income figure or viewer number on the face; no guarantee; no AI fear; no dashes.</li>
</ul>
<h2>Critic's read</h2>
<p><b>Verdict: likely APPROVE on the face, fix first on two points.</b></p>
<ol>
<li>The price line inside the button is small (it reads at about 21 px on a 1080 px ad). Ramanuj rejects anything small. Cut it to "Rs 10 · Refundable" at a larger size.</li>
<li>The one-line definition of tech law is on the carousels only. NCA ads did better with it on every face; add it to the singles or keep it in the primary text.</li>
</ol>
<p><b>Half-asleep test (ad 02):</b> who? LLB holders working in HR. What job? Tech law. Why yes? Rs 10, refundable, three live evenings.</p>
<h2>Calls only Ramanuj can make</h2>
<ul><li>Whether "LLB holders" outside law (01 to 05) count as lawyers for Tech Law (his 24 Sep rule: lawyers only).</li>
<li>Budget, and whether C1 runs as its own campaign or inside one ABO with C2 to C4.</li></ul></section>''')
for a in ADS:
    if a["kind"] == "single":
        c = a["cards"][0]
        pages.append('<section class="single"><img class="ad" src="final_c1/tlg_%s_single.jpg"><div class="meta"><div class="kick">Ad %s · Single image 4:5</div>'
                     '<h2>%s</h2><table>%s<tr><th>Picture</th><td>%s</td></tr><tr><th>Typeface</th><td>%s</td></tr></table></div></section>'
                     % (a["id"], a["id"], e(a["reader"]), copy_rows(c, True), e(a["idea"]), e(a["style"]["font"])))
    else:
        cards = "".join('<div class="cc"><img src="final_c1/tlg_%s_card%d.jpg"><table>%s</table></div>' % (a["id"], i + 1, copy_rows(c, i == 0))
                        for i, c in enumerate(a["cards"]))
        pages.append('<section class="car"><div class="kick">Ad %s · Carousel, 4 cards 1:1 · Picture: %s</div><h2>%s</h2><div class="grid">%s</div></section>'
                     % (a["id"], e(a["idea"]), e(a["reader"]), cards))
pages.append('''<section><h2>Production notes</h2><ul>
<li>Images: Higgsfield GPT Image 2.5, high quality, 2K. 19 images, about 52 credits. Job ids are in jobs_c1.json.</li>
<li>Text is laid over the pictures by compose.py, so copy can be changed without new images or credits.</li>
<li>Full-size files sit in the Higgsfield sandbox. The images in this PDF are 900 px previews. Allow the host d8j0ntlcm91z4.cloudfront.net in the environment's network settings to pull full-size files into the repo.</li>
<li>Next: C2 to C6, one board per campaign for approval first.</li></ul></section>''')
css = F + '''@page{size:1600px 1000px;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Inter;color:#1b1b1b;background:#F4F1EA}
section{width:1600px;height:1000px;padding:56px 70px;page-break-after:always;overflow:hidden;position:relative}
h1{font-family:Poppins;font-weight:800;font-size:60px;margin:6px 0 10px}h2{font-family:Poppins;font-weight:800;font-size:34px;margin:18px 0 10px}
.kick{font-weight:800;font-size:18px;letter-spacing:.06em;text-transform:uppercase;color:#C2412D}.lead{font-size:22px;line-height:1.45;max-width:1300px;margin:0 0 16px}
.board{width:1080px;display:block;border-radius:10px;box-shadow:0 6px 20px rgba(0,0,0,.15)}
.cover{display:flex;flex-direction:column}.cover .board{height:640px;width:auto;object-fit:contain;align-self:flex-start}
ul,ol{font-size:21px;line-height:1.5;padding-left:26px;margin:6px 0}li{margin:4px 0}p{font-size:21px;line-height:1.5;margin:8px 0}
.single{display:flex;gap:56px;align-items:center}.single .ad{height:888px;border-radius:12px;box-shadow:0 8px 26px rgba(0,0,0,.18)}
.meta{flex:1}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #DDD6C8;font-size:20px;line-height:1.4}
th{width:170px;font-weight:800;color:#444}.car h2{margin:6px 0 16px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px}
.cc img{width:100%;border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,.15)}.cc th,.cc td{font-size:15px;padding:6px 6px}.cc th{width:92px}'''
open(os.path.join(HERE, "pdf_c1.html"), "w").write('<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (css, "".join(pages)))
hs = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
subprocess.run([hs, "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                "--print-to-pdf=" + os.path.join(HERE, "C1_Graphic_Ads.pdf"), "file://" + os.path.join(HERE, "pdf_c1.html")], check=True, capture_output=True)
print("pdf ok")
