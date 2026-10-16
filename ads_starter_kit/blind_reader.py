#!/usr/bin/env python3
"""The blind-reader test, run as an actual isolated read instead of a box you tick.

WHY THIS EXISTS (15 Sep 2026)
=============================
AD_CREATION_DIRECTOR.md 12.5 and CLAUDE.md both prescribe this test and both say,
in as many words, that the session which wrote the brief cannot administer it:

    "You cannot run this test on your own writing. You wrote the brief, so your
     brain fills the gap and the fold reads fine to you - that's not carelessness,
     it's contamination, and it's why cryptic ads survive to Ramanuj even from a
     session that had every rule in this file in front of it."

The instruction was there. Nothing enforced it. A grep on 15 Sep 2026 found
`blind.reader` in 30 files, every one of them prose, and in zero scripts:
`creative_review.py` is the only judgment-layer tool and is self-described v0
fitted on one batch. So the check aimed squarely at this account's most expensive
rejection - "very complicated, very cryptic", said at least six times - was the
last one still running on the honour system, while pixel gaps, type floors and
hedge windows all got real gates.

WHAT THIS OWNS, AND WHAT IT CANNOT
==================================
Python cannot be the reader. What it CAN own is everything around the read, which
is exactly where the test was leaking:

  1. THE UNIT IS THE RENDERED FACE. The reader is handed the PNG, because that is
     what a person on Instagram actually sees - hierarchy, type size and all. An
     earlier draft of this tool dumped extracted HTML text instead; that works
     only for faces this repo still holds in source, which on 15 Sep 2026 was
     ONE of the nine priced or approved winners. The PNG route finds 148.

  2. CONTROLS, AUTOMATICALLY. The director says: "IF A BLIND READ COMES BACK BAD,
     RUN THE SAME TEST ON THE PRICED WINNERS BEFORE ACTING ON IT." That is the
     right instruction and it arrives too late - it is remembered only after bad
     news, by which point four rebuild passes were already spent chasing a broken
     ruler (measured 3 Sep 2026, the Patent faces). Here the controls go in BEFORE
     the read, every time.

  3. BLINDING. Candidates and controls are copied into .blind/ under opaque names
     (F01.png, F02.png, ...) and shuffled. The reader cannot tell which face is
     under test - the filename and the folder give nothing away - and neither can
     the operator spawning the agents, so a bad verdict cannot be quietly
     discounted after the fact. The key is written separately and never sent.

  4. A RELATIVE VERDICT. An absolute threshold is a broken ruler, and this is
     measured, not assumed: on call-out + head alone the four Patent faces that
     carry a live cost scored 0 of 4 CLEAR, including icp_28_biomedical_devices at
     Rs 91.36, the cheapest patent ad in the account. A test that fails every ad
     that ran cheaply does not discriminate. So a candidate is blocked only when it
     reads WORSE THAN THE CONTROL FLOOR. If the controls themselves score at the
     floor, this reports ERROR and blocks nothing: the instrument failed.

  5. STALENESS, BY CONTENT. `--score` writes .blind/result.json with a hash of
     every face, so check_all can tell a kit that passed a blind read from one that
     passed and was then rebuilt. It hashes rather than reading mtimes: a restyle
     applied and reverted re-renders byte-identical faces, and a gate that cries
     stale on an unchanged face teaches people to ignore it.

THE THREE STATES ARE check_all.py's, DELIBERATELY
=================================================
PASS / FINDINGS / ERROR, where ERROR means the test did not really run - no
controls resolved, a collapsed control band, or a partial set of answers. A test
that silently degrades to "nothing to report" is the 25 Aug failure this repo has
already paid for once.

USAGE
=====
    python blind_reader.py --prepare <kit>      write the blinded packets
    python blind_reader.py --score <kit>        unblind, score against the controls
    python blind_reader.py --status <kit>       did a blind read run, and is it stale
    python blind_reader.py --why                the evidence behind each rule
    python blind_reader.py --selftest           re-check controls and blinding

Between the two steps you spawn ONE fresh subagent per packet (Agent tool,
`general-purpose` or `Explore`), whose prompt is the packet body and NOTHING else -
no kit path, no brief, no ICP list. Paste each reply verbatim into
.blind/answers.txt. `--prepare` prints the exact instruction.
"""
import argparse
import hashlib
import html
import json
import os
import pathlib
import random
import re
import shutil
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).parent.resolve()

