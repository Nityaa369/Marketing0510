# Writing spec: per-reader content for 20 Contract Drafting Community landing pages

You write the READER-SPECIFIC half of each landing page as JSON. A builder adds the shared half
(why-now facts, the offer, the 16-document grid, the 9 live sessions, implementation, cost
comparison, refund, generic FAQ, disclaimer). Each page mirrors one Meta ad. Input per reader:
`banner` (ICP tape on the ad), `hook` (the ad's headline), `support`, `popup`, plus the angle row below.

## The product (only these facts may be used)
LawSikho Contract Drafting Community. 21 days, live online, 21 Oct to 11 Nov (do NOT put dates in
your text; the builder adds them). ₹200 incl. GST, refundable. Sold as a practice program: practical
drafting skills plus a showcase of where earning opportunities are. Never mention any paid course.
- A short reading and a quiz every day on WhatsApp; 9 live evening sessions on Zoom-style video calls
  (say "live online sessions", never name Zoom).
- Documents taught, one a day: parts of a contract; non-compete clause; e-commerce terms and
  conditions; employment agreement (plus a remote work monitoring policy); NDA and confidentiality
  clauses; cookie policy; co-founder agreement; DPDPA-compliant privacy policy; ESOP; SAFE agreement;
  term sheet; SaaS agreement; representations and warranties clause; IP licensing clause; commercial
  lease; vendor service agreement; joint development agreement. Extra: auditing D2C websites for
  silent obligations.
- 9 live sessions: (1) orientation, and using AI to find missing clauses and red flags in an
  influencer agreement; (2) finding issues in terms and conditions using AI; (3) listing your first
  gig on an online services marketplace; (4) questions to ask a client before drafting (co-founder
  agreement), and the roadmap; (5) reaching UK small businesses with a GDPR-compliant privacy policy;
  (6) pitching startups directly (Y Combinator lists, Apollo); (7) how law firm partners and in-house
  counsel think; (8) a LinkedIn profile that makes you known for contracts; (9) publishing your
  first article.

## Blocked: never write these
"21 contracts in 21 days"; "an expert corrects/reviews every draft"; "certificate"; "templates for
every contract"; recordings; any number of students, cohorts, jobs, clients or income; any job,
client, placement or income promise ("you will get clients" is banned; "how to reach clients" is
fine); "no competition", "few lawyers do this", or any newness claim; Fiverr; any regulator,
penalty or liability threat (never "you are exposed", "non-compliance", "fines"); AI-fear;
"more work at the same desk"; "not for you if"; "Is this for you?".

## Copy rules
- Plain Indian English for a tired reader on a phone. Short sentences (max 26 words, aim 12 to 18).
  Headings max 12 words, full sentences or plain statements, no puns, riddles, fragments or
  withheld referents ("this", "it" with nothing before it).
- NO em dashes or en dashes anywhere. No hyphen used as a dash. Write "to" for ranges.
- Banned words: transform, unlock, discover, elevate, leverage, empower, journey, game-changing,
  revolutionary, seamless, cutting-edge, freelance, freelancer, skyrocket, unleash, harness,
  navigate, landscape, adapt, struggling, guarantee, secret, hack.
- Hope, not pity: "want", never "struggling". The reader's current work is an ASSET they trade up
  with, never a liability. The offer is a better career: same craft (law), better payer
  (businesses and startups that need contracts drafted).
- Expand acronyms once per page where you use them: NDA (non-disclosure agreement), SAFE (simple
  agreement for future equity), ESOP (employee stock option plan), DPDPA (Digital Personal Data
  Protection Act), GDPR (the EU and UK data protection law), SaaS (software sold as a service).
- Every reader must be addressed as "you". Never assume gender except reader 08 (women lawyers).
- Write each page's text fresh. Do NOT reuse sentences across readers; each page must argue its
  own case. Different openings, different examples, different FAQ questions.

## JSON schema (one object per reader; write exactly these keys)
```
{
 "id": "01",
 "today": "Today, you ...",                 // one short sentence, max 14 words, the reader now
 "after": "After 21 days, you ...",         // one short sentence, max 16 words, what they can do then (a skill, not a result)
 "symptom_h2": "...",                        // heading that names their situation in their words
 "symptom": ["para", "para"],               // 2 paragraphs, 90 to 120 words total, their situation, hopeful
 "outcome_h2": "...",
 "outcome": "para",                          // 60 to 80 words: the better career; income only as a direction, no figures
 "alts_h2": "...",                           // e.g. "Three things readers like you try first"
 "alts": [{"t":"title","p":"why it did not change the job"}, x3],   // each p 25 to 35 words
 "reframe_h2": "...",
 "reframe": "para",                          // 50 to 70 words: the gap is positioning and practice, not effort or talent
 "role_h2": "...",                           // MUST contain a key word from the banner (e.g. "HR", "paralegal", "final-year")
 "role_intro": "para",                       // 40 to 60 words
 "role_points": [{"t":"what they already have","p":"how it carries into drafting"}, x3],  // each p 20 to 35 words
 "artifact_h2": "...",                       // what they draft in week one or the doc in the angle row
 "artifact_intro": "para",                   // 30 to 50 words
 "clause_title": "e.g. Clause 7. Non-compete",
 "clause": "a realistic 35 to 60 word clause in plain contract English, generic party names",
 "margin_note": "15 to 30 words, handwritten-style note written for THIS reader about why the clause matters",
 "plan_h2": "...",
 "plan": ["step", x4],                       // the 4 weeks after the camp, each 15 to 25 words, no promised results
 "room": ["...", x4],                        // finish the sentence "You are in the right room if you ..." (write only the ending, starting with a verb, 8 to 18 words)
 "faq": [{"q":"...","a":"..."}, x3],         // this reader's own worries; each a 30 to 55 words; no promises
 "buyer_line": "...",                        // one line they could say to family, first person, max 25 words, may include ₹200 and 21 days
 "close_h2": "...",                          // two plain clauses: reader named first as a PLURAL occupation, then what these 21 days add. e.g. "Final-year law students already study contract law. These 21 days turn it into contracts businesses sign."
 "close_lede": "para"                        // 25 to 45 words
}
```
Unique words per reader should total 650 to 800. Output: a JSON array of your readers, valid JSON,
UTF-8, written with the Write tool to the path you are given. Validate it parses
(`python3 -c "import json;json.load(open(PATH))"`) and grep it for "—", "–", and the banned words
before you finish. Reply with only the path and the word count per reader.

## Angle per reader (the page's argument and the clause document)
| Ad | Reader | Argument | Clause document |
|---|---|---|---|
| 01 | Final-year law students | Graduate with drafts already in hand, before the first interview | Co-founder agreement |
| 02 | Law graduates not practising yet | Startups hire drafters, not degree holders | SAFE agreement |
| 03 | Newly enrolled advocates | A first practice built on business clients, not court waiting | Vendor service agreement |
| 04 | Junior advocates in litigation chambers | Desk work on your own hours alongside the corridor | Commercial lease |
| 05 | Paralegals and legal assistants with an LLB | From preparing files to signing as the drafter | NDA (red flags found with AI) |
| 06 | Lawyers running their own small practice | Be there before the signature, not after the dispute | IP licence clause |
| 07 | Lawyers in smaller cities | Clients in Bengaluru and the UK, from your city | GDPR privacy policy |
| 08 | Women lawyers returning after a family break | One lesson a day on the phone, evening sessions | Remote work monitoring policy |
| 09 | Lawyers who moved cities after marriage | Desk work travels; court practice does not | Employment agreement |
| 10 | Indian lawyers living abroad with family | India and UK clients from any time zone | DPDPA and GDPR privacy policies |
| 11 | LLB holders working in HR | You already issue the documents; now draft them | Non-compete clause |
| 12 | LLB holders working in banking | The papers behind the money: term sheets, SAFEs | Term sheet |
| 13 | LLB holders working in content | Your writing skill, applied to terms and policies | Website terms, cookie policy |
| 14 | LLB holders in sales and operations | The contracts that close the deals you already run | SaaS agreement |
| 15 | LLB holders in BPO and back-office jobs | The lawyer you trained to be, from the parts of a contract up | Joint development agreement |
| 16 | Lawyers reviewing contracts in LPO jobs | From checking clauses to writing them | Representations and warranties |
| 17 | Company secretaries with an LLB | From records to founder and investor papers | Co-founder agreement and ESOP |
| 18 | Property and conveyancing lawyers | From sale deeds to commercial contracts | Commercial lease, then joint development agreement |
| 19 | Law students doing internships | Show drafted work in college, on LinkedIn | Parts of a contract |
| 20 | Lawyers who left a law firm for family | Come back with your own clients, not a desk at a firm | Client questions checklist (co-founder agreement) |

Note on 11 to 17: these readers hold an LLB; they are lawyers by training. Never call them
"non-lawyers". Note on 05: the LLB is what lets them draft as the lawyer.
