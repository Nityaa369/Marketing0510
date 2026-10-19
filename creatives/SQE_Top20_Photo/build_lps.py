# Builds 20 SQE Community landing pages, one per ICP poster, on Virat's persuasion order (19 Oct 2026):
# 1 problem and why this is the investment, 2 twelve "did you know" reasons, 3 positioning and stories,
# 4 bonus: the money behind English law, then the offer and the only disclaimer at the end.
# Facts: Day 0, Day 1 and Day 2 decks of the SQE community (sources named on the page). Run: python3 build_lps.py
import os, re, html, base64
def img_uri(n):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos', n + '.jpg'), 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode()

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "landing_pages")
PAY = "#PAYMENT_LINK_PENDING"   # BLOCKER: real GrowthX funnel URL per page, test-buy in a browser
DATES = "7 live evenings, 8 PM IST"
PRICE = "Rs 100, including GST"

CSS = """*{box-sizing:border-box;margin:0;padding:0}
:root{--ac:%(ac)s;--soft:%(soft)s;--ink:#15130F;--mut:#4B463D;--bg:%(bg)s}
body{font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:var(--bg);line-height:1.6;font-size:18px}
.wrap{max-width:780px;margin:0 auto;padding:0 20px}
.brand{font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--ac)}
.who{display:inline-block;background:var(--ac);color:#fff;font-weight:900;font-size:15px;letter-spacing:.06em;text-transform:uppercase;padding:8px 14px;border-radius:8px;margin-top:14px}
h1{font-size:38px;line-height:1.12;margin-top:14px;letter-spacing:-.015em}
h1 em{font-style:normal;color:var(--ac)}
.lead{font-size:21px;font-weight:600;margin-top:14px}
.def{margin-top:12px;color:var(--mut)}
.hero img{width:100%%;border-radius:14px;margin-top:18px;display:block}
.del{margin:16px 0 0;padding:0;list-style:none}
.del li{padding:6px 0 6px 30px;position:relative;font-weight:600}
.del li:before{content:'\\2713';position:absolute;left:0;color:var(--ac);font-weight:900}
.terms{margin-top:16px;background:#fff;border:2px solid var(--ac);border-radius:10px;padding:12px 16px;font-weight:700}
.btn{display:block;text-align:center;background:var(--ac);color:#fff;font-weight:900;font-size:21px;padding:17px;border-radius:12px;text-decoration:none;margin-top:18px}
section{padding:32px 0;border-bottom:1px solid #E4DED2}
.n{font-size:12px;font-weight:900;letter-spacing:.14em;color:var(--ac);text-transform:uppercase}
h2{font-size:27px;line-height:1.22;margin:6px 0 12px}
h3{font-size:20px;margin-top:18px}
p+p{margin-top:12px}
.box{background:#fff;border-left:6px solid var(--ac);padding:14px 18px;margin-top:14px;border-radius:6px}
.big{font-size:22px;font-weight:800;background:var(--soft);padding:16px 18px;border-radius:10px;margin-top:14px}
.facts{counter-reset:f;list-style:none;margin-top:12px;display:grid;gap:10px}
.facts li{counter-increment:f;background:#fff;border:1px solid #E4DED2;border-radius:10px;padding:14px 16px 14px 62px;position:relative}
.facts li:before{content:counter(f);position:absolute;left:14px;top:12px;width:36px;height:36px;border-radius:50%%;background:var(--ac);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}
.facts b{display:block}
.steps{counter-reset:s;list-style:none;margin-top:12px}
.steps li{counter-increment:s;padding:12px 0 12px 52px;position:relative;border-top:1px solid #E4DED2}
.steps li:before{content:counter(s);position:absolute;left:0;top:10px;width:36px;height:36px;border-radius:50%%;background:var(--ac);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center}
.story{background:#fff;border:1px solid #E4DED2;border-radius:10px;padding:14px 16px;margin-top:12px}
.story b{color:var(--ac)}
.stat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.stat div{background:#fff;border-top:6px solid var(--ac);border-radius:8px;padding:12px 14px}
.stat strong{display:block;font-size:30px;line-height:1.1}
.src{font-size:13px;color:var(--mut);margin-top:8px}
.close{background:var(--soft);padding:34px 0;border:0}
.disc{font-size:13px;color:var(--mut);padding:26px 0 110px}
footer.pad{padding:0 0 110px}
.disc p+p{margin-top:8px}
.sticky{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:3px solid var(--ac);padding:10px 16px;display:flex;gap:12px;align-items:center;justify-content:center;z-index:9}
.sticky span{font-weight:800;font-size:15px}
.sticky a{background:var(--ac);color:#fff;font-weight:900;padding:12px 20px;border-radius:10px;text-decoration:none;white-space:nowrap}
%(extra)s
@media(max-width:520px){h1{font-size:30px}h2{font-size:23px}.sticky span{display:none}.stat{grid-template-columns:1fr}}
"""
# hero layout variants, so the 20 pages do not read as one template
VAR = {
 "A": "header.hero{background:var(--soft);padding:30px 0 30px;border-bottom:8px solid var(--ac)}",
 "B": "header.hero{background:var(--ac);color:#fff;padding:30px 0}header.hero .brand,header.hero h1 em{color:#FFD21F}header.hero .who{background:#fff;color:var(--ac)}header.hero .def{color:#fff;opacity:.92}header.hero .terms{color:var(--ink)}header.hero .btn{background:#FFD21F;color:#111}header.hero .del li:before{color:#FFD21F}header.hero .lead{color:#fff}",
 "C": "header.hero{background:#fff;padding:30px 0;border-top:12px solid var(--ac)}header.hero .hero-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:center}@media(max-width:640px){header.hero .hero-grid{grid-template-columns:1fr}}header.hero img{margin-top:0}",
 "D": "header.hero{background:var(--soft);padding:30px 0}header.hero h1{font-family:Georgia,'Times New Roman',serif;font-weight:700;font-size:42px}header.hero .lead{border-left:6px solid var(--ac);padding-left:16px}",
}

