"""Build the 20 Contract Drafting Community landing pages (1 ad = 1 page).

    python3 build_lps.py <copy.json> <out_dir>

copy.json holds the reader-specific half (written to SPEC in this folder); this file holds the
shared half: why-now facts, the offer, the 16 documents, the 9 sessions, implementation, cost
comparison, refund, shared FAQ and the disclaimer. Facts come only from the CD 64-65 calendar
(docs/COMMUNITY_CURRICULA_Oct-Nov2026.md) and the dated sources on the why-now cards.
Works with JavaScript off: no script at all, native <details>, CSS-only sticky bar.
"""
import html, json, os, re, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ADS = os.path.join(HERE, "..", "ship")
ICPS = json.load(open(os.path.join(HERE, "..", "icps.json"), encoding="utf-8"))

PRICE = "₹200"
BTN = "Join the Contract Drafting Community for ₹200"
STICKY = "Join for ₹200 · 21 days, live online"
DATES = "21 Oct to 11 Nov"
DEFN = ("Contract drafting is writing the agreements a business signs: "
        "who does what, who pays, and who carries each risk.")


def slug(i):
    return f"cdtp-{i}"


def pay(i):
    return f"https://growthx.lawsikho.com/f/{slug(i)}"


# One accent tint per page (the button stays the ad's red; this varies the page around it).
TINTS = ["#1F6F8B", "#7A4E9E", "#2E7D4F", "#B5562A", "#3D5A99", "#8E3B5B", "#22766F", "#9A6B12",
         "#5B4BA0", "#2F6E9E", "#7D5A2E", "#3B7A3B", "#A1452E", "#45628A", "#6B3F86", "#287068",
         "#8A5A1E", "#4A5FA8", "#9B3F6E", "#2D6F57"]

WHY = [
    ("India's data protection rules were notified on 14 Nov 2025. Most duties start 18 months later.",
     "Businesses that hold customer or staff data need privacy policies and vendor terms written.",
     "DPDP Rules 2025, MeitY, notified 14 Nov 2025; PIB"),
    ("More than 2.23 lakh startups were recognised in India by 31 Mar 2026.",
     "Each one signs founder, hiring and vendor contracts, and most have no lawyer on staff.",
     "DPIIT data via Inc42; Manorama Yearbook, Apr 2026"),
    ("The UK had about 5.7 million private sector businesses at the start of 2025.",
     "Most are small firms. Each one that collects customer data needs a privacy notice, drafted from anywhere.",
     "UK Department for Business and Trade, Business population estimates 2025, Oct 2025"),
]

DOCS = ["Parts of a contract", "Non-compete clause", "E-commerce terms and conditions",
        "Employment agreement and remote work policy", "NDA and confidentiality clauses",
        "Cookie policy", "Co-founder agreement", "DPDPA privacy policy", "ESOP plan",
        "SAFE agreement", "Term sheet", "SaaS agreement", "Representations and warranties",
        "IP licensing clause", "Commercial lease", "Vendor service agreement",
        "Joint development agreement"]

SESSIONS = [
    "Using AI to find missing clauses and red flags",
    "Finding issues in website terms with AI",
    "Listing your first gig on a services marketplace",
    "Questions to ask a client before drafting",
    "Reaching UK small businesses with a GDPR privacy policy",
    "Pitching startups directly",
    "How law firm partners and in-house counsel think",
    "A LinkedIn profile that makes you known for contracts",
    "Publishing your first article",
]

SHARED_FAQ = [
    ("Do I need drafting experience before I join?",
     "No. Day one starts with the parts of a contract. Each later document builds on that, one a day."),
    ("What if I miss a live session?",
     "Sessions are live and recordings are not promised. The daily reading and quiz stay in the "
     "WhatsApp group, so you can keep up with the documents on your own time."),
    ("Is the ₹200 refundable?",
     "Yes. The fee is ₹200 including GST, and it is refundable."),
]

