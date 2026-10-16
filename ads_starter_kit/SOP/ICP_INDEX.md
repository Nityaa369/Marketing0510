# The ICP index — every audience this account has pointed an ad at

**Generated. Do not hand-edit — run `python -m adkit.icp --report`.**

538 shipped ads across 16 product lines, reduced to **455 distinct audiences**, each carrying its archetype, its verdict, and its live cost per result where one exists.

## Why this file exists

A blind test on 31 Aug 2026 ran the documented ICP method against three product
lines with no repo access. It found ~85% of the live audiences on Independent
Director and ~71% on Content Writing — both occupation-heavy lines — but only
**~32% on Women Remote**, whose live audiences are life situations. It also
re-proposed a practising-credential ICP that had already killed three kits.

The method generates occupations well. It is blind to **life situations** and to
**tail disciplines**, and it has no memory of what has been rejected. Those are
evidence problems, not instruction problems, which is what this index supplies.

**Read §2 (the situation vocabulary) and §4 (what has already failed) before
writing an ICP list.** Those two sections are the ones the method cannot generate.

**What "approved" means here.** Only Ramanuj's approvals count. Ramanuj, 31 Aug
2026: *"ignore the ones that i approved, they were finally not approved. only the
ones ramanuj approved became the final ads."* The 24 `ContentWriting_SectionA` ads
carry an in-house APPROVED label and are excluded from the verdict column for that
reason, matching `adkit/golden.py`. Their **audiences** are still indexed — who an
ad was aimed at is real evidence either way — they simply do not get to say
approved. A blank verdict means unknown, not bad: most ads were never given budget.

## 1. The shape of what has been built

| Archetype | | Ads | Index (1.00 = par) |
|---|---|---|---|
| **A** | an occupation, adding a line to what they already do | 272 | 0.98 |
| **B** | a life situation they are living in and can point at | 117 | 0.96 |
| **C** | an aspiration or abstract state | 37 | 1.05 |
| **D** | device-led, no ICP named | 47 | 1.22 |
| **E** | a broad population | 4 | 1.15 |
| **?** | unlabelled | 61 | - |

**51 of 538 ads (9%) are D or E** — device-led or a broad population. Those index 1.15 to 1.22 against a par of 1.00, so a meaningful share of everything ever built here was aimed at nobody in particular.

## 2. The situation vocabulary — 35 canonical life situations

**This is the section the method cannot produce from first principles**, and the
one to read before writing an ICP list. These are every life situation this account
has pointed an ad at, with the occupation stripped off: 88 shipped phrasings
collapse to 35 situations, because the same situation keeps being reused with a
different profession glued to the front (*lawyers* / *M.Sc holders* / *mothers*
restarting after a career break are one situation, not three).

**They travel across product lines far better than occupations do.** That is what
makes §2.1 useful: a situation proven on one line is a candidate for every other.

**restarting after a career break** — used on: patent, us-corporate-law, women-remote, us-accounting, sqe, ip-law, data-privacy

> She stopped working for a stretch, usually for family, and is now trying to get back into paid work in the field she trained for.
>
> **Pressure:** The gap on the CV grows every month she does not restart, and it is the first thing every employer reads.

**a decade out of work** — used on: women-remote

> The break is no longer a gap but an absence: the field has moved on, the old contacts are gone, and she can no longer picture what the working day would even look like.
>
> **Pressure:** Every year out makes the old qualification less usable, and she has no way back in through the door she left by.

**screened out for the resume gap** — used on: women-remote

> She is actively applying and being rejected before the interview, because the gap is the only thing the screen sees.
>
> **Pressure:** Applications are going out and nothing comes back, so the gap gets longer with every rejection.

**maternity leave about to end** — used on: women-remote

> She is still on paid leave with a return date on the calendar, and the job she goes back to is the one she left.
>
> **Pressure:** A fixed date: rejoin on the old terms, or resign and lose the income with nothing lined up.

**a free window while children are at school** — used on: women-remote

> The house empties for a fixed few hours each weekday and she has that window entirely to herself.
>
> **Pressure:** The window is already there and earning nothing, and it closes the moment the school bus returns.

