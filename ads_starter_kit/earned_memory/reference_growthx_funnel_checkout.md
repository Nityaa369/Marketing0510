---
name: reference-growthx-funnel-checkout
description: "How GrowthX funnel pages wire their pay button - by CTA text via bridge.js, not by href - and how to actually test one"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2387ada5-7a87-4eae-b265-1d2214562cdf
  modified: 2026-09-04T08:26:49.933Z
---

Funnel pages at `growthx.skillarbitra.ge/f/<slug>` (the "Funnel Deployer" platform) **do not
wire the pay button the way an ordinary page does.** Testing them as if they did produces a
false "dead checkout" every time. This cost a wrong blocker on 4 Sep 2026.

**How it actually works:**

1. Each page carries `window.__FUNNEL_DEPLOYER__` with `slug`, `price`, and a **`ctaLabels`**
   array, e.g. `["Start the 30 days — ₹100", "Join · ₹100"]`.
2. `/runtime/bridge.js` attaches a **delegated** click listener and matches a clicked
   `<a>` or `<button>` by its **normalised text content** against `ctaLabels`.
3. On a match it builds an in-page bottom sheet (`#fd-modal`) holding an iframe at
   **`/modal/<slug>`** — the real two-step checkout: name, WhatsApp, email, then payment.

**Therefore, on these pages:**

- `href="#"` on a CTA is **normal**, not a fault.
- There is **no `onclick`** on the element and **no gateway URL** in the page source.
- Clicking changes **neither the URL, nor the tab, nor the console**. Checking those three
  and concluding "nothing happened" is the trap.
- `PAYMENT_LINK_PENDING` and `TODO(dev)` strings appear in leftover inline handlers on some
  pages. The bridge overrides them; they are dead code, not a live stub.

**The correct test, cheap and bulk-runnable.** From the growthx origin, same-origin `fetch`
each `/f/<slug>`, parse `ctaLabels` out of `__FUNNEL_DEPLOYER__`, collect every `<a>`/`<button>`
text, normalise both (trim, collapse whitespace, lowercase, decode `&middot;` and `&#8377;`)
and check at least one CTA matches a label. Confirm once by hand: click, then assert
`#fd-modal` exists and `#fd-iframe` src is `/modal/<slug>`.

**One real failure mode worth checking**, documented in bridge.js's own comments: a CTA whose
label is *not* in `ctaLabels` (often a sticky mobile "Join →") falls through to a stale
`community.skillarbitra.ge/sp/…` URL. Only slugs in the hard-coded `COMMUNITY_INTERCEPT_SLUGS`
allow-list catch those. Scan for anchors pointing at `community.skillarbitra.ge` whose text is
not in `ctaLabels`. All 30 Independent Director pages were clean on 4 Sep 2026.

Related: [[feedback-contradiction-means-failed-test]], [[feedback-load-rate-is-not-traffic]].

**Served HTML is not upload source (28 Sep 2026).** A page fetched from `/f/<slug>` carries
blocks GrowthX injects at serve time: the `__FUNNEL_DEPLOYER__` + `__FUNNEL_PIXELS__` script,
`/runtime/bridge.js`, the Meta pixel, a legal footer (`padding:40px 24px 32px;text-align:center;
border-top:1px solid #ddd`) and Cloudflare's email-decode script. Strip them before reusing a live
page as a donor or re-uploading it, or the pixel double-fires. `LP_Swaps_28Sep/_reference/prepare.py`
does this. Sticky buttons whose text is not in `ctaLabels` (e.g. Legal AI's "Join · ₹100") only
worked through an inline `onclick` to `/modal/`; a rebuilt page must use the exact label.
