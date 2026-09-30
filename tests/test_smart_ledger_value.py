"""Deterministic tests for the SmartLedger V2.1 typed value receipt seam.

Covers: legacy V1 preservation, malformed receipts, evidence-before-reward,
valid V2.1 receipts (decision + contribution), writer idempotency/replay,
cross-owner isolation, privacy, unverified/duplicate/spam contributions, and
independent reconstruction (reread -> same calculation).

The SQL migration cannot be executed against a live database in this
environment; the in-memory writer below faithfully simulates the documented
semantics of nayanet_record_ledger_event() (unique(owner,source_table,
source_id), hash chain, owner isolation) and is labeled as such. The
companion script supabase/tests/nayanet_value_receipts_v21_tests.sql runs
the same cases against the real functions.
"""

import copy
import hashlib
import json

import pytest

from kernel.smart_ledger_value import (
    ENGINE,
    ReceiptError,
    build_alignment_decision_receipt,
    build_contribution_value_receipt,
    classify_value_assessment,
    is_legacy_starting_model,
    receipt_canonical_hash,
    recompute_contribution_from_receipt,
    recompute_decision_from_receipt,
    validate_value_receipt,
)
from kernel.value_calculus import (
    Candidate,
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
)

OWNER_A = "11111111-1111-1111-1111-111111111111"
OWNER_B = "22222222-2222-2222-2222-222222222222"
ACTOR = "33333333-3333-3333-3333-333333333333"
TS = "2026-09-30T23:59:00+00:00"

# Historical NayaNET_V1_STARTING_MODEL rows, exactly as the triggers write them.
LEGACY_NOTE_V1 = {"assessed": False, "base_points": 5,
                  "value_engine": "NayaNET_V1_STARTING_MODEL"}
LEGACY_SPACE_V1 = {"assessed": False, "base_points": 10,
                   "value_engine": "NayaNET_V1_STARTING_MODEL"}


def _contribution(**over):
    kw = dict(
        actor_id=ACTOR, owner_id=OWNER_A,
        source_table="smart_note_events", source_id="note-1",
        action_class="verified_intelligence",
        quality=0.8, relevance=0.9, verification=1.0, impact=0.7, novelty=0.8,
        verified_delta=3.0, points_per_unit=10.0,
        verification_state="VERIFIED_PASS",
        evidence=[{"source_table": "smart_note_receipts", "source_id": "r-1"}],
        recorded_by=ACTOR, recorded_at=TS,
    )
    kw.update(over)
    return build_contribution_value_receipt(**kw)


# --------------------------------------------------------------------------
# 1. Legacy preservation: history is never rewritten or reinterpreted.
# --------------------------------------------------------------------------

def test_legacy_v1_rows_classify_unassessed_and_are_untouched():
    for legacy in (LEGACY_NOTE_V1, LEGACY_SPACE_V1):
        before = copy.deepcopy(legacy)
        assert is_legacy_starting_model(legacy) is True
        assert classify_value_assessment(legacy) == "UNASSESSED"
        assert legacy == before  # byte-identical; classification never mutates


def test_legacy_rows_fail_typed_validation():
    # Legacy rows are provenance, not typed receipts: they must NOT validate
    # as V2.1 receipts (no silent reinterpretation).
    for legacy in (LEGACY_NOTE_V1, LEGACY_SPACE_V1):
        with pytest.raises(ReceiptError):
            validate_value_receipt(legacy)


# --------------------------------------------------------------------------
# 2. Malformed receipts are rejected with a reason.
# --------------------------------------------------------------------------

def _mutate(base, path, value):
    r = copy.deepcopy(base)
    node = r
    for key in path[:-1]:
        node = node[key]
    if value is _MISSING:
        node.pop(path[-1], None)
    else:
        node[path[-1]] = value
    return r


_MISSING = object()