# ---- shared, sourced facts (Day 0, Day 1, Day 2 decks; sources printed) ----
F = {
 "single":  ("One exam, recognised worldwide.", "The SQE is the single national exam to qualify as a solicitor of England and Wales. It replaced the older routes and is open to qualified lawyers from other countries, including India.", "SRA"),
 "nodegree":("No UK degree is required.", "The route asks for a degree or an equivalent qualification in any subject, plus the SQE passes. Your Indian law degree counts.", "SRA, Qualified lawyers"),
 "india":   ("The written exams are taken in India.", "SQE1 and the written part of SQE2 run at Pearson VUE test centres, including six Indian cities. Only the SQE2 oral sittings require a trip to England or Wales.", "sqe.sra.org.uk, test centre locations"),
 "exempt":  ("Enrolled advocates can apply to skip SQE2.", "A qualified lawyer with at least two years of professional experience can apply to the SRA for an SQE2 exemption. If granted, it removes five half-days of assessment, the SQE2 fee and the UK trip. The SRA decides each case.", "sra.org.uk, SQE exemptions"),
 "noqwe":   ("No two years of UK work experience for you.", "Qualified lawyers do not need the two years of qualifying work experience that fresh graduates must complete.", "SRA, Qualified lawyers"),
 "sat":     ("16,200 and more candidates sat the SQE in 2024 to 2025.", "You are joining a route that thousands of lawyers already take every year.", "SRA, SQE assessment statistics 2024 to 2025"),
 "forty":   ("About 40 percent of global business and financial transactions run on English law.", "Parties choose it because the case law is mature and the courts are trusted.", "The Law Society of England and Wales, International Data Insights Report 2025, citing TheCityUK"),
 "lcia":    ("78 percent of LCIA arbitrations in 2024 were on English-law contracts.", "English law is also the single most common governing law in new ICC cases, and applies in a quarter of SIAC cases.", "The Law Society of England and Wales, International Data Insights Report 2025; LCIA, ICC and SIAC annual casework reports 2024"),
 "london":  ("London is the world's first-choice arbitration seat.", "34 percent of practitioners name it their preferred seat, and it was the most popular ICC venue in 2024.", "2025 International Arbitration Survey, Queen Mary University of London and White and Case"),
 "export":  ("UK legal services earn about GBP 11 billion a year abroad.", "The UK is the second largest legal market in the world, behind only the United States.", "The Law Society of England and Wales, International Data Insights Report 2025"),
 "hiring":  ("57 percent of UK law firms say they struggle to hire.", "56 percent of in-house teams report the same. A firm that cannot hire does not care where a qualified English-law lawyer sits.", "The Access Group, The 10 biggest challenges facing the legal profession"),
 "common":  ("You already think in common law.", "The Indian Contract Act of 1872 was drafted on English principles, and Indian tort law is largely uncodified English common law. The same cases you cite are on the SQE1 syllabus.", "Indian Contract Act, 1872; SRA, SQE1 Assessment Specification"),
 "mcq":     ("SQE1 is 360 multiple-choice questions.", "Two papers, FLK1 and FLK2, closed book, on a computer. It rewards method, which is what a daily MCQ habit builds.", "SRA, SQE1 Assessment Specification"),
 "dubai":   ("Gulf free-zone courts work in English on common-law lines.", "The DIFC courts in Dubai run an English-language, common-law system, and apply English precedent where their own code is silent.", "DIFC Courts, difccourts.ae"),
 "asia":    ("Singapore and Hong Kong hire English-law lawyers.", "English law is the second most common governing law at SIAC, and at the Hong Kong centre too.", "The Law Society of England and Wales, International Data Insights Report 2025; SIAC and HKIAC annual reports 2024"),
 "enforce": ("Awards under English law travel.", "Arbitral awards are enforceable in more than 170 countries under the New York Convention.", "UN Convention on the Recognition and Enforcement of Foreign Arbitral Awards, 1958"),
 "shortage":("The UK has fewer solicitors coming through.", "Duty solicitors fell 26 percent since 2017, 40 percent are now 55 or older, and only 6 percent are under 35. That is demand, and it is why firms look abroad.", "The Law Society, criminal duty solicitors campaign; Law Gazette"),
 "criminal":("Criminal law is one of the SQE1 subjects.", "FLK2 covers criminal law and practice. Your bail and trial work is a head start, not a handicap.", "SRA, SQE1 Assessment Specification"),
 "land":    ("Land law and property practice are on the exam.", "FLK2 covers property practice and land law. Titles, deeds and leases are familiar ground.", "SRA, SQE1 Assessment Specification"),
 "business":("Business law is the first paper.", "FLK1 covers business organisations, rules and procedures, plus contract and dispute resolution. Deal lawyers start ahead.", "SRA, SQE1 Assessment Specification"),
 "oneyear": ("Most learners pass SQE1 within about a year of starting.", "A typical plan is nine to twelve months of part-time study, around work. The next realistic window for most of this group is SQE1 in July 2027.", "SRA, SQE assessment dates"),
 "centres": ("You can sit the written exams in many countries.", "Pearson VUE runs the sittings at more than 100 test centres across 26 countries. Check your nearest centre on the SRA site.", "sqe.sra.org.uk, test centre locations"),
 "fee":     ("The exemption application costs GBP 265.", "That fee covers one or both exemption requests. If SQE2 is waived you avoid an assessment fee of about GBP 3,000.", "sra.org.uk, Apply for an individual SQE assessment exemption; SQE fees 2026"),
 "firstmover":("Lawyers who moved first did it from their desks.", "Our members cleared SQE1 while in practice in India, then applied for the exemption with their own work samples and reference letters.", ""),
 "llm":     ("An LLM does not qualify you. The SQE does.", "A foreign LLM does not by itself give practising rights in England and Wales. The SQE is the route, and your degree still counts toward the entry requirement.", "SRA, Qualified lawyers"),
 "inhouse": ("In-house counsel qualify too.", "The SRA counts professional legal work experience, not only courtroom practice, toward the two years for the exemption application.", "sra.org.uk, SQE exemptions"),
 "profile": ("Firms shortlist on profile before the interview.", "Day 5 builds your international profile: the LinkedIn, the CV and the work samples that get a response from UK and Gulf firms.", ""),
}
STORIES = {
 "sanjana": ("Sanjana Roy, Mumbai to London", "A corporate and banking lawyer practising out of Mumbai. She joined the November 2024 batch, obtained the SQE2 exemption in February 2025 on the strength of her Indian practice, cleared SQE1 in July 2025, and moved to London. She is now Vice President in the EMEA Investment Banking and M&A legal team at Citi."),
 "prajwala":("Prajwala K. H. Lagali, Bengaluru to the UK", "A commercial lawyer who wanted to live and work in the UK rather than service it from India. She joined the March 2024 batch, cleared SQE1 in July 2024 and obtained the SQE2 exemption in October 2024. She now lives in the UK and works as General Commercial Counsel and Data Protection Officer at eMed Healthcare."),
 "atif":    ("Atif Ahmed, independent practice to dual-qualified solicitor", "An independent lawyer in international business law with an online practice serving clients across six continents. He joined the August 2024 batch, secured the SQE2 exemption in November 2024, cleared SQE1 in July 2025, and was formally admitted as a Solicitor of England and Wales in October 2025. He now practises as a dual-qualified lawyer, India and England and Wales."),
 "ramana":  ("Ramana Deshmukh, Mumbai litigation to the Roll of Solicitors", "A litigation and dispute resolution lawyer in Mumbai. He joined the December 2022 batch, converted his court experience into the SQE2 exemption in December 2024, cleared SQE1 in January 2025, and was admitted as a Solicitor by the SRA in March 2025. Start to finish, under three years, while practising."),
 "ridima":  ("Ridima Gupta, Saraf and Partners", "An associate in the M&A team at Saraf and Partners. She cleared SQE1 in July 2024 while working full time at the firm. The qualification raised her standing on cross-border work in India before any move abroad."),
 "mili":    ("Mili Upadhyay, Gujarat High Court", "A practising advocate at the Gujarat High Court. She joined the August 2024 batch, secured the SQE2 exemption in March 2025 on her court practice, and cleared SQE1 in July 2025. She is now completing admission as a Solicitor of England and Wales, without leaving her Gujarat practice."),
 "nakashvir":("Nakashvir Singh Aulakh, Supreme Court and Punjab and Haryana High Court", "An advocate practising before the Supreme Court of India and the Punjab and Haryana High Court, an RGNUL Patiala graduate. He joined the March 2024 batch and cleared both SQE1 papers, FLK1 and FLK2, in his first attempt in July 2026. He is applying for the SQE2 exemption on his court practice and building a dual-qualified litigation and advisory practice from India."),
}

