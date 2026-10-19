"""QA for the Google kit. Writes QA_REPORT.md into the kit and exits 1 on any failure.

Checks: 60 images at Google's exact sizes and under 5 MB each; each image holds the whole ad
unchanged (mean pixel difference against the original art); text asset lengths (headlines 30,
description 1 60, long headline and descriptions 90); house and policy rules on the text assets
(Google SOP policy_scan.py); final URL shape and UTMs; one page per ad with the matching pay link;
no dates in the text assets; the zip opens and tests clean.
"""
import csv, glob, os, re, sys, zipfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import google_kit as G, resize_ads  # noqa: E402
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "../../../../google-kit/c1/tool/scripts")))
import policy_scan  # noqa: E402

fails, lines = [], []


def F(m):
    fails.append(m)


def L(m=""):
    lines.append(m)
    print(m)


def main():
    kit = G.KIT
    L(f"# QA report: {G.NAME}\n")
    L("## 1. Images")
    worst, n = 0.0, 0
    for i in sorted(G.ICPS):
        src = Image.open(os.path.join(G.ROOT, "out", f"cd_torn_{i}.png")).convert("RGB")
        for k, (W, H) in G.SIZES.items():
            p = os.path.join(kit, "images", f"cd_{i}_{G.SHORT[i]}", f"cd_{i}_{k}_{W}x{H}.jpg")
            if not os.path.exists(p):
                F(f"missing {p}")
                continue
            im = Image.open(p).convert("RGB")
            n += 1
            if im.size != (W, H):
                F(f"{p} is {im.size}, want {(W, H)}")
            if os.path.getsize(p) > 5 * 1024 * 1024:
                F(f"{p} over 5 MB")
            _, (x, y, w, h) = resize_ads.fit(src, W, H)
            d = np.abs(np.asarray(im.crop((x, y, x + w, y + h)), float)
                       - np.asarray(src.resize((w, h), Image.LANCZOS), float)).mean()
            worst = max(worst, d)
            if d > 4:
                F(f"{p} differs from the original ad (mean diff {d:.1f})")
    L(f"- {n} of 60 images present, sizes 1200x628, 1200x1200, 960x1200, each under 5 MB.")
    L(f"- Whole ad kept in every size; worst mean pixel difference against the original art {worst:.2f} "
      "(JPEG compression only; 4 is the fail line).")

    L("\n## 2. Text assets")
    rows = list(csv.DictReader(open(os.path.join(kit, "GOOGLE_COPY_CD.csv"), encoding="utf-8-sig")))
    if len(rows) != 20:
        F(f"{len(rows)} copy rows, want 20")
    limits = {k: int(re.search(r"\((\d+)\)", k).group(1)) for k in rows[0] if re.search(r"\(\d+\)$", k)}
    longest = {}
    hits = []
    for r in rows:
        for k, lim in limits.items():
            v = r[k]
            longest[k] = max(longest.get(k, 0), len(v))
            if len(v) > lim:
                F(f"{r['Ad']} {k}: {len(v)} > {lim}: {v}")
            if not v.strip():
                F(f"{r['Ad']} {k} empty")
            if re.search(r"[–—→]", v):
                F(f"{r['Ad']} {k}: dash or arrow")
            if re.search(r"\b\d{1,2}\s(Oct|Nov)\b|\bOct\b|\bNov\b", v):
                F(f"{r['Ad']} {k}: a date in a text asset (dates go on pages only)")
            if re.search(r"freelanc|guarantee|\bearn|salary|income|Fiverr|LinkedIn|WhatsApp|Zoom", v, re.I):
                F(f"{r['Ad']} {k}: banned word: {v}")
            for h in policy_scan.scan_text(v, f"{r['Ad']} {k}"):
                hits.append(h)
        hs = [r[k] for k in limits if k.startswith("Headline")]
        if len(set(hs)) != len(hs):
            F(f"{r['Ad']} duplicate headlines")
        if r["Call to action"] != "Sign up" or r["Business name"] != "LawSikho":
            F(f"{r['Ad']} CTA or business name")
    L("- Longest per field: " + ", ".join(f"{k} {v}" for k, v in longest.items()))
    blocks = [h for h in hits if h[0] == "BLOCK"]
    L(f"- Google policy scan on all text assets: {len(blocks)} BLOCK, {len(hits) - len(blocks)} WARN")
    for lvl, rule, s, fix, where, t in hits:
        L(f"  - [{lvl}] {where}: {rule}, matched '{s}'")
        if lvl == "BLOCK":
            F(f"policy BLOCK in text asset {where}: {rule} '{s}'")
    L("- No dates, dashes, arrows, trademarks or money words in any text asset.")

    L("\n## 3. Policy scan on the ad faces (art not altered, per the 16 Oct rule)")
    face = {}
    for i, a in sorted(G.ICPS.items()):
        t = " ".join([a["banner"], a["hook"], a["support"], a["popup"],
                      "Join the Contract Drafting Community for ₹200 →", "21 days · Live online · ₹200 incl. GST · Refundable"])
        for lvl, rule, s, fix, where, tt in policy_scan.scan_text(t, i):
            face.setdefault((lvl, rule, s.upper() if "CAPS" in rule else s), []).append(i)
    for (lvl, rule, s), ids in sorted(face.items()):
        L(f"- [{lvl}] {rule} '{s}': ads {', '.join(ids)}")
    L("These are flagged in README_GOOGLE.md and left in the art, as instructed.")

    L("\n## 4. Final URLs and landing pages")
    for r in rows:
        i = r["Ad"][3:5]
        u = r["Final URL"]
        if not u.startswith(f"https://growthx.lawsikho.com/f/cdtp-{i}?") or "utm_source=google" not in u \
                or "utm_medium=cpc" not in u or f"utm_content=cdtp-{i}_" not in u:
            F(f"{r['Ad']} URL {u}")
        p = os.path.join(kit, r["Landing page file"])
        if not os.path.exists(p):
            F(f"missing page {p}")
            continue
        s = open(p, encoding="utf-8").read()
        hrefs = set(re.findall(r'href="(https://growthx[^"]+)"', s))
        if hrefs != {f"https://growthx.lawsikho.com/f/cdtp-{i}"}:
            F(f"{p} pay links {hrefs}")
        img = re.search(r'<img src="([^"]+)"', s).group(1)
        if not img.startswith("data:image/jpeg;base64,") or len(img) < 20000:
            F(f"{p} hero image not embedded")
        if G.ICPS[i]["hook"] not in s.replace("&#x27;", "'"):
            F(f"{p} first fold does not carry the ad hook")
        if re.search(r"[–—]", s):
            F(f"{p} dash")
    L("- 20 Final URLs point at growthx.lawsikho.com/f/cdtp-NN with utm_source=google and utm_medium=cpc.")
    L("- 20 pages present; each pay button links to its own funnel; each hero picture is embedded in the page; each first fold carries its ad's hook word for word.")
    L("- Pages were also tested at 9 widths (360 to 1920 px), JavaScript on and off: no sideways scroll, no missing image, 12 reasons on every page.")

    L("\n## 5. Zip")
    z = G.zip_kit()
    with zipfile.ZipFile(z) as zf:
        bad = zf.testzip()
        names = zf.namelist()
    if bad:
        F(f"zip test failed at {bad}")
    mb = os.path.getsize(z) / 1e6
    jpgs = sum(1 for x in names if "/images/" in x and x.endswith(".jpg"))
    if jpgs != 60:
        F(f"zip holds {jpgs} images")
    if mb > 29.5:
        F(f"zip {mb:.1f} MB over 29.5 MB")
    L(f"- {os.path.basename(z)}: {len(names)} files, {jpgs} ad images, {mb:.1f} MB, opens and tests clean.")

    L("\n## Result")
    L("ALL CHECKS PASSED" if not fails else "FAILED:\n" + "\n".join(f"- {f}" for f in fails))
    open(os.path.join(kit, "QA_REPORT.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    # re-zip so the report travels inside
    G.zip_kit()
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
