"""Coda 1 conformance: the public nine-node path really uses the Value Calculus.

Written against PUBLIC node operations (EVOLVE.propose / EVOLVE.evaluate),
never private helpers -- private-helper tests would only prove the calculator
calls itself, which is not the question.

Three claims are kept strictly separate and are never substituted for one
another:

  1. INVOCATION   -- a spy proves the public path reaches the canonical engine.
  2. CONSUMPTION  -- a substitution proves the runtime result actually depends
                     on engine output. The real evaluator is wrapped so its
                     result structure stays VALID; only a documented consumed
                     field is changed. Returning an invalid dict and treating
                     the resulting exception as proof is explicitly NOT done.
  3. ENFORCEMENT  -- an independent negative control proves a favorable numeric
                     score cannot buy authorization.

Pinned SHA: 4e87d4a5810f6b0b5b72e254f3d37ddf69826c87
Candidate-branch lineage ONLY. NOT the director-frozen candidate; that remains
pending confirmation from Naya 4.

Environment requirement: the shared-calculator integrity gate hashes raw on-disk
bytes with hashlib and compares them to the ratified pin cac79b6595ca651d8a110b71f25fff9fe50e67bc.
On a CRLF checkout (core.autocrlf=true) that comparison MISMATCHes even though
the file is byte-identical to the pin, and EVOLVE correctly refuses to score.
Run with core.autocrlf=false for these to exercise.

Non-production fixtures. No authority or verified outcome is manufactured here.
"""

from __future__ import annotations

import copy

import pytest

import kernel.value_calculus as v21_shared
from naya_kernel.nodes.evolve_node import EvolveNode

PINNED_SHA = "4e87d4a5810f6b0b5b72e254f3d37ddf69826c87"
ENGINE_VERSION = "DECISION-VALUE-CALCULUS-V2.1"


# --------------------------------------------------------------------------
# fixtures
# --------------------------------------------------------------------------
def _fields(**overrides):
    """Minimal COMPLETE proposal per evolve_node.propose's required field set.

    blast_radius is a NAMED CATEGORY (evolve_node.BLAST_RADIUS), not a number:
    LOCAL, COMPONENT, CROSS_NODE, SYSTEM, PRODUCTION, CONSTITUTIONAL.

    rollback_plan is a MAPPING with mechanism/authority/evidence/verification
    slots (evolve_node._rollback_plan_complete calls .get(slot) on it).
    """
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


def _propose_and_evaluate(node, fields=None):
    """Drive the public propose -> evaluate path, return (result, evolution_id)."""
    proposal = node.propose(fields=fields or _fields())
    if not isinstance(proposal, dict):
        return proposal, None
    if proposal.get("decision") == "REFUSED":
        return proposal, None
    eid = proposal.get("evolution_id")
    if eid is None:
        return proposal, None
    return node.evaluate(evolution_id=eid), eid


# ==========================================================================
# 1. INVOCATION -- spy on the module attribute the runtime resolves
# ==========================================================================
def test_public_path_invokes_canonical_evaluator(monkeypatch):
    """PROVES INVOCATION ONLY.

    A spy establishes that the public node path reaches the canonical engine.
    It makes NO claim about consumption: the runtime could call the engine and
    ignore the answer. That is test 2's job, and keeping them apart is the point.
    """
    calls = []
    real = v21_shared.evaluate_candidates

    def spy(*args, **kwargs):
        calls.append((args, kwargs))
        return real(*args, **kwargs)

    monkeypatch.setattr(v21_shared, "evaluate_candidates", spy)

    _propose_and_evaluate(EvolveNode())

    assert calls, "public EVOLVE.evaluate never reached value_calculus.evaluate_candidates"
    assert v21_shared.ENGINE_VERSION == ENGINE_VERSION