# ---- the 20 pages ----
P = []
def add(**k): P.append(k)
add(n=1, stem="litigating_advocates", var="A", ac="#14213D", soft="#E8ECF5", bg="#FBF9F4", who="For litigating advocates",
 h1="You argue in court every week. Now become a <em>UK solicitor</em> without pausing your practice.",
 lead="The written exams are taken in India. Your cause list keeps running while you qualify.",
 problem=["You are good in court. You win more than you lose. And each year looks like the last one: the same corridors, the same adjournments, the same fee pressure from clients who pay late. Roughly 60,000 law graduates enter the Indian market every year, all chasing the same clients, and reputation in Indian practice takes ten to fifteen years to compound.",
  "The problem is not your skill. It is the size of the market you are standing in. A lawyer in a market worth a few billion rupees and a lawyer in a market worth tens of billions of dollars are not playing the same game, even with identical ability.",
  "An English-law qualification does not replace your practice. It adds a second market to it. Clients today ask whether you are qualified under English law, not where you are sitting."],
 invest="For Rs 100 you get seven live evenings that show you the whole route, from registration to admission, and whether the SQE2 exemption is realistic for you. That is the cheapest due diligence you will ever do on a qualification that can double the market you serve.",
 facts=["single","india","exempt","common","forty","lcia","london","hiring","noqwe","mcq","oneyear","firstmover"],
 role="For a litigating advocate the first question is the SQE2 exemption. If you are enrolled with a State Bar Council, hold practising rights in civil or criminal litigation and have two years behind you, you can apply on your own court work, with a certificate of good standing and reference letters from a senior. Day 2 walks the four gates the SRA checks. Day 6 reviews your draft reference letter line by line.",
 stories=["mili","nakashvir","sanjana"], photo="01")
add(n=2, stem="experienced_advocates", var="D", ac="#0F3D2E", soft="#E6F0EA", bg="#F7F6F0", who="For experienced advocates",
 h1="You have built a practice in India. Now add a <em>UK solicitor qualification</em> and keep the practice running.",
 lead="Your years in court are the evidence the SRA looks at for the SQE2 exemption.",
 problem=["Ten or fifteen years in, your name carries weight in your city. That is also the ceiling: your fees are set by what your local market can pay, and growth means more hours of the same work.",
  "Most senior advocates assume a foreign qualification means stopping, moving and starting again. For an enrolled advocate with years of practice the route is the opposite. Your experience is the asset. The SRA can waive the practical exam, SQE2, on the strength of it.",
  "That leaves one written exam, taken in India, around your practice."],
 invest="Seven live evenings at Rs 100 will tell you, with the SRA's own criteria, whether your practice already qualifies you for the exemption. If it does, the hardest part of the route is already behind you.",
 facts=["exempt","noqwe","india","single","forty","export","hiring","common","fee","oneyear","firstmover","london"],
 role="For an experienced advocate the exemption file is everything: a certificate of good standing from your Bar Council, proof of qualification, redacted work samples, and supervisor reference letters that confirm dates, hours and practice areas. Day 6 is a launch lab where that draft letter is reviewed against the SRA list. Day 7 is live Q&A for the questions only you can ask.",
 stories=["nakashvir","ramana","prajwala"], photo="02")
add(n=3, stem="newly_enrolled", var="B", ac="#0B4F5C", soft="#E3F3F5", bg="#F4FAFA", who="For newly enrolled advocates",
 h1="You have just enrolled. Start your <em>UK solicitor qualification</em> in your first years of practice.",
 lead="Sit SQE1 while you build your practice. Apply for the SQE2 exemption once your two years are done.",
 problem=["The first years at the bar are the leanest. You are learning the courts, earning little and watching seniors take the interesting work. Everyone tells you to wait your turn.",
  "There is a second clock running. The SQE2 exemption needs two years of experience, and SQE1 needs about a year of part-time study. Start both now and the two clocks finish together.",
  "By the time you are a three-year advocate, you could also be a solicitor of England and Wales, with a market most of your batch never considered."],
 invest="Rs 100 for seven live evenings is less than one court fee. It gives you a plan that uses the slow years instead of waiting them out.",
 facts=["single","nodegree","india","mcq","oneyear","exempt","common","sat","forty","hiring","profile","firstmover"],
 role="For a newly enrolled advocate the plan is sequence: SQE1 first, exemption application at the two-year mark, admission after both. Day 2 sets the timeline. Day 3 is a mock SQE1 on negligence, a topic you already know. Day 4 maps the careers that open after qualification.",
 stories=["ridima","atif","sanjana"], photo="03")
