# Google Ads policy checklist for display / PMax / Demand Gen image ads

Run this on EVERY ad before rendering (copy check) and again on the rendered contact sheets
(layout check). One "no" = fix first. `scripts/policy_scan.py` catches most copy problems; the
layout items can only be checked by looking.

## A. Copy (what the ad says)
1. **No money or income claims.** No earn / earning / paid / pays / get paid / salary / income /
   side income / "pays better" / dollars. No ₹ or $ amounts except the course price (₹10, ₹100).
   No crore / lakh / billion figures. (Google: Financial services and Misrepresentation; team rule.)
2. **No guarantees or outcome promises.** No "get a job", "land clients", "in 6 months you will",
   "placement", "become eligible", "get licensed". Use "a plan to", "learn how to", "work toward".
3. **No predictions or future years.** No "2027 will", "best year", "expected in", "from May 2027".
   Present-tense facts only. (CEO rule.)
4. **No unverifiable superlatives or results.** No "#1", "only", "best", "record", "desperately need",
   learner result counts ("57 cleared"), named learners with outcomes, testimonials. A metaphorical
   line like "the only call for your comeback" is allowed only if it makes no factual claim.
5. **No dishonest-behaviour enablement.** Never imply doing someone else's academic work, exams,
   assignments, theses, reviews, grant applications or submissions. Always "in your own name",
   "as a named co-author", "credited". No "gigs", "per submission", "bought".
6. **No sensitive personal categories in targeted ads.** No crime / criminal / IPC / bail; no age
   ("45+", "in their 50s"); no health, religion, caste, sexual orientation, financial hardship,
   pregnancy, disability. Describe a role or situation neutrally.
7. **No government / official service look.** No "NRI files/cases", visa, passport, immigration filing,
   apostille, document services, "notice", "requested to note", official seals, government logos.
   Add "A legal education programme, not an immigration, visa or document service" near such topics.
8. **No third-party trademarks.** Zoom, Slack, Upwork, Fiverr, LinkedIn, WhatsApp, Google Meet, Clio,
   ChatGPT, Big 4 names. Use generic words.
9. **No ALL CAPS** words in headline, labels or CTA (acronyms like NCA, LLB, DPDP, GST, IST are fine).
10. **No em or en dashes** (house rule). Use "to", commas or full stops ("31 Oct to 2 Nov").
11. **Price line wording:** "₹10 incl. GST, refundable" (or "refundable anytime") wherever a price is shown.
    Live courses say "Live only" / "Live only, no recordings".
12. **One brand per ad.** LawSikho and SkillArbitrage are never co-branded on one ad.
13. **Every claim must be true for the bootcamp** and match the landing page (dates, timings, price,
    what is taught). The landing page must not contain the risky lines either; Google reviews it.

## B. Layout (how the ad looks)
1. **Fills the frame.** Tinted textured background on the whole canvas and a full-bleed bottom band.
   No white card floating on white, no big empty areas. (Image quality.)
2. **Native resolution.** Render each size directly at 1200x628, 1200x1200, 960x1200. Never upscale a
   small source, never upload a screenshot. JPEG quality 76 to 90.
3. **No fake UI.** No dialogs, notifications, incoming-call cards, Accept/Decline, close X, play
   buttons, cursors, checkboxes, toggles, input boxes, segmented before/after panels.
4. **No button-shaped CTA and no arrows.** CTA is plain text on the band. No pill, no rounded button,
   no →, ➜, >, chevrons.
5. **Readable text.** Nothing below about 13px at 1200 wide. Text scale reported by the renderer must
   stay at or above 0.70; if lower, shorten the copy. Logo and text never cut off at any edge.
6. **Safe area.** All content inside the centre 80% (10% margin each side). The band may bleed.
7. **High-visibility colours.** White on dark accent band, near-black on tinted background. Never red
   text on black or black on red. Check all 4 colour versions, not just C1.
8. **Visual has a clear link to the message** (photo of the audience, owl or puzzle piece of the
   concept, a simple diagram of the headline). No random stock decoration.
9. **Audience box first.** The first box under the logo names the role AND their situation in plain words.
10. **Explanation is big and bold.** The explanatory paragraph is heading-like (bold, about 26px at
    1200 wide, accent left rule), never small grey text.

## C. Delivery
1. 12 files per ad: C1 to C4 x landscape, square, portrait. Names `<slug>_C<n>_<size>_<W>x<H>.jpg`.
2. Same category folders as the source, one subfolder per ad named exactly like the ad (unless the
   requester asks for flat, one folder per ad).
3. Women-only ads stay in their own women folder.
4. One zip under 30 MB (re-render at lower JPEG quality before ever splitting).
5. Send 1 to 3 sample JPGs separately so they open inline on WhatsApp.
6. In the reply, list every policy fix made, and warn about risky lines still on the landing pages.
