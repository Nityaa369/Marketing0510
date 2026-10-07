"""Converting landing page template: 21-step spine (Ruchika's order).
Slots are filled from a config dict per ICP. Every unverified line is marked [[TAG: text]]:
  PENDING      blocks --publish (real learner story, consent, pay link)
  SCRIPT-CHECK needs the 2026 camp script
  VERIFY       needs a fact check before launch
Rules baked in: ICP named first, big; plain English; no income figures; no guarantees; no fear;
Rs 10 incl GST, refundable, live only; bar licensing always shown; the ONLY disclaimer is the last block;
nothing hedges above a pay button; no em or en dashes.
"""
import re, html

CSS = """
:root{--ac:%(ac)s;--ac2:%(ac2)s;--bg:%(bg)s;--ink:#16130E;--mut:#4A4338;--card:#fff;--line:rgba(0,0,0,.12)}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:Inter,system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--ink);font-size:19px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
section{padding:44px 0;border-top:1px solid var(--line)}
section.first{border-top:0;padding-top:22px}
.rail{text-align:center;font-size:13px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:var(--ac);margin-bottom:10px}
.callout{background:var(--ac);color:#fff;font-weight:900;text-transform:uppercase;text-align:center;border-radius:10px;padding:14px 16px 16px;font-size:clamp(34px,9vw,56px);line-height:1.05;letter-spacing:-.02em}
h1{font-size:clamp(32px,8.4vw,50px);line-height:1.08;letter-spacing:-.02em;font-weight:900;text-align:center;margin:22px 0 8px}
h2{font-size:clamp(27px,6.6vw,38px);line-height:1.12;letter-spacing:-.015em;font-weight:900;margin-bottom:14px}
h3{font-size:21px;line-height:1.2;font-weight:800;margin-bottom:6px}
p{margin:0 0 14px}
.gloss{text-align:center;font-weight:700;color:var(--mut);font-size:17px;margin-bottom:12px}
.lead{font-size:21px}
.eyebrow{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--ac);margin-bottom:8px}
.src{font-size:13px;color:var(--mut);margin-top:6px}
/* buttons */
.btn{display:block;background:var(--ac);color:#fff;text-align:center;font-weight:900;font-size:clamp(22px,6vw,30px);padding:18px 20px;border-radius:14px;text-decoration:none;box-shadow:0 6px 0 rgba(0,0,0,.18);margin:18px 0 8px}
.btn small{display:block;font-size:14px;font-weight:700;opacity:.92;letter-spacing:.03em;margin-top:2px}
.btn:active{transform:translateY(3px);box-shadow:0 3px 0 rgba(0,0,0,.18)}
.btn.ghost{background:#fff;color:var(--ac);border:3px solid var(--ac);box-shadow:none}
.microfoot{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;font-size:12px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}
/* chips + band */
.chips{display:flex;align-items:stretch;gap:6px;margin:10px 0 14px}
.chips .s{flex:1;background:#fff;color:var(--ac);border:2.5px solid var(--ac);border-radius:8px;text-align:center;font-size:14px;font-weight:900;padding:8px 4px;display:flex;align-items:center;justify-content:center;line-height:1.1}
.chips .a{align-self:center;font-weight:900;color:var(--ac)}
.band{display:flex;border:3px solid var(--ac);border-radius:12px;overflow:hidden;font-weight:900;text-align:center;margin-top:14px}
.band div{display:flex;align-items:center;justify-content:center;padding:10px 6px;font-size:15px;line-height:1.1;background:#fff;color:var(--ac)}
.band .hw{flex:.9;background:var(--ac);color:#fff}.band .m{flex:1.6}.band .p{flex:.6;font-size:20px;border-left:3px solid var(--ac)}
/* cards / lists */
.cards{display:grid;gap:12px;margin:14px 0}
.card{background:var(--card);border:2px solid var(--line);border-radius:14px;padding:16px 18px}
.card.fail{border-left:8px solid #B8B1A4}
.card .tag{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.steps{counter-reset:s;display:grid;gap:12px;margin:14px 0}
.step{display:flex;gap:14px;background:var(--card);border:2px solid var(--ac);border-radius:14px;padding:16px}
.step .n{flex:none;width:44px;height:44px;border-radius:50%%;background:var(--ac);color:#fff;font-weight:900;font-size:24px;display:flex;align-items:center;justify-content:center}
.tick{list-style:none;margin:10px 0 16px}.tick li{padding-left:34px;position:relative;margin-bottom:10px}
.tick li:before{content:"\\2713";position:absolute;left:0;top:0;width:24px;height:24px;border-radius:50%%;background:var(--ac);color:#fff;font-weight:900;font-size:15px;display:flex;align-items:center;justify-content:center}
table{width:100%%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;font-size:16px;margin:12px 0}
th,td{padding:12px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--ac);color:#fff;font-size:13px;letter-spacing:.08em;text-transform:uppercase}
tr.us td{background:var(--ac2);font-weight:800}
.quote{font-size:23px;font-weight:800;line-height:1.3;background:#fff;border:3px solid var(--ac);border-radius:14px;padding:18px 20px;margin:14px 0}
.stat{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:14px 0}
.stat div{background:#fff;border:2px solid var(--line);border-radius:14px;padding:14px}
.stat b{display:block;font-size:30px;line-height:1.05;color:var(--ac);font-weight:900}
ol.count{list-style:none;counter-reset:n;margin:14px 0;display:flex;flex-direction:column;gap:10px;padding:0}
ol.count li{counter-increment:n;background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 16px 14px 62px;position:relative;font-size:18px}
ol.count li::before{content:counter(n);position:absolute;left:14px;top:12px;width:34px;height:34px;border-radius:50%%;background:var(--ac);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:17px}
ol.count b{display:block;color:var(--ac);font-size:19px;margin-bottom:2px}
ol.count small{display:block;color:var(--mut);font-size:13px;margin-top:5px}
.story{background:#fff;border-left:6px solid var(--ac);border-radius:0 14px 14px 0;padding:16px 18px;margin:12px 0}
.story .who{font-weight:900;font-size:20px}.story .tag{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ac);margin:2px 0 8px}
.story p{margin:0 0 8px;font-size:17px}
/* did you know */
.dyk{position:relative;background:#FFF6D6;border:3px solid #16130E;border-radius:16px;padding:20px 18px 16px;margin:20px 0 6px;box-shadow:5px 5px 0 var(--ac)}
.dyk .tag{position:absolute;top:-14px;left:16px;background:var(--ac);color:#fff;font-weight:900;font-size:14px;letter-spacing:.1em;text-transform:uppercase;padding:5px 12px;border-radius:999px}
.dyk .f{font-size:21px;line-height:1.35;font-weight:800;margin-top:4px}
.dyk .s{font-size:12.5px;color:#4A4338;margin-top:8px}
/* day cards + option cards (no tables) */
.days{display:grid;gap:10px;margin:14px 0}
.dc{display:flex;align-items:center;gap:14px;background:#fff;border:2px solid var(--ac);border-radius:14px;padding:12px 14px}
.dc .d{flex:none;background:var(--ac);color:#fff;border-radius:10px;padding:8px 10px;text-align:center;font-weight:900;line-height:1.05;min-width:64px}
.dc .d b{display:block;font-size:26px}.dc .d span{font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.dc .w{font-weight:900;font-size:19px;line-height:1.2}.dc .w small{display:block;font-weight:700;color:var(--mut);font-size:15px;margin-top:2px}
.opts{display:grid;gap:10px;margin:14px 0}
.opt{background:#fff;border:2px solid var(--line);border-radius:14px;padding:14px 16px}
.opt.us{border:3px solid var(--ac);background:var(--ac2)}
.opt .k{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.opt .n{font-weight:900;font-size:19px;line-height:1.2;margin:2px 0}
.opt .c{font-weight:900;font-size:24px;color:var(--ac)}.opt .t{font-size:15px;color:var(--mut);margin-top:2px}
/* planner artifact */
.paper{background:#fff;border:3px solid #2A2A20;border-radius:6px;padding:18px;font-family:'Bitstream Charter',Caladea,Georgia,serif}
.paper .t{font-family:Inter,sans-serif;font-weight:900;letter-spacing:.08em;text-transform:uppercase;font-size:14px;border-bottom:2px solid #2A2A20;padding-bottom:8px;margin-bottom:10px}
.paper .r{display:flex;justify-content:space-between;gap:10px;align-items:baseline;padding:8px 0;border-bottom:1px dashed rgba(0,0,0,.25);font-size:17px}
.paper .r span{flex:none;min-width:104px;white-space:nowrap}.paper .r b{text-align:right}
/* fold faces */
.face{margin:16px 0 6px}
.phone{border-radius:18px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.16)}
.phone .top{background:#075E54;color:#fff;display:flex;align-items:center;gap:12px;padding:10px 16px}
.phone .av{width:38px;height:38px;border-radius:50%%;background:#C9D8D3;color:#075E54;font-weight:900;display:flex;align-items:center;justify-content:center}
.phone .nm{font-weight:800;font-size:17px;line-height:1.1}.phone .st{font-size:12px;opacity:.85}
.wall{background:#ECE5DD;padding:14px;display:flex;flex-direction:column;gap:9px}
.b{max-width:84%%;font-size:17px;line-height:1.28;padding:8px 12px 5px;border-radius:12px;box-shadow:0 1px 1px rgba(0,0,0,.12)}
.b.me{align-self:flex-end;background:#DCF8C6}.b.fr{align-self:flex-start;background:#fff}
.b i{display:block;text-align:right;font-style:normal;font-size:11px;color:#6B7B74}
.cal{background:#fff;border:3px solid var(--ac);border-radius:14px;padding:12px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.cal div{border:2px solid #D9D1E4;border-radius:10px;text-align:center;font-weight:800;padding:14px 0;font-size:18px;color:#4A3B5C}
.cal div.on{background:var(--ac);color:#fff;border-color:var(--ac);box-shadow:0 0 0 3px #fff,0 0 0 6px var(--ac);font-size:13px;line-height:1.1;padding:7px 2px}
.vcard{background:#fff;border-radius:16px;border-left:16px solid var(--ac);padding:26px 24px;box-shadow:0 12px 28px rgba(120,60,20,.22);transform:rotate(-1.6deg);margin:6px 4px}
.vcard .n{font-size:38px;font-weight:900;letter-spacing:-.02em}.vcard .d{font-size:18px;font-weight:700;color:var(--mut);margin-top:2px}
.vcard .q{font-size:28px;font-weight:900;color:var(--ac);line-height:1.1;margin-top:14px}.vcard .ip{font-size:15px;font-weight:700;color:var(--mut);margin-top:6px}
.lbl{text-align:center;font-size:12px;font-weight:700;color:var(--mut);margin-top:6px}
/* share + sticky */
.share{display:block;text-align:center;border:3px dashed var(--ac);color:var(--ac);font-weight:900;border-radius:14px;padding:14px;text-decoration:none;font-size:18px;margin-top:10px}
.sticky{position:fixed;left:0;right:0;bottom:0;background:var(--bg);border-top:2px solid var(--line);padding:10px 14px;z-index:9}
.sticky a{display:block;background:var(--ac);color:#fff;text-align:center;font-weight:900;font-size:20px;padding:14px;border-radius:12px;text-decoration:none}
body{padding-bottom:78px}
.end{font-size:13px;color:var(--mut);line-height:1.5;border-top:1px solid var(--line);padding:26px 0 40px}
mark.gap{background:#FFE36B;color:#3A2E00;padding:0 3px;border-radius:3px;font-size:.82em;font-weight:700}
@media(min-width:760px){.cards.three{grid-template-columns:repeat(3,1fr)}.sticky{display:none}body{padding-bottom:0}}
"""

