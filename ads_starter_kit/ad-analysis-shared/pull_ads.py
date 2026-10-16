"""Meta ad-performance pull by category keyword — works on any machine.

Discovers every campaign whose name matches your keyword across all ad accounts
the token can see, then reports ad-by-ad performance with public FB/IG links.
All rupee figures include 18% GST (Meta returns net values).

Usage:
    python3 pull_ads.py --list                 # list accounts + active campaigns (14d spend)
    python3 pull_ads.py women                  # all campaigns matching "women", last 14 days
    python3 pull_ads.py "remote work" --days 30
    python3 pull_ads.py women remote --days 7  # multiple keywords = OR match

Token lookup order:
    1. META_ACCESS_TOKEN environment variable (claude.ai/code: set it as an env secret)
    2. .env file next to this script (META_ACCESS_TOKEN=...)
    3. macOS Keychain entry `meta-access-token` (Ramanuj's machine only)

Output: reports/<keyword>_<date>.json and .html (opens in browser on a Mac).
"""
import argparse, datetime, json, os, sys, time, urllib.error, urllib.parse, urllib.request

GST = 1.18
API = "https://graph.facebook.com/v21.0"
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "reports")


def token():
    t = os.environ.get("META_ACCESS_TOKEN")
    if t:
        return t.strip()
    envf = os.path.join(HERE, ".env")
    if os.path.exists(envf):
        for line in open(envf, encoding="utf-8"):
            line = line.strip()
            if line.startswith("META_ACCESS_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    if sys.platform == "darwin":
        import subprocess
        try:
            return subprocess.check_output(
                ["security", "find-generic-password", "-a", os.environ.get("USER", ""),
                 "-s", "meta-access-token", "-w"], text=True).strip()
        except Exception:
            pass
    sys.exit("No token found. Set META_ACCESS_TOKEN as an env var or in a .env file "
             "next to this script. Ask Ramanuj for the read-only reporting token.")


def get(node, params, tok, retries=4):
    params = dict(params, access_token=tok)
    url = f"{API}/{node}?{urllib.parse.urlencode(params)}"
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            try:
                err = json.loads(e.read()).get("error", {}).get("message", str(e))
            except Exception:
                err = str(e)
            if i == retries - 1:
                return {"error": err}
            time.sleep(15)
        except Exception as e:
            if i == retries - 1:
                return {"error": str(e)}
            time.sleep(8)


def paged(node, params, tok):
    out, page = [], get(node, params, tok)
    while True:
        if "error" in page:
            print(f"  API ERROR on {node}: {page['error']}", file=sys.stderr)
            break
        out.extend(page.get("data", []))
        cur = (page.get("paging", {}).get("cursors", {}) or {}).get("after")
        if not page.get("paging", {}).get("next") or not cur:
            break
        page = get(node, dict(params, after=cur), tok)
    return out


def action_count(row, kinds):
    n = 0.0
    for a in row.get("actions") or []:
        if a.get("action_type") in kinds:
            n = max(n, float(a.get("value") or 0))
    return n


PURCHASE = ("purchase", "offsite_conversion.fb_pixel_purchase")
LEAD = ("lead", "offsite_conversion.fb_pixel_lead", "onsite_conversion.lead_grouped")
REG = ("complete_registration", "offsite_conversion.fb_pixel_complete_registration")


# Meta account_status: 1 ACTIVE, 2 DISABLED, 3 UNSETTLED. This used to return only
# status 1, which silently dropped UK SkillArbitrage (UNSETTLED) and the disabled
# Law Sikho account from every report. A disabled account can still hold spend inside
# the window, and a silent omission reads as a zero. Found 9 Sep 2026.
STATUS_NAME = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED"}
# GST applies to the Indian entity only. Grossing USD or GBP up by 18% and printing it
# behind a rupee sign would corrupt any total spanning accounts.
SYMBOL = {"INR": "₹", "USD": "$", "GBP": "£"}


def accounts(tok):
    d = get("me/adaccounts",
            {"fields": "name,account_id,account_status,currency", "limit": "200"}, tok)
    if "error" in d:
        sys.exit(f"Cannot list ad accounts: {d['error']}")
    return [(a["account_id"], a["name"], a.get("account_status"),
             a.get("currency") or "INR") for a in d.get("data", [])]


def money(net, currency):
    """Gross up by GST for INR only. Returns (amount, symbol)."""
    amt = float(net or 0) * (GST if currency == "INR" else 1.0)
    return amt, SYMBOL.get(currency, currency + " ")


def time_range(days):
    today = datetime.date.today()
    since = (today - datetime.timedelta(days=days)).isoformat()
    return json.dumps({"since": since, "until": today.isoformat()}), today


def list_campaigns(tok, days):
    tr, _ = time_range(days)
    accts = accounts(tok)
    silent = []
    for acct_id, acct_name, status, cur in accts:
        rows = paged(f"act_{acct_id}/insights",
                     {"level": "campaign", "time_range": tr,
                      "fields": "campaign_name,spend", "limit": "500"}, tok)
        rows = [r for r in rows if float(r.get("spend") or 0) > 0]
        if not rows:
            silent.append(f"{acct_name} [{STATUS_NAME.get(status, status)}]")
            continue
        flag = "" if status == 1 else f"  ** {STATUS_NAME.get(status, status)} **"
        print(f"\n{acct_name}  (act_{acct_id})  {cur}{flag}")
        for r in sorted(rows, key=lambda x: -float(x.get("spend") or 0)):
            amt, sym = money(r.get("spend"), cur)
            print(f"  {sym}{amt:>10,.0f}  {r.get('campaign_name')}")
    # State coverage explicitly. "Nothing is running" is only defensible when the
    # accounts checked are named alongside the claim.
    print(f"\n-- coverage: {len(accts)} accounts read, "
          f"{len(silent)} with no spend in {days}d --")
    if silent:
        print("   no spend: " + "; ".join(silent))

def pull(tok, keywords, days):
    tr, today = time_range(days)
    kws = [k.lower() for k in keywords]
    fields = ("campaign_name,adset_name,ad_name,ad_id,spend,impressions,"
              "inline_link_clicks,actions,frequency")
    ads = []
    seen_cur = set()
    for acct_id, acct_name, status, cur in accounts(tok):
        for r in paged(f"act_{acct_id}/insights",
                       {"level": "ad", "time_range": tr, "fields": fields, "limit": "500"}, tok):
            camp = r.get("campaign_name") or ""
            if not any(k in camp.lower() for k in kws):
                continue
            sp, _sym = money(r.get("spend"), cur)
            seen_cur.add(cur)
            imp = int(r.get("impressions") or 0)
            clk = int(r.get("inline_link_clicks") or 0)
            buys, leads = action_count(r, PURCHASE), max(action_count(r, LEAD),
                                                         action_count(r, REG))
            ads.append({
                "account": acct_name, "campaign": camp,
                "adset": r.get("adset_name"), "ad_name": r.get("ad_name"),
                "ad_id": r.get("ad_id"), "spend_gst": round(sp, 2), "currency": cur,
                "buyers": buys, "leads": leads,
                "imp": imp, "clicks": clk,
                "ctr": round(clk / imp * 100, 2) if imp else 0,
                "cpm_gst": round(sp / imp * 1000) if imp else 0,
                "freq": round(float(r.get("frequency") or 0), 2),
            })
    if len(seen_cur) > 1:
        print(f"WARNING: matched campaigns span {sorted(seen_cur)}. Costs are NOT "
              f"comparable across currencies - read each currency separately.",
              file=sys.stderr)
    if not ads:
        sys.exit(f"No campaigns matched {keywords} in the last {days} days "
                 f"(searched every account this token can see). "
                 f"Run with --list to see live campaign names.")

    # public links + status (only for ads that spent)
    for a in ads:
        if a["spend_gst"] <= 0:
            a["status"], a["fb"], a["ig"] = None, None, None
            continue
        d = get(a["ad_id"], {"fields": "effective_status,creative{effective_object_story_id,"
                                       "instagram_permalink_url}"}, tok)
        cr = (d or {}).get("creative") or {}
        a["status"] = (d or {}).get("effective_status")
        sid = cr.get("effective_object_story_id")
        a["fb"] = (f"https://www.facebook.com/{sid.split('_', 1)[0]}/posts/{sid.split('_', 1)[1]}"
                   if sid and "_" in sid else None)
        a["ig"] = cr.get("instagram_permalink_url")
    return ads, today


def report(ads, keywords, days, today):
    # never blend funnel types: group by campaign, each campaign gets its own table
    camps = {}
    for a in ads:
        camps.setdefault((a["account"], a["campaign"]), []).append(a)

    stamp = today.isoformat()
    slug = "_".join(k.replace(" ", "-") for k in keywords)
    os.makedirs(OUTDIR, exist_ok=True)
    jpath = os.path.join(OUTDIR, f"{slug}_{stamp}.json")
    json.dump({"pulled": stamp, "window_days": days, "keywords": keywords,
               "note": "All INR incl 18% GST.", "ads": ads},
              open(jpath, "w", encoding="utf-8"), indent=1)

    sections = []
    print(f"\nCampaigns matching {keywords} — last {days}d (all ₹ incl. GST)")
    for (acct, camp), rows in sorted(camps.items(),
                                     key=lambda kv: -sum(a["spend_gst"] for a in kv[1])):
        rows.sort(key=lambda a: -a["spend_gst"])
        sp = sum(a["spend_gst"] for a in rows)
        buys = sum(a["buyers"] for a in rows)
        leads = sum(a["leads"] for a in rows)
        # a campaign is judged on purchases if it has any, else on leads/registrations
        kind, n = ("buyer", buys) if buys else ("lead", leads)
        cost = f"₹{sp / n:,.0f}/{kind}" if n else "no results"
        print(f"\n■ {camp}  [{acct}]  ₹{sp:,.0f} · {n:.0f} {kind}s · {cost}")
        trs = []
        for a in rows:
            res = a["buyers"] if kind == "buyer" else a["leads"]
            cpr = round(a["spend_gst"] / res) if res else None
            print(f"  {(a['ad_name'] or '')[:44]:44} ₹{a['spend_gst']:>9,.0f} "
                  f"{res:>4.0f} {('₹%s' % format(cpr, ',')) if cpr else '—':>8} "
                  f"{a['ctr']:>5.2f}%  {a['status'] or ''}")
            fb = (f'<a class="b fb" href="{a["fb"]}" target="_blank">FB ↗</a>'
                  if a.get("fb") else '<span class="d">—</span>')
            ig = (f'<a class="b ig" href="{a["ig"]}" target="_blank">IG ↗</a>'
                  if a.get("ig") else '<span class="d">—</span>')
            trs.append(
                f'<tr><td class="n">{a["ad_name"] or ""}</td>'
                f'<td class="r">₹{a["spend_gst"]:,.0f}</td><td class="r">{res:.0f}</td>'
                f'<td class="r s">{("₹%s" % format(cpr, ",")) if cpr else "—"}</td>'
                f'<td class="r">{a["ctr"]:.2f}%</td><td class="r">₹{a["cpm_gst"]:,.0f}</td>'
                f'<td class="r">{a["freq"]:.2f}</td><td>{a["status"] or ""}</td>'
                f'<td>{fb} {ig}</td></tr>')
        sections.append(
            f'<h2>{camp} <span class="acct">{acct}</span></h2>'
            f'<div class="sub">₹{sp:,.0f} · {n:.0f} {kind}s · {cost} · cost column = per {kind}</div>'
            f'<table><thead><tr><th>Ad</th><th>Spend</th><th>{kind.title()}s</th>'
            f'<th>Cost/{kind}</th><th>CTR</th><th>CPM</th><th>Freq</th><th>Status</th>'
            f'<th>Links</th></tr></thead><tbody>{"".join(trs)}</tbody></table>')

    hpath = os.path.join(OUTDIR, f"{slug}_{stamp}.html")
    open(hpath, "w", encoding="utf-8").write(
        f"""<!doctype html><html><head><meta charset="utf-8">
<title>{" / ".join(keywords)} — {stamp}</title><style>
*{{box-sizing:border-box}}body{{font:14px/1.5 -apple-system,BlinkMacSystemFont,sans-serif;
margin:0;padding:28px;background:#f6f7f9;color:#16181d}}
h1{{margin:0 0 4px;font-size:23px}}h2{{font-size:16px;margin:30px 0 2px}}
h2 .acct{{font-size:12px;color:#6b7280;font-weight:400}}
.sub{{color:#6b7280;margin-bottom:10px;font-size:13px}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid #e5e7eb;
border-radius:10px;overflow:hidden;font-size:13px}}
th{{background:#111827;color:#fff;text-align:left;padding:9px 10px;font-size:11px;
text-transform:uppercase;letter-spacing:.05em}}
td{{padding:8px 10px;border-top:1px solid #f0f1f3}}
.r{{text-align:right;font-variant-numeric:tabular-nums}}.s{{font-weight:700}}
.n{{font-weight:600;max-width:300px}}
.b{{display:inline-block;padding:3px 8px;border-radius:5px;font-size:11px;font-weight:700;
text-decoration:none;color:#fff}}.fb{{background:#1877f2}}.ig{{background:#c13584}}
.d{{color:#d1d5db}}</style></head><body>
<h1>{" / ".join(keywords)}</h1>
<div class="sub">Pulled {stamp} · last {days} days · all ₹ <b>incl. 18% GST</b> ·
grouped by campaign — never compare cost/lead with cost/buyer across tables</div>
{"".join(sections)}</body></html>""")

    print(f"\nwrote {jpath}\nwrote {hpath}")
    _open_report(hpath)


def _open_report(path):
    """Open the HTML report in the default browser, on any OS."""
    try:
        if sys.platform == "darwin":
            os.system(f'open "{path}"')
        elif os.name == "nt":
            os.startfile(path)
        else:
            os.system(f'xdg-open "{path}" >/dev/null 2>&1 &')
    except Exception:
        pass  # the printed path is the fallback


def main():
    # Windows consoles default to cp1252 and cannot encode the rupee sign, which
    # crashed --list mid-report on 9 Sep 2026. Force UTF-8 on stdout/stderr.
    # That fix covered the console and missed the file writes, which take the same
    # platform default: on 18 Sep 2026 an `oct --days 2` pull printed all 100 ad rows,
    # then died writing the HTML report. The JSON had already landed (json.dump escapes
    # non-ASCII by default) so no data was lost, but the report never got written and
    # the run exited non-zero. Every open() in this file now names utf-8 explicitly.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    p = argparse.ArgumentParser()
    p.add_argument("keywords", nargs="*", help="campaign-name keywords (OR match)")
    p.add_argument("--days", type=int, default=14)
    p.add_argument("--list", action="store_true", help="list active campaigns instead")
    args = p.parse_args()
    tok = token()
    if args.list or not args.keywords:
        list_campaigns(tok, args.days)
        return
    ads, today = pull(tok, args.keywords, args.days)
    report(ads, args.keywords, args.days, today)


if __name__ == "__main__":
    main()
