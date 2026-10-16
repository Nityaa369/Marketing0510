#!/usr/bin/env python3
"""Rebuild the C1 Tech Law landing pages (1 ad = 1 page).

Reads the reader-specific copy from original/lp_tlc1-NN.html, keeps every claim as written,
and re-renders it in the new layout with new components. Run from this folder:
    python3 build_lps_c1.py
Writes lp_tlc1-NN.html next to this script. Pictures stay in img/.
"""
import re, glob, os, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
BTN = "Join the 3 live evenings for Rs 10"

# Reader-specific pieces written for the new layout (From -> To strip, redline margin note,
# and the "you already have" line). Everything else is parsed from the original page.
READER = {
 "01": dict(frm="Forwards contracts to Legal", to="Drafts them for tech companies",
            note="You see this clause in every vendor deal. Here you write it from the seller's side."),
 "02": dict(frm="Knows how money moves", to="Drafts the contracts behind fintech",
            note="Payments and lending products hang on clauses like this. You already know what breaks."),
 "03": dict(frm="Writes the content", to="Drafts the agreements around it",
            note="Who owns the work is the question every creator deal turns on. You have lived it."),
 "04": dict(frm="Closes the deal", to="Drafts the contract behind it",
            note="You have chased sign-off on terms like these. Now you are the one who writes them."),
 "05": dict(frm="Paused practice to care for family", to="Drafts agreements in the hours you have",
            note="One clause, one sitting. This is work that fits a broken day."),
 "06": dict(frm="New city, practice on hold", to="Drafts for clients from any city",
            note="The client reads your draft, not your address. Courts are not needed for this."),
 "07": dict(frm="Indian LLB, living abroad", to="Drafts for startups from where you are",
            note="This work travels. A draft goes by email and shared document, in any time zone."),
 "08": dict(frm="Handles tickets and targets", to="Drafts the service terms behind them",
            note="You know what a support promise looks like in real life. Now you put it in writing."),
 "09": dict(frm="Career break", to="Back in legal work, task by task",
            note="Short, self-contained tasks like this one are how many people return."),
 "10": dict(frm="Left the firm for family", to="Drafts for startups, on your terms",
            note="You have drafted clauses like this before. The camp adds the tech vocabulary."),
}

