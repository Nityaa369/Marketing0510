# Disapproval casebook (real Google Ads rejections, what caused them, how they were fixed)

Every entry below is an ad that Google actually disapproved or limited for this team, with the
screenshot reason. Before rendering ANY ad, compare it against every case here. If an ad shares a
trigger with a case, apply that case's fix even if Google has not flagged it yet.

---

## Case 1. HR GrowthCamp ad B4: Image quality ("design must fill the entire space")
- **Google reason:** Image quality. The image does not fill the entire space / has excess white space.
- **Cause:** The design sat in a white card with large empty margins. Background was plain white, so
  Google read the creative as not filling the frame.
- **Fix that passed:**
  - Tinted background over the whole canvas (accent mixed 88% with white) plus a fine dot texture.
  - A full-bleed coloured band across the bottom (edge to edge) carrying the CTA in white.
  - Content scaled to fill the safe area (centre 80%), no floating white card.
- **Rule:** Never leave a plain white or empty canvas. Every size must look full edge to edge.

## Case 2. HR consultant ad: Misleading ad design
- **Google reason:** Misleading ad design.
- **Cause:** A "TODAY / AFTER" two-panel comparison laid out like a form, plus white boxes that looked
  like input fields or UI cards.
- **Fix that passed:** Removed the segmented today/after panel and all form-like white boxes. Replaced
  with a headline, a bold explanation and a plain dot list.
- **Rule:** No segmented "before/after" panels, no form fields, no white input-like boxes, no checkboxes.

## Case 3. Tech Law "AirDrop" ads (2 ads): Misleading ad design
- **Google reason:** Misleading ad design.
- **Cause:** The ad imitated an iPhone AirDrop popup with "Accept / Decline" buttons, checkbox ticks and
  an arrow. Google treats fake system dialogs and fake buttons as deceptive.
- **Fix that passed:** Rebuilt with no dialog, no Accept/Decline, no checkboxes, no arrow. The idea
  survived only as a headline.
- **Rule:** Never imitate OS, phone, app or browser UI (dialogs, notifications, incoming calls,
  close X, Accept/Decline, play buttons, cursor, checkboxes, toggles).
- **Same trigger caught proactively:** NCA "Canada is calling" call-set had an iPhone incoming-call
  card with Decline/Accept. Removed before upload; kept "Canada is calling." as the headline.

## Case 4. Tech Law tl03 "In tech law, no senior is 20 years ahead of you": Image quality
- **Google reason:** Image quality.
- **Cause:** A small low-resolution screenshot-like creative: mostly plain white, small text, a blue
  button-shaped CTA, a black label box, large empty areas.
- **Fix that passed:**
  - Rendered fresh at full resolution for each size (JPEG quality 82 to 90), large type.
  - Tinted textured background + full-bleed bottom band, nothing left white.
  - Added a simple original visual tied to the headline (court-seniority staircase vs a single
    "same start line" bar for tech law).
  - CTA as plain white text on the band ("₹10 gets you all 3 days of the live bootcamp").
  - Outcome promise softened: "gets you tech disputes work in 6 months" -> "a 6-month plan to take on
    tech dispute work".
- **Rule:** Never upload screenshots or upscaled small images. Always render natively at 1200x628,
  1200x1200 and 960x1200.

