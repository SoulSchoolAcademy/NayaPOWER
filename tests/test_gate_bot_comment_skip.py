"""Tests for the merge-consensus gate's bot-comment skip.

.tools/check_merge_consensus.py is untouched by this change; the fix lives in
the workflow's job-level `if` (.github/workflows/merge-consensus-gate.yml).

Part 1 proves the trigger decision table with a faithful Python replica of
the exact shipped `if` expression (the test fails if the workflow text no
longer carries the bot clause — regression guard against drift between the
shipped trigger and the tested one).

Part 2 proves the gate's evaluation behavior is preserved for everything the
trigger still admits, using the REAL check_merge_consensus module with a
stubbed api_get (no network): (a) seat/human-triggered state still runs the
full evaluation and still fails closed, (b) an unattributed comment state
still fails closed on attribution, (c) a properly seat-tagged state passes.

Residual (honest): the final confirmation of GitHub's expression evaluation
is the first real bot comment after merge — no check run should fire for it.
That is observable, not eyeballed: issue_comment events from bots currently
produce a full run that fails closed on attribution (the burn this kills).
"""
import io
import os
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_merge_consensus import main  # noqa: E402

WORKFLOW = ROOT / ".github" / "workflows" / "merge-consensus-gate.yml"

HEAD = "a" * 64  # synthetic head SHA under test


# ---------------------------------------------------------------------------
# Part 1 — the trigger decision table
# ---------------------------------------------------------------------------

def job_should_run(event_name, issue_is_pr, comment_user_type):
    """Faithful replica of the workflow job-level `if`:

        (github.event_name != 'issue_comment' || github.event.issue.pull_request)
        && (github.event_name != 'issue_comment' || github.event.comment.user.type != 'Bot')

    GitHub expression semantics: dereferencing a property of a missing object
    (github.event.comment on non-issue_comment events) yields null, and
    null != 'Bot' evaluates to true.
    """
    is_comment = event_name == "issue_comment"
    issue_ok = (not is_comment) or bool(issue_is_pr)
    bot_ok = (not is_comment) or (comment_user_type != "Bot")
    return bool(issue_ok and bot_ok)


def test_workflow_carries_the_bot_skip_clause():
    """The shipped workflow must contain the exact bot-skip clause this table
    models — otherwise the table is testing a fiction."""
    text = WORKFLOW.read_text()
    assert "github.event.comment.user.type != 'Bot'" in text, (
        "workflow lost the bot-skip clause; the decision table no longer "
        "describes the shipped trigger")


def test_human_comment_on_pr_still_runs():
    assert job_should_run("issue_comment", True, "User") is True


def test_bot_comment_on_pr_is_skipped():
    # coderabbitai[bot] and friends: user.type == 'Bot' in the payload.
    # The `edited` comment type carries the same comment.user payload, so it
    # is skipped by the same clause — the condition only inspects the author.
    assert job_should_run("issue_comment", True, "Bot") is False


def test_automation_bot_comment_is_skipped():
    assert job_should_run("issue_comment", True, "Bot") is False


def test_comment_on_plain_issue_still_skipped():
    # Pre-existing behavior preserved: non-PR issue comments never run.
    assert job_should_run("issue_comment", False, "User") is False
    assert job_should_run("issue_comment", False, "Bot") is False


def test_pull_request_events_still_run():
    assert job_should_run("pull_request", None, None) is True


def test_pull_request_review_events_still_run():
    assert job_should_run("pull_request_review", None, None) is True


# ---------------------------------------------------------------------------
# Part 2 — evaluation preserved (real module, stubbed api_get, no network)
# ---------------------------------------------------------------------------

def _run_gate(pr_body, reviews, comments):
    """Run the real gate main() against synthetic PR state; return
    (exit_code, stdout)."""
    responses = {
        "/repos/o/r/pulls/1": {
            "number": 1,
            "user": {"login": "SoulSchoolAcademy"},
            "body": pr_body,
        },
        "/repos/o/r/pulls/1/reviews": reviews,
        "/repos/o/r/issues/1/comments": comments,
    }

    def fake_api_get(path, token):
        return responses[path]

    env = {"GH_TOKEN": "t", "REPO": "o/r", "PR_NUMBER": "1", "HEAD_SHA": HEAD}
    with patch.dict(os.environ, env), \
         patch("check_merge_consensus.api_get", side_effect=fake_api_get), \
         patch("sys.stdout", new=io.StringIO()) as out:
        try:
            main()
        except SystemExit as e:
            return e.code, out.getvalue()
        return 0, out.getvalue()


def test_unattributed_comment_state_fails_closed():
    """(b) A comment without an attributable seat still fails closed."""
    code, out = _run_gate(
        pr_body="human-value events work, no seat tag anywhere",
        reviews=[],
        comments=[{"body": "looks good to me"}],
    )
    assert code == 1
    assert "must declare the authoring seat" in out


def test_human_comment_state_still_fails_closed_without_receipt():
    """(a) Seat/human-triggered evaluation still runs and still fails closed:
    a seat review without the scorecard receipt is not consensus."""
    code, out = _run_gate(
        pr_body="human-value events work. Seat: Naya 5",
        reviews=[],
        comments=[{
            "body": "[NAYA 4 · REVIEW] APPROVED — reviewed end to end. "
                    "Seat: Naya 4",
        }],
    )
    assert code == 1
    assert "no scorecard receipt" in out


def test_seat_tagged_comment_state_passes():
    """(c) A properly seat-tagged comment state still passes."""
    code, out = _run_gate(
        pr_body="human-value events work. Seat: Naya 5",
        reviews=[],
        comments=[
            {"body": "[NAYA 4 · REVIEW] APPROVED — reviewed end to end. "
                     "Seat: Naya 4"},
            {"body": "## SCORECARD\n"
                     f"head: {HEAD}\n"
                     "merge: APPROVED\n"
                     "verdict: 9.2\n"
                     "Seat: Naya 3"},
        ],
    )
    assert code == 0
    assert "CONSENSUS GATE PASSED" in out
    assert "author Naya 5" in out and "reviewer Naya 4" in out \
        and "scorer Naya 3" in out
