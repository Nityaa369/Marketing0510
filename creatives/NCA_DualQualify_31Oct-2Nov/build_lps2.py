# Dual-qualify landing pages, v2. Tailwind CSS v4 (standalone CLI, compiled and inlined: single
# file, no CDN, fast first paint). Structure = Ruchika's 21 steps compressed into 10 numbered
# sections, carrying every element the account's history says converts:
#   - Rule 2 first fold order (CF 15-17 Aug, 7/7 approved: who-question, qualifier, offer,
#     definition, deliverables, terms) and Rule 3 (fold repeats the ad's words).
#   - Counted-list sections ("argument, not brochure", SOP/05).
#   - Now/after two-column map (DP donor pages, 14.7-18.7% results/LPV).
#   - 5 CTAs, each stating the full exchange (gate: a button never reads as a deposit).
#   - Closing fold names the reader FIRST with a self-contained lede (closing_reader rules).
#   - One h2 names the reader (lint L6). Sentences <= 34 words (L7). No dash characters.
#   - Market data labelled with source and date, page only. Disclaimer at the end only.
# Run: python3 build_lps2.py
import os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "landing_pages")
TW = os.path.expanduser("~/tools/tailwindcss")
PAY = "#PAYMENT_LINK_PENDING"  # BLOCKER: real GrowthX funnel URL per page, then test-buy in a browser

T = dict(dates="Sat 31 Oct, Sun 1 Nov and Mon 2 Nov 2026",
         times="2 to 5 PM IST on Sat and Sun, 7 to 10 PM IST on Mon")

BTN = "block w-full text-center text-white font-black text-xl rounded-xl py-4 px-6 bg-(--ac) shadow-lg"
H2 = "text-2xl font-black leading-tight mt-1 mb-4"
NUM = "text-xs font-black tracking-widest uppercase text-(--ac)"
SEC = "py-8 border-b border-black/10"

def cta(label):
    return '<a class="%s" href="%s">%s</a>' % (BTN, PAY, label)

ROUTE = ('<div class="flex items-center gap-2 mt-5 text-center">'
         '<div class="flex-1 border-3 border-(--ac) rounded-xl bg-white font-extrabold text-sm py-3 px-1">NCA exams, from India</div>'
         '<div class="text-(--ac) font-black">&#8594;</div>'
         '<div class="flex-1 border-3 border-(--ac) rounded-xl bg-white font-extrabold text-sm py-3 px-1">Bar licensing</div>'
         '<div class="text-(--ac) font-black">&#8594;</div>'
         '<div class="flex-1 border-3 border-(--ac) rounded-xl bg-(--ac) text-white font-extrabold text-sm py-3 px-1">Practise in Canada</div></div>')

FACTS = ('<ol class="mt-4 space-y-4 list-none">'
 '<li><b>1. The NCA rules changed on 1 March 2026.</b> Every applicant now takes an English screening and a short Indigenous law course. The bootcamp explains both, so the newest rules are the ones you learn. <span class="text-sm opacity-70">Source: nca.legal; CIC News, March 2026.</span></li>'
 '<li><b>2. Canada plans 380,000 new permanent residents a year, 2026 to 2028.</b> 64 percent come through economic programs, the kind a qualified professional uses. <span class="text-sm opacity-70">Source: IRCC levels plan, canada.ca.</span></li>'
 '<li><b>3. India is the largest source of new permanent residents: 127,320 in 2024.</b> The route is crowded for everyone except the professions with a licensing path. Law has one. <span class="text-sm opacity-70">Source: IRCC data via immigration.ca.</span></li>'
 '<li><b>4. The NCA exams run every month, online, from India.</b> The NCA itself puts the best case at about 10 months and the average at about two years. <span class="text-sm opacity-70">Source: nca.legal, costs and timelines.</span></li></ol>')

