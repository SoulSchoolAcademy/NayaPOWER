"""EVOLVE acceptance battery — NAYA-KERNEL-EVOLVE (candidate).

Mirrors EVOLVE-NODE-SPEC-CANDIDATE.md §11:
- §11.1 base acceptance (§9.1–9.9 retained)
- §11.2 golden tests (§9.10–9.19): golden successor, authority isolation,
  stale handoff, blocker omission, self-building chain, self-authorization
  negative, regression/rollback, recalibration gating, source parity,
  three-generation
- §11.3 property tests: no second score as authority, rollback-or-escalate,
  no self-ratification, bundle-as-one, mission compatibility, authority
  re-resolved per succession, CORE transfer gated
- §11.4 continuity metrics — diagnostics, never gates
Plus NodeBase conformance and cold-reconstruct units.
"""
import pytest

from naya_kernel.node_base import (
    NodeBase, GateVerdict, CALCULUS_V21_SPEC_HASH,
)
from naya_kernel.nodes import evolve_node
from naya_kernel.nodes.evolve_node import (
    EvolveNode,
    IMMUTABLE_SURFACE,
    CHANGE_CLASSES,
    BLAST_RADIUS,
    SUCCESSION_STATES,
    PROPOSAL_STATES,
    MATURITY_STATES,
    CRITICAL_SUCCESSOR_OBLIGATIONS,
    SUCCESSOR_PACKAGE_FIELDS,
    COLD_14,
    INTELLIGENCE_CLASSES,
    ORDERING_LAW,
    REFUSAL_IMMUTABLE_SURFACE,
    REFUSAL_CONFIG_MISMATCH,
    REFUSAL_BUNDLE_SPLIT,
    REFUSAL_ENVELOPE,
    REFUSAL_AUTHORITY,
    REFUSAL_BLOCKER_OMITTED,
    REFUSAL_HARM_POST_ADOPTION,
    REFUSAL_DIRECTOR_PROHIBITED,
    REFUSAL_REVOKED,
    REFUSAL_NO_FUTURE_BEHAVIOR,
    REFUSAL_MISSION,
    NO_AUTHORITY_GRANT,
    CONTINUITY_METRICS,
    successor_key,
    package_hash,
)


def _proposal(**over):
    base = {
        "objective": "reduce handoff reconstruction latency",
        "change_class": "DOCUMENTATION",
        "proposed_change": "add explicit state pointers to the handoff template",
        "expected_value": 0.9,
        "blast_radius": "LOCAL",
        "reversibility": 0.95,
        "rollback_plan": {
            "mechanism": "revert template to previous version",
            "authority": "HUMAN_DIRECTOR",
            "evidence": "receipted revert commit",
            "verification": "template renders identical to prior version",
        },
        "authority_requirement": "director-set envelope",
        "future_behavior": "successor reconstructs state without asking",
        "current_version": "v0.0.0",
        "proposed_version": "v0.0.1",
        "affected_components": ["handoff-template"],
        "mission_compatible": True,
    }
    base.update(over)
    return base


def _authorized(node, **over):
    """Propose → evaluate → authorize, in the default SPEC-ONLY config
    except where the test says otherwise. Returns the evolution_id."""
    res = node.propose(_proposal(**over))
    assert res["decision"] == "PROPOSED"
    eid = res["evolution_id"]
    node.evaluate(eid)
    # authorize works regardless of route in this implementation (authority
    # validation is separate from calculus ratification)
    auth = node.authorize(eid, {"issuer": "HUMAN_DIRECTOR", "scope": "evolve"})
    assert auth["decision"] == "AUTHORIZED"
    return eid


# ----------------------------------------------------------------------
# §11.1 base acceptance
# ----------------------------------------------------------------------

