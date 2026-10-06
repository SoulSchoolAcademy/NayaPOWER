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

# ==========================================================================
# RATCHET -- the debt is grandfathered, the drift class is not
# ==========================================================================
def test_ratchet_blocks_a_new_non_conformant_capture(tmp_path):
    """THE load-bearing test. A new bad capture must be BLOCKED.

    This is what makes the gate a real gate: legacy debt is exempted, anything
    new must pass. Without this, --ratchet would be --report with extra steps.
    """
    from tools.sn002_conformance import ratchet_violations

    def drop(doc):
        del doc["intelligence"]["machine_view"]["raw_source_separate_from_distillation"]

    new_bad = check_capture(_write(tmp_path, drop))
    assert not new_bad.conformant
    blocked = ratchet_violations([new_bad], baseline=set())  # baseline irrelevant
    assert len(blocked) == 1, "a NEW non-conformant capture was not blocked"


def test_ratchet_grandfathers_named_legacy_capture(tmp_path):
    from tools.sn002_conformance import ratchet_violations

    def drop(doc):
        del doc["intelligence"]["machine_view"]["raw_source_separate_from_distillation"]

    legacy = check_capture(_write(tmp_path, drop))
    name = Path(legacy.path).name
    assert ratchet_violations([legacy], baseline={name}) == []
    assert len(ratchet_violations([legacy], baseline=set())) == 1


def test_baseline_never_grows():
    """A ratchet that can grow is a permanent exemption, not a ratchet."""
    from tools.sn002_conformance import load_baseline

    exempt = load_baseline()
    assert isinstance(exempt, set)
    results = check_dir(CAPTURE_DIR)
    failing_names = {Path(r.path).name for r in failures_only(results)}
    # Every non-conformant capture must be named, or the ratchet is not armed.
    assert failing_names <= exempt, (
        f"non-conformant captures absent from the baseline (ratchet would "
        f"block them): {sorted(failing_names - exempt)}"
    )


def test_baseline_entries_that_now_conform_are_retirable(tmp_path):
    """The repair path: a conforming baseline entry must be droppable."""
    from tools.sn002_conformance import load_baseline, stale_baseline_entries

    exempt = load_baseline()
    good = check_capture(_write(tmp_path))
    stale = stale_baseline_entries([good], baseline=exempt | {Path(good.path).name})
    assert Path(good.path).name in stale


# ==========================================================================
# CORRECTION LIFECYCLE — historical defects stay immutable, not exempt
# ==========================================================================
def _write_correction_pair(tmp_path, *, successor_good=True, include_edge=True):
    r1 = json.loads(json.dumps(MINIMAL))
    r1["smart_note_id"] = "SN-100"
    r1["capture_id"] = "capture-r1"
    r1["lifecycle_state"] = "SUPERSEDED"
    r1["superseded_by_capture_id"] = "capture-r2"
    r1["supersession_reason"] = "R2 corrects a historical typed-machine defect."
    del r1["intelligence"]["machine_view"]["raw_source_separate_from_distillation"]

    r2 = json.loads(json.dumps(MINIMAL))
    r2["smart_note_id"] = "SN-101"
    r2["capture_id"] = "capture-r2"
    r2["lifecycle_state"] = "ACTIVE"
    if not successor_good:
        del r2["intelligence"]["machine_view"]["raw_source_separate_from_distillation"]
    r2["intelligence"]["connections"] = (
        [{"type": "SUPERSEDES", "target": "SN-100 — historical R1"}]
        if include_edge else []
    )

    (tmp_path / "SMART-NOTE-r1.json").write_text(
        json.dumps(r1, indent=2), encoding="utf-8")
    (tmp_path / "SMART-NOTE-r2.json").write_text(
        json.dumps(r2, indent=2), encoding="utf-8")
    return {r.capture_id: r for r in check_dir(tmp_path)}


def test_superseded_historical_gap_requires_conformant_successor_and_edge(tmp_path):
    results = _write_correction_pair(tmp_path)
    assert results["capture-r1"].conformant, results["capture-r1"].violations
    assert results["capture-r2"].conformant, results["capture-r2"].violations
    assert any("historical superseded capture" in a
               for a in results["capture-r1"].advisories)


def test_superseded_label_cannot_bypass_gate_without_successor(tmp_path):
    _write_correction_pair(tmp_path)
    (tmp_path / "SMART-NOTE-r2.json").unlink()
    results = check_dir(tmp_path)
    assert len(results) == 1
    assert not results[0].conformant
    assert any("target not found" in v for v in results[0].violations)


def test_superseded_label_cannot_point_to_nonconformant_successor(tmp_path):
    results = _write_correction_pair(tmp_path, successor_good=False)
    assert not results["capture-r2"].conformant
    assert not results["capture-r1"].conformant
    assert any("non-conformant" in v for v in results["capture-r1"].violations)


def test_superseded_label_requires_explicit_supersedes_edge(tmp_path):
    results = _write_correction_pair(tmp_path, include_edge=False)
    assert results["capture-r2"].conformant
    assert not results["capture-r1"].conformant
    assert any("SUPERSEDES edge" in v for v in results["capture-r1"].violations)


# ==========================================================================
# PROTECTED INTELLIGENCE — deletion must fail closed
# ==========================================================================
def _load_protected_registry():
    path = Path(".naya/protected-intelligence.json")
    assert path.is_file(), "protected-intelligence registry missing"
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_capture_ids():
    ids = {}
    for path in CAPTURE_DIR.glob("SMART-NOTE-*.json"):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        note_id = doc.get("smart_note_id") or doc.get("id")
        if note_id:
            ids[str(note_id)] = path
    return ids


def test_protected_intelligence_registry_has_unique_ids():
    registry = _load_protected_registry()
    protected = registry.get("protected", [])
    ids = [entry.get("smart_note_id") for entry in protected]
    assert ids and all(ids), "protected registry must contain named Smart Note IDs"
    assert len(ids) == len(set(ids)), "protected registry contains duplicate Smart Note IDs"


def test_every_protected_smart_note_exists_on_canonical_capture_surface():
    """Regression for a2f103f4: protected intelligence cannot disappear silently."""
    registry = _load_protected_registry()
    present = _canonical_capture_ids()
    missing = [
        entry["smart_note_id"]
        for entry in registry.get("protected", [])
        if entry["smart_note_id"] not in present
    ]
    assert not missing, (
        "PROTECTED INTELLIGENCE DELETION: canonical Smart Note(s) disappeared: "
        f"{missing}. Cleanup/optimization/duplication is not retirement authority."
    )


def test_incident_laws_are_mechanically_protected():
    """Specific negative-control anchor for the SN-0358/SN-0359 incident."""
    registry = _load_protected_registry()
    protected = {entry["smart_note_id"] for entry in registry.get("protected", [])}
    assert {"SN-0358", "SN-0359", "SN-0360"} <= protected
