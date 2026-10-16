#!/usr/bin/env python3
"""Emit manifest.json for a media-buyer kit — Option 1 of the kit-importer contract.

The importer (their side) turns a kit zip into draft funnels. With manifest.json at the zip
root it does zero guessing; without it, it falls back to parsing the README. This writes the
manifest so the fallback never runs.

Usage:
  python3 engine/make_manifest.py <kit_dir>                     dry run: print manifest + warnings
  python3 engine/make_manifest.py <kit_dir> --write             write <kit_dir>/manifest.json
  python3 engine/make_manifest.py <kit_dir> --write --stamp     also stamp '<!-- Deploy as /f/<slug> -->'
                                                             as line 1 of each LP (fallback source #1)
  python3 engine/make_manifest.py <kit_dir> --check             validate an existing manifest.json

Build every kit with `--write --stamp`, then gate the zip on `--check`.

THE SLUG IS THE LIVE URL. It is only ever read from something that documents it:

  1. kit_meta.json "slugs"                    (explicit override, always wins)
  2. the /f/<slug> in the LP's own COMMENT    (the page describes itself)
  3. a slug column in the README table        (Final URL / Funnel slug / GrowthX slug / …)
  4. a 'slug:' line in that ad's README or ad_copy.md block
  5. the filename                             — LAST RESORT, warns loudly, FAILS --check

Rule 5 is the bug this file once had: the 13 Aug 2026 bulk run derived slugs from filenames
and shipped the wrong deploy URL in 13 of 26 kits ('citrin-india' for a page whose brief says
'/us-acc-citrin-india'; '01-courtroom-calendar' for '/legalai-courtroom'). A filename is a
build-time label, not a URL. Note too that a /f/… in page SCRIPT is the checkout destination,
not this page's slug — US_Accounting's five LPs share one REG_URL, and reading it as the slug
would collapse five landing pages onto a single URL.

Everything else is derived from the kit folder itself: the README mapping table, the per-ad
blocks, and the LP HTML. Drop a kit_meta.json in the kit root to override anything the
derivation gets wrong:

    {
      "kit": "dataprivacy-mediabuyer-29-31aug",
      "brand": "skillarbitrage",
      "category": "growthcamp",
      "product": "Data Privacy Growth Camp",
      "price": "10", "currency": "INR",
      "tag": "dpdp-growthcamp",
      "slugs":        {"lp_01_it_security.html": "dpdp-it-security"},
      "names":        {"lp_01_it_security.html": "IT & Security"},
      "redeployOver": {"lp_01_it_security.html": "old-live-slug"}
    }

Established 13 Aug 2026, per the kit-importer format request.
"""
import sys, os, re, json, glob, html

CATEGORIES = ("paid_bootcamp", "free_bootcamp", "growthcamp", "community")
CTA_MAX = 64
PLACEHOLDER_PAY = ("PAYMENT_LINK_PENDING", "PAYMENT_PENDING", "BUY_URL_PENDING", "TODO_PAYMENT")


# ---------------------------------------------------------------- kit reading

def read_docs(kit):
    """(readme_text, all_text). Header fields come from the README/brief only — ad_copy*.md
    sorts before README.md and would otherwise hijack every 'first match in the head' rule."""
    def cat(paths):
        return "\n".join(open(p, encoding="utf-8", errors="replace").read()
                         for p in sorted(set(paths)))
    readme = cat(glob.glob(os.path.join(kit, "README*")) +
                 glob.glob(os.path.join(kit, "*BRIEF*.md")))
    copy = cat(glob.glob(os.path.join(kit, "ad_copy*.md")))
    return readme, (readme + "\n" + copy)