**employed, with the evenings free** — used on: us-accounting, women-remote, patent

> She holds a full day job and has two or three usable hours after it, currently spent on nothing that pays.
>
> **Pressure:** The salary is fixed until the next appraisal, so the only unclaimed money is in the hours after work.

**family care sets the schedule** — used on: women-remote, us-corporate-law

> Someone at home depends on her daily, so any work she takes has to bend around feeding, school runs and care hours rather than the other way round.
>
> **Pressure:** Every fixed-hours job on offer is unavailable to her, so the qualification sits unused while the care years run.

**living on someone else's income** — used on: women-remote

> The household has money coming in, but none of it is hers, so every spend is a request.
>
> **Pressure:** She wants to pay for something specific herself and cannot, and asking is the only route she has.

**a degree and no paid work history** — used on: women-remote

> She was educated for a career she never started, and has run a household competently for years with nothing on paper to show for it.
>
> **Pressure:** The degree is old and unaccompanied by a single line of work experience, and it gets harder to explain each year.

**children grown and gone** — used on: women-remote

> The children she organised her days around are adults now, living elsewhere, and the day is suddenly empty.
>
> **Pressure:** The reason she stopped working has ended, and twenty working years are still sitting there unspent.

**raising children as the only earner** — used on: women-remote

> She is the sole adult providing for her children, with no second income behind her.
>
> **Pressure:** Every household cost lands on one person, and there is no one to absorb a bad month.

**paid a hobby rate for real work** — used on: content-writing

> She already does the work and gets paid for it, but at pocket-money or small-town rates that treat it as a pastime.
>
> **Pressure:** The rate has not moved and will not, because the buyers she can reach do not pay more.

**tried working from home and stopped** — used on: women-remote

> She actually started something from home, ran it for a while, and it petered out.
>
> **Pressure:** She has already spent the enthusiasm once, and a second false start is the one she cannot afford.

**does not believe remote work is real** — used on: women-remote

> She has seen work-from-home offers that turned out to be scams or empty promises, and now doubts any of it is genuine paid work.
>
> **Pressure:** Distrust is costing her the option itself, while the household need that made her look has not gone away.

**called back into the office** — used on: women-remote

> Her work now requires her physically in an office, with a daily commute attached, whether or not the work needs it.
>
> **Pressure:** Hours and childcare money are being spent on travel that was not being spent last year, and the mandate is not negotiable.

**health limits the working hours** — used on: women-remote

> A health condition caps how many hours she can work and when, regardless of what she is capable of doing in them.
>
> **Pressure:** Standard full-time roles are closed to her, so capability keeps earning nothing.

**retired and still wants to work** — used on: women-remote

> The salaried job is over and she has no employer, but she has decades of usable experience and time she does not want to spend idle.
>
> **Pressure:** Nobody is hiring at that age on payroll, so the experience is depreciating with nowhere to be sold.

**retirement a few years away** — used on: consulting, independent-director, senior-ai

> Still employed and senior, with a known date after which the salary, the title and the team all stop.
>
> **Pressure:** The income has a stop date already fixed, and the years left to build a replacement are countable.

**past forty, too senior to start over** — used on: us-accounting, sqe, women-remote

> Twenty years into a career, old enough that no one will hire them into a junior role and young enough that stopping is two decades away.
>
> **Pressure:** The market prices them out of entry roles and their own ladder has no rungs left, so the middle is where they stay.

**the ladder has stopped moving** — used on: hr, consulting

> The designation has not changed in years and the next one is not visibly on offer, whatever the work has been.
>
> **Pressure:** One appraisal decides the whole year's income, and it has decided the same thing several years running.

**the person everything escalates to** — used on: consulting, senior-ai

> Fifteen or twenty years deep, they are the one the hard problems reach and the office cannot function without, on the same salary as the people who send them the problems.
>
> **Pressure:** The expertise is real and priced at zero, because it is bundled into a salary that does not move when the difficulty does.

**the household runs on one salary** — used on: consulting

