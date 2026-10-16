# 01 · Kit structure

## Naming

`<Course>_<Variant>_MediaBuyer_<dates>` — for example `HR_GrowthCamp_Wave10_MediaBuyer_22-24Aug`,
`DataPrivacy_MediaBuyer_29-31Aug`, `CorporateFinance_MediaBuyer_15-17Aug`.

Keep the course token identical across waves of the same course, so `adkit.corpus` and
`CAMPAIGN_MAP.md` group waves into one family and history accumulates instead of only
showing the latest batch.
A folder named `..._Earlier` or `..._Batch1` breaks that grouping. Use a date.

## Layout

```
<Kit>/
  ads/                 the shipped creative, PNG at 1080x1350
  landing_pages/       one self-contained page per ad
  html/                render sources for the ads, relative paths only
  photos/              every image the ad sources reference
  ad_copy.md           paste-ready primary text, headline, description, slug per ad
  README*.md           the launch spec for this drop
  gen_*.py             regenerates the statics and the pages
```

`ads/` plus `landing_pages/` is what makes a folder a kit as far as the brief tool is
concerned. Both must exist even if one is thin.

Everything self-contained. Nothing points outside the folder. Each landing page embeds
its own hero so it works as a single standalone file.

## One ad, one landing page

Never point two ads at one page. The page mirrors its ad's colours, headline wording and
hero device. Every ad gets its own palette; keep a `PALETTE_REGISTER.md` once a pack goes
past about six pairs.

Each page declares its slug on line 1: `<!-- Deploy as /f/<slug> -->`.

## The kit README

Record only what is specific to this drop. Do not restate the launch spec, the judging
rules or the compliance list — link to the SOP instead.

```markdown
# <Course> — media buyer kit — <dates>

<Offer line: dates, times, price incl. GST, live only, refundable, brand.>

N ad units, N landing pages, strict one ad to one page.

## Before traffic — read this first
<Approved vs not approved. Anything that cannot be re-rendered. Any rule this
kit knowingly breaks and why. Open sign-offs.>

## What is in this kit
<Only if it departs from SOP 01.>

## The pairs
| # | Ad | ICP | Landing page | Slug |

## Launch spec — deltas only
Baseline: [SOP/02_LAUNCH_SPEC.md](../SOP/02_LAUNCH_SPEC.md).
<Account if it differs. Ad sets that must be kept separate. CPP if re-baselined.>

## Blockers
<Numbered, each one actionable by a named person.>

## Anchor text, paste-ready
<Or point at ad_copy.md.>
```

## The SHIP format — what actually goes in the zip

**The working kit and the shipped kit are not the same thing, and the shipped one is
leaner.** Recorded 31 Aug 2026 after a Wave 9 handover shipped the whole working folder
and had to be rebuilt. Read `APPROVED/WomenRemote_Wave6/7/8_SEND_THIS/` before zipping —
that is the founder's own format and all three are byte-consistent with each other.

```
<Kit>_SEND_THIS/
  README.md          launch note + the full anchor text, one block per ad
  ad_copy_wN.md      the same anchor text, standalone
  ads/               <STEM>.png
  landing_pages/     lp_<STEM>.html          <- same stem, so pairing is structural
  manifest.json      what the deploy pipeline reads
  kit_meta.json      {"category": "growthcamp"}
```

**Ships:** those six things and nothing else.
**Does not ship:** `html/`, `photos/`, `previews/`, `value_props.md`, `hooks.md`,
`.word-cap`, any `*.py`, any contact sheet. Those are working files. They stay in the
working folder, where the gates and the next rebuild need them.

### Naming

Ad stems continue one series across waves of the same product — Wave 6 ran `X1`–`X6`,
Wave 7 `X7`–`X11`, Wave 8 `X21`–`X30`, so Wave 9 starts at `X31`. Never restart at 01 per
wave: the numbers are how a cell is referred to in reporting months later. The landing
page is always `lp_` plus the ad's exact stem, so no lookup table is needed to pair them.

### `manifest.json`

This is the deployment contract, not documentation. Missing it means the kit cannot ship.

```json
{
  "kit": "wave9",
  "brand": "skillarbitrage",
  "category": "growthcamp",
  "product": "Women's Remote Work Bootcamp",
  "price": "10",
  "currency": "INR",
  "tag": "women-s-remote-work-bootcamp",
  "funnels": [
    {
      "html": "landing_pages/lp_X31_evidence.html",
      "slug": "women-sep05-evidence",
      "name": "X31 Evidence",
      "ctaLabels": ["Book my seat for ₹10"],
      "redeployOver": null
    }
  ]
}
```

- `slug` carries **no `/f/` prefix**, even though the page's line-1 comment and the
  README both write it as `/f/<slug>`. Check the two agree before zipping.
- `ctaLabels` is the button text as it renders on the page.
- `redeployOver` is `null` unless this page replaces a live one at the same slug.
- Keep `product` and `tag` identical across waves of the same course, for the same
  reason the folder name does: history has to accumulate.

### The ship README

Wave 7's shape, which is the fullest of the three: title with camp anchors, a cell table
(`| Cell | ICP | Why it earns a slot |`), an ads-and-pages table with slugs, a launch
note, standing QA notes, then **the full anchor text reproduced per ad** so no second
file is needed. Each anchor block carries **ICP, Primary text, Headline, Description,
Landing page**, in that order.

## Build artifacts

Draft ad HTML lives in the kit's own `html/` folder, not `ads/`, so `preflight.py` does not
double-count it against the rendered PNGs. Do not delete it.

`__pycache__` never ships. Zips are outputs — rebuild them from `make_zip.py` rather than
keeping superseded copies.
