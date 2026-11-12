"""Canonical-path self-healing: the real elevation seam must reach the
grant-auto-renewal and receipt-as-authority machinery, not just the
low-level functions.

Shawn directive 2026-10-08 ("Make it what it should be and make it
right"): expiry is a review checkpoint, not a cliff — but the rebuilt
machinery was unreachable on the canonical path because
apply_elevation() never threaded attempt_renewal/verification_state/
receipts through. This file pins the wiring shut:

  - apply_elevation VERIFIED->RATIFIED with an expired-but-renewable
    grant + verification_state -> auto-renews and elevates (GRANT_RENEWED).
  - Same, but no verification_state / invalidated verification /
    objections -> stays expired (fail-closed, unchanged default).
  - apply_elevation with a valid SN-0340 receipt and no grants ->
    elevates via RECEIPT_AUTHORITY_OK.
  - check_elevation_grant defaults attempt_renewal=True (fail-closed
    preserved: no verification_state -> GRANT_EXPIRED).
  - Tampered grants are not curable by renewal.

Conventions: guard module loaded standalone via importlib (no repo imports).
"""
import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "truth_state_guard", ROOT / "tools" / "truth_state_guard.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def ts(days_offset):
    dt = datetime.now(timezone.utc) + timedelta(days=days_offset)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def make_expired_grant(sn="SN-9101"):
    issued = ts(-10)
    return g.make_grant(note_id=sn, target_state="RATIFIED",
                        issuer="Shawn Vibert", issuer_role="Human Director",
                        expires_days=7, issued_at=issued)


def make_live_grant(sn="SN-9101"):
    return g.make_grant(note_id=sn, target_state="RATIFIED",
                        issuer="Shawn Vibert", issuer_role="Human Director",
                        expires_days=7)


def good_vs(**over):
    vs = {"verification_valid": True, "scope_unchanged": True,
          "objections": [], "renewal_term_days": 7}
    vs.update(over)
    return vs


def good_evidence():
    return {"items": [{"type": "verification", "source": "test",
                       "content_hash": "a" * 64}]}


def verified_entry(sn="SN-9101"):
    return {"truth_state": "VERIFIED", "intelligent_block_id": sn}


def make_receipt(sn="SN-9101", **over):
    r = {
        "scope_target": sn,
        "scope_action": "learning_lock_in",
        "decided_by": "Naya 5",
        "decided_at": datetime.now(timezone.utc).isoformat(),
        "promotion_option_id": "promote",
        "step1_enumerate": {"options": [{"id": "promote"}, {"id": "hold"}]},
        "step2_score": {"scores": {
            "promote": {"value": 9, "consequences": 8,
                        "mission_vision_alignment": 9, "situational_awareness": 8},
            "hold": {"value": 4, "consequences": 5,
                     "mission_vision_alignment": 4, "situational_awareness": 5},
        }},
        "step3_gate": {"no_major_damage": True,
                       "positive_forward_effect": True, "reversible": True},
        "step4_decide": {
            "winner": "promote",
            "strongest_alternative": {"summary": "Hold for another verification cycle"},
            "falsifier": "A second independent verification run contradicts the first",
        },
        "step5_receipt": {"receipt_posted_comment_id": 6069650144},
    }
    r.update(over)
    return r


# ---------------------------------------------------------------------------
# Canonical path: expired grant + verification -> self-heals
# ---------------------------------------------------------------------------

def test_apply_elevation_renews_expired_grant_on_canonical_path():
    entry = verified_entry()
    ok, rec = g.apply_elevation(entry, "RATIFIED", authority="director",
                                evidence=good_evidence(),
                                elevation_grants=[make_expired_grant()],
                                verification_state=good_vs())
    assert ok, rec
    assert entry["truth_state"] == "RATIFIED"
    # Elevation history records the renewed grant.
    hist = entry.get("elevation_history") or []
    assert hist and hist[-1]["elevation_grant_id"].startswith("EG-")


