#!/usr/bin/env python3
"""Prove the fit gate discriminates, and that the chassis round-trips.

The repo's standing rule (CLAUDE.md): never widen a lexicon or loosen a rule
without re-running its selftest and reporting the before/after fit. A gate that
has never been shown to fire on a bad face and stay quiet on a good one is not
evidence of anything.

Three cases, all rendered through the real Chrome:

  A  a face copied from IndependentDirector_Wave1 ad 01, which shipped
     -> expected CLEAN at scale 1.00
  B  the same face with a definition sentence four times as long
     -> expected FINDINGS (F1 CLIPPED), because the .def eats the flexible slot.
        This is the 26 Aug 2026 defect that passed all five existing gates.
  C  a face whose .callout is forced to 40px by a later override, exactly the way
     IndependentDirector's `tight=True` block does it
     -> expected FINDINGS (F3 FLOOR), where ad_lint C8 reports clean because its
        re.search matches the 66px base rule first

    python -m adkit.selftest
"""
import pathlib
import shutil
import sys
import tempfile

from . import fit
from .chassis import Kit

TAKEAWAYS = [
    "IICA databank registration, done with you",
    "A 50-question mock exam, with answers",
    "Notes, templates and checklists",
    "A 90-day plan to your first board seat",
]
DEF = ("Every listed and large public company must have independent directors, who "
       "are outside members reviewing the accounts and the big decisions.")


def _kit(root):
    return Kit(root=root,
               brand="Skill<i>Arbitrage</i>",
               eyebrow="Independent Director Bootcamp",
               takeaways=TAKEAWAYS,
               cta="Save my seat &#8594;",
               terms=("<b>Free &middot; 12 to 14 September &middot; on Zoom</b><br>"
                      "9 hours live &middot; Sat, Sun 2-5 PM &middot; Mon 7-10 PM"),
               trust="NSE Emerge-listed &middot; NSDC &middot; IIT Roorkee iHUB")


