"""Grant auto-renewal + receipt-as-authority + instant promotion tests.

Shawn directive 2026-10-08: expiring grants that stall learning make no
sense. Expiry is a review checkpoint, not a cliff.

Covered:
  1. AUTO-RENEWAL — expired grant + valid verification -> renewed;
     expired grant + invalidated verification -> stays expired;
     scope changed / objections / live grant -> no renewal.
  2. RECEIPT-AS-AUTHORITY — valid SN-0340 five-step receipt without any
     grant -> accepted; tampered/failed/stale/mismatched -> rejected.
  3. INSTANT PROMOTION — passing verification auto-issues authority;
     failed verification -> refused (fail-closed).

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

H1 = "a" * 64
H2 = "b" * 64


def ts(days_offset):
    dt = datetime.now(timezone.utc) + timedelta(days=days_offset)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def make_expired_grant(sn="SN-9001"):
    """A grant that expired yesterday (issued 10 days ago, 7-day term)."""
    issued = ts(-10)
    grant = g.make_grant(note_id=sn, target_state="RATIFIED",
                         issuer="Shawn Vibert", issuer_role="Human Director",
                         expires_days=7, issued_at=issued)
    return grant


def good_verification_state(**over):
    vs = {"verification_valid": True,
          "scope_unchanged": True,
          "objections": [],
          "renewal_term_days": 7}
    vs.update(over)
    return vs


def make_receipt(sn="SN-9001", **over):
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
        "step5_receipt": {"receipt_posted_comment_id": 6064117129},
    }
    r.update(over)
    return r


# ---------------------------------------------------------------------------
# 1. AUTO-RENEWAL
# ---------------------------------------------------------------------------

def test_expired_grant_with_valid_verification_renews():
    grant = make_expired_grant()
    ok, rec = g.validate_grant(grant, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "GRANT_EXPIRED"
    # The core falsifier: same expired grant, renewal attempted, valid state.
    ok, rec = g.validate_grant(grant, "SN-9001", "RATIFIED",
                               attempt_renewal=True,
                               verification_state=good_verification_state())
    assert ok, rec
    assert rec["reason_code"] == "GRANT_RENEWED"


def test_evaluate_renewal_produces_sealed_receipt():
    grant = make_expired_grant()
    renewable, receipt, rec = g.evaluate_renewal(
        grant, good_verification_state(), now=ts(0))
    assert renewable and receipt is not None
    assert receipt["grant_id"] == grant["grant_id"]
    assert receipt["new_expires_at"] > grant["expires_at"]
    assert receipt["renewal_chain"] == [receipt["renewal_id"]]
    body = {k: v for k, v in receipt.items() if k != "renewal_hash"}
    assert receipt["renewal_hash"] == g._canonical_hash(body)


def test_expired_grant_with_invalid_verification_stays_expired():
    grant = make_expired_grant()
    ok, rec = g.validate_grant(
        grant, "SN-9001", "RATIFIED", attempt_renewal=True,
        verification_state=good_verification_state(verification_valid=False))
    assert not ok
    assert rec["reason_code"] == "GRANT_EXPIRED"


def test_expired_grant_with_changed_scope_stays_expired():
    grant = make_expired_grant()
    ok, rec = g.validate_grant(
        grant, "SN-9001", "RATIFIED", attempt_renewal=True,
        verification_state=good_verification_state(scope_unchanged=False))
    assert not ok and rec["reason_code"] == "GRANT_EXPIRED"


def test_expired_grant_with_objections_stays_expired():
    grant = make_expired_grant()
    ok, rec = g.validate_grant(
        grant, "SN-9001", "RATIFIED", attempt_renewal=True,
        verification_state=good_verification_state(objections=["seat-2 disputes evidence"]))
    assert not ok and rec["reason_code"] == "GRANT_EXPIRED"


def test_live_grant_needs_no_renewal():
    grant = g.make_grant(note_id="SN-9001", target_state="RATIFIED",
                         expires_days=7, issued_at=ts(0))
    renewable, receipt, rec = g.evaluate_renewal(
        grant, good_verification_state(), now=ts(0))
    assert not renewable and receipt is None
    assert rec["reason_code"] == "RENEWAL_NOT_NEEDED"


def test_renewal_without_attempt_flag_stays_expired():
    # Backward compatibility: default path still treats expiry as a cliff.
    grant = make_expired_grant()
    ok, rec = g.validate_grant(grant, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "GRANT_EXPIRED"


# ---------------------------------------------------------------------------
# 2. RECEIPT-AS-AUTHORITY
# ---------------------------------------------------------------------------

def test_valid_receipt_without_grant_accepted_as_authority():
    ok, rec = g.check_receipt_authority(make_receipt(), "SN-9001", "RATIFIED")
    assert ok, rec
    assert rec["reason_code"] == "RECEIPT_AUTHORITY_OK"


def test_tampered_receipt_rejected():
    # A receipt whose scores were altered after the fact must not authorize.
    r = make_receipt()
    r["step2_score"]["scores"]["hold"]["value"] = 99  # out of range
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok
    assert rec["reason_code"] == "RECEIPT_STEP2"


def test_receipt_with_failed_gate_rejected():
    r = make_receipt(step3_gate={"no_major_damage": False,
                                 "positive_forward_effect": True,
                                 "reversible": True})
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "RECEIPT_STEP3"


def test_receipt_with_losing_winner_rejected():
    r = make_receipt()
    r["step4_decide"] = dict(r["step4_decide"], winner="hold")
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "RECEIPT_STEP4"


def test_stale_receipt_rejected():
    old = (datetime.now(timezone.utc) - timedelta(days=8)).isoformat()
    r = make_receipt(decided_at=old)
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "RECEIPT_STALE"


def test_receipt_scope_mismatch_rejected():
    r = make_receipt(sn="SN-9999")
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "RECEIPT_SCOPE_MISMATCH"


def test_anonymous_receipt_rejected():
    r = make_receipt(decided_by="system")
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "RECEIPT_ANONYMOUS"


def test_private_receipt_not_authority():
    r = make_receipt(step5_receipt={})
    ok, rec = g.check_receipt_authority(r, "SN-9001", "RATIFIED")
    assert not ok and rec["reason_code"] == "RECEIPT_STEP5"


def test_elevation_accepts_receipt_when_no_grant():
    entry = {"smart_note_id": "SN-9001", "truth_state": "VERIFIED"}
    ok, rec = g.check_elevation_grant(entry, "RATIFIED", [],
                                      elevation_receipts=[make_receipt()])
    assert ok, rec
    assert rec["reason_code"] == "RECEIPT_AUTHORITY_OK"


def test_elevation_rejects_when_both_grant_and_receipt_bad():
    entry = {"smart_note_id": "SN-9001", "truth_state": "VERIFIED"}
    bad_grant = make_expired_grant()
    bad_receipt = make_receipt(step3_gate={"no_major_damage": False,
                                           "positive_forward_effect": True,
                                           "reversible": True})
    ok, rec = g.check_elevation_grant(entry, "RATIFIED", [bad_grant],
                                      elevation_receipts=[bad_receipt])
    assert not ok
    assert rec["reason_code"] == "RATIFIED_REQUIRES_ELEVATION_GRANT"


# ---------------------------------------------------------------------------
# 3. INSTANT PROMOTION PATH
# ---------------------------------------------------------------------------

def test_passing_verification_auto_issues_authority():
    vr = {"verification_passed": True, "verification_id": "VRF-20261008-001",
          "evidence": {"method": "independent-recompute", "result": "pass"}}
    grant, rec = g.issue_promotion_authority(vr, "SN-9001", "RATIFIED")
    assert grant is not None, rec
    assert rec["reason_code"] == "PROMOTION_AUTHORITY_ISSUED"
    assert grant["note_id"] == "SN-9001"
    assert grant["auto_issued"] is True
    assert grant["verification_id"] == "VRF-20261008-001"
    # The issued grant must itself validate.
    ok, vrec = g.validate_grant(grant, "SN-9001", "RATIFIED")
    assert ok, vrec


def test_failed_verification_issues_nothing():
    vr = {"verification_passed": False, "verification_id": "VRF-20261008-002"}
    grant, rec = g.issue_promotion_authority(vr, "SN-9001", "RATIFIED")
    assert grant is None
    assert rec["reason_code"] == "PROMOTION_AUTHORITY_REFUSED"


def test_ambiguous_verification_issues_nothing():
    vr = {"verification_id": "VRF-20261008-003"}  # no verification_passed key
    grant, rec = g.issue_promotion_authority(vr, "SN-9001", "RATIFIED")
    assert grant is None
    assert rec["reason_code"] == "PROMOTION_AUTHORITY_REFUSED"


# ---------------------------------------------------------------------------
# DB grant normalization
# ---------------------------------------------------------------------------

def test_normalize_db_grant_maps_row_to_canonical_shape():
    row = {
        "grant_id": "957d1de3-5e1c-4126-a90d-d6267f1d133b",
        "scope": {"target": "IB-NAYA-FLOW-LESSON-919db63a63784f3ba6bad79c7db1edb7"},
        "status": "ACTIVE",
        "issued_at": "2026-10-02T21:04:37.875154+00:00",
        "expires_at": "2026-10-09T21:04:37.875154+00:00",
    }
    grant = g.normalize_db_grant(row)
    assert grant is not None
    assert grant["grant_id"] == "957d1de3-5e1c-4126-a90d-d6267f1d133b"
    assert grant["note_id"] == "IB-NAYA-FLOW-LESSON-919DB63A63784F3BA6BAD79C7DB1EDB7"
    assert grant["db_status"] == "ACTIVE"
    # Canonical shape: timestamps parse, hash present.
    assert g._parse_grant_ts(grant["expires_at"]) is not None
    assert grant["grant_hash"]


def test_normalize_db_grant_rejects_non_dict():
    assert g.normalize_db_grant(None) is None
    assert g.normalize_db_grant("not-a-row") is None
