#!/usr/bin/env python3
"""Regression tests for the execution-continuity contract."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime" / "continuity_enforcement.py"
spec = importlib.util.spec_from_file_location("continuity_enforcement", RUNTIME)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_positive_and_deliberate_failures():
    assert module.self_test() == 0


def test_completed_execution_requires_durable_successor():
    policy = module.load_policy()
    orphan = {
        "event_id": "SE-20260825-999999-continuity-orphan",
        "effective_at": policy["effective_at"],
        "event_type": "execution-milestone",
        "continuity": {"execution_state": "COMPLETED"},
        "ready_to_run_execution": "THIS IS NOT EXECUTABLE",
    }
    errors = module.check_event(orphan, Path("orphan.json"), policy)
    assert any("canonical NEXT-EXECUTION successor" in error for error in errors), errors
    print("INVALID ORPHAN → RED")

    embedded = {
        "event_id": "SE-20260825-999999-continuity-embedded",
        "effective_at": policy["effective_at"],
        "event_type": "execution-milestone",
        "project_context": {"project_id": "x", "current_daily_project": "x", "current_objective": "test"},
        "representations": {
            "naya": {"id": "n", "canonical_event_id": "SE-20260825-999999-continuity-embedded", "lessons": ["learned"]},
            "shawn": {"id": "s", "canonical_event_id": "SE-20260825-999999-continuity-embedded", "lessons": ["learned"]},
        },
        "verification": {"status": "VERIFIED", "receipt": "r"},
        "receipt": {"receipt_id": "r"},
        "delivery": {"state": "VERIFIED"},
        "continuity": {"execution_state": "COMPLETED", "handoff": {"mission": "x"}, "learning_status": "LEARNED", "next_action_status": "RECORDED"},
        "next_execution": {"project": "x", "north_star": "x", "current_state": "x", "completed_work": ["x"], "verified_evidence": ["x"], "unresolved_issues": ["x"], "constraints": ["x"], "current_objective": "x", "next_action": "run validation", "execution_instructions": "Run validation", "success_criteria": ["x"], "verification_requirements": ["x"]},
    }
    errors = module.check_event(embedded, Path("embedded.json"), policy)
    assert any("durable NEXT-EXECUTION artifact path" in error for error in errors), errors
    print("EMBEDDED NON-DURABLE SUCCESSOR → RED")


def test_blocked_execution_requires_continuation():
    policy = module.load_policy()
    blocked = {
        "event_id": "SE-20260825-999999-continuity-blocked",
        "effective_at": policy["effective_at"],
        "event_type": "execution-milestone",
        "continuity": {"execution_state": "IN_PROGRESS", "blocked": True, "next_action_status": "RECORDED"},
        "ready_to_run_execution": "THIS IS NOT EXECUTABLE",
    }
    errors = module.check_event(blocked, Path("blocked.json"), policy)
    assert any("blocked execution requires a canonical NEXT-EXECUTION continuation path" in error for error in errors), errors
    print("BLOCKED WITHOUT CONTINUATION → RED")


def test_current_canonical_corpus():
    code, report = module.validate()
    assert code == 0, report
    assert report["status"] == "GREEN"
    print("CONTINUITY VALIDATOR → GREEN")


def test_canonical_historical_event_ids_preserve_case():
    policy = module.load_policy()
    event = {
        "event_id": "SE-20260830-SMART-NOTE-DELIVERY-TEACHING",
        "effective_at": policy["effective_at"],
        "continuity": {"execution_state": "IN_PROGRESS", "next_action_status": "RECORDED", "learning_status": "LEARNED"},
        "representations": {"naya": {"lessons": ["learned"]}, "shawn": {"lessons": ["learned"]}},
        "verification": {"status": "PENDING"},
        "receipt": {"receipt_id": "r"},
        "delivery": {"state": "PERSISTED"},
    }
    errors = module.check_event(event, Path("historical.json"), policy)
    assert not any("invalid event_id" in error for error in errors), errors


if __name__ == "__main__":
    raise SystemExit(0 if module.self_test() == 0 else 1)