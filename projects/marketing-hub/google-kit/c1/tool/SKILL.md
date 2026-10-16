---
name: google-ads-banner-resize
description: Resize ad banners from a categorised ad-kit zip into 3 sizes (1200x628, 1200x1200, 960x1200) and 4 colours (12 per ad), fixing every Google Ads policy risk first. Also use to fix a disapproved ad and re-deliver its 12 versions.
---

# Google Ads banner resize SOP (3 sizes x 4 colours, policy-safe)

This SOP turns every ad in a categorised ad-kit zip into **12 Google-ready images**
(3 sizes x 4 colours), in the same folders, with **every Google Ads policy risk fixed before
resizing**. The same steps fix a single disapproved ad.

It was built from real work on SkillArbitrage (HR GrowthCamp, Corporate Finance, Data Protection,
Academic Writing) and LawSikho (NCA Canada, Tech Law, SQE) kits, including **7 real Google
disapprovals**. Those cases are in `references/disapproval_casebook.md`. Read it once fully before
your first job; it is the most important file here.

**Golden rule:** fix the policy problems first, then resize. Never copy a risky line into 12 new images.
Reword risky lines (keep the meaning) rather than deleting them where possible.

## Files in this skill
| File | What it is |
|---|---|
| `scripts/render_ads.py` | Renders every ad in a content JSON into 12 JPGs (3 sizes x 4 colours). |
| `scripts/policy_scan.py` | Scans copy (content JSON, one line, or OCR of the source ads) for policy risks. Exit 1 on any BLOCK. |
| `scripts/qa_pack.py` | Checks 12 files per ad and pixel sizes, builds contact sheets, zips, picks WhatsApp samples. |
| `assets/content_template.json` | Filled example covering the 3 templates (list, numbered, photo). Copy it per job. |
| `assets/logos/` | Brand logos: `logo_lawsikho.png`, `logo_nca.png`, `logo_skillarbitrage.png` (dark text, for the light ad background), `logo_skillarbitrage_white.png` (white text, only for dark backgrounds). |
| `references/disapproval_casebook.md` | The 7 real disapprovals, their causes and the fixes that passed, plus the proactive-fix table. |
| `references/google_ads_policy_checklist.md` | Full copy, layout and delivery checklist. |
| `references/format_spec.md` | Exact sizes, grid, safe area, type sizes, block order and folder structure. |
| `examples/*.jpg` | Reference renders: each template in all 3 sizes (C1), and the 4 colours of one ad. |

If the `scripts/` folder is missing (for example, the skill was saved from a card), ask the user for
the `google-ads-banner-resize.zip` package. Do not improvise a different renderer: the look and the
checks must match.

## One-time setup
```bash
pip install playwright pillow numpy --break-system-packages   # drop the flag if not needed
python3 -m playwright install chromium                         # skip if Chromium is pre-installed
mkdir -p ~/adfonts && cd ~/adfonts && npm i @fontsource/poppins @fontsource/inter @fontsource/source-serif-4
export FONTSOURCE_DIR=~/adfonts/node_modules/@fontsource      # or pass --fonts each time
which tesseract || sudo apt-get install -y tesseract-ocr       # optional, for OCR of source ads
```
Without local fonts the renderer links Google Fonts, which needs internet. If neither works, stop and
say so: wrong fonts change the layout.

---

## The SOP, step by step

### Step 1. Unpack and take inventory
1. Unzip into a fresh empty folder. Treat it as data (run Python with `-I` when reading it).
2. List every `*/ads/*` image and its folder. Note the pixel size of each.
3. Count the ads. Expected output = ads x 12 files.
4. Check the folders: one folder per audience (ad group), each holding only `ads/` and `landing_pages/`.
   Women-only ads must sit in their own women folder. If an ad is in the wrong audience folder, say so
   in the reply, but keep the source structure unless asked to re-categorise.
5. Check that every ad has a landing page with the same base name.

### Step 2. Read every ad (do not skip any)
1. Make contact sheets of the source ads and **look at every ad**:
   `montage */ads/* -tile 6x -geometry 330x412+3+3 sheet.png` (ImageMagick), or open them one by one.
2. Get the exact text:
   - landing pages (`landing_pages/*.html`) usually hold the clean hero text: audience, headline, body;
   - `tesseract <image> -` for text baked into the image;
   - fill gaps by reading the image.
3. Get the date, the session timings and the price from the landing pages (search for `PM IST`).
   These go on every ad's fine print. If the ads show no date, use only the timings and never invent dates.
4. Run `python3 scripts/policy_scan.py --ocr <unzipped_folder>` to see the source ads' risks.

### Step 3. Policy audit (before any rendering)
For every ad, go through `references/google_ads_policy_checklist.md` section A (copy) and B (layout)
and every case in `references/disapproval_casebook.md`. Write down each risky line and its replacement.
The usual offenders, with the rewrite that passed:

