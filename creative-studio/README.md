# LawSikho Creative Studio (local, free)

Spreadsheet of readers in, finished ad posters out. Hero images are made **on your Mac**
with a free, open model; every word on the poster is typeset by Python, never by the model.

```
data/icps_template.xlsx ──► hero image per reader (AI, no text) ──► poster (exact copy, fixed template) ──► contact sheet
```

## The stack (chosen 22 Oct 2026, one tool, no overlap)

| Part | Choice | Licence | Why |
|---|---|---|---|
| Image engine | [MFLUX](https://github.com/filipstrand/mflux) 0.23+ | MIT | Native Apple Silicon (MLX), one command per image, no server |
| Model | Z-Image Turbo (`Tongyi-MAI/Z-Image-Turbo`, mflux name `z-image-turbo`) | Apache-2.0, not gated | MFLUX's recommended model now; 6B, 9 steps, photoreal people |
| Smaller option | `filipstrand/Z-Image-Turbo-mflux-4bit` (~6 GB) | tagged *tongyi-qianwen-license* on Hugging Face | For 8 to 16 GB Macs. Read that licence before commercial use |
| Posters | Pillow, pandas, openpyxl | MIT-style / BSD | Exact text, exact layout, batch from Excel |
| Fonts | Playfair Display, Anton, Inter | SIL OFL 1.1 | Free for commercial use; fetched by `scripts/fetch_fonts.sh` |

Not chosen: **FLUX.1 schnell** (Apache-2.0 but gated on Hugging Face, and MFLUX now lists
FLUX.1 as legacy); **ComfyUI** (node-graph app and server: more to install and nothing this
batch pipeline needs). Requirements checked against the MLX docs: Apple Silicon, macOS 14+,
native arm64 Python 3.10+. **Intel Macs cannot run MLX**, so they use posters-only mode.

## What runs where

| Step | Where | Verified in the cloud build? |
|---|---|---|
| Poster rendering, validation, batch, contact sheet | any computer | **Yes**: 24 tests pass; 20 posters + contact sheet rendered with placeholder heroes |
| `setup_mac.sh` | your Mac | Ran end to end on Linux in posters-only mode (venv, install, fonts, .env, report) |
| `mflux` install | your Mac | Installed (0.23.0) and its CLI flags read from source; it cannot *run* without a Mac GPU |
| Model download + hero generation | your Mac only | **Not verified**: no Apple Silicon here. First real test is step 4 below |

## Run it on your Mac

Open **Terminal** (not under Rosetta) and run these one at a time.

```bash
# 1. Get the code
git clone https://github.com/Nityaa369/Marketing0510.git
cd Marketing0510/creative-studio

# 2. Look before installing (changes nothing): chip, macOS, RAM, disk
python3 scripts/check_environment.py

# 3. One-time setup into ./.venv (no sudo). If it says uv is missing: brew install uv
bash scripts/setup_mac.sh
source .venv/bin/activate          # do this in every new Terminal

# 4. Download the model AND make a 256px test image (asks first; ~31 GB, or --small for ~6 GB)
python scripts/download_model.py   # 16 GB RAM or less:  python scripts/download_model.py --small

# 5. One hero image, then one poster. Look at both before going further.
python scripts/generate_hero.py --sheet data/icps_template.xlsx --row nca01_new_grads
python scripts/render_poster.py --sheet data/icps_template.xlsx --row nca01_new_grads
open outputs/individual_ads/nca01_new_grads.png

# 6. All 20 readers + contact sheet
python scripts/generate_batch.py --sheet data/icps_template.xlsx
open outputs/contact_sheets/
```

RAM guide: 24 GB+ keep `STUDIO_QUANTIZE=8`; 16 GB set `STUDIO_QUANTIZE=4` in `.env`;
8 GB use `--small` and expect slow runs. Time per image depends on the chip; the batch log
records the real seconds for every image (`outputs/logs/`).

**No Mac at hand (cloud session, office PC):** `STUDIO_HERO_BACKEND=hf_space` (or
`--backend hf_space`) calls the free public demo of the same model on Hugging Face
(`Tongyi-MAI/Z-Image-Turbo` Space) instead of running it locally. Any machine works, nothing
to download. Trade-offs: a shared GPU with queues and daily quotas, fixed output sizes (the
closest aspect ratio is used), and the prompt leaves your machine. Set `HF_TOKEN` in `.env`
for a higher quota.

**Intel Mac or no model yet:** `bash scripts/setup_mac.sh --posters-only`, put photos in
`assets/hero_images/`, fill the `hero_image` column, run step 6. To test the pipeline with
labelled stand-in images: `python scripts/generate_batch.py --sheet data/icps_template.xlsx --backend placeholder`.

## Your spreadsheet

`data/icps_template.xlsx` has 20 **example** NCA rows (real reader segments, sample copy:
approve every line before launch) and a `READ_ME` tab. Columns:

| Column | Required | Notes |
|---|---|---|
| `id` | yes | file name, letters/numbers/`_`/`-` |
| `campaign` | yes | for the media buyer |
| `icp` | yes | reader name; the ICP line becomes **{ICP} WANTING CANADIAN LEGAL PRACTICE 🍁** unless `banner` is filled |
| `headline` | yes | the big line; wrap a phrase in `*asterisks*` for red italic. Canada/Canadian/NCA are always red |
| `supporting` | yes | one plain line, set in red (never grey) |
| `cta` | yes | must contain JOIN NOW |
| `hero_prompt` | yes, unless `hero_image` | people and place only, never text |
| `banner`, `price`, `price_line`, `journey_tab`, `hero_image`, `seed` | no | blanks use brand defaults |

Change copy in the sheet and re-run: only changed rows are redone. Change brand facts
(dates, price, terms, banned phrases) in `config/brand.json`. Change geometry in
`templates/ncacanada/layout.json`.

## What the NCA template enforces

- Header: the LawSikho | NCA CANADA BOOTCAMP lockup (`assets/logos/lawsikho_nca_lockup.png`, from the owl ad).
- ICP line: yellow highlighter, Anton, "{READER} WANTING CANADIAN LEGAL PRACTICE" + maple leaf, one line, auto-sized.
- Pop-out **Start your Canadian Legal Practice journey** tab over a full-width red bar:
  **JOIN NOW AT ONLY ₹10 / for all 3 days · 9 hours of knowledge-enriching sessions**.
  The bar is 15.3% of the poster; rendering fails below 15%.
- Footer terms: ₹10 incl. GST · refundable · live only · 31 Oct to 2 Nov 2026.
- Validation **blocks** a row for: missing fields or hero, bare price (no "3 days" and
  "9 hours"), banned claims (100% pass, guaranteed, closes today, last day, assesses, aids,
  and others in `brand.json`), "Canadian practice" (must be Canadian Legal Practice),
  em or en dashes, CTA without JOIN NOW, duplicate ids.
- Text that cannot fit at the minimum size fails with `text overflow in '<field>'`
  instead of being cut off. Output size is checked after export (2160 x 2700 PNG, 4:5).
- The lockup is cropped from an existing ad (797 px wide), so it is slightly upscaled on the
  2x export. Replace it with a higher-resolution original at the same path when you have one.
- Posters made from placeholder heroes are flagged in the report and on the contact sheet.

## Failures and re-runs

Each run writes `outputs/batch_state.json`, `outputs/batch_report.csv` and a dated log in
`outputs/logs/`. A failed hero or poster is logged and the batch carries on. Run the same
command again and only failed or changed rows are redone (`--force` redoes posters,
`--only id1 id2` picks rows, `--limit 1` tries one).

## Layout

```
creative-studio/
├── config/brand.json            brand colours, fonts, camp facts, banned phrases
├── templates/ncacanada/layout.json   fixed poster geometry (1080x1350 base, exported at 2x)
├── data/icps_template.xlsx      20 example rows + READ_ME
├── studio/                      the engine (sheet, hero, poster, batch, contact_sheet)
├── scripts/                     check_environment, setup_mac.sh, fetch_fonts.sh, download_model,
│                                generate_hero, render_poster, generate_batch, create_contact_sheet,
│                                make_sample_sheet
├── tests/                       pytest: validation, poster, hero command, batch + re-runs
├── assets/logos/                 NCA lockup (committed)
├── assets/{fonts,references,hero_images}/   local only, not committed
└── outputs/{individual_ads,contact_sheets,logs}/  local only, not committed
```

Git never receives model weights (they live in `~/.cache/huggingface`), generated images,
fonts or `.env`. Run tests with `pytest`.
