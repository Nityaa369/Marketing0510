#!/usr/bin/env python3
"""Five borrowed-format face layouts, lifted from the reference set Ramanuj sent
on 1 September 2026.

WHY THIS FILE EXISTS. `layouts.py` holds the five house skeletons, each lifted
from a face that was approved AND priced: notice, serif, ladder, nameplate,
docket. All five are editorial - paper, serif display, ruled tables. The
reference set sent on 1 Sep 2026 is a different family entirely: flat social
formats with almost no furniture, a single drawn object, and the whole message
carried by two lines of type.

  1  an assistant chat thread, product held to the sky, prompt and one-line reply
  2  THIS IS YOUR / *sign* in heavy sans plus script, over a fortune cookie whose
     paper slip carries the message
  3  a two-panel stick-figure exchange, saturated ground, white panels
  4  a single stick figure at a desk, cream ground, thin accent frame, a pill
     label naming who the figure is
  5  a pixel-art device on a flat bright ground, question headline under it

None of these five has a live cost on this account, and that has to be said
plainly rather than buried. `SOP/00` section 2 records the two shapes that DO
have one and both are worse than par: pay chart 2.34 and toon/chat 1.22. The
`duo` and `chatui` layouts below are in the toon/chat family. They are being
built because they were asked for by name, and the honest read is that this wave
is a test of the family, not a bet on it. Judge the cells against campaign par
and kill the family if it repeats 1.22.

WHAT EVERY LAYOUT HERE STILL GUARANTEES, because these are the defects that have
actually shipped from this repo:

  * `.callout` and `.head` are emitted as REAL CLASSES with a REAL font-size in
    the stylesheet, never inline. `ad_lint` C8 matches on the class name, and the
    25 Aug 2026 silent pass was a generator that emitted inline styles only.
  * Both are clamped at their 64px floor whatever the auto-fit scale, so a tight
    face is absorbed by body type and never by identity type.
  * Nothing is positioned absolutely and nothing overlaps by construction, so
    `adkit.fit` can still see clipping as clipping. The fortune slip sits BETWEEN
    the two cookie halves in a flex row rather than on top of them, for exactly
    this reason.
  * Every drawn object is inline SVG or a CSS grid, so there is no external asset
    to go missing and no photograph to license.

The memory note this satisfies: *each ad in a batch needs its own layout
skeleton, not one template with a swapped widget*, and *lean into named formats*.
"""

W, H = 1080, 1350
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
SCRIPT = "'Segoe Script','Brush Script MT','Apple Chancery',cursive"
GUTTER = 60

PROVENANCE = {
    "chatui": ("reference set 1 Sep 2026, sheet 1", "-",
               "An assistant chat thread. Prompt is the ICP, reply is the turn. "
               "toon/chat family, index 1.22 - test, do not scale blind."),
    "fortune": ("reference set 1 Sep 2026, sheet 2", "-",
                "THIS IS YOUR / sign in sans plus script, over a cookie whose "
                "paper slip carries the promise."),
    "duo": ("reference set 1 Sep 2026, sheet 3", "-",
            "Two-panel stick-figure exchange on a saturated ground. The "
            "objection on the left, the answer on the right."),
    "desk": ("reference set 1 Sep 2026, sheet 4", "-",
             "One stick figure in a scene, thin accent frame, pill label naming "
             "who the figure is."),
    "pixel": ("reference set 1 Sep 2026, sheet 5", "-",
              "A pixel-art device on a flat bright ground, question headline "
              "under it."),
}


def _px(n, s):
    return "%dpx" % round(n * s)


def _idpx(n, s, floor=64):
    """Identity type never goes under its C8 floor, whatever the scale."""
    return "%dpx" % max(round(n * s), floor)


def _plain(s):
    out, keep = [], True
    for ch in s:
        if ch == "<":
            keep = False
        elif ch == ">":
            keep = True
        elif keep:
            out.append(ch)
    return "".join(out)


def _ground(pal):
    """Saturated ground for the flat formats, falling back to the paper page so a
    palette without one still renders."""
    return pal.get("bright", pal["page"])


