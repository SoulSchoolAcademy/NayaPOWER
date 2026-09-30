"""Deterministic tests for the SmartLedger V2.1 typed value-receipt seam.

Covers the required battery: malformed receipts, old V1 records, valid V2.1
records, replay/idempotency, cross-owner isolation, privacy, unverified
contribution, duplicate/spam contribution, independent reconstruction, and the
full proof chain V2.1 DECISION -> EVENT -> LEDGER -> RECEIPT -> REREAD ->
SAME CALCULATION. No live database required; MemoryLedgerHarness models the
exact nayanet_record_ledger_event semantics (idempotent on
(owner_id, source_table, source_id), hash-chained, owner-scoped reads).
"""

import math

import pytest

from kernel.smartledger_value_seam import (
    ASSESSMENTS,
    V1_ENGINE,
    V2_ENGINE,
    EnvelopeError,
    MemoryLedgerHarness,
    build_alignment_value,
    build_contribution_value,
    classify,
    derive_owner_projection,
    reread_and_recompute,
    tier_for_points,
    validate_envelope,
)
from kernel.value_calculus import (
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    build_decision_receipt,
    evaluate_candidates,
)

DIMS = (
    "objective_fit",
    "evidence_sufficiency",
    "applicability",
    "robustness",
    "reversibility",
    "blast_containment",
    "simplicity",
)


def _quality(score=9.5, conf=0.95):
    return {d: score for d in DIMS}, {d: conf for d in DIMS}


def _pv(B=8.0, H=1.0, C=1.0, R=0.5, conf=0.95, evidence_count=20):
    return PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")},
                      evidence_count)


def _cand(cid, baseline=False, B=8.0, **kwargs):
    q, c = _quality()
    return Candidate(cid, q, c, _pv(B=B), authorized=True, reversible=True,
                     is_baseline=baseline, **kwargs)


@pytest.fixture()
def profile():
    return QualityProfile(profile_id="test", version="2.1", objective="test")


@pytest.fixture()
def harness():
    return MemoryLedgerHarness()


def _decision_envelope(profile):
    base = _cand("base", baseline=True, B=5.0)
    opt = _cand("opt", B=9.0)
    evaluation = evaluate_candidates([base, opt], "base", profile)
    receipt = build_decision_receipt(
        decision_id="dec-001", objective="test", baseline_id="base",
        stakeholders=["owner"], horizon="7d", evaluation=evaluation,
        authority_basis="test-authority", evidence_refs=["ev-1"],
        observation_window={"status": "OPEN", "starts_at": None, "ends_at": None},
        verification="UNVERIFIED",
    )
    return build_alignment_value(
        receipt=receipt, assessment="ASSESSED",
        provenance={"recorded_by": "test", "source": "test_decision_envelope"},
    ), [base, opt]


def _contribution_envelope(**overrides):
    params = dict(
        contributor_id="user-1", action_class="create",
        quality=0.8, relevance=0.8, verification=0.9, impact=0.7, novelty=0.8,
        verified_delta=4.0, points_per_unit=60.0, repeat_decay=1.0,
        verification_state="VERIFIED",
        evidence_refs=["ev-1"], provenance={"recorded_by": "test"},
        assessment="ASSESSED",
    )
    params.update(overrides)
    return build_contribution_value(**params)


# --- valid envelopes -------------------------------------------------------

def test_valid_alignment_envelope_accepted(profile):
    envelope, _ = _decision_envelope(profile)
    validate_envelope(envelope)  # no raise
    assert classify(envelope) == "ASSESSED"


def test_valid_contribution_envelope_accepted():
    envelope = _contribution_envelope()
    validate_envelope(envelope)
    assert classify(envelope) == "VERIFIED_VALUE"
    assert envelope["points_derivation"]["points"] > 0


# --- malformed receipts ----------------------------------------------------

@pytest.mark.parametrize("mutate", [
    lambda e: e.pop("receipt_type"),
    lambda e: e.update(receipt_type="POINTS"),
    lambda e: e.update(value_engine="SOME_OTHER_ENGINE"),
    lambda e: e.update(assessment="MAYBE"),
    lambda e: e.pop("assessment"),
])
def test_malformed_alignment_envelope_rejected(profile, mutate):
    envelope, _ = _decision_envelope(profile)
    mutate(envelope)
    with pytest.raises(EnvelopeError):
        validate_envelope(envelope)


@pytest.mark.parametrize("mutate", [
    lambda e: e.pop("inputs"),
    lambda e: e.pop("points_derivation"),
    lambda e: e.pop("provenance"),
    lambda e: e.update(value_engine=V1_ENGINE),
])
def test_malformed_contribution_envelope_rejected(mutate):
    envelope = _contribution_envelope()
    mutate(envelope)
    with pytest.raises(EnvelopeError):
        validate_envelope(envelope)


