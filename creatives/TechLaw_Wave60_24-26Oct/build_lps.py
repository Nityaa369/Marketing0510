# Builds the 60 landing pages (1 ad = 1 page). Run: python3 build_lps.py
# Pages 01 to 50: the 21-step spine compressed into 10 numbered sections (as the NCA builder),
#   reader-specific text from lp_content/<id>.json plus the common blocks below.
# Pages 51 to 55: finish-joining pages for people who started checkout (short, pay button first).
# Pages 56 to 60: attendance pages for people who already paid (no pay button, calendar links).
# Rules carried: first fold repeats the ad's words; fold order who-question, qualifier, offer,
# definition, deliverables, terms; one h2 names the reader; sentences short; no dash characters;
# market data page-only with source and date; disclaimer at the very end only; real pay link per page.
import os, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave as W
from render import PAL, DELIV

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "landing_pages")
e = html.escape

CSS = """*{box-sizing:border-box;margin:0;padding:0}body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#15181F;background:#fff;line-height:1.55;font-size:17px}
.w{max-width:640px;margin:0 auto;padding:0 20px}.fold{background:var(--soft);padding:22px 0 30px}
.rail{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;text-align:center;margin-bottom:14px}.rail b{color:var(--ac)}
h1{font-size:34px;line-height:1.1;font-weight:900;color:var(--ac);letter-spacing:-.01em}.q{font-weight:700;margin-top:10px}
.offer{font-size:26px;line-height:1.18;font-weight:900;margin-top:14px}.def{background:#fff;border-left:6px solid var(--ac);padding:12px 14px;margin-top:16px;font-weight:600}
ol.dl{list-style:none;margin-top:16px}ol.dl li{display:flex;gap:12px;margin-top:10px;font-weight:700}ol.dl span{min-width:30px;height:30px;border-radius:50%;background:var(--ac);color:#fff;display:flex;align-items:center;justify-content:center;font-size:15px}
.terms{margin-top:16px;font-weight:700;font-size:15px}.btn{display:block;text-align:center;background:var(--ac);color:#fff;font-weight:900;font-size:19px;padding:16px;border-radius:14px;text-decoration:none;margin-top:18px;box-shadow:0 6px 16px rgba(0,0,0,.15)}
section{padding:30px 0;border-bottom:1px solid #E5E7EC}.num{font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:var(--ac)}
h2{font-size:24px;line-height:1.2;font-weight:900;margin:4px 0 12px}p{margin-top:10px}.card{background:var(--soft);border-radius:12px;padding:14px 16px;margin-top:12px}
.card b{display:block}table{width:100%;border-collapse:collapse;margin-top:12px;font-size:15px}td,th{border:1px solid #D9DCE3;padding:8px;text-align:left;vertical-align:top}th{background:var(--soft)}
.src{font-size:13px;color:#4A5160}.close{background:var(--soft);padding:34px 0}.close h2{font-size:28px}.disc{font-size:13px;color:#3F4552;padding:26px 0 90px}
.sticky{position:fixed;left:0;right:0;bottom:0;background:#fff;box-shadow:0 -4px 14px rgba(0,0,0,.12);padding:10px 16px}.sticky a{margin:0;padding:13px;font-size:17px}"""

