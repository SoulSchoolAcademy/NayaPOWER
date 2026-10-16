"""Tests for the CI caller of the anti-citogenesis claim-evidence gate.

Covers the runner's pure functions (seat-tag parsing, test-path extraction,
evidence assembly) and their integration with the gate adjudicator. IO
(GitHub API, env) is not tested here -- it is exercised by live dry runs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from check_claim_evidence import adjudicate  # noqa: E402
from ci_claim_evidence_gate import (  # noqa: E402
    build_evidence,
    extract_test_paths,
    parse_seat_tag,
    resolve_test_path,
)


def exists_of(*paths):
    s = set(paths)
    return lambda p: p in s


# --- seat tag parsing -------------------------------------------------------

def test_parse_seat_tag_basic():
    assert parse_seat_tag("Seat: Naya 5\n\n## What") == "Naya 5"


def test_parse_seat_tag_case_insensitive():
    assert parse_seat_tag("seat: naya4") == "naya4"


def test_parse_seat_tag_missing():
    assert parse_seat_tag("No seat here.") == ""


def test_parse_seat_tag_empty():
    assert parse_seat_tag("") == ""


def test_parse_seat_tag_first_wins():
    body = "Seat: Naya 5\nSeat: Naya 4"
    assert parse_seat_tag(body) == "Naya 5"


# --- test path extraction ---------------------------------------------------

def test_extracts_tests_dir_path():
    body = "Fixed. See tests/test_claim_evidence_gate.py (20/20 green)."
    assert extract_test_paths(body) == ["tests/test_claim_evidence_gate.py"]


def test_ignores_non_test_py():
    body = "Changed tools/check_claim_evidence.py and README.md."
    assert extract_test_paths(body) == []


def test_extracts_bare_test_filename():
    assert extract_test_paths("ran test_foo.py") == ["test_foo.py"]


def test_dedupes():
    body = "tests/test_a.py and tests/test_a.py again"
    assert extract_test_paths(body) == ["tests/test_a.py"]


def test_empty_body():
    assert extract_test_paths("") == []


# --- path resolution --------------------------------------------------------

def test_resolve_as_written():
    assert resolve_test_path("tests/test_a.py", exists_of("tests/test_a.py")) == "tests/test_a.py"


def test_resolve_bare_to_tests_dir():
    assert resolve_test_path("test_a.py", exists_of("tests/test_a.py")) == "tests/test_a.py"


def test_resolve_missing_returns_none():
    assert resolve_test_path("tests/test_nope.py", exists_of()) is None


# --- evidence assembly + gate integration ------------------------------------

def _run(body, author, reviews, check_runs, existing):
    exists = exists_of(*existing)
    ev = build_evidence(body, reviews, check_runs, exists)
    return adjudicate(body, author, ev, path_exists=exists), ev


def test_named_existing_test_admits():
    body = "Seat: Naya 5\nProven fixed by tests/test_truth.py."
    r, _ = _run(body, "Naya 5", [], [], ["tests/test_truth.py"])
    assert r["pass"] is True


def test_named_missing_test_fails_closed():
    """A claimed test that does not exist is evidence AGAINST, not skipped."""
    body = "Seat: Naya 5\nProven by tests/test_missing_xyz.py."
    r, ev = _run(body, "Naya 5", [], [], [])
    assert any(e.kind == "test" for e in ev)  # still recorded
    assert r["pass"] is False


def test_successful_ci_run_admits():
    body = "Seat: Naya 5\nIndependently verified -- CI run green on the head."
    runs = [{"id": 42, "status": "completed", "conclusion": "success"}]
    r, _ = _run(body, "Naya 5", [], runs, [])
    assert r["pass"] is True


def test_failed_ci_run_excluded():
    body = "Seat: Naya 5\nIndependently verified."
    runs = [{"id": 42, "status": "completed", "conclusion": "failure"}]
    r, _ = _run(body, "Naya 5", [], runs, [])
    assert r["pass"] is False


def test_in_progress_ci_run_excluded():
    """The gate's own in-progress run must not count as evidence."""
    body = "Seat: Naya 5\nIndependently verified."
    runs = [{"id": 42, "status": "in_progress", "conclusion": None}]
    r, _ = _run(body, "Naya 5", [], runs, [])
    assert r["pass"] is False


def test_different_seat_review_admits():
    body = "Seat: Naya 5\nIndependently verified by Naya 4."
    reviews = [{"id": 7, "state": "APPROVED", "body": "Seat: Naya 4\nLooks good."}]
    r, _ = _run(body, "Naya 5", reviews, [], [])
    assert r["pass"] is True


def test_same_seat_review_fails():
    """The 01:54 incident: author's own seat must not count."""
    body = "Seat: Naya 5\nIndependently verified."
    reviews = [{"id": 7, "state": "APPROVED", "body": "Seat: Naya 5\nVerified."}]
    r, _ = _run(body, "Naya 5", reviews, [], [])
    assert r["pass"] is False


def test_seatless_review_is_unattributable():
    body = "Seat: Naya 5\nIndependently verified."
    reviews = [{"id": 7, "state": "APPROVED", "body": "Looks good, no seat tag."}]
    r, _ = _run(body, "Naya 5", reviews, [], [])
    assert r["pass"] is False


