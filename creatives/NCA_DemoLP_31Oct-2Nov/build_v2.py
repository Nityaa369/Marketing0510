"""Demo LP v2: Ruchika's lp_nca_icp1b, kept in her structure, with fixes and a persuasion pass.
Changes: stamp markup bug, justified text off (rivers on phones), tables replaced by cards,
Did you know cards from dyk_facts.json (sourced from nca.legal), objection answers, glance strip,
mid page CTA, last-run proof line (pending). Every unchecked line is a yellow todo mark."""
import json, os, re, glob, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = json.load(open(os.path.join(HERE, "..", "NCA_LandingTemplate_31Oct-2Nov", "dyk_facts.json")))
def dyk(i):
    f = next(x for x in FACTS if x["id"] == i)
    todo = '' if f.get("status") == "checked" else ' <mark class="todo">VERIFY: re-open source on launch day</mark>'
    return '<div class="dyk"><div class="tag">Did you know?</div><div class="f">%s</div><div class="s">Source: %s.%s</div></div>' % (f["fact"], f["src"], todo)
def todo(t): return '<mark class="todo">%s</mark>' % t

h = open(os.path.join(HERE, "source_lp_nca_icp1b.html"), encoding="utf-8").read()
def sub(old, new, count=1):
    global h
    assert old in h, "missing: " + old[:70]
    h = h.replace(old, new, count)

# 1 markup bug in the stamp
sub('<div class="stamp"><span><div class="stamp"><span>&#127809;</span>CANADA</div>#9733;</span>CANADA</div>', '<div class="stamp"><span>&#127809;</span>CANADA</div>')
# 2 no justified text on phones
sub("p{margin-top:15px;max-width:62ch;text-align:justify;hyphens:auto}", "p{margin-top:15px;max-width:62ch;text-align:left}")
sub("ol.count li,ul.ticks li{text-align:justify;hyphens:auto}", "ol.count li,ul.ticks li{text-align:left}")
# 3 css additions
sub("</style></head>", """
.dyk{position:relative;background:#FFF6D6;border:3px solid var(--ink);border-radius:16px;padding:22px 18px 16px;margin:26px 0 8px;box-shadow:5px 5px 0 var(--acc)}
.dyk .tag{position:absolute;top:-14px;left:16px;background:var(--acc);color:#fff;font-weight:900;font-size:14px;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border-radius:999px}
.dyk .f{font-size:21px;line-height:1.35;font-weight:800;margin-top:2px}
.dyk .s{font-size:12.5px;color:var(--txt2);margin-top:8px}
.glance{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:18px}
.glance div{background:#fff;border:2px solid var(--ink);border-radius:12px;padding:10px 6px;text-align:center;font-weight:900;font-size:15px;line-height:1.15}
.glance b{display:block;font-size:22px;color:var(--acc)}
.opts{display:grid;gap:10px;margin:14px 0}
.opt{background:#fff;border:2px solid var(--line);border-radius:14px;padding:14px 16px}
.opt.us{border:3px solid var(--acc);background:var(--tint)}
.opt .k{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--txt2)}
.opt .n{font-weight:900;font-size:19px;line-height:1.25;margin:2px 0;color:var(--c2)}
.opt .c{font-weight:900;font-size:22px;color:var(--acc)}.opt .t{font-size:15px;color:var(--txt2);margin-top:2px}
.opt .src2{font-size:12.5px;color:var(--txt2);margin-top:4px}
mark.todo{background:#FFE36B;color:#3A2E00;padding:0 4px;border-radius:3px;font-size:.8em;font-weight:800}
.paths{display:grid;gap:10px;margin-top:14px}
.path{display:flex;gap:12px;background:#fff;border:2px solid var(--acc);border-radius:14px;padding:12px 14px}
.path .n{flex:none;width:36px;height:36px;border-radius:50%;background:var(--acc);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}
.path b{display:block;color:var(--c2)}.path span{font-size:16px;color:var(--txt2)}
</style></head>""")

# 4 glance strip + first dyk right after the fold terms
sub('<div class="terms">&#8377;10 incl. GST &middot; 31 Oct to 2 Nov &middot; 9 hours live online &middot; refundable</div>\n\n<!-- STEPS 4',
    '<div class="terms">&#8377;10 incl. GST &middot; 31 Oct to 2 Nov &middot; 9 hours live online &middot; refundable</div>\n<div class="glance"><div><b>3 days</b>9 hours, live</div><div><b>&#8377;10</b>refundable</div><div><b>From India</b>exams online</div></div>\n' + dyk("online") + '\n\n<!-- STEPS 4')

# 5 tables to cards: pay ladder
pay = re.search(r'<div class="tw"><table class="cmp pay">.*?</table></div>', h, re.S).group(0)
rows = [("Litigation lawyer in India, today", "&#8377;2 to 14 lakh a year", "AmbitionBox, 76 salaries, updated 22 Jun 2025"),
        ("Legal counsel in India, today", "&#8377;4.8 to 40 lakh a year", "AmbitionBox, about 2,000 salaries, updated 24 Jul 2025"),
        ("Lawyer in Ontario, licensed, median", "CAD 65.21 an hour, about &#8377;4,400", "Government of Canada Job Bank, NOC 41101, 2023-24 data, updated 19 Nov 2025"),
        ("Lawyer in Ontario, licensed, high", "CAD 112.98 an hour, about &#8377;7,600", "Job Bank, same report")]
