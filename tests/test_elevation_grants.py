"""Elevation-grant regression suite (Option C, ratified 2026-10-06).

VERIFIED->RATIFIED requires a valid, unexpired capability grant naming the
note. All other transitions are unaffected. Rejection is a non-event.

Conventions: the guard module is loaded standalone via importlib (no repo
imports), tests run against plain dicts.
"""
import copy
import importlib.util
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "truth_state_guard", ROOT / "tools" / "truth_state_guard.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

H1 = "a" * 64
H2 = "b" * 64


def make_entry(state="VERIFIED", sn="SN-9001"):
    return {"smart_note_id": sn, "intelligent_block_id": "IB-9001",
            "truth_state": state}


def make_evidence():
    items = [{"type": "document", "source": "src-0", "content_hash": H1},
             {"type": "test-report", "source": "src-1", "content_hash": H2}]
    receipt = {"note_id": "SN-9001", "old_state": "VERIFIED",
               "new_state": "RATIFIED", "promoter": "Shawn Vibert",
               "evidence_hashes": [H1, H2]}
    receipt["receipt_hash"] = g._canonical_hash(receipt)
    return {"items": items, "receipt": receipt}


def make_grant(sn="SN-9001", **kw):
    kw.setdefault("note_id", sn)
    return g.make_grant(**kw)


def snapshot(entry):
    return json.dumps(entry, sort_keys=True)


def ts(days_offset):
    dt = datetime.now(timezone.utc) + timedelta(days=days_offset)
    return dt.strftime("%Y%m%dT%H%M%SZ")


# --- Core grant-gating cases ---------------------------------------------

def test_no_grant_ratified_rejected():
    e = make_entry("VERIFIED")
    before = snapshot(e)
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[])
    assert not ok and rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert snapshot(e) == before


def test_no_grant_arg_ratified_rejected():
    # elevation_grants=None (not passed) must also reject.
    e = make_entry("VERIFIED")
    before = snapshot(e)
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence())
    assert not ok and rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert snapshot(e) == before


def test_expired_grant_rejected():
    grant = make_grant()
    # Backdate the grant so it is expired, then re-hash to keep integrity.
    body = {k: v for k, v in grant.items() if k != "grant_hash"}
    body["issued_at"] = ts(-10)
    body["expires_at"] = ts(-3)
    grant = dict(body, grant_hash=g._canonical_hash(body))
    e = make_entry("VERIFIED")
    before = snapshot(e)
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert not ok and rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert "GRANT_EXPIRED" in rec["detail"]
    assert snapshot(e) == before


def test_wrong_note_grant_rejected():
    grant = make_grant(sn="SN-OTHER")
    e = make_entry("VERIFIED", sn="SN-9001")
    before = snapshot(e)
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert not ok and rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert "GRANT_NOTE_MISMATCH" in rec["detail"]
    assert snapshot(e) == before


def test_valid_grant_accepted():
    grant = make_grant()
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert ok and rec["reason_code"] == "ELEVATED"
    assert e["truth_state"] == "RATIFIED"
    hist = e["elevation_history"][-1]
    assert hist["elevation_grant_id"] == grant["grant_id"]


def test_tampered_grant_rejected():
    grant = make_grant()
    grant["scope_note"] = "attacker was here"  # breaks grant_hash
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert not ok and rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert "GRANT_TAMPERED" in rec["detail"]
    assert e["truth_state"] == "VERIFIED"


def test_non_director_issuer_rejected():
    grant = make_grant(issuer="mallory", issuer_role="Operator")
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="mallory",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert not ok
    assert "GRANT_UNAUTHORIZED_ISSUER" in rec["detail"]
    assert e["truth_state"] == "VERIFIED"


def test_delegate_grant_accepted():
    grant = make_grant(issuer="Naya 4", issuer_role="Delegate",
                       delegated_by="Shawn Vibert")
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Naya 4",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert ok and rec["reason_code"] == "ELEVATED"
    assert e["truth_state"] == "RATIFIED"


def test_delegate_without_director_delegator_rejected():
    grant = make_grant(issuer="Naya 4", issuer_role="Delegate",
                       delegated_by="mallory")
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Naya 4",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert not ok and "GRANT_INVALID" in rec["detail"]
    assert e["truth_state"] == "VERIFIED"


# --- Non-RATIFIED transitions unaffected ----------------------------------

def test_demotion_without_grant_permitted():
    e = make_entry("RATIFIED")
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="naya-2")
    assert ok and rec["reason_code"] == "DEMOTION_PERMITTED"
    assert e["truth_state"] == "VERIFIED"


def test_candidate_to_verified_without_grant_unaffected():
    e = make_entry("CANDIDATE")
    ok, rec = g.apply_elevation(e, "VERIFIED", authority="naya-2",
                                evidence=make_evidence())
    assert ok and rec["reason_code"] == "ELEVATED"
    assert e["truth_state"] == "VERIFIED"


def test_verified_to_testing_demotion_without_grant():
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "TESTING", authority="naya-2")
    assert ok and rec["reason_code"] == "DEMOTION_PERMITTED"


def test_grant_ignored_for_non_ratified_target():
    # A grant present but transition is VERIFIED->ACTIVE: grant not consulted,
    # ACTIVE's own predecessor rule still applies (and fails here).
    grant = make_grant()
    e = make_entry("VERIFIED")
    ok, rec = g.apply_elevation(e, "ACTIVE", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert not ok and rec["reason_code"] == "ACTIVE_REQUIRES_VERIFIED_PREDECESSOR"


def test_grant_note_id_case_insensitive():
    grant = make_grant(sn="sn-9001")  # lowercase in, normalized upper
    e = make_entry("VERIFIED", sn="SN-9001")
    ok, rec = g.apply_elevation(e, "RATIFIED", authority="Shawn Vibert",
                                evidence=make_evidence(), elevation_grants=[grant])
    assert ok


def test_make_grant_self_validates():
    grant = g.make_grant(note_id="SN-1", expires_days=7)
    ok, rec = g.validate_grant(grant, "SN-1", "RATIFIED")
    assert ok and rec["reason_code"] == "GRANT_OK"


# --- Read-side audit: grant defect class ----------------------------------

def test_audit_flags_ratified_without_grant():
    # An entry with a recorded VERIFIED->RATIFIED transition but no grant_id
    # is flagged by the audit.
    registry = {"entries": [{
        "smart_note_id": "SN-9001", "truth_state": "RATIFIED",
        "elevation_history": [
            {"from": "VERIFIED", "to": "RATIFIED", "authority": "Shawn Vibert",
             "evidence_hashes": [H1], "at": "t", "kind": "elevation"},
        ],
    }]}
    audit = g.audit_registry_semantics(registry)
    assert "SN-9001" in audit["defects"]["ratified_without_elevation_grant"]


def test_audit_passes_ratified_with_grant():
    grant = make_grant()
    registry = {"entries": [{
        "smart_note_id": "SN-9001", "truth_state": "RATIFIED",
        "elevation_history": [
            {"from": "VERIFIED", "to": "RATIFIED", "authority": "Shawn Vibert",
             "evidence_hashes": [H1], "at": "t", "kind": "elevation",
             "elevation_grant_id": grant["grant_id"]},
        ],
    }]}
    audit = g.audit_registry_semantics(registry)
    assert audit["defects"]["ratified_without_elevation_grant"] == []
