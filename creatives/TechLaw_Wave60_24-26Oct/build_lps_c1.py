# Builds the 10 C1 landing pages for the user's graphic statics (1 ad = 1 page).
# Run: python3 build_lps_c1.py   -> landing_pages_c1/lp_tlc1-<nn>.html (+ img/)
# First fold repeats the ad: same picture, same banner, same hook, same supporting copy.
# Body: the reader-specific argument already written in lp_content/<old id>.json, the shared blocks
# from build_lps.py, plus two sections that trace to the camp facts (Day 1 concepts, Day 2 plan).
# The only disclaimer sits at the very end. No dash characters anywhere.
import os, sys, json, html, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_lps as B
e = html.escape
OUT = os.path.join(HERE, "landing_pages_c1")
IMG = os.path.join(HERE, "graphic", "c1_final_v4")  # the generated v4 ads; photo band cropped below
FUNNEL = "https://growthx.lawsikho.com/f/%s"
DEFINE = "Tech law is the legal work tech companies need: contracts, privacy, compliance and disputes."

# nn: (old lp_content id, accent, soft background, banner, hook [(text, accent?)], supporting copy)
ADS = {
 "01": ("02", "#13756B", "#EAF5F2", "For LLB holders working in HR",
        [("You used to hire the talent for firms.", 0), ("Now become the legal brains that advise them.", 1)],
        "Use your LLB to explore tech law, employment contracts and workplace compliance."),
 "02": ("03", "#1D5FD0", "#EAF1FC", "For LLB holders in banking",
        [("You already know how money moves.", 0), ("Now learn the law that drives fintech.", 1)],
        "Use your degree to explore fintech regulations, financial contracts and technology law."),
 "03": ("04", "#5B2BD6", "#F1ECFC", "For LLB holders in content",
        [("You used to write the content.", 0), ("Now learn to draft the contracts as well.", 1)],
        "Use your LLB to build practical skills in software agreements, privacy policies and tech law documents."),
 "04": ("05", "#D9480F", "#FDF0E8", "For LLB holders in sales & operations",
        [("You know how business works.", 0), ("Now become the legal brain behind the deal.", 1)],
        "Use your degree to explore commercial contracts, software agreements and compliance."),
 "05": ("07", "#B5122B", "#FBEDEF", "For lawyers who paused practice for family",
        [("You took a break from practice.", 0), ("Not from being a lawyer.", 1), ("Let's restart.", 0)],
        "Use your degree to rebuild practical legal skills in contracts, privacy and technology law."),
 "06": ("08", "#1D4FB8", "#EAF0FB", "For lawyers who moved cities after marriage",
        [("New city. New chapter.", 0), ("Your LLB still comes with you.", 1), ("Let's make use of it.", 0)],
        "Explore practical tech law skills that can open up new directions for your legal career."),
 "07": ("09", "#1E40AF", "#EAF0FB", "For Indian lawyers living abroad with family",
        [("You moved countries.", 0), ("Don't leave your legal ambitions behind.", 1)],
        "Use your Indian law degree to explore tech law skills and the opportunities open to you."),
 "08": ("01", "#B45309", "#FCF3E6", "For LLB holders in BPO & back-office jobs",
        [("Hello... your LLB is calling back.", 0), ("Let's get ready for the legal role you planned for.", 1)],
        "Use your degree to learn practical contract drafting, privacy and technology law skills."),
 "09": ("06", "#BE185D", "#FCEEF4", "For women lawyers returning after a family break",
        [("Your career took a break.", 0), ("Time to come back with a more flexible legal route.", 1)],
        "Refresh your legal skills and explore contracts, privacy and tech law, live from home."),
 "10": ("10", "#8A5A12", "#F8F1E4", "For lawyers who left a law firm for family",
        [("You left the firm.", 0), ("You didn't leave your legal potential.", 1), ("Let's get back.", 0)],
        "Use your degree to explore practical tech law work, from drafting software contracts to reviewing privacy policies."),
}
HOOK2 = {"02": "#B7791F", "05": "#B7791F", "10": "#B7791F"}  # where the ad used yellow, a readable amber
DELIV = ["Evening 1: draft a software development agreement with us, clause by clause.",
         "Evening 2: see six ways tech companies make money, and the legal work each one creates.",
         "Evening 3: review a startup's terms and learn how lawyers pitch the fix."]
