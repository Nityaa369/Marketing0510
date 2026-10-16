"""Blind-read the LANDING PAGE's closing fold, the last thing a reader sees before paying.

WHY THIS EXISTS
---------------
Every clarity gate in this repo points at the ad face. `simplicity.py`'s
dangling-reference rule and `blind_reader.py` both take the AD's first fold as
their unit, and nothing examines the landing page's closing section at all.

Measured 21 Sep 2026 on CorporateFinance_Notify_17-19Oct, a kit that had just
passed all ten gates of `check_all.py` clean: all 19 pages carried a `close_head`
written as the same riddle - two clauses, an implied contrast, the referent
withheld - sitting directly above the pay button.

    "The biggest thing your client owns has never been on a statement you sent
     them."
    "The arithmetic you have. The half where nothing is published is the half
     that is missing."        <- no verb in the first fragment
    "The finance half of the degree has never been handed a live company."
    "The second half of that conversation is already happening at your desk."
                              <- "that conversation" has no antecedent on the page

Ramanuj's reading: "none of them make any sense". That is Rule 2 - cryptic, by
the repo's own definition - in the single highest-value slot on the page, and no
gate could see it because no gate was looking there.

THE UNIT
--------
The closing fold is the LAST call-to-action on the page, plus the heading and
body text immediately above it. Defined by position, not by class: 269 of 534
landing pages in this folder use `<div class="close">` and 265 do not, so a
class-name rule would have been blind to half the corpus - the same defect as
ad_lint C8 matching class names while the generator emitted inline styles
(`feedback_c8_reads_first_css_rule`).

THE VERDICT IS RELATIVE
-----------------------
Three closing folds that demonstrably worked are shuffled in as blinded controls,
exactly as `blind_reader.py` does, and a candidate fails only when it reads worse
than one of them. A fixed bar would be wrong here for the same reason it was
wrong there: on the first real ad run `us05_evening`, the second-cheapest ad in
the account, scored 2/3, and a "three clean answers or it is cryptic" rule would
have condemned it.

A control is the closing fold of the landing page paired with a face that
PRICED CHEAP or that Ramanuj approved. An in-house APPROVED label is not
evidence (`feedback_only_ramanuj_approval_counts`).

WHAT IT CANNOT DO
-----------------
Comprehension only. It says nothing about whether anybody wants the offer, and a
page can read perfectly and still not sell. It is also a ONE-CLASS fit like
`simplicity.py`: it can show that a line does not read worse than one that
worked, and cannot show what it catches.

    python closing_reader.py --prepare <kit>     write the blinded packets
    python closing_reader.py --score <kit>       unblind, score against controls
    python closing_reader.py --status <kit>      did a read run for these pages?
    python closing_reader.py --why               the evidence behind each rule
    python closing_reader.py --selftest          re-score the rules
"""
import argparse
import hashlib
import html
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).parent.resolve()

N_CONTROLS = 3
OUTDIR = ".closing"

# The closing fold is the last CTA plus what sits above it. An anchor counts as a
# CTA if it says so in its class or reads like one. Kept deliberately wide: a
# missed CTA means the wrong fold is read, which is worse than a false positive
# (the LAST match wins, so an extra early match is harmless).
CTA_WORDS = r"join|enrol|enroll|register|reserve|book|pay|claim|start|seat|get\s+(?:my|the|started)"
# Not just <a>: 146 of the first 400 pages carry no anchor at all and put the CTA
# in a <button>. A rule that only read anchors reported those pages unreadable.
CLICKABLE = re.compile(r"<(a|button)\b([^>]*)>(.*?)</\1>", re.S | re.I)
HEADING = re.compile(r"<h[1-3]\b[^>]*>(.*?)</h[1-3]>", re.S | re.I)
TAG = re.compile(r"<[^>]*>")
SCRIPTY = re.compile(r"<(script|style|svg)\b.*?</\1>", re.S | re.I)

# Chrome that is not the closing argument and must come out before the fold is
# located. Two kinds, both found by running the gate and reading what it returned:
#
#   sticky bars   The sticky CTA is part of the LP standard (SOP/05), so the LAST
#                 CTA on the page is usually the sticky one, whose "heading above
#                 it" is the brand strip. 250 pages class it `sticky`, plus
#                 stickytop / sticky-cta / topbar / seatbar.
#   modals        118 containers class or id `modal`. A registration modal is
#                 hidden until the reader clicks, so it is not what anyone sees
#                 before deciding. Caught on the first real run: all three
#                 CONTROLS came back as a form block ("Full name Email Mobile
#                 +91") instead of a closing argument, which would have set the
#                 floor from a form rather than from copy that worked.
#
# Forms go too, for the same reason: field labels are not an argument.
CHROME_WORD = re.compile(
    r"\b(sticky\S*|topbar\S*|seatbar|bottombar|modal\S*|dialog\S*|overlay|popup)\b",
    re.I)
