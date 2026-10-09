"""Tests for scripts/build_law_tip_proof.py.

Positive control: valid live-law-proof artifacts -> tip-pinned proof JSON emitted.
Negative controls: tampered refusal / missing ids / bad tip -> exit non-zero,
NOTHING written (fail-closed).
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_law_tip_proof.py"
TIP = "ed82e8b39e7e892f4ffb15339061232eb55685ac"
RUN_ID = "37633508035"
AUTH_RECEIPT_ID = "85606889-e310-4d6a-a5f7-a10d020e5165"
REFUSAL_RECEIPT_ID = "cd6b23a6-6ad9-470e-ba7a-5cda42f7c90e"


def make_artifacts(d: Path) -> dict:
    """Write a valid artifact set mirroring live-law-proof.yml's real shapes."""
    arts = {
        "authorized.json": {
            "ok": True,
            "decision": {
                "status": "AUTHORIZED",
                "reason": "ACTIVE_IN_SCOPE_GRANT",
                "authority_refs": ["0e082400-de6d-485e-9ebc-51b34f5debdc"],
            },
            "receipt": {"id": AUTH_RECEIPT_ID, "action": "law_authority_decision"},
        },
        "refusal.json": {
            "ok": True,
            "decision": {
                "status": "NEEDS_HUMAN_AUTHORIZATION",
                "reason": "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
                "capability_available": True,
                "door": {"door_id": "DOOR-GITHUB"},
            },
            "receipt": {"id": REFUSAL_RECEIPT_ID, "status": "BLOCKED"},
        },
        "sn002.json": {
            "ok": True,
            "status": "EXISTING_ACTION_AUTHORITY_VERIFIED",
            "decision": {"status": "AUTHORIZED"},
            "action_receipt": {"action": "intelligence_commit"},
        },
        "ids.json": {
            "authorized_law_receipt_id": AUTH_RECEIPT_ID,
            "refusal_law_receipt_id": REFUSAL_RECEIPT_ID,
        },
        "v_auth.json": {
            "ok": True,
            "status": "LAW_DECISION_VERIFIED",
            "recomputed": {"status": "AUTHORIZED"},
        },
        "v_ref.json": {
            "ok": True,
            "status": "LAW_DECISION_VERIFIED",
            "recomputed": {
                "status": "NEEDS_HUMAN_AUTHORIZATION",
                "reason": "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
            },
        },
        "v_sn002.json": {"ok": True, "status": "EXISTING_ACTION_AUTHORITY_VERIFIED"},
    }
    paths = {}
    for name, payload in arts.items():
        p = d / name
        p.write_text(json.dumps(payload))
        paths[name] = p
    return paths


def run_builder(d: Path, paths: dict, out_name: str = "proof.json", extra=None):
    out = d / out_name
    cmd = [
        sys.executable, str(SCRIPT),
        "--tip-sha", TIP,
        "--run-id", RUN_ID,
        "--run-url", f"https://github.com/SoulSchoolAcademy/NayaPOWER/actions/runs/{RUN_ID}",
        "--law-runtime", "https://example.supabase.co/functions/v1/nayanet-law-runtime",
        "--authorized-json", str(paths["authorized.json"]),
        "--refusal-json", str(paths["refusal.json"]),
        "--sn002-json", str(paths["sn002.json"]),
        "--receipt-ids-json", str(paths["ids.json"]),
        "--verify-authorized-json", str(paths["v_auth.json"]),
        "--verify-refusal-json", str(paths["v_ref.json"]),
        "--verify-sn002-json", str(paths["v_sn002.json"]),
        "--out", str(out),
    ]
    if extra:
        cmd = [c if c != TIP else extra.get("--tip-sha", c) for c in cmd]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc, out


def test_positive_builds_tip_pinned_proof(tmp_path):
    """POSITIVE: valid artifacts -> PASS proof pinned to the exact tip."""
    paths = make_artifacts(tmp_path)
    proc, out = run_builder(tmp_path, paths)
    assert proc.returncode == 0, proc.stderr
    assert out.is_file()
    proof = json.loads(out.read_text())
    assert proof["schema"] == "naya.law.live-proof.v1"
    assert proof["status"] == "PASS"
    assert proof["source_main"] == TIP
    assert proof["run_id"] == int(RUN_ID)
    assert proof["authorized_case"]["decision"] == "AUTHORIZED"
    assert proof["authorized_case"]["law_receipt_id"] == AUTH_RECEIPT_ID
    # The negative control must be IN the proof: refusal despite capability.
    assert proof["refusal_case"]["decision"] == "NEEDS_HUMAN_AUTHORIZATION"
    assert proof["refusal_case"]["capability_available"] is True
    assert proof["refusal_case"]["requested_action"] == "production_deploy"
    assert proof["independent_verification"] is True
    assert proof["limits"], "honesty limits must travel with the proof"


def test_negative_tampered_refusal_refuses_to_emit(tmp_path):
    """NEGATIVE: if the runtime ever AUTHORIZED the deploy case, no proof lands."""
    paths = make_artifacts(tmp_path)
    tampered = json.loads(paths["refusal.json"].read_text())
    tampered["decision"]["status"] = "AUTHORIZED"  # the catastrophic case
    tampered["receipt"]["status"] = "ACTIVE"
    paths["refusal.json"].write_text(json.dumps(tampered))
    proc, out = run_builder(tmp_path, paths)
    assert proc.returncode != 0
    assert not out.exists(), "fail-closed: tampered refusal must not emit a proof"
    assert "NEGATIVE CONTROL" in proc.stderr


def test_negative_refusal_without_capability_refuses_to_emit(tmp_path):
    """NEGATIVE: refusal with capability_available=false proves nothing."""
    paths = make_artifacts(tmp_path)
    weak = json.loads(paths["refusal.json"].read_text())
    weak["decision"]["capability_available"] = False
    paths["refusal.json"].write_text(json.dumps(weak))
    proc, out = run_builder(tmp_path, paths)
    assert proc.returncode != 0
    assert not out.exists()


def test_negative_receipt_id_mismatch_refuses_to_emit(tmp_path):
    """NEGATIVE: receipt ids must match law-receipt-ids.json (anti-substitution)."""
    paths = make_artifacts(tmp_path)
    ids = json.loads(paths["ids.json"].read_text())
    ids["refusal_law_receipt_id"] = "00000000-0000-4000-8000-000000000000"
    paths["ids.json"].write_text(json.dumps(ids))
    proc, out = run_builder(tmp_path, paths)
    assert proc.returncode != 0
    assert not out.exists()


def test_negative_bad_tip_sha_refuses_to_emit(tmp_path):
    """NEGATIVE: proof must pin a real 40-hex tip, never a placeholder."""
    paths = make_artifacts(tmp_path)
    proc, out = run_builder(tmp_path, paths, extra={"--tip-sha": "NOT_A_SHA"})
    assert proc.returncode != 0
    assert not out.exists()


def test_negative_missing_artifact_refuses_to_emit(tmp_path):
    """NEGATIVE: a missing independent-verification artifact fails closed."""
    paths = make_artifacts(tmp_path)
    paths["v_ref.json"].unlink()
    proc, out = run_builder(tmp_path, paths)
    assert proc.returncode != 0
    assert not out.exists()
