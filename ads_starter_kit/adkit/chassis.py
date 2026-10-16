#!/usr/bin/env python3
"""The house ad-face chassis, once, instead of once per kit.

Why this exists. On 31 Aug 2026 this repo carried 20 per-kit generators totalling
9,890 lines, with no shared library anywhere:

    womens_ai_bootcamp/gen_formats.py          1,311 lines   926 CSS declarations
    ContentWriting_SectionA/gen_lps.py         1,702 lines
    IndependentDirector/gen_lps.py               774 lines
    IndependentDirector/gen_ads.py               390 lines   113 CSS declarations
    WomensRemoteWork_HiddenMarkets/gen_ads.py    327 lines   159 CSS declarations
    ContentWriting_SectionA/gen_ads.py           213 lines   143 CSS declarations

Every one of them re-derived the same 1080x1350 shell, the same Chrome screenshot
call, the same .callout/.head classes ad_lint C8 matches on, and the same
gutter/air constants. HiddenMarkets' own docstring says its chassis was "carried
over from womens_ai_bootcamp" -- by copy-paste, so it was re-emitted in full
anyway. That duplicated work is the largest single block of tokens in a kit build.

The geometry, type scale and colour roles here are lifted from
IndependentDirector_Wave1_MediaBuyer_12-14Sep/gen_ads.py, which shipped, and are
not re-tuned. What is new is three things that kill known defects:

  1. TIGHT IS MEASURED, NOT GUESSED. That generator carried a hand-written
     `tight=True` CSS override block per ad -- a human guessing a character
     budget. Here `scale` multiplies one size table, and Kit.render() finds the
     largest scale that actually fits by measuring the rendered box model
     (adkit.fit). SKILL.md, 26 Aug 2026: "a guessed budget cost two of the five
     cycles here."

  2. IT CANNOT SCALE BELOW THE IDENTITY FLOOR. .callout and .head are clamped
     at 64px whatever the scale, so only body elements absorb a tight fit. If a
     face still will not fit, it does not ship -- render() says so and names it.
     The fix is cutting words, which is the actual lesson: "Lengthening a
     definition sentence or a role name is never free."

     This is not theoretical. ad_lint C8 finds the FIRST
     `.callout{...font-size:Npx}` in the source with re.search, so a later
     override wins in the browser and is invisible to the linter.
     IndependentDirector_Wave1's `tight=True` block sets .callout to 58px and
     .head to 52px after the 66px/64px base rules -- both under C8's 64px hard
     floor, on faces that shipped reading as clean. Clamping here makes that
     class of override impossible to write.

  3. ONE PALETTE PER AD IS ENFORCED. Rule 4 (CLAUDE.md) required it and nothing
     checked it. Kit.render() refuses a kit where two faces share a palette.

A kit file is now data. Roughly ten lines per ad:

    from adkit import Kit

    kit = Kit(root=__file__,
              brand='Skill<i>Arbitrage</i>',
              eyebrow='Independent Director Bootcamp',
              takeaways=['IICA databank registration, done with you',
                         'A 50-question mock exam, with answers',
                         'Notes, templates and checklists',
                         'A 90-day plan to your first board seat'],
              cta='Save my seat &#8594;',
              terms='<b>Free &middot; 12 to 14 September &middot; on Zoom</b><br>'
                    '9 hours live &middot; Sat, Sun 2-5 PM &middot; Mon 7-10 PM',
              trust='NSE Emerge-listed &middot; NSDC &middot; IIT Roorkee iHUB')

    kit.face('01_company_secretaries', palette='clay',
             callout='A company secretary?',
             head='Boards need people who <em>know how a board works.</em>',
             card=('Sitting fee, per board meeting', '&#8377;25,000 to &#8377;1,00,000',
                   '10 to 18 meetings a year'),
             definition='Every listed and large public company must have independent '
                        'directors, who are outside members reviewing the accounts '
                        'and the big decisions.',
             proof='No prior board seat needed &middot; the exam is open-book')

    kit.render()        # all faces, auto-fit, fit report
    kit.render('01')    # just that one -- build ONE face first (SKILL.md)
"""
import pathlib
import subprocess
import sys

from . import fit, layouts, palettes

W, H = 1080, 1350
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
GUTTER = 60

# The scale ladder render() walks, largest first. 1.00 is the shipped
# IndependentDirector size table; 0.88 is roughly its hand-written `tight` block.
SCALES = (1.00, 0.96, 0.92, 0.88, 0.84, 0.80)


def _px(n, scale):
    return "%dpx" % round(n * scale)


