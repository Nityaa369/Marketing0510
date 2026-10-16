# Preflight for the wave: dashes, banned claims, income on faces, sentence length, page words,
# and sentence overlap between pages (block at 80%, the account's rule 4b). Run: python3 preflight.py
import os, re, sys, glob, json, itertools, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wave as W
HERE = os.path.dirname(os.path.abspath(__file__))
BANNED = [r"weeks away", r"free for all safe harbour", r"5,000 GCC", r"first legal tech unicorn", r"rewrote", r"burger",
          r"Upwork was free", r"guarantee", r"\$\s?\d", r"USD\s?\d", r"lakh a month", r"LPA", r"not for you if", r"will get you"]
fail = []
def text_of(p):
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"</?(h[1-6]|b|p|li|td|th|tr|div|section|summary|details|button|a)\b[^>]*>", " . ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t))
FACE_NUM = r"(Rs|INR|\u20b9|\$|USD)\s?\d[\d,]*(?<!10)\b|\d+\s?(lakh|LPA|%)|\d+\+?\s?(years?|yrs)\s?(of\s)?(experience|practice|PQE|standing)|\d+\+\s?years?"
for a in W.ADS:
    face = " ".join([a["callout"], a["head"], a["why"]])
    if re.search(FACE_NUM, face, re.I): fail.append("face number %s: %s" % (a["id"], face))
pages = sorted(glob.glob(os.path.join(HERE, "landing_pages", "*.html")))
sents = {}
for p in pages:
    t = text_of(p); n = len([w for w in t.split() if w != "."])
    if "—" in t or "–" in t: fail.append("dash " + os.path.basename(p))
    for b in BANNED:
        if re.search(b, t, re.I) and not (b == "guarantee" and "does not promise" in t): fail.append("banned '%s' in %s" % (b, os.path.basename(p)))
    long = [s for s in re.split(r"(?<=[.?!])\s", t) if len(s.split()) > 34]
    if long: fail.append("%s: %d sentences over 34 words" % (os.path.basename(p), len(long)))
    sents[os.path.basename(p)] = set(s.strip().lower() for s in re.split(r"(?<=[.?!])\s", t) if len(s.split()) > 4)
    print("%-26s %5d words" % (os.path.basename(p), n))
worst = 0; pairs = []
for x, y in itertools.combinations([k for k in sents if not re.search(r"-5[1-9]-|-60-", k)], 2):
    o = len(sents[x] & sents[y]) / max(1, min(len(sents[x]), len(sents[y])))
    worst = max(worst, o); pairs.append((o, x, y))
    if o >= 0.8: fail.append("overlap %.0f%% %s %s" % (o * 100, x, y))
for o, x, y in sorted(pairs, reverse=True)[:5]: print("  overlap %.0f%% %s %s" % (o * 100, x, y))
print("max sentence overlap between full pages: %.0f%%" % (worst * 100))
print("FINDINGS" if fail else "PASS"); [print(" -", f) for f in fail]
