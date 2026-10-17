"""Firing proofs for the truth guard's refusal surface (W5 guard_liveness wiring).

tools/guard_liveness.py now enumerates the refusal literals of
tools/truth_state_guard.py (the truth enforcement guard wired into
smart_note_v2.promote_note, the canonical write path). A refusal literal
with no executed test observing it is a guard that cannot be seen to fire
(SN-0468). These tests execute the guard and assert each refusal as an
observed outcome -- a source grep does not count (SN-0461).

Covered here: the eight refusal paths that had no firing proof when the
truth guard was wired into the liveness scan. The other paths were already
observed by test_truth_state_poison.py, test_elevation_grants.py and
test_grant_auto_renewal.py.

Conventions: guard module loaded standalone via importlib (no repo imports),
tests run against plain dicts.
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


def make_expired_grant(sn="SN-9001"):
    """A grant that expired yesterday (issued 10 days ago, 7-day term)."""
    issued = ts(-10)
    return g.make_grant(note_id=sn, target_state="RATIFIED",
                        issuer="Shawn Vibert", issuer_role="Human Director",
                        expires_days=7, issued_at=issued)


def make_receipt(sn="SN-9001", **over):
    receipt = {
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
        "step5_receipt": {"receipt_posted_comment_id": 6073861838},
    }
    receipt.update(over)
    return receipt


def test_grant_naming_wrong_target_state_is_refused():
    grant = g.make_grant(note_id="SN-9001", target_state="VERIFIED",
                         issuer="Shawn Vibert", issuer_role="Human Director",
                         expires_days=7, issued_at=ts(0))
    ok, rec = g.validate_grant(grant, "SN-9001", "RATIFIED", now=ts(0))
    assert not ok
    assert rec["reason_code"] == "GRANT_STATE_MISMATCH"


def test_non_object_entry_is_refused():
    ok, rec = g.apply_elevation("not-a-dict", "VERIFIED")
    assert not ok
    assert rec["reason_code"] == "INVALID_ENTRY"


def test_promotion_authority_with_no_note_named_is_refused():
    grant, rec = g.issue_promotion_authority(
        {"verification_passed": True, "verification_id": "V-1"},
        note_id="", target_state="RATIFIED")
    assert grant is None
    assert rec["reason_code"] == "PROMOTION_AUTHORITY_INVALID"


def test_receipt_with_unauthorized_scope_action_is_refused():
    receipt = make_receipt(scope_action="bogus_action")
    ok, rec = g.check_receipt_authority(receipt, "SN-9001", "RATIFIED")
    assert not ok
    assert rec["reason_code"] == "RECEIPT_ACTION_MISMATCH"


def test_receipt_enumerating_fewer_than_two_options_is_refused():
    receipt = make_receipt()
    receipt["step1_enumerate"] = {"options": [{"id": "promote"}]}
    ok, rec = g.check_receipt_authority(receipt, "SN-9001", "RATIFIED")
    assert not ok
    assert rec["reason_code"] == "RECEIPT_STEP1"


def test_receipt_whose_winner_is_not_the_promotion_option_is_refused():
    receipt = make_receipt(promotion_option_id="hold")
    ok, rec = g.check_receipt_authority(receipt, "SN-9001", "RATIFIED")
    assert not ok
    assert rec["reason_code"] == "RECEIPT_WINNER_MISMATCH"


def test_renewal_with_invalidated_verification_is_blocked():
    grant = make_expired_grant()
    ok, receipt, rec = g.evaluate_renewal(
        grant,
        {"verification_valid": False, "scope_unchanged": True,
         "objections": [], "renewal_term_days": 7},
        now=ts(0))
    assert not ok and receipt is None
    assert rec["reason_code"] == "RENEWAL_BLOCKED"


def test_renewal_of_a_non_object_grant_is_refused():
    ok, receipt, rec = g.evaluate_renewal("not-a-grant", {}, now=ts(0))
    assert not ok and receipt is None
    assert rec["reason_code"] == "RENEWAL_INVALID"
