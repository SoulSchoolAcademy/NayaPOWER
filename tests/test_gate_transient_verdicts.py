"""Gate-reliability tests (Worker 2, mother-brain sprint).

Two contracts under test:

1. TRANSIENT -> UNKNOWN, never a wrong FAIL, never a traceback.
   check_merge_consensus, check_pr_receipt, and ci_claim_evidence_gate must
   exit 2 with a plain-words "UNKNOWN" line when a transient failure
   (429 / rate-limited 403 / 5xx / network error) survives all retries.
   Genuine failures still exit 1 (FAIL); genuine passes still exit 0.

2. API-SAVING reorders are behavior-preserving.
   warn_overlapping_prs checks the already-posted marker before the N
   per-PR file fetches; ci_claim_evidence_gate accepts PR_BODY from the
   environment; check_merge_consensus stops paginating once the verdict is
   decided. Same verdicts, fewer calls.
"""
import io
import json
import os
import sys
import urllib.error
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_merge_consensus as consensus  # noqa: E402
import check_pr_receipt as receipt  # noqa: E402
import ci_claim_evidence_gate as claim_gate  # noqa: E402
import warn_overlapping_prs as overlap  # noqa: E402


# --- fakes ---------------------------------------------------------------

class _FakeHeaders(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class _FakeHTTPResp:
    """urlopen stand-in for the gate scripts' `with urlopen(...) as r`."""

    def __init__(self, status=200, payload=None, link="", headers=None):
        self.status = status
        self._body = (json.dumps(payload).encode()
                      if payload is not None else b"")
        self.headers = _FakeHeaders(headers or {})
        if link:
            self.headers["Link"] = link

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self, *args):
        return self._body


def _http_error(code, message="boom", retry_after=None):
    body = ('{"message": "%s"}' % message).encode()
    headers = {"Retry-After": str(retry_after)} if retry_after else {}
    return urllib.error.HTTPError("https://api.github.com/x", code, message,
                                 headers, io.BytesIO(body))


# --- 1a. consensus: transient -> UNKNOWN ----------------------------------

def _consensus_env(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "tok")
    monkeypatch.setenv("REPO", "o/r")
    monkeypatch.setenv("PR_NUMBER", "2368")
    monkeypatch.setenv("HEAD_SHA", "abc123")


def test_consensus_transient_api_error_exits_unknown(capsys, monkeypatch):
    """A rate limit that survives retries is UNKNOWN (exit 2), not FAIL."""
    _consensus_env(monkeypatch)
    with mock.patch.object(
            consensus, "run_gate",
            side_effect=consensus.TransientAPIError("still limited")):
        with pytest.raises(SystemExit) as exc:
            consensus.main()
    assert exc.value.code == 2
    out = capsys.readouterr().out
    assert "CONSENSUS GATE UNKNOWN" in out
    assert "re-run, not a FAIL" in out
    assert "Traceback" not in out


def test_consensus_genuine_api_error_still_fails(capsys, monkeypatch):
    """A permission failure is still FAIL (exit 1), not UNKNOWN."""
    _consensus_env(monkeypatch)
    with mock.patch.object(
            consensus, "run_gate",
            side_effect=consensus.GateAPIError("denied access")):
        with pytest.raises(SystemExit) as exc:
            consensus.main()
    assert exc.value.code == 1
    assert "CONSENSUS GATE FAILED" in capsys.readouterr().out


def test_consensus_5xx_retried_then_unknown():
    """502s are transient: retried, then TransientAPIError (a GateAPIError)."""
    errs = [_http_error(502, "Bad Gateway") for _ in range(5)]
    with mock.patch("urllib.request.urlopen", side_effect=errs) as m, \
         mock.patch.object(consensus, "time"):
        with pytest.raises(consensus.TransientAPIError):
            consensus.api_get("/repos/o/r/pulls/1", "tok")
    assert m.call_count == 5


def test_consensus_network_error_retried_then_unknown():
    """A dead network is transient: retried, then TransientAPIError."""
    with mock.patch("urllib.request.urlopen",
                    side_effect=OSError("net down")) as m, \
         mock.patch.object(consensus, "time") as mock_time:
        with pytest.raises(consensus.TransientAPIError):
            consensus.api_get("/repos/o/r/pulls/1", "tok")
    assert m.call_count == 5
    assert mock_time.sleep.call_count == 4


def test_consensus_early_exit_stops_pagination():
    """Approval on reviews page 1 + scorecard on comments page 1: only 3
    calls (PR object, reviews p1, comments p1) even though both endpoints
    advertise a next page. Verdict identical to the full drain."""
    head = "abc123def456"
    pr = _FakeHTTPResp(payload={"number": 2368,
                                "created_at": "2026-10-16T00:00:00Z",
                                "user": {"login": "author"},
                                "body": "Seat: Naya 5\nDo the thing."})
    rev1 = _FakeHTTPResp(
        payload=[{"state": "APPROVED", "user": {"login": "reviewer"},
                  "body": "Seat: Naya 4\nLooks good."}],
        link='<https://api.github.com/repos/o/r/pulls/2368/reviews?page=2>; rel="next"')
    scorecard = ("## SCORECARD\nhead: %s\nHonest scorecard: 9.4/10\n"
                 "Seat: Naya 4" % head)
    com1 = _FakeHTTPResp(
        payload=[{"body": scorecard}],
        link='<https://api.github.com/repos/o/r/issues/2368/comments?page=2>; rel="next"')
    with mock.patch("urllib.request.urlopen",
                    side_effect=[pr, rev1, com1]) as m, \
         mock.patch.object(consensus, "time"):
        consensus.run_gate("tok", "o/r", "2368", head)
    assert m.call_count == 3  # no page-2 fetch happened


