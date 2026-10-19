"""Google kit for the 20 Contract Drafting torn-paper ads (Performance Max / Demand Gen / Display).

    python3 google_kit.py

Same design as Meta (divyanshu, 16 Oct: "Google kit = same design as Meta by default"): each ad is fitted
whole into Google's three sizes with a wash from its own paper edge, words untouched. Text assets are
written for Google: neutral audience wording, no trademarks, no arrows, no dates, ₹200 only as the price.
Pages are the same 20 pages (1 ad = 1 page); only the UTM source changes.
"""
import csv, json, os, shutil, sys, zipfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import resize_ads  # noqa: E402

NAME = "ContractDrafting_TornPaper_LawSikho_21Oct-11Nov_Google"
KIT = os.path.join(ROOT, "google", NAME)
META_PAGES = os.path.join(ROOT, "kit", "ContractDrafting_TornPaper_LawSikho_21Oct-11Nov", "landing_pages")
ICPS = json.load(open(os.path.join(ROOT, "icps.json"), encoding="utf-8"))
SIZES = {"landscape": (1200, 628), "square": (1200, 1200), "portrait": (960, 1200)}
SHORT = {"01": "finalyear", "02": "graduates", "03": "newadvocates", "04": "junioradvocates",
         "05": "paralegals", "06": "smallpractice", "07": "smallercities", "08": "returning",
         "09": "newcity", "10": "abroad", "11": "hr", "12": "banking", "13": "content",
         "14": "salesops", "15": "bpo", "16": "lpo", "17": "companysecretary", "18": "property",
         "19": "interns", "20": "leftfirm"}
CAMPAIGNS = {
    "CD_G_A_StudentsAndNewLawyers": ["01", "02", "03", "04", "19"],
    "CD_G_B_LawyersNearContracts": ["05", "06", "16", "17", "18"],
    "CD_G_C_LawyersWorkingRemotely": ["07", "08", "09", "10", "20"],
    "CD_G_D_LLBHoldersInOtherJobs": ["11", "12", "13", "14", "15"],
}
CAMP_OF = {i: c for c, ids in CAMPAIGNS.items() for i in ids}

# (audience in neutral words, headline 1 = the move, headline 2 = the audience, long headline, description 3)
COPY = {
 "01": ("Final-year law students", "Graduate as a contract drafter", "For final-year law students",
        "Final-year law students: graduate as a lawyer who already drafts contracts for businesses",
        "Draft one document a day, from an NDA to a co-founder agreement."),
 "02": ("Law graduates not practising yet", "Draft contracts for startups", "For law graduates",
        "Law graduates: become the lawyer startups hire to draft their contracts",
        "Learn co-founder agreements, ESOP plans, SAFE agreements and term sheets."),
 "03": ("Newly enrolled advocates", "Start a drafting practice", "For newly enrolled advocates",
        "Newly enrolled advocates: build your first practice by drafting contracts for businesses",
        "Draft NDAs, employment agreements and vendor contracts for businesses."),
 "04": ("Junior advocates in litigation chambers", "Move from court to drafting", "For junior litigation lawyers",
        "Junior advocates: become the lawyer businesses call to draft their contracts",
        "Contract work is done at a desk: SaaS agreements, leases and vendor contracts."),
 "05": ("Paralegals and legal assistants with an LLB", "Draft contracts as the lawyer", "For paralegals with an LLB",
        "Paralegals with an LLB: draft the contract yourself, as the lawyer",
        "Spot missing clauses and red flags with AI, then draft the clause that fixes them."),
 "06": ("Lawyers running their own small practice", "Draft before your clients sign", "For small-practice lawyers",
        "Small-practice lawyers: become the lawyer clients come to before they sign",
        "Add the contracts startups need, like SaaS agreements and IP licences."),
 "07": ("Lawyers in smaller cities", "Draft for startups and the UK", "For lawyers in smaller cities",
        "Lawyers in smaller cities: draft contracts for startups and UK businesses from home",
        "Learn to draft a GDPR privacy policy for UK small businesses."),
 "08": ("Lawyers returning after a career break", "Return as a contract drafter", "For lawyers back from a break",
        "Lawyers back from a break: return as a contract drafting lawyer who works from home",
        "One short lesson a day on your phone, and live sessions in the evening."),
 "09": ("Lawyers who moved to a new city", "Draft contracts from any city", "For lawyers in a new city",
        "Lawyers in a new city: become a contract drafting lawyer who can work from any city",
        "Contracts are drafted at a desk, not argued in a local court."),
 "10": ("Indian lawyers living abroad", "Draft for India and UK clients", "For Indian lawyers abroad",
        "Indian lawyers abroad: draft contracts for businesses in India and the UK",
        "Learn to draft DPDPA and GDPR privacy policies for small businesses."),
 "11": ("LLB holders working in HR", "Draft HR contracts as a lawyer", "For LLB holders in HR",
        "LLB holders in HR: become the lawyer companies hire to draft offer letters and HR policies",
        "Draft employment agreements, non-compete clauses and ESOP plans."),
 "12": ("LLB holders working in banking", "Draft the papers behind deals", "For LLB holders in banking",
        "LLB holders in banking: become the lawyer who drafts the papers behind the deal",
        "Draft term sheets, SAFE agreements and representations and warranties clauses."),
 "13": ("LLB holders working in content", "Write contracts and policies", "For LLB holders in content",
        "LLB holders in content: write the contracts and policies businesses sign",
        "Draft website terms, privacy policies and cookie policies for online businesses."),
 "14": ("LLB holders in sales and operations", "Draft the contracts deals need", "For LLB holders in sales",
        "LLB holders in sales and operations: draft the contracts that close deals",
        "Draft SaaS agreements, vendor service agreements and commercial leases."),
 "15": ("LLB holders in BPO and back-office jobs", "Become a contract drafter", "For LLB holders in BPO jobs",
        "LLB holders in back-office jobs: become the contract drafting lawyer you trained to be",
        "Start with the parts of a contract and build up, one document a day."),
 "16": ("Lawyers reviewing contracts in LPO jobs", "From contract review to drafts", "For LPO contract reviewers",
        "LPO contract reviewers: become the lawyer who drafts the contracts you review",
        "Move from checking clauses to writing NDAs, SaaS agreements and IP licences."),
 "17": ("Company secretaries with an LLB", "Draft founder contracts", "For company secretaries",
        "Company secretaries with an LLB: draft the founder and investor contracts startups sign",
        "Draft co-founder agreements, SAFE agreements and term sheets."),
 "18": ("Property and conveyancing lawyers", "Go beyond sale deeds", "For property lawyers",
        "Property lawyers: become the lawyer businesses hire for their commercial contracts",
        "Build from commercial leases to SaaS agreements and joint development agreements."),
 "19": ("Law students doing internships", "Start drafting in college", "For law students interning",
        "Law students: start becoming a contract drafting lawyer while you are in college",
        "Learn the parts of a contract and draft one document a day."),
 "20": ("Lawyers who left a law firm", "Return with your own clients", "For lawyers who left a firm",
        "Lawyers who left a firm: come back as a contract drafting lawyer with your own clients",
        "Refresh with one contract a day and learn how to reach startup clients."),
}
H3, H4, H5 = "Contract Drafting Community", "Learn contract drafting live", "₹200 incl. GST, live online"
D1 = "One document a day, 9 live sessions. ₹200 incl. GST."
D2 = "Contract drafting is writing the agreements a business signs: duties, payment and risk."
D4 = "Refundable. Live online sessions, recordings not promised. By LawSikho."


