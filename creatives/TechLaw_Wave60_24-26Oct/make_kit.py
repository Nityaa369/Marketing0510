# Writes ad_copy.md, manifest.json and kit_meta.json from wave.py. Run: python3 make_kit.py
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave as W
from render import stem
HERE = os.path.dirname(os.path.abspath(__file__))
RISK = {
 "06": "Third-person opener ('For lawyers...') on purpose, for Meta's personal-attributes policy. Same for all career-break and between-jobs ads.",
 "09": "Targets Indian lawyers abroad: set location to India plus UAE, Saudi Arabia, Qatar, Singapore, UK, US, Canada. Camp times are IST.",
 "25": "Judiciary aspirants are law graduates; Ramanuj may treat them as non-practising. Confirm.",
 "29": "Final-year law students: Ramanuj must confirm whether students count as lawyers for Tech Law (24 Sep rule).",
 "38": "Sensitive life situation: third-person opener kept.",
 "39": "Senior advocates: years of practice go in targeting (age 40+), never on the face (ID '15+ years' ran 1.90x).",
 "48": "No age on the face. Experience is in targeting.",
 "55": "Payment help line names webinars@lawsikho.in (the script's bootcamp contact). Confirm it handles payment queries.",
}
lines = ["# Tech Law wave 60 · 24 to 26 Oct 2026 · LawSikho · ad copy", "",
 "Status: DRAFT for Ramanuj, not approved. Lawyers only. One reader and one message per ad. No income figure on any face.",
 "Rs 10 incl. GST, refundable, live only. Sat and Sun 6 to 9 PM IST, Mon 7 to 10 PM IST. Rebuild faces: `python3 render.py`; pages: `python3 build_lps.py`.", ""]
man = []
for c, cd in W.CAMPAIGNS.items():
    lines += ["## %s · %s · %s" % (c, cd["name"], cd["stage"]), "", cd["job"], ""]
    for a in [x for x in W.ADS if x["camp"] == c]:
        s = W.slug(a)
        lines += ["### %s · %s" % (a["id"], stem(a)),
                  "- **Ad set:** %s_%s" % (cd["name"], a["adset"]),
                  "- **Reader (targeting note):** %s" % a["reader"],
                  "- **Format:** %s" % a["fmt"],
                  "- **Face:** %s / %s / %s" % (a["callout"], a["head"], a["why"]),
                  "- **Meta headline:** %s" % a["mh"],
                  "- **Primary text:** %s" % W.primary_text(a),
                  "- **CTA button:** %s" % ("Learn more" if a["adset"] == "B_Turn_Up_Live" else "Sign up"),
                  "- **Landing page:** landing_pages/lp_%s.html · funnel slug `%s` · %s" % (s, s, W.FUNNEL % s)]
        if a["id"] in RISK: lines.append("- **Risk, recorded:** %s" % RISK[a["id"]])
        lines.append("")
        man.append(dict(id=a["id"], campaign=cd["name"], stage=cd["stage"], adset="%s_%s" % (cd["name"], a["adset"]),
                        reader=a["reader"], format=a["fmt"], image="ads/%s.png" % stem(a), landing_page="landing_pages/lp_%s.html" % s,
                        funnel_slug=s, meta_headline=a["mh"], primary_text=W.primary_text(a)))
open(os.path.join(HERE, "ad_copy.md"), "w").write("\n".join(lines))
json.dump(man, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
json.dump(dict(product="Tech Law Bootcamp", brand="LawSikho", camp="24 to 26 Oct 2026", price="Rs 10 incl. GST, refundable, live only",
               ads=60, campaigns=6, adsets=12, built="16 Oct 2026", status="DRAFT, no Ramanuj verdict"), open(os.path.join(HERE, "kit_meta.json"), "w"), indent=1)
print("ok", len(man))
