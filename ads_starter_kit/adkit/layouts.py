#!/usr/bin/env python3
"""Named face layouts, each lifted from a face that was approved AND priced.

WHY THIS EXISTS (31 Aug 2026). `chassis.py` shipped with exactly one skeleton:

    callout bar -> head -> stat card -> definition -> proof -> takeaway ticks ->
    button + terms

Every face a kit built came out in that shape, so a wave of five ads was one
template with the middle widget swapped. Asked for directly, on the first
GlobalPatent wave: *"I don't like the designs - look through the design styles of
past best performing ads (not only patent, overall) and redo the designs."*
`python -m adkit.styles --kit GlobalPatent_MediaBuyer_19-21Sep` scored that kit
**4 of 5 faces unclassified** - no device at all - which is the same finding by
machine.

The memory note this violates is older than the chassis: *"each ad in a batch needs
its own layout skeleton, not one template with a swapped widget."*

WHERE EACH LAYOUT COMES FROM. Read off the winners, not invented. Every one names
the face it is lifted from and that face's live cost:

  notice     us22_notice_fifties          Rs 29.65 / lead  THE CHEAPEST AD IN THE
                                          ACCOUNT. A pinned paper notice, tilted,
                                          with the hook set huge inside it and the
                                          turn in italic. us25 and us24 are the
                                          same shape at Rs 39.93 and Rs 41.21, so
                                          three of the four cheapest lead ads in
                                          the account are this one layout.
  serif      03_law_firm_associates       Rs 82.00 / purchase  THE CHEAPEST PAID AD.
                                          Also LawSikho brand, also a Rs 10 camp,
                                          also 19-21 Sep, so it is the closest
                                          precedent this repo has to a LawSikho
                                          patent wave. Serif display, ICP in a
                                          solid block, a left-ruled quote for the
                                          delivery sentence, and NO button.
  ladder     hoc_02_ladder                GOLDEN, unpriced. A rung table as the
                                          artefact: where the work leads, in
                                          stages, each rung already true of her.
  nameplate  Ramanuj's own Academic       Unpriced, but it is HIS OWN design, sent
             Writing face, 29 Aug         29 Aug. The ICP name IS the hero, set
                                          enormous and two-tone, over soft rounded
                                          cards and a price starburst.
  docket     new. The document the reader would be paid to produce, as the
             artefact. Built for the patent wave, where the deliverable IS a
             written report, and generalises to any camp whose output is a
             document. Closest priced relative is the notice family.

THE `quote` / `deliver` TRAP, learned 3 Sep 2026 on GlobalPatent wave 2. `spec.py`
auto-fills `deliver` with the kit's delivery sentence for EVERY ad. But the serif and
ladder shells render `x.get("quote") or x.get("deliver")`, so **passing a `quote` in
`extra` silently deletes the delivery sentence from that face**, and passing a custom
`deliver` on nameplate replaces it. Six of ten faces in that wave did this, and the
result was that a blind reader with no brief could answer "what will I be able to do on
the last day" on the notice face and on NO other. Docket had no slot at all until this
date. **Do not pass `quote` or `deliver` unless you intend to lose the kit constant.**

WHAT EVERY LAYOUT STILL GUARANTEES, because these are the defects that shipped:

  * `.callout` and `.head` are emitted as REAL CLASSES with a REAL font-size, in
    the stylesheet, never inline. ad_lint C8 matches on the class name and the
    25 Aug 2026 silent pass was a generator that emitted inline styles only.
  * Both are clamped at 64px whatever the scale, so a tight fit is absorbed by
    body type and never by identity type.
  * Nothing is positioned absolutely and nothing overlaps by construction, so
    adkit.fit can still see clipping as clipping.

    python -m adkit.layouts        the catalogue, with the source face and cost
"""

from . import layouts_social

W, H = 1080, 1350
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
GUTTER = 60

# layout -> (source face, live cost, one line)
PROVENANCE = {
    "default": ("IndependentDirector_Wave1", "-",
                "The original chassis. Kept so shipped kits do not move."),
    "notice": ("us22_notice_fifties", "Rs 29.65/lead",
               "A pinned paper notice, tilted. Cheapest ad in the account."),
    "serif": ("03_law_firm_associates", "Rs 82.00/purchase",
              "Serif display, solid ICP block, ruled delivery line. Cheapest "
              "paid ad, and LawSikho brand. A CTA button was added 3 Sep 2026."),
    "ladder": ("hoc_02_ladder", "-",
               "A rung table as the artefact. GOLDEN reference."),
    "nameplate": ("Ramanuj's own Academic Writing face, 29 Aug", "-",
                  "The ICP name as the hero, two-tone, over soft cards."),
    "docket": ("new, patent wave", "-",
               "The document the reader would be paid to produce."),
    "photo": ("supplied hero, 1 Sep 2026", "-",
              "A real photograph as the hero, given the room to be one. No "
              "takeaway list, because that block leaves only 200px for the "
              "image on the default chassis."),
}


def _px(n, s):
    return "%dpx" % round(n * s)


def _idpx(n, s, floor=64):
    """Identity type never goes under its C8 floor, whatever the scale."""
    return "%dpx" % max(round(n * s), floor)


def _barpx(n, s, floor=30):
    """The barrier-removal line ("no law degree needed") never goes under 30px.

    Added 3 Sep 2026. creative_judge C25 is the only FIX that fired on all ten
    Global Patent wave 2 faces: the barrier line rendered at 22 to 27px, i.e. as
    fine print, and C25 carries the strongest single number in that judge -- the
    pattern runs at a 0.41 cost index in the backtest, making it a conversion
    asset rather than a legal footnote. A blind reader with no brief independently
    said the same thing about the one face that had lost it: "that reassurance
    actually matters most here, because 'law firm' makes me assume I'm not
    eligible."

    A plain _px() shrinks with auto-fit, so a face fitted at 0.84 put a 32px base
    on screen at 27px. This floors it the way _idpx floors identity type.
    """
    return "%dpx" % max(round(n * s), floor)