def test_consensus_early_exit_keeps_going_when_undecided():
    """Approval only on reviews page 2: the gate must fetch it (no false
    UNKNOWN/FAIL from stopping too early)."""
    head = "abc123def456"
    pr = _FakeHTTPResp(payload={"number": 2368,
                                "created_at": "2026-10-16T00:00:00Z",
                                "user": {"login": "author"},
                                "body": "Seat: Naya 5\nDo the thing."})
    rev1 = _FakeHTTPResp(
        payload=[{"state": "COMMENTED", "user": {"login": "reviewer"},
                  "body": "n/a"}],
        link='<https://api.github.com/x?page=2>; rel="next"')
    rev2 = _FakeHTTPResp(
        payload=[{"state": "APPROVED", "user": {"login": "reviewer"},
                  "body": "Seat: Naya 4\nApproved."}])
    com1 = _FakeHTTPResp(payload=[{"body": "## SCORECARD\nhead: %s\n"
                                           "9.4/10\nSeat: Naya 4" % head}])
    with mock.patch("urllib.request.urlopen",
                    side_effect=[pr, rev1, rev2, com1]) as m, \
         mock.patch.object(consensus, "time"):
        consensus.run_gate("tok", "o/r", "2368", head)
    assert m.call_count == 4


# --- 1b. receipt: transient -> UNKNOWN ------------------------------------

def _receipt_body(url):
    return "## Evidence\n\nProves the fix: %s\n" % url


def test_receipt_429_becomes_unknown_not_dead(capsys, monkeypatch):
    """A rate-limited host is UNKNOWN (exit 2), not a dead handle."""
    monkeypatch.setenv("PR_BODY", _receipt_body("https://example.invalid/x"))
    with mock.patch("urllib.request.urlopen",
                    side_effect=_http_error(429, "Too Many Requests")), \
         mock.patch.object(receipt, "time"):
        with pytest.raises(SystemExit) as exc:
            receipt.main()
    assert exc.value.code == 2
    out = capsys.readouterr().out
    assert "RECEIPT GATE UNKNOWN" in out
    assert "re-run, not a FAIL" in out
    assert "dead artifact" not in out


def test_receipt_network_blip_becomes_unknown(capsys, monkeypatch):
    monkeypatch.setenv("PR_BODY", _receipt_body("https://example.invalid/x"))
    with mock.patch("urllib.request.urlopen",
                    side_effect=OSError("conn reset")), \
         mock.patch.object(receipt, "time"):
        with pytest.raises(SystemExit) as exc:
            receipt.main()
    assert exc.value.code == 2
    assert "RECEIPT GATE UNKNOWN" in capsys.readouterr().out


def test_receipt_404_still_fails_loudly(capsys, monkeypatch):
    """A genuinely gone URL still FAILs (exit 1)."""
    monkeypatch.setenv("PR_BODY", _receipt_body("https://example.invalid/x"))
    with mock.patch("urllib.request.urlopen",
                    side_effect=_http_error(404, "Not Found")):
        with pytest.raises(SystemExit) as exc:
            receipt.main()
    assert exc.value.code == 1
    out = capsys.readouterr().out
    assert "RECEIPT GATE FAILED" in out
    assert "dead artifact handle" in out


def test_receipt_live_url_still_passes(capsys, monkeypatch):
    monkeypatch.setenv("PR_BODY", _receipt_body("https://example.invalid/x"))
    with mock.patch("urllib.request.urlopen",
                    side_effect=[_FakeHTTPResp(status=200)]):
        receipt.main()  # exit 0: no SystemExit
    assert "Receipt OK" in capsys.readouterr().out


def test_receipt_head_rejection_falls_back_to_get():
    """HEAD 403 -> GET 200 is live, not dead and not transient."""
    with mock.patch("urllib.request.urlopen",
                    side_effect=[_http_error(403, "Forbidden"),
                                 _FakeHTTPResp(status=200)]) as m:
        kind, _ = receipt.probe_url("https://example.invalid/x")
    assert kind == "live"
    assert m.call_count == 2


def test_receipt_429_retried_then_unknown():
    """probe_url retries transients (3 attempts) before reporting unknown."""
    with mock.patch("urllib.request.urlopen",
                    side_effect=_http_error(429, "slow down")) as m, \
         mock.patch.object(receipt, "time") as mock_time:
        kind, detail = receipt.probe_url("https://example.invalid/x")
    assert kind == "transient"
    assert "429" in detail
    assert m.call_count == 3
    assert mock_time.sleep.call_count == 2


