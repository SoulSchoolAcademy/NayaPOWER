import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cold_start_activation_does_not_require_legacy_memory_state():
    result = subprocess.run(
        [sys.executable, ".naya/runtime/cold_start_activation.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert ".naya\\memory\\STATE.json" not in result.stdout
    assert "legacy memory STATE" not in result.stdout
