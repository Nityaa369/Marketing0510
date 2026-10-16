#!/usr/bin/env python3
"""
policy_scan.py - Flag Google Ads policy risks in ad copy BEFORE rendering.

Usage:
  python3 policy_scan.py content.json            # scan every text field in the content JSON
  python3 policy_scan.py --ocr SRC_FOLDER        # OCR the original ads (needs tesseract) to audit the source
  python3 policy_scan.py --text "any line here"  # scan one line

Exit code 1 if any BLOCK-level hit is found. Every hit prints the rule, the matched text
and the fix pattern to use. A clean scan is necessary, not sufficient: still do the manual
checklist in references/google_ads_policy_checklist.md (layout risks cannot be found by text).
"""
import json, os, re, subprocess, sys

# (level, rule, regex, fix)
RULES = [
 # Money / income claims (Financial claims, Misrepresentation, user rule: no money symbols or paid/earn wording)
 ("BLOCK", "Money claim: earn/earning", r"\bearn(s|ed|ing)?\b", "Replace with the skill or the work: 'draft contracts for startups', 'build deal work'."),
 ("BLOCK", "Money claim: paid/pays/pay you", r"\b(paid|pays|pay you|get paid|pays better|well[- ]paid|paying)\b", "Remove. Say what the person does, not what they are paid."),
 ("BLOCK", "Money claim: salary/income/side income", r"\b(salary|salaries|income|side income|per month|a month|lakh a|LPA|CTC)\b", "Remove figures and pay wording from the ad face."),
 ("BLOCK", "Money figure ($)", r"\$\s?\d|\bUSD\b|\bdollars?\b", "Remove. Keep non-money facts (counts, percentages of people, years)."),
 ("BLOCK", "Money figure (₹ amount other than the course price)", r"₹\s?(?!10\b)[\d,.]+\s*(lakh|crore|cr|k)?", "Remove. Only the bootcamp price (for example ₹10) may appear."),
 ("BLOCK", "Money figure (crore/lakh/billion)", r"\b\d[\d,.]*\s*(lakh|crore|billion|million|bn)\b", "Remove or turn into a non-money fact."),
 # Misleading ad design / clickbait
 ("BLOCK", "Arrow on CTA (Misleading ad design)", r"[→➜➔➝⇒>]{1}\s*$|→|➜|➔", "Remove every arrow. CTA is plain text on the band."),
 ("BLOCK", "Fake UI words (dialog/notification)", r"\b(Accept|Decline|Incoming call|AirDrop|is calling|Allow|Dismiss|OK button|notification)\b", "Never imitate a phone/OS dialog. Keep the idea as a headline only."),
 ("WARN",  "Button-like CTA text in caps", r"\b(JOIN NOW|CLICK HERE|REGISTER NOW|KNOW MORE|BOOK NOW)\b", "Sentence case, plain text on the band, no pill or button shape."),
 ("WARN",  "Official-notice framing", r"\b(NOTICE|are requested to note|official|circular)\b", "Remove notice/government look."),
 # Dishonest behaviour (academic)
 ("BLOCK", "Enabling dishonest behaviour (ghostwriting)", r"\b(writing the review itself|write (their|the|your client'?s?) (thesis|dissertation|assignment|review|paper)|ghost ?writ\w*|bought per submission|per submission|writing (and|&) editing gigs|gigs|examining theses|methods sections|writing up finished results|journal submission packages|grant applications)\b",
  "Reframe as credited work in the person's own name: 'systematic reviews as a named co-author', 'grant proposals as a named co-investigator', 'study design consulting'. Add 'Your name stays on your work'."),
 # Sensitive categories for personalised ads
 ("BLOCK", "Crime / criminal record (personalised ads limited)", r"\b(criminal|crime|crimes|IPC|Criminal Code|convict\w*|accused|bail)\b", "Reframe the audience: 'trial court litigators', 'litigators'. Compare 'trial practice', not 'Criminal Code/IPC'."),
 ("BLOCK", "Age targeting text", r"\b\d\d\s?\+|\bin their (30|40|50|60)s\b|\b[3-7]0s\b|\baged \d+|\bover (40|45|50|55|60)\b", "Use experience: 'senior lawyers with decades of practice'."),
 ("WARN",  "Personal hardship / health / finance state", r"\b(debt|broke|jobless|unemployed|divorced|pregnan\w*|disab\w*|illness)\b", "Do not imply you know a personal hardship. Describe the role or situation neutrally."),
 # Government documents and official services
 ("BLOCK", "Government documents / immigration service look", r"\b(NRI (files|cases)|visa (help|service|filing)|immigration (service|filing|help)|passport|PR file|OCI|apostille|document service|become eligible|get licensed|be licensed|guaranteed licen\w*)\b",
  "State it is legal education for professionals. Use 'work toward the Canadian bar'. Add 'A legal education programme, not an immigration, visa or document service' when the topic is near immigration/NRI."),
 # Unverifiable / predictions / guarantees
 ("BLOCK", "Future-year prediction", r"\b(20(2[7-9]|3\d))\b|\b(will be|is going to|expected (in|to)|next year|best year)\b", "Remove predictions and future dates. Say what is true now."),
 ("BLOCK", "Guarantee / outcome promise", r"\b(guarantee\w*|assured|100% (job|placement)|placement|land(s)? a job|get(s)? you (work|a job|clients)|in \d+ months)\b", "Use 'a plan to', 'learn how to'. No job, client or result promises."),
 ("WARN",  "Superlative / unverifiable claim", r"\b(#1|number one|best|only|top|leading|most|desperately|record)\b", "Keep only if it is a quote line with no factual claim (for example 'the only call for your comeback'); otherwise remove."),
 ("WARN",  "Learner result stats / testimonials", r"\b(our learners|already did|cleared NCA|\d+ (learners|students) (cleared|got|landed))\b", "Remove learner result numbers and named people from the ad face."),
 # Trademarks
 ("BLOCK", "Third-party trademark", r"\b(Zoom|Slack|Upwork|Fiverr|LinkedIn|WhatsApp|Google Meet|Clio|ChatGPT|Big 4 firm names|Deloitte|KPMG|EY|PwC)\b", "Use generic words: 'live online', 'your chats', 'freelance profile'. (Source lines in tiny print may cite publishers.)"),
 # Style / user rules
 ("WARN",  "ALL CAPS word (capitalisation)", r"\b[A-Z]{4,}\b", "Sentence case everywhere. Acronyms like NCA, LLB, DPDP, IST, GST, CFA are fine."),
 ("WARN",  "Em or en dash (house rule)", r"[–—]", "Use 'to', a comma or a full stop instead."),
]
ACRONYMS = {"NCA", "LLB", "LLM", "DPDP", "IST", "GST", "CFA", "MBA", "NBFC", "MSME", "MSMES", "SEBI", "NSE", "SME", "IPO", "IPOS", "UPSC", "NABH", "KYC", "HNI", "UAE", "NRI", "CMA", "TMT", "IELTS", "UTC", "DMCA", "SAFE", "PhD", "IIM", "NLU", "BFSI", "HR", "CEO", "USA", "IIT", "ICAI", "SSC", "CGTMSE", "SIDBI", "PMEGP", "MUDRA", "NGO", "SQE", "SRA", "LSAT", "PDF", "JPG", "CTA", "ICP", "OKLAB"}

