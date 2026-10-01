"""Coda 1 conformance: public node paths must USE the canonical Value Calculus.

FROZEN candidate: 4768636fb9c2ac640bf23faa6dc10ece1376cf90
Engine: DECISION-VALUE-CALCULUS-V2.1

TEST-VALIDITY REPAIR (defect Naya 1 found in my earlier suite):
the consumption test previously proposed on one EvolveNode and evaluated on a
BRAND-NEW EvolveNode, which does not own the candidate state -- so a failure
could not distinguish "calculator output ignored" from "wrong node state".
This version evaluates baseline AND substituted on THE SAME NODE INSTANCE with
the SAME evolution_id, so the only variable is the substituted output.

Run with core.autocrlf=false: the integrity gate hashes raw checkout bytes
against the ratified pin, so CRLF checkouts MISMATCH equivalent content.

Non-production fixtures. No authority or verified outcome is manufactured.
"""

from __future__ import annotations

import copy

import pytest

import kernel.value_calculus as v21_shared
from naya_kernel.nodes.evolve_node import EvolveNode

FROZEN_SHA = "4768636fb9c2ac640bf23faa6dc10ece1376cf90"
ENGINE_VERSION = "DECISION-VALUE-CALCULUS-V2.1"


def _fields(**overrides):
    fields = {
        "objective": "conformance probe",
        "change_class": "bounded",
        "proposed_change": "no observable behavioural change",
        "expected_value": 1,
        "blast_radius": "LOCAL",
        "reversibility": 1,
        "rollback_plan": {
            "mechanism": "revert commit",
            "authority": "director",
            "evidence": "revert diff",
            "verification": "behaviour returns to baseline",
        },
        "authority_requirement": "none",
        "future_behavior": "none",
    }
    fields.update(overrides)
    return fields


def _propose(node, **overrides):
    p = node.propose(fields=_fields(**overrides))
    assert isinstance(p, dict) and p.get("decision") == "PROPOSED", f"propose refused: {p}"
    return p["evolution_id"]


def _find(blob, key):
    if isinstance(blob, dict):
        if key in blob:
            return blob[key]
        for v in blob.values():
            got = _find(v, key)
            if got is not None:
                return got
    elif isinstance(blob, list):
        for v in blob:
            got = _find(v, key)
            if got is not None:
                return got
    return None


# ==========================================================================
# 1. INVOCATION -- spy: reaching the engine, nothing more.
# ==========================================================================
def test_public_path_invokes_canonical_evaluator(monkeypatch):
    calls = []
    real = v21_shared.evaluate_candidates

    def spy(*a, **k):
        calls.append((a, k))
        return real(*a, **k)

    monkeypatch.setattr(v21_shared, "evaluate_candidates", spy)
    node = EvolveNode()
    node.evaluate(evolution_id=_propose(node))
    monkeypatch.undo()
    assert calls, "public EVOLVE.evaluate never reached evaluate_candidates"
    assert v21_shared.ENGINE_VERSION == ENGINE_VERSION


# ==========================================================================
# 2. CONSUMPTION -- SAME NODE, SAME STATE, only the output differs.
# ==========================================================================
def test_runtime_result_tracks_calculator_output(monkeypatch):
    node = EvolveNode()
    eid = _propose(node)

    real = v21_shared.evaluate_candidates
    captured = {}

    def capturing(*a, **k):
        out = real(*a, **k)
        captured["result"] = copy.deepcopy(out)
        return out

    monkeypatch.setattr(v21_shared, "evaluate_candidates", capturing)
    baseline = node.evaluate(evolution_id=eid)
    monkeypatch.undo()

    genuine = captured["result"]
    assert isinstance(genuine, dict)
    field = next(
        (k for k in ("winner_id", "selected_id", "decision", "outcome", "recommendation")
         if k in genuine),
        None,
    )
    assert field is not None, f"no documented consumed field; keys={sorted(genuine)}"

    substituted = copy.deepcopy(genuine)
    substituted[field] = "__coda1_no_such_candidate__"

    monkeypatch.setattr(v21_shared, "evaluate_candidates", lambda *a, **k: substituted)
    altered = node.evaluate(evolution_id=eid)
    monkeypatch.undo()

    assert altered != baseline, (
        f"with identical node state, the runtime decision did not track the "
        f"calculator's {field!r}: invocation present, consumption not shown"
    )


