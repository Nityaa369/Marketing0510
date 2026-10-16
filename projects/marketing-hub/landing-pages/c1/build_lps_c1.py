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


def build(n, d):
    r = READER[n]
    s = d["secs"]
    href = d["href"]
    img, alt = d["img"]
    out = []
    a = out.append
    a(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
      f'<title>{d["title"]}</title><meta name="description" content="3 live evenings, 24 to 26 Oct. Rs 10 incl. GST, refundable.">'
      f'<style>{CSS.replace("--ac:#13756B;--soft:#EAF5F2", "--ac:%s;--soft:%s" % (d["ac"], d["soft"]))}</style></head><body>')
    a('<div class="top"><div class="w"><div class="brand">LawSikho</div><div class="cd" id="cd">Starts Sat 24 Oct<small>6 PM IST</small></div></div></div>')

    # FOLD
    a('<div class="fold" id="fold"><div class="w">')
    a(f'<span class="pill">{d["pill"]}</span>')
    a(f'<div class="hook">{d["hook"]}</div>')
    a(f'<p class="sup">{d["sup"]}</p>')
    a(f'<div class="hero"><img src="{img}" alt="{alt}"></div>')
    a(f'<div class="ft"><div><small>Today</small>{r["frm"]}</div><i>&rarr;</i><div class="to"><small>After the camp</small>{r["to"]}</div></div>')
    a(f'<div class="def">{d["def"]}</div>')
    a('<ol class="route">'
      '<li><span>1</span><small>Sat 24 Oct · 6 to 9 PM IST</small>Draft a software development agreement with us, clause by clause.</li>'
      '<li><span>2</span><small>Sun 25 Oct · 6 to 9 PM IST</small>See six ways tech companies make money, and the legal work each one creates.</li>'
      '<li><span>3</span><small>Mon 26 Oct · 7 to 10 PM IST</small>Review a startup\'s terms and learn how lawyers pitch the fix.</li></ol>')
    a('<div class="price"><div class="big">Rs 10<sub>incl. GST</sub></div><p>Refundable. Live only, no recordings. Joining details come on WhatsApp and email.</p></div>')
    a(btn(href, "<small>3 live evenings · 24 to 26 Oct</small>"))
    a(f'<p class="q">{d["q"]}</p>')
    a('</div></div>')

    # 01 name the reader (lede + rest)
    p1 = paras(s[0])
    a(f'<section class="rv"><div class="w"><span class="num">01</span><h2>{h2(s[0])}</h2>')
    a(f'<p class="lede">{p1[0]}</p>')
    for x in p1[1:]:
        a(f'<p>{x}</p>')
    a('</div></section>')

    # 02 the move
    a(f'<section class="rv"><div class="w"><span class="num">02</span><h2>{h2(s[1])}</h2>')
    for x in paras(s[1]):
        a(f'<p>{x}</p>')
    a(btn(href))
    a('</div></section>')

    # 03 what you tried (failed alternatives)
    a(f'<section class="rv fail"><div class="w"><span class="num">03</span><h2>{h2(s[2])}</h2>')
    for b, t in cards(s[2]):
        a(f'<div class="card"><b>{b}</b>{t}</div>')
    a('</div></section>')

    # 04 reframe + cost of staying
    hs = re.findall(r"<h2[^>]*>(.*?)</h2>", s[3])
    ps4 = paras(s[3])
    a(f'<section class="rv"><div class="w"><span class="num">04</span><h2>{hs[0]}</h2>')
    for x in ps4[:-1]:
        a(f'<p>{x}</p>')
    a(f'<h3>{hs[1]}</h3><p>{ps4[-1]}</p></div></section>')

    # 05 the work, tied to the reader
    a(f'<section class="rv work"><div class="w"><span class="num">05</span><h2>{h2(s[4])}</h2>')
    for x in paras(s[4]):
        a(f'<p>{x}</p>')
    a('</div></section>')

    # 06 five words
    a('<section class="rv"><div class="w"><span class="num">06</span><h2>Five words every tech contract uses</h2>'
      '<p>On Evening 1 you learn the five concepts behind most technology contracts. None of them needs coding.</p><div class="tg">')
    for b, t in cards(s[5]):
        a(f'<div class="card"><b>{b}</b>{t}</div>')
    a('</div></div></section>')

    # 07 the evenings
    a('<section class="rv"><div class="w"><span class="num">07</span><h2>What happens in the 3 live evenings</h2>')
    days = cards(s[6])
    for b, t in days[:3]:
        head, _, when = b.partition(" · ")
        a(f'<div class="day"><div class="dh"><span>{head}</span><span>{when}</span></div><div class="db">{t}</div></div>')
    a('<h3>The method we teach</h3><div class="steps">')
    for b, t in days[3:]:
        a(f'<div class="card"><b>{b}</b>{t}</div>')
    a('</div>')
    a(btn(href))
    a('</div></section>')

    # 08 the document you will draft (redline mock) + the 6-month note
    p8 = paras(s[7])
    a(f'<section class="rv"><div class="w"><span class="num">08</span><h2>{h2(s[7])}</h2><p>{p8[0]}</p>')
    a('<div class="doc"><div class="hd">Illustration · software development agreement</div><div class="bd">'
      '<div class="cl"><b>9. Intellectual property.</b> 9.1 The Developer assigns to the Client <mark>all rights in the Deliverables</mark> '
      'on <del>delivery</del><ins>payment in full</ins>.</div>'
      '<div class="cl">9.2 The Developer keeps its <mark>pre-existing tools</mark> and grants the Client a licence to use them inside the Deliverables.</div></div>'
      f'<div class="mg"><b>Margin note:</b> {r["note"]}</div></div>')
    for x in p8[1:]:
        a(f'<p>{x}</p>')
    a('</div></section>')

    # 09 plan
    a('<section class="rv"><div class="w"><span class="num">09</span><h2>The plan after the camp, in plain steps</h2><ol class="plan">')
    for x in re.findall(r'<li[^>]*>(.*?)</li>', s[8], re.S):
        a(f'<li>{x}</li>')
    a('</ol><p>This is the plan taught on Evening 2. How far you get depends on the hours you put in.</p></div></section>')

    # 10 proof (hedge moved to the end of the page, never above a pay button)
    a('<section class="rv"><div class="w"><span class="num">10</span><h2>Lawyers who took this route</h2>')
    for b, t in cards(s[9]):
        ini = "".join(w[0] for w in strip(b).split()[:2])
        a(f'<div class="proof"><div class="av">{ini}</div><div><b>{b}</b>{t}</div></div>')
    a('</div></section>')

    # 11 demand + cost comparison + risk removal
    a('<section class="rv"><div class="w"><span class="num">11</span><h2>Why the demand exists, and what it costs to find out</h2><div class="stats">')
    stats = [
        ("55,200", "startups recognised in 2025-26, and 2.4 lakh recognised in India by 30 Jun 2026.", "Inc42, 2026"),
        ("2,117", "global capability centres in India, employing about 23.6 lakh people.", "Nasscom-Zinnov via Business Today, May 2026"),
        ("1,215", "legal tech startups tracked in India.", "Tracxn, Sep 2026"),
        ("2,400+", "organisations use Harvey, by its own count. It hires Legal Engineers in Bengaluru who must be qualified Indian advocates.", "harvey.ai, 2026"),
    ]
    for num, tx, src in stats:
        a(f'<div class="stat"><div class="n">{num}</div><p>{tx}</p><span class="src">Source: {src}.</span></div>')
    a('</div><div class="cmp">'
      '<div><b>Figuring it out alone</b>Free, plus months of trial and error. Scattered articles and no feedback on your drafts.</div>'
      '<div><b>A long course first</b>A large fee, paid upfront. A commitment before you know if the work suits you.</div>'
      '<div class="us"><b>This bootcamp</b><span class="rs">Rs 10 incl. GST</span>Refundable. Three live evenings doing the work with us.</div></div>')
    a('<p><b>Risk removed.</b> The Rs 10 is refundable. Bring a laptop or phone and a notebook, and keep the three evenings free. Joining details arrive on WhatsApp and email.</p>')
    a(btn(href))
    a('</div></section>')

    # 12 FAQ
    a('<section class="rv"><div class="w"><span class="num">12</span><h2>Questions lawyers ask us</h2>')
    for i, (b, t) in enumerate(cards(s[11])):
        a(f'<details{" open" if i == 0 else ""}><summary>{b}</summary><div class="a">{t}</div></details>')
    a('</div></section>')

    # close
    a(f'<div class="close"><div class="w"><h2>{d["close"][0]}</h2><p>{d["close"][1]}</p>{btn(href, "<small>3 live evenings · 24 to 26 Oct</small>")}</div></div>')
    a(f'<div class="disc"><div class="w"><p><b>Please read.</b> {d["disc"].replace("<b>Please read.</b>", "").strip()}</p></div></div>')
    a(f'<div class="sticky" id="sticky"><a class="btn" href="{href}">Join for Rs 10 · refundable</a></div>')
    a(f'<script>{JS}</script></body></html>')
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