COST = ('<table class="w-full mt-4 text-sm bg-white border-collapse">'
 '<tr class="bg-(--soft)"><th class="border border-black/15 p-2 text-left">Route</th><th class="border border-black/15 p-2 text-left">Cost</th><th class="border border-black/15 p-2 text-left">What it asks of you</th></tr>'
 '<tr><td class="border border-black/15 p-2">A Canadian law degree</td><td class="border border-black/15 p-2">About CAD 35,000 to 56,000 a year</td><td class="border border-black/15 p-2">Move first, pause your work for years</td></tr>'
 '<tr><td class="border border-black/15 p-2">The NCA exams, from India</td><td class="border border-black/15 p-2">About CAD 3,000 plus taxes, minimum</td><td class="border border-black/15 p-2">Steady preparation beside your work</td></tr>'
 '<tr><td class="border border-black/15 p-2 font-bold">This bootcamp</td><td class="border border-black/15 p-2 font-bold">Rs 10, incl. GST, refundable</td><td class="border border-black/15 p-2 font-bold">Three live sessions, 9 hours</td></tr></table>'
 '<p class="text-sm opacity-70 mt-2">Figures from nca.legal. Fees are set by the NCA and can change.</p>')

SESSIONS = ('<div class="mt-4 space-y-4">'
 '<div class="bg-white rounded-xl p-4 shadow-sm"><div class="font-black text-(--ac) text-sm uppercase tracking-wider">Day 1 · Sat 31 Oct · 2 to 5 PM</div><p class="mt-1">How the NCA assesses an Indian LLB, the exam question types, and an IRAC answer you write yourself, live.</p></div>'
 '<div class="bg-white rounded-xl p-4 shadow-sm"><div class="font-black text-(--ac) text-sm uppercase tracking-wider">Day 2 · Sun 1 Nov · 2 to 5 PM</div><p class="mt-1">Your 12-month plan, the 2026 English screening and Indigenous law course, and how to find Canadian legal work from India.</p></div>'
 '<div class="bg-white rounded-xl p-4 shadow-sm"><div class="font-black text-(--ac) text-sm uppercase tracking-wider">Day 3 · Mon 2 Nov · 7 to 10 PM</div><p class="mt-1">The bar licensing step, and Canadian documents reviewed live, including a non-compete clause and a startup privacy policy.</p></div></div>'
 '<ul class="mt-5 space-y-1 font-semibold"><li>Where: online and live. Joining details arrive on WhatsApp and email.</li><li>Bring: a laptop and the three slots kept free. Nothing to prepare.</li><li>Not included: recordings. The sessions are live only.</li><li>Led by: Abhishek Pareek, who runs LawSikho\'s NCA programme.</li></ul>')

JOBBANK = ('<div class="bg-white border-l-6 border-(--ac) rounded-md p-4 mt-4"><p><b>Market data, not a promise:</b> Canada\'s Job Bank reports a median wage of CAD 65.21 an hour for lawyers in Ontario, where about 54,600 people work in the occupation.</p><p class="text-sm opacity-70 mt-1">Source: jobbank.gc.ca, NOC 41101, Ontario, 2025 to 2027 outlook.</p></div>')

DISC = ('<div class="max-w-xl mx-auto px-5 pt-8 pb-28 text-sm opacity-80 space-y-2">'
 '<p><b>Please read.</b> LawSikho is an independent education company. It is not part of the National Committee on Accreditation, the Federation of Law Societies of Canada, the Law Society of Ontario or any other Canadian law society or government body. None of them endorses it. Their requirements, fees and timelines are set by them, change from time to time, and should be confirmed on their own websites before you apply.</p>'
 '<p>The bootcamp teaches the route and a plan. It does not guarantee an NCA assessment result, exam results, a Certificate of Qualification, a licence to practise, a job, clients, a visa or immigration status. Learner stories describe individual experiences and are not typical results. Wage and economic figures are published market data, labelled with their source, and are not a promise of earnings. Nothing on this page is legal or immigration advice. Sample documents are illustrations for teaching.</p>'
 '<p>Live online sessions only; there are no recordings. Price Rs 10, including GST, refundable anytime on request.</p></div>')


def sec(n, step, title, body):
    return ('<section class="%s"><!-- steps %s --><div class="max-w-xl mx-auto px-5">'
            '<div class="%s">%s</div><h2 class="%s">%s</h2>%s</div></section>') % (SEC, step, NUM, n, H2, title, body)