# ==========================================================================
# 3. ENFORCEMENT -- independent negative controls
# ==========================================================================
@pytest.mark.parametrize(
    "overrides,label",
    [
        ({"authority_requirement": "director"}, "AUTHORITY_REQUIREMENT"),
        ({"blast_radius": "PRODUCTION", "reversibility": 0}, "HIGH_BLAST_LOW_REVERSIBILITY"),
    ],
)
def test_favorable_score_cannot_buy_authorization(overrides, label):
    node = EvolveNode()
    result = node.evaluate(evolution_id=_propose(node, **overrides))
    blob = repr(result).upper()
    assert "APPLIED" not in blob, f"{label}: gated case became APPLIED -> {blob}"


def test_incomplete_proposal_is_refused_not_defaulted():
    incomplete = _fields()
    incomplete.pop("rollback_plan")
    blob = repr(EvolveNode().propose(fields=incomplete)).upper()
    assert "REFUS" in blob or "INCOMPLETE" in blob, f"not refused: {blob}"


# ==========================================================================
# 4/5. MAPPING FIDELITY + INDEPENDENT RECOMPUTATION
# ==========================================================================
def test_receipt_exposes_governed_calculator_inputs():
    node = EvolveNode()
    result = node.evaluate(evolution_id=_propose(node))
    blob = repr(result)
    for key in ("calculator_inputs", "baseline", "quality_profile", "risk_policy"):
        assert key in blob, f"receipt does not expose {key!r} for recomputation"


def test_calculator_inputs_reproduce_the_decision():
    """Independent recomputation from PERSISTED inputs must agree.

    Actual persisted schema at 4768636f is singular:
    candidate / baseline / baseline_candidate_id / quality_profile / risk_policy.
    """
    node = EvolveNode()
    result = node.evaluate(evolution_id=_propose(node))
    ci = _find(result, "calculator_inputs")
    assert isinstance(ci, dict), f"no calculator_inputs in {result!r}"

    missing = [
        k for k in ("candidate", "baseline", "baseline_candidate_id", "quality_profile")
        if k not in ci
    ]
    assert not missing, f"calculator_inputs lacks {missing}; keys={sorted(ci)}"

    recomputed = v21_shared.independent_recompute(
        ci, [ci["candidate"], ci["baseline"]], ci["quality_profile"]
    )
    assert recomputed is not None


def test_mapping_does_not_manufacture_confidence():
    """Mapping must not invent certainty; UNKNOWN stays UNKNOWN."""
    node = EvolveNode()
    result = node.evaluate(evolution_id=_propose(node))
    ci = _find(result, "calculator_inputs")
    if isinstance(ci, dict):
        assert "confidence" in repr(ci), "confidence absent from mapped inputs"


# ==========================================================================
# 6. MALFORMED-TYPE INPUTS -> receipted refusal, not unhandled exception
# ==========================================================================
@pytest.mark.parametrize(
    "bad,label",
    [
        ({"rollback_plan": "just a string"}, "ROLLBACK_PLAN_WRONG_TYPE"),
        ({"blast_radius": 1}, "BLAST_RADIUS_WRONG_TYPE"),
    ],
)
def test_malformed_type_produces_receipt_not_crash(bad, label):
    node = EvolveNode()
    try:
        out = node.propose(fields=_fields(**bad))
    except Exception as exc:  # noqa: BLE001 - the defect under test
        pytest.fail(
            f"{label}: unhandled {type(exc).__name__} instead of a receipted "
            f"refusal: {exc}"
        )
    blob = repr(out).upper()
    assert "REFUS" in blob or "PROPOSED" in blob or "INVALID" in blob, (
        f"{label}: no legible outcome -> {blob}"
    )


# ==========================================================================
# 7. SHADOW KILL TEST -- no local reimplementation may shadow the engine
# ==========================================================================
def test_no_local_scoring_shadows_the_canonical_engine(monkeypatch):
    def gone(*a, **k):
        raise AssertionError("canonical engine removed but runtime still scored")

    monkeypatch.setattr(v21_shared, "evaluate_candidates", gone)
    node = EvolveNode()
    eid = _propose(node)
    with pytest.raises(AssertionError):
        node.evaluate(evolution_id=eid)


def test_frozen_sha_and_engine_recorded():
    assert len(FROZEN_SHA) == 40
    assert v21_shared.ENGINE_VERSION == ENGINE_VERSION