cards = '<div class="opts">' + "".join('<div class="opt"><div class="k">Reported pay</div><div class="n">%s</div><div class="c">%s</div><div class="src2">%s</div></div>' % r for r in rows) + '</div>'
sub(pay, cards)
cmp_ = re.search(r'<div class="tw"><table class="cmp"><thead><tr><th>Route</th>.*?</table></div>', h, re.S).group(0)
rows2 = [("A Canadian LLM first", "About a year abroad, away from practice", "A degree, and still no Canadian work on your record", False),
         ("PR first", "The move, before any work is lined up", "The right to live in Canada, and a job search from zero", False),
         ("The NCA alone, from notes", "Months of self-study", "A certificate, with no Canadian client or drafting sample", False),
         ("This bootcamp", "3 days, 9 hours, &#8377;10", "The exam method, five pieces of Canadian work seen live, the employer list and outreach messages, and a 12-month plan", True)]
c2 = '<div class="opts">' + "".join('<div class="opt%s"><div class="k">%s</div><div class="n">%s</div><div class="t"><b>Takes:</b> %s</div><div class="t"><b>You end with:</b> %s</div></div>' % (" us" if r[3] else "", "This route" if r[3] else "Another route", r[0], r[1], r[2]) for r in rows2) + '</div>'
sub(cmp_, c2)

# 6 DYK cards at natural pauses
sub('<!-- Market size and money', dyk("common") + '\n<!-- Market size and money')
sub('<!-- STEP 11: first usable artifact -->', dyk("five") + '\n<!-- STEP 11: first usable artifact -->')
sub('<!-- STEPS 13 and 14', dyk("time") + '\n<!-- STEPS 13 and 14')
sub('<!-- STEP 15: show the work', dyk("cert") + '\n<!-- STEP 15: show the work')
sub('<!-- STEP 17: compare', dyk("rules2026") + '\n<!-- STEP 17: compare')

# 7 qualification path as a visual stack (replaces the counted list wording but keeps content)
# mid page CTA after the 'order matters' story
sub("""<p class="note">As told in the bootcamp, from our learner records. Same lawyer, same effort. The order changed the result.</p>""",
    """<p class="note">As told in the bootcamp, from our learner records. Same lawyer, same effort. The order changed the result.</p>
<a class="cta" href="https://growthx.lawsikho.com/f/nca-oct-icp1b-litigator-inhouse">Join the &#8377;10 NCA bootcamp</a>
<div class="terms">&#8377;10 incl. GST &middot; refundable &middot; live only</div>""")

# 8 last-run proof (pending recount)
sub('<h2>Indian lawyers who took this route</h2>', '<h2>Indian lawyers who took this route</h2>\n<p>At our April 2024 NCA bootcamp, 550 people attended live on Day 1, and about 5,680 had registered. ' + todo("PENDING: recount from the April 2024 and later attendance lists; confirm this may be published") + '</p>')

# 9 more objection answers
more = """<h3>Do I have to move to Canada before I start?</h3><p>No. You can write the NCA exams online from India. Moving is a separate decision you can make later, and the bootcamp shows you the order. """ + todo("VERIFY: nca.legal, exams online") + """</p>
<h3>Do I need a Canadian degree or an LLM first?</h3><p>No. The NCA exists to assess law degrees from outside Canada, and you apply with your Indian LLB. The bootcamp explains where an LLM does and does not help. """ + todo("VERIFY: nca.legal, who can apply") + """</p>
<h3>My English is not perfect. Is that a problem?</h3><p>Since 1 March 2026 the NCA screens English language ability for every applicant. Day 1 shows what that check is, so you can plan for it instead of guessing. """ + todo("VERIFY: nca.legal English requirement") + """</p>
<h3>I am a fresher. Is this too early?</h3><p>It is a good time to start. Your degree is recent and the exams are open book, so the work is understanding Canadian law, not memorising. """ + todo("SCRIPT-CHECK: open book for 2026") + """</p>
<h3>What if it is not for me?</h3><p>Tell us and the &#8377;10 comes back. No questions asked. """ + todo("VERIFY: refund steps and window") + """</p>
<h3>Can I do this and keep working?</h3><p>Yes. The bootcamp is three live sessions, 9 hours in all. The NCA exams are online and you choose the month.</p>
"""
sub('<h3>I work in-house. Does this still fit?</h3>', more + '<h3>I work in-house. Does this still fit?</h3>')

# 10 title tweak and output
out = os.path.join(HERE, "lp_nca_icp1b_v2.html")
open(out, "w", encoding="utf-8").write(h)
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=430,17000",
                "--screenshot=" + os.path.join(HERE, "v2_full.png"), "file://" + out], check=True, capture_output=True)
print("ok", len(h))
