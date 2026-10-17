"""Convergence proof: check_merge_consensus._classify_http_error is a thin
caller over the one shared mechanism (tools/http_403.py).

gr-w257 built tools/http_403.py as THE shared 403 classifier; the consensus
gate kept its own copy. This test pins the converged behavior:

  1. The names the gate uses ARE the shared module's objects (not a local
     re-implementation) -- "truly the only mechanism".
  2. The observable contract on a fixed battery of synthetic HTTPErrors:
     429 -> rate_limit; quota 403 -> rate_limit (retried); permission 403 ->
     permission (fail fast); anything else -> error. Never raises.

Two deliberate alignment deltas vs the pre-convergence copy, both inherited
from the shared mechanism (the mechanism of record, already IV'd):
  - "Must have admin rights" 403: error -> permission (still fail-closed,
    now with the accurate verdict).
  - "quota exceeded" wording without the literal "rate limit": error ->
    rate_limit (a spent token retries instead of failing closed).
"""
import io
import sys
import urllib.error
from email.message import Message
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import http_403  # noqa: E402 -- the mechanism of record
from check_merge_consensus import _classify_http_error  # noqa: E402
import check_merge_consensus as cmc  # noqa: E402


def make_error(code, body: bytes, retry_after=None):
    headers = Message()
    if retry_after is not None:
        headers["Retry-After"] = str(retry_after)
    return urllib.error.HTTPError(
        "https://api.github.com/x", code, "HTTP error", headers,
        io.BytesIO(body))


def test_uses_the_shared_mechanism_not_a_copy():
    # The gate's names must BE the shared module's objects: one mechanism,
    # not two parallel truths.
    assert cmc.classify_403_body is http_403.classify_403_body
    assert cmc.read_error_body is http_403.read_error_body
    assert cmc.error_message is http_403.error_message
    assert cmc.retry_after_seconds is http_403.retry_after_seconds


def test_429_is_rate_limit():
    e = make_error(429, b'{"message": "API rate limit exceeded"}')
    kind, detail, ra = _classify_http_error(e)
    assert kind == "rate_limit"
    assert detail == "API rate limit exceeded"
    assert ra is None


def test_403_quota_body_is_rate_limit():
    e = make_error(403, b'{"message": "API rate limit exceeded for user ID 7."}')
    kind, detail, ra = _classify_http_error(e)
    assert kind == "rate_limit"
    assert "rate limit" in detail.lower()


def test_403_secondary_rate_limit_is_rate_limit():
    e = make_error(
        403, b'{"message": "You have exceeded a secondary rate limit."}')
    assert _classify_http_error(e)[0] == "rate_limit"


def test_403_with_retry_after_but_no_quota_text_is_rate_limit():
    e = make_error(403, b'{"message": "Forbidden"}', retry_after=30)
    kind, detail, ra = _classify_http_error(e)
    assert kind == "rate_limit"
    assert ra == 30


def test_403_permission_body_fails_fast():
    e = make_error(
        403, b'{"message": "Resource not accessible by personal access token."}')
    kind, detail, ra = _classify_http_error(e)
    assert kind == "permission"
    assert ra is None
    assert "not accessible" in detail.lower()


def test_403_must_have_admin_is_permission():
    # Alignment delta (shared mechanism): was "error", now "permission".
    # Still fail-closed; the verdict is accurate.
    e = make_error(403, b'{"message": "Must have admin rights to Repository."}')
    assert _classify_http_error(e)[0] == "permission"


def test_403_unknown_body_is_error():
    e = make_error(403, b'{"message": "Something unexpected happened."}')
    kind, detail, ra = _classify_http_error(e)
    assert kind == "error"
    assert ra is None


def test_403_quota_wording_without_rate_limit_is_rate_limit():
    # Alignment delta (shared mechanism): was "error", now retried.
    e = make_error(403, b'{"message": "quota exceeded for this token"}')
    assert _classify_http_error(e)[0] == "rate_limit"


def test_500_is_error_with_http_fallback():
    e = make_error(500, b"")
    kind, detail, ra = _classify_http_error(e)
    assert kind == "error"
    assert detail == "HTTP 500"


def test_non_json_body_falls_back_to_raw_text():
    e = make_error(403, b"plain text refusal")
    kind, detail, _ = _classify_http_error(e)
    assert kind == "error"
    assert detail == "plain text refusal"


def test_hostile_body_never_raises():
    class BadFP(io.BytesIO):
        def read(self, *a, **k):
            raise OSError("boom")

    headers = Message()
    e = urllib.error.HTTPError(
        "https://api.github.com/x", 403, "Forbidden", headers, BadFP(b"x"))
    kind, detail, ra = _classify_http_error(e)  # must not raise
    assert kind == "error"
    assert detail == "HTTP 403"
    assert ra is None


def test_non_403_429_with_retry_after_header_is_error():
    # Retry-After only upgrades 403s to transient; a 500 stays an error.
    e = make_error(500, b"boom", retry_after=10)
    assert _classify_http_error(e)[0] == "error"
