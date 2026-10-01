"""LAW node acceptance battery (LAW-NODE-SPEC-CANDIDATE.md §13).

CANDIDATE — NOT RATIFIED — NOT MERGED. Tests prove the spec is
implementable against its own acceptance battery; a green suite is
"implemented candidate", never a production claim.
"""
import pytest

import re

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes.law_node import LawNode, NODE_ID, PIPELINE_POSITION

PINNED = "constitution-v1-hash"


def grant(ref="g1", grantor="DIRECTOR", grantee="ACT",
          scope=None, revoked=False, expiry=None, chain=None, tampered=False):
    return {
        "grant_ref": ref, "grantor": grantor, "grantee": grantee,
        "scope": scope if scope is not None else ["send_email"],
        "bounds": {}, "expiry": expiry, "revoked": revoked,
        "chain": chain or [], "tampered": tampered,
    }


def proposal(pid="p1", proposed_by="ACT", action_type="send_email",
             scope_tag="send_email", action_class="routine",
             grant_ref="g1", grantor="DIRECTOR",
             flags=None, new_material_facts=False,
             constitution_hash=PINNED, **action_extra):
    p = {
        "proposalId": pid,
        "intent": "test intent",
        "action": {"type": action_type, "scope_tag": scope_tag,
                   "action_class": action_class, "targets": ["a@example.com"],
                   "bounds": {"max": 1}},
        "proposedBy": proposed_by,
        "authorityClaim": None if grant_ref is None
        else {"grant_ref": grant_ref, "grantor": grantor},
        "evidenceRefs": ["e1"],
        "stakes": "low",
        "reversibility": 8,
        "identityContext": {},
        "constitutionHash": constitution_hash,
        "flags": flags or {},
        "material_facts_version": 1,
    }
    if new_material_facts:
        p["new_material_facts"] = True
        p["material_facts_version"] = 2
    p["action"].update(action_extra)
    return p


def state(prop, grants=None, n=5, confidence=0.9, floor_k=3,
          seen=None, store=None):
    return {
        "proposal": prop,
        "constitution_store": store if store is not None else {
            "pinned_hash": PINNED, "corpus": {PINNED: "ratified text"},
            "reachable": True},
        "grants": grants if grants is not None else [grant()],
        "evidence": {"n": n, "confidence": confidence},
        "evidence_floor_k": floor_k,
        "seen_proposal_hashes": seen or {},
    }


def gate_of(result):
    # apply_transition prepends lineage frames ("GRANT_ARRIVED",
    # "lineage=p1") ahead of the "LAW <GATE>:" verdict line, so scan all
    # reasons and take the LAST "LAW <GATE>" occurrence.
    matches = re.findall(
        r"LAW (ADMISSIBLE|NEEDS_AUTHORITY|NEEDS_EVIDENCE|PROHIBITED|"
        r"INTAKE_REFUSED)", " ".join(result.reasons))
    return matches[-1]


# --- interface -------------------------------------------------------------
def test_module_exposes_node_class():
    assert issubclass(LawNode, NodeBase)


def test_manifest_entry_names_node():
    entry = LawNode().manifest_entry()
    assert entry.node_id == NODE_ID
    assert PIPELINE_POSITION == 2
    assert len(entry.responsibilities) >= 5


# §13.1 lawful, authorized, evidenced -> ADMISSIBLE with bounded envelope
def test_admissible_lawful_authorized_evidenced():
    node = LawNode()
    result = node.gate(state(proposal()))
    assert result.verdict == GateVerdict.PASS
    assert gate_of(result) == "ADMISSIBLE"
    env = node.last_receipt["envelope"]
    assert env["action"] == "send_email"
    assert env["targets"] == ["a@example.com"]
    assert node.last_receipt["authority_basis"] is not None


# precedence: PROHIBITED fires before the authority check is consulted — a
# valid grant does not move a hard-stop proposal
def test_precedence_prohibited_before_authority():
    node = LawNode()
    p = proposal(flags={"harm_flag": True, "harm_facts": ["x"]})
    result = node.gate(state(p, grants=[grant()]))  # grant is valid here
    assert gate_of(result) == "PROHIBITED"


# §13.2 LAW_OF_ONE beats a director grant; receipt names the harm facts
def test_law_of_one_beats_director_grant():
    node = LawNode()
    p = proposal(flags={"harm_flag": True,
                        "harm_facts": ["targeting a person's inbox with threats"]})
    result = node.gate(state(p, grants=[grant(ref="gd", grantor="DIRECTOR",
                                              grantee="ACT", scope=["*"])]))
    assert result.verdict == GateVerdict.FAIL
    assert gate_of(result) == "PROHIBITED"
    stops = node.last_receipt["hard_stops_fired"]
    assert stops[0]["hard_stop"] == "LAW_OF_ONE"
    assert "targeting a person's inbox with threats" in \
        stops[0]["triggering_facts"][0]