add(n=4, stem="criminal_lawyers", var="C", ac="#5B1425", soft="#F6E6EA", bg="#FBF5F3", who="For criminal lawyers",
 h1="Your weeks run on bail and trial dates. Now become a <em>solicitor of England and Wales</em> and work beyond one court.",
 lead="Criminal law is on the SQE1 syllabus. Your trial experience counts toward the SQE2 exemption.",
 problem=["Criminal practice is relentless. Bail at ten, a trial at two, a remand at five, and clients who cannot always pay. Your skill is real, and it is locked to one court complex.",
  "England and Wales has the opposite problem. The number of duty solicitors has fallen by a quarter since 2017, four in ten are over 55 and only six in a hundred are under 35. Whole counties have no junior criminal solicitor at all.",
  "A qualified criminal advocate from India, with English-law qualification, walks into that gap with exactly the skills it needs."],
 invest="For Rs 100 you learn whether your criminal litigation rights are the practice area the SRA accepts for the exemption. They are on the SRA's list. Seven evenings will show you how to evidence it.",
 facts=["criminal","shortage","exempt","india","single","noqwe","common","mcq","hiring","oneyear","firstmover","export"],
 role="For a criminal lawyer the SRA lists criminal litigation as one of the practice areas that can support an SQE2 exemption. Your bail applications, trials and appeals are the work samples. Day 2 explains the four gates, Day 3 tests you on an SQE1 question, Day 6 reviews your reference letter.",
 stories=["ramana","mili","nakashvir"], photo="04")
add(n=5, stem="civil_consumer", var="A", ac="#1B3A8C", soft="#E6ECF9", bg="#F6F8FD", who="For civil and consumer court lawyers",
 h1="You argue contract and tort cases every month. Now become a <em>UK solicitor</em> for clients abroad.",
 lead="The contract and tort you argue every day are the SQE1 subjects you already know.",
 problem=["Civil practice in India is slow money. A consumer complaint or a contract suit can take years, and your fee arrives at the end of it. You spend your best hours on adjournments.",
  "The law you argue is English law by another name. The Indian Contract Act was drafted on English principles. Indian tort is English common law, uncodified. Negligence, nuisance and vicarious liability are the same cases.",
  "Which means the exam that opens a global market tests what you already practise, and the practice itself is your exemption evidence."],
 invest="Rs 100 for seven live evenings, including a mock SQE1 question on duty of care. You will see in one evening how much of the syllabus you already own.",
 facts=["common","single","india","exempt","mcq","forty","lcia","enforce","noqwe","hiring","oneyear","firstmover"],
 role="For a civil lawyer the SRA lists civil litigation as a qualifying practice area for the SQE2 exemption. Your pleadings, interim applications and judgments are the work samples. Day 3 of the community is a mock SQE1 session on negligence and duty of care, run by our mentors.",
 stories=["ridima","nakashvir","prajwala"], photo="05")
add(n=6, stem="property_conveyancing", var="D", ac="#3E5C2A", soft="#EAF0E3", bg="#FAF8F2", who="For property and conveyancing lawyers",
 h1="You already work on titles and deeds. Now become a <em>solicitor of England and Wales</em>.",
 lead="Property practice and land law are on the SQE. Your daily work is the syllabus.",
 problem=["Conveyancing in India is volume work. Title searches, sale deeds, lease registrations, and a fee that has not moved in years. The work is careful and it is undervalued.",
  "In England and Wales, property is a core solicitor practice area, and one of the areas where rural firms struggle hardest to recruit. The SRA lists property practice among the areas that can support an SQE2 exemption.",
  "Your title work is both your exam preparation and your exemption evidence."],
 invest="Seven live evenings for Rs 100 show you how land law sits inside SQE1 and how your conveyancing files become an exemption application.",
 facts=["land","exempt","single","india","noqwe","shortage","hiring","common","mcq","oneyear","firstmover","export"],
 role="For a property lawyer the exam maps directly: FLK2 covers property practice and land law. The SRA accepts property practice as a qualifying area for the exemption. Day 2 shows the mapping. Day 6 reviews the reference letter from the senior who supervised your conveyancing work.",
 stories=["ramana","atif","sanjana"], photo="06")
add(n=7, stem="nclt_banking", var="B", ac="#4A1D5C", soft="#EFE6F3", bg="#FAF7FC", who="For NCLT and banking lawyers",
 h1="You appear before the tribunal. Now become the lawyer for <em>cross-border finance disputes</em>.",
 lead="Cross-border finance contracts choose English law. Qualify in it.",
 problem=["Insolvency and banking work in India is sophisticated and it is domestic. The lender is Indian, the borrower is Indian, the tribunal is Indian. The international restructurings, the ones with foreign bondholders and English-law facility agreements, go to firms in London and Singapore.",
  "Those agreements are governed by English law because that is what the finance market trusts. About 40 percent of global business and financial transactions run on it.",
  "An NCLT practitioner who is also an English-law solicitor can sit on the international side of the same restructuring."],
 invest="Rs 100 for seven evenings that show you how your tribunal practice supports an SQE2 exemption and which cross-border roles open after qualification.",
 facts=["forty","single","exempt","india","business","lcia","enforce","export","noqwe","hiring","oneyear","profile"],
 role="For a banking or insolvency lawyer, Day 4 is the session that matters: career pathways after SQE, including finance and restructuring teams at international firms and in-house at banks. Day 2 covers the exemption on the strength of your civil litigation and business practice.",
 stories=["sanjana","nakashvir","ridima"], photo="07")
add(n=8, stem="arbitration", var="C", ac="#2F3E4E", soft="#E7EBEF", bg="#F6F7F8", who="For arbitration lawyers",
 h1="You do arbitration in India. Now become an <em>international arbitration lawyer</em>.",
 lead="Most international arbitrations run on English-law contracts. Qualify in the law the work runs on.",
 problem=["Domestic arbitration in India is a good practice. It is also a crowded one, and the cross-border matters, with the real fees, are run by English-law solicitors from London and Singapore.",
  "That is structural. 78 percent of LCIA cases in 2024 were on English-law contracts. English law is the most common governing law in new ICC cases and applies in a quarter of SIAC cases. London is the world's preferred seat.",
  "The pool of English-qualified arbitration lawyers is the bottleneck. You can be in it."],
 invest="Seven live evenings for Rs 100, starting with the Day 1 session on why English law runs global disputes and ending with a plan to qualify in it from India.",
 facts=["lcia","london","enforce","forty","single","india","exempt","common","export","noqwe","oneyear","profile"],
 role="For an arbitration lawyer the civil litigation and dispute resolution work you already do is the exemption evidence. Day 1 gives you the market data with sources. Day 4 maps the arbitration and disputes roles at international firms that hire English-qualified lawyers.",
 stories=["sanjana","atif","nakashvir"], photo="08")