def _base(pal, s):
    """Shared reset and canvas. Every layout starts here."""
    return [
        ("*", {"margin": "0", "padding": "0", "box-sizing": "border-box"}),
        ("html,body", {"width": _px(W, 1), "height": _px(H, 1), "overflow": "hidden"}),
        ("body", {"font-family": SANS, "background": pal["page"], "color": pal["ink"]}),
        (".canvas", {"width": _px(W, 1), "height": _px(H, 1),
                     "padding": "%s %s %s" % (_px(44, s), _px(GUTTER, 1), _px(40, s)),
                     "display": "flex", "flex-direction": "column"}),
        (".grow", {"flex": "1", "min-height": "0"}),
        # A SECOND spacer with the same flex:1 splits leftover height into two
        # equal voids, which is what "a lot of empty gaps" looked like once the
        # face definition came off and there was real slack to split. .grow2
        # takes a quarter share, so the delivery block sits close to the footer
        # rule and the face carries ONE deliberate gap instead of two accidents.
        (".grow2", {"flex": "1", "min-height": "0"}),
        # `.keep` protects a credential's real casing inside an uppercased band.
        # Added 3 Sep 2026: the call-out bands are text-transform:uppercase, which
        # is right for "AGRI & FOOD SCIENCE GRADS" and wrong for "BVSc", which a vet
        # writes with a lower-case s and read as "BVSC". Dropping the transform on
        # the serif layout would have fixed that one face and silently restyled two
        # shipped ones whose call-outs are written in sentence case and rely on it
        # (AcademicWriting_Wave1 02_guest_lecturers, GlobalPatent wave 1
        # 03_agri_food_science). So the opt-out is per-token and lives on `_base`,
        # which means every layout gets it:
        #     callout="<span class='keep'>BVSc</span> &amp; VETERINARY GRADUATES"
        (".callout .keep", {"text-transform": "none"}),
    ]


# --------------------------------------------------------------------- notice

def _notice(pal, s):
    return _base(pal, s) + [
        (".nrail", {"text-align": "center", "font-size": _px(26, s),
                    "font-weight": "800", "letter-spacing": ".13em",
                    "text-transform": "uppercase", "color": pal["accent"],
                    "margin-bottom": _px(18, s)}),
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _idpx(62, s), "font-weight": "900",
                      "line-height": "1.05", "letter-spacing": "-.02em",
                      "text-transform": "uppercase", "text-align": "center",
                      "padding": "%s %s %s" % (_px(16, s), _px(22, s), _px(20, s)),
                      "border-radius": "8px"}),
        (".paper", {"background": "#FCFBF7", "margin-top": _px(34, s),
                    "padding": "%s %s %s" % (_px(48, s), _px(46, s), _px(44, s)),
                    "transform": "rotate(-0.7deg)",
                    "box-shadow": "0 18px 40px rgba(0,0,0,.16)",
                    "position": "relative"}),
        (".tape", {"width": _px(150, s), "height": _px(15, s),
                   "background": pal["line"], "margin": "0 auto %s" % _px(26, s),
                   "border-radius": "3px"}),
        (".nlabel", {"font-size": _px(30, s), "font-weight": "800",
                     "letter-spacing": ".16em", "text-transform": "uppercase",
                     "color": pal["accent"], "margin-bottom": _px(18, s)}),
        (".head", {"font-size": _idpx(70, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.024em",
                   "color": "#16130E"}),
        (".head em", {"font-style": "italic", "font-weight": "900"}),
        (".def", {"font-size": _px(34, s), "line-height": "1.36",
                  "text-align": "center", "margin-top": _px(26, s),
                  "padding": "0 %s" % _px(14, s)}),
        (".deliver", {"font-size": _px(34, s), "font-weight": "800",
                      "line-height": "1.34", "text-align": "center",
                      "margin-top": _px(20, s), "color": pal["accent"],
                      "padding": "0 %s" % _px(6, s)}),
        # Optional take-away list (extra=dict(ticks=[...], ticks_title=...)), added 22 Sep 2026 for
        # the DataProtection non-lawyer batch: cut to three short lines, the notice read as "too
        # empty"; a scannable list fills it without adding a paragraph. Absent ticks = unchanged.
        (".ticks", {"margin-top": _px(30, s), "background": "#fff",
                    "border": "2px solid " + pal["line"], "border-radius": "12px",
                    "padding": "%s %s" % (_px(20, s), _px(28, s))}),
        (".ticks .th", {"font-size": _barpx(26, s), "font-weight": "800",
                        "letter-spacing": ".12em", "text-transform": "uppercase",
                        "color": pal["accent"], "margin-bottom": _px(8, s)}),
        (".ticks .tk", {"font-size": _px(36, s), "font-weight": "800", "line-height": "1.3",
                        "padding": "%s 0" % _px(8, s), "color": pal["ink"]}),
        (".ticks .tk span", {"color": pal["accent"], "margin-right": _px(14, s)}),
        # Optional skill bridge (extra=dict(bridge=[(now, privacy), ...])), 22 Sep 2026, same
        # reason as the call layout's: show how the reader's current work carries over. Replaces
        # the definition line when present.
        (".bridge", {"margin-top": _px(26, s), "border-left": "6px solid " + pal["accent"],
                     "padding": "%s %s" % (_px(4, s), _px(22, s))}),
        (".bridge .th", {"font-size": _barpx(26, s), "font-weight": "800",
                         "letter-spacing": ".12em", "text-transform": "uppercase",
                         "color": pal["accent"], "margin-bottom": _px(6, s)}),
        (".bridge .br", {"font-size": _px(34, s), "line-height": "1.3", "padding": "%s 0" % _px(6, s),
                         "color": pal["ink"]}),
        (".bridge .br b", {"font-weight": "800", "display": "block"}),
        (".bridge .br span", {"color": pal["accent"], "font-weight": "800", "display": "block"}),
        # Labelled two-column bridge (extra=dict(bridge_cols=(now_label, privacy_label))), 22 Sep,
        # same as the call layout: name what you do now and what it becomes, not just an arrow.
        (".bgrid", {"display": "grid", "grid-template-columns": "1fr 1.25fr",
                    "column-gap": _px(20, s), "background": "#fff",
                    "border": "2px solid " + pal["line"], "border-radius": "12px",
                    "padding": "%s %s" % (_px(12, s), _px(24, s)), "margin-top": _px(26, s)}),
        (".bgrid .bt", {"grid-column": "1 / -1", "font-size": _barpx(26, s), "font-weight": "800",
                        "letter-spacing": ".12em", "text-transform": "uppercase",
                        "color": pal["accent"], "padding-bottom": _px(6, s)}),
        (".bgrid .bl", {"font-size": _px(20, s), "font-weight": "900", "letter-spacing": ".08em",
                        "text-transform": "uppercase", "color": pal["ink"],
                        "padding": "%s 0" % _px(6, s)}),
        (".bgrid .bn", {"font-size": _px(31, s), "font-weight": "800", "color": pal["ink"],
                        "line-height": "1.25", "padding": "%s 0" % _px(9, s),
                        "border-top": "1px solid " + pal["line"]}),
        (".bgrid .bp", {"font-size": _px(31, s), "font-weight": "800", "color": pal["accent"],
                        "line-height": "1.25", "padding": "%s 0" % _px(9, s),
                        "border-top": "1px solid " + pal["line"]}),
        # Optional full-width CTA (extra=dict(big_cta=True)), 22 Sep 2026: "make the join button
        # bigger". The footer then carries only the terms, left and right.
        (".bigbtn", {"background": pal["accent"], "color": "#fff", "text-align": "center",
                     "font-size": _px(46, s), "font-weight": "900",
                     "padding": "%s %s" % (_px(26, s), _px(30, s)),
                     "border-radius": "14px", "margin-top": _px(26, s)}),
        (".rule", {"border-top": "3px solid " + pal["ink"],
                   "margin-top": _px(24, s)}),
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(18, s),
                   "margin-top": _px(22, s)}),
        (".foot .sm", {"font-size": _barpx(27, s), "font-weight": "800",
                       "letter-spacing": ".07em", "text-transform": "uppercase",
                       "line-height": "1.3", "flex": "1"}),
        (".foot .sm.r", {"text-align": "right"}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(32, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(18, s), _px(34, s)),
                  "border-radius": "8px", "white-space": "nowrap"}),
    ]