CSS = r"""
:root{--ac:#13756B;--soft:#EAF5F2;--ink:#14171F;--mut:#4A5160;--line:#E3E6EC;--cta:#E11D2E;--cta2:#B91422}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);background:#fff;line-height:1.6;font-size:17px;-webkit-text-size-adjust:100%}
.w{max-width:680px;margin:0 auto;padding:0 20px}
.serif{font-family:Georgia,"Times New Roman",serif}
a{color:inherit}
/* top bar */
.top{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.96);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.top .w{display:flex;align-items:center;justify-content:space-between;height:52px}
.brand{font-family:Georgia,serif;font-size:24px;font-weight:700}
.cd{font-size:13px;font-weight:800;color:var(--ac);text-align:right;line-height:1.2}
.cd small{display:block;font-weight:600;color:var(--mut);font-size:11px}
/* fold */
.fold{background:linear-gradient(180deg,var(--soft) 0%,#fff 100%);padding:22px 0 26px}
.pill{display:inline-block;background:var(--ac);color:#fff;font-weight:800;font-size:13px;letter-spacing:.06em;text-transform:uppercase;padding:8px 13px;border-radius:999px}
.hook{font-family:Georgia,"Times New Roman",serif;font-size:36px;line-height:1.08;font-weight:700;margin-top:16px;letter-spacing:-.01em}
.hook span{display:block}
.sup{font-size:19px;font-weight:700;margin-top:14px;line-height:1.35}
.hero{position:relative;margin-top:18px}
.hero img{display:block;width:auto;max-width:100%;max-height:600px;margin:0 auto;border-radius:18px;box-shadow:0 10px 26px rgba(0,0,0,.16)}
.hero .tag{position:absolute;left:12px;bottom:12px;background:#fff;border-radius:12px;padding:8px 12px;font-size:13px;font-weight:800;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.hero .tag b{color:var(--ac)}
.ft{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:stretch;margin-top:16px}
.ft div{background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;font-size:14px;font-weight:700;line-height:1.3}
.ft div small{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin-bottom:3px}
.ft .to{border-color:var(--ac);background:var(--soft)}
.ft .to small{color:var(--ac)}
.ft i{display:flex;align-items:center;font-style:normal;font-weight:900;color:var(--ac);font-size:22px}
.def{background:#fff;border-left:6px solid var(--ac);border-radius:0 12px 12px 0;padding:12px 14px;margin-top:16px;font-weight:600;box-shadow:0 2px 10px rgba(0,0,0,.06)}
.q{font-weight:600;margin-top:16px;color:var(--mut);font-size:16px}
/* route */
.route{list-style:none;margin-top:18px;position:relative;padding-left:0}
.route li{position:relative;padding:0 0 14px 52px;font-weight:700}
.route li:before{content:"";position:absolute;left:17px;top:34px;bottom:0;width:2px;background:repeating-linear-gradient(var(--ac) 0 4px,transparent 4px 8px)}
.route li:last-child:before{display:none}
.route span{position:absolute;left:0;top:0;width:36px;height:36px;border-radius:50%;background:var(--ac);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900}
.route small{display:block;font-weight:700;color:var(--ac);font-size:12px;letter-spacing:.08em;text-transform:uppercase}
.price{display:flex;align-items:center;gap:14px;background:#fff;border:2px solid var(--ac);border-radius:16px;padding:12px 16px;margin-top:8px}
.price .big{white-space:nowrap;flex:0 0 auto;font-size:44px;font-weight:900;line-height:1;color:var(--ac)}
.price .big sub{display:block;font-size:13px;font-weight:700;color:var(--mut);vertical-align:baseline}
.price p{margin:0;font-weight:700;font-size:15px;line-height:1.35}
.btn{display:block;text-align:center;background:var(--cta);color:#fff;font-weight:900;font-size:19px;padding:17px 16px;border-radius:14px;text-decoration:none;margin-top:16px;box-shadow:0 8px 18px rgba(225,29,46,.32);transition:transform .15s,background .15s}
.btn:hover{background:var(--cta2);transform:translateY(-1px)}
.btn small{display:block;font-weight:600;font-size:13px;opacity:.92;margin-top:2px}
/* sections */
section{padding:34px 0;border-bottom:1px solid var(--line)}
.num{display:inline-block;font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:var(--ac);background:var(--soft);padding:4px 10px;border-radius:999px}
h2{font-size:26px;line-height:1.18;font-weight:900;margin:10px 0 12px;letter-spacing:-.005em}
h3{font-size:20px;line-height:1.2;font-weight:900;margin:22px 0 4px}
p{margin-top:12px}
.lede{font-family:Georgia,serif;font-size:21px;line-height:1.4;border-left:4px solid var(--ac);padding-left:14px;margin-top:14px}
.card{background:var(--soft);border-radius:14px;padding:14px 16px;margin-top:12px}
.card b{display:block;margin-bottom:2px}
.fail .card{background:#fff;border:1.5px solid var(--line);position:relative;padding-left:46px}
.fail .card:before{content:"\00D7";position:absolute;left:14px;top:10px;width:22px;height:22px;border-radius:50%;background:#F3D9DC;color:#B91422;font-weight:900;display:flex;align-items:center;justify-content:center;line-height:1}
.work p{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:14px 16px}
.work p:first-of-type{border-color:var(--ac)}
.terms3{display:grid;grid-template-columns:1fr;gap:10px;margin-top:12px}
.terms3 .card{margin:0;display:flex;gap:12px}
.terms3 .card em{font-style:normal;font-weight:900;color:var(--ac);min-width:96px}
/* redline mock */
.doc{background:#fff;border:1.5px solid #D4D8DF;border-radius:6px;box-shadow:0 8px 22px rgba(0,0,0,.1);margin-top:14px;font-family:Georgia,serif;font-size:15px;line-height:1.55;overflow:hidden}
.doc .hd{background:#F4F5F7;border-bottom:1px solid #D4D8DF;padding:8px 12px;font:700 12px system-ui,sans-serif;color:var(--mut);letter-spacing:.05em;text-transform:uppercase}
.doc .bd{padding:14px 14px 6px}
.doc .cl{margin-bottom:10px}
.doc mark{background:#FFF3B0;padding:0 2px}
.doc del{color:#B91422}
.doc ins{color:#0B6B3A;text-decoration:underline}
.doc .mg{margin:0 14px 14px;background:var(--soft);border-left:4px solid var(--ac);border-radius:0 8px 8px 0;padding:8px 10px;font:600 14px/1.4 system-ui,sans-serif}
.doc .mg b{color:var(--ac)}
/* terms grid */
.tg{display:grid;grid-template-columns:1fr;gap:10px;margin-top:12px}
.tg .card{margin:0}
@media(min-width:560px){.tg{grid-template-columns:1fr 1fr}.tg .card:last-child{grid-column:1/-1}}
/* days */
.day{border:1.5px solid var(--line);border-radius:16px;margin-top:12px;overflow:hidden}
.day .dh{background:var(--ac);color:#fff;padding:9px 14px;font-weight:800;font-size:14px;display:flex;justify-content:space-between;gap:8px}
.day .db{padding:12px 14px}
/* method + plan */
.steps{display:grid;grid-template-columns:1fr;gap:10px;margin-top:12px}
@media(min-width:560px){.steps{grid-template-columns:repeat(3,1fr)}}
.steps .card{margin:0}
.plan{list-style:none;margin-top:12px;counter-reset:p}
.plan li{counter-increment:p;position:relative;padding:12px 14px 12px 50px;margin-top:10px;border:1.5px solid var(--line);border-radius:14px}
.plan li:before{content:counter(p);position:absolute;left:12px;top:11px;width:28px;height:28px;border-radius:50%;background:var(--ac);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:14px}
/* proof */
.proof{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:14px;margin-top:12px}
.proof .av{flex:0 0 44px;height:44px;border-radius:50%;background:var(--ac);color:#fff;font-weight:900;display:flex;align-items:center;justify-content:center;font-size:17px}
.proof b{display:block}
/* stats */
.stats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.stat{background:var(--soft);border-radius:14px;padding:14px}
.stat .n{font-size:30px;font-weight:900;color:var(--ac);line-height:1.05}
.stat p{margin-top:6px;font-size:14px;line-height:1.4;font-weight:600}
.stat .src{display:block;margin-top:6px}
.src{font-size:12.5px;color:var(--mut);font-weight:500}
.cmp{display:grid;grid-template-columns:1fr;gap:10px;margin-top:14px}
@media(min-width:560px){.cmp{grid-template-columns:1fr 1fr 1.25fr}}
.cmp div{border:1.5px solid var(--line);border-radius:14px;padding:14px;font-size:15px}
.cmp div b{display:block;margin-bottom:4px}
.cmp .us{border:2.5px solid var(--ac);background:var(--soft);box-shadow:0 6px 16px rgba(0,0,0,.08)}
.cmp .us .rs{font-size:30px;font-weight:900;color:var(--ac);line-height:1.1}
/* faq */
details{border:1.5px solid var(--line);border-radius:14px;margin-top:10px;background:#fff}
summary{cursor:pointer;list-style:none;padding:14px 44px 14px 16px;font-weight:800;position:relative}
summary::-webkit-details-marker{display:none}
summary:after{content:"+";position:absolute;right:16px;top:10px;font-size:24px;font-weight:700;color:var(--ac)}
details[open] summary:after{content:"\2212"}
details[open]{border-color:var(--ac)}
details .a{padding:0 16px 14px;color:#2A2F3B}
/* close */
.close{background:linear-gradient(180deg,#fff,var(--soft));padding:38px 0;text-align:left}
.close h2{font-size:28px}
.disc{font-size:13px;color:#3F4552;padding:26px 0 100px}
.sticky{position:fixed;left:0;right:0;bottom:0;background:#fff;box-shadow:0 -4px 14px rgba(0,0,0,.14);padding:10px 16px;z-index:30;transform:translateY(110%);transition:transform .25s}
.sticky.on{transform:none}
.sticky .btn{margin:0;padding:13px;font-size:17px}
/* reveal */
.rv{opacity:0;transform:translateY(14px);transition:opacity .5s,transform .5s}
.rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}html{scroll-behavior:auto}.btn,.sticky{transition:none}}
@media(max-width:380px){.hook{font-size:31px}.ft{grid-template-columns:1fr}.ft i{justify-content:center;transform:rotate(90deg)}}
"""

