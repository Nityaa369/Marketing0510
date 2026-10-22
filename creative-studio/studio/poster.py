"""Poster composition: fixed template + hero image + exact copy typeset with Pillow."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .config import ROOT, color, fallback_fonts_in_use, font, load_brand, load_layout
from .hero import draw_maple_leaf, read_meta


class PosterError(RuntimeError):
    pass


@dataclass
class Word:
    text: str
    role: str
    fill: str
    glue: bool = False  # True = no space before this word (e.g. comma after *accent*)


@dataclass
class RenderReport:
    path: Path | None = None
    size: tuple[int, int] = (0, 0)
    font_sizes: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    cta_share: float = 0.0


# ---------------------------------------------------------------- text layout


def _width(words: list[Word], size: int, scale: float) -> float:
    if not words:
        return 0
    total = sum(font(w.role, int(size * scale)).getlength(w.text) for w in words)
    space = font(words[0].role, int(size * scale)).getlength(" ")
    gaps = sum(1 for w in words[1:] if not w.glue)
    return total + space * gaps


def _wrap(words: list[Word], size: int, scale: float, max_w: float) -> list[list[Word]] | None:
    lines: list[list[Word]] = [[]]
    for w in words:
        trial = lines[-1] + [w]
        if _width(trial, size, scale) <= max_w or not lines[-1] or w.glue:
            lines[-1] = trial
        else:
            lines.append([w])
    if any(_width(line, size, scale) > max_w for line in lines):
        return None  # a single word is wider than the box
    return lines


def fit_words(words, box, max_size, min_size, max_lines, spacing, scale, name):
    """Largest size (step 1px) where the words wrap into max_lines and fit the box."""
    x0, y0, x1, y1 = box
    max_w, max_h = (x1 - x0) * scale, (y1 - y0) * scale
    for size in range(max_size, min_size - 1, -1):
        lines = _wrap(words, size, scale, max_w)
        if lines is None or len(lines) > max_lines:
            continue
        height = size * scale * (1 + spacing * (len(lines) - 1))
        if height <= max_h:
            return size, lines
    raise PosterError(f"text overflow in '{name}': does not fit at {min_size}px in {max_lines} line(s)")


def rich_words(text: str, base_role: str, accent_role: str, base_fill: str, accent_fill: str, red_words) -> list[Word]:
    """*phrase* -> accent (italic red). Canada words are always red."""
    words: list[Word] = []
    red_re = re.compile(r"(?i)^\W*(" + "|".join(map(re.escape, red_words)) + r")") if red_words else None
    parts = text.split("*")
    for i, part in enumerate(parts):
        accent = i % 2 == 1
        glue_first = bool(words) and part[:1] not in ("", " ") and parts[i - 1][-1:] not in ("", " ")
        for j, token in enumerate(part.split()):
            fill = accent_fill if accent or (red_re and red_re.match(token)) else base_fill
            words.append(Word(token, accent_role if accent else base_role, fill, glue_first and j == 0))
    return words


def draw_lines(draw, lines, size, box, scale, spacing, align="center", valign="center"):
    x0, y0, x1, y1 = [v * scale for v in box]
    px = int(size * scale)
    line_h = px * spacing
    block_h = px + line_h * (len(lines) - 1)
    y = y0 + ((y1 - y0) - block_h) / 2 if valign == "center" else y0
    for line in lines:
        w = _width(line, size, scale)
        x = x0 + ((x1 - x0) - w) / 2 if align == "center" else x0
        for k, word in enumerate(line):
            f = font(word.role, px)
            if k and not word.glue:
                x += font(line[0].role, px).getlength(" ")
            draw.text((x, y + px), word.text, font=f, fill=word.fill, anchor="ls")
            x += f.getlength(word.text)
        y += line_h


def _box(b, s):
    return [int(v * s) for v in b]


# ---------------------------------------------------------------- poster


def render_poster(row: dict, hero_path: str | Path, out_path: str | Path, template: str = "ncacanada") -> RenderReport:
    brand = load_brand()
    L = load_layout(template)
    program = brand["programs"][L["program"]]
    red_words = program.get("red_words", [])
    s = L["canvas"]["scale"]
    W, H = L["canvas"]["width"], L["canvas"]["height"]
    c = lambda name: color(name, brand)  # noqa: E731
    report = RenderReport()

    canvas = Image.new("RGB", (W * s, H * s), c(L["canvas"]["background"]))
    d = ImageDraw.Draw(canvas)

    # header: logo file if supplied, else typeset wordmark (flagged as placeholder)
    hx0, hy0, hx1, hy1 = L["header"]["box"]
    logo = ROOT / brand["logo_file"]
    if logo.exists():
        with Image.open(logo) as lg:
            lg = lg.convert("RGBA")
            lh = L["header"]["logo_height"] * s
            lg = lg.resize((int(lg.width * lh / lg.height), lh))
            canvas.paste(lg, (40 * s, int((hy0 + hy1) / 2 * s - lh / 2)), lg)
    else:
        report.warnings.append(f"no logo at {brand['logo_file']}; using a typeset wordmark placeholder")
        f = font("headline", 34 * s)
        d.text((40 * s, (hy0 + hy1) / 2 * s), brand["brand_name"], font=f, fill=c("ink"), anchor="lm")
    right = rich_words(
        f"{program['program_name']} · {program['dates']}", "body", "body", c("ink"), c("red"), red_words
    )
    size, lines = fit_words(right, [hx1 / 2 - 40, hy0, hx1 - 40, hy1], L["header"]["text_size"], 14, 1, 1, s, "header")
    x_end = (hx1 - 40) * s
    w = _width(lines[0], size, s)
    draw_lines(d, lines, size, [x_end / s - w / s, hy0, hx1 - 40, hy1], s, 1, align="left")

    # ICP banner
    B = L["banner"]
    d.rectangle(_box(B["box"], s), fill=c(B["fill"]))
    banner_words = [Word(t, "banner", c(B["text_color"])) for t in row["banner"].upper().split()]
    bx0, by0, bx1, by1 = B["box"]
    size, lines = fit_words(
        banner_words, [bx0 + B["padding_x"], by0 + 8, bx1 - B["padding_x"], by1 - 8],
        B["max_size"], B["min_size"], B["max_lines"], 1.0, s, "banner",
    )
    draw_lines(d, lines, size, [bx0, by0, bx1, by1], s, 1.0)
    report.font_sizes["banner"] = size

    # hero
    Hc = L["hero"]
    hb = _box(Hc["box"], s)
    hero_path = Path(hero_path)
    if not hero_path.exists():
        raise PosterError(f"hero image missing: {hero_path}")
    with Image.open(hero_path) as im:
        hero = ImageOps.fit(im.convert("RGB"), (hb[2] - hb[0], hb[3] - hb[1]), Image.LANCZOS)
    if min(im.size) < min(hb[2] - hb[0], hb[3] - hb[1]) * 0.5:
        report.warnings.append(f"hero is low resolution ({im.size[0]}x{im.size[1]})")
    if read_meta(hero_path).get("placeholder"):
        report.warnings.append("PLACEHOLDER hero image: do not ship this poster")
    mask = Image.new("L", hero.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, *hero.size], radius=Hc["radius"] * s, fill=255)
    canvas.paste(hero, hb[:2], mask)
    d.rounded_rectangle(hb, radius=Hc["radius"] * s, outline=c(Hc["border_color"]), width=Hc["border"] * s)
    if Hc.get("maple_badge"):
        r = 46 * s
        cx, cy = hb[2] - r - 18 * s, hb[1] + r + 18 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c("white"), outline=c("red"), width=4 * s)
        draw_maple_leaf(d, (cx, cy + 4 * s), int(r * 0.62), c("red"))

    # headline (big line)
    Hl = L["headline"]
    words = rich_words(row["headline"], "headline", "headline_italic", c(Hl["color"]), c(Hl["accent_color"]), red_words)
    size, lines = fit_words(words, Hl["box"], Hl["max_size"], Hl["min_size"], Hl["max_lines"], Hl["line_spacing"], s, "headline")
    draw_lines(d, lines, size, Hl["box"], s, Hl["line_spacing"], Hl["align"])
    report.font_sizes["headline"] = size

    # supporting line (red, never grey)
    Sp = L["supporting"]
    words = [Word(t, "body", c(Sp["color"])) for t in row["supporting"].split()]
    size, lines = fit_words(words, Sp["box"], Sp["max_size"], Sp["min_size"], Sp["max_lines"], Sp["line_spacing"], s, "supporting")
    draw_lines(d, lines, size, Sp["box"], s, Sp["line_spacing"], Sp["align"])
    report.font_sizes["supporting"] = size

    # JOIN NOW bar: full width, counts toward the 15% rule
    Cb = L["cta_bar"]
    cb = Cb["box"]
    d.rectangle(_box(cb, s), fill=c(Cb["fill"]))
    report.cta_share = (cb[2] - cb[0]) * (cb[3] - cb[1]) / (W * H)
    if report.cta_share < Cb["min_area_share"]:
        raise PosterError(f"JOIN NOW bar is {report.cta_share:.1%} of the poster; rule is at least {Cb['min_area_share']:.0%}")
    bar_top = cb[1] + 18
    split = bar_top + (cb[3] - bar_top) * 0.62
    line1 = [Word(t, "cta", c(Cb["text_color"])) for t in f"{row['cta'].upper()} AT ONLY {row['price']}".split()]
    size, lines = fit_words(line1, [cb[0] + 40, bar_top, cb[2] - 40, split], Cb["line1_max"], Cb["line1_min"], 1, 1, s, "cta")
    draw_lines(d, lines, size, [cb[0], bar_top, cb[2], split], s, 1)
    report.font_sizes["cta"] = size
    line2 = [Word(t, "body", c(Cb["text_color"])) for t in row["price_line"].split()]
    size, lines = fit_words(line2, [cb[0] + 40, split, cb[2] - 40, cb[3] - 10], Cb["line2_max"], Cb["line2_min"], 1, 1, s, "price_line")
    draw_lines(d, lines, size, [cb[0], split, cb[2], cb[3] - 10], s, 1)

    # pop-out journey tab sitting on the bar
    Tb = L["journey_tab"]
    tb = Tb["box"]
    words = rich_words(row["journey_tab"], "body", "body", c(Tb["text_color"]), c(Tb["text_color"]), [])
    leaf_w = 40
    size, lines = fit_words(words, [tb[0] + 24 + leaf_w, tb[1], tb[2] - 24, tb[3]], Tb["max_size"], Tb["min_size"], 1, 1, s, "journey_tab")
    text_w = _width(lines[0], size, s) / s
    tab_w = text_w + leaf_w + 56
    cx = (tb[0] + tb[2]) / 2
    tab = [cx - tab_w / 2, tb[1], cx + tab_w / 2, tb[3]]
    d.rounded_rectangle(_box(tab, s), radius=14 * s, fill=c(Tb["fill"]), outline=c(Tb["outline"]), width=4 * s)
    draw_maple_leaf(d, (int((tab[0] + 22 + leaf_w / 2) * s), int((tb[1] + tb[3]) / 2 * s)), int(15 * s), c("red"))
    draw_lines(d, lines, size, [tab[0] + 22 + leaf_w, tb[1], tab[2] - 22, tb[3]], s, 1)

    # footer terms
    Ft = L["footer"]
    words = [Word(t, "body", c(Ft["color"])) for t in program["terms_line"].split()]
    size, lines = fit_words(words, [Ft["box"][0] + 30, *Ft["box"][1:3], Ft["box"][3]], Ft["text_size"], 12, 1, 1, s, "footer")
    draw_lines(d, lines, size, Ft["box"], s, 1)

    for role in fallback_fonts_in_use():
        report.warnings.append(f"font role '{role}' is using a fallback font; run scripts/fetch_fonts.sh")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "PNG", optimize=True)
    with Image.open(out_path) as check:
        if check.size != (W * s, H * s):
            raise PosterError(f"exported size {check.size} != expected {(W * s, H * s)}")
        report.size = check.size
    report.path = out_path
    return report