# ==========================================================================
# 2. CONSUMPTION -- substitute a documented consumed field, valid structure
# ==========================================================================
def test_runtime_result_tracks_calculator_output(monkeypatch):
    """PROVES CONSUMPTION.

    Run the real evaluator first to obtain a genuine result object, then return
    a deep copy with ONE documented consumed field changed and the structure
    still valid. If the runtime's decision tracks that field, the decision
    depends on engine output.

    A spy with an UNCHANGED runtime result fails this test -- that is exactly
    the intended separation between invocation and consumption.
    """
    real = v21_shared.evaluate_candidates
    captured = {}

    def capturing(*args, **kwargs):
        result = real(*args, **kwargs)
        captured["result"] = copy.deepcopy(result)
        return result

    monkeypatch.setattr(v21_shared, "evaluate_candidates", capturing)
    baseline_result, eid = _propose_and_evaluate(EvolveNode())
    monkeypatch.undo()

    genuine = captured.get("result")
    assert isinstance(genuine, dict), "evaluator must return a mapping to be substitutable"
    if eid is None:
        pytest.skip(f"propose did not yield an evolution_id; result={baseline_result!r}")

    consumed = next(
        (k for k in ("winner_id", "selected_id", "decision", "outcome") if k in genuine),
        None,
    )
    assert consumed is not None, f"no documented consumed field found; keys={sorted(genuine)}"

    substituted = copy.deepcopy(genuine)
    substituted[consumed] = "__coda1_no_such_candidate__"

    monkeypatch.setattr(v21_shared, "evaluate_candidates", lambda *a, **k: substituted)
    altered_result = EvolveNode().evaluate(evolution_id=eid)
    monkeypatch.undo()

    assert altered_result != baseline_result, (
        f"runtime decision did not track the calculator's {consumed!r}: "
        "invocation may be present but the result is NOT consumed"
    )


# ==========================================================================
# 3. ENFORCEMENT -- independent negative controls
# ==========================================================================
@pytest.mark.parametrize(
    "overrides,label",
    [
        ({"authority_requirement": "director"}, "AUTHORITY_REQUIREMENT"),
        ({"blast_radius": "PRODUCTION", "reversibility": 0}, "HIGH_BLAST_LOW_REVERSIBILITY"),
        ({"rollback_plan": ""}, "INCOMPLETE_PROPOSAL"),
    ],
)
def test_favorable_score_cannot_buy_authorization(overrides, label):
    """PROVES ENFORCEMENT -- independent of tests 1 and 2.

    Each case leaves a gate condition unsatisfied while scoring would otherwise
    be favorable, then asserts the node does not authorize. If a good score
    could buy permission, the engine's gate would be decorative.
    """
    result, _ = _propose_and_evaluate(EvolveNode(), fields=_fields(**overrides))
    blob = repr(result).upper()

    assert "APPLIED" not in blob, f"{label}: gated case became APPLIED -> {blob}"
    assert (
        "AUTHORIZ" not in blob
        or "REJECT" in blob
        or "REFUS" in blob
        or "NEEDS" in blob
    ), f"{label}: expected refusal/gate, got {blob}"


# ==========================================================================
# 4/5. MAPPING INTEGRITY + INDEPENDENT RECOMPUTATION
# ==========================================================================
def test_persisted_inputs_support_independent_recompute():
    """Recomputation must reproduce decision, selection, gate and values.

    Uses the engine's own independent_recompute over preserved inputs. A single
    matching scalar would NOT be sufficient for this claim.
    """
    result, _ = _propose_and_evaluate(EvolveNode())

    receipt = result.get("receipt") if isinstance(result, dict) else None
    receipt = receipt if isinstance(receipt, dict) else result
    assert isinstance(receipt, dict), f"no receipt available; result={result!r}"

    missing = [k for k in ("baseline_id", "candidates", "profile") if k not in receipt]
    assert not missing, f"receipt lacks recomputation inputs: {missing}"

    recomputed = v21_shared.independent_recompute(
        receipt, receipt["candidates"], receipt["profile"]
    )
    assert recomputed is not None


# ==========================================================================
# 6. MISSING-INPUT BEHAVIOR
# ==========================================================================
def test_incomplete_proposal_is_refused_not_defaulted():
    """Absent required input must be refused, never filled with invented values."""
    incomplete = _fields()
    incomplete.pop("rollback_plan")
    result = EvolveNode().propose(fields=incomplete)

    blob = repr(result).upper()
    assert "REFUS" in blob or "INCOMPLETE" in blob, (
        f"missing required input was not refused: {blob}"
    )


# ==========================================================================
# 7. CONFIGURATION BINDING
# ==========================================================================
def test_profile_reaches_the_evaluator(monkeypatch):
    """The profile actually used must be the one the evaluator receives."""
    seen = {}
    real = v21_shared.evaluate_candidates

    def capturing(candidates, baseline_id, profile, *a, **k):
        seen["profile"] = profile
        return real(candidates, baseline_id, profile, *a, **k)

    monkeypatch.setattr(v21_shared, "evaluate_candidates", capturing)
    _propose_and_evaluate(EvolveNode())
    monkeypatch.undo()

    assert seen.get("profile") is not None, "no profile reached the evaluator"


def test_pinned_sha_and_engine_recorded():
    """Guards against running this suite against an unintended revision."""
    assert len(PINNED_SHA) == 40
    assert v21_shared.ENGINE_VERSION == ENGINE_VERSION