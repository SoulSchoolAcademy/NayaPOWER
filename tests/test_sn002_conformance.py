"""Tests for the mechanical SN-002 capture conformance gate.

A gate that has never been seen to FAIL is not a gate. These tests are written
failure-first: the negative controls are the substance. If this suite only ever
passes conformant captures, it proves nothing.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.sn002_conformance import (
    CEILING_REQUIRED,
    check_capture,
    check_dir,
    failures_only,
)

CAPTURE_DIR = Path(".naya/capture")

MINIMAL = {
    "schema": "naya.smart-note-capture.v2",
    "smart_note_id": "SN-TEST",
    "capture_id": "20260101-sntest-fixture",
    "title": "Fixture",
    "category": "SYSTEM_INTELLIGENCE",
    "topic": "T",
    "subtopic": "S",
    "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
    "source": {"captured_at": "2026-01-01"},
    "projection": {},
    "intelligence": {
        "essence": "e", "human_view": "h", "simple_view": "s",
        "naya_view": "n", "ai_view": "a",
        "machine_view": {
            "raw_source_separate_from_distillation": True,
            "automatic_truth_ceiling": CEILING_REQUIRED,
        },
        "decisions": [], "connections": [], "uncertainty": "u",
        "applicability": "a", "learning_lesson": "l", "successor_effect": "s",
    },
}


def _write(tmp_path: Path, mutate=None) -> Path:
    doc = json.loads(json.dumps(MINIMAL))
    if mutate:
        mutate(doc)
    p = tmp_path / "SMART-NOTE-20260101-sntest-fixture.json"
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


# ==========================================================================
# POSITIVE CONTROL
# ==========================================================================
def test_minimal_conformant_capture_passes(tmp_path):
    assert check_capture(_write(tmp_path)).conformant


# ==========================================================================
# NEGATIVE CONTROLS -- the substance of this gate
# ==========================================================================
def test_missing_raw_source_key_is_rejected(tmp_path):
    """The exact defect that made SN-020/021/022 RED."""
    def drop(doc):
        del doc["intelligence"]["machine_view"]["raw_source_separate_from_distillation"]
    res = check_capture(_write(tmp_path, drop))
    assert not res.conformant
    assert any("raw_source_separate_from_distillation" in v for v in res.violations)


def test_string_true_is_rejected_not_accepted_as_boolean(tmp_path):
    """A string "true" must NOT satisfy a typed boolean gate."""
    def stringify(doc):
        doc["intelligence"]["machine_view"]["raw_source_separate_from_distillation"] = "true"
    res = check_capture(_write(tmp_path, stringify))
    assert not res.conformant, "string 'true' was accepted as a boolean"


def test_integer_one_is_rejected(tmp_path):
    def one(doc):
        doc["intelligence"]["machine_view"]["raw_source_separate_from_distillation"] = 1
    assert not check_capture(_write(tmp_path, one)).conformant


def test_wrong_ceiling_value_is_rejected(tmp_path):
    def promote(doc):
        doc["intelligence"]["machine_view"]["automatic_truth_ceiling"] = "VERIFIED"
    res = check_capture(_write(tmp_path, promote))
    assert not res.conformant
    assert any("automatic_truth_ceiling" in v for v in res.violations)


def test_cannot_pass_by_omitting_machine_view(tmp_path):
    def omit(doc):
        del doc["intelligence"]["machine_view"]
    assert not check_capture(_write(tmp_path, omit)).conformant


def test_wrong_schema_is_rejected(tmp_path):
    def bad_schema(doc):
        doc["schema"] = "naya.smart-note-capture.v1"
    assert not check_capture(_write(tmp_path, bad_schema)).conformant


def test_malformed_json_reports_rather_than_raises(tmp_path):
    p = tmp_path / "SMART-NOTE-20260101-sntest-broken.json"
    p.write_text("{not json", encoding="utf-8")
    res = check_capture(p)
    assert not res.conformant and res.violations


# ==========================================================================
# THE FALSE-PASS SURFACE THIS REPLACES
# ==========================================================================
def test_prose_containing_the_words_does_not_satisfy_this_gate(tmp_path):
    """held_out() would pass this. This gate must not.

    The projected markdown can contain every keyword and still lack the field.
    A conformance gate must read the capture, not the prose.
    """
    def prose_only(doc):
        mv = doc["intelligence"]["machine_view"]
        del mv["raw_source_separate_from_distillation"]
        doc["intelligence"]["human_view"] = (
            "raw_source_separate_from_distillation true -- the transcript is "
            "not intelligence and the raw source is separate from distillation"
        )
    assert not check_capture(_write(tmp_path, prose_only)).conformant, (
        "prose containing the keywords satisfied a conformance gate"
    )


# ==========================================================================
# AGAINST THE REAL TREE
# ==========================================================================
def test_real_captures_are_classified_and_some_fail():
    """Ground truth: the known-bad captures must be REJECTED by this gate.

    If this ever passes everything, the gate has stopped discriminating and the
    suite above is no longer evidence of anything.
    """
    results = check_dir(CAPTURE_DIR)
    assert results, "no captures found -- test is not exercising anything"
    bad = failures_only(results)
    assert bad, (
        "every capture now conforms; the known-bad captures were expected to "
        "fail and their repair must be verified before this gate goes green"
    )


def test_conformant_captures_exist_too():
    """A gate that rejects everything is useless."""
    results = check_dir(CAPTURE_DIR)
    assert any(r.conformant for r in results), "gate rejects every capture"