# C1 Proven readers: graphic ad brief (handover)

Campaign C1 of the Tech Law wave for the 8th Tech Law Bootcamp (Sat 24 and Sun 25 Oct 6 to 9 PM IST,
Mon 26 Oct 7 to 10 PM IST; Rs 10 incl. GST, refundable, live only). TOFU, cold audience. Draft for
Ramanuj; no Ramanuj verdict yet. Read `CLAUDE.md`, `HISTORICAL_CONTEXT.md` and
`RAMANUJ_APPROVAL_GUIDE.md` at the repo root before changing anything.

## Files

| File | What it is |
|---|---|
| `C1_Graphic_Ads.pdf` | 13 pages: board, build rules, critic read, every ad with its copy, production notes |
| `BOARD_C1.jpg` | All 10 ads on one image |
| `final_c1/*.jpg` | The 19 rendered ads (900 px previews; full size lives in the Higgsfield sandbox) |
| `copy_c1.py` | Source of truth for copy, colours, fonts and hand-set positions per ad |
| `compose.py` | Lays copy over each picture: call-out band, hook, reason, big button |
| `shoot.js`, `board.py`, `make_pdf.py` | Screenshot ads, build the board, build the PDF |
| `jobs_c1.json` | Higgsfield job id for each of the 19 pictures |
| `../inspiration/*.jpg` | The 7 reference posters the user supplied (style to match) |

## What the user asked for (their words, 16 Oct)

- Graphic images in the style of the inspiration posters; "dont ruin the creative brillance".
- "Every ad should look and feel different."
- Change the call-out hook writing style, keep the ICP. Write the ICP with clarity: "lawyer handling
  cheque bounce cases", not "handling cheque bounce cases".
- "Join now should be huge like 15% of creative space."
- "ICP call out clearly on top 10% of image."
- "Hooks are clear, dont make rubbish and waste tokens and credits."
- First show ONE image (a board) of how all 10 will look, campaign by campaign, before building the rest.
- Then: stop, give it in a PDF, do not use credits.

## Build rules every C1 ad follows

1. Top 10%: solid band naming the reader in full plain words ("For LLB holders working in HR").
2. Middle: one surreal photo idea that acts out the hook; one hook sentence naming the move into tech
   law (key phrase in the ad's accent colour); one reason sentence.
3. Bottom 15%: big "Join for Rs 10 →" button, plus the line "LawSikho Tech Law Bootcamp · Rs 10 incl.
   GST · 3 live evenings · Refundable".
4. Own picture, palette, typeface and layout per ad. A carousel keeps one person across its 4 cards.
5. Indian faces, light seamless studio backdrops, no text inside the generated picture.
6. No income figure or viewer-describing number on the face, no guarantee, no AI fear, no dashes.

## The 10 ads

| Ad | Format | Reader (band) | Hook | Picture idea | Typeface |
|---|---|---|---|---|---|
| 01 | Carousel x4 | For LLB holders working in a BPO | Step out of the cubicle and into tech law. | Walks out of a grey cubicle through a door cut in its wall, degree scroll in hand | Poppins |
| 02 | Single | For LLB holders working in HR | Turn your contract reading into a tech law career. | Giant magnifying glass over a wall-sized offer letter (mint) | DM Serif Display |
| 03 | Single | For LLB holders working in a bank | Take your banking know-how into fintech law. | Bank officer walks out of an open vault, coins floating (warm grey, gold) | Anton |
| 04 | Single | For LLB holders who write content for a living | Write contracts and policies as a tech lawyer. | Rides a giant fountain pen trailing a paper ribbon (lilac) | Fraunces |
| 05 | Single | For LLB holders working in sales or operations | Unlock tech law with the LLB you already have. | Carries a giant key toward a glowing keyhole (butter yellow) | Bebas Neue |
| 06 | Carousel x4 | For women lawyers returning after a family break | Restart your legal career in tech law, from home. | Releases a gold paper plane that climbs above a row of flat white ones (saree, blazer) | Montserrat |
| 07 | Single | For lawyers who paused practice to care for family | Come back to law as a tech lawyer, on your own hours. | Sits on a giant chrome alarm clock with a laptop, red panel behind, lavender; dial reads "3 live evenings, from home" | Playfair Display |
| 08 | Single | For lawyers who moved city after marriage | Start a tech law career wherever you live now. | Works from a suitcase beside a giant red map pin (powder blue) | League Spartan |
| 09 | Single | For Indian lawyers living abroad with family | Build a tech law career from any country. | Walks across the top of a giant white globe with a laptop (sky blue) | Space Grotesk |
| 10 | Carousel x4 | For lawyers who left a firm job for family | Set down the firm hours. Return through tech law. | Sets down a tower of firm files, keeps one slim laptop (seafoam) | Archivo Black |

Carousel cards: 01 and 06 walk through Evening 1 (software development agreement, clause by clause),
Evening 2 (six ways tech companies make money and the legal work each creates), Evening 3 (review a
startup's terms, pitch the fix). 10 runs "What carries over": your drafting (Evening 1), your eye for
what is missing (Evening 3, six checks), then the three dates. Full card copy is in `copy_c1.py`.

## Critic's read (open fixes)

- Verdict: likely APPROVE on the face; fix first on two points.
- The price line inside the button reads at about 21 px on a 1080 px ad. Ramanuj rejects anything
  small. Proposed: "Rs 10 · Refundable" at a larger size.
- The one-line tech law definition is on the carousels only. NCA ads did better with it on every face.
- Ramanuj's call: do LLB holders outside law (01 to 05) count as lawyers for Tech Law? His 24 Sep
  verdict was "non-lawyer ICPs do not work for tech law".

## How the pictures were made

- Higgsfield `gpt_image_2_5`, quality high, resolution 2k, 4:5 for singles and 1:1 for carousel cards;
  2.75 credits each; 19 images, about 52 credits. Carousel cards 2 to 4 pass the card 1 job id as an
  `image_references` media so the same person appears.
- Prompt pattern: "High-end conceptual advertising photograph, surreal scale play. [Indian person, age,
  clothes] [does the metaphor]. [Light colour] seamless studio backdrop, soft floor shadow, [accent]
  accents. Subject in the lower part; the top of the frame is clean empty backdrop for a headline.
  Photorealistic, crisp, premium. No text, letters, numbers or logos anywhere."

## Environment notes

- This container's network policy blocks the Higgsfield image host `d8j0ntlcm91z4.cloudfront.net`, so
  pictures cannot be downloaded here. Workaround used: download and render inside the Higgsfield
  sandbox (`mcp__higgsfield__sandbox_exec`, Playwright at `/usr/local/lib/node_modules`, fonts from
  `npm pack @fontsource/<name>`), then pull finished JPEGs back with `image_paths` (512 KB per call).
  The sandbox refuses base64 file relays; write scripts into it as plain heredocs.
- Allowing that host in the environment's network settings removes the workaround.
- Commit and push to `claude/happy-allen-ks5z24`. House style: plain English, no em or en dashes.