CONTAINER = re.compile(r"<(div|section|footer|nav|aside|dialog)\b([^>]*)>", re.I)
ANY_TAG = re.compile(r"<(/?)(div|section|footer|nav|aside|dialog)\b[^>]*>", re.I)
FORM = re.compile(r"<form\b.*?</form>", re.S | re.I)


def _strip_chrome(raw):
    """Remove sticky bars, modals and forms, balanced, before locating the fold."""
    raw = FORM.sub(" ", raw)
    while True:
        hit = None
        for m in CONTAINER.finditer(raw):
            attrs = m.group(2) or ""
            marker = re.search(r'(?:class|id)="([^"]*)"', attrs, re.I)
            if marker and CHROME_WORD.search(marker.group(1)):
                hit = m
                break
        if not hit:
            return raw
        depth, end = 0, len(raw)
        for t in ANY_TAG.finditer(raw, hit.start()):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = t.end()
                break
        raw = raw[:hit.start()] + " " + raw[end:]

def plain(markup):
    """Visible text of an HTML fragment, entities resolved, whitespace collapsed.

    html.unescape, not a hand-written table: the first cut listed a dozen entities
    and still shipped raw `&middot;` and `&rarr;` into the reader's packet, which
    is noise the reader then has to decode on top of the copy."""
    s = TAG.sub(" ", markup)
    s = html.unescape(s)
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


QUESTIONS = """1. Who is this addressed to?
2. What is being offered, and what does it cost?
3. Say the opening line again in your own words."""

READER_PROMPT = """Below is the closing section of a web page - the last thing a
reader sees before deciding whether to pay. You have NO other context: you have
not seen the rest of the page, the advertisement that led here, or anything about
the company. Do not guess at a product, course or brief beyond what is written
below. If the text does not tell you, the answer is CANNOT ANSWER - that is a
useful answer here, not a failure.

Question 3 is the important one. Restate the opening line in ordinary words, as
you would explain it to somebody else. If it does not mean anything definite to
you, say CANNOT ANSWER rather than guessing at what it might be gesturing at.

--- begin ---
{fold}
--- end ---

Answer all three questions in one line each. Reply in exactly this format and add
nothing else - no preamble, no summary, no advice about the writing:

{cid}
1: <your answer, or CANNOT ANSWER>
2: <your answer, or CANNOT ANSWER>
3: <your answer, or CANNOT ANSWER>

The questions:

{questions}"""


# ------------------------------------------------------------------ the fold

def closing_fold(path):
    """(head, body, cta) for one landing page, or None if there is no CTA.

    Position, not class: find the last CTA-looking anchor, then the last heading
    that starts before it. Everything between them is the body.
    """
    try:
        raw = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    raw = _strip_chrome(SCRIPTY.sub(" ", raw))

    ctas = []
    for m in CLICKABLE.finditer(raw):
        attrs, inner = m.group(2) or "", plain(m.group(3))
        looks = ("cta" in attrs.lower()
                 or re.search(CTA_WORDS, inner, re.I))
        if looks and inner:
            ctas.append(m)
    if not ctas:
        return None

    # The last CTA that actually has a heading above it. Walking backwards rather
    # than taking ctas[-1] outright means a trailing footer link cannot swallow
    # the fold.
    for cta in reversed(ctas):
        heads = [m for m in HEADING.finditer(raw) if m.start() < cta.start()]
        if not heads:
            continue
        head = heads[-1]
        return dict(head=plain(head.group(1)),
                    body=plain(raw[head.end():cta.start()]),
                    cta=plain(cta.group(3)))
    return None


def fold_text(fold):
    """The packet body, exactly as a reader sees it."""
    parts = [fold["head"]]
    if fold["body"]:
        parts.append(fold["body"])
    parts.append("[ button ] " + fold["cta"])
    return "\n\n".join(parts)


def _pages(kit):
    lp = pathlib.Path(kit) / "landing_pages"
    if not lp.is_dir():
        return []
    return [p for p in sorted(lp.glob("*.html"))
            if not p.name.startswith(("index", "_"))]


def _folds_hash(kit):
    """Content hash of every candidate CLOSING FOLD.

    Hashes the fold, not the file: a page rebuilt with an unrelated FAQ edit has
    not changed what this gate read, and a gate that cries stale on an unchanged
    fold teaches people to ignore it (`blind_reader._faces_hash`, 15 Sep)."""
    h = hashlib.sha256()
    for p in _pages(kit):
        fold = closing_fold(p)
        if not fold:
            continue
        h.update(p.name.encode("utf-8"))
        h.update(fold_text(fold).encode("utf-8"))
    return h.hexdigest()