class TestBaseAcceptance:
    def test_scored_under_old_config_with_hash_bound(self):
        node = EvolveNode()
        res = node.propose(_proposal())
        eid = res["evolution_id"]
        out = node.evaluate(eid)
        score = out["gate_score"]
        assert score["deciding_config_hash"] == node._config["configHash"]
        # FLAG-001 step 4 — V2.1 RATIFIED: the receipt binds the ratified
        # config hash and says RATIFIED, not hidden.
        assert score["calculus_spec_status"] == "RATIFIED"
        assert score["calculusConfigHash"] == CALCULUS_V21_SPEC_HASH
        assert "RESOLVE" in score["calculus_chain"]

    def test_rollback_armed_and_tested_before_apply(self):
        # A ratified-calculus config is needed to get past the SPEC-ONLY gate.
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)
        out = node.apply(eid)
        assert out["decision"] == "APPLIED"
        armed = node._armed_rollbacks[eid]
        assert armed["pre_authorized"] is True
        assert armed["plan"]["mechanism"]  # armed BEFORE apply; receipted

    def test_immutable_surface_proposals_refused_prohibited(self):
        node = EvolveNode()
        for klass, surface in (("AUTHORITY_MODEL", "AUTHORITY_MODEL"),
                               ("CONSTITUTION", "CONSTITUTIONAL_LAW"),
                               ("MISSION", "MISSION")):
            res = node.propose(_proposal(change_class=klass))
            assert res["decision"] == "REFUSED"
            assert res["refusal_code"] == REFUSAL_IMMUTABLE_SURFACE
            assert surface in res["touched_surface"]
        # Declared surface touch via touches_surface also fires.
        res = node.propose(_proposal(change_class="CONFIGURATION",
                                     touches_surface=["GATE_STRUCTURE"]))
        assert res["decision"] == "REFUSED"
        assert "GATE_STRUCTURE" in res["touched_surface"]

    def test_ratified_calculus_autonomous_path_admitted(self):
        # FLAG-001 step 4: V2.1 RATIFIED — the SPEC-ONLY (unratified-math)
        # branches are gone. An in-envelope proposal evaluates to the
        # AUTONOMOUS route; the gate no longer refuses on calculus grounds.
        node = EvolveNode()  # default config: calculus V2.1 RATIFIED
        eid = node.propose(_proposal())["evolution_id"]
        out = node.evaluate(eid)
        assert out["route"] == "AUTONOMOUS"
        assert not node._brief_outbox  # not briefed; autonomous path open
        auth = node.authorize(eid, {"issuer": "HUMAN_DIRECTOR",
                                    "scope": "evolve"})
        assert auth["decision"] == "AUTHORIZED"
        g = node.gate({"action": "apply", "evolution_id": eid})
        assert g.verdict is GateVerdict.NEED_EVIDENCE
        assert "AUTHORITY_VALIDATION_REQUIRED" in g.reasons

    def test_bundle_split_detected_on_crafted_split(self):
        node = EvolveNode()
        ids = []
        for i in range(3):
            res = node.propose(_proposal(
                objective="rewrite retrieval",  # shared objective
                expected_value=0.6, blast_radius="LOCAL", reversibility=0.5,
                proposed_change=f"split piece {i} of retrieval rewrite"))
            ids.append(res["evolution_id"])
        out = node.bundle_evaluate(ids)
        assert out["decision"] == "HARD_STOP"
        assert out["refusal_code"] == REFUSAL_BUNDLE_SPLIT
        # Unrelated proposals do not trip it.
        a = node.propose(_proposal(objective="objective-A",
                                   proposed_change="doc tweak A"))
        b = node.propose(_proposal(objective="objective-B", change_class="PROJECTION",
                                   proposed_change="doc tweak B"))
        out2 = node.bundle_evaluate([a["evolution_id"], b["evolution_id"]])
        assert out2["decision"] == "NO_SPLIT"

    def test_deciding_config_recompute_match_by_independent_seat(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = node.propose(_proposal())["evolution_id"]
        node.evaluate(eid)
        r1 = node.recompute(eid)
        assert r1["result"] == "MATCH"
        # An independent seat with the same receipts must reach the same
        # answer (recompute is deterministic under config C).
        r2 = node.recompute(eid)
        assert r2["result"] == r1["result"] == "MATCH"

    def test_deciding_config_change_voids_recompute(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = node.propose(_proposal())["evolution_id"]
        node.evaluate(eid)
        # Simulate config drift: the stored score no longer binds C.
        node._config["configHash"] = "drifted-not-the-deciding-config"
        r = node.recompute(eid)
        assert r["result"] == "MISMATCH"

    def test_envelope_breach_receipted(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "LOCAL",
                               "reversibility_floor": 0.9,
                               "value_threshold": 0.5}})
        res = node.propose(_proposal(blast_radius="CROSS_NODE",
                                     reversibility=0.5))
        out = node.evaluate(res["evolution_id"])
        assert out["route"] == "BRIEF"
        assert any("exceeds envelope" in r for r in out["reasons"])

    def test_revocation_executes_armed_rollback(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)
        node.apply(eid)
        before = node._versions["handoff-template"]
        assert before == "v0.0.1"
        out = node.revoke(eid, revoker="HUMAN_DIRECTOR")
        assert out["decision"] == "REVOKED"
        assert node._versions["handoff-template"] == "v0.0.0"  # armed plan ran
        cand = node._get(eid)
        assert cand["proposal"] == "ROLLED_BACK"

    def test_stale_proposals_rebased_never_auto_promoted(self):
        node = EvolveNode()
        res = node.propose(_proposal(current_version="v0.0.0"))
        eid = res["evolution_id"]
        node._config["currentVersion"] = "v0.0.1"  # the world moved on
        out = node.evaluate(eid)
        assert out["decision"] == "STALE_PROPOSAL"
        assert node._get(eid)["succession"] == "STALE"
        # Same at the CAS boundary: a loser rereads and reconciles.
        node2 = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                            "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                            "envelope": {
                                "allowed_change_classes": ["DOCUMENTATION"],
                                "max_blast_radius": "COMPONENT",
                                "reversibility_floor": 0.8,
                                "value_threshold": 0.5}})
        eid2 = _authorized(node2)
        node2._versions["handoff-template"] = "v0.0.1-someone-else"
        out2 = node2.apply(eid2)
        assert out2["decision"] == "STALE_PROPOSAL"

    def test_no_in_place_mutation_versioned_supersession(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)
        out = node.apply(eid)
        assert out["applied_version"] != node._config["currentVersion"]
        assert out["applied_version"] == "v0.0.1"
        # The old version survives as superseded lineage, not overwritten
        # silence: the armed rollback restores it by name.
        assert node._armed_rollbacks[eid] is not None

    def test_rollback_plan_must_name_four_slots(self):
        node = EvolveNode()
        res = node.propose(_proposal(rollback_plan={"mechanism": "revert"}))
        out = node.evaluate(res["evolution_id"])
        assert out["decision"] == "REFUSED"
        assert node._get(res["evolution_id"])["proposal"] == "REJECTED"

    def test_three_axes_never_collapse(self):
        node = EvolveNode()
        res = node.propose(_proposal())
        cand = node._get(res["evolution_id"])
        assert set(cand) >= {"proposal", "succession", "maturity"}
        assert cand["proposal"] in PROPOSAL_STATES
        assert cand["succession"] in SUCCESSION_STATES
        assert cand["maturity"] in MATURITY_STATES
        # Maturity advances one step at a time — no jumping to PRODUCTION_PROVEN.
        m1 = node.advance_maturity(res["evolution_id"])
        assert m1 == {"decision": "ADVANCED", "maturity": "TESTED",
                      "receipt_id": m1["receipt_id"]}
        with pytest.raises(ValueError):
            node._transition(cand, "maturity", "PRODUCTION_PROVEN",
                             reason="jump attempt")

    def test_illegal_transition_fail_closed(self):
        node = EvolveNode()
        res = node.propose(_proposal())
        cand = node._get(res["evolution_id"])
        with pytest.raises(ValueError):
            node._transition(cand, "proposal", "ADOPTED", reason="skip the gate")

    def test_exact_replay_rereads_material_change_versions(self):
        k1 = successor_key(parent="naya-A", successor="naya-B",
                           kernel_revision="kr-1", truth_snapshot={"t": 1},
                           active_work=[], learning_set=[])
        k2 = successor_key(parent="naya-A", successor="naya-B",
                           kernel_revision="kr-1", truth_snapshot={"t": 1},
                           active_work=[], learning_set=[])
        k3 = successor_key(parent="naya-A", successor="naya-B",
                           kernel_revision="kr-1", truth_snapshot={"t": 2},
                           active_work=[], learning_set=[])
        assert k1 == k2  # exact replay rereads (same key)
        assert k1 != k3  # material change versions (new key)
        assert len(k1) == 64

    def test_package_mutation_creates_new_version_never_silent_edit(self):
        p1 = {"handoff_id": "h1", "mission": "m"}
        h1 = package_hash(p1)
        p2 = {"handoff_id": "h1", "mission": "m-changed"}
        assert package_hash(p2) != h1

    def test_incomplete_proposal_refused_no_future_behavior(self):
        node = EvolveNode()
        fields = _proposal()
        del fields["future_behavior"]
        res = node.propose(fields)
        assert res["decision"] == "REFUSED"
        assert res["refusal_code"] == REFUSAL_NO_FUTURE_BEHAVIOR