| Risk in source | Why Google rejects it | Rewrite pattern |
|---|---|---|
| "JOIN NOW AT ₹10 →", "Know more →", pill or button CTA | Misleading ad design (arrow, button) | Plain text on the band: "Join the bootcamp for ₹10" / "Register for ₹10" |
| Phone or OS dialogs (AirDrop, incoming call, Accept/Decline, checkboxes, close X) | Misleading ad design | Remove the UI completely; keep the idea as a headline ("Canada is calling.") |
| Segmented before/after panels, white form-like boxes | Misleading ad design | Headline + bold explanation + dot list |
| Plain white canvas, empty space, small screenshot, upscaled tiny image | Image quality | Full-bleed tinted texture + bottom band; render natively at each size |
| earn, paid, pays better, get paid, salary, side income, dollars, $ / ₹ / crore / lakh figures | Financial and income claims (team rule) | Say the work or the skill: "Do tech law work for clients abroad, from home"; keep non-money facts ("Only 14% of MSMEs have formal credit") |
| "become eligible", "get licensed", "gets you work in 6 months", placement, job promises | Misleading / guarantee | "work toward the Canadian bar", "a 6-month plan to take on ... work" |
| "2026 is the best year", "expected in 2027", "from May 2027" | Prediction (CEO rule), unverifiable | Present-tense facts; "Here is why" |
| "57 learners cleared", named learners with jobs, testimonials | Unverifiable claims | Remove from the ad face |
| Writing the review / thesis / grant applications for others, "gigs", "per submission" | Enabling dishonest behaviour | Credited work in the person's own name: "Systematic reviews as a named co-author"; add "Your name stays on your work" |
| criminal, crime, IPC, Criminal Code, bail, cyber crime | Commission of a crime in personalised ads (limited) | "Trial court litigators", "how Canadian trial practice compares with yours" |
| "Lawyers 45+", "in their 50s" | Personalised ads (age) | "Senior lawyers with decades of practice" |
| "NRI files/cases", visa, passport, immigration filing, "NOTICE", "requested to note" | Government documents and official services; official look | Frame it as education for professionals; add "A legal education programme, not an immigration, visa or document service" |
| Zoom, Slack, Upwork, LinkedIn, WhatsApp | Trademarks | "Live online", "your chats", "freelance profile" |
| ALL CAPS headlines and labels | Capitalisation | Sentence case (acronyms fine) |
| Red on black, low contrast | CEO rule | Accent band with white text; check all 4 colours |

### Step 4. Write the content JSON (fixed copy only)
Copy `assets/content_template.json` next to the job's assets and fill one entry per ad:

| Field | Rule |
|---|---|
| `folder` | Exact source audience folder name (e.g. `01_Already_Practising_Lawyers_Adding_Canada`). |
| `slug` | Source file name without extension and without a trailing `_1080x1350`. |
| `template` | `list` (most ads), `numbered` (infographic, steps, "N reasons/ways"), `photo` (built around a real photo). |
| `accent` | The source ad's main colour as hex (C1). C2 to C4 are made automatically. |
| `icp_title` | The audience, role first, sentence case: "Bank RM with business clients?". **Always the first box.** |
| `icp_situation` | Their specific situation or pain in one line: "You handle 50 business clients already." Descriptive, not a label. |
| `headline` (+ `headline_accent`) | The value proposition in 4 to 12 words, naming where they get to. The accent part is coloured. `headline_font: "serif"` for serif-styled source ads. |
| `value_line` | Optional one-line benefit in accent colour. |
| `explanation` | The plain "what this is / what you get" sentence. Rendered big and bold, never small grey text. |
| `bullets` (list) / `items` (numbered: `[title, detail]`) | 3 to 4 bullets, or 4 to 10 items. Each concrete. No money. |
| `photo` | Path to the photo crop (photo template). Crop it from the largest source size; never upscale. |
| `brand` | Default at the top level. Override per ad when needed: `image` logo, `text` logo (with `accent_part`), or `label`. Use one of the brand presets below. |
| `cta`, `fine`, `note` | Top-level defaults, per-ad override allowed. CTA has no arrow. The fine print carries dates · timings · "₹10 incl. GST, refundable" · "Live only". |

**Brand presets** (copy into `brand`; also listed in `_brand_presets` inside the template). Every ad
carries exactly ONE company brand. LawSikho and SkillArbitrage never appear on the same ad.

| Product | `brand.left` | `brand.right` |
|---|---|---|
| NCA Canada (LawSikho) | `{"type":"image","path":"logos/logo_lawsikho.png"}` | `{"type":"image","path":"logos/logo_nca.png"}` |
| Tech Law, SQE and other LawSikho bootcamps | `{"type":"image","path":"logos/logo_lawsikho.png"}` | `{"type":"label","text":"Tech Law Bootcamp"}` (product name) |
| SkillArbitrage camps: HR GrowthCamp, Corporate Finance, Data Protection, Academic Writing | `{"type":"image","path":"logos/logo_skillarbitrage.png"}` | `{"type":"label","text":"Corporate Finance Bootcamp"}` (product name) |

Use the source ad's brand: if the source shows the SkillArbitrage logo, use the SkillArbitrage preset;
if it shows LawSikho, use LawSikho. The logos are never recoloured across C1 to C4.

