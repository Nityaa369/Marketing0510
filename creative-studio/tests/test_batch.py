import json

from conftest import write_sheet

from studio.batch import run_batch


def rows(n, good_row):
    return [dict(good_row, id=f"r{i:02d}", icp=f"Reader {i}") for i in range(n)]


def test_batch_makes_posters_and_contact_sheet(tmp_path, good_row):
    sheet = write_sheet(tmp_path / "s.xlsx", rows(3, good_row))
    r = run_batch(sheet, backend="placeholder", out_dir=tmp_path / "out", hero_dir=tmp_path / "heroes")
    assert r.ok and sorted(r.done) == ["r00", "r01", "r02"]
    assert all((tmp_path / "out/individual_ads" / f"{i}.png").exists() for i in r.done)
    assert r.contact_sheet and r.contact_sheet.exists()
    assert r.report.read_text().count("\n") == 4


def test_rerun_skips_unchanged_and_redoes_changed(tmp_path, good_row):
    data = rows(2, good_row)
    sheet = write_sheet(tmp_path / "s.xlsx", data)
    kw = dict(backend="placeholder", out_dir=tmp_path / "out", hero_dir=tmp_path / "heroes")
    run_batch(sheet, **kw)
    r = run_batch(sheet, **kw)
    assert r.skipped == ["r00", "r01"] and not r.done
    data[1]["headline"] = "A new big line about the Canadian bar."
    write_sheet(sheet, data)
    r = run_batch(sheet, **kw)
    assert r.skipped == ["r00"] and r.done == ["r01"]


def test_failures_are_logged_and_only_failed_rows_rerun(tmp_path, good_row, monkeypatch):
    import studio.batch as batch

    sheet = write_sheet(tmp_path / "s.xlsx", rows(3, good_row))
    kw = dict(backend="placeholder", out_dir=tmp_path / "out", hero_dir=tmp_path / "heroes")
    real = batch.generate_hero
    calls = []

    def flaky(rid, *a, **k):
        calls.append(rid)
        if rid == "r01":
            raise RuntimeError("model crashed")
        return real(rid, *a, **k)

    monkeypatch.setattr(batch, "generate_hero", flaky)
    r = run_batch(sheet, **kw)
    assert r.failed == {"r01": "hero: model crashed"} and sorted(r.done) == ["r00", "r02"]
    state = json.loads((tmp_path / "out/batch_state.json").read_text())
    assert state["r01"]["status"] == "failed" and state["r01"]["stage"] == "hero"
    log = next((tmp_path / "out/logs").glob("batch_*.log")).read_text()
    assert "r01 hero failed: model crashed" in log

    monkeypatch.setattr(batch, "generate_hero", real)
    calls.clear()
    r = run_batch(sheet, **kw)
    assert r.done == ["r01"] and r.skipped == ["r00", "r02"] and r.ok


def test_invalid_rows_reported_not_rendered(tmp_path, good_row):
    data = rows(2, good_row)
    data[0]["cta"] = "Buy"
    sheet = write_sheet(tmp_path / "s.xlsx", data)
    r = run_batch(sheet, backend="placeholder", out_dir=tmp_path / "out", hero_dir=tmp_path / "heroes")
    assert "r00" in r.invalid and r.done == ["r01"] and not r.ok


def test_hero_image_column_skips_generation(tmp_path, good_row, monkeypatch):
    from PIL import Image

    import studio.batch as batch

    photo = tmp_path / "photo.jpg"
    Image.new("RGB", (1200, 700), (200, 180, 160)).save(photo)
    data = [dict(good_row, hero_image=str(photo), hero_prompt="")]
    sheet = write_sheet(tmp_path / "s.xlsx", data)
    monkeypatch.setattr(batch, "generate_hero", lambda *a, **k: (_ for _ in ()).throw(AssertionError("called")))
    r = run_batch(sheet, out_dir=tmp_path / "out", hero_dir=tmp_path / "heroes")
    assert r.done == ["t01"]
