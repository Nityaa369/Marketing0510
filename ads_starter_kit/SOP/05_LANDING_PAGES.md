# 05 · Landing pages

## The first fold decides the conversion rate

> *"The weakest point is that the LPs do not talk about building a solo consulting business
> in the first fold. That can be confusing. The value needs to be clear upfront and it is
> not, so conversion will be lower than it can be otherwise."*

The first fold repeats the ad's promise **in the same words as the ad**. A reader who
clicked must land on the thing they clicked for, above the fold, without scrolling. The
page `h1` should appear verbatim on its own ad face — check it mechanically against the ad
HTML, not by eye, and record any deliberate exception in the kit README.

The Rule 2 defining sentence belongs in the first fold too, not only on the ad.

## Typography: the page has to be readable, and contrast is not the test

Added 1 Oct 2026, after Ruchika: *"the readability of the landing pages is very poor."* She was
right, and **contrast was not the problem** - the wave 6 pages measured 17.3:1 on body text,
17.4:1 on headings and 7.1:1 on the accent, all far past WCAG AA. Three other things were wrong,
and a page can pass every colour check and still be unreadable.

**1. Measure. 45 to 75 characters a line, aim for 66.** Wave 6 shipped 17px type in a 720px wrap,
which is 684px of content and about **80 characters** a line. Over the ceiling on every paragraph
of a 2,000 word page, which is what makes the eye lose its place on the return sweep. Fixed at
19px in a 660px wrap, about 65, with `p{max-width:62ch}` so no viewport can stretch it.

**2. Leading. A longer line needs MORE leading, not less.** 1.55 was tight for that measure.
Body is now 1.65.

**3. Do not let a display face do text work.** Every one of the **fourteen** h2 section headings
on a wave 6 page was set in Impact / Arial Black. Impact is a condensed poster face for a few
words at a large size; fourteen down a long page is what makes a page read as a flyer rather
than something anybody settles into. Section headings are now Georgia, the same serif the ad
face uses for its own headline. Impact survives in exactly two places: the ICP call-out, because
that **is** the face's call-out, and the single large price number.

**The hero mirrors the face, and check that it actually does.** Wave 6's hero was inherited from
wave 3 and kept `.main` as a two-column grid built for wave 3's collage image. With no image the
h1 was squeezed into a 40% column, two words a line, and the qualifier floated in the empty
column beside it. Worse, `h1 em` was `var(--acc)` over a gradient running **into** `var(--c1)`,
so the accent clause was dark red on dark red and all but invisible - on all twenty palettes.
A light hero ground with the reader in a dark band, the headline in ink and the second clause in
accent, is what the face does, is what Rule 3 asks the page to repeat, and takes that clause from
invisible to 7.1:1.

**Before shipping a kit, render one page at full height and look at it,** and render the closing
fold on its own. `adkit.fit.find_chrome()` plus `--screenshot --window-size=900,9000` gives a
full-page PNG in a second. No lint measures line length, leading, or a display face used for
body hierarchy; L7 and L8 below measure the two things that can be measured.

### 4. Sentence length. L7, and the ceilings are fitted

Same day, same reader, second report: *"readibility id dtill badin this section"*, pointing at
the closing fold. The typography was fixed by then. The **sentences** were not.

The seven Corporate Finance pages of 15-17 Aug are the only landing pages in this folder with a
measured conversion rate (9.3% to 20.7%), so they are the fit:

| | converted 9.3-20.7% | wave 6 before |
|---|---|---|
| body sentences | 623 | 1,990 |
| median words/sentence | 12 | 13 |
| p95 | 27 | 35 |
| **longest body sentence** | **34** | **54** |
| over 40 words | 0 (0.0%) | 64 (3.2%) |
| **longest heading** | **14 words** | **37 words** |
| headings over 16 words | 0 of 77 | 23 of 520 |