CONCEPTS = [  # Day 1 skill: the 5 concepts every tech lawyer must know (camp facts, Day 1)
 ("SLAs", "A service level agreement sets the uptime a software provider promises, what counts as downtime, and the credits a customer gets when the promise is missed."),
 ("Support metrics", "How fast a provider must answer and fix a problem, written as response and resolution times. Lawyers decide what happens when they slip."),
 ("APIs", "The connection that lets one app talk to another. The contract decides who may use it, for what, and who is liable when it breaks."),
 ("Source code and object code", "Source code is what programmers write. Object code is what the machine runs. Licences and ownership clauses turn on the difference."),
 ("White labelling", "Selling another company's product under your own brand. The agreement sets who owns what, the quality promised and who answers to the customer."),
]
PLAN = [  # Day 2: the 6-month plan (camp facts section 6), page-only, no income or job targets
 "About 2 hours a day: one hour learning, one hour on outreach and your track record.",
 "Months 1 and 2: start with the easier skills, such as privacy, website policies and contracts, and begin outreach in week 1.",
 "Outreach means posting what you learn on LinkedIn, pitching startups one hour a day, and helping lawyers abroad build their brand first.",
 "Aim for your first testimonials in month 1, then add skills one by one: SaaS, e-commerce, fintech, IP and takedowns, and more, about 20 over 6 months.",
]

def btn(slug, label="Join the 3 live evenings for Rs 10"):
    return '<a class="btn" href="%s">%s</a>' % (FUNNEL % slug, label)