> A senior professional whose family expenses, EMIs and school fees all rest on a single employer's payroll.
>
> **Pressure:** One layoff, one restructure, and the entire household income is zero; there is no second stream behind it.

**someone else sets the rate and the hours** — used on: consulting, women-remote

> What the work is worth and when it must happen are both decided by an employer, a school timetable or a family schedule, never by her.
>
> **Pressure:** The price of her time is fixed by another party and has not risen, and she has no mechanism to change either number.

**deep into a competitive exam attempt** — used on: patent, sqe

> One or more years are being spent preparing full time for a government or academic entrance exam with a single-digit success rate.
>
> **Pressure:** Each attempt costs a year with no fallback qualification, and the age limit on the exam is closing.

**waiting on an exam result** — used on: women-remote

> The exam is written and the result is months away, so there is a stretch of empty time with the outcome out of her hands.
>
> **Pressure:** Months of dead time now, and if the result is bad she starts the next year with nothing added.

**before the first job** — used on: patent, content-writing, sqe

> Final year or just graduated, holding a degree and no work anyone has paid for yet.
>
> **Pressure:** The placement window opens on an empty CV, and the batch behind them arrives next year.

**a certificate but no paid work** — used on: content-writing, sqe

> The internship or the enrolment is complete and the paper is in hand, but no client or employer has paid them for the work yet.
>
> **Pressure:** The credential expires in value the longer it sits with no billable work behind it, and juniors qualify every year.

**the plan-A qualification that closed** — used on: patent, us-accounting

> They aimed at a big professional track, medicine or CA or CPA, and it did not happen, so they are somewhere adjacent with the years already spent.
>
> **Pressure:** Years and fees went into a track that ended in nothing transferable, and restarting it costs the same again.

**a degree unused in an unrelated job** — used on: patent

> They earn a living in sales, BPO or admin while the specialist degree they hold has never been used at work.
>
> **Pressure:** The degree gets staler and less credible every year it is not used, while the current job builds nothing that transfers.

**living outside a metro** — used on: us-accounting, sqe, women-remote, us-corporate-law

> They live and intend to keep living in a small town or tier-2 or tier-3 city, where the local market sets both the work available and the price of it.
>
> **Pressure:** The local rate is the ceiling, and the only way anyone here raises it is by moving, which they are not going to do.

**planning to move abroad** — used on: sqe

> They intend to emigrate and need a qualification that is recognised where they are going, because the Indian one is not.
>
> **Pressure:** Visa and age thresholds tighten past thirty, and the qualification takes years they have to start now.

**already abroad on a home-country qualification** — used on: sqe

> They are working overseas, in a role capped by the fact that their professional qualification is not the local one.
>
> **Pressure:** The ceiling abroad is set by the licence they do not hold, and the visa clock keeps running while they sit under it.

**doing the job without the credential** — used on: hr

> They already perform the function daily, but have no qualification in it, so the title and the pay lag the work.
>
> **Pressure:** The next role asks for the paper they do not have, and someone with the paper and less experience gets it.

**on contract, not permanent** — used on: hr

> They do the same work as the permanent staff on a fixed-term contract, with a renewal date instead of a career.
>
> **Pressure:** The contract ends on a known date and renewal is someone else's decision, made without them.

**just resigned with no plan** — used on: content-writing

> They have left the job already, without the next thing arranged.
>
> **Pressure:** The salary has stopped and savings are being spent, so whatever they build has to start paying within months.

### 2.1 Coverage — which situations have never been tried on which line

`+` means an ad has run for that situation on that line. A blank is an untested
combination, and the cheapest place to look for the next ICP: the situation is
already proven to be a real audience, it has simply never been pointed at this
offer. Check the offer genuinely fits before building — not every pairing makes
sense, and a situation with no plausible route to the product is still a no.