PAY = "#PAYMENT_LINK_PENDING"
CTA = '<a class="btn" href="%s">Join the Rs 10 bootcamp<small>3 live days · Rs 10 incl. GST · Refundable</small></a>' % PAY
CHIPS = '<div class="chips"><div class="s">NCA exams, from India</div><div class="a">&#8594;</div><div class="s">Bar licensing</div><div class="a">&#8594;</div><div class="s">Practise in Canada</div></div>'
BAND = '<div class="band"><div class="hw">We show you how</div><div class="m">NCA exams + bar licensing, in 3 live days</div><div class="p">Rs 10</div></div>'
MICRO = '<div class="microfoot"><span>3 days · Live only</span><span>Rs 10 incl. GST · Refundable</span></div>'
GLOSS = '<div class="gloss">NCA: Canada\'s check on your Indian law degree.</div>'

def li(items): return '<ul class="tick">%s</ul>' % "".join("<li>%s</li>" % i for i in items)
def cards(items, cls="", tag=None):
    return '<div class="cards %s">%s</div>' % (cls, "".join('<div class="card %s">%s<h3>%s</h3><p>%s</p></div>' % ("fail" if tag else "", ('<div class="tag">%s</div>' % tag) if tag else "", t, b) for t, b in items))

import json, os
_DYK = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dyk_facts.json")))
def dyk(*ids):
    out = ""
    for i in ids:
        f = next(x for x in _DYK if x["id"] == i)
        flag = " [[VERIFY: re-open the source on launch day]]" if f.get("status") != "checked" else ""
        out += '<div class="dyk"><div class="tag">Did you know?</div><div class="f">%s</div><div class="s">Source: %s.%s</div></div>' % (f["fact"], f["src"], flag)
    return out
