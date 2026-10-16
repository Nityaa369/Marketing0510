# Google kit: Tech Law C1 (Display, Performance Max, Demand Gen)

Same 10 readers and the same camp as the Meta kit (8th Tech Law Bootcamp, Sat 24 and Sun 25 Oct 6 to 9 PM IST,
Mon 26 Oct 7 to 10 PM IST, Rs 10 incl. GST, refundable, live only). Draft for Ramanuj: no verdict on any ad,
reader, page or budget. Built with the team's `google-ads-banner-resize` SOP (in `tool/`).

## What is here
| Item | Where |
|---|---|
| 10 ads x 12 images (3 sizes x 4 colours) = 120 JPGs | `OUT/Tech_Law_C1_Google/<group>/<ad>/` |
| Sizes | landscape 1200x628, square 1200x1200, portrait 960x1200 (4:5) |
| Colours | C1 = the ad's own colour; C2 to C4 = hue rotated +90, +180, +270 (same contrast) |
| Text assets for every ad (headlines, long headline, descriptions, URL) | `GOOGLE_COPY_C1.csv` (lengths checked) |
| Contact sheets, 12 (one per size and colour) | `OUT/qa_sheets/` |
| Source copy used to render | `job/content.json` |
| Renderer, policy scan, QA (the SOP) | `tool/` |

Groups: `01_Outside_Law_LLB_Holders` (01 HR, 02 Banking, 03 Content, 04 Sales and ops, 08 BPO),
`02_Career_Break_And_Moved_Lawyers` (05, 06, 09, 10), `03_Lawyers_Abroad` (07).

## Why the Google ads look different from the Meta ads
Google disapproved 7 earlier ads from this account (see `tool/references/disapproval_casebook.md`). So the Meta
designs are not reused. Each Google ad is rebuilt from text, to the SOP:
- **No arrow or button shape.** "Join for Rs 10 ->" becomes plain text on the bottom band: "Register for ₹10".
- **Full frame, native size.** Tinted dotted background, full-width band, nothing left white. Never a scaled Meta image.
- **Audience box first, headline names the move**, one-sentence field definition on the face, bold explanation.
- **Neutral audience wording.** Meta wording that states a personal situation was changed:
  "paused practice for family" -> "Lawyers back from a practice break"; "moved cities after marriage" ->
  "Lawyers who moved to a new city"; "women lawyers returning after a family break" -> "Lawyers returning after a
  career break"; "left a law firm for family" -> "Lawyers who left a law firm". Reason: personalised-ads policy.
- **Ad 07 (abroad)** carries "A legal education programme for lawyers, not an immigration, visa or document service."
- **Removed from the face:** "in-house", "at your own pace" chips as promises, "legal brain", "potential", all
  money words, "Zoom/WhatsApp/LinkedIn", capital letters, em and en dashes, learner results.
- **Kept:** the dates, timings and "₹10 incl. GST, refundable" and "Live only, no recordings" on every ad.

## Checks run
- `policy_scan.py` on the image copy: 0 BLOCK. On the text sheet: 1 BLOCK, a false positive on the
  required line "not an immigration or visa service" (ad 07). Keep it.
- `qa_pack.py`: ALL CHECKS PASSED (120 files, correct sizes). Text scale stayed above 0.70 on every ad.
- I looked at the square and landscape contact sheets. Look at all 12 before upload.
- All headlines 30 characters or fewer, long headlines and descriptions 90 or fewer.

## How to set up in Google Ads
1. One Performance Max or Demand Gen campaign per group above (3 campaigns), conversion goal Purchase on the GrowthX pixel.
2. One asset group per ad: upload that ad's 12 images (landscape, square, portrait), add the 3 headlines, long
   headline, 2 descriptions, business name "LawSikho", call to action "Sign up" and the Final URL from the CSV.
3. Audience signals from `Audience`; use the reader's own words, no age or gender targeting.
4. Final URLs use `utm_source=google&utm_medium=cpc`. Create the GrowthX funnels `tlc1-01` to `tlc1-10` first.
5. Google Ads is not connected in this account (no API token), so cost per buyer must come from GrowthX paid seats.

## Critic's read (before Ramanuj)
- **Who:** passes. Targeting is lawyers and LLB holders only, so ads 01 to 04 and 08 (LLB holders working in HR, banking, content, sales and BPO) are not the non-lawyer readers Ramanuj struck on 24 Sep. One thing to confirm with him: that an LLB holder outside practice counts as a lawyer.
- **Prize:** every headline now names the move ("into tech law", "as a tech lawyer"), better than the Meta faces,
  which say "restart" or "routes".
- **Risks still on the landing pages (Google reviews them too):** "WhatsApp" (joining details) and "LinkedIn"
  (outreach plan) trademarks on all 10 pages; "lakh" in the market facts (startup and GCC counts, not money); and
  "in-house roles" on page 10. The pages are not rewritten for Google. Say if you want a Google version.
- **Gaps:** no Google CPP or CPL exists for this account, so there is no cost evidence for any of these ads. Do not judge
  on CTR or on a part-day. Needs Ramanuj: audience choice, routing, budget.

Half-asleep test: in 3 seconds the reader sees who it is for (the box), the job (the headline) and the reason to
say yes (3 live evenings for ₹10, refundable).
