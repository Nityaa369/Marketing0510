#!/usr/bin/env python3
"""Layouts scaffolded from a reference image. Generated stubs land here.

WHY THIS FILE EXISTS (15 Sep 2026). Pushed back on directly, and correctly:

    "generation is also a bottleneck, I had once given a few samples and you
     could not generate ads using that."

That is true, and the reason is structural rather than a bad prompt. Every visual
this account can produce comes from the layouts hand-written in `adkit/layouts.py`
and `adkit/layouts_social.py`. A layout is 50 to 115 lines of CSS plus a 20 to 45
line HTML shell, written against a contract that was never written down: which
class names the size gates look for (`ad_lint` C8 and `adkit.fit` both hunt for a
sized `.callout` and `.head`), which floors they must clear (64px, and 56px for the
identity bar), and which fields the shell must emit or `adkit.restyle` will mark
the layout incompatible with most copy.

So handing over reference images produced nothing, because the step between "here
is a picture I like" and "a layout the chassis can use" was an undocumented
80-line coding task. `restyle --spread` made that worse by being honest about it:
it can reach the eleven layouts that exist and cannot invent a twelfth.

WHAT THE SCAFFOLD DOES. `python -m adkit.layouts --new <name>` clones `notice` -
the cheapest face in the account, Rs 29.65/lead - under a new name, registers it,
and leaves you a layout that ALREADY renders, already clears the size floors, and
already emits every copy field. The remaining work is the part that needs eyes on
the reference: change the CSS. The contract is satisfied before you start, and
`python -m adkit.layouts --contract` prints what that contract is.

This file is separate from `layouts.py` on purpose. Provenance has to stay visible:
nothing in here was lifted from a priced face, so nothing in here carries a cost,
and `--list` will say so.
"""

# The clone source. Imported lazily inside the functions below to avoid
# a circular import - layouts.py imports this module at the bottom.
LAYOUTS = {}
PROVENANCE = {}


def _notice(pal, s):
    from .layouts import _notice as f
    return f(pal, s)


def _notice_shell(kit, ad, s):
    from .layouts import _notice_shell as f
    return f(kit, ad, s)


# The chassis helpers every layout is built from. Imported lazily for the same
# reason as above - layouts.py pulls this module in at the bottom of its own
# import, so a top-level `from .layouts import ...` would be circular.
#   _px    scale a pixel value with the auto-fitter
#   _idpx  same, but clamped at the 64px identity floor (.callout and .head only)
#   _base  the shared reset, canvas and .grow spacers
#   _plain strip markup from a brand string
# See `python -m adkit.layouts --contract`.

def _px(n, s):
    from .layouts import _px as f
    return f(n, s)


def _idpx(n, s, floor=64):
    from .layouts import _idpx as f
    return f(n, s, floor)


def _base(pal, s):
    from .layouts import _base as f
    return f(pal, s)


def _plain(s):
    from .layouts import _plain as f
    return f(s)


def _fonts():
    """(SERIF, SANS). A module-level `__getattr__` does NOT work here: PEP 562
    covers attribute access on the module object, while a bare `SERIF` inside a
    function is a global lookup straight into the module dict, so it raises
    NameError and never reaches the hook. Call this instead."""
    from .layouts import SERIF, SANS
    return SERIF, SANS




# ---------------------------------------------------------------- worklist
# Built 15 Sep 2026 from reference_images/IMG-20260806-WA0057.jpg
# (LawSikho, practising lawyers and in-house counsel, 29-31 Aug).
#
# Scaffolded with `--new`, which starts a layout as a clone of `notice` so it
# renders and clears the floors from the first command; the CSS below is then
# written against the reference. The class names and the 64px floors are the
# contract - see `python -m adkit.layouts --contract`.

def _worklist(pal, s):
    """The named-work list. Built 15 Sep 2026 from reference_images/
    IMG-20260806-WA0057.jpg (LawSikho, practising lawyers, 29-31 Aug).

    WHAT IT TAKES FROM THE REFERENCE. A hard accent band carrying the ICP, a
    serif display headline with one coloured clause, then the distinctive part:
    a kicker introducing a LIST OF NAMED WORK, each row on a thick left accent
    bar with a small-caps label above an ordinary-words line. Then the plain
    definition, the delivery sentence, a full-width dark CTA, and the brand
    bottom-right rather than top-left.

    WHAT IT DELIBERATELY DOES NOT TAKE. In the reference every row ends in a
    rate - "$300-400 per filing", "$100 per assignment". That is the pay-chart
    shape, which is the single worst-performing format in this account: index
    2.34 against par, measured across four product lines (Independent Director
    3.2x, Patent 3.1x, US Accounting 2.5x, Academic Writing 1.71x). The standing
    compliance list also keeps figures like that on the landing page and off the
    face. So the row's emphasis slot carries a CONCRETE DETAIL of the work, never
    a price. The skeleton is the borrowing; the rate card is not.

    Rows come from extra["rows"] as "LABEL | what it is" strings, and fall back
    to kit.takeaways so any kit renders without new data.
    """
    SERIF, _ = _fonts()
    return _base(pal, s) + [
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.06", "letter-spacing": "-.015em",
                      "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(18, s), _px(26, s), _px(22, s))}),
        (".head", {"font-family": SERIF, "font-size": _idpx(72, s),
                   "font-weight": "700", "line-height": "1.08",
                   "letter-spacing": "-.02em", "color": pal["ink"],
                   "margin-top": _px(30, s)}),
        (".head em", {"font-style": "italic", "font-weight": "700",
                      "color": pal["accent"]}),
        (".kick", {"font-size": _px(28, s), "font-weight": "800",
                   "letter-spacing": ".08em", "text-transform": "uppercase",
                   "color": pal["accent"], "margin-top": _px(30, s)}),
        (".rows", {"margin-top": _px(20, s)}),
        (".row", {"border-left": "%s solid %s" % (_px(7, s), pal["accent"]),
                  "padding-left": _px(22, s), "margin-top": _px(20, s)}),
        (".rlab", {"font-size": _px(26, s), "font-weight": "800",
                   "letter-spacing": ".1em", "text-transform": "uppercase",
                   "color": pal["accent"], "margin-bottom": _px(4, s)}),
        (".rtxt", {"font-size": _px(32, s), "line-height": "1.3",
                   "color": pal["ink"]}),
        (".rtxt b", {"font-weight": "800"}),
        # NO opacity here. simplicity.py R1 blocks text set at reduced opacity -
        # the "no blind-spot grey" rule from the 14 Aug clarity feedback. It fired
        # on the first render of this layout. Hierarchy comes from size and weight,
        # never from fading the words.
        (".def", {"font-size": _px(30, s), "line-height": "1.36",
                  "color": pal["ink"], "margin-top": _px(28, s)}),
        (".deliver", {"font-size": _px(31, s), "font-weight": "700",
                      "line-height": "1.32", "color": pal["ink"],
                      "margin-top": _px(16, s)}),
        (".cta", {"background": pal["ink"], "color": pal["page"],
                  "font-size": _px(37, s), "font-weight": "800",
                  "text-align": "center", "letter-spacing": ".01em",
                  "padding": "%s 0" % _px(22, s), "margin-top": _px(26, s)}),
        (".foot", {"display": "flex", "align-items": "baseline",
                   "justify-content": "space-between", "gap": _px(18, s),
                   "margin-top": _px(18, s)}),
        (".foot .sm", {"font-size": _px(26, s), "font-weight": "700",
                       "letter-spacing": ".04em", "color": pal["ink"]}),
        (".fbrand", {"font-family": SERIF, "font-size": _px(34, s),
                     "font-weight": "700", "color": pal["ink"],
                     "white-space": "nowrap"}),
    ]


def _worklist_rows(kit, ad, s):
    """extra["rows"] as "LABEL | text", else kit.takeaways with no label."""
    rows = ad.extra.get("rows") or list(kit.takeaways)[:4]
    out = []
    for r in rows:
        if "|" in r:
            lab, _, txt = r.partition("|")
            out.append('<div class="row"><div class="rlab">%s</div>'
                       '<div class="rtxt">%s</div></div>'
                       % (lab.strip(), txt.strip()))
        else:
            out.append('<div class="row"><div class="rtxt">%s</div></div>'
                       % r.strip())
    return '<div class="rows">%s</div>' % "".join(out)


def _worklist_shell(kit, ad, s):
    x = ad.extra
    return (
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="kick">%s</div>'
        '%s'
        '<div class="grow"></div>'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="cta">%s</div>'
        '<div class="foot"><div class="sm">%s</div>'
        '<div class="fbrand">%s</div></div>'
        % (ad.callout, ad.head,
           x.get("kick", "Here is the work, and what it is"),
           _worklist_rows(kit, ad, s),
           ad.definition, x.get("deliver", ""), kit.cta,
           x.get("foot_left", kit.terms or "Live only, no recordings"),
           _plain(kit.brand)))


LAYOUTS["worklist"] = (_worklist, _worklist_shell)
PROVENANCE["worklist"] = (
    "reference_images/IMG-20260806-WA0057.jpg", "-",
    "Named-work list on accent bars, serif head, brand bottom-right. The "
    "reference's per-row rates are deliberately NOT carried: pay-chart shape, "
    "index 2.34 vs par.")


# ---------------------------------------------------------------- search
# Scaffolded 17 Sep 2026 from: Inspo supplied in chat 17 Sep 2026: Natural Outcome hyaluronic moisturizer static, 'the search:' query bar then 'the solution:' packshot
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _search(pal, s):
    """The search and the solution. Built 17 Sep 2026 from a DTC skincare static
    supplied in chat: "the search:" over a search-bar query, "the solution:" over
    the product.

    WHAT IT TAKES FROM THE REFERENCE. Two big lowercase labels that do the work of
    a headline, a single search bar holding the reader's own query in their own
    words, and the answer presented as the thing you would buy. The reader's
    question sits above the answer, so the face reads as a before and after with
    no diagram.

    WHAT IT CHANGES. The reference opens on "the search:" with no reader named.
    This account names the ICP first, always (the eight cheapest ID statics all
    carried the audience slab above the headline), so the call-out band sits above
    both labels. The packshot becomes the offer card, because the product is a
    live camp, and the account's approved corpus is a card or artefact, not a
    photo. The card carries the head at the 64px identity floor, so C8 and fit
    see a real `.head`.
    """
    SERIF, _ = _fonts()
    return _base(pal, s) + [
        # Version 2, 17 Sep 2026, after "i think you can improve the layout". Four
        # things changed, each a defect of the first render rather than a taste call:
        #   1. The call-out wrapped to two lines and put the heaviest block on the
        #      face at the very top. It is one line now (shorter copy, tighter band).
        #   2. "the search:" sat as close to "the solution:" as to its own bar, so
        #      the face did not read as two groups. Label-to-object is now tight and
        #      the gap between the two groups is wide - that gap IS the "then".
        #   3. The offer read as a text box. It now carries a product label (tag
        #      left, dates right) like the packshot's printed label in the reference.
        #   4. A three-column footer wrapped every column. One full-width button and
        #      one terms line replace it.
        # The lit backdrop is a plain radial gradient standing in for the reference's
        # studio light. It is not an illustration.
        (".canvas", {"background": "radial-gradient(ellipse 80%% 55%% at 50%% 46%%, "
                                   "#FFFFFF 0%%, %s 70%%)" % pal["page"]}),
        (".srail", {"text-align": "center", "font-size": _px(26, s),
                    "font-weight": "800", "letter-spacing": ".14em",
                    "text-transform": "uppercase", "color": pal["accent"],
                    "margin-bottom": _px(14, s)}),
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.05", "letter-spacing": "-.02em",
                      "text-transform": "uppercase", "text-align": "center",
                      # Balanced, not nowrap: a short reader name stays on one line and a
                      # long one ("A practising Company Secretary?") breaks evenly in two.
                      # nowrap ran the text out of the band (fit F7, 17 Sep 2026).
                      "text-wrap": "balance",
                      "padding": "%s %s %s" % (_px(14, s), _px(18, s), _px(18, s)),
                      "border-radius": "12px",
                      # A floor under the band. On a two-line call-out the flexible
                      # spacer collapsed to zero and "the search:" touched the band.
                      "margin-bottom": _px(34, s)}),
        # Labels shrunk 17 Sep 2026 (76px -> 44px) after a half-asleep read: the biggest
        # words after the call-out said "the search:" and "the solution:", which carry no
        # meaning. The headline must be the second-biggest thing on the face.
        (".slab", {"text-align": "center", "font-size": _px(44, s),
                   "font-weight": "900", "letter-spacing": "-.04em",
                   "line-height": "1", "color": pal["ink"]}),
        (".gap", {"height": _px(64, s), "flex": "none"}),
        (".bar", {"display": "flex", "align-items": "center", "gap": _px(24, s),
                  "background": "#FFFFFF", "border-radius": _px(40, s),
                  "margin": "%s %s 0" % (_px(24, s), _px(24, s)),
                  "padding": "%s %s" % (_px(28, s), _px(44, s)),
                  "border": "2px solid " + pal["line"],
                  "box-shadow": "0 12px 30px rgba(0,0,0,.07)"}),
        (".bar svg", {"width": _px(46, s), "height": _px(46, s), "flex": "none"}),
        (".query", {"font-size": _px(48, s), "font-weight": "500",
                    "line-height": "1.22", "color": pal["ink"],
                    # Balanced so a long search never strands one word on line two.
                    "text-wrap": "balance"}),
        # The typing caret. One thin bar in the accent, the detail that makes a
        # rounded rectangle read as a search box someone is using right now. The
        # query is a plain block, not flex: in a flex row a two-line query pushed the
        # caret to the far right edge instead of after the last word (17 Sep 2026).
        (".caret", {"display": "inline-block", "width": _px(4, s),
                    "height": _px(52, s), "background": pal["accent"],
                    "margin-left": _px(6, s), "vertical-align": "-0.18em"}),
        (".offer", {"background": "#FFFFFF", "border-radius": "20px",
                    "margin-top": _px(24, s),
                    "padding": "%s %s %s" % (_px(30, s), _px(34, s), _px(34, s)),
                    "border": "2px solid " + pal["line"],
                    "box-shadow": "0 22px 50px rgba(0,0,0,.13)"}),
        (".olabel", {"display": "flex", "justify-content": "space-between",
                     "align-items": "center", "gap": _px(16, s),
                     "padding-bottom": _px(20, s), "margin-bottom": _px(24, s),
                     "border-bottom": "2px dashed " + pal["line"]}),
        # Offer tag enlarged 17 Sep 2026: in a skim test, cut-down September faces never
        # said "free class" at a glance, because it was fine print.
        (".otag", {"background": pal["accent"], "color": "#fff",
                   "font-size": _px(36, s), "font-weight": "800",
                   "letter-spacing": ".08em", "text-transform": "uppercase",
                   "padding": "%s %s" % (_px(10, s), _px(18, s)),
                   "border-radius": "8px", "white-space": "nowrap"}),
        (".odate", {"font-size": _px(38, s), "font-weight": "900",
                    "letter-spacing": "-.01em", "color": pal["accent"],
                    "white-space": "nowrap"}),
        (".head", {"font-size": _idpx(74, s), "font-weight": "900",
                   "line-height": "1.06", "letter-spacing": "-.026em",
                   "color": pal["ink"], "text-wrap": "balance"}),
        (".head em", {"font-style": "italic", "font-weight": "900",
                      "color": pal["accent"]}),
        (".def", {"font-size": _px(32, s), "line-height": "1.36",
                  "margin-top": _px(18, s)}),
        # Optional take-away list inside the offer card (extra=dict(gets=[...])),
        # added 23 Sep 2026. The card carried a headline and one line, so the face
        # named what the reader lacked and never what the camp hands over. Absent
        # `gets` leaves every existing search face unchanged.
        (".gets", {"margin-top": _px(14, s)}),
        (".gets .g", {"font-size": _px(30, s), "font-weight": "700",
                      "line-height": "1.26", "padding": "%s 0" % _px(7, s),
                      "border-top": "1px solid " + pal["line"],
                      "color": pal["ink"]}),
        (".gets .g span", {"color": pal["accent"], "font-weight": "900",
                           "margin-right": _px(10, s)}),
        (".deliver", {"font-size": _px(32, s), "font-weight": "500",
                      "line-height": "1.38", "margin-top": _px(20, s),
                      "color": pal["ink"]}),
        (".cta", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(40, s), "font-weight": "800",
                  "text-align": "center", "border-radius": "14px",
                  "padding": "%s 0" % _px(22, s)}),
        (".terms", {"text-align": "center", "font-size": _barpx(28, s),
                    "font-weight": "800", "letter-spacing": ".07em",
                    "text-transform": "uppercase", "color": pal["ink"],
                    "margin-top": _px(18, s)}),
    ]


def _barpx(n, s, floor=30):
    from .layouts import _barpx as f
    return f(n, s, floor)


# A plain magnifier: one circle, one line. It is the search bar's own glyph, the
# one UI element the reference is built on, not an illustration standing in for
# a real image (see the use-real-images memory, which is about drawn scenes).
_GLASS = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
          '<circle cx="10" cy="10" r="6.5" stroke="#6B6B6B" stroke-width="2.2"/>'
          '<line x1="15" y1="15" x2="21" y2="21" stroke="#6B6B6B" '
          'stroke-width="2.2" stroke-linecap="round"/></svg>')


def _search_shell(kit, ad, s):
    """extra: query, offer_tag, offer_date, deliver, terms_line.
    q_label / a_label default to the reference's own "the search:" / "the solution:"."""
    x = ad.extra
    definition = ('<div class="def">%s</div>' % ad.definition) if ad.definition else ""
    return (
        '<div class="srail">%s &middot; %s</div>'
        '<div class="callout">%s</div>'
        '<div class="grow"></div>'
        '%s'
        '<div class="bar">%s<div class="query">%s<span class="caret"></span></div></div>'
        '<div class="gap"></div>'
        '%s'
        '<div class="offer"><div class="olabel"><span class="otag">%s</span>'
        '<span class="odate">%s</span></div>'
        '<div class="head">%s</div>%s%s'
        '<div class="deliver">%s</div></div>'
        '<div class="grow"></div>'
        '<div class="cta">%s</div>'
        '<div class="terms">%s</div>'
        % (_plain(kit.brand), kit.eyebrow, ad.callout,
           # Both stage labels can be suppressed with q_label="" / a_label="".
           # Added 23 Sep 2026: band, label, query, label, card is four stages
           # before the offer, and the face read as "too complicated". The 19
           # October search faces pass neither key and are unchanged.
           ('<div class="slab">%s</div>' % x["q_label"]) if x.get("q_label") else
           ('' if "q_label" in x else '<div class="slab">the search:</div>'),
           _GLASS, x.get("query", ""),
           ('<div class="slab">%s</div>' % x["a_label"]) if x.get("a_label") else
           ('' if "a_label" in x else '<div class="slab">the solution:</div>'),
           x.get("offer_tag", ""), x.get("offer_date", ""),
           ad.head, definition,
           ('<div class="gets">%s</div>'
            % "".join('<div class="g"><span>&#10003;</span>%s</div>' % g
                      for g in x["gets"])) if x.get("gets") else "",
           x.get("deliver", ""),
           kit.cta, x.get("terms_line", ad.proof)))


LAYOUTS["search"] = (_search, _search_shell)


# ---------------------------------------------------------------- chat
# Built 17 Sep 2026 from a DTC static supplied in chat (a phone chat thread: a friend's grey
# bubble "Girl! My skin is breaking out, what should I do?", a picture message of the
# product, a blue "Try this" bubble, and the message bar).
#
# VERSION 2, 18 Sep 2026, after Ruchika: "the first message and the second message are not
# cohesive... if you look at the original sample, the problem statement and solution are too
# obvious. That is what we want." Three defects of v1, each fixed here:
#   1. The first bubble was an ad call-out in the second person ("A banker, retired after 30
#      years?"). Nobody texts like that. It is now the reader's own message, first person.
#   2. The reply was a card with a tag, a headline and a three-line paragraph, which reads as
#      an ad, not as a message. The paragraph is gone. What goes out is a SHARED POSTER: the
#      thing a friend would forward, carrying the offer and nothing else.
#   3. Nothing linked the two. A short outgoing line now answers the question in a friend's
#      words before the poster lands, so problem and solution sit next to each other.
#
# The chassis contract is unchanged: `.callout` is the incoming message (the ICP named first,
# in their own words) and `.head` is the poster's headline, both at or above the 64px floor.
#
# EVIDENCE WARNING. SOP/10 prices toon/chat faces at 1.22x par, and nothing on this layout
# has a live cost. It is a format test; judge it within its own campaign.

def _gutter():
    from .layouts import GUTTER
    return GUTTER