CSS = r"""
:root{--red:#E2231A;--ink:#1C1A17;--paper:#F7F0E3;--card:#FFFDF8;--yel:#FFD84D;--tint:TINT}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;overflow-x:clip}
body{background:var(--paper);color:var(--ink);font:19px/1.65 'Source Sans 3',Arial,sans-serif;overflow-x:clip;padding-bottom:84px}
h1,h2,h3{font-family:'Libre Caslon Text',Georgia,serif;line-height:1.2;text-wrap:balance}
h2{font-size:31px;margin:0 0 14px}h3{font-size:21px;margin:0 0 6px}
p{max-width:62ch;margin:0 0 14px}
.wrap{max-width:1080px;margin:0 auto;padding:0 18px}
section{padding:46px 0;border-top:2px dashed rgba(28,26,23,.14)}
.num{display:inline-block;font:700 13px/1 'Source Sans 3',Arial;letter-spacing:2px;text-transform:uppercase;color:var(--tint);margin-bottom:8px}
.top{background:var(--ink);color:#fff;font:700 16px/1 'Source Sans 3',Arial;padding:12px 0;letter-spacing:.4px}
.top b{color:var(--yel)}
.hero{display:grid;grid-template-columns:1.15fr .85fr;gap:34px;padding:30px 18px 40px;align-items:start}
.tape{display:inline-block;background:var(--yel);font:900 22px/1.25 'Archivo Black','Arial Black',sans-serif;padding:10px 16px;transform:rotate(-1.2deg);box-shadow:4px 4px 0 rgba(0,0,0,.12);margin-bottom:16px;text-transform:uppercase}
.hero h1{font-size:40px;margin-bottom:14px}
.sup{font-size:20px}
.defn{background:var(--card);border-left:6px solid var(--tint);padding:14px 16px;margin:16px 0;font-size:19px}
.fromto{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0}
.fromto div{background:var(--card);border:2px solid var(--ink);border-radius:10px;padding:10px 12px;font-size:17px;line-height:1.4}
.fromto b{display:block;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--tint)}
.facts{font-weight:700;font-size:17px;margin:10px 0}
.price{display:flex;gap:14px;align-items:center;background:var(--card);border:3px solid var(--ink);border-radius:14px;padding:12px 16px;margin:12px 0}
.price .big{font:900 40px/1 'Archivo Black','Arial Black',sans-serif;color:var(--red)}
.price p{margin:0;font-size:17px;line-height:1.4}
.pop{display:inline-block;background:var(--yel);font:800 17px/1.2 'Source Sans 3',Arial;padding:7px 12px;border-radius:8px;transform:rotate(-2deg);margin:6px 0 -4px 10px;position:relative;z-index:1;box-shadow:2px 3px 0 rgba(0,0,0,.15)}
.btn{display:block;width:100%;text-align:center;background:var(--red);color:#fff;text-decoration:none;font:900 22px/1.25 'Archivo Black','Arial Black',sans-serif;padding:20px 18px;border-radius:14px;box-shadow:0 7px 0 #8E120C;margin:4px 0 10px}
.btn:hover{filter:brightness(1.06)}
.terms{font-size:15px;color:#4a453d;margin:0}
.heroimg img{width:100%;height:auto;border-radius:12px;box-shadow:0 22px 36px -16px rgba(0,0,0,.45);transform:rotate(1.2deg);display:block}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:10px}
.card{background:var(--card);border:2px solid rgba(28,26,23,.18);border-radius:12px;padding:16px}
.card p{font-size:17px;margin:0}
.card .k{font:900 26px/1 'Archivo Black','Arial Black',sans-serif;color:var(--tint);display:block;margin-bottom:6px}
.why .card{border-top:6px solid var(--tint)}
.why h3{font-size:19px}
.src{display:block;margin-top:10px;font-size:14px;font-style:italic;color:#4a453d}
.doc{display:grid;grid-template-columns:1.4fr .8fr;gap:18px;align-items:start}
.clause{background:#fff;border:1px solid #d8cfbf;box-shadow:0 10px 24px -14px rgba(0,0,0,.4);padding:22px;font-family:'Libre Caslon Text',Georgia,serif;font-size:17px;line-height:1.7}
.clause b{display:block;margin-bottom:8px}
.note{background:#FFF7C2;font:700 22px/1.25 'Caveat','Comic Sans MS',cursive;padding:16px;transform:rotate(2.5deg);box-shadow:0 8px 14px rgba(0,0,0,.15);color:#2a2a2a}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.grid4 div{background:var(--card);border:2px solid rgba(28,26,23,.16);border-radius:10px;padding:10px 12px;font-weight:700;font-size:16px;line-height:1.35}
.grid4 small{display:block;color:var(--tint);font-weight:800;letter-spacing:1px}
ol.steps,ul.ticks{list-style:none;margin:10px 0 0}
ol.steps{counter-reset:s}
ol.steps li,ul.ticks li{position:relative;padding:0 0 12px 46px;max-width:66ch}
ol.steps li:before{counter-increment:s;content:counter(s);position:absolute;left:0;top:0;width:32px;height:32px;border-radius:50%;background:var(--tint);color:#fff;font-weight:800;text-align:center;line-height:32px}
ul.ticks li:before{content:"✓";position:absolute;left:4px;top:0;color:var(--tint);font-weight:900;font-size:22px}
table{border-collapse:collapse;width:100%;background:var(--card);font-size:17px}
th,td{border:1px solid #d8cfbf;padding:10px;text-align:left;vertical-align:top}
th{background:#efe6d4}
td.us{background:#FFF4C4;font-weight:700}
.tbl{overflow-x:auto}
details{background:var(--card);border:2px solid rgba(28,26,23,.16);border-radius:10px;padding:12px 16px;margin-bottom:10px}
summary{font-weight:800;cursor:pointer}
details p{margin:8px 0 0}
.say{font:700 26px/1.35 'Caveat','Comic Sans MS',cursive;background:#fff;border:2px dashed var(--tint);border-radius:12px;padding:16px 20px;max-width:640px}
.close{background:#FFF4D6;text-align:left}
.close h2{font-size:34px}
.disc{font-size:14px;color:#5a5348;padding:26px 0 40px}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:9;background:rgba(28,26,23,.96);padding:10px 14px}
.sticky a{display:block;max-width:560px;margin:0 auto;text-align:center;background:var(--red);color:#fff;text-decoration:none;font:900 18px/1.2 'Archivo Black','Arial Black',sans-serif;padding:14px;border-radius:10px}
@media(max-width:820px){
 .hero{grid-template-columns:1fr;gap:18px}
 .heroimg{max-width:420px}.heroimg img{transform:none}
 .cards3,.doc{grid-template-columns:1fr}
 .grid4{grid-template-columns:1fr 1fr}
 .hero h1{font-size:31px}h2{font-size:26px}.close h2{font-size:28px}
 .tape{font-size:18px}
 table{font-size:14px}th,td{padding:6px 5px}
 .btn{font-size:19px;padding:18px 12px}
}
@media(max-width:380px){.fromto{grid-template-columns:1fr}.grid4{grid-template-columns:1fr}}
"""

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo+Black&family=Caveat:wght@700"
         "&family=Libre+Caslon+Text:wght@400;700&family=Source+Sans+3:wght@400;700;800;900&display=swap")