def page(p):
    s = p["s"]
    hero = ('<header class="bg-(--soft) border-b-6 border-(--ac) py-8"><div class="max-w-xl mx-auto px-5">'
      '<div class="text-xs font-extrabold tracking-widest uppercase text-(--ac)">LawSikho · NCA and Canadian bar bootcamp</div>'
      '<div class="text-xs font-extrabold tracking-wider text-(--ac) mt-3">%(qual)s</div>'
      '<h1 class="text-4xl font-black leading-tight mt-2">%(h1)s</h1>'
      '<p class="text-lg font-bold mt-3">%(offer)s</p>'
      '<p class="mt-3 opacity-80"><b>NCA</b> means the National Committee on Accreditation: the body that checks your Indian law degree for Canada and tells you which exams to clear. You write those exams online, from India.</p>'
      '<ul class="mt-4 space-y-1 font-semibold"><li>&#10003; The NCA exams and how to prepare for them from India</li><li>&#10003; The bar licensing step that comes after</li><li>&#10003; Your own 12-month plan, written with you</li></ul>'
      '<div class="bg-white border-2 border-(--ac) rounded-xl p-3 mt-4 font-bold">%(dates)s<br>%(times)s<br>Live only, no recordings. Rs 10 incl. GST, refundable anytime.</div>'
      '<div class="mt-4">%(cta)s</div>'
      '%(route)s'
      '</div></header>') % dict(p, dates=T["dates"], times=T["times"], cta=cta("Try the route for Rs 10"), route=ROUTE)

    body = [hero]
    body.append(sec("01", "1-2", p["t1"], s[1]))
    body.append(sec("02", "3", p["t2"], s[2]))
    body.append(sec("03", "4-6", "Three ways lawyers get Canada wrong", s[3]))
    body.append(sec("04", "7-8", "The problem is not effort. It is positioning", s[4]))
    body.append(sec("05", "8", "Four facts that make 2026 the year to decide", FACTS +
      '<div class="mt-5">' + cta("Get the 3 live days for Rs 10") + "</div>"))
    body.append(sec("06", "9-11", "The offer: try the whole route for Rs 10", s[6] +
      '<ol class="mt-4 space-y-3 list-none">'
      '<li class="bg-white rounded-xl p-4 shadow-sm"><b class="text-(--ac)">Step 1.</b> Clear the NCA exams from India. Your degree is assessed, your subjects are set, and the exams are online, open book and monthly.</li>'
      '<li class="bg-white rounded-xl p-4 shadow-sm"><b class="text-(--ac)">Step 2.</b> Take Canadian legal work from India while you prepare, found on LinkedIn, Upwork and law-society directories. It builds your Canadian track record early.</li>'
      '<li class="bg-white rounded-xl p-4 shadow-sm"><b class="text-(--ac)">Step 3.</b> Pass the bar licensing, then practise in Canada, or serve Canadian clients from India as a Canada-qualified lawyer.</li></ol>'
      + s["artifact"]))
    body.append(sec("07", "12", p["t7"], s[7]))
    body.append(sec("08", "13-14", "People who took this route, and what the market pays",
      s[8] + JOBBANK + '<p class="text-sm opacity-70 mt-2">Named, as told in our bootcamp. Individual results vary.</p>'
      + '<div class="mt-5">' + cta("Join the 3 live days for Rs 10") + "</div>"))
    body.append(sec("09", "15-17", "The work, session by session, and what each route costs", SESSIONS + COST))
    body.append(sec("09b", "16", p["faq_h"],
      '<div class="mt-2 space-y-4">' + "".join(
        '<div class="bg-white rounded-xl p-4 shadow-sm"><p class="font-bold">%s</p><p class="mt-1">%s</p></div>' % qa
        for qa in p["faq"]) + "</div>"))
    body.append(sec("10", "18-19", "The risk, removed, and the line you can say at home",
      '<p>Rs 10, including GST. If it is not worth it, ask for the Rs 10 back, anytime, no reason needed. You keep everything you write in the sessions.</p>'
      '<div class="bg-(--soft) rounded-xl p-4 mt-4 text-lg font-bold">"%s"</div>'
      '<p class="mt-4"><b>You are in the right room if</b> %s</p>' % (s["quote"], s["room"])))
    # 20-21: closing fold, reader named first, no hedge, then stop.
    body.append('<section class="bg-(--soft) py-10"><!-- steps 20-21 --><div class="max-w-xl mx-auto px-5">'
      '<h2 class="text-3xl font-black leading-tight">%s</h2><p class="mt-3 text-lg">%s</p>'
      '<div class="mt-5">%s</div></div></section>' % (s["close_h"], s["close_p"], cta("Try the route for Rs 10")))
    body.append(DISC)
    body.append('<div class="fixed bottom-0 inset-x-0 bg-white border-t-3 border-(--ac) p-3 flex items-center justify-center gap-3 z-10">'
      '<span class="font-extrabold text-sm hidden sm:block">NCA and Canadian bar bootcamp · Rs 10 incl. GST · refundable</span>'
      '<a class="bg-(--ac) text-white font-black px-5 py-3 rounded-xl" href="%s">Try the route for Rs 10</a></div>' % PAY)

    return ('<!doctype html>\n<!-- /f/%(slug)s · pairs with ad %(stem)s · BLOCKER: pay links pending -->\n'
      '<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      '<title>%(title)s</title><style>:root{--ac:%(ac)s;--soft:%(soft)s}%(css)s p+p{margin-top:.75rem}</style></head>'
      '<body class="bg-[#FBF9F4] text-[#17140F] font-sans leading-relaxed">%(body)s</body></html>'
      ) % dict(p, css="%CSS%", body="".join(body))


