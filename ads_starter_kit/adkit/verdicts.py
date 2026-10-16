#!/usr/bin/env python3
"""The labelled negative set: which ads were rejected, and in whose words.

Why this exists. `corpus.py` shipped 31 Aug 2026 knowing only what was APPROVED,
by folder membership. But CAMPAIGN_MAP.md carries the rejections too, **with the
reason quoted**, and that is the more useful half -- an approved ad tells you one
thing that worked, a rejected ad with "you need to offer a different career to
this person, not threaten with a regulator" attached tells you the rule and the
exact sentence that broke it.

Three shapes are written in that file, and all three are read here:

  1. Verdict tables
     | `lp_01_collections_recovery` | Collections | REJECTED | "you need to..." |

  2. Numbered wave verdicts
     **Section A verdicts.** APPROVED: pairs 01, 02, 03, ...
     NOT APPROVED: 06, 13, 16, 17, 18, 19, 24.

  3. Prose
     Also rejected as cryptic, in `DataPrivacy_MediaBuyer_22-24Aug/`:
     `lp_05_global_freelance` (...) and `lp_04_second_innings` (...).

CONSERVATIVE ON PURPOSE, for the same reason the money join is: a verdict
attached to the wrong ad is worse than no verdict. Shape 2 has to guess which kit
a bare `06` belongs to, from the nearest folder named in the same section. When
that guess fails, the ad gets NO verdict rather than someone else's.

    python -m adkit.verdicts            everything parsed, grouped
    python -m adkit.verdicts --rejected only the rejections and their reasons
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = ROOT / "CAMPAIGN_MAP.md"

APPROVED, REJECTED = "APPROVED", "REJECTED"

# a name that could plausibly be an ad or a page, not a folder, script or doc
NAMEISH = re.compile(r"^(?!.*\.(py|md|zip|json)$)(?!.*/$)[A-Za-z0-9][A-Za-z0-9_.\-]{3,}$")


def _clean(tok):
    return tok.strip().strip("`*_ ").rstrip("/")


def _is_name(tok, raw=None):
    """`raw` is the token as written. A trailing slash means it is a FOLDER, and
    the check has to happen before _clean strips it -- otherwise
    `DataPrivacy_MediaBuyer_22-24Aug/` reads as an ad name and collects the
    rejection meant for the two pages inside it."""
    if raw is not None and raw.strip().endswith("/"):
        return False
    return bool(NAMEISH.match(tok)) and ("_" in tok or re.search(r"\d", tok))


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _overlap(folder, sentence):
    """Longest run of the normalised folder name that appears in the normalised
    sentence. Word-set overlap was not enough: "Section A verdicts" shares no
    WORD with `ContentWriting_SectionA_29-31Aug`, because the folder spells it
    `SectionA`. Scoring on substrings picked the right kit; scoring on words
    picked `content-writing-bootcamp` and would have filed seven rejections
    against the wrong ads."""
    f, s = _norm(folder), _norm(sentence)
    best = 0
    for i in range(len(f)):
        for j in range(i + best + 1, len(f) + 1):
            if f[i:j] in s:
                best = j - i
            else:
                break
    return best


def _tables(text):
    """Shape 1. Only rows whose third cell is a bare verdict word."""
    out = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        raw = cells[0]
        name = _clean(raw)
        verdict = cells[2].strip().upper()
        if verdict.startswith("APPROVED"):
            v = APPROVED
        elif verdict.startswith("REJECT") or verdict.startswith("NOT APPROVED"):
            v = REJECTED
        else:
            continue
        if not _is_name(name, raw):
            continue
        reason = cells[3].strip() if len(cells) > 3 else ""
        out.append((name, v, reason))
    return out


def _numbered(text):
    """Shape 2. `NOT APPROVED: 06, 13, 16` scoped to the nearest folder named in
    the same `##` section. Returns (kit_hint, number, verdict, reason)."""
    out = []
    section, folders, recent, pending = "", [], [], None
    for line in text.splitlines():
        if line.startswith("## "):
            section, folders, recent, pending = line[3:].strip(), [], [], None
        for f in re.findall(r"`([A-Za-z0-9_./ -]+/)`", line):
            folders.append(f.rstrip("/"))
        # Prose lines only. The wave table lists every folder in the campaign, so
        # including its rows meant a folder named literally in a nearby row scored
        # its FULL name (25 chars) and swamped the actual signal -- "Section A" in
        # the verdict sentence is only 8. That handed Section A's approvals to the
        # RMBC folder, which is two rows above it in the table.
        if not line.lstrip().startswith("|"):
            recent = (recent + [line])[-4:]
        m = re.search(r"\b(NOT APPROVED|APPROVED)\s*:\s*((?:pairs\s*)?[\d,\s]+)", line)
        if not m:
            # A wrapped continuation: the approved list runs onto the next line as
            # "20, 21, 22, 23 - 17 pairs, 18 ad images (...)". Without this, four
            # approved Section A pairs were simply absent from the index.
            if pending:
                cont = re.match(r"\s*(\d+(?:\s*,\s*\d+)+)\s*(?![\d,])", line)
                if cont:
                    kit_hint, verdict, why = pending
                    for n in re.findall(r"\d+", cont.group(1)):
                        out.append((kit_hint, n.zfill(2), verdict, why))
            pending = None
            continue
        verdict = REJECTED if m.group(1) == "NOT APPROVED" else APPROVED
        nums = re.findall(r"\d+", m.group(2))
        if not nums or not folders:
            continue
        # Score against the SURROUNDING LINES, not just this one. The verdicts are
        # written as a pair:
        #     **Section A verdicts.** APPROVED: pairs 01, 02, ...
        #     NOT APPROVED: 06, 13, 16, 17, 18, 19, 24.
        # Only the first line names the kit. Scoring the NOT APPROVED line alone
        # picked whichever folder happened to come first in the wave table, and
        # filed all seven rejections against the wrong kit.
        context = " ".join(recent)
        best = max(folders, key=lambda f: (_overlap(pathlib.Path(f).name, context),
                                           _overlap(pathlib.Path(f).name, section)))
        if _overlap(pathlib.Path(best).name, context + " " + section) < 5:
            continue          # no confident kit -- no verdict, rather than a wrong one
        for n in nums:
            out.append((best, n.zfill(2), verdict, line.strip()))
        pending = (best, verdict, line.strip())
    return out


def _prose(text):
    """Shape 3. A sentence that says something was rejected, plus the backticked
    names in it. Folder tokens and scripts are excluded by _is_name."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        flat = " ".join(para.split())
        if not re.search(r"\breject(ed|ion)?\b", flat, re.I):
            continue
        if "|" in flat:                       # already handled as a table
            continue
        raws = re.findall(r"`([^`]+)`", flat)
        names = [_clean(r) for r in raws if _is_name(_clean(r), r)]
        for n in names:
            out.append((n, REJECTED, flat[:240]))
    return out


