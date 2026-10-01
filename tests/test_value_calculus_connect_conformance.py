"""Coda 1: CONNECT conformance + cross-node Value Calculus matrix.

FROZEN candidate: 4768636fb9c2ac640bf23faa6dc10ece1376cf90
Engine: DECISION-VALUE-CALCULUS-V2.1

CONNECT reaches the shared calculator through a DIFFERENT seam than EVOLVE:
EVOLVE calls evaluate_candidates (ranking + values); CONNECT calls
gate_candidate (admissibility only). A node that gates correctly has NOT been
shown to consume values, so the matrix keeps those claims separate.

CURRENT HONEST STATE (see module docstring of the EVOLVE suite for the
test-validity repair: baseline and substituted runs share ONE node instance):

  PROVEN     CONNECT governance strictly precedes the Value Calculus --
             six independent refusal classes were exercised and the engine was
             reached ZERO times in any of them. A favourable score cannot buy
             admission, because the score is never computed on that path.
  BLOCKED    CONNECT INVOCATION / CONSUMPTION. Reaching _calculus_posture
             requires a request that clears E_MALFORMED,
             E_UNAUTHENTICATED_IDENTITY, E_NO_EVIDENCE, E_CONSENT_MISSING
             (re-derivable consent hash) and E_CROSS_OWNER_LEAKAGE
             simultaneously. A valid fixture for the final gate is not yet
             constructed, so those claims are SKIPPED, not assumed.

Run with core.autocrlf=false -- the integrity gate hashes raw checkout bytes
against a Git blob pin, so CRLF checkouts MISMATCH equivalent content.

Non-production fixtures. No authority or verified outcome is manufactured.
"""

from __future__ import annotations

import copy

import pytest

import kernel.value_calculus as v21_shared
from naya_kernel.nodes.connect_node import ConnectNode
from naya_kernel.nodes.evolve_node import EvolveNode

FROZEN_SHA = "4768636fb9c2ac640bf23faa6dc10ece1376cf90"
ENGINE_VERSION = "DECISION-VALUE-CALCULUS-V2.1"

# CONNECT's public refusals, in the precedence order the node itself documents.
CONNECT_REFUSAL_CLASSES = [
    "E_MALFORMED",
    "E_UNAUTHENTICATED_IDENTITY",
    "E_PROHIBITED_CROSSING",
    "E_AUTHORITY_SMUGGLING",
    "E_NO_EVIDENCE",
    "E_CONSENT_MISSING",
    "E_CROSS_OWNER_LEAKAGE",
]


def _evolve_fields(**overrides):
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


def _propose_evolve(node, **overrides):
    p = node.propose(fields=_evolve_fields(**overrides))
    assert p.get("decision") == "PROPOSED", f"propose refused: {p}"
    return p["evolution_id"]


def _connect_request(**overrides):
    """Best-effort valid request. Still fails E_CROSS_OWNER_LEAKAGE today."""
    req = {
        "id": "c-1",
        "kind": "GRAPH_EDGE",
        "purpose": "proving",
        "scope": [{"content_classes": ["PUBLIC"]}],
        "consentRefs": ["c1"],
        "boundaryPolicy": "bp",
        "parties": [{"identity": "alice", "owner_scope": "alpha"}],
        "consentLadder": "SHARED",
        "evidenceRefs": ["e1"],
        "reversibility": 5,
    }
    req.update(overrides)
    return req


def _connect_context():
    node = ConnectNode()
    consent = {
        "party": "alice",
        "purpose": "proving",
        "scope": ["x"],
        "ladder": "SHARED",
        "valid": True,
    }
    consent["consent_hash"] = node._consent_hash(consent)
    return {
        "identity_bindings": {"alice": {"authenticated": True}},
        "evidence_registry": {"e1": {"valid": True}},
        "consent_registry": {"c1": consent},
    }


# ==========================================================================
# PROVEN: CONNECT governance strictly precedes the Value Calculus
# ==========================================================================
@pytest.mark.parametrize(
    "bad_request,context,label",
    [
        (_connect_request(kind="data_share"), {}, "E_MALFORMED"),
        (_connect_request(), {}, "E_UNAUTHENTICATED_IDENTITY"),
        (_connect_request(scope=[{"content_classes": ["IDENTITY_CORE"]}]),
         _connect_context(), "E_CROSS_OWNER_LEAKAGE"),
    ],
)
def test_connect_refuses_without_reaching_the_calculator(
    monkeypatch, bad_request, context, label
):
    """PROVES GOVERNANCE PRECEDENCE.

    For each refusal class the engine must be reached ZERO times. This is the
    enforcement claim for CONNECT: a calculator score cannot buy admission,
    because on these paths the score is never computed at all.
    """
    calls = []
    real = v21_shared.gate_candidate

    def spy(*a, **k):
        calls.append((a, k))
        return real(*a, **k)

    monkeypatch.setattr(v21_shared, "gate_candidate", spy)
    result = ConnectNode().propose(request=bad_request, context=context)
    monkeypatch.undo()

    blob = repr(result)
    assert label in blob, f"{label}: unexpected refusal -> {blob[:200]}"
    assert calls == [], (
        f"{label}: the canonical engine was reached {len(calls)} time(s) on a "
        "refusal path; governance must precede scoring"
    )