def e(s):
    return html.escape(s, quote=False)


def button(i, popup=None):
    pop = f'<span class="pop">{e(popup)}</span>' if popup else ""
    return (f'{pop}<a class="btn" href="{pay(i)}">{e(BTN)}</a>'
            f'<p class="terms">{PRICE} incl. GST · Refundable · Live online · {DATES}</p>')


def sec(n, title, body, cls=""):
    return (f'<section class="{cls}"><div class="wrap"><span class="num">{n:02d}</span>'
            f'<h2>{e(title)}</h2>{body}</div></section>')


def page(c, n):
    i = c["id"]
    a = ICPS[i]
    tint = TINTS[n]
    s = []
    k = 1
    # 1. First fold: the ad's words.
    fold = f"""<div class="wrap hero"><div>
<div class="tape">{e(a['banner'])}</div>
<h1>{e(a['hook'])}</h1>
<p class="sup">{e(a['support'])}</p>
<p class="defn"><b>What is contract drafting?</b> {e(DEFN)}</p>
<div class="fromto"><div><b>Now</b>{e(c['today'])}</div><div><b>In 21 days</b>{e(c['after'])}</div></div>
<p class="facts">LawSikho Contract Drafting Community · {DATES} · 9 live evening sessions · one document a day</p>
<div class="price"><span class="big">{PRICE}</span><p><b>Including GST. Refundable.</b><br>All 21 days, live online.</p></div>
{button(i, a['popup'])}
</div><div class="heroimg"><img src="img/cd_{i}.jpg" width="480" height="720" alt="{e(a['banner'].capitalize())}: Learn the art of contract drafting"></div></div>"""
    # 2. Symptom.
    s.append(sec(2, c["symptom_h2"], "".join(f"<p>{e(p)}</p>" for p in c["symptom"])))
    # 3. Outcome.
    s.append(sec(3, c["outcome_h2"], f"<p>{e(c['outcome'])}</p>{button(i)}"))
    # 4. Three alternatives.
    cards = "".join(f'<div class="card"><span class="k">{j}</span><h3>{e(x["t"])}</h3><p>{e(x["p"])}</p></div>'
                    for j, x in enumerate(c["alts"], 1))
    s.append(sec(4, c["alts_h2"], f'<div class="cards3">{cards}</div>'))
    # 5. Reframe.
    s.append(sec(5, c["reframe_h2"], f"<p>{e(c['reframe'])}</p>"))
    # 6. Why now, sources on the card face.
    order = WHY[n % 3:] + WHY[:n % 3]
    why = "".join(f'<div class="card"><h3>Did you know? {e(h)}</h3><p>{e(p)}</p><span class="src">Source: {e(src)}</span></div>'
                  for h, p, src in order)
    s.append(sec(6, "Why businesses are hiring contract drafters now", f'<div class="cards3 why">{why}</div>'))
    # 7. The reader's role.
    pts = "".join(f'<li><b>{e(x["t"])}.</b> {e(x["p"])}</li>' for x in c["role_points"])
    s.append(sec(7, c["role_h2"], f'<p>{e(c["role_intro"])}</p><ul class="ticks">{pts}</ul>'))
    # 8. The offer.
    offer = f"""<ul class="ticks">
<li><b>21 days, {DATES}.</b> One document a day, with a reading and a quiz on WhatsApp.</li>
<li><b>9 live evening sessions online.</b></li>
<li><b>16 business documents plus the parts of a contract</b>, from an NDA to a joint development agreement.</li>
<li><b>{PRICE} including GST, refundable.</b> One payment for all 21 days.</li></ul>{button(i)}"""
    s.append(sec(8, "What you get for ₹200 in the Contract Drafting Community", offer))
    # 9. Mechanism.
    mech = """<ol class="steps">
<li><b>Learn one document a day</b> from a short reading on your phone.</li>
<li><b>Practise it live</b> in the evening, using AI to find missing clauses and red flags.</li>
<li><b>Take it to the people who sign:</b> UK small businesses, startups, LinkedIn and your first article.</li></ol>"""
    s.append(sec(9, "How the 21 days work, in three steps", mech))
    # 10. First artifact.
    art = f"""<p>{e(c['artifact_intro'])}</p><div class="doc"><div class="clause"><b>{e(c['clause_title'])}</b>{e(c['clause'])}</div>
<div class="note">{e(c['margin_note'])}</div></div>"""
    s.append(sec(10, c["artifact_h2"], art))
    # 11. The work, day by day.
    grid = "".join(f"<div><small>{j:02d}</small>{e(d)}</div>" for j, d in enumerate(DOCS, 1))
    sess = "".join(f"<li>{e(x)}</li>" for x in SESSIONS)
    s.append(sec(11, "The documents you will draft, and the 9 live sessions",
                 f'<div class="grid4">{grid}</div><h3 style="margin-top:22px">The live evening sessions</h3>'
                 f'<ol class="steps">{sess}</ol>'))
    # 12. Plan after the camp.
    s.append(sec(12, c["plan_h2"], '<ol class="steps">' + "".join(f"<li>{e(x)}</li>" for x in c["plan"]) + "</ol>"))
    # 13. Implementation.
    impl = """<ul class="ticks">
<li><b>The day you join</b>, you are added to the WhatsApp group.</li>
<li><b>Each morning</b>, the day's reading and quiz arrive on your phone.</li>
<li><b>On session evenings</b>, you join live online with a laptop and a notebook.</li>
<li><b>Breaks</b> on 30 Oct, 6 Nov and 7 to 8 Nov for Diwali.</li></ul>"""
    s.append(sec(13, "What a normal day in the community looks like", impl))
    # 14. Cost comparison (time and output only).
    tbl = f"""<div class="tbl"><table><tr><th></th><th>Learning alone from samples</th><th>A long theory course</th><th>Contract Drafting Community</th></tr>
<tr><th>Time</th><td>Open-ended</td><td>Months</td><td class="us">21 days</td></tr>
<tr><th>What you produce</th><td>Copies of other people's drafts</td><td>Notes and exams</td><td class="us">Practice on 16 business documents</td></tr>
<tr><th>Live practice</th><td>None</td><td>Lectures</td><td class="us">9 live evening sessions</td></tr>
<tr><th>Reaching clients</th><td>Left to you</td><td>Rarely covered</td><td class="us">UK small businesses, startups, LinkedIn, a first article</td></tr>
<tr><th>Cost to you</th><td>Your time</td><td>A large fee</td><td class="us">{PRICE} incl. GST, refundable</td></tr></table></div>"""
    s.append(sec(14, "Three ways to learn drafting, side by side", tbl))
    # 15. Right room.
    s.append(sec(15, "You are in the right room if...",
                 '<ul class="ticks">' + "".join(f"<li>You {e(re.sub(r'^(you|You)\s+', '', x))}</li>" for x in c["room"]) + "</ul>"))
    # 16. Risk removed.
    risk = f"""<p>The fee is {PRICE} including GST, and it is refundable. You need no drafting experience on day one.</p>{button(i)}"""
    s.append(sec(16, "What you risk by joining: ₹200, and it is refundable", risk))
    # 17. FAQ.
    faq = c["faq"][:2] + [{"q": q, "a": a_} for q, a_ in SHARED_FAQ[1:2]]
    s.append(sec(17, "Questions people ask before they join",
                 "".join(f'<details{" open" if j == 0 else ""}><summary>{e(x["q"])}</summary><p>{e(x["a"])}</p></details>'
                         for j, x in enumerate(faq))))
    # 18. Buyer language.
    s.append(sec(18, "How to explain it at home in one line", f'<p class="say">"{e(c["buyer_line"])}"</p>'))
    # 19 to 20. Close.
    close = f"""<p>{e(c['close_lede'])}</p><p><b>21 days, {DATES}. 9 live evening sessions. {PRICE} including GST, refundable.</b></p>{button(i)}"""
    s.append(sec(19, c["close_h2"], close, "close"))
    body = "\n".join(s)
    disc = ("LawSikho runs this community to build practical drafting skills and show where the earning "
            "opportunities are. We do not promise any job, client or income. Sessions are live; recordings are not promised.")
    title = f"Contract Drafting Community for {a['banner'].title().replace('For ', '').replace('Llb', 'LLB').replace('Lpo', 'LPO').replace('Bpo', 'BPO').replace('Hr', 'HR')}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | LawSikho</title>