def _base(pal, s, ground=None):
    return [
        ("*", {"margin": "0", "padding": "0", "box-sizing": "border-box"}),
        ("html,body", {"width": _px(W, 1), "height": _px(H, 1), "overflow": "hidden"}),
        ("body", {"font-family": SANS, "background": ground or pal["page"],
                  "color": pal["ink"]}),
        (".canvas", {"width": _px(W, 1), "height": _px(H, 1),
                     "padding": "%s %s %s" % (_px(44, s), _px(GUTTER, 1), _px(40, s)),
                     "display": "flex", "flex-direction": "column"}),
        (".grow", {"flex": "1", "min-height": "0"}),
    ]


# ------------------------------------------------------------------- figures
# Stick figures, inline. Head, spine, two arms, two legs, and one detail that
# carries the mood. Deliberately crude: the reference sheets are crude, and a
# careful drawing here would read as a different format.

def _fig_sad(ink, s):
    k = 1.25 * s
    return (
        '<svg class="fig" viewBox="0 0 200 240" width="%d" height="%d" '
        'aria-hidden="true">'
        '<g fill="none" stroke="%s" stroke-width="7" stroke-linecap="round">'
        '<circle cx="100" cy="62" r="52"/>'
        '<path d="M100 114 L100 186"/>'
        '<path d="M100 132 L58 168"/><path d="M100 132 L142 160"/>'
        '<path d="M100 186 L70 236"/><path d="M100 186 L130 236"/>'
        '<path d="M80 92 q20 -16 40 0"/>'
        '</g>'
        '<circle cx="80" cy="52" r="7" fill="%s"/>'
        '<circle cx="120" cy="52" r="7" fill="%s"/>'
        '<path d="M78 62 q-6 16 2 26" fill="none" stroke="%s" stroke-width="5" '
        'stroke-linecap="round"/>'
        '</svg>' % (round(150 * k), round(180 * k), ink, ink, ink, ink))


def _fig_cool(ink, s):
    k = 1.25 * s
    return (
        '<svg class="fig" viewBox="0 0 200 240" width="%d" height="%d" '
        'aria-hidden="true">'
        '<g fill="none" stroke="%s" stroke-width="7" stroke-linecap="round">'
        '<circle cx="100" cy="62" r="52"/>'
        '<path d="M100 114 L100 186"/>'
        '<path d="M100 132 L52 120"/><path d="M100 132 L148 150"/>'
        '<path d="M100 186 L70 236"/><path d="M100 186 L130 236"/>'
        '<path d="M80 84 q20 18 40 0"/>'
        '</g>'
        '<rect x="62" y="42" width="76" height="20" rx="5" fill="%s"/>'
        '</svg>' % (round(150 * k), round(180 * k), ink, ink))


def _fig_desk(ink, s):
    """Seated, elbow on a desk, looking at a monitor. Sheet 4."""
    k = 1.5 * s
    return (
        '<svg class="fig" viewBox="0 0 420 260" width="%d" height="%d" '
        'aria-hidden="true">'
        '<g fill="none" stroke="%s" stroke-width="7" stroke-linecap="round" '
        'stroke-linejoin="round">'
        '<path d="M30 214 L250 214 L286 246 L66 246 Z"/>'
        '<rect x="58" y="120" width="118" height="86" rx="5"/>'
        '<path d="M176 128 L206 112 L206 190 L176 206"/>'
        '<path d="M186 216 L240 216"/>'
        '<circle cx="330" cy="96" r="50"/>'
        '<path d="M330 146 L330 206"/>'
        '<path d="M330 166 L272 210"/>'
        '<path d="M330 172 L378 214"/>'
        '<path d="M306 118 q24 -12 48 0"/>'
        '</g>'
        '<path d="M308 88 q10 8 22 0" fill="none" stroke="%s" stroke-width="6" '
        'stroke-linecap="round"/>'
        '<path d="M338 88 q10 8 22 0" fill="none" stroke="%s" stroke-width="6" '
        'stroke-linecap="round"/>'
        '</svg>' % (round(400 * k), round(248 * k), ink, ink, ink))


