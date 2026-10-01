"""Tests for NAYA-KERNEL-CONNECT (CANDIDATE — NOT RATIFIED — NOT MERGED).

Mirrors the spec §14 acceptance battery: valid input reaches the intended
state; malformed input rejected; missing deps block; identity/authority
mismatch blocks with authority never created; provenance loss detected;
terminal states explicit; replay safe; receipts hashable; real invocation;
behavioral influence measured; independent verification; cold
reconstruction; leakage refused; revocation halts; door rule refused.
"""
import copy

import pytest

from naya_kernel.node_base import GateVerdict, NodeBase
from naya_kernel.nodes import connect_node
from naya_kernel.nodes.connect_node import ConnectNode

NOW = "2026-10-01T04:00:00+00:00"
FUTURE = "2999-01-01T00:00:00+00:00"
PAST = "2026-01-01T00:00:00+00:00"

BINDINGS = {
    "naya": {"authenticated": True, "owner_scope": "shawn-scope",
             "binding_ref": "b-naya"},
    "agent-y": {"authenticated": True, "owner_scope": "other-scope",
                "binding_ref": "b-y"},
    "agent-z": {"authenticated": True, "owner_scope": "shawn-scope",
                "binding_ref": "b-z"},
    "ghost": {"authenticated": False, "owner_scope": "shawn-scope",
              "binding_ref": "b-ghost"},
}

EVIDENCE = {"ev-1": {"content_hash": "abc123", "valid": True},
            "ev-2": {"content_hash": "def456", "valid": True},
            "ev-bad": {"content_hash": "zzz", "valid": False}}

POLICY = {"version": "v1", "forbidden_classes": [], "strictness": 1}


def make_consent(consent_id, party, purpose, expires_at=FUTURE,
                 revoked=False):
    body = {"consent_id": consent_id, "party": party, "purpose": purpose,
            "scope": ["reports", "facts"], "expires_at": expires_at,
            "revoked": revoked, "revocable": True}
    body["consent_hash"] = connect_node._sha256(
        {k: v for k, v in body.items() if k != "consent_hash"})
    return body


def make_registry(consents):
    return {c["consent_id"]: c for c in consents}


def make_context(consent_registry, now=NOW, evidence=EVIDENCE,
                 policy=POLICY, bindings=BINDINGS):
    return {"consent_registry": consent_registry,
            "identity_bindings": copy.deepcopy(bindings),
            "evidence_registry": copy.deepcopy(evidence),
            "boundary_policy": copy.deepcopy(policy),
            "now": now}


def make_edge_request(rid="conn-1", purpose="research", classes=("reports",),
                      parties=("naya",), kind="GRAPH_EDGE",
                      consent_refs=None, evidence_refs=("ev-1",),
                      ladder="SHARED"):
    party_list = [{"identity": p, "owner_scope": BINDINGS[p]["owner_scope"],
                   "role": "peer"} for p in parties]
    scope = [{"owner_scope": BINDINGS[p]["owner_scope"],
              "content_classes": list(classes)} for p in parties]
    if consent_refs is None:
        consent_refs = [f"consent-{p}" for p in parties]
    return {"id": rid, "kind": kind, "parties": party_list,
            "purpose": purpose, "scope": scope,
            "consentRefs": list(consent_refs),
            "evidenceRefs": list(evidence_refs),
            "boundaryPolicy": copy.deepcopy(POLICY),
            "expiresAt": None, "reversibility": 8.0,
            "consentLadder": ladder}


def make_consents(purpose="research", parties=("naya",)):
    return make_registry(
        [make_consent(f"consent-{p}", p, purpose) for p in parties])


@pytest.fixture()
def node():
    return ConnectNode()


# --- §14 battery ------------------------------------------------------

def test_01_valid_input_reaches_active(node):
    ctx = make_context(make_consents())
    result = node.propose(make_edge_request(), ctx, execution_id="t01")
    assert result["verdict"] == "ACTIVE"
    assert node.connections["conn-1"]["state"] == "ACTIVE"
    receipt = result["receipt"]
    assert receipt["node_id"] == connect_node.NODE_ID
    assert receipt["payload"]["connection_id"] == "conn-1"


