#!/usr/bin/env python3
"""One spec per kit. Everything else is generated from it.

Why this exists. Measured 31 Aug 2026 on `IndependentDirector_Wave1`:

    value_props.md   127 lines
    hooks.md          59 lines
    ad_copy.md       480 lines   = 666 lines of hand-typed markdown
                                 + the face data in gen_ads.py
                                 + the page data in gen_lps.py

and it is the SAME CONTENT. For ad 01, `field_definition` is typed verbatim three
times: in `value_props.md`, in the face's `definition=`, and in the landing page's
first fold. `statement` and `turn` are typed in `hooks.md` and again as the face's
call-out and headline. The deliverables are typed again as the takeaways.

Rule 3 *requires* that repetition to reach the page -- which is exactly the
argument for generating it rather than retyping it and then checking it with a
linter. Preflight's fold check and `lp_spine`'s L4 both exist to catch a
divergence that, on this path, cannot occur: there is one string and it is
written into all three places.

What a spec emits:

    value_props.md      in preflight's block format
    hooks.md            in hook_rules' block format
    ad_copy.md          in the block format corpus.py and copy_census.py parse
    html/ + ads/        via adkit.chassis, auto-fitted
    landing_pages/      via adkit.lp_spine, linted

THE DELIVERY SENTENCE IS A KIT CONSTANT, NOT A PER-AD FIELD. It carries an
`{outcome}` slot and nothing else changes between ads. 139 of 150 approved blocks
carry one and 136 name exactly three things; `IndependentDirector_Wave1` wrote a
fresh one per ad, carried 0 of 10, and reads flat. Here it is structurally
impossible to get wrong.

Opt-in. Existing kits keep their own generators and hand-written markdown; nothing
under a shipped kit folder is touched by this module.

    python -m adkit.spec --template > <kit>/spec.py
"""
import html as _html
import os
import pathlib
import re
import sys

from . import chassis, lp_spine
from . import layouts as layouts_mod

# The classes that carry selling copy, as opposed to chrome. Kept identical to
# adkit/restyle.py COPY_CLASSES - see that file for the measurement behind the
# split (one ad through notice then serif: callout/head/def identical, deliver
# renamed to quote, every chrome field different).
COPY_CLASSES = ("callout", "head", "def", "deliver", "quote", "kicker", "elig",
                "barrier")


def _copy_fields(html):
    """The selling-copy strings in a face's HTML, without rendering it."""
    import html as _h
    out = []
    for m in re.finditer(r'<[a-z]+[^>]*class="([^"]*)"[^>]*>(.*?)</[a-z]+>',
                         html, re.S):
        if not any(c in COPY_CLASSES for c in m.group(1).split()):
            continue
        txt = re.sub(r"<[^>]+>", " ", m.group(2))
        txt = re.sub(r"\s+", " ", _h.unescape(txt)).strip()
        if txt:
            out.append(txt)
    return out

AWARENESS = ("unaware", "problem aware", "solution aware", "product aware", "most aware")
ARCHETYPES = {"A": "an occupation", "B": "a life situation",
              "C": "an aspiration (rewrite)", "D": "device-led (do not build)",
              "E": "a broad population (rewrite)"}


# The scored ICP row. preflight.py is the gate and carries the reasoning; this
# only has to emit a line preflight can parse, and fail loudly at spec time
# rather than at the gate. Five dimensions, each 1 to 5, ranked by
# `python preflight.py --shortlist <kit>` before anything is built.
PAIN_DIMS = ("severity", "frequency", "activation", "reachability", "fit")


def _pain_line(name, pain):
    """Normalise pain= into the string preflight parses. None means opted out."""
    if pain is None or pain == "":
        return ""
    if isinstance(pain, str):
        return re.sub(r"\s+", " ", pain).strip()
    missing = [d for d in PAIN_DIMS if d not in pain]
    if missing:
        raise ValueError("%s: pain= is missing %s. All five of %s, each 1 to 5."
                         % (name, ", ".join(missing), ", ".join(PAIN_DIMS)))
    for d in PAIN_DIMS:
        if not (isinstance(pain[d], int) and 1 <= pain[d] <= 5):
            raise ValueError("%s: pain=%s is %r, must be an int 1 to 5"
                             % (name, d, pain[d]))
    return " | ".join("%s %d" % (d, pain[d]) for d in PAIN_DIMS)


