# Data Protection Bootcamp · 17–19 Oct 2026 · wave 3 — 20 ICPs

Built 1 Oct 2026, after Ruchika: *"the price for that is rising as well"*, with the same
brief as the Corporate Finance refresh — the readers that have worked or sit next to them,
the design that has worked, and a landing-page value proposition **completely different**
from the pages already live for this bootcamp.

## 1. The cost rise, diagnosed before anything was built

Live pull, 20 days to 1 Oct 2026 (`ad-analysis-shared/reports/DataPrivacy_2026-10-01.json`,
campaign `DataPrivacy_bootcamp_17-19Oct_CBO`, Skill Arbitrage). **₹2,43,659 incl. GST,
1,152 buyers, par ₹212.** August's DataPrivacy par was ₹144 gross, so cost is up about 47%.

Day by day, first half (21–25 Sep) against second half (26–30 Sep):

| | spend | buyers | CPP | CTR |
|---|---|---|---|---|
| 21–25 Sep | ₹93,947 | 488 | ₹193 | 0.59% |
| 26–30 Sep | ₹1,24,313 | 561 | ₹222 | 0.51% |
| | | | **+15%** | **−13%** |

Blended CPM appears to fall 57% across the same split. **That number is an artefact and
must not be reported** — WhatsApp Status runs at a CPM of ₹1–2 on 6% of spend and drags
the blended figure down (see `feedback_whatsapp_status_fakes_frequency`). Split by
placement, CPM is flat to slightly down **within every placement**, while CPP climbs:

| placement | share | CPP 21–25 Sep | CPP 26–30 Sep |
|---|---|---|---|
| instagram / feed | 31% | ₹229 | ₹211 |
| instagram / reels | 28% | ₹216 | **₹274** |
| facebook / feed | 18% | ₹216 | ₹225 |
| facebook / reels | 8% | ₹180 | **₹283** |
| instagram / stories | 7% | ₹185 | **₹279** |

Placement mix barely moved. **The feed placements are holding; Reels and Stories are where
the cost went.** Impressions are not getting dearer, the faces are getting tired in the
motion placements. That is a creative-refresh problem, which is what this wave is.

## 2. The design — newspaper, and it now has two independent measurements

Classifying every live ad by the design in its name:

| design | ads | spend | buyers | CPP | × par | band |
|---|---|---|---|---|---|---|
| **newspaper** | 5 | ₹68,869 | 358 | **₹192** | **0.91** | ±10% |
| call | 20 | ₹34,441 | 185 | ₹186 | 0.88 | ±14% |
| standard | 10 | ₹1,25,779 | 555 | ₹227 | 1.07 | ±8% |
| older `dpdp_` | 10 | ₹12,636 | 48 | ₹263 | 1.24 | ±28% |
| `7reasons` | 5 | ₹1,782 | 4 | ₹445 | 2.11 | ±98% |

This **replicates** the 23 Sep reading already recorded in `adkit/layouts_custom.py`
(`broadsheet` provenance: ₹136 over 5 faces against ₹168 over 9, same campaign, same week).
Two independent windows agreeing is the strongest design evidence in this product line.

**The honest caveat.** Within a single reader, no design has a repeatable win:

| reader | design A | design B |
|---|---|---|
| transcription_rcm | standard ₹222 (n=226) | call ₹220 (n=28) |
| side_practice | standard ₹198 (n=17) | call ₹290 (n=4) |
| firm_associates | newspaper ₹174 (n=169) | older ₹113 (n=13) |

So the aggregate is partly confounded by which readers happen to sit on which design.
Taken together with the 23 Sep within-campaign result, newspaper is the right bet and not
a proven law. **This wave uses `broadsheet` for all twenty**, which is the adkit layout
built from exactly these newspaper faces, rebuilt 23 Sep after the first version read as
"too much information": one column, five blocks, no photo.

## 3. The value proposition, and why it is not what is live

The pages live for this bootcamp argue **"add this service to the practice you have"** /
**"step up to the role one level above yours"**, then client types, pieces of work, where
India's law is, how the first matter arrives.

The camp's own scripts are titled **"International Career in Data Protection and Privacy
Management"** (`docs/DataProtection_17-19Oct2026_curriculum.md`). Day 1 teaches finding
projects on Upwork and Fiverr and pitching Y Combinator startups. Day 2 teaches networking
with foreign privacy consultants and Big Four partners, deciding on international data
transfer across the US, UK, Canada, EU, Singapore and Japan, and ten differences between
the DPDP Act and GDPR. Day 3 teaches an Upwork profile and a consultant website, proposals,
drafting a privacy policy under **California and Canadian** law, and negotiating your own
contract as a consultant or DPO.

**None of that is the argument on any live page.** So wave 3's value proposition is the
cross-border half of the same camp: *privacy work for clients abroad, from where you
already are.* It is fully traceable to the scripts, it is Rule 1 in its strongest form (a
different and better career, no regulator anywhere near it), and it matches the cheapest
pattern this account has ever run — US Accounting's "Same Work, Global Clients".

**Compliance limits carried into every line.** No income promise and no figures: "clients
abroad" and "paid in dollars" are allowed, amounts are not. No placement guarantee. Nothing
claimed that the scripts do not teach — in particular **not** a data-processing agreement,
**not** mapping a real company's data, **not** a 72-hour breach note.

## 4. The twenty readers

All figures incl. 18% GST, indexed to the live par of **₹212**, with the 95% band
(1.96/√n). A reader is cheaper or dearer only when the whole band sits on one side of par.

### Part A — proven cheap in the live window (4)

