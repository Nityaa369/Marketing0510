# Renders the 60 static faces (1080x1350, 4:5) from wave.py. Run: python3 render.py
# Formats with evidence: notice (0.81x twice), search (US Acc us51), email (DP wave 4 build),
# editorial (SQE 0.67x), eligibility check (Ramanuj approved on SQE), meme (Tech Law career break
# 0.91x), kinetic text (Tech Law unused LLB video winner), redline (Ruchika's format list).
# No chat faces (1.28x), no pay charts, no photos (no faces to source). Light backgrounds.
import os, sys, glob, subprocess, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave as W
import palette as P

HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
_P = P.build(60)
PAL = [_P[(i*23) % 60] for i in range(60)]  # spread hues so neighbours differ
e = html.escape

SENDERS = ["Meera Iyer", "Arjun Sethi", "Zoya Sheikh", "Harpreet Gill", "Kavya Nair", "Rohan Das",
           "Anjali Rao", "Imran Qureshi", "Divya Menon", "Siddharth Jain", "Neha Kulkarni"]
MIRROR = {
 "02": "You keep saying your law degree is wasted in HR.",
 "07": "You keep saying it is too late to come back to law.",
 "14": "You keep saying every account case looks the same.",
 "20": "You keep saying good legal work only exists in metros.",
 "24": "You keep saying your LLM has not opened a door yet.",
 "30": "You keep saying research never brings you your own clients.",
 "35": "You keep saying clients ask you contract questions you turn away.",
 "43": "You keep saying nobody hires a lawyer after a break.",
 "50": "You keep saying startups never reply to lawyers.",
 "52": "You said you would restart this year.",
 "59": "You asked me what Day 3 covers.",
}
QUERY = {
 "04": "can an llb holder become a tech lawyer",
 "09": "tech law career for indian lawyers living abroad",
 "17": "how can a family lawyer move into tech law",
 "25": "career option while preparing for judiciary",
 "29": "tech law work for final year law students",
 "34": "how an ip lawyer becomes a tech lawyer",
 "40": "move from document review to tech law",
 "44": "tech law career if not from nlu",
 "49": "what is taught in a tech law bootcamp",
 "55": "tech law bootcamp rs 10 payment did not go through",
}
MEME = {
 "06": ("Relatives: \"Will anyone hire you after the gap?\"", "Tech client: \"Can you send the privacy policy by Friday?\""),
 "18": ("Old view: defamation work ends in a courtroom.", "Now: creators and platforms need takedown notices and influencer agreements."),
 "26": ("Chamber life: your name on none of the files.", "Tech law: your own client, your own draft."),
 "38": ("Between jobs: \"I will wait for the right opening.\"", "Tech law: learn the work companies pay for while you wait."),
 "48": ("Myth: \"Tech law is only for fresh graduates.\"", "Fact: the rules are new, so nobody has a head start."),
}
REDLINE = {
 "11": ("Payment is due when the work is complete.", "20% advance, the rest paid on each milestone."),
 "32": ("The Company licenses the software.", "The Company licenses the object code only."),
 "46": ("The Developer may keep copies of the code.", "The Developer hands over all code and keeps no copies."),
 "57": ("The Client accepts the software on delivery.", "The Client gets 14 days of acceptance testing first."),
}
TICKS = {
 "10": ["You hold an LLB", "You left a firm job for family", "You can keep 3 evenings free"],
 "13": ["You practise before consumer forums", "You know refund and deficiency disputes", "You can keep 3 evenings free"],
 "22": ["You are newly enrolled", "You want your own clients", "You can keep 3 evenings free"],
 "36": ["You are a company secretary", "You hold an LLB", "You can keep 3 evenings free"],
 "41": ["You hold an LLB", "You have never written code", "You can keep 3 evenings free"],
 "54": ["You are a junior advocate", "Rs 10, refundable", "Live, 3 evenings, from home"],
}