def scan_text(t, where=""):
    hits = []
    for level, rule, rx, fix in RULES:
        for m in re.finditer(rx, t, flags=0 if "ALL CAPS" in rule else re.I):
            s = m.group(0)
            if "ALL CAPS" in rule and s.upper() in ACRONYMS: continue
            ctx = t[max(0, m.start() - 12):m.end() + 12].lower()
            if "income" in rule and "not an income promise" in ctx: continue
            if "Superlative" in rule and ("live only" in ctx or "only for" in ctx): continue
            if "₹" in rule and re.search(r"incl\.?\s*GST", t[m.end():m.end() + 14] or "", re.I): continue
            hits.append((level, rule, s, fix, where, t))
    return hits

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.startswith("_") or k in ("folder", "slug", "photo", "path", "accent", "template", "type", "headline_font"): continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

def report(hits):
    blocks = [h for h in hits if h[0] == "BLOCK"]
    for level, rule, s, fix, where, t in hits:
        print(f"[{level}] {rule}\n   at {where}: \"{t[:120]}\"\n   matched: {s!r}\n   fix: {fix}\n")
    print(f"{len(blocks)} BLOCK, {len(hits) - len(blocks)} WARN")
    return 1 if blocks else 0

def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    if sys.argv[1] == "--text": sys.exit(report(scan_text(" ".join(sys.argv[2:]), "text")))
    if sys.argv[1] == "--ocr":
        hits = []
        for root, _, files in os.walk(sys.argv[2]):
            for f in sorted(files):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) and "/ads" in root.replace("\\", "/") + "/":
                    txt = subprocess.run(["tesseract", os.path.join(root, f), "-"], capture_output=True, text=True).stdout
                    for line in filter(str.strip, txt.splitlines()): hits += scan_text(line, f)
        sys.exit(report(hits))
    cfg = json.load(open(sys.argv[1])); hits = []
    for where, t in walk(cfg): hits += scan_text(t, where)
    sys.exit(report(hits))

if __name__ == "__main__":
    main()