PAGES = [
dict(stem="nca_d_01_two_licences_5plus", slug="nca-oct-d01-dual-experienced", ac="#1F3B5C", soft="#E9EEF5",
  title="Keep your Indian licence, add Canada's",
  qual="ADVOCATES · LITIGATORS · IN-HOUSE COUNSEL · 5+ YEARS OF PRACTICE",
  h1="Practising law for 5+ years? <em class='text-(--ac)'>Keep your Indian licence. Add Canada's.</em>",
  offer="Keep your Indian licence and add Canada's. In 3 live days, we show you how to clear the NCA exams from India while your practice keeps running.",
  faq_h="Questions senior advocates ask before Day 1",
  faq=[("Will this clash with my court diary?","No. The sessions sit on a weekend and one evening, and the 12-month plan is built around your matters, not instead of them."),
       ("Is my seniority an advantage or a problem?","The NCA assesses the degree, so seniority is neutral there. In the licensing step and with clients, fifteen years of real matters is an asset few new graduates can match."),
       ("Does anything change in my Indian practice while I prepare?","Nothing. You remain an advocate in India throughout. The second licence is added beside the first, never in place of it.")],
  t1="Advocates with 5+ years: your licence is strong, and it stops at the border",
  t2="What you want is a second licence, not a second career",
  t7="Your practice now, and with the second licence",
  s={1:"<p>Five years in, your Indian licence carries weight. Clients trust it, courts know your name, juniors learn from you.</p><p>And yet when a client expands to Canada, or family asks about moving, your advice stops at the border. The question is not whether you are good enough. It is why one border decides where your experience counts.</p>",
     2:"<p>You do not want to start over in Canada. You want to hold two licences: the Indian one you earned and a Canadian one beside it, so the same experience works in two markets.</p><p>That is what dual qualification means, and it has a set route.</p>",
     3:('<ol class="mt-2 space-y-4 list-none">'
        '<li><b class="text-(--ac)">1. They treat Canada as a fresh start.</b> Selling up, moving, beginning again. For a senior advocate that throws away the most valuable asset you own: a running practice and a name.</li>'
        '<li><b class="text-(--ac)">2. They wait for a quiet year.</b> A good practice never offers one. The NCA exams are online and monthly, so the route is built for people who keep working.</li>'
        '<li><b class="text-(--ac)">3. They refer Canadian questions away.</b> Each referral sends a client relationship to another lawyer. A second licence keeps that work, and that client, with you.</li></ol>'),
     4:"<p>You already work harder than almost anyone reading this page, so effort is not the gap. The gap is positioning: your licence places you in one country.</p><p>The NCA's Certificate of Qualification, then a provincial licence, repositions the same degree and the same experience as recognised in Canada too. Every month without the second licence is a month your experience is priced by one market.</p>",
     6:"<p>Before you commit to anything, try the whole route for Rs 10, refundable. Three live sessions walk you from the first NCA application to bar licensing, with your own plan at the end.</p>",
     "artifact":"<p class='mt-4'><b>What you hold by the end of Day 2:</b> your two-licence map. What your Indian licence already covers, what the NCA will likely ask you to add, and the order in which you add it around your existing matters.</p>",
     7:('<table class="w-full mt-2 text-sm bg-white border-collapse">'
        '<tr class="bg-(--soft)"><th class="border border-black/15 p-2 text-left">Now</th><th class="border border-black/15 p-2 text-left">With licence 2</th></tr>'
        '<tr><td class="border border-black/15 p-2">Canadian questions get referred away</td><td class="border border-black/15 p-2">You advise on them, under your own licence</td></tr>'
        '<tr><td class="border border-black/15 p-2">One market prices your experience</td><td class="border border-black/15 p-2">Two markets bid for it</td></tr>'
        '<tr><td class="border border-black/15 p-2">Clients stop at the border</td><td class="border border-black/15 p-2">Clients cross it with you</td></tr>'
        '<tr><td class="border border-black/15 p-2">Canada is a someday conversation</td><td class="border border-black/15 p-2">Canada is a dated, five-year window you control</td></tr></table>'),
     8:"<p><b>Hezal Shah</b> was an in-house lawyer in Mumbai. In our bootcamp's own account, Hezal qualified first and then moved to Vancouver.</p><p class='mt-2'><b>Shashwat Jindal</b> practises from Ludhiana. As our bootcamp tells it, the practice serves four US firms, a Canadian firm and five startups, without leaving the city.</p>",
     "quote":"I am adding a Canadian licence to my Indian one. The practice stays.",
     "room":"you have practised for five years or more, you would rather add a market than restart in one, and you want a plan that fits around real matters.",
     "close_h":"Advocates with five years at the bar already hold the harder licence.",
     "close_p":"You earned the first licence in courtrooms. The second one is an assessment, a set of monthly exams you write from India, and a licensing step. Three live days show you the whole route, for Rs 10."}),

dict(stem="nca_d_02_myth_fact_canada", slug="nca-oct-d02-myth-fact", ac="#1E6A48", soft="#E6F1EA",
  title="Practise law in Canada with the LLB you already have",
  qual="LLB HOLDERS · ADVOCATES · ASSOCIATES · IN-HOUSE · ANY PRACTICE AREA",
  h1="Want to practise law in Canada? <em class='text-(--ac)'>Practise law in Canada with the LLB you already have.</em>",
  offer="Myth: you need a Canadian law degree first. Fact: the NCA assesses your Indian LLB and sets the exams. In 3 live days, we show you the route, step by step.",
  faq_h="Questions LLB holders ask before Day 1",
  faq=[("My LLB is a 3-year degree. Does it count?","The NCA assesses both 3-year and 5-year LLBs from recognised universities. Day 1 shows what each profile is usually assigned."),
       ("Which English test will I need?","A screening test is part of the NCA assessment since 1 March 2026, and a recent full test can exempt you. Day 2 covers exactly which scores count."),
       ("What if the NCA assigns me extra subjects?","You will know the likely list for your own profile on Day 1, before you pay the NCA anything. That is the point of checking first.")],
  t1="Lawyers who want Canada keep hearing what they lack",
  t2="What you want is the facts, current to 2026, and a route",
  t7="What you believed, against what is true",
  s={1:"<p>You would need a Canadian degree. You would need to move first. You would need to be younger, or richer, or from a bigger university.</p><p>Every conversation about practising law in Canada seems to start with what you lack. Most of that advice is out of date, and some of it was never true.</p>",
     2:"<p>You want three answers. Can my degree apply? What changed this year? And what exactly happens between applying and practising in Canada?</p><p>This page answers all three, with sources, and the bootcamp turns the answers into your own plan.</p>",
     3:('<ol class="mt-2 space-y-4 list-none">'
        '<li><b class="text-(--ac)">1. They buy a degree they did not need.</b> For an Indian LLB from a recognised university, the NCA assesses the degree you already hold and assigns exams. A Canadian degree is a longer, costlier route than most people need.</li>'
        '<li><b class="text-(--ac)">2. They move first and sort law out later.</b> Lawyers who land without a plan often spend years outside law. The exams can be written from India, so the move can come last, with the licence in sight.</li>'
        '<li><b class="text-(--ac)">3. They act on advice older than the rules.</b> Since 1 March 2026, every applicant takes an English screening and an Indigenous law course. Advice from last year misses both.</li></ol>'),
     4:"<p>Your degree is not the gap. An Indian LLB is already common-law training. The gap is positioning: today the degree is recognised in India only.</p><p>The NCA process positions the same degree as recognised in Canada. Lawyers who believe the route is closed stop reading about it, and never learn when the facts change in their favour. That is the real cost of the myths.</p>",
     6:"<p>Three live sessions replace every myth with a sourced fact, then walk you along the route with your own degree in hand. Rs 10, refundable.</p>",
     "artifact":"<p class='mt-4'><b>What you hold by the end of Day 1:</b> a one-page fact sheet for your own profile. Your degree type, the English test you need, the subjects you are likely to be assigned, and the province that fits.</p>",
     7:('<table class="w-full mt-2 text-sm bg-white border-collapse">'
        '<tr class="bg-(--soft)"><th class="border border-black/15 p-2 text-left">You believed</th><th class="border border-black/15 p-2 text-left">The fact</th></tr>'
        '<tr><td class="border border-black/15 p-2">I need a Canadian law degree</td><td class="border border-black/15 p-2">The NCA assesses your Indian LLB and sets exams</td></tr>'
        '<tr><td class="border border-black/15 p-2">I must move before I can start</td><td class="border border-black/15 p-2">The exams are online, written from India, monthly</td></tr>'
        '<tr><td class="border border-black/15 p-2">My English-medium LLB exempts me</td><td class="border border-black/15 p-2">Since 1 March 2026, every applicant is screened</td></tr>'
        '<tr><td class="border border-black/15 p-2">It takes a decade</td><td class="border border-black/15 p-2">The NCA\'s own best case is about 10 months, average about two years</td></tr></table>'),
     8:"<p><b>Navkaran Singh</b>, an Indian law graduate, cleared the NCA exams and went on to work in the Ontario courts, as our bootcamp tells it.</p><p class='mt-2'><b>Yashika Malhotra</b> was a litigator in India. In our bootcamp's own account, Yashika moved to Canada with a Canadian job already in hand.</p>",
     "quote":"I do not need a Canadian degree. The NCA assesses my Indian LLB.",
     "room":"you hold an Indian LLB, you are serious about practising law in Canada, and you prefer sourced facts to forum advice.",
     "close_h":"Lawyers with an Indian LLB: the route is open, and it is written down.",
     "close_p":"The myths cost people years. The facts fit on one page, and the bootcamp hands you that page with a plan attached, for Rs 10."}),

dict(stem="nca_d_03_ticket_newly_enrolled", slug="nca-oct-d03-try-route", ac="#9E2328", soft="#F6E9E6",
  title="Become a lawyer in Canada, try the route first",
  qual="NEWLY ENROLLED ADVOCATES · JUNIOR ASSOCIATES · RECENT LLB GRADUATES",
  h1="Newly enrolled advocate? <em class='text-(--ac)'>Become a lawyer in Canada. Try the route first, for Rs 10.</em>",
  offer="Admit one, live, for Rs 10. In 3 days you write an NCA-style answer and leave with a 12-month plan built around about 2 hours a day after court.",
  faq_h="Questions juniors ask before Day 1",
  faq=[("I enrolled this year. Is it too early?","No. The NCA assesses your degree, not your years of practice. Early evenings are the advantage seniors wish they still had."),
       ("What does the route cost after the bootcamp?","The NCA's own figures: about CAD 400 for the assessment and CAD 500 per exam. Nothing more is sold inside the camp."),
       ("What if the trial tells me Canada is not for me?","Then Rs 10 bought you a clear answer years early, and even the Rs 10 is refundable.")],
  t1="Newly enrolled advocates: the first year is full, and Canada sounds expensive",
  t2="What you want is an answer, cheaply, before any commitment",
  t7="Your evenings now, and on the route",
  s={1:"<p>You are learning court, drafting for a senior and earning very little. Canada keeps coming up, in posts you save at night and in calls from friends abroad.</p><p>It also sounds like a decision with a lot of zeros in it. So you tell yourself you will look at it properly one day, and the day does not come.</p>",
     2:"<p>You do not need to decide about Canada today. You need to find out, cheaply, whether the route suits you.</p><p>Everywhere else you try before you commit: a sample chapter, a demo class, a test drive. This is the test drive for a Canadian law career, and it costs Rs 10.</p>",
     3:('<ol class="mt-2 space-y-4 list-none">'
        '<li><b class="text-(--ac)">1. They decide without trying.</b> Some juniors rule Canada out without ever seeing an NCA question. Others commit on a friend\'s word. Both are guesses, and a career deserves better than a guess.</li>'
        '<li><b class="text-(--ac)">2. They buy a big course first.</b> Paying heavily before you know whether you even like the material is the expensive way to find out. Try the material first.</li>'
        '<li><b class="text-(--ac)">3. They ask seniors who never took the route.</b> Seniors are right about Indian practice. On the NCA, advice from someone who has walked it beats advice from someone who has heard of it.</li></ol>'),
     4:"<p>You are not short of commitment. You are short of information, and information is the cheapest thing on this page.</p><p>Once you have it, your position changes: from a junior wondering about Canada to a junior with a tested, dated plan. Early evenings are the most flexible you will ever have, and the route rewards people who start while that is true.</p>",
     6:"<p>Three live sessions, 9 hours, timed around court: two afternoons on the weekend and one evening. You try every stage of the route before spending anything beyond Rs 10.</p>",
     "artifact":"<p class='mt-4'><b>What you hold by the end of Day 1:</b> an NCA-style answer you wrote yourself, in the IRAC format. It is the fastest honest test of whether these exams suit you, before you pay a single NCA fee.</p>",
     7:('<table class="w-full mt-2 text-sm bg-white border-collapse">'
        '<tr class="bg-(--soft)"><th class="border border-black/15 p-2 text-left">Evenings now</th><th class="border border-black/15 p-2 text-left">Evenings on the route</th></tr>'
        '<tr><td class="border border-black/15 p-2">Scrolling posts from friends in Toronto</td><td class="border border-black/15 p-2">About 2 hours of NCA preparation, planned</td></tr>'
        '<tr><td class="border border-black/15 p-2">Canada is a maybe, someday</td><td class="border border-black/15 p-2">Canada is a 12-month plan with dates</td></tr>'
        '<tr><td class="border border-black/15 p-2">Waiting to feel senior enough</td><td class="border border-black/15 p-2">Building a second-country track record early</td></tr></table>'),
     8:"<p><b>Harshmir Swaitch</b> worked as a legal assistant at a Canadian firm, on NRI and immigration matters, while preparing, as our bootcamp tells it. The Canadian work started from India.</p><p class='mt-2'><b>Yashika Malhotra</b>, a litigator, had a Canadian job lined up before moving, in our bootcamp's own account.</p>",
     "quote":"I am trying the Canada route for three days before I decide anything.",
     "room":"you are early in your career, you have about 2 hours an evening, and you want to test the route before you commit to it.",
     "close_h":"Newly enrolled advocates have the one thing this route rewards most: time.",
     "close_p":"Three live days, one answer written in your own hand, and a plan you have actually tested. If it is not for you, the Rs 10 comes back. Either way, you stop guessing."}),

dict(stem="nca_d_04_split_contract_lawyers", slug="nca-oct-d04-same-drafting", ac="#0E5A6C", soft="#E3EEF2",
  title="Qualify in Canada, draft the same contracts",
  qual="CORPORATE LAWYERS · CONTRACT DRAFTERS · M&A · IN-HOUSE COUNSEL",
  h1="Corporate or contract lawyer? <em class='text-(--ac)'>Qualify in Canada. Draft for Canadian clients too.</em>",
  offer="The shareholders' agreements, service contracts, NDAs and privacy policies you draft now are the documents Canadian clients need too. In 3 live days, we show you how to qualify to draft them for Canada.",
  faq_h="Questions drafters ask before Day 1",
  faq=[("Is Canadian contract law very different from ours?","The roots are the same common law. The differences are specific, and they are exactly what the exams teach. Day 3 shows them on a live clause."),
       ("Can I work for Canadian clients before I am licensed?","Support work, drafting assistance and research can start from India while you prepare. Advising as a lawyer comes after licensing, and the plan sequences both."),
       ("I am in-house, not at a firm. Does this fit?","Yes. In-house counsel follow the same route, and a Canada-qualified lawyer on an Indian legal team is rare enough to be noticed.")],
  t1="Contract lawyers: your documents travel better than your licence",
  t2="What you want is the same drafting, instructed from a second country",
  t7="Document by document: India today, Canada next",
  s={1:"<p>A shareholders' agreement you draft in Mumbai would read well in Toronto. The structure, the protections, the boilerplate: you know them all.</p><p>What you cannot do is advise on that document under Canadian law. So the Canadian side of a deal is drafted by someone else, even when your client would rather keep it with you.</p>",
     2:"<p>You want to draft the same documents for Canadian startups, Canadian companies, and Indian clients entering Canada, as a lawyer qualified to advise them directly.</p><p>Canada is a common-law country, like India, so the skill carries. The licence is the missing piece, and it has a route.</p>",
     3:('<ol class="mt-2 space-y-4 list-none">'
        '<li><b class="text-(--ac)">1. They sell drafting abroad without a licence.</b> On open platforms, an unqualified drafter competes on price with every other unqualified drafter. Serious clients check the licence first.</li>'
        '<li><b class="text-(--ac)">2. They wait for a cross-border mandate.</b> Those mandates go to lawyers already qualified on both sides. Waiting leaves your position exactly where it is.</li>'
        '<li><b class="text-(--ac)">3. They buy a general international LLM.</b> It costs lakhs, pauses the practice, and still does not license you in Canada. The licence comes through the NCA route.</li></ol>'),
     4:"<p>Your drafting is not the gap. Where Canadian courts read a clause differently, that is precisely what the NCA exams teach and test.</p><p>The gap is positioning: you are seen as an Indian-law drafter. Dual qualification makes you a drafter Canadian clients can instruct directly, and the interesting cross-border work follows whoever holds both licences.</p>",
     6:"<p>Three live sessions built around documents: you watch Canadian versions of your daily work drafted, checked and priced, and leave with your own route plan. Rs 10, refundable.</p>",
     "artifact":"<p class='mt-4'><b>What you hold by the end of Day 3:</b> a non-compete clause reviewed under Canadian law, in your own markup. You see which instincts carry over and where Canadian courts read the clause differently.</p>",
     7:('<table class="w-full mt-2 text-sm bg-white border-collapse">'
        '<tr class="bg-(--soft)"><th class="border border-black/15 p-2 text-left">Document</th><th class="border border-black/15 p-2 text-left">India, today</th><th class="border border-black/15 p-2 text-left">Canada, in the bootcamp</th></tr>'
        '<tr><td class="border border-black/15 p-2">Employment agreement</td><td class="border border-black/15 p-2">You draft it under Indian law</td><td class="border border-black/15 p-2">Reviewed on Day 2</td></tr>'
        '<tr><td class="border border-black/15 p-2">Non-compete</td><td class="border border-black/15 p-2">You negotiate it</td><td class="border border-black/15 p-2">Reviewed under Canadian law, Day 3</td></tr>'
        '<tr><td class="border border-black/15 p-2">Company set-up</td><td class="border border-black/15 p-2">Indian incorporation</td><td class="border border-black/15 p-2">Incorporating in Canada, Day 3</td></tr>'
        '<tr><td class="border border-black/15 p-2">Privacy policy</td><td class="border border-black/15 p-2">Indian clients\' policies</td><td class="border border-black/15 p-2">For a Canadian founder, Day 3</td></tr></table>'),
     8:"<p><b>Shashwat Jindal</b> practises from Ludhiana. In our bootcamp's own account, the practice drafts for four US firms, a Canadian firm and five startups, all from India.</p><p class='mt-2'><b>Hezal Shah</b> was an in-house lawyer in Mumbai and, as our bootcamp tells it, moved to Vancouver after qualifying first.</p>",
     "quote":"I am qualifying in Canada so I can draft the same documents for Canadian clients.",
     "room":"contracts are your daily work, you want them instructed from two countries, and you want the route tested before any larger step.",
     "close_h":"Corporate and contract lawyers already draft what Canadian clients buy.",
     "close_p":"The documents are the same. The licence is the difference, and the route to it starts with three live days and Rs 10."}),
]


def build():
    os.makedirs(OUT, exist_ok=True)
    drafts = {}
    for p in PAGES:
        drafts[p["stem"]] = page(p)
    with tempfile.TemporaryDirectory() as td:
        for k, v in drafts.items():
            open(os.path.join(td, k + ".html"), "w").write(v)
        inp = os.path.join(td, "in.css")
        open(inp, "w").write('@import "tailwindcss";\n@source "./";\n')
        out = os.path.join(td, "out.css")
        subprocess.run([TW, "-i", inp, "-o", out, "-m"], check=True, capture_output=True, cwd=td)
        css = open(out).read()
    for k, v in drafts.items():
        open(os.path.join(OUT, "lp_" + k + ".html"), "w").write(v.replace("%CSS%", css))
        print("lp_" + k + ".html")


if __name__ == "__main__":
    build()
