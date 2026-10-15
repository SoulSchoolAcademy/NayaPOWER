"""Tests for tools/http_403.py -- the one shared 403 classifier.

Every fail-closed gate uses this to tell a quota 403 (INCONCLUSIVE/RETRY)
from a permission 403 (FAIL fast). Bodies below are real GitHub message
shapes. Garbage never raises. No network: HTTPError objects are faked.
"""

import io
import sys
import urllib.error
from email.message import Message
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from http_403 import (  # noqa: E402
    QuotaExhausted,
    classify_403_body,
    error_message,
    retry_after_seconds,
)


def fake_403(body: bytes, retry_after=None):
    headers = Message()
    if retry_after is not None:
        headers["Retry-After"] = str(retry_after)
    return urllib.error.HTTPError(
        "https://api.github.com/repos/x/y", 403, "Forbidden",
        headers, io.BytesIO(body))


# --- classifier: quota -------------------------------------------------------

def test_classify_primary_rate_limit():
    body = b'{"message":"API rate limit exceeded for user ID 12345.",' \
           b'"documentation_url":"https://docs.github.com/rest#rate-limiting"}'
    assert classify_403_body(body) == "quota"


def test_classify_secondary_rate_limit():
    body = (b'{"message":"You have exceeded a secondary rate limit. '
            b'Please wait a few minutes before you try again."}')
    assert classify_403_body(body) == "quota"


def test_classify_installation_quota():
    # The installation-token quota class that bit the team (API-STANDDOWN).
    body = b'{"message":"API rate limit exceeded for installation ID 98765."}'
    assert classify_403_body(body) == "quota"


def test_classify_quota_word_pair():
    body = b'{"message":"You have exceeded the request quota for this hour."}'
    assert classify_403_body(body) == "quota"


def test_classify_str_input():
    assert classify_403_body("API rate limit exceeded for user ID 1.") == "quota"


# --- classifier: permission ---------------------------------------------------

def test_classify_permission_personal_access_token():
    body = b'{"message":"Resource not accessible by personal access token.",' \
           b'"documentation_url":"https://docs.github.com/rest"}'
    assert classify_403_body(body) == "permission"


def test_classify_permission_integration():
    body = b'{"message":"Resource not accessible by integration."}'
    assert classify_403_body(body) == "permission"


def test_classify_permission_must_have_admin():
    body = b'{"message":"Must have admin rights to Repository."}'
    assert classify_403_body(body) == "permission"


# --- classifier: unknown stays fail-closed ------------------------------------

def test_classify_unknown_message():
    body = b'{"message":"Something the classifier has never seen."}'
    assert classify_403_body(body) == "unknown"


def test_classify_empty_body_is_unknown():
    assert classify_403_body(b"") == "unknown"
    assert classify_403_body("") == "unknown"
    assert classify_403_body(None) == "unknown"


def test_classify_garbage_never_raises():
    assert classify_403_body(b"\xff\xfe\x00not-utf8") == "unknown"
    assert classify_403_body(12345) == "unknown"


def test_classify_quota_beats_permission_on_mixed_body():
    # A spent token must never be mislabeled a permission fault.
    body = b"rate limit exceeded; resource not accessible is unrelated here"
    assert classify_403_body(body) == "quota"


# --- QuotaExhausted factory ----------------------------------------------------

def test_for_http_error_extracts_message_and_retry_after():
    body = b'{"message":"API rate limit exceeded for installation ID 99."}'
    exc = QuotaExhausted.for_http_error("GET /repos/x/y", fake_403(body, 30))
    assert "rate limit exceeded for installation ID 99" in str(exc)
    assert "GET /repos/x/y" in str(exc)
    assert exc.retry_after == 30
    assert "Retry-After: 30s" in str(exc)


def test_for_http_error_without_retry_after():
    body = b'{"message":"You have exceeded a secondary rate limit."}'
    exc = QuotaExhausted.for_http_error("GET /repos/x/y", fake_403(body))
    assert exc.retry_after is None
    assert "Retry-After" not in str(exc)


def test_for_http_error_accepts_preread_body():
    # Callers classify first (one read); the factory must not need a second.
    body = b'{"message":"API rate limit exceeded for user ID 7."}'
    err = fake_403(body)
    first = err.read()
    assert first == body
    exc = QuotaExhausted.for_http_error("GET /z", err, first)
    assert "rate limit exceeded for user ID 7" in str(exc)


def test_quota_exhausted_is_runtime_error():
    # Safety net: sites that only catch RuntimeError broadly stay fail-closed.
    assert isinstance(QuotaExhausted("x"), RuntimeError)


def test_retry_after_seconds_bad_header():
    assert retry_after_seconds(fake_403(b"{}", "not-a-number")) is None


def test_error_message_falls_back_to_raw_text():
    assert error_message(b"plain text body") == "plain text body"
    assert error_message(b"") == ""


# --- wiring: ci_claim_evidence_gate.api_get ------------------------------------

def test_claim_gate_api_get_quota_403_raises_quota_exhausted():
    from ci_claim_evidence_gate import api_get
    body = b'{"message":"API rate limit exceeded for installation ID 12345."}'
    with mock.patch("urllib.request.urlopen", side_effect=fake_403(body, 60)):
        try:
            api_get("/repos/x/y", "tok")
        except QuotaExhausted as e:
            assert e.retry_after == 60
            assert "installation ID 12345" in str(e)
            return
        raise AssertionError("expected QuotaExhausted, got a return")


def test_claim_gate_api_get_permission_403_stays_gate_blind():
    from ci_claim_evidence_gate import GateBlind, api_get
    body = b'{"message":"Resource not accessible by personal access token."}'
    with mock.patch("urllib.request.urlopen", side_effect=fake_403(body)):
        try:
            api_get("/repos/x/y", "tok")
        except GateBlind:
            return
        raise AssertionError("expected GateBlind, got a return")


def test_claim_gate_api_get_unknown_403_stays_gate_blind():
    from ci_claim_evidence_gate import GateBlind, api_get
    body = b'{"message":"Weird and unrecognized refusal."}'
    with mock.patch("urllib.request.urlopen", side_effect=fake_403(body)):
        try:
            api_get("/repos/x/y", "tok")
        except GateBlind:
            return
        raise AssertionError("expected GateBlind, got a return")


def test_claim_gate_api_get_500_stays_gate_blind():
    from ci_claim_evidence_gate import GateBlind, api_get
    err = urllib.error.HTTPError(
        "https://api.github.com/x", 500, "Server Error",
        Message(), io.BytesIO(b"boom"))
    with mock.patch("urllib.request.urlopen", side_effect=err):
        try:
            api_get("/repos/x/y", "tok")
        except GateBlind:
            return
        raise AssertionError("expected GateBlind, got a return")
