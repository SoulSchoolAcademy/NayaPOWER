"""Tests for the merge-consensus gate's hardened behavior.

tools/check_merge_consensus.py — covers the chronic-red root causes found
2026-10-11 (Lane Alpha forensics on real CI logs):
  R1. transient 403 rate-limits during merge bursts crashed the gate with a
      bare traceback  ->  classified retries honoring Retry-After, clean
      fail-closed messages, never a traceback
  R2. seat-receipt convention enforced retroactively on pre-convention PRs
      (e.g. #1825, opened 2026-09-30)  ->  PRs opened before 2026-10-11T16:30Z
      are skipped with a clear message
  R3. seat regex excluded Naya 1 (the scorecard judge)  ->  [12345]
  R4. review/scorecard matchers rejected the team's actual receipt formats
      ("## VERDICT: MERGE RECOMMENDED", "Honest scorecard: 9.4/10")
      ->  matchers accept both the incantation and the IV formats
"""
import io
import json
import sys
import urllib.error
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_merge_consensus import (  # noqa: E402
    GateAPIError,
    _looks_like_review,
    _looks_like_scorecard,
    _score_of,
    api_get,
    author_seat_of,
    run_gate,
    seat_of,
)


class _FakeHeaders(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class _FakeResponse:
    """Minimal stand-in for the urlopen context manager."""

    def __init__(self, payload, link="", headers=None):
        self._body = json.dumps(payload).encode("utf-8")
        hdrs = {"Link": link}
        hdrs.update(headers or {})
        self.headers = _FakeHeaders(hdrs)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self, *args):
        return self._body


def _http_error(code, message="rate limited", retry_after=None):
    hdrs = _FakeHeaders(
        {"Retry-After": str(retry_after)} if retry_after else {})
    return urllib.error.HTTPError(
        url="https://api.github.com/x", code=code, msg=message,
        hdrs=hdrs, fp=io.BytesIO(json.dumps({"message": message}).encode()))


# ---------------------------------------------------------------------------
# R1: rate-limit handling
# ---------------------------------------------------------------------------

def test_retry_after_header_honored():
    """A 403 rate-limit carrying Retry-After sleeps the header value
    (not the blind 1s/2s), then succeeds."""
    ok = _FakeResponse([{"id": 7}])
    with patch("urllib.request.urlopen",
               side_effect=[_http_error(403, "API rate limit exceeded",
                                       retry_after=7), ok]) as m, \
         patch("check_merge_consensus.time.sleep") as sleep_mock:
        result = api_get("/repos/o/r/issues/1/comments", "token")
    assert result == [{"id": 7}]
    assert m.call_count == 2
    sleep_mock.assert_called_once_with(7)


def test_exponential_backoff_without_header_then_gives_up_clean():
    """Without Retry-After the gate backs off 1/2/4/8s across 5 attempts,
    then raises GateAPIError (no traceback) saying it is rate-limited."""
    errs = [_http_error(403, "You have exceeded a secondary rate limit")
            for _ in range(5)]
    with patch("urllib.request.urlopen", side_effect=errs) as m, \
         patch("check_merge_consensus.time.sleep") as sleep_mock:
        with pytest.raises(GateAPIError, match="rate-limited"):
            api_get("/repos/o/r/pulls/1", "token")
    assert m.call_count == 5
    assert [c.args[0] for c in sleep_mock.call_args_list] == [1, 2, 4, 8]


def test_permission_403_fails_fast_without_retry():
    """A 403 'Resource not accessible' is a permission problem, not a rate
    limit: fail immediately, do not waste retries."""
    err = _http_error(403, "Resource not accessible by integration")
    with patch("urllib.request.urlopen", side_effect=[err]) as m:
        with pytest.raises(GateAPIError, match="denied access"):
            api_get("/repos/o/r/pulls/1", "token")
    assert m.call_count == 1


def test_404_becomes_gate_api_error_not_traceback():
    """A 404 is not retried and surfaces as GateAPIError, never a raw
    HTTPError traceback on the check."""
    with patch("urllib.request.urlopen",
               side_effect=[_http_error(404, "Not Found")]) as m:
        with pytest.raises(GateAPIError, match="HTTP 404"):
            api_get("/repos/o/r/pulls/999999", "token")
    assert m.call_count == 1


# ---------------------------------------------------------------------------
# R3: seat identity
# ---------------------------------------------------------------------------