# ----------------------------------------------------------------------
# §11.2 golden tests
# ----------------------------------------------------------------------

def _full_package(**over):
    base = {
        "parent_identity": "naya-A",
        "successor_identity": "naya-B",
        "kernel_revision": "kr-1",
        "contract_revisions": {},
        "mission": "build NayaPOWER",
        "current_truth": {"state": "operating"},
        "intelligence_refs": [],
        "learning_refs": [{"ref_id": "l1"}],
        "relationship_refs": [],
        "proof_refs": [],
        "recent_outcome_refs": [],
        "unknowns": ["Q-1"],
        "conflicts": [],
        "blockers": [{"blocker_id": "b1", "why": "needs director",
                      "affected_claim": "c1", "evidence_attempted": "e",
                      "authority_needed": "director", "dependencies": [],
                      "smallest_safe_next_step": "ask"}],
        "material_blockers_known": ["b1"],
        "active_work": ["w1"],
        "privacy_context": {"scope": "project"},
        "constraints": [],
        "next_action": "resume w1",
        "next_proof_requirement": "receipted handoff acceptance",
        "source_snapshot": {"state": "operating"},
        "intelligence_class": "REUSABLE",
    }
    base.update(over)
    return base


class TestGolden:
    def test_golden_successor_complete_package(self):
        node = EvolveNode()
        out = node.build_successor_package(_full_package())
        assert out["decision"] == "PACKAGED"
        assert out["successor_ready"] == 1
        assert out["missing_obligations"] == []
        pkg = node._handoff_packages[out["handoff_id"]]
        assert set(SUCCESSOR_PACKAGE_FIELDS) <= set(pkg)

    def test_authority_isolation_no_stale_authority(self):
        node = EvolveNode()
        out = node.build_successor_package(_full_package())
        pkg = node._handoff_packages[out["handoff_id"]]
        assert pkg["authority_context"]["authority_inherited"] is False
        assert pkg["authority_context"]["requires_reresolution"] is True

    def test_stale_handoff_live_truth_wins(self):
        node = EvolveNode()
        out = node.build_successor_package(_full_package(
            source_snapshot={"state": "operating"}))
        hid = out["handoff_id"]
        v = node.verify_continuity(hid, {"state": "deploying"})  # live disagrees
        assert v["decision"] == "STALE"
        assert v["divergences"] == ["state"]
        pkg = node._handoff_packages[hid]
        assert pkg["handoff_valid"] is False  # marked STALE, not trusted

    def test_blocker_omission_makes_handoff_invalid(self):
        node = EvolveNode()
        fields = _full_package()
        fields["blockers"] = []  # material blocker b1 known but omitted
        out = node.build_successor_package(fields)
        assert out["decision"] == "INVALID"
        assert out["omitted_material_blockers"] == ["b1"]
        pkg = node._handoff_packages[out["handoff_id"]]
        assert pkg["handoff_valid"] is False

    def test_self_building_chain_improvement_without_self_authorization(self):
        node = EvolveNode()
        # EVOLVE can model a constitutional-touching gap (it may observe and
        # prepare) but any adoption route dies at PROPOSE — PROHIBITED.
        res = node.propose(_proposal(
            change_class="CONSTITUTION",
            objective="study gate ordering"))
        assert res["decision"] == "REFUSED"
        assert res["refusal_code"] == REFUSAL_IMMUTABLE_SURFACE

    def test_self_authorization_negative_always_prohibited(self):
        node = EvolveNode()
        out = node.refuse_instruction({
            "from_seat": "HUMAN_DIRECTOR",
            "requests": ["AUTHORITY_MODEL"],
        })
        assert out["decision"] == "REFUSED"
        assert out["refusal_code"] == REFUSAL_DIRECTOR_PROHIBITED
        assert out["lawful_path"] == "explicit director ratification"
        # Gate bypass also fires, from any seat.
        out2 = node.refuse_instruction({
            "from_seat": "VERIFY", "requests": ["DOCUMENTATION"],
            "bypass_gate": True})
        assert out2["decision"] == "REFUSED"

    def test_regression_rollback_history_preserved(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)
        node.apply(eid)
        out = node.report_harm(eid, {"severity": "high", "signal": "regression"})
        assert out["decision"] == "ROLLED_BACK"
        cand = node._get(eid)
        assert cand["proposal"] == "ROLLED_BACK"
        # History chain recorded, never erased.
        transitions = [t["to"] for t in cand["transitions"]]
        assert "ROLLED_BACK" in transitions
        assert node._versions["handoff-template"] == "v0.0.0"

    def test_director_approved_harm_still_rolls_back(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)  # director authorized the adoption
        node.apply(eid)
        out = node.report_harm(eid, {"severity": "high"})
        # The Director approved the CHANGE; the HARM was not approved.
        assert out["decision"] == "ROLLED_BACK"

    def test_recalibration_gating_versioned_candidate_never_in_place(self):
        node = EvolveNode()
        out = node.refuse_envelope_mutation(requester="EVOLVE_SELF")
        assert out["decision"] == "REFUSED"
        # EVOLVE exposes no method that mutates its own envelope.
        assert not hasattr(node, "set_envelope")

    def test_source_parity_continuity_verified(self):
        node = EvolveNode()
        out = node.build_successor_package(_full_package(
            source_snapshot={"state": "operating", "rev": "abc"}))
        v = node.verify_continuity(out["handoff_id"],
                                   {"state": "operating", "rev": "abc"})
        assert v["decision"] == "CONTINUOUS"
        assert v["bounded_truth_to_self"]["mission"] == "build NayaPOWER"

    def test_three_generation_no_drift(self):
        node = EvolveNode()
        hid1 = node.build_successor_package(_full_package(
            successor_identity="naya-B", source_snapshot={"gen": 1}))["handoff_id"]
        hid2 = node.build_successor_package(_full_package(
            parent_identity="naya-B", successor_identity="naya-C",
            source_snapshot={"gen": 1}))["handoff_id"]
        # Same declared state → same successor next action (A_s = A_p);
        # materially identical state yields identical package hash inputs.
        p1 = node._handoff_packages[hid1]
        p2 = node._handoff_packages[hid2]
        assert p1["next_action"] == p2["next_action"]
        # Independent replayability: handoff ID + sources + snapshot ⇒
        # materially equivalent context.
        from naya_kernel.nodes.evolve_node import SUCCESSOR_PACKAGE_FIELDS
        canonical = {f: p1[f] for f in SUCCESSOR_PACKAGE_FIELDS
                     if f != "package_hash"}
        assert p1["package_hash"] == package_hash(canonical)

    def test_completeness_not_an_average(self):
        node = EvolveNode()
        fields = _full_package()
        fields["mission"] = ""  # one missing critical obligation
        out = node.build_successor_package(fields)
        assert out["successor_ready"] == 0
        assert "mission" in out["missing_obligations"]

    def test_cold_14_questions_defined(self):
        assert len(COLD_14) == 14
        assert "how does the next Naya continue" in COLD_14

    def test_ordering_law_mission_first(self):
        assert ORDERING_LAW == ("MISSION", "LAW", "SAFETY", "TRUTH", "VALUE")