def _words(s):
    return len(re.sub(r"<[^>]+>", " ", s or "").split())


class Spec(object):
    def __init__(self, root, brand, eyebrow, camp, base_url, cta, terms, when,
                 delivery, takeaways, not_promised, faq_common, trust, footer,
                 description="", close_h=None, close_p=None, take_h=None):
        """`delivery` is the kit's one delivery sentence and MUST contain the
        literal `{outcome}`. Everything else is a per-kit constant."""
        if "{outcome}" not in delivery:
            raise ValueError(
                "the delivery sentence must carry an {outcome} slot -- it is a kit "
                "constant with one variable clause, not a per-ad sentence. See "
                "SOP/00_CONSTANTS.md section 6.")
        self.root = pathlib.Path(root).parent if str(root).endswith(".py") \
            else pathlib.Path(root)
        self.brand, self.eyebrow, self.camp = brand, eyebrow, camp
        self.base_url, self.cta, self.terms, self.when = base_url, cta, terms, when
        self.delivery = delivery
        self.takeaways, self.not_promised = list(takeaways), list(not_promised)
        self.faq_common, self.trust, self.footer = list(faq_common), trust, footer
        self.description = description
        # The landing page's closing fold. Optional, because the spine has a
        # default - but that default was written for a free camp and said
        # "Registration is free" above a paid button on 13 pages before
        # closing_reader caught it (24 Sep 2026). A paid kit should set both.
        self.close_h, self.close_p = close_h, close_p
        # The take-away heading. Default says nothing about price; a free camp
        # sets "What you take away, free" and a paid one must not.
        self.take_h = take_h
        self.ads = []

    def ad(self, num, name, palette, icp, archetype, awareness, better_job,
           field_definition, deliverables, buying_pressure,
           statement, turn, axis, callout, headline, situation, pivot, outcome,
           lp_h1, lp_facts, lp_sections, lp_qualifiers, slug,
           head=None, card=None, proof="", banner=None, banner_h=None, shot=None,
           lp_fact_source="", faq_extra=(), layout="default", extra=None,
           pain=None, hypothesis=""):
        """One ICP, once. `field_definition` reaches the face, the page and
        value_props.md from this single string.

        `pain` is the scored ICP row (added 4 Sep 2026), either a dict of the five
        dimensions or a ready-made string. Optional so the kits that predate it
        still build, but it prints a nudge when missing: without it an ICP list is
        flat, every candidate looks equal, and the weak cells are only found after
        the kit exists. `python preflight.py --shortlist <kit>` ranks them.
        """
        if archetype not in ARCHETYPES:
            raise ValueError("archetype must be one of %s" % ", ".join(ARCHETYPES))
        if archetype in ("C", "D", "E"):
            print("  SOP/08  %s is archetype %s (%s). Rewrite it into an A or a B "
                  "before building." % (name, archetype, ARCHETYPES[archetype]))
        if awareness.split(".")[0].strip().lower() not in AWARENESS:
            raise ValueError("awareness must start with one of: %s" % ", ".join(AWARENESS))
        if len(deliverables) < 3:
            raise ValueError("%s: preflight blocks on fewer than three named "
                             "deliverables" % name)
        pain_line = _pain_line(name, pain)
        if not pain_line:
            print("  %s has no pain= score. The ICP list stays flat and nothing "
                  "ranks it. See preflight.py --shortlist." % name)
        self.ads.append(dict(
            num=str(num).zfill(2), name=name, palette=palette, icp=icp,
            archetype=archetype, awareness=awareness, better_job=better_job,
            hypothesis=hypothesis,
            field_definition=field_definition, deliverables=list(deliverables),
            buying_pressure=buying_pressure, statement=statement, turn=turn, axis=axis,
            callout=callout, head=head if head is not None else turn,
            headline=headline, situation=situation, pivot=pivot, outcome=outcome,
            card=card, proof=proof, banner=banner, banner_h=banner_h, shot=shot,
            lp_h1=lp_h1, lp_facts=list(lp_facts), lp_sections=list(lp_sections),
            lp_qualifiers=list(lp_qualifiers), slug=slug,
            lp_fact_source=lp_fact_source, faq_extra=list(faq_extra),
            layout=layout, pain=pain_line, extra=dict(extra or {})))
        return self

    # ---------------------------------------------------------------- derived

    def primary_text(self, a):
        """The four moves, assembled. MOVE 3 is the kit constant with this ad's
        outcome clause dropped in -- which is the whole point."""
        return " ".join(x.strip() for x in (
            a["situation"], a["pivot"],
            self.delivery.replace("{outcome}", a["outcome"]),
            self.terms_sentence()) if x and x.strip())

    def terms_sentence(self):
        """MOVE 4 as prose. `self.terms` is the FACE's terms strip, so it is markup:
        it legitimately carries `&#8377;` and `&#183;`. The primary text is pasted
        into Meta as plain prose, so stripping tags is not enough -- the entities
        have to be decoded and the middot separators turned into sentence breaks.

        Found 31 Aug 2026 building GlobalPatent_Wave1, whose ad_copy.md came out
        reading "&#8377;10 &#183; 19 to 21 September" and needed the method
        monkeypatched to stop it. A kit that did not notice would have shipped
        entity codes as ad copy.

        Overriding this on a kit is still fine and is a copy choice, not a
        workaround: the auto-joined form is correct but rarely the best sentence.
        """
        # A <br> is a separator, not whitespace. Before this, a two-line terms
        # strip came out as "live online 14 drafting templates" - the clause
        # either side of the break ran together and then took one full stop
        # between the wrong words (24 Sep 2026, Arbitration practice-split).
        t = re.sub(r"(?i)<br\s*/?>", " · ", self.terms)
        t = _html.unescape(re.sub(r"<[^>]+>", " ", t))
        parts = [re.sub(r"\s+", " ", x).strip(" .") for x in t.split("·")]
        parts = [x for x in parts if x]
        return (". ".join(parts) + ".") if parts else ""

    def lp_file(self, a):
        return "lp_%s_%s.html" % (a["num"], a["name"].split("_", 1)[-1])

    def ad_png(self, a):
        return "%s_%s.png" % (a["num"], a["name"].split("_", 1)[-1]) \
            if not a["name"].startswith(a["num"]) else "%s.png" % a["name"]

    # ---------------------------------------------------------------- writers

    def write_value_props(self):
        out = ["# Value propositions\n",
               "Generated from spec.py. Edit the spec, not this file.\n"]
        for a in self.ads:
            out.append("\n## %s\nad: ads/%s\nlp: landing_pages/%s\n"
                       "better_job: %s\nfield_definition: %s\ndeliverables: %s\n"
                       "buying_pressure: %s\nawareness: %s\nhypothesis: %s\n"
                       "archetype: %s\n%s"
                       % (a["num"], self.ad_png(a), self.lp_file(a), a["better_job"],
                          a["field_definition"], " | ".join(a["deliverables"]),
                          a["buying_pressure"], a["awareness"],
                          a.get("hypothesis") or "TODO - what is this ad testing?",
                          a["archetype"],
                          ("pain_score: %s\n" % a["pain"]) if a.get("pain") else ""))
        (self.root / "value_props.md").write_text("".join(out), encoding="utf-8")

    def write_hooks(self):
        out = ["# Hooks\n\nGenerated from spec.py. Approve this table before any "
               "image is rendered.\n"]
        for a in self.ads:
            out.append("\n## %s | %s\nstatement: %s\nturn: %s\naxis: %s\n"
                       % (a["num"], a["icp"], a["statement"], a["turn"], a["axis"]))
        (self.root / "hooks.md").write_text("".join(out), encoding="utf-8")

    def write_ad_copy(self):
        out = ["# Ad copy: %s\n\nGenerated from spec.py. The delivery sentence is a "
               "kit constant:\n\n> %s\n\nOnly the outcome clause changes between "
               "blocks.\n" % (self.camp, self.delivery)]
        for a in self.ads:
            out.append("\n## %s\n**Primary text:** %s\n**Headline:** %s\n"
                       "**Description:** %s\n**Page:** %s (in landing_pages/) "
                       "· slug `%s`\n"
                       % (a["name"], self.primary_text(a), a["headline"],
                          self.description or self.terms_sentence(),
                          self.lp_file(a), a["slug"]))
        (self.root / "ad_copy.md").write_text("".join(out), encoding="utf-8")

    def probe_layouts(self):
        """Which layouts can carry each ad's copy, WITHOUT rendering anything.

        Why this exists (15 Sep 2026). A batch visual refresh has to know which
        (ad, layout) pairs are legal, and layouts are not interchangeable - they
        consume different field sets, so some drop a line. Finding that out by
        trial costs a full render each time, and a render is ~19s because it drives
        Chrome once per scale probe plus once per screenshot. Five ads against
        eleven layouts would be about sixteen minutes.

        But the question is answerable from the HTML STRING alone, which is pure
        string building. So this builds every (ad, layout) face in memory, with no
        Chrome and no files, and reports the copy fields each one would carry.
        One pass, well under a second, and `adkit.restyle --spread` then needs a
        single real render for the assignment it picks.
        """
        import json as _json
        out = {}
        for a in self.ads:
            per = {}
            for name in sorted(getattr(layouts_mod, "LAYOUTS", {})):
                kit = chassis.Kit(root=self.root, brand=self.brand,
                                  eyebrow=self.eyebrow, takeaways=self.takeaways,
                                  cta=self.cta, terms=self.terms, trust=self.trust)
                self._one_face(kit, a, layout=name)
                try:
                    html = kit.html(kit.ads[-1], 1.0)
                except Exception as exc:                        # noqa: BLE001
                    per[name] = {"error": str(exc)[:120]}
                    continue
                per[name] = {"text": _copy_fields(html)}
            out[a["name"]] = per
        print("ADKIT_PROBE_JSON " + _json.dumps(out))
        return 0

    def build_faces(self, *only):
        kit = chassis.Kit(root=self.root, brand=self.brand, eyebrow=self.eyebrow,
                          takeaways=self.takeaways, cta=self.cta, terms=self.terms,
                          trust=self.trust)
        for a in self.ads:
            self._one_face(kit, a)
        return kit.render(*only)

    def _one_face(self, kit, a, layout=None):
        """Add one ad to a chassis Kit. Factored out of build_faces so that
        probe_layouts() can build the same face under a different layout without
        duplicating this argument list - two copies of it would drift."""
        kit.face(self.ad_png(a)[:-4], palette=a["palette"], callout=a["callout"],
                 head=a["head"], card=a["card"],
                 # `face_definition` lets a kit keep the field definition on the
                 # PAGE (Rule 2 step 4, and lint L4 checks the first fold) while
                 # leaving it OFF the face. Added 4 Sep 2026: on US Corporate Law
                 # the definition sentence was a third block of body copy under a
                 # head that already says the job, and it read as clutter --
                 # "adding text but not a value and the ad is looking too hotch
                 # potch". None of the four approved USCL faces carries one.
                 # Default is unchanged, so every existing kit keeps it.
                 definition=a["extra"].get("face_definition",
                                           a["field_definition"]),
                 proof=a["proof"], banner=a["banner"], banner_h=a["banner_h"],
                 shot=a["shot"],
                 layout=layout if layout is not None else self._layout_of(a),
                 extra=dict(a["extra"],
                            deliver=a["extra"].get(
                                "deliver",
                                self.delivery.replace("{outcome}",
                                                      a["outcome"]))))

    def build_pages(self):
        camp = lp_spine.Camp(root=self.root, brand=self.brand, camp=self.camp,
                             base_url=self.base_url, cta_label=self.cta,
                             when=self.when, takeaways=self.takeaways,
                             not_promised=self.not_promised,
                             faq_common=self.faq_common, trust=self.trust,
                             footer=self.footer)
        camp.close_h, camp.close_p = self.close_h, self.close_p
        camp.take_h = self.take_h
        defs = {}
        for a in self.ads:
            # The sub-head under the H1 used to be the ad's `turn`, which is
            # also what most lp_h1 lines are written from, so the first fold said
            # the same sentence twice: "Somebody is paid to write the papers you
            # read" over "Somebody is paid to write those papers." The approved
            # ACW pages put the ICP band there instead, so the fold reads as
            # promise, then who it is for, then what the field is.
            camp.page(file=self.lp_file(a), slug=a["slug"], palette=a["palette"],
                      h1=a["lp_h1"], statement=a["callout"],
                      definition=a["field_definition"],   # <- the same single string
                      facts=a["lp_facts"], sections=a["lp_sections"],
                      qualifiers=a["lp_qualifiers"], faq_extra=a["faq_extra"],
                      fact_source=a["lp_fact_source"],
                      icp=a["icp"] + " " + a["callout"])   # L6 only
            defs[self.lp_file(a)] = a["field_definition"]
        return camp.render(ad_definitions=defs)

    # ---------------------------------------------------- the restyle override
    #
    # WHY (15 Sep 2026). Asked for directly: "i share a sample of an ad visual
    # that i like, and the ads are regenerated using that sample as reference
    # without changing text. i have tried it in claude and it does not happen."
    #
    # It did not happen because there was no operation for it. Restyling meant
    # hand-editing `layout=` inside a kit's spec.py, and a model in there to change
    # one keyword will also tidy a headline on the way past - so the text moves,
    # which is the one thing the request said not to do.
    #
    # So the override lives OUTSIDE spec.py, in <kit>/.restyle.json ({ad: layout}),
    # and spec.py stays the source of record, unedited. `python -m adkit.restyle`
    # writes that file, re-renders, and then PROVES the text did not move by
    # diffing every text node on the face before and after.

    RESTYLE_FILE = ".restyle.json"

    def _overrides(self):
        import json
        f = pathlib.Path(self.root) / self.RESTYLE_FILE
        if not f.is_file():
            return {}
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            return {}

    def _layout_of(self, a):
        return self._overrides().get(a["name"], a["layout"])

    def report(self):
        print("\n  %-26s %-4s %-14s %-10s %5s %5s" %
              ("ad", "arch", "awareness", "layout", "prim", "head"))
        print("  " + "-" * 74)
        levels, lays = set(), []
        for a in self.ads:
            lvl = a["awareness"].split(".")[0].strip().lower()
            levels.add(lvl)
            lays.append(self._layout_of(a))
            pw, hw = _words(self.primary_text(a)), _words(a["headline"])
            flag = "" if 80 <= pw <= 110 else "  <- outside 80-110"
            flag += "" if 4 <= hw <= 10 else "  <- outside 4-10 words"
            print("  %-26s %-4s %-14s %-10s %5d %5d%s"
                  % (a["name"][:26], a["archetype"], lvl[:14],
                     a["layout"][:10], pw, hw, flag))
        # Structural diversity. This used to fire only when EVERY face shared one
        # layout, which is the one case nobody ships - 8 of 10 in a single skeleton
        # passed silently. The rule is now a share: no layout may carry more than
        # half a wave of four or more.
        #
        # The threshold is the reviewer's, not a finding from cost. Rule 4b and
        # "make sure each have distinct colour palette" are his; only two styles
        # carry a measured cost (pay chart 2.34x, toon/chat 1.22x) and neither
        # speaks to sameness. So this WARNS and never blocks - a gate that blocks
        # on an unpriced aesthetic rule would be inventing evidence.
        if len(self.ads) >= 4:
            top, n = "", 0
            for lay in set(lays):
                if lays.count(lay) > n:
                    top, n = lay, lays.count(lay)
            if n > len(lays) / 2.0:
                from . import layouts as _layouts
                print("\n  WARNING %d of %d faces use the '%s' layout. Meta treats "
                      "visually\n  similar faces as one ad, and a wave in one skeleton "
                      "is one template\n  with the widget swapped. %d distinct layout(s) "
                      "here; adkit/layouts.py\n  carries %d. Restyle one without touching "
                      "its copy:\n    python -m adkit.restyle %s --list"
                      % (n, len(lays), top, len(set(lays)),
                         len(getattr(_layouts, "LAYOUTS", {})),
                         pathlib.Path(self.root).name))
        if len(levels) == 1 and len(self.ads) > 1:
            print("\n  WARNING every block carries the same awareness level (%s). "
                  "That is how\n  a wave of twenty ads reads as twenty copies of one "
                  "ad." % levels.pop())

    def write(self, *only, **kw):
        """Emit the markdown, then build. Returns 0 when everything is clean."""
        # A kit's spec.py ends in `sys.exit(spec.write())`, so it cannot be
        # imported without rendering. adkit.restyle --spread needs the layout
        # compatibility matrix and nothing else, so it sets this and gets it
        # without Chrome, without touching a single file.
        if os.environ.get("ADKIT_PROBE_LAYOUTS"):
            return self.probe_layouts()
        self.root.mkdir(parents=True, exist_ok=True)
        self.write_value_props()
        self.write_hooks()
        self.write_ad_copy()
        self.report()
        if kw.get("copy_only"):
            return 0
        print()
        rc = self.build_faces(*only)
        print()
        rc |= self.build_pages()
        print("\n  Now: approve hooks.md as a table, then ONE pair, then the rest.\n"
              "  Then run  python check_all.py %s" % self.root.name)
        return rc


