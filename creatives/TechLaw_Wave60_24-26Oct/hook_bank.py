import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave as W
ALT = {
"01":"Are you an LLB holder in a back-office job? You could build a career as a tech lawyer. Support work runs on service levels, and SLAs are tech law.",
"02":"Holding an LLB in HR? You could move into tech law. You have already sat on the buyer's side of software contracts.",
"03":"Holding an LLB in a bank job? You could become a fintech lawyer. Lending apps need people who know the banking half.",
"04":"Holding an LLB and writing for a living? You could draft policies as a tech lawyer. Plain writing is the hard part for most lawyers.",
"05":"LLB holder in sales? You could move into tech law. The work follows how a business sells, which you already know.",
"06":"For lawyers returning after a break: tech law could be your way back. The client sees your draft, not your CV.",
"07":"For lawyers who paused practice for family: tech law work comes one task at a time, on a laptop.",
"08":"For lawyers who moved city after marriage: tech law does not need your old court. It needs your drafting.",
"09":"For Indian lawyers living abroad: your drafting travels even when your licence does not. Start in tech law.",
"10":"For lawyers who left a firm for family: the contracts you drafted then are the skill tech companies need now.",
"11":"Cheque bounce lawyer? You could build a tech law career without pausing your practice. Notices and contract reviews use the same skill.",
"12":"Cyber fraud lawyer? You already know half of tech law. Learn the contracts behind the apps.",
"13":"Are you a consumer forum lawyer? You could become an e-commerce lawyer. Refund policies are consumer law, written in advance.",
"14":"Handling account freeze cases? You could become a fintech lawyer. You already know KYC from the court side.",
"15":"Criminal defence lawyer? You could start a tech law career beside your practice. Reading facts for gaps is how contracts are reviewed.",
"16":"Recovery lawyer? You could move into fintech law. Digital lenders need lawyers who know both sides of a loan.",
"17":"Family lawyer? You could add a tech law career without pausing your practice. Your clients' disputes already run through apps.",
"18":"Defamation lawyer? You could become a lawyer for creators and platforms. Influencer agreements and takedowns are drafting work.",
"19":"Labour lawyer? You could become a tech lawyer. Startups need contractor and IP assignment agreements before anything else.",
"20":"District court lawyer? You could start a tech law career from your own city. The work is done on a laptop.",
"21":"Junior advocate? In tech law, no senior is 20 years ahead of you. Be first, not junior.",
"22":"Just enrolled? You could start your career in tech law. Each small task becomes a work sample.",
"23":"Not from an NLU? In tech law, clients judge your draft, not your college.",
"24":"LLM done? You could put it to work as a tech lawyer. Draft a software contract with us, live.",
"25":"Preparing for judiciary? You could build a tech law career in about 2 hours a day, around your study.",
"26":"Junior in a chamber? Tech law could give you your own clients, not only your senior's files.",
"27":"Junior associate? You could move into a tech law career. Firm tech teams hire lawyers who can show tech contracts.",
"28":"Paralegal with an LLB? You could step up into tech law. Small US firms send out first drafts.",
"29":"Final-year law student? One finished privacy policy could break the no-experience loop.",
"30":"Legal researcher? You could turn research into a tech law career. The work starts with reading rules closely.",
"31":"In-house at a non-tech company? You could move into an in-house tech law career. Your vendor contracts are the starting point.",
"32":"Contract lawyer? You could become a tech lawyer. A software development agreement is still a contract.",
"33":"Banking lawyer? You could become a fintech lawyer. A lending app is a lending business with software in front.",
"34":"IP lawyer? You could move into tech law. Software is IP, licensed by the clause.",
"35":"Tax lawyer? You could add tech law. Software, SaaS and gaming companies need contract work too.",
"36":"Company secretary with an LLB? You could turn compliance work into a tech law career.",
"37":"Law teacher? You could practise tech law alongside your teaching, around your timetable.",
"38":"For lawyers between jobs: this is a good time to learn the work tech companies pay for.",
"39":"Senior advocate? In tech law the rules are new for everyone, and your judgement on risk counts.",
"40":"Document review lawyer? You could move up into tech law. You already review contracts at scale.",
"41":"Worried tech law needs coding? It does not. The work follows how a business makes money.",
"42":"Practising outside the big cities? Tech law work is done on a laptop, from your own city.",
"43":"After a career break? In tech law the client judges the draft, not the gap.",
"44":"Not from an NLU? Firm tech teams ask to see contracts you have drafted.",
"45":"Not ready to leave court? Start tech law around court hours, about 2 hours a day.",
"46":"Curious what tech law work looks like? On Day 1 you draft a software contract, clause by clause.",
"47":"Tech contracts full of jargon? Five words on Day 1 make most of them readable.",
"48":"Wondering if it is too late? The rules are new, so nobody has a head start.",
"49":"What do the 3 evenings cover? A software contract, tech business models, and a startup's terms.",
"50":"Want startup clients? Learn how lawyers reach founders by fixing their terms.",
"51":"Your Rs 10 seat is still open. The tech law bootcamp starts Saturday, 6 PM.",
"52":"Your seat is held. Restart in tech law this Saturday, from home.",
"53":"You started joining. Finish in a minute and bring your court skills into tech law.",
"54":"Live only, once. Be there when the tech law bootcamp starts on Saturday.",
"55":"Payment did not go through? Try UPI or card. Your seat is waiting.",
"56":"Saturday, 6 PM. No recordings. Set your reminder.",
"57":"Day 1: bring a notebook. You draft a software development agreement.",
"58":"Day 2: six ways tech companies make money, and the legal work in each.",
"59":"Day 3: review a startup's terms live and see how lawyers pitch the fix.",
"60":"Monday starts at 7 PM, not 6.",
}
def table(camps):
    out=["| # | Reader | Call-out | Prize line | Reason | Format | Alternate (question hook) |","| --- | --- | --- | --- | --- | --- | --- |"]
    for a in W.ADS:
        if a["camp"] in camps:
            out.append("| %s | %s | %s | %s | %s | %s | %s |" % (a["id"], a["reader"], a["callout"], a["head"], a["why"], a["fmt"], ALT[a["id"]]))
    return "\n".join(out)
if __name__=="__main__":
    c=sys.argv[1].split(",")
    print(table(c))