add(n=9, stem="international_career", var="A", ac="#0D3B66", soft="#E3EEF8", bg="#F5F9FD", who="For lawyers who want an international career",
 h1="You have thought about working abroad for years. Now find out if a <em>UK solicitor qualification</em> is your way in.",
 lead="One qualification, recognised in the UK, the Gulf, Singapore and beyond. The written exams are taken in India.",
 problem=["Every year you tell yourself this is the year. Then the question stops you: which country, which exam, which cost, and will it even be recognised. So nothing moves.",
  "Here is the mistake most lawyers make. They think migration first, then qualification. Move, hope, and pay for it with visa pressure. Qualification first is the durable order: earn under English law from wherever you are, and move only if it suits.",
  "The SQE is the qualification that travels. England and Wales, the UAE free zones, Singapore and Hong Kong all run English-law work."],
 invest="Rs 100 for seven evenings that answer the question you have carried for years: is this real for someone like me, and what are the twelve months after yes.",
 facts=["single","nodegree","india","centres","forty","export","dubai","asia","exempt","hiring","profile","oneyear"],
 role="If you want an international career, Day 1 shows where an England and Wales qualification is recognised and which markets are hiring. Day 4 maps the roles. Day 5 builds the profile that gets a reply from a foreign firm.",
 stories=["sanjana","prajwala","atif"], photo="09")
add(n=10, stem="dubai_gulf", var="B", ac="#0E5A5A", soft="#E2F0EF", bg="#F7F3E8", who="For lawyers who want to work in Dubai or the Gulf",
 h1="You want legal work in the Gulf. Now qualify in the <em>English law</em> its courts and contracts run on.",
 lead="DIFC courts work in English on common-law lines. An England and Wales qualification is the credential they recognise.",
 problem=["You have seen friends move to Dubai and come back with the same story: good life, but legal work behind a wall. Without a recognised qualification, Indian lawyers end up as paralegals or in compliance roles.",
  "The Gulf's commercial legal work sits in free zones with their own English-language, common-law courts. The DIFC in Dubai applies English precedent where its own code is silent. The firms there hire English-qualified lawyers.",
  "Qualify in English law from India and the Gulf opens as a lawyer, not as support staff."],
 invest="Seven evenings for Rs 100, including the Day 1 session on the Gulf and Singapore markets and the route to qualify without leaving India.",
 facts=["dubai","single","india","forty","lcia","enforce","export","nodegree","exempt","hiring","profile","oneyear"],
 role="If the Gulf is your goal, Day 1 covers the free-zone courts and what they recognise. Day 4 maps in-house and firm roles in the UAE. Day 5 builds a profile aimed at Gulf employers, who shortlist on qualification first.",
 stories=["prajwala","sanjana","ramana"], photo="10")
add(n=11, stem="england", var="D", ac="#1F2A5A", soft="#E6E8F3", bg="#F8F3EE", who="For lawyers who want to practise in England",
 h1="You want to practise law in England. Start the qualification <em>now, from India</em>.",
 lead="Written exams in Indian cities, then SRA admission. You land with the hard part done.",
 problem=["Most lawyers who want England plan it backwards: get there first, then figure out the qualification. That means unpaid years, visa pressure and a job below your level while you study.",
  "The SQE lets you reverse the order. SQE1 is written in India. The SQE2 exemption, if granted, removes the only part that needs a UK trip. You can arrive already qualified, or close to it.",
  "And England needs you. 57 percent of firms report difficulty hiring, and the solicitor pipeline outside London has thinned for a decade."],
 invest="Rs 100 for seven live evenings that lay out the exact route from registration to the Roll of Solicitors, in order, with the SRA's own rules.",
 facts=["single","india","exempt","noqwe","hiring","shortage","export","nodegree","mcq","oneyear","profile","firstmover"],
 role="If England is the plan, Day 2 is the session on the route: mySRA account, SQE1 booking, exemption application, character and suitability, admission. Day 4 covers where the jobs are, including regional firms that cannot fill roles.",
 stories=["atif","ramana","prajwala"], photo="11")
add(n=12, stem="singapore_hk", var="C", ac="#25313A", soft="#E4ECEE", bg="#F2F8F8", who="For lawyers who want to work in Singapore or Hong Kong",
 h1="You want an Asian legal hub. Now become an <em>English-law lawyer</em> those hubs hire.",
 lead="English law is the second most common governing law at the Singapore and Hong Kong arbitration centres.",
 problem=["Singapore and Hong Kong are closer, familiar and full of Indian professionals. The legal roles there, though, go to lawyers with a recognised common-law qualification.",
  "Both hubs run on English-law work. A quarter of SIAC cases apply English law, and it is the second most common governing law in Hong Kong as well. International firms in both cities staff those matters with English-qualified lawyers.",
  "An England and Wales qualification earned from India is the credential that moves you from the Indian desk to the international one."],
 invest="Seven evenings for Rs 100 that cover the Asia markets on Day 1 and the route to qualify in English law from India.",
 facts=["asia","lcia","enforce","single","india","forty","export","nodegree","exempt","hiring","profile","oneyear"],
 role="If Singapore or Hong Kong is your target, Day 1 covers both markets with the casework data. Day 4 maps the roles. Day 5 builds a profile for international firms, who shortlist on qualification and work samples.",
 stories=["sanjana","ridima","nakashvir"], photo="12")
add(n=13, stem="living_abroad", var="A", ac="#5A3A22", soft="#F3E8DF", bg="#FCF4EC", who="For Indian lawyers living abroad",
 h1="You moved abroad. Now qualify as a <em>UK solicitor</em> from where you live.",
 lead="SQE exams run at test centres in more than 26 countries. Your Indian enrolment still counts.",
 problem=["You moved for family or for a partner's job, and your law degree came with you as a line on a CV nobody reads. Local requalification looks like starting again.",
  "The SQE is different. It is open to qualified lawyers from other countries, it does not need a UK degree, and the written exams run at Pearson VUE centres in more than 100 locations across 26 countries.",
  "If you are an enrolled advocate with two years of Indian practice behind you, you can also apply for the SQE2 exemption from abroad."],
 invest="Rs 100 for seven live evenings, from wherever you are, that show you the route and whether your Indian experience already covers the practical exam.",
 facts=["centres","single","nodegree","exempt","noqwe","forty","export","dubai","asia","hiring","profile","oneyear"],
 role="If you live abroad, the sessions are live online in the evening, Indian time; check the schedule against your time zone. Day 2 covers the exemption file, which can be assembled from India by post. Day 5 builds a profile for the country you are in.",
 stories=["prajwala","sanjana","atif"], photo="13")