def test_02_malformed_input_rejected(node):
    ctx = make_context(make_consents())
    request = make_edge_request()
    del request["kind"]
    result = node.propose(request, ctx, execution_id="t02")
    assert result["verdict"] == "REJECTED"
    assert any("E_MALFORMED" in r for r in result["reasons"])
    empty = make_edge_request(parties=())
    result = node.propose(empty, ctx, execution_id="t02b")
    assert result["verdict"] == "REJECTED"


def test_03_missing_consent_blocks_safely(node):
    ctx = make_context(make_consents())
    # Empty consentRefs is malformed intake (required field empty).
    request = make_edge_request(consent_refs=[])
    result = node.propose(request, ctx, execution_id="t03")
    assert result["verdict"] == "REJECTED"
    assert any("E_MALFORMED" in r for r in result["reasons"])
    # Unresolvable refs are §4.2 missing consent (PROHIBITED, not malformed).
    request = make_edge_request(consent_refs=["consent-nobody"])
    result = node.propose(request, ctx, execution_id="t03e")
    assert result["verdict"] == "REJECTED"
    assert any("E_CONSENT_MISSING" in r for r in result["reasons"])


def test_03b_expired_consent_blocks(node):
    registry = make_registry(
        [make_consent("consent-naya", "naya", "research",
                      expires_at=PAST)])
    ctx = make_context(registry)
    result = node.propose(make_edge_request(), ctx, execution_id="t03b")
    assert result["verdict"] == "REJECTED"
    assert any("expired" in r for r in result["reasons"])


def test_03c_forged_consent_blocks(node):
    consent = make_consent("consent-naya", "naya", "research")
    consent["consent_hash"] = "forged" + "0" * 58
    ctx = make_context(make_registry([consent]))
    result = node.propose(make_edge_request(), ctx, execution_id="t03c")
    assert result["verdict"] == "REJECTED"
    assert any("hash mismatch" in r for r in result["reasons"])


def test_03d_purpose_mismatched_consent_blocks(node):
    consent = make_consent("consent-naya", "naya", "other-purpose")
    ctx = make_context(make_registry([consent]))
    result = node.propose(make_edge_request(), ctx, execution_id="t03d")
    assert result["verdict"] == "REJECTED"
    assert any("purpose mismatch" in r for r in result["reasons"])


def test_04_unauthenticated_identity_blocks(node):
    ctx = make_context(make_consents(parties=("ghost",)))
    request = make_edge_request(parties=("ghost",),
                                consent_refs=["consent-ghost"])
    result = node.propose(request, ctx, execution_id="t04")
    assert result["verdict"] == "REJECTED"
    assert any("E_UNAUTHENTICATED_IDENTITY" in r for r in result["reasons"])


def test_05_authority_never_created_or_transmitted(node):
    ctx = make_context(make_consents())
    request = make_edge_request()
    request["carry_authority"] = True
    result = node.propose(request, ctx, execution_id="t05a")
    assert result["verdict"] == "REJECTED"
    assert any("E_AUTHORITY_SMUGGLING" in r for r in result["reasons"])

    request = make_edge_request(classes=("permissions",))
    result = node.propose(request, ctx, execution_id="t05b")
    assert result["verdict"] == "REJECTED"
    assert any("E_AUTHORITY_SMUGGLING" in r for r in result["reasons"])

    request = make_edge_request(purpose="bypass the law gate for speed")
    result = node.propose(request, ctx, execution_id="t05c")
    assert result["verdict"] == "REJECTED"
    assert any("E_AUTHORITY_SMUGGLING" in r for r in result["reasons"])


def test_05b_authority_checks_declare_only(node):
    checks = node.authority_checks()
    assert isinstance(checks, list) and checks
    joined = " ".join(checks).lower()
    # Declares validations only — no grant/inference/expansion language.
    assert "no authority grant" in joined
    assert "declared only" in joined


def test_06_provenance_loss_detected(node):
    ctx = make_context(make_consents())
    result = node.propose(make_edge_request(), ctx, execution_id="t06")
    receipt = copy.deepcopy(result["receipt"])
    receipt["payload"]["purpose"] = "forged-purpose"
    assert node.recompute(receipt) == "MISMATCH"
    fresh = result["receipt"]
    assert node.recompute(fresh) == "MATCH"


