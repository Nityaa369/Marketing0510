#!/usr/bin/env python3
"""Trust-claim guard for ad copy & landing pages. Keeps credential claims accurate & consistent.
ALSO: negative-sell guard — flags discouragement sermons in money copy ("nobody walks out…",
"don't expect…", "starts modest"). LP money sections must be an upside ladder of verified rates
plus ONE short results-vary line (Ramanuj, 18 Jul 2026). These are scan-only (no --fix).
APPROVED (the ONLY allowed phrasing):
  - NSE Emerge-listed        (NEVER bare "NSE Listed"/"NSE-listed" — implies main board. Entity: Addictive Learning Technology Ltd, NSE SME/Emerge.)
  - Recognised NSDC Training Partner
  - IIT Roorkee iHUB Training Partner   (the iHUB, not "IIT Roorkee"; correct order "IIT Roorkee iHUB")
BRAND — by product line, NOT global:
  - SkillArbitrage products (HR, US accounting, women, ACW, skilling) -> brand "SkillArbitrage"; "by LawSikho" is a violation
  - LawSikho products (lawyer camps, IP law, patent, judiciary, USCL, litigation, CA Bar/SQE) -> "by LawSikho" is CORRECT; "by SkillArbitrage" is the violation
Usage:  python3 check_claims.py [files or globs...]          -> scan + report violations (exit 1 if any)
        python3 check_claims.py --fix [files or globs...]    -> auto-fix the files, then report
        python3 check_claims.py ads/ip_law_wave3_jul13/*.md  -> check a kit's copy
        (no file args -> legacy women-bootcamp TARGETS)
  --brand skillarbitrage|lawsikho|auto   default auto: inferred per file from path keywords
                                         (see LAWSIKHO_HINTS below); unknown paths -> skillarbitrage.
                                         Pass --brand explicitly if the kit folder name is ambiguous.
"""
import re, sys, os, glob
HOME=os.path.expanduser("~")
W=os.path.join(HOME,"ads and landing pages","women-remote-work")
K=os.path.join(HOME,"ad-monitor-deploy","ads","women_ai_kit_jul4")
TARGETS=[os.path.join(W,"landing-page-"+d,"index.html") for d in
         ["icp1-career-restarter","icp2-small-town","icp3-zero-to-one","icp4-single-mother","icp5-failed-home-biz","skeptic","retargeting"]]
TARGETS+=[os.path.join(W,"ad-creatives-all-icps.md"),
          os.path.join(K,"lp_dc01_earn_without_leaving_family.html"),
          os.path.join(K,"lp_dc01_earn_without_leaving_family_v2.html"),
          os.path.join(K,"lp_8steps_remote_job.html")]

# brand auto-detection from path keywords (product line, per global CLAUDE.md rule)
LAWSIKHO_HINTS=("lawsikho","ip_law","iplaw","patent","judiciary","uscl","litigation","lawyer",
                "sqe","ca_bar","cabar","arbitration","contract_drafting","legal_ai","legalai")
def infer_brand(path):
    p=path.lower()
    return "lawsikho" if any(h in p for h in LAWSIKHO_HINTS) else "skillarbitrage"

