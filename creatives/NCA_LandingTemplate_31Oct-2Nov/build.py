import os, glob, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from template import build, gaps, preview, publish_ready
HERE = os.path.dirname(os.path.abspath(__file__))
HS = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]

MECH = [
 ("NCA exams, from India", "NCA is Canada's check on your Indian law degree. You write its exams online, from India. We show you what they cover and how to choose your first one."),
 ("Bar licensing", "After the NCA, a province's law society licenses lawyers. Each province has its own steps. We show you the order, so nothing surprises you later."),
 ("Practise in Canada", "With a Canadian qualification you can apply to practise. We show you what comes after the exams and where each path leads."),
]
BASE_IMPL = [
 "Live online. Sat 31 Oct and Sun 1 Nov, 2 to 5 PM IST. Mon 2 Nov, 7 to 10 PM IST.",
 "Live only, with no recordings, so bring your questions.",
 "You need a phone or laptop and an internet connection.",
 "Pay Rs 10 and you get the live links for all 3 days.",
]
FAIL_TAG = None
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
WORK = ["Day 1: NCA question types, with a worked sample answer. A non-compete clause reviewed under Canadian law. Messages to send to your first Canadian contacts.",
        "Day 2: how licensing works after the NCA, including the bar exams. Your 12 month plan. How to search for Canadian legal work online.",
        "Day 3: a terms and conditions review and a privacy policy under Canadian law. A profile and a proposal template for your first Canadian client."]

