#!/usr/bin/env python3
"""
creative_review.py - the judgment layer preflight.py explicitly cannot run.

preflight.py catches mechanical failures (dead links, hedges above the CTA,
banned patterns). It says outright: "It cannot judge whether an ad offers a
better career (Rule 1) or whether it assumes knowledge (Rule 2)." This is
that check, built from verified evidence in RAMANUJ_FEEDBACK.md rather than
from the abstract rule statement alone - the DPDP 9-ad batch (5 approved,
4 rejected, one exception left unresolved) and the 3-draft "cryptic" fix.

This is v0. It knows what one verified batch and one verified edit sequence
showed. Confidence levels below are honest about that - nothing here is
claimed as settled beyond what RAMANUJ_FEEDBACK.md actually verified. Once
RAMANUJ_QUESTIONNAIRE.md comes back with a fuller pass over the real source
folder, the patterns below should be replaced wholesale, not patched.

Usage:
    python creative_review.py <html-file-or-folder> [...]

This does not return a pass/fail exit code the way preflight.py does -
every finding here is a flag for a human to weigh, not a blocker. The one
confirmed exception in the source evidence (an ad that should have been
rejected by this exact logic and wasn't) is the reason: fast human judgment
does not always follow the reconstructed rule, so this tool should not
pretend to replace it.
"""

import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- Rule 1
# Current-job-obligation framing: "your X is now/needs Y" - the shape shared
# by 3 of 4 rejected ads in the DPDP batch (collections_recovery,
# finance_payroll, vendor_onboarding). See RAMANUJ_FEEDBACK.md Part 3.3.
OBLIGATION_FRAME = re.compile(
    r"\byour\s+\w+(?:\s+\w+){0,3}\s+(?:is now|now needs|now requires|now counts as|"
    r"has to be|needs a)\b", re.I,
)

# Career-pivot framing: names a specific senior role, or an explicit exit
# from the current track. Shared by all 5 approved ads in the same batch.
PIVOT_FRAME = re.compile(
    r"\bbecome (?:the|a)\b|\bmove into\b.{0,20}\binstead\b|\bstart a\b.{0,20}\bcareer\b|"
    r"\bnew career\b|\bswitch to\b", re.I,
)

# The specific offer-line construction that was an elevated-risk signal, not
# a deterministic one: 3 of 4 ads carrying it were rejected, 1 was approved
# with no distinguishing wording found. Flag as a warning, never a blocker.
NAMED_CREDIT_LINE = re.compile(
    r"named the person who (?:fixed|built|added|created|wrote)", re.I,
)

# Direct regulator/threat language - the mechanism CLAUDE.md Rule 1 names
# outright ("threaten with a regulator"), independent of the obligation-frame
# pattern above.
REGULATOR_THREAT = re.compile(
    r"\bbanned outright\b|\bregulator\b.{0,15}\b(?:watch|expos)|"
    r"\bliabilit(?:y|ies)\b|\bexposed\b|\bnow (?:prohibited|illegal)\b", re.I,
)

# ---------------------------------------------------------------- Rule 2
# A line that names who the ad is for, using a role/title/situation word,
# within the first ~120 characters. Heuristic only - cannot see layout order
# the way a human reviewing the rendered page can.
AUDIENCE_ID = re.compile(
    r"\b(?:manager|officer|professional|engineer|lawyer|advocate|consultant|"
    r"analyst|coordinator|accountant|secretary|owner|founder|student|graduate|"
    r"you (?:handle|hold|run|already))\b", re.I,
)

# A sentence that defines the field in plain words - "X is Y, Z and W" shape.
# CLAUDE.md Rule 2 step 4. Heuristic, not a guarantee of quality.
FIELD_DEFINITION = re.compile(
    r"\b\w+(?: \w+){0,3}\s+is\s+\w+(?:,\s*\w+(?: \w+)?)+(?:,?\s+and\s+\w+(?: \w+)?)\b", re.I,
)

QUALIFIER_ROW = re.compile(r"[·|]\s*\S+\s*[·|]\s*\S+")


def visible_text(html: str) -> str:
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<[^>]+>", "\n", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"[ \t]+", " ", html).strip()