def _notice_shell(kit, ad, s):
    x = ad.extra
    return (
        '<div class="nrail">%s &middot; %s</div>'
        '<div class="callout">%s</div>'
        '<div class="paper"><div class="tape"></div>'
        '<div class="nlabel">%s</div><div class="head">%s</div></div>'
        '<div class="grow"></div>'
        '%s'
        '%s'
        '<div class="grow"></div>'
        '%s'
        '<div class="rule"></div>'
        '<div class="foot"><div class="sm">%s</div>'
        '%s'
        '<div class="sm r">%s</div></div>'
        % (_plain(kit.brand), kit.eyebrow, ad.callout,
           x.get("label", "Notice"), ad.head,
           (('<div class="bgrid"><div class="bt">%s</div><div class="bl">%s</div>'
             '<div class="bl">%s</div>%s</div>'
             % (x.get("bridge_title", "Your skills, in data privacy"), x["bridge_cols"][0],
                x["bridge_cols"][1], "".join('<div class="bn">%s</div><div class="bp">%s</div>' % r
                                             for r in x["bridge"])))
            if x.get("bridge") and x.get("bridge_cols") else
           (('<div class="bridge"><div class="th">%s</div>%s</div>'
             % (x.get("bridge_title", "Your skills, in data privacy"), "".join(
                 '<div class="br"><b>%s</b> <span>&#8594; %s</span></div>' % r
                 for r in x["bridge"])))
            if x.get("bridge") else '<div class="def">%s</div>' % ad.definition)),
           ('<div class="ticks"><div class="th">%s</div>%s</div>'
            % (x.get("ticks_title", ""), "".join(
                '<div class="tk"><span>&#10003;</span>%s</div>' % t for t in x["ticks"])))
           if x.get("ticks") else '<div class="deliver">%s</div>' % x.get("deliver", ""),
           ('<div class="bigbtn">%s</div>' % kit.cta) if x.get("big_cta") else "",
           x.get("foot_left", "Live on Zoom"),
           "" if x.get("big_cta") else '<div class="btn">%s</div>' % kit.cta,
           x.get("foot_right", ad.proof)))


# ---------------------------------------------------------------------- serif

