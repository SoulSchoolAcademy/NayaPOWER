"""Permanent regressions for the semantic truth-state poisoning hole.

THE ATTACK (Naya 3, PR #1463): a direct edit to
`.naya/memory/smart-notes/index.json` escalated truth_state CANDIDATE ->
RATIFIED. The structural poison battery saw a well-formed registry with
correct hashes. It could not see that nobody held promotion authority and no
promotion evidence existed.

These tests are the battery growing teeth. Each one is a negative control: it
fails loudly if the invariant is removed. A guard with no failing test is
decoration.
"""

from __future__ import annotations

import copy
import hashlib
import json

import pytest

from tools.truth_state_guard import (
    GuardResult,
    apply_elevation,
    audit_registry_semantics,
    authority_is_valid,
    check_elevation,
    evidence_is_valid,
    is_escalation,
    rank,
)


def _receipt(note_id="SN-TEST", hashes=("h1",)):
    body = {
        "schema": "naya.promotion-receipt.v1",
        "note_id": note_id,
        "promoter": "shawn",
        "evidence_hashes": list(hashes),
    }
    body["receipt_hash"] = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return body


def _authority(promoter="shawn", scope="ratify"):
    return {"promoter": promoter, "scope": scope}


def _bundle(*hashes):
    return [{"content_hash": h} for h in hashes]


def _candidate_entry():
    return {"smart_note_id": "SN-TEST", "truth_state": "CANDIDATE"}


# ==========================================================================
# REPRODUCTION -- Naya 3's attack, executed directly on the registry
# ==========================================================================
def test_direct_edit_escalation_is_the_attack_we_are_closing():
    """The structural battery cannot see this. That is the whole point."""
    registry = {"entries": [_candidate_entry()]}
    # A hand edit. No authority, no evidence, no receipt.
    registry["entries"][0]["truth_state"] = "RATIFIED"

    problems = audit_registry_semantics(registry)
    assert problems, (
        "a hand-edited CANDIDATE->RATIFIED escalation was NOT detected; the "
        "semantic guard is not working"
    )
    assert "promotion" in problems[0]


# ==========================================================================
# CASE 1 -- CANDIDATE -> RATIFIED by direct edit: REJECTED
# ==========================================================================
def test_case1_candidate_to_ratified_without_authority_rejected():
    res = apply_elevation(_candidate_entry(), "RATIFIED")
    assert not res.allowed
    assert "promotion_authority" in res.missing


def test_case1_rejection_records_nothing():
    """A rejected write must be a NON-EVENT, not a recorded failure."""
    entry = _candidate_entry()
    res = apply_elevation(entry, "RATIFIED")
    assert not res.allowed
    assert entry["truth_state"] == "CANDIDATE", "rejected write mutated the entry"
    assert "authority_history" not in entry
    assert "promotion_receipt" not in entry


def test_case1_with_valid_authority_and_evidence_succeeds():
    r = _receipt()
    entry = _candidate_entry()
    res = apply_elevation(entry, "RATIFIED", _authority(), r, _bundle("h1"))
    assert res.allowed
    assert entry["truth_state"] == "RATIFIED"
    assert entry["promotion_authority"]["promoter"] == "shawn"
    assert entry["authority_history"]


# ==========================================================================
# CASE 2 -- ACTIVE fabricated without provenance: REJECTED
# ==========================================================================
def test_case2_active_without_verified_predecessor_rejected():
    res = apply_elevation(_candidate_entry(), "ACTIVE", _authority(),
                          _receipt(), _bundle("h1"))
    assert not res.allowed
    assert any("proven_predecessor" in m for m in res.missing)


def test_case2_active_from_verified_with_evidence_succeeds():
    entry = _candidate_entry()
    entry["truth_state"] = "VERIFIED"
    res = apply_elevation(entry, "ACTIVE", _authority(), _receipt(), _bundle("h1"))
    assert res.allowed and entry["truth_state"] == "ACTIVE"


def test_case2_active_detected_in_audit_without_provenance():
    registry = {"entries": [{"smart_note_id": "SN-X", "truth_state": "ACTIVE"}]}
    assert audit_registry_semantics(registry)


# ==========================================================================
# CASE 3 -- LEARNED asserted without behavioral evidence: REJECTED
# ==========================================================================
def test_case3_learned_without_behavioral_evidence_rejected():
    entry = _candidate_entry()
    entry["truth_state"] = "RATIFIED"
    res = apply_elevation(entry, "LEARNED", _authority(), _receipt(), _bundle("h1"))
    assert not res.allowed
    assert "behavioral_evidence" in res.missing


def test_case3_learned_with_behavioral_evidence_succeeds():
    entry = _candidate_entry()
    entry["truth_state"] = "RATIFIED"
    res = apply_elevation(entry, "LEARNED", _authority(), _receipt(), _bundle("h1"),
                          behavioral_evidence=[{"task": "t", "delta": 0.4}])
    assert res.allowed and entry["truth_state"] == "LEARNED"


def test_case3_learned_without_behavior_found_by_audit():
    registry = {"entries": [{"smart_note_id": "SN-L", "truth_state": "LEARNED",
                             "promotion_authority": _authority(),
                             "promotion_receipt": "abc"}]}
    problems = audit_registry_semantics(registry)
    assert any("behavioral" in p for p in problems)


# ==========================================================================
# CASE 4 -- supersession that erases authority history: REJECTED
# ==========================================================================
def test_case4_supersession_preserves_authority_history():
    entry = _candidate_entry()
    apply_elevation(entry, "RATIFIED", _authority(), _receipt(), _bundle("h1"))
    entry["superseded_by"] = "SN-NEXT"
    assert entry["authority_history"], "supersession erased authority history"
    assert audit_registry_semantics({"entries": [entry]}) == []


def test_case4_audit_flags_erased_history():
    registry = {"entries": [{
        "smart_note_id": "SN-S", "truth_state": "RATIFIED",
        "superseded_by": "SN-NEXT", "promotion_authority": _authority(),
        "promotion_receipt": "abc",
    }]}
    problems = audit_registry_semantics(registry)
    assert any("authority history erased" in p for p in problems)


# ==========================================================================
# FAIL-CLOSED PRIMITIVES
# ==========================================================================
def test_tampered_receipt_is_invalid():
    r = _receipt()
    r["evidence_hashes"] = ["h2"]
    assert not evidence_is_valid(r, _bundle("h1"))


def test_receipt_with_mismatched_bundle_is_invalid():
    assert not evidence_is_valid(_receipt(), _bundle("different"))


def test_blank_authority_is_invalid():
    assert not authority_is_valid({"promoter": "", "scope": "ratify"})
    assert not authority_is_valid({"promoter": "shawn", "scope": ""})
    assert not authority_is_valid(None)


def test_unknown_state_never_outranks_candidate():
    assert rank("GARBAGE") == 0
    assert not is_escalation("CANDIDATE", "GARBAGE")


def test_demotion_is_always_permitted():
    """Containment must never be blocked."""
    entry = {"smart_note_id": "SN-D", "truth_state": "LEARNED"}
    res = apply_elevation(entry, "CANDIDATE")
    assert res.allowed and entry["truth_state"] == "CANDIDATE"


def test_registry_audit_passes_clean_registry():
    assert audit_registry_semantics(
        {"entries": [{"smart_note_id": "SN-OK", "truth_state": "VERIFIED"}]}
    ) == []