BASE = """*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,Arial,sans-serif;background:%(bg)s;color:#14171F;display:flex;flex-direction:column;padding:40px 56px 32px}
.rail{text-align:center;font-size:25px;font-weight:900;letter-spacing:.12em;text-transform:uppercase}
.rail b{color:%(ac)s}
.callout{font-size:70px;font-weight:900;line-height:1.04;letter-spacing:-.02em;color:%(ac)s}
.head{font-size:62px;font-weight:900;line-height:1.08;letter-spacing:-.02em}
.why{font-size:39px;line-height:1.3}
.def{font-size:31px;line-height:1.32;background:%(hi)s;border-radius:14px;padding:16px 22px;font-weight:700}
.grow{flex:1;min-height:6px}
.btn{background:%(ac)s;color:#fff;text-align:center;font-size:50px;font-weight:900;padding:24px;border-radius:70px;margin-top:22px}
.foot{text-align:center;font-size:26px;font-weight:900;letter-spacing:.06em;text-transform:uppercase;margin-top:14px}
.lab{text-align:center;font-size:22px;color:#4A5160;margin-top:6px}
.card{background:#fff;border-radius:26px;box-shadow:0 14px 36px rgba(20,30,50,.13)}
"""
DELIV = {
 "C1": ["Draft a software development agreement", "Review a startup's terms", "Reach startups in the US, UK, Canada, Europe"],
 "C2": ["Review a startup's terms", "Draft a software contract, clause by clause", "Reach startups without pausing your practice"],
 "C3": ["Draft a software development agreement", "Review a startup's terms", "Turn each task into a work sample"],
 "C4": ["Draft a software development agreement", "Draft an e-commerce refund policy", "Map the legal work in 6 business models"],
 "C5": ["Day 1: a software contract, drafted live", "Day 2: how tech companies make money", "Day 3: a startup's terms, reviewed live"],
 "C6": ["Sat 24 Oct, 6 to 9 PM IST", "Sun 25 Oct, 6 to 9 PM IST", "Mon 26 Oct, 7 to 10 PM IST"],
}
def deliv(a, size=34):
    rows = "".join('<div style="display:flex;gap:16px;align-items:flex-start;margin-top:10px"><div style="min-width:44px;height:44px;border-radius:50%%;background:%s;color:#fff;font-size:26px;font-weight:900;display:flex;align-items:center;justify-content:center">%d</div><div style="font-size:%dpx;font-weight:700;line-height:1.25;padding-top:3px">%s</div></div>' % (a["_ac"], n + 1, size, e(x)) for n, x in enumerate(DELIV[a["camp"]]))
    lab = "In 3 live evenings" if a["camp"] != "C6" else "The 3 live evenings"
    return '<div style="margin-top:22px"><div style="font-size:24px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:#4A5160">%s</div>%s</div>' % (lab, rows)

RAIL = '<div class="rail">LawSikho <b>|</b> Tech Law Bootcamp</div>'
FOOT = ('<div class="btn">%s</div><div class="foot">Rs 10 incl. GST · Live only · Refundable</div>' % W.BTN)

def body_kinetic(a):
    return (RAIL + '<div style="margin-top:56px" class="callout">%s</div>'
            '<div class="head" style="font-size:84px;margin-top:30px">%s</div>'
            '<div class="why" style="margin-top:34px;font-size:44px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div>' % (e(a["callout"]), e(a["head"]), e(a["why"]), deliv(a, 40), e(W.DEFINE)) + FOOT)

def body_email(a, i):
    s = SENDERS[i % len(SENDERS)]  # email uses a slimmer button row below
    mir = MIRROR.get(a["id"], "")
    return (RAIL + '<div class="card" style="margin-top:22px;padding:30px 42px;flex:1;display:flex;flex-direction:column">'
            '<div style="align-self:flex-start;background:#EEF0F4;color:#4A5160;font-size:24px;font-weight:800;padding:6px 16px;border-radius:8px">Inbox</div>'
            '<div class="callout" style="font-size:56px;margin-top:12px">%s</div>'
            '<div class="head" style="font-size:46px;margin-top:10px">%s</div>'
            '<div style="display:flex;align-items:center;gap:18px;margin-top:18px;padding-bottom:16px;border-bottom:2px solid #E7E9EE">'
            '<div style="width:64px;height:64px;border-radius:50%%;background:%s;color:#fff;font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center">%s</div>'
            '<div><div style="font-size:29px;font-weight:800">%s</div><div style="font-size:23px;color:#5A6170">to me</div></div></div>'
            '<div class="why" style="margin-top:14px;font-size:33px">%s</div>'
            '<div class="why" style="margin-top:10px;font-size:33px">%s</div>%s<div class="grow"></div>'
            '<div class="def" style="font-size:27px">%s</div>'
            '<div class="why" style="margin-top:10px;font-size:33px">Rs 10 live bootcamp, 3 evenings. Join me?</div></div>'
            % (e(a["callout"]), e(a["head"]), PAL[i][0], s[0], e(s), e(mir), e(a["why"]), deliv(a, 28), e(W.DEFINE)) + FOOT +
            '<div class="lab">Dramatised email. Not a real learner.</div>')