# -------------------------------------------------------------------- controls

def _lp_for_face(png):
    """The landing page paired with an ad face. Rule 4: lp_ + the ad's exact stem."""
    png = pathlib.Path(png)
    lp_dir = png.parent.parent / "landing_pages"
    if not lp_dir.is_dir():
        return None
    exact = lp_dir / ("lp_%s.html" % png.stem)
    if exact.is_file():
        return exact
    # Ship folders renumber the stem (08_loan_consultant for 01_loan_consultant),
    # so fall back to the descriptive half of the name.
    tail = png.stem.split("_", 1)[-1]
    for cand in sorted(lp_dir.glob("lp_*.html")):
        if cand.stem.endswith(tail):
            return cand
    return None


def controls(exclude_kit, n=N_CONTROLS):
    """Closing folds of pages whose FACE priced cheap or was approved, priced first.

    Reuses blind_reader.controls so there is exactly one definition of "worked" in
    the repo, including its 17 Sep fix for namesake faces inheriting a price they
    never earned."""
    sys.path.insert(0, str(ROOT))
    try:
        import blind_reader
    except Exception as exc:                                    # noqa: BLE001
        return [], "could not import blind_reader: %s" % exc

    # Ask for a wide pool: most faces will not have a usable paired page.
    pool, err = blind_reader.controls(exclude_kit, n=200)
    if err:
        return [], err

    out, seen = [], set()
    for row in pool:
        lp = _lp_for_face(row["src"])
        if not lp or lp in seen:
            continue
        fold = closing_fold(lp)
        if not fold or not fold["head"]:
            continue
        seen.add(lp)
        out.append(dict(src=str(lp), ad=row["ad"], why=row["why"]))
        if len(out) >= n:
            break
    if not out:
        return [], "no control page had a readable closing fold"
    return out, ""


# --------------------------------------------------------------------- prepare

def prepare(kit, seed=None):
    kit = pathlib.Path(kit).resolve()
    pages = _pages(kit)
    if not pages:
        print("ERROR  no landing_pages/*.html in %s" % kit)
        return 2

    items = []
    for p in pages:
        fold = closing_fold(p)
        if not fold or not fold["head"]:
            print("ERROR  %s has no readable closing fold (no CTA, or no heading\n"
                  "       above it). The gate cannot read what it cannot find."
                  % p.name)
            return 2
        items.append(dict(kind="candidate", ad=p.stem, src=str(p),
                          why="under test", fold=fold))

    ctrl, err = controls(kit)
    if err:
        print("ERROR  %s" % err)
        return 2
    for c in ctrl:
        c["kind"] = "control"
        c["fold"] = closing_fold(c["src"])
        items.append(c)

    rng = random.Random(seed if seed is not None else 0xC105)
    rng.shuffle(items)

    out = kit / OUTDIR
    out.mkdir(exist_ok=True)
    for stale in list(out.glob("packet_C*.txt")):
        stale.unlink()

    key = []
    for i, it in enumerate(items, start=1):
        cid = "C%02d" % i
        body = READER_PROMPT.format(fold=fold_text(it["fold"]), cid=cid,
                                    questions=QUESTIONS)
        (out / ("packet_%s.txt" % cid)).write_text(body, encoding="utf-8")
        key.append(dict(cid=cid, kind=it["kind"], ad=it["ad"],
                        src=it["src"], why=it["why"]))
    (out / "key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")

    print("\n  kit: %s" % kit.name)
    print("  %d packet(s) in %s" % (len(key), out))
    print("  %d candidate(s) + %d control(s), shuffled behind opaque ids.\n"
          % (len(items) - len(ctrl), len(ctrl)))
    print("  the controls in this run (the reader is NOT told which these are):")
    for c in ctrl:
        print("    %-34s %s" % (c["ad"], c["why"]))
    print("""
  NOW, one subagent per packet:
    read packet_C*.txt and pass its body as the ENTIRE prompt of a fresh subagent.
    No kit path, no brief, no ICP list, nothing about this account. Launch them in
    ONE message so they run at once and cannot see each other's answers.

  Paste every reply verbatim into:
    %s

  Then:
    python closing_reader.py --score "%s"
""" % (out / "answers.txt", kit.name))
    return 0


# ----------------------------------------------------------------------- score

CID = re.compile(r"^\s*\**\s*(C\d{2})\s*\**\s*$")


