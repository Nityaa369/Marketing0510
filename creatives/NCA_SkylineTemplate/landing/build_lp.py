"""Landing pages for the NCA skyline ads: one page per ad, same 21-step spine as
creatives/NCA_LandingTemplate_31Oct-2Nov/template.py, with a skyline first fold that repeats the
ad's hook and prize word for word. Run: python3 build_lp.py (from anywhere)."""
import base64, glob, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "NCA_LandingTemplate_31Oct-2Nov"))
import template as T
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]

def b64(name):
    return "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "assets", name), "rb").read()).decode()
ART = b64("art_leaf_skyline.png")
STRIP = lambda t: re.sub(r"</?em>", "", t)

# Skyline fold face: the leaf art from the ad, then the ad's three pillars in the ad's words.
def face(kind, c):
    return ('<div class="face sky"><img src="%s" alt=""><div class="pills">'
            '<div><b>NCA exams</b>Canada\'s check on your Indian law degree. Written online, from India. Every month.</div>'
            '<div><b>Canadian bar</b>Then bar licensing. You become eligible to apply.</div>'
            '<div><b>Practise in Canada</b>Same craft, Canadian clients and courts.</div></div>'
            '<div class="stick">We show you how.</div></div>') % ART
T.face = face
T.CSS += """
.callout{background:transparent;color:var(--ink);text-transform:none;text-align:left;padding:0;font-size:clamp(40px,11vw,66px);line-height:.98;letter-spacing:-.04em}
.callout em,h1 em{font-style:normal;color:var(--ac)}
h1{text-align:left;font-size:clamp(30px,8vw,46px);margin:14px 0 10px}
.face.sky{position:relative;margin:0 0 10px}
.face.sky img{display:block;width:150px;height:auto;margin:-10px 0 0 auto}
.pills{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:6px}
.pills div{background:#fff;border:2px solid #F3D9D2;border-radius:12px;padding:10px 8px;font-size:13px;line-height:1.25;text-align:center;color:var(--mut)}
.pills b{display:block;color:var(--ink);font-size:16px;margin-bottom:3px}
.stick{display:inline-block;background:#FFF04A;font-weight:900;font-size:22px;padding:4px 14px;border-radius:6px;transform:rotate(-2deg);margin:10px 0 2px}
.gloss{text-align:left}
"""
THEME = dict(ac="#F2371D", ac2="#FEECE7", bg="#FEFDF7")

DISCLAIMER = re.compile(r'<div class="end">.*?</div>', re.S)
SIGNOFF = ('<p style="text-align:center;font-weight:700;font-size:17px;color:#4A4338;padding:10px 0 34px">'
           'Live only, no recordings. If Saturday passes, this edition is gone. Rs 10, refundable anytime.</p>')
def launch_version(page):
    """The pages/ copy: no end disclaimer (user instruction, 7 Oct) and no gap markers in the
    visible text. GAPS.md still records every open item; preview/ keeps them highlighted."""
    page = DISCLAIMER.sub(SIGNOFF, page)
    return T.GAP.sub("", page).replace(" Source:", " Source:")

MECH = [
 ("NCA exams, from India", "NCA is Canada's check on your Indian law degree. You write its exams online, from India. We show you what they cover and how to choose your first one."),
 ("Bar licensing", "After the NCA, a province's law society licenses lawyers. Each province has its own steps. We show you the order, so nothing surprises you later."),
 ("Practise in Canada", "With a Canadian qualification you can apply to practise. We show you what comes after the exams and where each path leads."),
]
IMPL = [
 "Live online. Sat 31 Oct and Sun 1 Nov, 2 to 5 PM IST. Mon 2 Nov, 7 to 10 PM IST.",
 "Live only, with no recordings, so bring your questions.",
 "You need a phone or laptop and an internet connection.",
 "Pay Rs 10 and you get the live links for all 3 days.",
]
WORK = ["Day 1: NCA question types, with a worked sample answer. A non-compete clause reviewed under Canadian law. Messages to send to your first Canadian contacts.",
        "Day 2: how licensing works after the NCA, including the bar exams. Your 12 month plan. How to search for Canadian legal work online.",
        "Day 3: a terms and conditions review and a privacy policy under Canadian law. A profile and a proposal template for your first Canadian client."]