def _face(kit, name, definition, palette="clay"):
    kit.face(name, palette=palette,
             callout="A company secretary?",
             head="Boards need people who <em>know how a board works.</em>",
             card=("Sitting fee, per board meeting",
                   "&#8377;25,000 to &#8377;1,00,000", "10 to 18 meetings a year"),
             definition=definition,
             proof="No prior board seat needed &middot; the exam is open-book")
    return kit


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="adkit_selftest_"))
    (tmp / "html").mkdir()
    chrome = fit.find_chrome()
    results = []
    try:
        # A -- the shipped face
        k = _face(_kit(tmp), "A_shipped", DEF)
        (tmp / "html" / "A_shipped.html").write_text(k.html(k.ads[0], 1.00),
                                                     encoding="utf-8")
        a = fit.check(tmp / "html" / "A_shipped.html", chrome)
        results.append(("A shipped face, scale 1.00", a, False))

        # B -- an over-long definition, the flexible-slot defect
        long_def = DEF + " " + (
            "It is a statutory appointment made by the shareholders on a public "
            "record, it runs for a fixed term of five years renewable once, and the "
            "role carries a duty of independent judgement on the audit committee, "
            "the nomination and remuneration committee, and every material related "
            "party transaction the board is asked to approve in that period. ") * 3
        k2 = _face(_kit(tmp), "B_overstuffed", long_def, palette="pine")
        (tmp / "html" / "B_overstuffed.html").write_text(k2.html(k2.ads[0], 1.00),
                                                         encoding="utf-8")
        b = fit.check(tmp / "html" / "B_overstuffed.html", chrome)
        results.append(("B over-long definition, scale 1.00", b, True))

        # C -- a late override under the C8 floor, the ID `tight` pattern
        k3 = _face(_kit(tmp), "C_override", DEF, palette="navy")
        page = k3.html(k3.ads[0], 1.00).replace(
            "</style>", ".callout{font-size:40px}.head{font-size:38px}</style>")
        (tmp / "html" / "C_override.html").write_text(page, encoding="utf-8")
        c = fit.check(tmp / "html" / "C_override.html", chrome)
        results.append(("C .callout overridden to 40px after the 66px rule", c, True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- landing-page lint: prove L1-L4 fire, and stay quiet on a good page
    from .lp_spine import Camp
    good = Camp(root=tmp, brand="SkillArbitrage", camp="Test Camp",
                base_url="https://growthx.skillarbitra.ge/f/", cta_label="Save my seat",
                when="Free &middot; 12 to 14 September", takeaways=["a", "b", "c"],
                not_promised=["No placement is guaranteed."],
                faq_common=[("Q", "A")], trust="NSE Emerge-listed", footer="SkillArbitrage.")
    good.page(file="p.html", slug="test-slug", palette="clay", h1="H",
              statement="S", definition="Board work is reviewing the accounts.",
              facts=[("l", "b", "s")],
              sections=[("Why", "<p>" + ("word " * 1700) + "</p>")],
              qualifiers=["You have ten years of experience."])
    page = good.build(good.pages[0])
    lp_cases = [
        ("LP clean page", good.lint(page, good.pages[0],
                                    "Board work is reviewing the accounts.")[0], False),
        ("LP L1 dead pay stub",
         good.lint(page.replace('href="https://growthx.skillarbitra.ge/f/test-slug"',
                                'href="#"'), good.pages[0])[0], True),
        ("LP L2 banned qualifier",
         good.lint(page.replace("<h2>Why</h2>", "<h2>This is not for you if</h2>"),
                   good.pages[0])[0], True),
        ("LP L3 em-dash",
         good.lint(page.replace("<h2>Why</h2>", "<h2>Why — really</h2>"),
                   good.pages[0])[0], True),
        ("LP L4 definition missing from fold",
         good.lint(page, good.pages[0], "Patent drafting is writing claims.")[0], True),
        # L6: the page must name the reader in a section heading. The good page
        # above carries the ICP "board member" and a heading of "Why", so it must
        # FIRE; adding a heading that names her must silence it.
        ("LP L6 no heading names the reader",
         good.lint(page, dict(good.pages[0], icp="INDEPENDENT BOARD MEMBERS"))[0], True),
        ("LP L6 quiet when a heading names her",
         good.lint(page.replace("<h2>Why</h2>", "<h2>Why a board member is asked</h2>"),
                   dict(good.pages[0], icp="INDEPENDENT BOARD MEMBERS"))[0], False),
    ]
    for label, found, expect in lp_cases:
        results.append((label, [f for f in found if not f.startswith("L5")], expect))

    # ---- verdict parsing: the ground truth written in CAMPAIGN_MAP.md
    from . import verdicts as V
    by_name, by_number = V.load()
    checks = [
        ("V table REJECTED is read",
         (by_name.get("lp_01_collections_recovery") or {}).get("verdict") == V.REJECTED),
        ("V table APPROVED is read",
         (by_name.get("lp_05_pharmacovigilance") or {}).get("verdict") == V.APPROVED),
        ("V prose rejection is read",
         (by_name.get("lp_05_global_freelance") or {}).get("verdict") == V.REJECTED),
        ("V a folder is NOT an ad name",
         "dataprivacy_mediabuyer_22-24aug" not in by_name),
        ("V numbered verdicts hit the RIGHT kit",
         (V.for_ad("06_x", "ContentWriting_SectionA_29-31Aug", by_name, by_number) or {})
         .get("verdict") == V.REJECTED),
        ("V an approved number stays approved",
         (V.for_ad("05_x", "ContentWriting_SectionA_29-31Aug", by_name, by_number) or {})
         .get("verdict") == V.APPROVED),
        ("V a wrapped continuation line is read",
         (V.for_ad("21_x", "ContentWriting_SectionA_29-31Aug", by_name, by_number) or {})
         .get("verdict") == V.APPROVED),
        ("V no verdict leaks to an unrelated kit",
         V.for_ad("06_x", "WomenRemote_Wave4_SEND_THIS", by_name, by_number) is None),
    ]
    # expect_findings is ALWAYS False here: a passing check produces no findings.
    # Writing `not passed` instead made the assertion self-fulfilling -- got and
    # expected moved together, so every case reported PASS and the block proved
    # nothing. A test that cannot fail is worse than no test.
    for label, passed in checks:
        results.append((label, [] if passed else ["parsed wrong"], False))

    # ---- GOLDEN is derivable, and never contains a recorded reject
    from . import golden as G
    ents = G.collect()
    names = {e["name"].lower() for e in ents}
    rejects = {n for n, r in by_name.items() if r["verdict"] == V.REJECTED}
    gchecks = [
        ("G collects faces from every source",
         len({e["source"] for e in ents}) == len(G.SOURCES)),
        ("G includes Ramanuj's own faces",
         sum(1 for e in ents if e["provenance"] == "ramanuj") > 0),
        ("G excludes every recorded reject", not (names & rejects)),
        ("G joins live cost to the cheapest ad in the account",
         any(e["live"] and e["live"]["cost"] < 31 for e in ents)),
    ]
    for label, passed in gchecks:
        results.append((label, [] if passed else ["failed"], False))

    ok = True
    print()
    for label, findings, expect_findings in results:
        got = bool(findings)
        verdict = "PASS" if got == expect_findings else "FAIL"
        if verdict == "FAIL":
            ok = False
        print("  %-4s %-46s expected %-9s got %s"
              % (verdict, label, "FINDINGS" if expect_findings else "clean",
                 "FINDINGS" if got else "clean"))
        for f in findings:
            print("           " + f)
    print("\n  fit gate discriminates: %s" % ("yes" if ok else "NO -- do not rely on it"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