TEMPLATE = '''"""<Camp name> — spec. Everything in the kit is generated from this file."""
import sys
sys.path.insert(0, r"<repo root>")
from adkit.spec import Spec
from adkit.lp_spine import paras, bullets, box, counted

spec = Spec(
    root=__file__,
    brand="Skill<i>Arbitrage</i>",
    eyebrow="<Camp Name>",
    camp="<Camp Name>, <dates>",
    base_url="https://growthx.skillarbitra.ge/f/",
    cta="Save my seat &#8594;",
    terms="<b>Free &middot; <dates> &middot; on Zoom</b><br>9 hours live &middot; live only",
    when="Free &middot; <dates> &middot; live on Zoom<br>9 hours live, live only, no recordings",
    # THE KIT CONSTANT. Three named things the reader leaves holding, third is the plan.
    delivery=("In our free 3-day live bootcamp, we show you <thing one>, <thing two>, "
              "and {outcome}."),
    takeaways=["<takeaway 1>", "<takeaway 2>", "<takeaway 3>", "<takeaway 4>"],
    not_promised=["No seat or placement is guaranteed.",
                  "No income figure is promised. Figures quoted are published market data.",
                  "No recordings. The sessions are live only."],
    faq_common=[("<common question>", "<answer>")],
    trust="NSE Emerge-listed &middot; NSDC &middot; IIT Roorkee iHUB",
    footer="SkillArbitrage. This is an educational programme. No placement is guaranteed.",
)

spec.ad(
    num=1, name="01_<icp_slug>", palette="clay", slug="<funnel-slug>",
    icp="<ICP IN CAPS>", archetype="A",          # A or B only
    awareness="problem aware. <what that changes about this ad>",
    # What this ad TESTS, as a claim that could turn out to be WRONG. "This will
    # work" cannot be wrong and is blocked. Name the belief you are betting
    # against, so a rejection teaches the next kit something about the reader
    # rather than only about this face. Pairs with adkit.verdict --review.
    hypothesis="<she believes X, so showing Y should beat Z>",
    better_job="<the different, better job — never the same job with more work>",
    field_definition="<X is Y, in ordinary words. Reaches the face AND the page from here.>",
    deliverables=["<named thing>", "<named thing>", "<named thing>"],
    buying_pressure="<the named force: a frozen rate, a notice period, a ceiling>",
    # the scored ICP row, each 1 to 5. Ranked by preflight.py --shortlist BEFORE
    # anything is built, so a weak cell is struck while striking one is free.
    #   severity  what it costs them     frequency  how often it bites
    #   activation  is something forcing the decision NOW
    #   reachability  can this exact person be targeted on Meta
    #   fit  does this camp change the outcome for them
    pain=dict(severity=4, frequency=4, activation=4, reachability=4, fit=4),
    # hook (hooks.md)
    statement="<the reader's present tense>", turn="<the turn>",
    axis="<what the two clauses share — the human column>",
    # face
    callout="<the question that names the ICP>",
    card=("<label>", "<one number>", "<sub>"),
    proof="<small proof line>",
    # copy (four moves; MOVE 3 comes from the kit delivery sentence)
    situation="<~12 words, concrete nouns, no adjectives>",
    pivot="<~25 words: the asset they have is worth more somewhere else>",
    outcome="<the clause that completes the delivery sentence>",
    headline="<4-10 words, names the destination role>",
    # landing page
    lp_h1="<the ad's promise, same words>",
    lp_facts=[("<label>", "<big>", "<sub>")],
    lp_fact_source="<where these figures come from>",
    lp_sections=[("<why this reader>", paras(["<para>", "<para>"])),
                 ("<N sectors hiring this>", counted([("<row>", "<body>")]))],
    lp_qualifiers=["<you are in the right room if...>"],
)

sys.exit(spec.write())
'''


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if "--template" in argv:
        print(TEMPLATE.replace("<repo root>",
                               str(pathlib.Path(__file__).resolve().parent.parent)))
        return 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