@pytest.mark.parametrize("path,value", [
    (["receipt_type"], "POINTS"),
    (["receipt_type"], _MISSING),
    (["engine"], "SOMETHING_ELSE"),
    (["engine_version"], "1.0"),
    (["verification_state"], "MAYBE"),
    (["inputs"], {}),
    (["inputs"], _MISSING),
    (["evidence"], {}),
    (["value_calculation"], {}),
    (["points_derivation"], _MISSING),
    (["provenance"], _MISSING),
    (["provenance", "owner_id"], ""),
    (["provenance", "source_table"], _MISSING),
    (["privacy_classification"], "SUPER_PUBLIC"),
    (["value_calculation", "cvs"], 9.5),
    (["value_calculation", "cvs"], -9.5),
    (["value_calculation", "factors"], {}),
    (["inputs", "action_class"], ""),
])
def test_malformed_contribution_receipts_rejected(path, value):
    bad = _mutate(_contribution(), path, value)
    with pytest.raises(ReceiptError) as exc:
        validate_value_receipt(bad)
    assert "VALUE_RECEIPT_INVALID" in str(exc.value)


def test_malformed_alignment_receipt_rejected():
    good = _alignment_receipt()
    bad = _mutate(good, ["decision_receipt"], {"receipt_type": "NOPE"})
    with pytest.raises(ReceiptError):
        validate_value_receipt(bad)


# --------------------------------------------------------------------------
# 3. Evidence before reward: no points without verification.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("state", ["UNVERIFIED", "PASS_PENDING_WINDOW", "FAIL", "ESCALATE"])
def test_points_require_verified_pass(state):
    r = _contribution(verification_state=state)
    assert r["points_derivation"]["points_awarded"] == 0
    assert classify_value_assessment(r) == ("VERIFIED_VALUE" if state == "VERIFIED_PASS" else "ASSESSED")
    tampered = copy.deepcopy(r)
    tampered["points_derivation"]["points_awarded"] = 5
    with pytest.raises(ReceiptError) as exc:
        validate_value_receipt(tampered)
    assert "evidence before reward" in str(exc.value)


def test_negative_cvs_is_evidence_never_punishment():
    r = _contribution(verified_delta=-4.0)
    assert r["value_calculation"]["cvs"] < 0
    assert r["points_derivation"]["points_awarded"] == 0
    assert classify_value_assessment(r) == "VERIFIED_VALUE"


def test_repeat_decay_defeats_farming():
    first = _contribution(repeat_count=1)
    third = _contribution(repeat_count=3)
    assert third["points_derivation"]["repeat_decay"] == pytest.approx(1 / 3)
    assert third["points_derivation"]["points_awarded"] == pytest.approx(
        first["points_derivation"]["points_awarded"] / 3
    )
    assert third["points_derivation"]["points_awarded"] > 0  # still recognition, just decayed


def test_unverified_contribution_records_zero_points():
    r = _contribution(verification_state="UNVERIFIED")
    assert r["value_calculation"]["cvs"] > 0  # value assessed...
    assert r["points_derivation"]["points_awarded"] == 0  # ...but no reward yet
    assert classify_value_assessment(r) == "ASSESSED"


# --------------------------------------------------------------------------
# 4. Valid V2.1 receipts: decision + contribution end to end.
# --------------------------------------------------------------------------

def _dims(score=8.0, conf=0.9):
    dims = ["objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity"]
    return {d: score for d in dims}, {d: conf for d in dims}


def _pv(B=5.0, conf=0.9):
    from kernel.value_calculus import PVEstimate
    return PVEstimate(B, 1.0, 1.0, 0.5,
                      {k: conf for k in ("B", "H", "C", "R")}, 5)


def _decision_inputs():
    q, c = _dims()
    hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    base = Candidate("do_nothing", q, c, _pv(B=5.0), authorized=True,
                     is_baseline=True, **hard)
    act = Candidate("assess_note", q, c, _pv(B=8.0), authorized=True, **hard)
    return [base, act]