JS = r"""
(function(){
var t=new Date('2026-10-24T18:00:00+05:30').getTime(),el=document.getElementById('cd');
function tick(){var d=t-Date.now();if(!el)return;if(d<=0){el.innerHTML='Live now<small>Sat 24 Oct, 6 PM IST</small>';return}
var D=Math.floor(d/864e5),h=Math.floor(d%864e5/36e5),m=Math.floor(d%36e5/6e4);
el.innerHTML='Starts in '+D+'d '+h+'h '+m+'m<small>Sat 24 Oct, 6 PM IST</small>'}
tick();setInterval(tick,30000);
var s=document.getElementById('sticky'),f=document.getElementById('fold');
function sc(){var r=f.getBoundingClientRect();s.classList.toggle('on',r.bottom<0)}
window.addEventListener('scroll',sc,{passive:true});sc();
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08}):null;
document.querySelectorAll('.rv').forEach(function(n){if(io)io.observe(n);else n.classList.add('in')});
})();
"""


def strip(s):
    return H.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def parse(path):
    s = open(path, encoding="utf-8").read()
    d = {}
    d["title"] = re.search(r"<title>(.*?)</title>", s).group(1)
    d["ac"], d["soft"] = re.search(r"--ac:(#\w+);--soft:(#\w+)", s).groups()
    d["pill"] = re.search(r'class="pill">(.*?)</div>', s).group(1)
    d["hook"] = re.search(r'class="hook">(.*?)</div>', s, re.S).group(1)
    d["sup"] = re.search(r'class="sup">(.*?)</div>', s).group(1)
    d["q"] = re.search(r'class="q">(.*?)</p>', s).group(1)
    d["def"] = re.search(r'class="def">(.*?)</div>', s).group(1)
    d["href"] = re.search(r'class="btn" href="([^"]+)"', s).group(1)
    d["img"] = re.search(r'<img class="hero" src="([^"]+)" alt="([^"]*)"', s).groups()
    secs = re.findall(r'<section><div class="w">(.*?)</div></section>', s, re.S)
    d["secs"] = secs
    d["close"] = re.search(r'<div class="close"><div class="w"><h2>(.*?)</h2><p>(.*?)</p>', s, re.S).groups()
    d["disc"] = re.search(r'<div class="disc"><div class="w"><p>(.*?)</p>', s, re.S).group(1)
    return d