def parse_answers(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = CID.match(line)
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
                or a.startswith("i cannot")
                or a.startswith("unclear")
                or a in ("n/a", "-", "unknown", "not stated"))


def score(kit):
    kit = pathlib.Path(kit).resolve()
    out = kit / OUTDIR
    keyf, ansf = out / "key.json", out / "answers.txt"
    if not keyf.exists():
        print("ERROR  no %s - run --prepare first." % keyf)
        return 2
    key = json.loads(keyf.read_text(encoding="utf-8"))
    answers = parse_answers(ansf.read_text(encoding="utf-8")
                            if ansf.exists() else "")

    missing = [k["cid"] for k in key if k["cid"] not in answers]
    if missing:
        print("ERROR  no answer for %d of %d fold(s): %s\n"
              "       A partial read is not a pass.\n"
              "       Spawn the missing subagents, paste their replies into\n"
              "       %s" % (len(missing), len(key), " ".join(missing), ansf))
        return 2

    for k in key:
        a = answers[k["cid"]]
        k["answers"] = dict((str(q), a.get(q, "")) for q in (1, 2, 3))
        k["score"] = sum(1 for q in (1, 2, 3) if _clear(a.get(q, "")))

    ctrl = [k for k in key if k["kind"] == "control"]
    cand = [k for k in key if k["kind"] == "candidate"]
    floor = min(k["score"] for k in ctrl)

    width = max(len(k["ad"]) for k in key)
    print("\n  kit: %s\n" % kit.name)
    print("  %-4s %-*s %-10s %-6s %s"
          % ("id", width, "closing fold", "kind", "clear", "what it is"))
    print("  " + "-" * (width + 44))
    for k in sorted(key, key=lambda r: (r["kind"], -r["score"])):
        print("  %-4s %-*s %-10s %d/3    %s"
              % (k["cid"], width, k["ad"], k["kind"], k["score"], k["why"]))

    print("\n  control floor: %d/3   (the worst score among closing folds whose "
          "face was approved or ran cheap)" % floor)

    verdict, rc = "PASS", 0
    if floor == 0:
        verdict, rc = "ERROR", 2
        print("""
  ERROR  a closing fold that WORKED scored 0/3. The instrument failed, not the
         pages. Blocking nothing. Read .closing/packet_*.txt and check what the
         reader was actually sent before reading anything into the scores above.""")
    else:
        bad = [k for k in cand if k["score"] < floor]
        if bad:
            verdict, rc = "FINDINGS", 1
            print("\n  FINDINGS  %d closing fold(s) read less clearly than one that "
                  "worked:\n" % len(bad))
            for k in bad:
                print("    %s  (%d/3, floor %d)" % (k["ad"], k["score"], floor))
                for q in ("1", "2", "3"):
                    a = k["answers"][q]
                    print("      %s %s. %s" % ("  " if _clear(a) else "XX", q,
                                               a or "(no answer)"))
            print("\n  Question 3 is the one that matters. A reader who cannot restate")
            print("  the opening line has been handed a riddle in the last slot before")
            print("  the pay button. The fix is almost always to say the thing plainly:")
            print("  name the work the reader already does, then what this adds.")
        else:
            print("\n  PASS  every closing fold read at least as clearly as one whose")
            print("        face was approved or ran cheap. Comprehension only - this")
            print("        says nothing about whether anybody wants the offer.")

    (out / "result.json").write_text(json.dumps(dict(
        verdict=verdict, floor=floor, folds_hash=_folds_hash(kit),
        candidates=[dict(ad=k["ad"], score=k["score"]) for k in cand],
        controls=[dict(ad=k["ad"], score=k["score"], why=k["why"]) for k in ctrl],
    ), indent=2), encoding="utf-8")
    return rc


# ---------------------------------------------------------------------- status

def status(kit):
    """Did a closing read actually run for the pages as they stand right now?"""
    kit = pathlib.Path(kit).resolve()
    res = kit / OUTDIR / "result.json"
    if not _pages(kit):
        print("SKIP   %s has no landing pages." % kit.name)
        return 0
    if not res.exists():
        print("ERROR  no closing read has been run for %s.\n"
              "       Re-run: python closing_reader.py --prepare \"%s\""
              % (kit.name, kit.name))
        return 2
    saved = json.loads(res.read_text(encoding="utf-8"))
    if saved.get("folds_hash") != _folds_hash(kit):
        print("ERROR  the closing read is STALE - the closing folds changed after "
              "it ran.\n       Re-run: python closing_reader.py --prepare \"%s\""
              % kit.name)
        return 2
    v = saved.get("verdict")
    if v == "PASS":
        print("PASS   %d closing fold(s) read at or above the control floor of %d/3."
              % (len(saved.get("candidates", [])), saved.get("floor", 0)))
        return 0
    print("%-6s closing read recorded verdict %s - see %s" % (v, v, res))
    return 1 if v == "FINDINGS" else 2


