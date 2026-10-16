"""Daily Meta ad report for LawSikho / SkillArbitrage.

Reads the System User token (ad-analysis-shared/.env), pulls every account the
token can see, applies SOP/02 + SOP/03 + SOP/10, and writes an HTML working file to the
system temp folder. The report itself goes in the chat reply, never an Artifact or a file
in this repo (SOP/10 Delivery, 28 Sep 2026).

    python daily_report.py                 # writes %TEMP%/daily_report.html
    python daily_report.py --out other.html

Routing: the token, never the Ads MCP. The MCP cannot read LawSikho Ad Account 4,
which carries live bootcamp spend (SOP/03, settled 9 Sep 2026).
"""
import argparse, collections, datetime, html, json, math, os, re, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ad-analysis-shared"))
import pull_ads as P

HERE = os.path.dirname(os.path.abspath(__file__))
CAL = os.path.join(HERE, "BOOTCAMP_CALENDAR.md")

# Bands from SOP/10, derived from SOP/02's own Rs 250/300/450 so a Rs 10 camp
# reproduces existing policy exactly rather than inventing a second standard.
SCALE, WATCH, BREAKER = 0.83, 1.30, 1.50
FREQ_FATIGUE, FREQ_FLAG, FREQ_ACT = 3.5, 4.5, 5.0
MIN_N = 20          # SOP/03: never judge an ad on fewer than 20 results
LEARN_EVENTS = 50   # Meta learning phase, per ad set per 7 days

MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def blank():
    return {"spend": 0.0, "buys": 0, "leads": 0, "imp": 0, "clicks": 0, "lpv": 0, "freq": 0.0}


def add(a, r):
    for k in ("spend", "buys", "leads", "imp", "clicks", "lpv"):
        a[k] += r[k]
    a["freq"] = max(a["freq"], r["freq"])


def fetch(tok, days=7):
    since = (datetime.date.today() - datetime.timedelta(days=days - 1)).isoformat()
    tr = json.dumps({"since": since, "until": datetime.date.today().isoformat()})
    fields = ("campaign_name,adset_name,ad_name,ad_id,spend,impressions,"
              "inline_link_clicks,actions,frequency")
    rows, accounts = [], []
    for acct_id, acct_name, status, cur in P.accounts(tok):
        got = P.paged("act_%s/insights" % acct_id,
                      {"level": "ad", "time_range": tr, "time_increment": "1",
                       "fields": fields, "limit": "500"}, tok)
        spent = False
        for r in got:
            sp = float(r.get("spend") or 0)
            if sp <= 0:
                continue
            spent = True
            rows.append({
                "acct": acct_name, "cur": cur, "day": r.get("date_start"),
                "camp": r.get("campaign_name") or "", "adset": r.get("adset_name") or "",
                "ad": r.get("ad_name") or "", "ad_id": r.get("ad_id"),
                # GST on INR only; USD/GBP accounts must never be grossed up (SOP/03).
                "spend": sp * (P.GST if cur == "INR" else 1.0),
                "imp": int(r.get("impressions") or 0),
                "clicks": int(r.get("inline_link_clicks") or 0),
                "lpv": P.action_count(r, ("landing_page_view",)),
                "buys": P.action_count(r, P.PURCHASE),
                "leads": max(P.action_count(r, P.LEAD), P.action_count(r, P.REG)),
                "freq": float(r.get("frequency") or 0),
            })
        accounts.append((acct_name, status, cur, spent))
    return rows, accounts


CREATIVE_FIELDS = ("creative{effective_object_story_id,instagram_permalink_url,object_type,"
                   "object_story_spec{link_data{link},video_data{call_to_action}},"
                   "asset_feed_spec{link_urls{website_url}}}")