FIGURES = {"sad": _fig_sad, "cool": _fig_cool, "desk": _fig_desk}


def _figure(kind, ink, s):
    return FIGURES.get(kind, _fig_cool)(ink, s)


# ----------------------------------------------------------------- pixel art
# A matrix of characters becomes a grid of squares. '#' is ink, '.' is empty,
# '+' is the accent. Sheet 5 is the Chrome offline dinosaur; anything drawable
# on a 16-wide grid works, and the grid is what makes it read as pixel art
# rather than as clipart.

def _pixel_grid(rows, ink, accent, cell):
    w = max(len(r) for r in rows)
    cells = []
    for r in rows:
        r = r.ljust(w, ".")
        for ch in r:
            if ch == "#":
                cells.append('<i style="background:%s"></i>' % ink)
            elif ch == "+":
                cells.append('<i style="background:%s"></i>' % accent)
            else:
                cells.append("<i></i>")
    return ('<div class="pix" style="grid-template-columns:repeat(%d,%dpx)">%s</div>'
            % (w, cell, "".join(cells)))


# ---------------------------------------------------------------------- chatui
# REBUILT 1 Sep 2026 after the first version was rejected on sight: "not well
# designed". Three faults, all real:
#
#   1. The hero was a grey wrapper around a white card of grey placeholder bars.
#      Sheet 1 holds a real product photograph; grey bars are a wireframe, and a
#      wireframe on a finished ad reads as unfinished work. Replaced with a real
#      commission card that carries actual words the reader would be paid to
#      write, and it is now OPTIONAL - a face with nothing true to put in it
#      renders without one rather than filling the space with furniture.
#   2. The reply was unattributed 66px text floating under the bubble, so the
#      thread stopped reading as a thread at exactly the point that matters.
#      It now carries an avatar and sits in an answer row.
#   3. Three full-width blocks on three different alignments (card centred,
#      bubble right, headline left) and no focal point. Everything below the
#      bubble now shares one left edge.


