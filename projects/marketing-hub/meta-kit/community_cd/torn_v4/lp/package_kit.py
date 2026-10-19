"""Assemble the Meta kit: 20 ads + 20 pages + upload sheet + copy + manifest + value props + hooks.

    python3 package_kit.py <copy.json>
"""
import csv, json, os, re, shutil, subprocess, sys, zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
NAME = "ContractDrafting_TornPaper_LawSikho_21Oct-11Nov"
KIT = os.path.join(ROOT, "kit", NAME)
sys.path.insert(0, HERE)
import build_lps, vp_data  # noqa: E402

ICPS = json.load(open(os.path.join(ROOT, "icps.json"), encoding="utf-8"))
CAMPAIGN = "CD_Community_TornPaper_21Oct-11Nov_Sales"
SETS = {
    "A_StudentsAndNewLawyers": ["01", "02", "03", "04", "19"],
    "B_LawyersNearContracts": ["05", "06", "16", "17", "18"],
    "C_LawyersWhoseLifeMoved": ["07", "08", "09", "10", "20"],
    "D_LLBHoldersInOtherJobs": ["11", "12", "13", "14", "15"],
}
SET_OF = {i: s for s, ids in SETS.items() for i in ids}
SHORT = {"01": "finalyear", "02": "graduates", "03": "newadvocates", "04": "junioradvocates",
         "05": "paralegals", "06": "smallpractice", "07": "smallercities", "08": "womenreturning",
         "09": "movedmarriage", "10": "abroad", "11": "hr", "12": "banking", "13": "content",
         "14": "salesops", "15": "bpo", "16": "lpo", "17": "companysecretary", "18": "property",
         "19": "interns", "20": "leftfirm"}
AXIS = {"01": "graduation: a degree now against drafting skill now",
        "02": "the degree held against the drafting job it can buy",
        "03": "enrolment against a first practice of business clients",
        "04": "court corridors against desk work for businesses",
        "05": "preparing files against drafting as the lawyer",
        "06": "after the dispute against before the signature",
        "07": "a smaller city against clients from anywhere",
        "08": "a family break against a home-based comeback",
        "09": "a city move against work that moves with you",
        "10": "living abroad against India and UK clients",
        "11": "issuing HR documents against drafting them as the lawyer",
        "12": "how money moves against the papers behind the deal",
        "13": "writing for a living against writing contracts",
        "14": "seeing deals done against drafting the contracts that close them",
        "15": "a back-office job against the lawyer the LLB trained",
        "16": "reviewing contracts against drafting them",
        "17": "company records against founder and investor contracts",
        "18": "sale deeds against commercial contracts",
        "19": "interning against becoming a drafter in college",
        "20": "leaving the firm against coming back with own clients"}
HEADLINE = "Contract Drafting Community, ₹200"
DESC = "21 days, live online. Refundable."


def url(i):
    return (f"https://growthx.lawsikho.com/f/cdtp-{i}?utm_source=meta&utm_medium=paid_social"
            f"&utm_campaign=cd_tornpaper&utm_content=cdtp-{i}_{SHORT[i]}")


def primary(i):
    a = ICPS[i]
    return (f"{a['hook']}\n\n{a['support']}\n\n"
            "LawSikho Contract Drafting Community: 21 days, one document a day, 9 live evening sessions. "
            "₹200 incl. GST. Refundable. Live online.")