def h2(sec):
    return re.search(r"<h2[^>]*>(.*?)</h2>", sec).group(1)


def paras(sec):
    return re.findall(r"<p>(.*?)</p>", sec, re.S)


def cards(sec):
    return re.findall(r'<div class="card"><b>(.*?)</b>(.*?)</div>', sec, re.S)


def btn(href, sub=""):
    return f'<a class="btn" href="{href}">{BTN}{sub}</a>'


WHY = {
 "01": "Employee records are personal data. Offer letters, HR policies and payroll vendor terms all sit inside this law, and you already know where they are.",
 "02": "Banks and fintechs hold more personal data than most. Consent notices and vendor contracts need drafting by someone who understands money products.",
 "03": "Every creator platform and media app collects user data. Privacy policies and brand-deal data clauses need someone who writes well and reads the law.",
 "04": "Every CRM, lead list and vendor deal runs on customer data. The contracts and compliance notes need someone who knows how the deal really runs.",
 "05": "This work arrives as documents: policies, notices, vendor terms. Documents can be drafted in the hours you actually have.",
 "06": "The clients are companies, not courts. A privacy document can be drafted from any city.",
 "07": "Indian companies need these documents, and so do foreign firms that serve users in India. The drafting can be done from where you live.",
 "08": "Outsourcers hold other companies' customer data. Processor terms and breach clauses are where your knowledge of the real workflow counts.",
 "09": "Short, self-contained documents such as privacy notices can be drafted one task at a time. Three live evenings show if it suits you.",
 "10": "You have drafted contracts before. Tech companies need privacy and vendor terms drafted, and you already read law closely.",
}

DYK = [
 ("India's data protection rules were notified on 14 Nov 2025, and most duties start 18 months later.",
  "Every business that holds customer or staff data needs privacy notices, consent wording and vendor terms written. Businesses are only starting to buy this work.",
  "DPDP Rules 2025, MeitY, notified 14 Nov 2025; PIB; Deccan Herald"),
 ("A record 55,200 startups were recognised in India in 2025-26.",
  "More than 2.23 lakh startups were recognised by 31 Mar 2026. Each one signs software, vendor and customer contracts, and most have no lawyer on staff.",
  "Inc42; Manorama Yearbook, Apr 2026"),
 ("India has 2,117 global capability centres, employing about 23.6 lakh people.",
  "These are the Indian offices of global companies. They run on data, software and outsourcing agreements, and they need people who can read those terms.",
  "Nasscom-Zinnov via Business Today, May 2026"),
 ("Tracxn tracks 1,215 legal tech startups in India.",
  "Legal tech companies need people who know both the law and the product. One of them, Harvey, hires Legal Engineers in Bengaluru who must be qualified Indian advocates.",
  "Tracxn, Sep 2026; harvey.ai, 2026"),
 ("India published its AI governance guidelines on 5 Nov 2025.",
  "They are not a new statute. They apply existing law, so AI companies need contracts and data terms that already comply with the law as it stands.",
  "MeitY, India AI Governance Guidelines, 5 Nov 2025"),
]

