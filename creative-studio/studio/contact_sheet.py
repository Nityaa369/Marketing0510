"""One image showing every poster in a batch, labelled, for review."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

from .config import color, font


def create_contact_sheet(
    items: list[tuple[Path, str]],
    out_path: str | Path,
    title: str = "Contact sheet",
    thumb_width: int = 420,
    columns: int | None = None,
    flagged: set[str] | None = None,
) -> Path:
    """items: (poster_path, label). Labels in `flagged` get a red PLACEHOLDER tag."""
    if not items:
        raise ValueError("no posters to put on the contact sheet")
    flagged = flagged or set()
    columns = columns or min(5, max(1, math.ceil(math.sqrt(len(items)))))
    with Image.open(items[0][0]) as first:
        ratio = first.height / first.width
    tw, th = thumb_width, int(thumb_width * ratio)
    gap, label_h, head_h = 24, 48, 110
    rows = math.ceil(len(items) / columns)
    W = columns * tw + (columns + 1) * gap
    H = head_h + rows * (th + label_h + gap) + gap
    sheet = Image.new("RGB", (W, H), color("cream"))
    d = ImageDraw.Draw(sheet)
    d.text((gap, head_h / 2), f"{title} · {len(items)} posters", font=font("headline", 48), fill=color("ink"), anchor="lm")
    label_font = font("body", 22)
    for i, (path, label) in enumerate(items):
        r, c = divmod(i, columns)
        x = gap + c * (tw + gap)
        y = head_h + r * (th + label_h + gap)
        with Image.open(path) as im:
            sheet.paste(im.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline=color("ink"), width=2)
        limit = 22 if label in flagged else 34
        text = label if len(label) <= limit else label[: limit - 1] + "…"
        d.text((x, y + th + 10), text, font=label_font, fill=color("ink"))
        if label in flagged:
            tag = "PLACEHOLDER"
            tl = d.textlength(tag, font=label_font)
            d.rectangle([x + tw - tl - 16, y + th + 6, x + tw, y + th + 40], fill=color("red"))
            d.text((x + tw - tl - 8, y + th + 10), tag, font=label_font, fill=color("white"))
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, "PNG", optimize=True)
    return out_path