def _chat(pal, s):
    g = _gutter()
    return _base(pal, s) + [
        (".canvas", {"background": "#FFFFFF"}),
        (".chead", {"display": "flex", "align-items": "center",
                    "justify-content": "space-between",
                    "margin": "-%s -%spx 0" % (_px(44, s), g),
                    "padding": "%s %spx %s" % (_px(22, s), g, _px(18, s)),
                    "background": pal["page"], "border-bottom": "2px solid " + pal["line"]}),
        (".chead svg", {"width": _px(50, s), "height": _px(50, s), "color": pal["accent"]}),
        (".cname", {"text-align": "center", "font-size": _px(38, s), "font-weight": "700",
                    "color": pal["ink"], "line-height": "1.1"}),
        (".csub", {"font-size": _px(34, s), "font-weight": "700", "letter-spacing": ".12em",
                   "text-transform": "uppercase", "color": pal["accent"],
                   "margin-top": _px(4, s)}),
        (".gap", {"height": _px(26, s), "flex": "none"}),
        # 1. the reader's own message, in their words
        (".callout", {"flex": "none", "align-self": "flex-start", "max-width": "92%",
                      "background": "#ECECEE", "color": "#111",
                      "font-size": _idpx(64, s), "font-weight": "500",
                      "line-height": "1.18", "letter-spacing": "-.01em",
                      "margin-top": _px(28, s), "padding": "%s %s" % (_px(28, s), _px(38, s)),
                      "border-radius": "%s %s %s %s" % (_px(44, s), _px(44, s),
                                                        _px(44, s), _px(10, s))}),
        # 2. the friend's reply in words, so the poster is not the first answer
        (".reply", {"flex": "none", "align-self": "flex-end", "max-width": "80%",
                    "background": pal["accent"], "color": "#fff",
                    "font-size": _px(46, s), "font-weight": "600", "line-height": "1.2",
                    "padding": "%s %s" % (_px(22, s), _px(34, s)),
                    "border-radius": "%s %s %s %s" % (_px(44, s), _px(44, s),
                                                      _px(10, s), _px(44, s)),
                    "margin-top": _px(16, s), "text-wrap": "balance"}),
        # 3. the shared poster. v2b, 18 Sep 2026: in v2 the poster was the same accent as the
        # two bubbles, so reply, poster and CTA merged into one dark mass and the poster
        # stopped reading as an attachment. It is now a flyer: paper ground, a coloured band
        # with the offer and the brand, and photo corners (one radius, not a bubble tail), so
        # the eye reads it as the thing a friend forwarded.
        (".poster", {"flex": "none", "align-self": "flex-end", "width": "88%", "margin-top": _px(14, s),
                     "background": pal["card"], "color": pal["ink"],
                     "border": "2px solid " + pal["line"],
                     "border-radius": _px(28, s), "overflow": "hidden",
                     "box-shadow": "0 18px 40px rgba(0,0,0,.16)"}),
        (".pband", {"background": pal["accent"], "color": "#fff",
                    "display": "flex", "align-items": "center",
                    "justify-content": "space-between", "gap": _px(14, s),
                    "padding": "%s %s" % (_px(16, s), _px(28, s))}),
        (".ptag", {"font-size": _px(34, s), "font-weight": "800", "letter-spacing": ".08em",
                   "text-transform": "uppercase"}),
        (".pbrand", {"font-size": _px(34, s), "font-weight": "800", "letter-spacing": ".06em",
                     "text-transform": "uppercase", "white-space": "nowrap"}),
        (".pbody", {"padding": "%s %s %s" % (_px(20, s), _px(26, s), _px(18, s))}),
        (".head", {"font-size": _idpx(68, s), "font-weight": "900", "line-height": "1.06",
                   "letter-spacing": "-.025em", "color": pal["ink"],
                   "text-wrap": "balance"}),
        (".head em", {"font-style": "italic", "color": pal["accent"]}),
        (".pdate", {"font-size": _px(34, s), "font-weight": "900", "color": pal["accent"],
                    "margin-top": _px(12, s), "padding-top": _px(10, s),
                    "border-top": "2px solid " + pal["line"]}),
        # the agenda. Added 18 Sep 2026 on review: "in the original ads, there is more
        # information around what happens in the bootcamp. currently it is all lost." The
        # chat layout had replaced the old faces' session list with one chips line, so the
        # face said what the camp was called and never what happens in it. A forwarded event
        # flyer is exactly the artefact that carries an agenda, so the day rows go inside it.
        (".agenda", {"margin-top": _px(10, s), "display": "flex",
                     "flex-direction": "column", "gap": _px(8, s)}),
        (".prow", {"display": "flex", "gap": _px(18, s), "align-items": "flex-start"}),
        (".pday", {"flex": "none", "width": _px(178, s), "font-size": _px(33, s),
                   "font-weight": "800", "letter-spacing": ".05em",
                   "text-transform": "uppercase", "color": pal["accent"],
                   "line-height": "1.18", "padding-top": _px(3, s)}),
        (".ptitle", {"font-size": _px(35, s), "font-weight": "800", "color": pal["ink"],
                     "line-height": "1.15"}),
        (".psub", {"font-size": _px(33, s), "font-weight": "600", "color": pal["ink"],
                   "line-height": "1.25", "margin-top": _px(3, s)}),
        (".pkeep", {"font-size": _px(32, s), "font-weight": "700", "color": pal["ink"],
                    "margin-top": _px(12, s), "padding-top": _px(10, s),
                    "border-top": "2px solid " + pal["line"], "line-height": "1.3"}),
        (".pcta", {"display": "block", "background": pal["accent"], "color": "#fff",
                   "font-size": _px(40, s), "font-weight": "800", "text-align": "center",
                   "letter-spacing": "-.01em", "border-radius": _px(14, s),
                   "margin-top": _px(14, s),
                   "padding": "%s %s" % (_px(16, s), _px(20, s))}),
        (".chips", {"font-size": _px(32, s), "font-weight": "700", "margin-top": _px(8, s),
                    "color": pal["ink"]}),
        (".cta", {"align-self": "flex-end", "margin-top": _px(14, s),
                  "background": pal["accent"], "color": "#fff",
                  "font-size": _px(46, s), "font-weight": "700",
                  "padding": "%s %s" % (_px(20, s), _px(38, s)),
                  "border-radius": "%s %s %s %s" % (_px(44, s), _px(44, s),
                                                    _px(10, s), _px(44, s))}),
        (".terms", {"align-self": "flex-end", "font-size": _barpx(26, s),
                    "font-weight": "800", "letter-spacing": ".06em",
                    "text-transform": "uppercase", "color": pal["ink"],
                    "margin-top": _px(10, s)}),
        # the message bar, slimmer in v2: it is chrome, and v1 gave it too much room
        # margin-top, not the .grow spacer above it: grow collapses to zero on a full face,
        # so the closing bubble was sitting flush on the message bar. 18 Sep 2026, on review:
        # "for some ads, the last message is merging with the last line". Same defect as the
        # header gap, same fix.
        (".cbar", {"display": "flex", "align-items": "center", "gap": _px(18, s),
                   "margin-top": _px(34, s)}),
        (".cplus", {"width": _px(50, s), "height": _px(50, s), "border-radius": "50%",
                    "background": "#E3E3E8", "display": "flex", "align-items": "center",
                    "justify-content": "center", "flex": "none"}),
        (".cfield", {"flex": "1", "display": "flex", "align-items": "center",
                     "justify-content": "space-between",
                     "border": "2px solid #6E6E73", "border-radius": _px(60, s),
                     "padding": "%s %s" % (_px(8, s), _px(24, s))}),
        (".cfield span", {"font-size": _px(30, s), "color": "#55555A"}),
        (".cbar svg", {"width": _px(34, s), "height": _px(34, s)}),
    ]


_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
_BACK = _SVG % ("currentColor", "2.6", '<polyline points="15 4 7 12 15 20"/>')
_VIDEO = _SVG % ("currentColor", "1.8", '<rect x="2" y="6" width="14" height="12" rx="2"/><polygon points="22 8 16 12 22 16 22 8"/>')
_PLUS = _SVG % ("#3A3A3C", "2", '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>')
_MIC = _SVG % ("#2B2B2E", "1.8", '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><line x1="12" y1="18" x2="12" y2="22"/>')
_PIC = _SVG % ("#2B2B2E", "1.8", '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><polyline points="21 15 16 10 5 21"/>')
_HEART = _SVG % ("#2B2B2E", "1.8", '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>')


def _chat_shell(kit, ad, s):
    """extra: reply, offer_tag, offer_date, agenda, keep_line, chips, terms_line, cta_emoji.

    `callout` is the reader's own message, first person, about 50 characters. `reply` is the
    friend's answer in words, and is OPTIONAL: leave it out and the flyer answers the question
    on its own, which is the shape of the reference. `head` is the flyer's headline.

    `cta_line` is the friend's closing nudge and overrides kit.cta for this face, because the
    same sentence on all eighteen faces reads as a template ("go, generate all the rest with
    the varied closing lines", 18 Sep 2026). The offer terms are carried by the flyer's band
    and its button, so this line never has to sell.

    `agenda` is a list of (day, title, sub) triples, one per session, and `keep_line` is what
    the reader takes away. Both are what the flyer is FOR: the review on 18 Sep 2026 was that
    the chat faces had lost everything the older faces said about what happens in the camp.
    `chips` remains for a face that wants a single line instead, and is ignored when `agenda`
    is given."""
    x = ad.extra
    rows = "".join(
        '<div class="prow"><div class="pday">%s</div><div><div class="ptitle">%s</div>'
        '<div class="psub">%s</div></div></div>' % r for r in x.get("agenda") or ())
    body = ('<div class="agenda">%s</div>' % rows) if rows else \
           ('<div class="chips">%s</div>' % x.get("chips", ""))
    if x.get("keep_line"):
        body += '<div class="pkeep">%s</div>' % x["keep_line"]
    if x.get("cta_button"):
        body += '<div class="pcta">%s</div>' % x["cta_button"]
    return (
        '<div class="chead">%s<div class="cname">%s<div class="csub">%s</div></div>%s</div>'
        '<div class="grow"></div>'
        '<div class="callout">%s</div>'
        '%s'
        '<div class="poster"><div class="pband"><span class="ptag">%s</span>'
        '<span class="pbrand">%s</span></div><div class="pbody">'
        '<div class="head">%s</div>'
        '<div class="pdate">%s</div>'
        '%s</div></div>'
        '<div class="cta">%s%s</div>'
        '%s'
        '<div class="grow"></div>'
        '<div class="cbar"><div class="cplus">%s</div><div class="cfield">'
        '<span>Message...</span><span>%s %s %s</span></div></div>'
        % (_BACK, _plain(kit.brand), kit.eyebrow, _VIDEO, ad.callout,
           ('<div class="reply">%s</div>' % x["reply"]) if x.get("reply") else "",
           x.get("offer_tag", ""), _plain(kit.brand), ad.head,
           x.get("offer_date", ""), body,
           x.get("cta_line", kit.cta), x.get("cta_emoji", " &#128070;"),
           ('<div class="terms">%s</div>' % x["terms_line"]) if x.get("terms_line") else "",
           _PLUS, _MIC, _PIC, _HEART))


LAYOUTS["chat"] = (_chat, _chat_shell)
PROVENANCE["chat"] = (
    "DTC skincare chat-thread static supplied in chat, 17 Sep 2026 (grey question bubble, "
    "product picture message, blue 'Try this' bubble)", "-",
    "v2 (18 Sep): the reader's own message in the first person, a friend's reply in words, "
    "then a shared poster instead of a text card. Chat faces price at 1.22x par in SOP/10, "
    "so this is a format test.")
PROVENANCE["search"] = (
    "DTC skincare static supplied in chat, 17 Sep 2026 ('the search:' / "
    "'the solution:')", "-",
    "Search bar holding the reader's own query, then the offer card as the answer. "
    "ICP band added above both labels; packshot replaced by the offer card.")


# ---------------------------------------------------------------- venn
# Built 18 Sep 2026 from a DTC supplement static supplied in chat (blue gradient, "1 CHEW THAT
# DOES BOTH", two outlined circles, the packshot in the intersection, a small caption).
# See this module's docstring for what was taken and what was deliberately changed.
#
# THE ARGUMENT THE SHAPE MAKES. A Venn diagram says one thing: these two are usually separate,
# and here they are not. It is therefore only honest on a face where the two circles really are
# two different things the reader currently has to choose between. Do not use it to pair a thing
# with a restatement of itself.
#
# EVIDENCE WARNING. No face on this layout has a live cost. SOP/10's measured styles are pay
# chart (2.34x par, never use) and toon/chat (1.22x). This is a format test; judge it inside its
# own campaign.

def _venn(pal, s):
    SERIF, SANS = _fonts()
    ring = "3px solid #FFFFFF"
    return _base(pal, s) + [
        (".canvas", {"background": "linear-gradient(180deg, rgba(255,255,255,.02) 0%%, rgba(255,255,255,.34) 100%%), %s" % pal["accent"],
                     "color": "#FFFFFF", "text-align": "center"}),
        # 1. the ICP line. The reference has no audience line; this account requires one.
        (".callout", {"font-size": _idpx(66, s), "font-weight": "800", "line-height": "1.02",
                      "letter-spacing": "-.01em", "text-transform": "uppercase",
                      "color": "#FFFFFF", "text-wrap": "balance"}),
        # 2. the headline, the reference's own treatment: tall, condensed, one italic word
        (".head", {"font-size": _idpx(78, s), "font-weight": "700", "line-height": "1.04",
                   "letter-spacing": "-.02em", "text-transform": "uppercase",
                   "color": "#FFFFFF", "margin-top": _px(14, s), "text-wrap": "balance"}),
        (".head em", {"font-style": "italic", "font-weight": "700"}),
        # 3. the two circles
        (".venn", {"position": "relative", "width": "100%", "height": _px(560, s),
                   "margin-top": _px(26, s), "flex": "none"}),
        (".ring", {"position": "absolute", "top": "0", "width": _px(560, s),
                   "height": _px(560, s), "border": ring, "border-radius": "50%"}),
        (".ring.l", {"left": "0"}),
        (".ring.r", {"right": "0"}),
        (".vlab", {"position": "absolute", "top": "50%", "transform": "translateY(-50%)",
                   "width": _px(276, s), "font-size": _px(42, s), "font-weight": "700",
                   "line-height": "1.1", "letter-spacing": "-.01em",
                   "text-transform": "uppercase", "color": "#FFFFFF"}),
        (".vlab.l", {"left": _px(28, s)}),
        (".vlab.r", {"right": _px(28, s)}),
        # 4. the intersection: the camp itself, where the packshot sat
        (".lens", {"position": "absolute", "left": "50%", "top": "50%",
                   "transform": "translate(-50%,-50%)", "width": _px(248, s),
                   "background": "#FFFFFF", "color": pal["ink"],
                   "border-radius": _px(22, s),
                   "padding": "%s %s" % (_px(20, s), _px(14, s)),
                   "box-shadow": "0 18px 40px rgba(0,0,0,.20)"}),
        (".lens b", {"display": "block", "font-size": _px(58, s), "font-weight": "900",
                     "line-height": "1.06", "letter-spacing": "-.02em"}),
        (".lens span", {"display": "block", "font-size": _px(30, s), "font-weight": "800",
                        "color": pal["accent"], "margin-top": _px(6, s)}),
        # 5. the plain-words definition, kept off the reference but required by Rule 2
        (".def", {"font-size": _px(31, s), "font-weight": "600", "line-height": "1.3",
                  "color": "#FFFFFF", "margin-top": _px(22, s)}),
        (".deliver", {"font-size": _px(29, s), "font-weight": "700", "line-height": "1.32",
                      "color": "#FFFFFF", "margin-top": _px(12, s)}),
        # 6. the ask. The reference has none; every face here carries one.
        (".cta", {"display": "inline-block", "background": "#FFFFFF", "color": pal["accent"],
                  "font-size": _px(40, s), "font-weight": "900",
                  "letter-spacing": "-.01em", "border-radius": _px(60, s),
                  "padding": "%s %s" % (_px(20, s), _px(46, s)), "margin-top": _px(20, s)}),
        (".terms", {"font-size": _barpx(27, s), "font-weight": "800", "letter-spacing": ".06em",
                    "text-transform": "uppercase", "color": "#FFFFFF",
                    "margin-top": _px(12, s)}),
        # 7. the caption, the reference's "DM-01 Daily Multivitamin"
        (".cap", {"font-size": _px(28, s), "font-weight": "700", "letter-spacing": ".04em",
                  "color": "#FFFFFF", "margin-top": _px(16, s)}),
    ]


def _venn_shell(kit, ad, s):
    """extra: left, right, lens_top, lens_bot, deliver, terms_line, cap (all optional but
    `left` and `right` are the point of the layout).

    `callout` is the ICP line, `head` the headline with one <em> word, `left` and `right` the two
    things the reader currently has to choose between, and the lens is the camp."""
    x = ad.extra
    return (
        '<div class="grow"></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="venn">'
        '<div class="ring l"></div><div class="ring r"></div>'
        '<div class="vlab l">%s</div><div class="vlab r">%s</div>'
        '<div class="lens"><b>%s</b><span>%s</span></div>'
        '</div>'
        '%s%s'
        '<div><span class="cta">%s</span></div>'
        '<div class="terms">%s</div>'
        '<div class="cap">%s</div>'
        '<div class="grow"></div>'
        % (ad.callout, ad.head, x.get("left", ""), x.get("right", ""),
           x.get("lens_top", _plain(kit.brand)), x.get("lens_bot", ""),
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           ('<div class="deliver">%s</div>' % x["deliver"]) if x.get("deliver") else "",
           kit.cta, x.get("terms_line", ad.proof), x.get("cap", "")))


LAYOUTS["venn"] = (_venn, _venn_shell)
PROVENANCE["venn"] = (
    "DTC supplement static supplied in chat, 18 Sep 2026 (blue gradient, '1 CHEW THAT DOES "
    "BOTH', two outlined circles, packshot in the intersection)", "-",
    "The two circles carry two things the reader has to choose between today, and the camp "
    "sits where they meet. ICP line, definition, CTA and terms added: the reference is a "
    "brand static with no audience line and no ask. No live cost on this layout yet.")


# ---------------------------------------------------------------- alert
# Built 21 Sep 2026 from a DTC sunscreen static supplied in chat (flat-lay of bottles, centred
# alert dialog, "REMINDER / Don't Skip Your Sunscreen! / OKAY | GOT IT!"). See this module's
# docstring for what was taken, what changed, and the Meta policy line this layout stays behind.

def _alert(pal, s):
    SERIF, SANS = _fonts()
    return _base(pal, s) + [
        (".canvas", {"background": pal["accent"], "position": "relative",
                     "align-items": "center", "justify-content": "center"}),
        # the flat-lay: the camp's own artefacts, scattered and rotated behind the dialog
        (".lay", {"position": "absolute", "inset": "0", "overflow": "hidden"}),
        (".doc", {"position": "absolute", "background": pal["card"], "color": pal["ink"],
                  "border-radius": _px(14, s), "padding": "%s %s" % (_px(20, s), _px(22, s)),
                  "box-shadow": "0 20px 44px rgba(0,0,0,.16)"}),
        (".doc .t", {"font-size": _px(26, s), "font-weight": "900", "letter-spacing": ".08em",
                     "text-transform": "uppercase", "color": pal["accent"]}),
        (".doc .r", {"height": _px(9, s), "background": pal["line"], "border-radius": "99px",
                     "margin-top": _px(11, s)}),
        # the dialog
        (".dlg", {"position": "relative", "width": "78%", "background": pal["card"],
                  "border-radius": _px(30, s), "overflow": "hidden",
                  "box-shadow": "0 28px 70px rgba(0,0,0,.28)"}),
        (".dbody", {"padding": "%s %s %s" % (_px(40, s), _px(38, s), _px(34, s)),
                    "text-align": "center"}),
        (".callout", {"font-size": _idpx(64, s), "font-weight": "900", "line-height": "1.06",
                      "letter-spacing": "-.02em", "color": pal["accent"],
                      "text-transform": "uppercase", "text-wrap": "balance"}),
        (".head", {"font-size": _idpx(68, s), "font-weight": "700", "line-height": "1.14",
                   "letter-spacing": "-.02em", "color": pal["ink"], "margin-top": _px(18, s),
                   "text-wrap": "balance"}),
        (".head em", {"font-style": "italic", "font-weight": "800", "color": pal["accent"]}),
        (".dsub", {"font-size": _px(31, s), "font-weight": "600", "line-height": "1.3",
                   "color": pal["ink"], "margin-top": _px(16, s)}),
        (".dnote", {"font-size": _px(28, s), "font-weight": "800", "color": pal["accent"],
                    "margin-top": _px(16, s), "text-align": "center"}),
        # the button row: two cells and a divider, as on the reference, with the primary action
        # filled the way a real dialog marks its default. Neither cell is a dismissal.
        (".btns", {"display": "flex", "border-top": "2px solid " + pal["line"]}),
        (".btn", {"flex": "1", "text-align": "center", "font-size": _px(40, s),
                  "font-weight": "800", "color": pal["ink"], "padding": "%s 0" % _px(26, s)}),
        (".btn.go", {"background": pal["accent"], "color": "#FFFFFF", "font-weight": "900"}),
        # the artefacts carry what the three days produce. In the reference the ground holds the
        # product; here it holds the work, and each card says what it is.
        (".doc .s", {"font-size": _px(25, s), "font-weight": "600", "line-height": "1.24",
                     "color": pal["ink"], "margin-top": _px(8, s)}),
        (".terms", {"position": "relative", "font-size": _barpx(28, s), "font-weight": "800",
                    "letter-spacing": ".06em", "text-transform": "uppercase", "color": "#FFFFFF",
                    "margin-top": _px(26, s), "text-align": "center"}),
        (".cap", {"position": "relative", "font-size": _px(28, s), "font-weight": "700",
                  "color": "#FFFFFF", "margin-top": _px(12, s), "text-align": "center"}),
    ]