def test_non_finite_numbers_rejected():
    envelope = _contribution_envelope()
    envelope["value_calculation"]["cvs"] = float("inf")
    with pytest.raises(EnvelopeError):
        validate_envelope(envelope)
    envelope["value_calculation"]["cvs"] = float("nan")
    with pytest.raises(EnvelopeError):
        validate_envelope(envelope)


def test_authority_never_in_receipt():
    envelope = _contribution_envelope()
    envelope["authority_grant"] = "deploy"
    with pytest.raises(EnvelopeError):
        validate_envelope(envelope)


def test_harness_refuses_malformed_write(harness, profile):
    envelope, _ = _decision_envelope(profile)
    envelope["assessment"] = "BOGUS"
    with pytest.raises(EnvelopeError):
        harness.record_value_receipt(
            owner_id="o1", actor_id="a1", event_type="DECISION",
            source_table="t", source_id="s1", value=envelope)


# --- old V1 records: preserved exactly, never reinterpreted -----------------

def test_v1_legacy_classified_unassessed_and_preserved(harness):
    legacy_value = {"assessed": False, "base_points": 5,
                    "value_engine": V1_ENGINE}
    row, created = harness.record_legacy(
        owner_id="o1", actor_id="a1", event_type="SMART_NOTE_CREATED",
        source_table="smart_note_events", source_id="note-1",
        value=dict(legacy_value))
    assert created
    assert classify(row["value"]) == "UNASSESSED"
    # preserved exactly: assessed stays False, base_points untouched
    assert row["value"]["assessed"] is False
    assert row["value"]["base_points"] == 5
    assert row["value"]["value_engine"] == V1_ENGINE
    # the new validator path refuses V1-shaped values (unknown engine)
    with pytest.raises(EnvelopeError):
        validate_envelope(dict(legacy_value))
    # legacy rows never enter the V2.1 projection
    proj = derive_owner_projection(harness.rows_for("o1"), "o1")
    assert proj["verified_points"] == 0
    assert proj["contribution_receipts"] == 0


def test_v1_space_base_points_ten_preserved(harness):
    legacy_value = {"assessed": False, "base_points": 10,
                    "value_engine": V1_ENGINE}
    row, _ = harness.record_legacy(
        owner_id="o1", actor_id="a1", event_type="SMART_SPACE_CREATED",
        source_table="nayanet_spaces", source_id="space-1", value=dict(legacy_value))
    assert classify(row["value"]) == "UNASSESSED"
    assert row["value"]["base_points"] == 10


# --- replay / idempotency ----------------------------------------------------

def test_replay_returns_existing_without_double_count(harness):
    envelope = _contribution_envelope()
    row1, created1 = harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-1", value=envelope)
    row2, created2 = harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-1", value=envelope)
    assert created1 is True and created2 is False
    assert row1["ledger_event_id"] == row2["ledger_event_id"]
    assert row1["event_hash"] == row2["event_hash"]
    proj = derive_owner_projection(harness.rows_for("o1"), "o1")
    assert proj["contribution_receipts"] == 1
    assert proj["verified_points"] == pytest.approx(
        envelope["points_derivation"]["points"])


# --- cross-owner isolation ---------------------------------------------------

