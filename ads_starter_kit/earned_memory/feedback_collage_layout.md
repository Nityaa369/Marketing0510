---
name: collage-layout
description: "The collage-reveal face (CF wave 3, 29-30 Sep 2026) — approved design, 1080x1350, reader call-out + \"Do X work, not just Y\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2ef98ee6-3d94-4d45-8baf-088e7a5f2d29
  modified: 2026-09-30T07:40:41.813Z
---

The collage-reveal face was approved by the user on 29 Sep 2026 ("I like the ad visuals, go ahead with this for all ICPs"). It came from a Growth School reel ad. The face has:
- a halftone hand lifting a cloche off a plate of what the camp gives, with no text in the art
- one saturated colour field per ad
- a call-out pill naming the reader as a question
- a giant condensed two-tone headline, "Do corporate finance work, not just [their current work]."
- one delivery line, a full-width button, and the times

**Why:** the user wanted direct, simple hooks that pass the 20% brain test, with no riddles. They declined a Reels cut ("I want our ad dimensions").

**How to apply:**
- Build from `CorporateFinance_Wave3_MediaBuyer_17-19Oct/build.py`. The headline auto-fits from 96px; `text-wrap:balance` on the call-out.
- Pages come from `build_lps.py` there. The first screen of each page is the same colour field, collage and headline.
- On the first blind read, all 7 faces scored 3/3 and were read as a step UP. Readers repeatedly flagged "your first client" as unspecified; consider "first corporate finance client".
- Wave 4 (37-40, new readers, 30 Sep) fixed "first client" on the face: "...leave with a 6-month plan to raise it for your first client". Blind readers then answered Q3 concretely.
- The user rejected "no bank job needed" as "not a strong enough hook". The replacement "Raise money for businesses, like an investment banker." names the work and the career.
- A call-out must carry a job title. "In loan sales at a fintech" tripped simplicity S6 and judge C23; "Loan sales executive at..." passed.
- preflight's stub check now skips data: URIs. Base64 art had matched "TODO" case-insensitively.

Related: [[feedback_half_asleep_callouts]], [[project_corporate_finance_live_cost]].
