from conftest import write_sheet

from studio.sheet import Row, fill_defaults, load_rows, validate_row


def check(data, program, layout):
    row = Row(dict(data))
    fill_defaults(row, program, layout)
    return validate_row(row, program)


def test_good_row_passes_and_gets_defaults(good_row, program, layout):
    row = check(good_row, program, layout)
    assert row.ok, row.errors
    assert row.data["banner"] == "NEW LAW GRADS WANTING CANADIAN LEGAL PRACTICE"
    assert "3 days" in row.data["price_line"] and "9 hours" in row.data["price_line"]
    assert row.data["journey_tab"] == "Start your Canadian Legal Practice journey"


def test_missing_required_fields(good_row, program, layout):
    good_row.pop("headline")
    good_row["icp"] = ""
    row = check(good_row, program, layout)
    assert "missing 'headline'" in row.errors and "missing 'icp'" in row.errors


def test_needs_prompt_or_image(good_row, program, layout):
    good_row.pop("hero_prompt")
    assert "needs 'hero_prompt' or 'hero_image'" in check(good_row, program, layout).errors


def test_missing_hero_file(good_row, program, layout):
    good_row["hero_image"] = "/nope/missing.png"
    assert any("hero_image not found" in e for e in check(good_row, program, layout).errors)


def test_bare_price_rejected(good_row, program, layout):
    good_row["price_line"] = "only ₹10"
    errors = check(good_row, program, layout).errors
    assert any("3 days" in e for e in errors) and any("9 hours" in e for e in errors)


def test_banned_phrases_and_wording(good_row, program, layout):
    good_row["supporting"] = "100% pass and it closes today. Start your Canadian practice."
    errors = " | ".join(check(good_row, program, layout).errors)
    assert "100% pass" in errors and "closes today" in errors and "Canadian Legal Practice" in errors


def test_dashes_rejected(good_row, program, layout):
    good_row["headline"] = "Qualify NCA – then the bar"
    assert any("dash" in e for e in check(good_row, program, layout).errors)


def test_cta_must_say_join_now(good_row, program, layout):
    good_row["cta"] = "Register"
    assert "cta must contain JOIN NOW" in check(good_row, program, layout).errors


def test_bad_id_and_duplicates(tmp_path, good_row, program, layout):
    bad = dict(good_row, id="has space")
    path = write_sheet(tmp_path / "s.xlsx", [good_row, dict(good_row), bad])
    rows = load_rows(path, program, layout)
    assert rows[0].ok
    assert any("duplicate" in e for e in rows[1].errors)
    assert any("may only use" in e for e in rows[2].errors)


def test_sample_sheet_is_valid(program, layout):
    from conftest import ROOT

    rows = load_rows(ROOT / "data" / "icps_template.xlsx", program, layout)
    assert len(rows) == 20
    assert all(r.ok for r in rows), {r.id: r.errors for r in rows if not r.ok}
    assert len({r.get("icp") for r in rows}) == 20
