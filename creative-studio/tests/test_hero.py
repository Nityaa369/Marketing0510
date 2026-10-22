import shlex

import pytest

import studio.hero as hero


def test_mflux_command_is_built_from_settings(tmp_path, layout, monkeypatch):
    seen = {}

    class Done:
        returncode = 0
        stdout = stderr = ""

    def fake_run(cmd, **kw):
        seen["cmd"] = cmd
        out = cmd[cmd.index("--output") + 1]
        from PIL import Image

        Image.new("RGB", (1344, 688)).save(out)
        return Done()

    monkeypatch.setattr(hero.shutil, "which", lambda exe: "/usr/bin/" + exe)
    monkeypatch.setattr(hero.subprocess, "run", fake_run)
    monkeypatch.setenv("STUDIO_QUANTIZE", "4")
    monkeypatch.delenv("STUDIO_MODEL", raising=False)
    path = hero.generate_hero("r1", "an Indian advocate's chamber", layout, backend="mflux", seed=7, out_dir=tmp_path)
    cmd = seen["cmd"]
    assert cmd[0] == "mflux-generate-z-image-turbo"
    assert cmd[cmd.index("--model") + 1] == "z-image-turbo"
    assert cmd[cmd.index("--seed") + 1] == "7" and cmd[cmd.index("-q") + 1] == "4"
    assert "no text" in cmd[cmd.index("--prompt") + 1]
    assert hero.read_meta(path)["model"] == "z-image-turbo"
    # same prompt + seed: reused, no second model run
    seen.clear()
    hero.generate_hero("r1", "an Indian advocate's chamber", layout, backend="mflux", seed=7, out_dir=tmp_path)
    assert not seen


def test_missing_mflux_gives_clear_error(tmp_path, layout, monkeypatch):
    monkeypatch.setattr(hero.shutil, "which", lambda exe: None)
    with pytest.raises(hero.HeroError, match="setup_mac.sh"):
        hero.generate_hero("r1", "scene", layout, backend="mflux", out_dir=tmp_path)


def test_quantize_none_drops_flag(tmp_path, layout, monkeypatch):
    seen = {}
    monkeypatch.setattr(hero.shutil, "which", lambda exe: "/x")
    monkeypatch.setattr(hero.subprocess, "run", lambda cmd, **kw: seen.setdefault("cmd", cmd) and (_ for _ in ()).throw(SystemExit))
    monkeypatch.setenv("STUDIO_QUANTIZE", "none")
    with pytest.raises(SystemExit):
        hero._run_mflux(tmp_path / "x.png", "p", 64, 64, 1)
    assert "-q" not in seen["cmd"] and shlex.join(seen["cmd"]).count("--output") == 1