def _serif(pal, s):
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(30, s), "font-weight": "800",
                    "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal"}),
        (".eyebrow", {"font-size": _px(26, s), "font-weight": "800",
                      "letter-spacing": ".14em", "text-transform": "uppercase",
                      "color": pal["accent"]}),
        (".hrule", {"border-top": "5px solid " + pal["accent"],
                    "margin-top": _px(12, s)}),
        (".callout", {"display": "inline-block", "background": pal["accent"],
                      "color": "#fff", "font-size": _idpx(64, s),
                      "font-weight": "900", "line-height": "1.08",
                      "letter-spacing": "-.015em", "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(8, s), _px(20, s), _px(12, s)),
                      "margin-top": _px(74, s)}),
        (".head", {"font-family": SERIF, "font-size": _idpx(66, s),
                   "font-weight": "700", "line-height": "1.13",
                   "margin-top": _px(14, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        # 32 -> 46 and floored, 3 Sep 2026. On the serif layout the kicker carries the
        # TENSION line, which on the Rs 82.00 `03_law_firm_associates` face -- the
        # cheapest paid ad in the account -- is "The work is already here. The trained
        # people are not." That is the second thing a reader looks at, and 32px on a
        # 1080 canvas renders about 15px in feed. creative_judge C8 called it "barely
        # visible" and it was right.
        #
        # The control matters here: rendering the winner's OWN call-out, head and
        # kicker through this chassis fired the identical C8 note, which proves the
        # finding is the chassis rather than the copy. C8's own floor is 56px; 46 is
        # RAISED AGAIN to 56 on 3 Sep 2026 (US Corporate Law wave 2). At 46 this was the
        # ONLY finding left on that kit and it fired on all ten faces, taking
        # creative_judge to 0 accept. 56 is C8's own floor, it is still clearly
        # subordinate to a 64px head, and every kit re-rendered clean at it.
        # THE BARRIER LINE IS A QUALIFIER ROW, NOT A SECOND HEADLINE. At 56px in
        # the accent colour it sat within 10px of the 66px head and wrapped to two
        # ragged lines, so the face had three competing primary elements (band,
        # head, barrier) and no hierarchy at all -- which is what "the no law
        # degree required can be designed better" is looking at. The Rs 82
        # approved face runs FIVE distinct sizes; this one ran band 64 / head 66 /
        # barrier 56 / body 37.
        #
        # Set as the house qualifier row instead: uppercase, letterspaced, one
        # line, clearly subordinate. C25's evidence is a 30px FLOOR (see _barpx),
        # never a requirement to run it at headline size, and 38px caps still
        # reads as a strip rather than as fine print.
        # ONE CLASS WAS DOING TWO JOBS, and each inherited the other's floor.
        # Corrected 4 Sep 2026 after "the no law degree required can be designed
        # better". On the Rs 82 winner `.kicker` carries the TENSION line, a piece
        # of argument that deserves C8's 56px identity floor. On US Corporate Law
        # the tension line was dropped, so `.kicker` fell back to the BARRIER line
        # ("no law degree, no US bar exam, no visa") -- which has its own rule,
        # C25, whose measured floor is 30px, and which is a qualifier row rather
        # than a headline. Running it at 56px in the accent colour put it within
        # 10px of the 66px head and wrapped it to two ragged lines, so the face had
        # three competing primary elements and no hierarchy.
        #
        # Demoting `.kicker` itself was the wrong fix: it dropped the tension line
        # under C8 too, and creative_judge caught it on AcademicWriting wave 1
        # face 02 immediately. So the two are now separate classes and the shell
        # picks by CONTENT -- see _serif_shell. Neither rule was weakened.
        # Floor is 56, not 52: C8 hard-fails a kicker under 56px, and at s=0.97 a
        # floor of 52 let round(56*0.97)=54 through. creative_judge caught it on
        # AcademicWriting wave 1 face 02. The floor must equal the rule.
        (".kicker", {"font-size": _barpx(56, s, floor=56), "font-weight": "800",
                     "color": pal["accent"], "margin-top": _px(22, s),
                     "line-height": "1.3"}),
        # The barrier line, set as the house qualifier row: uppercase, letterspaced,
        # one line, clearly subordinate to the head. 38px is well above C25's 30px
        # floor and reads as a strip rather than as fine print.
        (".barrier", {"font-size": _barpx(38, s, floor=34), "font-weight": "800",
                      "color": pal["accent"], "margin-top": _px(44, s),
                      "text-transform": "uppercase", "letter-spacing": ".05em",
                      "line-height": "1.34"}),
        (".sfoot", {"display": "flex", "align-items": "center",
                    "gap": _px(24, s), "margin-top": _px(18, s)}),
        (".sterms", {"flex": "1"}),
        # .btn styled to match the other layouts, added with the shell change above.
        (".btn", {"display": "inline-block", "background": pal["accent"],
                  "color": "#fff", "font-family": SANS,
                  "font-size": _px(30, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(18, s), _px(34, s)),
                  "border-radius": "8px", "white-space": "nowrap"}),
        (".def", {"font-family": SERIF, "font-size": _px(34, s),
                  "line-height": "1.4", "margin-top": _px(16, s)}),
        # NO QUOTE BAR. Reported as "what is this weird line next to the
        # paragraph". The bar is an ASIDE device: on the Rs 82 approved face it
        # marks a small closing note sitting under a coloured tension line and a
        # grey question paragraph, so it has something to be an aside FROM. On
        # this face the definition and the tension line are both gone, leaving the
        # delivery sentence as the ONLY body copy -- a quote bar on the only
        # paragraph is decoration with no function, and at 8px against 37px bold
        # serif it reads as a stray stroke. Body copy, set as body copy.
        # Slack is spent on MARGIN and on the size of the value proposition, not
        # left for the flex spacers to pool. Dropping the quote bar and demoting
        # the barrier line freed about 100px, and flex put all of it into one
        # 200px void. Fixed margins absorb it as rhythm instead; whatever is left
        # still goes to .grow / .grow2, so the layout stays elastic.
        (".quote", {"font-family": SERIF, "font-size": _px(41, s),
                    "font-weight": "600", "line-height": "1.44",
                    "margin-top": _px(56, s)}),
        (".rule", {"border-top": "3px solid " + pal["ink"]}),
        (".fline", {"font-size": _px(26, s), "font-weight": "800",
                    "letter-spacing": ".09em", "text-transform": "uppercase",
                    "margin-top": _px(20, s)}),
        (".fprice", {"font-size": _px(29, s), "font-weight": "800",
                     "color": pal["accent"], "margin-top": _px(8, s)}),
        (".trust", {"font-size": _px(26, s), "font-weight": "600",
                    "margin-top": _px(10, s), "color": pal["ink"]}),
    ]


def _serif_shell(kit, ad, s):
    x = ad.extra
    # An EMPTY definition drops the whole div rather than rendering a blank one,
    # which would still contribute its margins and reopen the gap the two .grow
    # spacers exist to close. A kit turns the face definition off by passing
    # extra=dict(face_definition="") - see adkit/spec.py. The page keeps it.
    dfn = ('<div class="def">' + ad.definition + '</div>') if ad.definition else ""
    # An explicit `kicker` is a TENSION line and keeps C8's 56px identity floor.
    # Falling back to ad.proof means this slot holds the BARRIER line, which is a
    # qualifier row governed by C25 (30px floor) and set smaller so it does not
    # compete with the head. The class follows the content, not the slot.
    if x.get("kicker"):
        kick = '<div class="kicker">' + x["kicker"] + '</div>'
    else:
        kick = '<div class="barrier">' + ad.proof + '</div>'
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div><div class="hrule"></div>'
        '<div><div class="callout">%s</div></div>'
        '<div class="head">%s</div>'
        '%s'
        '<div class="grow"></div>'
        '%s'
        '<div class="quote">%s</div>'
        '<div class="grow2"></div>'
        # CTA button added 3 Sep 2026, and MOVED INTO THE FOOTER on 4 Sep after the
        # obvious question: "would a button come above the footer in an ad??" No. It
        # was floating between the delivery block and the footer rule, orphaned from
        # the terms it belongs with. Every other layout in this file puts the button
        # in the footer row beside the date and price, and now so does this one.
        '<div class="rule"></div>'
        '<div class="sfoot"><div class="btn">%s</div>'
        '<div class="sterms"><div class="fline">%s</div>'
        '<div class="fprice">%s</div></div></div>'
        '<div class="trust">%s</div>'
        % (kit.brand, kit.eyebrow, ad.callout, ad.head,
           kick, dfn,
           x.get("quote") or x.get("deliver", ""), kit.cta,
           x.get("fline", "Live online"),
           x.get("fprice", ""), kit.trust))


# --------------------------------------------------------------------- ladder

def _ladder(pal, s):
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(28, s), "font-weight": "800",
                    "letter-spacing": ".14em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal"}),
        (".eyebrow", {"font-size": _px(26, s), "font-weight": "800",
                      "letter-spacing": ".14em", "text-transform": "uppercase",
                      "color": pal["ink"]}),
        (".hrule", {"border-top": "4px solid " + pal["ink"],
                    "margin-top": _px(12, s)}),
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-family": SERIF, "font-size": _idpx(64, s),
                      "font-weight": "700", "line-height": "1.12",
                      "text-transform": "uppercase", "letter-spacing": "0",
                      "padding": "%s %s %s" % (_px(14, s), _px(24, s), _px(18, s)),
                      "margin-top": _px(44, s)}),
        (".head", {"font-family": SERIF, "font-size": _idpx(66, s),
                   "font-weight": "700", "line-height": "1.12",
                   "margin-top": _px(16, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".rungs", {"margin-top": _px(26, s), "padding-top": _px(20, s),
                    "border-top": "2px solid " + pal["line"]}),
        (".rung", {"display": "flex", "gap": _px(22, s), "align-items": "baseline",
                   "margin-bottom": _px(14, s), "min-height": _px(34, s)}),
        (".rung .l", {"flex": "0 0 %s" % _px(300, s), "font-size": _px(27, s),
                      "font-weight": "800", "letter-spacing": ".05em",
                      "text-transform": "uppercase", "color": pal["accent"]}),
        (".rung .r", {"flex": "1", "font-size": _px(30, s), "font-weight": "800",
                      "line-height": "1.22"}),
        (".def", {"font-size": _px(33, s), "line-height": "1.4",
                  "margin-top": _px(16, s), "color": pal["ink"]}),
        (".quote", {"font-size": _px(33, s), "font-weight": "800",
                    "line-height": "1.32", "margin-top": _px(20, s)}),
        (".proof", {"font-size": _barpx(32, s), "font-weight": "800",
                    "line-height": "1.3", "margin-top": _px(14, s),
                    "color": pal["accent"]}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(32, s), "font-weight": "800",
                  "display": "inline-block", "margin-top": _px(22, s),
                  "padding": "%s %s" % (_px(18, s), _px(34, s))}),
        # margin trimmed 16 -> 6, 3 Sep 2026, same cause as the nameplate foot:
        # _barpx added height the ladder had no slack for and the face overflowed
        # by a constant 3px whatever the copy said.
        (".dline", {"font-size": _barpx(26, s), "font-weight": "800",
                    "letter-spacing": ".12em", "text-transform": "uppercase",
                    "margin-top": _px(6, s), "color": pal["ink"]}),
    ]


