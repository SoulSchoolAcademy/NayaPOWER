"""Tier B scorecards are bound to the material diff, not merely the commit SHA."""
from tools.check_unified_pr_paperwork import (
    _scorecard_for_current_head,
    compute_diff_fingerprint,
)


def scorecard(head, diff_hash, verification=True):
    verification_line = (
        "Verification: tests run and replay behavior independently inspected\n"
        if verification else ""
    )
    return (
        "## SCORECARD\n"
        "Score: 9/10\n"
        f"Head SHA: {head}\n"
        f"Diff-SHA256: {diff_hash}\n"
        + verification_line
        + "Seat: Naya Delta"
    )


def test_tier_b_reuses_scorecard_if_commit_changes_but_material_diff_does_not():
    old_head, current_head, diff_hash = "a" * 40, "b" * 40, "d" * 64
    ok, detail = _scorecard_for_current_head(
        [{"body": scorecard(old_head, diff_hash)}],
        current_head,
        "Naya Alpha",
        9.0,
        tier="B",
        diff_hash=diff_hash,
    )
    assert ok
    assert "material diff fingerprint matches" in detail


def test_tier_b_rejects_scorecard_when_material_diff_changes():
    old_head, current_head = "a" * 40, "b" * 40
    ok, _ = _scorecard_for_current_head(
        [{"body": scorecard(old_head, "d" * 64)}],
        current_head,
        "Naya Alpha",
        9.0,
        tier="B",
        diff_hash="e" * 64,
    )
    assert not ok


def test_tier_b_requires_verification_attestation():
    head, diff_hash = "b" * 40, "d" * 64
    ok, _ = _scorecard_for_current_head(
        [{"body": scorecard(head, diff_hash, verification=False)}],
        head,
        "Naya Alpha",
        9.0,
        tier="B",
        diff_hash=diff_hash,
    )
    assert not ok


def test_diff_fingerprint_is_deterministic_and_changes_with_patch():
    files = [{
        "filename": "tools/a.py",
        "status": "modified",
        "sha": "a" * 40,
        "patch": "@@ -1 +1 @@",
        "additions": 1,
        "deletions": 1,
    }]
    first = compute_diff_fingerprint(files)
    assert first == compute_diff_fingerprint(list(files))
    changed = [dict(files[0], patch="@@ -1 +2 @@")]
    assert first != compute_diff_fingerprint(changed)