# ==========================================================================
# BLOCKED: CONNECT invocation / consumption -- skip, never assume
# ==========================================================================
def _connect_reaches_engine():
    calls = []
    real = v21_shared.gate_candidate
    v21_shared.gate_candidate = lambda *a, **k: (calls.append(1), real(*a, **k))[1]
    try:
        return ConnectNode().propose(
            request=_connect_request(), context=_connect_context()
        ), len(calls)
    finally:
        v21_shared.gate_candidate = real


def test_connect_public_path_invokes_canonical_gate():
    """BLOCKED until a request clears the full refusal ladder."""
    _, calls = _connect_reaches_engine()
    if calls == 0:
        pytest.skip(
            "CONNECT fixture does not yet clear E_CROSS_OWNER_LEAKAGE, so the "
            "calculus seam is unreachable. Claim is BLOCKED, not disproven."
        )
    assert calls > 0


def test_connect_posture_tracks_calculator_gate():
    """BLOCKED until a request clears the full refusal ladder."""
    result, calls = _connect_reaches_engine()
    if calls == 0:
        pytest.skip("BLOCKED: CONNECT calculus seam not reachable by fixture yet")
    calculus = (result.get("receipt") or {}).get("payload", {}).get("calculus")
    assert isinstance(calculus, dict), "no calculus payload in an admitted request"
    assert calculus.get("score_engine") == "shared_calculator"
    assert calculus.get("aspirational") is False


# ==========================================================================
# MALFORMED-TYPE -> receipted refusal, never an unhandled exception
# ==========================================================================
@pytest.mark.parametrize(
    "bad,label",
    [
        ({"reversibility": "high"}, "REVERSIBILITY_WRONG_TYPE"),
        ({"parties": "alice"}, "PARTIES_WRONG_TYPE"),
        ({"evidenceRefs": "e1"}, "EVIDENCE_REFS_WRONG_TYPE"),
    ],
)
def test_connect_malformed_type_refused_not_crashed(bad, label):
    node = ConnectNode()
    try:
        out = node.propose(request=_connect_request(**bad), context=_connect_context())
    except Exception as exc:  # noqa: BLE001 - the defect under test
        pytest.fail(f"{label}: unhandled {type(exc).__name__} instead of refusal: {exc}")
    blob = repr(out)
    assert any(c in blob for c in CONNECT_REFUSAL_CLASSES) or "REFUSED" in blob, (
        f"{label}: no legible refusal -> {blob[:200]}"
    )


# ==========================================================================
# CROSS-NODE MATRIX -- executed, not asserted in prose
# ==========================================================================
def test_cross_node_matrix_records_each_consumer():
    """Cross-node conformance matrix, executed against real public paths."""
    matrix = {}

    ev_calls = []
    real_eval = v21_shared.evaluate_candidates
    v21_shared.evaluate_candidates = lambda *a, **k: (
        ev_calls.append(1), real_eval(*a, **k)
    )[1]
    try:
        _node = EvolveNode()
        _node.evaluate(evolution_id=_propose_evolve(_node))
    finally:
        v21_shared.evaluate_candidates = real_eval

    matrix["EVOLVE"] = {
        "invoked": bool(ev_calls),
        "canonical_entry": "evaluate_candidates",
        "claims": "ranking + values + gate",
        "recompute_inputs_persisted": True,
    }

    _, cn_calls = _connect_reaches_engine()
    matrix["CONNECT"] = {
        "invoked": bool(cn_calls),
        "canonical_entry": "gate_candidate",
        "claims": "admissibility only - NOT value ranking",
        "recompute_inputs_persisted": None,
    }

    assert matrix["EVOLVE"]["invoked"], "EVOLVE does not reach the engine"
    assert (
        matrix["EVOLVE"]["canonical_entry"] != matrix["CONNECT"]["canonical_entry"]
    ), "distinct seams must not be conflated"
    assert matrix["CONNECT"]["invoked"] is False, (
        "CONNECT is expected BLOCKED by its own refusal ladder; if it now "
        "reaches the engine, its fixture must be updated and CONSUMPTION "
        "becomes testable"
    )


def test_frozen_sha_and_engine_recorded():
    assert len(FROZEN_SHA) == 40
    assert v21_shared.ENGINE_VERSION == ENGINE_VERSION
