"""Tests for the Decision Principle Governance check.

The gate proves the philosophy governs the code:
1. Cross-implementation agreement (two independent readings agree)
2. Live pipeline excludes prohibited before optimizing
3. Verdict mapping correct and fail-closed
"""

import subprocess
import sys
import os

import pytest

CHECK = os.path.join(
    os.path.dirname(__file__), "..", "tools", "protocol", "checks",
    "decision_principle_governance.py",
)
CHECK = os.path.abspath(CHECK)


def run_check(*args):
    result = subprocess.run(
        [sys.executable, CHECK, *args],
        capture_output=True, text=True, timeout=120,
    )
    return result


def test_governance_check_passes_on_clean_tree():
    """The gate passes when the principle governs the pipeline."""
    result = run_check("--record", "{}")
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "OK:" in result.stdout


def test_governance_check_rejects_invalid_record():
    """Malformed input fails closed — never silently passes."""
    result = run_check("--record", "not-json")
    assert result.returncode == 1
    assert "FAIL" in result.stdout


def test_governance_check_rejects_non_object_record():
    """A non-object record fails closed."""
    result = run_check("--record", "[1,2,3]")
    assert result.returncode == 1
    assert "FAIL" in result.stdout


def test_governance_names_all_three_proofs():
    """The OK output names what was proven."""
    result = run_check("--record", "{}")
    assert result.returncode == 0
    out = result.stdout
    assert "cross-implementation" in out
    assert "excludes prohibited" in out
    assert "verdict mapping" in out


def test_manifest_registers_governance():
    """The protocol manifest registers the governance check."""
    import json
    manifest_path = os.path.join(
        os.path.dirname(__file__), "..", "kernel", "protocol",
        "protocol_manifest.json",
    )
    manifest_path = os.path.abspath(manifest_path)
    with open(manifest_path) as f:
        manifest = json.load(f)
    laws = manifest.get("laws", [])
    ids = [l.get("id") for l in laws]
    assert "DECISION-PRINCIPLE-GOVERNANCE" in ids
    entry = next(l for l in laws if l.get("id") == "DECISION-PRINCIPLE-GOVERNANCE")
    assert entry["check"] == "tools/protocol/checks/decision_principle_governance.py"
    # The check file must exist at the registered path.
    assert os.path.exists(os.path.join(
        os.path.dirname(manifest_path), "..", "..",
        entry["check"],
    ))


def test_disqualification_documented_in_value_calculus():
    """The operational code carries the disqualification distinction."""
    vc_path = os.path.join(
        os.path.dirname(__file__), "..", "kernel", "value_calculus.py",
    )
    vc_path = os.path.abspath(vc_path)
    with open(vc_path) as f:
        content = f.read()
    assert "DISQUALIFIED from the competition entirely" in content
    assert "not scored" in content.lower() or "not a score" in content.lower()


def test_governance_fails_when_disqualification_broken():
    """Negative control: if the gate stops disqualifying, the check FAILS.

    This is the sabotage proof living in the repo — not just in a PR
    description. If someone weakens gate_candidate so hard violations
    no longer return PROHIBITED, run_governance() must raise.
    """
    import sys
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from tools.protocol.checks import decision_principle_governance as gov
    import kernel.value_calculus as vc

    real_gate = vc.gate_candidate

    def broken_gate(candidate, profile, risk_policy):
        # Sabotage: hard violations no longer disqualify.
        if candidate.hard_violation:
            q = real_gate(candidate, profile, risk_policy)[2]
            return "NEEDS_EVIDENCE", ["SABOTAGED"], q
        return real_gate(candidate, profile, risk_policy)

    vc.gate_candidate = broken_gate
    # decision_principle.verify_pipeline_excludes_first imports gate_candidate
    # at call time from kernel.value_calculus, so the patch applies.
    try:
        with pytest.raises(AssertionError):
            gov.run_governance()
    finally:
        vc.gate_candidate = real_gate


def test_governance_fails_when_implementations_diverge():
    """Negative control: if the two implementations disagree, the check FAILS."""
    import sys
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    from tools.protocol.checks import decision_principle_governance as gov
    import kernel.decision_principle as dp

    real_independent = dp._independent_decide

    def broken_independent(actions):
        # Sabotage: independent implementation never disqualifies.
        result = real_independent(actions)
        result["disqualified"] = []
        return result

    dp._independent_decide = broken_independent
    try:
        with pytest.raises(AssertionError):
            gov.run_governance()
    finally:
        dp._independent_decide = real_independent