S_NAV = ("Navkaran Singh", "District court litigator, Patiala", [
 "He graduated in 2015 and practised in the Patiala district courts. In early 2022 he tried the NCA Constitutional Law exam on his own and did not clear it.",
 "He enrolled in May 2022 and cleared all the prescribed NCA exams. He already held Canadian PR, and it had not been enough on its own. After the exams he applied for government jobs in Ontario and was offered a court and client representative role at the North Bay courts."])
S_HEZ = ("Hezal Shah", "In-house counsel, Mumbai", [
 "LLB from Government Law College Mumbai, 2013. She worked as in-house counsel at Conde Nast. Her husband took a job in Canada, and she did not want to give up her career.",
 "She started preparing in October 2022, wrote her first exam in April 2023 and began clearing exams in June 2023. She moved to Vancouver in December 2023 with four subjects cleared, and cleared the last one by March 2024."])
S_YAS = ("Yashika Malhotra", "Litigator, Chandigarh", [
 "She worked under a senior for four years, then started taking remote legal work from clients abroad. When her husband got a job in Canada, she chose to qualify instead of stopping work.",
 "She cleared four NCA subjects in six months, and moved to Montreal in January 2024 to a job at a large company."])
S_ARC = ("Archita Sarkar", "Corporate lawyer, Pune", [
 "LLB, 2014, Pune. She moved to Canada on PR in August 2023 and enrolled for the NCA exams. She cleared two subjects, Professional Responsibility and Constitutional Law.",
 "By the end of February 2024 she was working as a Senior Legal Specialist at Marsh McLennan in Canada. She found the job after she arrived, and her Indian experience helped her get it."])
S_SHU = ("Shubham Vashisht", "BCom LLB, Punjab University, 2018", [
 "He cleared the NCA exams in all prescribed subjects in March 2024, then moved to the Greater Vancouver area, where he works as a legal assistant at a law firm."])
FAIL_H = "You have probably tried these"
TIME = "The NCA path takes ten months at the fastest and about two years on average."

