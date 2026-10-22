import pytest
from PIL import Image

from studio.hero import generate_hero
from studio.poster import PosterError, fit_words, render_poster, rich_words
from studio.sheet import Row, fill_defaults


def full_row(data, program, layout):
    row = Row(dict(data))
    fill_defaults(row, program, layout)
    return row.data


@pytest.fixture
def hero(tmp_path, layout):
    return generate_hero("t01", "test scene", layout, backend="placeholder", out_dir=tmp_path)


def test_renders_at_expected_size(tmp_path, hero, good_row, program, layout):
    rep = render_poster(full_row(good_row, program, layout), hero, tmp_path / "p.png")
    c = layout["canvas"]
    assert rep.size == (c["width"] * c["scale"], c["height"] * c["scale"])
    with Image.open(tmp_path / "p.png") as im:
        assert im.size == rep.size
    assert rep.cta_share >= 0.15
    assert any("PLACEHOLDER" in w for w in rep.warnings)


def test_cta_bar_is_red_full_width(tmp_path, hero, good_row, program, layout):
    render_poster(full_row(good_row, program, layout), hero, tmp_path / "p.png")
    s = layout["canvas"]["scale"]
    y = (layout["cta_bar"]["box"][3] - 6) * s
    with Image.open(tmp_path / "p.png") as im:
        im = im.convert("RGB")
        for x in (2, im.width // 2 - 400, im.width - 3):
            assert im.getpixel((x, y)) == (0xC8, 0x10, 0x2E)


def test_long_headline_shrinks_then_overflows(tmp_path, hero, good_row, program, layout):
    good_row["headline"] = "You can qualify NCA, then the Canadian bar, " * 4
    rep = render_poster(full_row(good_row, program, layout), hero, tmp_path / "a.png")
    assert rep.font_sizes["headline"] < layout["headline"]["max_size"]
    good_row["headline"] = "You can qualify NCA, then the Canadian bar, " * 12
    with pytest.raises(PosterError, match="overflow in 'headline'"):
        render_poster(full_row(good_row, program, layout), hero, tmp_path / "b.png")


def test_missing_hero_raises(tmp_path, good_row, program, layout):
    with pytest.raises(PosterError, match="hero image missing"):
        render_poster(full_row(good_row, program, layout), tmp_path / "none.png", tmp_path / "p.png")


def test_accent_and_canada_words_are_red():
    words = rich_words("Practise in *Canada now*, today.", "headline", "headline_italic", "ink", "red", ["Canada"])
    styled = {w.text: (w.role, w.fill, w.glue) for w in words}
    assert styled["Practise"] == ("headline", "ink", False)
    assert styled["Canada"] == ("headline_italic", "red", False)
    assert styled[", today."[0:1]] == ("headline", "ink", True)  # comma glued to the accent


def test_fit_words_respects_max_lines():
    words = rich_words("one two three four five six seven eight", "body", "body", "ink", "red", [])
    size, lines = fit_words(words, [0, 0, 200, 400], 60, 10, 2, 1.1, 1, "t")
    assert len(lines) <= 2