def test_07_revoked_connection_invisible_to_selector(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="t07")
    assert node.retrieve("conn-1") is not None
    node.revoke("conn-1", "consent revoked", "t07-revoke", now=NOW)
    assert node.retrieve("conn-1") is None  # selector sees nothing
    # ...but lineage remains visible as evidence.
    lineage = node.lineage("conn-1")
    assert lineage["state"] == "REVOKED"
    assert lineage["transitions"]


def test_08_duplicate_execution_is_safe(node):
    ctx = make_context(make_consents())
    first = node.propose(make_edge_request(), ctx, execution_id="t08")
    second = node.propose(make_edge_request(), ctx, execution_id="t08")
    assert second["replayed"] is True
    assert first["receipt"]["receipt_hash"] == \
        second["receipt"]["receipt_hash"]
    establish = [r for r in node.ledger
                 if r.get("execution_id") == "t08"
                 and r.get("receipt_kind") == "establish"]
    assert len(establish) == 1


def test_09_receipt_complete_hashable_rederivable(node):
    ctx = make_context(make_consents())
    result = node.propose(make_edge_request(), ctx, execution_id="t09")
    receipt = result["receipt"]
    assert connect_node.ConnectNode._verify_receipt_hash(receipt)
    payload = receipt["payload"]
    for field in ("connection_id", "kind", "parties", "consent_refs",
                  "purpose", "scope", "consent_ladder", "boundary_policy",
                  "evidence_refs", "calculus", "authority_basis",
                  "lease_expiry", "reversibility", "edge", "transitions"):
        assert field in payload, field


def test_10_nodebase_conformance():
    assert issubclass(ConnectNode, NodeBase)
    node = ConnectNode()
    entry = node.manifest_entry()
    assert entry.node_id == connect_node.NODE_ID
    assert node.persisted_transitions()
    assert node.evidence_hooks()
    assert node.authority_checks()
    assert node.cold_reconstruct([])["connections"] == {}


def test_11_connection_changes_visible_context(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="t11")
    visible = node.applicable_context(
        "conn-1", {"content_class": "reports"})["visible"]
    assert visible, "ACTIVE connection must change what ACT can see"
    node.revoke("conn-1", "revoked", "t11-revoke", now=NOW)
    after = node.applicable_context(
        "conn-1", {"content_class": "reports"})["visible"]
    assert after == [], "revocation must remove the context (measured)"


def test_12_independent_verification(node):
    ctx = make_context(make_consents())
    result = node.propose(make_edge_request(), ctx, execution_id="t12")
    # A party other than the connecting instance verifies the receipt.
    verifier = ConnectNode()
    assert verifier.recompute(result["receipt"]) == "MATCH"
    tampered = copy.deepcopy(result["receipt"])
    tampered["payload"]["scope"] = []
    assert verifier.recompute(tampered) == "MISMATCH"


def test_13_cold_successor_reconstructs(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(rid="c-1"), ctx, execution_id="t13a")
    node.propose(make_edge_request(rid="c-2"), ctx, execution_id="t13b")
    node.share("c-1", {"content_class": "reports", "content_hash": "h1",
                       "purpose": "research", "owner_scope": "shawn-scope",
                       "from_party": "naya", "to_party": "naya", "at": NOW},
               "t13-share", consent_registry=ctx["consent_registry"])
    bad = make_edge_request(rid="c-3")
    bad["carry_authority"] = True
    node.propose(bad, ctx, execution_id="t13c")
    forged = copy.deepcopy(node.ledger[-1])
    forged["payload"]["connection_id"] = "forged"
    receipts = node.ledger + [forged]

    cold = ConnectNode()
    view = cold.cold_reconstruct(receipts)
    assert set(view["connections"]) == {"c-1", "c-2"}
    assert view["connections"]["c-1"]["state"] == "ACTIVE"
    assert len(view["what_crossed"]) == 1
    assert view["what_crossed"][0]["content_hash"] == "h1"
    assert any(r["connection_id"] == "c-3" for r in view["refusals"])
    assert view["policy_history"], "policy at any point must be recoverable"
    assert view["forged_receipts_skipped"] == 1


