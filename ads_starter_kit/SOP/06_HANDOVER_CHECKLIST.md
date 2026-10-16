# 06 · Handover checklist

## Run the mechanical check

```bash
python preflight.py <folder-or-files>
```

A BLOCKER means the work is not finished. Fix and re-run. Do not hand over work that fails,
and do not describe work as ready if you have not run it. Preflight catches mechanical
failures only — it cannot judge Rules 1 and 2.

Preflight's ad-to-landing-page pairing check counts `.png`/`.jpg`/`.jpeg` in `ads/`, so it
does not fire while the ads are still HTML. Re-run it after the PNG render.

## State these four lines in the reply

1. `preflight.py` run and result.
2. **The better job each ad offers** (Rule 1). One line per ad. If the answer is "the same
   job, done more carefully" or "the same job, plus a new obligation", it is not ready.
3. **The sentence in each ad that defines the field** (Rule 2, step 4), quoted.
4. **Confirmation you opened each landing page** and the pay button carries a real URL.

If you cannot fill one in, the work is not ready to send.

## The recurring blockers

These have blocked nearly every wave. Check them by name.

1. **Payment link.** Real funnel URL wired, funnel confirmed to exist, test-bought in a real
   browser. Not curl.
2. **Ads rendered to PNG.** `python gen_kit.py` (or the kit's equivalent) run, not left as
   HTML drafts.
3. **Every page opened.** Not a spot check of two out of ten.
4. **Analytics.** Confirm the deploy pipeline injects gtag/fbq; the pages carry none.
5. **Founder block sign-off.** The first-person quote and a photograph. Open since wave 1.
6. **Named proof from past cohorts.** Section 9 resting on the eleven-cohort line alone is
   the single biggest available lift on these pages.
7. **Learner names.** Confirm published learner records can be presented as learners of
   *this* programme — the source records say "our course", not the specific bootcamp.
8. **Account routing** confirmed with Ramanuj where a kit doubles the creative count or the
   ICP mix for one batch.
9. **Rights** cleared on any borrowed meme, song line or film reference.

## Never hand over ads without their landing pages

Asked twice in one week: *"But where are the landing pages?"* An ad with no LP is not
finished work. A kit of finished ad faces with no funnel slugs is not a shippable pack —
say so plainly rather than shipping more pages with a dead stub.