def fetch_links(tok, ad_ids):
    """Public FB/IG permalinks and the landing page each ad points at.

    Batched 50 ids per call against the Graph root, so a few hundred ads cost a
    handful of requests instead of one each. These are the real post permalinks a
    person can open, never Ads Manager URLs.
    """
    links, ids = {}, sorted(set(i for i in ad_ids if i))
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        got = P.get("", {"ids": ",".join(chunk), "fields": CREATIVE_FIELDS}, tok)
        if "error" in got:
            continue
        for aid, node in (got or {}).items():
            cr = (node or {}).get("creative") or {}
            sid = cr.get("effective_object_story_id")
            fb = None
            if sid and "_" in sid:
                page, post = sid.split("_", 1)
                fb = "https://www.facebook.com/%s/posts/%s" % (page, post)
            oss = cr.get("object_story_spec") or {}
            lp = ((oss.get("link_data") or {}).get("link"))
            if not lp:
                # A video ad carries its destination under video_data, not link_data.
                # Missing this hid the landing page of 54 Senior AI video ads and made
                # two whole waves unrankable (10 Sep 2026).
                cta = (oss.get("video_data") or {}).get("call_to_action") or {}
                lp = (cta.get("value") or {}).get("link")
            if not lp:
                feed = (cr.get("asset_feed_spec") or {}).get("link_urls") or []
                if feed:
                    lp = feed[0].get("website_url")
            links[aid] = {"fb": fb, "ig": cr.get("instagram_permalink_url"), "lp": lp}
    return links


def load_funnels(path):
    """GrowthX funnel counts, as saved from the get_leads_report MCP tool.

    Keyed by funnel slug. Meta ads join to it through the landing page URL, which
    is always `https://<host>/f/<slug>` - the ad name almost never matches the
    funnel name (8%), the slug in the link matches 57% of ads and 90% of spend.
    """
    if not path or not os.path.exists(path):
        return {}, {}
    d = json.load(open(path, encoding="utf-8"))
    by_slug = {}
    for x in d.get("byFunnel", []):
        by_slug[(x.get("slug") or "").strip("/").lower()] = x
    return by_slug, {"total": d.get("total"), "paid": d.get("paid"),
                     "truncated": d.get("truncated"),
                     "revenue": sum(x.get("paidAmountTotal") or 0
                                    for x in d.get("byFunnel", []))}


def lp_slug(url):
    m = re.search(r"/f/([^/?#]+)", url or "")
    return m.group(1).strip("/").lower() if m else None


def gx_result(fn):
    """What GrowthX counts as this funnel's result, matched to what Meta counts.

    A free-registration funnel has no payment, so its result is the registration -
    comparing Meta's lead count against GrowthX's `paid` there reads as -100% when
    the two actually agree (2,857 vs 2,817 on USACC, 9 Sep 2026).
    """
    if not fn:
        return None
    if fn.get("funnelType") == "lead":
        return fn.get("total") or 0
    return fn.get("paid") or 0


