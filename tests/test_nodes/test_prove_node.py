"""NAYA-KERNEL-PROVE tests (CANDIDATE — NOT RATIFIED — NOT MERGED).

Mirrors the PROVE-NODE-SPEC-CANDIDATE.md §9 acceptance battery (12 items),
plus NodeBase conformance, the §4 refusal family, §2.4/§3.8 stakes handling,
the §6.1 graph-edge mapping, and the §8 seal-to-cross freshness rule.

Evidence-law note: tests assert refusal and hold behavior as first-class
outcomes. A refusal that fires correctly is a PASS of the battery, not a
failure of the implementation.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes import prove_node
from naya_kernel.nodes.prove_node import ProveNode


NOW = datetime.now(timezone.utc)
TS = NOW.isoformat()
FRESH = (NOW - timedelta(hours=2)).isoformat()
STALE = (NOW - timedelta(days=30)).isoformat()


def make_evidence(n, *, source_prefix="sensor", method="direct-read",
                  acquired_at=FRESH, qualified=True, independent=True,
                  restates=False, provisional=False, distinct_failure_modes=True):
    """Build n evidence refs. Independent by default: distinct source, method,
    and day per item; distinct failure_mode per item so no single shared
    failure mode collapses independence (§3.9)."""
    out = []
    for i in range(n):
        day = (NOW - timedelta(days=i)).isoformat() if distinct_failure_modes else acquired_at
        out.append({
            "address": f"ev-{source_prefix}-{i}",
            "source": f"{source_prefix}-{i}",
            "acquisition_method": f"{method}-{i}",
            "acquired_at": day,
            "qualified_oracle": qualified,
            "failure_mode": f"mode-{i}" if distinct_failure_modes else "shared-mode",
            "independent_of_claim": independent,
            "restates_claim": restates,
            "provisional_until": (NOW + timedelta(days=7)).isoformat() if provisional else None,
        })
    return out


def base_claim(**over):
    claim = {
        "id": "claim-001",
        "class": "EMPIRICAL",
        "assertion": "the suite passed",
        "assertions": [{"text": "the suite passed", "evidence": ["ev-0"]}],
        "evidence": make_evidence(5),
        "stakes": "low",
        "overturn_conditions": ["a failing run under the same conditions"],
        "observation_recorded_with_method": True,
        "raw_data_retained": True,
        "freshness_seconds": 7 * 24 * 3600,
        "as_of": TS,
    }
    claim.update(over)
    return claim


def seal_consequential(node, claim_id="claim-001"):
    """Drive a consequential EMPIRICAL claim all the way to sealed L4."""
    claim = base_claim(
        id=claim_id,
        stakes="consequential",
        evidence=make_evidence(6),
        assertions=[{"text": "the deployment is live", "evidence": ["ev-sensor-0"]}],
        recompute={
            "independence_dimension": "blinded_inputs",
            "can_disagree": True,
            "result": "MATCH",
            "method": "independent observer re-derived the state from the evidence",
        },
    )
    node.submit(claim)
    last = None
    for _ in range(4):
        last = node.advance(claim_id)
    assert last["level"] == 4 and last["sealed"], last
    return claim_id


# -- NodeBase conformance ----------------------------------------------------


def test_nodebase_conformance():
    assert issubclass(ProveNode, NodeBase)
    node = ProveNode()
    entry = node.manifest_entry()
    assert entry.node_id == "NAYA-KERNEL-PROVE"
    assert entry.responsibilities
    assert len(node.persisted_transitions()) >= 8
    assert node.evidence_hooks()
    assert "no_authority_granted_by_prove" in node.authority_checks()
    # authority_checks declares but never grants (convention from prior nodes).
    assert not any("grant" in c.lower() and "never" not in c.lower() and "no_" not in c
                   for c in node.authority_checks())


def test_gate_conformance_intake():
    node = ProveNode()
    claim = base_claim()
    node.submit(claim)
    result = node.gate({"claim": claim})
    assert result.verdict in (GateVerdict.NEED_EVIDENCE, GateVerdict.PASS)
    # A bare intake never invents PASS for unproven material.
    assert result.verdict == GateVerdict.NEED_EVIDENCE


def test_gate_conformance_pass_on_sealed():
    node = ProveNode()
    claim_id = seal_consequential(node)
    claim = node._claims[claim_id]["claim"]
    result = node.gate({"claim": claim})
    assert result.verdict == GateVerdict.PASS


def test_gate_conformance_refusal_is_fail():
    node = ProveNode()
    claim = base_claim(id="claim-ref", about="prove-machinery")
    result = node.gate({"claim": claim})
    assert result.verdict == GateVerdict.FAIL
    assert any("§4.2" in r for r in result.reasons)


# -- §9.1: bare assertion with no evidence is UNPROVEN by construction ------


def test_1_bare_assertion_unproven_by_construction():
    node = ProveNode()
    claim = base_claim(id="claim-bare", evidence=[], assertions=[{"text": "x", "evidence": []}])
    node.submit(claim)
    out = node.advance("claim-bare")
    assert out["advanced"] is False and out["level"] == 0
    assert "UNPROVEN by construction" in node._gate_G1(claim)["reasons"][0]


# -- §9.2: evidence without resolvable provenance names the gap -------------


def test_2_unresolvable_provenance_names_gap():
    node = ProveNode()
    bad = make_evidence(1)[0]
    del bad["source"]
    bad["acquired_at"] = "not-a-time"
    claim = base_claim(id="claim-prov", evidence=[bad],
                       assertions=[{"text": "x", "evidence": [bad["address"]]}])
    node.submit(claim)
    g2 = node._gate_G2(claim)
    assert not g2["passed"]
    assert any("missing source" in r for r in g2["reasons"])
    assert any("unparseable acquired_at" in r for r in g2["reasons"])


# -- §9.3: laundering — claim restated as its own evidence ------------------


def test_3_laundering_fails_g3_and_records_finding():
    node = ProveNode()
    claim = base_claim(id="claim-launder",
                       evidence=make_evidence(2, independent=False, restates=True),
                       assertions=[{"text": "x", "evidence": ["ev-sensor-0"]}])
    node.submit(claim)
    out = node.advance("claim-launder")
    assert out["advanced"] is False
    assert any("§4.3" in r for r in out["refusal"])
    findings = node._findings.get("claim-launder", [])
    assert any(f["kind"] == "evidence_laundering" for f in findings)
    # Findings carry no automatic consequence — the node still holds no authority.
    assert "no_authority_granted_by_prove" in node.authority_checks()


# -- §9.4: IMPLEMENTED without read-back is refused, not "pending" ----------


def test_4_implemented_without_readback_refused():
    node = ProveNode()
    claim = base_claim(id="claim-impl", **{"class": "PROCEDURAL", "implemented_only": True})
    node.submit(claim)
    out = node.advance("claim-impl")
    assert out["advanced"] is False
    assert any("§4.4" in r for r in out["refusal"])
    # With a real read-back the PROCEDURAL battery can pass G4.
    claim2 = base_claim(id="claim-impl2", **{
        "class": "PROCEDURAL", "implemented_only": False, "read_back_observed": True})
    node.submit(claim2)
    out2 = node.advance("claim-impl2")
    assert out2["level"] == 1  # G1–G3 pass; L2 needs G4+floors (procedural floors)


# -- §9.5: predictions capped at L1 ------------------------------------------


def test_5_predictive_capped_at_l1_and_refused_for_l2():
    node = ProveNode()
    claim = base_claim(
        id="claim-pred", **{
            "class": "PREDICTIVE", "stakes": "low",
            "basis_stated": True, "uncertainty_bound": True,
            "falsification_conditions": True,
            "evidence": make_evidence(3),
        })
    node.submit(claim)
    out = node.advance("claim-pred")
    assert out["level"] == 1 and out["sealed"]  # sealed *to its cap* (§1.5)
    # Presenting it for L2+ is refused outright.
    claim2 = dict(claim)
    claim2["id"] = "claim-pred2"
    claim2["is_prediction_presented_for"] = 2
    node.submit(claim2)
    out2 = node.advance("claim-pred2")
    assert out2["advanced"] is False
    assert any("§4.1" in r for r in out2["refusal"])


def test_5b_forecast_crossing_rule():
    node = ProveNode()
    claim = base_claim(
        id="claim-fc", **{
            "class": "PREDICTIVE", "stakes": "low",
            "basis_stated": True, "uncertainty_bound": True,
            "falsification_conditions": True,
            "evidence": make_evidence(3),
            "forecast_horizon_until": (NOW + timedelta(days=3)).isoformat(),
        })
    node.submit(claim)
    node.advance("claim-fc")
    cross = node.forecast_crossing("claim-fc")
    assert cross["cross"] is True and cross["as"] == "forecast"
    assert cross["valid_until"] == claim["forecast_horizon_until"]
    # No horizon → no crossing.
    claim2 = dict(claim); claim2["id"] = "claim-fc2"; del claim2["forecast_horizon_until"]
    node.submit(claim2); node.advance("claim-fc2")
    cross2 = node.forecast_crossing("claim-fc2")
    assert cross2["cross"] is False
    # Non-predictive claims may not use the forecast path.
    node.submit(base_claim(id="np"))
    with pytest.raises(ValueError):
        node.forecast_crossing("np")


# -- §9.6: claims about PROVE's own machinery route to VERIFY ----------------


def test_6_prove_machinery_claims_route_to_verify():
    node = ProveNode()
    claim = base_claim(id="claim-selfcert", about="prove-machinery")
    node.submit(claim)
    out = node.advance("claim-selfcert")
    assert out["advanced"] is False
    assert any("§4.2" in r and "VERIFY" in r for r in out["refusal"])


# -- §9.7: G5 theater is rejected --------------------------------------------


def test_7_g5_theater_rejected():
    node = ProveNode()
    claim = base_claim(
        id="claim-theater", stakes="high",
        recompute={"result": "MATCH"},  # no dimension, no can_disagree → theater
    )
    node.submit(claim)
    node.advance("claim-theater")
    out = node.advance("claim-theater")
    assert out["level"] == 2  # climbs to TESTED, held there: G5 fails
    g5 = node._gate_G5(claim)
    assert not g5["passed"]
    assert any("theater" in r for r in g5["reasons"])


# -- §9.8: consequential claims reach CONNECT only with sealed L4 ------------


def test_8_consequential_crosses_only_on_sealed_l4():
    node = ProveNode()
    claim = base_claim(
        id="claim-cons", stakes="consequential",
        evidence=make_evidence(6),
        recompute={"independence_dimension": "agent", "can_disagree": True,
                   "result": "MATCH"},
    )
    node.submit(claim)
    early = node.crossing_check("claim-cons")
    assert early["cross"] is False
    assert "unproven" in early["reason"]
    for _ in range(4):
        out = node.advance("claim-cons")
    assert out["level"] == 4 and out["sealed"]
    late = node.crossing_check("claim-cons")
    assert late["cross"] is True
    assert late["sealed_receipt"]


# -- §9.9: unproven material refused at the boundary with a receipt ----------


def test_9_unproven_refused_at_boundary_with_receipt():
    node = ProveNode()
    node.submit(base_claim(id="claim-unproven"))
    out = node.crossing_check("claim-unproven")
    assert out["cross"] is False
    assert out["receipt_id"] in node._receipts
    assert node._receipts[out["receipt_id"]]["kind"] == "crossing_refused"


# -- §9.10: challenge → both sides visible; re-gate or invalidate ------------


def test_10_challenge_moves_to_challenged_and_invalidates():
    node = ProveNode()
    claim_id = seal_consequential(node)
    # Counter-evidence that fails the gates on the augmented set (e.g. a
    # single restated observation) drags the claim down.
    counter = make_evidence(1, source_prefix="counter", restates=True,
                            independent=False, distinct_failure_modes=False)
    out = node.challenge(claim_id, counter)
    assert out["state"] == "INVALIDATED"
    assert node._claims[claim_id]["sealed"] is False


def test_10b_challenge_survived_restores_level():
    node = ProveNode()
    claim_id = seal_consequential(node)
    # Weak-but-honest counter-evidence: independent, qualified — gates still pass.
    counter = make_evidence(2, source_prefix="counter")
    out = node.challenge(claim_id, counter)
    assert out["state"] == "PROVEN"
    assert node._claims[claim_id]["sealed_receipt_id"] is not None


# -- §9.11: cold successor recomputes sealed verdict to MATCH ----------------


def test_11_recompute_match_and_cold_reconstruct():
    node = ProveNode()
    claim_id = seal_consequential(node)
    receipt_id = node._claims[claim_id]["sealed_receipt_id"]
    assert node.recompute(receipt_id) == "MATCH"
    # A receipt whose machinery binding changed cannot recompute.
    tampered = dict(node._receipts[receipt_id])
    tampered["battery_version"] = "0.9.9-evil"
    assert node._recompute_from_receipt(tampered) == "MISMATCH"
    # Cold reconstruction replays receipts; mismatching seals demote.
    fresh = ProveNode()
    state = fresh.cold_reconstruct([node._receipts[receipt_id], tampered])
    assert state["determinism"]["checked"] == 2
    assert state["determinism"]["matched"] == 1
    assert tampered["id"] in state["determinism"]["mismatched"]


# -- §9.12: "just this once" is refused and receipted -------------------------


def test_12_floor_lowering_refused_and_briefed():
    node = ProveNode()
    claim_id = seal_consequential(node, "claim-floor")
    # Reset to a held state to make the override meaningful.
    node._claims[claim_id]["maturity_level"] = 2
    node._claims[claim_id]["state"] = "TESTED"
    out = node.advance(claim_id, override=True)
    assert out["advanced"] is False
    assert "§4.6" in out["refusal"]
    assert out["receipt_id"] in node._receipts
    # Consequential → BRIEFED to the Director, 9-part artifact, open item.
    assert "director_brief_id" in out
    brief = next(b for b in node._briefs if b["id"] == out["director_brief_id"])
    assert brief["status"] == "open"
    for part in ("decision_required", "meaning", "options", "benefits_risks",
                 "reversibility", "evidence", "uncertainty", "recommendation",
                 "authorization_requested"):
        assert brief[part]


# -- stakes: §2.4 default high; raise bounded (§3.8); never lower -------------


def test_stakes_default_high_and_raise_bounded():
    node = ProveNode()
    claim = base_claim(id="claim-stakes")
    del claim["stakes"]
    node.submit(claim)
    assert node._stakes(claim) == "high"
    raised = node.raise_stakes("claim-stakes", "new evidence of blast radius")
    assert raised["stakes"] == "consequential"
    # Second raise without new deficiency evidence is refused (§3.8).
    with pytest.raises(ValueError):
        node.raise_stakes("claim-stakes", "again")
    # With new deficiency evidence, a *different* claim may raise twice.
    node.submit(base_claim(id="claim-stakes2", stakes="low"))
    node.raise_stakes("claim-stakes2", "r1", deficiency_evidence=["e1"])
    node.raise_stakes("claim-stakes2", "r2", deficiency_evidence=["e2"])


def test_prove_may_raise_never_lower():
    node = ProveNode()
    node.submit(base_claim(id="claim-nolower", stakes="consequential"))
    with pytest.raises(ValueError):
        node.raise_stakes("claim-nolower", "nope")
    # The required-level table is never lowered by PROVE — no API exists for it.


# -- evidence floors §3.9 ------------------------------------------------------


def test_n1_caps_at_l1_no_n1_proven():
    node = ProveNode()
    claim = base_claim(id="claim-n1", stakes="low",
                       evidence=make_evidence(1),
                       assertions=[{"text": "x", "evidence": ["ev-sensor-0"]}])
    node.submit(claim)
    out = node.advance("claim-n1")
    assert out["level"] == 1
    out = node.advance("claim-n1")
    assert out["level"] == 1  # capped: floors fail, single observation


def test_shared_failure_mode_collapses_independence():
    node = ProveNode()
    claim = base_claim(id="claim-shared", stakes="low",
                       evidence=make_evidence(6, distinct_failure_modes=False),
                       assertions=[{"text": "x", "evidence": ["ev-sensor-0"]}])
    indep = node._independent_observations(claim)
    assert indep == []  # one shared failure mode → not independent (§3.9)


def test_qualified_priors_floor():
    node = ProveNode()
    claim = base_claim(id="claim-priors", stakes="low",
                       evidence=make_evidence(2, distinct_failure_modes=False),
                       priors=[{"qualified": True, "ref": f"p{i}"} for i in range(20)],
                       assertions=[{"text": "x", "evidence": ["ev-sensor-0"]}])
    floors = node._evidence_floors(claim)
    assert floors["passed"]


# -- provisional evidence §3.10 -------------------------------------------------


def test_provisional_evidence_capped_at_l2():
    node = ProveNode()
    claim = base_claim(id="claim-prov2", stakes="low",
                       evidence=make_evidence(5, provisional=True),
                       assertions=[{"text": "x", "evidence": ["ev-sensor-0"]}])
    node.submit(claim)
    node.advance("claim-prov2")
    out = node.advance("claim-prov2")
    assert out["level"] == 2
    out = node.advance("claim-prov2")  # G5 would pass, but the cap holds
    assert out["level"] == 2
    assert node._claims["claim-prov2"].get("regate_queued_until")


# -- graph edge mapping §6.1 -----------------------------------------------------


def test_attestation_edge_maps_proven_to_supported_never_verified():
    node = ProveNode()
    claim_id = seal_consequential(node)
    receipt = node._receipts[node._claims[claim_id]["sealed_receipt_id"]]
    edge = node.attestation_edge(receipt)
    assert edge["relationship_type"] == "SUPPORTS"
    assert edge["epistemic_state"] == "SUPPORTED"  # PROVEN → SUPPORTED, never VERIFIED
    assert edge["epistemic_state"] != "VERIFIED"
    assert "PROVE_SEALED_L4" in edge["reason_codes"]
    assert "VERIFIED_BY" not in str(edge)
    challenge_edge = node.attestation_edge(receipt, kind="challenge")
    assert challenge_edge["relationship_type"] == "CONTRADICTS"
    assert challenge_edge["epistemic_state"] == "CONTRADICTED"


# -- seal-to-cross freshness §8 ----------------------------------------------------


def test_seal_to_cross_freshness_blocks_stale_seal():
    node = ProveNode()
    claim_id = seal_consequential(node)
    first = node.crossing_check(claim_id)
    assert first["cross"] is True
    # A challenge lands in the gap; it survives re-gating...
    node.challenge(claim_id, make_evidence(2, source_prefix="gap"))
    # ...but the seal is no longer the latest seal-affecting write: crossing holds.
    held = node.crossing_check(claim_id)
    assert held["cross"] is False
    assert "seal-to-cross" in held["reason"]
    # Re-gating re-affirms the seal; crossing passes again.
    node.advance(claim_id)
    again = node.crossing_check(claim_id)
    assert again["cross"] is True


# -- §4.5 proof as permission: stamped, authorization inference refused ----------


def test_proof_as_permission_flagged():
    node = ProveNode()
    claim = base_claim(id="claim-perm", stakes="low", offered_as_authorization=True)
    node.submit(claim)
    out = node.advance("claim-perm")
    assert out["advanced"] is False
    assert any("§4.5" in r for r in out["refusal"])
    # The stamp path (without the category error) is independent.
    claim2 = base_claim(id="claim-perm2", stakes="low")
    node.submit(claim2)
    out2 = node.advance("claim-perm2")
    assert out2["advanced"] is True


# -- §4.7 bundle rule --------------------------------------------------------------


def test_bundle_rule_reassembles_decomposition():
    node = ProveNode()
    claim = base_claim(id="claim-bundle", stakes="low",
                       pieces=[{"id": "p1"}, {"id": "p2"}])
    node.submit(claim)
    out = node.advance("claim-bundle")
    assert out["advanced"] is False
    assert any("§4.7" in r for r in out["refusal"])


# -- §4.8 BLOCKED stays UNPROVEN -----------------------------------------------------


def test_blocked_never_counts_as_established():
    node = ProveNode()
    claim = base_claim(id="claim-blocked", block_state="BLOCKED")
    node.submit(claim)
    out = node.advance("claim-blocked")
    assert out["advanced"] is False
    assert any("§4.8" in r for r in out["refusal"])


# -- G6 calibration §3.6 ---------------------------------------------------------------


def test_quantitative_without_uncertainty_stays_unproven():
    node = ProveNode()
    claim = base_claim(id="claim-q", stakes="low", quantitative=True,
                       uncertainty_stated=False,
                       recompute={"independence_dimension": "agent",
                                  "can_disagree": True, "result": "MATCH"})
    node.submit(claim)
    node.advance("claim-q")
    node.advance("claim-q")
    out = node.advance("claim-q")
    assert out["level"] == 3  # G6 fails at the L3→L4 step
    claim2 = base_claim(id="claim-q2", stakes="low", quantitative=True,
                        uncertainty_stated=True,
                        recompute={"independence_dimension": "agent",
                                   "can_disagree": True, "result": "MATCH"})
    node.submit(claim2)
    for _ in range(4):
        out2 = node.advance("claim-q2")
    assert out2["level"] == 4 and out2["sealed"]


# -- G7 freshness ------------------------------------------------------------------------


def test_stale_evidence_fails_g7():
    node = ProveNode()
    claim = base_claim(id="claim-stale", stakes="low", freshness_seconds=86400,
                       evidence=make_evidence(5, acquired_at=STALE),
                       assertions=[{"text": "x", "evidence": ["ev-sensor-0"]}])
    node.submit(claim)
    g7 = node._gate_G7(claim)
    assert not g7["passed"]
    assert any("stale" in r for r in g7["reasons"])


# -- deductive battery -------------------------------------------------------------------


def test_deductive_premises_must_meet_required_level():
    node = ProveNode()
    claim = base_claim(id="claim-ded", **{
        "class": "DEDUCTIVE", "stakes": "low",
        "premises": [{"level": 2}, {"level": 1}],  # one premise below required L2
    })
    node.submit(claim)
    out = node.advance("claim-ded")
    assert out["level"] == 1  # G4 fails: weak premise


# -- supersession --------------------------------------------------------------------------


def test_supersede_keeps_lineage():
    node = ProveNode()
    node.submit(base_claim(id="claim-old", stakes="low"))
    node.advance("claim-old")
    node.advance("claim-old")  # sealed L2
    node.submit(base_claim(id="claim-new", stakes="low"))
    node.advance("claim-new")
    node.advance("claim-new")
    node.raise_stakes("claim-new", "consequential blast radius")  # L4 required
    node._claims["claim-new"]["claim"]["recompute"] = {
        "independence_dimension": "evidence_selection", "can_disagree": True,
        "result": "MATCH"}
    for _ in range(3):
        node.advance("claim-new")
    assert node._claims["claim-new"]["maturity_level"] == 4
    out = node.supersede("claim-old", "claim-new")
    assert out["state"] == "SUPERSEDED"
    assert node._claims["claim-old"]["superseded_by"] == "claim-new"


# -- receipts: hash-bound, field-complete (§5) ----------------------------------------------


def test_receipt_carries_spec_fields_and_hash():
    node = ProveNode()
    node.submit(base_claim(id="claim-rcpt"))
    out = node.advance("claim-rcpt")
    receipt = node._receipts[out["receipt_id"]]
    for field in ("claim_id", "claim_class", "stakes", "required_level",
                  "maturity_level", "battery_id", "battery_version",
                  "overturn_conditions", "issued_at", "issued_by",
                  "execution_id", "receipt_hash", "claim_snapshot"):
        assert field in receipt, field
    assert receipt["receipt_hash"]
    assert receipt["battery_id"] == "prove-acceptance-battery"