def kebab(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def derive_product(doc, kit):
    m = re.search(r"^#\s+(.+)$", doc, re.M)
    if not m:
        return os.path.basename(os.path.abspath(kit)).replace("_", " ")
    t = m.group(1)
    t = re.split(r"\s+[—·|]\s+|\s+--\s+", t)[0]          # drop " — media buyer kit", " · 26 Jul"
    t = re.sub(r"\s*\(.*?\)\s*$", "", t)                  # drop trailing "(packaged 9 Aug 2026)"
    t = re.sub(r"\b(media[- ]buyer\s+)?kit\b\s*$", "", t, flags=re.I)
    return t.strip(" -–—·:") or os.path.basename(os.path.abspath(kit))


# Product lines whose brand is fixed by the SKILL's branding rule, used only when the README
# does not declare a brand outright.
LAWSIKHO_PRODUCTS = ("patent", "uscl", "sqe", "judiciary", "litigation", "arbitration",
                     "ca bar", "criminal", "corplit", "legal ai", "ip law")


def derive_brand(readme, product):
    m = re.search(r"\*{0,2}Brand\*{0,2}\s*:?\*{0,2}\s*([A-Za-z][A-Za-z ]{2,20})", readme)
    if m:
        b = kebab(m.group(1).split("(")[0])
        for known in ("skillarbitrage", "lawsikho"):
            if known in b:
                return known, True
    has_ls, has_sa = "LawSikho" in readme, "SkillArbitrage" in readme
    if has_sa and not has_ls: return "skillarbitrage", True
    if has_ls and not has_sa: return "lawsikho", True
    p = product.lower()
    if any(k in p for k in LAWSIKHO_PRODUCTS):
        return "lawsikho", False
    counted = "lawsikho" if readme.count("LawSikho") > readme.count("SkillArbitrage") else "skillarbitrage"
    return counted, False


# \b before Rs/INR matters: these are searched case-insensitively, and without it the 'rs' in
# 'anchors,' matches and captures a bare comma.
MONEY = r"(?:₹\s?|\bRs\.?\s?|\bINR\s?)(\d[\d,]*)"


def offer_scope(readme):
    """The H1 plus the bold anchor lines under it — where the offer is actually stated.
    Deeper body text is full of salary and market figures that must never be read as a price."""
    h1 = re.search(r"^#\s+(.+)$", readme, re.M)
    return (h1.group(1) if h1 else "") + "\n" + readme[:800]


def is_free_funnel(readme):
    # space-separated only: 'free-registration' inside a campaign name or URL is not a funnel type
    return bool(re.search(r"\bFREE\s+(registration|bootcamp|camp|signup|sign\s?up)"
                          r"|Funnel\*{0,2}:?\*{0,2}\s*\**FREE", readme[:2500], re.I))


def derive_price(readme):
    """('10', 'INR') for a paid offer, (None, None) when the README states no price."""
    labelled = re.search(r"(?:Price|Offer|Entry|Ticket|Fee)\b[^\n]{0,40}?" + MONEY, readme[:2500], re.I)
    if labelled:
        v = labelled.group(1).replace(",", "")
        return (None, None) if v == "0" else (v, "INR")
    if is_free_funnel(readme):
        return None, None
    m = re.search(MONEY, offer_scope(readme))
    if m:
        v = m.group(1).replace(",", "")
        if v != "0" and len(v) <= 6:
            return v, "INR"
    return None, None


def derive_category(readme, price):
    """Exactly one of CATEGORIES. Order matters: an explicitly FREE funnel is a free_bootcamp
    even when the page also talks about the community that comes with it."""
    offer = offer_scope(readme)
    if is_free_funnel(readme):
        return "free_bootcamp"
    if re.search(r"\bcommunit(y|ies)\b", offer, re.I):
        return "community"
    if re.search(r"growth\s*camp", offer, re.I):
        return "growthcamp"
    return "free_bootcamp" if price is None else "paid_bootcamp"


# ------------------------------------------------------- README slug plumbing

# Header wording for the slug column, across every kit README in the archive:
# "Final URL", "Funnel slug", "GrowthX slug", "Suggested slug", "LP slug", "Deploy slug".
SLUG_COL = re.compile(r"final url|live url|(deploy(ed)?|funnel|growthx|suggested|lp)\s*(url|slug)"
                      r"|^slug$", re.I)


def parse_mapping(doc):
    """lp filename -> {'ad': ad_id, 'final_url': slug or None} from the ad-to-LP table."""
    out, final_col = {}, None
    for line in doc.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if any(SLUG_COL.search(c) for c in cells):
            final_col = next(i for i, c in enumerate(cells) if SLUG_COL.search(c))
            continue
        lp = next((re.search(r"(lp_[a-z0-9_]+\.html)", c, re.I) for c in cells
                   if re.search(r"lp_[a-z0-9_]+\.html", c, re.I)), None)
        if not lp:
            continue
        ad = next((re.sub(r"\.png$", "", c) for c in cells if c.lower().endswith(".png")), None)
        url = None
        if final_col is not None and final_col < len(cells):
            cand = cells[final_col]
            if cand and cand not in ("—", "-", "none", "TBD"):
                url = cand
        out[lp.group(1)] = {"ad": ad, "final_url": url}
    return out


# The slug label inside a per-ad block. Kits write it as "Suggested LP slug:",
# "Suggested URL slug:", "LP slug:", "GrowthX slug `x`" or plain "slug `x`".
SLUG_LABEL = re.compile(r"(?:suggested\s+)?(?:lp|url|growthx|funnel|deploy)?\s*slug\s*:?\**\s*"
                        r"[`\"']?/?([A-Za-z0-9][A-Za-z0-9/_-]*)", re.I)


def parse_slug_hints(doc):
    """Suggested slug per ad id AND per lp filename, from the per-ad blocks in a README/ad_copy.

    Headings vary far more than the original '## <ad>.png' rule allowed:
        ## us02_citrin_tripled.png → landing_pages/lp_citrin_india.html
        ## 2. us02_citrin_tripled.png → landing_pages/lp_citrin_india.html
        ## w2_01_govt_order — Govt-job aspirants        (pairs with lp_w2_01_govt_order.html)
        ## cw1 — Examiner post decoded → lp_cw1_examiner_decoded.html
    so split on headings and key each block by every ad id and LP filename it mentions.
    """
    hints = {}
    for m in re.finditer(r"^#{2,3}\s+(.*?)$(.*?)(?=^#{2,3}\s|\Z)", doc, re.S | re.M):
        head, block = m.group(1), m.group(2)
        sec = head + "\n" + block
        s = SLUG_LABEL.search(sec)
        if not s:
            continue
        slug = s.group(1)
        for ad in re.findall(r"([A-Za-z0-9_]+)\.png", sec):
            hints.setdefault(ad, slug)
        for lp in re.findall(r"(lp_[A-Za-z0-9_-]+\.html)", sec):
            hints.setdefault(lp, slug)
        # heading that names an ad/LP code with no .png or .html, e.g. "## w2_01_govt_order"
        code = re.match(r"\s*(?:\d+[.)]\s*)?([A-Za-z][A-Za-z0-9_]{3,})", head)
        if code:
            hints.setdefault(code.group(1), slug)
            hints.setdefault(f"lp_{code.group(1)}.html", slug)
    return hints


def clean_slug(raw):
    """Normalise a slug hint to a bare deploy slug, or None if it's really a filename."""
    if not raw:
        return None
    s = raw.strip().strip("`\"'*").strip()
    s = re.sub(r"^https?://[^/]+", "", s)
    s = s.strip("/")
    s = re.sub(r"^f/", "", s)
    if s.lower().endswith(".html") or s.lower().startswith("lp_"):
        return None
    s = kebab(s)
    return s or None


def slug_from_filename(fn):
    return kebab(re.sub(r"^lp[_-]", "", os.path.splitext(fn)[0]))


# Contact sheets and QA boards live alongside the LPs but are not funnels.
NOT_LPS = ("index.html", "preview_board.html", "evidence_bank.html", "contact_sheet.html")


def is_not_a_landing_page(fn):
    return fn.startswith("_") or fn.lower() in NOT_LPS or fn.lower().startswith("preview")


ACRONYMS = {"ai", "ml", "it", "hr", "crm", "ca", "cs", "gcc", "bfsi", "bpo", "kpo", "lpo",
            "sqe", "us", "uk", "id", "rid", "dpdp", "rcm", "bgv", "tpa", "gst", "ipo", "ip",
            "qa", "omr", "sme", "b2b", "esg", "cxo", "ma", "nda", "kyc", "llb", "llm"}


def humanize(fn):
    words = [w for w in re.split(r"[_\-]+", re.sub(r"^lp[_-]", "", os.path.splitext(fn)[0])) if w]
    while words and words[0].isdigit():      # "01_it_security" -> "IT Security"
        words.pop(0)
    if len(words) > 1 and words[-1].lower() == "lp":
        words.pop()
    out = [w.upper() if w.lower() in ACRONYMS else w.capitalize() for w in words]
    return " ".join(out) or os.path.splitext(fn)[0]


# --------------------------------------------------------------- LP HTML bits

TAG = re.compile(r"<[^>]+>")


def _text(frag):
    # Strip tags to NOTHING, not to a space: CTA labels wrap currency inline
    # (`— <span class="rs">₹</span>100 →`), and substituting a space produced
    # 'Get the brief — ₹ 100 →' — a label that matches no button on the page.
    return re.sub(r"\s+", " ", html.unescape(TAG.sub("", frag))).strip()


COMMENT = re.compile(r"<!--(.*?)-->", re.S)


def lp_deploy_comment(src):
    """The deploy slug the page declares, read ONLY from HTML comments.

    Kits word this line three ways, all seen in the archive:
        <!-- Deploy as /f/id-route-break-in -->
        <!-- D2 angles LP · … Deploy as GrowthX paid funnel at /f/id-community-quiz-omr … -->
        <!-- LegalAI refresh LP · … GrowthX paid funnel /f/legalai-courtroom … -->
    so match the /f/<slug> token itself rather than a fixed phrase.

    Comments only, deliberately: a `/f/…` in page script is the CHECKOUT destination, not
    this page's URL. US_Accounting's five LPs each set REG_URL to one shared registration
    funnel — reading that as the deploy slug would collapse five pages onto one URL.
    """
    for c in COMMENT.findall(src[:8000]):
        m = re.search(r"/f/([a-z0-9][a-z0-9-]*)", c, re.I)
        if m:
            return clean_slug(m.group(1))
    return None


def lp_ctas(src):
    """CTA button/link text, verbatim, in document order."""
    labels, seen = [], set()

    def add(t):
        if t and t not in seen and len(t) <= 120:
            seen.add(t); labels.append(t)

    # attrs must tolerate '>' inside quoted values (onclick handlers do this) or the tag ends
    # early and the label comes out as '">Show me the road…'
    el = r"""<(a|button)\b((?:"[^"]*"|'[^']*'|[^>])*)>(.*?)</\1>"""
    for m in re.finditer(el, src, re.S | re.I):
        attrs, inner = m.group(2), m.group(3)
        # kits use either .cta or .btn for the buy button; both are in play across the archive
        if re.search(r'class\s*=\s*["\'][^"\']*\b(cta|btn)\b', attrs, re.I) or "openPay(" in attrs:
            add(_text(inner))
    if not labels:  # no .cta class in this LP — fall back to buy-intent wording
        for m in re.finditer(el, src, re.S | re.I):
            t = _text(m.group(3))
            if re.match(r"^(join|enrol|enroll|register|buy|pay|book|get|reserve|claim)\b", t, re.I) \
               and len(t) <= 80:
                add(t)
    return labels


def lp_all_control_text(src):
    """Rendered text of every <a>/<button> on the page — what a buyer actually sees."""
    el = r"""<(a|button)\b((?:"[^"]*"|'[^']*'|[^>])*)>(.*?)</\1>"""
    return [_text(m.group(3)) for m in re.finditer(el, src, re.S | re.I) if _text(m.group(3))]


def lp_pay_placeholder(src):
    return any(p in src for p in PLACEHOLDER_PAY)


# ------------------------------------------------------------------ the build

def build(kit):
    """Return (manifest_dict, warnings_list)."""
    warn = []
    kit = kit.rstrip("/")
    base = os.path.basename(os.path.abspath(kit))
    readme, doc = read_docs(kit)
    if not readme:
        warn.append("no README/brief markdown found — most header fields are guesses")

    meta_path = os.path.join(kit, "kit_meta.json")
    meta = json.load(open(meta_path, encoding="utf-8")) if os.path.exists(meta_path) else {}

    price, currency = derive_price(readme)
    product = derive_product(readme, kit)
    brand, brand_declared = derive_brand(readme, product)
    if not brand_declared and "brand" not in meta:
        warn.append(f"README does not declare a brand — inferred '{brand}' from the product line. "
                    f"Add '**Brand: …**' to the README or set it in kit_meta.json.")
    m = {
        "kit": meta.get("kit", kebab(base)),
        "brand": meta.get("brand", brand),
        "category": meta.get("category", derive_category(readme, price)),
        "product": meta.get("product", product),
    }
    price = meta.get("price", price)
    currency = meta.get("currency", currency)
    if price:
        m["price"], m["currency"] = str(price), currency or "INR"
    m["tag"] = meta.get("tag", kebab(product))

    if not price and m["category"] != "free_bootcamp":
        warn.append(f"category is '{m['category']}' but no price is stated in the README — "
                    f"the importer will treat this as a free funnel. Add the price to the README "
                    f"or set it in kit_meta.json.")
    if m["category"] not in CATEGORIES:
        warn.append(f"category '{m['category']}' is not one of {CATEGORIES} — set it in kit_meta.json")
    if m["category"] == "growthcamp" and re.search(r"GrowthCamp", doc) and not re.search(r"Growth Camp", doc):
        warn.append("README writes 'GrowthCamp' without a space — their auto-detector wants 'Growth Camp' "
                    "(manifest.json makes this cosmetic, but fix it for the humans)")

    mapping = parse_mapping(doc)
    hints = parse_slug_hints(doc)
    lps = sorted(glob.glob(os.path.join(kit, "landing_pages", "*.html"))) \
        or sorted(glob.glob(os.path.join(kit, "lp", "*.html")))
    lps = [p for p in lps if not is_not_a_landing_page(os.path.basename(p))]
    if not lps:
        warn.append("no landing pages found — nothing importable in this kit")

    funnels, primaries = [], {}
    for path in lps:
        fn = os.path.basename(path)
        src = open(path, encoding="utf-8", errors="replace").read()
        rel = os.path.relpath(path, kit).replace(os.sep, "/")

        # slug, in the importer's own priority order
        slug = (clean_slug(meta.get("slugs", {}).get(fn))
                or lp_deploy_comment(src)
                or clean_slug((mapping.get(fn) or {}).get("final_url"))
                or clean_slug(hints.get((mapping.get(fn) or {}).get("ad") or ""))
                or clean_slug(hints.get(fn)))
        if not slug:
            # A filename is a build-time label, not a URL. Deriving one here is what shipped
            # `citrin-india` for a page whose brief says `/us-acc-citrin-india`, so this is a
            # loud last resort: --check treats a filename-derived slug as a failure.
            slug = slug_from_filename(fn)
            warn.append(f"{fn}: NO SLUG DECLARED ANYWHERE — fell back to the filename ('{slug}'), "
                        f"which is probably NOT the live URL. Add a '<!-- Deploy as /f/<slug> -->' "
                        f"line to the LP, a slug column to the README table, or set it in "
                        f"kit_meta.json \"slugs\".")

        ctas = lp_ctas(src)
        if not ctas:
            warn.append(f"{fn}: no CTA button text found — importer cannot auto-detect the button")
        for c in ctas:
            if len(c) > CTA_MAX:
                warn.append(f"{fn}: CTA '{c[:40]}…' is {len(c)} chars (>{CTA_MAX}) — importer warns on this")
        if ctas:
            primaries[fn] = ctas[0]
        if lp_pay_placeholder(src):
            warn.append(f"{fn}: checkout link is still a placeholder — wire the real payment link before zipping")

        funnels.append({
            "html": rel,
            "slug": slug,
            "name": meta.get("names", {}).get(fn, humanize(fn)),
            "ctaLabels": ctas,
            "redeployOver": meta.get("redeployOver", {}).get(fn),
        })

    if len(set(primaries.values())) > 1:
        warn.append("CTA text differs across landing pages in this kit: "
                    + "; ".join(f"{k} → '{v}'" for k, v in sorted(primaries.items()))
                    + " — use one consistent string")

    dupes = {f["slug"] for f in funnels if [g["slug"] for g in funnels].count(f["slug"]) > 1}
    for d in sorted(dupes):
        warn.append(f"duplicate slug '{d}' across landing pages — each LP needs its own live URL")

    # HOLD ads: statics with no landing page are noise in the zip
    pngs = {os.path.splitext(os.path.basename(p))[0]
            for p in glob.glob(os.path.join(kit, "ads", "*.png"))}
    mapped = {v["ad"] for v in mapping.values() if v.get("ad")}
    # Only meaningful when the README actually has an ad-to-LP mapping table to read; without
    # one, every static looks orphaned.
    orphan = sorted(pngs - mapped) if mapped else []
    if orphan:
        warn.append(f"{len(orphan)} ad static(s) have no landing page ({', '.join(orphan[:4])}"
                    f"{'…' if len(orphan) > 4 else ''}) — move them to hold/ or leave them out of the zip")

    m["funnels"] = funnels
    return m, warn


# ------------------------------------------------------------------ validate

def validate(kit):
    """Errors (list of str) for an existing manifest.json. Empty list == valid."""
    kit = kit.rstrip("/")
    p = os.path.join(kit, "manifest.json")
    if not os.path.exists(p):
        return ["no manifest.json in kit root — run: python3 engine/make_manifest.py %s --write" % kit]
    try:
        m = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return [f"manifest.json is not valid JSON: {e}"]
    if not isinstance(m, dict):
        return ["manifest.json is not a kit manifest (expected a JSON object with 'kit'/'funnels')"]

    errs = []
    for f in ("kit", "brand", "category", "product", "tag", "funnels"):
        if not m.get(f):
            errs.append(f"manifest.json: missing '{f}'")
    if m.get("category") not in CATEGORIES:
        errs.append(f"manifest.json: category '{m.get('category')}' not one of {CATEGORIES}")
    if ("price" in m) != ("currency" in m):
        errs.append("manifest.json: price and currency must appear together (omit both for free funnels)")
    if not isinstance(m.get("funnels"), list) or not m.get("funnels"):
        errs.append("manifest.json: 'funnels' must be a non-empty list")
        return errs

    slugs = set()
    for i, f in enumerate(m["funnels"]):
        tag = f.get("html") or f"funnels[{i}]"
        for k in ("html", "slug", "name", "ctaLabels"):
            if k not in f:
                errs.append(f"manifest.json: {tag} missing '{k}'")
        if "redeployOver" not in f:
            errs.append(f"manifest.json: {tag} missing 'redeployOver' (use null if it is not a redeploy)")
        if f.get("html") and not os.path.exists(os.path.join(kit, f["html"])):
            errs.append(f"manifest.json: {tag} points at a file that is not in the kit")
        s = f.get("slug") or ""
        if s.startswith("/") or s.endswith(".html"):
            errs.append(f"manifest.json: {tag} slug '{s}' must be a bare deploy slug, not a path or filename")
        if s in slugs:
            errs.append(f"manifest.json: duplicate slug '{s}'")
        slugs.add(s)
        for c in f.get("ctaLabels") or []:
            if len(c) > CTA_MAX:
                errs.append(f"manifest.json: {tag} CTA label is {len(c)} chars (>{CTA_MAX})")
        if not f.get("ctaLabels"):
            errs.append(f"manifest.json: {tag} has no ctaLabels")

        src_path = os.path.join(kit, f.get("html", ""))
        if os.path.exists(src_path):
            src = open(src_path, encoding="utf-8", errors="replace").read()
            if lp_pay_placeholder(src):
                errs.append(f"{tag}: checkout link is still a placeholder")

            # The page is the authority on its own URL. Run --write --stamp so this line
            # exists; an absent or disagreeing one means the slug was never verified.
            declared = lp_deploy_comment(src)
            if declared is None:
                errs.append(f"{tag}: the LP declares no '<!-- Deploy as /f/<slug> -->' — its slug "
                            f"is unverified (regenerate with --write --stamp)")
            elif declared != s:
                errs.append(f"{tag}: manifest slug '{s}' but the page declares '{declared}'")

            # bridge.js binds the buy button by its visible text, so a label that is not a
            # control on the page binds nothing.
            rendered = lp_all_control_text(src)
            for c in f.get("ctaLabels") or []:
                if c not in rendered:
                    near = [t for t in rendered
                            if re.sub(r"\s+", "", t) == re.sub(r"\s+", "", c)]
                    hint = f" (the page renders '{near[0]}')" if near else ""
                    errs.append(f"{tag}: ctaLabel '{c}' is not a button/link on the page{hint}")
    return errs


def stamp_slugs(kit, manifest):
    """Write '<!-- Deploy as /f/<slug> -->' as line 1 of each LP (importer fallback source #1)."""
    n = 0
    for f in manifest["funnels"]:
        p = os.path.join(kit, f["html"])
        src = open(p, encoding="utf-8").read()
        want = f"<!-- Deploy as /f/{f['slug']} -->"
        if re.match(r"\s*<!--\s*Deploy as", src, re.I):
            src = re.sub(r"^\s*<!--\s*Deploy as[^>]*-->\s*\n", "", src, count=1, flags=re.I)
        open(p, "w", encoding="utf-8").write(want + "\n" + src)
        n += 1
    return n


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    kit = (args[0] if args else ".").rstrip("/")
    if not os.path.isdir(kit):
        print(f"not a directory: {kit}"); sys.exit(2)

    if "--check" in flags:
        errs = validate(kit)
        if errs:
            print("MANIFEST: FAIL")
            for e in errs: print("  ✗", e)
            sys.exit(1)
        print("MANIFEST: PASS")
        return

    m, warn = build(kit)
    if "--write" in flags:
        out = os.path.join(kit, "manifest.json")
        open(out, "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")
        print(f"wrote {out} — {len(m['funnels'])} funnel(s), category={m['category']}, "
              f"price={m.get('price', 'free')}")
        if "--stamp" in flags:
            print(f"stamped 'Deploy as' comment into {stamp_slugs(kit, m)} landing page(s)")
    else:
        print(json.dumps(m, ensure_ascii=False, indent=2))

    for w in warn:
        print("  ! " + w, file=sys.stderr)
    if warn:
        print(f"  ({len(warn)} warning(s) — none of these block the import, but each is manual "
              f"cleanup on their side)", file=sys.stderr)


if __name__ == "__main__":
    main()