def body_notice(a):
    return (RAIL + '<div class="card" style="margin-top:22px;padding:34px 46px;flex:1;display:flex;flex-direction:column;border:5px double %s">'
            '<div style="text-align:center;font-size:30px;font-weight:900;letter-spacing:.3em;color:%s">NOTICE</div>'
            '<div style="text-align:center;font-size:22px;font-weight:700;color:#4A5160;margin-top:4px">Issued by LawSikho</div>'
            '<div class="callout" style="margin-top:26px">%s</div>'
            '<div class="head" style="margin-top:16px">%s</div>'
            '<div class="why" style="margin-top:22px;font-size:42px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div></div>' % (a["_ac"], a["_ac"], e(a["callout"]), e(a["head"]), e(a["why"]), deliv(a, 38), e(W.DEFINE)) + FOOT)

def body_search(a):
    q = QUERY.get(a["id"], a["callout"].lower().rstrip("?"))
    return (RAIL + '<div class="callout" style="margin-top:30px">%s</div>'
            '<div class="card" style="margin-top:26px;padding:18px 28px;border-radius:60px;display:flex;align-items:center;gap:18px">'
            '<div style="width:34px;height:34px;border:5px solid #6A7080;border-radius:50%%"></div>'
            '<div style="font-size:34px;color:#30343C">%s</div></div>'
            '<div class="card" style="margin-top:22px;padding:30px 36px;flex:1;display:flex;flex-direction:column">'
            '<div style="font-size:24px;color:#4A5160">lawsikho.com · Tech Law Bootcamp</div>'
            '<div class="head" style="font-size:52px;color:%s;margin-top:8px">%s</div>'
            '<div class="why" style="margin-top:16px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div></div>' % (e(a["callout"]), e(q), a["_ac"], e(a["head"]), e(a["why"]), deliv(a, 32), e(W.DEFINE)) + FOOT)

def body_editorial(a):
    return (RAIL + '<div style="margin-top:22px;border-top:6px solid #14171F;border-bottom:2px solid #14171F;padding:10px 0;display:flex;justify-content:space-between;font-size:24px;font-weight:800;letter-spacing:.1em">'
            '<span>THE TECH LAW BRIEF</span><span>ISSUED BY LAWSIKHO</span></div>'
            '<div style="font-size:30px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:%s;margin-top:30px">For you</div>'
            '<div class="callout" style="margin-top:8px">%s</div>'
            '<div class="head" style="font-family:Georgia,serif;font-size:70px;margin-top:20px">%s</div>'
            '<div class="why" style="margin-top:24px;border-left:8px solid %s;padding-left:22px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div>' % (a["_ac"], e(a["callout"]), e(a["head"]), a["_ac"], e(a["why"]), deliv(a), e(W.DEFINE)) + FOOT)

def body_eligibility(a):
    t = TICKS.get(a["id"], ["You hold an LLB", a["callout"].rstrip("?"), "You can keep 3 evenings free"])
    rows = "".join('<div style="display:flex;gap:20px;align-items:center;margin-top:16px"><div style="width:52px;height:52px;border-radius:12px;background:%s;color:#fff;font-size:38px;font-weight:900;display:flex;align-items:center;justify-content:center">&#10003;</div><div style="font-size:38px;font-weight:700">%s</div></div>' % (a["_ac"], e(x)) for x in t)
    return (RAIL + '<div class="callout" style="margin-top:30px">%s</div>'
            '<div class="card" style="margin-top:24px;padding:28px 36px">'
            '<div style="font-size:28px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#4A5160">Quick check</div>%s</div>'
            '<div class="head" style="margin-top:26px">%s</div>'
            '<div class="why" style="margin-top:16px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div>' % (e(a["callout"]), rows, e(a["head"]), e(a["why"]), deliv(a, 32), e(W.DEFINE)) + FOOT)

