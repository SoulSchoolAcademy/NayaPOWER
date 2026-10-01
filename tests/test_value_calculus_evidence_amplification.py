"""Coda 1: does duplicate evidence inflate quality in connect-v21map-v1?

FROZEN candidate: 4768636fb9c2ac640bf23faa6dc10ece1376cf90

connect-v21map-v1 derives:
    evidence_sufficiency = min(10.0, len(evidence_refs) * 2.0)

Quality therefore comes from REFERENCE COUNT, and the mapping never checks
whether those references are distinct. Measured at the frozen SHA:

    none         suff= 0.0  gate=NEEDS_EVIDENCE  Q=0.500
    one          suff= 2.0  gate=NEEDS_EVIDENCE  Q=0.900
    dup x3       suff= 6.0  gate=NEEDS_EVIDENCE  Q=1.700
    dup x5       suff=10.0  gate=NEEDS_EVIDENCE  Q=2.500
    distinct x5  suff=10.0  gate=NEEDS_EVIDENCE  Q=2.500

Two distinct things are true and must not be conflated:

  1. AMPLIFICATION IS REAL IN THE SCORE. Repeating ONE weak reference five
     times nearly triples Q (0.900 -> 2.500) and is byte-for-byte
     indistinguishable from five independent references. The engine cannot
     tell correlated evidence from corroborating evidence.

  2. AMPLIFICATION DID NOT FLIP THE GATE HERE. Every case stayed
     NEEDS_EVIDENCE, because evidence_sufficiency floors the gate rather than
     the aggregate Q lifting it. So this is NOT a proven authorization bypass.

The honest severity is therefore: a real correlation-blindness defect in a
reported quality metric, with the authorization consequence UNPROVEN at this
SHA. Anyone citing this as an authority bypass would be overclaiming; anyone
dismissing it as harmless would be ignoring that Q is reported as
`quality_Q` in the shared-calculus posture receipt.

Private-helper level: `_to_v21_candidate` + the canonical `gate_candidate`.
This SUPPLEMENTS the public-path suite; it does not replace it. Reaching the
same seam through public CONNECT.propose remains BLOCKED on a valid
cross-owner fixture.

Run with core.autocrlf=false. Non-production fixtures.
"""

from __future__ import annotations

import pytest

import kernel.value_calculus as v21_shared
from naya_kernel.nodes.connect_node import ConnectNode

FROZEN_SHA = "4768636fb9c2ac640bf23faa6dc10ece1376cf90"

_BASE = {
    "id": "c-1",
    "kind": "GRAPH_EDGE",
    "purpose": "p",
    "scope": [{"content_classes": ["PUBLIC"]}],
    "consentRefs": ["c1"],
    "boundaryPolicy": "bp",
    "parties": [{"identity": "alice", "owner_scope": "alpha"}],
    "consentLadder": "SHARED",
    "reversibility": 5,
}


def _profile():
    return v21_shared.QualityProfile(
        profile_id="connect-v21map", version="V2.1", objective="o"
    )


def _gate_for(refs):
    node = ConnectNode()
    req = dict(_BASE)
    req["evidenceRefs"] = refs
    cand = node._to_v21_candidate(req)
    gate, reasons, q = v21_shared.gate_candidate(cand, _profile(), v21_shared.RiskPolicy())
    return cand.quality["evidence_sufficiency"], gate, q["Q"]


# ==========================================================================
# 1. AMPLIFICATION IS REAL -- duplicates inflate quality
# ==========================================================================
def test_duplicates_are_indistinguishable_from_distinct_references():
    """PROVEN: N copies of one reference score identically to N distinct ones."""
    _, _, q_dup = _gate_for(["e1"] * 5)
    _, _, q_distinct = _gate_for(["e1", "e2", "e3", "e4", "e5"])
    assert q_dup == q_distinct, (
        "distinct handling changed; update this test before trusting the "
        "correlation-blindness finding"
    )


def test_repeating_one_reference_inflates_quality():
    """PROVEN: repeating a single reference raises reported quality."""
    _, _, q_one = _gate_for(["e1"])
    _, _, q_five = _gate_for(["e1"] * 5)
    assert q_five > q_one, f"no amplification observed ({q_one} -> {q_five})"


def test_amplification_saturates_at_the_cap():
    """PROVEN: the attack saturates; more copies buy nothing."""
    suff_five, _, _ = _gate_for(["e1"] * 5)
    suff_twenty, _, _ = _gate_for(["e1"] * 20)
    assert suff_five == 10.0
    assert suff_twenty == 10.0, "cap is not 10.0; mapping may have changed"


# ==========================================================================
# 2. NOT PROVEN -- amplification does not currently buy authorization
# ==========================================================================
def test_amplification_alone_does_not_change_the_gate():
    """Guards against overclaiming an authorization bypass.

    This test is deliberately narrow: it asserts only that, in this
    configuration, reference-count inflation does not by itself move the gate
    off NEEDS_EVIDENCE. It does NOT assert that amplification is harmless --
    the correlation-blindness defect stands regardless of this result.
    """
    gates = {}
    for label, refs in [
        ("none", []),
        ("one", ["e1"]),
        ("dup_x5", ["e1"] * 5),
        ("distinct_x5", ["e1", "e2", "e3", "e4", "e5"]),
    ]:
        _, gate, _ = _gate_for(refs)
        gates[label] = gate

    assert len(set(gates.values())) == 1, (
        f"reference count DID move the gate: {gates}. If this now differs, "
        "reassess whether duplication can buy admissibility and report it."
    )
    assert set(gates.values()) == {v21_shared.NEEDS_EVIDENCE}, gates


def test_unknown_stays_unknown_not_defaulted():
    """Mapping must not invent certainty for fields the request omits."""
    node = ConnectNode()
    cand = node._to_v21_candidate(dict(_BASE, evidenceRefs=["e1"]))
    blob = repr(cand)
    assert "None" in blob, (
        "expected omitted fields to remain UNKNOWN (None); if they are now "
        "defaulted, that is a mapping-fidelity finding worth filing"
    )


def test_frozen_sha_recorded():
    assert len(FROZEN_SHA) == 40
    assert v21_shared.ENGINE_VERSION == "DECISION-VALUE-CALCULUS-V2.1"