#!/usr/bin/env python3
"""Media-buyer kit validator — run BEFORE zipping any handoff folder.
Usage: python3 engine/package_check.py <kit_dir>
FAILS (exit 1) unless:
  1. every ads/*.png has a matching '## <ad_id>' anchor entry in ad_copy*.md
     with non-empty **Primary text:**, **Headline:**, **Description:**
  2. the README embeds the anchor text (an 'Anchor text' section) or the full
     per-ad blocks — a buyer must never need a second file to paste copy
  3. every LP referenced in the mapping exists in landing_pages/ (or is marked live)
  4. no stale artifacts: 'PENDING', 'Launch-blocked', doubled time strings,
     'An agenda, not a promise'
  5. manifest.json is present at the kit root and valid — the importer contract, so the
     kit turns into draft funnels with zero manual cleanup on their side.
     Fix with: python3 engine/make_manifest.py <kit_dir> --write
Established 20 Jul 2026 after hr_21-24 anchor entries silently missed a handoff zip.
Check 5 added 13 Aug 2026, per the kit-importer format request.
"""
import sys, os, re, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_manifest
import verdict_log

def fail(msgs):
    print("PACKAGE CHECK: FAIL")
    for m in msgs: print("  ✗", m)
    sys.exit(1)

# --- CLI ---------------------------------------------------------------------
# --accept-defects C21,X1 --reason "..."  ships a REJECTed creative anyway. The
# override is deliberately awkward and always logged: the point is not to make it
# impossible, it is to make it attributable.
argv = sys.argv[1:]
accept_defects, override_reason = (), None
if "--accept-defects" in argv:
    i = argv.index("--accept-defects")
    accept_defects = tuple(c.strip() for c in argv[i + 1].split(",")) if i + 1 < len(argv) else ()
    del argv[i:i + 2]
if "--reason" in argv:
    i = argv.index("--reason")
    override_reason = argv[i + 1] if i + 1 < len(argv) else None
    del argv[i:i + 2]
positional = [a for a in argv if not a.startswith("--")]

kit = positional[0] if positional else "."
errs = []

if accept_defects and not override_reason:
    fail(["--accept-defects requires --reason \"<why>\"; an unexplained override is "
          "indistinguishable from a mistake six weeks later"])

ads = sorted(glob.glob(os.path.join(kit, "ads", "*.png")))
if not ads: errs.append("no ads/*.png found")

copies = glob.glob(os.path.join(kit, "ad_copy*.md"))
copy_text = "\n".join(open(c).read() for c in copies) if copies else ""
if not copies: errs.append("no ad_copy*.md in kit root")

readmes = glob.glob(os.path.join(kit, "README*"))
readme_text = "\n".join(open(r).read() for r in readmes) if readmes else ""
if not readmes: errs.append("no README in kit root")

for a in ads:
    ad_id = os.path.splitext(os.path.basename(a))[0]  # e.g. hr_16_sideincome2
    # match '## hr_16_sideincome2' allowing suffixes after the id
    pat = re.compile(rf"^## {re.escape(ad_id)}\b(.*?)(?=^## |\Z)", re.S | re.M)
    m = pat.search(copy_text)
    if not m:
        errs.append(f"{ad_id}: NO anchor entry in ad_copy")
        continue
    block = m.group(0)
    for field in ("**Primary text:**", "**Headline:**", "**Description:**"):
        if field not in block or len(block.split(field, 1)[1].splitlines()[0].strip()) < 5:
            errs.append(f"{ad_id}: anchor entry missing/empty {field}")
    if "SUPERSEDED" in block:
        errs.append(f"{ad_id}: marked SUPERSEDED in ad_copy but PNG is in the kit — remove one")
    # README must carry this ad's copy too (buyer reads one file)
    if m and readme_text and ad_id not in readme_text:
        errs.append(f"{ad_id}: not mentioned in README (mapping or anchor appendix)")

if readme_text and "Primary text:" not in readme_text:
    errs.append("README has no embedded anchor text ('Primary text:' not found) — add the anchor appendix")

lps = set(os.path.basename(p) for p in glob.glob(os.path.join(kit, "landing_pages", "*.html")))
for ref in set(re.findall(r"lp_[a-z0-9_]+\.html", copy_text + readme_text)):
    if ref not in lps:
        errs.append(f"referenced LP not in kit: {ref}")

STALE = ["Launch-blocked", "LP PENDING", "Mon Sat–Sun", "An agenda, not a promise"]
for f in copies + readmes + sorted(glob.glob(os.path.join(kit, "landing_pages", "*.html"))):
    t = open(f).read()
    for pat in STALE:
        if pat in t: errs.append(f"stale artifact '{pat}' in {os.path.basename(f)}")

errs += make_manifest.validate(kit)

# --- check 6: the judgement gate ---------------------------------------------
# Added 16 Aug 2026. Until now creative_judge.py only ran when someone chose to run
# it, so a REJECTed creative could still be zipped and sent. Measured over 30 days,
# 25% of Ramanuj's messages were corrections on work that had reached him unjudged.
# A kit does not leave this machine while anything in it is rejected or unjudged.
rows = verdict_log.read_all()
gate_errs = []
for a in ads:
    ok, detail = verdict_log.gate(a, rows=rows, accept_defects=accept_defects)
    if not ok:
        gate_errs.append(detail)
if gate_errs:
    errs += gate_errs
    errs.append("run: python3 ads/creative_judge.py %s   (then fix and re-render)" % kit)
elif accept_defects:
    for a in ads:
        verdict_log.record_override(a, accept_defects, override_reason)
    print(f"  ! shipping with accepted defects {','.join(accept_defects)}: {override_reason}")

if errs: fail(errs)
print(f"PACKAGE CHECK: PASS — {len(ads)} ads, each with complete anchor text; README carries the copy; {len(lps)} LPs present; manifest.json valid.")