<meta name="description" content="{e(a['hook'])} {PRICE} incl. GST, refundable, 21 days live online.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="{FONTS}">
<style>{CSS.replace('TINT', tint)}</style></head><body>
<div class="sticky"><a href="{pay(i)}">{e(STICKY)}</a></div>
<div class="top"><div class="wrap"><b>LawSikho</b> · Contract Drafting Community · Learn the art of contract drafting</div></div>
{fold}
{body}
<div class="wrap disc"><p>{e(disc)}</p></div>
</body></html>"""


def words(htm):
    t = re.sub(r"<(style|script)\b.*?</\1>", " ", htm, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return len(re.findall(r"[A-Za-z₹0-9][\w'₹.,-]*", t))


if __name__ == "__main__":
    copy = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    for n, c in enumerate(sorted(copy, key=lambda x: x["id"])):
        i = c["id"]
        im = Image.open(os.path.join(ADS, f"CD_torn_{i}.jpg")).convert("RGB").resize((480, 720), Image.LANCZOS)
        im.save(os.path.join(out, "img", f"cd_{i}.jpg"), quality=74, optimize=True, progressive=True)
        h = page(c, n)
        open(os.path.join(out, f"lp_cd_{i}.html"), "w", encoding="utf-8").write(h)
        print(i, words(h), "words", len(h.encode()) // 1024, "KB")
