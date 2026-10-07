# Converting landing page template (NCA Canada, 31 Oct to 2 Nov 2026)

`template.py` holds the 21 step spine (Ruchika's order). `build.py` holds one config per ICP and writes:
- `pages/lp_*.html`: the page with gap markers as plain text (not for launch)
- `preview/lp_*.html`: the same with gaps highlighted yellow
- `GAPS.md`: every open item per page

Pages are built in the style of the three approved faces: advocates (chat, navy), associates (calendar, purple), fresh graduates (card, rust).

## The spine, as built
Fold (steps 1 to 3 repeat the ad: callout, the face, head, gloss, route chips, how band, pay button) > symptom > outcome > three failed alternatives > reframe (not effort) > why now (5 counted, sourced facts) > offer with dates and pay button > route in 3 steps plus why you can start from India > what you can do by the end of Day 1 plus the plan > longer term change > proof 1, real learners from the script > proof 2, group and public numbers > the work, day by day > implementation > cost compare > risk (Rs 10, refundable, live only) > buyer language plus WhatsApp share > next step > stop selling and the only disclaimer.

## To make a new page
Copy one config in `build.py`. Change `callout`, `head`, `face` (chat, calendar or card), `theme`, the copy keys and `stories`. Keep the route chips and the band: bar licensing is non negotiable.

## Gates (publish only when all pass)
- `[[PENDING: ...]]` blocks launch: learner consent and current job, real counts, the pay link (`#PAYMENT_LINK_PENDING`).
- `[[SCRIPT-CHECK: ...]]` needs the 2026 script. The only script on hand is the April 2024 run.
- `[[VERIFY: ...]]` means re-open the source on launch day.

Rules baked in: no income figure, no guarantee, no fear, no scarcity, no dashes, disclaimer only at the very end, never co-brand LawSikho and SkillArbitrage.

## Left out on purpose (from the script)
Pay figures, "top 2% of earners", seat counts and scarcity, "100% pass rate", the claim that remote work from India counts toward PR points, and the outdated election and immigration lines. See `docs/NCA_SCRIPT_EXTRACT_2026-10-07.md`, section 5.
