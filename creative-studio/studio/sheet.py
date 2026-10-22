"""Read and validate the ICP spreadsheet.

One row = one poster. Column names are case-insensitive; spaces become underscores.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .config import load_brand

COLUMNS = {
    "id": "Unique short id, used in file names (e.g. nca01_new_grads)",
    "campaign": "Campaign name for the media buyer",
    "icp": "Reader name as it appears in the banner (e.g. NEW LAW GRADS)",
    "banner": "Optional. Full banner text. Blank = template default '{icp} WANTING CANADIAN LEGAL PRACTICE'",
    "headline": "The big line. Wrap a phrase in *asterisks* to set it in red italic",
    "supporting": "One plain supporting line under the headline",
    "cta": "Button text. Must contain JOIN NOW",
    "price": "Optional. Blank = brand price (₹10)",
    "price_line": "Optional. Line under JOIN NOW. Must say 3 days and 9 hours",
    "journey_tab": "Optional. Pop-out tab over the bar. Blank = program default",
    "hero_prompt": "Scene for the image model. Describe people and place, never text",
    "hero_image": "Optional. Path to your own hero image; skips generation",
    "seed": "Optional. Whole number for a repeatable hero image",
}
REQUIRED = ["id", "campaign", "icp", "headline", "supporting", "cta"]
TEXT_FIELDS = ["icp", "banner", "headline", "supporting", "cta", "price_line", "journey_tab"]
DEFAULT_PRICE_LINE = "for all {days} days · {hours} hours of knowledge-enriching sessions"


@dataclass
class Row:
    data: dict
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.data.get("id", "")).strip()

    @property
    def ok(self) -> bool:
        return not self.errors

    def get(self, key: str, default: str = "") -> str:
        value = self.data.get(key)
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return default
        text = str(value).strip()
        return text if text else default


def _norm(col: str) -> str:
    return re.sub(r"\W+", "_", str(col).strip().lower()).strip("_")


def read_sheet(path: str | Path, sheet_name: str | int = 0) -> list[dict]:
    path = Path(path)
    if path.suffix.lower() in (".csv", ".tsv"):
        df = pd.read_csv(path, sep="\t" if path.suffix.lower() == ".tsv" else ",", dtype=str)
    else:
        df = pd.read_excel(path, sheet_name=sheet_name, dtype=str)
    df.columns = [_norm(c) for c in df.columns]
    df = df.dropna(how="all")
    return [{k: (None if pd.isna(v) else v) for k, v in rec.items()} for rec in df.to_dict("records")]


def fill_defaults(row: Row, program: dict, layout: dict) -> None:
    d = row.data
    if not row.get("banner"):
        d["banner"] = layout["banner"]["default_text"].format(icp=row.get("icp").upper())
    if not row.get("price"):
        d["price"] = program["price"]
    if not row.get("price_line"):
        d["price_line"] = DEFAULT_PRICE_LINE.format(days=program["days"], hours=program["hours"])
    if not row.get("journey_tab"):
        d["journey_tab"] = program["journey_tab"]
    if not row.get("cta"):
        d["cta"] = "JOIN NOW"


def validate_row(row: Row, program: dict, brand: dict | None = None) -> Row:
    brand = brand or load_brand()
    for col in REQUIRED:
        if not row.get(col):
            row.errors.append(f"missing '{col}'")
    if row.id and not re.fullmatch(r"[A-Za-z0-9_\-]+", row.id):
        row.errors.append(f"id '{row.id}' may only use letters, numbers, - and _")
    if not row.get("hero_prompt") and not row.get("hero_image"):
        row.errors.append("needs 'hero_prompt' or 'hero_image'")
    if row.get("hero_image") and not Path(row.get("hero_image")).expanduser().exists():
        row.errors.append(f"hero_image not found: {row.get('hero_image')}")
    if row.get("seed") and not re.fullmatch(r"\d+(\.0)?", row.get("seed")):
        row.errors.append("seed must be a whole number")
    if row.get("cta") and "JOIN NOW" not in row.get("cta").upper():
        row.errors.append("cta must contain JOIN NOW")

    price_line = row.get("price_line").lower()
    for phrase in program.get("price_frame_required", []):
        if phrase.lower() not in price_line:
            row.errors.append(f"price_line must say '{phrase}' (never a bare price)")

    text = " ".join(row.get(f) for f in TEXT_FIELDS + ["hero_prompt"])
    for phrase in brand.get("banned_phrases", []):
        if re.search(rf"(?i)(?<!\w){re.escape(phrase)}(?!\w)", text):
            row.errors.append(f"banned phrase: '{phrase}'")
    for rule in brand.get("required_phrase_rules", []):
        if re.search(rule["pattern"], text):
            row.errors.append(rule["message"])

    if re.search(r"(?i)\b(text|words?|letters?|sign|logo)\b", row.get("hero_prompt")) and "no text" not in row.get(
        "hero_prompt"
    ).lower():
        row.warnings.append("hero_prompt mentions text/signs; the model must not draw copy (posters add it)")
    return row


def load_rows(path: str | Path, program: dict, layout: dict) -> list[Row]:
    rows = []
    seen: set[str] = set()
    for rec in read_sheet(path):
        row = Row(dict(rec))
        fill_defaults(row, program, layout)
        validate_row(row, program)
        if row.id in seen:
            row.errors.append(f"duplicate id '{row.id}'")
        seen.add(row.id)
        rows.append(row)
    return rows
