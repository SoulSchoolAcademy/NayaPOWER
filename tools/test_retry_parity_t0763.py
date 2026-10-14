#!/usr/bin/env python3
"""Retry-parity falsifier battery (packet 1, design infra-asks-t0754).

CANDIDATE verification for the claim/delivery gate retry-parity mechanism
(branch naya/retry-parity-t0763). Offline: every transport is stubbed —
zero github.com traffic. Runs with: python3 tools/test_retry_parity_t0763.py

Falsifier (design (c)):
  F1: stubbed transport returns 403, 403, then 200 -> gate emits two retry
      lines then PASS and made exactly 3 HTTP calls.
  F2: stub returns 403 "Resource not accessible" -> exactly 1 call and
      immediate blind (permission fails fast).
Plus T3, the positive control the brief requires: transport-blindness flips
the verdict on otherwise identical inputs (the #2579 pattern).
"""
import io
import json
import os
import sys
import unittest
from email.message import Message

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ci_claim_evidence_gate as claim_gate  # noqa: E402
import activation_gate as delivery_gate  # noqa: E402


def _http_error(code, body_text, rate_remaining="0", retry_after=None):
    hdrs = Message()
    hdrs["X-RateLimit-Remaining"] = rate_remaining
    hdrs["X-RateLimit-Reset"] = "1799999999"
    if retry_after is not None:
        hdrs["Retry-After"] = str(retry_after)
    return __import__("urllib.error", fromlist=["error"]).HTTPError(
        "https://api.github.com/x", code, "Forbidden",
        hdrs, io.BytesIO(body_text.encode("utf-8")))


def _ok_response(payload):
    class _Resp:
        def __enter__(self):
            return io.BytesIO(json.dumps(payload).encode("utf-8"))

        def __exit__(self, *a):
            return False

    return _Resp()


def _stub_urlopen(sequence):
    """Build a urlopen replacement. sequence items: ('err', HTTPError) or
    ('ok', payload-dict). Returns (fn, calls_list)."""
    calls = []

    def _fn(req, timeout=None):
        calls.append(getattr(req, "full_url", str(req)))
        kind, item = sequence[min(len(calls) - 1, len(sequence) - 1)]
        if kind == "err":
            raise item
        return _ok_response(item)

    return _fn, calls


def _rate_limit_403():
    return _http_error(
        403, '{"message": "API rate limit exceeded for installation.", '
        '"documentation_url": "https://docs.github.com/rest"}')


def _permission_403():
    return _http_error(
        403, '{"message": "Resource not accessible by integration", '
        '"documentation_url": "https://docs.github.com/rest"}',
        rate_remaining="60")