def _ladder_shell(kit, ad, s):
    x = ad.extra
    rungs = "".join('<div class="rung"><div class="l">%s</div>'
                    '<div class="r">%s</div></div>' % (l, r)
                    for l, r in x.get("rungs", []))
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div><div class="hrule"></div>'
        '<div><div class="callout">%s</div></div>'
        '<div class="head">%s</div>'
        '<div class="rungs">%s</div>'
        '<div class="grow"></div>'
        '<div class="def">%s</div>'
        '<div class="quote">%s</div>'
        '<div class="proof">%s</div>'
        '<div class="grow"></div>'
        '<div><div class="btn">%s</div></div>'
        '<div class="dline">%s</div>'
        % (kit.brand, kit.eyebrow, ad.callout, ad.head, rungs,
           ad.definition, x.get("quote") or x.get("deliver", ""),
           ad.proof, kit.cta,
           x.get("dline", "")))


# ------------------------------------------------------------------ nameplate

def _nameplate(pal, s):
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "flex-start"}),
        (".brand", {"font-size": _px(30, s), "font-weight": "900",
                    "letter-spacing": ".08em", "text-transform": "uppercase",
                    "color": pal["accent"]}),
        (".brand i", {"font-style": "normal", "color": pal["ink"]}),
        (".badge", {"background": pal["accent"], "color": "#fff",
                    "width": _px(152, s), "height": _px(152, s),
                    "border-radius": "50%", "display": "flex",
                    "flex-direction": "column", "align-items": "center",
                    "justify-content": "center", "text-align": "center",
                    "line-height": "1.05"}),
        (".badge b", {"font-size": _px(44, s), "font-weight": "900"}),
        (".badge span", {"font-size": _px(21, s), "font-weight": "800",
                         "letter-spacing": ".1em", "text-transform": "uppercase"}),
        (".pills", {"display": "flex", "flex-wrap": "wrap", "gap": _px(10, s),
                    "margin-top": _px(18, s)}),
        (".pill", {"background": pal["card"], "font-size": _px(26, s),
                   "font-weight": "800", "border-radius": "999px",
                   "padding": "%s %s" % (_px(12, s), _px(22, s))}),
        (".callout", {"font-size": _idpx(96, s), "font-weight": "900",
                      "line-height": "1.0", "letter-spacing": "-.035em",
                      "text-transform": "uppercase", "margin-top": _px(22, s),
                      "color": pal["ink"]}),
        (".callout em", {"font-style": "normal", "color": pal["accent"]}),
        (".uline", {"width": _px(300, s), "height": _px(12, s),
                    "background": pal["line"],
                    "border-radius": "999px", "margin-top": _px(16, s)}),
        (".soft", {"background": pal["card"], "border-radius": _px(26, s),
                   "padding": "%s %s" % (_px(20, s), _px(32, s)),
                   "margin-top": _px(16, s)}),
        (".head", {"font-size": _idpx(44, s), "font-weight": "800",
                   "line-height": "1.24"}),
        (".head em", {"font-style": "italic", "color": pal["accent"]}),
        (".def", {"font-size": _px(32, s), "line-height": "1.38"}),
        # Added 31 Aug 2026: the shell used to drop ad.proof silently, so a face
        # on this layout could not say what the reader leaves with. A blind
        # reader returned CANNOT TELL on "what will I be able to do on the last
        # day" for exactly that reason.
        (".proof", {"font-size": _barpx(27, s), "font-weight": "800",
                    "line-height": "1.34", "color": pal["accent"]}),
        # margin trimmed 24 -> 12 on 3 Sep 2026. Flooring the barrier line at 30px
        # (_barpx) added height this shell had no slack for, and both nameplate
        # faces overflowed by a constant 7px regardless of copy length -- i.e. it
        # was fixed margin, not content. Cutting words here would have been the
        # wrong fix.
        (".foot", {"display": "flex", "align-items": "center",
                   "justify-content": "space-between", "gap": _px(20, s),
                   "margin-top": _px(12, s)}),
        (".foot .d", {"font-size": _barpx(26, s), "font-weight": "800",
                      "line-height": "1.34"}),
        (".foot .d s", {"text-decoration": "none", "color": pal["accent"]}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(30, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(18, s), _px(32, s)),
                  "border-radius": "999px", "white-space": "nowrap"}),
    ]