def _chatui(pal, s):
    return _base(pal, s, "#FFFFFF") + [
        (".canvas", {"width": _px(W, 1), "height": _px(H, 1),
                     "padding": "%s %s %s" % (_px(38, s), _px(52, 1), _px(36, s)),
                     "display": "flex", "flex-direction": "column"}),
        (".cbar", {"display": "flex", "align-items": "center",
                   "gap": _px(16, s), "padding-bottom": _px(20, s),
                   "border-bottom": "2px solid #ECECEC"}),
        (".cbar .mk", {"width": _px(34, s), "height": _px(26, s),
                       "border-top": "5px solid " + pal["ink"],
                       "border-bottom": "5px solid " + pal["ink"]}),
        (".cbar .nm", {"font-size": _px(31, s), "font-weight": "800"}),
        (".cbar .nm i", {"font-style": "normal", "color": pal["accent"]}),
        (".cbar .sp", {"flex": "1"}),
        (".cbar .dot", {"width": _px(26, s), "height": _px(26, s),
                        "border": "3px solid #BFBFBF", "border-radius": "50%"}),
        # the commission card: a real brief, not placeholder bars
        (".brief", {"border": "3px solid #E6E6EA", "border-radius": _px(20, s),
                    "margin-top": _px(26, s), "overflow": "hidden"}),
        (".brief .bh", {"background": pal["accent"], "color": "#fff",
                        "font-size": _px(23, s), "font-weight": "800",
                        "letter-spacing": ".16em", "text-transform": "uppercase",
                        "padding": "%s %s" % (_px(12, s), _px(24, s))}),
        (".brief .bb", {"padding": "%s %s" % (_px(20, s), _px(24, s))}),
        (".brief .t", {"font-size": _px(34, s), "font-weight": "800",
                       "line-height": "1.2"}),
        (".brief .m", {"font-size": _px(26, s), "font-weight": "700",
                       "color": "#6A6A72", "margin-top": _px(8, s)}),
        (".askrow", {"display": "flex", "justify-content": "flex-end",
                     "margin-top": _px(28, s)}),
        (".callout", {"background": "#F0F0F2", "border-radius": _px(28, s),
                      "border-bottom-right-radius": _px(8, s),
                      "font-size": _idpx(64, s), "font-weight": "700",
                      "line-height": "1.14", "letter-spacing": "-.02em",
                      "padding": "%s %s" % (_px(22, s), _px(30, s)),
                      "max-width": "80%", "text-align": "left"}),
        (".ansrow", {"display": "flex", "gap": _px(20, s),
                     "align-items": "flex-start", "margin-top": _px(28, s)}),
        (".av", {"flex": "0 0 auto", "width": _px(54, s), "height": _px(54, s),
                 "border-radius": "50%", "background": pal["accent"],
                 "color": "#fff", "font-size": _px(26, s), "font-weight": "900",
                 "display": "flex", "align-items": "center",
                 "justify-content": "center", "margin-top": _px(8, s)}),
        (".ans", {"flex": "1", "min-width": "0"}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "800",
                   "line-height": "1.14", "letter-spacing": "-.025em"}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".def", {"font-size": _px(29, s), "line-height": "1.42",
                  "margin-top": _px(18, s), "color": "#3A3A3A"}),
        (".deliver", {"font-size": _px(28, s), "font-weight": "800",
                      "line-height": "1.36", "margin-top": _px(16, s),
                      "color": pal["accent"]}),
        (".proofline", {"font-size": _px(27, s), "font-weight": "800",
                        "line-height": "1.32", "margin-top": _px(14, s),
                        "color": "#3A3A3A"}),
        (".inbar", {"display": "flex", "align-items": "center",
                    "gap": _px(18, s), "border": "3px solid #E3E3E3",
                    "border-radius": "999px",
                    "padding": "%s %s" % (_px(12, s), _px(20, s)),
                    "margin-top": _px(20, s)}),
        (".inbar .plus", {"font-size": _px(34, s), "color": "#9A9A9A",
                          "font-weight": "700"}),
        (".inbar .ph", {"flex": "1", "font-size": _px(29, s), "color": "#8A8A8A"}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(29, s), "font-weight": "800",
                  "border-radius": "999px", "white-space": "nowrap",
                  "padding": "%s %s" % (_px(14, s), _px(28, s))}),
        (".terms", {"font-size": _px(26, s), "font-weight": "700",
                    "line-height": "1.34", "text-align": "center",
                    "margin-top": _px(16, s), "color": "#4A4A4A"}),
        (".terms b", {"font-weight": "800", "color": pal["ink"]}),
    ]


def _chatui_shell(kit, ad, s):
    x = ad.extra
    brief = ""
    if x.get("brief_title"):
        brief = ('<div class="brief"><div class="bh">%s</div>'
                 '<div class="bb"><div class="t">%s</div>'
                 '<div class="m">%s</div></div></div>'
                 % (x.get("brief_head", "A commission"), x["brief_title"],
                    x.get("brief_meta", "")))
    return (
        '<div class="cbar"><div class="mk"></div>'
        '<div class="nm">%s</div><div class="sp"></div>'
        '<div class="dot"></div></div>'
        '%s'
        '<div class="askrow"><div class="callout">%s</div></div>'
        '<div class="ansrow"><div class="av">SA</div><div class="ans">'
        '<div class="head">%s</div>'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proofline">%s</div>'
        '</div></div>'
        '<div class="grow"></div>'
        '<div class="inbar"><div class="plus">+</div>'
        '<div class="ph">%s</div><div class="btn">%s</div></div>'
        '<div class="terms">%s</div>'
        % (kit.brand, brief, ad.callout, ad.head, ad.definition,
           x.get("deliver", ""), ad.proof,
           x.get("placeholder", "Ask anything"), kit.cta, kit.terms))


# --------------------------------------------------------------------- fortune