| Situation | academic writing | arbitration | consulting | content writing | data privacy | hr | independent director | ip law | patent | senior ai | sqe | tech law | us accounting | us corporate law | women remote |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| restarting after a career break |  |  |  |  | + |  |  | + | + |  | + |  | + | + | + |
| a decade out of work |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| screened out for the resume gap |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| maternity leave about to end |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| a free window while children are at school |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| employed, with the evenings free |  |  |  |  |  |  |  |  | + |  |  |  | + |  | + |
| family care sets the schedule |  |  |  |  |  |  |  |  |  |  |  |  |  | + | + |
| living on someone else's income |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| a degree and no paid work history |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| children grown and gone |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| raising children as the only earner |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| paid a hobby rate for real work |  |  |  | + |  |  |  |  |  |  |  |  |  |  |  |
| tried working from home and stopped |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| does not believe remote work is real |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| called back into the office |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| health limits the working hours |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| retired and still wants to work |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| retirement a few years away |  |  | + |  |  |  | + |  |  | + |  |  |  |  |  |
| past forty, too senior to start over |  |  |  |  |  |  |  |  |  |  | + |  | + |  | + |
| the ladder has stopped moving |  |  | + |  |  | + |  |  |  |  |  |  |  |  |  |
| the person everything escalates to |  |  | + |  |  |  |  |  |  | + |  |  |  |  |  |
| the household runs on one salary |  |  | + |  |  |  |  |  |  |  |  |  |  |  |  |
| someone else sets the rate and the hours |  |  | + |  |  |  |  |  |  |  |  |  |  |  | + |
| deep into a competitive exam attempt |  |  |  |  |  |  |  |  | + |  | + |  |  |  |  |
| waiting on an exam result |  |  |  |  |  |  |  |  |  |  |  |  |  |  | + |
| before the first job |  |  |  | + |  |  |  |  | + |  | + |  |  |  |  |
| a certificate but no paid work |  |  |  | + |  |  |  |  |  |  | + |  |  |  |  |
| the plan-A qualification that closed |  |  |  |  |  |  |  |  | + |  |  |  | + |  |  |
| a degree unused in an unrelated job |  |  |  |  |  |  |  |  | + |  |  |  |  |  |  |
| living outside a metro |  |  |  |  |  |  |  |  |  |  | + |  | + | + | + |
| planning to move abroad |  |  |  |  |  |  |  |  |  |  | + |  |  |  |  |
| already abroad on a home-country qualification |  |  |  |  |  |  |  |  |  |  | + |  |  |  |  |
| doing the job without the credential |  |  |  |  |  | + |  |  |  |  |  |  |  |  |  |
| on contract, not permanent |  |  |  |  |  | + |  |  |  |  |  |  |  |  |  |
| just resigned with no plan |  |  |  | + |  |  |  |  |  |  |  |  |  |  |  |

**466 untested situation-by-line combinations.** Most are wrong for their offer; the
point is that the list of candidates is finite, written down, and no longer has to
be re-invented from scratch every wave.

## 3. Occupations and disciplines (archetype A)

Grouped by line. **Split an occupation at the degree people actually hold**, not at
the sector — that rule is why `semicon_vlsi` and `agri_foodsci` beat a generic
science ICP by 1.5x to 2.4x.


**arbitration**

| Occupation | Verdict | Live |
|---|---|---|
| in-house company secretaries handling disputes | GOLDEN | - |
| junior lawyers drafting for a senior | GOLDEN | - |
| law students who have done moots | approved | - |
| litigators losing days to court adjournments | GOLDEN | - |
| practising lawyers with no arbitration brief yet | approved | - |

**content-writing**

