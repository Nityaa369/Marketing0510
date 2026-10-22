"""Spreadsheet -> hero images -> posters -> contact sheet, with resumable state.

State lives in outputs/batch_state.json. A row is skipped on the next run when its inputs
(copy, prompt, seed, template, brand config) are unchanged and its poster still exists, so
re-running after a failure only redoes the failed rows.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

from .config import CONFIG_DIR, OUTPUTS_DIR, TEMPLATES_DIR, load_brand, load_layout
from .contact_sheet import create_contact_sheet
from .hero import HERO_DIR, backend_from_env, generate_hero
from .poster import render_poster
from .sheet import load_rows

log = logging.getLogger("studio.batch")


@dataclass
class BatchResult:
    done: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: dict[str, str] = field(default_factory=dict)
    invalid: dict[str, list[str]] = field(default_factory=dict)
    warnings: dict[str, list[str]] = field(default_factory=dict)
    contact_sheet: Path | None = None
    report: Path | None = None

    @property
    def ok(self) -> bool:
        return not self.failed and not self.invalid


def _hash(row: dict, template: str, backend: str) -> str:
    h = hashlib.sha256()
    h.update(json.dumps(row, sort_keys=True, default=str).encode())
    h.update(backend.encode())
    hero_image = row.get("hero_image")
    if hero_image and Path(str(hero_image)).expanduser().exists():
        h.update(str(Path(str(hero_image)).expanduser().stat().st_mtime).encode())
    h.update((TEMPLATES_DIR / template / "layout.json").read_bytes())
    h.update((CONFIG_DIR / "brand.json").read_bytes())
    return h.hexdigest()[:16]


def setup_logging(log_dir: Path) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / f"batch_{time.strftime('%Y%m%d')}.log"
    root = logging.getLogger("studio")
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == str(path) for h in root.handlers):
        fh = logging.FileHandler(path)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        root.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
        root.addHandler(sh)
    root.setLevel(logging.INFO)
    return path


def run_batch(
    sheet: str | Path,
    template: str = "ncacanada",
    *,
    backend: str | None = None,
    out_dir: Path = OUTPUTS_DIR,
    hero_dir: Path = HERO_DIR,
    force: bool = False,
    only: list[str] | None = None,
    limit: int | None = None,
    contact_sheet: bool = True,
) -> BatchResult:
    setup_logging(out_dir / "logs")
    layout = load_layout(template)
    program = load_brand()["programs"][layout["program"]]
    ads_dir = out_dir / "individual_ads"
    state_path = out_dir / "batch_state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    result = BatchResult()

    rows = load_rows(sheet, program, layout)
    if only:
        rows = [r for r in rows if r.id in only]
    if limit:
        rows = rows[:limit]
    log.info("batch start: %s rows from %s (template %s)", len(rows), sheet, template)

    for row in rows:
        rid = row.id or "(no id)"
        if row.warnings:
            result.warnings[rid] = list(row.warnings)
        if not row.ok:
            result.invalid[rid] = row.errors
            state[rid] = {"status": "invalid", "errors": row.errors}
            log.error("%s invalid: %s", rid, "; ".join(row.errors))
            continue

        key = _hash(row.data, template, backend or backend_from_env())
        poster_path = ads_dir / f"{rid}.png"
        prev = state.get(rid, {})
        if not force and prev.get("status") == "ok" and prev.get("hash") == key and poster_path.exists():
            result.skipped.append(rid)
            continue

        entry = {"hash": key, "updated": time.strftime("%Y-%m-%d %H:%M:%S")}
        try:
            if row.get("hero_image"):
                hero = Path(row.get("hero_image")).expanduser()
            else:
                t0 = time.time()
                hero = generate_hero(rid, row.get("hero_prompt"), layout, backend=backend, seed=row.get("seed"), out_dir=hero_dir)
                log.info("%s hero ready in %.1fs: %s", rid, time.time() - t0, hero)
            entry["hero"] = str(hero)
        except Exception as exc:  # noqa: BLE001 - every failure is logged and the batch continues
            entry.update(status="failed", stage="hero", error=str(exc))
            state[rid] = entry
            result.failed[rid] = f"hero: {exc}"
            log.error("%s hero failed: %s", rid, exc)
            _save(state_path, state)
            continue
        try:
            rep = render_poster(row.data, hero, poster_path, template)
            entry.update(status="ok", poster=str(poster_path), warnings=rep.warnings, font_sizes=rep.font_sizes)
            if rep.warnings:
                result.warnings.setdefault(rid, []).extend(rep.warnings)
            result.done.append(rid)
            log.info("%s poster ok: %s", rid, poster_path)
        except Exception as exc:  # noqa: BLE001
            entry.update(status="failed", stage="poster", error=str(exc))
            result.failed[rid] = f"poster: {exc}"
            log.error("%s poster failed: %s", rid, exc)
        state[rid] = entry
        _save(state_path, state)

    _save(state_path, state)
    result.report = _write_report(out_dir / "batch_report.csv", rows, state)

    if contact_sheet:
        ready = [r for r in rows if state.get(r.id, {}).get("status") == "ok" and (ads_dir / f"{r.id}.png").exists()]
        if ready:
            flagged = {r.id for r in ready if any("PLACEHOLDER" in w for w in state[r.id].get("warnings", []))}
            stamp = time.strftime("%Y%m%d_%H%M")
            result.contact_sheet = create_contact_sheet(
                [(ads_dir / f"{r.id}.png", r.id) for r in ready],
                out_dir / "contact_sheets" / f"{Path(sheet).stem}_{stamp}.png",
                title=f"{program['program_name']} · {Path(sheet).name}",
                flagged=flagged,
            )
    log.info(
        "batch end: %s made, %s skipped (unchanged), %s failed, %s invalid",
        len(result.done), len(result.skipped), len(result.failed), len(result.invalid),
    )
    return result


def _save(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    tmp.replace(path)


def _write_report(path: Path, rows, state: dict) -> Path:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "campaign", "icp", "status", "stage", "error", "warnings", "poster"])
        for r in rows:
            s = state.get(r.id, {})
            w.writerow([
                r.id, r.get("campaign"), r.get("icp"), s.get("status", ""), s.get("stage", ""),
                s.get("error", "; ".join(s.get("errors", []))), "; ".join(s.get("warnings", [])), s.get("poster", ""),
            ])
    return path