def _alert_shell(kit, ad, s):
    """extra: sub, note, btn_more, btn_go, docs, terms_line, cap.

    `docs` entries may write their label as "TITLE | one line of detail", which is how the
    take-aways reach the face without swelling the dialog.

    `callout` is the dialog title and carries the ICP. `head` is the one line the reader is meant
    to read. `docs` is a list of (label, left, top, width, rotation) for the flat-lay behind it,
    and falls back to the kit's takeaways so any kit renders."""
    x = ad.extra
    docs = x.get("docs") or [(t, l, t2, w, r) for t, (l, t2, w, r) in zip(
        [k.split(",")[0][:18] for k in kit.takeaways],
        [("-4%", "6%", "34%", "-13deg"), ("70%", "16%", "34%", "11deg"),
         ("2%", "70%", "32%", "9deg")])]
    lay = "".join(
        '<div class="doc" style="left:%s;top:%s;width:%s;transform:rotate(%s)">'
        '<div class="t">%s</div>%s</div>'
        % (l, t2, w, r, lbl.split("|")[0].strip(),
           ('<div class="s">%s</div>' % lbl.split("|")[1].strip()) if "|" in lbl else
           ('<div class="r" style="width:86%"></div><div class="r" style="width:64%"></div>'
            '<div class="r" style="width:74%"></div>'))
        for lbl, l, t2, w, r in docs)
    return (
        '<div class="lay">%s</div>'
        '<div class="dlg"><div class="dbody">'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '%s'
        '%s'
        '</div><div class="btns"><div class="btn">%s</div>'
        '<div class="btn go">%s</div></div></div>'
        '<div class="terms">%s</div>'
        '<div class="cap">%s</div>'
        % (lay, ad.callout, ad.head,
           ('<div class="dsub">%s</div>' % x["sub"]) if x.get("sub") else "",
           ('<div class="dnote">%s</div>' % x["note"]) if x.get("note") else "",
           x.get("btn_more", "What's in it"), x.get("btn_go", kit.cta),
           x.get("terms_line", ad.proof), x.get("cap", _plain(kit.brand))))


LAYOUTS["alert"] = (_alert, _alert_shell)
PROVENANCE["alert"] = (
    "DTC sunscreen static supplied in chat, 21 Sep 2026 (flat-lay of bottles, centred alert "
    "dialog, REMINDER / one line / two buttons)", "-",
    "A dialog is recognised before it is read, which is what the venn wave failed on in the "
    "skim test. The scattered objects are the camp's artefacts, the title carries the ICP and "
    "the right button is the real CTA. Deliberately not a system-UI copy: Meta disallows "
    "creative that imitates platform UI. No live cost yet.")


# ---------------------------------------------------------------- brief
# Built 21 Sep 2026 from the two corporate finance faces that beat par (cf_loan_consultant Rs 164,
# cf_cma Rs 170). See this module's docstring for the skeleton and what the refresh changes.

def _brief(pal, s):
    SERIF, SANS = _fonts()
    return _base(pal, s) + [
        (".canvas", {"background": pal["page"], "color": pal["ink"]}),
        (".rail", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between"}),
        (".brand", {"font-size": _px(34, s), "font-weight": "800", "letter-spacing": "-.01em"}),
        (".brand em", {"font-style": "normal", "color": pal["accent"]}),
        (".pill", {"border": "3px solid " + pal["accent"], "color": pal["accent"],
                   "font-size": _px(28, s), "font-weight": "900", "letter-spacing": ".04em",
                   "border-radius": "999px",
                   "padding": "%s %s" % (_px(10, s), _px(26, s))}),
        # 2. the ICP, as a question
        (".callout", {"font-size": _idpx(70, s), "font-weight": "900", "line-height": "1.06",
                      "letter-spacing": "-.025em", "margin-top": _px(26, s),
                      "text-wrap": "balance"}),
        (".callout em", {"font-style": "normal", "color": pal["accent"]}),
        # 3. the qualifier row
        (".elig", {"display": "flex", "flex-wrap": "wrap", "gap": _px(10, s),
                   "margin-top": _px(16, s)}),
        (".elig span", {"background": pal["card"], "border": "2px solid " + pal["line"],
                        "border-radius": "999px", "font-size": _px(25, s), "font-weight": "800",
                        "letter-spacing": ".06em", "text-transform": "uppercase",
                        "padding": "%s %s" % (_px(8, s), _px(18, s))}),
        # 4. the offer, in plain words
        (".head", {"font-size": _idpx(64, s), "font-weight": "900", "line-height": "1.1",
                   "letter-spacing": "-.02em", "color": pal["accent"],
                   "margin-top": _px(22, s), "text-wrap": "balance"}),
        (".head em", {"font-style": "italic"}),
        # 5. the definition, which is the step CLAUDE.md Rule 2 says is usually the missing one
        (".def", {"font-size": _px(32, s), "font-style": "italic", "line-height": "1.34",
                  "margin-top": _px(18, s)}),
        # 6. the offer block and the artefact
        (".cols", {"display": "flex", "gap": _px(26, s), "margin-top": _px(26, s),
                   "align-items": "flex-start"}),
        (".left", {"flex": "1.06"}),
        (".right", {"flex": "1"}),
        (".when", {"font-size": _px(34, s), "font-weight": "900", "color": pal["accent"],
                   "line-height": "1.18"}),
        (".tklabel", {"font-size": _px(31, s), "font-weight": "900", "margin-top": _px(14, s)}),
        (".ticks", {"margin-top": _px(10, s)}),
        (".ticks div", {"position": "relative", "font-size": _px(29, s), "font-weight": "700",
                        "line-height": "1.22", "padding-left": _px(44, s),
                        "margin-top": _px(14, s)}),
        (".ticks b", {"position": "absolute", "left": "0", "top": _px(2, s),
                      "width": _px(32, s), "height": _px(32, s), "border-radius": "50%",
                      "background": pal["accent"], "color": "#FFFFFF", "font-size": _px(20, s),
                      "display": "flex", "align-items": "center", "justify-content": "center"}),
        (".dev", {"background": pal["card"], "border": "2px solid " + pal["line"],
                  "border-radius": _px(20, s), "overflow": "hidden",
                  "box-shadow": "0 18px 40px rgba(0,0,0,.12)"}),
        (".dev .h", {"background": pal["ink"], "color": "#FFFFFF", "font-size": _px(28, s),
                     "font-weight": "900", "letter-spacing": ".06em",
                     "text-transform": "uppercase",
                     "padding": "%s %s" % (_px(14, s), _px(20, s))}),
        (".dev .row", {"display": "flex", "justify-content": "space-between", "gap": _px(14, s),
                       "font-size": _px(26, s), "font-weight": "700",
                       "padding": "%s %s" % (_px(12, s), _px(20, s)),
                       "border-top": "2px solid " + pal["line"]}),
        (".dev .row span:last-child", {"color": pal["accent"], "font-weight": "900",
                                       "white-space": "nowrap"}),
        (".dev .foot", {"background": pal["page"], "font-size": _px(25, s), "font-weight": "800",
                        "color": pal["ink"], "border-top": "2px solid " + pal["line"],
                        "padding": "%s %s" % (_px(12, s), _px(20, s))}),
        # 7. the ask
        (".ctabar", {"background": pal["accent"], "color": "#FFFFFF", "text-align": "center",
                     "margin": "%s -%spx 0" % (_px(26, s), _gutter()),
                     "padding": "%s %spx %s" % (_px(24, s), _gutter(), _px(20, s))}),
        (".ctabar .go", {"font-size": _px(46, s), "font-weight": "900",
                         "letter-spacing": "-.01em"}),
        (".terms", {"font-size": _barpx(27, s), "font-weight": "800", "margin-top": _px(8, s)}),
    ]


def _brief_shell(kit, ad, s):
    """extra: elig, when, deliver, ticks, dev_title, dev_rows, dev_foot, terms_line, pill.

    `callout` is the ICP question with the reader's title in <em>, `head` is the offer in plain
    words, `definition` is the "<field> means A, B and C" sentence, and the device is one artefact
    from the reader's own desk: a title, rows of (label, value), and a footer line."""
    x = ad.extra
    ticks = "".join('<div><b>&#10003;</b>%s</div>' % t
                    for t in (x.get("ticks") or kit.takeaways))
    rows = "".join('<div class="row"><span>%s</span><span>%s</span></div>' % r
                   for r in (x.get("dev_rows") or ()))
    return (
        '<div class="rail"><div class="brand">%s</div><div class="pill">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="elig">%s</div>'
        '<div class="head">%s</div>'
        '%s'
        '<div class="grow"></div>'
        '<div class="cols"><div class="left">'
        '<div class="when">%s</div><div class="tklabel">Key takeaways</div>'
        '<div class="ticks">%s</div></div>'
        '<div class="right"><div class="dev"><div class="h">%s</div>%s%s</div></div></div>'
        '<div class="grow"></div>'
        '<div class="ctabar"><div class="go">%s</div><div class="terms">%s</div></div>'
        % (kit.brand, x.get("pill", "LIVE"), ad.callout,
           "".join("<span>%s</span>" % e for e in (x.get("elig") or ())),
           ad.head,
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           x.get("when", ""), ticks,
           x.get("dev_title", ""), rows,
           ('<div class="foot">%s</div>' % x["dev_foot"]) if x.get("dev_foot") else "",
           kit.cta, x.get("terms_line", ad.proof)))


LAYOUTS["brief"] = (_brief, _brief_shell)
PROVENANCE["brief"] = (
    "CorporateFinance_MediaBuyer_15-17Aug faces 4_loan-consultant and 1_cost-accountant",
    "Rs 164 / Rs 170 per purchase, against a campaign par of Rs 193.94",
    "The only structure in this campaign with a live cost under par, and the first fold "
    "CLAUDE.md Rule 2 quotes. The refresh changes the surface - type scale, chip qualifiers, "
    "checked take-aways, a real artefact device, redrawn pill and CTA bar - and leaves the "
    "order of the seven elements alone.")


# ---------------------------------------------------------------- notify
# Built 21 Sep 2026: the sunscreen notification reference as the visual system, carrying the
# content skeleton of the two corporate finance faces that beat par (Rs 164, Rs 170).
# See this module's docstring for the mapping and the Meta policy line it stays behind.

def _notify(pal, s):
    return _base(pal, s) + [
        (".canvas", {"background": "linear-gradient(180deg, %s 0%%, %s 100%%)"
                     % (pal["page"], pal["card"]), "justify-content": "center"}),
        # the stack behind: the second and third notification, peeking
        (".stack2", {"background": pal["card"], "border": "2px solid " + pal["line"],
                     "border-radius": _px(30, s), "height": _px(40, s), "width": "92%",
                     "align-self": "center", "margin-bottom": "-%s" % _px(22, s)}),
        (".stack3", {"background": pal["card"], "border": "2px solid " + pal["line"],
                     "border-radius": _px(30, s), "height": _px(34, s), "width": "84%",
                     "align-self": "center", "margin-bottom": "-%s" % _px(18, s)}),
        # the notification itself
        (".note", {"background": "#FFFFFF", "border": "2px solid " + pal["line"],
                   "border-radius": _px(34, s), "overflow": "hidden",
                   "box-shadow": "0 26px 60px rgba(0,0,0,.14)"}),
        (".app", {"display": "flex", "align-items": "center", "gap": _px(14, s),
                  "padding": "%s %s %s" % (_px(20, s), _px(28, s), _px(6, s))}),
        (".tile", {"width": _px(52, s), "height": _px(52, s), "border-radius": _px(14, s),
                   "background": pal["accent"], "color": "#FFFFFF", "font-size": _px(26, s),
                   "font-weight": "900", "display": "flex", "align-items": "center",
                   "justify-content": "center", "flex": "none"}),
        (".appname", {"font-size": _px(26, s), "font-weight": "800", "letter-spacing": ".06em",
                      "text-transform": "uppercase", "color": pal["ink"], "flex": "1"}),
        (".now", {"font-size": _px(30, s), "font-weight": "800", "color": pal["accent"]}),
        (".nbody", {"padding": "%s %s %s" % (_px(4, s), _px(28, s), _px(24, s))}),
        (".callout", {"font-size": _idpx(64, s), "font-weight": "900", "line-height": "1.07",
                      "letter-spacing": "-.025em", "color": pal["ink"], "text-wrap": "balance"}),
        (".callout em", {"font-style": "normal", "color": pal["accent"]}),
        (".elig", {"display": "flex", "flex-wrap": "wrap", "gap": _px(8, s),
                   "margin-top": _px(14, s)}),
        (".elig span", {"background": pal["page"], "border-radius": "999px",
                        "font-size": _px(23, s), "font-weight": "800", "letter-spacing": ".05em",
                        "text-transform": "uppercase", "color": pal["ink"],
                        "padding": "%s %s" % (_px(7, s), _px(16, s))}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "800", "line-height": "1.1",
                   "letter-spacing": "-.02em", "color": pal["accent"], "margin-top": _px(18, s),
                   "text-wrap": "balance"}),
        (".def", {"font-size": _px(30, s), "line-height": "1.32", "color": pal["ink"],
                  "margin-top": _px(14, s)}),
        # the attachment: the artefact, as a rich notification would carry a preview
        (".att", {"border": "2px solid " + pal["line"], "border-radius": _px(18, s),
                  "overflow": "hidden", "margin-top": _px(20, s)}),
        (".att .h", {"background": pal["ink"], "color": "#FFFFFF", "font-size": _px(25, s),
                     "font-weight": "900", "letter-spacing": ".08em", "text-transform": "uppercase",
                     "padding": "%s %s" % (_px(11, s), _px(18, s))}),
        (".att .row", {"display": "flex", "justify-content": "space-between", "gap": _px(12, s),
                       "font-size": _px(26, s), "font-weight": "700", "color": pal["ink"],
                       "padding": "%s %s" % (_px(11, s), _px(18, s)),
                       "border-top": "2px solid " + pal["line"]}),
        (".att .row span:last-child", {"color": pal["accent"], "font-weight": "900",
                                       "white-space": "nowrap"}),
        # the meta line: information, deliberately not shaped like a control.
        # It is ONE sentence and must wrap as one. It was display:flex until 21 Sep 2026,
        # which made the text node and the <i> two independent flex items: each wrapped on
        # its own, stranding a separator at the end of the left column.
        (".meta", {"display": "block", "line-height": "1.34",
                   "font-size": _px(30, s), "font-weight": "800", "letter-spacing": ".04em",
                   "text-transform": "uppercase", "color": pal["ink"], "margin-top": _px(18, s)}),
        (".meta i", {"font-style": "normal", "color": pal["accent"]}),
        # one action, full width. Nothing beside it to click instead.
        (".acts", {"display": "flex", "border-top": "2px solid " + pal["line"]}),
        (".act", {"flex": "1", "text-align": "center", "font-size": _px(42, s),
                  "font-weight": "900", "background": pal["accent"], "color": "#FFFFFF",
                  "letter-spacing": "-.01em", "padding": "%s 0" % _px(26, s)}),
        (".terms", {"text-align": "center", "font-size": _barpx(27, s), "font-weight": "800",
                    "letter-spacing": ".05em", "text-transform": "uppercase", "color": pal["ink"],
                    "margin-top": _px(24, s)}),
        (".cap", {"text-align": "center", "font-size": _px(26, s), "font-weight": "700",
                  "color": pal["ink"], "margin-top": _px(10, s)}),
    ]


def _notify_shell(kit, ad, s):
    """extra: elig, tile, now, att_title, att_rows, meta, act_go, terms_line, cap.

    `callout` is the ICP as a question with the reader's title in <em>, `head` is the offer in
    plain words, `definition` is the "<field> means A, B and C" sentence, and the attachment
    carries the take-aways as label/value rows from the reader's own desk."""
    x = ad.extra
    rows = "".join('<div class="row"><span>%s</span><span>%s</span></div>' % r
                   for r in (x.get("att_rows") or ()))
    return (
        '<div class="grow"></div>'
        '<div class="stack3"></div><div class="stack2"></div>'
        '<div class="note">'
        '<div class="app"><div class="tile">%s</div>'
        '<div class="appname">%s</div><div class="now">%s</div></div>'
        '<div class="nbody">'
        '<div class="callout">%s</div>'
        '<div class="elig">%s</div>'
        '<div class="head">%s</div>'
        '%s'
        '<div class="att"><div class="h">%s</div>%s</div>'
        '%s'
        '</div>'
        '<div class="acts"><div class="act">%s</div></div>'
        '</div>'
        '<div class="terms">%s</div>'
        '<div class="cap">%s</div>'
        '<div class="grow"></div>'
        % (x.get("tile", "SA"), x.get("appname", kit.eyebrow), x.get("now", "now"),
           ad.callout,
           "".join("<span>%s</span>" % e for e in (x.get("elig") or ())),
           ad.head,
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           x.get("att_title", ""), rows,
           ('<div class="meta">%s</div>' % x["meta"]) if x.get("meta") else "",
           x.get("act_go", kit.cta),
           x.get("terms_line", ad.proof), x.get("cap", _plain(kit.brand))))


LAYOUTS["notify"] = (_notify, _notify_shell)
PROVENANCE["notify"] = (
    "DTC sunscreen static supplied in chat, 21 Sep 2026 (flat ground, centred notification "
    "dialog, two-cell action row), carrying the content skeleton of "
    "CorporateFinance_MediaBuyer_15-17Aug 4_loan-consultant and 1_cost-accountant",
    "structure priced at Rs 164 and Rs 170 against a Rs 193.94 par",
    "The refresh is the notification; the content is the one that beat par. Take-aways ride "
    "in the attachment card, the qualifier row becomes notification chips, and the primary "
    "action is filled. No live cost on this surface yet.")


# ---------------------------------------------------------------- call
# Built 21 Sep 2026 for the LawSikho Data Protection 17-19 Oct wave, from an AG1 static
# supplied in chat ("Your immune system / rings ..." over a photo, one "Accept" slider). The
# idea, in Ruchika's words: "they are getting a call from a better opportunity".
#
# What was taken: the incoming-call composition. Everything centred, the caller's name as
# the hero, a small "is calling ..." line under it, and ONE slide-to-act pill at the foot.
#
# What was changed, and why:
#   - The AG1 slider is iOS's answer control: a green phone glyph and a fake "Accept". House
#     rule (SOP/10): "Creative must not imitate platform or system UI in a misleading way: no
#     status bar, no platform glyphs, no fake close control, brand colours throughout, and
#     the only control-looking element is the real CTA." So the knob carries an arrow in the
#     brand accent, never a phone, and the pill's label IS the CTA ("Join for Rs 10"). No
#     Decline button: one action only.
#   - AG1 carries two lines of text because its brand and product are already known. The
#     alert layout was killed on 21 Sep for "so much information is missing from the ad",
#     and a visual refresh must carry the priced face's content (feedback_notify_layout). So
#     the ICP comes first as .callout, the caller's name is the winning headline as .head,
#     and a caller card carries the definition and the take-aways as label/value rows.
#   - Centred throughout. simplicity L1 fires only on competing LEFT edges when most blocks
#     are not centred, so a fully centred face passes by construction.
#   - No opacity anywhere (banned in layouts). The chip fill is a SOLID mix of the accent
#     toward white, computed here, so no text or fill is faded.

def _mix(a, b, t):
    """Solid colour t of the way from hex a to hex b."""
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(ca, cb))


