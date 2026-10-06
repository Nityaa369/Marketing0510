# Builds the four NCA landing pages, one per ad in this kit, on Ruchika's 21-step order.
# Run: python3 build_lps.py   (writes landing_pages/lp_<ad stem>.html)
# Facts: docs/NCA_WEB_RESEARCH_2026-10-06.md and the April 2024 script summary in the starter kit.
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "landing_pages")
PAY = "#PAYMENT_LINK_PENDING"  # BLOCKER: replace with the real GrowthX funnel URL per page and test-buy in a browser

CAMP = dict(
    dates="Saturday 31 October, Sunday 1 November and Monday 2 November 2026",
    times="2 to 5 PM IST on Saturday and Sunday, 7 to 10 PM IST on Monday",
    price="Rs 10, including GST, refundable anytime",
)

CSS = """*{box-sizing:border-box;margin:0;padding:0}
:root{--ac:%(ac)s;--soft:%(soft)s;--ink:#17140F;--mut:#4A443B;--bg:#FBF9F4}
body{font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;font-size:18px}
.wrap{max-width:760px;margin:0 auto;padding:0 20px}
header.hero{background:var(--soft);padding:34px 0 30px;border-bottom:6px solid var(--ac)}
.brand{font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--ac)}
.qual{font-size:13px;font-weight:800;letter-spacing:.1em;color:var(--ac);margin-top:14px}
h1{font-size:36px;line-height:1.15;margin-top:10px;letter-spacing:-.01em}
h1 em{font-style:italic;color:var(--ac)}
.offer{font-size:21px;font-weight:700;margin-top:14px}
.def{margin-top:12px;color:var(--mut)}
.del{margin:16px 0 0;padding:0;list-style:none}
.del li{padding:6px 0 6px 30px;position:relative;font-weight:600}
.del li:before{content:'\\2713';position:absolute;left:0;color:var(--ac);font-weight:900}
.terms{margin-top:16px;background:#fff;border:2px solid var(--ac);border-radius:10px;padding:12px 16px;font-weight:700}
.btn{display:block;text-align:center;background:var(--ac);color:#fff;font-weight:900;font-size:20px;padding:16px;border-radius:12px;text-decoration:none;margin-top:18px}
section{padding:30px 0;border-bottom:1px solid #E6E0D4}
.n{font-size:12px;font-weight:900;letter-spacing:.14em;color:var(--ac);text-transform:uppercase}
h2{font-size:26px;line-height:1.25;margin:6px 0 12px}
p+p{margin-top:12px}
.box{background:#fff;border-left:6px solid var(--ac);padding:14px 18px;margin-top:14px;border-radius:6px}
.steps{counter-reset:s;list-style:none;margin-top:12px}
.steps li{counter-increment:s;padding:12px 0 12px 52px;position:relative;border-top:1px solid #E6E0D4}
.steps li:before{content:counter(s);position:absolute;left:0;top:10px;width:36px;height:36px;border-radius:50%%;background:var(--ac);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}
table{width:100%%;border-collapse:collapse;margin-top:12px;font-size:16px;background:#fff}
td,th{border:1px solid #E0D9CC;padding:10px;text-align:left;vertical-align:top}
th{background:var(--soft)}
.src{font-size:13px;color:var(--mut);margin-top:8px}
.quote{font-size:21px;font-weight:700;background:var(--soft);padding:16px 18px;border-radius:10px;margin-top:12px}
.close{background:var(--soft);padding:34px 0;border:0}
.disc{font-size:13px;color:var(--mut);padding:26px 0 110px}
.disc p+p{margin-top:8px}
.sticky{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:3px solid var(--ac);padding:10px 16px;display:flex;gap:12px;align-items:center;justify-content:center;z-index:9}
.sticky span{font-weight:800;font-size:15px}
.sticky a{background:var(--ac);color:#fff;font-weight:900;padding:12px 20px;border-radius:10px;text-decoration:none;white-space:nowrap}
@media(max-width:520px){h1{font-size:29px}h2{font-size:23px}.sticky span{display:none}}
"""

FACTS_SRC = ('<p class="src">Sources: IMF World Economic Outlook, October 2025 (via statisticstimes.com); '
             'IRCC 2026 to 2028 Immigration Levels Plan (canada.ca); IRCC permanent resident data for 2024 '
             '(via immigration.ca); Federation of Law Societies of Canada, nca.legal.</p>')

