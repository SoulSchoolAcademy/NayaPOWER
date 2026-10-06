"""Truth-state poisoning regression suite (#1468).

The structural audit (audit_registry) checks shape — hashes, duplicates,
projection paths — and could not see a hand-edited CANDIDATE->RATIFIED
escalation. These tests pin the semantic invariant: elevation requires
BOTH authority AND evidence at write time; rejection is a non-event.

Conventions: the guard module is loaded standalone via importlib (no repo
imports), tests run against plain dicts so the invariant is verified
independently of any registry implementation.
"""
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "truth_state_guard", ROOT / "tools" / "truth_state_guard.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

H1 = "a" * 64
H2 = "b" * 64
H3 = "c" * 64


def make_entry(state="CANDIDATE", sn="SN-9001"):
    return {"smart_note_id": sn, "intelligent_block_id": "IB-9001",
            "truth_state": state}


def make_evidence(n=2, with_receipt=True, types=None):
    types = types or ["document", "test-report"]
    items = [{"type": t, "source": f"src-{i}", "content_hash": h}
             for i, (t, h) in enumerate(zip(types, [H1, H2, H3]))][:n]
    ev = {"items": items}
    if with_receipt:
        receipt = {"note_id": "SN-9001", "old_state": "CANDIDATE",
                   "new_state": "VERIFIED", "promoter": "naya-2",
                   "evidence_hashes": [it["content_hash"] for it in items]}
        receipt["receipt_hash"] = g._canonical_hash(receipt)
        ev["receipt"] = receipt
    return ev


def snapshot(entry):
    return json.dumps(entry, sort_keys=True)


# --- The four attack cases: permanent regressions -------------------------

def test_case1_direct_edit_candidate_to_ratified_rejected():
    # The original #1468 repro: hand-editing the registry CANDIDATE->RATIFIED
    # was invisible to audit_registry. Through the guard it is rejected.
    e = make_entry("CANDIDATE")
    before = snapshot(e)
    ok, rec = g.apply_elevation(e, "RATIFIED", authority=None, evidence=None)
    assert not ok and rec["reason_code"] == "ELEVATION_REQUIRES_AUTHORITY"
    assert snapshot(e) == before


def test_case2_active_fabricated_without_provenance_rejected():
    e = make_entry("CANDIDATE")
    ev = make_evidence()  # valid items, but no VERIFIED predecessor receipt
    ok, rec = g.apply_elevation(e, "ACTIVE", authority="mallory", evidence=ev)
    assert not ok and rec["reason_code"] == "ACTIVE_REQUIRES_VERIFIED_PREDECESSOR"
    assert e["truth_state"] == "CANDIDATE"


def test_case3_learned_without_behavioral_evidence_rejected():
    e = make_entry("VERIFIED")
    e["elevation_history"] = [{"from": "CANDIDATE", "to": "VERIFIED",
                               "authority": "naya-2", "evidence_hashes": [H1],
                               "evidence_types": ["document"], "at": "t", "kind": "elevation"}]
    ev = make_evidence(types=["document", "test-report"])  # no behavioral item
    ok, rec = g.apply_elevation(e, "LEARNED", authority="naya-2", evidence=ev)
    assert not ok and rec["reason_code"] == "LEARNED_REQUIRES_BEHAVIORAL_EVIDENCE"
    assert e["truth_state"] == "VERIFIED"


def test_case4_supersession_erasing_authority_rejected():
    old = make_entry("RATIFIED", sn="SN-9000")
    old["elevation_history"] = [{"from": "CANDIDATE", "to": "RATIFIED",
                                 "authority": "shawn", "evidence_hashes": [H1],
                                 "evidence_types": ["document"], "at": "t", "kind": "elevation"}]
    new = make_entry("CANDIDATE", sn="SN-9001")  # fresh entry, history wiped
    ok, rec = g.apply_elevation(new, "RATIFIED", authority="mallory",
                                evidence=make_evidence(), superseded_entry=old)
    assert not ok and rec["reason_code"] == "SUPERSESSION_ERASES_AUTHORITY"
    assert new["truth_state"] == "CANDIDATE"


# --- Negative controls: legitimate transitions still pass -----------------

def test_legit_candidate_to_verified():
    e = make_entry("CANDIDATE")
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="naya-2", evidence=make_evidence())
    assert ok and rec["reason_code"] == "ELEVATED"
    assert e["truth_state"] == "VERIFIED"
    hist = e["elevation_history"]
    assert len(hist) == 1 and hist[0]["authority"] == "naya-2"
    assert hist[0]["evidence_hashes"] == [H1, H2]


def test_legit_verified_to_ratified():
    # Under the elevation-grant law (Option C, ratified 2026-10-06), a legit
    # VERIFIED->RATIFIED carries a director-issued grant. Without one it is
    # rejected (see test_elevation_grants.py).
    e = make_entry("VERIFIED")
    grant = g.make_grant(note_id="SN-9001", issuer="Shawn Vibert",
                         issuer_role="Human Director", expires_days=7)
    ok, _ = g.apply_elevation(e, "RATIFIED", authority="shawn",
                              evidence=make_evidence(), elevation_grants=[grant])
    assert ok and e["truth_state"] == "RATIFIED"


def test_legit_ratified_to_active_with_predecessor():
    e = make_entry("RATIFIED")
    pred = {"note_id": "SN-9001", "old_state": "CANDIDATE", "new_state": "VERIFIED",
            "promoter": "naya-2", "evidence_hashes": [H1]}
    pred["receipt_hash"] = g._canonical_hash(pred)
    ev = make_evidence()
    ev["predecessor_receipt"] = pred
    ok, rec = g.apply_elevation(e, "ACTIVE", authority="shawn", evidence=ev)
    assert ok and e["truth_state"] == "ACTIVE", rec