SESSIONS = [
 ("Day 1 · Sat 24 Oct · 6 to 9 PM IST", "Why tech law now, the 5 concepts every tech lawyer uses (SLAs, APIs, source and object code, white labelling, SaaS), and a software development agreement drafted with you, clause by clause. Then how lawyers reach startups in the US, UK, Canada, Europe and India."),
 ("Day 2 · Sun 25 Oct · 6 to 9 PM IST", "Six ways tech companies make money and the legal work each one creates, the services e-commerce companies need from lawyers, the 6-month plan, and how to network with US, UK and Canadian lawyers."),
 ("Day 3 · Mon 26 Oct · 7 to 10 PM IST", "Reviewing a startup's terms and pitching the fix, an e-commerce refund policy, an influencer agreement, and building a freelance profile for privacy work."),
]
MECH = [
 ("1. Skills", "Learn a few high-demand tasks first: contracts, website terms and policies. Not the whole field."),
 ("2. Track record", "Turn each task into a work sample, a short article or a post that shows what you can do."),
 ("3. Outreach", "Offer useful help to startups and to lawyers abroad, deliver well, and ask for a testimonial."),
]
PROOFS = [
 ("Mayank Barman", "Studied at Calcutta University and began learning tech law in his second year. He worked in the TMT team at Cyril Amarchand Mangaldas and is now an associate on Khaitan & Co's data privacy team."),
 ("Anurag Sushant", "Started as a fresher at a data protection consultancy, moved to privacy work at Deloitte, and is now a Senior Associate at KPMG in Dubai."),
 ("Tuba Sanobar", "A 2021 law graduate from Nagpur who was litigating. She now works at Infosys as a privacy and data protection analyst."),
 ("Pratik Harsh", "Ran his own firm before taking up tech law consulting, and now works at Conde Nast."),
 ("Raghav Trehan", "A GGSIPU graduate and company secretary. He cleared CIPP/E and joined Mastercard's data privacy team."),
]
FACTS = {
 "dpdp": ("The DPDP Rules were notified on 13 Nov 2025. Most duties for every business, including notice, consent, security and breach reporting, start on 13 May 2027.", "PIB, 17 Nov 2025"),
 "itr": ("From 20 Feb 2026, platforms must remove content within 3 hours of a government or court order, and must label AI-generated audio and video.", "LiveLaw, Feb 2026"),
 "rbi": ("On 28 Nov 2025 the RBI consolidated its rules into 244 Master Directions and withdrew 9,445 circulars.", "News On AIR, 28 Nov 2025"),
 "gst": ("On 27 May 2026 the Supreme Court upheld 28% GST on online money gaming, reviving tax demands of over Rs 1 lakh crore.", "Business Today, 27 May 2026"),
 "gcc": ("India has 2,117 global capability centres employing about 23.6 lakh people.", "Nasscom-Zinnov via Business Today, May 2026"),
 "startups": ("A record 55,200 startups were recognised in 2025-26, and India had 2.4 lakh recognised startups by 30 Jun 2026.", "Inc42, 2026"),
 "legaltech": ("Tracxn tracks 1,215 legal tech startups in India.", "Tracxn, Sep 2026"),
 "harvey": ("Harvey, a legal AI company used by 2,400+ organisations by its own count, hires Legal Engineers in Bengaluru who must be qualified Indian advocates.", "harvey.ai, 2026"),
 "upi": ("UPI carried 24,162 crore payments worth Rs 314 lakh crore in 2025-26.", "Lok Sabha data via The Tribune, 2026"),
 "digital": ("MeitY estimates the digital economy at 11.74% of national income in 2022-23 and projects nearly one-fifth by 2030.", "Inc42, Jan 2025"),
 "rdi": ("The Rs 1 lakh crore RDI Fund has backed its first 22 projects with loans at 3 to 4% for up to 15 years, on condition the IP stays in India.", "Business Today, 29 Sep 2026"),
}
FACTSET = {"C1": ["startups", "gcc", "legaltech", "harvey"], "C2": ["dpdp", "itr", "rbi", "gst"],
           "C3": ["harvey", "startups", "itr", "rdi"], "C4": ["upi", "rbi", "dpdp", "digital"],
           "C5": ["legaltech", "dpdp", "gcc", "startups"]}

def pay(a): return W.FUNNEL % W.slug(a)
def btn(a, label="Join the 3 live evenings for Rs 10"): return '<a class="btn" href="%s">%s</a>' % (pay(a), label)
def ps(paras): return "".join("<p>%s</p>" % e(x) for x in paras)
def sec(n, title, body): return '<section><div class="w"><div class="num">%s</div><h2>%s</h2>%s</div></section>' % (n, e(title), body)
def head(a, i, title):
    ac, _, bg, hi = PAL[i]
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><style>:root{--ac:%s;--soft:%s}%s</style></head><body>' % (e(title), ac, bg, CSS))
def fold(a, qualifier, cta=True):
    d = "".join('<li><span>%d</span>%s</li>' % (n + 1, e(x)) for n, x in enumerate(DELIV[a["camp"]]))
    return ('<div class="fold"><div class="w"><div class="rail">LawSikho <b>|</b> Tech Law Bootcamp</div>'
            '<h1>%s</h1><p class="q">%s</p><div class="offer">%s</div><div class="def">%s</div>'
            '<ol class="dl">%s</ol><p class="terms">%s, %s. Rs 10 incl. GST, refundable. Live only, no recordings.</p>%s</div></div>'
            % (e(a["callout"]), e(qualifier), e(a["head"]), e(W.DEFINE), d, W.DATES, W.TIMES, btn(a) if cta else ""))