def test_dismissed_review_excluded():
    body = "Seat: Naya 5\nIndependently verified."
    reviews = [{"id": 7, "state": "DISMISSED", "body": "Seat: Naya 4\nRetracted."}]
    r, ev = _run(body, "Naya 5", reviews, [], [])
    assert not any(e.kind == "seat_review" for e in ev)
    assert r["pass"] is False


def test_no_attestations_vacuous_pass():
    body = "Seat: Naya 5\nShipped the re-stamp. Three files."
    r, _ = _run(body, "Naya 5", [], [], [])
    assert r["pass"] is True
    assert r["verdicts"] == []


def test_undeclared_author_seat_documented_behavior():
    """No 'Seat:' tag: any seated review counts (limitation 6)."""
    body = "Independently verified by Naya 4."
    reviews = [{"id": 7, "state": "APPROVED", "body": "Seat: Naya 4\nOK."}]
    r, _ = _run(body, "", reviews, [], [])
    assert r["pass"] is True


# --- IO fail-closed (the "gate that passes when blind is theater" claim) ---

import os  # noqa: E402
from unittest import mock  # noqa: E402

from ci_claim_evidence_gate import GateBlind, main, run_gate  # noqa: E402


def test_api_failure_raises_gate_blind():
    """Any GitHub API failure blinds the gate -- it must not pass blind."""
    with mock.patch("urllib.request.urlopen", side_effect=OSError("net down")):
        try:
            run_gate("o/r", "1", "abc123", "/nonexistent", "token")
        except GateBlind:
            return
    raise AssertionError("run_gate did not raise GateBlind on API failure")


def test_main_missing_env_fails_closed():
    """Missing CI env vars fail the gate, never pass it."""
    with mock.patch.dict(os.environ, {}, clear=True):
        assert main() == 1


def test_run_gate_reaches_evidence_assembly():
    """Regression: run_gate must call build_evidence with the right arity.

    A previous version passed author_seat into build_evidence (5 args for
    4 params) -- a TypeError that crashed every PR carrying an attestation.
    The api-failure test never reached that line; this one does, with all
    three API calls mocked green and a body that contains an attestation.
    """
    import ci_claim_evidence_gate as gate_mod

    pr_body = "Seat: Naya 5\n\n## Proof\n\nThis was independently verified."

    def fake_api_get(path, token):
        if path.endswith("/reviews?per_page=100"):
            return []
        if "check-runs" in path:
            return {"check_runs": []}
        return {"body": pr_body}

    with mock.patch.object(gate_mod, "api_get", side_effect=fake_api_get):
        rc = run_gate("o/r", "1", "abc123", "/nonexistent", "token")
    # Bare attestation, no evidence: the gate must FAIL (closed), not crash.
    assert rc == 1


# --- w269: HTTP error detail (the 403 byte-level discriminator) --------------
# Mocked IO only -- no network. The whole point of w269: urllib's bare
# error string discards GitHub's JSON error payload, so a 403 reads as
# "Forbidden (GATE_BLIND)" with quota-vs-permission UNDETERMINED. The detail
# line restores the discriminator.

import io  # noqa: E402
import urllib.error  # noqa: E402
from http.client import HTTPMessage  # noqa: E402

from ci_claim_evidence_gate import api_get  # noqa: E402


def _http_error_403(body: str):
    headers = HTTPMessage()
    headers["X-RateLimit-Limit"] = "5000"
    headers["X-RateLimit-Remaining"] = "0"
    return urllib.error.HTTPError(
        url="https://api.github.com/repos/o/r/pulls/1",
        code=403,
        msg="Forbidden",
        hdrs=headers,
        fp=io.BytesIO(body.encode("utf-8")),
    )


def test_http_error_logs_response_body_and_headers(capsys):
    """A 403 must log the server's JSON error + headers before failing closed."""
    payload = '{"message": "API rate limit exceeded for installation ID 12345.", "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}'
    with mock.patch("urllib.request.urlopen", side_effect=_http_error_403(payload)):
        try:
            api_get("/repos/o/r/pulls/1", "token")
        except GateBlind as exc:
            assert "HTTP 403" in str(exc)
        else:
            raise AssertionError("api_get did not raise GateBlind on 403")
    out = capsys.readouterr().out
    assert "GATE_BLIND HTTP DETAIL" in out
    assert "API rate limit exceeded" in out  # the discriminator survives
    assert "X-RateLimit-Remaining" in out


def test_http_error_detail_survives_unreadable_body(capsys):
    """An unreadable response body must not crash the detail formatter."""
    err = _http_error_403("x")

    def boom():
        raise OSError("fp broken")

    err.read = boom
    with mock.patch("urllib.request.urlopen", side_effect=err):
        try:
            api_get("/repos/o/r/pulls/1", "token")
        except GateBlind:
            pass
        else:
            raise AssertionError("api_get did not raise GateBlind on 403")
    out = capsys.readouterr().out
    assert "GATE_BLIND HTTP DETAIL" in out
    assert "<response body unreadable>" in out
