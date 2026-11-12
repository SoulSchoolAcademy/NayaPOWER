"""Tests for the Human Value instrument v1.

These tests prove the actual seam: measurement exists only when it is
validatable, deterministic, and recomputable by a cold successor. Every
fail-closed rule and every pinned number is asserted here — a green suite is
the instrument's proof of honesty.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from kernel.value_calculus import QualityProfile
from tools.human_value import compute_hv, real_outcome_loop
from tools.human_value.schema import SchemaError, validate_event, validate_ledger

EXAMPLES = REPO_ROOT / "tools" / "human_value" / "examples"
LEDGER = EXAMPLES / "example-events.jsonl"
RECEIPTS = EXAMPLES / "example-receipts.json"


def valid_event(**overrides):
    base = {
        "schema_version": "1",
        "event_id": "HV-20261008-001",
        "recorded_at": "2026-10-08",
        "value_type": "useful_outcome",
        "value_units": 1,
        "unit_description": "one human-requested outcome delivered",
        "evidence": [{"kind": "feed_comment", "ref": "https://example.invalid/x"}],
    }
    base.update(overrides)
    return base


# ---- Example corpus: pinned, deterministic recomputation --------------------

def test_example_corpus_computes_pinned_values():
    raw_lines, events = compute_hv.load_ledger(LEDGER)
    assert len(events) == 8
    report = compute_hv.compute(events, 7, date(2026, 10, 7))
    hv = report["hv_per_day_by_type"]
    assert hv["cognitive_load_reduced"] == pytest.approx(75 / 7, abs=1e-4)
    assert hv["rework_avoided"] == pytest.approx(3 / 7, abs=1e-4)
    assert hv["error_prevented"] == pytest.approx(1 / 7, abs=1e-4)
    assert hv["useful_outcome"] == pytest.approx(4 / 7, abs=1e-4)
    assert hv["attention_demanded"] == pytest.approx(2 / 7, abs=1e-4)
    assert report["hv_per_day_total"] == pytest.approx(85 / 7, abs=1e-4)
    assert report["dai_per_day"] == pytest.approx(2 / 7, abs=1e-4)
    assert report["events_validated"] == 8
    assert report["events_in_window"] == 8


def test_recomputation_is_deterministic():
    _, events_a = compute_hv.load_ledger(LEDGER)
    _, events_b = compute_hv.load_ledger(LEDGER)
    ra = compute_hv.compute(events_a, 7, date(2026, 10, 7))
    rb = compute_hv.compute(events_b, 7, date(2026, 10, 7))
    assert ra == rb


def test_ledger_hash_is_stable_and_sensitive():
    lines_a, _ = compute_hv.load_ledger(LEDGER)
    h1 = compute_hv.ledger_sha256(lines_a)
    h2 = compute_hv.ledger_sha256(lines_a)
    assert h1 == h2 and h1.startswith("sha256:")
    tampered = lines_a + [lines_a[0]]
    assert compute_hv.ledger_sha256(tampered) != h1


def test_window_excludes_old_events():
    old = valid_event(event_id="HV-OLD-001", recorded_at="2026-09-01",
                      value_type="useful_outcome", value_units=100)
    new = valid_event(event_id="HV-NEW-001", recorded_at="2026-10-07",
                      value_type="useful_outcome", value_units=1)
    events = validate_ledger([old, new])
    report = compute_hv.compute(events, 7, date(2026, 10, 7))
    assert report["events_in_window"] == 1
    assert report["hv_per_day_by_type"]["useful_outcome"] == pytest.approx(1 / 7, abs=1e-4)


# ---- Fail closed: no credit without valid evidence -------------------------

@pytest.mark.parametrize("mutation", [
    {"evidence": []},                                            # empty evidence
    {"evidence": [{"kind": "feed_comment", "ref": ""}]},          # empty ref
    {"evidence": [{"kind": "telegram", "ref": "x"}]},             # unknown kind
    {"evidence": [{"kind": "content_hash", "ref": "not-a-hash"}]},# malformed hash
    {"evidence": "not-a-list"},                                  # wrong shape
])
def test_no_evidence_no_credit(mutation):
    with pytest.raises(SchemaError):
        validate_event(valid_event(**mutation))


def test_duplicate_event_id_fails_closed():
    e1 = valid_event(event_id="HV-DUP-001")
    e2 = valid_event(event_id="HV-DUP-001")
    with pytest.raises(SchemaError, match="duplicate event_id"):
        validate_ledger([e1, e2])


@pytest.mark.parametrize("mutation", [
    {"value_type": "vibes"},                 # unknown type
    {"value_units": -1},                      # negative units
    {"value_units": float("inf")},            # non-finite
    {"recorded_at": "10/08/2026"},            # bad date
    {"schema_version": "2"},                 # wrong version
    {"delta_v_actual": 11.0},                # out of calculus range
    {"mystery_field": "x"},                  # strict schema: unknown field
    {"beneficiary": "everyone"},              # unknown beneficiary
])
def test_malformed_event_fails_closed(mutation):
    with pytest.raises(SchemaError):
        validate_event(valid_event(**mutation))


def test_missing_required_field_fails_closed():
    e = valid_event()
    del e["unit_description"]
    with pytest.raises(SchemaError, match="unit_description"):
        validate_event(e)


# ---- Real-outcome loop: prediction meets observation ------------------------

def _receipts():
    return json.loads(RECEIPTS.read_text(encoding="utf-8"))


def test_calibration_join_is_correct():
    _, events = compute_hv.load_ledger(LEDGER)
    summary = real_outcome_loop.calibrate(_receipts(), events)
    assert summary["n"] == 3
    # errors: |6.5-7.0|=0.5, |7.0-6.0|=1.0, |4.0-6.5|=2.5
    assert summary["mean_absolute_error"] == pytest.approx(4.0 / 3, abs=1e-9)
    # signed: -0.5 +1.0 -2.5 = -2.0
    assert summary["mean_signed_error"] == pytest.approx(-2.0 / 3, abs=1e-9)
    assert summary["overprediction_detected"] is True
    assert summary["confidence_multiplier"] == pytest.approx(1 / (1 + 4.0 / 3), abs=1e-9)


def test_partial_rows_are_dropped_not_imputed():
    # event with decision_id but no observed outcome: cannot join
    orphan = valid_event(event_id="HV-ORPHAN-001", decision_id="DEC-EXAMPLE-001")
    events = validate_ledger([orphan])
    summary = real_outcome_loop.calibrate(_receipts(), events)
    assert summary["n"] == 0
    assert summary["mean_absolute_error"] == 0.0


def test_recalibration_needs_thin_evidence_gate():
    profile = QualityProfile(profile_id="p", version="v1", objective="o")
    orphan = validate_ledger([valid_event(event_id="HV-T-001", decision_id="DEC-EXAMPLE-001")])
    with pytest.raises(ValueError, match=">= 3 joined observations"):
        real_outcome_loop.recalibration_candidate(
            profile, "v2", _receipts(), orphan, ["evidence"])
    _, events = compute_hv.load_ledger(LEDGER)
    receipt = real_outcome_loop.recalibration_candidate(
        profile, "v2", _receipts(), events, ["sha256:pinned"])
    assert receipt["receipt_type"] == "VALUE_RECALIBRATION"
    assert receipt["state"] == "LEARN_CANDIDATE"
    assert receipt["automatic_promotion"] is False
    assert receipt["calibration_summary"]["n"] == 3


# ---- CLI: fail-closed exits -------------------------------------------------

def test_cli_succeeds_on_example_corpus(capsys):
    rc = compute_hv.main(["--ledger", str(LEDGER), "--receipts", str(RECEIPTS)])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["hv_per_day_total"] == pytest.approx(85 / 7, abs=1e-4)
    assert out["calibration"]["n"] == 3
    assert out["ledger_sha256"].startswith("sha256:")


def test_cli_fails_closed_on_ledger_drift(capsys, tmp_path):
    bad = tmp_path / "bad.jsonl"
    bad.write_text('{"schema_version": "1", "event_id": "x"}\n', encoding="utf-8")
    rc = compute_hv.main(["--ledger", str(bad)])
    assert rc == 2  # schema error, no number emitted


def test_cli_fails_closed_on_hash_mismatch(capsys):
    rc = compute_hv.main(["--ledger", str(LEDGER),
                          "--expect-ledger-sha256", "sha256:deadbeef"])
    assert rc == 2


def test_cli_fails_closed_on_empty_ledger(capsys, tmp_path):
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    rc = compute_hv.main(["--ledger", str(empty)])
    assert rc == 2