def _nameplate_shell(kit, ad, s):
    x = ad.extra
    pills = "".join('<div class="pill">%s</div>' % p for p in x.get("pills", []))
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="badge"><b>%s</b><span>%s</span></div></div>'
        '<div class="pills">%s</div>'
        '<div class="callout">%s</div><div class="uline"></div>'
        '<div class="soft"><div class="head">%s</div></div>'
        '<div class="soft"><div class="def">%s</div></div>'
        '%s%s'
        '<div class="grow"></div>'
        '<div class="foot"><div class="d">%s</div>'
        '<div class="btn">%s</div></div>'
        % (kit.brand, x.get("badge_big", "&#8377;10"),
           x.get("badge_sub", "to join"), pills,
           ad.callout, ad.head, ad.definition,
           ('<div class="soft"><div class="proof">%s</div></div>'
            % x.get("deliver", "")) if x.get("deliver") else "",
           ('<div class="soft"><div class="proof">%s</div></div>' % ad.proof)
           if ad.proof else "",
           x.get("dline", ""), kit.cta))


# --------------------------------------------------------------------- docket

def _docket(pal, s):
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(28, s), "font-weight": "800",
                    "letter-spacing": ".12em", "text-transform": "uppercase"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(20, s), "font-weight": "800",
                      "letter-spacing": ".16em", "text-transform": "uppercase",
                      "color": pal["accent"]}),
        (".callout", {"font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.06", "letter-spacing": "-.025em",
                      "margin-top": _px(26, s),
                      "padding-bottom": _px(16, s),
                      "border-bottom": "4px solid " + pal["line"]}),
        (".callout em", {"font-style": "normal", "color": pal["accent"]}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.08", "letter-spacing": "-.025em",
                   "color": pal["accent"], "margin-top": _px(20, s),
                   "margin-bottom": _px(28, s)}),
        (".doc", {"background": "#FFFFFF", "border": "3px solid " + pal["line"],
                  "border-radius": "6px", "overflow": "hidden",
                  "box-shadow": "0 14px 30px rgba(0,0,0,.10)"}),
        (".doc .hd", {"background": pal["accent"], "color": "#fff",
                      "font-size": _px(26, s), "font-weight": "800",
                      "letter-spacing": ".14em", "text-transform": "uppercase",
                      "padding": "%s %s" % (_px(14, s), _px(26, s))}),
        (".row", {"display": "flex", "gap": _px(20, s), "align-items": "baseline",
                  "padding": "%s %s" % (_px(21, s), _px(26, s)),
                  "border-bottom": "2px solid " + pal["line"],
                  "min-height": _px(40, s)}),
        (".row:last-child", {"border-bottom": "0"}),
        (".row .n", {"flex": "0 0 %s" % _px(44, s), "font-size": _px(27, s),
                     "font-weight": "900", "color": pal["accent"]}),
        (".row .t", {"flex": "1", "font-size": _px(28, s), "font-weight": "800",
                     "line-height": "1.24"}),
        (".def", {"font-size": _px(33, s), "line-height": "1.38",
                  "margin-top": _px(22, s)}),
        # .deliver added 3 Sep 2026. A blind reader with no brief could answer "what
        # will I be able to do on the last day" on the notice faces and on NO docket
        # face, because this shell rendered the definition and the proof but never the
        # kit's delivery sentence. spec.py auto-fills `deliver` for every ad already;
        # the shell simply was not printing it.
        (".deliver", {"font-size": _px(30, s), "font-weight": "700",
                      "line-height": "1.36", "margin-top": _px(14, s)}),
        (".proof", {"font-size": _barpx(32, s), "font-weight": "800",
                    "color": pal["accent"], "margin-top": _px(14, s),
                    "line-height": "1.3"}),
        (".foot", {"display": "flex", "align-items": "center", "gap": _px(22, s),
                   "margin-top": _px(22, s), "padding-top": _px(20, s),
                   "border-top": "3px solid " + pal["ink"]}),
        (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(31, s), "font-weight": "800",
                  "padding": "%s %s" % (_px(18, s), _px(32, s)),
                  "border-radius": "8px", "white-space": "nowrap"}),
        (".terms", {"font-size": _px(26, s), "font-weight": "700",
                    "line-height": "1.32"}),
        (".terms b", {"font-weight": "800"}),
    ]


def _docket_shell(kit, ad, s):
    x = ad.extra
    rows = "".join('<div class="row"><div class="n">%s</div>'
                   '<div class="t">%s</div></div>' % (n, t)
                   for n, t in x.get("rows", []))
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="head">%s</div>'
        '<div class="doc"><div class="hd">%s</div>%s</div>'
        '<div class="grow"></div>'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proof">%s</div>'
        '<div class="grow"></div>'
        '<div class="foot"><div class="btn">%s</div>'
        '<div class="terms">%s</div></div>'
        % (kit.brand, kit.eyebrow, ad.callout, ad.head,
           x.get("doc_title", "Deliverable"), rows,
           ad.definition, x.get("deliver", ""), ad.proof, kit.cta,
           # A one-line terms strip when the face supplies it; the two-line
           # kit default was clipping at the canvas edge under a full-width CTA.
           x.get("terms_line", kit.terms)))


# --------------------------------------------------------------------- photo