| Occupation | Verdict | Live |
|---|---|---|
| agency copywriters priced for Indian clients | GOLDEN | - |
| agency writers who take client briefs | - | - |
| content creators who post their own work | approved | - |
| content writers fielding client texts after hours | - | - |
| content writers on per-word rates late at night | - | - |
| content writers paid per word | GOLDEN | - |
| content writers reading strategist job listings | approved | - |
| content writers surrounded by AI shortcut talk | - | - |
| content writers told AI replaced them | - | - |
| content writers wanting a strategist title in India | approved | - |
| content writers who already plan campaigns | approved | - |
| content writers who read client briefs daily | - | - |
| content writers whose clients haggle every rupee | - | - |
| editors rewriting other people's drafts | rejected | - |
| experienced writers whose per-word rate never moved | - | - |
| freelance writers building a client roster alone | - | - |
| freelance writers holding a founder's retainer | - | - |
| freelance writers juggling five small gigs | - | - |
| freelance writers paid per word | - | - |
| freelance writers who lost a retainer to AI | - | - |
| freelance writers with feast-and-famine months | - | - |
| freelance writers with many small clients | - | - |
| high-output freelance writers with flat income | - | - |
| in-house writers and content leads with backlogs | - | - |
| in-house writers climbing the writing promotion ladder | - | - |
| in-house writers collecting vague feedback | - | - |
| in-house writers doing everything but writing | rejected | - |
| in-house writers left as a team of one | - | - |
| in-house writers whose promotion has stalled | - | - |
| Indian content writers meeting difficult clients | - | - |
| Indian writers chasing clients on job platforms | - | - |
| Indian writers who want to bill in dollars | - | - |
| Indian writers working with European D2C brands | - | - |
| Indian writers working with US small businesses | - | - |
| journalists at outlets that keep shrinking | - | - |
| journalists filing stories at shrinking outlets | - | - |
| junior writers second-guessing every draft | - | - |
| PR and communications professionals writing releases | - | - |
| PR professionals with no number to report | - | - |
| proofreaders and copy editors | - | - |
| senior content writers stuck on the title ladder | - | - |
| senior writers, leads and editors on writing teams | - | - |
| SEO blog writers whose traffic is falling | - | - |
| SEO content writers who know page structure | - | - |
| social media managers stuck on daily posting | - | - |
| social media writers in India | - | - |
| social media writers who cannot explain results | - | - |
| solo in-house marketers writing everything | - | - |
| solo marketers running a brand's whole funnel | - | - |
| solo marketers running every part of campaigns | - | - |
| solo marketing executives at startups | - | - |
| teachers who explain for a living | - | - |
| teachers who explain things for a living | - | - |
| translators billing per word for brands | - | - |
| translators paid per word for brand copy | - | - |
| video creators who can hold attention | approved | - |
| writers argued down on word counts | rejected | - |
| writers asked to discount because AI helped | - | - |
| writers charging by the word | - | - |
| writers cleaning up AI drafts by the hour | - | - |
| writers doing a whole team's work alone | - | - |
| writers doing bulk product listings for flat fees | rejected | - |
| writers paid for words, not campaigns | - | - |
| writers paid per word in India | - | - |
| writers paid per word or in bulk | - | - |
| writers quoted per word or per article | - | - |
| writers scrolling job boards for shrinking gigs | - | - |
| writers stuck on captions and SEO tweaks | - | - |
| writers wanting portfolio proof, not a certificate | - | - |
| writers who cannot find better-paying clients | - | - |
| writers who cannot show what writing earned | rejected | - |
| writers who never saw AI content strategist defined | - | - |
| writers who only write one campaign piece | - | - |
| writers who receive briefs from someone else | - | - |
| writers who track their own word output | - | - |
| writers whose day is AI cleanup briefs | - | - |
| writers whose rates have never moved | - | - |
| writers whose samples get no reply | rejected | - |
| writers with no portfolio to show clients | - | - |

**data-privacy**