def read_calendar():
    """Every camp whose dates have not passed, with days remaining."""
    if not os.path.exists(CAL):
        return []
    today, out = datetime.date.today(), []
    for line in open(CAL, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[1] not in ("MAIN", "RE"):
            continue
        # "31 Oct–2 Nov" crosses a month. The single-month pattern could not read it,
        # so every month-end camp was silently skipped by the coverage check
        # (Strategic HR and NCA, 31 Oct, found 17 Sep 2026).
        m2 = re.search(r"(\d+)\s+([A-Z][a-z]{2})\s*[-–]\s*(\d+)\s+([A-Z][a-z]{2})", cells[2])
        m = re.search(r"(\d+)\s*[-–]\s*(\d+)\s+([A-Z][a-z]{2})", cells[2])
        if m2:
            parts = (int(m2.group(1)), MONTHS.get(m2.group(2)), int(m2.group(3)), MONTHS.get(m2.group(4)))
        elif m:
            mon = MONTHS.get(m.group(3))
            parts = (int(m.group(1)), mon, int(m.group(2)), mon)
        else:
            continue
        if not parts[1] or not parts[3]:
            continue
        try:
            start = datetime.date(today.year, parts[1], parts[0])
            end = datetime.date(today.year, parts[3], parts[2])
        except ValueError:
            continue
        if end < today:
            continue
        # The calendar bolds the next camp with markdown asterisks; they are not
        # part of the name and were printing raw in the report.
        out.append({"camp": cells[0].strip("* "), "type": cells[1],
                    "dates": cells[2].strip("* "),
                    "start": start, "end": end, "days": (start - today).days})
    return sorted(out, key=lambda c: c["start"])


# Match a calendar camp to a live campaign by shared significant words.
STOP = {"the", "for", "and", "of", "as", "in", "to", "global", "career",
        "revolution", "work", "post", "innings", "bootcamp", "camp", "main"}


def words(s):
    # 2-letter words are kept: "IP law" and "HR" are whole camp names here, and
    # dropping them made the matcher report live camps as dark (9 Sep 2026).
    # CamelCase is split first: `WomenAI_FREE_3-5Oct` and `SeniorConsulting_BC_3-5Oct`
    # read as single words "womenai" and "seniorconsulting", so both live October
    # campaigns were reported as dark camps two days running (16-17 Sep 2026).
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    return set(w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 1 and w not in STOP)


COMMUNITY = ("community", "21day", "21 day", "14day")


def name_days(nm):
    """Day-of-month numbers embedded in a campaign name, e.g. Sep_12th, 19-21Sep.

    Deliberately not \\b-anchored: underscore is a word character, so \\b never
    fires inside `BC_19-21Sep2026` and the date guard silently matched nothing.
    That let the US Corporate Law campaign answer for the Corporate finance camp
    (9 Sep 2026). Four-digit runs starting 20 are years, not days.
    """
    out = set()
    for run in re.findall(r"\d+", nm):
        if len(run) <= 2 and 1 <= int(run) <= 31:
            out.add(int(run))
    return out


MONTH_WORDS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12}


def name_months(nm):
    """Months named in a campaign name: `3-5Oct2026`, `Sep_12th`, `05_07_October_2024`.

    A whole alphabetic run must BE a month, so `Marketing` is not March.
    """
    out = set()
    for run in re.findall(r"[A-Za-z]+", nm):
        mo = MONTH_WORDS.get(run.lower())
        if mo:
            out.add(mo)
    return out


def match_camp(camp, live_names):
    """Best live campaign for a calendar camp. A guess, like campaign_map_sync's."""
    cw = words(camp["camp"])
    if not cw:
        return None
    need = 2 if len(cw) > 2 else 1
    end = camp.get("end", camp["start"] + datetime.timedelta(days=2))
    span = [camp["start"] + datetime.timedelta(days=i) for i in range((end - camp["start"]).days + 1)]
    window = set(d.day for d in span)
    months = set(d.month for d in span)
    best, score = None, 0
    for nm in live_names:
        # The calendar lists bootcamps. A community campaign is a different product
        # and must never stand in for one - Community_Women_AI_June was answering
        # for the 19-21 Sep women bootcamp rerun.
        if any(k in nm.lower() for k in COMMUNITY):
            continue
        ov = len(cw & words(nm))
        nd = name_days(nm)
        nmo = name_months(nm)
        # A campaign that carries the camp's own dates needs only one shared word.
        # Two words was too strict for a name that abbreviates: `CorpFinance_bootcamp_
        # 17-19Oct_CBO` shares only "finance" with the Corporate Finance camp, and
        # `RID + ID BC 10-12 Oct 2026_CBO_LEAD` only "id" with Independent Director.
        # Both were reported dark on 23 Sep 2026 while spending in the same report -
        # the Bootcamps board and the coverage check contradicting each other.
        dated = bool(nd & window) and bool(nmo & months)
        if ov < (1 if dated else need) or ov <= score:
            continue
        if nd and not (nd & window):
            continue
        # Day numbers alone let `US Accounting_AND_Bookkeeping_Sep_12th` answer for the
        # 10-12 OCT camp (12 is in both), so two dark October camps read as covered
        # (17 Sep 2026). A named month that is not the camp's month rules it out.
        if nmo and not (nmo & months):
            continue
        best, score = nm, ov
    return best


def rupees(x):
    """Indian grouping: 12,34,567."""
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