def load():
    """Returns {lowercased name: dict(verdict, reason, how)} plus a separate
    numbered index {(kit_hint_lower, '06'): dict(...)}."""
    by_name, by_number = {}, {}
    if not MAP.exists():
        return by_name, by_number
    text = MAP.read_text(encoding="utf-8", errors="replace")
    for name, v, reason in _tables(text):
        by_name[name.lower()] = dict(verdict=v, reason=reason, how="table")
    for name, v, reason in _prose(text):
        by_name.setdefault(name.lower(), dict(verdict=v, reason=reason, how="prose"))
    for kit, num, v, reason in _numbered(text):
        by_number[(kit.lower(), num)] = dict(verdict=v, reason=reason, how="numbered")

    # Explicitly recorded verdicts win over anything inferred from prose.
    # `adkit.verdict` writes these at the moment the review happens, which is the
    # only point at which the reviewer's exact words are still available.
    try:
        from adkit import verdict as _recorded
        by_name.update(_recorded.load())
    except Exception:                                     # noqa: BLE001
        pass
    return by_name, by_number


def for_ad(ad_name, kit, by_name, by_number):
    """The verdict for one ad, or None. Name match first; the numbered index only
    applies when the kit actually matches the hint."""
    hit = by_name.get(ad_name.lower())
    if hit:
        return hit
    # NOT \b: an underscore is a word character, so `\b` never fires between the
    # digits and the rest of `06_wheres_the_work`, and the numbered verdicts
    # silently matched nothing at all. Match the separator explicitly.
    m = re.match(r"^(\d{1,2})(?=[_\-. ]|$)", ad_name)
    if not m:
        return None
    num = m.group(1).zfill(2)
    kit_base = pathlib.Path(kit).name.lower()
    for (hint, n), rec in by_number.items():
        if n == num and (hint in kit_base or kit_base in hint):
            return rec
    return None


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    by_name, by_number = load()
    only_rej = "--rejected" in argv
    rows = [(n, r) for n, r in by_name.items()
            if not only_rej or r["verdict"] == REJECTED]
    rows.sort(key=lambda x: (x[1]["verdict"], x[0]))
    print("\n  %d named verdicts, %d numbered, from %s\n"
          % (len(by_name), len(by_number), MAP.name))
    for name, r in rows:
        print("  %-34s %-9s %s" % (name[:34], r["verdict"], r["reason"][:70]))
    if not only_rej and by_number:
        print()
        for (kit, num), r in sorted(by_number.items()):
            print("  %-34s %-9s (numbered, kit %s)"
                  % (num, r["verdict"], pathlib.Path(kit).name[:34]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