DISCLAIMER = """<div class="disc wrap">
<p><b>Please read.</b> LawSikho is an independent education company. It is not part of, and is not endorsed by, the National
Committee on Accreditation, the Federation of Law Societies of Canada, the Law Society of Ontario or any other Canadian law society
or government body. Their requirements, fees and timelines are set by them, change from time to time, and should be confirmed on their
own websites before you apply.</p>
<p>The bootcamp teaches the route and a plan. It does not guarantee an NCA assessment result, exam results, a Certificate of
Qualification, a licence to practise, a job, clients, a visa or immigration status. Learner stories describe individual experiences and
are not typical results. Wage and economic figures are published market data, labelled with their source, and are not a promise of
earnings. Nothing on this page is legal or immigration advice. Sample documents shown are illustrations for teaching.</p>
<p>Live online sessions only; there are no recordings. Price Rs 10, including GST, refundable anytime on request.</p></div>"""


def sec(n, title, body):
    return '<section><!-- %s --><div class="wrap"><h2>%s</h2>%s</div></section>' % (n, title, body)


def page(p):
    s = p["s"]
    parts = []
    # 1 to 3 live in the first fold
    parts.append("""<header class="hero"><div class="wrap">
<div class="brand">LawSikho · Canada law bootcamp</div>
<div class="qual">%(qual)s</div>
<h1>%(h1)s</h1>
<p class="offer">%(offer)s</p>
<p class="def"><b>NCA</b> means the National Committee on Accreditation: the body that checks your Indian law degree for Canada and tells you which exams to clear. You write those exams online, from India.</p>
<ul class="del"><li>The NCA exams and how to prepare for them from India</li><li>The bar licensing step that comes after</li><li>Your own 12-month plan, written with you</li></ul>
<div class="terms">%(dates)s<br>%(times)s<br>Live only, no recordings. %(price)s.</div>
<a class="btn" href="%(pay)s">Join the Rs 10 bootcamp</a>
<p class="def" style="margin-top:16px">%(s1)s</p>
</div></header>""" % dict(p, **CAMP, pay=PAY, s1=s[1]))
    titles = p["t"]
    for i in range(2, 21):
        parts.append(sec("Step %d" % i, titles[i], s[i]))
    parts.append("""<section class="close"><!-- Step 21 --><div class="wrap"><h2>%s</h2>%s
<a class="btn" href="%s">Join the Rs 10 bootcamp</a></div></section>""" % (titles[21], s[21], PAY))
    html = """<!doctype html>
<!-- /f/%(slug)s · pairs with ad %(stem)s · BLOCKER: pay links are placeholders until the GrowthX funnel exists -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title><style>%(css)s</style></head><body>
%(body)s
%(disc)s
<div class="sticky"><span>NCA and Canadian bar bootcamp · Rs 10 incl. GST · refundable</span><a href="%(pay)s">Join the Rs 10 bootcamp</a></div>
</body></html>""" % dict(p, css=CSS % p, body="\n".join(parts), disc=DISCLAIMER, pay=PAY)
    return html


# The shared "why Canada" box, written differently per page so pages do not repeat each other.
def why(lead):
    return ('<div class="box"><p>%s</p><ul class="del">'
            '<li>Canada is a G7 member and the world\'s 10th largest economy, about USD 2.28 trillion in 2025.</li>'
            '<li>It plans to welcome 380,000 new permanent residents a year from 2026 to 2028, 64%% of them in economic programs.</li>'
            '<li>India was the largest source of new permanent residents in 2024: 127,320 people.</li>'
            '<li>Canada is a common-law country, like India. The NCA has a set route for Indian law degrees.</li></ul>%s</div>'
            % (lead, FACTS_SRC))

COST_TABLE = """<table><tr><th>Route</th><th>What it costs</th><th>What it needs from you</th></tr>
<tr><td>A Canadian law degree</td><td>Tuition of about CAD 35,000 to 56,000 a year (NCA's own figure)</td><td>Moving first, years of study, pausing your work</td></tr>
<tr><td>The NCA exams, from India</td><td>About CAD 400 to assess your degree and CAD 500 per exam; NCA puts the minimum near CAD 3,000 plus taxes</td><td>Study alongside your work; exams are held every month</td></tr>
<tr><td>This bootcamp</td><td>Rs 10, including GST, refundable anytime</td><td>Three live sessions, 9 hours in all</td></tr></table>
<p class="src">Source: nca.legal/costs-and-timelines. Fees are set by the NCA and can change.</p>"""

IMPL = """<ul class="del"><li><b>When:</b> %(dates)s.</li><li><b>Time:</b> %(times)s. Day 3 runs in the evening.</li>
<li><b>Where:</b> live online. There are no recordings, so block the three slots now.</li>
<li><b>Price:</b> %(price)s.</li><li><b>Bring:</b> your LLB mark sheets, a notebook, and one question you have never had answered.</li>
<li><b>Led by:</b> Abhishek Pareek, who runs LawSikho's NCA programme.</li></ul>""" % CAMP