class ClaimGateRetryTests(unittest.TestCase):
    def setUp(self):
        self._orig_urlopen = claim_gate.urllib.request.urlopen
        self._orig_sleep = claim_gate.time.sleep
        claim_gate.time.sleep = lambda s: None  # battery must not wait

    def tearDown(self):
        claim_gate.urllib.request.urlopen = self._orig_urlopen
        claim_gate.time.sleep = self._orig_sleep

    def test_F1_two_retries_then_pass_exactly_3_calls(self):
        """Falsifier F1: 403, 403, 200 -> two retry lines, PASS, 3 calls."""
        fn, calls = _stub_urlopen([
            ("err", _rate_limit_403()),
            ("err", _rate_limit_403()),
            ("ok", {"body": "x"}),
        ])
        claim_gate.urllib.request.urlopen = fn
        err = io.StringIO()
        old = sys.stderr
        sys.stderr = err
        try:
            got = claim_gate.api_get("/repos/o/r/pulls/1", "tok")
        finally:
            sys.stderr = old
        self.assertEqual(got, {"body": "x"})
        self.assertEqual(len(calls), 3, f"expected 3 HTTP calls, got {len(calls)}")
        lines = err.getvalue()
        self.assertIn("(attempt 1/5)", lines)
        self.assertIn("(attempt 2/5)", lines)
        self.assertIn("x-ratelimit-remaining=0", lines)
        self.assertIn("waiting 1s", lines)   # formula: 1 * 2^(1-1)
        self.assertIn("waiting 2s", lines)   # formula: 1 * 2^(2-1)

    def test_F2_permission_403_fails_fast_one_call(self):
        """Falsifier F2: 403 'Resource not accessible' -> 1 call, blind."""
        fn, calls = _stub_urlopen([("err", _permission_403())])
        claim_gate.urllib.request.urlopen = fn
        with self.assertRaises(claim_gate.GateBlind):
            claim_gate.api_get("/repos/o/r/pulls/1", "tok")
        self.assertEqual(len(calls), 1, f"expected 1 HTTP call, got {len(calls)}")

    def test_T3_verdict_follows_transport_same_inputs(self):
        """Positive control (the #2579 pattern): identical inputs, transport
        moved, verdict moved. Available -> PASS; blind -> GateBlind (fail closed)."""
        orig = claim_gate.api_get
        pr_body = {"body": "plain body with no attestations at all"}

        claim_gate.api_get = lambda path, token: pr_body
        try:
            code = claim_gate.run_gate("o/r", "1", "a" * 40, "/tmp", "tok")
        finally:
            claim_gate.api_get = orig
        self.assertEqual(code, 0, "transport available -> PASS (exit 0)")

        def _blind(path, token):
            raise claim_gate.GateBlind("GET /repos/o/r/pulls/1 failed: sim")

        claim_gate.api_get = _blind
        try:
            with self.assertRaises(claim_gate.GateBlind):
                claim_gate.run_gate("o/r", "1", "a" * 40, "/tmp", "tok")
        finally:
            claim_gate.api_get = orig

    def test_T3b_blind_path_exit_code_unchanged(self):
        """Blind still fails closed with the EXISTING exit code (packet 1 does
        not adopt packet-3's exit-2 contract — scope hold, stated in receipt)."""
        env = {"GITHUB_REPOSITORY": "o/r", "PR_NUMBER": "1",
               "PR_HEAD_SHA": "a" * 40, "GITHUB_TOKEN": "tok"}
        old_env = dict(os.environ)
        os.environ.update(env)
        orig = claim_gate.run_gate
        claim_gate.run_gate = lambda *a: (_ for _ in ()).throw(
            claim_gate.GateBlind("sim"))
        out = io.StringIO()
        old_out = sys.stdout
        sys.stdout = out
        try:
            code = claim_gate.main()
        finally:
            sys.stdout = old_out
            claim_gate.run_gate = orig
            os.environ.clear()
            os.environ.update(old_env)
        self.assertEqual(code, 1, "blind -> exit 1 (unchanged)")
        self.assertIn("GATE_BLIND", out.getvalue())


class DeliveryGateRetryTests(unittest.TestCase):
    def setUp(self):
        self._orig_urlopen = delivery_gate.urllib.request.urlopen
        self._orig_sleep = delivery_gate.time.sleep
        delivery_gate.time.sleep = lambda s: None

    def tearDown(self):
        delivery_gate.urllib.request.urlopen = self._orig_urlopen
        delivery_gate.time.sleep = self._orig_sleep

    def test_F1_two_retries_then_success_exactly_3_calls(self):
        fn, calls = _stub_urlopen([
            ("err", _rate_limit_403()),
            ("err", _rate_limit_403()),
            ("ok", {"sha": "abc"}),
        ])
        delivery_gate.urllib.request.urlopen = fn
        err = io.StringIO()
        old = sys.stderr
        sys.stderr = err
        try:
            got = delivery_gate._api("GET", "/repos/o/r", "tok")
        finally:
            sys.stderr = old
        self.assertEqual(got, {"sha": "abc"})
        self.assertEqual(len(calls), 3, f"expected 3 HTTP calls, got {len(calls)}")
        lines = err.getvalue()
        self.assertIn("ACTIVATION-DELIVERY GATE: api retry", lines)
        self.assertIn("(attempt 1/5)", lines)
        self.assertIn("(attempt 2/5)", lines)

    def test_F2_permission_403_raises_immediately_one_call(self):
        fn, calls = _stub_urlopen([("err", _permission_403())])
        delivery_gate.urllib.request.urlopen = fn
        err = io.StringIO()
        old = sys.stderr
        sys.stderr = err
        try:
            with self.assertRaises(RuntimeError):
                delivery_gate._api("GET", "/repos/o/r", "tok")
        finally:
            sys.stderr = old
        self.assertEqual(len(calls), 1, f"expected 1 HTTP call, got {len(calls)}")
        self.assertNotIn("api retry", err.getvalue())

    def test_exhaustion_message_names_rate_limit(self):
        fn, _ = _stub_urlopen([("err", _rate_limit_403()) for _ in range(5)])
        delivery_gate.urllib.request.urlopen = fn
        with self.assertRaises(RuntimeError) as ctx:
            delivery_gate._api("GET", "/repos/o/r", "tok")
        self.assertIn("rate-limited after 5 attempts", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
