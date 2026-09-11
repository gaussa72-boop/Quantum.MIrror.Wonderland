import json
from game_engine import QuantumGameEngine, GameGenerationError


def test_web_fallback_generates_project(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    engine = QuantumGameEngine(output_dir=str(tmp_path))
    result = engine.generate("A tiny space adventure", "web", "game")
    assert result["id"]
    assert result["files"]
    assert (tmp_path / f"{result['id']}.zip").is_file()


def test_mod_and_dlc_are_distinct(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    engine = QuantumGameEngine(output_dir=str(tmp_path))
    mod = engine.generate("Add a magic sword", "web", "mod")
    dlc = engine.generate("Add a new moon world", "web", "dlc")
    assert any(p.startswith("mod/") for p in mod["files"])
    assert any(p.startswith("dlc/") for p in dlc["files"])


def test_invalid_target_rejected(tmp_path):
    engine = QuantumGameEngine(output_dir=str(tmp_path))
    try:
        engine.generate("hello", "invalid", "game")
    except GameGenerationError:
        return
    raise AssertionError("invalid target was accepted")


def test_download_path_is_strict(tmp_path):
    engine = QuantumGameEngine(output_dir=str(tmp_path))
    try:
        engine.download_path("../../etc/passwd")
    except GameGenerationError:
        return
    raise AssertionError("unsafe project id was accepted")