CFG = {
"lp_advocates": dict(
  title="Experienced advocates: practise law in Canada too | LawSikho", face="chat",
  theme=dict(ac="#1D3A6B", ac2="#E6ECF6", bg="#F1ECE4"),
  callout="Experienced advocates?", dyk=['online','session','cost','notdegree'], head="Practise law in Canada too.",
  chat=[("fr","You can write Canada's exams from India?","9:41 PM"),("me","Yes. Online. A session every month.","9:42 PM"),("fr","And my chamber?","9:42 PM"),("me","Stays open. You study around your cause list.","9:43 PM")],
  sym_eyebrow="You may recognise this", sym_h="You built a practice. Canada keeps coming up.",
  sym_p=["You are in court every week and your chamber runs on you. Every few months the thought returns: could I practise in Canada too?","Then the next hearing arrives and the thought goes. You assume the route means leaving your practice."],
  out_h="Practise law in Canada too, without closing your chamber",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.","Choose exam months around your cause list.","Keep your Indian practice running while you study.","Leave day 3 with a plan on paper."],
  fail_h="You have probably tried these",
  fail=[("Asking around","Everyone has a half answer. One says two years, another says five. Nobody shows you the order."),("Reading old forum threads","Mixed advice, no dates, and no way to tell which part still applies."),("Waiting for a quiet month","A quiet month does not come in court. The exams are online, and a session is held every month, so you do not need a quiet month.")],
  reframe_h="The issue is not effort. It is a route you have never seen laid out.",
  reframe_p=["You already work harder than most people who qualify abroad. What is missing is the order of the steps and where they fit around your cause list.","Canada outside Quebec runs on common law, the system you practise in. The NCA exams still test Canadian law, so you study. But you study as someone who reads statutes and cases for a living. Source: Justice Canada."],
  cost_h="Another year of someday", cost_p=["The NCA path takes time: ten months at the fastest, about two years for the average candidate.","The date you start is the only part you control."], cost_src="Source: nca.legal.",
  art_h="A plan with your cause list in it", art_t="Your exam plan (sample)",
  art_rows=[("Month 1","Choose your first NCA exam"),("Months 2 to 4","Study on court light days"),("Month 5","Write your first exam, online"),("After","Bar licensing for your province")],
  long_h="Two practices, one qualification at a time", long_li=["A Canadian qualification added to your Indian licence.","The option to practise in Canada, now or later.","A chamber that kept running while you studied."],
  p2_h="Lawyers from India who started the same way", stories=[S_NAV, S_YAS],
  impl=BASE_IMPL, lang_h="Say it to your chamber, or a friend",
  lang_q="The NCA exams are online, from India, with a session every month. I am finding out the whole route for Rs 10, without touching my practice.",
  next_h="Pay Rs 10. Join on Saturday."),
"lp_associates": dict(
  title="Law firm associates: pick the month, qualify in Canada | LawSikho", face="calendar",
  theme=dict(ac="#5B2C83", ac2="#EFE6F7", bg="#F4EEFA"),
  callout="Law firm associates?", dyk=['session','time','versant','cert'], head="Pick the month. Qualify in Canada.", chat=None,
  sym_eyebrow="You may recognise this", sym_h="Your calendar belongs to your billable hours.",
  sym_p=["Your week is targets, client calls and late nights. You are good at the job. And one question keeps getting parked: what if I qualified in Canada?","The parking is not laziness. Every plan you have seen assumes you have free months."],
  out_h="A Canadian qualification that fits your own calendar",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.","Choose your exam month around your billable hours.","Study one exam at a time, from India.","Leave day 3 with a calendar on paper."],
  fail_h="You have probably tried these",
  fail=[("Waiting for a slow quarter","A firm calendar does not stay slow for long. The plan has to fit a busy year."),("Looking at a Canadian degree","A degree abroad is one route. There is another: the NCA exams, written from India."),("Asking a senior","They know the firm. They may not know the Canadian route.")],
  reframe_h="The issue is not effort. It is where the exams sit in your year.",
  reframe_p=["The NCA exams are online, with a session every month and each subject every third month, so you choose when. One exam at a time is a plan that fits a job.","You already draft and review for a living. Canada outside Quebec uses common law, like India, so the habits you built carry over. Source: Justice Canada."],
  cost_h="A year with no plan", cost_p=["If you plan this month, you choose your first exam month. If you do not, your calendar chooses for you.","The NCA path takes ten months at the fastest and about two years on average."], cost_src="Source: nca.legal.",
  art_h="A 12 month exam calendar", art_t="Your exam calendar (sample)",
  art_rows=[("Month 1","Choose your first NCA exam"),("Month 3","Your exam month, around billable hours"),("Month 4","Review, then pick the next exam"),("After","Bar licensing for your province")],
  long_h="A qualification that is yours, not your firm's", long_li=["A Canadian qualification built one exam at a time.","A choice of where to practise later.","A plan that never asked you to stop working."],
  p2_h="Lawyers who fitted the exams around a full time job", stories=[S_ARC, S_HEZ],
  impl=BASE_IMPL, lang_h="Say it to a colleague",
  lang_q="The exams are online, from India. I can pick my month around my billable hours. I am finding out the full route for Rs 10.",
  next_h="Choose Saturday. Pay Rs 10."),
"lp_fresh_grads": dict(
  title="Fresh out of law school: qualify as a lawyer in Canada | LawSikho", face="card",
  theme=dict(ac="#B2451E", ac2="#FBE7DB", bg="#FBEFE6"),
  callout="Fresh out of law school?", dyk=['online','time','ielts_skip','lawsociety'], head="Qualify as a lawyer in Canada.", chat=None,
  sym_eyebrow="You may recognise this", sym_h="Your degree is done. Your plan is not.",
  sym_p=["You have an LLB and a long list of options. Friends are joining chambers or preparing for exams. You keep wondering about Canada, but nobody has shown you where to start."],
  out_h="Start a Canadian qualification in your first year out",
  out_li=["See the whole route: NCA exams, bar licensing, practice in Canada.","Know what your first exam could be.","Study one exam at a time, from India.","Leave day 3 with your first plan on paper."],
  fail_h="You have probably tried these",
  fail=[("Scrolling forums","Old threads and mixed advice. Hard to tell what still applies."),("Waiting to settle in first","The longer you wait, the more it feels like starting from zero."),("Planning a Canadian degree","That is one route. There is another: the NCA exams, written from India.")],
  reframe_h="The issue is not marks. It is not knowing the first step.",
  reframe_p=["You do not need a perfect plan. You need the order: NCA exams, then bar licensing, then practice.","Canada outside Quebec runs on common law, the same system you just studied. Source: Justice Canada."],
  cost_h="Starting early starts the clock early", cost_p=["The NCA path takes ten months at the fastest and about two years on average.","Starting in your first year out means your clock starts first."], cost_src="Source: nca.legal.",
  art_h="Your first plan, on paper", art_t="Your first year plan (sample)",
  art_rows=[("Month 1","Choose your first NCA exam"),("Months 2 to 5","Study, one exam at a time"),("Month 6","Write your first exam, online"),("After","Bar licensing for your province")],
  long_h="A Canada-qualified lawyer, one exam at a time", long_li=["A Canadian qualification added to your Indian degree.","A choice of where to practise later.","A start that did not wait for permission."],
  p2_h="Graduates and young lawyers who started early", stories=[S_SHU, S_YAS],
  impl=BASE_IMPL, lang_h="Say it to your friends",
  lang_q="The NCA exams are online, from India. I am finding out the whole route, from my LLB to practising in Canada, for Rs 10.",
  next_h="Start now. Pay Rs 10. Join on Saturday."),
}

for _c in CFG.values():
    _c.setdefault("mech", MECH); _c.setdefault("work", WORK)
report = ["# Landing page gaps (7 Oct 2026)\n", "Pay link: `#PAYMENT_LINK_PENDING` on every CTA. Wire it before launch.\n"]
for stem, c in CFG.items():
    page = build(c)
    open(os.path.join(HERE, "pages", stem + ".html"), "w").write(page)
    pv = os.path.join(HERE, "preview", stem + ".html")
    open(pv, "w").write(preview(page))
    g = gaps(page)
    report.append("\n## %s  (publish ready: %s)\n" % (stem, publish_ready(page)))
    for tag, txt in g: report.append("- **%s**: %s\n" % (tag, txt))
    # full-page render, then slice
    subprocess.run([HS, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=430,17000",
                    "--screenshot=" + os.path.join(HERE, "preview", stem + "_full.png"), "file://" + pv], check=True, capture_output=True)
open(os.path.join(HERE, "GAPS.md"), "w").write("".join(report))
print("built", list(CFG))