def _photo(pal, s):
    """A supplied photograph as the hero, added 1 Sep 2026.

    The default chassis can carry a banner, but it also renders the takeaway
    list unconditionally, which leaves about 200px of the 1350 for the image.
    At that height a photograph is a decorative strip, not a hero, and pushing
    it larger crushes the footer to zero height instead of overflowing it -
    which adkit.fit could not see, because nothing extended past the canvas.
    This shell drops the takeaway list and gives the image the room instead.
    """
    return _base(pal, s) + [
        (".top", {"display": "flex", "justify-content": "space-between",
                  "align-items": "baseline"}),
        (".brand", {"font-size": _px(30, s), "font-weight": "800"}),
        (".brand i", {"font-style": "normal", "color": pal["accent"]}),
        (".eyebrow", {"font-size": _px(22, s), "font-weight": "800",
                      "letter-spacing": ".15em", "text-transform": "uppercase",
                      "color": pal["accent"]}),
        (".callout", {"background": pal["accent"], "color": "#fff",
                      "font-size": _idpx(64, s), "font-weight": "900",
                      "line-height": "1.06", "letter-spacing": "-.025em",
                      "text-transform": "uppercase",
                      "padding": "%s %s %s" % (_px(16, s), _px(24, s), _px(20, s)),
                      "border-radius": _px(10, s), "margin-top": _px(20, s)}),
        (".shot", {"margin-top": _px(16, s), "border-radius": _px(12, s),
                   "overflow": "hidden", "flex-shrink": "0"}),
        (".shot img", {"width": "100%", "display": "block"}),
        (".head", {"font-size": _idpx(64, s), "font-weight": "900",
                   "line-height": "1.1", "letter-spacing": "-.025em",
                   "margin-top": _px(22, s)}),
        (".head em", {"font-style": "normal", "color": pal["accent"]}),
        (".def", {"font-size": _px(33, s), "line-height": "1.38",
                  "margin-top": _px(16, s)}),
        (".deliver", {"font-size": _px(32, s), "font-weight": "800",
                      "line-height": "1.34", "margin-top": _px(14, s),
                      "color": pal["accent"]}),
        (".proof", {"font-size": _barpx(31, s), "font-weight": "800",
                    "line-height": "1.3", "margin-top": _px(12, s)}),
                (".foot", {"display": "block", "margin-top": _px(18, s),
                   "padding-top": _px(18, s),
                   "border-top": "3px solid " + pal["ink"]}),
                # 31 -> 40px with a deeper pad, 23 Sep 2026: on the scene faces the
        # Join button was the smallest element on a face whose whole job is
        # the click.
                (".btn", {"background": pal["accent"], "color": "#fff",
                  "font-size": _px(44, s), "font-weight": "900",
                  "padding": "%s 0" % _px(24, s), "display": "block",
                  "width": "100%", "text-align": "center",
                  "border-radius": "10px"}),
                (".terms", {"font-size": _px(27, s), "font-weight": "700",
                    "line-height": "1.3", "text-align": "center",
                    "margin-top": _px(12, s)}),
        (".terms b", {"font-weight": "800"}),
        # Optional spoken line over the photograph (extra=dict(said="...")), added
        # 23 Sep 2026. This is the device in the APPROVED MassHysteria arbitration
        # faces - a real scene, one thing the person says, then the offer - and
        # adkit had no way to draw it. Absent `said`, nothing changes.
        (".shot", {"position": "relative"}),
        (".bubble", {"position": "absolute", "left": _px(26, s), "right": _px(26, s),
                     "bottom": _px(22, s), "background": "#fff",
                     "border-radius": "14px",
                     "padding": "%s %s" % (_px(20, s), _px(24, s)),
                     "box-shadow": "0 10px 30px rgba(0,0,0,.28)"}),
        (".bubble p", {"font-size": _px(34, s), "font-weight": "800",
                       "line-height": "1.26", "color": "#14110D"}),
        # Film-still dialogue captions (extra=dict(bubbles=[...])), added 30 Sep
        # 2026 for the Tech Law Bollywood-still meme. The format Ruchika sent is
        # two people in one frame, each with a plain white caption box placed
        # near the speaker, so one bottom-anchored `said` cannot draw it. Each
        # entry is dict(text=..., at="top:..;left:..;width:.."), positioned in
        # px on the shot. Absent `bubbles`, nothing changes.
        (".mb", {"position": "absolute", "background": "#fff",
                 "border-radius": "10px",
                 "padding": "%s %s" % (_px(12, s), _px(18, s)),
                 "box-shadow": "0 6px 18px rgba(0,0,0,.30)"}),
        (".mb p", {"font-size": _px(31, s), "font-weight": "700",
                   "line-height": "1.24", "color": "#14110D"}),
        # Ink, not accent: the benefit is the strongest line after the head, and
        # the delivery line under it was competing in the same colour.
        (".benefit", {"font-size": _px(36, s), "font-weight": "800",
                      "line-height": "1.26", "margin-top": _px(12, s),
                      "color": pal["ink"]}),
        (".benefit em", {"font-style": "normal", "color": pal["accent"]}),
    ]


def _photo_shell(kit, ad, s):
    x = ad.extra
    return (
        '<div class="top"><div class="brand">%s</div>'
        '<div class="eyebrow">%s</div></div>'
        '<div class="callout">%s</div>'
        '<div class="shot"%s><img src="../photos/%s" alt=""%s>%s</div>'
        '<div class="head">%s</div>'
        '%s'
        '<div class="def">%s</div>'
        '<div class="deliver">%s</div>'
        '<div class="proof">%s</div>'
        '<div class="grow"></div>'
        '<div class="foot"><div class="btn">%s</div>'
        '<div class="terms">%s</div></div>'
        % (kit.brand, kit.eyebrow, ad.callout,
           (' style="height:%s;overflow:hidden"' % x["shot_h"])
           if x.get("shot_h") else "",
           ad.banner or ad.shot,
           (' style="height:100%%;object-fit:cover;object-position:%s"'
            % x.get("shot_pos", "50% 28%")) if x.get("shot_h") else "",
           (('<div class="bubble"><p>%s</p></div>' % x["said"])
            if x.get("said") else "")
           + "".join('<div class="mb overlay" style="%s"><p>%s</p></div>'
                     % (b.get("at", ""), b["text"])
                     for b in x.get("bubbles", [])),
           ad.head,
           ('<div class="benefit">%s</div>' % x["benefit"]) if x.get("benefit") else "",
           ad.definition, x.get("deliver", ""), ad.proof,
           kit.cta,
           # One-line terms when the face supplies it: the two-line kit
           # default clipped at the canvas edge under a full-width CTA.
           x.get("terms_line", kit.terms)))


# ------------------------------------------------------------------ registry

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


LAYOUTS = {
    "notice": (_notice, _notice_shell),
    "serif": (_serif, _serif_shell),
    "ladder": (_ladder, _ladder_shell),
    "nameplate": (_nameplate, _nameplate_shell),
    "docket": (_docket, _docket_shell),
    "photo": (_photo, _photo_shell),
}

# The borrowed-format family, added 1 Sep 2026 from the reference set Ramanuj
# sent. Kept in its own module because its provenance is a reference sheet rather
# than a priced face, and that difference has to stay visible: none of the five
# carries a live cost, and two of them are in the toon/chat family that indexes
# 1.22 against par. See adkit/layouts_social.py.
LAYOUTS.update(layouts_social.LAYOUTS)
PROVENANCE.update(layouts_social.PROVENANCE)