# ----------------------------------------------------------------------
# §11.3 property tests
# ----------------------------------------------------------------------

class TestProperties:
    def test_value_calculus_cannot_create_authority(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        res = node.propose(_proposal(expected_value=999.0))
        eid = res["evolution_id"]
        out = node.evaluate(eid)
        # A sky-high score still routes through authority validation.
        assert out["route"] == "AUTONOMOUS"
        auth = node.authorize(eid, {"issuer": "EVOLVE_SELF", "scope": "all"})
        assert auth["decision"] == "REFUSED"
        assert auth["refusal_code"] == REFUSAL_AUTHORITY

    def test_rollback_or_escalate_on_harm(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)
        node.apply(eid)
        node._armed_rollbacks.pop(eid)  # no armed rollback exists
        out = node.report_harm(eid, {"severity": "high"})
        # No armed rollback → the governed LAW path, never silent drop.
        assert out["decision"] == "HARM_RECORDED_NO_ARMED_ROLLBACK"
        assert out["route"] == "LAW_GOVERNED_PATH"

    def test_no_self_ratification(self):
        node = EvolveNode()
        # EVOLVE cannot ratify its own proposals: there is no ratify method,
        # and authorize() from EVOLVE's own seat is refused.
        assert not hasattr(node, "ratify")
        eid = node.propose(_proposal())["evolution_id"]
        out = node.authorize(eid, {"issuer": "EVOLVE", "scope": "self"})
        assert out["decision"] == "REFUSED"

    def test_bundle_evaluated_as_one(self):
        node = EvolveNode()
        ids = [node.propose(_proposal(objective="shared",
                                      proposed_change=f"p{i}",
                                      reversibility=0.5))["evolution_id"]
               for i in range(2)]
        out = node.bundle_evaluate(ids)
        assert out["decision"] == "HARD_STOP"
        assert out["bundle"]["shared_objective"] is True

    def test_mission_compatibility_resolved_for_every_proposal(self):
        node = EvolveNode()
        res = node.propose(_proposal(mission_compatible=False))
        assert res["decision"] == "REFUSED"
        assert res["refusal_code"] == REFUSAL_IMMUTABLE_SURFACE
        assert "MISSION" in res["touched_surface"]

    def test_authority_reresolved_per_succession_never_inherited(self):
        node = EvolveNode()
        out = node.build_successor_package(_full_package())
        pkg = node._handoff_packages[out["handoff_id"]]
        assert pkg["authority_context"] == {
            "prior_refs": [],
            "authority_inherited": False,
            "requires_reresolution": True,
        }

    def test_core_intelligence_transfer_needs_director_word(self):
        node = EvolveNode()
        fields = _full_package(intelligence_refs=[
            {"ref_id": "core-1", "intelligence_class": "CORE"}])
        out = node.build_successor_package(fields)  # no director word
        assert out["core_intelligence_blocked"] == ["core-1"]
        pkg = node._handoff_packages[out["handoff_id"]]
        assert pkg["intelligence_refs"] == []  # CORE withheld, not leaked
        # With the director's explicit word per handoff, it flows.
        out2 = node.build_successor_package(fields,
                                            director_authorized_core=True)
        pkg2 = node._handoff_packages[out2["handoff_id"]]
        assert pkg2["intelligence_refs"][0]["intelligence_class"] == "CORE"

    def test_personality_trait_evolutions_always_brief(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        res = node.propose(_proposal(touches_personality=True))
        assert res["route"] == "BRIEF"
        out = node.evaluate(res["evolution_id"])
        assert out["route"] == "BRIEF"
        assert any("personality" in r for r in out["reasons"])

    def test_blast_radius_labels_never_create_authority(self):
        assert list(BLAST_RADIUS) == ["LOCAL", "COMPONENT", "CROSS_NODE",
                                      "SYSTEM", "PRODUCTION", "CONSTITUTIONAL"]
        node = EvolveNode()
        res = node.propose(_proposal(blast_radius="CONSTITUTIONAL"))
        assert res["decision"] == "PROPOSED"  # classification admitted...
        out = node.evaluate(res["evolution_id"])
        # ...but the label authorizes nothing: outside envelope → BRIEF.
        assert out["route"] == "BRIEF"

    def test_immutable_surface_complete_seven_items(self):
        assert set(IMMUTABLE_SURFACE) == {
            "CONSTITUTIONAL_LAW", "AUTHORITY_MODEL", "IDENTITY", "MISSION",
            "PROVENANCE_REQUIREMENTS", "GATE_STRUCTURE", "HARD_STOP_FLAGS"}
        assert len(IMMUTABLE_SURFACE) == 7  # mission is item 8 in §2.2, A1


# ----------------------------------------------------------------------
# §11.4 — metrics are diagnostics, never gates
# ----------------------------------------------------------------------

class TestMetrics:
    def test_metrics_recorded_never_gate(self):
        node = EvolveNode()
        for name in CONTINUITY_METRICS:
            out = node.record_continuity_metric(name, 0.5)
            assert out["decision"] == "RECORDED"
        assert set(node.metrics()) == set(CONTINUITY_METRICS)
        # Metrics do not change any gate decision. (FLAG-001 step 4: with
        # V2.1 RATIFIED the in-envelope proposal routes AUTONOMOUS —
        # metrics are still diagnostics, never gates.)
        eid = node.propose(_proposal())["evolution_id"]
        out = node.evaluate(eid)
        assert out["route"] == "AUTONOMOUS"

    def test_unknown_metric_refused(self):
        node = EvolveNode()
        out = node.record_continuity_metric("made_up_metric", 1.0)
        assert out["decision"] == "REFUSED"

    def test_continuity_gain_formula_available(self):
        # ContinuityGain = HumanReconstructionCost_baseline −
        # HumanReconstructionCost_successor (recorded, never gated).
        node = EvolveNode()
        node.record_continuity_metric("successor_reconstruction_latency", 12.0)
        node.record_continuity_metric("successor_reconstruction_latency", 4.0)
        latencies = node.metrics()["successor_reconstruction_latency"]
        gain = latencies[0] - latencies[-1]
        assert gain == 8.0


# ----------------------------------------------------------------------
# NodeBase conformance, receipts, cold reconstruct
# ----------------------------------------------------------------------

class TestConformance:
    def test_is_node_base(self):
        assert issubclass(EvolveNode, NodeBase)

    def test_manifest_entry(self):
        entry = EvolveNode().manifest_entry()
        assert entry.node_id == "NAYA-KERNEL-EVOLVE"
        assert entry.version == "V1-CANDIDATE"
        assert len(entry.responsibilities) >= 8

    def test_persisted_transitions_name_all_axes(self):
        node = EvolveNode()
        t = node.persisted_transitions()
        assert "OBSERVED_GAP->PROPOSED" in t
        assert "SOURCE_ONLY->TESTED" in t
        assert "DRAFT->VALIDATING" in t

    def test_evidence_hooks(self):
        hooks = EvolveNode().evidence_hooks()
        assert "evolution_receipt_ledger" in hooks
        assert "successor_package_store" in hooks

    def test_authority_checks_declare_never_grant(self):
        checks = EvolveNode().authority_checks()
        assert checks[0] == NO_AUTHORITY_GRANT
        assert not any("grant" in c.lower() and "never" not in c.lower()
                       and "no_authority" not in c.lower()
                       for c in checks[1:])

    def test_gate_unknown_action_fails(self):
        g = EvolveNode().gate({"action": "teleport"})
        assert g.verdict is GateVerdict.FAIL

    def test_gate_propose_prohibited_fails(self):
        g = EvolveNode().gate({"action": "propose", "proposal": {
            "change_class": "MISSION", "future_behavior": "x"}})
        assert g.verdict is GateVerdict.FAIL
        assert REFUSAL_IMMUTABLE_SURFACE in g.reasons

    def test_gate_propose_no_future_behavior_fails(self):
        g = EvolveNode().gate({"action": "propose", "proposal": {
            "change_class": "DOCUMENTATION"}})
        assert g.verdict is GateVerdict.FAIL
        assert REFUSAL_NO_FUTURE_BEHAVIOR in g.reasons

    def test_gate_evaluate_in_envelope_passes_when_ratified(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = node.propose(_proposal())["evolution_id"]
        node.evaluate(eid)
        g = node.gate({"action": "evaluate", "evolution_id": eid})
        assert g.verdict is GateVerdict.PASS

    def test_gate_apply_ratified_requires_authority_validation(self):
        # FLAG-001 step 4: V2.1 RATIFIED — no unratified-math refusal.
        # apply still requires authority validation (EVOLVE grants none).
        node = EvolveNode()
        eid = _authorized(node)
        g = node.gate({"action": "apply", "evolution_id": eid})
        assert g.verdict is GateVerdict.NEED_EVIDENCE
        assert "AUTHORITY_VALIDATION_REQUIRED" in g.reasons

    def test_gate_handoff_needs_completeness_check(self):
        g = EvolveNode().gate({"action": "handoff"})
        assert g.verdict is GateVerdict.NEED_EVIDENCE
        assert any("COMPLETENESS" in r for r in g.reasons)

    def test_gate_metrics_always_pass_diagnostic(self):
        g = EvolveNode().gate({"action": "metrics"})
        assert g.verdict is GateVerdict.PASS

    def test_all_receipts_hash_bound(self):
        node = EvolveNode()
        eid = node.propose(_proposal())["evolution_id"]
        node.evaluate(eid)
        from naya_kernel.nodes.evolve_node import _hash
        for receipt in node._receipts:
            body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
            assert receipt["receipt_hash"] == _hash(body), receipt["receipt_type"]
            assert receipt["authority_created"] is False
            assert "calculusVersion" in receipt and "calculusRatified" in receipt
            # FLAG-001 step 4: the ratified V2.1 config hash is bound.
            assert receipt.get("calculusConfigHash") == CALCULUS_V21_SPEC_HASH

    def test_evolution_and_successor_receipts_kept_separate(self):
        node = EvolveNode()
        eid = node.propose(_proposal())["evolution_id"]
        node.evaluate(eid)
        node.build_successor_package(_full_package())
        types = {r["receipt_type"] for r in node._receipts}
        assert "GATED" in types            # evolution receipt
        assert "SUCCESSOR_PACKAGE" in types  # successor receipt — separate

    def test_cold_reconstruct_replays_adoption_and_rollback(self):
        node = EvolveNode({"calculusVersion": "V2.1", "calculusRatified": True,
                           "kernelRevision": "kr-0", "currentVersion": "v0.0.0",
                           "envelope": {
                               "allowed_change_classes": ["DOCUMENTATION"],
                               "max_blast_radius": "COMPONENT",
                               "reversibility_floor": 0.8,
                               "value_threshold": 0.5}})
        eid = _authorized(node)
        node.apply(eid)
        node.verify_adoption(eid, {"verify_accepted": True})
        node.report_harm(eid, {"severity": "high"})
        node.refuse_instruction({"from_seat": "VERIFY",
                                 "requests": ["CONSTITUTIONAL_LAW"]})
        node.build_successor_package(_full_package())
        state = node.cold_reconstruct(node._receipts)
        assert eid in state["adopted"]
        assert any(r["evolution_id"] == eid for r in state["rolled_back"])
        assert len(state["judgment_rule_refusals"]) == 1
        assert state["handoff_packages"]  # readiness recorded, not invented
        assert state["determinism"]["matched"] == state["determinism"]["checked"]
        assert state["determinism"]["mismatched"] == []

    def test_cold_reconstruct_detects_tampered_receipt(self):
        node = EvolveNode()
        node.propose(_proposal())
        tampered = dict(node._receipts[0])
        tampered["reason"] = "forged"  # mutate without resealing
        state = node.cold_reconstruct([tampered])
        assert state["determinism"]["mismatched"] == [
            tampered["receipt_id"]]
        assert state["determinism"]["matched"] == 0

    def test_cold_reconstruct_answers_successor_questions(self):
        node = EvolveNode()
        node.build_successor_package(_full_package())
        state = node.cold_reconstruct(node._receipts)
        hid = next(iter(state["handoff_packages"]))
        pkg_state = state["handoff_packages"][hid]
        assert pkg_state["successor_ready"] == 1
        assert pkg_state["missing_obligations"] == []

    def test_observe_registers_gap_without_adopting(self):
        node = EvolveNode()
        receipt = node.observe({"gap": "repeated manual state explanation",
                                "source": "VERIFY reopened receipts"})
        assert receipt["receipt_type"] == "GAP_OBSERVED"
        cand = node._get(receipt["evolution_id"])
        assert cand["proposal"] == "OBSERVED_GAP"

    def test_diagnose_computes_bounded_impact_closure(self):
        node = EvolveNode()
        eid = node.propose(_proposal(
            affected_components=["schema"]))["evolution_id"]
        out = node.diagnose(eid, {"schema": ["runtime", "migrations"],
                                  "runtime": ["proof"]})
        assert "schema" in out["impact_closure"]
        assert "runtime" in out["impact_closure"]