def _profile():
    return QualityProfile(
        profile_id="NAYAPOWER-DECISION",
        version="2.1",
        objective="maximum responsible verified value",
        min_evidence_count=2,
        relative_margin=0.10,
    )


def _alignment_receipt(verification="VERIFIED_PASS"):
    from kernel.value_calculus import build_decision_receipt
    evaluation = evaluate_candidates(_decision_inputs(), "do_nothing",
                                     _profile(), RiskPolicy())
    inner = build_decision_receipt(
        decision_id="dec-1", objective="assess contribution",
        baseline_id="do_nothing", stakeholders=["member"],
        horizon="session", evaluation=evaluation,
        authority_basis="human_director", evidence_refs=["note-1"],
        observation_window={"status": "closed"}, verification=verification,
        delta_v_actual=2.0,
    )
    return build_alignment_decision_receipt(
        decision_receipt=inner, owner_id=OWNER_A,
        source_table="value_decisions", source_id="dec-1",
        recorded_by=ACTOR, recorded_at=TS,
    )


def test_valid_alignment_decision_receipt():
    r = _alignment_receipt()
    assert r["receipt_type"] == "ALIGNMENT_DECISION"
    assert r["engine"] == ENGINE
    # Embedded canonical receipt is byte-identical (strict-JSON schema still applies).
    assert r["decision_receipt"]["receipt_type"] == "ALIGNMENT_DECISION"
    assert r["decision_receipt"]["schema_version"] == "2.1"
    # Decision receipts mint no recognition points.
    assert r["points_derivation"]["points_awarded"] == 0
    assert classify_value_assessment(r) == "VERIFIED_VALUE"


def test_pending_window_decision_is_assessed_not_verified_value():
    r = _alignment_receipt(verification="PASS_PENDING_WINDOW")
    assert classify_value_assessment(r) == "ASSESSED"


def test_contribution_points_math_matches_kernel():
    r = _contribution()
    from kernel.value_calculus import contribution_value_score, contribution_points
    expected_cvs = contribution_value_score(
        quality=0.8, relevance=0.9, verification=1.0, impact=0.7,
        novelty=0.8, verified_delta=3.0)
    assert r["value_calculation"]["cvs"] == pytest.approx(expected_cvs)
    assert r["points_derivation"]["points_awarded"] == pytest.approx(
        contribution_points(expected_cvs, 10.0, 1.0))
    assert classify_value_assessment(r) == "VERIFIED_VALUE"


# --------------------------------------------------------------------------
# 5. Writer semantics: idempotency, replay, cross-owner isolation, privacy.
#    (In-memory simulation of nayanet_record_ledger_event() semantics.)
# --------------------------------------------------------------------------

class FakeSmartLedger:
    """Simulates the SQL writer's documented semantics:
    unique(owner_id, source_table, source_id); hash-chained; immutable replay;
    provenance owner must equal the recording owner (cross-owner isolation)."""

    def __init__(self):
        self.rows = {}

    def record_value_receipt(self, owner_id, receipt, privacy="PRIVATE"):
        validate_value_receipt(receipt)
        prov_owner = receipt["provenance"]["owner_id"]
        if prov_owner != owner_id:
            raise ReceiptError("VALUE_RECEIPT_OWNER_MISMATCH")
        if privacy not in ("PRIVATE", "SHARED", "COLLECTIVE", "PUBLIC"):
            raise ReceiptError("VALUE_RECEIPT_INVALID: bad privacy_classification")
        key = (owner_id, receipt["provenance"]["source_table"],
               receipt["provenance"]["source_id"])
        if key in self.rows:
            return self.rows[key], False  # replay: existing row, unchanged
        prev = ""
        for (o, _, _), row in self.rows.items():
            if o == owner_id:
                prev = row["event_hash"]
        body = "|".join([owner_id, receipt["receipt_type"],
                         receipt["provenance"]["source_table"],
                         receipt["provenance"]["source_id"], prev,
                         receipt_canonical_hash(receipt)])
        event_hash = hashlib.sha256(body.encode()).hexdigest()
        row = {"owner_id": owner_id,
               "event_type": receipt["receipt_type"],
               "source_table": receipt["provenance"]["source_table"],
               "source_id": receipt["provenance"]["source_id"],
               "privacy_classification": privacy,
               "value": copy.deepcopy(receipt),
               "event_hash": event_hash,
               "previous_chain_hash": prev or None}
        self.rows[key] = row
        return row, True


