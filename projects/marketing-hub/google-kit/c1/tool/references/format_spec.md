# Ad format specification (all sizes)

See the sample images in `examples/` (C1 of every template in all 3 sizes, and the 4 colours of one ad).

## Sizes and files
| Size name | Pixels | Google use | File name pattern |
|---|---|---|---|
| landscape | 1200 x 628 (1.91:1) | Display, PMax, Demand Gen landscape | `<slug>_C<n>_landscape_1200x628.jpg` |
| square | 1200 x 1200 (1:1) | Display, PMax, Demand Gen square | `<slug>_C<n>_square_1200x1200.jpg` |
| portrait | 960 x 1200 (4:5) | PMax / Demand Gen portrait | `<slug>_C<n>_portrait_960x1200.jpg` |

`<n>` = 1, 2, 3, 4 (colour version). 3 sizes x 4 colours = **12 files per ad**. JPEG, RGB,
progressive, quality 76 to 90 (82 default), each file well under Google's 5 MB limit.

## Colour versions
- **C1** = the ad's own accent colour (taken from the source ad's main brand/accent colour).
- **C2, C3, C4** = the accent hue rotated +90, +180, +270 degrees in OKLab. Lightness and chroma are
  kept, so contrast is identical in every version; chroma is pulled in only if a colour falls outside sRGB.
- From each accent the renderer derives: background = accent mixed 88% with white, texture dots =
  accent mixed 78% toward the background, band = accent mixed 28% with black.
- Photos and logos are never recoloured. Text stays near-black on the background and white on the band.

## Grid and safe area (every size)
- Safe box = centre 80%: left/top margin = 10% of width/height. All text, logos and photos (except
  full-bleed elements) sit inside it.
- Full-bleed elements: tinted textured background, bottom band (from 22px above the CTA to the bottom
  edge), and in landscape photo ads the left 42% photo panel.
- Everything uses one scale variable `--s`; the renderer starts at 1.7 and shrinks by 0.01 until
  nothing overflows the safe box. A final scale under 0.70 means the copy is too long.

## Base type sizes (multiplied by --s)
| Element | Font | Base size |
|---|---|---|
| Logo image height (LawSikho, NCA, SkillArbitrage PNGs in `assets/logos/`) | image | 40px |
| Product label on the right of the brand row | Inter 800, accent colour | 19px |
| Audience box title | Poppins 800, white on accent | 34px |
| Audience box situation | Inter 600, white | 22px |
| Headline (sans) | Poppins 800, accent part coloured | 56px (list), 46px (numbered), 50px (photo) |
| Headline (serif option) | Source Serif 4 800, accent part italic | same sizes |
| Value line (optional) | Inter 800, accent colour | 30px |
| Explanation | Inter 800, accent left rule 8px | 26px (23-24px in numbered/photo) |
| Bullets | Inter 600, accent dot | 23px |
| Numbered item title / detail | Inter 800 / Inter 500 | 23px / 18px |
| CTA (on band) | Poppins 800 white | 44px |
| Fine print (on band) | Inter 600 white | 16px |
| Note (on band) | Inter 500 white | 13px |

## Order of blocks
**Portrait and square (stacked):**
1. Brand row: logo left, second logo or product label right
2. Audience box (role + situation)  <- always first box
3. Headline (+ accent part)
4. Value line (optional)
5. Explanation (bold, left rule)      [list template]
   / numbered items, then explanation [numbered template]
   / photo (fills the free space), then explanation [photo template]
6. Bullets (list template)
7. Spacer
8. Band: CTA, fine print (dates · timings · price incl. GST, refundable · live only), optional note

**Landscape (two columns):**
- list: left 52% = audience box + headline; right = value line or first 3 bullets; band below.
- numbered: left 46% = audience box + headline; right = item titles only (no details); band below.
- photo: photo panel full-bleed on the left 42%; text column (brand, audience box, headline) on the
  right; band below across the full width.

## Templates and when to use them
| Template | Use for source ads that are | Example |
|---|---|---|
| list | Headline + short paragraph + 3-4 points (most ads) | NCA trial court litigators |
| numbered | Infographics, steps, "N reasons", "N ways", catalogues | CorpFinance bank RM |
| photo | Ads built around a real photo of the audience | g_litigator |

For concept art in the source (owl, puzzle piece, illustrations) crop the clean art region from the
source (only if it is at least ~450px wide) and place it next to the headline; if the source is tiny,
draw a simple SVG of the same concept instead of upscaling.

## Folder structure
```
<Kit>_Resized/
  01_<Audience_Folder>/
    <ad_slug>/
      <ad_slug>_C1_landscape_1200x628.jpg
      <ad_slug>_C1_square_1200x1200.jpg
      <ad_slug>_C1_portrait_960x1200.jpg
      ... C2, C3, C4 ...
  10_Women_<...>/            <- women-only ads always in their own folder
```
Flat mode (only when asked): `<Kit>_Resized/<ad_slug>/<12 files>`.
Slug = the source ad file name without extension and without a trailing `_1080x1350`.