def first_fold(text: str, chars: int = 400) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return " ".join(lines)[:chars]


def review_page(path: Path):
    flags = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [("ERROR", f"could not read file: {e}", "n/a")]

    text = visible_text(raw)
    fold = first_fold(text)

    # --- Rule 1: framing ---
    obligation_hits = OBLIGATION_FRAME.findall(fold)
    pivot_hits = PIVOT_FRAME.findall(text[:600])
    threat_hits = REGULATOR_THREAT.findall(text[:800])

    if obligation_hits and not pivot_hits:
        flags.append((
            "WARN",
            f'current-job-obligation framing with no career-pivot language found '
            f'("{fold[:90]}..."). 3 of 4 ads with this shape were rejected in the '
            f'verified DPDP batch.',
            "high",
        ))
    if threat_hits and not pivot_hits:
        flags.append((
            "WARN",
            f"regulator/threat language present with no pivot framing to balance it "
            f'({threat_hits[:3]}). This is the exact "threaten with a regulator" '
            f"pattern CLAUDE.md Rule 1 names.",
            "high",
        ))

    credit_hits = NAMED_CREDIT_LINE.findall(text)
    if credit_hits:
        flags.append((
            "INFO",
            f'"named the person who [fixed/built/added] it" offer-line construction '
            f"found. Elevated risk (3/4 rejected in verified sample) but NOT a "
            f"deterministic fail - one exception was approved with no explanation "
            f"found. Confirm the headline above it uses pivot framing.",
            "low",
        ))

    # --- Rule 2: cryptic ---
    aud_pos = None
    m = AUDIENCE_ID.search(fold)
    if m:
        aud_pos = m.start()
    if aud_pos is None:
        flags.append((
            "WARN",
            "no audience-identifying word found in the first ~400 characters. "
            "Cannot confirm the reader knows who this is for before the hook lands.",
            "medium",
        ))
    elif aud_pos > 120:
        flags.append((
            "INFO",
            f"audience identification appears at character {aud_pos} of the first "
            f"fold - if a hook or metaphor sits before it, that's the exact "
            f'"who are you talking to and why" failure from the verified 3-draft '
            f"sequence. Confirm by reading the rendered page, not just this text.",
            "medium",
        ))

    if not QUALIFIER_ROW.search(text[:800]):
        flags.append((
            "INFO",
            "no qualifier row detected (e.g. 'ROLE · AGE/YEARS · SCOPE'). If one "
            "exists, confirm it lists every field/title that should self-select in, "
            "not just 2-3 examples - narrow qualifier rows were the second half of "
            "the verified 'cryptic' fix.",
            "medium",
        ))

    if not FIELD_DEFINITION.search(text):
        flags.append((
            "INFO",
            "no plain-words field-definition sentence detected (CLAUDE.md Rule 2 "
            "step 4, 'X is Y, Z and W'). Heuristic only - check by hand.",
            "low",
        ))

    return flags


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    targets = []
    for arg in argv[1:]:
        p = Path(arg)
        if p.is_dir():
            targets += list(p.rglob("*.html"))
        elif p.suffix.lower() == ".html":
            targets.append(p)

    if not targets:
        print("No HTML files found.")
        return 1

    print("creative_review.py - judgment-layer flags, v0 (built from a 9-ad verified sample)")
    print("Every flag here is something to weigh, not a blocker. Confidence is per-flag.\n")

    total = 0
    for path in sorted(set(targets)):
        flags = review_page(path)
        if not flags:
            continue
        try:
            label = path.relative_to(Path.cwd())
        except ValueError:
            label = path
        print(f"\n{label}")
        for level, msg, conf in flags:
            print(f"  {level:5} [{conf:6} confidence]  {msg}")
            total += 1

    print("\n" + "-" * 64)
    print(f"{len(set(targets))} pages checked, {total} flags raised.")
    print("\nThis script only knows what one verified 9-ad batch and one verified")
    print("3-draft edit sequence showed. It will under-flag anything that batch")
    print("didn't happen to cover, and it CANNOT catch the one confirmed exception")
    print("in that same batch (a rejected-pattern ad that was actually approved).")
    print("Treat every flag as a prompt to think, not a verdict.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
