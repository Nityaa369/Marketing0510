#!/usr/bin/env python3
"""Read and write engine/creative_verdicts.jsonl.

The log existed before this module and creative_judge.py still appends to it; this
adds the lookup side, which is what turns a record of judgements into a gate.

The freshness rule is the whole point. A verdict authorises the exact bytes it was
computed from, so a verdict older than the PNG it names authorises nothing: someone
edited the creative after it was judged. Without that check the gate would be
trivially defeated by fixing nothing and re-zipping.

Schema (superset; older rows carry only the first group and are read fine):
    ts, kit, file, gate, verdict, reason, rules_fired, n_block, n_fix, n_warn
    source      producer | whatsapp | manual
    iterations  how many judge-fix rounds preceded this verdict
    overrides   [{code, reason, ts}]
"""

import hashlib
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "creative_verdicts.jsonl")

REJECT = "REJECT"
ACCEPT = "ACCEPT"
CHANGES = "ACCEPT WITH CHANGES"


def _stem(name):
    return os.path.splitext(os.path.basename(name))[0]


def _stem_variants(name):
    """Every plausible spelling of a creative's stem.

    Kits are not consistent: women_ai_r10_sep05 judges `src_W3_N18_caregiver.html`
    and ships `W3_N18_caregiver.png`. A literal stem match reported that freshly
    judged creative as "never judged", which would have blocked a clean kit and
    taught everyone to reach for --accept-defects. Same variant list as
    creative_judge.stem_variants, deliberately: the gate must agree with the judge
    about what counts as the same creative.
    """
    stem = _stem(name)
    out = [stem]
    for rx in (r"^src_", r"^_+", r"^ad_", r"_1080x1350$"):
        out += [re.sub(rx, "", s) for s in list(out)]
    return set(s for s in out if s)


def read_all(path=LOG):
    rows = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue        # a torn line must not blind the gate entirely
    except FileNotFoundError:
        pass
    return rows


def latest_for(creative, path=LOG, rows=None):
    """Newest verdict for a creative, matched on stem.

    The log records the HTML filename while the kit ships PNGs, so `hr_04.html`
    and `hr_04.png` have to resolve to the same creative.
    """
    want = _stem_variants(creative)
    rows = read_all(path) if rows is None else rows
    hits = [r for r in rows if _stem_variants(r.get("file", "")) & want]
    return max(hits, key=lambda r: r.get("ts", "")) if hits else None


def _mtime_iso(p):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime(p)))


def is_stale(row, creative_path):
    """True if the creative was modified after it was judged.

    A verdict dated in the future is also treated as stale. It should not happen,
    but if it does it would authorise every later edit indefinitely, which is the
    one failure this check exists to prevent. Clock skew must not open the gate.
    """
    if not row or not row.get("ts"):
        return True
    ts = row["ts"]
    if ts > time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() + 120)):
        return True
    try:
        return ts < _mtime_iso(creative_path)
    except OSError:
        return True


def gate(creative_path, path=LOG, rows=None, accept_defects=()):
    """Decide whether this creative may ship.

    Returns (ok, detail). Absence of a verdict is a failure, not a pass: the
    default has to be closed, or the gate only catches creatives someone already
    chose to submit.
    """
    row = latest_for(creative_path, path, rows)
    name = os.path.basename(creative_path)

    if row is None:
        return False, f"{name}: never judged. Run: python3 ads/creative_judge.py <kit>"

    if is_stale(row, creative_path):
        return False, (f"{name}: judged {row.get('ts')} but the file changed since "
                       f"({_mtime_iso(creative_path)}). Re-judge it.")

    verdict = row.get("verdict", "")
    if verdict.startswith(REJECT):
        fired = [c for c in row.get("rules_fired", []) if c not in accept_defects]
        if not fired:
            return True, f"{name}: REJECT overridden ({','.join(row.get('rules_fired', []))})"
        return False, f"{name}: {verdict} — {', '.join(fired)}"

    if verdict == CHANGES:
        return True, f"{name}: {verdict} ({row.get('reason', '')})"

    return True, f"{name}: {verdict}"


def record_human(creative, verdict, diagnosis, rule_code=None, path=LOG):
    """Log what RAMANUJ decided, next to what the machine decided.

    This is the loop that was missing. The log held 42 machine verdicts and zero
    human ones, so nobody could ask the only question that improves a rulebook:
    where does the judge disagree with the owner? Without that record, every
    correction is a conversation that evaporates, and the same defect ships again
    six weeks later under a different kit name.

    rule_code: the checker that caught it, or None. None is the interesting case —
    it means a defect he can see and the system cannot, which is a rule to build.
    """
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "file": os.path.basename(creative),
            "verdict": verdict,
            "judged_by": "ramanuj",
            "diagnosis": diagnosis,
            "rule_code": rule_code,
            "source": "human",
        }, ensure_ascii=False) + "\n")


def gap_id(row):
    """Stable id for a logged human rejection.

    Timestamps are written to the second, and several verdicts recorded in one pass
    share one. Keying closures on ts alone made the last closure win for every gap
    in that second, silently marking an open gap as solved. Hash the content too.
    """
    raw = f"{row.get('ts','')}|{row.get('file','')}|{row.get('diagnosis','')}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def close_gap(gid, rule_code, note="", path=LOG):
    """Record that a checker now catches what only Ramanuj used to catch."""
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "gap_closed": gid, "rule_code": rule_code, "note": note,
            "source": "system",
        }, ensure_ascii=False) + "\n")


def rule_gaps(path=LOG, include_closed=False):
    """Human rejections no checker caught: the worklist of rules still to build.

    This is the report to read before deciding what to improve. A defect Ramanuj can
    see and the system cannot is worth more than another refinement of a rule that
    already works.
    """
    rows = read_all(path)
    closed = {r["gap_closed"]: r for r in rows if r.get("gap_closed")}
    out = []
    for r in rows:
        if r.get("judged_by") != "ramanuj" or r.get("rule_code"):
            continue
        if not str(r.get("verdict", "")).startswith("REJECT"):
            continue
        gid = gap_id(r)
        c = closed.get(gid)
        if c and not include_closed:
            continue
        out.append((gid, r.get("file", ""), r.get("diagnosis", ""),
                    c["rule_code"] if c else None))
    return out


def record_override(creative, codes, reason, path=LOG):
    """Append an explicit, attributable override.

    Overrides are logged rather than silently permitted so that "we shipped this
    anyway" stays answerable later.
    """
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "file": os.path.basename(creative),
            "verdict": "OVERRIDE",
            "overrides": [{"code": c, "reason": reason} for c in codes],
            "source": "manual",
        }, ensure_ascii=False) + "\n")