def _fortune(pal, s):
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(28, s), "font-weight": "900",
                    "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(22, s), "font-weight": "800",
                      "letter-spacing": ".16em", "text-transform": "uppercase",
                      "color": pal["accent"]}),
        (".callout", {"font-size": _idpx(88, s), "font-weight": "900",
                      "line-height": "1.0", "letter-spacing": "-.03em",
                      "text-transform": "uppercase", "text-align": "center",
                      "margin-top": _px(40, s)}),
        # line-height 1.08 was set from the sans metrics and a script face does
        # not fit in it: on a two-line call-out the ascenders of head line 2 rode
        # up into .callout, and adkit.fit reported F2 OVERLAP 527x12px on
        # 15_commerce_law. Script needs a line box of its own.
        (".head", {"font-family": SCRIPT, "font-size": _idpx(78, s),
                   "font-weight": "700", "line-height": "1.3",
                   "text-align": "center", "margin-top": _px(16, s),
                   "color": pal["accent"]}),
        (".head em", {"font-style": "italic"}),
        (".cookie", {"display": "flex", "align-items": "center",
                     "justify-content": "center", "gap": "0",
                     "margin-top": _px(30, s)}),
        # The cookie halves are clipped rounded triangles rather than CSS border
        # triangles: a border triangle has a hard 90 degree corner and reads as a
        # traffic sign. Each half leans in toward the slip, which is what makes
        # the object read as one broken cookie rather than two shapes.
        (".half", {"flex": "0 0 auto", "display": "block"}),
        (".half.l", {"transform": "rotate(-7deg)"}),
        (".half.r", {"transform": "rotate(7deg) scaleX(-1)"}),
        (".slip", {"background": "#FFFFFF", "flex": "1",
                   "border": "2px solid #DCD6C6",
                   "padding": "%s %s" % (_px(26, s), _px(18, s)),
                   "text-align": "center", "font-size": _px(33, s),
                   "font-weight": "800", "line-height": "1.26",
                   "letter-spacing": ".01em",
                   "box-shadow": "0 8px 22px rgba(0,0,0,.10)"}),
        (".def", {"font-size": _px(28, s), "line-height": "1.42",
                  "text-align": "center", "margin-top": _px(30, s),
                  "padding": "0 %s" % _px(10, s)}),
        (".deliver", {"font-size": _px(28, s), "font-weight": "800",
                      "line-height": "1.36", "text-align": "center",
                      "margin-top": _px(16, s), "color": pal["accent"]}),
        # ad.proof was silently dropped by all five of these shells on the
        # first build, which is the identical defect layouts.py records
        # against `nameplate`: a blind reader could not answer "am I
        # eligible" because the qualifier never reached the face. The
        # APPROVED corpus carries a negation qualifier on 37% of blocks.
        (".proofline", {"font-size": _px(27, s), "font-weight": "800",
                        "line-height": "1.3", "text-align": "center",
                        "margin-top": _px(12, s)}),
        (".rule", {"border-top": "3px solid " + pal["ink"], "margin-top": _px(22, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(20, s),
                   "margin-top": _px(20, s)}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(30, s), "font-weight": "800",
                  "border-radius": "999px", "white-space": "nowrap",
                  "padding": "%s %s" % (_px(16, s), _px(30, s))}),
        (".terms", {"font-size": _px(26, s), "font-weight": "700",
                    "line-height": "1.34", "text-align": "right", "flex": "1"}),
        (".terms b", {"font-weight": "800"}),
    ]


def _cookie_half(cls, s):
    """One half of a broken fortune cookie: a rounded wedge with a curved base
    and a fold arc across it. Sheet 2."""
    w, h = round(200 * s), round(216 * s)
    return (
        '<svg class="half %s" viewBox="0 0 200 216" width="%d" height="%d" '
        'aria-hidden="true">'
        '<path d="M100 14 C140 58 176 138 186 194 C132 208 68 208 14 194 '
        'C24 138 60 58 100 14 Z" fill="#E3A863"/>'
        '<path d="M100 14 C140 58 176 138 186 194 C160 200 132 203 104 204 '
        'L100 14 Z" fill="#CE8B3C"/>'
        '<path d="M46 150 C86 132 118 132 156 154" fill="none" stroke="#B0702B" '
        'stroke-width="6" stroke-linecap="round"/>'
        '</svg>' % (cls, w, h))


