"""
Red-team tests for the Gate-1 boot wiring (ACT, Naya Gamma, 2026-10-13).

Claims under test:
1. tools/activation_checklist.py is wired into the REAL boot decision
   paths — kernel/protocol/protocol_integrity_gate.py (the invoked gate,
   run by CI on every PR/push) and kernel/protocol/cold_start_gate.py
   run_cold_start (the documented boot boundary) — not into a test
   harness.
2. A FORGED checklist pass is rejected, not trusted.
3. Fail closed: missing/tampered/unreadable canonical bytes refuse boot;
   no crash, no silent pass.

Positive AND negative controls: the gate must pass what it claims to
pass and block what it claims to block.
"""
import json
import os
import shutil
import sys
import tempfile

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start  # noqa: E402
from kernel.protocol.protocol_integrity_gate import check_activation_checklist  # noqa: E402
from kernel.protocol.read_receipt import issue_receipt  # noqa: E402
import importlib.util  # noqa: E402
from pathlib import Path  # noqa: E402


def _load_checklist_tool():
    spec = importlib.util.spec_from_file_location(
        "naya_activation_checklist_test",
        os.path.join(REPO_ROOT, "tools", "activation_checklist.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def tool():
    return _load_checklist_tool()


@pytest.fixture(scope="module")
def canonical(tool):
    canonical, err = tool.load_canonical(REPO_ROOT)
    assert canonical is not None, f"canonical artifacts unreadable: {err}"
    return canonical


def _good_state():
    return ColdStartState(
        agent_id="naya-red-team",
        human_director="Shawn Vibert",
        lane="act",
        authority_summary="Protected gates: production deploys, credentials/money, "
                          "destructive actions, ratification, security/privacy. "
                          "Law 11 (do no harm) is the only hard law.",
        current_truth_location="mission-state feed #2154 and current main",
        next_action="verify the boot gate wiring",
        receipt=issue_receipt("naya-red-team", {
            "q1": "Shawn Vibert",
            "q2": "production deploys, credentials and money, destructive actions, "
                  "ratification, security and privacy",
            "q3": "No, never",
            "q4": "9.0",
            "q5": "independent evidence and proof",
        }),
    )


def _honest_claim(canonical):
    return {
        "lessons": [{"lesson_id": lid, "sha256": h}
                    for lid, h in canonical["lesson_hashes"].items()],
        "v2": dict(canonical["v2_hashes"]),
    }


# ---------- positive controls ----------

def test_self_audit_passes_on_real_tree(tool, canonical):
    """The checklist verifies on the real repo: 14 lessons + V2 intact."""
    verdict, violations = tool.check_checklist(canonical)
    assert verdict == "CHECKLIST-VERIFIED", f"unexpected violations: {violations}"


def test_invoked_boot_gate_check_passes():
    """protocol_integrity_gate's new check runs green on the real tree —
    this is the gate CI actually invokes (auto_brain step 5)."""
    passed, detail = check_activation_checklist()
    assert passed, f"boot gate checklist check failed: {detail}"


def test_run_cold_start_honest_path_passes():
    """The documented boot boundary still passes for an honest state."""
    assert run_cold_start(_good_state()).passed


def test_run_cold_start_honest_claim_passes(tool, canonical):
    """An honest agent claim (recomputed hashes) verifies through the gate."""
    res = run_cold_start(_good_state(), checklist_claim=_honest_claim(canonical))
    assert res.passed, f"honest claim refused: {res.failures}"


# ---------- red-team: forged pass must be rejected ----------

def test_forged_lesson_hash_rejected(tool, canonical):
    """Attack: claim a lesson with a forged sha256. Must be REJECT."""
    claim = _honest_claim(canonical)
    claim["lessons"][0]["sha256"] = "0" * 64  # forger's fake hash
    verdict, violations = tool.check_checklist(canonical, claim)
    assert verdict == "REJECT"
    assert any("LESSON_FINGERPRINT_MISMATCH" in x for x in violations)


def test_forged_claim_rejected_through_boot_boundary(tool, canonical):
    """Same forgery, submitted through run_cold_start — boot refused."""
    claim = _honest_claim(canonical)
    claim["lessons"][6]["sha256"] = "deadbeef" * 8
    res = run_cold_start(_good_state(), checklist_claim=claim)
    assert not res.passed
    assert any("Gate 1" in f or "checklist" in f.lower() for f in res.failures)


def test_partial_claim_rejected(tool, canonical):
    """Attack: claim only 13 of 14 lessons. Partial loading is not activation."""
    claim = _honest_claim(canonical)
    claim["lessons"] = claim["lessons"][:13]
    verdict, violations = tool.check_checklist(canonical, claim)
    assert verdict == "REJECT"
    assert any("LESSON_MISSING" in x for x in violations)


def test_fake_lesson_id_rejected(tool, canonical):
    """Attack: claim includes an unregistered lesson id (L15)."""
    claim = _honest_claim(canonical)
    claim["lessons"].append({"lesson_id": "L15", "sha256": "1" * 64})
    verdict, violations = tool.check_checklist(canonical, claim)
    assert verdict == "REJECT"
    assert any("LESSON_NOT_REGISTERED" in x for x in violations)


def test_tampered_canonical_bytes_rejected(tool):
    """Attack: someone edits one lesson byte in the canonical curriculum.
    The self-audit must catch the drift (pin mismatch), not pass silently."""
    tmp = tempfile.mkdtemp(prefix="bootgate-redteam-")
    try:
        shutil.copytree(os.path.join(REPO_ROOT, "NAYA-ACTIVATION"),
                        os.path.join(tmp, "NAYA-ACTIVATION"))
        shutil.copytree(os.path.join(REPO_ROOT, "BRAIN", "01-GOVERNANCE"),
                        os.path.join(tmp, "BRAIN", "01-GOVERNANCE"))
        # Tamper: flip one byte in the curriculum JSON
        cur = os.path.join(tmp, "NAYA-ACTIVATION", "thinking-curriculum.json")
        with open(cur, encoding="utf-8") as f:
            data = json.load(f)
        data["lessons"][0]["title"] = "TAMPERED " + data["lessons"][0]["title"]
        with open(cur, "w", encoding="utf-8") as f:
            json.dump(data, f)
        canonical, err = tool.load_canonical(tmp)
        assert canonical is not None, f"setup failed: {err}"
        verdict, violations = tool.check_checklist(canonical)
        assert verdict == "REJECT"
        assert any("CURRICULUM_STALE" in x for x in violations)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_missing_checklist_tool_fail_closed(monkeypatch):
    """The checklist tool itself is gone: the boot boundary must refuse,
    not crash (fail closed), through the real code path."""
    import kernel.protocol.cold_start_gate as csg
    monkeypatch.setattr(csg, "_CHECKLIST_TOOL", Path("/nonexistent/checklist.py"))
    failures = csg._check_activation_checklist()
    assert failures and "refused" in failures[0].lower()


def test_duplicate_lesson_claim_rejected(tool, canonical):
    """Attack: claim the same lesson twice to reach 14 entries."""
    claim = _honest_claim(canonical)
    claim["lessons"].append(dict(claim["lessons"][0]))
    verdict, violations = tool.check_checklist(canonical, claim)
    assert verdict == "REJECT"
    assert any("LESSON_DUPLICATE" in x for x in violations)