def test_14_cross_owner_leakage_refused(node):
    # Both parties consented, but the scope reaches into other-scope's
    # private classes without that owner's consent (confused deputy).
    registry = make_consents(parties=("naya", "agent-z"))
    ctx = make_context(registry)
    request = make_edge_request(
        rid="leak-1", parties=("naya", "agent-z"),
        classes=("reports", "private-notes"))
    request["scope"].append({"owner_scope": "other-scope",
                             "content_classes": ["private-notes"]})
    result = node.propose(request, ctx, execution_id="t14")
    assert result["verdict"] == "REJECTED"
    assert any("E_CROSS_OWNER_LEAKAGE" in r for r in result["reasons"])


def test_14b_majority_cannot_move_anothers_context(node):
    registry = make_consents(parties=("naya", "agent-y"))
    ctx = make_context(registry)
    request = make_edge_request(
        rid="leak-2", parties=("naya", "agent-y"), ladder="PUBLIC")
    result = node.propose(request, ctx, execution_id="t14b")
    assert result["verdict"] == "REJECTED"
    assert any("cannot consent on behalf of another mind" in r
               for r in result["reasons"])


def test_15_consent_revocation_halts_sharing(node):
    registry = make_consents()
    ctx = make_context(registry)
    node.propose(make_edge_request(), ctx, execution_id="t15")
    share_ok = node.share(
        "conn-1", {"content_class": "reports", "content_hash": "h1",
                   "purpose": "research", "owner_scope": "shawn-scope",
                   "from_party": "naya", "to_party": "naya", "at": NOW},
        "t15-share-ok", consent_registry=registry)
    assert share_ok["verdict"] == "SHARED"
    # Consent is revoked; the next crossing is a violation, not a share.
    registry["consent-naya"]["revoked"] = True
    share_bad = node.share(
        "conn-1", {"content_class": "reports", "content_hash": "h2",
                   "purpose": "research", "owner_scope": "shawn-scope",
                   "from_party": "naya", "to_party": "naya", "at": NOW},
        "t15-share-bad", consent_registry=registry)
    assert share_bad["verdict"] == "VIOLATION"
    assert share_bad["code"] == "E_CONSENT_MISSING"
    # Revoking the connection marks derived edges STALE; the manifest of
    # what crossed is handed to the revoking party's VERIFY.
    result = node.revoke("conn-1", "consent revoked", "t15-revoke", now=NOW)
    assert result["verdict"] == "REVOKED"
    assert node.edge_ledger["conn-1"]["epistemic_state"] == "STALE"
    manifest = result["receipt"]["payload"]["manifest_for_verify"]
    assert manifest and manifest[0]["content_hash"] == "h1"


def test_16_door_rule_violation_refused(node):
    ctx = make_context(make_consents())
    request = make_edge_request(rid="door-1", kind="INTERFACE_OPEN")
    request["door_proposal"] = {
        "improves": "faster access", "for_whom": "agents",
        "state_kept": ["canonical_memory"],  # competing source of truth
        "governance": "charter v1",
    }
    result = node.propose(request, ctx, execution_id="t16")
    assert result["verdict"] == "REJECTED"
    assert any("E_DOOR_RULE" in r for r in result["reasons"])


def test_16b_valid_door_opens(node):
    ctx = make_context(make_consents())
    request = make_edge_request(rid="door-2", kind="INTERFACE_OPEN")
    request["door_proposal"] = {
        "improves": "action latency for agents", "for_whom": "agents",
        "state_kept": ["ephemeral transport buffers"],  # not competing
        "governance": "interface charter v1",
    }
    result = node.open_interface(request, ctx, execution_id="t16b")
    assert result["verdict"] == "ACTIVE"
    assert node.interfaces["door-2"]["state"] == "OPEN"


def test_16c_interface_statefulness_creep_disconnects(node):
    node.interfaces["creepy"] = {
        "interface_id": "creepy",
        "door_proposal": {"state_kept": ["canonical_memory"]},
        "state": "OPEN",
    }
    result = node.audit_interface("creepy")
    assert result["verdict"] == "DISCONNECTED"
    assert node.interfaces["creepy"]["state"] == "DISCONNECTED"