# --- 1c. claim-evidence: transient -> UNKNOWN, PR_BODY fast path ---------

def test_claim_gate_pr_body_skips_pr_fetch():
    """With PR_BODY in the environment, run_gate must not fetch the PR
    object at all — same untrusted text, one fewer API call."""
    calls = []

    def fake_api_get(path, token):
        calls.append(path)
        if "check-runs" in path:
            return {"check_runs": []}
        return []

    body = "Seat: Naya 5\n\nProven by tests/test_x.py."
    env = {"PR_BODY": body}
    with mock.patch.dict(os.environ, env, clear=False), \
         mock.patch.object(claim_gate, "api_get", side_effect=fake_api_get):
        rc = claim_gate.run_gate("o/r", "1", "abc123", "/nonexistent", "t")
    assert not any(p.endswith("/pulls/1") for p in calls), calls
    assert rc == 1  # bare attestation, no evidence: still FAILs closed


def test_claim_gate_no_pr_body_fetches_live():
    """Without PR_BODY the live PR fetch still happens (old behavior)."""
    calls = []

    def fake_api_get(path, token):
        calls.append(path)
        if path.endswith("/pulls/1"):
            return {"body": "no attestations here"}
        return []

    with mock.patch.dict(os.environ, {}, clear=True), \
         mock.patch.object(claim_gate, "api_get", side_effect=fake_api_get):
        rc = claim_gate.run_gate("o/r", "1", "abc123", "/nonexistent", "t")
    assert any(p.endswith("/pulls/1") for p in calls)
    assert rc == 0


# --- 2. overlap watch: marker-first reorder --------------------------------

def _overlap_env(monkeypatch):
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("PR_NUMBER", "123")
    monkeypatch.setenv("BASE_SHA", "base")
    monkeypatch.setenv("HEAD_SHA", "head")


def _fake_git_diff(*args, **kwargs):
    class R:
        stdout = "tools/x.py\n"
    return R()


def test_overlap_marker_skips_file_fetches(capsys, monkeypatch):
    """Marker present: 2 calls (list PRs + comments), zero per-PR file
    fetches, no post — the N+1 saving."""
    _overlap_env(monkeypatch)
    calls = []

    def fake_api(path, method="GET", data=None):
        calls.append((method, path))
        if "pulls?state=open" in path:
            return [{"number": 123, "title": "mine"},
                    {"number": 124, "title": "other"}]
        if path.endswith("/comments?per_page=100"):
            return [{"body": "<!-- overlap-watch -->\nold warning"}]
        if "/files" in path:
            return [{"filename": "tools/x.py"}]
        raise AssertionError("unexpected POST " + path)

    with mock.patch.object(overlap, "api", side_effect=fake_api), \
         mock.patch.object(overlap.subprocess, "run", _fake_git_diff):
        overlap.main()
    assert calls == [("GET", "/repos/o/r/pulls?state=open&base=main&per_page=30"),
                     ("GET", "/repos/o/r/issues/123/comments?per_page=100")]
    assert "already posted" in capsys.readouterr().out


def test_overlap_no_marker_still_warns_and_posts(capsys, monkeypatch):
    """No marker + real overlap: files fetched, warning posted (behavior
    preserved — only the order changed)."""
    _overlap_env(monkeypatch)
    calls = []
    posted = []

    def fake_api(path, method="GET", data=None):
        calls.append((method, path))
        if "pulls?state=open" in path:
            return [{"number": 123, "title": "mine"},
                    {"number": 124, "title": "other"}]
        if path.endswith("/comments?per_page=100"):
            return [{"body": "just a review comment"}]
        if "/files" in path:
            return [{"filename": "tools/x.py"}]
        if method == "POST":
            posted.append(data)
            return {}
        raise AssertionError("unexpected call " + path)

    with mock.patch.object(overlap, "api", side_effect=fake_api), \
         mock.patch.object(overlap.subprocess, "run", _fake_git_diff):
        overlap.main()
    assert ("GET", "/repos/o/r/pulls/124/files?per_page=100") in calls
    assert len(posted) == 1
    assert "<!-- overlap-watch -->" in posted[0]["body"]
    assert "Posted overlap warning" in capsys.readouterr().out


def test_overlap_no_hits_no_post(capsys, monkeypatch):
    """No marker, no overlapping files: nothing posted."""
    _overlap_env(monkeypatch)
    posted = []

    def fake_api(path, method="GET", data=None):
        if "pulls?state=open" in path:
            return [{"number": 123, "title": "mine"},
                    {"number": 124, "title": "other"}]
        if path.endswith("/comments?per_page=100"):
            return []
        if "/files" in path:
            return [{"filename": "tools/unrelated.py"}]
        if method == "POST":
            posted.append(data)
        return {}

    with mock.patch.object(overlap, "api", side_effect=fake_api), \
         mock.patch.object(overlap.subprocess, "run", _fake_git_diff):
        overlap.main()
    assert posted == []
    assert "No overlapping open PRs." in capsys.readouterr().out