PAGES = [
dict(stem="nca_s_01_editorial_5plus_years", slug="nca-oct-s01-experienced", ac="#1F3B5C", soft="#E9EEF5",
     title="Canadian qualification without pausing your practice",
     qual="ADVOCATES · LITIGATORS · IN-HOUSE COUNSEL · 5+ YEARS OF PRACTICE",
     h1="Practising law for 5 years or more? <em>Start your Canadian qualification without pausing your practice.</em>",
     offer="In 3 live days, we show you how to clear Canada's NCA exams from India and what the bar licensing step asks of you. You leave with a 12-month plan that fits around your practice.",
     t={2:"You are good at your work. Canada still feels like a door for someone younger",
        3:"What you actually want: your experience to count in Canada too",
        4:"Failed alternative 1: waiting until the practice is quieter",
        5:"Failed alternative 2: the Canadian LLM, or a law degree from scratch",
        6:"Failed alternative 3: moving first and hoping law follows",
        7:"The problem is not effort. It is positioning",
        8:"What another year of 'someday' costs an experienced lawyer",
        9:"The offer: a 3-day live bootcamp for experienced Indian advocates",
        10:"How the route works, in 3 steps",
        11:"What you leave Day 1 holding",
        12:"Where this takes a senior practice over the next few years",
        13:"Proof: an in-house lawyer who moved with the plan",
        14:"Proof: a Ludhiana practice with clients abroad",
        15:"The work, not a pep talk",
        16:"The details",
        17:"What the alternatives cost, side by side",
        18:"The risk is Rs 10, and even that comes back if you ask",
        19:"What to tell your family, or your partners at the firm",
        20:"Your next step",
        21:"You have built a practice in India. This adds Canada to it"},
     s={1:"If you have been at the bar for five years or longer, this page is written for you: the advocate whose skills are proven and whose name already means something in one city.",
        2:"<p>You run matters on your own. Juniors bring you their drafts. Clients call you by name. And yet, every time a colleague's child lands in Toronto or a client asks about Canada, a quiet thought returns: that route was for people who started early.</p><p>You have probably looked it up once or twice. The pages were full of acronyms, fees in Canadian dollars and advice written for students. Nothing spoke to a lawyer with a running practice.</p>",
        3:"<p>You do not want to start over. You want the years you have already put in to be recognised in a second country, so that your next decade has two markets instead of one.</p><p>Put simply: to be a lawyer who is qualified in India and on the route to practise in Canada, without closing the office to get there.</p>",
        4:"<p>Most experienced advocates plan to look at Canada once the current matters settle. Matters do not settle. A good practice gets busier, not lighter, and the plan moves to next year again.</p><p>The NCA route was built for people who keep working. Waiting for free time treats it like a full-time course, which it is not.</p>",
        5:"<p>The second instinct is a Canadian LLM or a full law degree. It feels safe because it is familiar. But it usually means moving, pausing your income and spending lakhs before you know what Canada will actually ask of you.</p><p>For most Indian LLB holders, the NCA assesses the degree you already have and tells you exactly which exams to clear. The degree can come later, if at all.</p>",
        6:"<p>The third path is moving on a work permit or permanent residence first and sorting out law later. Many skilled lawyers who do this end up working outside law for years, because they arrive with no Canadian track record and no plan for licensing.</p><p>Moving is the last step, not the first.</p>",
        7:"<p>You already work harder than most people reading this page. Effort is not what stands between you and Canada.</p><p>What stands between you is how you are positioned: as a lawyer whose qualification is recognised in one country. The NCA's Certificate of Qualification repositions the same degree and the same experience as recognised in Canada too. That is a paperwork and exam problem, and paperwork and exam problems have a route.</p>",
        8:"<p>The cost of staying unclear is not dramatic. It is quiet. It is one more year where your experience counts in one market only, and one more year of looking at the route instead of walking it.</p><p>The NCA gives you five years to finish once your assessment comes back. The clock only starts when you do.</p>",
        9:"<p>A 3-day live bootcamp, run by LawSikho, for Indian lawyers who want to practise in Canada. You spend 9 hours with us across a weekend and one evening.</p><p>By the end, you know what the NCA will likely assign you, how to prepare for those exams around your practice, what the bar licensing step asks of you, and your own 12-month plan.</p>"
          + why("Why Canada, and why now, for a lawyer with your experience:"),
        10:"<ol class='steps'><li><b>Clear the NCA exams from India.</b> The NCA assesses your Indian LLB and usually assigns core subjects such as Canadian constitutional, administrative and criminal law, and professional responsibility. The exams are online, open book and proctored, so you sit them from home.</li><li><b>Take Canadian legal work from India while you prepare.</b> Contracts valid in Canada, privacy policies for Canadian startups and research support for Canadian lawyers can be found on LinkedIn, Upwork and law-society directories. This builds a Canadian track record before you move.</li><li><b>Pass the bar licensing, then practise.</b> In Ontario that means the Law Society's licensing exams plus articling or the Law Practice Program. Then you practise in Canada, or bill Canadian clients as a Canada-qualified lawyer.</li></ol>",
        11:"<p>On Day 1 you see the types of question the NCA asks and how to answer them in the IRAC format: issue, rule, application, conclusion. You write an answer yourself, live.</p><p>You leave with a list of the subjects you are most likely to be assigned and where your Indian practice already gives you a head start.</p>",
        12:"<p>Over the next few years, the change is a second jurisdiction on your name. Your current clients still see an Indian advocate. New clients, from Canada or with Canadian business, see a lawyer qualified for both.</p><div class='box'><p><b>Market data, not a promise:</b> Canada's Job Bank reports a median wage of CAD 65.21 an hour for lawyers in Ontario, where about 54,600 people work in the occupation, with a moderate outlook for 2025 to 2027.</p><p class='src'>Source: jobbank.gc.ca, NOC 41101, Ontario.</p></div>",
        13:"<p>Hezal Shah was an in-house lawyer in Mumbai. In our bootcamp's own account, Hezal followed the qualify-first route and moved to Vancouver.</p><p>The point is the order: qualification and plan first, the move after.</p>",
        14:"<p>Shashwat Jindal practises from Ludhiana, not a metro. As our bootcamp tells it, that practice took on work for four US firms, a Canadian firm and five startups, all from India.</p><p>A city outside the metros was not the obstacle. Not having a route was.</p>",
        15:"<ul class='del'><li>Day 1: NCA question types, and an IRAC answer you write live</li><li>Day 2: the 12-month plan, and finding Canadian work on Upwork and LinkedIn; a Canadian employment agreement, reviewed</li><li>Day 3: a non-compete clause reviewed under Canadian law, the top 20 questions a CEO asks before expanding into Canada, incorporating a Canadian company, and a privacy policy for a Canadian founder</li></ul><p>Each of these is a piece of Canadian legal work you can show a client or employer.</p>",
        16:IMPL,
        17:COST_TABLE,
        18:"<p>You pay Rs 10, including GST. If you decide it was not worth it, ask for a refund, at any time. You risk three slots in your calendar, and you keep everything you write in them.</p>",
        19:"<p>When someone asks what you are doing, here is the sentence:</p><p class='quote'>\"I am getting my Indian law practice recognised in Canada, from here, without closing the office.\"</p><p>You are in the right room if you have practised for five years or more and would rather add a market than start over. You want a plan you can follow around real work.</p>",
        20:"<p>Press the button, pay Rs 10, and you will get the joining details on WhatsApp and email. Then block Saturday and Sunday from 2 to 5 PM, and Monday from 7 to 10 PM.</p>",
        21:"<p>Experienced advocates already have the hard part: years of real practice. The bootcamp shows you how to have that experience recognised in Canada, one step at a time, while your practice keeps running.</p>"}),

dict(stem="nca_s_02_eligibility_check", slug="nca-oct-s02-eligibility", ac="#1E6A48", soft="#E6F1EA",
     title="Are you eligible to practise law in Canada?",
     qual="LLB HOLDERS · ADVOCATES · ASSOCIATES · IN-HOUSE · ANY PRACTICE AREA",
     h1="Want to practise law in Canada? <em>Check if you are eligible to apply.</em>",
     offer="In 3 live days, we show you whether your Indian LLB is eligible to apply to the NCA, and what the 2026 rules ask of every applicant. Then we show you how to clear the NCA exams from India, and the bar licensing step after.",
     t={2:"You have searched 'how to practise law in Canada' more than once",
        3:"What you want is a yes or no, and then a route",
        4:"Failed alternative 1: piecing it together from forums",
        5:"Failed alternative 2: asking an immigration consultant about licensing",
        6:"Failed alternative 3: assuming you need a Canadian degree first",
        7:"The problem is not your degree. It is how you are positioned",
        8:"What staying unsure costs you",
        9:"The offer: a 3-day eligibility-to-licence bootcamp",
        10:"The route, in 3 steps",
        11:"The first thing you take away: your eligibility checklist",
        12:"What changes once you are on the route",
        13:"Proof: from the NCA exams to the Ontario courts",
        14:"Proof: a litigator who moved with a job in hand",
        15:"The work, laid out",
        16:"The details",
        17:"The cost of each way in",
        18:"Remove the risk",
        19:"The sentence you can repeat",
        20:"Your next step",
        21:"If you want to practise law in Canada, start with where you stand"},
     s={1:"If you hold an Indian LLB and want to practise law in Canada, this page is for you. It answers the first question everyone has, and few get a straight answer to: can I apply?",
        2:"<p>You have read three blogs, two forum threads and a video, and each said something slightly different. One mentioned five exams, another seven. One said you need a Canadian LLM. None said what changed this year.</p><p>The result is a tab you keep open and never act on.</p>",
        3:"<p>You want two things. First, a clear answer: is my degree eligible to apply? Second, if yes, the exact route from where you are today to practising law in Canada.</p>",
        4:"<p>Forums are generous but scattered. Advice from 2019 sits next to advice from last week, and the rules have moved since. In 2026 alone, every NCA applicant now needs an English test and an Indigenous law course.</p><p>You can spend months reading and still not know which advice applies to your degree.</p>",
        5:"<p>Immigration consultants know visas. Licensing to practise law is a different system, run by the NCA and the provincial law societies. A visa can take you to Canada. It does not make you a lawyer there.</p>",
        6:"<p>Many lawyers assume a Canadian degree is the only way. For an Indian LLB from a recognised university, the NCA usually assesses the degree you already hold and assigns a set of exams instead. A full Canadian degree costs far more and asks you to move first.</p>",
        7:"<p>You are not missing ability, and you are not missing effort. Your Indian LLB is already common-law training.</p><p>What you are missing is positioning. Today your degree is recognised in India. The NCA process repositions the same degree as recognised in Canada. Eligibility is the first box on that route.</p>",
        8:"<p>Staying unsure has a real cost, even if it is a quiet one. Each month you spend not knowing is a month you could have been preparing. And because the rules change, as they did on 1 March 2026, last year's research may already be out of date.</p>",
        9:"<p>A 3-day live bootcamp by LawSikho. We start where you are: is your degree eligible to apply? Then we walk the whole route with you, to practising law in Canada.</p>"
          + why("Why so many Indian lawyers are looking at Canada:"),
        10:"<ol class='steps'><li><b>Apply to the NCA and clear its exams.</b> Your degree is assessed, and you are told which subjects to clear. Since 1 March 2026, every applicant also takes an English test and an Indigenous law course. The exams are online, so you write them from India.</li><li><b>Get the Certificate of Qualification.</b> Once you pass, the NCA issues it. It puts you level with a Canadian common-law graduate for licensing.</li><li><b>Pass the bar licensing, then practise.</b> Each province runs its own licensing. In Ontario that is the Law Society's licensing exams plus articling or the Law Practice Program.</li></ol>",
        11:"<p>You leave with a filled-in checklist for your own profile:</p><ul class='del'><li>Is my LLB from a recognised university? Is it a 3-year or 5-year degree?</li><li>Which English test do I need, or is my existing test score recent enough?</li><li>Which NCA subjects am I likely to be assigned?</li><li>Which province, and which licensing path, fits my plan?</li></ul>",
        12:"<p>Once you are on the route, the question changes from 'can I?' to 'which month do I sit my next exam?'. NCA exams are held every month. The NCA puts the best case at about 10 months and the average at about two years.</p><p>You also stop being one more lawyer hoping to move, and become a lawyer with a dated plan.</p>",
        13:"<p>Navkaran Singh is an Indian law graduate. In our bootcamp's own account, Navkaran cleared the NCA exams and went on to work in the Ontario courts.</p><p>The route Navkaran used is the same three steps on this page.</p>",
        14:"<p>Yashika Malhotra was a litigator in India. As our bootcamp tells it, Yashika moved to Canada with a Canadian job already in hand, rather than moving first and searching after.</p>",
        15:"<ul class='del'><li>Day 1: how the NCA assesses an Indian LLB, the question types, and an IRAC answer you write live</li><li>Day 2: your 12-month plan, the 2026 English test and Indigenous law course, and finding Canadian legal work from India</li><li>Day 3: the bar licensing step, and Canadian legal documents reviewed live, including a non-compete clause and a startup privacy policy</li></ul>",
        16:IMPL,
        17:COST_TABLE,
        18:"<p>Rs 10, including GST. Refundable anytime if you ask. If the checklist tells you the route is not right for you yet, you have spent Rs 10 to know that for certain, and you can still ask for it back.</p>",
        19:"<p class='quote'>\"I checked my eligibility for Canada, and I have a route and a plan to practise law there.\"</p><p>You are in the right room if you hold an Indian LLB, you are serious about practising law in Canada, and you want facts that are current to 2026.</p>",
        20:"<p>Press the button and pay Rs 10. Joining details reach you on WhatsApp and email. Keep your mark sheets handy for Day 1.</p>",
        21:"<p>Indian lawyers who want to practise in Canada usually stop at the first question. This bootcamp answers it for your degree, then shows you every step after it.</p>"}),

dict(stem="nca_s_03_planner_newly_enrolled", slug="nca-oct-s03-newly-enrolled", ac="#9E2328", soft="#F6E9E6",
     title="Prepare for the NCA exams in 2 hours a day",
     qual="NEWLY ENROLLED ADVOCATES · JUNIOR ASSOCIATES · RECENT LLB GRADUATES",
     h1="Newly enrolled advocate? <em>Prepare for Canada's NCA exams in 2 hours a day.</em>",
     offer="In 3 live days, we show you how to fit NCA exam preparation into about 2 hours a day around court. You also see what comes after the exams, and build the 12-month plan that takes your career international.",
     t={2:"You just got your enrolment. The career ahead already looks narrow",
        3:"What you want: an international career that starts now, not someday",
        4:"Failed alternative 1: waiting until you are more senior",
        5:"Failed alternative 2: saving up for a foreign LLM",
        6:"Failed alternative 3: studying the NCA alone, at night, with no plan",
        7:"The problem is not hours. It is positioning",
        8:"What waiting costs a new advocate",
        9:"The offer: a 3-day live bootcamp for advocates early in their career",
        10:"How 2 hours a day turns into a Canadian qualification",
        11:"What you leave holding: your weekly timetable",
        12:"Where you are in a few years",
        13:"Proof: a legal assistant at a Canadian firm, working from India",
        14:"Proof: moving with a job already lined up",
        15:"What the 3 days actually cover",
        16:"The details",
        17:"Compare the ways in",
        18:"No risk to try it",
        19:"How to explain it to your senior",
        20:"Your next step",
        21:"New advocates have the one thing seniors cannot buy: time"},
     s={1:"If you enrolled recently, or you are in your first years of practice, this is for you. You work long days under a senior and wonder whether the career can be bigger than one courtroom.",
        2:"<p>The day starts at court and ends with drafts for your senior. The pay is modest. The work is real, but it is the same few kinds of matter, in the same few courts.</p><p>Meanwhile, friends from law school post from Toronto, London and Dubai. You are not sure how they got there, and you are not sure the route is open to someone who just enrolled.</p><p>You did not study law for five years to have your options set in your first year.</p>",
        3:"<p>You want an international career, and you want it to start now, while you are still early enough to shape it. A qualification that travels, built in the hours you already have.</p>",
        4:"<p>Many juniors tell themselves they will look at foreign qualifications once they are senior. But seniority in India builds a practice in India. It does not add a second country to your name.</p><p>The early years, when evenings are still yours, are the easiest time to start.</p>",
        5:"<p>A foreign LLM sounds like the ticket abroad. It usually costs lakhs, means leaving your enrolment behind for a year or more, and still does not license you to practise in Canada on its own.</p>",
        6:"<p>Some juniors download NCA material and study at night with no structure. Without knowing which subjects the NCA will assign, which rules changed in 2026 and what comes after the exams, motivation fades within weeks.</p>",
        7:"<p>You do not need more hours. You already have about 2 a day, after court. What you need is positioning: a plan that turns those hours into a Canadian qualification instead of scattered reading.</p><p>The NCA route rewards steady preparation. That is exactly what a junior's evening can give it.</p>",
        8:"<p>Waiting costs you the cheapest years to start. Every year you wait, your evenings fill up and the route looks bigger. Starting now means your Canadian qualification grows alongside your Indian career, not after it.</p>",
        9:"<p>A 3-day live bootcamp by LawSikho, built so a working junior can attend: two afternoons and one evening, 9 hours in all.</p>"
          + why("Why Canada is worth your evenings:"),
        10:"<ol class='steps'><li><b>About 2 hours a day on the NCA exams.</b> Our bootcamp's plan is roughly six months of preparation at 2 hours a day for the core NCA subjects. You write the exams online, from India.</li><li><b>Small pieces of Canadian work while you prepare.</b> Research, drafting support or document review for Canadian lawyers and startups, found on LinkedIn and Upwork. It builds a Canadian record.</li><li><b>Bar licensing, then practise in Canada.</b> With your Certificate of Qualification, you move to the provincial licensing step, such as Ontario's licensing exams plus articling or the Law Practice Program.</li></ol>",
        11:"<p>You leave Day 2 with a weekly timetable that fits around court: which NCA subject in which week, how many hours a day, and when to book your first exam.</p><p>You also write one IRAC answer live on Day 1, so you know how the exams feel before you spend a rupee on them.</p>",
        12:"<p>In a few years, you are not just a few years more senior. You are an Indian advocate on the route to, or holding, a Canadian qualification, with a record of Canadian work. That is a different starting point for any job, client or move.</p>",
        13:"<p>Harshmir Swaitch worked as a legal assistant at a Canadian firm, on NRI and immigration matters, while preparing. That is how our bootcamp tells it.</p><p>Canadian work did not wait for the move. It started from India.</p>",
        14:"<p>Yashika Malhotra, a litigator, moved to Canada with a Canadian job already lined up, according to our bootcamp's account. The plan came first; the flight came last.</p>",
        15:"<ul class='del'><li>Day 1: how the NCA works for an Indian LLB, the question types, and an IRAC answer you write</li><li>Day 2: the 12-month plan and your weekly timetable; how to find Canadian work on Upwork and LinkedIn; a Canadian employment agreement</li><li>Day 3: Canadian documents reviewed live, the bar licensing step, and what happens after the Certificate of Qualification</li></ul>",
        16:IMPL,
        17:COST_TABLE,
        18:"<p>Rs 10, including GST, and refundable anytime. Sessions run on a Saturday and Sunday afternoon and a Monday evening, so you do not miss court.</p>",
        19:"<p class='quote'>\"I am using my evenings to prepare for Canada's NCA exams, so my practice can go international.\"</p><p>You are in the right room if you are early in your career, you have about 2 hours a day, and you want your next few years to add a country, not just seniority.</p>",
        20:"<p>Press the button and pay Rs 10. You get the joining link on WhatsApp and email. Block the three slots now; there are no recordings.</p>",
        21:"<p>Newly enrolled advocates who want an international career already have the evenings it needs. The bootcamp turns those 2 hours a day into a route to practise law in Canada.</p>"}),

dict(stem="nca_s_04_redline_contract_lawyers", slug="nca-oct-s04-contract-lawyers", ac="#0E5A6C", soft="#E3EEF2",
     title="You already draft under common law. Qualify in Canada",
     qual="CORPORATE LAWYERS · CONTRACT DRAFTERS · M&A · IN-HOUSE COUNSEL",
     h1="Corporate or contract lawyer? <em>You already draft under common law. Qualify to practise it in Canada.</em>",
     offer="In 3 live days, we show you how your drafting carries into Canadian law and how to clear the NCA exams from India. You also see how to take Canadian contract work while you prepare, and the bar licensing step after.",
     t={2:"You draft agreements every week. Most of them never leave India",
        3:"What you want: the same drafting, for clients in a bigger market",
        4:"Failed alternative 1: hoping the firm sends you abroad",
        5:"Failed alternative 2: an LLM to 'go international'",
        6:"Failed alternative 3: freelancing on platforms with no qualification behind you",
        7:"The problem is not skill. It is positioning",
        8:"What staying in one jurisdiction costs a drafter",
        9:"The offer: a 3-day live bootcamp for corporate and contract lawyers",
        10:"The 3-step route for a drafter",
        11:"The first artifact: a Canadian clause, reviewed",
        12:"The longer-term change",
        13:"Proof: a practice outside the metros, drafting for clients abroad",
        14:"Proof: an in-house lawyer, Mumbai to Vancouver",
        15:"The documents you work on",
        16:"The details",
        17:"What each route costs",
        18:"The risk, removed",
        19:"How to say it to your firm",
        20:"Your next step",
        21:"Corporate lawyers already have the skill Canada uses every day"},
     s={1:"If you draft, review or negotiate contracts for a living, at a firm, in-house or in your own practice, this page is for you.",
        2:"<p>Shareholders' agreements, service contracts, NDAs, employment terms. You know which clause the other side will push on before they do. And almost every one of those documents is governed by Indian law and signed by Indian clients.</p><p>You have probably noticed how many of your clients now sell abroad, raise money from abroad, or hire people abroad. The contracts follow them. Often the foreign side is drafted by someone else, because nobody on the Indian side is qualified to advise on it.</p>",
        3:"<p>You want to use the same skill for a bigger market: Canadian startups, Canadian companies expanding abroad and Indian companies entering Canada, as a lawyer qualified to advise them.</p>",
        4:"<p>Many associates wait for a cross-border mandate or a secondment. Those come to a few, and they come late. They also leave your qualification exactly where it was.</p>",
        5:"<p>An LLM abroad feels like the international move. It costs lakhs, pauses your work, and on its own still does not license you to practise in Canada.</p><p>For a drafter with clients and a track record, stepping away for a year also means handing those clients to someone else.</p>",
        6:"<p>Some drafters try selling contract work on global platforms. Without a recognised qualification, you compete on price with every other unqualified drafter, and serious clients look elsewhere.</p>",
        7:"<p>Your drafting is not the gap. Canada, like India, is a common-law country, so the way you read and build a contract already transfers. Some rules differ, and that is what the exams test.</p><p>The gap is positioning: you are seen as an Indian-law drafter. The NCA's Certificate of Qualification, then bar licensing, repositions you as a lawyer Canadian clients can instruct.</p>",
        8:"<p>Staying in one jurisdiction caps who can instruct you. Every year the skill grows, but the market it is allowed to serve stays the same size.</p><p>It also caps the matters you see. The more interesting cross-border work, where a Canadian entity sits on one side of the table, goes to whoever is qualified on that side. A drafter qualified in both countries can sit on either side.</p>",
        9:"<p>A 3-day live bootcamp by LawSikho, with live review of Canadian documents, for lawyers who draft for a living.</p>"
          + why("Why Canada is a strong market for a drafter's skill:"),
        10:"<ol class='steps'><li><b>Clear the NCA exams from India.</b> The NCA assesses your LLB and assigns subjects. The exams are online and open book, and you write them alongside your work.</li><li><b>Take Canadian contract work while you prepare.</b> Contracts valid in Canada, privacy policies for Canadian startups and incorporation support, found on LinkedIn, Upwork and law-society directories.</li><li><b>Bar licensing, then practise.</b> With your Certificate of Qualification you take your province's licensing step, then advise Canadian clients as a qualified lawyer.</li></ol>",
        11:"<p>On Day 3 you review a non-compete clause under Canadian law, live. You see where an Indian-trained drafter's instinct is right, and where Canadian courts read the clause differently.</p><p>You keep your marked-up version.</p>",
        12:"<p>Over time, your client list stops ending at the border. You draft for Indian companies entering Canada and for Canadian businesses, and your name carries a Canadian qualification.</p><p>Inside a firm or a legal team, that makes you the person who can take the Canadian side of a deal. In your own practice, it lets you offer Canadian clients the same careful drafting you already offer Indian ones, as a qualified lawyer rather than a vendor.</p><div class='box'><p><b>Market data, not a promise:</b> Canada's Job Bank reports a median wage of CAD 65.21 an hour for lawyers in Ontario, with a moderate outlook for 2025 to 2027.</p><p class='src'>Source: jobbank.gc.ca, NOC 41101, Ontario.</p></div>",
        13:"<p>Shashwat Jindal practises from Ludhiana. In our bootcamp's own account, that practice took on work for four US firms, a Canadian firm and five startups, without moving.</p>",
        14:"<p>Hezal Shah was an in-house lawyer in Mumbai and, as our bootcamp tells it, moved to Vancouver after taking the qualify-first route.</p>",
        15:"<ul class='del'><li>A Canadian employment agreement, reviewed (Day 2)</li><li>A non-compete clause under Canadian law (Day 3)</li><li>The top 20 questions a CEO asks before expanding into Canada (Day 3)</li><li>Incorporating a Canadian company, step by step (Day 3)</li><li>A privacy policy for a Canadian startup founder (Day 3)</li><li>NCA question types and an IRAC answer you write (Day 1)</li></ul>",
        16:IMPL,
        17:COST_TABLE,
        18:"<p>Rs 10, including GST, refundable anytime. You keep the documents you mark up during the sessions either way.</p><p>The sessions sit on a Saturday and Sunday afternoon and a Monday evening, so they do not collide with a working week of closings and calls.</p>",
        19:"<p class='quote'>\"I am qualifying in Canada so I can draft for Canadian clients, not just Indian ones.\"</p><p>You are in the right room if contracts are your daily work and you want that work to reach a second common-law market.</p>",
        20:"<p>Press the button and pay Rs 10. The joining link arrives on WhatsApp and email. Bring a contract you drafted recently; you will see it differently by Day 3.</p>",
        21:"<p>Corporate and contract lawyers already have the skill Canadian clients pay for. The bootcamp shows you the route to be qualified to use it there.</p>"}),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in PAGES:
        assert sorted(p["s"]) == list(range(1, 22)) and sorted(p["t"]) == list(range(2, 22)), p["stem"]
        with open(os.path.join(OUT, "lp_%s.html" % p["stem"]), "w") as f:
            f.write(page(p))
        print("lp_%s.html" % p["stem"])