def test_apply_elevation_no_verification_state_stays_expired():
    entry = verified_entry()
    ok, rec = g.apply_elevation(entry, "RATIFIED", authority="director",
                                evidence=good_evidence(),
                                elevation_grants=[make_expired_grant()])
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert entry["truth_state"] == "VERIFIED"  # rejection is a non-event


def test_apply_elevation_invalidated_verification_stays_expired():
    entry = verified_entry()
    ok, rec = g.apply_elevation(
        entry, "RATIFIED", authority="director", evidence=good_evidence(),
        elevation_grants=[make_expired_grant()],
        verification_state=good_vs(verification_valid=False))
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert entry["truth_state"] == "VERIFIED"


def test_apply_elevation_objections_block_renewal():
    entry = verified_entry()
    ok, rec = g.apply_elevation(
        entry, "RATIFIED", authority="director", evidence=good_evidence(),
        elevation_grants=[make_expired_grant()],
        verification_state=good_vs(objections=["scope review pending"]))
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"


def test_apply_elevation_scope_drift_blocks_renewal():
    entry = verified_entry()
    ok, rec = g.apply_elevation(
        entry, "RATIFIED", authority="director", evidence=good_evidence(),
        elevation_grants=[make_expired_grant()],
        verification_state=good_vs(scope_unchanged=False))
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"


# ---------------------------------------------------------------------------
# Canonical path: receipt-as-authority
# ---------------------------------------------------------------------------

def test_apply_elevation_accepts_valid_receipt_without_grant():
    entry = verified_entry()
    ok, rec = g.apply_elevation(entry, "RATIFIED", authority="director",
                                evidence=good_evidence(),
                                elevation_grants=[],
                                elevation_receipts=[make_receipt()])
    assert ok, rec
    assert entry["truth_state"] == "RATIFIED"
    hist = entry.get("elevation_history") or []
    assert hist and hist[-1]["to"] == "RATIFIED"  # no grant: receipt path


def test_apply_elevation_rejects_stale_receipt():
    receipt = make_receipt(decided_at=(datetime.now(timezone.utc)
                                       - timedelta(days=8)).isoformat())
    entry = verified_entry()
    ok, rec = g.apply_elevation(entry, "RATIFIED", authority="director",
                                evidence=good_evidence(),
                                elevation_grants=[],
                                elevation_receipts=[receipt])
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert entry["truth_state"] == "VERIFIED"


# ---------------------------------------------------------------------------
# Default flip is fail-closed
# ---------------------------------------------------------------------------

def test_check_elevation_grant_defaults_to_attempt_renewal():
    import inspect
    default = inspect.signature(g.check_elevation_grant).parameters[
        "attempt_renewal"].default
    assert default is True


def test_default_flip_renews_with_verification_state():
    entry = verified_entry()
    ok, rec = g.check_elevation_grant(entry, "RATIFIED",
                                      [make_expired_grant()],
                                      verification_state=good_vs())
    assert ok, rec
    assert rec["reason_code"] == "GRANT_OK"
    assert "auto-renewed" in rec["detail"]


def test_default_flip_stays_expired_without_verification_state():
    entry = verified_entry()
    ok, rec = g.check_elevation_grant(entry, "RATIFIED", [make_expired_grant()])
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert "GRANT_EXPIRED" in rec["detail"]


def test_tampered_grant_not_curable_by_renewal():
    grant = make_expired_grant()
    grant["issuer"] = "Someone Else"  # breaks the sealed hash
    entry = verified_entry()
    ok, rec = g.check_elevation_grant(entry, "RATIFIED", [grant],
                                      verification_state=good_vs())
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"
    assert "GRANT_TAMPERED" in rec["detail"]


def test_live_grant_still_grant_ok():
    entry = verified_entry()
    ok, rec = g.check_elevation_grant(entry, "RATIFIED", [make_live_grant()],
                                      verification_state=good_vs())
    assert ok, rec
    assert rec["reason_code"] == "GRANT_OK"