# A control is a face that demonstrably worked. "Worked" is one of two things and
# never a third: the Meta pull priced it at or under this ceiling, or Ramanuj
# approved it. An in-house APPROVED label is not evidence and admits nothing here -
# the same selection rule adkit/golden.py uses, from the 31 Aug correction.
CONTROL_CPL_CEILING = 75.0     # Rs/lead. Par is ~Rs 60-80 across the free camps.
N_CONTROLS = 3

# Questions 1-3 are SCORED (parse_answers reads only those). 4-6 are read by the person running
# the check and never scored, so adding them moved no verdict:
#   4 and 5 are the memory rule "always check the value prop" (Ramanuj, 26 Aug 2026), which was
#     only ever asked by hand;
#   6 caught what 1-3 could not on IndependentDirector_Calendar 01, 28 Sep 2026: a 3/3 face
#     carrying "the company's CFO" (no company named) and a bare "IICA databank" (never
#     explained). The user found the first; question 6 found the second.
QUESTIONS = """1. Who is this addressed to?
2. What job would I be doing?
3. What will I be able to do on the last day that I cannot do today?
4. In one sentence, what is this ad offering you that you do not have now?
5. If you were the person addressed, would this feel like a step UP or a step DOWN from the career you had?
6. Is there any phrase that points at something the ad never tells you (for example "the company" when no company is named), or a term it never explains? Quote it, or say NONE."""

READER_PROMPT = """Read the image at this exact path and nothing else:

    {img}

It is a single advertisement, exactly as it would appear to someone scrolling
past it. You have NO other context. Do not open any other file, do not look
around the folder it sits in, and do not guess at a product, company, course or
brief beyond what is visible in the image itself. If the image does not tell you,
the answer is CANNOT ANSWER - that is a useful answer here, not a failure.

Answer all six questions in one line each. Reply in exactly this format and
add nothing else - no preamble, no summary, no advice about the ad:

{fid}
1: <your answer, or CANNOT ANSWER>
2: <your answer, or CANNOT ANSWER>
3: <your answer, or CANNOT ANSWER>
4: <your answer, or CANNOT ANSWER>
5: <UP or DOWN, and a few words why, or CANNOT ANSWER>
6: <quote any phrase, or NONE>

The questions:

{questions}"""


# ----------------------------------------------------- text, for the record only

class _Face(HTMLParser):
    """Pull every text node off a face in render order, attributed to the nearest
    classed ancestor so `<div class="head">Journals <em>commission</em> reviews</div>`
    comes back as one line and not three.

    This is NOT what the reader sees - the reader gets the PNG. It is written
    beside each packet so that a verdict can be argued about later without
    re-rendering, and so a face with no PNG yet can still be read at the hooks
    stage."""

    def __init__(self):
        HTMLParser.__init__(self)
        self.stack, self.nodes, self.n = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "img", "meta", "link", "hr"):
            return
        self.n += 1
        self.stack.append((self.n, dict(attrs).get("class", "")))

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if not data.strip():
            return
        owner = None
        for i, c in reversed(self.stack):
            if c:
                owner = (i, c)
                break
        if owner is None:
            owner = self.stack[-1] if self.stack else (0, "")
        self.nodes.append((owner[0], owner[1], data))


def _sizes(css):
    """class -> font-size px, taking the LAST matching rule, not the first.

    ad_lint C8 takes the first and is wrong for exactly this reason: a later
    override wins in the browser and C8 cannot see it. Measured 31 Aug 2026, 7 of
    10 shipped IndependentDirector faces render under C8's floor while it reports
    them clean (memory: c8_reads_first_css_rule)."""
    out = {}
    for m in re.finditer(r"\.([A-Za-z0-9_-]+)[^{}]*\{([^}]*)\}", css, re.S):
        s = re.search(r"font-size:\s*([\d.]+)px", m.group(2))
        if s:
            out[m.group(1)] = float(s.group(1))
    return out