def _fortune_shell(kit, ad, s):
    x = ad.extra
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="grow"></div>'
        '<div class="cookie">%s'
        '<div class="slip">%s</div>%s</div>'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proofline">%s</div>'
        '<div class="grow"></div>'
        '<div class="rule"></div>'
        '<div class="foot"><div class="btn">%s</div>'
        '<div class="terms">%s</div></div>'
        % (kit.brand, kit.eyebrow, ad.callout, ad.head,
           _cookie_half("l", s), x.get("slip", ""), _cookie_half("r", s),
           ad.definition, x.get("deliver", ""), ad.proof, kit.cta, kit.terms))


# ------------------------------------------------------------------------- duo

def _duo(pal, s):
    g = _ground(pal)
    return _base(pal, s, g) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(28, s), "font-weight": "900",
                    "letter-spacing": ".12em", "text-transform": "uppercase",
                    "color": "#FFFFFF"}),
        (".brand i", {"font-style": "normal", "color": "#FFFFFF"}),
        (".eyebrow", {"font-size": _px(22, s), "font-weight": "800",
                      "letter-spacing": ".16em", "text-transform": "uppercase",
                      "color": "#FFFFFF"}),
        (".callout", {"background": "#FFFFFF", "color": pal["ink"],
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.06", "letter-spacing": "-.025em",
                      "text-transform": "uppercase", "text-align": "center",
                      "border-radius": _px(18, s), "margin-top": _px(26, s),
                      "padding": "%s %s" % (_px(18, s), _px(24, s))}),
        (".panels", {"display": "flex", "gap": _px(18, s), "margin-top": _px(24, s)}),
        (".pnl", {"flex": "1", "background": "#FFFFFF",
                  "border-radius": _px(22, s),
                  "padding": "%s %s %s" % (_px(24, s), _px(22, s), _px(16, s)),
                  "display": "flex", "flex-direction": "column",
                  "align-items": "center", "text-align": "center"}),
        (".bub", {"background": "#F0F0F0", "color": pal["ink"],
                  "border-radius": _px(18, s), "font-size": _px(30, s),
                  "font-weight": "700", "line-height": "1.26",
                  "padding": "%s %s" % (_px(16, s), _px(18, s)), "width": "100%"}),
        (".bub.a", {"background": pal["accent"], "color": "#FFFFFF",
                    "font-weight": "800"}),
        (".fig", {"margin-top": _px(14, s), "display": "block"}),
        (".pnl .fig", {"margin-top": "auto"}),
        (".head", {"background": "#FFFFFF", "border-radius": _px(20, s),
                   "font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.025em",
                   "margin-top": _px(20, s),
                   "padding": "%s %s" % (_px(20, s), _px(24, s))}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".slab", {"background": "#FFFFFF", "border-radius": _px(20, s),
                   "margin-top": _px(16, s),
                   "padding": "%s %s" % (_px(20, s), _px(24, s))}),
        (".def", {"font-size": _px(28, s), "line-height": "1.4"}),
        (".deliver", {"font-size": _px(27, s), "font-weight": "800",
                      "line-height": "1.34", "margin-top": _px(12, s),
                      "color": pal["accent"]}),
        # ad.proof was silently dropped by all five of these shells on the
        # first build, which is the identical defect layouts.py records
        # against `nameplate`: a blind reader could not answer "am I
        # eligible" because the qualifier never reached the face. The
        # APPROVED corpus carries a negation qualifier on 37% of blocks.
        (".proofline", {"font-size": _px(27, s), "font-weight": "800",
                        "line-height": "1.3", "margin-top": _px(10, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(20, s),
                   "margin-top": _px(18, s)}),
        (".btn", {"background": "#FFFFFF", "color": pal["accent"],
                  "font-size": _px(30, s), "font-weight": "900",
                  "border-radius": "999px", "white-space": "nowrap",
                  "padding": "%s %s" % (_px(16, s), _px(30, s))}),
        (".terms", {"font-size": _px(26, s), "font-weight": "800",
                    "line-height": "1.34", "text-align": "right", "flex": "1",
                    "color": "#FFFFFF"}),
        (".terms b", {"font-weight": "900"}),
    ]