| Occupation | Verdict | Live |
|---|---|---|
| agency staff holding client customer lists | - | - |
| AI and ML engineers asked about training data | - | - |
| auditors selling audit days to repeat clients | - | - |
| BFSI operations staff under a regulator | - | - |
| BPO and KPO staff processing client data | - | - |
| broking and wealth staff holding investor records | - | - |
| chartered accountants testing client controls | - | - |
| clinical research staff taking documented consent | - | - |
| cloud and data engineers taking deletion tickets | - | - |
| coaching institute admissions teams with student leads | - | - |
| company secretaries running board and consent paperwork | - | - |
| diagnostic lab operators sending reports by chat | - | - |
| ecommerce operations staff across scattered customer systems | - | - |
| fintech lending app teams collecting borrower data | - | - |
| founders stuck in enterprise security questionnaires | - | - |
| gaming platform staff running age and KYC checks | - | - |
| GCC privacy staff running the parent's EU rules | - | - |
| healthtech product and ops staff moving patient data | - | - |
| HR and payroll staff holding employee records | - | - |
| in-house compliance officers | - | - |
| insurance brokers with a field agent force | - | - |
| IT security engineers running access and incident response | - | - |
| logistics ops staff running rider apps | - | - |
| LPO and translation staff handling foreign data | - | - |
| marketing and CRM managers owning the customer database | - | - |
| matrimonial and dating platform staff holding profiles | - | - |
| medical transcription and RCM staff in India | - | Rs 103.16 |
| mid-level managers looking for a specialism | - | - |
| payments company staff already doing data residency | - | - |
| payroll outsourcing providers running many clients' records | - | - |
| pharmacovigilance professionals handling named patient data | - | - |
| practising lawyers asked about the new law | - | - |
| procurement staff signing vendor contracts | - | - |
| product designers building the consent screen | - | - |
| recruitment and background-verification staff holding candidate documents | - | - |
| school and edtech administrators holding children's records | - | - |
| streaming platform data and advertising teams | - | - |
| TPA claims staff opening medical files | - | - |
| university administrators holding full student records | - | - |

**hr**

| Occupation | Verdict | Live |
|---|---|---|
| bank and BFSI HR running hiring verification | - | - |
| BPO HR staff hiring at huge scale | - | - |
| business owners hiring without an HR team | - | - |
| campus recruitment staff wanting their own firm | - | - |
| commission-based recruitment consultants | - | Rs 134.07 |
| compensation and HR data analysts in spreadsheets | - | - |
| hotel HR running rosters and trainee batches | - | - |
| HR helpdesk staff answering the queue | - | - |
| HRMS administrators cleaning data and chasing approvals | - | - |
| IT staffing recruiters submitting CVs to US clients | - | - |
| learning and development trainers building courses | - | - |
| logistics HR handling contractor and attendance records | - | - |
| ops managers landed with HR duties | - | - |
| pharma HR keeping audit-ready employee files | - | - |
| retail store HR handling multi-city joining papers | - | - |
| school and college HR hiring faculty | - | - |
| talent acquisition heads running a recruiter team | - | - |
| the HR person in a family business | - | - |

**independent-director**

| Occupation | Verdict | Live |
|---|---|---|
| CFOs and finance heads who read financial statements | approved | - |
| chartered accountants facing audit committees | - | - |
| company secretaries taking the board's minutes | - | - |
| corporate lawyers working the Companies Act | approved | - |
| CXOs who have spent years reporting to boards | approved | - |
| founders who have handed over the business | - | - |
| general counsel and in-house legal heads | - | - |
| HR heads and CHROs | - | - |
| in-house counsel and company secretaries | approved | - |
| independent consultants billing a day rate | - | - |
| litigators | approved | - |
| plant and operations heads | - | - |
| professors and academics | approved | - |
| public sector and bank general managers nearing retirement | - | - |
| retiring armed forces officers | approved | Rs 64.8 |
| senior managers who chair review meetings | approved | - |
| senior women CXOs without a board seat | - | - |
| serving CFOs and finance heads | - | - |

**ip-law**

| Occupation | Verdict | Live |
|---|---|---|
| law graduates who never practised | approved | - |
| law students still in college | approved | - |
| lawyer mothers working around school hours | approved | - |
| lawyers stuck mid career | approved | - |
| women lawyers in India | approved | - |
| women lawyers in India wanting remote IP work | approved | - |

**patent**

