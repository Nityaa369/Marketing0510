"""The `search` ad's hero, for the landing page. One component, every search-layout kit.

Why this exists. On 21-22 Sep 2026 Ruchika asked three times for the October search pages
to look like their ads ("why is the search bar style that is used in the ad not showing up
in the landing pages??"). Seven kits each re-drew the search bar by hand and every one came
out as a thin one-line pill: smaller query type, no typing caret, no card shadow, a
different offer card. The ad's look lives in `layouts_custom._search`; this module is that
same CSS, the same markup and the same glyph, scaled from the 1080px ad canvas to a web
column. A page that uses it cannot drift from its ad, because there is one source.

    from adkit import search_hero
    css  = search_hero.css("pine")            # palette name the ad was rendered with
    html = search_hero.block(rail="SkillArbitrage &middot; Tech Law Bootcamp",
                             callout="A litigator, 2 to 10 years in court?",
                             query="which practice area is growing fastest",
                             offer_tag="&#8377;10 3-day live bootcamp",
                             offer_date="24 to 26 Oct",
                             head="Take your court skills <em>into tech disputes.</em>",
                             deliver="We show you ...",
                             definition="Tech law is ...")   # optional, sits in the card

Put `css` in the page's <style> and `block` at the top of the hero. Class names carry an
`sh-` prefix so they cannot collide with the page's own stylesheet. No opacity, no
animation: the hero reads at rest.
"""
from . import palettes
from .layouts import SANS
from .layouts_custom import _GLASS

# Ad canvas is 1080px wide; the page column is 600px. Every ad measure is scaled by this,
# with a floor on small phones so identity type never drops below legible.
K = 600 / 1080


def _p(n):
    return "%.0fpx" % (n * K)


def _clamp(n, vw, lo):
    """Ad size n at the 600px column, shrinking with the viewport, never below lo."""
    return "clamp(%dpx,%.1fvw,%.0fpx)" % (lo, vw, n * K)


def css(palette_name):
    p = palettes.get(palette_name)
    a, ink, line, page = p["accent"], p["ink"], p["line"], p["page"]
    return """
.sh-hero{font-family:%(sans)s;color:%(ink)s;max-width:600px;margin:0 auto;padding:%(pt)s 0 %(pb)s;
 background:radial-gradient(ellipse 80%% 55%% at 50%% 46%%,#FFFFFF 0%%,%(page)s 70%%)}
.sh-rail{text-align:center;font-size:13px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
 color:%(a)s;margin-bottom:%(m8)s}
.sh-callout{background:%(a)s;color:#fff;font-size:%(co)s;font-weight:900;line-height:1.05;
 letter-spacing:-.02em;text-transform:uppercase;text-align:center;text-wrap:balance;
 padding:%(cp1)s %(cp2)s %(cp3)s;border-radius:8px;margin:0 0 %(cm)s}
.sh-slab{text-align:center;font-size:%(slab)s;font-weight:900;letter-spacing:-.04em;line-height:1;color:%(ink)s}
.sh-gap{height:%(gap)s}
.sh-bar{display:flex;align-items:center;gap:%(bg)s;background:#FFFFFF;border-radius:%(br)s;
 margin:%(bm)s %(bm)s 0;padding:%(bp1)s %(bp2)s;border:2px solid %(line)s;box-shadow:0 7px 17px rgba(0,0,0,.07)}
.sh-bar svg{width:%(svg)s;height:%(svg)s;flex:none}
.sh-query{font-size:%(q)s;font-weight:500;line-height:1.22;color:%(ink)s;text-wrap:balance}
.sh-caret{display:inline-block;width:2px;height:1.08em;background:%(a)s;margin-left:3px;vertical-align:-0.18em}
.sh-offer{background:#FFFFFF;border-radius:12px;margin-top:%(om)s;padding:%(op1)s %(op2)s %(op2)s;
 border:2px solid %(line)s;box-shadow:0 12px 28px rgba(0,0,0,.13)}
.sh-olabel{display:flex;justify-content:space-between;align-items:center;gap:9px;flex-wrap:wrap;
 padding-bottom:%(olp)s;margin-bottom:%(olm)s;border-bottom:2px dashed %(line)s}
.sh-otag{background:%(a)s;color:#fff;font-size:%(tag)s;font-weight:800;letter-spacing:.08em;
 text-transform:uppercase;padding:%(tp1)s %(tp2)s;border-radius:5px;white-space:nowrap}
.sh-odate{font-size:%(date)s;font-weight:900;letter-spacing:-.01em;color:%(a)s;white-space:nowrap}
.sh-head{font-size:%(head)s;font-weight:900;line-height:1.06;letter-spacing:-.026em;color:%(ink)s;text-wrap:balance;margin:0}
.sh-head em{font-style:italic;font-weight:900;color:%(a)s}
.sh-def,.sh-deliver{font-size:16px;line-height:1.45;margin-top:10px;color:%(ink)s}
.sh-deliver{font-weight:500}
""" % dict(sans=SANS, ink=ink, a=a, line=line, page=page,
           pt=_p(44), pb=_p(40), m8=_p(14),
           co=_clamp(64, 7.4, 24), cp1=_p(14), cp2=_p(18), cp3=_p(18), cm=_p(34),
           slab=_clamp(44, 5.4, 20), gap=_p(64),
           bg=_p(24), br=_p(40), bm=_p(24), bp1=_p(28), bp2=_p(44), svg=_p(46),
           q=_clamp(48, 5.6, 18),
           om=_p(24), op1=_p(30), op2=_p(34), olp=_p(20), olm=_p(24),
           tag=_clamp(36, 3.9, 13), tp1=_p(10), tp2=_p(18), date=_clamp(38, 4.2, 14),
           head=_clamp(74, 8.4, 28))


def block(rail, callout, query, offer_tag, offer_date, head, deliver="", definition="",
          q_label="the search:", a_label="the solution:"):
    d = '<p class="sh-def">%s</p>' % definition if definition else ""
    dv = '<p class="sh-deliver">%s</p>' % deliver if deliver else ""
    return (
        '<div class="sh-hero">'
        '<div class="sh-rail">%s</div>'
        '<h1 class="sh-callout">%s</h1>'
        '<div class="sh-slab">%s</div>'
        '<div class="sh-bar">%s<div class="sh-query">%s<span class="sh-caret"></span></div></div>'
        '<div class="sh-gap"></div>'
        '<div class="sh-slab">%s</div>'
        '<div class="sh-offer"><div class="sh-olabel"><span class="sh-otag">%s</span>'
        '<span class="sh-odate">%s</span></div>'
        '<h2 class="sh-head">%s</h2>%s%s</div>'
        '</div>'
        % (rail, callout, q_label, _GLASS, query, a_label, offer_tag, offer_date, head, d, dv))
