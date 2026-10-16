# Spec: reader-specific landing page content (one JSON file per ad)

Write `lp_content/<id>.json` for each ad id you are given. The page engine adds the common blocks
(first fold terms, 3-step mechanism, the 3 sessions, two learner proofs, sourced market facts, cost
comparison, refund, buttons, disclaimer). You write ONLY the parts below, for ONE reader.

Read first: `wave.py` (your ads: callout, head, why, reader), `../../docs/TECH_LAW_CAMP_FACTS_2026-10-16.md`
(what the camp teaches; every claim must trace to it), `../../docs/research/tech_law_2026-10-16/02_audience_voice.md`
(buyer language), `../../docs/research/tech_law_2026-10-16/04_fact_check.md` ("Do not use" list), `../../RAMANUJ_APPROVAL_GUIDE.md`.

JSON schema (all strings plain text, no HTML):
{
  "id": "01",
  "qualifier": "One sentence: who this page is for, in the reader's own terms.",
  "symptom_title": "Short heading", "symptom": ["2 or 3 short paragraphs: their situation today, in their words"],
  "outcome_title": "Short heading", "outcome": ["1 or 2 paragraphs: what changes if they move into tech law (the career, not money)"],
  "alternatives_title": "Short heading",
  "alternatives": [{"t": "A route they already tried or considered", "why": "Why it did not get them there"}, x3],
  "reframe_title": "Short heading", "reframe": ["2 paragraphs: it is a positioning problem, not effort; their current skill is the asset"],
  "cost_title": "Short heading", "cost": ["1 paragraph: the cost of staying unclear. Gentle. Never a threat, never fear."],
  "role_h2": "A heading that NAMES THE READER'S ROLE, e.g. 'What tech law work looks like for a consumer forum lawyer'",
  "role": ["3 paragraphs: concrete tech law tasks this reader would do, tied to what they already know"],
  "first_artifact": "1 paragraph: the first thing they will have done after the camp (from the camp: software development agreement clauses on Day 1, a startup's terms reviewed on Day 3, a refund policy or influencer agreement on Day 3)",
  "longer_term": ["1 paragraph: what the next 6 months can look like if they follow the 2 hours a day plan. No promises."],
  "faq": [{"q": "A doubt in the reader's own words", "a": "A plain answer that traces to the script"}, x4],
  "closing_title": "Starts with the reader, e.g. 'Consumer forum lawyers: ...'",
  "closing": "A self-contained 2 or 3 sentence lede that names the reader first and the move into tech law."
}

Hard rules (a page that breaks one is rejected):
- About 900 to 1,100 words across your fields. Sentences of 34 words or fewer. Plain English.
- No em dashes or en dashes anywhere. Write "3 to 5" not "3-5". Use commas or full stops.
- Lawyers only. Offer a new, better career: same craft, better payer. Never a regulator threat, never
  "more work at the same desk", never "be named the person who fixed it".
- No income figures, salaries, dollar amounts or earnings stories. No job, client or placement promise.
  Use "could", never "will get". No AI fear.
- No statistics (the engine adds sourced facts). No learner names (the engine adds proofs).
- Never use: "DPDP deadline is weeks away", "Section 79 ... safe harbour" quotes, "5,000 GCCs", "first
  legal tech unicorn", "rewrote its rulebook", "USD 10 below a burger flipper", "Upwork was free".
- Facts about the camp: 3 live evenings, Sat 24 and Sun 25 Oct 6 to 9 PM IST, Mon 26 Oct 7 to 10 PM IST;
  Rs 10 incl. GST, refundable, live only, no recordings. Day 1: 5 tech concepts (SLAs, APIs, source vs
  object code, white labelling, SaaS), drafting a software development agreement, reaching startups in
  the US, UK, Canada, Europe and India, networking with US lawyers. Day 2: 6 ways tech companies make
  money, the 6-month plan, services e-commerce companies need, networking with US, UK and Canadian
  lawyers. Day 3: reviewing a startup's terms and pitching the fix, an e-commerce refund policy, an
  influencer agreement, getting lawyers onto podcasts, an Upwork profile for privacy work, a Wyoming
  company for a blockchain founder. Plan: 2 hours a day (1 learning, 1 outreach). Formula: skills plus
  track record plus outreach. No coding needed: the work follows the business model.
- Each page must argue differently from the others in your batch: different situation, different failed
  alternatives, different reframe. Do not reuse sentences across pages.
- Valid JSON (double quotes, no trailing commas). Run `python3 -c "import json;json.load(open(F))"` on each file.
