"""Explicit blocking findings persist until the same declared seat clears them."""
from tools.check_unified_pr_paperwork import _has_unresolved_hold


def test_unresolved_cross_seat_hold_blocks():
    comments = [{
        "created_at": "2026-10-21T10:00:00Z",
        "body": "Seat: Naya Delta\nVERDICT: HOLD\nFinding: authorization bypass remains reachable.",
    }]
    blocked, reason, cure, owner = _has_unresolved_hold(
        comments, "Naya Alpha", "a" * 40, "A", None
    )
    assert blocked
    assert "Naya Delta" in reason
    assert "same reviewing seat" in cure
    assert owner == "Reviewing seat"


def test_same_seat_current_head_pass_clears_hold():
    head = "b" * 40
    comments = [
        {
            "created_at": "2026-10-21T10:00:00Z",
            "body": "Seat: Naya Delta\nVERDICT: HOLD\nFinding: authorization bypass remains reachable.",
        },
        {
            "created_at": "2026-10-21T11:00:00Z",
            "body": f"Seat: Naya Delta\nVERDICT: PASS\nHead SHA: {head}\nFinding resolved and retested.",
        },
    ]
    blocked, _, _, _ = _has_unresolved_hold(comments, "Naya Alpha", head, "A", None)
    assert not blocked


def test_unattributed_hold_fails_closed():
    comments = [{"body": "VERDICT: HOLD\nFinding: missing reviewer identity."}]
    blocked, reason, _, owner = _has_unresolved_hold(comments, "Naya Alpha", "a" * 40, "A", None)
    assert blocked
    assert "no declared reviewer seat" in reason
    assert owner == "Reviewing lane"


def test_tier_b_hold_clears_with_same_material_diff():
    old_head, current_head, diff_hash = "a" * 40, "b" * 40, "d" * 64
    comments = [
        {"created_at": "2026-10-21T10:00:00Z", "body": "Seat: Naya Delta\nVERDICT: HOLD\nFinding: test failure."},
        {"created_at": "2026-10-21T11:00:00Z", "body": f"Seat: Naya Delta\nVERDICT: PASS\nHead SHA: {old_head}\nDiff-SHA256: {diff_hash}\nFinding resolved and retested."},
    ]
    blocked, _, _, _ = _has_unresolved_hold(comments, "Naya Alpha", current_head, "B", diff_hash)
    assert not blocked