add(n=14, stem="llm_abroad", var="B", ac="#5C1A33", soft="#F4E4EA", bg="#FBF3EA", who="For lawyers with an LLM from abroad",
 h1="You studied law abroad. Now turn that degree into a <em>UK solicitor qualification</em>.",
 lead="An LLM is a degree. The SQE is the licence. Your LLM counts toward the entry requirement.",
 problem=["You spent a year and a serious sum on an LLM. It was a good year. It did not give you practising rights anywhere, and in India it is another line on the CV.",
  "A foreign LLM does not by itself qualify you to practise in England and Wales. The SQE does. And the SQE route accepts your degree toward its entry requirement, so the LLM is not wasted; it is the first half of a qualification you never finished.",
  "If you are also an enrolled advocate with two years of practice, the SQE2 exemption may cover the practical exam."],
 invest="Seven evenings for Rs 100 that show you how to finish what the LLM started, without a second year abroad.",
 facts=["llm","single","nodegree","india","exempt","mcq","forty","export","hiring","profile","oneyear","sat"],
 role="If you hold an LLM, Day 2 explains what counts and what does not, in the SRA's own words. Day 4 maps the careers your combined profile opens. Day 5 turns the LLM plus SQE into a profile international firms read.",
 stories=["ridima","sanjana","ramana"], photo="14")
add(n=15, stem="associates", var="D", ac="#12307A", soft="#E4EAF8", bg="#F5F7FD", who="For law firm associates",
 h1="You are good at your job, and the cross-border work goes elsewhere. Now <em>qualify to do it yourself</em>.",
 lead="Prepare around your billable hours. The written exams are taken in India.",
 problem=["You draft well, you close on time and you are trusted by partners. Then a cross-border matter comes in and it goes to the London office, or to an English-qualified lateral hire.",
  "That is not about ability. It is about qualification. Clients on international matters want a lawyer qualified under English law on the file.",
  "An associate who adds that qualification, from inside the firm, is the one the partners send the cross-border work to."],
 invest="Rs 100 for seven live evenings at 8 PM, after the day's billing, that give you a plan to qualify around your job.",
 facts=["forty","single","india","exempt","inhouse","business","hiring","export","noqwe","oneyear","profile","firstmover"],
 role="For an associate the exemption question is whether your firm work counts. The SRA counts professional legal work experience in a relevant practice area, with a supervising lawyer's reference. Day 2 sets the test. Day 6 reviews the reference letter your partner would sign.",
 stories=["ridima","sanjana","nakashvir"], photo="15")
add(n=16, stem="corporate_ma", var="C", ac="#22303C", soft="#E6EAEE", bg="#FAF5E8", who="For corporate and M&A lawyers",
 h1="You work on deals every day. Now become the <em>English-law deal lawyer</em> global clients hire.",
 lead="Business law is the first SQE1 paper. The law most cross-border deals choose is the one you would qualify in.",
 problem=["Your deals are getting bigger and more international, and the governing law clause keeps saying England and Wales. When it does, the English-qualified lawyer takes the lead and you take the Indian-law carve-out.",
  "About 40 percent of global business and financial transactions run on English law. That is why.",
  "Qualify in it and the lead on those deals is available to you."],
 invest="Seven evenings for Rs 100, including a mock SQE1 question on business law, the paper you are best placed to pass.",
 facts=["business","forty","single","india","exempt","inhouse","export","lcia","noqwe","hiring","oneyear","profile"],
 role="For a corporate lawyer the SRA lists business organisations, rules and procedures among the practice areas that can support an exemption. Your transaction documents, redacted, are the work samples. Day 3 tests you on an SQE1 question. Day 4 maps corporate roles at international firms.",
 stories=["ridima","sanjana","atif"], photo="16")
add(n=17, stem="in_house", var="A", ac="#0B5D3B", soft="#E3F1E9", bg="#F3F9F5", who="For in-house counsel",
 h1="You advise one company. Now become counsel that <em>global companies hire</em>.",
 lead="Take the written exams in India while you stay in your job.",
 problem=["In-house, your value is judged by one company. Your salary band is set by its HR, your growth by its org chart. Moving to a multinational, or to its UK or Gulf office, needs a qualification they recognise.",
  "56 percent of in-house legal teams in the UK report hiring pressure. They want counsel who can own English-law contracts, not just review them.",
  "The SRA counts in-house legal work toward the SQE2 exemption, so your years in the company are evidence, not a gap."],
 invest="Rs 100 for seven evenings after work that show you how your in-house experience fits the SRA's route, and which global counsel roles open after it.",
 facts=["inhouse","hiring","single","india","exempt","forty","business","export","noqwe","oneyear","profile","firstmover"],
 role="For in-house counsel, Day 2 covers how professional legal work experience counts for the exemption, including the reference from your general counsel. Day 4 covers in-house pathways at multinationals. Two of our featured members hold exactly those roles today.",
 stories=["sanjana","prajwala","ramana"], photo="17")
add(n=18, stem="practice_owners", var="B", ac="#4A3320", soft="#F1E8DC", bg="#F8F1E4", who="For lawyers who own a practice",
 h1="You built your own practice. Now <em>add a UK arm</em> to it.",
 lead="Qualify as a solicitor of England and Wales from your own chamber. Your clients' cross-border work stays with you.",
 problem=["You built a practice from nothing. Now your clients grow, do business abroad, sign English-law contracts, and for that work they go to someone else.",
  "A practice owner who is also an English-law solicitor keeps that work, and can take on referral work from UK firms that cannot hire.",
  "Your seniority is also your exemption evidence: years of practice, your own name on the letterhead, and the SRA's list of qualifying practice areas."],
 invest="Seven evenings for Rs 100, with a live Q&A on Day 7 for the questions a practice owner has: regulation, insurance, how members set up cross-border work.",
 facts=["exempt","noqwe","single","india","forty","export","hiring","enforce","common","oneyear","firstmover","fee"],
 role="For a practice owner the question is practical: who signs your reference letter when you are the senior. Day 2 and Day 6 cover that, including references from opposing counsel, judges and clients. Day 7 is live Q&A with the mentors.",
 stories=["mili","ramana","atif"], photo="18")