## Case 5. Academic Writing "Ten ways ... takes on paid research work" (5 ads): Enabling dishonest behaviour
Ads: postdoctoral researchers, highly qualified homemakers, retired academics, assistant professors,
college lecturers.
- **Google reason:** Enabling dishonest behaviour ("products or services that help users fake
  documents, cheat on exams ... aren't allowed").
- **Cause:** The 10-item list read as ghostwriting other people's academic work for money:
  "Writing the review itself", "Writing up finished results", "Grant applications",
  "Methods sections and protocols", "Journal submission packages", "Examining theses abroad",
  "Peer review support", "The grant applications you write for the PI are bought, per submission",
  "find writing and editing gigs". Plus money words "paid research work", "Paid expert consultations",
  "earns nothing", and NSE / NSDC claims.
- **Fix used:** Reframed as credited research consulting in the person's own name:
  - Headline: "Ten ways a <role> builds research consulting work in their own name."
  - Items (choose 10 per audience): Evidence synthesis projects · Expert consultations ·
    Journal peer reviewing · Systematic reviews as a named co-author · Grant proposals as a named
    co-investigator / Grant proposals you lead · Study protocols as the methodologist · Study design
    consulting · Research methods training (and mentoring) · Evidence reports for companies ·
    Plain-language summaries for funders · Literature searching and screening · Second reviewer on
    systematic reviews · Research data coding and analysis · Reference and data checking ·
    Advisory board roles · Publishing from your own results · Research proposals as a named collaborator.
  - Outreach line: "the outreach plan to reach foreign universities, think tanks and policy institutes"
    (never "gigs").
  - Fine print adds "Your name stays on your work". NSE / NSDC claims removed.
- **Rule:** In any academic/writing product never say or imply writing, editing, examining or submitting
  work that another person will present as their own. Words to avoid: thesis/dissertation/assignment
  writing, "write the review/paper", ghostwriting, gigs, per submission, bought, examining theses,
  methods sections, journal submission packages, grant applications (for others).

## Case 6. NCA "Practising criminal law in India?": Commission of a crime in personalised advertising (Eligible, limited)
- **Google reason:** Commission of a crime in personalised advertising. "Content related to someone's
  personal criminal record cannot be used in personalised advertising."
- **Cause:** "Practising criminal law", "Criminal lawyers are requested to note", "Criminal Code",
  "IPC". Google cannot tell "lawyers who practise criminal law" from "people with a criminal record",
  so the ad is limited in targeted campaigns. The "NOTICE ... are requested to note" box also looked
  like an official notice.
- **Fix used:** Audience reframed as "Trial court litigators in India. Years of arguing in court, and
  Canada is on your mind." Comparison line changed to "how Canadian trial practice compares with
  yours". Notice box removed. Arrow on "Register at ₹10 →" removed.
- **Rule:** Never use criminal, crime, IPC, Criminal Code, bail, accused, convicted, cyber crime in ad
  copy. Already-shipped ads still carrying it: NCA_Owl_23_criminal, nca_call23_criminal,
  tl09_cyber_it_act ("Cyber crime and IT Act lawyers") -> rename audience to "trial court litigators" /
  "IT Act and cyber law litigators" style without "crime".

## Case 7. NCA "Handling NRI clients' cases in Punjab?": Insufficient original content + Government documents and official services (certificate required)
- **Google reasons:** (a) Insufficient original content. (b) Government Documents and Official
  Services, certificate required.
- **Cause (b):** "NRI clients' cases", "Your NRI files, and the Canadian law behind them", "how Canadian
  firms draft and review their files", and the name "Canadian Law Bootcamp" made it look like an NRI /
  immigration / document-processing service, which needs a government certificate to advertise.
- **Cause (a):** Thin text-only card, half empty, generic copy (and a thin / duplicated landing page).
- **Fix used:**
  - Audience: "Lawyers in Punjab. Many of your clients have family settled in Canada."
  - Headline: "Learn how Canadian contract and tort law works, from Punjab."
  - Bold explanation of the 3 evenings + an original panel "India and Canada are both common law.
    What carries over: contract law principles, tort law principles, reading and applying case law."
  - Fine print: "A legal education programme for lawyers, not an immigration, visa or document service."
  - Brand line "NCA Canada Bootcamp" instead of "Canadian Law Bootcamp".
  - Landing page must be detailed and unique (Google reviews it for original content too).
- **Rule:** Near immigration / NRI / visa / passport / licensing topics, always say it is education
  for professionals and never offer to handle files, documents or applications. Never say "become
  eligible", "get licensed"; say "work toward the Canadian bar".

---

## Issues fixed proactively during resizing (would have been disapproved)
| Found in source ad | Policy | Replaced with |
|---|---|---|
| "JOIN NOW AT ₹10 →", "Know more →", yellow pill buttons | Misleading ad design (arrow, button) | Plain text CTA on the band: "Join the bootcamp for ₹10" |
| iPhone incoming-call card "Canada is calling... Decline / Accept" | Misleading ad design | Headline "Canada is calling." only |
| "Earn from US clients", "Earn in dollars from home", "Start earning", "get paid", "It pays better", "Companies pay for", "Earn a side income", "US lawyers pay remote help", "The bank pays you once" | Financial / income claims (team rule: no money words) | Skill or work lines: "Do tech law work for clients abroad, from home", "Companies need privacy policies. Learn to draft them." |
| $60.7 billion, ₹3.06 lakh crore, ₹25 to 40 lakh LLM, $2,000 a month, salary ranges | Money figures | Non-money facts: "Only 14% of MSMEs have formal credit", "1,475 private deals in 2025" |
| "2026 is the best year", "33,000+ expected in 2026", "from May 2027", "core rules start in 2027" | Predictions (CEO rule) / unverifiable | Present-tense facts, "Here is why" |
| "Our learners already did: 57 cleared NCA, 12 chose province", named learners with jobs | Unverifiable claims / testimonials | Removed |
| "Become eligible for the Canadian bar", "Get licensed", "Be licensed on both sides" | Guarantee / misleading | "work toward the Canadian bar" |
| "Lawyers in their 50s", "Lawyers 45+ and semi-retired" | Personalised ads (age) | "Senior lawyers with decades of practice" |
| "live on Zoom", "muting Slack", "Upwork profile" | Trademarks | "Live online", "muting your chats", "freelance profile" |
| ALL CAPS headlines and labels | Capitalisation / editorial | Sentence case |
| Red text on black, low contrast pairs | CEO rule | Accent colour palette rotated in OKLab, white text on dark band |
| Tiny 290px source PNGs | Image quality | Rebuilt natively, never upscaled |