def _call(pal, s):
    chip = _mix(pal["accent"], "#FFFFFF", 0.20)
    ring = _mix(pal["accent"], "#FFFFFF", 0.32)
    return _base(pal, s) + [
        (".canvas", {"background": "linear-gradient(180deg, %s 0%%, %s 100%%)"
                     % (pal["accent"], pal["ink"]), "color": "#FFFFFF",
                     "align-items": "center", "text-align": "center"}),
        (".rail", {"font-size": _px(25, s), "font-weight": "800", "letter-spacing": ".08em",
                   "text-transform": "uppercase", "color": pal["line"]}),
        # The reader's title must be the BRIGHTEST words on the face. On the notify layout
        # the highlight was dark accent on white and popped; on this dark ground the same
        # rule inverts, and a light-tint <em> read as de-emphasis (first render, 21 Sep).
        # So the question sits in the light tint and the title in full white.
        (".callout", {"font-size": _idpx(64, s), "font-weight": "900", "line-height": "1.08",
                      "letter-spacing": "-.02em", "color": pal["line"], "text-wrap": "balance",
                      "margin-top": _px(22, s)}),
        (".callout em", {"font-style": "normal", "color": "#FFFFFF"}),
        (".elig", {"display": "flex", "flex-wrap": "wrap", "justify-content": "center",
                   "gap": _px(8, s), "margin-top": _px(16, s)}),
        (".elig span", {"background": chip, "border-radius": "999px", "color": "#FFFFFF",
                        "font-size": _px(22, s), "font-weight": "800", "letter-spacing": ".05em",
                        "text-transform": "uppercase",
                        "padding": "%s %s" % (_px(7, s), _px(16, s))}),
        # the caller: a brand monogram in a ringed circle, never a platform glyph
        (".avatar", {"width": _px(112, s), "height": _px(112, s), "border-radius": "50%",
                     "background": pal["line"], "color": pal["accent"],
                     "box-shadow": "0 0 0 %s %s" % (_px(10, s), ring),
                     "display": "flex", "align-items": "center", "justify-content": "center",
                     "font-size": _px(40, s), "font-weight": "900", "flex": "none",
                     "margin-top": _px(28, s)}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "800", "line-height": "1.08",
                   "letter-spacing": "-.02em", "color": "#FFFFFF", "text-wrap": "balance",
                   "margin-top": _px(22, s)}),
        (".ring", {"font-size": _px(34, s), "font-weight": "600", "color": pal["line"],
                   "margin-top": _px(8, s)}),
        # the caller card: what the call is about. White, so it reads as the one detail panel.
        (".card", {"width": "100%", "background": pal["card"], "color": pal["ink"],
                   "border-radius": _px(24, s), "margin-top": _px(26, s), "text-align": "left"}),
        (".card .def", {"font-size": _px(27, s), "line-height": "1.32", "color": pal["ink"],
                        "padding": "%s %s %s" % (_px(18, s), _px(24, s), _px(4, s))}),
        (".card .h", {"font-size": _px(23, s), "font-weight": "900", "letter-spacing": ".08em",
                      "text-transform": "uppercase", "color": pal["accent"],
                      "padding": "%s %s %s" % (_px(12, s), _px(24, s), _px(4, s))}),
        (".card .row", {"display": "flex", "justify-content": "space-between",
                        "gap": _px(12, s), "font-size": _px(26, s), "font-weight": "700",
                        "color": pal["ink"], "padding": "%s %s" % (_px(10, s), _px(24, s)),
                        "border-top": "2px solid " + pal["line"]}),
        (".card .row span:last-child", {"color": pal["accent"], "font-weight": "900",
                                        "white-space": "nowrap"}),
        (".card .pad", {"height": _px(8, s)}),
        # Optional skill bridge (extra=dict(bridge=[(now, privacy), ...], bridge_title=...)), added
        # 22 Sep 2026: "the ads are generally still not clear on how say my skills as a bank
        # executive or product manager are transferrable to a data privacy career". Two rows,
        # the reader's current task on the left, the privacy task it becomes on the right. When
        # present it replaces the definition line; the page keeps the definition.
        (".card .brow", {"font-size": _px(31, s), "line-height": "1.25",
                         "padding": "%s %s" % (_px(10, s), _px(24, s)),
                         "border-top": "1px solid " + pal["line"]}),
        (".card .brow .bn", {"font-weight": "800", "color": pal["ink"], "display": "block"}),
        (".card .brow .ba", {"font-weight": "900", "color": pal["accent"],
                             "margin-right": _px(8, s)}),
        (".card .brow .bp", {"font-weight": "800", "color": pal["accent"]}),
        # Labelled two-column bridge (extra=dict(bridge_cols=(now_label, privacy_label))), 22 Sep:
        # "there has to be some indication of what you do now and how it translates to data
        # privacy work, not just an arrow".
        (".card .bgrid", {"display": "grid", "grid-template-columns": "1fr 1.25fr",
                          "column-gap": _px(18, s), "padding": "%s %s" % (_px(6, s), _px(24, s))}),
        (".card .bgrid .bl", {"font-size": _px(19, s), "font-weight": "900",
                              "letter-spacing": ".08em", "text-transform": "uppercase",
                              "color": pal["accent"], "padding": "%s 0" % _px(6, s)}),
        (".card .bgrid .bn", {"font-size": _px(29, s), "font-weight": "800", "color": pal["ink"],
                              "line-height": "1.25", "padding": "%s 0" % _px(9, s),
                              "border-top": "1px solid " + pal["line"]}),
        (".card .bgrid .bp", {"font-size": _px(29, s), "font-weight": "800",
                              "color": pal["accent"], "line-height": "1.25",
                              "padding": "%s 0" % _px(9, s),
                              "border-top": "1px solid " + pal["line"]}),
        # Optional one-line offer (extra=dict(offer_line=...)), 22 Sep 2026: "condense what the
        # camp offers into one line". Replaces the take-away table when present.
        (".card .offer", {"font-size": _px(29, s), "font-weight": "800", "line-height": "1.3",
                          "color": pal["ink"], "padding": "%s %s" % (_px(12, s), _px(24, s)),
                          "border-top": "2px solid " + pal["line"], "background": pal["page"]}),
        # the one action: a slide-to-act pill in brand colours. The label is the real CTA and
        # is centred in the space to the RIGHT of the knob, which is where the eye expects a
        # slider's label. The notify wave's CTA defect was a label sitting off-centre.
        (".pill", {"width": "100%", "background": "#FFFFFF", "border-radius": "999px",
                   "display": "flex", "align-items": "center", "margin-top": _px(28, s),
                   "padding": _px(12, s), "flex": "none"}),
        (".knob", {"width": _px(88, s), "height": _px(88, s), "border-radius": "50%",
                   "background": pal["accent"], "color": "#FFFFFF", "flex": "none",
                   "display": "flex", "align-items": "center", "justify-content": "center",
                   "font-size": _px(44, s), "font-weight": "900"}),
        (".go", {"flex": "1", "text-align": "center", "font-size": _px(42, s),
                 "font-weight": "900", "color": pal["accent"], "letter-spacing": "-.01em",
                 "padding-right": _px(88, s)}),
        (".terms", {"font-size": _barpx(26, s), "font-weight": "800", "letter-spacing": ".05em",
                    "text-transform": "uppercase", "color": pal["line"],
                    "margin-top": _px(18, s)}),
    ]


def _call_shell(kit, ad, s):
    """extra: rail, elig, mono, ring, att_title, att_rows, act_go, terms_line.

    `callout` is the ICP as a question with the reader's title in <em>; `head` is the caller,
    the winning headline; `definition` opens the caller card; the take-aways ride as
    label/value rows beneath it."""
    x = ad.extra
    rows = "".join('<div class="row"><span>%s</span><span>%s</span></div>' % r
                   for r in (x.get("att_rows") or ()))
    return (
        '<div class="rail">%s</div>'
        '<div class="callout">%s</div>'
        '<div class="elig">%s</div>'
        '<div class="grow"></div>'
        '<div class="avatar">%s</div>'
        '<div class="head">%s</div>'
        '<div class="ring">%s</div>'
        '<div class="card">%s%s%s<div class="pad"></div></div>'
        '<div class="grow"></div>'
        '<div class="pill"><div class="knob">&#8594;</div><div class="go">%s</div></div>'
        '<div class="terms">%s</div>'
        % (x.get("rail", kit.eyebrow), ad.callout,
           "".join("<span>%s</span>" % e for e in (x.get("elig") or ())),
           x.get("mono", "LS"), ad.head, x.get("ring", "is calling&#8230;"),
           (('<div class="h">%s</div>' % x.get("bridge_title", "Your skills, in data privacy"))
            + (('<div class="bgrid"><div class="bl">%s</div><div class="bl">%s</div>%s</div>'
                % (x["bridge_cols"][0], x["bridge_cols"][1], "".join(
                    '<div class="bn">%s</div><div class="bp">%s</div>' % r for r in x["bridge"])))
               if x.get("bridge_cols") else
               "".join('<div class="brow"><span class="bn">%s</span><span class="ba">&#8594;</span>'
                       '<span class="bp">%s</span></div>' % r for r in x["bridge"])))
           if x.get("bridge") else
           (('<div class="def">%s</div>' % ad.definition) if ad.definition else ""),
           "" if x.get("offer_line") else
           '<div class="h">%s</div>' % x.get("att_title", "What the call is about"),
           ('<div class="offer">%s</div>' % x["offer_line"]) if x.get("offer_line") else rows,
           x.get("act_go", kit.cta), x.get("terms_line", ad.proof)))


LAYOUTS["call"] = (_call, _call_shell)
PROVENANCE["call"] = (
    "AG1 static supplied in chat, 21 Sep 2026 (incoming-call composition over a photo, one "
    "slide-to-accept pill), carrying the content of the DPDP faces that beat par: "
    "dpdp_wave2_firm_associates Rs 97, side_practice Rs 115, litigators Rs 116, "
    "data_analysts Rs 117, transcription_rcm Rs 122 (GST incl., par Rs 144)",
    "content priced at 0.67x to 0.85x DPDP par on n=76 to 325",
    "The refresh is the incoming call from a better opportunity; the content is the one that "
    "beat par. Brand colours, an arrow knob and the real CTA as the pill's label keep it "
    "behind the SOP/10 line on imitating system UI. No live cost on this surface yet.")


# ---------------------------------------------------------------- translate
# Built 22 Sep 2026 for the Academic Writing 24-26 Oct wave, from a reference Ruchika
# supplied in chat: a lifestyle photo (a woman in a wine blazer holding tea) with a
# translator card over it, "What I say" -> "What it means", the right panel a darker
# tile carrying the real meaning.
#
# What was taken: the two-label translator card. The left panel is the reader's own
# life in plain words, the right panel is what that same skill is worth, on a darker
# tile - so the face reads as a before and after with no diagram, and the value
# proposition (Ruchika, 22 Sep: "make more money, utilise your skillset") is the thing
# the card translates INTO.
#
# What was changed, and why:
#   - No dropdown chevrons, no swap button, no microphone, speaker, copy or close glyphs.
#     SOP/10: no fake close control, no platform glyphs, the only control-looking element
#     is the real CTA. The labels are plain tabs and the swap is a printed arrow.
#   - The reference names nobody. This account names the ICP first, always, so the
#     call-out band sits above the card, and the head (the value line) sits between.
#   - The photo is optional (extra["photo"], from the kit's photos/ folder). With no
#     photo the ground is the palette page colour, never a drawn illustration.
#   - No opacity anywhere (banned in layouts): tints are solid mixes.

def _translate(pal, s):
    # v3, 22 Sep 2026. v2 stacked the card to fix space and lost the device: "now the
    # translate layout is gone". The side-by-side translator IS the reference - two tabs
    # joined by a swap mark, two panes beneath them - so v3 puts it back and keeps v2's
    # fixes inside it:
    #   - COLOUR: clean warm-white ground, ONE deep accent, the payoff pane a white tile
    #     (the reference's right tile is the lit one).
    #   - READABILITY: both panes bold at 40px+, chips at full-strength accent.
    #   - SPACE: v1's panes were content-height, so the short left pane left a dead corner.
    #     Panes now stretch to one shared height and the card is sized to fill the face.
    #   - The swap mark is printed text, not a button; no chevrons, mic, speaker or close
    #     glyphs (SOP/10: the only control-looking element is the real CTA).
    tint = _mix(pal["accent"], "#FFFFFF", 0.88)
    tabline = _mix(pal["accent"], "#FFFFFF", 0.55)
    return _base(pal, s) + [
        (".canvas", {"background": pal["page"]}),
        (".rail", {"display": "flex", "justify-content": "space-between",
                   "font-size": _px(24, s), "font-weight": "800", "letter-spacing": ".08em",
                   "text-transform": "uppercase", "color": pal["accent"]}),
        (".callout", {"font-size": _idpx(66, s), "font-weight": "900", "line-height": "1.04",
                      "letter-spacing": "-.005em", "text-transform": "uppercase",
                      "color": "#FFFFFF", "background": pal["accent"], "align-self": "flex-start",
                      "padding": "%s %s" % (_px(12, s), _px(24, s)), "margin-top": _px(30, s),
                      "border-radius": _px(8, s)}),
        (".head", {"font-size": _idpx(76, s), "font-weight": "900", "line-height": "1.04",
                   "letter-spacing": "-.025em", "color": pal["ink"],
                   # "pretty", not "balance": balance evened a 7-word head into three short
                   # lines and left the right third of the face empty ("why is the heading
                   # entirely left aligned?", 22 Sep 2026).
                   "text-wrap": "pretty", "margin-top": _px(24, s)}),
        (".photo", {"margin-top": _px(24, s), "border-radius": _px(22, s), "overflow": "hidden",
                    "height": _px(300, s), "flex": "none"}),
        (".photo img", {"width": "100%", "height": "100%", "object-fit": "cover",
                        "display": "block"}),
        # the translator card
        (".tr", {"background": pal["accent"], "border-radius": _px(28, s), "color": "#FFFFFF",
                 "padding": _px(26, s), "margin-top": _px(32, s), "flex": "none",
                 "display": "flex", "flex-direction": "column"}),
        (".tr .tabs", {"display": "flex", "align-items": "center", "gap": _px(12, s)}),
        (".tr .tab", {"flex": "1", "border": "2px solid " + tabline,
                      "border-radius": _px(12, s), "font-size": _px(28, s),
                      "font-weight": "800", "color": "#FFFFFF",
                      "padding": "%s %s" % (_px(12, s), _px(18, s))}),
        (".tr .swap", {"font-size": _px(40, s), "font-weight": "900", "color": "#FFFFFF",
                       "flex": "none", "line-height": "1"}),
        (".tr .panes", {"display": "flex", "align-items": "stretch", "gap": _px(14, s),
                        "margin-top": _px(16, s), "min-height": _px(390, s)}),
        (".tr .pane", {"flex": "1", "border-radius": _px(18, s),
                       "padding": "%s %s" % (_px(26, s), _px(22, s)),
                       "display": "flex", "flex-direction": "column"}),
        (".tr .now", {"font-size": _px(44, s), "font-weight": "800", "line-height": "1.16",
                      "color": "#FFFFFF"}),
        (".tr .worth", {"background": pal["card"], "color": pal["ink"]}),
        (".tr .worth .big", {"font-size": _px(44, s), "font-weight": "900",
                             "line-height": "1.12", "letter-spacing": "-.01em",
                             "color": pal["ink"]}),
        (".tr .chips", {"display": "flex", "flex-direction": "column", "gap": _px(8, s),
                        "margin-top": "auto", "padding-top": _px(18, s)}),
        (".tr .chips span", {"background": tint, "color": pal["accent"],
                             "border-radius": _px(10, s), "font-size": _px(27, s),
                             "font-weight": "800",
                             "padding": "%s %s" % (_px(8, s), _px(14, s))}),
        # v3b: the left pane carries its own chip column - the reader's everyday tasks -
        # so each row on the left translates to the row beside it on the right. It fills
        # the dead lower half of the left pane with content, not a spacer.
        (".tr .nowchips span", {"background": _mix(pal["accent"], "#FFFFFF", 0.16),
                                "color": "#FFFFFF"}),

        (".def", {"font-size": _px(28, s), "line-height": "1.34", "color": pal["ink"],
                  "margin-top": _px(20, s)}),
        (".deliver", {"font-size": _px(33, s), "line-height": "1.3", "font-weight": "600",
                      "color": pal["ink"], "margin-top": _px(26, s)}),
        (".offer", {"font-size": _px(40, s), "font-weight": "900", "line-height": "1.15",
                    "color": pal["accent"], "letter-spacing": "-.01em",
                    "margin-top": _px(22, s)}),
        (".btn", {"background": pal["accent"], "color": "#FFFFFF", "border-radius": "999px",
                  "text-align": "center", "font-size": _px(40, s), "font-weight": "900",
                  "padding": "%s %s" % (_px(22, s), _px(24, s)), "margin-top": _px(16, s),
                  "flex": "none"}),
        (".terms", {"font-size": _barpx(26, s), "font-weight": "800", "letter-spacing": "0",
                    "white-space": "nowrap", "text-transform": "uppercase", "color": pal["ink"],
                    "text-align": "center", "margin-top": _px(16, s)}),
        # Ink, not accent: the benefit is the strongest line after the head, and
        # the delivery line under it was competing in the same colour.
        (".benefit", {"font-size": _px(34, s), "font-weight": "800",
                      "line-height": "1.26", "margin-top": _px(10, s),
                      "color": pal["ink"]}),
        (".benefit em", {"font-style": "normal", "color": pal["accent"]}),
    ]


def _translate_shell(kit, ad, s):
    """extra: rail_l, rail_r, photo, tab_now, tab_worth, now, now_sub, worth, worth_sub (a list of
    chips, or one string), deliver, offer, terms_line.

    `callout` is the ICP; `head` is the value line; the card translates `now` (the
    reader's life, in their words) into `worth` (the paid work) on a white tile beside it,
    with the deliverables as chips at the tile's foot."""
    x = ad.extra
    photo = ('<div class="photo"><img src="../photos/%s" alt=""></div>' % x["photo"]
             if x.get("photo") else "")
    sub = x.get("worth_sub") or ()
    if isinstance(sub, str):
        sub = (sub,)
    chips = ('<div class="chips">%s</div>' % "".join("<span>%s</span>" % c for c in sub)
             if sub else "")
    nsub = x.get("now_sub") or ()
    nchips = ('<div class="chips nowchips">%s</div>'
              % "".join("<span>%s</span>" % c for c in nsub) if nsub else "")
    return (
        '<div class="rail"><span>%s</span><span>%s</span></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '%s%s'
        '<div class="tr"><div class="tabs"><div class="tab">%s</div>'
        '<div class="swap">&#8646;</div><div class="tab">%s</div></div>'
        '<div class="panes"><div class="pane"><div class="now">%s</div>%s</div>'
        '<div class="pane worth"><div class="big">%s</div>%s</div></div></div>'
        '%s%s'
        '<div class="grow"></div>'
        '<div class="offer">%s</div>'
        '<div class="btn">%s</div>'
        '<div class="terms">%s</div>'
        % (x.get("rail_l", kit.brand), x.get("rail_r", kit.eyebrow), ad.callout, ad.head,
           # What the reader KEEPS, as its own line under the head. Added 23 Sep
           # 2026 with the same slot on `photo`: the faces named the move and the
           # deliverables and never the benefit.
           ('<div class="benefit">%s</div>' % x["benefit"]) if x.get("benefit") else "",
           photo, x.get("tab_now", "What you do now"), x.get("tab_worth", "What it is worth"),
           x.get("now", ""), nchips, x.get("worth", ""), chips,
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           ('<div class="deliver">%s</div>' % x["deliver"]) if x.get("deliver") else "",
           x.get("offer", ""), kit.cta, x.get("terms_line", kit.terms)))


LAYOUTS["translate"] = (_translate, _translate_shell)
PROVENANCE["translate"] = (
    "Translator-card lifestyle static supplied in chat, 22 Sep 2026 ('What I say' -> "
    "'What it means' over a photo), carrying the Academic Writing 24-26 Oct hooks",
    "-",
    "The reader's own life in the left panel, the paid version of the same skill on the "
    "darker right tile. Plain tabs and a printed arrow, no dropdowns or player glyphs, to "
    "stay behind the SOP/10 line on imitating UI. No live cost on this layout yet.")


