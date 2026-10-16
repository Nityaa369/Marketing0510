---
name: project-ship-zip-house-format
description: "The final SEND_THIS zip is leaner than the working kit — six items only, plus manifest.json, with ad stems continuing one X-series across waves"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a3d0333-bb8b-40f2-94d0-089942c945ac
  modified: 2026-08-31T10:13:35.948Z
---

The zip that goes to the team is **not** the working folder. It carries exactly six
things and nothing else:

```
<Kit>_SEND_THIS/
  README.md  ad_copy_wN.md  ads/  landing_pages/  manifest.json  kit_meta.json
```

Working files stay behind: `html/`, `previews/`, `photos/`, `value_props.md`, `hooks.md`,
`.word-cap`, any `*.py`, any contact sheet.

- **`manifest.json` is the deployment contract** and a kit without one cannot ship. Its
  `slug` has **no `/f/` prefix**, though the page's line-1 comment and the README both
  write `/f/<slug>`. Verify they agree.
- **Ad stems continue one X-series across waves of a product**, never restarting per
  wave: Wave 6 `X1`-`X6`, Wave 7 `X7`-`X11`, Wave 8 `X21`-`X30`, Wave 9 `X31`-`X36`. The
  landing page is `lp_` + the ad's exact stem, so pairing needs no lookup.
- The README follows Wave 7's shape: camp anchors, cell table with "why it earns a slot",
  ads-and-pages table with slugs, launch note, standing QA notes, then the full anchor
  text per ad (ICP / Primary text / Headline / Description / Landing page).

**Why:** the media buyer and the deploy pipeline are the audience, not a reviewer.

**How to apply:** before building any handover zip, open
`APPROVED/WomenRemote_Wave6/7/8_SEND_THIS/` and copy that structure. Recorded 31 Aug 2026
after shipping the whole working folder, then a stripped-down invention of my own, before
being pointed at the format that already existed. **Look at what the last approved wave
shipped before designing a zip.** Also note: a pending sign-off is a launch gate, not an
approval verdict — an approved ad still belongs in the kit.

Written up in `SOP/01_KIT_STRUCTURE.md` and step 12 of the generate-ad-kit skill.
See also [[feedback_run_every_gate]].

**The zip is built by `make_ship.py`, not by hand (4 Sep 2026).** `adkit/ship.py` refuses to
write unless the folder holds exactly the six items, deletes any stale zip first, and asserts
forward-slash separators. Both hand-zipping failures had already happened: PowerShell's
`Compress-Archive` writes backslash paths, which a Mac unpacks as ten flat files literally
named `ads'_transfer_pricing.png`; and a rebuilt folder once sat beside an older zip, so
the file being sent held the previous faces. One command per kit:

```
cd <kit>_MediaBuyer_<dates> && python make_ship.py
```


**Ruchika wants the kit's .py and .md files in the zip too (17 Sep 2026).** Asked on the US
Accounting 10-12 Oct wave: "add the py and md files to the zip too". They go in one
`source/` folder beside the six deploy items, same relative paths as the working kit, via
`zip_ship(OUT, allow=("source",))` in `adkit/ship.py`. The six items stay untouched so the
deploy contract does not change. Model: `USAccounting_Search_MediaBuyer_10-12Oct/make_ship.py`.