add(n=19, stem="ip_data_privacy", var="D", ac="#4B2C8F", soft="#ECE6F7", bg="#F6F3FB", who="For IP and data privacy lawyers",
 h1="You advise on rules that cross borders. Now qualify in the <em>English law</em> behind much of it.",
 lead="Tech, IP and data work is global. The qualification that travels is English law.",
 problem=["Your clients are global by default: a SaaS company with EU users, a startup licensing IP to a UK partner, a data processor under three regimes. Your advice stops at the Indian border.",
  "The contracts those clients sign are English-law contracts more often than any other. The firms that advise on them hire English-qualified lawyers.",
  "Your specialism is rare and in demand. The qualification is what lets it travel."],
 invest="Rs 100 for seven live evenings, including the Day 4 session on tech, IP and privacy pathways after qualification.",
 facts=["forty","single","india","nodegree","exempt","inhouse","business","export","asia","hiring","profile","oneyear"],
 role="For an IP or privacy lawyer, Day 4 covers the technology and data roles at international firms and in-house, where one of our featured members is now a Data Protection Officer in the UK. Day 5 builds a profile around your specialism.",
 stories=["prajwala","sanjana","ridima"], photo="19")
add(n=20, stem="smaller_cities", var="C", ac="#4D5A1E", soft="#EDF0DF", bg="#F9F6E8", who="For lawyers in smaller cities",
 h1="You practise in a smaller city. Now qualify as a <em>UK solicitor</em> without moving anywhere.",
 lead="Written exams in six Indian cities. Live sessions every evening on your phone.",
 problem=["In a smaller city the ceiling is low and visible. The clients are local, the fees are local, and the lawyers who grow are the ones who leave for Delhi or Mumbai.",
  "There is a route that does not require moving. The SQE written exams are taken at test centres in six Indian cities. Preparation is reading, daily MCQs and live evening sessions. The exemption file is paper.",
  "And the UK's own shortage is in its smaller towns, where firms cannot fill roles. A qualified lawyer who already knows small-city practice is exactly who they need."],
 invest="Seven evenings for Rs 100, live online, no travel, that show you a qualification your city has never limited.",
 facts=["india","single","nodegree","shortage","hiring","exempt","common","mcq","oneyear","export","profile","firstmover"],
 role="For a lawyer in a smaller city the daily rhythm matters: a reading PDF at noon, five MCQs at two, the answer key at six, a case study at four, the live session at eight. All on WhatsApp and Zoom. Day 2 confirms your nearest test centre.",
 stories=["mili","atif","nakashvir"], photo="20")

PROG = """<ol class="steps">
<li><b>Day 0, Orientation.</b> How the community works, the material you get, and a plain introduction to the SQE.</li>
<li><b>Day 1, The global opportunity.</b> Where an England and Wales qualification is recognised, with sourced market data.</li>
<li><b>Day 2, SQE decoded.</b> Routes, fees, dates, test centres, and the SQE2 exemption for enrolled advocates, gate by gate.</li>
<li><b>Day 3, Mock SQE1.</b> A live session on a real syllabus topic with SQE-style questions and the structured answer method.</li>
<li><b>Day 4, Career pathways after SQE.</b> Firms, in-house, the Gulf, Singapore, and what each hires for.</li>
<li><b>Day 5, Build your international profile.</b> The CV, LinkedIn and work samples that get a reply.</li>
<li><b>Day 6, Launch lab.</b> Your draft exemption reference letter reviewed line by line against the SRA list.</li>
<li><b>Day 7, Live Q&amp;A.</b> Your questions, answered by the mentors.</li></ol>
<p class="src">Every day: a reading PDF at 12 PM, a 5-question MCQ poll at 2 PM, the answer key at 6 PM, a learner case study at 4 PM, and the live session at 8 PM. Live only, no recordings. Complete all seven days and you receive a certificate of participation.</p>"""

DISC = """<div class="disc wrap">
<p><b>Please read.</b> LawSikho is an independent education company. It is not part of, and is not endorsed by, the Solicitors Regulation Authority, the Law Society of England and Wales, Kaplan, Pearson VUE or any government body. Their requirements, fees, dates and test centre locations are set by them, change from time to time, and should be confirmed on their own websites before you register or apply.</p>
<p>The community teaches the route and a plan. It does not guarantee an exam result, an exemption decision, admission, a job, clients, a visa or immigration status. SQE exemptions are decided by the SRA case by case. Learner stories describe individual experiences and are not typical results. Market and economic figures are published data from the sources named, and are not a promise of earnings. Nothing on this page is legal or immigration advice.</p>
<p>Live online sessions only; there are no recordings. Price %s. Fee terms, including any refund, are stated at checkout.</p></div>""" % PRICE

def sec(k, title, body, n=None):
    nn = '<div class="n">%s</div>' % n if n else ''
    return '<section><!-- %s --><div class="wrap">%s<h2>%s</h2>%s</div></section>' % (k, nn, title, body)

