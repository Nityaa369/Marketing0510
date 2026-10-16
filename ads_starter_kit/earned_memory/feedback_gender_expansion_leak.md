---
name: feedback-gender-expansion-leak
description: Women AI 3-5 Oct reached 25% men despite genders=[2]; cause unknown; the individual_setting theory was wrong (UI shows a strict Women limit)
metadata:
  type: feedback
---

Women AI 3-5 Oct (WomenAI_FREE_3-5Oct-2026_BC_CBO_v1) sent 22.5% of 7-day spend (Rs 42,606) and
1,008 registrations to men although every ad set had genders=[2] and advantage_audience=0. The
cause was `targeting.targeting_automation.individual_setting = {gender: 1, age: 1}` on 10 of 11
ad sets, which makes gender and age suggestions. The 21 Sep report guessed retargeting sets; wrong.

**Why:** the Advantage+ audience flag alone does not prove the audience is locked.
**How to apply:** on any gender- or age-restricted camp, read `individual_setting` as well as
`advantage_audience`, and confirm with a gender breakdown of spend. See [[project-growthx-extract-refresh]].

**Rechecked 22 Sep, same day: the cause is not proven.** Meta's delivery_estimate returns the
same 113-133M women with individual_setting on or off, and a Community_Women_AI ad set with
gender:1 (advantage_audience 1) runs 3.4% male. What IS proven: 10 ad sets with byte-identical
targeting ran 2% to 60% male, stable daily, no edits - a binding gender limit cannot do that.
Test that settles it: turn the switch off and check next-day male share. Lesson: a setting that
correlates with a leak is a hypothesis; check it against a control ad set before calling it the cause.

**Later on 22 Sep: the switch theory is dead.** The user's Ads Manager screenshot of BroadWFH_B shows
Advantage+ off, Gender: Women, Age 25-65+, and no relaxation control at all. So
`individual_setting {age:1, gender:1}` in the API is not a visible or actionable setting. Not WhatsApp
either (male share vs WhatsApp spend share across ad sets: r = -0.47). Meta refuses a gender x
publisher_platform breakdown. Next test proposed: read registrant names from the male-heavy funnels.
Do not recommend flipping a setting from an API field without first seeing it in the Ads Manager UI.