EXTRA_CSS = r"""
/* 3D layer */
body{overflow-x:clip}section{overflow-x:clip}
.p3{perspective:1100px}
.hero{perspective:1000px}
.hero .t3{transform-style:preserve-3d;transition:transform .25s ease-out;animation:fl 7s ease-in-out infinite;will-change:transform}
.hero .t3 img{box-shadow:0 28px 40px -18px rgba(0,0,0,.45),0 6px 14px rgba(0,0,0,.18)}
@keyframes fl{0%,100%{transform:rotateY(-5deg) rotateX(2deg)}50%{transform:rotateY(5deg) rotateX(-2deg)}}
.hero .t3.on{animation:none}
/* coin */
.price{perspective:600px}
.coin{flex:0 0 76px;height:76px;position:relative;transform-style:preserve-3d;animation:spin 6s linear infinite}
.coin b{position:absolute;inset:0;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;backface-visibility:hidden;border:4px solid #fff;box-shadow:0 0 0 3px var(--ac),0 8px 14px rgba(0,0,0,.25)}
.coin .f{background:radial-gradient(circle at 30% 25%,#fff7c9,#f1c24b 60%,#c8921a);color:#5a3a00;font-size:24px}
.coin .k{background:radial-gradient(circle at 30% 25%,#e9fff5,#7fd4b2 60%,#2c8f6a);color:#06402c;transform:rotateY(180deg);font-size:12px;line-height:1.1;padding:6px}
@keyframes spin{to{transform:rotateY(360deg)}}
.price .big{display:block;font-size:26px;line-height:1.1;color:var(--ac);font-weight:900;margin-bottom:4px}.price p{flex:1}
/* section number */
.num:before{content:counter(sec,decimal-leading-zero)}
body{counter-reset:sec}
section{counter-increment:sec}
.num{font-size:0}
.num:before{font-size:12px}
/* why now */
.why3{display:grid;gap:12px;margin-top:14px}
.dyk{perspective:900px;height:var(--h,236px);position:relative}
.dyk button{all:unset;display:block;width:100%;height:100%;cursor:pointer;position:relative;transform-style:preserve-3d;transition:transform .7s cubic-bezier(.2,.7,.2,1);border-radius:16px}
.dyk button:focus-visible{outline:3px solid var(--ac);outline-offset:3px}
.dyk.fl button{transform:rotateY(180deg)}
.dyk .fc{position:absolute;inset:0;border-radius:16px;padding:16px 16px 14px;backface-visibility:hidden;-webkit-backface-visibility:hidden;display:flex;flex-direction:column;box-shadow:0 14px 24px -12px rgba(0,0,0,.35)}
.dyk .fr{background:#fff;border:2px solid var(--ac)}
.dyk .bk{background:var(--ac);color:#fff;transform:rotateY(180deg)}
.dyk .q{font-size:12px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:var(--ac);margin:0}
.dyk .ft2{font-size:19px;line-height:1.28;font-weight:900;margin-top:8px}
.dyk .hint{margin-top:auto;font-size:13px;font-weight:800;color:var(--ac)}
.dyk .bk .q{color:#fff;opacity:.9}
.dyk .bk p{margin-top:8px;font-size:15.5px;line-height:1.45;font-weight:600}
.dyk .bk .src{color:#fff;opacity:.9;margin-top:auto;font-size:12.5px}
.dyk .you{background:#fff;color:var(--ink);border-radius:10px;padding:8px 10px;margin-top:8px;font-size:14.5px;line-height:1.4;font-weight:700}
.chain{margin-top:18px;transform-style:preserve-3d;transform:rotateX(10deg) rotateY(-8deg);transition:transform .4s;position:relative;padding-bottom:6px}
.chain .lv{position:relative;background:#fff;border:2px solid var(--ac);border-radius:14px;padding:12px 14px;margin-top:-6px;box-shadow:0 14px 18px -10px rgba(0,0,0,.35);font-weight:700;font-size:15px}
.chain .lv:nth-child(1){transform:translateZ(0);margin-left:0;margin-right:30px}
.chain .lv:nth-child(2){transform:translateZ(26px);margin-left:15px;margin-right:15px;background:var(--soft)}
.chain .lv:nth-child(3){transform:translateZ(52px);margin-left:30px;margin-right:0;background:var(--ac);color:#fff;border-color:var(--ac)}
.chain .lv small{display:block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:800;opacity:.8}
.chain:hover,.chain.on{transform:none}
/* five words: flip */
.tg .card.w{padding:0;background:none;perspective:700px;height:170px}
.tg .card.w button{all:unset;display:block;width:100%;height:100%;cursor:pointer;position:relative;transform-style:preserve-3d;transition:transform .6s;border-radius:14px}
.tg .card.w button:focus-visible{outline:3px solid var(--ac);outline-offset:2px}
.tg .card.w.fl button{transform:rotateY(180deg)}
.tg .card.w .a1,.tg .card.w .a2{position:absolute;inset:0;border-radius:14px;padding:14px 16px;backface-visibility:hidden;-webkit-backface-visibility:hidden;box-shadow:0 10px 18px -10px rgba(0,0,0,.3)}
.tg .card.w .a1{background:var(--soft);display:flex;flex-direction:column;justify-content:center;font-size:22px;font-weight:900}
.tg .card.w .a1 em{font-style:normal;font-size:13px;color:var(--ac);font-weight:800;margin-top:6px}
.tg .card.w .a2{background:#fff;border:2px solid var(--ac);transform:rotateY(180deg);font-size:14.5px;line-height:1.45;overflow:auto}
@media(min-width:560px){.tg .card.w{height:190px}}
/* contract 3d */
.stack{perspective:1000px;margin-top:14px}
.stack .t{transform-style:preserve-3d;transform:rotateX(6deg) rotateY(-7deg);transition:transform .35s;position:relative}
.stack .t:hover,.stack .t.on{transform:none}
.stack .t:before,.stack .t:after{content:"";position:absolute;inset:0;border-radius:6px;background:#fff;border:1.5px solid #D4D8DF;z-index:-1}
.stack .t:before{transform:translateZ(-14px) translate(8px,8px)}
.stack .t:after{transform:translateZ(-28px) translate(16px,16px);opacity:.8}
.stack .doc{margin-top:0}
/* tilt steps */
.route li{transition:transform .2s}
.cmp .us{transform:perspective(700px) rotateX(3deg) translateZ(0);}
@media(prefers-reduced-motion:reduce){.hero .t3,.coin{animation:none}.dyk button,.tg .card.w button{transition:none}.chain,.stack .t{transform:none}}
"""