# §13.3 known-wrong instruction from the director is refused with evidence
# and a lawful alternative proposed
def test_judgment_rule_refuses_director_known_wrong():
    node = LawNode()
    p = proposal(proposed_by="DIRECTOR", grant_ref="gd",
                 flags={"known_wrong_flag": True,
                        "known_wrong_facts": ["premise contradicted by e1"]})
    g = grant(ref="gd", grantor="DIRECTOR", grantee="DIRECTOR")
    result = node.gate(state(p, grants=[g]))
    assert gate_of(result) == "PROHIBITED"
    reasons = " ".join(node.last_receipt["reasons"])
    assert "I was told to" in reasons
    assert node.last_receipt["lawful_alternative"] is not None


# tau-zero classes: physical harm is never grantable
def test_tau_zero_physical_harm_not_grantable():
    node = LawNode()
    p = proposal(action_class="physical_harm", action_type="strike",
                 scope_tag="strike")
    result = node.gate(state(p, grants=[grant(ref="gd", grantor="DIRECTOR",
                                              grantee="ACT", scope=["*"])]))
    assert gate_of(result) == "PROHIBITED"
    assert node.last_receipt["hard_stops_fired"][0]["hard_stop"] == "TAU_ZERO"


# §13.4 forged authority claim is PROHIBITED and surfaced
def test_forged_grant_ref_is_prohibited_and_surfaced():
    node = LawNode()
    p = proposal(grant_ref="ghost-grant")
    result = node.gate(state(p, grants=[]))
    assert gate_of(result) == "PROHIBITED"
    stops = node.last_receipt["hard_stops_fired"]
    assert stops[0]["hard_stop"] == "AUTHORITY_FORGERY"


def test_tampered_proposal_hash_is_forgery():
    node = LawNode()
    s = state(proposal())
    s["proposal_hash_claimed"] = "deadbeef"
    result = node.gate(s)
    assert gate_of(result) == "PROHIBITED"
    assert node.last_receipt["hard_stops_fired"][0]["hard_stop"] == \
        "AUTHORITY_FORGERY"


# self-generated authority is invalid (Art. V.6) -> NEEDS_AUTHORITY, not forgery
def test_self_generated_authority_invalid_not_forgery():
    node = LawNode()
    g = grant(ref="self", grantor="ACT", grantee="ACT", chain=[])
    result = node.gate(state(proposal(grant_ref="self", grantor="ACT"),
                             grants=[g]))
    assert gate_of(result) == "NEEDS_AUTHORITY"
    assert node.last_receipt["hard_stops_fired"] == []


def test_revoked_or_expired_grant_needs_authority():
    node = LawNode()
    g = grant(ref="rev", revoked=True)
    result = node.gate(state(proposal(grant_ref="rev"), grants=[g]))
    assert gate_of(result) == "NEEDS_AUTHORITY"


def test_grant_scope_mismatch_needs_authority():
    node = LawNode()
    g = grant(ref="narrow", scope=["read_only"])
    result = node.gate(state(proposal(grant_ref="narrow"), grants=[g]))
    assert gate_of(result) == "NEEDS_AUTHORITY"


# §13.5 NEEDS_AUTHORITY flips to ADMISSIBLE only on a validated grant
def test_grant_arrival_transitions_to_admissible():
    node = LawNode()
    # a valid but out-of-scope grant: invalid-but-not-forged -> NEEDS_AUTHORITY
    narrow = grant(ref="narrow", scope=["read_only"])
    r1 = node.gate(state(proposal(grant_ref="narrow"), grants=[narrow]))
    assert gate_of(r1) == "NEEDS_AUTHORITY"
    s2 = state(proposal(grant_ref="g1"), grants=[grant()])
    r2 = node.apply_transition(s2, "GRANT_ARRIVED")
    assert gate_of(r2) == "ADMISSIBLE"
    assert "GRANT_ARRIVED" in r2.reasons[0]


def test_terminal_prohibited_cannot_reopen():
    node = LawNode()
    p = proposal(flags={"harm_flag": True})
    r1 = node.gate(state(p))
    assert gate_of(r1) == "PROHIBITED"
    r2 = node.apply_transition(state(proposal(), grants=[grant()]),
                               "GRANT_ARRIVED")
    assert r2.verdict == GateVerdict.FAIL
    assert node.last_receipt["gate"] == "PROHIBITED"  # state unchanged


# evidence floor
def test_needs_evidence_then_floor_met():
    node = LawNode()
    r1 = node.gate(state(proposal(), n=1, confidence=0.9))
    assert gate_of(r1) == "NEEDS_EVIDENCE"
    r2 = node.apply_transition(state(proposal(), n=5, confidence=0.9),
                               "EVIDENCE_FLOOR_MET")
    assert gate_of(r2) == "ADMISSIBLE"


# §10.1 intake refusal
def test_intake_refusal_missing_proposed_by():
    node = LawNode()
    p = proposal()
    del p["proposedBy"]
    result = node.gate(state(p))
    assert result.verdict == GateVerdict.FAIL
    assert node.last_receipt["gate"] == "INTAKE_REFUSED"


