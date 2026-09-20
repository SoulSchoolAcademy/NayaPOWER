#!/usr/bin/env python3
"""Narrow proof for CCT-005 Outcome -> independent Verification Receipt."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_verified_outcome_emits_receipt_after_authoritative_verification():
    er = load("evidence_runtime_test", ROOT / ".naya/runtime/evidence_runtime.py")
    vr = load("cct005_verification_receipt_test", ROOT / ".naya/runtime/cct005_verification_receipt.py")

    outcome = {
        "outcome_id": "OUT-CCT005-INDEPENDENT-001",
        "provenance": {"activity_receipt_id": "RCP-CCT005-ACTIVITY-001"},
    }
    claim = {
        "schema": "naya-power-claim/v1",
        "claim_id": outcome["outcome_id"],
        "statement": "The CCT-005 outcome was independently verified from the canonical Activity receipt.",
        "success_criteria": ["Outcome subject and Activity evidence are bound in a verified receipt."],
        "created_at": "2026-09-20T17:00:00Z",
        "status": "VERIFIED",
        "evidence_ids": ["EV-CCT005-INDEPENDENT-001"],
        "source": "CCT-005 outcome verification",
    }
    evidence = {
        "schema": "naya-power-evidence/v1",
        "evidence_id": "EV-CCT005-INDEPENDENT-001",
        "claim_id": outcome["outcome_id"],
        "observed_at": "2026-09-20T17:01:00Z",
        "method": "independent Activity receipt inspection",
        "command": "python tools/test_cct005_verification_receipt.py",
        "observed_output": "Canonical Activity receipt RCP-CCT005-ACTIVITY-001 observed and bound to the CCT-005 outcome.",
        "result": "PASS",
        "commit_sha": "TEST-CCT005-VERIFICATION",
        "environment": "isolated verification test",
        "source": "canonical Activity receipt",
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = er.verify_claim(
            claim,
            {evidence["evidence_id"]: evidence},
            expected_commit="TEST-CCT005-VERIFICATION",
        )
        assert result["status"] == "VERIFIED", result

        receipt = vr.build_outcome_verification_receipt(
            outcome,
            activity_receipt_id="RCP-CCT005-ACTIVITY-001",
            claim=claim,
            evidence_by_id={evidence["evidence_id"]: evidence},
            verify_claim_fn=er.verify_claim,
            receipt_id="VR-CCT005-INDEPENDENT-001",
            verified_at="2026-09-20T17:02:00Z",
            expected_commit="TEST-CCT005-VERIFICATION",
        )
        assert receipt["subject_ref"] == outcome["outcome_id"]
        assert receipt["evidence_refs"] == ["RCP-CCT005-ACTIVITY-001"]
        assert receipt["verification_state"] == "outcome_verified"
        assert receipt["verifier_type"] == "external_evidence"
        assert "authority_id" not in receipt
        assert "decision_id" not in receipt

        # Fail closed: a claim that the authoritative verifier rejects cannot
        # manufacture an outcome_verified receipt.
        rejected = dict(claim)
        rejected["status"] = "UNVERIFIED"
        try:
            vr.build_outcome_verification_receipt(
                outcome,
                activity_receipt_id="RCP-CCT005-ACTIVITY-001",
                claim=rejected,
                evidence_by_id={evidence["evidence_id"]: evidence},
                verify_claim_fn=er.verify_claim,
                receipt_id="VR-CCT005-REJECTED-001",
                expected_commit="TEST-CCT005-VERIFICATION",
            )
        except vr.VerificationReceiptRejected:
            pass
        else:
            raise AssertionError("unverified outcome must not emit outcome_verified receipt")


if __name__ == "__main__":
    test_verified_outcome_emits_receipt_after_authoritative_verification()
    print("PASS test_verified_outcome_emits_receipt_after_authoritative_verification")