def test_legit_active_to_learned_with_behavioral():
    e = make_entry("ACTIVE")
    ev = make_evidence(types=["behavioral", "document"])
    ok, _ = g.apply_elevation(e, "LEARNED", authority="shawn", evidence=ev)
    assert ok and e["truth_state"] == "LEARNED"


def test_demotion_always_permitted():
    # Containment must never be blocked: RATIFIED->CANDIDATE with no
    # authority and no evidence still applies.
    e = make_entry("RATIFIED")
    ok, rec = g.apply_elevation(e, "CANDIDATE")
    assert ok and rec["reason_code"] == "DEMOTION_PERMITTED"
    assert e["truth_state"] == "CANDIDATE"


def test_noop_same_state():
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="x", evidence=make_evidence())
    assert ok and rec["reason_code"] == "NOOP_SAME_STATE"
    assert "elevation_history" not in e


# --- Rejection is a non-event ----------------------------------------------

def test_rejection_records_nothing():
    # The test a reviewer should read first: a rejected write must not
    # record a state, a history, or a receipt. A rejected write that
    # records itself is still a write.
    e = make_entry("CANDIDATE")
    before = snapshot(e)
    ok, _ = g.apply_elevation(e, "RATIFIED", authority="mallory", evidence=None)
    assert not ok
    assert snapshot(e) == before
    assert "elevation_history" not in e


# --- Edge cases -------------------------------------------------------------

def test_unknown_state_rejected():
    e = make_entry("CANDIDATE")
    ok, rec = g.apply_elevation(e, "BLESSED", authority="shawn", evidence=make_evidence())
    assert not ok and rec["reason_code"] == "UNKNOWN_STATE"
    assert e["truth_state"] == "CANDIDATE"


def test_anonymous_authority_rejected():
    e = make_entry("CANDIDATE")
    for anon in ("", "anonymous", "UNKNOWN", "  "):
        ok, rec = g.apply_elevation(e, "VERIFIED", authority=anon, evidence=make_evidence())
        assert not ok and rec["reason_code"] == "ELEVATION_REQUIRES_AUTHORITY", anon
    assert e["truth_state"] == "CANDIDATE"


def test_evidence_item_missing_hash_rejected():
    e = make_entry("CANDIDATE")
    ev = {"items": [{"type": "document", "source": "s"}]}  # no content_hash
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="naya-2", evidence=ev)
    assert not ok and rec["reason_code"] == "INVALID_EVIDENCE_ITEM"


def test_tampered_receipt_rejected():
    e = make_entry("CANDIDATE")
    ev = make_evidence()
    ev["receipt"]["promoter"] = "mallory"  # alter after hash computed
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="naya-2", evidence=ev)
    assert not ok and rec["reason_code"] == "RECEIPT_TAMPERED"


def test_authority_and_evidence_checked_separately():
    # Authority is checked first and independently: bad authority + good
    # evidence fails on authority; good authority + bad evidence fails on
    # evidence. The checks never conflate.
    e = make_entry("CANDIDATE")
    ok, rec = g.apply_elevation(e, "VERIFIED", authority=None, evidence=make_evidence())
    assert not ok and rec["reason_code"] == "ELEVATION_REQUIRES_AUTHORITY"
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="naya-2", evidence={"items": []})
    assert not ok and rec["reason_code"] == "ELEVATION_REQUIRES_EVIDENCE"


# --- Read side: semantic audit finds escalation on disk ---------------------

def test_audit_semantics_detects_disk_escalation():
    registry = {"entries": [
        {"smart_note_id": "SN-1", "truth_state": "RATIFIED"},  # no provenance
        {"smart_note_id": "SN-2", "truth_state": "ACTIVE",
         "elevation_history": [{"from": "CANDIDATE", "to": "ACTIVE",
                                "authority": "mallory", "evidence_hashes": [H1],
                                "evidence_types": ["document"], "at": "t", "kind": "elevation"}]},
        {"smart_note_id": "SN-3", "truth_state": "RATIFIED", "supersedes": "SN-0"},
    ]}
    r = g.audit_registry_semantics(registry)
    assert not r["ok"]
    assert r["defects"]["elevated_without_provenance"] == ["SN-1"]
    assert r["defects"]["active_without_verified_predecessor"] == ["SN-2"]
    assert r["defects"]["supersession_erased_history"] == ["SN-3"]


def test_audit_semantics_clean_registry_ok():
    registry = {"entries": [
        {"smart_note_id": "SN-1", "truth_state": "CANDIDATE"},
        {"smart_note_id": "SN-2", "truth_state": "RATIFIED",
         "elevation_history": [{"from": "CANDIDATE", "to": "RATIFIED",
                                "authority": "shawn", "evidence_hashes": [H1],
                                "evidence_types": ["document"], "at": "t", "kind": "elevation"}]},
        {"smart_note_id": "SN-3", "truth_state": "LEARNED",
         "elevation_history": [{"from": "ACTIVE", "to": "LEARNED",
                                "authority": "shawn", "evidence_hashes": [H1],
                                "evidence_types": ["behavioral"], "at": "t", "kind": "elevation"}]},
    ]}
    r = g.audit_registry_semantics(registry)
    assert r["ok"], r["defects"]
    assert r["defect_total"] == 0