def analyse(rows, accounts, cal):
    today = datetime.date.today().isoformat()
    yday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    camp = collections.defaultdict(blank)
    aset = collections.defaultdict(blank)
    ad = collections.defaultdict(blank)
    day = collections.defaultdict(blank)
    camp_day = collections.defaultdict(blank)
    acct_of = {}
    for r in rows:
        add(camp[r["camp"]], r)
        add(day[r["day"]], r)
        add(camp_day[(r["camp"], r["day"])], r)
        add(aset[(r["camp"], r["adset"])], r)
        add(ad[(r["camp"], r["ad"], r["ad_id"])], r)
        acct_of[r["camp"]] = r["acct"]
    # A campaign is judged on whichever event it actually optimises for.
    kind = dict((c, "buyers" if v["buys"] >= v["leads"] else "leads") for c, v in camp.items())

    def n_of(v, c):
        return v["buys"] if kind[c] == "buyers" else v["leads"]

    def cpr(v, c):
        n = n_of(v, c)
        return v["spend"] / n if n else None

    def group(c):
        if kind[c] == "leads":
            return "lead"
        low = c.lower()
        if any(k in low for k in ("community", "21day", "21 day", "14day")):
            return "community"
        return "bootcamp"

    findings = []
    live = list(camp.keys())

    # L0 - a dated camp with no campaign behind it. Nothing else can surface this.
    claimed = set()
    for c in cal:
        # Reruns are never advertised on this account - no RE camp has ever had an ad
        # campaign (Ruchika, 9 Sep 2026). Checking coverage on them produced five false
        # alarms on the first run, including a CRITICAL one on Corporate finance.
        # Only MAIN camps can be dark.
        if c["type"] == "RE":
            continue
        # One campaign covers one camp. `cal` is date-sorted, so the nearest camp
        # claims it first: the undated `MAIN - Academic Writing` campaign for 26 Sep
        # was also answering for the 24-26 Oct Academic Writing camp.
        hit = match_camp(c, [n for n in live if n not in claimed])
        if hit:
            claimed.add(hit)
        # The camps-ahead table used to re-run the matcher over every live campaign,
        # so a campaign already claimed by a nearer camp appeared against a later one
        # while the finding above correctly called that later camp dark. The table
        # said `MAIN - Academic Writing` and the top finding said "no live campaign",
        # in the same report (23 Sep 2026). One assignment, read by both.
        c["campaign"] = hit
        if hit is None:
            near = c["days"] <= 7
            findings.append({
                "sev": "critical" if near else "high", "layer": "L0",
                "what": "%s (%s, %s) has no live campaign" % (c["camp"], c["type"], c["dates"]),
                "why": "Camp opens in %d days. No cost figure can ever surface this, because "
                       "there is no spend to have a cost." % c["days"],
                "do": "Launch it today, or confirm it was cancelled.",
                "money": None, "sort": (0, c["days"])})

    # L0 - spent yesterday, nothing today.
    for c in live:
        if camp_day.get((c, yday), blank())["spend"] > 1000 and \
                camp_day.get((c, today), blank())["spend"] == 0:
            findings.append({
                "sev": "critical", "layer": "L0",
                "what": "%s spent yesterday but nothing today" % c,
                "why": "Ran Rs %s yesterday, zero so far today." % rupees(camp_day[(c, yday)]["spend"]),
                "do": "Check budget, schedule and delivery errors.",
                "money": camp_day[(c, yday)]["spend"], "sort": (1, 0)})

    # Group medians. SOP/10's ladder wants a trailing baseline for the funnel type,
    # not a campaign's own average - grading a campaign against itself makes a cheap
    # campaign's ordinary ads look like breaches. Global Patent ads at Rs 229 fired
    # the breaker against their own Rs 105 campaign while beating every business
    # target in the account (9 Sep 2026).
    gmed = {}
    for g in ("bootcamp", "lead", "community"):
        vals = sorted(x for x in (cpr(camp[c], c) for c in live
                                  if group(c) == g and camp[c]["spend"] > 5000) if x)
        if vals:
            gmed[g] = vals[len(vals) // 2]

    # Buyers per 1000 clicks, by group - the sanity check on a low load rate.
    def per_k(v, c):
        return (n_of(v, c) / v["clicks"] * 1000) if v["clicks"] else None

    gk = {}
    for g in ("bootcamp", "lead", "community"):
        vals = sorted(x for x in (per_k(camp[c], c) for c in live
                                  if group(c) == g and camp[c]["clicks"] > 200) if x)
        if vals:
            gk[g] = vals[len(vals) // 2]

    # L3 - the link or the page, not the ad.
    for c in live:
        v = camp[c]
        if v["clicks"] >= 200 and v["lpv"] > 0:
            load = v["lpv"] / v["clicks"] * 100
            # Guard from feedback-load-rate-is-not-traffic: a low load rate with
            # normal buyers-per-click means the page-view tag is under-firing, not
            # that the link is broken. This exact campaign produced that false
            # alarm once already; do not publish it twice.
            k, kb = per_k(v, c), gk.get(group(c))
            if k and kb and k >= kb * 0.7:
                findings.append({
                    "sev": "medium", "layer": "L3",
                    "what": "%s: page views look under-counted (%.0f%% load rate)" % (c, load),
                    "why": "Only %.0f%% of clicks register a page view, but it still buys at "
                           "%.1f per 1000 clicks against %.1f for its group. Buyers arrive, so "
                           "the page-view tag is under-firing - the link is not broken."
                           % (load, k, kb),
                    "do": "Fix the measurement, not the ad. Do not pause anything on this.",
                    "money": None, "sort": (8, -v["spend"])})
                continue
            if load < 40:
                findings.append({
                    "sev": "critical", "layer": "L3",
                    "what": "%s: only %.0f%% of clicks reach the page" % (c, load),
                    "why": "%s page views from %s clicks over 7 days. Paying for clicks that "
                           "never arrive." % (rupees(v["lpv"]), rupees(v["clicks"])),
                    "do": "Open the ad's link in a browser. Check the destination and page speed.",
                    "money": v["spend"], "sort": (2, -v["spend"])})
            elif load < 60:
                findings.append({
                    "sev": "high", "layer": "L3",
                    "what": "%s: %.0f%% of clicks reach the page" % (c, load),
                    "why": "Below the 60%% investigate line.",
                    "do": "Open the link and time the page load.",
                    "money": v["spend"], "sort": (3, -v["spend"])})

    # L2 - circuit breaker, against the funnel type's median, never the campaign's own.
    for (c, a, aid), v in ad.items():
        base, this, n = gmed.get(group(c)), cpr(v, c), n_of(v, c)
        if base and this and n >= MIN_N and this > base * BREAKER:
            findings.append({
                "sev": "high", "layer": "L2",
                "what": "%s is running %.1fx the going rate" % (a, this / base),
                "why": "Rs %s against Rs %s, the median for %s campaigns, on %d results "
                       "(margin +-%.0f%%). Its campaign is %s."
                       % (rupees(this), rupees(base), group(c), int(n),
                          196 / math.sqrt(n), c),
                "do": "Pause this ad. Past the circuit breaker with enough data to act.",
                "money": v["spend"], "sort": (4, -v["spend"])})

    # L6 - ad sets too thin to ever leave the learning phase.
    for c in live:
        base = cpr(camp[c], c)
        if not base:
            continue
        floor = LEARN_EVENTS * base / 7
        thin = [(s, v) for (cc, s), v in aset.items()
                if cc == c and v["spend"] / 7 < floor and v["spend"] > 3000]
        if len(thin) >= 3:
            waste = sum(v["spend"] for _, v in thin)
            got = sum(n_of(v, c) for _, v in thin)
            findings.append({
                "sev": "medium", "layer": "L6",
                "what": "%s: %d ad sets funded below the learning floor" % (c, len(thin)),
                "why": "Rs %s over 7 days bought %d results across them. An ad set needs about "
                       "Rs %s a day at this cost to reach 50 events a week and stabilise."
                       % (rupees(waste), int(got), rupees(floor)),
                "do": "Consolidate into the funded sets, or close them.",
                "money": waste, "sort": (5, -waste)})

    # L1 - frequency.
    for (c, a, aid), v in ad.items():
        if v["freq"] >= FREQ_FLAG and v["spend"] > 3000:
            findings.append({
                "sev": "high" if v["freq"] >= FREQ_ACT else "medium", "layer": "L1",
                "what": "%s at frequency %.1f" % (a, v["freq"]),
                "why": "The same people are seeing it repeatedly.",
                "do": "Duplicate to a new audience. Raising its budget makes this worse.",
                "money": v["spend"], "sort": (6, -v["spend"])})

    # L6 - money in the wrong place.
    for c in live:
        tot_s, tot_n = camp[c]["spend"], n_of(camp[c], c)
        if tot_n < 30 or tot_s < 20000:
            continue
        for (cc, a, aid), v in ad.items():
            if cc != c or v["spend"] < 5000:
                continue
            ns = n_of(v, c)
            share_s = v["spend"] / tot_s
            share_n = ns / tot_n if tot_n else 0
            if share_n and share_s / share_n > 1.4 and ns >= MIN_N:
                findings.append({
                    "sev": "medium", "layer": "L6",
                    "what": "%s takes %.0f%% of spend for %.0f%% of results"
                            % (a, share_s * 100, share_n * 100),
                    "why": "Rs %s for %d results in %s." % (rupees(v["spend"]), int(ns), c),
                    "do": "Move budget to the cheaper ads in this campaign.",
                    "money": v["spend"], "sort": (7, -v["spend"])})

    scale = []
    for (c, a, aid), v in ad.items():
        base, this, n = gmed.get(group(c)), cpr(v, c), n_of(v, c)
        if base and this and n >= MIN_N and this <= base * SCALE:
            scale.append({"camp": c, "ad": a, "cpr": this, "base": base,
                          "n": n, "spend": v["spend"]})
    scale.sort(key=lambda x: x["cpr"] / x["base"])

    findings.sort(key=lambda f: f["sort"])
    return dict(accounts=accounts, cal=cal, camp=camp, aset=aset, ad=ad, day=day,
                camp_day=camp_day, kind=kind, acct_of=acct_of, group=group,
                n_of=n_of, cpr=cpr, findings=findings, scale=scale, gmed=gmed,
                # RE rows never carry a campaign: reruns are not advertised on this
                # account, so a fuzzy match there is noise (the 3-5 Oct Senior AI
                # campaign was standing in for the 31 Oct Senior AI rerun).
                match=lambda c: c.get("campaign"),
                today=today, yday=yday, live=live)


def reconcile(data, by_slug):
    """Per ad: what Meta claims, what the funnel platform recorded, and the gap.

    Meta attributes a result to the ad that earned the click; GrowthX records the
    payment that actually came through the page. They are measuring different
    things, so a gap is information rather than an error - but a large one means
    the CPP being optimised against is not the CPP being banked.
    """
    links, ad = data.get("links", {}), data["ad"]
    n_of = data["n_of"]
    # Reconcile per FUNNEL, not per ad. Several ads routinely point at one landing
    # page, and comparing each ad against that page's combined total produced
    # nonsense - one Retired ID ad read +1625% against 2,053 leads that a dozen ads
    # had produced between them (9 Sep 2026).
    grouped, unmatched, nolink = {}, 0, 0
    for (c, a, aid), v in ad.items():
        s = lp_slug((links.get(aid) or {}).get("lp"))
        if not s:
            nolink += 1
            continue
        if s not in by_slug:
            unmatched += 1
            continue
        g = grouped.setdefault(s, {"spend": 0.0, "meta": 0, "ads": [], "camps": set()})
        g["spend"] += v["spend"]
        g["meta"] += n_of(v, c)
        g["ads"].append(a)
        g["camps"].add(c)

    out = []
    for s, g in grouped.items():
        fn = by_slug[s]
        gx_n, st = gx_result(fn), (fn.get("byStatus") or {})
        out.append({
            "slug": s, "funnel": fn.get("funnel") or s, "ads": sorted(g["ads"]),
            "n_ads": len(g["ads"]), "camp": sorted(g["camps"])[0] if g["camps"] else "",
            "spend": g["spend"], "meta": g["meta"], "gx": gx_n,
            "gap": ((gx_n - g["meta"]) / g["meta"] * 100) if g["meta"] else None,
            "gx_cost": (g["spend"] / gx_n) if gx_n else None,
            "form_only": st.get("Form only", 0),
            "started": st.get("Checkout started", 0),
            "expired": st.get("Expired", 0),
            "failed": st.get("Failed", 0),
            "revenue": fn.get("paidAmountTotal") or 0,
            "ftype": fn.get("funnelType"), "group": fn.get("group"),
        })
    out.sort(key=lambda x: -x["spend"])
    covered = sum(x["spend"] for x in out)
    total = sum(v["spend"] for v in ad.values())
    return {"rows": out, "unmatched": unmatched, "nolink": nolink,
            "covered": covered, "total": total,
            "pct": (covered / total * 100) if total else 0}


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "daily_report.html"))
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--funnels", default=os.path.join(HERE, "funnels_today.json"),
                    help="JSON saved from the GrowthX get_leads_report MCP tool, "
                         "covering exactly the same dates as --days")
    args = ap.parse_args()

    import report_render
    tok = P.token()
    rows, accounts = fetch(tok, args.days)
    if not rows:
        sys.exit("No spend found in any account over the last %d days. "
                 "That is unusual - check the token and account status before "
                 "reporting it as a result." % args.days)
    data = analyse(rows, accounts, read_calendar())
    data["links"] = fetch_links(tok, [r["ad_id"] for r in rows])
    by_slug, totals = load_funnels(args.funnels)
    data["gx"], data["gx_totals"] = by_slug, totals
    data["gx_days"] = args.days
    data["recon"] = reconcile(data, by_slug)

    # A big gap between what Meta claims and what the funnel banked means the cost
    # being optimised against is not the cost being paid. Only worth raising with
    # enough results behind it and real money on the ad.
    for x in data["recon"]["rows"]:
        if x["gap"] is None or x["meta"] < MIN_N or x["spend"] < 10000:
            continue
        if abs(x["gap"]) >= 30:
            over = x["gap"] < 0
            data["findings"].append({
                "sev": "medium", "layer": "L7",
                "what": "%s: Meta says %d, the funnel recorded %d (%+.0f%%)"
                        % (x["funnel"], int(x["meta"]), int(x["gx"]), x["gap"]),
                "why": "Meta credits the ad that earned the click; the funnel records what "
                       "came through the page. %s"
                       % (("Meta is claiming more than the funnel banked, so the real cost "
                           "per result is nearer Rs %s than Meta's figure."
                           % rupees(x["gx_cost"])
                           # gx_cost is None when the funnel recorded nothing at all over
                           # the window, which is also the deepest possible gap (-100%).
                           # Formatting it crashed the whole run after the pull had already
                           # succeeded (1 Oct 2026); a stale funnels file makes it routine.
                           if x["gx_cost"] is not None else
                           "The funnel recorded nothing over this window, so no cost per "
                           "result can be computed from it. Check the funnels file is for "
                           "the same dates before trusting the gap.") if over else
                          "The page received more than Meta sent it, which usually means "
                          "other traffic reaches it too - Google, WhatsApp or organic. Do "
                          "not credit this ad with the difference."),
                "do": "Trust the funnel number for this page. Check the pixel if the gap holds.",
                "money": x["spend"], "sort": (9, -x["spend"])})
    data["findings"].sort(key=lambda f: f["sort"])

    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        fh.write(report_render.render(data))

    # The findings also go to stdout, so a scheduled run says what it found
    # without anyone opening the page.
    print("ACT TODAY (%d)" % len(data["findings"]))
    for f in data["findings"][:14]:
        print("  [%s/%s] %s" % (f["sev"].upper(), f["layer"], f["what"]))
        print("      -> %s" % f["do"])
    print("\nwrote %s" % args.out)


if __name__ == "__main__":
    main()
