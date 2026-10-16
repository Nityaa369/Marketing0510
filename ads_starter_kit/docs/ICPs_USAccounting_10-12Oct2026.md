# ICP list - US Accounting & Bookkeeping, free camp 10-12 Oct 2026

Round one of approval. **No ad face, no landing page.** Strike rows, then only what survives is
built in the `search` layout alongside the 8 faces already rendered in
`USAccounting_Search_MediaBuyer_10-12Oct/`.

Asked 17 Sep 2026: *"there are 8 really good ICPs. Are there ten more ICPs we can come up with so
we have an ad set of at least 15 ads?"*

Sources: a lifetime ad-level Meta pull of every US Accounting campaign on the token (Jan-Sep
2026), GrowthX registrations for September, `SOP/ICP_INDEX.md` (§2 situations, us-accounting
occupations), `adkit.icp --situations` and `--rejected`, `adkit.corpus --like`.

**Read costs within a campaign only.** The funnel changed across the year: Jan-Jun campaigns ran
at Rs 140-230 a lead, July Rs 82, August Rs 60, September Rs 42. An April ad at Rs 93 is cheap
for April. The "x" figures below are each ad against its own campaign's average.

**Nothing is rejected on this line.** `adkit.icp --rejected` carries no US Accounting verdicts.

---

## The 8 already built (for the ranking; costs are 12-14 Sep, Rs per lead)

1. **accountants-in-their-50s** - us22_notice_fifties Rs 38 on 1,144 (0.91x). Experience that the Indian job market calls too senior.
2. **employed-accountants-free-evenings** - us05_evening + us24_notice_evening, Rs 39 on 9,519 between them (0.94x). A day job that ends when the US work day starts.
3. **practising-company-secretaries** - us35_notice_cs Rs 40 on 186 (0.94x). Filing discipline pointed at US tax.
4. **indian-tax-consultants** - us26_notice_tax Rs 41 on 867 (0.98x). An Indian tax season that ends; the US one runs January to April.
5. **bcom-graduates-first-job** - us21_notice_bcom Rs 42 on 636 (1.00x). A first job search that keeps hitting the same firms.
6. **ca-inter-cleared-then-stopped** - us28_notice_ca_inter Rs 43 on 304 (1.02x). Skills without the final tag.
7. **small-town-accountants** - us25_notice_small_town Rs 48 on 86; us04_small_town Rs 40 in Aug. A town they do not want to leave.
8. **tally-accountants** - us27_notice_xero Rs 49 on 206 (1.18x). Software US clients do not use.

## Candidates - 18 new, ranked in value_props.md (revised 17 Sep after review)

Review notes that changed this list: split "entries, reconciliations and payroll" into separate
readers; rephrase "called back to the office"; swap commerce lecturers for tuition teachers; and
look for sector splits the way HR found hospital HR.

**The hospital-HR precedent, measured.** `hospital` in `Hr_bootcamp_22nd_august` ran Rs 135 a
buyer on 64, **0.77x** that camp's Rs 175 average, on only Rs 8,658 of budget. Worked, never
scaled. The same camp's hospitality cells did not: `hospitality_qsr` 1.12x on 8,
`w10_52_hospitality` 1 buyer. A sector split works when the sector has its own specialist work.

### The "Same Work, Global Clients" reader, split three ways

"Ad 3A - Same Work, Global Clients" was the cheapest ad in three consecutive camps (0.66x on
4,929 in April, 0.60x in May, 0.82x in June) and named entries, reconciliations and payroll
together. Three job titles sit inside that, each a box people tick on a job board:

9. **accounts-executives-daily-books** - Accounts executives doing daily entries and ledgers. Ceiling: the same books at an Indian employer's rate. Awareness: problem aware. Overlaps the Tally face (08) in the feed; separate ad sets.
23. **ap-ar-reconciliation-executives** - Accounts payable, receivable and bank reconciliation executives. Ceiling: month-end work that decides the close, paid as routine. Awareness: problem aware.
20. **payroll-executives** - Payroll executives running the monthly cycle. US payroll in Gusto and ADP is a service US bookkeepers sell. Ceiling: the same cycle on flat pay. Awareness: unaware.

### Sector splits (the hospital-HR pattern)

24. **hospital-and-clinic-accountants** - Accountants in hospital and clinic accounts departments: insurance billing, patient receivables. Maps to US medical and dental practice bookkeeping. The closest analogue to hospital HR. Awareness: unaware.
25. **construction-and-real-estate-accountants** - Accountants at builders and contractors: project costing, running-account bills. Maps to US contractor job-costing bookkeeping. Awareness: unaware.
26. **restaurant-and-hotel-accountants** - HOLD. Daily sales and stock reconciliations map to US restaurant bookkeeping, but HR's hospitality cells were the weak ones. Build only if 24 works.

### With a live cost on this line already

10. **women-accountants-restarting** - August "Indian mom" 0.92x on 502, "women" 1.08x on 812; June "Career Gap" 1.04x on 1,903. The September relaunch ran 1.69x on a tired face. Awareness: unaware.
11. **mcom-graduates** - March "B.Com or M.Com degree" 3,020 leads at 1.02x, shared with B.Com. Awareness: problem aware.
12. **cma-aspirants-between-attempts** - February "CA/CMA exams holding you back" 0.78x on 216. Awareness: unaware.
13. **ca-firm-audit-and-accounts-staff** - Approved for September (us13, us31), starved at 4 leads each (Rs 30, Rs 24). Awareness: problem aware.
14. **gcc-bpo-accounting-staff** - Approved for September (us12, us29), starved at 2-3 leads. Awareness: solution aware.
15. **gst-practitioners** - us14 Rs 46 on 9, starved. Overlaps tax consultants (04). Awareness: problem aware.

### Situations and new occupations

18. **accountants-whose-work-from-home-ended** - Renamed from "called back to the office". Face call-out: *Accountant, work from home ended?* The Women AI free camp's cheapest ad is `WF_t2c_wfh_ended` (Rs 52 on 202). Awareness: problem aware.
19. **senior-accountants-stuck-designation** - Same designation for years; the "ladder has stopped moving" situation from HR and Consulting. Awareness: problem aware.
22. **accountancy-tuition-teachers** - Replaces commerce lecturers. Class 11-12 and B.Com accountancy tutors already earn independently from the skill, so client work reads as more of the same, not a demotion. Ceiling: income capped by batch size and the exam calendar. Awareness: unaware.

### Recommended strikes

16. **finance-mbas-outside-finance** - may read bookkeeping as a step down.
17. **retired-accountants** - April 1.36x, and overlaps the 50s cell.
21. **marketplace-seller-accountants** - too hard to reach on Meta.
Commerce lecturers - struck and replaced by 22.

---

## Caveats

- `pain_score` is not fitted to cost. Where a candidate has a live cost, trust the cost.
- Reachability is scored for the face doing the selecting in a broad accounting audience, as on
  Patent, not for Meta detailed targeting.
- Candidates 15 and 17 overlap readers already in the 8 (tax consultants, 50s). If both survive
  they compete for the same people and belong in separate ad sets.
- The camp is free; costs above are cost per lead.