def counted(items):
    return '<ol class="count">%s</ol>' % "".join("<li><b>%s</b>%s<small>%s</small></li>" % i for i in items)
def stories(items):
    return "".join('<div class="story"><div class="who">%s</div><div class="tag">%s</div>%s</div>' % (n, t, "".join("<p>%s</p>" % p for p in ps)) for n, t, ps in items)

WHY = [
 ("Canada is a top 10 economy.", " The IMF ranks it 10th largest in the world, at about USD 2.28 trillion in 2025. It is a G7 member.", "Source: IMF World Economic Outlook, October 2025."),
 ("Its legal market is worth about CAD 21 to 22 billion a year.", " Canada has 141,540 practising lawyers, and law firms there say hiring and training people is their top economic challenge.", "Sources: IBISWorld, Law Firms in Canada; Federation of Law Societies of Canada, Statistics Report 2024; Canadian Lawyer. [[VERIFY: re-open all three sources on launch day]]"),
 ("India and Canada are building a trade deal.", " The two governments signed the terms for a trade agreement on 2 March 2026, set a target of USD 50 billion in trade by 2030, and aim to finish the talks by the end of 2026. These are aims, not results.", "Sources: Business Today, 2 Mar 2026; India Briefing. [[VERIFY: latest round of talks]]"),
 ("Indian companies already work there.", " About 50 Indian companies have invested around CAD 11 billion in Canada and employ over 33,000 people.", "Source: CII and Canada India Business Council report, June 2026, via ETV Bharat. [[VERIFY: re-check on launch day]]"),
 ("The NCA rules changed on 1 March 2026.", " Every applicant now gets English screening and an Indigenous law course. Learn the current rules before you pay for an exam.", "Source: nca.legal. [[VERIFY: current NCA requirements]]"),
]
HOW_FROM_INDIA = [
 ("Both systems are common law.", " Canada outside Quebec runs on common law, like India. The subjects will feel familiar, though you still have to learn Canadian law.", "Source: Justice Canada."),
 ("The exams are online, with a session every month.", " You write from home, in India, with a proctor watching. Each core subject comes round every third month, so you pick your sitting.", "Source: nca.legal, exam information, and the NCA 2026 and 2027 exam schedules."),
 ("The NCA decides your exams after it assesses your degree.", " Core subjects usually include Canadian constitutional law, administrative law, criminal law, professional responsibility and foundations of Canadian law. Your own list comes from the NCA.", "[[SCRIPT-CHECK: subjects and open book format from the April 2024 script; confirm for 2026]]"),
 ("The exams are open book, and 50 percent passes.", " You can bring paper books, not electronic copies. You are marked on applying concepts to a fact pattern, not on memory.", "Source: nca.legal, exam information and online exam rules."),
]

