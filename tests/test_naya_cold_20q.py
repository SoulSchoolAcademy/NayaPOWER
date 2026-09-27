from __future__ import annotations

import json
from pathlib import Path

from naya_cold_20q import examine


def valid_receipt():
    return {
        "schema": "naya/intelligence-evaluation-receipt/v1",
        "test_id": "Q",
        "fixture_id": "F",
        "source_commit": "abc",
        "runtime_version": "1",
        "input_hash": "sha256:x",
        "execution_path": ["real"],
        "state_before": {},
        "state_after": {"status": "SUCCESS"},
        "evidence_ids": ["e1"],
        "authority_decision": "AUTHORIZED",
        "expected": {"status": "SUCCESS"},
        "actual": {"status": "SUCCESS"},
        "failures": [],
        "uncertainties": [],
        "reproduction": {"command": "real", "result": "PASS"},
        "evidence_level": "L4_VERIFIED",
        "evaluator_integrity": {
            "positive_control": "PASS",
            "negative_control": "PASS",
            "mutation_control": "PASS",
            "contradiction_control": "PASS",
            "stale_control": "PASS",
            "cold_control": "PASS",
        },
    }


def test_cold_runner_ignores_prose_and_static_json(tmp_path: Path):
    p = tmp_path / ".naya" / "project-intelligence"
    p.mkdir(parents=True)
    (p / "claim.json").write_text(
        json.dumps({"status": "PROVEN", "future_behavior_changed": True}),
        encoding="utf-8",
    )
    report = examine(tmp_path)
    assert report["valid_receipts"] == 0
    assert report["answerable"] == 0
    assert report["unproven"] == 20


def test_cold_runner_accepts_only_gate_valid_receipts(tmp_path: Path):
    p = tmp_path / ".naya" / "receipts"
    p.mkdir(parents=True)
    (p / "receipt.json").write_text(json.dumps(valid_receipt()), encoding="utf-8")
    report = examine(tmp_path)
    assert report["valid_receipts"] == 1
    assert report["answerable"] >= 1


def test_cold_runner_requires_stronger_levels_for_causal_and_compounding():
    # The runner's question table itself must preserve the promotion boundaries.
    from naya_cold_20q import QUESTIONS
    levels = {q.id: q.minimum_level for q in QUESTIONS}
    assert levels["Q13"] == "L5_CAUSALLY_ATTRIBUTED"
    assert levels["Q18"] == "L7_COMPOUNDED"
    assert levels["Q19"] == "L8_COLD_SUCCESSOR_PROVEN"