def url(i):
    return (f"https://growthx.lawsikho.com/f/cdtp-{i}?utm_source=google&utm_medium=cpc"
            f"&utm_campaign=cd_tornpaper_google&utm_content=cdtp-{i}_{SHORT[i]}")


def rows():
    out = []
    for i in sorted(ICPS):
        aud, h1, h2, lh, d3 = COPY[i]
        out.append({"Ad": f"cd_{i}_{SHORT[i]}", "Campaign": CAMP_OF[i], "Audience signal": aud,
                    "Headline 1 (30)": h1, "Headline 2 (30)": h2, "Headline 3 (30)": H3,
                    "Headline 4 (30)": H4, "Headline 5 (30)": H5, "Long headline (90)": lh,
                    "Description 1 (60)": D1, "Description 2 (90)": D2, "Description 3 (90)": d3,
                    "Description 4 (90)": D4, "Business name": "LawSikho", "Call to action": "Sign up",
                    "Final URL": url(i), "Landing page file": f"landing_pages/lp_cd_{i}.html",
                    "Images": f"images/cd_{i}_{SHORT[i]}/ (3 files)"})
    return out


def build():
    if os.path.isdir(KIT):
        shutil.rmtree(KIT)
    os.makedirs(os.path.join(KIT, "images"))
    shutil.copytree(META_PAGES, os.path.join(KIT, "landing_pages"))
    for i in sorted(ICPS):
        d = os.path.join(KIT, "images", f"cd_{i}_{SHORT[i]}")
        os.makedirs(d)
        src = Image.open(os.path.join(ROOT, "out", f"cd_torn_{i}.png"))
        for k, (W, H) in SIZES.items():
            im, _ = resize_ads.fit(src, W, H)
            im.save(os.path.join(d, f"cd_{i}_{k}_{W}x{H}.jpg"), quality=93, optimize=True, progressive=True)
    rs = rows()
    with open(os.path.join(KIT, "GOOGLE_COPY_CD.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0]))
        w.writeheader()
        w.writerows(rs)
    # contact sheets, one per size
    os.makedirs(os.path.join(KIT, "contact_sheets"))
    for k, (W, H) in SIZES.items():
        tw = 300 if k != "landscape" else 400
        th = round(tw * H / W)
        sheet = Image.new("RGB", (5 * tw + 60, 4 * th + 50), "white")
        for n, i in enumerate(sorted(ICPS)):
            im = Image.open(os.path.join(KIT, "images", f"cd_{i}_{SHORT[i]}", f"cd_{i}_{k}_{W}x{H}.jpg"))
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (10 + (n % 5) * (tw + 10), 10 + (n // 5) * (th + 10)))
        sheet.save(os.path.join(KIT, "contact_sheets", f"{k}_{W}x{H}.jpg"), quality=82)
    shutil.copy(os.path.join(HERE, "README_GOOGLE.md"), KIT)


def zip_kit():
    z = os.path.join(ROOT, "google", f"{NAME}_SEND_THIS.zip")
    if os.path.exists(z):
        os.remove(z)
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for d, _, fs in os.walk(KIT):
            for fn in sorted(fs):
                p = os.path.join(d, fn)
                zf.write(p, os.path.join(NAME, os.path.relpath(p, KIT)))
    return z


if __name__ == "__main__":
    build()
    print("built", KIT)
