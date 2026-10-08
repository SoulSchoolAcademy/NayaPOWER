"""Tests for the REAL Human Value ledger (tools/human_value/ledgers/).

These tests prove the seam the continuity gate demanded: real measurement is
only real when it validates, recomputes deterministically for a cold
successor, and every event carries durable evidence. Numbers are NOT pinned
here — the ledger grows as real events are observed; determinism and
evidence-discipline are what get asserted.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.human_value import compute_hv  # noqa: E402
from tools.human_value.schema import SchemaError, validate_ledger  # noqa: E402

LEDGERS = REPO_ROOT / "tools" / "human_value" / "ledgers"
LEDGER = LEDGERS / "real-events.jsonl"
RECEIPTS = LEDGERS / "decision-predictions.json"


def load_events():
    raw_lines, events = compute_hv.load_ledger(LEDGER)
    return raw_lines, events


def test_real_ledger_validates_fail_closed():
    raw_lines, events = load_events()
    assert len(events) >= 1, "a real ledger with zero events measures nothing"
    validated = validate_ledger([json.loads(line) for line in raw_lines])
    assert len(validated) == len(events)


def test_real_ledger_has_no_synthetic_data():
    raw = LEDGER.read_text()
    assert "SYNTHETIC" not in raw, "example corpus must never leak into the real ledger"
    assert "example.invalid" not in raw


def test_every_real_event_carries_durable_evidence():
    _, events = load_events()
    for e in events:
        assert e["evidence"], f"{e['event_id']}: no evidence = no credit"
        for item in e["evidence"]:
            ref = item["ref"]
            assert ref.startswith("https://github.com/SoulSchoolAcademy/NayaPOWER/"), (
                f"{e['event_id']}: evidence ref is not a durable repo pointer: {ref}"
            )


def test_real_ledger_recomputes_deterministically():
    raw_lines, events = load_events()
    r1 = compute_hv.compute(events, 7, date(2026, 10, 8))
    r2 = compute_hv.compute(events, 7, date(2026, 10, 8))
    assert r1 == r2
    raw_lines_again, _ = compute_hv.load_ledger(LEDGER)
    assert compute_hv.ledger_sha256(raw_lines) == compute_hv.ledger_sha256(raw_lines_again)


def test_real_ledger_as_of_is_latest_event_date_not_wall_clock():
    _, events = load_events()
    latest = max(e["recorded_at"] for e in events)
    report = compute_hv.compute(events, 7, date.fromisoformat(latest))
    assert report["as_of"] == latest


def test_real_ledger_numbers_are_sane():
    _, events = load_events()
    report = compute_hv.compute(events, 7, date(2026, 10, 8))
    assert report["hv_per_day_total"] >= 0
    assert report["dai_per_day"] >= 0
    assert report["events_in_window"] == len(events)


def test_predictions_parse_and_join_integrity_holds():
    receipts = compute_hv.load_receipts(RECEIPTS)
    assert receipts, "the prediction side of the loop must not be empty"
    pred_ids = {r["decision_id"] for r in receipts}
    _, events = load_events()
    for e in events:
        if e.get("decision_id"):
            assert e["decision_id"] in pred_ids, (
                f"{e['event_id']}: decision_id has no pre-registered prediction "
                "(retroactive credit is forbidden)"
            )
    summary = compute_hv.calibrate(receipts, events)
    joined_ids = {row["decision_id"] for row in summary["records"]}
    expected = {
        e["decision_id"]
        for e in events
        if e.get("decision_id") and isinstance(e.get("delta_v_actual"), (int, float))
    }
    assert joined_ids == expected


def test_thin_evidence_does_not_move_the_profile():
    from tools.human_value import real_outcome_loop
    from kernel.value_calculus import QualityProfile

    receipts = compute_hv.load_receipts(RECEIPTS)
    _, events = load_events()
    profile = QualityProfile(profile_id="p", version="v1", objective="o")
    joined = real_outcome_loop.join_prediction_to_outcome(receipts, events)
    if len(joined) < 3:
        try:
            real_outcome_loop.recalibration_candidate(
                profile, "v-next", receipts, events, evidence_refs=[]
            )
        except ValueError as exc:
            assert ">= 3" in str(exc)
        else:
            raise AssertionError("recalibration must refuse thin evidence")


def test_second_real_observation_closes_this_runs_prediction():
    """DEC-20261008-HV-REALDATA-002 was pre-registered BEFORE this run's ledger
    work (predicted_at 2026-10-08T15:50:00Z, before any event was appended).
    Its outcome event closes the second real prediction->observation join
    (n=2). Recalibration must still honestly refuse below n=3."""
    from tools.human_value import real_outcome_loop
    from kernel.value_calculus import QualityProfile

    receipts = compute_hv.load_receipts(RECEIPTS)
    pred = next(
        r for r in receipts if r["decision_id"] == "DEC-20261008-HV-REALDATA-002"
    )
    assert pred["predicted_at"] < "2026-10-08T16:00:00Z", (
        "DEC-002 must be pre-registered before the work it predicts"
    )
    _, events = load_events()
    outcome = [
        e for e in events
        if e.get("decision_id") == "DEC-20261008-HV-REALDATA-002"
        and isinstance(e.get("delta_v_actual"), (int, float))
    ]
    assert len(outcome) == 1, "exactly one outcome event closes DEC-002"
    summary = compute_hv.calibrate(receipts, events)
    assert summary["n"] == 2, f"expected 2 joined observations, got {summary['n']}"
    joined = {row["decision_id"]: row for row in summary["records"]}
    assert joined["DEC-20261008-HV-REALDATA-002"]["delta_v_predicted"] == float(
        pred["delta_v_predicted"]
    )
    # Recalibration still refuses: n=2 is below the n>=3 floor. Honest, not gated by hope.
    profile = QualityProfile(profile_id="p", version="v1", objective="o")
    try:
        real_outcome_loop.recalibration_candidate(
            profile, "v-next", receipts, events, evidence_refs=[]
        )
    except ValueError as exc:
        assert ">= 3" in str(exc)
    else:
        raise AssertionError("recalibration must refuse at n=2")
