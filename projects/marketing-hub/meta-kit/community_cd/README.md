# Contract Drafting Community: "Learning the Art of Contract Drafting" (20 Meta ads, 1080x1350)

Format: divyanshu's torn-paper reference (torn hole with a photo, title on torn strips with a
highlighter, handwritten margin notes). Copy: the 20 ICPs in
`docs/COMMUNITY_HOOKS_CD_LEGALAI_20each_2026-10-19.md`. Each ad has its own palette, named by
colour-theory scheme in `ads.py`, plus its own title font, handwriting font, tilt and hole shape.

Pipeline
1. `GRID_PROMPT.txt` makes ONE 4k image holding all 20 hero photos (Higgsfield gpt_image_2_5,
   4:5, 4k, medium, 1.25 credits). Generated 19 Oct, job 06e4713a-8890-45f1-8071-63ab90491eb8.
2. Save it as `grid_20.png`, then `python3 crop_grid.py grid_20.png` writes photos/cd_01..20.jpg.
3. `python3 build.py` renders out/cd_art_01..20.png (Chromium via node playwright).
Missing photos render as a labelled "PHOTO NN PENDING" placeholder.

## Set 2: "20 beginnings" cards (divyanshu's version 2 layout, fixed), 19 Oct
- Netflix removed. Biggest line names the move into contract drafting (`cards.py` HEADS); no puns
  or fragments. Readers are the approved 20; body is the approved hook. Button "Join for ₹200 →"
  at 50px (full exchange, never "Join now"). No dates.
- Characters: ONE Higgsfield grid, job 34e3f98c-d826-49ba-a855-78f38f3e8c1c (gpt_image_2_5, 4k,
  1.25 credits), 20 distinct Indian people, full heads, buns and arms inside each cell. The first
  grid (c3f51b3f...) cropped buns and arms and was replaced.
- Build: save the grid as `ill_grid2.png`, `python3 crop_grid.py ill_grid2.png ill png`,
  `python3 -c "..."` to write cards.json from cards.py, then `python3 card_build.py cards.json out`
  (PW env = path to node playwright). Text is set by us in HTML, so nothing is garbled.
- The 20 PNGs were rendered and checked in the Higgsfield sandbox on 19 Oct; this environment
  cannot download from d8j0ntlcm91z4.cloudfront.net, so the PNGs are not in the repo yet.
