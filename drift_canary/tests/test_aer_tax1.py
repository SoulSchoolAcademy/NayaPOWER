"""AER-TAX-1 tests (SN-0805): authority separation, the versioned governance
state, the commit boundary, the three races (R1-R12), fast incident
containment, the Authorize(a,s) predicate, history preservation, the AER-TAX-1
receipt, the independent history verifier, the guard-removal mutants, and
AER-TAX-001. Every negative test gets a positive control."""
import pytest

from drift_canary.revocation_linearization import (
    AER_TAX1_IMPLEMENTATION_STATUS,
    AUTHORITY_SEPARATION,
    TAX_CHANGE_TABLE,
    GovernanceState,
    prepare_governed_change,
    commit_prepared_change,
    supersede_receipt,
    rollback_governed_change,
    contain_incident,
    authorize_tax_action,
    act_execute,
    reconcile_inflight,
    make_tax_receipt,
    tax_r_harness,
    verify_committed_history,
    aer_tax_001,
)


def _law():
    return {"receipt": "LAW-1", "valid": True}


def _gov_ab():
    gov = GovernanceState()
    for s in ("scope:A", "scope:B"):
        gov.scope_mapping[s] = {"parent": None, "children": [],
                                "taxonomy_version": 0}
        gov.active_qualifications[s] = {"guarantee": f"idem:{s}",
                                        "status": "QUALIFIED",
                                        "qualification_rev": 0,
                                        "taxonomy_version": 0}
    return gov


def _guarantee(scope):
    return {"guarantee_id": f"idem:{scope}", "verified": True,
            "qualified_scopes": (scope,), "revision": 0, "current": True}


# --- Honest scope ----------------------------------------------------------------------------------

def test_implementation_status_is_harness_demonstration():
    s = AER_TAX1_IMPLEMENTATION_STATUS
    assert s["enters_as"] == "isolated harness demonstration"
    assert "live production authority change" in s["not_a"]
    assert "parallel governance registry" in s["not_a"]
    assert "full protocol implementation" in s["not_verified"]


def test_authority_separation_three_authorities():
    assert set(AUTHORITY_SEPARATION) == {"taxonomy", "qualification", "law"}
    assert set(TAX_CHANGE_TABLE) == {"MERGE_SPLIT", "PROVISIONAL_SCOPE",
                                     "INCIDENT_WITHDRAWAL",
                                     "BASELINE_PROMOTION_ACT"}


# --- Governance state ---------------------------------------------------------------------------------

def test_snapshot_is_not_an_authority_token():
    gov = _gov_ab()
    snap = gov.snapshot()
    assert snap["authority_token"] is False
    assert snap["governance_epoch"] == 0
    assert set(snap["revisions"]) == {"taxonomy", "incident", "qualification",
                                      "baseline", "policy"}


def test_epoch_monotonic_and_versions_never_reused():
    gov = _gov_ab()
    e0 = gov.epoch
    p = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A", "scope:B"],
         "evidence": {"merged_id": "scope:AB"}, "law_receipt": _law()}, gov)
    assert commit_prepared_change(gov, p)["committed"]
    assert gov.epoch > e0
    r = rollback_governed_change(gov, "m1", "test rollback")
    assert gov.epoch > e0 + 1
    # Rollback is a NEW revision: the bumped revisions are recorded, nothing
    # rewound.
    assert set(r["bumped_revisions"]) == {"taxonomy", "incident",
                                          "qualification", "baseline",
                                          "policy"}


def test_prepare_does_not_mutate_state():
    gov = _gov_ab()
    e0, rev0 = gov.epoch, dict(gov.revisions)
    prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A", "scope:B"],
         "evidence": {"merged_id": "scope:AB"}, "law_receipt": _law()}, gov)
    assert gov.epoch == e0 and gov.revisions == rev0
    # Preparation is concurrent-safe: no lock needed, no state touched.


def test_commit_rejects_stale_snapshot():
    gov = _gov_ab()
    stale = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A", "scope:B"],
         "evidence": {"merged_id": "scope:AB"}, "law_receipt": _law()}, gov)
    # Another change commits first: the incident revision moves.
    other = prepare_governed_change(
        {"change_id": "w1", "change_type": "INCIDENT_WITHDRAWAL",
         "scopes": ["scope:B"],
         "evidence": {"incident": {"incident_id": "i1", "confirmed": True},
                      "verifier_ref": "v"}, "law_receipt": _law()}, gov)
    assert commit_prepared_change(gov, other)["committed"]
    r = commit_prepared_change(gov, stale)
    assert not r["committed"] and r["status"] == "REJECTED_STALE_SNAPSHOT"
    assert "incident" in r["stale_revisions"]