# ---------------------------------------------------------------- calendar
# Scaffolded 23 Sep 2026 from: Calendar week UI supplied in chat, 23 Sep 2026: day strip with today circled, hour rows, one coloured event block
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _calendar(pal, s):
    """The reader's own week. Built 23 Sep 2026 from a calendar-UI static supplied
    in chat (day strip, hour rows, one coloured event block).

    WHAT IT TAKES FROM THE REFERENCE. The day strip with one day circled, the hour
    rows with their times down the left, and a single coloured event block that is
    the only thing worth reading in the grid.

    WHAT IT DELIBERATELY DOES NOT TAKE. The reference is a mood board: a food
    photograph, cutlery stickers and sunglasses scattered over twelve empty hours.
    All of it is decoration, and twelve hour rows would shrink the device until the
    event line is unreadable. Four rows, one event, nothing loose on top.

    WHY IT IS BEHIND THE SOP/10 FAKE-UI LINE. The grid carries no control the reader
    could try to press: no button, no chip, no checkbox. The only control-looking
    element on the face is the real CTA. Same line the `call` and `notify` layouts
    stay behind.

    ONLY FOR READERS WHOSE STORY IS TIME - evenings, school hours, an empty week
    after a break. For anyone else the device says nothing the headline does not,
    and the priced `serif` block beats it.

    TWO MODES, NEVER MIXED (23 Sep 2026, Ruchika: "the rows and columns both have
    days in the calendar, which is the error"). The first build drew the Mon to Sun
    strip on every face while half the faces used days as row labels too, so the
    grid claimed two axes of days and read as nothing:
      mode "day"   the strip is drawn, one day circled, and every row is a time.
      mode "week"  NO strip at all, and every row is a day. The caption carries the
                   span instead.

    Data comes from extra["mode"], extra["days"] (7 labels, one prefixed with * for
    the circled day, day mode only), extra["date_line"], and extra["slots"] as
    "WHEN | text" strings, where a row prefixed with * is the accent event.
    """
    SERIF, _ = _fonts()
    tint = _mix(pal["accent"], "#FFFFFF", 0.90)
    rule = _mix(pal["accent"], "#FFFFFF", 0.72)
    return _base(pal, s) + [
        (".canvas", {"background": pal["page"]}),
        (".rail", {"display": "flex", "justify-content": "space-between",
                   "font-size": _px(24, s), "font-weight": "800", "letter-spacing": ".08em",
                   "text-transform": "uppercase", "color": pal["accent"]}),
        (".callout", {"background": pal["accent"], "color": "#FFFFFF",
                      "font-size": _idpx(64, s), "font-weight": "900", "line-height": "1.06",
                      "letter-spacing": "-.015em", "text-transform": "uppercase",
                      "align-self": "flex-start", "margin-top": _px(26, s),
                      "padding": "%s %s %s" % (_px(14, s), _px(24, s), _px(18, s))}),
        (".head", {"font-family": SERIF, "font-size": _idpx(70, s), "font-weight": "700",
                   "line-height": "1.08", "letter-spacing": "-.02em", "color": pal["ink"],
                   "margin-top": _px(26, s)}),
        (".head em", {"font-style": "italic", "font-weight": "700", "color": pal["accent"]}),
        # the device
        (".cal", {"background": "#FFFFFF", "border": "%s solid %s" % (_px(2, s), rule),
                  "border-radius": _px(18, s), "margin-top": _px(28, s),
                  "overflow": "hidden"}),
        (".days", {"display": "flex", "border-bottom": "%s solid %s" % (_px(2, s), rule),
                   "padding": "%s %s" % (_px(16, s), _px(10, s))}),
        (".day", {"flex": "1", "text-align": "center", "font-size": _px(26, s),
                  "font-weight": "700", "color": pal["ink"]}),
        (".day b", {"display": "block", "font-size": _px(30, s), "font-weight": "800",
                    "margin-top": _px(4, s)}),
        (".day.on b", {"background": pal["ink"], "color": "#FFFFFF", "border-radius": "999px",
                       "width": _px(46, s), "height": _px(46, s), "line-height": _px(46, s),
                       "margin": "%s auto 0" % _px(4, s)}),
        (".dateline", {"text-align": "center", "font-size": _px(30, s), "font-weight": "800",
                       "color": pal["ink"], "padding": "%s 0" % _px(14, s),
                       "border-bottom": "%s solid %s" % (_px(2, s), rule)}),
        # Two blocks, not four events (Ruchika, 23 Sep: "it can be as simple as two blocks").
        # So each block is given real height rather than leaving a void under a short card,
        # and the when-column is wide enough for a span like "Mon to Wed" on one line.
        (".slot", {"display": "flex", "align-items": "center",
                   "border-bottom": "%s solid %s" % (_px(2, s), rule),
                   "padding": "%s %s" % (_px(34, s), _px(22, s))}),
        (".slot:last-child", {"border-bottom": "none"}),
        # extra["fill"]: a face whose headline runs short leaves the spare height in .grow,
        # which showed as an empty band between the delivery line and the offer (ID calendar
        # wave, 28 Sep 2026: id36 and id39 beside seven fuller faces). Opt-in, so the rows
        # take four fifths of the spare height and the band keeps one fifth; faces with no
        # spare height do not move.
        (".cal.fill", {"flex": "4 1 auto", "display": "flex", "flex-direction": "column",
                       "min-height": "0"}),
        (".cal.fill .slot", {"flex": "1 1 auto"}),
        (".hr", {"width": _px(168, s), "flex": "none", "font-size": _px(28, s),
                 "font-weight": "700", "color": pal["ink"]}),
        # a long span ("Weeks 1 and 2", "Mon and Tue") wrapped to two lines and threw the
        # row's baseline out, so the shell widens the column when any label needs it
        (".cal.wide .hr", {"width": _px(250, s)}),
        (".ev", {"flex": "1", "font-size": _px(30, s), "font-weight": "700",
                 "color": pal["ink"], "padding": "%s %s" % (_px(12, s), _px(16, s)),
                 "border-radius": _px(8, s)}),
        # the one block worth reading: accent bar, accent ground, never faded type
        (".slot.on .ev", {"background": tint, "color": pal["accent"], "font-weight": "800",
                          "border-left": "%s solid %s" % (_px(8, s), pal["accent"])}),
        (".def", {"font-size": _px(30, s), "line-height": "1.36", "color": pal["ink"],
                  "margin-top": _px(26, s)}),
        (".deliver", {"font-size": _px(31, s), "line-height": "1.32", "font-weight": "600",
                      "color": pal["ink"], "margin-top": _px(22, s)}),
        # extra["deliver_big"]: the line under the calendar at reading size. Asked for on the
        # ID calendar wave, 28 Sep 2026 ("the text below the calendar can be enlarged so that
        # it is easier to read"), once that line was cut to 18 words. Opt-in, so the shipped
        # HR calendar faces, whose line runs three rows at 31px, do not move on a rebuild.
        (".deliver.big", {"font-size": _px(38, s), "line-height": "1.28", "font-weight": "700",
                          "text-wrap": "balance"}),
        (".offer", {"font-size": _px(38, s), "font-weight": "900", "line-height": "1.15",
                    "letter-spacing": "-.01em", "color": pal["accent"],
                    "margin-top": _px(22, s)}),
        (".btn", {"background": pal["accent"], "color": "#FFFFFF", "border-radius": "999px",
                  "text-align": "center", "font-size": _px(40, s), "font-weight": "900",
                  "padding": "%s %s" % (_px(22, s), _px(24, s)), "margin-top": _px(16, s)}),
        (".terms", {"font-size": _px(26, s), "font-weight": "800", "letter-spacing": ".04em",
                    "text-transform": "uppercase", "color": pal["ink"],
                    "margin-top": _px(16, s), "white-space": "nowrap"}),
    ]


def _calendar_shell(kit, ad, s):
    """extra: rail_l, rail_r, days (7 labels, "*" marks the circled day), date_line,
    slots ("TIME | text", "*" marks the accent event), deliver, offer, terms_line."""
    x = ad.extra
    # week mode drops the strip entirely: its rows already carry the days.
    cells = []
    if x.get("mode", "day") == "day":
        days = x.get("days") or ("M 27", "Tu 28", "W 29", "Th 30", "F 31", "Sa 1", "*Su 2")
        for d in days:
            on = d.startswith("*")
            lab, _, num = d.lstrip("*").partition(" ")
            cells.append('<div class="day%s">%s<b>%s</b></div>'
                         % (" on" if on else "", lab, num))
    rows = []
    for sl in (x.get("slots") or ()):
        on = sl.startswith("*")
        when, _, what = sl.lstrip("*").partition("|")
        rows.append('<div class="slot%s"><div class="hr">%s</div><div class="ev">%s</div></div>'
                    % (" on" if on else "", when.strip(), what.strip()))
    return (
        '<div class="rail"><span>%s</span><span>%s</span></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="cal%s%s">%s%s%s</div>'
        '%s%s'
        '<div class="grow"></div>'
        '<div class="offer">%s</div>'
        '<div class="btn">%s</div>'
        '<div class="terms">%s</div>'
        % (x.get("rail_l", kit.brand), x.get("rail_r", kit.eyebrow), ad.callout, ad.head,
           " wide" if any(len(s2.lstrip("*").split("|")[0].strip()) > 9
                          for s2 in (x.get("slots") or ())) else "",
           " fill" if x.get("fill") else "",
           ('<div class="days">%s</div>' % "".join(cells)) if cells else "",
           ('<div class="dateline">%s</div>' % x["date_line"]) if x.get("date_line") else "",
           "".join(rows),
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           ('<div class="deliver%s">%s</div>' % (" big" if x.get("deliver_big") else "",
                                                  x["deliver"])) if x.get("deliver") else "",
           x.get("offer", ""), kit.cta, x.get("terms_line", kit.terms)))


LAYOUTS["calendar"] = (_calendar, _calendar_shell)
PROVENANCE["calendar"] = (
    "Calendar week UI supplied in chat, 23 Sep 2026: day strip with today circled, "
    "hour rows, one coloured event block",
    "-",
    "The reader's own week, with the paid work already in it. Four hour rows and one "
    "accent event; the reference's photo, stickers and twelve empty hours are dropped. "
    "No live cost yet: the only two fake-UI formats measured on this account went "
    "opposite ways (tweet card Rs 126, chat 1.22x par), so it ships beside a serif "
    "face for the same reader.")


# ---------------------------------------------------------------- syllabus
# Scaffolded 23 Sep 2026 from: crimlit_sep26_04_full-calendar, the live face at Rs 229 a buyer against a Rs 475 community median: 21 numbered day cards in three columns, week colour bands, key terms highlighted
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _syllabus(pal, s):
    """The 21 cell syllabus grid.

    Taken from `crimlit_sep26_04_full-calendar`, the only layout source in this
    repo whose live cost sits BELOW its campaign median: Rs 229 a buyer against
    Rs 475 across the community half, while carrying 92% of that campaign's
    spend. Everything here is copied from that face except the call-out band,
    which the reference does not have - it names no ICP at all, which is
    archetype D (index 1.22, "do not build"). The band is the one thing this
    layout adds, and settling whether it helps or hurts is the point of the wave.

    Three mechanics from the reference are held fixed, because they are the only
    plausible reasons it beat four re-skins of the same device (Rs 393, 404, 477
    and 522): ALL of the days are shown, never a subset dressed as the whole; the
    terms a criminal lawyer's eye catches are marked inside the cell; and the
    grid is read by row, three across, so the eye lands on a day number first.

    Week banding rides the rule above each cell rather than the text, so every
    word on the face keeps full ink contrast. No opacity anywhere - a tint that
    reads fine on screen is how shipped faces went under the contrast floor.
    """
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(28, s), "font-weight": "800",
                    "letter-spacing": ".13em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(24, s), "font-weight": "800",
                      "letter-spacing": ".12em", "text-transform": "uppercase",
                      "color": pal["accent"]}),
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.06", "letter-spacing": "-.02em",
                      "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(14, s), _px(22, s), _px(18, s)),
                      "border-radius": "8px", "margin-top": _px(18, s)}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.025em",
                   "color": pal["ink"], "margin-top": _px(16, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".legend", {"display": "flex", "gap": _px(9, s), "flex-wrap": "nowrap",
                     "margin-top": _px(18, s)}),
        (".legend .lg", {"font-size": _px(20, s), "font-weight": "900",
                         "letter-spacing": ".06em", "text-transform": "uppercase",
                         "padding": "%s %s" % (_px(7, s), _px(11, s)),
                         "border-radius": "5px", "white-space": "nowrap",
                         "color": "#fff", "background": pal["ink"]}),
        (".legend .lg.w1", {"background": pal["accent"]}),
        (".legend .lg.w2", {"background": pal["ink"]}),
        (".legend .lg.w3", {"background": pal["ink"], "color": pal["bright"]}),
        (".legend .lg.price", {"background": pal["bright"], "color": pal["ink"]}),
        (".sgrid", {"display": "grid", "grid-template-columns": "1fr 1fr 1fr",
                    "column-gap": _px(15, s), "row-gap": _px(9, s),
                    "margin-top": _px(16, s)}),
        (".sgrid .cell", {"border-top": "4px solid " + pal["line"],
                          "padding-top": _px(6, s), "min-height": _px(92, s)}),
        (".sgrid .cell.w1", {"border-top-color": pal["accent"]}),
        (".sgrid .cell.w2", {"border-top-color": pal["ink"]}),
        (".sgrid .cell.w3", {"border-top-color": pal["bright"]}),
        (".sgrid .d", {"font-size": _px(18, s), "font-weight": "900",
                       "letter-spacing": ".07em", "text-transform": "uppercase",
                       "color": "#fff", "background": pal["accent"],
                       "display": "inline-block", "border-radius": "4px",
                       "padding": "%s %s" % (_px(3, s), _px(7, s))}),
        (".sgrid .cell.w2 .d", {"background": pal["ink"]}),
        (".sgrid .cell.w3 .d", {"background": pal["ink"], "color": pal["bright"]}),
        (".sgrid .t", {"font-size": _px(24, s), "font-weight": "700",
                       "line-height": "1.22", "color": pal["ink"],
                       "margin-top": _px(5, s)}),
        # The marked term is weight plus accent COLOUR, not a highlighter block.
        # First render marked all 21 cells on a lime ground, which made the grid
        # read as one solid block and left `bright` doing four jobs at once - the
        # price chip, the week 3 chip, the week 3 rule and every mark. Colour is
        # free here and keeps the mark at full contrast.
        (".sgrid .t b", {"font-weight": "900", "color": pal["accent"]}),
        (".deliver", {"font-size": _px(28, s), "font-weight": "800",
                      "line-height": "1.28", "color": pal["ink"],
                      "margin-top": _px(14, s)}),
        (".def", {"font-size": _px(26, s), "line-height": "1.28",
                  "color": pal["ink"], "margin-top": _px(8, s)}),
        (".rule", {"border-top": "3px solid " + pal["ink"], "margin-top": _px(14, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(16, s),
                   "margin-top": _px(14, s)}),
        (".foot .sm", {"font-size": _barpx(24, s), "font-weight": "800",
                       "letter-spacing": ".05em", "text-transform": "uppercase",
                       "line-height": "1.28", "flex": "1"}),
        (".foot .sm.r", {"text-align": "right"}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(30, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(15, s), _px(28, s)),
                  "border-radius": "8px", "white-space": "nowrap"}),
    ]


def _syllabus_shell(kit, ad, s):
    """extra: days=[(n, text, week)], weeks=[(label, week)], price, deliver.

    `days` carries the FACE wording, which is the syllabus abbreviated to fit a
    grid cell in two lines. The unabbreviated version is on the landing page, and
    the spec writes both from one SKILLS list, so a face cannot name a day the
    page does not teach.
    """
    x = ad.extra
    days = x.get("days") or []
    weeks = x.get("weeks") or []
    cells = "".join(
        '<div class="cell w%d"><span class="d">Day %d</span>'
        '<div class="t">%s</div></div>' % (w, n, t) for n, t, w in days)
    legend = "".join('<div class="lg w%d">%s</div>' % (w, lab) for lab, w in weeks)
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="legend"><div class="lg price">%s</div>%s</div>'
        '<div class="sgrid">%s</div>'
        '<div class="grow"></div>'
        '%s%s'
        '<div class="rule"></div>'
        '<div class="foot"><div class="sm">%s</div>'
        '<div class="btn">%s</div>'
        '<div class="sm r">%s</div></div>'
        % (kit.brand, kit.eyebrow, ad.callout, ad.head,
           x.get("price", "&#8377;100"), legend, cells,
           ('<div class="deliver">%s</div>' % x["deliver"]) if x.get("deliver") else "",
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           x.get("foot_left", "21 days &middot; live online"), kit.cta,
           x.get("foot_right", ad.proof)))


LAYOUTS["syllabus"] = (_syllabus, _syllabus_shell)
PROVENANCE["syllabus"] = ("crimlit_sep26_04_full-calendar, the live face at Rs 229 a buyer against a Rs 475 community median: 21 numbered day cards in three columns, week colour bands, key terms highlighted", "-",
                        "Scaffolded 23 Sep 2026. Still a clone of notice until its CSS "
                        "is written.")