# Layouts scaffolded from a reference image with `--new`. Separate module so their
# provenance stays visible: none is lifted from a priced face. See
# adkit/layouts_custom.py for why the scaffold exists at all.
try:
    from . import layouts_custom
    LAYOUTS.update(layouts_custom.LAYOUTS)
    PROVENANCE.update(layouts_custom.PROVENANCE)
except ImportError:                                             # pragma: no cover
    pass


def rules(layout, pal, scale):
    return LAYOUTS[layout][0](pal, scale)


def shell(layout, kit, ad, scale):
    return LAYOUTS[layout][1](kit, ad, scale)


CONTRACT = """
WHAT A LAYOUT MUST PROVIDE
==========================
Written down 15 Sep 2026. It was never written down before, which is why handing
over reference images produced nothing: the gap between a picture and a usable
layout was an undocumented 80-line coding task.

A layout is a pair of functions registered in LAYOUTS:

    _<name>(pal, s)            -> a CSS string. `pal` is the palette, `s` the
                                  auto-fit scale (0.80 to 1.00). Multiply every
                                  px through _px(n, s) so auto-fit can shrink it.
    _<name>_shell(kit, ad, s)  -> the HTML inside <div class="canvas">.

THE FOUR HARD REQUIREMENTS
  1. A sized `.callout` class and a sized `.head` class must appear in the CSS as
     CLASS RULES, not inline styles. `ad_lint` C8 matches class names; a face with
     inline styles only is invisible to the strictest size gate in the repo and
     reads as a clean pass. check_all's "C8 reachability" gate fails the kit.
  2. `.callout` and `.head` must compute to 64px or more. Use _idpx(n, s) rather
     than _px for those two - it clamps at the floor so auto-fit cannot shrink
     identity type below it. `adkit.fit` measures the RENDERED size, so a later
     override that wins in the browser will be caught.
  3. The shell must emit every copy field the ad carries: ad.callout, ad.head,
     ad.definition, and extra["deliver"]. A layout that drops one is legal, but
     `adkit.restyle` will refuse to move any ad whose copy uses the missing field,
     which is why `serif` can only take 2 of 10 faces in one patent kit.
  4. Leave vertical slack as `<div class="grow"></div>`, not as fixed margins.
     `adkit.gaps` blocks a face that pools more than 200px of background in one
     place, and fixed spacing is how that happens.

CHROME IS YOURS. The brand rail, eyebrow, trust row, terms bar and CTA button vary
freely between layouts - restyle reports chrome differences and never blocks them.

    python -m adkit.layouts --new <name>        scaffold one, already renderable
    python -m adkit.layouts --contract          this
"""

SCAFFOLD = '''

# ---------------------------------------------------------------- {name}
# Scaffolded {date} from: {source}
#
# This began as a byte-for-byte clone of `notice`, the cheapest face in the
# account (us22_notice_fifties, Rs 29.65/lead), so it renders and clears every
# size floor before you touch it. Change the CSS to match the reference. Do not
# change the class names or the floors - see `python -m adkit.layouts --contract`.

def _{name}(pal, s):
    return _notice(pal, s)


def _{name}_shell(kit, ad, s):
    return _notice_shell(kit, ad, s)


LAYOUTS["{name}"] = (_{name}, _{name}_shell)
PROVENANCE["{name}"] = ("{source}", "-",
                        "Scaffolded {date}. Still a clone of notice until its CSS "
                        "is written.")
'''


def scaffold(name, source):
    import datetime
    import pathlib
    import re as _re
    if not _re.match(r"^[a-z][a-z0-9_]{1,23}$", name):
        print("layout name must be lowercase letters, digits and underscores: %r"
              % name)
        return 2
    if name in LAYOUTS:
        print("'%s' already exists. Pick another name, or edit it in place." % name)
        return 2
    f = pathlib.Path(__file__).resolve().parent / "layouts_custom.py"
    body = f.read_text(encoding="utf-8")
    if "from .layouts import" not in body:
        body = body.replace(
            "LAYOUTS = {}\nPROVENANCE = {}",
            "# The clone source. Imported lazily inside the functions below to avoid\n"
            "# a circular import - layouts.py imports this module at the bottom.\n"
            "LAYOUTS = {}\nPROVENANCE = {}\n\n\n"
            "def _notice(pal, s):\n"
            "    from .layouts import _notice as f\n"
            "    return f(pal, s)\n\n\n"
            "def _notice_shell(kit, ad, s):\n"
            "    from .layouts import _notice_shell as f\n"
            "    return f(kit, ad, s)\n")
    body += SCAFFOLD.format(name=name, source=source or "a supplied reference",
                            date=datetime.date.today().strftime("%d %b %Y"))
    f.write_text(body, encoding="utf-8")
    print("""
  '%s' scaffolded into adkit/layouts_custom.py.

  It already renders, already clears the 64px floors and already emits every copy
  field, because it starts as a clone of `notice` (Rs 29.65/lead). Nothing about
  the chassis contract is left for you to work out.

  NEXT, and this is the only part that needs the reference in front of you:
    1. open adkit/layouts_custom.py and rewrite _%s(pal, s) - the CSS
    2. rewrite _%s_shell(kit, ad, s) if the structure differs from notice
    3. see it on a real ad:
         python -m adkit.restyle <kit> --ad <ad> --to %s
       which proves the selling copy survived, and reverts if it did not
    4. python check_all.py <kit>

  Until step 1 it is a clone, and --list will say so.
""" % (name, name, name, name))
    return 0


def main(argv):
    if "--contract" in argv:
        print(CONTRACT)
        return 0
    if "--new" in argv:
        i = argv.index("--new")
        if i + 1 >= len(argv):
            print("usage: python -m adkit.layouts --new <name> [--from \"<reference>\"]")
            return 2
        src = ""
        if "--from" in argv:
            j = argv.index("--from")
            if j + 1 < len(argv):
                src = argv[j + 1]
        return scaffold(argv[i + 1], src)
    print(__doc__.split("WHY THIS")[0])
    print("  %-11s %-42s %-18s" % ("layout", "lifted from", "live cost"))
    print("  " + "-" * 76)
    for name, (src, cost, note) in PROVENANCE.items():
        print("  %-11s %-42s %-18s" % (name, src[:42], cost))
        print("  %-11s %s" % ("", note))
    print("\n  A layout with no cost is not a worse layout. It is one nobody has\n"
          "  spent enough on to have an opinion about.\n")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