def test_commit_rejects_closure_change_phantom():
    gov = _gov_ab()
    p = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A"],
         "evidence": {"merged_id": "scope:A2"}, "law_receipt": _law()}, gov)
    # Phantom: the mapping moves under the prepared change without going
    # through a governed commit (simulated direct edit).
    gov.scope_mapping["scope:A"]["children"] = ["scope:Ax"]
    r = commit_prepared_change(gov, p)
    # The revision check fires first here (no revision moved, but closure did).
    assert not r["committed"]
    assert r["status"] in ("REJECTED_CLOSURE_CHANGED", "REJECTED_STALE_SNAPSHOT")


def test_commit_rejects_without_law():
    gov = _gov_ab()
    p = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A"],
         "evidence": {"merged_id": "scope:A2"},
         "law_receipt": {"receipt": "LAW-1", "valid": False}}, gov)
    r = commit_prepared_change(gov, p)
    assert not r["committed"] and r["status"] == "REJECTED_NO_LAW"


def test_superseded_receipt_stays_historical():
    gov = _gov_ab()
    p = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A"],
         "evidence": {"merged_id": "scope:A2"}, "law_receipt": _law()}, gov)
    mg = commit_prepared_change(gov, p)
    seq = mg["receipt"]["seq"]
    sup = supersede_receipt(gov, seq, "test")
    assert sup["superseded"]
    # The original receipt is untouched in the log.
    orig = next(r for r in gov.receipts if r["seq"] == seq)
    assert orig["change_id"] == "m1" and "supersedes_seq" not in orig


# --- Incident containment -------------------------------------------------------------------------------

def test_contain_incident_confirmed_withdraws():
    gov = _gov_ab()
    r = contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:A"],
                               "confirmed": True}, _law())
    assert r["contained"] and r["kind"] == "CONFIRMED"
    assert gov.active_qualifications["scope:A"]["status"] == "WITHDRAWN"
    # Unaffected paths preserved.
    assert gov.active_qualifications["scope:B"]["status"] == "QUALIFIED"


def test_contain_incident_precautionary_not_confirmed():
    gov = _gov_ab()
    r = contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:A"],
                               "confirmed": False, "uncertain_scope": True},
                        _law())
    assert r["contained"] and r["kind"] == "PRECAUTIONARY_HOLD"
    assert r["uncertain_scope_recorded"]
    # Unverified incidents are never labeled confirmed.
    assert gov.incidents["i1"]["confirmed"] is False


def test_contain_incident_needs_law():
    gov = _gov_ab()
    r = contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:A"],
                               "confirmed": True}, {"valid": False})
    assert not r["contained"]


# --- Authorize(a,s) ------------------------------------------------------------------------------------------

def test_authorize_predicate_all_five_conjuncts():
    gov = _gov_ab()
    r = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                             _law())
    assert r["authorized"]
    assert all(r["checks"].values())
    assert set(r["checks"]) == {"CurrentTaxonomy", "CurrentQualification",
                                "NoDisqualifyingIncident", "EvidenceCovers",
                                "LAWPermits"}


def test_authorize_denied_provisional_scope():
    gov = _gov_ab()
    p = prepare_governed_change(
        {"change_id": "pr", "change_type": "PROVISIONAL_REGISTER",
         "scopes": ["scope:P"], "evidence": {}, "law_receipt": _law()}, gov)
    assert commit_prepared_change(gov, p)["committed"]
    r = authorize_tax_action(gov, "a1", "scope:P", _guarantee("scope:P"),
                             _law())
    assert not r["authorized"]
    assert not r["checks"]["CurrentQualification"]


def test_authorize_denied_after_withdrawal():
    gov = _gov_ab()
    contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:A"],
                           "confirmed": True}, _law())
    r = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                             _law())
    assert not r["authorized"]
    assert not r["checks"]["NoDisqualifyingIncident"]


def test_authorize_statistical_parent_is_not_evidence():
    gov = _gov_ab()
    # A guarantee qualified for A never covers B via a shared statistical
    # parent: EvidenceCovers is semantic, not statistical.
    g = _guarantee("scope:A")
    g["statistical_parent_id"] = "shared-parent"
    r = authorize_tax_action(gov, "a1", "scope:B", g, _law())
    assert not r["authorized"] and not r["checks"]["EvidenceCovers"]


def test_authorize_denied_no_law():
    gov = _gov_ab()
    r = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                             {"valid": False})
    assert not r["authorized"] and not r["checks"]["LAWPermits"]


# --- ACT boundary -----------------------------------------------------------------------------------------------

def test_act_execute_fresh_authorization():
    gov = _gov_ab()
    auth = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                                _law())
    r = act_execute(gov, auth, _guarantee("scope:A"), _law())
    assert r["executed"]
    assert gov.inflight["a1"]["status"] == "INTENT_FENCED"
    # The intent is committed; no transaction held across a provider call.