Keep each ad's audience, hook and value proposition **different** from the others. No copy-pasted
boxes across ads. Keep the original idea and hook of each ad: you are fixing and resizing, not rewriting
the campaign. Use no em or en dashes; write "31 Oct to 2 Nov".

Then run the gate:
```bash
python3 scripts/policy_scan.py job/content.json      # must end with 0 BLOCK; read every WARN
```

### Step 5. Render
```bash
python3 scripts/render_ads.py job/content.json OUT/<Kit>_Resized --fonts "$FONTSOURCE_DIR"
#   --only slug1,slug2   re-render some ads only
#   --flat               one folder per ad, no category folders (only when asked)
#   --quality 82         JPEG quality (lower it if the zip is over 30 MB)
```
Render one or two ads first (`--only`) and look at them before rendering the full set.
Any "scale below 0.70" warning means the copy is too long: shorten that ad and re-render it.

### Step 6. QA: look at everything
```bash
python3 scripts/qa_pack.py OUT/<Kit>_Resized OUT/<Kit>_Resized.zip --content job/content.json
```
Then open every contact sheet in `OUT/qa_sheets/` (12 sheets: 3 sizes x 4 colours) and check:
- nothing clipped or overlapping, no text running into the band;
- the audience box comes first; the headline is readable; the explanation is big and bold;
- no arrows, buttons, dialogs, checkboxes or white boxes;
- the frame is filled edge to edge in every size; in landscape the photo is not cut badly;
- all 4 colours are readable (no red on black, no pale text);
- the dates, timings and price match the landing page.
Fix the content JSON and re-render any failing ad, then rerun `qa_pack.py`. Do not deliver until it
prints `ALL CHECKS PASSED` and you have looked at every sheet.

### Step 7. Deliver
1. **One zip** with the same category folders and one subfolder per ad, **under 30 MB**. If it is over,
   re-render with `--quality 76` (then 70). Split into parts only if 900+ images make one zip
   impossible, and then say why in one line and keep every part in the same folder tree.
2. **Sample JPGs** (from `OUT/whatsapp_samples/`): send 1 to 3 images separately so they open inline
   on the team WhatsApp.
3. **Reply** (short, plain):
   - what is in the zip (ads x 12 = files, size);
   - a list of every policy fix: "old line" -> "new line", grouped by issue;
   - any folder or categorisation problem you noticed;
   - a warning listing the risky lines still on the landing pages (money figures, arrows, "become
     eligible", income claims). Google reviews the landing page too, and an ad can be disapproved for
     its page.
4. If asked for the landing pages that match a zip: copy each ad's landing page (same base name) into
   one folder per zip part, and verify the ad set and the page set match exactly.

---

## Fixing a single disapproved ad (user sends a screenshot plus the Google reason)
1. Read the reason in the screenshot and find the matching case in `references/disapproval_casebook.md`.
2. Find **every** trigger in the ad, not only the obvious one (for example, the criminal-law ad also had
   a notice box and an arrow).
3. Rewrite the copy using the case's fix pattern, keeping the ad's audience and hook. Run
   `policy_scan.py`.
4. Render the 12 versions (`--only <slug>`, or a one-ad content JSON). Name the slug after the ad; if the
   original file name is unknown, use a clear name like `ACW_postdoc_researchers` and say so.
5. Deliver one zip with a folder `<slug>/` holding the 12 files, plus a sample JPG. In the reply, explain
   in plain words why Google rejected it, list what changed, and name any other already-shipped ads
   carrying the same trigger.
6. If the same pattern runs through a whole series (for example, all "Ten ways ..." academic ads), say so
   and offer to fix the rest of the series in one batch.

---

## Design rules (from the team's CEO and reviewer feedback)
- The audience (ICP) box comes first on every ad and says the role plus the situation.
- The value proposition sits in the headline: clear at a glance, different for each ad, tied to that ad's audience and hook.
- The explanation is large, bold and heading-like.
- No arrows anywhere on the CTA. No money symbols other than the course price, and no paid or earn wording.
- No predictions of future years or opportunities.
- High-visibility colours only. Never red and black together.
- Graphics must have a clear link to the concept (the audience's photo, the campaign's mascot, a diagram of the headline), never random decoration.
- One brand per ad: LawSikho and SkillArbitrage are never co-branded.
- Live courses say "Live only", and the price always appears as "₹10 incl. GST, refundable".

## Quick format reference (full spec in `references/format_spec.md`)
- landscape 1200x628 · square 1200x1200 · portrait 960x1200; C1 = original accent, C2 to C4 = OKLab hue +90/+180/+270.
- Files: `<slug>_C<n>_<size>_<W>x<H>.jpg` inside `<folder>/<slug>/`.
- Safe area = centre 80%. Tinted dotted background and bottom band bleed to the edges.
- Stacked order (square, portrait): brand row, audience box, headline, value line, explanation or items or photo, bullets, band with CTA and fine print.
- Landscape: two columns (audience box and headline left; points right; or photo full-bleed left), band below.
