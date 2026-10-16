---
name: feedback-contradiction-means-failed-test
description: "An impossibility inside your own result is a failed test, not an open question - re-test before publishing it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2387ada5-7a87-4eae-b265-1d2214562cdf
  modified: 2026-09-04T08:27:01.995Z
---

**When a finding contains an impossibility, the finding is wrong. Re-test before publishing.**

On 4 Sep 2026 I reported that 22 of 30 Independent Director landing pages could not take
money, behind 92% of the campaign's spend. In the same report I wrote that **220 of the
campaign's 239 buyers had come through those "dead" pages**, and filed it as "an open
question" and "not possible as it stands".

That was the test failing, announced in my own output, and I published around it. The
founder disproved the whole finding in one sentence: *"the buttons are working for me."*
The pages wire their CTA by **text match in a delegated script**, so `href="#"`, no
`onclick`, and no URL change on click are all normal — see
[[reference-growthx-funnel-checkout]].

**Why:** a contradiction is cheap information and it arrives *before* the mistake is
public. Re-testing would have cost minutes. Publishing instead cost a false blocker on a
live campaign, three artifacts that had to be retracted, and the founder's time.

**How to apply:**

- If a result requires something impossible to be true (buyers without a checkout, purchases
  without page views, spend without delivery), **stop and re-test the instrument.** Do not
  write the words "open question", "needs investigation", or "not possible as it stands"
  about your own conclusion and then ship it.
- Prefer testing the **mechanism the system actually uses** over the mechanism you assume.
  Read the runtime script before judging a button.
- Confirm a negative by **observing the positive path once**: click it and watch what
  appears, rather than listing the things that did not happen.
- Where a claim would trigger real work by someone else, hold it to the standard of
  something you would act on yourself.

Related: [[feedback-load-rate-is-not-traffic]] - the same day, the opposite error avoided,
because there the arithmetic was checked *before* acting.

**23 Sep 2026, the same failure inside one report.** The daily report's top finding said
four camps had "no live campaign" while its own Bootcamps board showed two of them
spending: `CorpFinance_bootcamp_17-19Oct_CBO` at Rs 276 a buyer and
`RID + ID BC 10-12 Oct 2026_CBO_LEAD` at Rs 63 a lead. Two separate causes, both in
`daily_report.py`: the camps-ahead table re-ran `match_camp` over every live campaign
while the finding used a de-duplicated pass, so the table and the finding disagreed; and
the matcher needed two shared words, which an abbreviating name (`CorpFinance`, `RID + ID`)
never has. Fixed by one shared assignment (`c["campaign"]`) read by both, and by lowering
the bar to one shared word when the campaign name carries the camp's own dates. Six dark
camps became four. **Before reporting a campaign dark, look for it in the report's own
spending tables.**