def test_replay_returns_existing_row_unchanged():
    ledger = FakeSmartLedger()
    r = _contribution()
    row1, created1 = ledger.record_value_receipt(OWNER_A, r)
    # Tamper attempt via replay with different points: must NOT overwrite.
    tampered = copy.deepcopy(r)
    tampered["points_derivation"]["points_awarded"] = 999
    row2, created2 = ledger.record_value_receipt(OWNER_A, tampered)
    assert created1 is True and created2 is False
    assert row2["event_hash"] == row1["event_hash"]
    assert row2["value"]["points_derivation"]["points_awarded"] != 999


def test_cross_owner_write_rejected():
    ledger = FakeSmartLedger()
    r = _contribution()  # provenance.owner_id == OWNER_A
    with pytest.raises(ReceiptError) as exc:
        ledger.record_value_receipt(OWNER_B, r)
    assert "OWNER_MISMATCH" in str(exc.value)
    assert ledger.rows == {}


def test_same_source_different_owner_is_separate_chain():
    ledger = FakeSmartLedger()
    ra = _contribution()
    rb = _contribution()
    rb["provenance"]["owner_id"] = OWNER_B
    row_a, _ = ledger.record_value_receipt(OWNER_A, ra)
    row_b, _ = ledger.record_value_receipt(OWNER_B, rb)
    assert row_a["event_hash"] != row_b["event_hash"]
    assert row_a["owner_id"] != row_b["owner_id"]


def test_privacy_classification_preserved():
    ledger = FakeSmartLedger()
    r = _contribution()
    row, _ = ledger.record_value_receipt(OWNER_A, r, privacy="SHARED")
    assert row["privacy_classification"] == "SHARED"
    assert row["value"]["privacy_classification"] == "PRIVATE"  # receipt's own claim untouched
    with pytest.raises(ReceiptError):
        ledger.record_value_receipt(OWNER_A, _contribution(), privacy="SUPER_PUBLIC")


# --------------------------------------------------------------------------
# 6. Independent reconstruction: reread -> same calculation.
# --------------------------------------------------------------------------

def test_independent_reread_recomputes_same_contribution():
    stored = json.loads(json.dumps(_contribution()))  # DB round-trip
    result = recompute_contribution_from_receipt(stored)
    assert result["ok"] is True
    assert result["cvs_matches"] and result["points_match"]
    assert result["repeat_decay_matches"]
    assert result["receipt_hash"] == receipt_canonical_hash(stored)


def test_independent_reread_detects_tampering():
    stored = json.loads(json.dumps(_contribution()))
    stored["value_calculation"]["cvs"] = stored["value_calculation"]["cvs"] + 1.0
    result = recompute_contribution_from_receipt(stored)
    assert result["ok"] is False
    assert result["cvs_matches"] is False


def test_independent_decision_recompute_matches():
    r = _alignment_receipt()
    stored = json.loads(json.dumps(r))  # DB round-trip
    result = recompute_decision_from_receipt(stored, _decision_inputs(),
                                             _profile(), RiskPolicy())
    assert result["ok"] is True
    assert result["matches_decision"] and result["matches_selected"]


def test_receipt_hash_is_deterministic():
    a = receipt_canonical_hash(_contribution())
    b = receipt_canonical_hash(json.loads(json.dumps(_contribution())))
    assert a == b and len(a) == 64