CFG = {
"nca_sky_01_broad_thinking_about_canada": dict(
  title="Practise law in Canada with your Indian LLB | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="The thought comes back every few months.",
  sym_p=["You are a lawyer in India. Somewhere between a hearing and a draft, Canada comes up again. A cousin moved. A client expanded. A friend posted a photo from Toronto.", "You have never found out whether the route is real for someone with an Indian LLB. So the thought goes back in the drawer."],
  out_h="Find out, once, whether Canada is real for you",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Know what the NCA will most likely ask of you.", "See how the exams fit around the work you already do.", "Leave day 3 with a plan on paper, or a clear no."],
  fail=[("Googling it late at night", "Twenty tabs, each with a different answer, none of them for an Indian LLB holder."), ("Asking someone who moved", "They did it one way, years ago. The rules changed on 1 March 2026."), ("Waiting for the right year", "The right year never announces itself. The exams are monthly, so any year can be the one.")],
  reframe_h="The issue is not courage. It is that nobody laid the route out for you.",
  reframe_p=["You already read statutes and argue cases for a living. Canada outside Quebec runs on common law, the system you trained in. Source: Justice Canada.", "What you were missing is the order: NCA exams first, written from India, then bar licensing, then practice. Once you see the order, the decision becomes yours."],
  cost_h="Another year of not knowing", cost_p=[TIME, "Not knowing has its own cost: every year you wait is a year you could have spent on the first exam."], cost_src="Source: nca.legal.",
  art_h="Your own answer, on paper", art_t="Your route (sample)",
  art_rows=[("Day 1", "What the NCA will most likely ask of you"), ("Day 2", "Your 12 month plan"), ("Day 3", "Your first Canadian client, on paper"), ("After", "First exam month, chosen by you")],
  long_h="A second country where you are a lawyer", long_li=["A Canadian qualification added to your Indian LLB.", "The option to practise in Canada, now or later.", "A decision made on facts, not on a thought in a drawer."],
  p2_h="Lawyers from India who found out, then did it", stories=[S_HEZ, S_NAV],
  lang_h="Say it to a friend who also thinks about Canada", lang_q="The NCA exams are online, from India, every month. I am finding out the whole route for Rs 10 this weekend.",
  next_h="Pay Rs 10. Find out on Saturday.", dyk=["online", "time", "rules2026", "cert"]),
"nca_sky_02_final_year_student": dict(
  title="Final-year law students: start a Canadian law career | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="Everyone is asking what you will do after your LLB.",
  sym_p=["You are in your final year. Placements, chambers, judiciary coaching, a master's abroad. Each option has a deadline and someone pushing it.", "Canada is on your list too, but nobody at college can tell you how an Indian LLB gets there."],
  out_h="A Canadian law career that starts the year you graduate",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Know when a final-year student can apply to the NCA.", "Start the first exam in your first year out, from India.", "Leave day 3 with a plan timed to your graduation."],
  fail=[("The college placement cell", "It knows Indian firms. It does not know the NCA."), ("A master's abroad as the only route", "An LLM is one route. The NCA exams, written from India, are another, and cheaper."), ("Deciding to think about it after graduating", "After graduating comes the first job, and the first job decides the next five years.")],
  reframe_h="The issue is not your marks. It is that your timing is better than you think.",
  reframe_p=["The law you study now is common law. So is Canada's, outside Quebec. Source: Justice Canada.", "Your reading habits are at their peak in final year. A plan made now puts your first NCA exam in the same year your friends start their first job."],
  cost_h="The first job decides the next five years", cost_p=["Once you join a chamber or a firm, your time is theirs. A plan made now runs alongside, not instead.", TIME], cost_src="Source: nca.legal.",
  art_h="A plan timed to your graduation", art_t="Your graduation plan (sample)",
  art_rows=[("Final year", "Know your route and your first subject"), ("Month of graduation", "Apply to the NCA for assessment"), ("Months 2 to 6", "Study, one exam at a time"), ("After", "Bar licensing for your province")],
  long_h="Two countries open to you before you are 25", long_li=["A Canadian qualification started in your first year out.", "A choice of where to practise, made by you.", "A head start on classmates who waited."],
  p2_h="Graduates who started early", stories=[S_SHU, S_YAS],
  lang_h="Say it to your batchmates", lang_q="The NCA exams are online, from India. I am finding out how my LLB gets me to Canada, for Rs 10, before placements decide for me.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["common", "time", "five", "cert"]),
"nca_sky_03_fresh_graduate": dict(
  title="LLB done, not yet practising: practise in Canada | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="You have a degree and no direction yet.",
  sym_p=["The LLB is done. Enrolment is pending or just through. The offers you have are small, and the ones you want are not here.", "You want a plan bigger than your first offer. Canada keeps coming up, and nobody has shown you where to start."],
  out_h="A plan bigger than your first offer",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Know what your first NCA exam could be.", "Study one exam at a time, from India, while you take your first job.", "Leave day 3 with a 12 month plan on paper."],
  fail=[("Scrolling forums", "Old threads, mixed advice, and no way to tell what still applies after the 2026 rule change."), ("Taking any job to settle first", "A year passes, and starting from zero feels harder, not easier."), ("Planning a Canadian degree", "That is one route. There is another: the NCA exams, written from India, with no second degree.")],
  reframe_h="The issue is not experience. It is not knowing the first step.",
  reframe_p=["The NCA does not ask for years in court. It assesses your Indian LLB and sets your exams. You write them online, from India. Source: nca.legal.", "The order is NCA exams, then bar licensing, then practice. Once you know the first step, the rest is a calendar."],
  cost_h="A first job that decides for you", cost_p=["Without a plan, your first job becomes your path by default.", TIME], cost_src="Source: nca.legal.",
  art_h="Your first plan, on paper", art_t="Your first year plan (sample)",
  art_rows=[("Month 1", "Choose your first NCA exam"), ("Months 2 to 5", "Study, one exam at a time"), ("Month 6", "Write your first exam, online"), ("After", "Bar licensing for your province")],
  long_h="A Canada-qualified lawyer, one exam at a time", long_li=["A Canadian qualification added to your Indian degree.", "A choice of where to practise later.", "A start that did not wait for the perfect first job."],
  p2_h="Graduates who started before they settled", stories=[S_SHU, S_ARC],
  lang_h="Say it to your friends", lang_q="The NCA exams are online, from India. I am finding out the whole route, from my LLB to practising in Canada, for Rs 10.",
  next_h="Start now. Pay Rs 10.", dyk=["five", "online", "time", "cert"]),
"nca_sky_04_newly_enrolled_advocate": dict(
  title="Newly enrolled advocates: qualify for Canada alongside court | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="You are new at the bar. Can you go international from here?",
  sym_p=["You enrolled recently. Your days are filing, mentions and waiting outside courtrooms. You are learning fast.", "And you wonder whether a lawyer this early can build a Canada option at all, or whether that is for people with ten years behind them."],
  out_h="Qualify for Canada alongside your first years in court",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "A weekly timetable that fits around court.", "Study about two hours a day, in the hours your senior does not need you.", "Leave day 3 with the timetable on paper."],
  fail=[("Waiting until you are senior", "Seniority brings more work, not more time. The early years have the lightest afternoons."), ("Asking your senior", "They know your court. The Canadian route is outside their experience."), ("Reading about the bar exam first", "The bar exam comes after the NCA. Starting there is starting in the middle.")],
  reframe_h="The issue is not seniority. It is that the early years are the best years to study.",
  reframe_p=["The script of the bootcamp puts it simply: about two hours a day, for months, is what the NCA exams take. A new advocate has those hours. A senior often does not. [[SCRIPT-CHECK: confirm the 2 hours a day line is in the 2026 script]]", "Your first years in court go on as usual. The exams are online, from India, every month, so you pick the month your cause list is light. Source: nca.legal."],
  cost_h="The years when you had the time", cost_p=["Every year at the bar adds clients and matters. The hours you have now will not come back.", TIME], cost_src="Source: nca.legal.",
  art_h="A weekly timetable around court", art_t="Your week (sample)",
  art_rows=[("Mon to Fri, 7 to 9 PM", "NCA study, one subject"), ("Saturday morning", "Practice answers"), ("Court days", "Nothing changes"), ("Your exam month", "Written online, from India")],
  long_h="Two licences before most of your batch has one", long_li=["A Canadian qualification built in your first years at the bar.", "A practice in India that never paused.", "The option to practise in Canada when you choose."],
  p2_h="Young advocates who started early", stories=[S_YAS, S_SHU],
  lang_h="Say it to a fellow junior", lang_q="The NCA exams are online, from India, every month. I am finding out how to qualify for Canada alongside court, for Rs 10.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["online", "time", "rules2026", "cert"]),
"nca_sky_05_experienced_advocate": dict(
  title="Experienced advocates: keep your practice, add a Canadian licence | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="You have a practice. You will not close it.",
  sym_p=["Your chamber runs on you. Clients, juniors, a cause list that fills itself. You are not going anywhere in a hurry.", "And still you want a second market. Not instead of this one. As well as this one."],
  out_h="Keep your practice. Add a Canadian licence.",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Choose exam months around your cause list.", "Keep your Indian practice running while you study.", "Leave day 3 with a map of what your licence covers and what to add."],
  fail=[("Assuming the route means leaving", "It does not. The NCA exams are written from India. Nothing in them asks you to stop practising."), ("Asking around the bar", "Everyone has a half answer. One says two years, another says five. Nobody shows you the order."), ("Waiting for a quiet month", "A quiet month does not come in court. The exams are monthly, so you do not need one.")],
  reframe_h="The issue is not effort. It is a route you have never seen laid out.",
  reframe_p=["You already work harder than most people who qualify abroad. What is missing is the order of the steps and where they fit around your cause list.", "Canada outside Quebec runs on common law, the system you practise in. The NCA exams still test Canadian law, so you study. But you study as someone who reads statutes and cases for a living. Source: Justice Canada."],
  cost_h="Another year of someday", cost_p=[TIME, "The date you start is the only part you control."], cost_src="Source: nca.legal.",
  art_h="A map of what your licence covers", art_t="Your licence map (sample)",
  art_rows=[("What you hold", "Indian licence, your practice areas"), ("What the NCA adds", "Canadian law exams, from India"), ("What the province adds", "Bar licensing, its own steps"), ("What you end with", "Two licences, one practice kept")],
  long_h="Two practices, one qualification at a time", long_li=["A Canadian qualification added to your Indian licence.", "The option to practise in Canada, now or later.", "A chamber that kept running while you studied."],
  p2_h="Practising lawyers who added Canada without closing anything", stories=[S_NAV, S_HEZ],
  lang_h="Say it to your chamber", lang_q="The NCA exams are online, from India, every month. I am finding out the whole route for Rs 10, without touching my practice.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["online", "time", "rules2026", "cert"]),
"nca_sky_06_litigator": dict(
  title="In court every week: serve Canadian clients from India | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="Your week is set by hearing dates.",
  sym_p=["Dates get listed, adjourned, relisted. You spend hours in the corridor for a two minute mention. Your calendar belongs to the court.", "You want work that a court calendar does not control. Not instead of litigation. Alongside it."],
  out_h="Qualify to serve Canadian clients from India",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "See the Canadian legal work you can do from India while you prepare.", "Study in hearing-free hours, one exam at a time.", "Leave day 3 with a plan that has your cause list in it."],
  fail=[("Taking more briefs", "More briefs means more corridor hours. It does not change who controls your week."), ("Waiting for the vacation bench", "Court vacations are short and you need them. The exams are monthly, so you do not need a vacation to start."), ("Looking at arbitration", "A good move inside India. It is still one market and one calendar.")],
  reframe_h="The issue is not your workload. It is that all of it sits in one calendar.",
  reframe_p=["Day 2 of the bootcamp shows Canadian legal work you can do from India while you prepare: reviews and drafts that do not wait on a bench. [[SCRIPT-CHECK: confirm the Day 2 remote work content for 2026]]", "Canada outside Quebec runs on common law, so a litigator's reading habits carry over. The exams test Canadian law, and you write them online, from India, in a month you choose. Source: nca.legal."],
  cost_h="Another year in the corridor", cost_p=["The corridor hours do not add up to anything. Two hours of NCA study a day do.", TIME], cost_src="Source: nca.legal.",
  art_h="A plan with hearing-free hours", art_t="Your week (sample)",
  art_rows=[("Court days", "Mentions, hearings, as usual"), ("Evenings, 2 hours", "NCA study, one subject"), ("Friday afternoon", "Canadian document work, from India"), ("Your exam month", "A month with a light cause list")],
  long_h="Work that waits for you, not for the bench", long_li=["A Canadian qualification built around a litigation practice.", "Canadian clients served from India, in your own hours.", "The option to practise in Canada when you choose."],
  p2_h="Litigators who did it", stories=[S_NAV, S_YAS],
  lang_h="Say it to a colleague at the bar", lang_q="I am finding out how to qualify to serve Canadian clients from India, around my cause list, for Rs 10.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["online", "common", "time", "cert"]),
"nca_sky_07_corporate_contract_lawyer": dict(
  title="Corporate and contract lawyers: draft for Canadian clients too | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="You draft every day. You want bigger clients.",
  sym_p=["Shareholder agreements, vendor contracts, NDAs by the dozen. You are good at it. Your clients are Indian companies, and the ceiling on what they pay is set by the Indian market.", "You want to draft for bigger clients, in a bigger market, without starting over."],
  out_h="Qualify in Canada. Draft for Canadian clients too.",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Mark up a non-compete clause under Canadian law on Day 3.", "See the contract work Canadian startups send to lawyers in India.", "Leave day 3 with your first Canadian markup done."],
  fail=[("Chasing bigger Indian clients", "Bigger Indian clients still pay Indian rates and want the same documents."), ("A foreign LLM", "A year off and a large fee, for a degree that is not a licence anywhere."), ("Picking up US work on platforms", "Without a qualification, you are the cheapest bidder. With one, you are the lawyer.")],
  reframe_h="The issue is not your drafting. It is which law you are qualified in.",
  reframe_p=["Canada outside Quebec uses common law, like India, so contract drafting is familiar ground. The clauses differ, the method does not. Source: Justice Canada.", "On Day 3 you review a non-compete under Canadian law, live, and see how close it is to what you do now. [[SCRIPT-CHECK: confirm the non-compete demo for 2026]]"],
  cost_h="Another year at Indian rates", cost_p=["Your drafting improves every year. Your market does not, unless you qualify in another one.", TIME], cost_src="Source: nca.legal.",
  art_h="A clause marked up under Canadian law", art_t="Your first markup (sample)",
  art_rows=[("Clause", "Non-compete, Canadian employment agreement"), ("Test", "Reasonableness under provincial law"), ("Your markup", "Duration, territory, scope"), ("After", "The same skill, for Canadian clients")],
  long_h="The same craft, a bigger market", long_li=["A Canadian qualification added to your drafting practice.", "Canadian clients who send contract work to India.", "The option to practise in Canada when you choose."],
  p2_h="Corporate lawyers who moved their craft", stories=[S_ARC, S_HEZ],
  lang_h="Say it to a colleague", lang_q="Contract drafting in Canada is common law, like ours. I am finding out how to qualify and draft for Canadian clients, for Rs 10.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["common", "online", "time", "cert"]),
"nca_sky_08_law_firm_associate": dict(
  title="Law firm associates: qualify as a Canadian lawyer | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="You are good at your job. The cross-border work goes to someone else.",
  sym_p=["Your hours are billed, your reviews are good, your promotion is on track. When a Canadian matter comes in, it goes to the foreign counsel or the partner with the contact.", "You want to be qualified somewhere else too. Not to leave. To have the choice."],
  out_h="Qualify as a Canadian lawyer, around your billable hours",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Choose your exam month around your billable year.", "Review a Canadian employment agreement on Day 2 and incorporate a Canadian company on paper on Day 3.", "Leave day 3 with your 12 month calendar."],
  fail=[("Waiting for a slow quarter", "A firm calendar does not stay slow for long. The plan has to fit a busy year."), ("Hoping the firm sends you", "Secondments go to the few. A qualification you own goes with you."), ("A foreign LLM", "A year off and a large fee. The NCA exams are written from India, with no year off.")],
  reframe_h="The issue is not ambition. It is where the exams sit in your year.",
  reframe_p=["The NCA exams are online and run every month, so you choose when. One exam at a time is a plan that fits a job. Source: nca.legal.", "You already draft and review for a living. Canada outside Quebec uses common law, like India, so the habits you built carry over. Source: Justice Canada."],
  cost_h="A year with no plan", cost_p=["If you plan this month, you choose your first exam month. If you do not, your calendar chooses for you.", TIME], cost_src="Source: nca.legal.",
  art_h="A 12 month exam calendar", art_t="Your exam calendar (sample)",
  art_rows=[("Month 1", "Choose your first NCA exam"), ("Month 3", "Your exam month, around billable hours"), ("Month 4", "Review, then pick the next exam"), ("After", "Bar licensing for your province")],
  long_h="A qualification that is yours, not your firm's", long_li=["A Canadian qualification built one exam at a time.", "A choice of where to practise later.", "A plan that never asked you to stop working."],
  p2_h="Lawyers who fitted the exams around a full time job", stories=[S_ARC, S_HEZ],
  lang_h="Say it to a colleague", lang_q="The exams are online, from India. I can pick my month around my billable hours. I am finding out the full route for Rs 10.",
  next_h="Choose Saturday. Pay Rs 10.", dyk=["online", "time", "five", "cert"]),
"nca_sky_09_moving_to_canada": dict(
  title="Moving to Canada? Take your law career with you | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="You have decided to move. Your profession has not been told.",
  sym_p=["The IELTS is booked or done. The PR file is in progress. The family has a date in mind.", "And one question sits under all of it: what happens to my law career when I land? Nobody in the immigration process answers that."],
  out_h="Land in Canada with the exams already behind you",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Write the NCA exams from India, before you move.", "See what Canadian legal work you can do from India while the file moves.", "Leave day 3 with a plan matched to your move date."],
  fail=[("Planning to sort it after landing", "After landing comes rent, a first job and a new city. The exams are easier from your own desk in India."), ("Assuming your Indian licence transfers", "It does not. The NCA assesses your degree and sets exams. Then a province licenses you."), ("Taking any job on arrival", "Many lawyers do, and stay there. A plan made before the flight changes that.")],
  reframe_h="The issue is not the move. It is the order.",
  reframe_p=["The NCA exams can be written from India, online, every month. A lawyer who starts before the move lands with the exams behind them, not ahead of them. Source: nca.legal.", "Hezal Shah moved with four subjects cleared and finished the last one after landing. The order was the difference. [[PENDING: confirm the story with the learner]]"],
  cost_h="Landing with nothing started", cost_p=["Every month in India before the move is a month you can write an exam from home.", TIME], cost_src="Source: nca.legal.",
  art_h="A plan matched to your move date", art_t="Your move plan (sample)",
  art_rows=[("Now", "NCA assessment, first subject"), ("Months 2 to 8", "Exams, online, from India"), ("Move month", "Land with exams behind you"), ("After landing", "Bar licensing in your province")],
  long_h="Arrive as a lawyer, not as a new start", long_li=["NCA exams written before the flight.", "A Canadian qualification underway on landing day.", "A profession that moved with you."],
  p2_h="Lawyers who moved with the exams already underway", stories=[S_HEZ, S_ARC],
  lang_h="Say it to your family", lang_q="I can write Canada's NCA exams from India, before we move. I am finding out the whole route for Rs 10.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["online", "rules2026", "time", "cert"]),
"nca_sky_10_in_house_counsel": dict(
  title="In-house counsel: become a Canada-qualified lawyer | LawSikho",
  sym_eyebrow="You may recognise this", sym_h="Your company works with Canada. The advice comes from outside.",
  sym_p=["You are the legal team, or most of it. Contracts, compliance, the board pack. When a Canadian question comes up, the company pays outside counsel, and you forward emails.", "You want a qualification that is yours, in a market your company already touches."],
  out_h="Become a Canada-qualified lawyer, after office hours",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.", "Write the exams online, from India, after your office day.", "See the top questions a CEO asks before expanding into Canada, on Day 3.", "Leave day 3 with your 12 month plan."],
  fail=[("Waiting for the company to sponsor something", "Companies sponsor what they need this quarter. A qualification is yours for life."), ("Reading Canadian law on the side", "Reading without a route is a hobby. The NCA gives you the subjects and the exam dates."), ("A part-time LLM", "Two years and a large fee, for a degree that is not a licence.")],
  reframe_h="The issue is not your role. It is that your qualification stops at the border.",
  reframe_p=["The NCA exams are online, monthly, and written from India, so they fit after an office day. Source: nca.legal.", "On Day 3 the bootcamp walks through the questions a CEO asks before expanding into Canada, the kind your company already asks outside counsel. [[SCRIPT-CHECK: confirm the Day 3 expansion content for 2026]]"],
  cost_h="Another year forwarding emails", cost_p=["The Canadian questions will keep coming. Who answers them is up to you.", TIME], cost_src="Source: nca.legal.",
  art_h="Your 12 month plan, after office hours", art_t="Your plan (sample)",
  art_rows=[("Weekdays, 7 to 9 PM", "NCA study, one subject"), ("Month 4", "First exam, online, from India"), ("Months 5 to 12", "Remaining exams"), ("After", "Bar licensing for your province")],
  long_h="A qualification that is yours, in a market you already know", long_li=["A Canadian qualification added to your in-house experience.", "The option to practise in Canada, or to be the counsel who can.", "A plan that fitted after office hours."],
  p2_h="In-house lawyers who did it", stories=[S_HEZ, S_ARC],
  lang_h="Say it to a colleague", lang_q="The NCA exams are online, from India, after office hours. I am finding out the whole route to being Canada-qualified for Rs 10.",
  next_h="Pay Rs 10. Join on Saturday.", dyk=["online", "time", "five", "cert"]),
}

ads = {a["stem"]: a for a in json.load(open(os.path.join(ROOT, "ads.json")))}
report = ["# Landing page gaps, skyline set (7 Oct 2026)\n", "Pay link: `#PAYMENT_LINK_PENDING` on every CTA. Wire it before launch.\n"]
for stem, c in CFG.items():
    ad = ads[stem]
    c.update(callout=ad["hook"], head=ad["prize"], face="skyline", theme=THEME, fail_h=FAIL_H, mech=MECH, work=WORK, impl=IMPL)
    page = T.build(c)
    open(os.path.join(HERE, "pages", "lp_" + stem + ".html"), "w").write(launch_version(page))
    pv = os.path.join(HERE, "preview", "lp_" + stem + ".html")
    open(pv, "w").write(T.preview(page))
    report.append("\n## lp_%s  (publish ready: %s)\n" % (stem, T.publish_ready(page)))
    for tag, txt in T.gaps(page): report.append("- **%s**: %s\n" % (tag, txt))
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=430,17000",
                    "--screenshot=" + os.path.join(HERE, "preview", "lp_" + stem + "_full.png"), "file://" + pv], check=True, capture_output=True)
    words = len(re.sub(r"<[^>]+>", " ", page).split())
    print("built lp_%s, about %d words" % (stem, words))
open(os.path.join(HERE, "GAPS.md"), "w").write("".join(report))