def face(kind, c):
    if kind == "chat":
        return '<div class="face"><div class="phone"><div class="top"><div class="av">A</div><div><div class="nm">Adv. Mehta</div><div class="st">online</div></div></div><div class="wall">' + "".join('<div class="b %s">%s<i>%s</i></div>' % (w, t, tm) for w, t, tm in c["chat"]) + '</div></div><div class="lbl">Dramatised chat. Not a real learner.</div></div>'
    if kind == "calendar":
        mo = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
        return '<div class="face"><div class="cal">' + "".join('<div class="on">Your exam month<br>Mar</div>' if m == "Mar" else "<div>%s</div>" % m for m in mo) + '</div><div class="lbl">Sample calendar</div></div>'
    return '<div class="face"><div class="vcard"><div class="n">Your Name</div><div class="d">LLB (India)</div><div class="q">Canada-qualified lawyer</div><div class="ip">In progress. One exam at a time, from India.</div></div><div class="lbl">Sample card</div></div>'

def build(c):
    s = []
    A = s.append
    # FOLD (steps 1 to 3 repeat the ad in its words)
    A('<section class="first"><div class="wrap"><div class="rail">LawSikho · Canada law bootcamp</div><div class="callout">%s</div>%s<h1>%s</h1>%s%s%s%s%s%s</div></section>' % (c["callout"], face(c["face"], c), c["head"], GLOSS, CHIPS, BAND, CTA, MICRO, ""))
    # 2 symptom
    A('<section data-step="2"><div class="wrap"><div class="eyebrow">%s</div><h2>%s</h2>%s</div></section>' % (c["sym_eyebrow"], c["sym_h"], "".join("<p>%s</p>" % p for p in c["sym_p"])))
    # 3 outcome
    A('<section data-step="3"><div class="wrap"><div class="eyebrow">What you want</div><h2>%s</h2>%s</div></section>' % (c["out_h"], li(c["out_li"])))
    # 4-6 failed alternatives
    A('<section data-step="4-6"><div class="wrap"><div class="eyebrow">What you have probably tried</div><h2>%s</h2>%s</div></section>' % (c["fail_h"], cards(c["fail"], "three", tag="Tried, did not move you")))
    # 7 reframe
    A('<section data-step="7"><div class="wrap"><div class="eyebrow">The real issue</div><h2>%s</h2>%s</div></section>' % (c["reframe_h"], "".join("<p>%s</p>" % p for p in c["reframe_p"])))
    # 8 cost of staying unclear + the big why
    A('<section data-step="8"><div class="wrap"><div class="eyebrow">Why now</div><h2>Why Canada, and why this year</h2>%s<h3 style="margin-top:22px">%s</h3>%s<p class="src">%s</p></div></section>' % (counted(WHY), c["cost_h"], "".join("<p>%s</p>" % p for p in c["cost_p"]), c["cost_src"]))
    # 9 offer + CTA
    A('<section data-step="9"><div class="wrap"><div class="eyebrow">The bootcamp</div><h2>3 live days. Rs 10. We show you how.</h2><p class="lead">A live Canada law bootcamp from LawSikho. You see the full route from your Indian law degree to practising in Canada: the NCA exams, then bar licensing, then practice.</p>%s<div class="days"><div class="dc"><div class="d"><span>Sat</span><b>31</b><span>Oct</span></div><div class="w">Day 1<small>2 to 5 PM IST, live</small></div></div><div class="dc"><div class="d"><span>Sun</span><b>1</b><span>Nov</span></div><div class="w">Day 2<small>2 to 5 PM IST, live</small></div></div><div class="dc"><div class="d"><span>Mon</span><b>2</b><span>Nov</span></div><div class="w">Day 3<small>7 to 10 PM IST, live</small></div></div></div>%s%s</div></section>' % (CHIPS, CTA, MICRO))
    # 10 mechanism
    A('<section data-step="10"><div class="wrap"><div class="eyebrow">How it works</div><h2>The route, in 3 steps</h2><div class="steps">%s</div><h3 style="margin-top:22px">Why you can start from India</h3>%s</div></section>' % ("".join('<div class="step"><div class="n">%d</div><div><h3>%s</h3><p>%s</p></div></div>' % (i + 1, t, b) for i, (t, b) in enumerate(c["mech"])), counted(HOW_FROM_INDIA)))
    # 11 first artifact
    A('<section data-step="11"><div class="wrap"><div class="eyebrow">What you can do by the end of Day 1</div><h2>%s</h2>%s<div class="paper"><div class="t">%s</div>%s</div><p class="src">Sample layout. Your own plan is built in the bootcamp. [[SCRIPT-CHECK: confirm the sample answer, the clause review and the 12 month plan are in the 2026 camp]]</p></div></section>' % (c["art_h"], li(["Write a first answer in the format NCA examiners expect, step by step (issue, rule, application, conclusion).", "Review a non-compete clause under Canadian law.", "See the core subjects, and which one to start with."]), c["art_t"], "".join('<div class="r"><span>%s</span><b>%s</b></div>' % r for r in c["art_rows"])))
    # 12 longer-term
    A('<section data-step="12"><div class="wrap"><div class="eyebrow">Where this goes</div><h2>%s</h2>%s</div></section>' % (c["long_h"], li(c["long_li"])))
    # 13 proof 1: real learners from the script
    A('<section data-step="13"><div class="wrap"><div class="eyebrow">Proof 1: real people on this route</div><h2>%s</h2>%s<p class="src">Named from LawSikho learner records, April 2024 bootcamp. These people cleared NCA exams and moved or found work. None of them is described here as a licensed Canadian lawyer. [[PENDING: confirm each story with the learner, written consent, current job and employer. The script gives two different dates for when Navkaran Singh cleared.]]</p>%s</div></section>' % (c["p2_h"], stories(c["stories"]), CTA))
    # 14 proof 2: the wider group and the public numbers
    A('<section data-step="14"><div class="wrap"><div class="eyebrow">Proof 2: you would not be first</div><h2>They are not the only ones</h2><div class="stat"><div><b>59</b>learners had cleared at least one NCA subject, and 11 had cleared all of them, at the time of the April 2024 bootcamp.<span class="src" style="display:block">[[PENDING: recount from the learner list before launch]]</span></div><div><b>1,858,755</b>Canadians of Indian origin in the 2021 census, 5.1% of the country.<span class="src" style="display:block">Source: Statistics Canada. [[VERIFY: re-check on launch day]]</span></div></div><p>Fastest NCA path: about 10 months. The average candidate takes about two years. Source: nca.legal.</p></div></section>')
    # 15 the work (from the April 2024 script)
    A('<section data-step="15"><div class="wrap"><div class="eyebrow">What we actually do</div><h2>The work, not a pep talk</h2><div class="day-list">%s</div><p class="src">[[SCRIPT-CHECK: replace with the 2026 script, day by day]]</p></div></section>' % li(c["work"]))
    # 16 implementation
    A('<section data-step="16"><div class="wrap"><div class="eyebrow">The details</div><h2>Where, when, what you need</h2>%s</div></section>' % li(c["impl"]))
    # 17 cost compare
    A('<section data-step="17"><div class="wrap"><div class="eyebrow">What it costs to find out</div><h2>Rs 10 to see the whole route</h2><div class="opts"><div class="opt us"><div class="k">This bootcamp</div><div class="n">LawSikho Canada bootcamp, 3 live days</div><div class="c">Rs 10</div><div class="t">Including GST. Refundable.</div></div><div class="opt"><div class="k">Another route</div><div class="n">One NCA exam prep course from a commercial provider</div><div class="c">CAD 499</div><div class="t">Per course. OsgoodePD price page, 6 Oct 2026.</div></div><div class="opt"><div class="k">Another cost</div><div class="n">NCA assessment, then each NCA exam</div><div class="c">CAD 400 + CAD 500 each</div><div class="t">Plus Canadian taxes. Source: nca.legal, costs and timelines.</div></div></div><p class="src">Prices of other providers are theirs and change. We list them so you can see what a first step usually costs.</p></div></section>')
    # 18 risk removal
    A('<section data-step="18"><div class="wrap"><div class="eyebrow">Your risk</div><h2>Rs 10. Refundable. Live only.</h2>%s%s</div></section>' % (li(["You pay Rs 10 including GST.", "It is refundable. [[VERIFY: refund steps and window, in one plain line]]", "It is live only, so you can ask your question on the day.", "You decide on the exams after you have seen the whole route."]), CTA))
    # 19 buyer language
    A('<section data-step="19"><div class="wrap"><div class="eyebrow">Say it to your people</div><h2>%s</h2><div class="quote">%s</div><a class="share" href="https://wa.me/?text=%s">Send this to someone who needs it</a></div></section>' % (c["lang_h"], c["lang_q"], html.escape(c["lang_q"]).replace(" ", "%20")))
    # 20 next step
    A('<section data-step="20"><div class="wrap"><div class="eyebrow">Next step</div><h2>%s</h2><p class="lead">Pay Rs 10. You get the live links for all 3 days.</p>%s%s</div></section>' % (c["next_h"], CTA, MICRO))
    # 21 stop selling + only disclaimer
    A('<section data-step="21" style="border-top:0"><div class="wrap"><p style="text-align:center;font-weight:800;font-size:20px">That is everything. See you on Saturday.</p><div class="end">LawSikho is not part of, or approved by, the National Committee on Accreditation, any Canadian law society or any government. Whether you can qualify depends on your own eligibility, your exam results and each province\'s rules, which change. We do not promise admission, a licence, a job or an income. Facts on this page were checked on 7 Oct 2026 from the sources named beside them.</div></div></section>')
    ids = c.get("dyk", ["online", "time", "rules2026", "cert"])
    def inject(step, extra):
        for k, sec in enumerate(s):
            if 'data-step="%s"' % step in sec[:40]:
                s[k] = sec.rsplit("</div></section>", 1)[0] + extra + "</div></section>"
                return
    inject("2", dyk(ids[0]))
    inject("10", dyk(ids[1]))
    inject("16", dyk(ids[2]))
    inject("18", dyk(ids[3]))
    body = "\n".join(s) + '\n<div class="sticky"><a href="%s">Join the Rs 10 bootcamp</a></div>' % PAY
    return "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>%s</title><style>%s</style></head><body>%s</body></html>" % (html.escape(c["title"]), CSS % c["theme"], body)

GAP = re.compile(r"\[\[(PENDING|SCRIPT-CHECK|VERIFY):\s*([^\]]*)\]\]")
def gaps(page_html):
    return GAP.findall(page_html)
def preview(page_html):
    return GAP.sub(lambda m: '<mark class="gap">%s: %s</mark>' % (m.group(1), m.group(2)), page_html)
def publish_ready(page_html):
    return not [g for g in gaps(page_html) if g[0] == "PENDING"] and "PAYMENT_LINK_PENDING" not in page_html