def page(nn):
    old, ac, soft, banner, hook, support = ADS[nn]
    c = json.load(open(os.path.join(HERE, "lp_content", "%s.json" % old)))
    slug = "tlc1-%s" % nn
    hk = "".join('<span style="display:block;color:%s">%s</span>' % (HOOK2.get(nn, "#D7191F") if a else "#15181F", e(t)) for t, a in hook)
    title = " ".join(t for t, _ in hook)
    pi = int(old) % len(B.PROOFS); proofs = [B.PROOFS[pi], B.PROOFS[(pi + 2) % len(B.PROOFS)]]
    card = lambda t, d: '<div class="card"><b>%s</b>%s</div>' % (e(t), e(d))
    facts = "".join('<li style="margin-top:10px">%s <span class="src">Source: %s.</span></li>' % (e(B.FACTS[k][0]), e(B.FACTS[k][1])) for k in B.FACTSET["C1"])
    cost = ('<table><tr><th>Route</th><th>What it costs</th><th>What you get</th></tr>'
            '<tr><td>Figuring it out alone</td><td>Free, plus months of trial and error</td><td>Scattered articles and no feedback on your drafts</td></tr>'
            '<tr><td>A long course before you have tried the work</td><td>A large fee, paid upfront</td><td>A commitment before you know if the work suits you</td></tr>'
            '<tr><td><b>This bootcamp</b></td><td><b>Rs 10 incl. GST, refundable</b></td><td><b>Three live evenings doing the work with us</b></td></tr></table>')
    css = B.CSS + (".brand{font-family:Georgia,'Times New Roman',serif;font-size:30px;font-weight:700;text-align:center}"
                   ".pill{display:block;width:max-content;max-width:100%;margin:10px auto 0;background:var(--ac);color:#fff;font-weight:800;font-size:13px;"
                   "letter-spacing:.06em;text-transform:uppercase;padding:9px 14px;border-radius:10px;text-align:center}"
                   ".hook{font-family:Georgia,'Times New Roman',serif;font-size:33px;line-height:1.1;font-weight:700;margin-top:16px}"
                   ".sup{background:#fff;border-left:6px solid var(--ac);border-radius:12px;padding:12px 14px;margin-top:14px;font-weight:700}"
                   ".hero{display:block;width:100%;border-radius:16px;margin-top:16px;box-shadow:0 8px 22px rgba(0,0,0,.16)}"
                   ".btn{background:#E11D2E}")  # same red Join button as the ads
    b = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         '<title>%s | Tech Law Bootcamp | LawSikho</title><style>:root{--ac:%s;--soft:%s}%s</style></head><body>' % (e(title), ac, soft, css)]
    dl = "".join('<li><span>%d</span>%s</li>' % (n + 1, e(x)) for n, x in enumerate(DELIV))
    b.append('<div class="fold"><div class="w"><div class="brand">LawSikho</div><div class="pill">%s</div><div class="hook">%s</div>'
             '<div class="sup">%s</div><p class="q">%s</p><div class="def">%s</div><ol class="dl">%s</ol>'
             '<p class="terms">Sat 24 and Sun 25 Oct, 6 to 9 PM IST. Mon 26 Oct, 7 to 10 PM IST. Rs 10 incl. GST, refundable. Live only, no recordings.</p>%s'
             '<img class="hero" src="img/TL_C1_%s.jpg" alt="%s" style="margin-top:18px"></div></div>'
             % (e(banner), hk, e(support), e(c["qualifier"]), e(DEFINE), dl, btn(slug), nn, e(banner)))
    sec = B.sec; ps = B.ps
    b.append(sec("01", c["symptom_title"], ps(c["symptom"])))
    b.append(sec("02", c["outcome_title"], ps(c["outcome"]) + btn(slug)))
    b.append(sec("03", c["alternatives_title"], "".join(card(x["t"], x["why"]) for x in c["alternatives"])))
    b.append(sec("04", c["reframe_title"], ps(c["reframe"]) + "<h2 style='font-size:20px;margin-top:20px'>%s</h2>" % e(c["cost_title"]) + ps(c["cost"])))
    b.append(sec("05", c["role_h2"], ps(c["role"])))
    b.append(sec("06", "Five words every tech contract uses",
                 "<p>On Evening 1 you learn the five concepts behind most technology contracts. None of them needs coding.</p>" + "".join(card(t, d) for t, d in CONCEPTS)))
    b.append(sec("07", "What happens in the 3 live evenings", "".join(card(t, d) for t, d in B.SESSIONS) + "<p><b>The method we teach</b></p>" +
                 "".join(card(t, d) for t, d in B.MECH) + btn(slug)))
    b.append(sec("08", "What you will have done by Monday night", "<p>%s</p>" % e(c["first_artifact"]) + ps(c["longer_term"])))
    b.append(sec("09", "The plan after the camp, in plain steps", '<ol style="padding-left:20px">%s</ol>' % "".join('<li style="margin-top:8px">%s</li>' % e(x) for x in PLAN) +
                 "<p>This is the plan taught on Evening 2. How far you get depends on the hours you put in.</p>"))
    b.append(sec("10", "Lawyers who took this route", "".join(card(n, d) for n, d in proofs) + '<p class="src">Individual results. They depend on each learner\'s own work.</p>'))
    b.append(sec("11", "Why the demand exists, and what it costs to find out", '<p><b>Market data, not a promise:</b></p><ol style="padding-left:20px">%s</ol>' % facts + cost +
                 "<p><b>Risk removed.</b> The Rs 10 is refundable. Bring a laptop or phone and a notebook, and keep the three evenings free. Joining details arrive on WhatsApp and email.</p>" + btn(slug)))
    b.append(sec("12", "Questions lawyers ask us", "".join(card(x["q"], x["a"]) for x in c["faq"])))
    b.append('<div class="close"><div class="w"><h2>%s</h2><p>%s</p>%s</div></div>' % (e(c["closing_title"]), e(c["closing"]), btn(slug)))
    b.append(B.disc())
    b.append('<div class="sticky">%s</div></body></html>' % btn(slug, "Join for Rs 10"))
    html_ = "".join(b)
    assert "—" not in html_ and "–" not in html_, nn
    return slug, html_

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True); built = []
    from PIL import Image
    for nn in ADS:
        src = os.path.join(IMG, "TL_C1_%s.jpg" % nn)
        if os.path.exists(src):
            im = Image.open(src).convert("RGB"); w, h = im.size; im = im.crop((0, int(h * .30), w, int(h * .68))); im.thumbnail((720, 1400)); im.save(os.path.join(OUT, "img", "TL_C1_%s.jpg" % nn), quality=82)
        slug, h = page(nn); open(os.path.join(OUT, "lp_%s.html" % slug), "w").write(h); built.append(slug)
    print("built", len(built))