def test_handshake_full_flow_to_active(node):
    registry = make_consents(parties=("naya", "agent-y"))
    ctx = make_context(registry)
    request = make_edge_request(rid="ml-1", parties=("naya", "agent-y"),
                                kind="MIND_LINK",
                                consent_refs=["consent-naya",
                                              "consent-agent-y"])
    started = node.propose(request, ctx, execution_id="th-1")
    assert started["verdict"] == "CONSENT_PENDING"
    assert node.connections["ml-1"]["state"] == "CONSENT_PENDING"

    node.handshake_step(
        "ml-1", "mutual_auth", {"both_authenticated": True}, "th-2")
    node.handshake_step(
        "ml-1", "policy_exchange",
        {"policy": {"version": "v2", "forbidden_classes": ["raw-dumps"],
                    "strictness": 5}}, "th-3")
    node.handshake_step("ml-1", "consent_exchange", {"receipts": 2}, "th-4")
    cap = node.handshake_step(
        "ml-1", "capability_advertisement",
        {"capabilities": ["summarize"]}, "th-5")
    assert cap["receipt"]["payload"]["steps_done"]
    node.handshake_step("ml-1", "lease_issuance",
                        {"expires_at": FUTURE}, "th-6")
    # The stricter policy governs: intersection, not union (§5.3).
    intersected = node.connections["ml-1"].get("intersected_policy")
    assert intersected["strictness"] == 5
    assert intersected["forbidden_classes"] == ["raw-dumps"]

    done = node.handshake_complete("ml-1", "th-7")
    assert done["verdict"] == "ACTIVE"
    edge = node.edge_ledger["ml-1"]
    # Cross-owner edge carries BOTH parties' scopes (§10).
    assert "other-scope" in edge["owner_scope"]
    assert "shawn-scope" in edge["owner_scope"]


def test_handshake_holds_inert_until_complete(node):
    registry = make_consents(parties=("naya", "agent-y"))
    ctx = make_context(registry)
    request = make_edge_request(rid="ml-2", parties=("naya", "agent-y"),
                                kind="MIND_LINK",
                                consent_refs=["consent-naya",
                                              "consent-agent-y"])
    result = node.propose(request, ctx, execution_id="thb-1")
    assert result["verdict"] == "CONSENT_PENDING"
    refused = node.share(
        "ml-2", {"content_class": "reports", "content_hash": "h",
                 "purpose": "research", "owner_scope": "shawn-scope",
                 "from_party": "naya", "to_party": "agent-y", "at": NOW},
        "thb-share")
    assert refused["verdict"] == "REFUSED"  # never half-trusted
    with pytest.raises(ValueError):
        node.handshake_complete("ml-2", "thb-2")


def test_half_open_handshake_fails_closed(node):
    registry = make_consents(parties=("naya", "agent-y"))
    ctx = make_context(registry)
    request = make_edge_request(rid="ml-3", parties=("naya", "agent-y"),
                                kind="MIND_LINK",
                                consent_refs=["consent-naya",
                                              "consent-agent-y"])
    node.propose(request, ctx, execution_id="thc-1")
    node.connections["ml-3"]["handshake"]["window_expires"] = PAST
    closed = node.close_stale_handshakes(now=NOW, execution_id="thc-close")
    assert len(closed) == 1
    assert node.connections["ml-3"]["state"] == "REJECTED"


def test_capability_advertisement_grants_nothing(node):
    registry = make_consents(parties=("naya",))
    ctx = make_context(registry)
    request = make_edge_request(rid="ml-4", parties=("naya",),
                                kind="MIND_LINK")
    node.propose(request, ctx, execution_id="tca-1")
    record = node.connections["ml-4"]
    result = node.handshake_step(
        "ml-4", "capability_advertisement",
        {"capabilities": ["write_scoped"]}, "tca-2")
    steps = node.connections["ml-4"]["handshake"]["steps"]
    assert steps[-1]["payload"]["grants_nothing"] is True
    assert record["state"] == "CONSENT_PENDING"


