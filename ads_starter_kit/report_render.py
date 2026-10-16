"""HTML rendering for the daily ad report. Emits an Artifact-ready fragment:
no doctype, html, head or body tags - those are supplied at publish time."""
import datetime, html, math

E = html.escape

CSS = """
<style>
:root{
  --ground:#F5F7F7; --surface:#FFFFFF; --sunk:#EDF1F1;
  --ink:#101619; --mid:#4E5C61; --faint:#7C8B90; --line:#D9E1E2;
  --accent:#0B5D57; --accent-soft:#E2EFED;
  --critical:#A3291B; --high:#9C5E08; --medium:#6E6412; --good:#1B6742;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0D1315; --surface:#141C1F; --sunk:#101819;
    --ink:#E7EEEF; --mid:#9DACB0; --faint:#77878B; --line:#243135;
    --accent:#5AC9BD; --accent-soft:#12302E;
    --critical:#F08A78; --high:#E0A44A; --medium:#C9BE5E; --good:#63C48E;
  }
}
:root[data-theme="dark"]{
  --ground:#0D1315; --surface:#141C1F; --sunk:#101819;
  --ink:#E7EEEF; --mid:#9DACB0; --faint:#77878B; --line:#243135;
  --accent:#5AC9BD; --accent-soft:#12302E;
  --critical:#F08A78; --high:#E0A44A; --medium:#C9BE5E; --good:#63C48E;
}
*{box-sizing:border-box}
body{background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:15px; line-height:1.55; margin:0;}
.wrap{max-width:1080px; margin:0 auto; padding:40px 24px 96px;}
h1{font-size:30px; line-height:1.15; margin:0 0 6px; letter-spacing:-.02em; text-wrap:balance;}
h2{font-size:13px; text-transform:uppercase; letter-spacing:.09em; color:var(--faint);
  margin:0; font-weight:600;}
h3{font-size:17px; margin:0 0 2px; letter-spacing:-.01em;}
p{margin:0}
.sub{color:var(--mid); font-size:15px; max-width:66ch;}
.head{border-bottom:2px solid var(--ink); padding-bottom:20px; margin-bottom:8px;}
.stamp{font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:12px;
  color:var(--faint); letter-spacing:.04em;}
section{padding-top:34px;}
.shead{display:flex; align-items:baseline; gap:12px; border-bottom:1px solid var(--line);
  padding-bottom:8px; margin-bottom:16px;}
.shead .note{font-size:12.5px; color:var(--faint); margin-left:auto; text-align:right;}
.stack{display:flex; flex-direction:column; gap:10px;}
.finding{display:grid; grid-template-columns:auto 1fr; gap:0 16px;
  background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--sev);
  border-radius:3px; padding:14px 16px;}
.finding.critical{--sev:var(--critical)} .finding.high{--sev:var(--high)}
.finding.medium{--sev:var(--medium)}
.tag{font-family:"IBM Plex Mono",monospace; font-size:10.5px; font-weight:600;
  letter-spacing:.08em; color:var(--sev); text-transform:uppercase; padding-top:4px;
  white-space:nowrap;}
.finding .why{color:var(--mid); font-size:14px; margin-top:3px;}
.finding .do{font-size:14px; margin-top:8px; padding-top:8px; border-top:1px dotted var(--line);}
.finding .do b{color:var(--accent); font-weight:600;}
.scroll{overflow-x:auto; border:1px solid var(--line); border-radius:3px;
  background:var(--surface);}
table{border-collapse:collapse; width:100%; font-size:13.5px;}
th{text-align:left; font-size:11px; text-transform:uppercase; letter-spacing:.07em;
  color:var(--faint); font-weight:600; padding:10px 12px; border-bottom:1px solid var(--line);
  white-space:nowrap; background:var(--sunk);}
td{padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top;}
tr:last-child td{border-bottom:none}
.num{font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums;
  text-align:right; white-space:nowrap;}
.nm{font-family:"IBM Plex Mono",monospace; font-size:12.5px;}
.dim{color:var(--faint)}
.pill{display:inline-block; font-family:"IBM Plex Mono",monospace; font-size:10.5px;
  font-weight:600; letter-spacing:.05em; padding:2px 7px; border-radius:2px;
  border:1px solid currentColor; white-space:nowrap;}
.p-good{color:var(--good)} .p-watch{color:var(--high)} .p-bad{color:var(--critical)}
.p-flat{color:var(--faint)}
a{color:var(--accent); text-decoration:none; border-bottom:1px solid transparent;}
a:hover{border-bottom-color:currentColor}
a:focus-visible{outline:2px solid var(--accent); outline-offset:2px;}
.bars{display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:1px;
  background:var(--line); border:1px solid var(--line); border-radius:3px; overflow:hidden;}
.bar{background:var(--surface); padding:12px 14px;}
.bar .k{font-size:11px; text-transform:uppercase; letter-spacing:.07em; color:var(--faint);}
.bar .v{font-family:"IBM Plex Mono",monospace; font-size:19px; margin-top:3px;
  font-variant-numeric:tabular-nums;}
.partial{background:var(--accent-soft);}
.caveat{background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--accent);
  border-radius:3px; padding:14px 16px; font-size:14px; color:var(--mid);}
.caveat b{color:var(--ink)}
footer{margin-top:46px; padding-top:16px; border-top:1px solid var(--line);
  font-size:12.5px; color:var(--faint);}
@media (max-width:640px){
  .wrap{padding:26px 14px 70px} h1{font-size:24px}
  .finding{grid-template-columns:1fr; gap:6px}
}
</style>
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">')


def rupees(x):
    d = str(int(round(x)))
    neg, d = (d[0] == "-"), d.lstrip("-")
    if len(d) <= 3:
        out = d
    else:
        head, tail, parts = d[:-3], d[-3:], []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        out = ",".join(parts + [tail])
    return ("-" if neg else "") + out


def band(ratio):
    if ratio is None:
        return '<span class="pill p-flat">no data</span>'
    if ratio <= 0.83:
        return '<span class="pill p-good">scale</span>'
    if ratio < 1.30:
        return '<span class="pill p-flat">on target</span>'
    if ratio < 1.50:
        return '<span class="pill p-watch">watch</span>'
    return '<span class="pill p-bad">breaker</span>'


def render(d):
    camp, aset, ad = d["camp"], d["aset"], d["ad"]
    n_of, cpr, group = d["n_of"], d["cpr"], d["group"]
    today, yday = d["today"], d["yday"]
    days = sorted(d["day"])
    out = [FONTS, "<title>Daily Ad Desk</title>", CSS, '<div class="wrap">']

    # ---------- header ----------
    t_sp = d["day"].get(today, {}).get("spend", 0)
    y_sp = d["day"].get(yday, {}).get("spend", 0)
    week = sum(d["day"][x]["spend"] for x in days)
    frac = (t_sp / y_sp * 100) if y_sp else 0
    read = [a for a in d["accounts"] if a[3]]
    stamp = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M IST")
    out.append('<div class="head">')
    out.append('<p class="stamp">%s</p>' % E(stamp))
    out.append("<h1>Daily ad desk</h1>")
    out.append('<p class="sub">Every Meta account the reporting token can read: '
               '<b>%d accounts</b>, %d of them spending. All rupees include 18%% GST. '
               'Google Ads is not covered - there is no API access, so this is the Meta '
               'picture only.</p>' % (len(d["accounts"]), len(read)))
    out.append("</div>")

    out.append('<div class="bars" style="margin-top:18px">')
    for k, v in (("Today so far", "Rs " + rupees(t_sp)),
                 ("Yesterday", "Rs " + rupees(y_sp)),
                 ("7 days", "Rs " + rupees(week)),
                 ("Buyers 7d", rupees(sum(d["day"][x]["buys"] for x in days))),
                 ("Leads 7d", rupees(sum(d["day"][x]["leads"] for x in days)))):
        out.append('<div class="bar"><div class="k">%s</div><div class="v">%s</div></div>' % (k, v))
    out.append("</div>")

    out.append('<div class="caveat" style="margin-top:14px"><b>Today is a part day.</b> '
               'It has spent %.0f%% of yesterday\'s total so far. Volumes will look halved; '
               'cost per result is a rate and stays comparable, so judge on that. Nothing here '
               'should be killed on today alone - six part-day kill calls on this account all '
               'collapsed when re-checked at seven days.</div>' % frac)

    # ---------- act today ----------
    f = d["findings"]
    out.append("<section>")
    out.append('<div class="shead"><h2>Act today</h2>'
               '<span class="note">%d open, hardest first</span></div>' % len(f))
    if not f:
        out.append('<div class="caveat">Nothing is broken and nothing has breached its '
                   'circuit breaker. The correct action today is none - every edit restarts '
                   'Meta\'s learning phase, so leaving a working ad set alone is a decision, '
                   'not neglect.</div>')
    else:
        out.append('<div class="stack">')
        for x in f[:14]:
            money = (' &middot; Rs %s committed' % rupees(x["money"])) if x["money"] else ""
            out.append(
                '<div class="finding %s"><div class="tag">%s<br>%s</div><div>'
                '<h3>%s</h3><p class="why">%s%s</p>'
                '<p class="do"><b>Do:</b> %s</p></div></div>'
                % (x["sev"], E(x["sev"]), E(x["layer"]), E(x["what"]), E(x["why"]), money,
                   E(x["do"])))
        out.append("</div>")
    out.append("</section>")

    # ---------- camp coverage ----------
    out.append("<section>")
    out.append('<div class="shead"><h2>Camps ahead</h2>'
               '<span class="note">from BOOTCAMP_CALENDAR.md</span></div>')
    out.append('<div class="scroll"><table><tr><th>Camp</th><th>Type</th><th>Dates</th>'
               '<th class="num">Days</th><th>Campaign behind it</th></tr>')
    for c in d["cal"]:
        m = d["match"](c)
        if m:
            cell = '<span class="nm">%s</span>' % E(m)
        elif c["type"] == "RE":
            # Reruns are not advertised on this account, so an empty cell here is
            # the expected state, not a gap.
            cell = '<span class="pill p-flat">rerun, not advertised</span>'
        else:
            cell = '<span class="pill p-bad">no campaign</span>'
        out.append("<tr><td>%s</td><td class=\"dim\">%s</td><td class=\"nm\">%s</td>"
                   '<td class="num">%d</td><td>%s</td></tr>'
                   % (E(c["camp"]), E(c["type"]), E(c["dates"]), c["days"], cell))
    out.append("</table></div>")
    out.append("</section>")

    # ---------- day by day ----------
    out.append("<section>")
    out.append('<div class="shead"><h2>Day by day</h2>'
               '<span class="note">whole account, all funnels together</span></div>')
    out.append('<div class="scroll"><table><tr><th>Day</th><th class="num">Spend</th>'
               '<th class="num">Buyers</th><th class="num">Leads</th>'
               '<th class="num">Clicks</th></tr>')
    for x in days:
        v = d["day"][x]
        lbl = datetime.date.fromisoformat(x).strftime("%a %d %b")
        cls = ' class="partial"' if x == today else ""
        tail = ' <span class="dim">part day</span>' if x == today else ""
        out.append('<tr%s><td class="nm">%s%s</td><td class="num">%s</td>'
                   '<td class="num">%s</td><td class="num">%s</td><td class="num">%s</td></tr>'
                   % (cls, lbl, tail, rupees(v["spend"]), rupees(v["buys"]),
                      rupees(v["leads"]), rupees(v["clicks"])))
    out.append("</table></div></section>")

    # ---------- boards ----------
    titles = {"bootcamp": ("Bootcamps", "measured in buyers &middot; scale under 0.83x, breaker at 1.5x"),
              "lead": ("Lead campaigns", "measured in registrations - never comparable with buyers"),
              "community": ("Community", "a separate product line with its own baseline")}
    for g in ("bootcamp", "lead", "community"):
        camps = [c for c in d["live"] if group(c) == g and camp[c]["spend"] >= 5000]
        if not camps:
            continue
        camps.sort(key=lambda c: -camp[c]["spend"])
        out.append("<section>")
        out.append('<div class="shead"><h2>%s</h2><span class="note">%s</span></div>'
                   % (titles[g][0], titles[g][1]))
        out.append('<div class="scroll"><table><tr><th>Campaign</th><th>Account</th>'
                   '<th class="num">Today</th><th class="num">Yesterday</th>'
                   '<th class="num">7-day cost</th><th class="num">n</th>'
                   '<th class="num">Reach page</th><th class="num">Page buys</th>'
                   '<th>Band</th></tr>')
        med = d["gmed"].get(g)
        for c in camps:
            v = camp[c]
            t = d["camp_day"].get((c, today))
            y = d["camp_day"].get((c, yday))
            def cell(x):
                if not x:
                    return '<span class="dim">-</span>'
                n = n_of(x, c)
                return "Rs " + rupees(x["spend"] / n) if n else '<span class="dim">-</span>'
            b = cpr(v, c)
            load = (v["lpv"] / v["clicks"] * 100) if v["clicks"] else None
            conv = (n_of(v, c) / v["lpv"] * 100) if v["lpv"] else None
            out.append(
                '<tr><td class="nm">%s</td><td class="dim">%s</td>'
                '<td class="num">%s</td><td class="num">%s</td>'
                '<td class="num"><b>%s</b></td><td class="num dim">%d</td>'
                '<td class="num">%s</td><td class="num">%s</td><td>%s</td></tr>'
                % (E(c[:46]), E(d["acct_of"][c]), cell(t), cell(y),
                   ("Rs " + rupees(b)) if b else "-", int(n_of(v, c)),
                   ("%.0f%%" % load) if load is not None else '<span class="dim">-</span>',
                   ("%.1f%%" % conv) if conv is not None else '<span class="dim">-</span>',
                   band(b / med if (b and med) else None)))
        out.append("</table></div></section>")

    # ---------- ad set funding ----------
    out.append("<section>")
    out.append('<div class="shead"><h2>Is the budget spread too thin?</h2>'
               '<span class="note">Meta needs 50 results a week per ad set</span></div>')
    out.append(
        '<p class="sub" style="margin-bottom:10px">When an ad set is new or edited, Meta does '
        'not yet know who buys, so it explores - and while it explores, costs run high and '
        'jumpy. It settles down once the ad set collects about <b>50 results in 7 days</b>. '
        'Below that it stays stuck exploring, and stays expensive.</p>'
        '<p class="sub" style="margin-bottom:10px">That turns into simple arithmetic: to get '
        '50 results a week, an ad set has to be able to afford 50 results. At Rs 355 a buyer '
        'that is 50 x 355 = Rs 17,750 a week, so about <b>Rs 2,536 a day</b>. An ad set given '
        'Rs 200 a day can never get there, however good its creative is.</p>'
        '<p class="sub" style="margin-bottom:14px">So splitting one budget across many ad sets '
        'can leave every one of them too thin to settle. <b>Funded</b> below counts how many of '
        'a campaign\'s ad sets clear their own floor. <span class="dim">A caveat: clearing out '
        'the starved sets recovers their wasted spend, but it does not close the whole gap - '
        'on the worst campaign here it moves the cost about a fifth of the way. Treat this as '
        'a lead, not a diagnosis.</span></p>')
    out.append('<div class="scroll"><table><tr><th>Campaign</th><th class="num">Cost</th>'
               '<th class="num">Ad sets</th><th class="num">Floor per day</th>'
               '<th class="num">Funded</th><th>Read</th></tr>')
    rowsf = []
    for c in d["live"]:
        b = cpr(camp[c], c)
        if not b or camp[c]["spend"] < 20000:
            continue
        floor = 50 * b / 7
        sets = [v for (cc, s), v in aset.items() if cc == c]
        okc = sum(1 for v in sets if v["spend"] / 7 >= floor)
        rowsf.append((c, b, len(sets), floor, okc))
    rowsf.sort(key=lambda r: (r[4] / r[2]) if r[2] else 1)
    for c, b, ns, floor, okc in rowsf:
        ratio = okc / ns if ns else 1
        pill = ('<span class="pill p-bad">spread thin</span>' if ratio < 0.34
                else '<span class="pill p-watch">mixed</span>' if ratio < 0.7
                else '<span class="pill p-good">concentrated</span>')
        out.append('<tr><td class="nm">%s</td><td class="num">Rs %s</td>'
                   '<td class="num">%d</td><td class="num">Rs %s</td>'
                   '<td class="num">%d of %d</td><td>%s</td></tr>'
                   % (E(c[:46]), rupees(b), ns, rupees(floor), okc, ns, pill))
    out.append("</table></div></section>")

    # ---------- funnel platform ----------
    rec = d.get("recon") or {}
    gxt = d.get("gx_totals") or {}
    if rec.get("rows"):
        out.append("<section>")
        out.append('<div class="shead"><h2>What the funnel actually recorded</h2>'
                   '<span class="note">GrowthX, same %d days</span></div>' % d.get("gx_days", 7))
        out.append(
            '<p class="sub" style="margin-bottom:12px">Meta credits a result to the ad that '
            'earned the click. The funnel platform records what came through the page. They '
            'measure different things, so a gap is information, not an error - but a big one '
            'means <b>the cost you are optimising against is not the cost you are banking</b>. '
            'One row per landing page, because several ads often share one - comparing a '
            'single ad against a page many ads feed is how you get a +1600%% gap that means '
            'nothing. Covering '
            '<b>Rs %s of Rs %s (%.0f%%)</b> of spend.</p>'
            % (rupees(rec["covered"]), rupees(rec["total"]), rec["pct"]))
        if gxt:
            out.append('<div class="bars" style="margin-bottom:14px">')
            for k, v in (("Leads recorded", rupees(gxt.get("total") or 0)),
                         ("Paid", rupees(gxt.get("paid") or 0)),
                         ("Tripwire receipts", "Rs " + rupees(gxt.get("revenue") or 0))):
                out.append('<div class="bar"><div class="k">%s</div><div class="v">%s</div></div>'
                           % (k, v))
            out.append("</div>")
            out.append(
                '<div class="caveat" style="margin-bottom:14px"><b>Tripwire receipts are not '
                'revenue.</b> These are the Rs 10, Rs 100 and Rs 200 entry payments, so the '
                'figure above is roughly a seventh of what was spent to get them. That is the '
                'design of the funnel, not a loss - the actual revenue is the course sold '
                'afterwards, which this platform does not report. <b>Never compute a return '
                'on ad spend from this number.</b></div>')
        out.append('<div class="scroll"><table><tr><th>Landing page</th>'
                   '<th class="num">Ads</th><th class="num">Spend</th>'
                   '<th class="num">Meta says</th><th class="num">Funnel recorded</th>'
                   '<th class="num">Gap</th><th class="num">Real cost</th>'
                   '<th class="num">Form only</th><th class="num">Started</th>'
                   '<th class="num">Expired</th></tr>')
        for x in rec["rows"][:30]:
            g = x["gap"]
            gcls = ("p-bad" if g is not None and g <= -30 else
                    "p-good" if g is not None and g >= 30 else "p-flat")
            gtxt = ("%+.0f%%" % g) if g is not None else "-"
            out.append('<tr><td class="nm">%s</td><td class="num dim">%d</td>'
                       '<td class="num">%s</td>'
                       '<td class="num">%d</td><td class="num">%d</td>'
                       '<td class="num"><span class="pill %s">%s</span></td>'
                       '<td class="num">%s</td><td class="num dim">%d</td>'
                       '<td class="num dim">%d</td><td class="num dim">%d</td></tr>'
                       % (E(x["funnel"]), x["n_ads"], rupees(x["spend"]),
                          int(x["meta"]), int(x["gx"]),
                          gcls, gtxt,
                          ("Rs " + rupees(x["gx_cost"])) if x["gx_cost"] else "-",
                          x["form_only"], x["started"], x["expired"]))
        out.append("</table></div>")
        if rec.get("unmatched") or rec.get("nolink"):
            out.append('<p class="sub" style="margin-top:10px;font-size:13px" class="dim">'
                       '<span class="dim">%d ads point at a page with no activity in this '
                       'window, and %d carry no readable link - they are absent from this '
                       'table, not zero.</span></p>'
                       % (rec.get("unmatched", 0), rec.get("nolink", 0)))
        out.append("</section>")

    # ---------- creative ----------
    links = d.get("links", {})
    allads = sorted(ad.items(), key=lambda kv: -kv[1]["spend"])
    out.append("<section>")
    out.append('<div class="shead"><h2>Every ad</h2>'
               '<span class="note">%d ads with spend &middot; sorted by spend</span></div>'
               % len(allads))
    out.append('<p class="sub" style="margin-bottom:14px">Cost is compared against the '
               'median for that ad\'s funnel type, not its own campaign. <b>n</b> is how many '
               'results the figure rests on and the margin is how far it could move by chance '
               '- under 20 results, greyed out, it is not worth acting on. Links open the '
               'live post and the page it sends people to.</p>')
    out.append('<div class="scroll"><table><tr><th>Ad</th><th>Campaign</th>'
               '<th class="num">Spend</th><th class="num">Cost</th><th class="num">n</th>'
               '<th class="num">Margin</th><th class="num">Freq</th><th>Band</th>'
               '<th>Open</th></tr>')
    for (c, a, aid), v in allads:
        b, this, n = d["gmed"].get(group(c)), cpr(v, c), n_of(v, c)
        marg = ("&plusmn;%.0f%%" % (196 / math.sqrt(n))) if n else "-"
        fr = ('<span class="pill p-watch">%.1f</span>' % v["freq"]) if v["freq"] >= 3.5 \
             else "%.1f" % v["freq"]
        L = links.get(aid) or {}
        opens = []
        for label, key in (("FB", "fb"), ("IG", "ig"), ("LP", "lp")):
            if L.get(key):
                opens.append('<a href="%s" target="_blank" rel="noopener">%s</a>'
                             % (E(L[key]), label))
            else:
                opens.append('<span class="dim">%s</span>' % label)
        out.append('<tr><td class="nm">%s</td><td class="dim">%s</td>'
                   '<td class="num">%s</td><td class="num">%s</td>'
                   '<td class="num %s">%d</td><td class="num dim">%s</td>'
                   '<td class="num">%s</td><td>%s</td>'
                   '<td class="nm" style="white-space:nowrap">%s</td></tr>'
                   % (E(a), E(c[:26]), rupees(v["spend"]),
                      ("Rs " + rupees(this)) if this else "-",
                      "" if n >= 20 else "dim", int(n), marg, fr,
                      band(this / b if (this and b and n >= 20) else None),
                      " &middot; ".join(opens)))
    out.append("</table></div></section>")

    # ---------- scale ----------
    if d["scale"]:
        out.append("<section>")
        out.append('<div class="shead"><h2>Cheapest ads - worth more budget</h2>'
                   '<span class="note">raise 15-20%, then leave it 3 days</span></div>')
        out.append('<p class="sub" style="margin-bottom:14px">These are buying results for '
                   '<b>at least 17% below the going rate</b> for their funnel type, on enough '
                   'results to trust. The move is to raise the budget 15-20% and then leave it '
                   'alone for three days - a bigger jump, or a change every day, restarts '
                   'Meta\'s learning and undoes the advantage. <span class="dim">They are '
                   'candidates rather than winners because more budget means wider delivery, '
                   'so a cheap ad often gets a little dearer as it grows.</span></p>')
        out.append('<div class="scroll"><table><tr><th>Ad</th><th>Campaign</th>'
                   '<th class="num">Its cost</th><th class="num">Campaign cost</th>'
                   '<th class="num">n</th></tr>')
        for s in d["scale"][:12]:
            out.append('<tr><td class="nm">%s</td><td class="dim">%s</td>'
                       '<td class="num"><b>Rs %s</b></td><td class="num dim">Rs %s</td>'
                       '<td class="num dim">%d</td></tr>'
                       % (E(s["ad"][:44]), E(s["camp"][:26]), rupees(s["cpr"]),
                          rupees(s["base"]), int(s["n"])))
        out.append("</table></div></section>")

    out.append("</div>")
    return "\n".join(out)