def _identity_px(n, scale, floor=64):
    """Identity type never goes under its C8 floor, whatever the scale."""
    return "%dpx" % max(round(n * scale), floor)


def _rules(pal, scale):
    """The size table, scaled. Every px value on the face lives here and nowhere
    else, which is what makes auto-fit a single number instead of an override
    block per ad."""
    s = scale
    return [
        ("*", {"margin": "0", "padding": "0", "box-sizing": "border-box"}),
        ("html,body", {"width": _px(W, 1), "height": _px(H, 1), "overflow": "hidden"}),
        ("body", {"font-family": SANS, "background": pal["page"], "color": pal["ink"]}),
        (".canvas", {"width": _px(W, 1), "height": _px(H, 1),
                     "padding": "%s %s %s" % (_px(42, s), _px(GUTTER, 1), _px(40, s)),
                     "display": "flex", "flex-direction": "column"}),
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline", "margin-bottom": _px(26, s)}),
        (".brand", {"font-size": _px(28, s), "font-weight": "800"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(21, s), "font-weight": "800",
                      "letter-spacing": ".14em", "text-transform": "uppercase",
                      "color": pal["accent"]}),

        # ad_lint C8 reads .callout and .head by CLASS NAME. Both are emitted as
        # real classes with a real font-size, never inline styles -- the 25 Aug
        # 2026 silent pass was a generator that emitted inline styles only.
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _identity_px(66, s), "font-weight": "900",
                      "line-height": "1.04", "letter-spacing": "-.02em",
                      "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(16, s), _px(24, s), _px(20, s)),
                      "border-radius": "10px"}),
        (".head", {"font-size": _identity_px(64, s), "font-weight": "900",
                   "line-height": "1.06", "letter-spacing": "-.026em",
                   "margin-top": _px(20, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),

        (".card", {"background": pal["card"], "border": "3px solid " + pal["line"],
                   "border-radius": "12px",
                   "padding": "%s %s" % (_px(26, s), _px(30, s)),
                   "margin-top": _px(24, s)}),
        (".card .lbl", {"font-size": _px(23, s), "font-weight": "800",
                        "letter-spacing": ".13em", "text-transform": "uppercase",
                        "color": pal["accent"], "margin-bottom": _px(6, s)}),
        (".card .big", {"font-size": _px(82, s), "font-weight": "900",
                        "letter-spacing": "-.03em", "line-height": "1.02"}),
        (".card .sub", {"font-size": _px(26, s), "font-weight": "600",
                        "margin-top": _px(6, s)}),

        (".band", {"margin-top": _px(14, s), "flex-shrink": "0",
                   "border-radius": "12px", "overflow": "hidden",
                   "border": "3px solid " + pal["line"], "line-height": "0"}),
        (".band img", {"width": "100%", "display": "block"}),
        (".band.fit", {"display": "flex", "justify-content": "center",
                       "background": "transparent", "border": "0",
                       "border-radius": "0"}),
        (".band.fit img", {"width": "auto", "max-width": "100%",
                           "border-radius": "12px",
                           "border": "3px solid " + pal["line"]}),

        (".duo", {"display": "flex", "gap": _px(18, s), "margin-top": _px(22, s),
                  "height": _px(352, s)}),
        (".duo .card", {"flex": "1.02", "margin-top": "0",
                        "padding": "%s %s" % (_px(22, s), _px(24, s)),
                        "display": "flex", "flex-direction": "column",
                        "justify-content": "center"}),
        (".duo .card .lbl", {"font-size": _px(21, s), "letter-spacing": ".1em"}),
        (".duo .card .big", {"font-size": _px(74, s)}),
        (".duo .card .sub", {"font-size": _px(24, s)}),
        (".duo .shot", {"flex": "1", "border-radius": "12px", "overflow": "hidden",
                        "border": "3px solid " + pal["line"]}),
        (".duo .shot img", {"width": "100%", "height": "100%",
                            "object-fit": "cover", "object-position": "center",
                            "display": "block"}),

        (".def", {"font-size": _px(31, s), "line-height": "1.38",
                  "margin-top": _px(22, s)}),
        (".proof", {"font-size": _px(27, s), "font-weight": "800",
                    "line-height": "1.34", "margin-top": _px(18, s),
                    "margin-bottom": _px(10, s), "color": pal["accent"]}),
        (".grow", {"flex": "1", "min-height": "0"}),

        (".tkhead", {"font-size": _px(22, s), "font-weight": "800",
                     "letter-spacing": ".14em", "text-transform": "uppercase",
                     "color": pal["accent"], "margin-bottom": _px(13, s),
                     "padding-top": _px(18, s),
                     "border-top": "3px solid " + pal["line"]}),
        # min-height turns a silent overlap into visible overflow, which fit.py
        # then catches as F1 rather than F2 (SKILL.md, 26 Aug 2026).
        (".tk", {"font-size": _px(29, s), "font-weight": "600", "line-height": "1.3",
                 "margin-bottom": _px(10, s), "padding-left": _px(36, s),
                 "text-indent": _px(-36, s), "min-height": _px(30, s)}),
        (".tk span", {"color": pal["accent"], "font-weight": "900",
                      "margin-right": _px(13, s)}),

        (".bar", {"display": "flex", "align-items": "center", "gap": _px(22, s),
                  "margin-top": _px(22, s)}),
        (".btn", {"background": pal["accent"], "color": "#fff", "font-size": _px(31, s),
                  "font-weight": "800",
                  "padding": "%s %s" % (_px(19, s), _px(32, s)),
                  "border-radius": "9px", "white-space": "nowrap"}),
        (".terms", {"font-size": _px(24, s), "font-weight": "700",
                    "line-height": "1.3"}),
        (".terms b", {"font-weight": "800"}),
        (".trust", {"font-size": _px(21, s), "font-weight": "700",
                    "margin-top": _px(14, s), "color": pal["accent"]}),
    ]


def css(pal, scale=1.0, layout="default"):
    """`default` is the original chassis and is byte-identical to what shipped.
    Any other name comes from adkit.layouts, where each skeleton names the
    approved-and-priced face it was lifted from."""
    out = []
    rules = _rules(pal, scale) if layout == "default"         else layouts.rules(layout, pal, scale)
    for sel, props in rules:
        body = ";".join("%s:%s" % (k, v) for k, v in props.items())
        out.append("%s{%s}" % (sel, body))
    return "\n".join(out)


def callout_px(scale):
    return max(round(66 * scale), int(fit.CALLOUT_FLOOR))


def head_px(scale):
    return max(round(64 * scale), int(fit.HEAD_FLOOR))


class Ad(object):
    def __init__(self, name, palette, callout, head="", card=None, definition="",
                 proof="", banner=None, banner_h=None, shot=None,
                 layout="default", extra=None):
        if layout != "default" and layout not in layouts.LAYOUTS:
            raise ValueError("unknown layout %r. Known: default, %s"
                             % (layout, ", ".join(sorted(layouts.LAYOUTS))))
        self.layout = layout
        self.extra = dict(extra or {})
        self.name = name
        self.palette_name = palette if isinstance(palette, str) else "(literal)"
        self.pal = palettes.get(palette)
        self.callout = callout
        self.head = head
        self.card = card
        self.definition = definition
        self.proof = proof
        self.banner = banner
        self.banner_h = banner_h
        self.shot = shot

    def body(self):
        card = ""
        if self.card:
            lbl, big, sub = self.card
            card = ('<div class="card"><div class="lbl">%s</div>'
                    '<div class="big">%s</div><div class="sub">%s</div></div>'
                    % (lbl, big, sub))
        if self.shot:
            hero = ('<div class="duo">%s<div class="shot">'
                    '<img src="../photos/%s" alt=""></div></div>' % (card, self.shot))
        else:
            hero = card
        if self.banner and self.banner_h:
            strip = ('<div class="band fit"><img src="../photos/%s" '
                     'style="height:%dpx" alt=""></div>' % (self.banner, self.banner_h))
        elif self.banner:
            strip = '<div class="band"><img src="../photos/%s" alt=""></div>' % self.banner
        else:
            strip = ""
        head = '<div class="head">%s</div>' % self.head if self.head else ""
        proof = '<div class="proof">%s</div>' % self.proof if self.proof else ""
        definition = '<div class="def">%s</div>' % self.definition if self.definition else ""
        return ('<div class="callout">%s</div>%s%s%s%s%s'
                % (self.callout, strip, head, hero, definition, proof))


class Kit(object):
    """One kit's constants, plus its ads. Everything a face repeats lives here
    once -- the brand lockup, the eyebrow, the takeaway list, the CTA, the terms
    strip and the trust line."""

    def __init__(self, root, brand, eyebrow, takeaways, cta, terms, trust=""):
        self.root = pathlib.Path(root).parent if str(root).endswith(".py") \
            else pathlib.Path(root)
        self.brand = brand
        self.eyebrow = eyebrow
        self.takeaways = list(takeaways)
        self.cta = cta
        self.terms = terms
        self.trust = trust
        self.ads = []

    def face(self, name, **kw):
        self.ads.append(Ad(name, **kw))
        return self

    def html(self, ad, scale=1.0):
        if ad.layout != "default":
            return ('<!doctype html><html><head><meta charset="utf-8">'
                    '<style>%s</style></head><body><div class="canvas">'
                    '%s</div></body></html>'
                    % (css(ad.pal, scale, ad.layout),
                       layouts.shell(ad.layout, self, ad, scale)))
        ticks = "".join('<div class="tk"><span>&#10003;</span>%s</div>' % t
                        for t in self.takeaways)
        trust = '<div class="trust">%s</div>' % self.trust if self.trust else ""
        return ('<!doctype html><html><head><meta charset="utf-8">'
                '<style>\n%s\n</style></head><body><div class="canvas">'
                '<div class="top"><div class="brand">%s</div>'
                '<div class="eyebrow">%s</div></div>'
                '%s'
                '<div class="grow"></div>'
                '<div class="tkhead">What you leave with</div>%s'
                '<div class="bar"><div class="btn">%s</div>'
                '<div class="terms">%s</div></div>'
                '%s</div></body></html>'
                % (css(ad.pal, scale), self.brand, self.eyebrow, ad.body(),
                   ticks, self.cta, self.terms, trust))

    def _check_palettes(self):
        seen = {}
        clashes = []
        for a in self.ads:
            if a.palette_name in seen:
                clashes.append((seen[a.palette_name], a.name, a.palette_name))
            seen[a.palette_name] = a.name
        return clashes

    def render(self, *only, **kw):
        """Write html/ and ads/, auto-fitting each face. Returns exit-code style
        int: 0 clean, 1 something did not fit."""
        verbose = kw.pop("verbose", True)
        html_dir = self.root / "html"
        ads_dir = self.root / "ads"
        html_dir.mkdir(parents=True, exist_ok=True)
        ads_dir.mkdir(parents=True, exist_ok=True)

        clashes = self._check_palettes()
        if clashes:
            for a, b, p in clashes:
                print("  RULE 4  %s and %s share palette %r. One palette per ad."
                      % (a, b, p))
            return 1

        want = [o.lstrip("0") for o in only]
        chrome = fit.find_chrome()
        bad = 0
        for ad in self.ads:
            if want and ad.name.split("_")[0].lstrip("0") not in want:
                continue
            src = html_dir / ("%s.html" % ad.name)
            chosen, last = None, []
            for s in SCALES:
                src.write_text(self.html(ad, s), encoding="utf-8")
                try:
                    last = fit.check(src, chrome)
                except RuntimeError as e:
                    print("  %-38s ERROR   %s" % (ad.name, e))
                    last = ["probe did not run"]
                    break
                if not last:
                    chosen = s
                    break
            if chosen is None:
                bad += 1
                print("  %-38s DOES NOT FIT at any scale down to %.2f. Cut "
                      "words: identity type is clamped at %dpx and will not "
                      "shrink to make room." % (ad.name, min(SCALES),
                                                int(fit.CALLOUT_FLOOR)))
                for line in last:
                    print("      " + line)
                continue
            src.write_text(self.html(ad, chosen), encoding="utf-8")
            out = ads_dir / ("%s.png" % ad.name)
            subprocess.run([chrome, "--headless=new", "--disable-gpu",
                            "--hide-scrollbars", "--screenshot=%s" % out,
                            "--window-size=%d,%d" % (W, H),
                            "--force-device-scale-factor=1",
                            src.resolve().as_uri()],
                           check=True, capture_output=True)
            if verbose:
                note = "" if chosen == 1.00 else "  (auto-fit %.2f)" % chosen
                print("  %-38s rendered  callout %dpx  head %dpx%s"
                      % (ad.name, callout_px(chosen), head_px(chosen), note))
        if bad:
            print("\n  %d face(s) did not fit. A face that only fits below the "
                  "64px/56px floors is not tight, it is non-compliant." % bad)
        # `only` matches the NUMBER before the first underscore, not the name. A name
        # ("01_cal_recently_retired") matched nothing and rendered nothing, silently,
        # and the old PNG stayed on disk looking current (28 Sep 2026; the calendar
        # memory records the same miss on 23 Sep). Say so instead.
        if want and not any(ad.name.split("_")[0].lstrip("0") in want for ad in self.ads):
            print("  NOTHING RENDERED: %s matched no face. Pass the ad number, e.g. 01."
                  % ", ".join(only))
            return 1
        return 1 if bad else 0


def main(argv):
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