def _duo_shell(kit, ad, s):
    x = ad.extra
    left, right = x.get("bubbles", ("", ""))
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="grow"></div>'
        '<div class="panels">'
        '<div class="pnl"><div class="bub">%s</div>%s</div>'
        '<div class="pnl"><div class="bub a">%s</div>%s</div>'
        '</div>'
        '<div class="head">%s</div>'
        '<div class="slab"><div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proofline">%s</div></div>'
        '<div class="grow"></div>'
        '<div class="foot"><div class="btn">%s</div>'
        '<div class="terms">%s</div></div>'
        % (kit.brand, kit.eyebrow, ad.callout,
           left, _figure("sad", ad.pal["ink"], s),
           right, _figure("cool", ad.pal["ink"], s),
           ad.head, ad.definition, x.get("deliver", ""), ad.proof,
           kit.cta, kit.terms))


# ------------------------------------------------------------------------ desk

def _desk(pal, s):
    return _base(pal, s) + [
        (".canvas", {"width": _px(W, 1), "height": _px(H, 1),
                     "padding": _px(34, 1), "display": "flex",
                     "flex-direction": "column"}),
        (".frame", {"flex": "1", "min-height": "0",
                    "border": "4px solid " + pal["accent"],
                    "padding": "%s %s %s" % (_px(34, s), _px(38, s), _px(30, s)),
                    "display": "flex", "flex-direction": "column"}),
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(28, s), "font-weight": "900",
                    "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(22, s), "font-weight": "800",
                      "letter-spacing": ".16em", "text-transform": "uppercase",
                      "color": "#8A8A8A"}),
        (".callout", {"font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.08", "letter-spacing": "-.025em",
                      "color": pal["accent"], "margin-top": _px(30, s)}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.025em",
                   "margin-top": _px(8, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".stage", {"display": "flex", "justify-content": "center",
                    "margin-top": _px(10, s)}),
        (".pillrow", {"display": "flex", "justify-content": "center",
                      "margin-top": _px(10, s)}),
        (".pill", {"background": pal["accent"], "color": "#fff",
                   "font-size": _px(30, s), "font-weight": "800",
                   "border-radius": "999px",
                   "padding": "%s %s" % (_px(14, s), _px(30, s))}),
        (".def", {"font-size": _px(28, s), "line-height": "1.42",
                  "margin-top": _px(24, s)}),
        (".deliver", {"font-size": _px(27, s), "font-weight": "800",
                      "line-height": "1.34", "margin-top": _px(14, s),
                      "color": pal["accent"]}),
        # ad.proof was silently dropped by all five of these shells on the
        # first build, which is the identical defect layouts.py records
        # against `nameplate`: a blind reader could not answer "am I
        # eligible" because the qualifier never reached the face. The
        # APPROVED corpus carries a negation qualifier on 37% of blocks.
        (".proofline", {"font-size": _px(27, s), "font-weight": "800",
                        "line-height": "1.3", "margin-top": _px(10, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(20, s),
                   "margin-top": _px(18, s), "padding-top": _px(18, s),
                   "border-top": "3px solid " + pal["line"]}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(30, s), "font-weight": "800",
                  "border-radius": "8px", "white-space": "nowrap",
                  "padding": "%s %s" % (_px(16, s), _px(30, s))}),
        (".terms", {"font-size": _px(26, s), "font-weight": "700",
                    "line-height": "1.34", "text-align": "right", "flex": "1"}),
        (".terms b", {"font-weight": "800"}),
    ]