def extract(path):
    """[(text, size_px, classes)] in render order. Spacers carry no text, so drop."""
    raw = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", raw, re.S))
    sizes = _sizes(css)
    body = re.search(r"<body[^>]*>(.*)</body>", raw, re.S)
    p = _Face()
    p.feed(body.group(1) if body else raw)

    merged, order = {}, []
    for eid, cls, text in p.nodes:
        if eid not in merged:
            merged[eid] = [cls, []]
            order.append(eid)
        merged[eid][1].append(text)

    out = []
    for eid in order:
        cls, parts = merged[eid]
        text = re.sub(r"\s+", " ", html.unescape(" ".join(parts))).strip()
        if not text:
            continue
        found = [sizes[c] for c in cls.split() if c in sizes]
        out.append((text, max(found) if found else None, cls))
    return out


def render_text(nodes):
    seen = [px for _, px, _ in nodes if px]
    big = max(seen) if seen else 0
    lines = []
    for text, px, _ in nodes:
        tag = ("[LARGEST LINE]" if px and px == big
               else ("[%dpx]" % px if px else "[small print]"))
        lines.append("%-18s %s" % (tag, text))
    return "\n".join(lines)


# ------------------------------------------------------------------- controls

def controls(exclude_kit, n=N_CONTROLS):
    """Faces that demonstrably worked, priced first.

    Priced beats approved because money settles an argument and a label does not:
    `feedback_only_ramanuj_approval_counts` plus adkit/golden.py's note that the
    priced tables are "the only combination that settles an argument". Approved
    faces fill the rest of the slots."""
    sys.path.insert(0, str(ROOT))
    try:
        from adkit import corpus as _corpus
        rows = _corpus.index()
    except Exception as exc:                                    # noqa: BLE001
        return [], "could not read the corpus: %s" % exc

    exclude = pathlib.Path(exclude_kit).resolve()
    priced, approved, seen = [], [], set()
    for row in rows:
        png = row.get("png")
        kit_dir = row.get("kit_dir")
        if not png or not kit_dir:
            continue
        try:
            if pathlib.Path(kit_dir).resolve() == exclude:
                continue
        except OSError:
            continue
        png = pathlib.Path(png)
        if not png.is_file() or png in seen:
            continue
        live = row.get("live") or {}
        # The live cost must belong to THIS face, not a namesake. Found 17 Sep 2026:
        # corpus.match_live joins on shared words, so every refresh of a reader
        # inherits its predecessor's price. `us43_search_small_town`, a face shipped
        # that day and never run, and `us04_small_town` both carried
        # `us25_notice_small_town`'s Rs 40 and were picked as "priced" controls. A
        # control must be the ad that actually spent, so require one name to
        # contain the other ("RID_i7_forces" / "i7_forces", "USACC_us05_evening" /
        # "us05_evening").
        own = live.get("name", "").lower()
        mine = str(row.get("ad", "")).lower()
        if own and not (mine in own or own in mine):
            live = {}
        cheap = (live.get("family") == "lead"
                 and live.get("cost", 1e9) <= CONTROL_CPL_CEILING)
        if cheap:
            seen.add(png)
            priced.append(dict(src=str(png), ad=row["ad"], cost=live["cost"],
                               why="Rs%.0f/lead, live" % live["cost"]))
        elif row.get("approved"):
            seen.add(png)
            approved.append(dict(src=str(png), ad=row["ad"], cost=9e9,
                                 why="Ramanuj approved"))
    priced.sort(key=lambda r: r["cost"])
    # A deterministic sample of the approved pool, so a run is reproducible but the
    # same three faces are not the control set for every kit forever.
    random.Random(hash(str(exclude)) & 0xFFFF).shuffle(approved)
    pool = priced + approved
    return pool[:n], ""


# -------------------------------------------------------------------- prepare

def _faces_hash(kit):
    """A content hash of every candidate face.

    This was an mtime comparison until 15 Sep 2026, when a restyle that was
    applied and then reverted re-rendered the kit to BYTE-IDENTICAL faces and the
    gate reported STALE anyway. A gate that cries stale on an unchanged face
    teaches people to ignore it, which is worse than not having it. Content, not
    timestamps."""
    h = hashlib.sha256()
    for p in _candidates(kit):
        h.update(p.name.encode("utf-8"))
        h.update(p.read_bytes())
    return h.hexdigest()


