"""Tests for naya_kernel.nodes.self_node (CANDIDATE implementation).

Mirrors the acceptance battery in SELF-NODE-SPEC-CANDIDATE.md §9:
valid input → READY with a complete boot receipt; every §4 refusal
condition → FAIL with the condition named; DEGRADED narrows scope;
recompute() MATCHes; cold_reconstruct() rebuilds from receipts alone.
"""
import hashlib
import json

import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes import self_node
from naya_kernel.nodes.self_node import SelfNode


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _h(obj):
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


def make_state(**overrides):
    payload = {"boot_count": 7, "owner_scope": "shawn-personal"}
    checkpoint_hash = _h(payload)
    predecessor = {
        "predecessor_hash": None,
        "checkpoint_hash": checkpoint_hash,
        "config_hash": "config-rev-9",
        "identity_binding": "bind-1",
    }
    predecessor["receipt_hash"] = _h(
        {k: v for k, v in predecessor.items() if k != "receipt_hash"})
    state = {
        "execution_id": "exec-001",
        "seen_execution_ids": [],
        "identity_claim": {"type": "NAYA"},
        "identity_binding": {
            "binding_ref": "bind-1",
            "verified": True,
            "actor_type": "NAYA",
        },
        "mission_ref": "mission:ratified-v1",
        "scope_ref": "scope:ratified-v1",
        "ratified_sources": {
            "mission:ratified-v1": {"text": "serve Shawn as Naya"},
            "scope:ratified-v1": {"actions": ["read", "summarize"]},
        },
        "owner_scope": "shawn-personal",
        "kernel_revision": "rev-9",
        "checkpoint": {
            "hash": checkpoint_hash,
            "payload": payload,
            "owner_scope": "shawn-personal",
        },
        "predecessor_receipt": predecessor,
        "known": ["mission text"],
        "unknown": [],
        "blocked": ["production database"],
    }
    state.update(overrides)
    return state


# -- interface ------------------------------------------------------------
def test_module_exposes_node_class():
    assert issubclass(SelfNode, NodeBase)


def test_manifest_entry_names_responsibilities():
    entry = SelfNode().manifest_entry()
    assert entry.node_id == "NAYA-KERNEL-SELF"
    assert entry.version == "0.1.0-candidate"
    assert len(entry.responsibilities) >= 5


def test_persisted_transitions_cover_state_machine():
    t = SelfNode().persisted_transitions()
    for name in ("UNINITIALIZED->BOOTING", "BOOTING->READY",
                 "BOOTING->DEGRADED", "BOOTING->FAILED", "boot_receipt_issued"):
        assert name in t


def test_authority_checks_grant_nothing():
    checks = SelfNode().authority_checks()
    assert checks, "SELF must declare the authority boundary it does not grant"
    # "grant" may appear only inside negations ("not_granted",
    # "no_authority_grant_*"): no check may affirm granting authority.
    for check in checks:
        negated = check.replace("not_granted", "").replace(
            "no_authority_grant_performed", "")
        assert "grant" not in negated, \
            f"authority check affirms granting: {check}"


def test_evidence_hooks_cover_sources():
    hooks = SelfNode().evidence_hooks()
    for name in ("identity_binding_registry", "ratified_source_store",
                 "checkpoint_store", "continuity_receipt_chain",
                 "boot_receipt_log"):
        assert name in hooks


# -- happy path ------------------------------------------------------------
def test_valid_boot_reaches_ready_with_complete_receipt():
    node = SelfNode()
    result = node.gate(make_state())
    assert result.verdict == GateVerdict.PASS
    receipt = node.last_boot_receipt
    assert receipt["boot_state"] == "READY"
    # §5: every required field present.
    for field in ("identityContext", "predecessor_binding_hash",
                  "checkpoint_hash", "config_hash", "mission_ref", "scope_ref",
                  "truth_boundary", "transition_log", "async_receipts",
                  "issued_at", "issued_by", "owner_scope", "receipt_hash"):
        assert field in receipt, f"boot receipt missing {field}"
    # §6: transition log UNINITIALIZED → BOOTING → READY.
    hops = [(t["before"], t["after"]) for t in receipt["transition_log"]]
    assert hops == [("UNINITIALIZED", "BOOTING"), ("BOOTING", "READY")]
    # §2: identity context handed to LAW.
    ctx = receipt["identityContext"]
    assert ctx["actor"]["authenticated"] is True
    assert ctx["actor"]["binding_ref"] == "bind-1"
    assert ctx["truth_boundary"]["blocked"] == ["production database"]
    # Receipt is hash-bound and self-consistent.
    assert SelfNode._verify_receipt_hash(receipt)
    assert ctx["boot_receipt_id"] == receipt["receipt_hash"]


def test_recompute_matches_on_valid_receipt():
    node = SelfNode()
    node.gate(make_state())
    assert node.recompute(node.last_boot_receipt) == "MATCH"


