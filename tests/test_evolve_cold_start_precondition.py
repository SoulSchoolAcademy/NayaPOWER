import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/evolve-cold-start-precondition.py"


def load_probe():
    spec = importlib.util.spec_from_file_location("evolve_probe", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_real_repo_is_reconstructable_without_external_workspace():
    result = load_probe().evaluate(ROOT)
    assert result["ok"] is True, result
    assert result["node_count"] == 9
    assert result["behavioral_cold_successor_proven"] is False
    assert result["activation_claim"] == "NOT_MADE"


def test_missing_repo_artifact_fails_closed(tmp_path):
    result = load_probe().evaluate(tmp_path)
    assert result["ok"] is False
    assert "missing_repo_artifact:manifest" in result["gaps"]