# exact special-case (band/chip) fixes run FIRST
EXACT=[
 ('<div class="trust-item">&#127891; NSE Listed</div>\n    <div class="trust-item">&#127891; NSDC Partner</div>\n    <div class="trust-item">&#127891; IHUB IIT Roorkee</div>',
  '<div class="trust-item">&#127891; NSE Emerge-listed</div>\n    <div class="trust-item">&#127891; Recognised NSDC Training Partner</div>\n    <div class="trust-item">&#127891; IIT Roorkee iHUB Training Partner</div>'),
 ('<div class="stat"><span class="n">NSE&nbsp;Listed</span><span class="l">NSDC &middot; IHUB IIT Roorkee</span></div>',
  '<div class="stat"><span class="n" style="font-size:18px">NSE Emerge-listed</span><span class="l">Recognised NSDC &amp; IIT Roorkee iHUB Training Partner</span></div>'),
 ('<div><span class="n">NSE&nbsp;Listed</span><span class="l">NSDC &middot; IHUB IIT Roorkee</span></div>',
  '<div><span class="n" style="font-size:18px">NSE Emerge-listed</span><span class="l">Recognised NSDC &amp; IIT Roorkee iHUB Training Partner</span></div>'),
]
# ordered regex rules (accuracy normalizations, safe in chip + prose)
def fix_text(t,brand):
    for a,b in EXACT: t=t.replace(a,b)
    if brand=="skillarbitrage":
        t=re.sub(r'backed by LawSikho \(NSE Emerge-listed\)','backed by an NSE Emerge-listed company',t,flags=re.I)
        t=re.sub(r'By SkillArbitrage \(NSE Emerge-Listed\)','NSE Emerge-listed',t)
        t=re.sub(r'by LawSikho','by SkillArbitrage',t,flags=re.I)           # brand rule (SkillArbitrage products)
    else:
        t=re.sub(r'by SkillArbitrage','by LawSikho',t,flags=re.I)          # brand rule (LawSikho products)
    t=re.sub(r'NSE[\s ]+Emerge[\s \-]+Listed','NSE Emerge-listed',t,flags=re.I)  # normalise emerge variants
    t=re.sub(r'NSE[\s \-]+listed','NSE Emerge-listed',t,flags=re.I)   # bare NSE listed -> Emerge (emerge ones already normalised, won't match)
    t=re.sub(r'IHUB[\s ]+IIT[\s ]+Roorkee','IIT Roorkee iHUB',t,flags=re.I)       # correct name/order
    t=t.replace('IIT Roorkee iHUB Partner','IIT Roorkee iHUB Training Partner')             # chip suffix (only where 'Partner' followed)
    t=re.sub(r'(?<!Recognised )NSDC Training Partner','Recognised NSDC Training Partner',t) # ensure Recognised prefix
    t=re.sub(r'\bNSDC Partner\b','Recognised NSDC Training Partner',t)
    return t