EXTRA_JS = r"""
(function(){
document.querySelectorAll('.dyk button,.tg .card.w button').forEach(function(b){b.addEventListener('click',function(){var c=b.parentNode;c.classList.toggle('fl');b.setAttribute('aria-pressed',c.classList.contains('fl'))})});
var h=document.querySelector('.hero .t3');
if(h){var hr=h.parentNode;hr.addEventListener('pointermove',function(e){if(e.pointerType==='touch')return;var r=hr.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;h.classList.add('on');h.style.transform='rotateY('+(x*14)+'deg) rotateX('+(-y*10)+'deg)'});
hr.addEventListener('pointerleave',function(){h.classList.remove('on');h.style.transform=''})}
document.querySelectorAll('.chain,.stack .t').forEach(function(n){if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){n.classList.toggle('on',e.intersectionRatio>.6)})},{threshold:[0,.6]}).observe(n)}});
})();
"""

def build(n, d):
    r = READER[n]
    s = d["secs"]
    href = d["href"]
    img, alt = d["img"]
    out = []
    a = out.append
    def sec(title, extra=""):
        a(f'<section class="rv {extra}"><div class="w"><span class="num"></span><h2>{title}</h2>')
    def end():
        a('</div></section>')
    a(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      f'<title>{d["title"]}</title><meta name="description" content="3 live evenings, 24 to 26 Oct. Rs 10 incl. GST, refundable.">'
      f'<style>{CSS.replace("--ac:#13756B;--soft:#EAF5F2", "--ac:%s;--soft:%s" % (d["ac"], d["soft"]))}{EXTRA_CSS}</style></head><body>')
    a('<div class="top"><div class="w"><div class="brand">LawSikho</div><div class="cd" id="cd">Starts Sat 24 Oct<small>6 PM IST</small></div></div></div>')

    # FOLD: repeats the ad's promise in its words
    a('<div class="fold" id="fold"><div class="w">')
    a(f'<span class="pill">{d["pill"]}</span>')
    a(f'<div class="hook">{d["hook"]}</div>')
    a(f'<p class="sup">{d["sup"]}</p>')
    a(f'<div class="hero"><div class="t3"><img src="{img}" alt="{alt}"></div></div>')
    a(f'<div class="ft"><div><small>Today</small>{r["frm"]}</div><i>&rarr;</i><div class="to"><small>After the camp</small>{r["to"]}</div></div>')
    a(f'<div class="def">{d["def"]}</div>')
    a('<ol class="route">'
      '<li><span>1</span><small>Sat 24 Oct · 6 to 9 PM IST</small>Draft a software development agreement with us, clause by clause.</li>'
      '<li><span>2</span><small>Sun 25 Oct · 6 to 9 PM IST</small>See six ways tech companies make money, and the legal work each one creates.</li>'
      '<li><span>3</span><small>Mon 26 Oct · 7 to 10 PM IST</small>Review a startup\'s terms and learn how lawyers pitch the fix.</li></ol>')
    a('<div class="price"><div class="coin"><b class="f">Rs 10</b><b class="k">Refund-<br>able</b></div><p><span class="big">Rs 10 incl. GST</span>Refundable. Live only, no recordings. Joining details come on WhatsApp and email.</p></div>')
    a(btn(href, "<small>3 live evenings · 24 to 26 Oct</small>"))
    a(f'<p class="q">{d["q"]}</p>')
    a('</div></div>')

    # 1 Name the reader and the symptom
    p1 = paras(s[0])
    sec(h2(s[0]))
    a(f'<p class="lede">{p1[0]}</p>')
    for x in p1[1:]:
        a(f'<p>{x}</p>')
    end()

    # 2 Outcome: the new, better career
    sec(h2(s[1]))
    for x in paras(s[1]):
        a(f'<p>{x}</p>')
    a(btn(href))
    end()

    # 3 Three failed alternatives
    sec(h2(s[2]), "fail")
    for b, t in cards(s[2]):
        a(f'<div class="card"><b>{b}</b>{t}</div>')
    end()

    # 4 Reframe (positioning, not effort) and cost of staying unclear
    hs = re.findall(r"<h2[^>]*>(.*?)</h2>", s[3])
    ps4 = paras(s[3])
    sec(hs[0])
    for x in ps4[:-1]:
        a(f'<p>{x}</p>')
    a(f'<h3>{hs[1]}</h3><p>{ps4[-1]}</p>')
    end()

    # 5 Why now: what the market is like (sourced, framed as demand, no fear)
    sec("Why now: where tech law work is coming from")
    a('<p>Tech companies are being created, regulated and sold to faster than they can hire lawyers who understand them. Tap each card to see what it means for your work.</p>')
    a('<div class="why3">')
    for i, (fact, mean, src) in enumerate(DYK):
        you = WHY[n] if i == 0 else ""
        a(f'<div class="dyk" style="--h:{[380, 270, 290, 310, 290][i]}px"><button type="button" aria-pressed="false">'
          f'<span class="fc fr"><span class="q">Did you know?</span><span class="ft2">{fact}</span><span class="hint">Tap to see what it means for you &#8635;</span></span>'
          f'<span class="fc bk"><span class="q">What it means</span><p>{mean}</p>'
          + (f'<span class="you"><b>For you:</b> {you}</span>' if you else '')
          + f'<span class="src">Source: {src}.</span></span></button></div>')
    a('</div>')
    a('<h3>The chain of buyers</h3><p>Three kinds of buyer create the work, from the many small to the few large.</p>')
    a('<div class="chain"><div class="lv"><small>Layer 1 · many buyers</small>Startups: 2.23 lakh recognised by 31 Mar 2026. Contracts, terms, privacy notices.</div>'
      '<div class="lv"><small>Layer 2 · big employers</small>2,117 global capability centres. Vendor, data and outsourcing agreements.</div>'
      '<div class="lv"><small>Layer 3 · new buyers</small>1,215 legal tech startups and AI companies. Lawyers who know the product.</div></div>')
    a('<p class="src" style="margin-top:12px">These figures show where the work is. They are not a promise of any job or client.</p>')
    a(btn(href))
    end()

    # 6 What the work looks like for this reader
    sec(h2(s[4]), "work")
    for x in paras(s[4]):
        a(f'<p>{x}</p>')
    end()

    # 7 Offer and mechanism: three evenings and the method
    sec("What happens in the 3 live evenings")
    days = cards(s[6])
    for b, t in days[:3]:
        head, _, when = b.partition(" · ")
        a(f'<div class="day"><div class="dh"><span>{head}</span><span>{when}</span></div><div class="db">{t}</div></div>')
    a('<h3>The method we teach</h3><div class="steps">')
    for b, t in days[3:]:
        a(f'<div class="card"><b>{b}</b>{t}</div>')
    a('</div>')
    a(btn(href))
    end()

    # 8 Five words, as flip cards
    sec("Five words every tech contract uses")
    a('<p>On Evening 1 you learn the five concepts behind most technology contracts. None of them needs coding. Tap a card to turn it over.</p><div class="tg">')
    for b, t in cards(s[5]):
        a(f'<div class="card w"><button type="button" aria-pressed="false"><span class="a1">{b}<em>Tap to see the meaning</em></span><span class="a2">{t}</span></button></div>')
    a('</div>')
    end()

    # 9 First artifact: the document you draft
    p8 = paras(s[7])
    sec(h2(s[7]))
    a(f'<p>{p8[0]}</p>')
    a('<div class="stack"><div class="t"><div class="doc"><div class="hd">Illustration · software development agreement</div><div class="bd">'
      '<div class="cl"><b>9. Intellectual property.</b> 9.1 The Developer assigns to the Client <mark>all rights in the Deliverables</mark> '
      'on <del>delivery</del><ins>payment in full</ins>.</div>'
      '<div class="cl">9.2 The Developer keeps its <mark>pre-existing tools</mark> and grants the Client a licence to use them inside the Deliverables.</div></div>'
      f'<div class="mg"><b>Margin note:</b> {r["note"]}</div></div></div></div>')
    for x in p8[1:]:
        a(f'<p>{x}</p>')
    end()

    # 10 Plan after the camp
    sec("The plan after the camp, in plain steps")
    a('<ol class="plan">')
    for x in re.findall(r'<li[^>]*>(.*?)</li>', s[8], re.S):
        a(f'<li>{x}</li>')
    a('</ol><p>This is the plan taught on Evening 2. How far you get depends on the hours you put in.</p>')
    end()

    # 11 Proof
    sec("Lawyers who took this route")
    for b, t in cards(s[9]):
        ini = "".join(w[0] for w in strip(b).split()[:2])
        a(f'<div class="proof"><div class="av">{ini}</div><div><b>{b}</b>{t}</div></div>')
    end()

    # 12 Cost comparison and risk removal
    sec("What it costs to find out")
    a('<div class="cmp">'
      '<div><b>Figuring it out alone</b>Free, plus months of trial and error. Scattered articles and no feedback on your drafts.</div>'
      '<div><b>A long course first</b>A large fee, charged upfront. A commitment before you know if the work suits you.</div>'
      '<div class="us"><b>This bootcamp</b><span class="rs">Rs 10 incl. GST</span>Refundable. Three live evenings doing the work with us.</div></div>')
    a('<p><b>Risk removed.</b> The Rs 10 is refundable. Bring a laptop or phone and a notebook, and keep the three evenings free. Joining details arrive on WhatsApp and email.</p>')
    a(btn(href))
    end()

    # 13 FAQ in the reader's own words
    sec("Questions lawyers ask us")
    for i, (b, t) in enumerate(cards(s[11])):
        a(f'<details{" open" if i == 0 else ""}><summary>{b}</summary><div class="a">{t}</div></details>')
    end()

    # close
    a(f'<div class="close"><div class="w"><h2>{d["close"][0]}</h2><p>{d["close"][1]}</p>{btn(href, "<small>3 live evenings · 24 to 26 Oct</small>")}</div></div>')
    a(f'<div class="disc"><div class="w"><p><b>Please read.</b> {d["disc"].replace("<b>Please read.</b>", "").strip()}</p></div></div>')
    a(f'<div class="sticky" id="sticky"><a class="btn" href="{href}">Join for Rs 10 · refundable</a></div>')
    a(f'<script>{JS}{EXTRA_JS}</script></body></html>')
    return "".join(out)



def main():
    for f in sorted(glob.glob(os.path.join(HERE, "original", "lp_tlc1-*.html"))):
        n = re.search(r"tlc1-(\d\d)", f).group(1)
        d = parse(f)
        # keep the original disclaimer, and add the proof hedge that used to sit above a button
        d["disc"] = d["disc"]
        out = build(n, d)
        assert "—" not in out and "–" not in out, "dash found in " + n
        open(os.path.join(HERE, f"lp_tlc1-{n}.html"), "w", encoding="utf-8").write(out)
        words = len(strip(re.sub(r"<(style|script)>.*?</\1>", "", out, flags=re.S)).split())
        print(n, "ok", words, "words")


if __name__ == "__main__":
    main()
