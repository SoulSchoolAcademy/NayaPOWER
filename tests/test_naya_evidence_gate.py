"""Tests for the intelligence-evaluation evidence gate.

These tests are deliberately adversarial: the evaluator must reject artifacts that
look persuasive but do not prove execution, causality, learning, or continuity.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from naya_evidence_gate import evaluate_receipt, load_receipt


def receipt(**overrides):
    base = {
        "schema": "naya/intelligence-evaluation-receipt/v1",
        "test_id": "N9-001",
        "fixture_id": "fixture-001",
        "source_commit": "abc123",
        "runtime_version": "50",
        "input_hash": "sha256:input",
        "execution_path": ["real_entrypoint", "real_runtime", "real_assertion"],
        "state_before": {"status": "COLD"},
        "state_after": {"status": "SUCCESS"},
        "evidence_ids": ["evt-1", "receipt-1"],
        "authority_decision": "AUTHORIZED",
        "expected": {"status": "SUCCESS"},
        "actual": {"status": "SUCCESS"},
        "failures": [],
        "uncertainties": [],
        "reproduction": {"command": "python test.py", "result": "PASS"},
        "evidence_level": "L4_VERIFIED",
        "causal": {
            "claim": "runtime change caused outcome",
            "control": "control-run-1",
            "treatment": "treatment-run-1",
            "confounders": [],
        },
        "learning": {
            "outcome_observed": True,
            "lesson": "lesson-1",
            "persisted": True,
            "retrieved": True,
            "behavior_changed": True,
            "measured_improvement": 0.2,
        },
        "cold_successor": {
            "cold_run": True,
            "inherited_evidence": ["receipt-1"],
            "continuation_action": "next-action",
        },
        "evaluator_integrity": {
            "positive_control": "PASS",
            "negative_control": "PASS",
            "mutation_control": "PASS",
            "contradiction_control": "PASS",
            "stale_control": "PASS",
            "cold_control": "PASS",
        },
        "system_learning": "evaluator rejects assertion-only evidence",
    }
    base.update(overrides)
    return base


def test_verified_receipt_is_accepted():
    verdict = evaluate_receipt(receipt())
    assert verdict.status == "PASS"
    assert verdict.evidence_level == "L4_VERIFIED"


def test_assertion_only_receipt_is_rejected():
    r = receipt(
        evidence_ids=[],
        execution_path=[],
        reproduction={"command": "", "result": "ASSERTION_ONLY"},
        actual={"status": "SUCCESS", "source": "static-file"},
    )
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert "execution" in " ".join(verdict.reasons).lower()


def test_learning_claim_requires_measured_behavior_change():
    r = receipt(learning={
        "outcome_observed": True,
        "lesson": "lesson-1",
        "persisted": True,
        "retrieved": True,
        "behavior_changed": True,
        "measured_improvement": None,
    })
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("measured" in reason.lower() for reason in verdict.reasons)


def test_causal_claim_requires_control_and_treatment():
    r = receipt(causal={
        "claim": "architecture caused improvement",
        "control": None,
        "treatment": "treatment-run-1",
        "confounders": [],
    })
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("control" in reason.lower() for reason in verdict.reasons)


def test_stale_evidence_cannot_pass_as_current():
    r = receipt(source_freshness="STALE")
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("stale" in reason.lower() for reason in verdict.reasons)


def test_cold_successor_requires_an_actual_continuation_action():
    r = receipt(cold_successor={
        "cold_run": True,
        "inherited_evidence": ["receipt-1"],
        "continuation_action": None,
    })
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("successor" in reason.lower() for reason in verdict.reasons)


def test_unknown_must_not_be_upgraded_by_language():
    r = receipt(
        evidence_level="L0_ASSERTED",
        actual={"status": "PASS", "language": "PROVEN"},
        reproduction={"command": "echo proven", "result": "PASS"},
    )
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("level" in reason.lower() or "assert" in reason.lower()
               for reason in verdict.reasons)


def test_receipt_round_trip(tmp_path: Path):
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt()), encoding="utf-8")
    loaded = load_receipt(path)
    assert loaded["test_id"] == "N9-001"
    assert evaluate_receipt(loaded).status == "PASS"


def test_evaluator_integrity_is_load_bearing():
    r = receipt(evaluator_integrity={
        "positive_control": "PASS",
        "negative_control": "FAIL",
        "mutation_control": "PASS",
        "contradiction_control": "PASS",
        "stale_control": "PASS",
        "cold_control": "PASS",
    })
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("negative" in reason.lower() for reason in verdict.reasons)


def test_l5_requires_causal_controls():
    r = receipt(evidence_level="L5_CAUSALLY_ATTRIBUTED", causal={})
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("causal" in reason.lower() for reason in verdict.reasons)


def test_l6_requires_held_out_generalization():
    r = receipt(evidence_level="L6_GENERALIZED", generalization={})
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("general" in reason.lower() or "held" in reason.lower()
               for reason in verdict.reasons)


def test_l7_requires_generational_compounding():
    r = receipt(evidence_level="L7_COMPOUNDED", compounding={})
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("compound" in reason.lower() or "generation" in reason.lower()
               for reason in verdict.reasons)


def test_learning_requires_positive_measured_improvement():
    r = receipt(learning={
        "outcome_observed": True,
        "lesson": "lesson-1",
        "persisted": True,
        "retrieved": True,
        "behavior_changed": True,
        "measured_improvement": 0,
    })
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("improvement" in reason.lower() for reason in verdict.reasons)


def test_stale_control_must_itself_be_load_bearing():
    r = receipt(source_freshness="CURRENT", evaluator_integrity={
        "positive_control": "PASS",
        "negative_control": "PASS",
        "mutation_control": "PASS",
        "contradiction_control": "PASS",
        "stale_control": "FAIL",
        "cold_control": "PASS",
    })
    verdict = evaluate_receipt(r)
    assert verdict.status == "FAIL"
    assert any("stale" in reason.lower() for reason in verdict.reasons)
