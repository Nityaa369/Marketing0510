---
name: feedback-search-layout
description: "The `search` layout - \"the search:\" query bar then \"the solution:\" offer card, built from a DTC skincare inspo on 17 Sep 2026; ICP band added above, packshot replaced by the offer card"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4d1fca80-c9d7-436b-8c41-3000397bc5e2
  modified: 2026-09-17T11:08:21.589Z
---

`search` (adkit/layouts_custom.py, 17 Sep 2026) was built from an inspo static Ruchika
supplied in chat: a skincare ad with "the search:" over a search-bar query ("how to stop
dry flaky skin") and "the solution:" over the product packshot. First use:
`USAccounting_Search_MediaBuyer_10-12Oct/01_search_fifties`, the approved us22 "accountant
in your 50s" copy with the query "accounting jobs after 50".

**Two deliberate changes from the reference.** The reference names no reader, so the ICP
band sits above both labels ([[feedback_icp_named_first]]). The packshot becomes an offer
card (accent top strip with the camp and dates, `.head` at the 64px floor, delivery
sentence), because the product is a live camp and the approved corpus is artefact-led,
not photo-led ([[feedback_house_ad_formula]]).

**Why:** a new format needs the chassis contract to be seen by C8 and fit, and the blind
read to prove it is not cryptic. First render passed every face gate and blind-read 3/3,
level with the us22 and us04 controls (us05 control 2/3).

**How to apply:** supply `extra` keys `query`, `offer_top`, `deliver`, `foot_left`;
`q_label`/`a_label` default to "the search:"/"the solution:". The query must be the
reader's own plain words, and a positive question - never a fear search (Rule 1).
**The query carries the problem, never the ICP again.** First query "accounting jobs after
50" repeated the call-out ("Accountant in your 50s?"); Ruchika caught it 17 Sep. In the
inspo the search is the problem ("how to stop dry flaky skin") and the product answers it,
so the query should be the question the head answers: "what to do with 25 years in
accounting" -> "Take your experience to US firms, who are short of it." A long
call-out wraps: the band uses `text-wrap: balance` so it breaks evenly instead of
orphaning the last word. Nothing in it has a live cost yet.

**Name a tool in the delivery line.** Rolled out to 8 US Accounting readers the same day.
02 evenings and 07 small town blind-read 2/3 with "the skills, the toolstack"; changing the
line to "US bookkeeping in QuickBooks and Xero" took both to 3/3, and the readers quoted the
tools back as what they could do on the last day. Faces whose line names nothing concrete
("the top 20 skills", "the licence route") are the ones that wobble on question 3.
Confirmed at 21 faces the same day: every face naming QuickBooks/Xero read 3/3; the only
2/3 was 06 CA Inter, whose line still says "the top 20 skills". **Weaker than it looked:** on
the re-read 06 named the tools and still went 2/3, and 05 ("top 20 skills") dropped 3/3->2/3.
One reader per face swings a point either way; the us05 control does the same.

**Half-asleep skim test (Ruchika, 17 Sep: "at 30% brain capacity").** `.skim/skim_test.py` in
the kit shows only call-out, search, head, tag and button. The headline must name the work:
"Take your experience to US firms, who are short of it" and "Your CA-firm experience pays in
dollars" left skimmers unable to say the job; "Keep the books for US firms, with 25 years
behind you" and "Do the same audit and accounts work for US firms" went 3/3. Clever turns
("not the tag", "US office hours", "the close") stalled readers. Final wording skimmed 45/45;
the three priced controls, cut to their own skim unit, scored 1-2/3 and never showed "free",
which is why the offer tag is now 36px and the button says "Join the free bootcamp".
