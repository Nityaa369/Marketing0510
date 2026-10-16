---
name: feedback-report-scripts-narrow-silently
description: A reporting script that filters accounts or assumes one currency shrinks the numbers with no error - check the filter before trusting a total
metadata:
  type: feedback
---

**Found 9 Sep 2026** while making `pull_ads.py` the default reporting path. Two faults
had been sitting in it since it was written, both invisible:

- `accounts()` returned only `account_status == 1`, so **UNSETTLED and DISABLED
  accounts were dropped from every report with no mention**. A disabled account can
  still hold spend inside the reporting window.
- Every figure was multiplied by 1.18 for GST and printed behind a rupee sign,
  **including the two USD accounts and the GBP one**. Dollars would have been grossed
  up as rupees and folded into an INR total.

Both were harmless only by luck: those accounts were all at zero spend the day it was
checked. Neither would ever have raised an error - the total would just have been wrong.

Now: GST applies to INR alone, each account prints its own currency, a keyword pull
spanning two currencies warns instead of summing, and `--list` ends with a coverage
line naming every account read.

**Why:** this is the same failure as reporting "no ads are running" while three
accounts are unreadable - the number looks complete because nothing objected. A filter
in a reporting script is a silent claim about scope.

**How to apply:** before trusting any aggregate from a script in this repo, read the
line that selects what goes into it. Ask what it excludes and whether the exclusion is
stated in the output. See [[feedback-ads-reports-route-through-token]] and
[[project-meta-data-pull-path]].
