#!/usr/bin/env python3
"""
campaign_map_sync.py - join live Meta performance back onto the kits in this folder.

`ad-analysis-shared/pull_ads.py` answers "what is spending and what is it costing".
This answers the question that folder actually cares about: **which of the pairs we
built are the ones that worked**, so the next wave is built on evidence rather than
from scratch (the stated purpose of CAMPAIGN_MAP.md).

It reads the GST-inclusive JSON that pull_ads.py already writes, matches each live
ad name back to the .png in a kit's ads/ folder, and prints a verdict block per
campaign using the SOP/02 and SOP/03 thresholds:

    scale <= Rs 250 CPP  ·  target <= Rs 300  ·  circuit breaker > Rs 450  ·  freq > 3.5 = fatigue

Usage:
    python campaign_map_sync.py                      # newest report in reports/
    python campaign_map_sync.py --report <file.json>
    python campaign_map_sync.py --write              # also update the block in CAMPAIGN_MAP.md

The match is a guess, not a fact. Meta ad names are typed by the media buyer and
nothing enforces that they echo the .png filename. So every run prints its match
rate and lists what it could not place: treat a low rate as "the naming convention
is not being followed", not as "these ads did not run". Nothing is written to
CAMPAIGN_MAP.md unless you pass --write, and then only between the markers.

All rupee figures come in already grossed up by pull_ads.py. Never multiply again.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Windows consoles default to cp1252 and would die on the report glyphs.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "ad-analysis-shared" / "reports"
CAMPAIGN_MAP = HERE / "CAMPAIGN_MAP.md"

BEGIN = "<!-- BEGIN AUTO PERFORMANCE -->"
END = "<!-- END AUTO PERFORMANCE -->"

# SOP/02 · Money
SCALE_AT = 250
TARGET = 300
BREAKER = 450
FATIGUE_FREQ = 3.5

# Structural tokens only - kit prefixes and file noise. Keep this list SHORT.
# Anything descriptive must stay: "test" was in here once and reduced the real
# creative "11_eye_test" to the single weak token {eye}.
NOISE = {"ad", "ads", "png", "jpg", "jpeg", "lp", "cw", "final"}


def norm_tokens(s):
    """Identity-carrying tokens of a name: alpha, 3+ chars, minus known noise."""
    parts = re.split(r"[^a-z0-9]+", (s or "").lower())
    return [p for p in parts if p.isalpha() and len(p) >= 3 and p not in NOISE]


def norm_join(s):
    return "_".join(norm_tokens(s))


def index_kits():
    """Every ad face in the folder, keyed by its file stem.

    A kit is any directory holding an ads/ subfolder with images in it - the
    structure SOP/01 mandates.
    """
    out = []
    for ads_dir in sorted(HERE.glob("**/ads")):
        if not ads_dir.is_dir():
            continue
        parts = ads_dir.parts
        if any(x in {"__pycache__", ".git", "node_modules"} for x in parts):
            continue
        # archived / superseded creative must never win a match over the live kit
        if any(x.lower().startswith(("_archive", "archive", "_old", "_superseded"))
               for x in parts):
            continue
        kit = ads_dir.parent
        for img in sorted(ads_dir.iterdir()):
            if img.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue
            toks = norm_tokens(img.stem)
            if not toks:
                continue
            out.append({
                "kit": kit.relative_to(HERE).as_posix(),
                "file": img.relative_to(HERE).as_posix(),
                "stem": img.stem,
                "tokens": set(toks),
                "joined": "_".join(toks),
            })
    return out


def match(ad_name, kits):
    """Best kit face for a live ad name. Returns (entry, score, ambiguous)."""
    toks = set(norm_tokens(ad_name))
    if not toks:
        return None, 0.0, False
    joined = "_".join(norm_tokens(ad_name))

    # Pad with separators so containment lands on token boundaries. Without this
    # the stem "tally" matches the ad name "Totally Unrelated" - caught in test.
    padded = f"_{joined}_"

    scored = []
    for k in kits:
        kj = k["joined"]
        if not kj:
            continue
        # A single-token stem is too weak to carry a containment match on its own
        # ("hero", "chat"); it must match the whole name exactly.
        if len(k["tokens"]) < 2 or len(toks) < 2:
            score = 1.0 if k["tokens"] == toks else 0.0
        elif f"_{kj}_" in padded or padded in f"_{kj}_":
            score = 1.0  # one name contains the other, token-aligned
        else:
            union = toks | k["tokens"]
            score = len(toks & k["tokens"]) / len(union) if union else 0.0
        if score > 0:
            scored.append((score, k))
    if not scored:
        return None, 0.0, False

    scored.sort(key=lambda t: -t[0])
    best_score, best = scored[0]
    if best_score < 0.6:
        return None, best_score, False
    # Only genuinely ambiguous when the tie is between *different creatives*.
    # The same stem sitting in several kit folders is duplication, not ambiguity.
    tied_stems = {k["stem"] for sc, k in scored if abs(sc - best_score) < 1e-9}
    return best, best_score, len(tied_stems) > 1


def newest_report():
    if not REPORTS.is_dir():
        return None
    files = sorted(REPORTS.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def verdict(cpr, freq):
    """SOP/02 thresholds. cpr may be None when a cell has no results yet."""
    if cpr is None:
        return "no results"
    if cpr > BREAKER:
        return "PAUSE (circuit breaker)"
    if cpr <= SCALE_AT:
        return "SCALE"
    if cpr <= TARGET:
        return "on target"
    if freq and freq > FATIGUE_FREQ:
        return "over target - fatigue, refresh"
    return "over target"


def build(report_path):
    data = json.loads(report_path.read_text(encoding="utf-8"))
    ads = data.get("ads", [])
    kits = index_kits()

    campaigns = {}
    matched = unmatched = 0
    misses = []
    for a in ads:
        entry, score, ambiguous = match(a.get("ad_name"), kits)
        if entry:
            matched += 1
        else:
            unmatched += 1
            misses.append(a.get("ad_name") or "(unnamed)")
        row = dict(a, _kit=entry, _score=score, _ambiguous=ambiguous)
        campaigns.setdefault((a.get("account"), a.get("campaign")), []).append(row)

    lines = []
    lines.append(f"_Auto-generated from `{report_path.name}` "
                 f"({data.get('pulled')}, last {data.get('window_days')} days). "
                 f"All Rs incl. 18% GST. Do not hand-edit between the markers._")
    lines.append("")

    # Never blend funnel types: one table per campaign, never a folder-wide total.
    for (acct, camp), rows in sorted(
            campaigns.items(), key=lambda kv: -sum(r.get("spend_gst", 0) for r in kv[1])):
        rows.sort(key=lambda r: -r.get("spend_gst", 0))
        spend = sum(r.get("spend_gst", 0) for r in rows)
        buys = sum(r.get("buyers", 0) for r in rows)
        leads = sum(r.get("leads", 0) for r in rows)
        kind, total = ("buyer", buys) if buys else ("lead", leads)

        lines.append(f"### {camp}")
        head = f"Account **{acct}** · Rs {spend:,.0f} · {total:.0f} {kind}s"
        if total:
            head += f" · Rs {spend / total:,.0f} per {kind}"
        lines.append(head)
        lines.append("")
        lines.append(f"| Ad | Kit pair | Spend | {kind.title()}s | Cost/{kind} | Freq | Verdict |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in rows:
            res = r.get("buyers", 0) if kind == "buyer" else r.get("leads", 0)
            sp = r.get("spend_gst", 0)
            cpr = sp / res if res else None
            freq = r.get("freq") or 0
            if r["_kit"]:
                pair = f"[{r['_kit']['stem']}]({r['_kit']['file']})"
                if r["_ambiguous"]:
                    pair += " **(ambiguous)**"
                elif r["_score"] < 1.0:
                    pair += f" ~{r['_score']:.2f}"
            else:
                pair = "unmatched"
            lines.append(
                f"| {r.get('ad_name') or ''} | {pair} | Rs {sp:,.0f} | {res:.0f} | "
                f"{('Rs %s' % format(round(cpr), ',')) if cpr else '—'} | "
                f"{freq:.2f} | {verdict(cpr, freq)} |")
        lines.append("")

    total_ads = matched + unmatched
    rate = (matched / total_ads * 100) if total_ads else 0
    lines.append(f"**Match rate: {matched}/{total_ads} ads ({rate:.0f}%) placed against a kit "
                 f"in this folder.**")
    if misses:
        lines.append("")
        lines.append("Unmatched live ad names (kit not found, or named differently in Meta):")
        for m in sorted(set(misses)):
            lines.append(f"- `{m}`")
    lines.append("")
    return "\n".join(lines), rate, matched, total_ads


def write_block(body):
    text = CAMPAIGN_MAP.read_text(encoding="utf-8")
    block = f"{BEGIN}\n\n## Live performance\n\n{body}\n{END}"
    if BEGIN in text and END in text:
        pre = text.split(BEGIN)[0]
        post = text.split(END, 1)[1]
        text = pre + block + post
    else:
        text = text.rstrip() + "\n\n---\n\n" + block + "\n"
    CAMPAIGN_MAP.write_text(text, encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--report", help="report JSON from pull_ads.py (default: newest)")
    p.add_argument("--write", action="store_true",
                   help="update the auto block in CAMPAIGN_MAP.md")
    args = p.parse_args()

    path = Path(args.report) if args.report else newest_report()
    if not path or not path.exists():
        sys.exit(
            "No report found. Pull one first:\n"
            "    python ad-analysis-shared/pull_ads.py --list\n"
            "    python ad-analysis-shared/pull_ads.py <keyword> --days 14\n"
            f"(looked in {REPORTS})")

    body, rate, matched, total = build(path)
    print(body)
    if args.write:
        write_block(body)
        print(f"\nupdated {CAMPAIGN_MAP.name} between the markers.")
    if total and rate < 60:
        print("\nWARNING: fewer than 60% of live ads matched a kit. Check that ads are "
              "named in Meta after their .png stem before trusting this table.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
