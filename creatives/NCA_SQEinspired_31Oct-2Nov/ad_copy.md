# NCA Canada bootcamp, 31 Oct to 2 Nov 2026 · LawSikho · SQE-inspired wave

Status: DRAFT for Ramanuj, not approved. Each face borrows the shape of an SQE ad that ran cheap or
that Ramanuj approved (evidence below). One reader, one message, the route (NCA exams from India,
then bar licensing, then practise) on every face. No dates on faces. Rs 10 incl. GST, refundable,
live only. Rebuild: `python3 build.py <this folder>`.

## What worked for SQE (sources: PERFORMANCE_2026-10-05.md, adkit/data/icp_raw.json, GOLDEN.md, gate-rules.md)
| SQE evidence | Cost vs par | Lesson for NCA |
|---|---|---|
| `sqe_h_secondact` "Become a UK solicitor without pausing your practice" (advocates in their 40s and 50s; no number on the face) | **0.63x**, cheapest SQE ad | Qualify without giving up the practice you have. Put the age band in targeting, not the call-out |
| `Sqe_ondemand` | 0.65x | (copy not in the bundle) |
| `sqr_c_editorial`, light editorial design | 0.67x | Editorial serif face |
| `sqe_l_gulf` "Gulf legal work runs on English common law" | 0.89x | Match the law they already know to the market |
| `sqd_routes` "Are you eligible to migrate to the UK?" + `sqd_over30` + duty-chart kit | **Ramanuj approved** (GOLDEN) | Eligibility question, sourced official facts, abundance framing |
| `sqe_r_newadvocates` "Become a UK solicitor in two hours a day" | built, unpriced | A named daily time block |
| `sqe_e_contracts` "You already draft under English law. Qualify in it." | built, unpriced | Confirm the skill they already have |
| `sqx_g2_seniors_15plus` (a number on the face) | **1.29x** | Numbers on the face lose, again |
| `sqx_l_family_home` | 1.27x | Family angle loses (already dropped for NCA) |
| Targeting: IELTS interest 0.73x, English 0.68x, "UK" 0.84x; bar-exam interest **1.84x**, LLM 1.37x | | Target IELTS/English interest; never lead with "bar exam" |
| Rules: "eligible to apply", never "automatic" (C16); abundance not scarcity (C19); proof numbers conservative ("70+", never "170+") | | Applied below |

## nca_s_01_editorial_5plus_years (editorial, from sqe_h_secondact + sqr_c_editorial)
- **ICP:** Lawyers practising for 5 years or more
- **Face head:** Start your Canadian qualification without pausing your practice.
- **Headline:** Qualify for Canada without pausing your practice
- **Primary text:** An advocate with five or more years of practice, thinking about Canada? You do not have to stop practising to start. The NCA exams, Canada's check on your Indian law degree, are written from India. Clear them, pass the bar licensing, then practise in Canada. In our 3-day live bootcamp, we explain each step and build your 12-month plan with you. Live only, no recordings. Rs 10 incl. GST, refundable anytime.
- **Risk:** "5+ years" kept on the call-out at Ruchika's request. SQE's cheapest ad carried no number and `seniors_15plus` lost at 1.29x. Run a twin with the call-out "EXPERIENCED ADVOCATES?" in the same ad set to settle it.

## nca_s_02_eligibility_check (checklist, from Ramanuj-approved sqd_routes)
- **ICP:** Indian lawyers who want to practise in Canada
- **Face head:** Are you eligible to apply?
- **Headline:** Are you eligible to practise law in Canada?
- **Primary text:** Want to practise law in Canada? Check where you stand. You need an Indian LLB from a recognised university, an English test (required for every NCA applicant since 1 March 2026), and the NCA exams, written from India. Then the bar licensing, then you practise. In our 3-day live bootcamp, we explain each step and build your 12-month plan with you. Live only, no recordings. Rs 10 incl. GST, refundable anytime.
- **Rule:** says "eligible to apply", never "automatic" (gate C16). English-test rule sourced in `docs/NCA_WEB_RESEARCH_2026-10-06.md`.

## nca_s_03_planner_newly_enrolled (day planner, from sqe_r_newadvocates)
- **ICP:** Newly enrolled advocates (the 0 to 2 years reader, with no number on the face)
- **Face head:** Prepare for Canada's NCA exams in 2 hours a day.
- **Headline:** Prepare for the NCA exams in 2 hours a day
- **Primary text:** Newly enrolled and thinking about Canada? You can prepare for Canada's NCA exams in about 2 hours a day, alongside court. The exams are written from India. Clear them, pass the bar licensing, then practise in Canada. In our 3-day live bootcamp, we explain each step and build your 12-month plan with you. Live only, no recordings. Rs 10 incl. GST, refundable anytime.
- **Check:** "2 hours a day" is from the April 2024 script (about 6 months at 2 hours a day). Confirm in the 2026 script.

## nca_s_04_redline_contract_lawyers (contract document, from sqe_e_contracts)
- **ICP:** Corporate and contract lawyers
- **Face head:** You already draft under common law. Qualify to practise it in Canada.
- **Headline:** You already draft under common law
- **Primary text:** A corporate or contract lawyer? You already draft under common law, and Canada is a common-law country. Qualify to practise there: clear the NCA exams from India, pass the bar licensing, then practise in Canada. On Day 3 you review a Canadian contract, live. In our 3-day live bootcamp, we explain each step and build your 12-month plan with you. Live only, no recordings. Rs 10 incl. GST, refundable anytime.
- **Check:** Day 3 contract review is from the April 2024 script (a non-compete under Canadian law). Confirm in the 2026 script. The clause on the face is an illustrative sample, not a real client document.

## Landing pages (`landing_pages/lp_<ad stem>.html`, built by `build_lps.py`)
Ruchika's 21-step order, one page per ad, each in its ad's palette: 1,675 to 1,997 words, no sentence
over 34 words, no heading over 16, 34 to 41% sentence overlap between pages (blocks at 80%). The only
disclaimer is at the very end. First fold: who-question, qualifier row, the ad's promise, NCA defined,
3 deliverables, dates, times, price, button.

**Blockers before any spend:**
1. **Pay buttons are placeholders** (`#PAYMENT_LINK_PENDING`). Create the four GrowthX funnels
   (`nca-oct-s01-experienced`, `-s02-eligibility`, `-s03-newly-enrolled`, `-s04-contract-lawyers`),
   put the real URLs in `PAY`, and test-buy each in a browser.
2. **Learner stories** (Hezal Shah, Shashwat Jindal, Navkaran Singh, Yashika Malhotra, Harshmir
   Swaitch) are as told in the April 2024 script summary, worded "in our bootcamp's own account".
   Confirm each person's current facts and consent with Abhishek Pareek before publishing.
3. **Confirm in the 2026 script:** the Day 1 to 3 content, "about 2 hours a day / six months", the
   2026-rules session, the WhatsApp joining message, and that Abhishek Pareek leads.
4. **Sourced facts used:** IMF Oct 2025 (Canada 10th largest economy, G7), IRCC 2026 to 2028 levels
   plan (380,000 PR a year, 64% economic), IRCC 2024 (India 127,320 new PRs), nca.legal (fees,
   monthly exams, 10 months best case, about 2 years average, 5-year window, JD tuition), Job Bank
   NOC 41101 Ontario (CAD 65.21 median an hour, labelled market data, page only). "Canada is the 7th
   best economy" was checked and is wrong (10th), so it is not used.