# ---------------------------------------------------------------- broadsheet
# Scaffolded 23 Sep 2026 from: the DPDP newspaper faces (oct_01/04/07/14/15), blended Rs 136 a buyer against Rs 168 for the standard treatment in the same campaign and week; masthead, ICP slug bar, serif deck, photo column, drop-cap column, boxed price panel
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _broadsheet(pal, s):
    """A front page, cut to five blocks: masthead, ICP, head, what-you-get, price.

    Taken from the DataProtection 17-19 Oct newspaper faces, the only treatment in
    this repo measured against a sibling treatment in the SAME campaign and week:
    Rs 136 a buyer over 5 faces and 65 buyers against Rs 168 over 9 faces and 155
    buyers. Margins overlap, so probably better, not proven.

    REBUILT 23 Sep 2026 after the first version was read back as "too much
    information". That version carried eleven blocks, a second brand name, and all
    fourteen syllabus days in a two-column spread. A reader who is half asleep does
    not parse eleven blocks; they read the band, the head, and one list.

    So: one column, five blocks, and the type goes UP rather than the content
    going wider. The masthead is the real brand, not an invented paper. There is no
    strap row, no standfirst and no separate price box - the price rides the
    footer, which is where the reader already looks for it.
    """
    SERIF, SANS = _fonts()
    paper = pal.get("soft") or "#EFEBE1"
    return _base(pal, s) + [
        ("body", {"background": paper, "color": pal["ink"], "font-family": SERIF}),
        (".canvas", {"background": paper}),
        (".mast", {"border-top": "10px solid " + pal["ink"],
                   "border-bottom": "3px solid " + pal["ink"],
                   "padding": "%s 0 %s" % (_px(12, s), _px(10, s)),
                   "display": "flex", "align-items": "baseline",
                   "justify-content": "space-between", "gap": _px(14, s)}),
        (".mast .nameplate", {"font-family": SERIF, "font-weight": "700",
                              "font-size": _px(52, s), "line-height": "1",
                              "letter-spacing": "-.015em"}),
        (".mast .nameplate i", {"font-style": "normal", "color": pal["accent"]}),
        (".mast .price", {"font-family": SANS, "font-size": _px(30, s),
                          "font-weight": "900", "letter-spacing": ".04em",
                          "text-transform": "uppercase", "white-space": "nowrap"}),
        (".callout", {"display": "block", "background": pal["ink"], "color": paper,
                      "font-family": SANS, "font-size": _idpx(68, s),
                      "font-weight": "900", "line-height": "1.05",
                      "letter-spacing": "-.015em", "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(12, s), _px(20, s), _px(16, s)),
                      "margin-top": _px(26, s)}),
        (".head", {"font-family": SERIF, "font-size": _idpx(80, s),
                   "font-weight": "700", "line-height": "1.06",
                   "letter-spacing": "-.028em", "margin-top": _px(24, s),
                   "color": pal["ink"]}),
        (".head em", {"font-style": "italic", "color": pal["accent"]}),
        (".def", {"font-family": SERIF, "font-size": _px(36, s),
                  "line-height": "1.28", "margin-top": _px(18, s),
                  "color": pal["ink"]}),
        (".gets", {"border-top": "3px solid " + pal["ink"],
                   "border-bottom": "3px solid " + pal["ink"],
                   "margin-top": _px(26, s), "padding": "%s 0" % _px(6, s)}),
        (".gets .gh", {"font-family": SANS, "font-size": _barpx(24, s),
                       "font-weight": "900", "letter-spacing": ".12em",
                       "text-transform": "uppercase", "color": pal["accent"],
                       "padding": "%s 0 %s" % (_px(10, s), _px(6, s))}),
        (".gets .g", {"font-family": SERIF, "font-size": _px(40, s),
                      "font-weight": "700", "line-height": "1.2",
                      "padding": "%s 0" % _px(11, s),
                      "border-top": "1px solid " + pal["line"]}),
        (".gets .g:first-of-type", {"border-top": "0"}),
        (".rule", {"border-top": "3px solid " + pal["ink"], "margin-top": _px(18, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(16, s),
                   "margin-top": _px(16, s)}),
        (".foot .sm", {"font-family": SANS, "font-size": _barpx(26, s),
                       "font-weight": "800", "letter-spacing": ".04em",
                       "text-transform": "uppercase", "line-height": "1.25"}),
        (".btn", {"background": pal["accent"], "color": "#fff", "font-family": SANS,
                  "font-size": _px(34, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(16, s), _px(30, s)),
                  "white-space": "nowrap"}),
        # big_cta: the button takes the whole line and the terms sit above it. Added
        # 1 Oct 2026; the recorded reference for this layout is "a full-width join
        # button", and a small footer pill was rejected on a notice face on 29 Sep.
        (".foot.big", {"display": "block"}),
        (".foot.big .sm", {"margin-bottom": _px(14, s)}),
        (".foot.big .btn", {"display": "block", "text-align": "center",
                            "font-size": _px(40, s),
                            "padding": "%s 0" % _px(22, s)}),
    ]


def _broadsheet_shell(kit, ad, s):
    """extra: price_flag, gets [str], gets_title, foot_left. Five blocks, no more."""
    x = ad.extra
    gets = "".join('<div class="g">%s</div>' % g for g in (x.get("gets") or []))
    return (
        '<div class="mast"><div class="nameplate">%s</div>'
        '<div class="price">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="def">%s</div>'
        '<div class="grow"></div>'
        '<div class="gets"><div class="gh">%s</div>%s</div>'
        '<div class="rule"></div>'
        '<div class="foot%s"><div class="sm">%s</div><div class="btn">%s</div></div>'
        % (kit.brand, x.get("price_flag", "&#8377;200"),
           ad.callout, ad.head, ad.definition,
           x.get("gets_title", "What you get"), gets,
           " big" if x.get("big_cta") else "",
           x.get("foot_left", "&#8377;200 one time &middot; refund anytime"), kit.cta))


LAYOUTS["broadsheet"] = (_broadsheet, _broadsheet_shell)
PROVENANCE["broadsheet"] = ("the DPDP newspaper faces (oct_01/04/07/14/15), blended Rs 136 a buyer against Rs 168 for the standard treatment in the same campaign and week; masthead, ICP slug bar, serif deck, photo column, drop-cap column, boxed price panel", "-",
                        "Scaffolded 23 Sep 2026. Still a clone of notice until its CSS "
                        "is written.")

# ---------------------------------------------------------------- newsprop
# Built 23 Sep 2026 from a supplied DTC reference: a hand holding a newspaper
# against a sky, the offer printed inside the newspaper's own blank panel.
# The photograph is generated and lives in the kit's photos/ folder; nothing
# here draws a newspaper in CSS.

def _newsprop(pal, s):
    """Photo of a held newspaper, the promise printed in its blank panel.

    Four blocks, in reading order: who it is for, the newspaper carrying the
    promise, what Rs 200 gets you, the price and the button. The headline sits
    INSIDE the photograph, which is the whole point of the device - the reader
    sees a newspaper first and the words second, the way they would on a
    newsstand.
    """
    SERIF, SANS = _fonts()
    return _base(pal, s) + [
        ("body", {"background": pal["page"], "color": pal["ink"],
                  "font-family": SANS}),
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline", "margin-bottom": _px(12, s)}),
        (".brand", {"font-size": _px(28, s), "font-weight": "800",
                    "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(24, s), "font-weight": "800",
                      "letter-spacing": ".1em", "text-transform": "uppercase",
                      "color": pal["accent"]}),
        (".callout", {"display": "block", "background": pal["ink"], "color": "#fff",
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.05", "letter-spacing": "-.015em",
                      "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(12, s), _px(18, s), _px(16, s))}),
        # The photograph. `cover` on a fixed box, so the panel percentages below
        # stay true whatever the source image's exact pixel size.
        (".shot", {"position": "relative", "width": "100%",
                   "height": _px(700, s), "margin-top": _px(14, s),
                   "background-position": "center 58%",
                   "background-size": "cover", "background-repeat": "no-repeat"}),
        (".shot .panel", {"position": "absolute", "left": "27%", "right": "27%",
                          "top": "22%", "height": "36%",
                          "display": "flex", "align-items": "center",
                          "justify-content": "center", "text-align": "center"}),
        (".head", {"font-family": SERIF, "font-size": _idpx(64, s),
                   "font-weight": "700", "line-height": "1.1",
                   "letter-spacing": "-.02em", "color": "#14110D"}),
        (".head em", {"font-style": "italic", "color": pal["accent"]}),
        (".gets", {"margin-top": _px(16, s), "border-top": "3px solid " + pal["ink"]}),
        (".gets .g", {"font-size": _px(31, s), "font-weight": "700",
                      "line-height": "1.24", "padding": "%s 0" % _px(9, s),
                      "border-bottom": "1px solid " + pal["line"],
                      "color": pal["ink"]}),
        (".gets .g span", {"color": pal["accent"], "font-weight": "900",
                           "margin-right": _px(10, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(16, s),
                   "margin-top": _px(16, s)}),
        (".foot .sm", {"font-size": _barpx(25, s), "font-weight": "800",
                       "letter-spacing": ".04em", "text-transform": "uppercase",
                       "line-height": "1.25"}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(32, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(15, s), _px(28, s)),
                  "border-radius": "8px", "white-space": "nowrap"}),
    ]


def _newsprop_shell(kit, ad, s):
    """extra: photo (path relative to the kit), gets [str], foot_left."""
    x = ad.extra
    gets = "".join('<div class="g"><span>&#10003;</span>%s</div>' % g
                   for g in (x.get("gets") or []))
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="shot" style="background-image:url(\'%s\');background-position:%s">'
        '<div class="panel" style="%s"><div class="head">%s</div></div></div>'
        '<div class="grow"></div>'
        '<div class="gets">%s</div>'
        '<div class="foot"><div class="sm">%s</div><div class="btn">%s</div></div>'
        % (kit.brand, kit.eyebrow, ad.callout,
           x.get("photo", ""), x.get("focus", "center 58%"),
           # The blank rectangle sits somewhere different in every photograph, so
           # the panel box is per-ad. Defaults are the news_a geometry.
           x.get("panel", "left:27%;right:27%;top:22%;height:36%"),
           ad.head, gets,
           x.get("foot_left", "&#8377;200 one time &middot; refund anytime"),
           kit.cta))


LAYOUTS["newsprop"] = (_newsprop, _newsprop_shell)
PROVENANCE["newsprop"] = (
    "DTC skincare static supplied in chat, 23 Sep 2026: a hand holding a "
    "newspaper against a sky with the offer inside the paper's own panel",
    "-",
    "The newspaper is a PROP in the photograph, not the layout of the ad. An "
    "earlier attempt made the whole canvas a newspaper front page and was "
    "rejected for exactly that. The photograph is generated and stored in the "
    "kit; the panel geometry is measured off it and expressed as percentages.")


# ---------------------------------------------------------------- frontpage
# Built 26 Sep 2026 for Tech Law wave 2, ported from the hand-built sample that
# Ruchika approved ("i like the 43 words one"), after the 99-word first cut was
# read back as "too text heavy" and she asked "where is the register button?".
# Reference: the DPDP newspaper faces (oct_01/04/07/14/15), Rs 157 per paid on
# GrowthX, 18-24 Sep. Shape taken, copy not (the reference's "no one is senior to
# you" breaks the newness rule).
#
# NOT the same as `broadsheet` above (one column, no photo, price in the footer).
# This keeps the reference's photo column and boxed price, cut to about 45 words:
# brand, masthead, strip, reader bar, head, photo + three ticks + price box, and a
# full-width filled button. Photo is ad.shot, from the kit's photos/ folder,
# generated in black and white.
#   extra: strip_left, strip_right, gets_title, gets [3], price_big, price_sub

def _frontpage(pal, s):
    SERIF, SANS = _fonts()
    paper = pal["page"]
    return _base(pal, s) + [
        ("body", {"background": paper, "color": pal["ink"], "font-family": SERIF}),
        (".brand", {"text-align": "center", "font-family": SANS, "font-weight": "700",
                    "font-size": _px(20, s), "letter-spacing": ".14em",
                    "text-transform": "uppercase"}),
        (".mast", {"font-family": SERIF, "font-weight": "700", "font-size": _px(78, s),
                   "line-height": "1", "text-align": "center", "letter-spacing": "-.01em",
                   "text-transform": "uppercase", "margin-top": _px(6, s)}),
        (".strip", {"display": "flex", "justify-content": "space-between",
                    "border-top": "4px double " + pal["ink"],
                    "border-bottom": "1.5px solid " + pal["ink"],
                    "margin-top": _px(12, s), "padding": "%s 0" % _px(9, s),
                    "font-family": SANS, "font-weight": "700", "font-size": _px(18, s),
                    "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".callout", {"align-self": "flex-start", "background": pal["accent"],
                      "color": "#FFFFFF", "font-family": SANS, "font-weight": "800",
                      "font-size": _idpx(66, s), "line-height": "1.05",
                      "letter-spacing": ".01em", "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(14, s), _px(22, s), _px(12, s)),
                      "margin-top": _px(26, s)}),
        (".head", {"font-family": SERIF, "font-weight": "700", "font-size": _idpx(84, s),
                   "line-height": "1.02", "letter-spacing": "-.02em",
                   "margin-top": _px(18, s)}),
        (".head em", {"font-style": "normal"}),
        (".hr", {"border-top": "1.5px solid " + pal["ink"], "margin-top": _px(24, s)}),
        (".fp", {"display": "grid", "grid-template-columns": "1.12fr 1fr",
                 "margin-top": _px(24, s), "flex": "1", "min-height": "0"}),
        (".fp .photo", {"overflow": "hidden", "border": "1.5px solid " + pal["ink"],
                        "margin-right": _px(26, s)}),
        (".fp .photo img", {"width": "100%", "height": "100%", "object-fit": "cover",
                            "display": "block", "filter": "grayscale(1) contrast(1.05)"}),
        (".fp .col", {"border-left": "1.5px solid " + pal["ink"], "padding-left": _px(26, s),
                      "display": "flex", "flex-direction": "column"}),
        (".fp .gh", {"font-family": SANS, "font-weight": "800", "font-size": _px(20, s),
                     "letter-spacing": ".14em", "text-transform": "uppercase",
                     "border-bottom": "1.5px solid " + pal["ink"],
                     "padding-bottom": _px(8, s)}),
        (".fp .tk", {"font-family": SERIF, "font-weight": "700", "font-size": _px(40, s),
                     "line-height": "1.15", "padding": "%s 0" % _px(18, s),
                     "border-bottom": "1px solid " + pal["line"]}),
        (".fp .price", {"margin-top": "auto", "border": "4px double " + pal["ink"],
                        "padding": "%s %s %s" % (_px(16, s), _px(12, s), _px(14, s)),
                        "text-align": "center"}),
        (".fp .price .n", {"font-family": SERIF, "font-weight": "700",
                           "font-size": _px(78, s), "line-height": "1"}),
        (".fp .price .s", {"font-family": SANS, "font-weight": "800",
                           "font-size": _px(25, s), "letter-spacing": ".06em",
                           "text-transform": "uppercase", "margin-top": _px(6, s)}),
        (".btn", {"margin-top": _px(22, s), "background": pal["accent"], "color": "#FFFFFF",
                  "text-align": "center", "font-family": SANS, "font-weight": "800",
                  "font-size": _px(40, s), "padding": "%s 0" % _px(22, s),
                  "border-radius": "6px"}),
    ]


def _frontpage_shell(kit, ad, s):
    x = ad.extra
    ticks = "".join('<div class="tk">&#10003; %s</div>' % g for g in (x.get("gets") or [])[:3])
    return (
        '<div class="brand">%s</div>'
        '<div class="mast">%s</div>'
        '<div class="strip"><span>%s</span><span>%s</span></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="hr"></div>'
        '<div class="fp"><div class="photo"><img src="../photos/%s" alt=""%s></div>'
        '<div class="col"><div class="gh">%s</div>%s'
        '<div class="price"><div class="n">%s</div><div class="s">%s</div></div></div></div>'
        '<div class="btn">%s &#8594;</div>'
        % (_plain(kit.brand), kit.eyebrow, x.get("strip_left", "Live online"),
           x.get("strip_right", ""), ad.callout, ad.head, ad.shot or "",
           (' style="object-position:%s"' % x["shot_pos"]) if x.get("shot_pos") else "",
           x.get("gets_title", "What you learn"), ticks,
           x.get("price_big", "&#8377;10"), x.get("price_sub", "incl. GST, refundable"),
           kit.cta))


LAYOUTS["frontpage"] = (_frontpage, _frontpage_shell)
PROVENANCE["frontpage"] = (
    "the DPDP newspaper faces (oct_01/04/07/14/15), Rs 157 per paid on GrowthX 18-24 Sep; "
    "cut to ~45 words and approved by Ruchika 26 Sep 2026", "-",
    "Newspaper front page with a photo column, three ticks, a boxed price and a "
    "full-width button.")


# ---------------------------------------------------------------- notes
# Built 30 Sep 2026 from a DTC skincare static supplied in chat ("Why is everyone obsessed with
# NIACINAMIDE / Know your ingredients." on an iPhone Notes card, eyes emoji peeking over the top
# edge, the key phrase shown as selected text with blue drag handles, soft glass-drop ground).
# Asked for as the second NCA face per reader: "one notice format and one Notes app style ad".
#
# Mapping: the reader's question is the small line (`callout`, still >= 64px, C8); the offer is
# the big line (`head`); the <em> part of the head is rendered as the SELECTED text, which is the
# reference's one visual trick and puts the eye on the turn. Below the card: the delivery line,
# one full-width button, the terms. No price on the card itself: it lives in the button and the
# terms, as on the full-width notice faces.

def _notes(pal, s):
    from .layouts import _barpx
    amber, sel, handle = "#E3A31B", "#D3E8F5", "#3F92C6"
    return _base(pal, s) + [
        (".canvas", {"background":
                     "radial-gradient(circle at 18%% 12%%, rgba(255,255,255,0) 0 %s, "
                     "rgba(255,255,255,.95) %s, rgba(0,0,0,.09) %s, rgba(255,255,255,0) %s), "
                     "radial-gradient(circle at 78%% 58%%, rgba(255,255,255,0) 0 %s, "
                     "rgba(255,255,255,1) %s, rgba(0,0,0,.10) %s, rgba(255,255,255,0) %s), "
                     "linear-gradient(160deg, #F4F4F2 0%%, %s 100%%)"
                     % (_px(300, 1), _px(318, 1), _px(330, 1), _px(342, 1),
                        _px(360, 1), _px(378, 1), _px(392, 1), _px(406, 1), pal["page"])}),
        (".rail", {"text-align": "center", "font-size": _px(26, s), "font-weight": "800",
                   "letter-spacing": ".13em", "text-transform": "uppercase",
                   "color": pal["accent"]}),
        (".card", {"position": "relative", "background": "#FFFFFF", "border-radius": _px(44, s),
                   "box-shadow": "0 30px 70px rgba(0,0,0,.14)",
                   "padding": "%s %s %s" % (_px(30, s), _px(52, s), _px(52, s)),
                   "margin-top": _px(70, s)}),
        # drawn, not an emoji: the emoji font differs by platform (Windows renders purple
        # Fluent eyes), so the reference's white eyes with brown irises are drawn in CSS.
        (".eyes", {"position": "absolute", "top": "-%s" % _px(62, s), "right": _px(110, s),
                   "display": "flex", "gap": _px(4, s)}),
        (".eye", {"position": "relative", "width": _px(62, s), "height": _px(88, s),
                  "background": "radial-gradient(ellipse at 40% 30%, #FFFFFF 55%, #E6E6E6 100%)",
                  "border": "2px solid #CFCFCF", "border-radius": "50%",
                  "box-shadow": "0 6px 14px rgba(0,0,0,.18)"}),
        (".eye i", {"position": "absolute", "left": "50%", "bottom": _px(12, s),
                    "width": _px(36, s), "height": _px(38, s), "margin-left": "-%s" % _px(20, s),
                    "border-radius": "50%",
                    "background": "radial-gradient(circle at 36% 34%, #FFFFFF 0 11%, #111 13% 38%, "
                                  "#7A4A12 41% 100%)"}),
        (".nbar", {"display": "flex", "justify-content": "space-between", "align-items": "center",
                   "color": amber, "font-size": _px(34, s), "font-weight": "600",
                   "margin-bottom": _px(34, s)}),
        (".nbar .dots", {"font-size": _px(40, s), "letter-spacing": ".08em", "font-weight": "900"}),
        (".callout", {"font-size": _idpx(64, s), "font-weight": "500", "line-height": "1.12",
                      "letter-spacing": "-.01em", "text-align": "center", "color": "#1F1F1F",
                      "text-wrap": "balance"}),
        # line-height 1.3, not 1.14: at 1.14 each selected line's background painted over the
        # descenders of the line above ("q" and "y" cut on 62, reported 30 Sep 2026). The
        # highlight is also a band (gradient) rather than the full inline box, for the same reason.
        (".head", {"font-size": _idpx(84, s), "font-weight": "800", "line-height": "1.3",
                   "letter-spacing": "-.025em", "text-align": "center", "color": "#141414",
                   "margin-top": _px(26, s), "text-wrap": "balance"}),
        (".head .sel", {"background": "linear-gradient(transparent 14%%, %s 14%%, %s 96%%, "
                                      "transparent 96%%)" % (sel, sel),
                        "box-decoration-break": "clone",
                        "-webkit-box-decoration-break": "clone",
                        "padding": "0 %s" % _px(6, s)}),
        (".head .hd", {"display": "inline-block", "position": "relative", "width": _px(6, s),
                       "height": "1.02em", "background": handle, "vertical-align": "-0.16em"}),
        (".head .hd::before", {"content": "''", "position": "absolute", "left": "50%",
                               "width": _px(20, s), "height": _px(20, s),
                               "margin-left": "-%s" % _px(10, s), "border-radius": "50%",
                               "background": handle}),
        (".head .hd.l::before", {"top": "-%s" % _px(14, s)}),
        (".head .hd.r::before", {"bottom": "-%s" % _px(14, s)}),
        (".def", {"font-size": _px(32, s), "line-height": "1.34", "text-align": "center",
                  "margin-top": _px(24, s), "color": "#333"}),
        (".deliver", {"font-size": _px(34, s), "font-weight": "800", "line-height": "1.34",
                      "text-align": "center", "color": pal["accent"], "margin-top": _px(40, s),
                      "padding": "0 %s" % _px(10, s)}),
        (".bigbtn", {"background": pal["accent"], "color": "#fff", "text-align": "center",
                     "font-size": _px(46, s), "font-weight": "900",
                     "padding": "%s %s" % (_px(26, s), _px(30, s)),
                     "border-radius": _px(16, s), "margin-top": _px(28, s)}),
        (".terms", {"text-align": "center", "font-size": _barpx(27, s), "font-weight": "800",
                    "letter-spacing": ".06em", "text-transform": "uppercase", "color": pal["ink"],
                    "margin-top": _px(20, s)}),
    ]


def _notes_shell(kit, ad, s):
    """extra: deliver, terms_line, note_label (default Notes).
    The <em>...</em> part of `head` becomes the selected text with drag handles."""
    import re as _re
    x = ad.extra
    head = _re.sub(r"<em>(.*?)</em>",
                   r'<span class="sel"><i class="hd l"></i>\1<i class="hd r"></i></span>',
                   ad.head, flags=_re.S)
    return (
        '<div class="rail">%s &middot; %s</div>'
        '<div class="grow"></div>'
        '<div class="card">'
        '<div class="eyes"><span class="eye"><i></i></span><span class="eye"><i></i></span></div>'
        '<div class="nbar"><span>&#8249; %s</span><span class="dots">&middot;&middot;&middot;</span></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '%s'
        '</div>'
        '<div class="deliver">%s</div>'
        '<div class="bigbtn">%s</div>'
        '<div class="terms">%s</div>'
        '<div class="grow"></div>'
        % (_plain(kit.brand), kit.eyebrow,
           x.get("note_label", "Notes"), ad.callout, head,
           ('<div class="def">%s</div>' % ad.definition) if ad.definition else "",
           x.get("deliver", ""), kit.cta, x.get("terms_line", ad.proof)))


LAYOUTS["notes"] = (_notes, _notes_shell)
PROVENANCE["notes"] = (
    "DTC skincare Notes-app static supplied in chat, 30 Sep 2026 (niacinamide card)", "-",
    "An iPhone Notes card: the reader's question, the offer in large type with its key phrase "
    "shown as selected text, eyes emoji peeking over the card; delivery line and one full-width "
    "button below.")


# ---------------------------------------------------------------- share
# Built 30 Sep 2026 from a DTC skincare static supplied in chat (a phone file-share prompt:
# "<brand> wants to share: <file>.pdf", a ticked checklist, a tinted band, Decline/Accept).
# First sample: NCA 42 (company secretaries with an LLB), shown beside its notice face.
#
# Mapping, and what was deliberately NOT carried over:
# - no platform icon, no platform name, no status bar: Meta disallows creative that imitates
#   platform UI misleadingly [[feedback-notify-layout]]. The icon is our own drawn file glyph.
# - the reader's question is the `callout` at the top (>= 64px, C8); the offer is the file
#   name (`head`, >= 64px), with ".pdf" as a small grey tag so the sentence still reads plainly.
# - the reference's "ACCEPT?" is cut: alone it is a small riddle (Ruchika, 30 Sep: no puzzles).
# - three ticks, not five, and no emojis (the emoji font differs on the renderer).
# - ONE action. Decline/Accept became a single full-width filled button: a second control
#   competes for the click, which is what sank `alert` on 21 Sep.
#   extra: sender, ticks [3], band, terms_line

def _share(pal, s):
    from .layouts import _barpx
    soft = pal["line"]
    return _base(pal, s) + [
        (".canvas", {"background":
                     "radial-gradient(circle at 12%% 88%%, rgba(255,255,255,.75) 0 %s, "
                     "rgba(255,255,255,0) %s), "
                     "radial-gradient(circle at 92%% 18%%, rgba(255,255,255,.6) 0 %s, "
                     "rgba(255,255,255,0) %s), "
                     "linear-gradient(170deg, %s 0%%, %s 100%%)"
                     % (_px(160, 1), _px(300, 1), _px(120, 1), _px(260, 1), pal["page"], soft)}),
        (".rail", {"text-align": "center", "font-size": _px(26, s), "font-weight": "800",
                   "letter-spacing": ".13em", "text-transform": "uppercase",
                   "color": pal["accent"]}),
        (".card", {"background": "rgba(255,255,255,.96)", "border-radius": _px(44, s),
                   "box-shadow": "0 30px 70px rgba(0,0,0,.13)",
                   "padding": "%s %s %s" % (_px(40, s), _px(48, s), _px(44, s)),
                   "margin-top": _px(34, s), "text-align": "center"}),
        (".fico", {"position": "relative", "width": _px(74, s), "height": _px(92, s),
                   "margin": "0 auto", "border-radius": _px(10, s),
                   "background": pal["accent"]}),
        (".fico::before", {"content": "''", "position": "absolute", "top": "0", "right": "0",
                           "border-style": "solid",
                           "border-width": "0 %s %s 0" % (_px(24, s), _px(24, s)),
                           "border-color": "transparent #FFFFFF %s transparent" % soft}),
        (".fico b", {"position": "absolute", "left": "0", "right": "0", "bottom": _px(14, s),
                     "color": "#FFFFFF", "font-size": _px(20, s), "font-weight": "900",
                     "letter-spacing": ".06em"}),
        (".callout", {"font-size": _idpx(66, s), "font-weight": "800", "line-height": "1.1",
                      "letter-spacing": "-.015em", "color": pal["ink"],
                      "margin-top": _px(22, s), "text-wrap": "balance"}),
        (".sender", {"font-size": _px(32, s), "color": "#555", "margin-top": _px(18, s)}),
        (".head", {"font-size": _idpx(66, s), "font-weight": "800", "line-height": "1.14",
                   "letter-spacing": "-.02em", "color": pal["accent"],
                   "margin-top": _px(8, s), "text-wrap": "balance"}),
        (".head em", {"font-style": "normal"}),
        (".head .ext", {"font-size": ".5em", "font-weight": "700", "color": "#8A8A8A",
                        "letter-spacing": "0"}),
        (".list", {"border": "2px solid " + soft, "border-radius": _px(26, s),
                   "margin-top": _px(28, s), "text-align": "left", "overflow": "hidden"}),
        (".row", {"display": "flex", "align-items": "center", "gap": _px(22, s),
                  "padding": "%s %s" % (_px(20, s), _px(26, s)),
                  "font-size": _px(34, s), "font-weight": "600", "line-height": "1.22",
                  "color": pal["ink"]}),
        (".row + .row", {"border-top": "2px solid " + soft}),
        (".box", {"flex": "0 0 auto", "width": _px(46, s), "height": _px(46, s),
                  "border-radius": _px(10, s), "background": pal["accent"], "color": "#FFFFFF",
                  "display": "flex", "align-items": "center", "justify-content": "center",
                  "font-size": _px(30, s), "font-weight": "900"}),
        (".band", {"margin-top": _px(24, s), "background": soft, "border-radius": _px(18, s),
                   "padding": "%s %s" % (_px(18, s), _px(20, s)), "font-size": _px(32, s),
                   "font-weight": "800", "letter-spacing": ".04em", "text-transform": "uppercase",
                   "color": pal["ink"]}),
        (".bigbtn", {"background": pal["accent"], "color": "#fff", "text-align": "center",
                     "font-size": _px(46, s), "font-weight": "900",
                     "padding": "%s %s" % (_px(24, s), _px(30, s)),
                     "border-radius": _px(18, s), "margin-top": _px(24, s)}),
        (".terms", {"align-self": "center", "margin-top": _px(26, s),
                    "background": "rgba(255,255,255,.85)", "border-radius": "999px",
                    "padding": "%s %s" % (_px(16, s), _px(34, s)),
                    "box-shadow": "0 8px 22px rgba(0,0,0,.08)",
                    "font-size": _barpx(28, s), "font-weight": "800", "letter-spacing": ".05em",
                    "text-transform": "uppercase", "color": pal["ink"]}),
    ]


def _share_shell(kit, ad, s):
    x = ad.extra
    rows = "".join('<div class="row"><span class="box">&#10003;</span><span>%s</span></div>' % t
                   for t in (x.get("ticks") or kit.takeaways)[:3])
    return (
        '<div class="rail">%s &middot; %s</div>'
        '<div class="grow"></div>'
        '<div class="card">'
        '<div class="fico"><b>PDF</b></div>'
        '<div class="callout">%s</div>'
        '<div class="sender">%s</div>'
        '<div class="head">%s<span class="ext">.pdf</span></div>'
        '<div class="list">%s</div>'
        '<div class="band">%s</div>'
        '<div class="bigbtn">%s</div>'
        '</div>'
        '<div class="terms">%s</div>'
        '<div class="grow"></div>'
        % (_plain(kit.brand), kit.eyebrow, ad.callout,
           x.get("sender", "%s wants to share with you:" % _plain(kit.brand)),
           ad.head, rows, x.get("band", ""), kit.cta, x.get("terms_line", ad.proof)))


LAYOUTS["share"] = (_share, _share_shell)
PROVENANCE["share"] = (
    "DTC skincare file-share static supplied in chat, 30 Sep 2026 (a checklist PDF offered "
    "for download)", "-",
    "A file-share card: the reader's question, '<brand> wants to share with you:', the offer "
    "as the file name, three ticked take-aways, a price band and one full-width button.")


# ---------------------------------------------------------------- airdrop
# Scaffolded 01 Oct 2026 from: iOS AirDrop share sheet: rounded card, radar icon, 'X wants to share' + filename, ACCEPT?, checklist rows with ticked boxes, tinted banner line, Decline/Accept footer, save pill below
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _airdrop(pal, s):
    SERIF, SANS = _fonts()
    return _base(pal, s) + [
        # The sheet itself. iOS share sheets are a near-white card with a large
        # corner radius floating on the blurred page, so the canvas keeps the
        # palette's page colour and the card sits on top of it.
        (".sheet", {"background": "#FDFBFA", "border-radius": _px(44, s),
                    "padding": "%s %s %s" % (_px(40, s), _px(38, s), _px(10, s)),
                    "box-shadow": "0 %s %s rgba(0,0,0,.14)" % (_px(26, s), _px(60, s)),
                    "display": "flex", "flex-direction": "column"}),
        (".radar", {"text-align": "center", "line-height": "0",
                    "margin-top": _px(24, s)}),
        (".radar svg", {"width": _px(88, s), "height": _px(88, s)}),
        (".adtitle", {"text-align": "center", "font-size": _px(48, s),
                      "font-weight": "800", "letter-spacing": "-.01em",
                      "margin-top": _px(8, s), "color": "#1B1B1D"}),
        (".from", {"text-align": "center", "font-size": _px(31, s),
                   "line-height": "1.3", "margin-top": _px(12, s), "color": "#4A4A4F"}),
        (".file", {"text-align": "center", "font-size": _px(31, s),
                   "font-weight": "700", "margin-top": _px(4, s), "color": "#1B1B1D"}),
        # The reader, at the TOP of the sheet (Ruchika, 1 Oct: "put the heading (icp) at
        # the top, then the airdrop bit"). It was under the filename, which read as an
        # afterthought on a device whose own chrome is the loudest thing in the frame.
        # C8 reads this class name, so it stays a class rule and uses _idpx, which clamps
        # at the 64px identity floor whatever auto-fit does.
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.06", "letter-spacing": "-.02em",
                      "text-transform": "uppercase", "text-align": "center",
                      "border-radius": _px(18, s),
                      "padding": "%s %s" % (_px(16, s), _px(14, s))}),
        (".ask", {"text-align": "center", "font-size": _px(30, s), "font-weight": "800",
                  "letter-spacing": ".16em", "text-transform": "uppercase",
                  "margin-top": _px(20, s), "color": "#6A6A70"}),
        # The checklist. Hairline-separated rows inside one bordered block, the way
        # a share sheet lists what is coming across.
        (".rows", {"border": "%s solid %s" % (_px(2, s), pal["line"]),
                   "border-radius": _px(22, s), "margin-top": _px(14, s),
                   "overflow": "hidden"}),
        (".row", {"display": "flex", "align-items": "center", "gap": _px(20, s),
                  "padding": "%s %s" % (_px(17, s), _px(20, s)),
                  "border-bottom": "%s solid %s" % (_px(2, s), pal["line"]),
                  "font-size": _px(35, s), "font-weight": "600", "line-height": "1.25"}),
        (".row:last-child", {"border-bottom": "0"}),
        (".box", {"flex": "none", "width": _px(40, s), "height": _px(40, s),
                  "border-radius": _px(10, s), "background": pal["accent"],
                  "color": "#fff", "font-size": _px(27, s), "font-weight": "900",
                  "display": "flex", "align-items": "center",
                  "justify-content": "center"}),
        # The turn, as the sheet's own highlighted line. Second identity class.
        (".head", {"background": pal["soft"], "color": pal["ink"],
                   "font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.02em",
                   "text-align": "center", "border-radius": _px(18, s),
                   "margin-top": _px(20, s),
                   "padding": "%s %s" % (_px(18, s), _px(16, s))}),
        (".head em", {"font-style": "italic", "color": pal["accent"]}),
        (".def", {"text-align": "center", "font-size": _px(29, s),
                  "line-height": "1.35", "color": "#4A4A4F", "margin-top": _px(14, s)}),
        # Decline / Accept, split by a hairline the way iOS splits a two-button sheet.
        (".actions", {"display": "flex", "margin-top": _px(22, s),
                      "border-top": "%s solid %s" % (_px(2, s), pal["line"])}),
        (".act", {"flex": "1", "text-align": "center", "font-size": _px(40, s),
                  "font-weight": "600", "color": "#0A7AFF",
                  "padding": "%s 0" % _px(22, s)}),
        (".act.y", {"font-weight": "800"}),
        (".act.y", {"border-left": "%s solid %s" % (_px(2, s), pal["line"])}),
        # The delivery sentence, then a REAL join button. Decline/Accept above is the
        # device's own chrome and reads as iOS, not as a call to action - Ruchika, 1 Oct:
        # "there is no clear join now button". A small footer pill was rejected on the
        # notice faces on 29 Sep for the same reason, so this is full width and on the
        # accent, like `notice` with big_cta.
        (".dline", {"text-align": "center", "font-size": _px(30, s), "font-weight": "700",
                    "line-height": "1.3", "color": "#1B1B1D", "margin-top": _px(22, s)}),
        (".bigbtn", {"background": pal["accent"], "color": "#fff", "text-align": "center",
                     "font-size": _px(46, s), "font-weight": "900",
                     "padding": "%s %s" % (_px(24, s), _px(30, s)),
                     "border-radius": _px(16, s), "margin-top": _px(16, s)}),
        (".tline", {"text-align": "center", "font-size": _px(26, s), "font-weight": "800",
                    "letter-spacing": ".04em", "text-transform": "uppercase",
                    "margin-top": _px(12, s), "color": pal["ink"]}),
    ]