def test_recompute_mismatch_on_tampered_receipt():
    node = SelfNode()
    node.gate(make_state())
    receipt = dict(node.last_boot_receipt)
    receipt["boot_state"] = "READY"  # keep plausible, tamper the mission
    tampered_inputs = dict(receipt["inputs"])
    tampered_inputs["mission_ref"] = "mission:forged"
    receipt["inputs"] = tampered_inputs
    assert node.recompute(receipt) == "MISMATCH"


# -- §4 refusal conditions --------------------------------------------------
def test_unauthenticated_identity_refused():
    node = SelfNode()
    result = node.gate(make_state(identity_binding={
        "binding_ref": "bind-9", "verified": False, "actor_type": "NAYA"}))
    assert result.verdict == GateVerdict.FAIL
    assert "4.1" in result.reasons[0]
    assert node.last_boot_receipt["boot_state"] == "FAILED"


def test_missing_binding_refused():
    node = SelfNode()
    result = node.gate(make_state(identity_binding=None))
    assert result.verdict == GateVerdict.FAIL


def test_identity_conflict_refused():
    node = SelfNode()
    result = node.gate(make_state(identity_claim={"type": "DIRECTOR"}))
    assert result.verdict == GateVerdict.FAIL
    assert "4.2" in result.reasons[0]


def test_replayed_execution_id_refused():
    node = SelfNode()
    result = node.gate(make_state(seen_execution_ids=["exec-001"]))
    assert result.verdict == GateVerdict.FAIL
    assert "replay" in result.reasons[0].lower()


def test_missing_execution_id_refused():
    node = SelfNode()
    result = node.gate(make_state(execution_id=None))
    assert result.verdict == GateVerdict.FAIL


def test_checkpoint_hash_mismatch_refused():
    state = make_state()
    state["checkpoint"] = dict(state["checkpoint"])
    state["checkpoint"]["payload"] = {"boot_count": 999}  # tampered
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.FAIL
    assert "4.3" in result.reasons[0]


def test_checkpoint_mismatch_with_predecessor_refused():
    state = make_state()
    other_payload = {"boot_count": 1}
    state["checkpoint"] = {
        "hash": _h(other_payload),
        "payload": other_payload,
        "owner_scope": "shawn-personal",
    }
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.FAIL
    assert "4.3" in result.reasons[0]


def test_broken_chain_without_genesis_refused():
    node = SelfNode()
    result = node.gate(make_state(predecessor_receipt=None))
    assert result.verdict == GateVerdict.FAIL
    assert "4.4" in result.reasons[0]


def test_unverifiable_predecessor_receipt_refused():
    state = make_state()
    state["predecessor_receipt"] = dict(state["predecessor_receipt"])
    state["predecessor_receipt"]["receipt_hash"] = "deadbeef"
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.FAIL
    assert "4.4" in result.reasons[0]


def test_forked_chain_refused():
    state = make_state()
    r1 = dict(state["predecessor_receipt"])
    r2 = dict(state["predecessor_receipt"])
    r2["receipt_hash"] = _h({"fork": "second-successor"})
    state["receipt_chain"] = [r1, r2]
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.FAIL
    assert "fork" in result.reasons[0].lower()


def test_mid_chain_fork_refused():
    # Two distinct successors of one predecessor: a real fork, not just
    # two genesis claimants.
    root = {"predecessor_hash": None, "checkpoint_hash": "cp0",
            "config_hash": "c0"}
    root["receipt_hash"] = _h({k: v for k, v in root.items()
                               if k != "receipt_hash"})
    succ_a = {"predecessor_hash": root["receipt_hash"],
              "checkpoint_hash": "cpA", "config_hash": "c0"}
    succ_a["receipt_hash"] = _h({k: v for k, v in succ_a.items()
                                 if k != "receipt_hash"})
    succ_b = {"predecessor_hash": root["receipt_hash"],
              "checkpoint_hash": "cpB", "config_hash": "c0"}
    succ_b["receipt_hash"] = _h({k: v for k, v in succ_b.items()
                                 if k != "receipt_hash"})
    assert succ_a["receipt_hash"] != succ_b["receipt_hash"]
    state = make_state(predecessor_receipt=succ_a,
                       receipt_chain=[root, succ_a, succ_b])
    # Point the state's checkpoint at succ_a's checkpoint so the failure
    # under test is the fork, not checkpoint integrity.
    payload = {"boot_count": 7}
    state["checkpoint"] = {"hash": _h(payload), "payload": payload,
                           "owner_scope": "shawn-personal"}
    succ_a["checkpoint_hash"] = _h(payload)
    succ_a["receipt_hash"] = _h({k: v for k, v in succ_a.items()
                                 if k != "receipt_hash"})
    state["predecessor_receipt"] = succ_a
    state["receipt_chain"] = [root, succ_a, succ_b]
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.FAIL
    assert "fork" in result.reasons[0].lower()


