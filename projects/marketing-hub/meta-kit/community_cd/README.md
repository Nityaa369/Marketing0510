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