def test_seat_of_recognizes_naya_1_the_judge():
    assert seat_of("Seat: Naya 1") == "Naya 1"
    assert seat_of("[NAYA 1 · REVIEW] APPROVED") == "Naya 1"


def test_seat_of_still_recognizes_2_through_5():
    for n in "2345":
        assert seat_of(f"Seat: Naya {n}") == f"Naya {n}"
    assert seat_of("no tag here") is None


def test_author_seat_uses_explicit_declaration_not_incidental_mention():
    # Regression: PR #2373's body discusses "Naya 1" (the judge) in prose
    # before declaring "Seat: Naya 5". Authorship is the declaration.
    body = ("3. Seat regex excluded Naya 1 (the scorecard judge). "
            "Needs Naya 2/3/4 review.\n\nSeat: Naya 5")
    assert author_seat_of(body) == "Naya 5"
    assert author_seat_of("mentions Naya 2 in prose, no declaration") is None
    assert author_seat_of("Seat: Naya 3") == "Naya 3"


def test_gate_reads_author_from_declaration_despite_prose_mentions(capsys):
    """End to end: a PR body that mentions other seats in prose but declares
    Seat: Naya 5 attributes authorship to Naya 5."""
    body = ("Fixes the gate. The Naya 1 judge will score this; "
            "needs Naya 2/3/4 review.\n\nSeat: Naya 5")

    def fake_api_get(path, token):
        if path.endswith("/pulls/2373"):
            return _pr_response("2026-10-11T20:00:00Z", body)
        if path.endswith("/reviews"):
            return []
        return [{"body": "status update"}]

    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        with pytest.raises(SystemExit):
            run_gate("tok", "o/r", "2373", HEAD)
    out = capsys.readouterr().out
    assert "author (Naya 5)" in out
    assert "author (Naya 1)" not in out


# ---------------------------------------------------------------------------
# R4: receipt format matchers
# ---------------------------------------------------------------------------

def test_review_matcher_accepts_incantation():
    assert _looks_like_review("[NAYA 2 · REVIEW] APPROVED — looks good")


def test_review_matcher_accepts_iv_verdict_format():
    # The format IV workers actually post on sign-out.
    assert _looks_like_review("## VERDICT: MERGE RECOMMENDED\n**Honest scorecard: 9.4/10.**")


def test_review_matcher_rejects_plain_comment():
    assert not _looks_like_review("rebased onto the new tip, CI re-running")
    assert not _looks_like_review("## VERDICT: CHANGES REQUESTED")


def test_score_extraction_formats():
    assert _score_of("verdict: 9.4") == 9.4
    assert _score_of("**Honest scorecard: 9.4/10.**") == 9.4
    assert _score_of("Score 8/10") == 8.0
    assert _score_of("no score here") is None


HEAD = "d0144aee427dab3a1ab2df05f97962cb83b81f35"


def test_scorecard_matcher_accepts_legacy_format():
    body = f"## SCORECARD\nhead: {HEAD}\nverdict: 9.0\nSeat: Naya 3"
    assert _looks_like_scorecard(body, HEAD)


def test_scorecard_matcher_accepts_iv_format():
    body = (f"## VERDICT: MERGE RECOMMENDED\n**Honest scorecard: 9.4/10.**\n"
            f"head {HEAD}\nSeat: Naya 3")
    assert _looks_like_scorecard(body, HEAD)


def test_scorecard_matcher_rejects_low_score():
    body = f"Honest scorecard: 7.5/10\nhead {HEAD}\nSeat: Naya 3"
    assert not _looks_like_scorecard(body, HEAD)


def test_scorecard_matcher_requires_exact_head():
    body = "## SCORECARD\nhead: aaaa1111\nverdict: 9.5\nSeat: Naya 3"
    assert not _looks_like_scorecard(body, HEAD)


# ---------------------------------------------------------------------------
# R2: pre-convention skip + end-to-end run_gate behavior
# ---------------------------------------------------------------------------

def _pr_response(created_at, body):
    return {"number": 2368, "user": {"login": "SoulSchoolAcademy"},
            "created_at": created_at, "body": body}