def disc():
    return ('<div class="disc"><div class="w"><p><b>Please read.</b> Individual results depend on each learner\'s own work. '
            'LawSikho does not promise any job, client, internship or income. Learner stories describe what individuals did. '
            'Market figures come from the sources named beside them and can change. The Rs 10 fee is refundable on request. '
            'The bootcamp is live only and is not recorded.</p></div></div>')

def full_page(a, i, c):
    pi = int(a["id"]) % len(PROOFS); proofs = [PROOFS[pi], PROOFS[(pi + 2) % len(PROOFS)]]
    facts = "".join('<li style="margin-top:10px">%s <span class="src">Source: %s.</span></li>' % (e(FACTS[k][0]), e(FACTS[k][1])) for k in FACTSET[a["camp"]])
    alts = "".join('<div class="card"><b>%s</b>%s</div>' % (e(x["t"]), e(x["why"])) for x in c["alternatives"])
    sessions = "".join('<div class="card"><b>%s</b>%s</div>' % (e(t), e(d)) for t, d in SESSIONS)
    mech = "".join('<div class="card"><b>%s</b>%s</div>' % (e(t), e(d)) for t, d in MECH)
    prf = "".join('<div class="card"><b>%s</b>%s</div>' % (e(n), e(d)) for n, d in proofs)
    faq = "".join('<div class="card"><b>%s</b>%s</div>' % (e(x["q"]), e(x["a"])) for x in c["faq"])
    cost = ('<table><tr><th>Route</th><th>What it costs</th><th>What you get</th></tr>'
            '<tr><td>Figuring it out alone</td><td>Free, plus months of trial and error</td><td>Scattered articles and no feedback on your drafts</td></tr>'
            '<tr><td>A long course before you have tried the work</td><td>A large fee, paid upfront</td><td>A commitment before you know if the work suits you</td></tr>'
            '<tr><td><b>This bootcamp</b></td><td><b>Rs 10 incl. GST, refundable</b></td><td><b>Three live evenings doing the work with us</b></td></tr></table>')
    b = [head(a, i, a["head"] + " | Tech Law Bootcamp | LawSikho"), fold(a, c["qualifier"])]
    b.append(sec("01", c["symptom_title"], ps(c["symptom"])))
    b.append(sec("02", c["outcome_title"], ps(c["outcome"]) + btn(a)))
    b.append(sec("03", c["alternatives_title"], alts))
    b.append(sec("04", c["reframe_title"], ps(c["reframe"]) + "<h2 style='font-size:20px;margin-top:20px'>%s</h2>" % e(c["cost_title"]) + ps(c["cost"])))
    b.append(sec("05", c["role_h2"], ps(c["role"])))
    b.append(sec("06", "What happens in the 3 live evenings", sessions + "<p><b>The method we teach</b></p>" + mech +
                 "<p>The plan is about 2 hours a day: one hour learning, one hour outreach. No coding is needed. The work follows the business model.</p>" + btn(a)))
    b.append(sec("07", "What you will have done by Monday night", "<p>%s</p>" % e(c["first_artifact"]) + ps(c["longer_term"])))
    b.append(sec("08", "Lawyers who took this route", prf + '<p class="src">Individual results. They depend on each learner\'s own work.</p>'))
    b.append(sec("09", "Why the demand exists, and what it costs to find out",
                 '<p><b>Market data, not a promise:</b></p><ol style="padding-left:20px">%s</ol>' % facts + cost +
                 "<p><b>Risk removed.</b> The Rs 10 is refundable. Bring a laptop or phone and a notebook, and keep the three evenings free. Joining details arrive on WhatsApp and email.</p>" + btn(a)))
    b.append(sec("10", "Questions lawyers ask us", faq))
    b.append('<div class="close"><div class="w"><h2>%s</h2><p>%s</p>%s</div></div>' % (e(c["closing_title"]), e(c["closing"]), btn(a)))
    b.append(disc())
    b.append('<div class="sticky">%s</div></body></html>' % btn(a, "Join for Rs 10"))
    return "".join(b)

