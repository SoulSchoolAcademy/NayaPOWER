"""Contract and real-selector diagnostic for the 43-lesson candidate exam.

A GREEN result means the test infrastructure ran and described its outcomes
truthfully, NEVER that Naya proved 43 lessons or authorization to ACT.
"""
import hashlib
import warnings
from pathlib import Path

from tools import learning_exam_43 as exam


def test_43_unique_lessons_and_held_out_scenarios():
    key = exam.read_cases()
    assert len(key["cases"]) == 43
    assert key["unspecified_remaining"] == 2
    for c in key["cases"]:
        assert c["scenario"] and c["expected_behavior"]
        assert c["wrong_lesson_id"] != c["smart_note_id"]
        assert c["scoring_status"] == "NOT_RUN"
        assert c["canonical_receipt_verified"] is False


def test_blind_prompts_never_ship_answer_key():
    x = exam.make_blind_questions()
    assert x["num_cases"] == 43
    assert x["answer_key_included"] is False
    assert len(x["cases"]) == 43
    assert all(set(c) == {"test_id", "scenario"} for c in x["cases"])
    assert all("expected_behavior" not in c and "smart_note_id" not in c
               for c in x["cases"])


def test_real_43_case_retrieval_audit_runs_without_mutating_canonical_intelligence():
    before = hashlib.sha256(exam.REGISTRY.read_bytes()).hexdigest()
    out = exam.audit_repository_retrieval()
    after = hashlib.sha256(exam.REGISTRY.read_bytes()).hexdigest()
    assert before == after, "A retrieval exam MUST NOT mutate the canonical registry"
    assert out["cases"] == 43
    assert len(out["results"]) == 43
    assert sum(out["retrieval_counts"].values()) == 43
    assert out["test_type"] == "DIAGNOSTIC_ONLY_NOT_LEARNING"
    assert out["full_learning_passes_basis"] == "NOT_TESTED_NO_VERIFIED_OUTCOME"
    assert out["full_learning_passes"] == 0
    assert any(x["retrieval"] == "BLOCKED_ID_COLLISION" for x in out["results"]), (
        "The known SN-0501 collision must be surfaced, not silently resolved."
    )
    warnings.warn(
        "43-LESSON REAL RETRIEVAL DIAGNOSTIC (NOT A LEARNING SCORE): "
        + str(out["retrieval_counts"])
        + "; full causal/authorization/successor tests NOT_RUN",
        UserWarning,
        stacklevel=1,
    )