def _desk_shell(kit, ad, s):
    x = ad.extra
    return (
        '<div class="frame">'
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="grow"></div>'
        '<div class="stage">%s</div>'
        '<div class="pillrow"><div class="pill">%s</div></div>'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proofline">%s</div>'
        '<div class="grow"></div>'
        '<div class="foot"><div class="btn">%s</div>'
        '<div class="terms">%s</div></div>'
        '</div>'
        % (kit.brand, kit.eyebrow, ad.callout, ad.head,
           _figure(x.get("figure", "desk"), ad.pal["ink"], s),
           x.get("pill", ""), ad.definition, x.get("deliver", ""), ad.proof,
           kit.cta, kit.terms))


# ----------------------------------------------------------------------- pixel

def _pixel(pal, s):
    g = _ground(pal)
    return _base(pal, s, g) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(30, s), "font-weight": "900",
                    "letter-spacing": ".1em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal"}),
        (".eyebrow", {"font-size": _px(22, s), "font-weight": "800",
                      "letter-spacing": ".16em", "text-transform": "uppercase"}),
        (".stage", {"display": "flex", "justify-content": "center",
                    "margin-top": _px(10, s)}),
        (".pix", {"display": "grid", "gap": "2px"}),
        (".pix i", {"display": "block", "width": _px(22, s), "height": _px(22, s)}),
        (".callout", {"font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.08", "letter-spacing": "-.028em",
                      "text-align": "center", "margin-top": _px(28, s)}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.028em",
                   "text-align": "center", "margin-top": _px(10, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".def", {"font-size": _px(29, s), "line-height": "1.42",
                  "text-align": "center", "margin-top": _px(24, s),
                  "padding": "0 %s" % _px(16, s)}),
        (".deliver", {"font-size": _px(28, s), "font-weight": "800",
                      "line-height": "1.34", "text-align": "center",
                      "margin-top": _px(16, s)}),
        # ad.proof was silently dropped by all five of these shells on the
        # first build, which is the identical defect layouts.py records
        # against `nameplate`: a blind reader could not answer "am I
        # eligible" because the qualifier never reached the face. The
        # APPROVED corpus carries a negation qualifier on 37% of blocks.
        (".proofline", {"font-size": _px(27, s), "font-weight": "800",
                        "line-height": "1.3", "text-align": "center",
                        "margin-top": _px(12, s)}),
        (".bar", {"background": pal["ink"], "border-radius": "999px",
                  "display": "flex", "align-items": "center",
                  "justify-content": "space-between", "gap": _px(20, s),
                  "margin-top": _px(20, s),
                  "padding": "%s %s" % (_px(16, s), _px(24, s))}),
        (".bar .btn", {"background": _ground(pal), "color": pal["ink"],
                       "font-size": _px(29, s), "font-weight": "900",
                       "border-radius": "999px", "white-space": "nowrap",
                       "padding": "%s %s" % (_px(12, s), _px(26, s))}),
        (".bar .terms", {"font-size": _px(26, s), "font-weight": "700",
                         "line-height": "1.32", "color": "#FFFFFF",
                         "text-align": "right", "flex": "1"}),
        (".bar .terms b", {"font-weight": "900"}),
    ]


def _pixel_shell(kit, ad, s):
    x = ad.extra
    art = _pixel_grid(x.get("pixels", ["####"]), ad.pal["ink"],
                      ad.pal["accent"], max(round(22 * s), 12))
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="grow"></div>'
        '<div class="stage">%s</div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proofline">%s</div>'
        '<div class="grow"></div>'
        '<div class="bar"><div class="btn">%s</div>'
        '<div class="terms">%s</div></div>'
        % (_plain(kit.brand), kit.eyebrow, art, ad.callout, ad.head,
           ad.definition, x.get("deliver", ""), ad.proof, kit.cta, kit.terms))


LAYOUTS = {
    "chatui": (_chatui, _chatui_shell),
    "fortune": (_fortune, _fortune_shell),
    "duo": (_duo, _duo_shell),
    "desk": (_desk, _desk_shell),
    "pixel": (_pixel, _pixel_shell),
}