# The AirDrop radar: three concentric arcs over a dot, in Apple's system blue.
_RADAR = ('<svg viewBox="0 0 64 64" fill="none" stroke="#0A7AFF" stroke-width="4.6" '
          'stroke-linecap="round"><path d="M6 32a31 31 0 0 1 52 0"/>'
          '<path d="M15 43a21 21 0 0 1 34 0"/>'
          '<path d="M24 53a11 11 0 0 1 16 0"/>'
          '<circle cx="32" cy="60" r="3" fill="#0A7AFF" stroke="none"/></svg>')


def _airdrop_shell(kit, ad, s):
    x = ad.extra
    rows = "".join('<div class="row"><span class="box">&#10003;</span>%s</div>' % t
                   for t in x.get("ticks", []))
    return (
        '<div class="grow"></div>'
        '<div class="sheet">'
        '<div class="callout">%s</div>'
        '<div class="radar">%s</div>'
        '<div class="adtitle">AirDrop</div>'
        '<div class="from">%s wants to share:</div>'
        '<div class="file">&ldquo;%s&rdquo;</div>'
        '<div class="ask">%s</div>'
        '<div class="rows">%s</div>'
        '<div class="head">%s</div>'
        '<div class="def">%s</div>'
        '<div class="actions"><div class="act">Decline</div>'
        '<div class="act y">%s</div></div>'
        '</div>'
        '<div class="grow2"></div>'
        '<div class="dline">%s</div>'
        '<div class="bigbtn">%s</div>'
        '<div class="tline">%s</div>'
        % (ad.callout, _RADAR, x.get("sender", kit.eyebrow), x.get("file", ""),
           x.get("ask", "Accept?"), rows, ad.head, ad.definition,
           x.get("accept", "Accept"), x.get("deliver", ""), kit.cta,
           x.get("terms_line", "")))


LAYOUTS["airdrop"] = (_airdrop, _airdrop_shell)
PROVENANCE["airdrop"] = ("iOS AirDrop share sheet: rounded card, radar icon, 'X wants to share' + filename, ACCEPT?, checklist rows with ticked boxes, tinted banner line, Decline/Accept footer, save pill below", "-",
                        "Built 1 Oct 2026 from a reference Ruchika sent, for the Tech Law "
                        "24-26 Oct wave (71-75). The sheet carries the reader in .callout "
                        "and the turn in .head; the checklist rows are the camp's named "
                        "deliverables, so the device argues instead of decorating.")