def test_act_execute_stale_authorization_rechecked():
    gov = _gov_ab()
    auth = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                                _law())
    contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:A"],
                           "confirmed": True}, _law())
    r = act_execute(gov, auth, _guarantee("scope:A"), _law())
    assert not r["executed"] and r["reason"] == "stale authorization"


def test_act_execute_unaffected_scope_survives_unrelated_change():
    gov = _gov_ab()
    auth = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                                _law())
    # Unrelated provisional registration moves the epoch but not A's state.
    p = prepare_governed_change(
        {"change_id": "pr", "change_type": "PROVISIONAL_REGISTER",
         "scopes": ["scope:P"], "evidence": {}, "law_receipt": _law()}, gov)
    assert commit_prepared_change(gov, p)["committed"]
    r = act_execute(gov, auth, _guarantee("scope:A"), _law())
    assert r["executed"]  # no global bottleneck: A's state is what matters


def test_act_execute_mutant_no_revalidation_executes_stale():
    gov = _gov_ab()
    auth = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                                _law())
    contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:A"],
                           "confirmed": True}, _law())
    bad = act_execute(gov, auth, _guarantee("scope:A"), _law(),
                      revalidate_at_execution=False)
    assert bad["executed"]  # the mutant executes the stale authorization
    good = act_execute(gov, dict(auth), _guarantee("scope:A"), _law(),
                       revalidate_at_execution=True)
    assert not good["executed"]


def test_reconcile_inflight_preserves_unresolved():
    gov = _gov_ab()
    auth = authorize_tax_action(gov, "a1", "scope:A", _guarantee("scope:A"),
                                _law())
    act_execute(gov, auth, _guarantee("scope:A"), _law())
    r = reconcile_inflight(gov, "a1", "EFFECT_UNKNOWN")
    assert r["reconciled"] and r["outcome"] == "EFFECT_UNKNOWN"
    assert "enforcement boundary" in r["note"]
    assert not reconcile_inflight(gov, "nope", "X")["reconciled"]


# --- Receipt + history verifier --------------------------------------------------------------------------------------

def test_tax_receipt_split_never_requalified():
    with pytest.raises(ValueError):
        make_tax_receipt("s1", "TAXONOMY_SPLIT", {}, ["a"],
                         {"a": {"ok": True, "result": "REQUALIFIED"}},
                         "v", _law(), "COMMITTED")


def test_tax_receipt_prepared_not_committed():
    r = make_tax_receipt("s1", "TAXONOMY_SPLIT", {}, ["a"],
                         {"a": {"ok": True,
                                "result": "REASSESSMENT_REQUIRED"}},
                         "v", _law(), "PREPARED_NOT_COMMITTED")
    assert r["status"] == "PREPARED_NOT_COMMITTED"
    assert "never counts as committed" in r["note"]


def test_verify_committed_history_clean():
    gov = _gov_ab()
    p = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A"],
         "evidence": {"merged_id": "scope:A2"}, "law_receipt": _law()}, gov)
    assert commit_prepared_change(gov, p)["committed"]
    v = verify_committed_history(gov)
    assert v["verified"], v["issues"]
    assert v["receipts_replayed"] == 1


def test_verify_committed_history_flags_stale_publication():
    gov = _gov_ab()
    gov.scope_mapping["scope:C"] = {"parent": None, "children": [],
                                    "taxonomy_version": 0}
    stale = prepare_governed_change(
        {"change_id": "m1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A", "scope:B"],
         "evidence": {"merged_id": "scope:AB"}, "law_receipt": _law()}, gov)
    contain_incident(gov, {"incident_id": "i1", "scopes": ["scope:C"],
                           "confirmed": False}, _law())
    bad = commit_prepared_change(gov, stale, check_incident_revision=False)
    assert bad["committed"]  # the mutant commits
    v = verify_committed_history(gov)
    assert not v["verified"]
    assert any("stale incident" in i for i in v["issues"])


# --- R1–R12 + AER-TAX-001 -----------------------------------------------------------------------------------------------------

def test_r_harness_all_twelve_pass():
    results = tax_r_harness()
    assert [i for i, _, _ in results] == [f"R{i}" for i in range(1, 13)]
    bad = [(i, n) for i, v, n in results if v != "PASS"]
    assert not bad, bad


def test_aer_tax_001():
    r = aer_tax_001()
    assert len(r["interleavings"]) == 12
    bad = [i for i in r["interleavings"] if not i["accepted"]]
    assert not bad, bad
    m1 = r["mutant_incident_check_removed"]
    assert m1["stale_publication_committed"]
    assert m1["independent_verifier_flags_stale"]
    assert m1["restored"] == "rejected"
    m2 = r["mutant_taxonomy_check_removed"]
    assert m2["unsupported_inheritance"]
    assert m2["restored"] == "HELD"
