# Writes meta_kit_c1/C1_meta_upload_sheet.csv: one row per ad, every field Ads Manager asks for.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "meta_kit_c1")
CAMP = "TL_C1_ProvenReaders_24-26Oct_Sales"
SETS = {"A": ("C1A_UnusedLLB_IN_23-45", "India", "23 to 45"),
        "B": ("C1B_CareerBreak_IN_25-50", "India", "25 to 50"),
        "B2": ("C1B2_Abroad_7geo_25-50", "India, UAE, Saudi Arabia, Qatar, Singapore, UK, US, Canada", "25 to 50")}
ADS = [  # nn, ad set, short name, hook, supporting copy (user's script), headline (user's CTA line)
 ("01", "A", "HR", "You used to hire the talent for firms. Now become the legal brains that advise them.",
  "Use your LLB to explore tech law, employment contracts and workplace compliance.", "Join the Tech Law Bootcamp for ₹10"),
 ("02", "A", "Banking", "You already know how money moves. Now learn the law that drives fintech.",
  "Use your LLB to explore fintech regulations, financial contracts, payments, compliance and technology law.", "Join the Tech Law Bootcamp for ₹10"),
 ("03", "A", "Content", "You used to write the content. Now learn to draft the contracts as well.",
  "Use your LLB to build practical skills in software agreements, privacy policies and tech law documents.", "Join the Tech Law Bootcamp for ₹10"),
 ("04", "A", "SalesOps", "You know how business works. Now become the legal brain behind the deal.",
  "Use your degree to explore commercial contracts, software agreements and compliance.", "Join the Tech Law Bootcamp for ₹10"),
 ("08", "A", "BPO", "Hello... your LLB is calling back. Let's get ready for the legal role you planned for.",
  "Use your degree to learn practical contract drafting, privacy and technology law skills.", "Give your LLB a new direction. Join for ₹10"),
 ("05", "B", "PausedPractice", "You took a break from practice. Not from being a lawyer. Let's restart.",
  "Use your degree to rebuild practical legal skills in contracts, privacy and technology law.", "Take your next step. Join for ₹10"),
 ("06", "B", "MovedCity", "New city. New chapter. Your LLB still comes with you. Let's make use of it.",
  "Explore practical tech law skills that can open up new directions for your legal career.", "Put your degree to work. Join for ₹10"),
 ("09", "B", "WomenReturning", "Your career took a break. Time to come back with a more flexible legal route.",
  "Refresh your legal skills and explore contracts, privacy and tech law, live from home.", "Start your next chapter. Join for ₹10"),
 ("10", "B", "LeftFirm", "You left the firm. You didn't leave your legal potential. Let's get back.",
  "Use your degree to explore practical tech law work, from drafting software contracts to reviewing privacy policies.", "Explore a new direction. Join for ₹10"),
 ("07", "B2", "Abroad", "You moved countries. Don't leave your legal ambitions behind.",
  "Use your Indian law degree to explore tech law skills and the opportunities open to you.", "Start exploring. Join for ₹10"),
]
TAIL = ("Tech law is the legal work tech companies need: contracts, privacy, compliance and disputes.\n\n"
        "In 3 live evenings you draft a software development agreement with us, see six ways tech companies make money, and review a startup's terms.\n\n"
        "Sat 24 and Sun 25 Oct, 6 to 9 PM IST. Mon 26 Oct, 7 to 10 PM IST.\nRs 10 incl. GST. Refundable. Live only, no recordings.")
rows = []
for nn, s, short, hook, sup, head in ADS:
    slug = "tlc1-%s" % nn
    url = "https://growthx.lawsikho.com/f/%s?utm_source=meta&utm_medium=paid_social&utm_campaign=tl_c1_proven_readers&utm_content=%s_%s" % (slug, slug, short.lower())
    text = "%s\n\n%s\n\n%s" % (hook, sup, TAIL)
    assert "—" not in text + head and "–" not in text + head
    rows.append({"Campaign": CAMP, "Ad set": SETS[s][0], "Locations": SETS[s][1], "Age": SETS[s][2],
                 "Ad name": "C1_%s_%s" % (nn, short), "Image 9:16 (Stories, Reels)": "9x16/TL_C1_%s_9x16.jpg" % nn,
                 "Image 4:5 (Feed)": "4x5/TL_C1_%s_4x5.jpg" % nn, "Primary text": text, "Headline": head,
                 "Description": "3 live evenings, 24 to 26 Oct. Refundable.", "Call to action": "Sign up",
                 "Website URL": url, "Landing page file": "landing_pages_c1/lp_%s.html" % slug, "GrowthX funnel slug": slug})
with open(os.path.join(OUT, "C1_meta_upload_sheet.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "rows; longest primary text", max(len(r["Primary text"]) for r in rows), "chars")