# ---------------------------------------------------------------- launchlist
# Scaffolded 01 Oct 2026 from: SC_Oct3|w9_20_hospital_admin and 10 sibling faces, Senior Consulting 3-5 Oct 2026, measured 0.67x par on 2,060 buyers
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _launchlist(pal, s):
    """The "launch your own" named-work list. Built 1 Oct 2026 from the eleven
    SC_Oct3|w9_* faces of Senior Consulting 3-5 Oct, which ran 0.67x par on 2,060
    buyers while that campaign's verb-headline faces ran 1.50x on 1,380 in the same
    weeks. The same structure carries Global Patent's cheapest faces (veterinary
    0.59), US Corporate Law's (cs_inhouse_mnc 0.75) and Academic Writing's
    (medical_researchers 0.78): 29 ads, 5,568 buyers, 0.79 across four campaigns.

    WHAT IT TAKES FROM THE REFERENCE, in order:
      1. a thin brand rail, brand left and camp name right
      2. the ICP in a hard solid band, small caps, nothing else on the line
      3. a serif display headline naming the DESTINATION as a noun phrase, with
         one clause in the accent colour. Never a verb lead - that is the single
         thing the 1.50x faces in the same campaign all did.
      4. a small outlined qualifier pill: the barrier removed, stated positively
      5. one bold promise line, then one short plain paragraph
      6. the named work as a NUMBERED list, 01/02/03, label plus one ordinary line
      7. the price line, a full-width dark button, then the terms bar

    WHAT IT DELIBERATELY HAS NOT GOT: a middle widget. Every face in the 1.50x
    group carried an extra table, bar chart or two-column panel between the
    headline and the list; not one of the 0.67x faces did."""
    SERIF, SANS = _fonts()
    return _base(pal, s) + [
        (".canvas", {"background": pal["page"], "color": pal["ink"],
                     "font-family": SANS}),
        (".rail", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between",
                   "font-size": _px(25, s), "font-weight": "800",
                   "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".rail .camp", {"color": pal["accent"]}),
        # 2. the ICP, in a hard band
        (".callout", {"display": "inline-block", "background": pal["ink"],
                      "color": "#FFFFFF", "font-size": _idpx(74, s),
                      "font-weight": "900", "line-height": "1.1",
                      "letter-spacing": "-.01em", "text-transform": "uppercase",
                      "margin-top": _px(30, s), "text-wrap": "balance",
                      "padding": "%s %s" % (_px(12, s), _px(22, s))}),
        # 3. the destination, as a noun phrase
        (".head", {"font-family": SERIF, "font-size": _idpx(96, s),
                   "font-weight": "700", "line-height": "1.06",
                   "letter-spacing": "-.02em", "margin-top": _px(22, s),
                   "text-wrap": "balance"}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        # 4. the barrier, removed, stated positively
        (".qual", {"display": "inline-block", "border": "3px solid " + pal["accent"],
                   "color": pal["ink"], "font-size": _px(30, s), "font-weight": "800",
                   "border-radius": _px(10, s), "margin-top": _px(20, s),
                   "padding": "%s %s" % (_px(8, s), _px(18, s))}),
        # 5. the promise, then the plain paragraph
        (".promise", {"font-size": _px(32, s), "font-weight": "900",
                      "line-height": "1.26", "margin-top": _px(20, s)}),
        (".lede", {"font-size": _px(29, s), "font-weight": "600",
                   "line-height": "1.34", "margin-top": _px(12, s),
                   "color": pal["ink"]}),
        # 6. the named work, numbered
        (".rows", {"margin-top": _px(22, s)}),
        (".rows .row", {"display": "flex", "gap": _px(18, s),
                        "margin-top": _px(16, s), "align-items": "flex-start"}),
        (".rows .num", {"font-size": _px(28, s), "font-weight": "900",
                        "color": pal["accent"], "min-width": _px(46, s),
                        "padding-top": _px(3, s)}),
        (".rows .rlab", {"font-size": _px(30, s), "font-weight": "900",
                         "line-height": "1.2"}),
        (".rows .rtxt", {"font-size": _px(26, s), "font-weight": "600",
                         "line-height": "1.3", "margin-top": _px(5, s),
                         "color": pal["ink"], "opacity": ".78"}),
        # 7. the ask
        (".price", {"font-size": _px(30, s), "font-weight": "900",
                    "margin-top": _px(24, s)}),
        (".cta", {"background": pal["ink"], "color": "#FFFFFF", "text-align": "center",
                  "font-size": _px(38, s), "font-weight": "900",
                  "border-radius": _px(8, s), "margin-top": _px(14, s),
                  "padding": "%s %s" % (_px(22, s), _px(18, s))}),
        (".terms", {"font-size": _barpx(25, s), "font-weight": "800",
                    "letter-spacing": ".08em", "text-transform": "uppercase",
                    "color": pal["ink"], "margin-top": _px(16, s)}),
    ]


def _launchlist_rows(kit, ad, s):
    """extra["rows"] as "LABEL | text", else kit.takeaways with no label."""
    rows = ad.extra.get("rows") or list(kit.takeaways)[:4]
    out = []
    for i, r in enumerate(rows, 1):
        lab, _, txt = r.partition("|")
        body = ('<div class="rlab">%s</div><div class="rtxt">%s</div>'
                % (lab.strip(), txt.strip())) if txt.strip() else (
               '<div class="rlab">%s</div>' % lab.strip())
        out.append('<div class="row"><div class="num">%02d</div>'
                   '<div>%s</div></div>' % (i, body))
    return '<div class="rows">%s</div>' % "".join(out)


def _launchlist_shell(kit, ad, s):
    """extra: camp, qual, promise, lede, rows, price_line, deliver, terms_line."""
    x = ad.extra
    bits = [
        '<div class="rail"><div>%s</div><div class="camp">%s</div></div>'
        % (_plain(kit.brand), x.get("camp", kit.eyebrow)),
        '<div><span class="callout">%s</span></div>' % ad.callout,
        '<div class="head">%s</div>' % ad.head,
    ]
    if x.get("qual"):
        bits.append('<div><span class="qual">%s</span></div>' % x["qual"])
    if x.get("promise"):
        bits.append('<div class="promise">%s</div>' % x["promise"])
    if x.get("lede"):
        bits.append('<div class="lede">%s</div>' % x["lede"])
    if ad.definition:
        bits.append('<div class="lede">%s</div>' % ad.definition)
    bits.append(_launchlist_rows(kit, ad, s))
    bits.append('<div class="grow"></div>')
    bits.append('<div class="price">%s</div>'
                % x.get("price_line", x.get("deliver", "")))
    bits.append('<div class="cta">%s</div>' % kit.cta)
    bits.append('<div class="terms">%s</div>'
                % x.get("terms_line", ad.proof))
    return "".join(bits)


LAYOUTS["launchlist"] = (_launchlist, _launchlist_shell)
PROVENANCE["launchlist"] = ("SC_Oct3|w9_20_hospital_admin and 10 sibling faces, Senior Consulting 3-5 Oct 2026, measured 0.67x par on 2,060 buyers", "-",
                        "Scaffolded 01 Oct 2026. Still a clone of notice until its CSS "
                        "is written.")


# ---------------------------------------------------------------- darkobject
# Built 1 Oct 2026 from the twenty-four live `SC_Oct3|dos_*` faces of Senior
# Consulting 3-5 Oct, which ran Rs 108 against a Rs 139 campaign par (0.78x) on
# 904 buyers while the same campaign's verb-headline faces ran 1.53x on 1,547.
# It is the second-cheapest design on this product and the only one that is not
# a list, which is why a wave can carry both without the faces reading the same.


def _contrast_pair(a, b):
    def lum(c):
        ch = [x / 255.0 for x in c]
        ch = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
              for x in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _lift(hexc, need=4.6):
    """Raise a light-page accent towards white until it reads on the dark ground.

    Every palette in the register is built for a light page, so its accent is a
    dark ink that would disappear on #07070A. Lifting it keeps "one palette per
    ad" meaningful here instead of making all ten dark faces identical.
    """
    import colorsys
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    hue, light, sat = colorsys.rgb_to_hls(r, g, b)
    # Raise LIGHTNESS and hold saturation. Blending towards white instead
    # desaturates, and ten dark faces then carry ten versions of the same grey:
    # #A8231C went to #BE5D58, which is not carmine any more.
    sat = min(1.0, max(sat, 0.55))
    for _ in range(60):
        rr, gg, bb = (int(round(c * 255))
                      for c in colorsys.hls_to_rgb(hue, light, sat))
        if _contrast_pair((rr, gg, bb), (7, 7, 10)) >= need:
            break
        light = min(0.92, light + 0.02)
    return "#%02X%02X%02X" % (rr, gg, bb)


def _darkobject(pal, s):
    """The dark spotlit face. Second cheapest design on Senior Consulting.

    WHAT IT TAKES FROM THE REFERENCE (`dos_erp_chair`, Rs 102, read off the live
    creative on 1 Oct 2026), in order:
      1. a pure near-black ground with one warm pool of light low in the frame
      2. a small centred brand lockup, sans over serif
      3. the ICP in large letter-spaced caps, cream, on nothing
      4. a serif display headline naming the DESTINATION as a noun phrase, the
         second clause in the palette's accent lifted for a dark ground
      5. two quiet lines: the barrier removed, then the promise
      6. the object, lit. OPTIONAL: pass extra["object"] and the photograph fills
         the lower half. Without one the same space carries the three named
         pieces of work on a lit panel, so the face never pools empty black --
         `adkit.gaps` blocks more than 200px of flat background in one place.
      7. two pill rows at the foot: the price, then the dates and the time

    WHAT IT DELIBERATELY HAS NOT GOT, like `launchlist`: a middle widget. Every
    1.53x face in this campaign carries an extra table, chip row or two-column
    panel between the headline and the list. Neither of this wave's designs does.
    """
    SERIF, SANS = _fonts()
    ground, cream = "#07070A", "#F2EFE9"
    acc = _lift(pal["accent"])
    return _base(pal, s) + [
        (".canvas", {"background": ground, "color": cream,
                     "font-family": SANS, "text-align": "center",
                     "background-image":
                         "radial-gradient(ellipse 70% 42% at 50% 78%,"
                         " rgba(255,236,208,.17) 0%, rgba(255,236,208,.06) 42%,"
                         " rgba(0,0,0,0) 72%)"}),
        (".lock .b", {"font-size": _px(26, s), "font-weight": "800",
                      "letter-spacing": ".30em", "text-transform": "uppercase",
                      "color": cream}),
        (".lock .c", {"font-family": SERIF, "font-size": _px(34, s),
                      "margin-top": _px(6, s), "color": "#DFDCD7"}),
        # Ruchika, 2 Oct 2026: "the ICP looks like it is part of the heading".
        # On the reference it is cream caps sitting straight on top of a cream
        # serif headline, so the two read as one block. A solid accent band with
        # the ground colour inside it makes it a label, the way the hard ink band
        # does on `launchlist`, and separates it from the destination line.
        (".callout", {"display": "inline-block", "background": acc,
                      "color": ground, "font-size": _idpx(64, s),
                      "font-weight": "900", "letter-spacing": ".02em",
                      "line-height": "1.1", "text-transform": "uppercase",
                      "margin-top": _px(36, s), "text-wrap": "balance",
                      "padding": "%s %s" % (_px(10, s), _px(20, s)),
                      "border-radius": _px(8, s)}),
        (".head", {"font-family": SERIF, "font-size": _idpx(90, s),
                   "font-weight": "700", "line-height": "1.04",
                   "letter-spacing": "-.015em", "margin-top": _px(28, s),
                   "color": cream, "text-wrap": "balance"}),
        (".head em", {"font-style": "normal", "color": acc}),
        (".qual", {"font-family": SERIF, "font-size": _barpx(34, s),
                   "margin-top": _px(22, s), "color": "#D5D2CD"}),
        (".lede", {"font-family": SERIF, "font-size": _px(31, s),
                   "line-height": "1.34", "margin-top": _px(10, s),
                   "color": "#CBC8C3"}),
        (".obj", {"margin-top": _px(18, s), "flex-shrink": "0",
                  "border-radius": _px(10, s), "overflow": "hidden"}),
        (".obj img", {"width": "100%", "display": "block"}),
        (".lit", {"margin-top": _px(26, s), "text-align": "left",
                  "border": "1px solid rgba(242,239,233,.22)",
                  "border-radius": _px(14, s),
                  "background": "rgba(242,239,233,.045)",
                  "padding": "%s %s" % (_px(20, s), _px(26, s))}),
        (".lit .r", {"display": "flex", "gap": _px(16, s),
                     "padding": "%s 0" % _px(11, s),
                     "border-top": "1px solid rgba(242,239,233,.13)"}),
        (".lit .n", {"font-size": _px(27, s), "font-weight": "900",
                     "color": acc, "min-width": _px(44, s)}),
        (".lit .l", {"font-size": _px(29, s), "font-weight": "800",
                     "line-height": "1.2", "color": cream}),
        (".lit .t", {"font-size": _px(25, s), "font-weight": "500",
                     "line-height": "1.3", "margin-top": _px(4, s),
                     "color": "#C6C3BE"}),
        # Ruchika, 2 Oct 2026: "there is no clear Join now button". The reference
        # ends on two informational pill rows and nothing that reads as a control,
        # and a small footer pill was rejected once already on 29 Sep 2026
        # ([[feedback_full_width_join_button]]). The button fills the line.
        (".price", {"font-size": _px(30, s), "font-weight": "800",
                    "color": cream, "margin-top": _px(22, s)}),
        (".cta", {"display": "block", "background": acc, "color": ground,
                  "text-align": "center", "font-size": _px(40, s),
                  "font-weight": "900", "border-radius": _px(10, s),
                  "margin-top": _px(14, s),
                  "padding": "%s %s" % (_px(22, s), _px(18, s))}),
        (".terms", {"font-size": _barpx(24, s), "font-weight": "800",
                    "letter-spacing": ".07em", "text-transform": "uppercase",
                    "color": "#BFBCB7", "margin-top": _px(14, s)}),
    ]


def _darkobject_shell(kit, ad, s):
    """extra: camp_title, qual, promise, lede, rows, object, when_line, deliver.

    `rows` are the same "LABEL | text" pairs `launchlist` takes, so the two
    designs for one reader carry byte-identical copy and `adkit.restyle` can move
    a face between them without touching a word.
    """
    x = ad.extra
    bits = [
        '<div class="lock"><div class="b">%s</div>'
        '<div class="c">%s</div></div>'
        % (_plain(kit.brand), x.get("camp_title", _plain(kit.eyebrow))),
        '<div class="callout">%s</div>' % ad.callout,
        '<div class="head">%s</div>' % ad.head,
    ]
    if x.get("qual"):
        bits.append('<div class="qual">%s</div>' % x["qual"])
    for key in ("promise", "lede"):
        if x.get(key):
            bits.append('<div class="lede">%s</div>' % x[key])
    if ad.definition:
        bits.append('<div class="lede">%s</div>' % ad.definition)
    if x.get("object"):
        bits.append('<div class="obj"><img src="../photos/%s" alt=""></div>'
                    % x["object"])
    else:
        rows = x.get("rows") or list(kit.takeaways)[:3]
        out = []
        for i, r in enumerate(rows, 1):
            lab, _, txt = r.partition("|")
            body = '<div class="l">%s</div>' % lab.strip()
            if txt.strip():
                body += '<div class="t">%s</div>' % txt.strip()
            out.append('<div class="r"><div class="n">%02d</div>'
                       '<div>%s</div></div>' % (i, body))
        bits.append('<div class="lit">%s</div>' % "".join(out))
    bits.append('<div class="grow"></div>')
    bits.append('<div class="price">%s</div>'
                % x.get("price_line", x.get("deliver", "")))
    bits.append('<div class="cta">%s</div>' % kit.cta)
    bits.append('<div class="terms">%s</div>'
                % x.get("terms_line", x.get("when_line", ad.proof)))
    return "".join(bits)


LAYOUTS["darkobject"] = (_darkobject, _darkobject_shell)
PROVENANCE["darkobject"] = (
    "SC_Oct3|dos_erp_chair and 23 sibling faces, Senior Consulting 3-5 Oct 2026",
    "Rs 108 / 0.78x par",
    "Built 1 Oct 2026. The dark spotlit face: near-black ground, one warm pool "
    "of light, cream caps and a serif destination headline. Takes a photographed "
    "object in extra['object']; without one the lit panel carries the named work.")


# ---------------------------------------------------------------- strucklist
# Scaffolded 01 Oct 2026 from: Three lines of what she is waiting for, each struck through, then the line that answers them
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _wf_mix(a, b, t):
    """Blend two hex colours. Used instead of `opacity` on text: simplicity R1 blocks
    faded type, and a mixed colour gives the same quietness without the fade."""
    a, b = a.lstrip("#"), b.lstrip("#")
    out = []
    for i in (0, 2, 4):
        ca, cb = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append(int(round(ca + (cb - ca) * t)))
    return "#%02X%02X%02X" % tuple(out)


def _wf_tint(pal, pct=0.12):
    """A pale ground for the delivery panel: the accent blended into the page.

    The palettes carry page/accent/ink/card/line and no tint, and a hardcoded
    off-white would make all twenty faces share one panel colour, which is the
    thing "every ad gets its own colour palette" exists to prevent.
    """
    def mix(a, b):
        a, b = a.lstrip("#"), b.lstrip("#")
        out = []
        for i in (0, 2, 4):
            ca, cb = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
            out.append(int(round(ca * (1 - pct) + cb * pct)))
        return "#%02X%02X%02X" % tuple(out)
    return mix(pal["page"], pal["accent"])


def _wf_chrome(pal, s):
    """The chassis both Women AI devices sit on, read off the live Oct creatives.

    The Oct wave was ONE skeleton with a swappable middle: thin brand rail, the
    ICP in an angled solid flag, a bold sans headline under a short accent rule,
    one quiet grey line, the device, the constant "WHAT WE DO IN 3 DAYS" panel,
    then a dark footer carrying the dates and the CTA. Keeping the chrome shared
    is what lets two faces in one wave differ by argument rather than by trim.
    """
    SERIF, SANS = _fonts()
    return _base(pal, s) + [
        (".canvas", {"background": pal["page"], "color": pal["ink"],
                     "font-family": SANS,
                     "border": "%s solid %s" % (_px(5, s), pal["accent"])}),
        # No `opacity` on any text here. simplicity R1 blocks faded type, and a
        # mixed colour reads the same without being faded.
        (".rail", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between",
                   "font-size": _px(26, s), "font-weight": "800",
                   "letter-spacing": ".13em", "text-transform": "uppercase",
                   "color": _wf_mix(pal["ink"], pal["page"], 0.28)}),
        (".rail .camp", {"color": pal["accent"]}),
        # the ICP, in a flag with one clipped corner
        (".callout", {"display": "inline-block", "background": pal["ink"],
                      "color": "#FFFFFF", "font-size": _idpx(66, s),
                      "font-weight": "800", "line-height": "1.14",
                      "letter-spacing": "-.005em", "text-transform": "uppercase",
                      "margin-top": _px(26, s), "text-wrap": "balance",
                      "clip-path": "polygon(0 0, 100%% 0, calc(100%% - %s) 100%%, 0 100%%)"
                                   % _px(34, s),
                      "padding": "%s %s %s %s" % (_px(14, s), _px(56, s),
                                                  _px(16, s), _px(26, s))}),
        # the headline. A plain statement, never a riddle: the reader's own
        # situation, then the plain offer. No wordplay, nothing withheld.
        (".head", {"font-size": _idpx(84, s), "font-weight": "800",
                   "line-height": "1.1", "letter-spacing": "-.025em",
                   "margin-top": _px(24, s), "text-wrap": "balance"}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".hrule", {"width": _px(220, s), "height": _px(7, s),
                    "background": pal["accent"], "margin-top": _px(20, s),
                    "border-radius": _px(4, s)}),
        (".sub", {"font-size": _barpx(31, s, 26), "font-weight": "500",
                  "line-height": "1.36", "margin-top": _px(26, s),
                  "color": _wf_mix(pal["ink"], pal["page"], 0.22)}),
        # the constant delivery panel
        (".deliver", {"background": _wf_tint(pal), "margin-top": _px(24, s),
                      "border-left": "%s solid %s" % (_px(9, s), pal["accent"]),
                      "padding": "%s %s %s %s" % (_px(22, s), _px(26, s),
                                                  _px(24, s), _px(28, s))}),
        (".deliver .dh", {"font-size": _barpx(26, s), "font-weight": "800",
                          "letter-spacing": ".16em", "text-transform": "uppercase",
                          "color": pal["accent"], "margin-bottom": _px(10, s)}),
        (".deliver .dt", {"font-size": _px(33, s), "font-weight": "700",
                          "line-height": "1.34", "color": pal["ink"]}),
        # the dark footer
        (".foot", {"background": pal["ink"], "display": "flex",
                   "align-items": "center", "justify-content": "space-between",
                   "gap": _px(18, s), "margin-top": _px(26, s),
                   "padding": "%s %s" % (_px(22, s), _px(26, s))}),
        (".foot .fd", {"font-size": _px(31, s), "font-weight": "800",
                       "color": "#FFFFFF", "line-height": "1.25"}),
        (".btn", {"background": pal["accent"], "color": "#FFFFFF",
                  "font-size": _px(33, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(16, s), _px(30, s)),
                  "border-radius": _px(8, s), "white-space": "nowrap"}),
        (".bigbtn", {"background": pal["accent"], "color": "#FFFFFF",
                     "text-align": "center", "font-size": _px(44, s),
                     "font-weight": "900", "margin-top": _px(22, s),
                     "border-radius": _px(12, s),
                     "padding": "%s %s" % (_px(24, s), _px(28, s))}),
    ]


def _wf_shell(kit, ad, s, device):
    """The shared shell. `device` is the HTML for the middle, and the only part
    that differs between the two layouts.

    Emits every copy field the contract names - callout, head, definition and
    extra["deliver"] - so `adkit.restyle` can move any ad between them.
    """
    x = ad.extra
    bits = [
        '<div class="rail"><div>%s</div><div class="camp">%s</div></div>'
        % (_plain(kit.brand), x.get("camp", kit.eyebrow)),
        '<div><span class="callout">%s</span></div>' % ad.callout,
        '<div class="head">%s</div>' % ad.head,
        '<div class="hrule"></div>',
    ]
    if ad.definition:
        bits.append('<div class="sub">%s</div>' % ad.definition)
    bits.append(device)
    bits.append('<div class="grow"></div>')
    bits.append('<div class="deliver"><div class="dh">%s</div>'
                '<div class="dt">%s</div></div>'
                % (x.get("deliver_title", "What we do in 3 days"),
                   x.get("deliver", kit.deliver if hasattr(kit, "deliver") else "")))
    if x.get("big_cta"):
        bits.append('<div class="bigbtn">%s</div>' % kit.cta)
        bits.append('<div class="foot"><div class="fd">%s</div></div>'
                    % x.get("foot_left", ad.proof))
    else:
        bits.append('<div class="foot"><div class="fd">%s</div>'
                    '<div class="btn">%s</div></div>'
                    % (x.get("foot_left", ad.proof), kit.cta))
    return "".join(bits)


def _strucklist(pal, s):
    """The struck list. Read off `WF_11_CPP112_R3_stop_waiting`, which ran 0.82x
    par on 3,104 registrations in WomenAI_FREE_3-5Oct, and its palette variant
    `WF_ALT_11` at 0.97x on 2,223 - together 0.88x on 5,327, the only design on
    this product that is under par with a band that clears 1.0 (+/-3%).

    WHAT IT TAKES FROM THE REFERENCE, in order:
      1. the shared chassis rail and ICP flag
      2. a bold sans headline stating the offer plainly, then a short accent rule
      3. one quiet line underneath
      4. THE DEVICE: three things she is waiting for, each struck through, then
         one line in the accent colour that answers all three. The strike is the
         whole argument - it says the waiting is the problem, not her.
      5. the constant delivery panel, then the dark footer

    WHAT IT DELIBERATELY HAS NOT GOT: a fourth struck line. On the live face the
    panel is three and a verdict; a longer list reads as a complaint, and
    `simplicity.py` counts words on the face.

    The struck lines come from extra["waiting"]; extra["verdict"] is the answer.
    """
    return _wf_chrome(pal, s) + [
        (".waits", {"background": "#FFFFFF", "margin-top": _px(28, s),
                    "border-left": "%s solid %s" % (_px(9, s), pal["accent"]),
                    "padding": "%s %s %s %s" % (_px(26, s), _px(26, s),
                                                _px(28, s), _px(30, s))}),
        (".waits .w", {"font-size": _px(36, s), "font-weight": "800",
                       "line-height": "1.3", "color": pal["ink"],
                       "text-decoration": "line-through",
                       "text-decoration-thickness": _px(4, s),
                       "padding": "%s 0" % _px(9, s)}),
        (".waits .v", {"font-size": _px(36, s), "font-weight": "800",
                       "line-height": "1.3", "color": pal["accent"],
                       "margin-top": _px(16, s)}),
    ]


def _strucklist_shell(kit, ad, s):
    """extra: camp, waiting (list of 3), verdict, deliver, foot_left, big_cta."""
    x = ad.extra
    waits = list(x.get("waiting") or [])[:3]
    rows = "".join('<div class="w">%s</div>' % w for w in waits)
    verdict = x.get("verdict", "")
    if verdict:
        rows += '<div class="v">%s</div>' % verdict
    device = '<div class="waits">%s</div>' % rows if rows else ""
    return _wf_shell(kit, ad, s, device)


LAYOUTS["strucklist"] = (_strucklist, _strucklist_shell)
PROVENANCE["strucklist"] = ("WF_11_CPP112_R3_stop_waiting + WF_ALT_11, WomenAI_FREE_3-5Oct-2026", "0.88x par",
                        "Built 01 Oct 2026 off the live creatives. 5,327 registrations, "
                        "+/-3%. The only Women AI design under par with a clean band.")


# ---------------------------------------------------------------- clockband
# Scaffolded 01 Oct 2026 from: A horizontal band from the hour the house goes quiet to the hour it fills again, with her work named in the middle
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _clockband(pal, s):
    """The clock band. Read off `R2_school_hours` (0.91x par on 308 Rs10 buyers,
    Sep), `N02_teacher_evening` (0.98x on 496, Sep) and the Oct refresh
    `WF_04_CPP90_R2_school_hours` (0.59x on 52) - together 0.93x on 856, +/-7%,
    the second design on this product that is under par.

    WHAT IT TAKES FROM THE REFERENCE: the same chassis, with the middle replaced
    by a single horizontal band - the hour her time opens on the left, the hour
    it closes on the right, and the work named in the accent colour across the
    middle. It is the only device here that shows a QUANTITY of time rather than
    describing one, which is why it carries the hours ICPs and the struck list
    carries the money-pressure ones.

    WHAT IT DELIBERATELY HAS NOT GOT: a second row. The live faces carry exactly
    one band; a second turns it into a timetable and the eye stops reading it in
    one pass.

    extra["band"] is (left_time, left_label, centre_label, right_time, right_label).
    """
    return _wf_chrome(pal, s) + [
        (".band", {"background": "#FFFFFF", "margin-top": _px(28, s),
                   "border-left": "%s solid %s" % (_px(9, s), pal["accent"]),
                   "display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(16, s),
                   "padding": "%s %s" % (_px(26, s), _px(28, s))}),
        # No `white-space: nowrap` here. A long time string ("9 PM to 6 AM") on a
        # flex child with nowrap runs straight past the band's own box, which is
        # what adkit.fit F7 caught on 05_night_shift and 06_nurses_rotating.
        # Wrapping is the fix; the band stays one row either way.
        (".band .t", {"font-size": _px(52, s), "font-weight": "900",
                      "line-height": "1.05", "color": pal["ink"],
                      "max-width": _px(300, s), "overflow-wrap": "break-word"}),
        (".band .l", {"font-size": _barpx(24, s), "font-weight": "800",
                      "letter-spacing": ".10em", "text-transform": "uppercase",
                      "color": _wf_mix(pal["ink"], pal["page"], 0.30),
                      "margin-top": _px(6, s), "max-width": _px(300, s)}),
        (".band .mid", {"flex": "1", "text-align": "center",
                        "padding": "0 %s" % _px(8, s)}),
        (".band .mid .ml", {"font-size": _barpx(26, s), "font-weight": "800",
                            "letter-spacing": ".12em",
                            "text-transform": "uppercase",
                            "color": pal["accent"], "line-height": "1.25"}),
        (".band .mid .mr", {"height": _px(8, s), "background": pal["accent"],
                            "border-radius": _px(4, s),
                            "margin-top": _px(12, s)}),
        (".band .r", {"text-align": "right"}),
    ]


def _clockband_shell(kit, ad, s):
    """extra: camp, band (5-tuple), deliver, foot_left, big_cta."""
    x = ad.extra
    b = x.get("band")
    device = ""
    if b:
        lt, ll, mid, rt, rl = b
        device = ('<div class="band">'
                  '<div><div class="t">%s</div><div class="l">%s</div></div>'
                  '<div class="mid"><div class="ml">%s</div>'
                  '<div class="mr"></div></div>'
                  '<div class="r"><div class="t">%s</div>'
                  '<div class="l">%s</div></div></div>'
                  % (lt, ll, mid, rt, rl))
    return _wf_shell(kit, ad, s, device)


LAYOUTS["clockband"] = (_clockband, _clockband_shell)
PROVENANCE["clockband"] = ("R2_school_hours + N02_teacher_evening + WF_04, Women AI Sep and Oct", "0.93x par",
                        "Built 01 Oct 2026 off the live creatives. 856 results, +/-7%. "
                        "Carries the hours ICPs; strucklist carries the money ones.")