def test_authority_inheritance_refused_not_stripped():
    node = SelfNode()
    result = node.gate(make_state(successor_package={
        "carries_authority": True, "owner_scope": "shawn-personal"}))
    assert result.verdict == GateVerdict.FAIL
    assert "4.5" in result.reasons[0]
    # Refused, not silently repaired: the package is not consumed.
    assert node.last_boot_receipt["boot_state"] == "FAILED"


@pytest.mark.parametrize("signal", [
    "name_similarity", "chat_text_possession", "browser_state",
    "timing", "object_id", "usefulness",
])
def test_excluded_identity_signals_refused(signal):
    node = SelfNode()
    result = node.gate(make_state(identity_evidence_sources=[signal]))
    assert result.verdict == GateVerdict.FAIL
    assert "4.6" in result.reasons[0]


def test_unratified_mission_refused():
    node = SelfNode()
    result = node.gate(make_state(mission_ref="mission:unratified-claim"))
    assert result.verdict == GateVerdict.FAIL
    assert "4.7" in result.reasons[0]


def test_cross_owner_checkpoint_refused():
    state = make_state()
    state["checkpoint"] = dict(state["checkpoint"])
    state["checkpoint"]["owner_scope"] = "someone-else"
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.FAIL
    assert "4.8" in result.reasons[0]


# -- DEGRADED: narrow, never widen -------------------------------------------
def test_unratified_scope_degrades_with_narrowed_scope():
    node = SelfNode()
    result = node.gate(make_state(scope_ref="scope:unratified-claim"))
    assert result.verdict == GateVerdict.PASS
    receipt = node.last_boot_receipt
    assert receipt["boot_state"] == "DEGRADED"
    assert receipt["effective_scope"]["actions"] == []
    assert any(r.startswith("DEGRADED") for r in result.reasons)


def test_ambiguous_mission_narrows_scope_without_guessing():
    node = SelfNode()
    result = node.gate(make_state(mission_ambiguous=True))
    assert result.verdict == GateVerdict.PASS
    receipt = node.last_boot_receipt
    assert receipt["boot_state"] == "DEGRADED"
    assert "mission: binding valid but mission ambiguous" in \
        receipt["truth_boundary"]["unknown"]


def test_stale_checkpoint_marked_unknown_not_current():
    state = make_state()
    state["checkpoint"] = dict(state["checkpoint"])
    state["checkpoint"]["superseded_by"] = "checkpoint:newer-hash"
    node = SelfNode()
    result = node.gate(state)
    assert result.verdict == GateVerdict.PASS
    receipt = node.last_boot_receipt
    assert receipt["boot_state"] == "READY"  # integrity holds
    assert any("superseded" in u for u in
               receipt["truth_boundary"]["unknown"])


# -- genesis ------------------------------------------------------------------
def test_ratified_genesis_boots_without_predecessor_or_checkpoint():
    node = SelfNode()
    result = node.gate(make_state(
        execution_id="genesis-1",
        predecessor_receipt=None,
        checkpoint=None,
        genesis={"ratified": True, "first_execution_id": "genesis-1"},
    ))
    assert result.verdict == GateVerdict.PASS
    assert node.last_boot_receipt["boot_state"] == "READY"
    assert node.last_boot_receipt["checkpoint_hash"] is None


def test_unratified_genesis_does_not_boot():
    node = SelfNode()
    result = node.gate(make_state(
        execution_id="genesis-1",
        predecessor_receipt=None,
        checkpoint=None,
        genesis={"ratified": False, "first_execution_id": "genesis-1"},
    ))
    assert result.verdict == GateVerdict.FAIL


# -- cold reconstruction (§8) ----------------------------------------------------
def test_cold_reconstruct_rebuilds_from_receipts_alone():
    node = SelfNode()
    node.gate(make_state())
    rebuilt = SelfNode().cold_reconstruct([node.last_boot_receipt])
    assert rebuilt["status"] == "READY"
    assert rebuilt["identity_context"]["actor"]["binding_ref"] == "bind-1"
    assert rebuilt["continuity"]["checkpoint_hash"] == \
        node.last_boot_receipt["checkpoint_hash"]
    # Deterministic: same inputs → same state.
    rebuilt2 = SelfNode().cold_reconstruct([node.last_boot_receipt])
    assert rebuilt2["status"] == rebuilt["status"]
    assert rebuilt2["identity_context"] == rebuilt["identity_context"]


def test_cold_reconstruct_fails_without_receipts():
    assert SelfNode().cold_reconstruct([])["status"] == "FAILED"


def test_cold_reconstruct_fails_on_unverifiable_receipt():
    node = SelfNode()
    node.gate(make_state())
    bad = dict(node.last_boot_receipt)
    bad["receipt_hash"] = "deadbeef"
    assert SelfNode().cold_reconstruct([bad])["status"] == "FAILED"


def test_cold_reconstruct_does_not_proceed_from_failed_boot():
    node = SelfNode()
    node.gate(make_state(identity_binding=None))
    assert node.last_boot_receipt["boot_state"] == "FAILED"
    rebuilt = SelfNode().cold_reconstruct([node.last_boot_receipt])
    assert rebuilt["status"] == "FAILED"
