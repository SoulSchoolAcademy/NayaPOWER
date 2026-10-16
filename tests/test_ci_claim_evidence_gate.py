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


# --- IO fail-closed / transient UNKNOWN --------------------------------------

import io  # noqa: E402
import os  # noqa: E402
from unittest import mock  # noqa: E402

from ci_claim_evidence_gate import (  # noqa: E402
    GateBlind,
    GateTransient,
    api_get,
    main,
    run_gate,
)


def _http_error(code, message, retry_after=None):
    import urllib.error
    body = ('{"message": "%s"}' % message).encode()
    headers = {"Retry-After": str(retry_after)} if retry_after else {}
    return urllib.error.HTTPError("http://x/", code, message, headers,
                                 io.BytesIO(body))


class _FakeResp:
    """A urlopen context-manager stand-in returning parsed JSON."""
    def __init__(self, payload):
        self._payload = payload
    def __enter__(self):
        return self
    def __exit__(self, *exc):
        return False
    def read(self):
        return json_payload(self._payload)


def json_payload(obj):
    import json as _json
    return _json.dumps(obj).encode()


def test_transient_network_failure_raises_gate_transient():
    """A dead network is transient, not blind: retries, then GateTransient
    (UNKNOWN), never a silent pass and never a traceback."""
    import ci_claim_evidence_gate as gate_mod
    with mock.patch("urllib.request.urlopen", side_effect=OSError("net down")), \
         mock.patch.object(gate_mod, "time") as mock_time:
        try:
            run_gate("o/r", "1", "abc123", "/nonexistent", "token")
        except GateTransient:
            assert mock_time.sleep.call_count == 4  # 5 attempts, 4 waits
            return
    raise AssertionError("run_gate did not raise GateTransient on net failure")


def test_persistent_rate_limit_raises_gate_transient():
    """429 on every attempt: 5 tries, then GateTransient (UNKNOWN)."""
    import ci_claim_evidence_gate as gate_mod
    errs = [_http_error(429, "API rate limit exceeded") for _ in range(5)]
    with mock.patch("urllib.request.urlopen", side_effect=errs) as m, \
         mock.patch.object(gate_mod, "time"):
        try:
            api_get("/repos/o/r/pulls/1", "token")
        except GateTransient as e:
            assert "rate-limited" in str(e)
            assert m.call_count == 5
            return
    raise AssertionError("api_get did not raise GateTransient on 429")


def test_rate_limit_then_success_recovers():
    """Transient then green: the retry heals and the call returns data."""
    import ci_claim_evidence_gate as gate_mod
    errs = [_http_error(429, "API rate limit exceeded"),
            _http_error(429, "API rate limit exceeded")]
    with mock.patch("urllib.request.urlopen",
                    side_effect=errs + [_FakeResp({"ok": True})]) as m, \
         mock.patch.object(gate_mod, "time") as mock_time:
        assert api_get("/repos/o/r/pulls/1", "token") == {"ok": True}
    assert m.call_count == 3
    assert mock_time.sleep.call_count == 2


def test_5xx_is_transient_not_blind():
    """A 502 is the host's problem, not the verdict's: GateTransient."""
    import ci_claim_evidence_gate as gate_mod
    errs = [_http_error(502, "Bad Gateway") for _ in range(5)]
    with mock.patch("urllib.request.urlopen", side_effect=errs), \
         mock.patch.object(gate_mod, "time"):
        try:
            api_get("/repos/o/r/pulls/1", "token")
        except GateTransient:
            return
    raise AssertionError("api_get did not raise GateTransient on 502")


def test_permission_403_raises_gate_blind_fast():
    """A 403 'Resource not accessible' is genuine: GateBlind, no retries."""
    err = _http_error(403, "Resource not accessible by integration")
    with mock.patch("urllib.request.urlopen", side_effect=[err]) as m:
        try:
            api_get("/repos/o/r/pulls/1", "token")
        except GateBlind as e:
            assert "403" in str(e)
            assert m.call_count == 1
            return
    raise AssertionError("api_get did not raise GateBlind on permission 403")


def test_404_raises_gate_blind_fast():
    """A 404 is genuine: GateBlind, no retries."""
    err = _http_error(404, "Not Found")
    with mock.patch("urllib.request.urlopen", side_effect=[err]) as m:
        try:
            api_get("/repos/o/r/pulls/1", "token")
        except GateBlind:
            assert m.call_count == 1
            return
    raise AssertionError("api_get did not raise GateBlind on 404")


def test_main_transient_returns_unknown_not_fail(capsys):
    """main() maps GateTransient to exit 2 with an UNKNOWN line, never a
    FAIL line and never a traceback."""
    import ci_claim_evidence_gate as gate_mod
    env = {"GITHUB_REPOSITORY": "o/r", "PR_NUMBER": "1",
           "PR_HEAD_SHA": "abc", "GITHUB_TOKEN": "t"}
    with mock.patch.dict(os.environ, env, clear=True), \
         mock.patch.object(gate_mod, "run_gate",
                           side_effect=GateTransient("GET x failed: net")):
        assert main() == 2
    out = capsys.readouterr().out
    assert "UNKNOWN" in out
    assert "re-run, not a FAIL" in out
    assert "FAIL --" not in out
    assert "Traceback" not in out


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