def test_purpose_drift_suspends_first(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="tpd-1")
    drift = node.share(
        "conn-1", {"content_class": "reports", "content_hash": "h1",
                   "purpose": "marketing",  # != connection purpose
                   "owner_scope": "shawn-scope",
                   "from_party": "naya", "to_party": "naya", "at": NOW},
        "tpd-share")
    assert drift["verdict"] == "SUSPENDED"
    assert drift["code"] == "E_PURPOSE_DRIFT"
    assert node.connections["conn-1"]["state"] == "SUSPENDED"
    # Confirmed drift → REVOKED.
    revoked = node.confirm_drift("conn-1", "tpd-confirm")
    assert revoked["verdict"] == "REVOKED"


def test_review_clears_suspension_without_widening(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="trv-1")
    node.suspend("conn-1", "precaution", "trv-2")
    result = node.clear_review("conn-1", "trv-3", reviewer="naya-verify")
    assert result["verdict"] == "ACTIVE"
    assert node.connections["conn-1"]["state"] == "ACTIVE"


def test_scope_narrowing_allowed_widening_refused(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(classes=("reports", "facts")),
                 ctx, execution_id="tsc-1")
    narrowed = node.narrow_scope(
        "conn-1", [{"owner_scope": "shawn-scope",
                    "content_classes": ["reports"]}], "tsc-2")
    assert narrowed["verdict"] == "SCOPE_NARROWED"
    with pytest.raises(ValueError) as excinfo:
        node.narrow_scope(
            "conn-1", [{"owner_scope": "shawn-scope",
                        "content_classes": ["reports", "raw-dumps"]}],
            "tsc-3")
    assert "widening refused" in str(excinfo.value)


def test_lease_expiry_auto_revokes(node):
    ctx = make_context(make_consents())
    request = make_edge_request()
    request["expiresAt"] = PAST
    node.propose(request, ctx, execution_id="tl-1")
    result = node.share(
        "conn-1", {"content_class": "reports", "content_hash": "h1",
                   "purpose": "research", "owner_scope": "shawn-scope",
                   "from_party": "naya", "to_party": "naya", "at": NOW},
        "tl-share")
    assert result["verdict"] == "REFUSED"
    assert node.connections["conn-1"]["state"] == "REVOKED"


def test_revocation_race_is_violation(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="trr-1")
    node.revoke("conn-1", "revoked", "trr-2", now=NOW)
    # Share in flight with a crossing timestamp after revocation.
    result = node.share(
        "conn-1", {"content_class": "reports", "content_hash": "h1",
                   "purpose": "research", "owner_scope": "shawn-scope",
                   "from_party": "naya", "to_party": "naya",
                   "at": "2999-06-01T00:00:00+00:00"},
        "trr-share")
    assert result["verdict"] in ("VIOLATION", "REFUSED")


def test_illegal_transition_fails_closed(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="tit-1")
    with pytest.raises(ValueError, match="fail closed"):
        node.apply_transition("conn-1", "PROPOSED", "backwards", "tit-2")
    with pytest.raises(KeyError, match="unknown connection"):
        node.revoke("nope", "x", "tit-3")
    # REVOKED is terminal: revoke twice fails closed.
    node.revoke("conn-1", "revoked", "tit-4", now=NOW)
    with pytest.raises(ValueError, match="fail closed"):
        node.revoke("conn-1", "again", "tit-5", now=NOW)


def test_no_evidence_refused(node):
    ctx = make_context(make_consents())
    # An invalid evidence ref is §4.1 refusal (proximity/similarity alone
    # never suffices).
    request = make_edge_request(evidence_refs=("ev-bad",))
    result = node.propose(request, ctx, execution_id="tne-1")
    assert result["verdict"] == "REJECTED"
    assert any("E_NO_EVIDENCE" in r for r in result["reasons"])
    # An empty ref list is malformed intake (required field empty).
    request = make_edge_request(evidence_refs=())
    result = node.propose(request, ctx, execution_id="tne-2")
    assert result["verdict"] == "REJECTED"
    assert any("E_MALFORMED" in r for r in result["reasons"])


def test_governance_export_refused(node):
    ctx = make_context(make_consents())
    request = make_edge_request(classes=("law_state",))
    result = node.propose(request, ctx, execution_id="tge-1")
    assert result["verdict"] == "REJECTED"
    assert any("E_GOVERNANCE_EXPORT" in r for r in result["reasons"])