def finish_page(a, i):
    sessions = "".join('<div class="card"><b>%s</b>%s</div>' % (e(t), e(d)) for t, d in SESSIONS)
    faq = [("My payment did not go through. What now?", "Tap the button and try again by UPI or card. If money left your account without a confirmation, it is normally reversed by the payment gateway. You can also write to webinars@lawsikho.in."),
           ("Is the Rs 10 refundable?", "Yes. It is refundable on request."),
           ("Will there be recordings?", "No. The three evenings are live only, so keep them free."),
           ("Do I need to know coding?", "No. Tech law work follows the business model, not the code.")]
    f = "".join('<div class="card"><b>%s</b>%s</div>' % (e(q), e(x)) for q, x in faq)
    q = {"51": "Finish joining in about a minute. It is refundable.", "52": "Your seat is held for you.",
         "53": "You started joining. Finish in about a minute.", "54": "Rs 10, refundable, live.",
         "55": "Try the payment again by UPI or card."}[a["id"]]
    b = [head(a, i, a["head"] + " | Tech Law Bootcamp | LawSikho"), fold(a, q)]
    b.append(sec("01", "The 3 live evenings", sessions + btn(a)))
    b.append(sec("02", "Before you pay", f + btn(a)))
    b.append(disc()); b.append('<div class="sticky">%s</div></body></html>' % btn(a, "Finish joining for Rs 10"))
    return "".join(b)

CAL = [("Tech Law Bootcamp Day 1", "20261024T123000Z/20261024T153000Z"),
       ("Tech Law Bootcamp Day 2", "20261025T123000Z/20261025T153000Z"),
       ("Tech Law Bootcamp Day 3", "20261026T133000Z/20261026T163000Z")]
def cal_link(t, d):
    from urllib.parse import quote
    return "https://calendar.google.com/calendar/render?action=TEMPLATE&text=%s&dates=%s&details=%s" % (
        quote(t), d, quote("LawSikho Tech Law Bootcamp. Live only, no recordings. Joining details are in your WhatsApp and email."))

def attend_page(a, i):
    focus = {"56": 0, "57": 0, "58": 1, "59": 2, "60": 2}[a["id"]]
    cards = "".join('<div class="card"><b>%s</b>%s<p><a href="%s">Add to Google Calendar</a></p></div>' % (e(SESSIONS[k][0]), e(SESSIONS[k][1]), cal_link(*CAL[k])) for k in range(3))
    b = [head(a, i, a["head"] + " | Tech Law Bootcamp | LawSikho"),
         '<div class="fold"><div class="w"><div class="rail">LawSikho <b>|</b> Tech Law Bootcamp</div><h1>%s</h1><div class="offer">%s</div>'
         '<p class="q">%s</p><a class="btn" href="%s">Add Day %d to my calendar</a></div></div>' % (e(a["callout"]), e(a["head"]), e(a["why"]), cal_link(*CAL[focus]), focus + 1)]
    b.append(sec("01", "Your 3 live evenings", cards))
    b.append(sec("02", "Before Saturday", ps(["Keep a laptop or phone and a notebook ready.", "Joining details are in your WhatsApp and email. Check your spam folder too.",
                                             "There are no recordings, so keep all three evenings free. Attend at least 2.5 hours each day to receive that day's templates."])))
    b.append(disc()); b.append("</body></html>")
    return "".join(b)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); missing = []
    for i, a in enumerate(W.ADS):
        n = int(a["id"]); path = os.path.join(OUT, "lp_%s.html" % W.slug(a))
        if n <= 50:
            f = os.path.join(HERE, "lp_content", "%s.json" % a["id"])
            if not os.path.exists(f): missing.append(a["id"]); continue
            page = full_page(a, i, json.load(open(f)))
        elif n <= 55: page = finish_page(a, i)
        else: page = attend_page(a, i)
        assert "—" not in page and "–" not in page, a["id"]
        open(path, "w").write(page)
    print("built", 60 - len(missing), "missing content:", missing)
