---
name: judging-static-ads
description: Use when someone uploads or pastes a static ad image (or points at ad HTML) for review — "will this pass", "feedback", "accept or reject", or just an image with no text. Produces a verdict, brief problems with fixes, and an offer to fix.
---

# Judging Static Ads

When a static ad arrives (image in chat, or a path to ad HTML), run this protocol. The
deliverable is a VERDICT + brief ranked problems + an offer to fix. Keep the whole reply
short — verdict line, numbered problems (one line each with its fix), one optional
what's-working line, the offer. Depth only if asked.

Paths below are relative to this skill folder.

## Protocol

1. **Find the source.** Grep the ads/creative folders for distinctive strings from the image
   (kicker text, headline fragment). Check kit folders and `~/Downloads`. Getting the HTML
   matters: without it, Gate 0 (all CSS/copy rules) cannot run.
2. **Run Gate 0 when source exists:** `python3 engine/creative_judge.py <file_or_kit_dir>` —
   it wraps ad_lint (C1–C27), render QA, crop QA, check_claims, and logs the verdict.
   **When image-only: the verdict must say "vision-only — Gate 0 never ran".** Never present
   an image-only pass as a full pass (a 44px kicker sailed through once this way).
   - Gate 0 needs **Pillow** for the pixel checks. It finds the rendered PNG beside the HTML,
     or in a sibling `ads/`, `previews/`, `renders/`, `png/` or `out/` (one level of
     subfolder deep, which covers `ads/<name>_carousel/`), or by matching the descriptive
     tail when the render was renumbered (`html/cw_29_eye_test.html` → `ads/11_eye_test.png`),
     but only when exactly one candidate matches.
     **FIXED 24 Aug 2026 — read this if you have old verdicts on file.** `png_for()` used to
     look *only* beside the HTML. Every kit in this repo keeps sources in `html/` and renders
     in a sibling `ads/`, so it returned `None` for all of them and **the entire pixel gate
     silently skipped on every creative ever judged.** `ad_render_qa` (E1–E4) and `crop_qa`
     (X1) had never run. Re-running Section A after the fix produced 79 findings that had
     never been reported: 46 E2, 23 X1, 8 E1, 1 E3, 1 E0. Any verdict logged before this date
     is copy-only — treat its silence on clipping and crop as unknown, not as a pass.
   - If a checker cannot run you now get `[WARN E9] … the check was NOT performed`. That is
     not a pass. Install Pillow and run again.
3. **Vision pass** — the rulebooks are `reference/gate-rules.md` (V1–V20 + the teardowns) and
   `reference/house-rules.md` (the standing rules Gate 0 cannot see). The checks that have
   caught real rejects:
   - Identity call-out: PERSON in a situation, large, high-contrast block, crop-safe. A bare
     situation ("BACK AFTER A BREAK?"), a canvas-coloured chip, or small-type-above-huge-type
     is a blind spot.
   - Biggest line names the PRIZE the TG wants, never the product ("this bootcamp teaches…"),
     and names the aspiration explicitly — what the reader BECOMES.
   - Problem step present (the spine step that goes missing).
   - Value list mined from THIS camp's delivery script, matched to the ICP's goal type:
     job-seekers get the route to the job; practice/in-role ICPs get artifacts.
   - Nothing that must be read below the CTA or outside the 1:1 crop (y 135–1215). Redundant
     recap ink (dates, price, refund) below the line is a blessed pattern, not a defect.
   - CTA states the full exchange ("₹10 gets you all 3 days"), never bare "reserve my seat".
   - Barrier lines ("no degree/experience") legible and above the CTA — never fine print.
4. **Verify claims** against the evidence bank and product ground-truth files. Check that a
   number on the ad still means what its source says: a figure can be sourced and still be
   misused (11,000 D2C brands *selling online* is not 11,000 brands *that pay for campaign
   strategy*). An unverifiable stat = hold, not reject.
5. **Check the standing rules** in `reference/house-rules.md` — brand by product line,
   vocabulary gates, banned topics and audiences, the ad formula, the four campaign pieces.

## Verdict

First line, always one of:
- **ACCEPT** — clean; state any WARNs as deliberate decisions.
- **ACCEPT WITH CHANGES** — fixable defects; list them ranked, fix in one line each.
- **REJECT — rethink** — 2+ substantive defects or any hard ban (banned proof names,
  negative-qualification block, HR topic call-out, freelancer targeting, distress framing).

Append "(vision-only — Gate 0 never ran)" when judging from an image without source.

Rules postdating an approved creative are noted, not retro-enforced — check the file's build
date before enforcing a recent rule. A clean gate pass is "no known defect", never "good ad";
the teardown questions decide.

## Then offer to fix

Always end with the offer:
- Source found → offer to edit the HTML, re-render (headless Chrome, or the kit build script),
  re-run the judge, and show before/after. Show the **1:1 centre crop** side by side when the
  fix was a crop-safety fix — that is the proof that reads instantly.
- Image-only → ask for the kit/file, or offer to rebuild the ad on the kit chassis with the
  fixes applied.
- Template-level defects (same issue across sibling cells) → offer to fix the template and
  regenerate all cells, not one.

Work on a `_v2` copy rather than overwriting an approved original, unless told otherwise.

## Before a kit ships

`python3 engine/package_check.py <kit_dir>` is the ship gate. It refuses to zip a kit whose
creatives were REJECTed, whose anchor text or landing pages are missing, or whose verdicts are
stale — a verdict older than the PNG it names authorises nothing, because the creative changed
after it was judged. Overrides exist (`--accept-defects C21 --reason "…"`) and are always
logged; the point is attribution, not impossibility.

## Feedback loop

When the owner's verdict disagrees with the judge's, that is rulebook input, not a one-off:
score the miss, encode it (an ad_lint rule with a fire-rate test on approved vs unshipped
kits, or a V-rule in `reference/gate-rules.md`). Every new mechanical rule MUST pass the
backtest discipline before it can block: **never reject what was approved and shipped, never
reject ads that beat their campaign median.** A change that only ever *lowers* a rule's fire
rate is safe by construction.