| Occupation | Verdict | Live |
|---|---|---|
| agriculture and food science graduates | - | Rs 131.49 |
| BAMS and ayurveda graduates | - | Rs 121.53 |
| biomedical and medical device engineers | - | - |
| biotech and life science researchers | - | - |
| biotech bench scientists and lab researchers | - | - |
| CRO and clinical research professionals | - | - |
| EV, battery and solar hardware engineers | - | - |
| industrial chemists on formulation lines | - | - |
| IT and software engineers | - | - |
| lawyers with a B.Sc or M.Sc behind the LL.B | - | - |
| lawyers with a B.Tech behind the LL.B | - | - |
| M.Tech holders in engineering | - | - |
| medical and scientific writers | - | - |
| pharma QA, QC, regulatory and PV staff | - | - |
| pharmacists working behind the counter | - | - |
| R&D engineers at companies that file patents | - | - |
| school teachers of physics, chemistry or biology | - | - |
| science and engineering research fellows on stipends | - | - |
| scientists in CSIR labs and industry R&D | - | - |
| VLSI and semiconductor design engineers | - | Rs 120.68 |

**sqe**

| Occupation | Verdict | Live |
|---|---|---|
| criminal litigators | - | - |
| disputes and litigation lawyers | - | - |
| experienced Indian lawyers in practice | - | - |
| indian lawyers wanting to migrate to the UK | approved | - |
| IP and technology lawyers | - | - |
| law firm associates | - | - |
| lawyers running their own practice or small firm | - | - |
| lawyers who draft and negotiate contracts | - | - |
| paralegals and unqualified legal support staff | - | - |

**tech-law**

| Occupation | Verdict | Live |
|---|---|---|
| courtroom litigators with drafting and cross skills | - | - |
| junior lawyers under senior advocates | - | - |
| litigators appearing in trial courts | - | - |

**us-accounting**

| Occupation | Verdict | Live |
|---|---|---|
| accountants doing entries, reconciliations and payroll | approved | - |
| accountants in their 40s and 50s | approved | - |
| accountants who only know Tally | approved | - |
| audit and accounts staff at CA firms | approved | - |
| B.Com graduates wanting dollar accounting work | approved | - |
| B.Com graduates with no finance seat | approved | - |
| CA Inter clearers who stopped there | approved | - |
| employed accountants with free evenings | approved | Rs 30.55 |
| experienced Indian accountants | approved | - |
| finance MBAs working in sales or ops | approved | - |
| GCC and finance BPO accounting staff | approved | - |
| practising chartered accountants wanting US clients | approved | - |
| practising chartered accountants with their own office | approved | - |
| practising company secretaries running filings | approved | - |
| practising cost accountants (CMAs) | approved | - |
| practitioners filing GST returns for clients | approved | - |
| Tally accountants who do not know cloud books | approved | - |
| tax practitioners filing returns for clients | approved | - |
| tax practitioners who file client returns | approved | - |

**us-corporate-law**

| Occupation | Verdict | Live |
|---|---|---|
| chartered accountants applying to GCCs | approved | - |
| company secretaries keeping boards and registers | approved | - |
| company secretaries serving companies with US subsidiaries | approved | - |
| company secretary trainees in their batch | approved | - |
| compliance officers tracking filings and deadlines | approved | - |
| contract managers running intake and renewals | approved | - |
| corporate lawyers whose clients have US entities | approved | - |
| due diligence analysts on Indian deals | approved | - |
| ediscovery reviewers paid by the project | approved | - |
| final year law students facing placements | approved | - |
| in-house company secretaries in MNC compliance | approved | - |
| in-house counsel handling only Indian law | approved | - |
| junior litigation lawyers in their early years | approved | - |
| law firm associates serving clients with US arms | approved | Rs 81.9 |
| law graduates with no practice income | approved | - |
| law lecturers teaching company law | approved | - |
| lawyers targeting GCC in-house legal teams | approved | - |
| legal process managers stuck on document review | approved | - |
| legal researchers writing memos others sign | approved | - |
| practising CAs with startup clients incorporating abroad | approved | - |
| startup legal advisers whose clients flip to the US | approved | - |
| women lawyers wanting remote corporate work | approved | - |

**women-remote**

