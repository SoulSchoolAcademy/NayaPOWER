"""P0 value-density: a submitted PR review must carry its own scorecard,
triggering BOTH existing pull_request_review workflows without issue_comment.

Negative controls: stale head, same author seat, dismissed review, and hold.
"""
import pytest

from tools import check_merge_consensus as consensus
from tools import check_unified_pr_paperwork as paperwork

HEAD = "a" * 40
REPO = "SoulSchoolAcademy/NayaPOWER"
PR = 2938
DIFF = "b" * 64


def receipt(seat="Naya Gpt-6", head=HEAD, score="9.5", verdict=True):
    approval = "[NAYA GPT-6 · REVIEW] APPROVED\n" if verdict else ""
    return (
        f"Seat: {seat}\n"
        + approval
        + "## SCORECARD\n"
        + f"Head SHA: {head}\n"
        + f"Diff-SHA256: {DIFF}\n"
        + f"Scorecard: {score}/10\n"
        + "Verification: independently checked trigger scope, dispatch, and refusal controls\n"
    )


def run_consensus(monkeypatch, review):
    pr = {"created_at": "2026-10-22T17:00:00Z",
          "user": {"login": "SoulSchoolAcademy"},
          "body": "Seat: Naya Resolve"}
    def fetch(url, token):
        if url.endswith(f"/pulls/{PR}"):
            return pr
        if url.endswith(f"/pulls/{PR}/reviews"):
            return [review]
        if url.endswith(f"/issues/{PR}/comments"):
            return []
        raise AssertionError(url)
    monkeypatch.setattr(consensus, "api_get", fetch)
    consensus.run_gate("fake-token", REPO, PR, HEAD)


def test_submitted_review_automatically_qualifies_cross_seat_consensus(monkeypatch, capsys):
    run_consensus(monkeypatch, {"state": "COMMENTED", "body": receipt(),
                              "user": {"login": "SoulSchoolAcademy"}})
    assert "CONSENSUS GATE PASSED" in capsys.readouterr().out


@pytest.mark.parametrize("review", [
    {"state": "COMMENTED", "body": receipt(seat="Naya Resolve")},
    {"state": "COMMENTED", "body": receipt(head="c" * 40)},
    {"state": "DISMISSED", "body": receipt()},
    {"state": "PENDING", "body": receipt()},
    {"state": "CHANGES_REQUESTED", "body": receipt()},
])
def test_invalid_review_cannot_grant_consensus(monkeypatch, review):
    with pytest.raises(SystemExit) as exc:
        run_consensus(monkeypatch, review)
    assert exc.value.code == 1


def run_paperwork(monkeypatch, review, capsys):
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.setenv("GH_TOKEN", "fake-token")
    monkeypatch.setenv("PR_NUMBER", str(PR))
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    monkeypatch.setattr(paperwork, "_read_event", lambda: {})
    monkeypatch.setattr(paperwork, "compute_diff_fingerprint", lambda files: DIFF)
    monkeypatch.setattr(paperwork.receipt, "main", lambda: None)
    pr = {"head": {"sha": HEAD}, "body": "Seat: Naya Resolve",
          "title": "Tier A gate trigger repair", "changed_files": 1}
    files = [{"filename": ".github/workflows/merge-consensus-gate.yml",
              "status": "modified", "additions": 1, "deletions": 1, "changes": 2}]
    def fetch(url, token):
        if url.endswith(f"/pulls/{PR}"):
            return pr
        if url.endswith(f"/pulls/{PR}/files"):
            return files
        if url.endswith(f"/issues/{PR}/comments"):
            return []
        if url.endswith(f"/pulls/{PR}/reviews"):
            return [review]
        raise AssertionError(url)
    monkeypatch.setattr(paperwork.consensus, "api_get", fetch)
    rc = paperwork.run()
    return rc, capsys.readouterr().out


def test_submitted_review_carries_current_head_paperwork(monkeypatch, capsys):
    rc, out = run_paperwork(monkeypatch, {"state": "COMMENTED",
                                         "body": receipt()}, capsys)
    assert rc == 0, out
    assert "UNIFIED PAPERWORK GATE: PASS" in out


@pytest.mark.parametrize("review", [
    {"state": "COMMENTED", "body": receipt(seat="Naya Resolve")},
    {"state": "COMMENTED", "body": receipt(head="c" * 40)},
    {"state": "COMMENTED", "body": receipt(score="9.0")},
    {"state": "DISMISSED", "body": receipt()},
    {"state": "PENDING", "body": receipt()},
    {"state": "CHANGES_REQUESTED", "body": receipt()},
])
def test_invalid_review_cannot_grant_paperwork(monkeypatch, capsys, review):
    rc, out = run_paperwork(monkeypatch, review, capsys)
    assert rc != 0
    assert "SCORECARD_MISSING_OR_STALE" in out


def test_submitted_hold_refuses_even_with_separate_valid_review(monkeypatch, capsys):
    # Deliberate hold from the reviewing seat must not be overridden by
    # a second review body that happens to include a qualifying scorecard.
    monkeypatch.setenv("REPO", REPO)
    monkeypatch.setenv("GH_TOKEN", "fake-token")
    monkeypatch.setenv("PR_NUMBER", str(PR))
    monkeypatch.setattr(paperwork, "_read_event", lambda: {})
    monkeypatch.setattr(paperwork, "compute_diff_fingerprint", lambda files: DIFF)
    pr = {"head": {"sha": HEAD}, "body": "Seat: Naya Resolve",
          "title": "Tier A gate trigger repair", "changed_files": 1}
    files = [{"filename": ".github/workflows/merge-consensus-gate.yml",
              "status": "modified", "additions": 1, "deletions": 1, "changes": 2}]
    reviews = [
        {"state": "COMMENTED", "body": receipt()},
        {"state": "CHANGES_REQUESTED",
         "body": "Seat: Naya Gpt-6\nVerdict: HOLD\n"},
    ]
    def fetch(url, token):
        if url.endswith(f"/pulls/{PR}"):
            return pr
        if url.endswith(f"/pulls/{PR}/files"):
            return files
        if url.endswith(f"/issues/{PR}/comments"):
            return []
        if url.endswith(f"/pulls/{PR}/reviews"):
            return reviews
        raise AssertionError(url)
    monkeypatch.setattr(paperwork.consensus, "api_get", fetch)
    rc = paperwork.run()
    out = capsys.readouterr().out
    assert rc != 0
    assert "UNRESOLVED_HOLD" in out
