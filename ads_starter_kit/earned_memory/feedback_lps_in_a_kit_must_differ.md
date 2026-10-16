---
name: feedback-lps-in-a-kit-must-differ
description: Landing pages within one kit must carry different arguments, not the same page with a new headline - a reader sees several ads from one campaign and clicks more than one
metadata:
  type: feedback
---

Separate LP files is not enough. The pages must actually say different things.

**Why:** stated 31 Aug 2026 on the women bootcamp kit just shipped — *"they see different
ads, and then they click on it, but the lp is the same over and over again, making them
disinterested."* Measured as median pairwise sentence overlap: WomenRemote_Wave8 **84%**,
Wave6 90%, USParalegal 93%. Wave 8's ten pages carry an identical H2 sequence and change
only the H1. `WomenRemote_Wave9_LPs_SEND_THIS` is the model at **1%** — each page has its
own argument: a Saturday walkthrough, the case in numbers, three career-break stories, a
demand board.

**How to apply:** keep the spine (10 sections, 1,500–2,000 words, counted lists, sticky
CTA) and change the ARGUMENT inside it, per ad. This does not contradict "do not redesign
the spine": Corporate Finance sits at 74% overlap and converts 9.3–20.7%, so a shared
spine does not cost conversion on a single page. The defect is about the reader seeing
several, not about any one page. `preflight.py` blocks a kit above 80% overlap and warns
above 65%; it flags 14 kits in the repo today.

Related: [[feedback-checkers-refit-basis]], [[feedback-landing-page-standard]]
