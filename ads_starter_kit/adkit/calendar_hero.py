"""The `calendar` ad's hero, for the landing page. One component, every calendar-layout kit.

Why this exists. Rule 4: a page mirrors its ad's colours, headline wording and hero device.
The search wave learned it the slow way (three requests on 21-22 Sep 2026, "why is the
search bar style that is used in the ad not showing up in the landing pages??") and the fix
was one module built from the ad's own CSS, `search_hero`. This is the same thing for
`layouts_custom._calendar`: its measures, scaled from the 1080px ad canvas to a 600px web
column, and its markup, so a page that uses it cannot drift from its ad.

    from adkit import calendar_hero
    css  = calendar_hero.css("pine")
    html = calendar_hero.block(rail="SkillArbitrage &middot; Independent Director Bootcamp",
                               callout="Recently retired?",
                               head="Sit on company boards, <em>as an independent director.</em>",
                               caption="Your week, after the farewell",      # optional
                               slots=["Mon | Morning walk, no alarm", "*Thu | Board meeting"],
                               deliver="In 3 free live sessions we show you ...",
                               definition="An independent director is ...")  # optional

Slots are the ad's own strings: "WHEN | text", "*" marks the one accent event. Week mode
only (no day strip), which is how every face in the first calendar waves ran. Class names
carry a `ch-` prefix. No opacity, no animation: the hero reads at rest.
"""
from . import palettes
from .layouts import SANS, SERIF
from .layouts_custom import _mix

K = 600 / 1080


def _p(n):
    return "%.0fpx" % (n * K)


def _clamp(n, vw, lo):
    """Ad size n at the 600px column, shrinking with the viewport, never below lo."""
    return "clamp(%dpx,%.1fvw,%.0fpx)" % (lo, vw, n * K)


def css(palette_name):
    p = palettes.get(palette_name)
    a, ink, page = p["accent"], p["ink"], p["page"]
    tint, rule = _mix(a, "#FFFFFF", 0.90), _mix(a, "#FFFFFF", 0.72)
    return """
.ch-hero{font-family:%(sans)s;color:%(ink)s;max-width:600px;margin:0 auto;padding:22px 0 6px}
.ch-rail{display:flex;justify-content:space-between;gap:12px;font-size:12px;font-weight:800;
 letter-spacing:.08em;text-transform:uppercase;color:%(a)s}
@media (max-width:480px){.ch-rail{flex-direction:column;gap:2px}}
.ch-callout{display:inline-block;background:%(a)s;color:#fff;font-size:%(co)s;font-weight:900;
 line-height:1.06;letter-spacing:-.015em;text-transform:uppercase;margin-top:%(m26)s;
 padding:%(cp1)s %(cp2)s %(cp3)s}
.ch-head{font-family:%(serif)s;font-size:%(hd)s;font-weight:700;line-height:1.08;letter-spacing:-.02em;
 color:%(ink)s;margin-top:%(m26)s;text-wrap:balance}
.ch-head em{font-style:italic;font-weight:700;color:%(a)s}
.ch-cal{background:#fff;border:2px solid %(rule)s;border-radius:12px;margin-top:%(m28)s;overflow:hidden}
.ch-date{text-align:center;font-size:%(dt)s;font-weight:800;color:%(ink)s;padding:10px 0;
 border-bottom:2px solid %(rule)s}
.ch-slot{display:flex;align-items:center;border-bottom:2px solid %(rule)s;padding:14px 12px}
.ch-slot:last-child{border-bottom:none}
.ch-when{width:%(hr)s;flex:none;font-size:%(tx)s;font-weight:700;color:%(ink)s}
.ch-cal.wide .ch-when{width:%(hrw)s}
.ch-ev{flex:1;font-size:%(tx)s;font-weight:700;color:%(ink)s;padding:6px 10px;border-radius:6px}
.ch-slot.on .ch-ev{background:%(tint)s;color:%(a)s;font-weight:800;border-left:5px solid %(a)s}
.ch-deliver{font-size:%(dl)s;line-height:1.36;font-weight:600;color:%(ink)s;margin-top:%(m22)s}
.ch-deliver.big{font-size:%(dlb)s;line-height:1.28;font-weight:700}
.ch-def{background:#fff;border-left:5px solid %(a)s;border-radius:8px;padding:12px 14px;
 margin-top:16px;font-size:16px;line-height:1.5;color:%(ink)s}
.ch-offer{font-size:%(of)s;font-weight:900;line-height:1.15;letter-spacing:-.01em;color:%(a)s;
 margin-top:%(m22)s}
""" % dict(sans=SANS, serif=SERIF, ink=ink, a=a, page=page, tint=tint, rule=rule,
           co=_clamp(64, 8.6, 30), hd=_clamp(70, 9.2, 32), dt=_clamp(30, 4.4, 17),
           tx=_clamp(30, 4.2, 16), dl=_clamp(31, 4.4, 17), dlb=_clamp(38, 5.2, 19), of=_clamp(38, 5.4, 21),
           hr=_p(168), hrw=_p(250), m26=_p(26), m28=_p(28), m22=_p(22),
           cp1=_p(14), cp2=_p(24), cp3=_p(18))


def block(rail, callout, head, slots, deliver="", caption="", definition="", offer="",
          rail_r="Independent Director Bootcamp", deliver_big=False):
    rows = []
    for sl in slots:
        on = sl.startswith("*")
        when, _, what = sl.lstrip("*").partition("|")
        rows.append('<div class="ch-slot%s"><div class="ch-when">%s</div>'
                    '<div class="ch-ev">%s</div></div>'
                    % (" on" if on else "", when.strip(), what.strip()))
    # the ad widens its when-column for a label past nine characters; so does the page
    wide = any(len(s.lstrip("*").split("|")[0].strip()) > 9 for s in slots)
    left = rail.split("&middot;")[0].strip()
    return (
        '<div class="ch-hero">'
        '<div class="ch-rail"><span>%s</span><span>%s</span></div>'
        '<h1 class="ch-callout">%s</h1>'
        '<div class="ch-head">%s</div>'
        '<div class="ch-cal%s">%s%s</div>'
        '%s%s%s'
        '</div>'
        % (left, rail_r, callout, head, " wide" if wide else "",
           ('<div class="ch-date">%s</div>' % caption) if caption else "", "".join(rows),
           ('<p class="ch-deliver%s">%s</p>' % (" big" if deliver_big else "", deliver))
           if deliver else "",
           ('<p class="ch-def">%s</p>' % definition) if definition else "",
           ('<div class="ch-offer">%s</div>' % offer) if offer else ""))