def body_meme(a):
    m1, m2 = MEME.get(a["id"], (a["callout"], a["why"]))
    return (RAIL + '<div class="callout" style="margin-top:26px;font-size:62px">%s</div>'
            '<div class="card" style="margin-top:20px;padding:26px 32px;font-size:38px;font-weight:800;line-height:1.28;border-left:14px solid #9AA0AC">%s</div>'
            '<div class="card" style="margin-top:16px;padding:26px 32px;font-size:38px;font-weight:800;line-height:1.28;border-left:14px solid %s">%s</div>'
            '<div class="head" style="margin-top:26px;font-size:58px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div>' % (e(a["callout"]), e(m1), a["_ac"], e(m2), e(a["head"]), deliv(a), e(W.DEFINE)) + FOOT)

def body_redline(a):
    old, new = REDLINE.get(a["id"], ("", ""))
    return (RAIL + '<div class="callout" style="margin-top:28px">%s</div>'
            '<div class="card" style="margin-top:22px;padding:28px 34px;font-family:Georgia,serif">'
            '<div style="font-size:24px;font-family:Inter,Arial,sans-serif;font-weight:900;letter-spacing:.08em;color:#4A5160">SOFTWARE DEVELOPMENT AGREEMENT · REDLINE</div>'
            '<div style="font-size:38px;line-height:1.35;margin-top:14px;color:#9C2B2B;text-decoration:line-through">%s</div>'
            '<div style="font-size:38px;line-height:1.35;margin-top:10px;color:#14171F;background:%s;padding:4px 10px;border-radius:6px">%s</div></div>'
            '<div class="head" style="margin-top:26px">%s</div>'
            '<div class="why" style="margin-top:14px">%s</div>%s<div class="grow"></div>'
            '<div class="def">%s</div>' % (e(a["callout"]), e(old), a["_hi"], e(new), e(a["head"]), e(a["why"]), deliv(a, 32), e(W.DEFINE)) + FOOT)

def face(a, i):
    a = dict(a); a["_ac"], _, a["_bg"], a["_hi"] = PAL[i]
    css = BASE % dict(ac=a["_ac"], bg=a["_bg"], hi=a["_hi"])
    f = a["fmt"]
    b = {"kinetic": lambda: body_kinetic(a), "email": lambda: body_email(a, i), "notice": lambda: body_notice(a),
         "search": lambda: body_search(a), "editorial": lambda: body_editorial(a),
         "eligibility": lambda: body_eligibility(a), "meme": lambda: body_meme(a), "redline": lambda: body_redline(a)}[f]()
    if a["adset"] == "B_Turn_Up_Live":  # already paid: no buy button, a reminder instead
        b = b.replace('<div class="btn">%s</div>' % W.BTN, '<div class="btn">Set a reminder</div>')
        b = b.replace("Rs 10 incl. GST · Live only · Refundable", "Live only · No recordings")
        b = b.replace("Rs 10 live bootcamp, 3 evenings. Join me?", "See you on Saturday at 6 PM.")
    return '<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (css, b)

def stem(a):
    return "tl60_%s_%s_%s" % (a["id"], a["camp"].lower(), a["fmt"])

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for i, a in enumerate(W.ADS):
        if only and a["id"] not in only: continue
        h = os.path.join(HERE, "html", stem(a) + ".html"); open(h, "w").write(face(a, i))
        subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1080,1350", "--screenshot=" + os.path.join(HERE, "ads", stem(a) + ".png"),
                        "file://" + h], check=True, capture_output=True)
    print("rendered", len(glob.glob(os.path.join(HERE, "ads", "*.png"))))