`L7` blocks a body sentence over **34 words** and a heading over **16**. Both sit one above the
observed maximum of work that converted, so the gate fires 0 times on that corpus and 144 times
on wave 6 as built. One-class fit, like `simplicity.py`: it shows the rule does not block good
work, and cannot show what it catches.

**Multi-sentence headings are not the rule.** The converting pages carry seven of them (*"Your
seat is Rs 10. Take it."*, 6 words). Length is the rule.

The three constructions that broke it, all of them list-shaped:

- **A colon with a list run into prose.** *"...is built in front of you: the projections, the pitch
  deck, the loan proposal and the information memorandum, with the market sizing underneath them
  and the term sheet and SAFE that follow."* 54 words. The colon becomes a full stop and the list
  becomes its own sentence with its own verb.
- **A two-sentence heading.** The closing fold's h2 ran 22 to 37 words because it carried both *who
  you are* and *what the evenings do*. The heading keeps the clause that names the reader, which is
  the one the closing-reader gate needs first; the rest drops into a lede paragraph under it.
- **An agenda line that lists a whole day in one breath.** Split at the clause boundary. No fact
  is lost; three sentences carry what one did.

**The closing fold does not carry the inventory.** `DELIVER`, the kit's constant delivery sentence,
was printed twice on every page: once in section 9, where the full document list belongs, and again
in the last 200 pixels before the pay button. The fold is now a heading that names the reader, one
lede sentence, one offer sentence, the button, the terms. It also took 42 words off every page.

### 5. Contrast, measured on every pair the stylesheet declares. L8

The readability report turned out to be two arithmetic failures as well, and both had survived a
hand contrast check that morning:

| | pair | measured | needs |
|---|---|---|---|
| `.cta`, `.sticky a` | `color:var(--ink)` on `background:var(--acc)` | **1.46:1 to 2.68:1** | 4.5:1 |
| `.close` | `#fff` on a gradient whose centre stop is `var(--c0)` | **1.07:1 to 1.23:1** | 4.5:1 |

So the **pay button on every page of a twenty-page wave**, in-page and in the fixed bottom bar, was
dark text on a dark accent. The hand check had read 7.1:1 and called the page fine - it measured
accent **text on the page ground** and never measured ink **on** the accent. Reading one pair proves
nothing about the other. White on accent measures 6.26:1 at its worst; white on ink, 16.45:1.

`L8` resolves the page's own `:root` custom properties and checks every rule that sets both a
background and a colour. **A gradient is checked against every stop in it**, which is what catches
the closing fold: it passed against its dark end and failed against its light one. Blocks under
4.5:1, warns under 7. It fires 0 blockers on the converting corpus.

Twice in one day a light gradient stop collided with the text on top of it (the hero `h1 em`, then
the closing fold). **Prefer a solid ground for any block carrying text.**

## The pay button

- Carries a **real** funnel URL: `https://growthx.skillarbitra.ge/f/<the page's own slug>`.
- No `TODO(dev)`, no `PAYMENT_LINK_PENDING`, no `href="#"`, no literal `<slug>`.
- **Never put a hedge or disclaimer paragraph above the CTA.** If a figure needs that much
  qualification, remove the figure.
- **Test-buy in a real browser.** `curl` returns false 404s on GrowthX funnels and proves
  nothing. The browser test is the only one that counts.
- **Open the page you are about to send.** Every time. Every page, not a spot check.

A wired button is not a live funnel. Confirm the GrowthX funnel exists for each slug
separately from confirming the wiring.

## The 21-step spine is the current standard (recorded 28 Sep 2026)

Since 25 Sep 2026 every new kit's pages are built on the user's **21-step sales-page framework**
(name the buyer, symptom, outcome, three things people try, the reframe, what stays the same,
the offer, a 3-step route, the first artefact, the longer change, proof, the work, logistics,
a time-and-output comparison, risk removed, one line to repeat, the close). It shipped on
`StrategicHR_Wave1_MediaBuyer_31Oct-2Nov`, `USAccounting_Wave2_MediaBuyer_10-12Oct`,
`NCA_LawSikho_MediaBuyer_31Oct-2Nov` and `IndependentDirector_Calendar_MediaBuyer_10-12Oct`.
Start a new kit from one of those: copy its `build_lps.py` (the builder holds the camp's
constants) and its `LP_WRITER_BRIEF_21.md`, and write the reader copy per page in
`lp_content21/NN.json`. House adaptations: "if nothing changes" carries no threat or number
(Rule 1), the comparison is time and output only, proof is only real named people.

**Why this note exists:** the ID calendar kit (28 Sep) was built on the older spine below
because this file and the generate-ad-kit skill still described it, and the 21-step spine was
only written down inside the three kits that used it. The user caught it at handover.
**No live cost yet:** keep the old-spine pages of a rebuilt kit as `build_lps_v1.py` and
compare leads per landing-page view once the wave has 7 days and 20+ leads.

The older spine below still describes the house sections; it is no longer what a new kit ships.

## The section spine (older, superseded 25 Sep 2026)

Eleven sections, with the hero, the future-state section, the qualifiers and one FAQ
written for that ad's reader:

1. What the three evenings give you
2. The buyer, named
3. How the work gets bought
4. What the work is quoted at
5. Who runs this
6. Testimonials
7. Where this puts you
8. Ten reasons
9. This is for you if
10. Reserve your seat
11. Questions

## Money data is matched per page

A page never quotes a role the reader is not being pointed at. A student page uses a
fresher block and per-project pricing, not a strategist salary band. A page whose ad
promises what the work is quoted at outside a salary uses retainer and per-campaign
pricing, not salary bands.

## Build

- Self-contained. Hero embedded. No sibling folders, nothing to upload alongside.
- Typically 36 to 90 KB, around 2,800 to 3,000 words.
- Pages carry no analytics themselves — confirm the deploy pipeline injects gtag/fbq.

---

## What the conversion data actually says (measured 31 Aug 2026)

Meta pull, Skill Arbitrage account, `last_30d`, 40 ads with `landing_page_views` and results.
LP conversion here = **results ÷ landing page views**. One ad points at one page, so this
measures the page *and* its match to the ad that sent the traffic.

### The benchmarks

| Funnel | Median LP conversion | Range observed |
|---|---|---|
| **Free bootcamp** (registration) | **30.5%** | 19.1% – 34.5% |
| **Paid camp** (₹10 / ₹100 purchase) | **9.6%** | 5.1% – 20.7% |

Judge a page against its own funnel type. A 12% page is excellent for a paid camp and a
disaster for a free bootcamp.

### About a fifth of clicks never reach the page

Median click → landing-page-view is **78%**, and it varies from 68% to 86%. That gap is
paid-for traffic that never saw a word we wrote. It does **not** explain conversion
differences (click→LPV vs conversion, r = +0.09), so treat it as a separate loss to chase in
the deploy pipeline, not as a page-copy problem.

### The page spine is already a solved constant — the ICP is not

This is the finding that matters most, and it is not what we expected to find.

All **seven** Corporate Finance pages are structurally identical: same 10 `h2` sections, same
first-fold slot order, 1,712 to 1,737 words — a spread of 25 words across the whole kit. Their
conversion ranges from **9.3% to 20.7%**. Same skeleton, same designer, same week, **2.2×
apart.** The same holds inside every other kit measured:

| Campaign | Best page | Worst page | Spread |
|---|---|---|---|
| Corporate Finance | `cf_loan_consultant` 20.7% | `cf_gcc` 7.5% | **2.8×** |
| Data Privacy | `wave2_litigators` 14.7% | `rs_15b_returning_soft` 5.1% | **2.9×** |
| HR | `w10_60_agency` 17.6% | `working_women_side_income` 6.6% | **2.7×** |
| Senior AI | `Rented_Exec` 17.2% | `professor_subject` 7.5% | 2.3× |
| Patent | `Exam window` 11.1% | `mm_01_govtexam` 5.4% | 2.1× |
| US Accounting | `office hours` 31.8% | `America needs accountants` 19.1% | 1.7× |

**So do not go looking for a better page template. We already have one.** Within a kit, what
moves conversion two to three times is **which reader you sent to it** — see
[08_ICP_SELECTION.md](08_ICP_SELECTION.md). Effort spent redesigning the spine is effort spent
on the variable that is already fixed.

The worked pair, both from `CorporateFinance_MediaBuyer_15-17Aug`, identical page skeleton:

> **20.7%** — *"A loan consultant whose every conversation ends at a loan?"*
> `DSA · LOAN CONSULTANTS · CREDIT ADVISORS · B.COM`
> "Do corporate finance work that goes further than arranging the loan."

> **9.3%** — *"A retired banker who still wants to work, from home?"*
> `RETIRED BANKERS · PSU AND PRIVATE · NO UPPER AGE LIMIT`
> "Do corporate finance work from home, for clients anywhere."

The first names a **ceiling** ("every conversation ends at a loan"). The second names an
**aspiration** ("still wants to work"). That is the whole difference, and it is the Ceiling test
in `SOP/08` §3.

### The spine that is actually shipping

Read off the three highest-converting kits. It is **not** the eleven sections listed above —
those pages run 2,800–3,000 words, and the measured winners run shorter:

| Kit | Words | `h2` sections |
|---|---|---|
| HR `lp_60_agency` (17.6%, best in kit) | 1,544 | 9 |
| Corporate Finance (all seven) | ~1,725 | 10 |
| Data Privacy | 1,913–2,372 | 10 |

**Nine or ten sections, 1,500 to 2,000 words.** The common order:

1. The situation, named in the reader's terms
2. The demand, as a **counted list** ("8 sectors creating a flood of privacy work", "8 systems, and a one-person desk")
3. The gap, as a **counted list** ("The 5 things your CS course never taught you")
4. Why this lands on *you* specifically
5. What the work pays — market data, **LP only, never the ad face**
6. The evenings, in detail, and what you leave with
7. People who made this move
8. **Positive qualification** — *"You are in the right room if…"*, never *"this is not for you if…"*
9. Straight answers / questions

Two of the counted-list sections are what make the page feel like an argument rather than a
brochure. Keep the counts real and specific (8, 5, 3), not round-number filler.

### Watch the qualification heading

The Data Privacy and HR kits use **"You are in the right room if"** — correct, positive, and
what this SOP requires. The Corporate Finance kit uses **"Is this for you?"**, which sits one
word from the banned *"this is not for you if…"* block. Prefer the Data Privacy wording.

### Dead pay buttons are still shipping

**Every one of the six Data Privacy pages in the repo carries `PAYMENT_LINK_PENDING`** — on the
account's cheapest paid camp. The live funnel is deployed elsewhere, so the campaign runs; the
repo copies are the danger, because they are exactly the pages someone will reuse as a donor.
Re-read the pay button rules above before copying any page.

---

## Rule 4b — the landing pages in one kit must actually differ

Added 31 Aug 2026, from the founder, on the women bootcamp kit he had just shipped:

> *"if i am showing ads to someone for the women bootcamp, they see different ads, and
> then they click on it, but the lp is the same over and over again, making them
> disinterested. so we have to come up with different lps in the same kit"*

Rule 4 already said 1 ad = 1 LP, and every kit obeyed it **as separate files**. Nothing
measured whether the files said anything different. Measured as median pairwise overlap
of whole sentences:

| Kit | LPs | Overlap |
|---|---|---|
| `USParalegal_LawSikho_MediaBuyer_29-31Aug` | 7 | **93%** |
| `WomenRemote_Wave6_SEND_THIS` | 6 | **90%** |
| `WomenRemote_Wave8_SEND_THIS` | 10 | **84%** — the reported kit |
| `WomenRemote_Wave4_SEND_THIS` | 28 | 77% |
| `CorporateFinance_MediaBuyer_15-17Aug` | 7 | 74% |
| **`WomenRemote_Wave9_LPs_SEND_THIS`** | 7 | **1%** — the model |

Wave 8's ten pages carry an **identical H2 sequence** and change only the H1. Wave 9 gives
each page its own argument — a Saturday walkthrough, the case in numbers, three
career-break stories, a demand board — and overlaps by 1%.

**This does not contradict "do not redesign the page spine."** The spine is the chassis:
ten sections, 1,500–2,000 words, counted lists, sticky CTA. Corporate Finance sits at 74%
and converts 9.3% to 20.7%, so a shared spine is not what costs conversion *on one page*.
The defect is about the **reader, not the page**: one person sees several ads from the same
campaign, clicks more than one, and lands somewhere she has already read. **Keep the spine,
change the argument inside it.**

`preflight.py` blocks at 80% and warns at 65%.

---

## The closing fold — say it plainly, it is the last thing before the money

Added 21 Sep 2026, from the founder, on the CorporateFinance notify wave:
*"These type of lines that have been added - none of them make any sense."*

The closing fold is the **last call-to-action on the page plus the heading above it**. It
is the final argument a reader gets before deciding to pay, and it had no standard and no
gate. All nineteen pages of that kit carried a heading written as the same riddle — two
clauses, an implied contrast, the referent withheld — and the kit had just passed all ten
gates of `check_all.py` clean.

    "The biggest thing your client owns has never been on a statement you sent them."
    "The arithmetic you have. The half where nothing is published is the half
     that is missing."                          <- no verb in the first clause
    "The second half of that conversation is already happening at your desk."
                                                <- "that conversation" has no antecedent

**The standard.** Name the work the reader already does, then what this adds. Two plain
clauses. No withheld referent, no "that conversation" or "the file" with nothing to point
at, no fragment without a verb.

    "You already work out whether a company can repay. This is how you work out
     what it is worth."

**Name the PERSON, not only the work** (added 1 Oct 2026, Tech Law 24-26 Oct). The standard
above is necessary and it is not sufficient. Four folds in that kit scored 2/3, and all four
failed on question 1, *who is this addressed to*, while answering question 3 perfectly. Each
one described the work and never put a noun on the reader:

    "You already draft and appear on your senior's matters."    -> "CANNOT ANSWER"
    "You have the law degree and no first matter yet."          -> "CANNOT ANSWER"
    "You are a junior lawyer, and every matter you touch is your senior's."   -> clear

The same opening clause passed on one page and failed on another in the same run, so the gate
samples this noisily and a clean score does not prove the fold names anybody. Write the reader
into the first three words and the question stops being askable. Cheap to do, and it is the
same defect C23 catches on an ad face, one slot later.

**Why no regex.** A rule banning two-clause headings would have blocked *"Thirty years of
credit judgement does not expire. The vocabulary of a deal takes three evenings."*, which
is two clauses and perfectly clear. The judgement needs a reader with no context.

**The gate.** `closing_reader.py`, wired into `check_all.py` as `closing read`, on the same
contract as the ad-face blind read: three closing folds whose face priced cheap or was
approved are shuffled in as blinded controls, and a page fails only when it reads worse
than one of them. Never run is an ERROR, not a pass; a page rebuilt after its read reads
STALE, measured on the fold rather than the file. The instrument works — on its first run
it caught two of the replacement lines, including one a reader said "does not parse as
ordinary English".

    python closing_reader.py --prepare <kit>     # then one subagent per packet
    python closing_reader.py --score <kit>
    python closing_reader.py --why               # the evidence behind each rule

Comprehension only. It says nothing about whether anybody wants the offer.
