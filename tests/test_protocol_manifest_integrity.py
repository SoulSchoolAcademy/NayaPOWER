"""Tests for the Team Naya protocol machine law.

The protocol is code, not just prose. These tests verify:
1. The manifest is well-formed and complete
2. The cold-start gate enforces the boot contract
3. Law IDs are unique (ambiguous authority is a defect)
4. Protected gates outrank all other laws
5. Truth states do not collapse
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "kernel" / "protocol" / "protocol_manifest.json"
GATE_PATH = ROOT / "kernel" / "protocol" / "protocol_integrity_gate.py"


@pytest.fixture
def manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def test_manifest_exists():
    assert MANIFEST_PATH.exists(), "protocol manifest must exist"


def test_manifest_has_required_keys(manifest):
    required = ["laws", "protected_gates", "truth_states", "operating_loop",
                "never_do", "law_conflict_hierarchy", "cold_start_required"]
    for key in required:
        assert key in manifest, f"manifest missing: {key}"


def test_five_protected_gates(manifest):
    gates = manifest["protected_gates"]
    assert len(gates) == 5, f"expected 5 protected gates, found {len(gates)}"
    for gate in gates:
        assert gate["requires"] == "shawn_explicit_word", \
            f"gate {gate['id']} must require Shawn's word"


def test_gates_first_in_hierarchy(manifest):
    hierarchy = manifest["law_conflict_hierarchy"]
    assert hierarchy[0] == "protected_gates", \
        "protected gates must outrank all other laws"


def test_law_ids_unique(manifest):
    ids = [law["id"] for law in manifest["laws"]]
    assert len(ids) == len(set(ids)), "duplicate law IDs = ambiguous authority"


def test_six_truth_states(manifest):
    assert len(manifest["truth_states"]) == 6


def test_truth_states_have_rules(manifest):
    rules = manifest["truth_state_rules"]
    for state in manifest["truth_states"]:
        assert state in rules, f"{state} has no non-equivalence rules"


def test_never_do_comprehensive(manifest):
    assert len(manifest["never_do"]) >= 10, "never-do list must be comprehensive"


def test_cold_start_gate_exists():
    assert GATE_PATH.exists(), "cold-start gate must exist"


def test_cold_start_gate_passes():
    result = subprocess.run(
        [sys.executable, str(GATE_PATH), "--agent-id", "test-agent", "--json"],
        capture_output=True, text=True, timeout=60, cwd=ROOT
    )
    assert result.returncode == 0, f"gate failed: {result.stdout}\n{result.stderr}"
    data = json.loads(result.stdout)
    assert data["pass"] is True
    assert len(data["failures"]) == 0


def test_gate_does_not_grant_authority():
    """Passing the gate verifies readiness, not authority. This must be explicit."""
    result = subprocess.run(
        [sys.executable, str(GATE_PATH), "--agent-id", "test-agent", "--json"],
        capture_output=True, text=True, timeout=60, cwd=ROOT
    )
    data = json.loads(result.stdout)
    assert "authority" in data["note"].lower(), \
        "gate must explicitly state it does not grant authority"