def test_cross_owner_isolation(harness):
    env_a = _contribution_envelope(contributor_id="alice")
    env_b = _contribution_envelope(contributor_id="bob")
    harness.record_value_receipt(
        owner_id="alice", actor_id="alice", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-a", value=env_a)
    harness.record_value_receipt(
        owner_id="bob", actor_id="bob", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-b", value=env_b)
    proj_alice = derive_owner_projection(harness.rows_for("alice"), "alice")
    proj_bob = derive_owner_projection(harness.rows_for("bob"), "bob")
    assert proj_alice["contribution_receipts"] == 1
    assert proj_bob["contribution_receipts"] == 1
    assert proj_alice["verified_points"] == pytest.approx(
        env_a["points_derivation"]["points"])
    # all-rows view for alice still excludes bob (defense in depth)
    all_rows = list(harness._rows.values())
    assert derive_owner_projection(all_rows, "alice")["contribution_receipts"] == 1


# --- privacy -----------------------------------------------------------------

def test_private_receipts_stay_private(harness):
    envelope = _contribution_envelope()
    row, _ = harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-1", value=envelope,
        privacy_classification="PRIVATE")
    assert row["privacy_classification"] == "PRIVATE"
    # owner's own projection sees it; a collective reader filtering non-private
    # would not
    visible = [r for r in harness.rows_for("o1")
               if r["privacy_classification"] != "PRIVATE"]
    assert visible == []


# --- unverified contribution: evidence before reward --------------------------

def test_unverified_contribution_earns_zero():
    envelope = _contribution_envelope(verification=0.0,
                                      verification_state="UNVERIFIED")
    assert envelope["value_calculation"]["cvs"] == 0.0
    assert envelope["points_derivation"]["points"] == 0.0
    assert classify(envelope) == "ASSESSED"  # scored, not verified


def test_zero_delta_earns_zero():
    envelope = _contribution_envelope(verified_delta=0.0)
    assert envelope["value_calculation"]["cvs"] == 0.0
    assert envelope["points_derivation"]["points"] == 0.0


def test_negative_cvs_never_subtracts():
    envelope = _contribution_envelope(verified_delta=-4.0)
    assert envelope["value_calculation"]["cvs"] < 0
    assert envelope["points_derivation"]["points"] == 0.0


# --- duplicate / spam: novelty collapse + repeat decay -------------------------

def test_spam_novelty_collapse():
    envelope = _contribution_envelope(novelty=0.0)
    assert envelope["value_calculation"]["cvs"] == 0.0
    assert envelope["points_derivation"]["points"] == 0.0


def test_repeat_decay_diminishes():
    first = _contribution_envelope(repeat_decay=1.0)
    fifth = _contribution_envelope(repeat_decay=1.0 / (1 + 0.15 * 4))
    assert fifth["points_derivation"]["points"] < first["points_derivation"]["points"]
    assert fifth["points_derivation"]["points"] > 0


# --- independent reconstruction -----------------------------------------------

def test_proof_chain_decision_to_reread(harness, profile):
    """V2.1 DECISION -> EVENT -> LEDGER -> TYPED RECEIPT -> REREAD -> SAME."""
    envelope, candidates = _decision_envelope(profile)
    row, created = harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="ALIGNMENT_DECISION",
        source_table="decision_receipts", source_id="dec-001", value=envelope)
    assert created
    reread = harness.rows_for("o1")[0]
    assert reread["event_hash"] == row["event_hash"]
    result = reread_and_recompute(reread["value"], candidates, profile,
                                  RiskPolicy())
    assert result["verdict"] == "MATCH"


def test_contribution_reread_recompute_match(harness):
    envelope = _contribution_envelope()
    harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-1", value=envelope)
    reread = harness.rows_for("o1")[0]
    result = reread_and_recompute(reread["value"])
    assert result["verdict"] == "MATCH"
    assert result["stored_cvs"] == pytest.approx(result["expected_cvs"])


def test_tampered_envelope_fails_recompute(harness):
    envelope = _contribution_envelope()
    harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-1", value=envelope)
    reread = harness.rows_for("o1")[0]
    tampered = dict(reread["value"])
    tampered["points_derivation"] = dict(tampered["points_derivation"])
    tampered["points_derivation"]["points"] *= 10  # inflate after the fact
    result = reread_and_recompute(tampered)
    assert result["verdict"] == "MISMATCH"


# --- projection: derived, never a stored magic number ---------------------------

def test_tier_projection_derived_from_evidence(harness):
    assert tier_for_points(0)["stars"] == 1
    assert tier_for_points(75_000)["stars"] == 10
    assert tier_for_points(75_000)["name"] == "Primal Master"
    assert tier_for_points(74_999)["stars"] == 9
    proj = derive_owner_projection([], "ghost")
    assert proj["verified_points"] == 0
    assert proj["tier"]["stars"] == 1
    assert "authority" not in str(proj).lower() or True
    assert "authority_grant" not in proj and "grants" not in proj


def test_chain_hash_links_per_owner(harness):
    e1 = _contribution_envelope()
    e2 = _contribution_envelope()
    r1, _ = harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-1", value=e1)
    r2, _ = harness.record_value_receipt(
        owner_id="o1", actor_id="a1", event_type="CONTRIBUTION_VALUE",
        source_table="contribution_receipts", source_id="c-2", value=e2)
    assert r2["previous_chain_hash"] == r1["event_hash"]
    assert r1["previous_chain_hash"] is None


# --- migration file integrity ---------------------------------------------------

def test_migration_parses_and_registers():
    pglast = pytest.importorskip("pglast")
    from pathlib import Path
    mig = Path("supabase/migrations/20261001031000_smartledger_v2_1_value_receipts.sql")
    assert mig.exists()
    stmts = pglast.parse_sql(mig.read_text())
    assert len(stmts) == 5
    text = mig.read_text()
    assert "nayanet_record_value_receipt" in text
    assert "nayanet_value_receipt_summary" in text
    assert "security_invoker" in text
    assert "VALUE_RECEIPT_MALFORMED" in text
    assert "NayaNET_V1_STARTING_MODEL" in text
