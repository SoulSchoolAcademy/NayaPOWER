"""Tests for HTTP-DETAIL logging in ci_claim_evidence_gate.api_get.

The gate must fail closed on every IO failure (GateBlind), but an HTTPError
now carries the status code plus a truncated response body in the GateBlind
message -- turning the next 403 mystery into a readable log line. The bearer
token must NEVER appear in that line.
"""

import io
import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from ci_claim_evidence_gate import GateBlind, api_get  # noqa: E402


TOKEN = "ghp_testtoken_never_logged_12345"


def _http_error(code=403, body=b""):
    return urllib.error.HTTPError(
        "https://api.github.com/repos/x/y/pulls/1",
        code,
        "Forbidden" if code == 403 else "Error",
        {},
        io.BytesIO(body),
    )


def _raise(exc, monkeypatch):
    def boom(*args, **kwargs):
        raise exc

    monkeypatch.setattr("urllib.request.urlopen", boom)


def test_httperror_carries_status_and_truncated_body(monkeypatch):
    body = b'{"message":"API rate limit exceeded for installation ID 123.","documentation_url":"https://docs.github.com"}' * 10
    _raise(_http_error(403, body), monkeypatch)
    with pytest.raises(GateBlind) as ei:
        api_get("/repos/x/y/pulls/1", TOKEN)
    msg = str(ei.value)
    assert "HTTP 403" in msg
    assert "API rate limit exceeded" in msg
    assert "[truncated," in msg
    assert body.decode() not in msg  # full body must not be logged


def test_httperror_never_logs_token(monkeypatch):
    evil = b'{"message":"denied for token ' + TOKEN.encode() + b' on this endpoint"}'
    _raise(_http_error(403, evil), monkeypatch)
    with pytest.raises(GateBlind) as ei:
        api_get("/repos/x/y/pulls/1", TOKEN)
    msg = str(ei.value)
    assert TOKEN not in msg
    assert "<redacted>" in msg


def test_httperror_empty_body_still_names_status(monkeypatch):
    _raise(_http_error(403, b""), monkeypatch)
    with pytest.raises(GateBlind) as ei:
        api_get("/repos/x/y/pulls/1", TOKEN)
    msg = str(ei.value)
    assert "HTTP 403" in msg
    assert "<empty body>" in msg


def test_httperror_unreadable_body_still_gateblind(monkeypatch):
    err = _http_error(403, b"{}")

    def bad_read():
        raise OSError("connection already closed")

    err.read = bad_read  # simulate a torn-down error stream
    _raise(err, monkeypatch)
    with pytest.raises(GateBlind) as ei:
        api_get("/repos/x/y/pulls/1", TOKEN)
    assert "unreadable" in str(ei.value)


def test_urlerror_still_gateblind_without_http_detail(monkeypatch):
    _raise(urllib.error.URLError("connection refused"), monkeypatch)
    with pytest.raises(GateBlind) as ei:
        api_get("/repos/x/y/pulls/1", TOKEN)
    assert "HTTP" not in str(ei.value)
