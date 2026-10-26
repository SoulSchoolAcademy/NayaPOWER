"""Naya Code of Honor: authority before optimization, at existing law checks.

These are *decision-record compliance* checks, NOT LAW or ACT grants.
A record with pass=true and may_act=false is a correctly recorded refusal;
an unauthorized attempted action always fails. No extra decision engine.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    "tools/protocol/checks/decision_log.py",
    "kernel/protocol/checks/decision_log.py",
)


def load_checker(path: str):
    spec = importlib.util.spec_from_file_location(
        "naya_authority_probe_" + path.replace("/", "_"),
        ROOT / path,
    )
    assert spec and spec.loader
    # Each legacy checker imports sibling checks from its owning directory.
    parent = str((ROOT / path).parent.parent)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def record():
    return {
        "decision": "Select safest lawful implementation",
        "options": [
            {"id": "build", "description": "Use existing authorized seam"},
            {"id": "refuse", "description": "Decline unauthorized operation"},
        ],
        "scores": {"build": 9, "refuse": 5},
        "winner": "build",
        "authority": {
            "admissible": True,
            "protected_gate_hit": False,
            "gates_checked": ["GATE-1", "GATE-2", "GATE-3", "GATE-4", "GATE-5"],
        },
        "decided_at": "2026-10-26T19:00:00Z",
        "decider": "cold-naya",
    }


@pytest.mark.parametrize("checker", CHECKS)
def test_authorized_highest_value_record_is_only_eligible_for_law_act(checker):
    v = load_checker(checker).check(record())
    assert v["pass"] is True, v
    assert v["details"]["may_act"] is True
    assert v["details"]["outcome"] == "PROCEED"
    assert any("subsequent LAW/ACT checks" in r for r in v["reasons"])


@pytest.mark.parametrize("checker", CHECKS)
@pytest.mark.parametrize("case", ("absent", "unknown", "false", "string_false"))
def test_missing_or_denied_authority_never_acts(checker, case):
    sample = record()
    if case == "absent":
        del sample["authority"]["admissible"]
    elif case == "unknown":
        sample["authority"]["admissible"] = None
    elif case == "false":
        sample["authority"]["admissible"] = False
    else:
        sample["authority"]["admissible"] = "false"
    v = load_checker(checker).check(sample)
    assert v["pass"] is False, v
    assert v["details"]["may_act"] is False
    assert v["details"]["violation"] == "NAYA_CODE_AUTHORITY_BREACH"


@pytest.mark.parametrize("checker", CHECKS)
@pytest.mark.parametrize("fake_approval", (True, "approved 2026-10-26", None))
def test_protected_gate_cannot_be_cleared_by_self_claimed_approval(
    checker, fake_approval
):
    sample = record()
    sample["authority"]["protected_gate_hit"] = True
    sample["authority"]["shawn_approval"] = fake_approval
    v = load_checker(checker).check(sample)
    assert v["pass"] is False, v
    assert v["details"]["may_act"] is False
    assert v["details"]["violation"] == "NAYA_CODE_AUTHORITY_BREACH"


@pytest.mark.parametrize("checker", CHECKS)
def test_refusal_record_passes_without_granting_execution(checker):
    sample = record()
    sample["winner"] = "refuse"
    sample["scores"] = {"build": 5, "refuse": 10}
    sample["authority"]["admissible"] = False
    sample["authority"]["protected_gate_hit"] = True
    v = load_checker(checker).check(sample)
    assert v["pass"] is True, v
    assert v["details"]["may_act"] is False
    assert v["details"]["outcome"] == "GATE"
    assert any("NOT authorized to execute" in r for r in v["reasons"])


@pytest.mark.parametrize("checker", CHECKS)
def test_cli_denies_fake_gate_permission(checker):
    sample = record()
    sample["authority"]["protected_gate_hit"] = True
    sample["authority"]["shawn_approval"] = True
    cmd = [
        sys.executable, str(ROOT / checker),
        "--record", json.dumps(sample), "--json"
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode == 1, (proc.stdout, proc.stderr)
    output = json.loads(proc.stdout)
    assert output["details"]["violation"] == "NAYA_CODE_AUTHORITY_BREACH"


def test_existing_tools_and_kernel_checkers_agree_for_probe_cases():
    tool, kernel = [load_checker(name) for name in CHECKS]
    for permitted, protected in [(True, False), (False, False), (True, True)]:
        sample = record()
        sample["authority"]["admissible"] = permitted
        sample["authority"]["protected_gate_hit"] = protected
        assert tool.check(sample) == kernel.check(sample)
