# value_props.md data per ad: better job, buying pressure, awareness, hypothesis, pain score.
# pain_score order: severity | frequency | activation | reachability | fit. Not fitted to live cost.
DEFN = ("Contract drafting is writing the agreements a business signs: who does what, who pays, "
        "and who carries each risk.")
DELIV = {
 "01": "Co-founder agreement | NDA and confidentiality clauses | Client questions before drafting | A LinkedIn profile known for contracts",
 "02": "SAFE agreement | Term sheet | Co-founder agreement | Pitching startups directly",
 "03": "Vendor service agreement | Employment agreement | NDA | Pitching startups directly",
 "04": "Commercial lease | SaaS agreement | Vendor service agreement | Questions to ask a client",
 "05": "NDA red flags found with AI | Missing clauses in terms and conditions | Employment agreement | Vendor service agreement",
 "06": "IP licensing clause | SaaS agreement | Co-founder agreement | Pitching founders directly",
 "07": "GDPR-compliant privacy policy for UK small businesses | Pitching startups on LinkedIn | SaaS agreement | First article",
 "08": "Remote work monitoring policy | Employment agreement | Daily phone readings and quizzes | Evening live sessions",
 "09": "Employment agreement | Vendor service agreement | LinkedIn profile known for contracts | First marketplace listing",
 "10": "DPDPA privacy policy | GDPR privacy policy for UK small businesses | SaaS agreement | First marketplace listing",
 "11": "Non-compete clause | Employment agreement | Remote work monitoring policy | ESOP plan",
 "12": "Term sheet | SAFE agreement | Representations and warranties | ESOP plan",
 "13": "E-commerce terms and conditions | Cookie policy | DPDPA privacy policy | First published article",
 "14": "SaaS agreement | Vendor service agreement | Representations and warranties | Pitching startups directly",
 "15": "Parts of a contract | Joint development agreement | NDA | Employment agreement",
 "16": "Representations and warranties | IP licensing clause | Red flags found with AI | SaaS agreement",
 "17": "Co-founder agreement | ESOP plan | SAFE agreement | Term sheet",
 "18": "Commercial lease | Joint development agreement | Vendor service agreement | IP licensing clause",
 "19": "Parts of a contract | NDA | LinkedIn profile known for contracts | First published article",
 "20": "Client questions before a co-founder agreement | SaaS agreement | Pitching startups directly | LinkedIn profile known for contracts",
}
JOB = {
 "01": "Graduate as a contract drafting lawyer who already drafts for businesses and startups.",
 "02": "Become the contract drafting lawyer startups hire for founder and investor papers.",
 "03": "Build a first practice drafting contracts for businesses instead of waiting for court briefs.",
 "04": "Become the contract drafting lawyer businesses call, working at a desk on your own hours.",
 "05": "Move from preparing files for a lawyer to drafting contracts as the lawyer.",
 "06": "Become the lawyer businesses hire before they sign, drafting their startup contracts.",
 "07": "Draft contracts for startups and UK small businesses as a lawyer based in your own city.",
 "08": "Return to law as a contract drafting lawyer who works from home.",
 "09": "Become a contract drafting lawyer whose clients and work move with you to any city.",
 "10": "Draft contracts for Indian and UK businesses as a lawyer living abroad.",
 "11": "Become the lawyer companies hire to draft their employment contracts and HR policies.",
 "12": "Become the lawyer who drafts term sheets, SAFE agreements and investor contracts.",
 "13": "Become the lawyer who drafts the website terms, policies and contracts businesses sign.",
 "14": "Become the lawyer who drafts the SaaS and vendor contracts that close deals.",
 "15": "Become the contract drafting lawyer your LLB trained you to be, drafting for businesses.",
 "16": "Become the lawyer who drafts contracts for clients instead of reviewing them in a queue.",
 "17": "Become the lawyer startups hire to draft founder, ESOP and investor contracts.",
 "18": "Become the lawyer businesses hire for commercial contracts, beyond sale deeds and leases.",
 "19": "Start working as a contract drafting lawyer while still in college, with drafts to show.",
 "20": "Come back as a contract drafting lawyer with your own clients instead of a firm desk.",
}
PRESSURE = {
 "01": "Final exams end soon and the first job hunt starts; recruiters ask what you have drafted, not what you studied.",
 "02": "A degree with no practice yet: every month out of work makes the LLB harder to explain to an employer.",
 "03": "New enrolment means a thin brief list; court income builds slowly and depends on the cause list.",
 "04": "Junior chamber fees follow the cause list, so every adjournment moves the income and the hours.",
 "05": "A paralegal salary scale is fixed below the lawyers whose files you prepare, though you hold the same LLB.",
 "06": "Clients walk in only after a dispute, so matter-at-a-time income is irregular and dries up between cases.",
 "07": "Local rate cards are low in a smaller city and the bigger-paying business clients go elsewhere.",
 "08": "Returning after a career break with school hours to plan around; court timings do not fit caring duties.",
 "09": "Relocation after marriage reset the court practice to zero; a new bar means building from the queue again.",
 "10": "Relocated abroad with a visa that may limit local practice; Indian law skills sit unused in a new time zone.",
 "11": "HR roles hit a ceiling for LLB holders; the legal drafting is sent to outside counsel and paid there.",
 "12": "Banking pay rises slowly on a fixed scale while the deal papers go to lawyers paid per matter.",
 "13": "Content work is paid per article or per word; legal drafting pays for the same writing skill at a higher rate.",
 "14": "Sales targets and shift hours cap growth; the contracts that close the deals are drafted by someone else.",
 "15": "Back-office shift work on a fixed salary scale with no promotion path that uses the LLB.",
 "16": "LPO review is per document in a queue, on night shift rosters, with a capped salary scale.",
 "17": "Company secretary work is a filing calendar on a fixed scale; founders pay lawyers for the contracts.",
 "18": "Property work is per deed at local rates and dries up when the market slows.",
 "19": "Internships are unpaid and exam season is near; placements ask for drafted work before the degree ends.",
 "20": "Left a firm for family and lost the salary; a firm desk is hard to return to after a career break.",
}
AWARE = {
 **{k: "problem aware: knows the current path is slow; the page must define contract drafting and show the work before the offer" for k in ["01", "02", "03", "04", "19"]},
 **{k: "solution aware: already near contracts at work; skip the problem, show the documents they would draft and how clients are reached" for k in ["05", "06", "16", "17", "18"]},
 **{k: "unaware: has not seen drafting as a career from home; the page must show the field, the daily rhythm and the hours first" for k in ["08", "09", "10", "20"]},
 **{k: "unaware: sees the LLB as unused; the page must name drafting as legal work their current job already touches, then define it" for k in ["11", "12", "13", "14", "15"]},
 "07": "problem aware: knows smaller-city fees are low; the page must show that business clients can be reached remotely, with the UK route",
}
HYP = {
 "01": "Students think drafting comes after the first job, so showing drafts done before graduation should beat a generic career pitch.",
 "02": "Non-practising graduates think they need a firm first, so naming startups as the hirer should beat naming law firms.",
 "03": "New advocates assume a practice means court, so a business-client practice should read as a new route, not a side task.",
 "04": "Junior advocates value time over title, so desk hours should beat any status argument for this reader.",
 "05": "Paralegals do not see themselves as the drafter, so naming the LLB they hold should beat naming the skills.",
 "06": "Small-practice lawyers think of contracts as low-fee work, so 'before they sign' should beat a price argument.",
 "07": "Smaller-city lawyers assume clients must be local, so the UK and Bengaluru route should beat a remote-work pitch.",
 "08": "Returning women lawyers fear the hours, not the law, so one phone lesson a day should beat a career argument.",
 "09": "Relocated lawyers think practice restarts from zero, so 'work travels' should beat a skills pitch.",
 "10": "Lawyers abroad think Indian law is unusable there, so naming India and UK clients should beat naming the skill.",
 "11": "HR staff with an LLB do not see offer letters as legal drafting, so naming the documents they issue should beat naming law.",
 "12": "Banking staff see deals as finance, so naming the papers behind the money should beat naming contract law.",
 "13": "Content writers think legal drafting is a different craft, so 'your writing, applied' should beat a law-first pitch.",
 "14": "Sales staff think of contracts as paperwork after the deal, so 'contracts that close deals' should beat a law pitch.",
 "15": "BPO staff with an LLB feel it is too late, so starting from the parts of a contract should beat an advanced pitch.",
 "16": "LPO reviewers think drafting needs years at a firm, so 'you already read the clauses' should beat a beginner pitch.",
 "17": "CS professionals see founders' papers as filings, so naming the contracts behind them should beat naming compliance.",
 "18": "Property lawyers think commercial work is another field, so 'from lease to JDA' should beat a fresh-start pitch.",
 "19": "Interns think drafting is taught on the job, so 'show drafted work in college' should beat a placement pitch.",
 "20": "Lawyers who left a firm think a firm desk is the only way back, so 'your own clients' should beat a re-entry pitch.",
}
PAIN = {
 "01": "4 | 4 | 5 | 5 | 5", "02": "4 | 5 | 4 | 4 | 5", "03": "4 | 5 | 4 | 4 | 5", "04": "4 | 5 | 3 | 4 | 4",
 "05": "4 | 5 | 3 | 3 | 5", "06": "3 | 4 | 3 | 3 | 4", "07": "4 | 5 | 3 | 4 | 4", "08": "5 | 4 | 4 | 4 | 4",
 "09": "5 | 4 | 4 | 3 | 4", "10": "4 | 4 | 3 | 3 | 4", "11": "3 | 4 | 3 | 4 | 4", "12": "3 | 4 | 3 | 3 | 3",
 "13": "3 | 4 | 3 | 3 | 4", "14": "3 | 4 | 3 | 3 | 3", "15": "4 | 5 | 3 | 3 | 4", "16": "4 | 5 | 3 | 3 | 5",
 "17": "3 | 4 | 3 | 3 | 4", "18": "3 | 4 | 3 | 3 | 4", "19": "3 | 4 | 4 | 5 | 5", "20": "5 | 4 | 4 | 3 | 4",
}


def block(i):
    s, f, a, r, ft = [x.strip() for x in PAIN[i].split("|")]
    return (f"## {i}\nad: ads/cd_{i}.jpg\nlp: landing_pages/lp_cd_{i}.html\n"
            f"better_job: {JOB[i]}\nfield_definition: {DEFN}\ndeliverables: {DELIV[i]}\n"
            f"buying_pressure: {PRESSURE[i]}\nawareness: {AWARE[i]}\nhypothesis: {HYP[i]}\n"
            f"pain_score: severity {s} | frequency {f} | activation {a} | reachability {r} | fit {ft}\n")