# -------------------------------------------------------------------- selftest

def selftest():
    """Can the fold finder actually find the fold, on both halves of the corpus?"""
    ok = True

    # 1. The fold finder, on a page with div.close and one without.
    found = missing = 0
    for p in sorted(ROOT.glob("*/landing_pages/*.html"))[:400]:
        fold = closing_fold(p)
        if fold and fold["head"] and fold["cta"]:
            found += 1
        else:
            missing += 1
    total = found + missing
    rate = 100.0 * found / total if total else 0.0
    good = rate >= 90.0
    ok = ok and good
    print("    %s the fold finder reads %d of %d page(s), %.0f%%"
          % ("ok   " if good else "FAIL ", found, total, rate))

    # 2. It must not be a class-name rule. 269 of 534 pages use div.close and 265
    #    do not; both halves have to be readable or the gate is blind to half the
    #    corpus, which is the ad_lint C8 failure.
    with_cls = without = 0
    for p in sorted(ROOT.glob("*/landing_pages/*.html"))[:400]:
        raw = p.read_text(encoding="utf-8", errors="replace")
        fold = closing_fold(p)
        if not (fold and fold["head"]):
            continue
        if re.search(r'<div class="close"', raw):
            with_cls += 1
        else:
            without += 1
    both = with_cls > 0 and without > 0
    ok = ok and both
    print("    %s reads both markup shapes: %d with div.close, %d without"
          % ("ok   " if both else "FAIL ", with_cls, without))

    # 3. _clear must reject the refusals a reader actually writes.
    refusals = ["CANNOT ANSWER", "cannot answer - it does not say",
                "I cannot tell", "unclear", "n/a"]
    accepts = ["Wealth managers and MF distributors",
               "Three live evenings for Rs 10"]
    bad = ([r for r in refusals if _clear(r)]
           + [a for a in accepts if not _clear(a)])
    ok = ok and not bad
    print("    %s _clear separates refusals from real answers%s"
          % ("ok   " if not bad else "FAIL ", "" if not bad else ": %s" % bad[:2]))

    # 4. The riddles that started this. None is a pass on its own - the verdict is
    #    relative - but the finder must at least surface them as the head.
    riddles = ["The biggest thing your client owns has never been on a statement",
               "The arithmetic you have"]
    print("    the 21 Sep riddles are the evidence, not a threshold: the verdict")
    print("    is always relative to a control that worked. %d recorded." % len(riddles))

    print("\n    One-class fit, like simplicity.py: it can show a line does not read")
    print("    worse than one that worked. It cannot show what it catches.")
    return 0 if ok else 1


WHY = """
closing_reader.py - the evidence behind each rule

  THE UNIT IS THE LAST CTA, NOT A CLASS NAME
    269 of 534 landing pages in this folder wrap the closing section in
    <div class="close">; 265 do not. A class-name rule would read half the
    corpus and report the other half clean, which is exactly how ad_lint C8
    shipped 7 of 10 Independent Director faces under its own size floor
    (feedback_c8_reads_first_css_rule). So the fold is defined by position:
    the last call-to-action on the page, and the heading above it.

  THE VERDICT IS RELATIVE
    Three closing folds whose FACE priced cheap or was approved are shuffled in
    blinded. A candidate fails only below the worst control. A fixed bar was
    tried on the ad reader and was wrong: us05_evening, at Rs 31/lead the
    second-cheapest ad in the account, scored 2/3 (feedback_blind_reader_...).

  QUESTION 3 IS THE INSTRUMENT
    "Say the opening line again in your own words." The 21 Sep defect was not
    missing information, it was withheld reference: "that conversation" and
    "the file" with no antecedent, and one heading with no verb at all. A
    reader who cannot restate the line has been handed a riddle in the last
    slot before the pay button.

  WHY NOT A REGEX
    "This line is a riddle" is not mechanically testable. A rule that banned
    two-clause headings would have blocked "Thirty years of credit judgement
    does not expire. The vocabulary of a deal takes three evenings.", which is
    two clauses and perfectly clear. The judgement needs a reader with no
    context, which is what this is.

  WHAT IT CANNOT DO
    Comprehension only. A page can read perfectly and sell nothing. One-class
    fit: it can show a line does not read worse than one that worked, and
    cannot show what it catches.
"""


def main(argv):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__)
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
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