1. **Cyber lawyers** — lawyers already taking cyber-crime, IT Act and online-fraud matters, who want advisory work that is not tied to a police station or a court date. Live: ₹168, n=122, **0.79× par**, ±18%. The cheapest reader at scale in the campaign.
2. **Law firm associates** — associates at Indian law firms who want a specialism the firm does not yet have, and foreign clients the firm does not yet serve. Live: ₹170, n=182, **0.80× par**, ±15%. Cheaper under LawSikho too (law firm audiences 0.85× on n=484); the only reader with evidence under both brands.
3. **Women lawyers returning after a break** — qualified advocates coming back after time away, who want work that can be done from home and does not depend on a court calendar. Live: ₹193, n=81, **0.91× par**, ±22%.
4. **Litigators** — courtroom advocates who want advisory work that does not collapse when a hearing is adjourned, and that can be billed to clients outside India. Live: ₹195, n=96, **0.92× par**, ±20%.

### Part B — the volume reader, already working for clients abroad (1)

5. **Medical transcription and RCM specialists** — people who already produce work consumed by American hospitals and billing companies, and who want to be paid for judgement rather than turnaround. Live: ₹222, n=254, **1.05× par**, ±12%. The largest single cell in the campaign and the best natural fit for an international argument: the client is already abroad, only the work changes.

### Part C — cheaper than par, but thin. Fund these properly or do not run them (5)

6. **Broking and wealth compliance staff** — compliance and operations staff at broking houses and wealth managers, who hold client financial data and want a skill that travels outside the firm. Live: ₹145, n=18, 0.69× par, ±46%.
7. **Young law graduates** — graduates in their first two or three years, choosing the area they want to be known for before anyone has decided it for them. Live: ₹116, n=9. LawSikho law-university audiences 0.82× on n=372, while law STUDENTS come in dearer at 1.10× on n=1,973: graduates, never students.
8. **Company secretaries in practice** — CS professionals already filing and advising on governance, adding privacy work for companies with overseas parents or customers. Live: ₹98, n=7. LawSikho `cs` ad sets 0.69× on n=529, the strongest named segment in LawSikho's legal history.
9. **Consumer protection lawyers** — lawyers already arguing individual rights against companies, for whom data rights are the newer version of the same claim. Live: ₹144, n=5.
10. **Solo advocates** — advocates practising alone who want a service they can sell without a firm's letterhead, including to clients outside India. Live: ₹194, n=4.

### Part D — at par on the old argument. The international angle is the test (3)

11. **Pharmacovigilance associates** — people handling named patient safety data every day, in an industry whose sponsors and clients are usually foreign. Live: ₹207, n=34, 0.98×. The canonical Rule 1 approval of 12 Aug 2026 was written for this reader.
12. **Data analysts** — analysts who already handle the personal data a privacy programme governs, and who want to decide what may be done with it rather than report on it. Live: ₹214, n=34, 1.01×.
13. **Lawyers with a side practice** — advocates running an independent practice alongside a job or a chamber, adding a line that bills in dollars. Live: ₹216, n=21, 1.02×.

### Part E — adjacent to the winners, chosen because the client is already abroad (7)

Each of these sits one step from a reader that worked, and each already does work that is
consumed outside India. That adjacency is the whole claim; none has its own DPDP number, so
each is a bet that could be wrong and the wave should be read that way.

14. **Legal process outsourcing associates** — lawyers at LPOs doing document review and contract work for US and UK firms, who want to be the person scoping the matter rather than clearing the queue. Adjacent to law firm associates (0.80×) and to transcription/RCM (the proven "already serves foreign clients" cell).
15. **Paralegals supporting US and UK law firms** — paralegals already inside foreign firms' workflows, who want a named specialism rather than support work. Same adjacency.
16. **Compliance staff at global capability centres** — people in the India arm of a foreign company, already working to a parent's standard, who want the privacy mandate rather than the reporting pack. Adjacent to data analysts and BFSI operations.
17. **Medical coders and health information staff** — coders and HIM staff handling patient records for American providers. Directly adjacent to transcription/RCM, the campaign's largest and most durable cell.
18. **In-house counsel at companies with overseas customers** — the lawyer inside a company who becomes the owner of the privacy question the moment a European or American customer asks. LawSikho in-house ad sets 0.80× on n=389, but only 6 ads across 2 campaigns: promising and thin.
19. **Employment and labour lawyers** — lawyers advising employers, who hold every employee's personal record, and whose multinational clients are already asked for a privacy position. LawSikho `Employment` / `HR_Labour_Law` 0.94× on n=1,242 across 2 campaigns.
20. **Technology and IP lawyers** — lawyers advising software and platform businesses, the companies that hold the most personal data and sell it across borders. LawSikho 0.99× on n=10,689.

### Deliberately not rebuilt

On the live numbers these cost more than par and the band clears it, so they do not get a
face in this wave: **insurance** (₹322, 1.52×, n=38), **branch operations** (₹366, 1.73×,
n=18), **clinical research** (₹261, 1.23×, n=55), **logistics** (₹250, 1.18×, n=49). Also
excluded on LawSikho's own history: **law students** (1.10× on n=1,973) and **contract
law** (1.54×).

## 5. Budget

Twenty faces need about ₹1,00,000 over seven days to read at all — ₹5,000 a face is roughly
24 buyers at the current par, a ±40% band. Below that, cut the wave rather than the per-face
floor; the Corporate Finance waves of 23–28 Sep launched fifteen faces, gave one ₹15,767 and
fourteen between ₹100 and ₹2,400, and only the funded one could be read. If the budget is
smaller, drop Part C and Part E's weakest and run Parts A, B and D.