| Occupation | Verdict | Live |
|---|---|---|
| former bank relationship managers | - | - |
| freelancers still quoting an old rate card | - | - |
| law graduates not practising in court | - | - |
| MA psychology graduates without an M.Phil seat | - | - |
| night-shift customer support agents | - | - |
| nurses who left the shift roster | - | - |
| retail floor staff on a shift roster | - | - |
| school front-office coordinators | - | - |
| school teachers wanting evening income | approved | - |
| skin and cosmetic clinic therapists, fully booked | - | - |
| special educators at a capped pay grade | - | - |
| tuition teachers with locally capped fees | approved | - |
| women on BPO and call-centre night shifts | approved | - |
| women running the family shop unpaid | approved | - |
| women who left hotel and airline front-desk jobs | approved | - |
| women working BPO and call-centre shifts | approved | - |

## 4. What has already failed — read before proposing anything

| Audience | Line | Why |
|---|---|---|
| writers whose samples get no reply | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |
| writers argued down on word counts | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |
| interns finishing with only a certificate | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |
| writers who cannot show what writing earned | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |
| in-house writers doing everything but writing | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |
| writers doing bulk product listings for flat fees | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |
| editors rewriting other people's drafts | content-writing | NOT APPROVED: 06, 13, 16, 17, 18, 19, 24. Ship only what `make_approved_zip.py` filters to. |

**The standing rule this account paid three kits to learn:** a *practising
professional credential* cannot be the ICP for a general remote-work product. A
dietitian does not want to become a dietitian's assistant. Use the credential for
targeting and for landing-page proof; keep the ad's identity band a **situation**.

## 5. Priced audiences — the only ones that settle an argument

| Audience | Line | Archetype | Live |
|---|---|---|---|
| accountants in their forties and fifties | us-accounting | B | Rs 29.65 |
| employed accountants with free evenings | us-accounting | A | Rs 30.55 |
| Employed graduates, evenings free? | academic-writing |  | Rs 41.21 |
| employed women with two free evening hours | women-remote | B | Rs 41.21 |
| women professionals, at their widest | independent-director | E | Rs 60.98 |
| retiring armed forces officers | independent-director | A | Rs 64.8 |
| no audience named | us-accounting | D | Rs 72.65 |
| law firm associates serving clients with US arms | us-corporate-law | A | Rs 81.9 |
| medical transcription and RCM staff in India | data-privacy | A | Rs 103.16 |
| VLSI and semiconductor design engineers | patent | A | Rs 120.68 |
| BAMS and ayurveda graduates | patent | A | Rs 121.53 |
| agriculture and food science graduates | patent | A | Rs 131.49 |
| commission-based recruitment consultants | hr | A | Rs 134.07 |

## 6. An open question: objection-led ICPs

The archetype table calls anything that is neither an occupation nor a situation
a **C**, indexes it at 1.05, and says rewrite. But this account has shipped ads
whose audience is neither — it is a *belief the reader holds about herself*:

- *women who believe remote income is not for them* — `X2_myth_truth` (APPROVED)
- *women who think it is too late* — `W4_not_too_late` (WomenRemote_Wave4_SEND_THIS)
- *women who think it is too late* — `W4_not_too_late_cag` (WomenRemote_Wave4_SEND_THIS)
- *women who think they are not technical* — `W6_whatsapp_level` (WomenRemote_Wave4_SEND_THIS)
- *women who think they are not technical* — `W6_whatsapp_level_cag` (WomenRemote_Wave4_SEND_THIS)

These are not sloppiness. `W4_not_too_late` and `W6_whatsapp_level` are cells of
`WomenRemote_Wave4_SEND_THIS`, the founder's own kit, which gated **28 of 28
ACCEPT**; `X2_myth_truth` shipped in the approved Wave 6. So the taxonomy has no
name for a pattern that keeps passing review: the ICP is an **objection**, and
the ad exists to answer it. It behaves like a situation — she can point at the
belief — but carries no occupation and no life circumstance.

**Do not "fix" these by rewriting them into an A or a B.** That is what the
table would tell you to do, and it would delete a working pattern. Treat
objection-led as a fourth buildable shape, and note the honest limit: **none of
them carries a live cost**, so the case for it is approval, not money. If one
ever gets budget, price it before promoting the pattern.

---

Regenerate with `python -m adkit.icp --report`. Labels live in
`adkit/data/icp_labels.json` and are committed, so the index is reviewable and
stable rather than re-derived differently on every run.
