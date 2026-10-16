# Design styles that have gone live

**Generated — run `python -m adkit.styles --write`.** The taxonomy is read off the
work: the device names the kit generators write in their own docstrings, the six
approved hook types in `AD_CREATION_DIRECTOR.md` §4, and the formats explored in
`new ad types/`.

**Why this file exists:** so a wave has variety in it. Check a kit with
`python -m adkit.styles --kit <folder>` — it warns when most of the faces are the
same shape, which is the visual version of the landing-page problem in Rule 4b: a
reader who sees several ads from one campaign should not see one idea.

**How honest the index column is.** Only two styles have a measured cost index. The
Meta pull names ads the way the media buyer named them, and most faces cannot be
matched to a row — `CPL_WINNERS_31Aug2026.md` carries the same caveat. `-` means
nobody has spent enough on that style to have an opinion about it. It does not mean
the style is bad, and it must not be quoted as if it did.

**Coverage, stated plainly:** most faces in this repo cannot be classified from
their filename or their markup, so the **Faces** column counts only the ones that
carry a device signal. It is not a census, and the totals should not be quoted as
one. The value of this file is the catalogue and the named examples.

| Style | Faces | Index | Live cost where known |
|---|---|---|---|
| pay chart | 2 | 2.34 | — |
| toon / cartoon | 9 | 1.22 | — |
| chat / messaging | 4 | 1.22 | — |
| notice / letter | 19 | — | ₹30/lead |
| quote card | 10 | — | — |
| comparison table | 2 | — | — |
| chart / quadrant | 17 | — | — |
| duty / rota / checklist | 30 | — | — |
| receipt / invoice / form | 2 | — | — |
| calendar / timeline | 1 | — | — |
| ladder / progression | 2 | — | — |
| collage / sticker | 20 | — | — |
| photo-led | 54 | — | ₹41/lead |
| carousel | 4 | — | — |
| object + paper slip | 3 | — | — |
| pixel art | 2 | — | — |

## What each style is, and when it earns its place

### pay chart — 2 faces, 2 kits

A salary figure as the hero. MEASURED WORST IN THE ACCOUNT, index 2.34 against a par of 1.00, replicated across three product lines. Also banned from the face on compliance grounds. Do not build one.

- `paychart_independent_director_12_14Sep2026/paychart_independent_director_12_14Sep2026/ads/pc_independent_director.png`
- `paychart_us_accounting_12_14Sep2026/paychart_us_accounting_12_14Sep2026/ads/pc_us_accounting.png`

### toon / cartoon — 9 faces, 3 kits

Drawn characters, usually two, with a caption. Format index 1.22. The account's highest-CTR ad is one of these and it costs more than its campaign median - the clearest case that CTR does not defend an ad.

- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/08_free_evenings.png`
- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/10_career_break.png`
- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/11_designation_stuck.png`

### chat / messaging — 4 faces, 2 kits

A messaging thread as the artefact. Indexes with toon at 1.22. Reads fast, converts unremarkably.

- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/07_degree_unused.png`
- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/12_edtech_experts.png`
- `WomenRemote_Wave4_SEND_THIS/ads/W6_whatsapp_level.png`

### notice / letter — 19 faces, 3 kits

An official-looking notice. The shape behind us22_notice_fifties (Rs 29.65) and us25/us24 - three of the four cheapest lead ads in the account.

- `APPROVED/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/ads/us20_notice.png`
- `APPROVED/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/ads/us21_notice_bcom.png`
- `APPROVED/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/ads/us22_notice_fifties.png`

### quote card — 10 faces, 6 kits

The reader's own sentence, set large. Hook type 2 and 5. mh01_corridor is the GOLDEN reference.

- `AcademicWriting_Wave1_MediaBuyer_26-28Sep/ads/02_guest_lecturers.png`
- `AcademicWriting_Wave1_MediaBuyer_26-28Sep/ads/05_net_aspirants.png`
- `AcademicWriting_Wave1_SEND_THIS/ads/02_guest_lecturers.png`

### comparison table — 2 faces, 2 kits

Two columns the reader can put herself in. Hook type 3.

- `ContentWriting_SectionA_29-31Aug/ads/23_per_word_both_ways.png`
- `new ad types/remaining6_contentwriting_29-31Aug/ads/40_per_word_both_ways.png`

### venn / overlap - 19 faces, 1 kit

Two outlined circles: the work the reader already does in one, the work the camp adds in the
other, and the offer sitting in the intersection. Built 18 Sep 2026 from a DTC supplement static
("1 CHEW THAT DOES BOTH"). Layout `venn` in `adkit/layouts_custom.py`.

**Only honest when the two sides really are separate today.** A Venn whose circles are a skill and
a restatement of that skill says nothing, and the reader can see it.

**No live cost yet.** The whole of `CorporateFinance_Venn_MediaBuyer_17-19Oct` is on this shape,
so it will be measurable against that campaign's par of Rs 193.94 per purchase, and nowhere else.

- `CorporateFinance_Venn_MediaBuyer_17-19Oct/ads/01_loan_consultant.png`
- `CorporateFinance_Venn_MediaBuyer_17-19Oct/ads/04_company_secretary.png`

### notification card - 19 faces, 1 kit

One white notification card centred on a flat brand ground, with a second and third card peeking
behind it the way a stack reads on a lock screen. Built 21 Sep 2026 from a DTC sunscreen static.
Layout `notify` in `adkit/layouts_custom.py`.

**The refresh is the notification; the content is the one that beat par.** Two devices were built
and rejected first: `venn`, whose intersection was a category error, and `alert`, which carried
the look and almost none of the information. What ships carries the full first fold inside the
card: the app row, the ICP as a question, the qualifier row as chips, the offer in plain words,
the one-sentence definition, the take-aways as an attachment card, the meta line, and ONE
full-width filled action. That skeleton is the one `cf_loan_consultant` (Rs 164) and `cf_cma`
(Rs 170) ran on against a Rs 193.94 par.

**Two rules the skim tests produced, and both are enforced in the kit's build.py.** The offer line
names the work and never defines it by contrast with the reader's current job. And no face may
read as a downgrade: the offer is the same client seen at a higher level, an engagement rather
than a task, never piecework and never starting again.

**One action only.** A second cell ("What's in it") was removed because it competes for the click
with the thing that takes the money.

**Meta compliance.** Creative must not imitate platform or system UI in a misleading way: no
status bar, no platform glyphs, no fake close control, brand colours throughout, and the only
control-looking element is the real CTA.

**No live cost yet.** The whole of `CorporateFinance_Notify_MediaBuyer_17-19Oct` is on this shape,
so it is measurable against that campaign's par and nowhere else.

- `CorporateFinance_Notify_MediaBuyer_17-19Oct/ads/01_loan_consultant.png`
- `CorporateFinance_Notify_MediaBuyer_17-19Oct/ads/12_newly_qualified_ca.png`

### chart / quadrant — 17 faces, 7 kits

A simple plot with her current and target bucket both visible. Hook type 6. Numeric axis ticks MUST cite a source on the face.

- `APPROVED/ID_FreeBootcamp_FULL_MediaBuyer_12-14Sep/id_full_sep12/ads/v5_career_curves.png`
- `APPROVED/SQE_DutyChart_Kit_Sep2026/SQE_DutyChart_Kit_Sep2026/ads/sqd_dutychart.png`
- `ContentWriting_SectionA_29-31Aug/ads/16_will_you.png`

### duty / rota / checklist — 30 faces, 10 kits

A list of the actual work, as an artefact. SQE_DutyChart is the reference.

- `AcademicWriting_Wave1_MediaBuyer_26-28Sep/ads/03_school_teachers.png`
- `AcademicWriting_Wave1_SEND_THIS/ads/03_school_teachers.png`
- `ad_brief_tool/data/build_artifacts/ContentWriting_RMBC_29-31Aug/v1_rejected/ads/rm_02_proofreader-editor.png`

### receipt / invoice / form — 2 faces, 2 kits

A financial artefact. Carries money without putting a figure in the headline.

- `GlobalPatent_MediaBuyer_19-21Sep/ads/04_bioinformatics.png`
- `GlobalPatent_Wave1_SEND_THIS/ads/04_bioinformatics.png`

### calendar / timeline — 1 faces, 1 kits

Time as the device. CAUTION: calendar and exam-window motifs are the device-led archetype D, which indexes 1.22 and is the most expensive archetype measured. Name the reader, never the date.

- `Patent_Wave2_MediaBuyer_7Aug/ads/w2_03_deadline_calendar.png`

### ladder / progression — 2 faces, 1 kits

Where the work leads, in stages. hoc_02_ladder is the GOLDEN reference.

- `APPROVED/SQE_DutyChart_Kit_Sep2026/SQE_DutyChart_Kit_Sep2026/ads/sqd_routes.png`
- `APPROVED/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/US_Accounting_MissedICP_Notice_MediaBuyer_12-14Sep/ads/us16_ea_route.png`

### collage / sticker — 20 faces, 1 kits

Assembled fragments. Built for Content Writing wave 6.

- `new ad types/formats_v1_aug18/ads/01_poll_arbitration.png`
- `new ad types/formats_v1_aug18/ads/02_notes_sqe.png`
- `new ad types/formats_v1_aug18/ads/03_card_arbitration.png`

### photo-led — 54 faces, 9 kits

A real photograph as the hero. Most approved ads in this account carry NO photograph - the director says default to a device instead.

- `APPROVED/LawSikho-Arbitration-MassHysteria-22Aug2026/ads/mh01_corridor.png`
- `APPROVED/LawSikho-Arbitration-MassHysteria-22Aug2026/ads/mh02_office.png`
- `APPROVED/LawSikho-Arbitration-MassHysteria-22Aug2026/ads/mh03_chamber.png`

### carousel — 4 faces, 2 kits

Multi-frame. Counted as one cell.

- `ContentWriting_SectionA_29-31Aug/ads/cw_22_carousel/cw_22_swipe_reveal_01.png`
- `ContentWriting_SectionA_29-31Aug/ads/cw_22_carousel/cw_22_swipe_reveal_02.png`
- `new ad types/swipe_reveal_contentwriting_29-31Aug/ads/cw_22_swipe_reveal_01.png`

### object + paper slip — 3 faces, 2 kits

A drawn object holding a paper slip that carries the promise, under a sans-plus-script headline. Reference set 1 Sep 2026, sheet 2. No live cost yet.

- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/06_retired_faculty.png`
- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/15_commerce_law.png`
- `new ad types/wave6_contentwriting_29-31Aug/ads/cw_48_final-year-student.png`

### pixel art — 2 faces, 1 kits

A pixel-grid device on a flat bright ground. Reference set 1 Sep 2026, sheet 5. No live cost yet.

- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/09_small_city.png`
- `AcademicWriting_Wave2_MediaBuyer_26-28Sep/ads/14_engineering.png`

## The two rules this file exists to serve

1. **Vary the device across a wave.** `python -m adkit.styles --kit <folder>` warns
   when 60% or more of a kit's faces are one style.
2. **Never build a pay chart**, and treat calendar/exam-window motifs as the
   device-led archetype D — 1.22 against par, the most expensive archetype measured.
   If you cannot name who the ad is for before you pick the device, you are building
   a D.
