# Google kit, same design as Meta (Tech Law C1)

The 10 supplied creative images, unchanged, in the three Google image sizes. Nothing on any ad is redrawn,
retyped or recoloured. Where the Google shape differs, the whole ad is kept and the rest is a colour wash made
from the ad's own edge pixels.

| Folder | Size | Files |
|---|---|---|
| `landscape_1200x628/` | 1.91:1 | 10 |
| `square_1200x1200/` | 1:1 | 10 |
| `portrait_960x1200/` | 4:5 | 10 |

30 files, all under 5 MB. Text assets (headlines, descriptions, URLs): `../c1/GOOGLE_COPY_C1.csv`.
Rebuild: `python3 build_same_design.py`.

## QA (done)
- Sizes exact on all 30; every file under 5 MB.
- Each ad checked against the supplied image: mean pixel difference at most 3.4 out of 255 (resizing and JPEG only).
- Native fit (no padding): portrait for ads 04 to 09 (4:5 sources). Everything else sits on a wash.
- Landscape: the ad is 502 px wide inside 1200 px, so its small text is hard to read in feeds. That is the
  price of "nothing cropped".

## Risk, in the team's own casebook terms (your call)
These designs contain the patterns Google disapproved before (`../c1/tool/references/disapproval_casebook.md`):
1. **"JOIN FOR ₹10 ->"** a red button shape with an arrow: Misleading ad design (cases 3 and the SOP table).
2. **All-capital labels** ("FOR LLB HOLDERS ..." pills, "TECH LAW BOOTCAMP", the button): capitalisation.
3. **Text on a photograph with chips and boxes** (cream boxes with icons): can read as UI or form boxes.
4. **Wording:** "in-house" chips (05, 08, 09, 10), "international practice" (07), personal-situation labels
   ("paused practice for family", "moved cities after marriage", "women lawyers ... family break") for personalised ads.
If Google disapproves one, the policy-safe set in `../c1/OUT/Tech_Law_C1_Google/` (120 images) is the fallback.
Run these first as a small test; do not put the whole budget behind them before they pass review.