def test_policy_forbidden_refused(node):
    policy = copy.deepcopy(POLICY)
    policy["forbidden_classes"] = ["RAW_PRIVATE_MEMORY"]
    ctx = make_context(make_consents(), policy=policy)
    request = make_edge_request(classes=("RAW_PRIVATE_MEMORY",))
    result = node.propose(request, ctx, execution_id="tpf-1")
    assert result["verdict"] == "REJECTED"
    assert any("E_PROHIBITED_CROSSING" in r for r in result["reasons"])


def test_supersede_keeps_lineage(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(rid="v1"), ctx, execution_id="tss-1")
    node.propose(make_edge_request(rid="v2"), ctx, execution_id="tss-2")
    result = node.supersede("v1", "v2", "tss-3")
    assert result["verdict"] == "SUPERSEDED"
    assert result["superseded_by"] == "v2"
    assert node.retrieve("v1") is None
    assert node.retrieve("v2") is not None


def test_invalidate_poisoned_edge(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="tinv-1")
    result = node.invalidate("conn-1", "counterpart illegitimate",
                             "tinv-2")
    assert result["verdict"] == "INVALID"
    assert node.edge_ledger["conn-1"]["epistemic_state"] == "INVALIDATED"
    assert node.retrieve("conn-1") is None


def test_gate_verdict_mapping(node):
    ctx = make_context(make_consents())
    good = node.gate({**ctx, "connection_request": make_edge_request()})
    assert good.verdict == GateVerdict.PASS
    bad = node.gate({**ctx, "connection_request": {"id": "x"}})
    assert bad.verdict == GateVerdict.FAIL
    request = make_edge_request(rid="async-1", parties=("naya", "agent-y"),
                                kind="MIND_LINK",
                                consent_refs=["consent-naya",
                                              "consent-agent-y"])
    async_ctx = make_context(make_consents(parties=("naya", "agent-y")))
    pending = node.gate({**async_ctx, "connection_request": request})
    assert pending.verdict == GateVerdict.NEED_EVIDENCE


def test_edge_binding_fields(node):
    ctx = make_context(make_consents())
    result = node.propose(make_edge_request(), ctx, execution_id="teb-1")
    edge = result["receipt"]["payload"]["edge"]
    assert edge["relationship_id"] == "conn-1"
    assert edge["consent_ref"] == ["consent-naya"]  # required by V2 selector
    assert "CONNECT_VALIDATED" in edge["reason_codes"]
    assert edge["applicability"]["purpose"] == "research"
    assert edge["epistemic_state"] == "CONNECTED"


def test_traverse_bounded_deterministic(node):
    ctx = make_context(make_consents(parties=("naya", "agent-y")))
    node.propose(make_edge_request(rid="g1", parties=("naya",),
                                   consent_refs=["consent-naya"]),
                 ctx, execution_id="tt-1")
    node.propose(make_edge_request(rid="g2", parties=("naya", "agent-y"),
                                   consent_refs=["consent-naya",
                                                 "consent-agent-y"]),
                 ctx, execution_id="tt-2")
    first = node.traverse("naya", max_hops=2)
    second = node.traverse("naya", max_hops=2)
    assert first == second
    assert all(h["from"] != h["to"] for h in first)


def test_rank_relevance_deterministic(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(rid="r1", purpose="research"),
                 ctx, execution_id="trn-1")
    node.propose(make_edge_request(rid="r2", purpose="marketing"),
                 ctx, execution_id="trn-2")
    query = {"purpose": "research", "content_classes": ["reports"]}
    first = node.rank_relevance(query)
    second = node.rank_relevance(query)
    assert first == second
    assert first[0]["connection_id"] == "r1"  # purpose match outranks


def test_assess_applicability(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="taa-1")
    ok = node.assess_applicability(
        "conn-1", {"purpose": "research", "content_class": "reports",
                   "owner_scope": "shawn-scope"})
    assert ok["applicable"] is True
    wrong_purpose = node.assess_applicability(
        "conn-1", {"purpose": "ads", "content_class": "reports",
                   "owner_scope": "shawn-scope"})
    assert wrong_purpose["applicable"] is False
    node.revoke("conn-1", "revoked", "taa-2", now=NOW)
    revoked = node.assess_applicability(
        "conn-1", {"purpose": "research", "content_class": "reports",
                   "owner_scope": "shawn-scope"})
    assert revoked["applicable"] is False