def page(p):
    img = '<img src="%s" alt="">' % img_uri(p["photo"])
    head_inner = """<div class="brand">LawSikho · SQE Community</div>
<div class="who">%(who)s</div>
<h1>%(h1)s</h1>
<p class="lead">%(lead)s</p>
<p class="def">The SQE is the one exam that makes you a solicitor of England and Wales. It is open to Indian advocates, and the written parts are taken in India.</p>""" % p
    DEL = [["7 live evening sessions, one a day at 8 PM IST","The SQE2 exemption route explained gate by gate, with your file started","A mock SQE1 session plus daily MCQs with answer keys","Career pathways and your international profile"],
           ["One live session every evening for seven days, 8 PM IST","Whether you can apply to skip SQE2, checked against the SRA's four gates","A real SQE1 question worked live, and five MCQs a day with answers","Where qualified Indian lawyers get hired, and how to be shortlisted"],
           ["Seven evenings, live, two hours each, from your phone","Your exemption file started: the documents, the reference letter, the fee","The structured answer method for SQE1, practised on the syllabus","A profile that UK, Gulf and Singapore firms reply to"]][p["n"] % 3]
    terms = '<ul class="del">' + "".join("<li>%s</li>" % d for d in DEL) + '</ul>' + """
<div class="terms">%s · %s · Live only, no recordings · Certificate of participation</div>
<a class="btn" href="%s">Join the SQE Community for Rs 100</a>""" % (DATES, PRICE, PAY)
    if p["var"] == "C":
        hero = '<header class="hero"><div class="wrap"><div class="hero-grid"><div>%s</div>%s</div>%s</div></header>' % (head_inner, img, terms)
    else:
        hero = '<header class="hero"><div class="wrap">%s%s%s</div></header>' % (head_inner, img, terms)
    parts = [hero]
    # 1 problem and why this is the investment
    prob = "".join("<p>%s</p>" % x for x in p["problem"])
    prob += '<div class="big">Why this could be the most important investment you make this year</div><p>%s</p>' % p["invest"]
    parts.append(sec("problem", "Why you, and why now", prob, "1. The problem"))
    # 2 twelve did-you-know
    items = "".join('<li><b>%s</b>%s%s</li>' % (F[k][0], F[k][1], '<div class="src">Source: %s</div>' % F[k][2] if F[k][2] else '') for k in p["facts"])
    parts.append(sec("facts", "Did you know? 12 reasons this is worth your attention", '<ol class="facts">%s</ol>' % items, "2. Once you see it"))
    # 3 positioning, how we help, why us, stories
    INTRO = ["<p>LawSikho runs the Crack the SQE course and this low-cost entry to it: a 7-day community that puts the whole route in front of you before you spend on anything else. Two mentors run every session: Prem Deep Arora, lead mentor on SQE and strategy, and Arpana Sachdeva, community manager, who leads the orientation, the mock, the pathways and the Q&amp;A. Avlokit Yadav, counsellor, speaks to you one to one about your own roadmap.</p>",
             "<p>We are not a coaching centre selling a syllabus. The community exists so that you decide with the facts in hand: the SRA's rules, the real fees and dates, and a mentor who has walked Indian lawyers through the exemption file. Prem Deep Arora leads the strategy sessions. Arpana Sachdeva runs the orientation, the mock and the Q&amp;A. Avlokit Yadav calls you to map your own route.</p>",
             "<p>Why LawSikho: we have taken Indian lawyers through this route before, and the members featured below are the proof. Every session is live, with a mentor who answers your question, not a recording. Prem Deep Arora, lead mentor, decodes the exam and the market. Arpana Sachdeva, community manager, runs five of the seven sessions. Avlokit Yadav, counsellor, works with you one to one.</p>"][p["n"] % 3]
    pos = INTRO + """
<h3>What the seven days look like</h3>%s
<h3>What this looks like for you</h3><div class="box">%s</div>
<h3>Members who did it</h3>%s
<p class="src">Members of the LawSikho Crack the SQE programme. Individual experiences, not typical results.</p>""" % (PROG, p["role"], "".join('<div class="story"><b>%s.</b> %s</div>' % STORIES[s] for s in p["stories"]))
    parts.append(sec("us", "How we help, and why us", pos, "3. Our position"))
    # 4 bonus: the money behind English law
    BON = ["<p>This is the part most lawyers never see written down. English law is not only a qualification. It is one of Britain's largest exports, and the people delivering it are increasingly not sitting in England.</p>",
           "<p>Here is the brownie point. The qualification you are considering sits on top of a market, and the market is large, measured, and short of people.</p>",
           "<p>One more thing, and it is the thing that makes the rest worth it: the size of the market an England and Wales qualification lets you serve.</p>"][p["n"] % 3]
    TAIL = ["<p>On Day 1 the mentors walk through what that market pays and how a qualified Indian lawyer enters it: regional UK firms that cannot hire, Gulf free-zone firms, Singapore and Hong Kong practices, and international in-house teams. Salary ranges are shown with their sources in the session, not here, because they depend on the market, the role and you.</p><p>The return is four things, not one: income, time, optionality and risk control. A second market is a hedge against the first.</p>",
            "<p>Day 1 puts numbers to it, with sources: what regional UK firms, Gulf firms, Asian practices and in-house teams pay, and which of them hire from India. We keep the pay figures in the session because they depend on the role and the market, and a number on a page without its context misleads.</p><p>Think of the return in four layers: what you earn, the hours it takes, the doors it keeps open, and how exposed you are to one market. A second qualification improves all four.</p>",
            "<p>The Day 1 session shows the market in detail, with the pay ranges and their sources, for each route a qualified Indian lawyer can take: UK regional firms, the Gulf, Singapore and Hong Kong, and multinational in-house teams. We do not print those ranges here, because out of context they promise more than they should.</p><p>What a second market gives you is not only income. It is time, options and a hedge against one economy. That is the investment case.</p>"][p["n"] % 3]
    bonus = BON + """
<div class="stat"><div><strong>GBP 11bn</strong>UK legal services exports a year</div><div><strong>No. 2</strong>legal market in the world, after the US</div><div><strong>40%%</strong>of global business and financial deals under English law</div><div><strong>78%%</strong>of LCIA arbitrations on English-law contracts</div></div>
<p class="src">Sources: The Law Society of England and Wales, International Data Insights Report 2025 (citing TheCityUK); LCIA Annual Casework Report 2024.</p>
""" + TAIL
    parts.append(sec("bonus", "Bonus: the money behind English law", bonus, "4. The brownie points"))
    # offer and close
    close = """<section class="close"><div class="wrap"><div class="n">Your next step</div><h2>%s</h2>
<p>%s. %s. Live only, no recordings. A certificate of participation when you complete all seven days.</p>
<a class="btn" href="%s">Join the SQE Community for Rs 100</a>
<p class="src">%s</p></div></section>""" % (["Seven evenings. Rs 100. The whole route, in order.","Decide with the facts. Seven live evenings for Rs 100.","Your next twelve months, planned in seven evenings. Rs 100."][p["n"] % 3], DATES, PRICE, PAY,
   ["After payment you get the WhatsApp group link. The first reading PDF arrives at 12 PM on Day 0.","Pay, and the WhatsApp group link is on the confirmation screen. Day 0 starts with the orientation at 8 PM.","The join link arrives with your payment confirmation. Fill the profiling form and the counsellor calls you before Day 2."][p["n"] % 3])
    parts.append(close)
    parts.append('<footer class="pad"></footer>')
    parts.append('<div class="sticky"><span>%s</span><a href="%s">Join for Rs 100</a></div>' % (p["who"], PAY))
    css = CSS % dict(ac=p["ac"], soft=p["soft"], bg=p["bg"], extra=VAR[p["var"]])
    title = re.sub("<.*?>", "", p["h1"])
    return "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>%s · LawSikho</title><style>%s</style></head><body>%s</body></html>" % (html.escape(title), css, "".join(parts))

os.makedirs(OUT, exist_ok=True)
for p in P:
    h = page(p)
    open(os.path.join(OUT, "lp_sqe_%02d_%s.html" % (p["n"], p["stem"])), "w").write(h)
    words = len(re.sub("<[^>]+>", " ", h.split("<body>")[1]).split())
    print("%02d %-22s %s words" % (p["n"], p["stem"], words))