def test_pre_convention_pr_is_skipped_not_failed(capsys):
    """PR #1825 (opened 2026-09-30) predates the seat convention: the gate
    skips with a clear message instead of failing on a stale assertion."""
    def fake_api_get(path, token):
        return _pr_response("2026-09-30T12:00:00Z", "old PR body, no seat tag")
    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        run_gate("tok", "o/r", "1825", HEAD)  # must not raise
    out = capsys.readouterr().out
    assert "CONSENSUS GATE SKIPPED" in out
    assert "1825" in out


def test_unknown_created_at_enforces_fail_closed(capsys):
    """If created_at is missing the gate enforces (fail closed) rather than
    skipping on an unknown timestamp."""
    def fake_api_get(path, token):
        pr = _pr_response("", "body without declaration")
        del pr["created_at"]
        return pr
    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        with pytest.raises(SystemExit):
            run_gate("tok", "o/r", "2368", HEAD)
    out = capsys.readouterr().out
    assert "PR body must declare the authoring seat" in out
    assert "SKIPPED" not in out


def test_post_convention_full_pass(capsys):
    """Author Naya 5, IV-verdict review from Naya 2, IV-format scorecard
    from Naya 3 naming the exact head -> PASSED."""
    review = ("[SIGN OUT] IV seat. ## VERDICT: MERGE RECOMMENDED\n"
              "Seat: Naya 2")
    scorecard = (f"**Honest scorecard: 9.4/10.**\nhead {HEAD}\n"
                 f"## VERDICT: MERGE RECOMMENDED\nSeat: Naya 3")

    def fake_api_get(path, token):
        if path.endswith("/pulls/2368"):
            return _pr_response("2026-10-11T18:00:00Z", "Seat: Naya 5\nbody")
        if path.endswith("/reviews"):
            return []
        return [{"body": review}, {"body": scorecard}]

    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        run_gate("tok", "o/r", "2368", HEAD)
    out = capsys.readouterr().out
    assert "CONSENSUS GATE PASSED" in out
    assert "Naya 5" in out and "Naya 2" in out and "Naya 3" in out


def test_author_cannot_review_own_work():
    """A verdict comment from the author's own seat does not count."""
    own_verdict = ("## VERDICT: MERGE RECOMMENDED\n**Honest scorecard: "
                   f"9.9/10.**\nhead {HEAD}\nSeat: Naya 5")

    def fake_api_get(path, token):
        if path.endswith("/pulls/2368"):
            return _pr_response("2026-10-11T18:00:00Z", "Seat: Naya 5")
        if path.endswith("/reviews"):
            return []
        return [{"body": own_verdict}]

    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        with pytest.raises(SystemExit) as exc:
            run_gate("tok", "o/r", "2368", HEAD)
    assert exc.value.code == 1


def test_missing_review_fails_with_actionable_message(capsys):
    def fake_api_get(path, token):
        if path.endswith("/pulls/2368"):
            return _pr_response("2026-10-11T18:00:00Z", "Seat: Naya 5")
        if path.endswith("/reviews"):
            return []
        return [{"body": "just a status comment"}]

    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        with pytest.raises(SystemExit):
            run_gate("tok", "o/r", "2368", HEAD)
    out = capsys.readouterr().out
    assert "no review from a seat other than the author (Naya 5)" in out


def test_missing_seat_declaration_fails_with_fix(capsys):
    def fake_api_get(path, token):
        return _pr_response("2026-10-11T18:00:00Z", "body without declaration")

    with patch("check_merge_consensus.api_get", side_effect=fake_api_get):
        with pytest.raises(SystemExit):
            run_gate("tok", "o/r", "2368", HEAD)
    out = capsys.readouterr().out
    assert "PR body must declare the authoring seat" in out


def test_api_error_becomes_plain_words_not_traceback(capsys, monkeypatch):
    """R1 end to end: an API outage exits 1 via fail() with 'unable to
    verify consensus' — no traceback text on the check."""
    monkeypatch.setenv("GH_TOKEN", "tok")
    monkeypatch.setenv("REPO", "o/r")
    monkeypatch.setenv("PR_NUMBER", "2368")
    monkeypatch.setenv("HEAD_SHA", HEAD)
    with patch("check_merge_consensus.api_get",
               side_effect=GateAPIError("GitHub API rate-limited")):
        with pytest.raises(SystemExit) as exc:
            __import__("check_merge_consensus").main()
    assert exc.value.code == 1
    out = capsys.readouterr().out
    err = capsys.readouterr().err
    assert "CONSENSUS GATE FAILED: unable to verify consensus" in out
    assert "Traceback" not in out + err