# §13.6 LAW unreachable / constitution store corrupt -> halt, nothing executes
def test_evaluation_incomplete_halts_pipeline():
    node = LawNode()
    s = state(proposal(), store={"pinned_hash": PINNED, "corpus": {},
                                 "reachable": False})
    result = node.gate(s)
    assert gate_of(result) == "PROHIBITED"
    assert node.last_receipt["halt_pipeline"] is True
    assert "EVALUATION_INCOMPLETE" in " ".join(node.last_receipt["reasons"])


# §13.7 a refused bundle resubmitted as pieces is caught as one
def test_bundle_split_caught_as_one():
    node = LawNode()
    bad_piece = proposal(pid="piece-b",
                         flags={"harm_flag": True, "harm_facts": ["z"]})
    good_piece = proposal(pid="piece-a")
    bundled = proposal(pid="bundle")
    bundled["bundle_of"] = [good_piece, bad_piece]
    result = node.gate(state(bundled))
    assert gate_of(result) == "PROHIBITED"
    assert "bundle rule" in " ".join(node.last_receipt["reasons"])


# §13.8 ACT execution outside its envelope is detected as a violation
def test_envelope_violation_detected():
    node = LawNode()
    node.gate(state(proposal()))
    ok = node.detect_envelope_violation(
        {"proposal_id": "p1", "action": "send_email",
         "targets": ["a@example.com"], "bounds": {"max": 1}})
    assert ok["violation"] is False
    bad = node.detect_envelope_violation(
        {"proposal_id": "p1", "action": "send_email",
         "targets": ["boss@example.com"], "bounds": {"max": 1}})
    assert bad["violation"] is True
    assert "constitutional violation" in bad["reason"]


# §13.9 cold successor recomputes a historical verdict to MATCH
def test_recompute_match():
    node = LawNode()
    node.gate(state(proposal()))
    assert node.recompute(node.last_receipt) == "MATCH"


def test_recompute_mismatch_on_tampered_receipt():
    node = LawNode()
    node.gate(state(proposal()))
    tampered = dict(node.last_receipt)
    tampered["gate"] = "PROHIBITED"
    assert node.recompute(tampered) == "MISMATCH"


# §13.10 EVOLVE candidate touching hard-stop flags is caught (defense in depth)
def test_gate_redesign_smuggling_caught():
    node = LawNode()
    p = proposal(pid="ev-1", proposed_by="EVOLVE",
                 action_type="disable_hard_stop", scope_tag="hard_stops")
    g = grant(ref="ev", grantor="DIRECTOR", grantee="EVOLVE", scope=["*"])
    result = node.gate(state(p, grants=[g]))
    assert gate_of(result) == "PROHIBITED"
    assert "GATE_REDESIGN" in " ".join(node.last_receipt["reasons"])


# §13.11 resubmission without new facts is refused as RESUBMISSION
def test_verdict_shopping_refused():
    node = LawNode()
    p = proposal(pid="rs", flags={"harm_flag": True})
    r1 = node.gate(state(p))
    assert gate_of(r1) == "PROHIBITED"
    # same proposal content, new id, no new facts -> the node's own
    # shopping registry (content identity, excludes proposalId) fires
    p2 = proposal(pid="rs2", flags={"harm_flag": True})
    r2 = node.gate(state(p2))
    assert gate_of(r2) == "PROHIBITED"
    assert "RESUBMISSION" in " ".join(node.last_receipt["reasons"])


def test_resubmission_with_new_facts_is_fresh():
    node = LawNode()
    p = proposal(pid="rs", flags={"harm_flag": True})
    r1 = node.gate(state(p))
    assert gate_of(r1) == "PROHIBITED"
    # honestly versioned new facts: not shopping — though the new facts
    # here do not clear the harm flag, so it is still PROHIBITED, just
    # not as RESUBMISSION
    p2 = proposal(pid="rs3", flags={"harm_flag": True}, new_material_facts=True)
    r2 = node.gate(state(p2))
    assert gate_of(r2) == "PROHIBITED"
    assert "RESUBMISSION" not in " ".join(node.last_receipt["reasons"])


# determinism: same proposal + constitution + grants -> same verdict
def test_deterministic_verdicts():
    s1, s2 = state(proposal()), state(proposal())
    r1, r2 = LawNode().gate(s1), LawNode().gate(s2)
    assert r1.verdict == r2.verdict
    assert r1.reasons[0] == r2.reasons[0]


# constitution skew: evaluated under the pinned version, skew receipted
def test_constitution_skew_reevaluated_under_pinned():
    node = LawNode()
    p = proposal(constitution_hash="stale-hash")
    result = node.gate(state(p))
    assert gate_of(result) == "ADMISSIBLE"
    assert node.last_receipt["constitution_skew"] is True


# authority_checks declare validations; LAW never grants
def test_authority_checks_never_grant():
    checks = LawNode().authority_checks()
    assert "no_authority_grant_performed" in checks
    assert not any("grant_authority" in c for c in checks)
