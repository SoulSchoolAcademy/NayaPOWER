"""Adversarial suite for UD-03: CHANGING OUR MIND TAKES EVIDENCE.

Acceptance gate: PASS only if challenges requalify correctly, history is
intact, weak evidence can't change truth, and drifted thresholds are
caught. One failure = FAIL.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evidence_ledger import (
    BeliefLedger, ContextFingerprint, Refusal,
    SUPPORTS, REFUTES,
    SETTLED, CHALLENGED, REQUALIFIED, UNRESOLVED,
    NO_EVIDENCE, WEAK_EVIDENCE, EVIDENCE_IMMUTABLE,
    CONFIDENCE_EXCEEDS_EVIDENCE, DRIFT_UNREQUALIFIED, SAFETY_FROM_ABSENCE,
    max_supported_confidence, confidence_interval,
)


def fresh_ledger(**kw):
    return BeliefLedger(**kw)


def register_connector_belief(ledger):
    """'The connector is safe for production' — settled on solid evidence."""
    e1 = ledger.record_evidence("3 independent safety reviews passed",
                                0.8, "safety-team", SUPPORTS)
    ledger.register_belief("connector-safe",
                            "The connector is safe for production use.",
                            [e1], confidence=0.8)
    return e1


# --- positive: genuine evidence updates, history intact ---------------------

def test_genuine_evidence_updates_belief():
    L = fresh_ledger()
    register_connector_belief(L)
    e2 = L.record_evidence("reproduced data-corruption incident in staging",
                           0.85, "qa-team", SUPPORTS)  # supports the NEW view
    h = L.update_belief("connector-safe",
                        "The connector corrupts data under load; not safe.",
                        [e2], confidence=0.8)
    assert L.status("connector-safe") == REQUALIFIED
    hist = L.history("connector-safe")
    assert len(hist) == 2, "old version must be retained"
    assert hist[0].interpretation.startswith("The connector is safe")
    assert hist[1].interpretation.startswith("The connector corrupts")
    assert hist[1].prev_hash == hist[0].version_hash, "hash chain intact"
    assert hist[1].version_hash == h
    assert e2 in hist[1].evidence_ids, "new version cites its cause"


def test_protective_action_triggers_before_truth_changes():
    L = fresh_ledger()
    register_connector_belief(L)
    # 0.35 >= protect 0.30 but < change_truth 0.70: protect now, truth stays.
    L.record_evidence("field report suggests possible data harm in edge cases",
                      0.35, "field-team", REFUTES)
    assert L.protective_check("connector-safe") == "PROTECT"
    assert L.status("connector-safe") == SETTLED, \
        "truth must NOT change on protect-level evidence"


def test_unaffected_beliefs_continue():
    L = fresh_ledger()
    register_connector_belief(L)
    e = L.record_evidence("docs are accurate", 0.9, "docs-team", SUPPORTS)
    L.register_belief("docs-ok", "The docs are accurate.", [e])
    e_harm = L.record_evidence("possible data harm reported", 0.5,
                             "field", REFUTES)
    L.challenge("connector-safe", [e_harm])
    assert L.status("docs-ok") == SETTLED
    assert L.rely("docs-ok")["version"] == 1


def test_return_to_unresolved_is_honest():
    L = fresh_ledger()
    register_connector_belief(L)
    e = L.record_evidence("conflicting lab results, methodology disputed",
                          0.5, "lab", REFUTES)
    L.return_to_unresolved("connector-safe", [e],
                           "evidence conflicts; refusing to force an update")
    assert L.status("connector-safe") == UNRESOLVED
    try:
        L.rely("connector-safe")
        assert False, "relying on unresolved belief must be refused"
    except Refusal as r:
        assert r.code == "UNRESOLVED_BELIEF"


# --- negative: no evidence, weak evidence, inflation -------------------------

def test_evidence_free_update_refused():
    L = fresh_ledger()
    register_connector_belief(L)
    try:
        L.update_belief("connector-safe", "Actually it is not safe.", [])
        assert False, "evidence-free mind-change must be refused"
    except Refusal as r:
        assert r.code == NO_EVIDENCE, r.code
    assert L.status("connector-safe") == SETTLED
    assert len(L.history("connector-safe")) == 1


def test_update_citing_unrecorded_evidence_refused():
    L = fresh_ledger()
    register_connector_belief(L)
    try:
        L.update_belief("connector-safe", "New view.", ["ev-9999"])
        assert False
    except Refusal as r:
        assert r.code == NO_EVIDENCE, r.code


def test_weak_evidence_cannot_change_truth():
    L = fresh_ledger()
    register_connector_belief(L)
    e = L.record_evidence("one anecdotal report of slowness", 0.4,
                          "anon", SUPPORTS)  # 0.4 < change_truth 0.70
    try:
        L.update_belief("connector-safe", "The connector is slow.", [e])
        assert False, "thin evidence must not rewrite settled truth"
    except Refusal as r:
        assert r.code == WEAK_EVIDENCE, r.code
    assert L.status("connector-safe") == SETTLED


def test_confidence_inflation_refused():
    L = fresh_ledger()
    register_connector_belief(L)
    e1 = L.record_evidence("second review passed", 0.5, "safety-team", SUPPORTS)
    e2 = L.record_evidence("third review passed", 0.5, "safety-team", SUPPORTS)
    # for_new = 1.0 >= 0.70 (passes weak-evidence), cap = 0.75 < 0.95 claimed
    try:
        L.update_belief("connector-safe", "Safer than we thought.",
                        [e1, e2], confidence=0.95)
        assert False, "confidence beyond evidence must be refused"
    except Refusal as r:
        assert r.code == CONFIDENCE_EXCEEDS_EVIDENCE, r.code


def test_contradicting_evidence_cannot_be_deleted():
    L = fresh_ledger()
    register_connector_belief(L)
    e = L.record_evidence("reproduced corruption twice", 0.85, "qa", REFUTES)
    try:
        L.retract_evidence(e)
        assert False, "deleting contradicting evidence must be refused"
    except Refusal as r:
        assert r.code == EVIDENCE_IMMUTABLE, r.code
    assert L.get_evidence(e).statement.startswith("reproduced corruption"), \
        "evidence must still be present"


def test_silent_rewrite_is_structurally_impossible():
    L = fresh_ledger()
    register_connector_belief(L)
    b = L._beliefs["connector-safe"]
    hist = L.history("connector-safe")
    assert isinstance(hist, tuple), "history must be an immutable tuple"
    try:
        hist.append("forged")
        assert False
    except AttributeError:
        pass
    for name in ("rewrite", "replace_interpretation", "edit_version",
                 "set_interpretation", "overwrite"):
        assert not hasattr(L, name), f"no silent-rewrite path: {name}"
        assert not hasattr(b, name), f"no silent-rewrite path: {name}"
    v = hist[0]
    try:
        v.interpretation = "forged"
        assert False
    except Exception:
        pass  # frozen dataclass
    assert L.history("connector-safe")[0].interpretation.startswith(
        "The connector is safe")


def test_below_listen_threshold_stays_settled():
    L = fresh_ledger()
    register_connector_belief(L)
    e = L.record_evidence("vague rumor of issues", 0.2, "anon", REFUTES)
    st = L.challenge("connector-safe", [e])
    assert st == SETTLED, "easy to listen != easy to change"
    # ...but the evidence was still recorded (listening happened)
    assert L.get_evidence(e).weight == 0.2


def test_challenge_opens_versioned_path():
    L = fresh_ledger()
    register_connector_belief(L)
    e = L.record_evidence("independent lab reproduced corruption", 0.6,
                          "lab", REFUTES)  # >= listen 0.25
    st = L.challenge("connector-safe", [e])
    assert st == CHALLENGED
    assert L.status("connector-safe") == CHALLENGED


# --- negative: absence of harm is not safety ---------------------------------

def test_absence_of_harm_is_not_proof_of_safety():
    L = fresh_ledger()
    register_connector_belief(L)
    try:
        L.assess_safety_from_observations("connector-safe", 0)
        assert False, "zero observed harms must never certify safety"
    except Refusal as r:
        assert r.code == SAFETY_FROM_ABSENCE, r.code


def test_uncertainty_interval_honest_on_no_evidence():
    lo, hi = confidence_interval([], [])
    assert (lo, hi) == (0.0, 1.0), "no evidence = total uncertainty, stated"


def test_quantity_is_not_proof():
    cap = max_supported_confidence([0.1] * 10)
    assert cap < 0.70, f"ten weak sources must not clear change-truth: {cap}"


# --- drift: thresholds bound to their context --------------------------------

def test_drifted_thresholds_block_consequential_reliance():
    L = fresh_ledger()
    register_connector_belief(L)
    assert L.rely("connector-safe")["version"] == 1
    L.note_context_drift(ContextFingerprint(policy="p2", model="m2",
                                            evaluator="e2", environment="prod"))
    try:
        L.rely("connector-safe")
        assert False, "drifted thresholds must block reliance"
    except Refusal as r:
        assert r.code == DRIFT_UNREQUALIFIED, r.code
    e = L.record_evidence("strong new review", 0.9, "safety", SUPPORTS)
    try:
        L.update_belief("connector-safe", "Even safer.", [e])
        assert False, "drifted thresholds must block updates too"
    except Refusal as r:
        assert r.code == DRIFT_UNREQUALIFIED, r.code


def test_requalification_restores_reliance():
    L = fresh_ledger()
    register_connector_belief(L)
    L.note_context_drift(ContextFingerprint(policy="p2", model="m2",
                                            evaluator="e2", environment="prod"))
    L.requalify_thresholds(ContextFingerprint(policy="p2", model="m2",
                                              evaluator="e2", environment="prod"),
                           "recalibrated on 200 labeled cases under p2/m2")
    assert L.rely("connector-safe")["version"] == 1


def test_receipts_cover_every_transition():
    L = fresh_ledger()
    register_connector_belief(L)
    e_ref = L.record_evidence("lab reproduced corruption", 0.6, "lab", REFUTES)
    L.challenge("connector-safe", [e_ref])  # SETTLED -> CHALLENGED
    e_sup = L.record_evidence("root cause confirmed in code review", 0.85,
                              "eng", SUPPORTS)
    L.update_belief("connector-safe", "Corrupts under load.", [e_sup])
    kinds = {r.transition for r in L.receipts("connector-safe")}
    assert "NONE->SETTLED" in kinds
    assert any("CHALLENGED" in t for t in kinds)
    assert any("REQUALIFIED" in t for t in kinds)
    for r in L.receipts():
        assert r.id and r.at and r.reason, "receipts carry their proof"


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except Exception as ex:
            failed += 1
            print(f"FAIL {name}: {type(ex).__name__}: {ex}")
    print(f"\n{len(tests) - failed}/{len(tests)} green")
    sys.exit(1 if failed else 0)