def test_explain_connection_answers_five_questions(node):
    ctx = make_context(make_consents())
    node.propose(make_edge_request(), ctx, execution_id="tec-1")
    explanation = node.explain_connection("conn-1")
    assert explanation["who"]
    assert explanation["under_what_consent"] == ["consent-naya"]
    assert "boundary_policy" in explanation
    assert explanation["transitions"]


def test_calculus_posture_is_aspirational(node):
    ctx = make_context(make_consents())
    result = node.propose(make_edge_request(), ctx, execution_id="tcp-1")
    calculus = result["receipt"]["payload"]["calculus"]
    assert calculus["aspirational"] is True
    assert calculus["calculusVersion"] == "v2.1-CANDIDATE"


# --- spaces (§6) -------------------------------------------------------

def test_space_lifecycle(node):
    created = node.create_space(
        {"id": "space-1",
         "charter": {"purpose": "family photos",
                     "membership_rules": {"admission": "charter-consent"},
                     "retention_policy": {
                         "after_exit": "no retention beyond participation"}},
         "boundaryPolicy": copy.deepcopy(POLICY)}, "tsp-1")
    assert created["verdict"] == "ACTIVE"
    joined = node.join_space(
        "space-1", {"identity": "naya", "owner_scope": "shawn-scope",
                    "consent_ref": "consent-naya"}, "tsp-2")
    assert joined["verdict"] == "JOINED"
    # Exit is unilateral: no other consent needed.
    exited = node.exit_space("space-1", "naya", "tsp-3")
    assert exited["verdict"] == "EXITED"
    assert "no retention beyond participation" in \
        exited["receipt"]["payload"]["retention_applied"]


def test_charter_change_requires_every_member(node):
    node.create_space(
        {"id": "space-2",
         "charter": {"purpose": "study",
                     "membership_rules": {"admission": "charter-consent"},
                     "retention_policy": {"after_exit": "ledger-only"}},
         "boundaryPolicy": copy.deepcopy(POLICY)}, "tch-1")
    node.join_space("space-2", {"identity": "naya",
                                "owner_scope": "shawn-scope",
                                "consent_ref": "c1"}, "tch-2")
    node.join_space("space-2", {"identity": "agent-y",
                                "owner_scope": "other-scope",
                                "consent_ref": "c2"}, "tch-3")
    new_charter = {"purpose": "marketing", "membership_rules": {},
                   "retention_policy": {}}
    with pytest.raises(ValueError, match="re-consent"):
        node.change_charter("space-2", new_charter, ["naya"], "tch-4")
    ok = node.change_charter("space-2", new_charter, ["naya", "agent-y"],
                             "tch-5")
    assert ok["verdict"] == "CHARTER_CHANGED"
    assert node.spaces["space-2"]["charter_version"] == 2


def test_dissolve_space_retains_lineage(node):
    node.create_space(
        {"id": "space-3",
         "charter": {"purpose": "tmp",
                     "membership_rules": {"admission": "charter-consent"},
                     "retention_policy": {"after_exit": "ledger-only"}},
         "boundaryPolicy": copy.deepcopy(POLICY)}, "tds-1")
    dissolved = node.dissolve_space("space-3", "tds-2")
    assert dissolved["verdict"] == "DISSOLVED"
    assert node.spaces["space-3"]["state"] == "DISSOLVED"
    with pytest.raises(ValueError):
        node.join_space("space-3", {"identity": "naya",
                                    "owner_scope": "shawn-scope",
                                    "consent_ref": "c1"}, "tds-3")


def test_space_entry_needs_charter_consent(node):
    node.create_space(
        {"id": "space-4",
         "charter": {"purpose": "tmp",
                     "membership_rules": {"admission": "charter-consent"},
                     "retention_policy": {"after_exit": "ledger-only"}},
         "boundaryPolicy": copy.deepcopy(POLICY)}, "tsec-1")
    with pytest.raises(ValueError, match="consent_ref"):
        node.join_space("space-4", {"identity": "naya",
                                    "owner_scope": "shawn-scope"},
                        "tsec-2")