def _candidates(kit):
    ads = kit / "ads"
    if not ads.is_dir():
        return []
    # 22 Sep 2026: the old pattern matched "review" ANYWHERE in the name, so a real face
    # called 05_woman_phd_litreview.png (AcademicWriting_Wave1_MediaBuyer_24-26Oct) was
    # silently dropped from the test and the kit read as PASS with 29 of 30 faces measured.
    # Sheets and boards are named FOR what they are (contact_sheet.png, review_board.png,
    # index.png, thumb_01.png, faces_grid.png), so match the word at the start of the stem
    # or as a suffix token (_sheet, _grid, _thumb), never inside a face's own words.
    faces = sorted(p for p in ads.glob("*.png")
                   if not re.search(r"^(index|contact|review|sheet|thumbs?|grid)(_|$)"
                                    r"|_(sheet|grid|thumbs?)$", p.stem, re.I))
    # 23 Sep 2026: a CAROUSEL is one ad whose cards are <stem>_c1.._cN, and the unit of this
    # test is the FIRST FOLD (feedback_blind_reader_unit_is_the_first_fold). Card 1 is what a
    # scroller sees before deciding to swipe, so read card 1 and drop the rest. Without this
    # the Tech Law carousel kit offered 40 packets for 10 ads, which is why the gate was left
    # unrun and reported ERROR. A kit of single faces is untouched: nothing ends in _c<digit>.
    if any(re.search(r"_c\d+$", p.stem) for p in faces):
        faces = [p for p in faces if not re.search(r"_c\d+$", p.stem)
                 or re.search(r"_c1$", p.stem)]
    return faces