# violation scanners (run in scan mode); brand-neutral claims first
BANNED=[
 # Proof-name ban (13 Aug 2026): Sandya Advani appeared on a senior-AI LP draft and NOTHING
 # mechanical caught it — the rule lived only in memory (approved proof: Garima Pandey,
 # Amaresh Kumar). check_claims runs on both ads and LPs, so the ban lives here.
 (re.compile(r'sandya\s+advani',re.I), 'Sandya Advani as proof (banned — use Garima Pandey / Amaresh Kumar)'),
 (re.compile(r'NSE(?![\s ]?Emerge)[\s \-]+listed',re.I), 'bare "NSE listed" (must be "NSE Emerge-listed")'),
 (re.compile(r'\bNSDC Partner\b'),                                  '"NSDC Partner" (must be "Recognised NSDC Training Partner")'),
 (re.compile(r'IHUB[\s ]+IIT[\s ]+Roorkee',re.I),         '"IHUB IIT Roorkee" (must be "IIT Roorkee iHUB Training Partner")'),
]
# NEGATIVE-SELL guard (Ramanuj, 18 Jul 2026: hedge sermons rejected — money copy = upside ladder of
# verified rates + ONE short results-vary line; see memory feedback_lp_money_section_upside_ladder).
# Scan-only, no auto-fix: the rewrite needs the product's pay-research figures, not a substitution.
_NS='discouragement/negative-sell (money copy = upside ladder + one hedge line, never a sermon)'
BANNED+=[(re.compile(p,re.I),_NS) for p in [
 r"\b(nobody|no one|no-one) walks out\b",
 r"anyone who tells you otherwise",
 r"is selling (you )?something",
 r"let['’]?s be honest about (the )?money",
 r"because most pages (here )?aren['’]?t",
 r"\bstarts? modest\b",
 r"pay like first work anywhere",
 r"\bdon['’]?t expect\b",
 r"won['’]?t (get|make you) rich",
 r"\bnot get rich\b",
 r"\bget.rich.quick\b",
 r"\bno promises\b",
 r"\bwe can['’]?t promise\b",
]]
# SELF-SABOTAGE guard (Ramanuj, 9 Aug 2026: "please stop sneaking in shit that reduce conversion").
# Origin: a landing page for the content bootcamp shipped the line "this camp has not run yet, so
# there are no student results to show you and we are not going to invent any" — on a product with
# ELEVEN prior cohorts. It was both false and a volunteered negative. The wider pattern is
# honesty-flavoured hedging that reads as integrity and costs conversion: announcing what the buyer
# does NOT get, disclaiming proof, or pre-empting objections nobody raised.
# Rule: state what the buyer GETS. Compliance needs ONE short results-vary line, not a sermon.
# See [[feedback_conversion_first_filter]] and [[feedback_no_anti_promise_framing]].
_SS='self-sabotage (volunteered negative — say what the buyer GETS, never what they do not)'
BANNED+=[(re.compile(p,re.I),_SS) for p in [
 r"\b(has|have|had) not run yet\b",
 r"\bno (student|learner|cohort) results\b",
 r"\bnot going to invent\b",
 r"\bwe are not able to\b",
 r"\bthere are no results\b",
 r"\bno certificate\b",
 r"\bneither of those is what\b",
 r"\bnobody masters\b",
 r"\byou (probably )?will not (finish|master)\b",
 r"\bthis is not for\b",
 r"\bdo not expect to\b",
 r"\bunproven\b",
]]
BRAND_BANNED={
 "skillarbitrage":[(re.compile(r'by LawSikho',re.I), '"by LawSikho" (SkillArbitrage product — brand SkillArbitrage only)')],
 "lawsikho":      [(re.compile(r'by SkillArbitrage',re.I), '"by SkillArbitrage" (LawSikho product — brand LawSikho only)')],
}
def scan(t,brand):
    out=[]
    for rx,msg in BANNED+BRAND_BANNED[brand]:
        for m in rx.finditer(t):
            ln=t[:m.start()].count("\n")+1
            out.append((ln,msg,m.group(0)))
    return out

argv=sys.argv[1:]
fix=("--fix" in argv); argv=[a for a in argv if a!="--fix"]
brand_opt="auto"
if "--brand" in argv:
    i=argv.index("--brand")
    if i+1>=len(argv) or argv[i+1].lower() not in ("skillarbitrage","lawsikho","auto"):
        print("--brand needs skillarbitrage | lawsikho | auto"); sys.exit(2)
    brand_opt=argv[i+1].lower(); del argv[i:i+2]
unknown=[a for a in argv if a.startswith("-")]
if unknown: print("unknown flag(s):",*unknown,"\n"+__doc__); sys.exit(2)
files=[]
for a in argv:  # shell usually expands globs; glob here covers quoted patterns
    hits=sorted(glob.glob(a,recursive=True))
    files+=hits if hits else [a]   # keep literal so MISSING is reported
targets=files or TARGETS

total_v=0
for f in targets:
    brand=infer_brand(f) if brand_opt=="auto" else brand_opt
    if not os.path.exists(f): print("  MISSING:",f); continue
    t=open(f,encoding="utf-8").read()
    if fix:
        nt=fix_text(t,brand)
        if nt!=t: open(f,"w",encoding="utf-8").write(nt)
    t=open(f,encoding="utf-8").read()
    v=scan(t,brand); total_v+=len(v)
    name=f.replace(W+"/","").replace(K+"/","KIT/")
    if os.path.isabs(name):
        rel=os.path.relpath(name)
        if not rel.startswith(".."): name=rel
    tag="LS" if brand=="lawsikho" else "SA"
    if v:
        print(f"✗ [{tag}] {name}")
        for ln,msg,txt in v[:8]: print(f"    L{ln}: {msg}  ->  '{txt}'")
    else:
        print(f"✓ [{tag}] {name}")
print(f"\n{'FIXED + ' if fix else ''}{total_v} violation(s) remaining.")
sys.exit(1 if total_v else 0)