def main(copy_path):
    if os.path.isdir(KIT):
        shutil.rmtree(KIT)
    for d in ("ads", "landing_pages"):
        os.makedirs(os.path.join(KIT, d))
    subprocess.run([sys.executable, os.path.join(HERE, "build_lps.py"), copy_path,
                    os.path.join(KIT, "landing_pages")], check=True)
    ids = sorted(ICPS)
    for i in ids:
        Image.open(os.path.join(ROOT, "out", f"cd_torn_{i}.png")).convert("RGB").save(
            os.path.join(KIT, "ads", f"cd_{i}.jpg"), quality=88, optimize=True)
    cs = Image.open(os.path.join(ROOT, "ship", "CONTACT_SHEET_v4.jpg")).convert("RGB")
    cs.thumbnail((1600, 1600))
    cs.save(os.path.join(KIT, "CONTACT_SHEET.jpg"), quality=78)

    open(os.path.join(KIT, "value_props.md"), "w", encoding="utf-8").write(
        "# Value props, Contract Drafting Community torn-paper set\n\n" + "\n".join(vp_data.block(i) for i in ids))
    hk = ["# Hooks, Contract Drafting Community torn-paper set\n"]
    for i in ids:
        a = ICPS[i]
        parts = re.split(r"(?<=\.)\s+", a["hook"], maxsplit=1)
        hk.append(f"## {i} | {a['banner'].replace('FOR ', '', 1)}\nstatement: {parts[0]}\n"
                  f"turn: {parts[1] if len(parts) > 1 else ''}\naxis: {AXIS[i]}\n")
    open(os.path.join(KIT, "hooks.md"), "w", encoding="utf-8").write("\n".join(hk))

    rows, man = [], []
    for i in ids:
        a = ICPS[i]
        row = {"Campaign": CAMPAIGN, "Ad set": SET_OF[i], "Locations": "India", "Age": "21 to 45",
               "Ad name": f"CD_TP_{i}_{SHORT[i]}", "Image (2:3 feed, 1024x1536)": f"ads/cd_{i}.jpg",
               "Primary text": primary(i), "Headline": HEADLINE, "Description": DESC,
               "Call to action": "Sign up", "Website URL": url(i),
               "Landing page file": f"landing_pages/lp_cd_{i}.html", "GrowthX funnel slug": f"cdtp-{i}",
               "GrowthX ctaLabels": build_lps.BTN}
        if i == "10":
            row["Locations"] = "UAE, UK, USA, Canada, Singapore, Australia (Indian expats)"
        rows.append(row)
        man.append({"id": i, "icp": a["banner"], "hook": a["hook"], "support": a["support"], "popup": a["popup"],
                    "ad": row["Image (2:3 feed, 1024x1536)"], "landing_page": row["Landing page file"],
                    "hero_image": f"landing_pages/img/cd_{i}.jpg", "ad_set": SET_OF[i],
                    "growthx_slug": row["GrowthX funnel slug"], "website_url": row["Website URL"],
                    "button": build_lps.BTN, "meta_cta": "SIGN_UP", "headline": HEADLINE,
                    "description": DESC, "primary_text": row["Primary text"]})
    with open(os.path.join(KIT, "CD_meta_upload_sheet.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    json.dump({"kit": NAME, "brand": "LawSikho", "product": "Contract Drafting Community",
               "price": "₹200 incl. GST, refundable", "dates_on_pages_only": "21 Oct to 11 Nov 2026",
               "campaign": CAMPAIGN, "ad_sets": SETS, "ads": man},
              open(os.path.join(KIT, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    ac = ["# Ad copy, 20 Meta ads (LawSikho · Contract Drafting Community)\n",
          f"Headline (all): **{HEADLINE}** ({len(HEADLINE)} characters). Description: **{DESC}** CTA: **Sign up** (SIGN_UP).\n"]
    for i in ids:
        a = ICPS[i]
        ac.append(f"## {i} · {a['banner']}\n\n- Ad set: {SET_OF[i]}\n- Pop-up on the button: {a['popup']}\n"
                  f"- Hook line: {len(a['hook'])} characters\n- URL: {url(i)}\n- Page: landing_pages/lp_cd_{i}.html\n\n"
                  "Primary text:\n\n" + "\n".join("> " + l if l else ">" for l in primary(i).split("\n")) + "\n")
    open(os.path.join(KIT, "ad_copy.md"), "w", encoding="utf-8").write("\n".join(ac))
    shutil.copy(os.path.join(HERE, "README_FOR_MEDIA_BUYER.md"), KIT)

    z = os.path.join(ROOT, "kit", f"{NAME}_SEND_THIS.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for d, _, fs in os.walk(KIT):
            for fn in sorted(fs):
                p = os.path.join(d, fn)
                zf.write(p, os.path.join(NAME, os.path.relpath(p, KIT)))
    print("zip", z, os.path.getsize(z) // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1])