def prepare(kit, seed=None):
    kit = pathlib.Path(kit).resolve()
    faces = _candidates(kit)
    if not faces:
        print("ERROR  no ads/*.png in %s. The reader needs the rendered face - "
              "render the kit first." % kit.name)
        return 2

    ctrl, note = controls(kit)
    if note:
        print("  note: %s" % note)
    if len(ctrl) < 2:
        print("ERROR  only %d control face(s) resolved. Without them this test cannot\n"
              "       tell a bad ad from a broken ruler, which is the one failure it\n"
              "       exists to prevent. A control is an approved face or one the Meta\n"
              "       pull priced at or under Rs%.0f/lead."
              % (len(ctrl), CONTROL_CPL_CEILING))
        return 2

    items = [dict(src=str(f), kind="candidate", ad=f.stem, why="under test")
             for f in faces]
    items += [dict(src=c["src"], kind="control", ad=c["ad"], why=c["why"])
              for c in ctrl]

    random.Random(20260915 if seed is None else seed).shuffle(items)

    out = kit / ".blind"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()

    key = []
    for i, it in enumerate(items, 1):
        fid = "F%02d" % i
        img = out / ("%s.png" % fid)
        shutil.copyfile(it["src"], img)
        (out / ("packet_%s.txt" % fid)).write_text(
            READER_PROMPT.format(img=img, fid=fid, questions=QUESTIONS),
            encoding="utf-8")
        # the text dump, for the record - never sent to the reader
        srchtml = kit / "html" / ("%s.html" % it["ad"])
        if it["kind"] == "candidate" and srchtml.is_file():
            (out / ("text_%s.txt" % fid)).write_text(
                render_text(extract(srchtml)), encoding="utf-8")
        it.update(fid=fid, img=str(img))
        key.append(it)

    (out / "key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    ans = out / "answers.txt"
    ans.write_text("# Paste each subagent reply below, verbatim. One block per face.\n",
                   encoding="utf-8")

    n_c = sum(1 for k in key if k["kind"] == "candidate")
    print("\n  kit: %s" % kit.name)
    print("  %d packet(s) in %s" % (len(key), out))
    print("  %d candidate(s) + %d control(s), shuffled behind opaque ids.\n"
          % (n_c, len(ctrl)))
    print("  the controls in this run (the reader is NOT told which these are):")
    for c in ctrl:
        print("    %-34s %s" % (c["ad"], c["why"]))
    print("""
  NOW, one subagent per packet:
    read packet_F*.txt and pass its body as the ENTIRE prompt of a fresh subagent
    (Agent tool, general-purpose or Explore). No kit path, no brief, no ICP list,
    nothing about this account. Launch them in ONE message so they run at once and
    cannot see each other's answers.

    WHAT THIS GATE CANNOT SEE (added 1 Oct 2026, after Ruchika caught in one glance a
    headline twenty blind readers had just passed 3/3):

      This gate measures whether a face CAN be decoded. It does not measure whether a face
      reads WITHOUT decoding, and it is blind to a headline that sells a chore instead of a
      career. Corporate Finance wave 6 ran "Write the loan proposal, not just fill the form"
      on all twenty faces. Every reader answered "what job would I be doing" correctly, so
      every face scored 3/3 and read as a step UP. The line still offers a loan consultant
      different paperwork at the same desk, which is CLAUDE.md Rule 1, and it never once says
      the reader ends up in corporate finance, which is the 21 Sep Notify rejection.

      NOT MECHANICAL, do by hand before trusting a pass: read each headline on its own and
      ask "does this name a career, or a task?" If the reader could do the thing in the
      headline tomorrow at their current desk, it is a chore. No score here will tell you.

  Paste every reply verbatim into:
    %s

  Then:
    python blind_reader.py --score "%s"
""" % (ans, kit.name))
    return 0


# ---------------------------------------------------------------------- score

FID = re.compile(r"^\s*\**\s*(F\d{2})\s*\**\s*$")


def parse_answers(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = FID.match(line)
        if m:
            cur = m.group(1)
            out.setdefault(cur, {})
            continue
        q = re.match(r"\s*\**\s*([123])\s*[:.)]\s*(.+)", line)
        if q and cur:
            out[cur][int(q.group(1))] = q.group(2).strip().strip("*").strip()
    return out


def _clear(ans):
    if not ans:
        return False
    a = ans.strip().lower().rstrip(".")
    return not (a.startswith("cannot answer")
                or a.startswith("cannot tell")
                or a in ("n/a", "-", "unclear", "unknown", "not stated"))


def score(kit):
    kit = pathlib.Path(kit).resolve()
    out = kit / ".blind"
    keyf, ansf = out / "key.json", out / "answers.txt"
    if not keyf.exists():
        print("ERROR  no %s - run --prepare first." % keyf)
        return 2
    key = json.loads(keyf.read_text(encoding="utf-8"))
    answers = parse_answers(ansf.read_text(encoding="utf-8")
                            if ansf.exists() else "")

    missing = [k["fid"] for k in key if k["fid"] not in answers]
    if missing:
        print("ERROR  no answer for %d of %d face(s): %s\n"
              "       A partial read is not a pass - that is the 25 Aug failure mode.\n"
              "       Spawn the missing subagents, paste their replies into\n"
              "       %s" % (len(missing), len(key), " ".join(missing), ansf))
        return 2

    for k in key:
        a = answers[k["fid"]]
        k["answers"] = dict((str(q), a.get(q, "")) for q in (1, 2, 3))
        k["score"] = sum(1 for q in (1, 2, 3) if _clear(a.get(q, "")))

    ctrl = [k for k in key if k["kind"] == "control"]
    cand = [k for k in key if k["kind"] == "candidate"]
    floor = min(k["score"] for k in ctrl)

    width = max(len(k["ad"]) for k in key)
    print("\n  kit: %s\n" % kit.name)
    print("  %-4s %-*s %-10s %-6s %s"
          % ("id", width, "face", "kind", "clear", "what it is"))
    print("  " + "-" * (width + 44))
    for k in sorted(key, key=lambda r: (r["kind"], -r["score"])):
        print("  %-4s %-*s %-10s %d/3    %s"
              % (k["fid"], width, k["ad"], k["kind"], k["score"], k["why"]))

    print("\n  control floor: %d/3   (the worst score among faces that were approved "
          "or ran cheap)" % floor)

    verdict = "PASS"
    rc = 0
    if floor == 0:
        verdict, rc = "ERROR", 2
        print("""
  ERROR  a face that WORKED scored 0/3. The instrument failed, not the ads.
         Blocking nothing. This is the 3 Sep Patent result exactly: on a partial
         face the four priced patent ads scored 0 of 4 CLEAR, and four rebuild
         passes were spent chasing a ruler rather than a defect. Check what the
         reader was actually sent (.blind/packet_*.txt, .blind/F*.png) before
         reading anything into the candidate scores above.""")
    else:
        bad = [k for k in cand if k["score"] < floor]
        if bad:
            verdict, rc = "FINDINGS", 1
            print("\n  FINDINGS  %d candidate(s) read less clearly than a face that "
                  "worked:\n" % len(bad))
            for k in bad:
                print("    %s  (%d/3, floor %d)" % (k["ad"], k["score"], floor))
                for q in ("1", "2", "3"):
                    a = k["answers"][q]
                    print("      %s %s. %s" % ("  " if _clear(a) else "XX", q,
                                               a or "(no answer)"))
                print("      -> nine times out of ten the missing piece is the")
                print("         plain-words field-definition sentence (Rule 2, step 4).")
            print("\n  A face below the control floor does not get shown to anyone until")
            print("  it is fixed and re-read. Same weight as a preflight.py blocker.")
        else:
            print("\n  PASS  every candidate read at least as clearly as a face that was")
            print("        approved or ran cheap. Comprehension only - this says")
            print("        nothing about desire (director 12.5).")

    (out / "result.json").write_text(json.dumps(dict(
        verdict=verdict, floor=floor, faces_hash=_faces_hash(kit),
        candidates=[dict(ad=k["ad"], score=k["score"]) for k in cand],
        controls=[dict(ad=k["ad"], score=k["score"], why=k["why"]) for k in ctrl],
    ), indent=2), encoding="utf-8")
    return rc


# --------------------------------------------------------------------- status

def status(kit):
    """Did a blind read actually run for the faces as they stand right now?

    Without this, the gate is defeated by rebuilding a face after the read - which
    is the ordinary way of working, not a dodge."""
    kit = pathlib.Path(kit).resolve()
    res = kit / ".blind" / "result.json"
    if not res.exists():
        print("ERROR  no blind read has been run for %s.\n"
              "       python blind_reader.py --prepare \"%s\"" % (kit.name, kit.name))
        return 2
    r = json.loads(res.read_text(encoding="utf-8"))
    stored = r.get("faces_hash")
    if stored is None and "faces_mtime" in r:
        stored = None                      # a pre-hash result: re-read rather than guess
    if stored != _faces_hash(kit):
        print("ERROR  the blind read is STALE - the faces changed after it ran.\n"
              "       Re-run: python blind_reader.py --prepare \"%s\"" % kit.name)
        return 2
    print("  %-9s blind read current, control floor %d/3, %d candidate(s)"
          % (r["verdict"], r["floor"], len(r["candidates"])))
    return 0 if r["verdict"] == "PASS" else (1 if r["verdict"] == "FINDINGS" else 2)


# ------------------------------------------------------------------- selftest

def selftest():
    ok = True
    print("\n  CONTROLS - can the ruler be checked at all?\n")
    kits = [p.parent for p in sorted(ROOT.glob("*/ads")) if p.is_dir()]
    probe = kits[0] if kits else ROOT
    ctrl, note = controls(probe)
    if note:
        print("    note: %s" % note)
    for c in ctrl:
        print("    %-34s %-20s %s" % (c["ad"], c["why"],
                                      pathlib.Path(c["src"]).parent.parent.name[:28]))
    enough = len(ctrl) >= 2
    priced = sum(1 for c in ctrl if "lead" in c["why"])
    print("      %s  at least 2 controls resolve" % ("ok  " if enough else "FAIL"))
    print("      %s  at least 1 carries a live cost, not just a label"
          % ("ok  " if priced else "warn"))
    ok = ok and enough

    print("\n  BLINDING - does anything in a packet give the answer away?\n")
    body = READER_PROMPT.format(img=r"C:\...\.blind\F07.png", fid="F07",
                                questions=QUESTIONS)
    leaks = [w for w in ("candidate", "control", "under test", "approved",
                         "SkillArbitrage", "LawSikho")
             if w.lower() in body.lower()]
    print("      %s  no candidate/control marker in the packet body%s"
          % ("ok  " if not leaks else "FAIL",
             "" if not leaks else "  (found: %s)" % ", ".join(leaks)))
    print("      ok    faces are copied to F01.png.. so the source path is not sent")
    ok = ok and not leaks

    print("\n  SCORING - does the relative verdict behave?\n")
    cases = [
        ("a candidate below the control floor is blocked", [3, 3], [1], True),
        ("a candidate level with the floor passes", [3, 2], [2], False),
        ("controls at 0 mean the ruler broke, block nothing", [0, 0], [0], None),
    ]
    for label, cs, ds, expect_block in cases:
        floor = min(cs)
        got = None if floor == 0 else any(d < floor for d in ds)
        good = got == expect_block
        print("      %s  %s" % ("ok  " if good else "FAIL", label))
        ok = ok and good

    print("\n  ANSWER PARSING - do the reader's replies survive?\n")
    sample = "F03\n1: A company secretary\n2: CANNOT ANSWER\n3: value a company\n"
    p = parse_answers(sample)
    good = p.get("F03", {}).get(1, "").startswith("A company") \
        and not _clear(p["F03"][2]) and _clear(p["F03"][3])
    print("      %s  a well-formed reply scores 2/3" % ("ok  " if good else "FAIL"))
    ok = ok and good

    print("\n  %s\n" % ("every check passed" if ok
                        else "SELFTEST FAILED - fix before using"))
    return 0 if ok else 1


WHY = """
WHERE EACH RULE CAME FROM
=========================

the test is run by a subagent, not by this session
    AD_CREATION_DIRECTOR.md 12.5, verbatim: "You cannot run this test on your own
    writing ... that's not carelessness, it's contamination, and it's why cryptic
    ads survive to Ramanuj even from a session that had every rule in this file in
    front of it." The instruction sat in 30 files and in zero scripts (grepped
    15 Sep 2026).

the reader is handed the rendered PNG, not extracted text
    Two reasons. A person sees the face, not a text dump, and the memory note
    `blind_reader_needs_the_whole_face` is about exactly that loss. And the corpus
    is mostly PNG: on 15 Sep 2026 only ONE of the nine priced-or-approved winners
    still had an html/ source in this repo (APPROVED/ ships PNGs and landing
    pages, no faces), so a text-only test could not assemble a control set at all.
    148 approved faces have PNGs.

controls go in BEFORE the read, not after a bad one
    Director Step 9: "IF A BLIND READ COMES BACK BAD, RUN THE SAME TEST ON THE
    PRICED WINNERS BEFORE ACTING ON IT. That control costs one subagent and it is
    the difference between a real defect and a broken ruler." Measured 3 Sep 2026:
    on call-out + head only, the four Patent faces carrying a live cost scored 0 of
    4 CLEAR, three of them VAGUE, including icp_28_biomedical_devices at Rs 91.36,
    the cheapest patent ad in the account. Four rebuild passes went into it.
    A control you remember only after bad news is not a control.

the verdict is relative, never absolute
    Same measurement. Any fixed threshold that fails every priced winner is a
    broken ruler. A candidate is blocked only when it reads worse than a face that
    was approved or that the Meta pull priced at or under Rs%.0f/lead.

priced controls outrank approved ones
    `feedback_only_ramanuj_approval_counts` and adkit/golden.py: the priced tables
    are "the only combination that settles an argument". An in-house APPROVED
    label admits nothing here, per the 31 Aug correction - "ignore the ones that i
    approved, they were finally not approved".

the read goes stale when a face is re-rendered
    --score records the newest face mtime; --status fails if a face moved after
    it. Rebuilding a face after its read is the ordinary way of working, not a
    dodge, so the gate has to notice it rather than trust a green tick from
    yesterday.

three states, not two
    check_all.py's contract. ERROR covers no controls, a collapsed control band and
    a partial set of answers, because "nothing to report" from a test that did not
    run is the 25 Aug failure this repo already paid for once.

WHAT THIS CANNOT DO
===================
It measures COMPREHENSION and never desire. Director 12.5 records a face that
passed the blind read on all five questions and was still wrong, because the
biggest line sold the buying decision rather than a job - "this one is a human read
of the biggest line, every time". A clean run here is not permission to ship.

It is not fitted against live cost. No face has been priced on the back of a
blind-read score, so this decides what to REBUILD, never what will convert.

The reader has file access in order to open the image. The path is opaque and the
prompt forbids looking around, but that is an instruction, not a sandbox.
""" % CONTROL_CPL_CEILING


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--prepare", metavar="KIT")
    ap.add_argument("--score", metavar="KIT")
    ap.add_argument("--status", metavar="KIT")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--why", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv[1:])
    if a.why:
        print(WHY)
        return 0
    if a.selftest:
        return selftest()
    if a.prepare:
        return prepare(a.prepare, a.seed)
    if a.score:
        return score(a.score)
    if a.status:
        return status(a.status)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
