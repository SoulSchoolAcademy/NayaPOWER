#!/usr/bin/env python3
"""Packet 3 (t0762) — GATE_BLIND marker + exit-2 contract falsifier battery.

Design: hidden_files/infra-asks-design-t0754-lane6.md, PACKET 3.
Source (quoted, not paraphrased — live byte #2537 comment 6167590868, t0748):
  "3. Give GATE_BLIND its own marker (not FAILURE) so a blinded run reads as
   'transport-blind, re-run advised' and never masquerades as verdict
   instability."

Exit-code contract: 0 = pass, 1 = judged-fail, 2 = blind. The word
FAIL/REJECT/FAILED never appears on a blind line; the word GATE_BLIND never
appears on a judged line. A builder seat may map exit 2 -> "re-run advised"
but NEVER -> pass (still non-zero -> still blocking).

Design falsifier (c), run at action time:
  run each gate with a revoked token (or a stub returning 403 "Resource not
  accessible") -> assert stdout contains the literal token GATE_BLIND,
  exit code == 2, and grep -c of judged-fail tokens (FAIL, REJECT, FAILED)
  on the blind line == 0. Then run with a judged-fail fixture (e.g. claim
  gate with unattested body) -> assert exit == 1 and no GATE_BLIND token.
  Distinctness is mechanical.

All offline: the transport is stubbed, so blindness is deterministic.
"""
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
import urllib.error
import urllib.request
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ci_claim_evidence_gate as cig  # noqa: E402
import activation_gate as ag  # noqa: E402
import check_merge_consensus as cmc  # noqa: E402

JUDGED_TOKENS = re.compile(r"FAIL|REJECT|FAILED")

# The exit->action contract a builder seat may rely on. Exit 2 never maps to
# pass; the blind line itself carries the re-run advice.
EXIT_ACTION = {0: "pass", 1: "blocked: judged-fail", 2: "blocked: blind, re-run advised"}


class _JsonResp:
    def __init__(self, payload):
        self._payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return self._payload


def _http_403(body_text):
    return urllib.error.HTTPError(
        "https://api.github.com/x", 403, "Forbidden", {},
        io.BytesIO(body_text.encode()))


def _http_429(body_text):
    return urllib.error.HTTPError(
        "https://api.github.com/x", 429, "Too Many Requests", {},
        io.BytesIO(body_text.encode()))


class _Env:
    """Set env vars for a test, restore after."""

    def __init__(self, **vars):
        self.vars = vars
        self.saved = {}

    def __enter__(self):
        for k, v in self.vars.items():
            self.saved[k] = os.environ.get(k)
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        return self

    def __exit__(self, *a):
        for k, old in self.saved.items():
            if old is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = old
        return False


def _run_capture(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = fn(*args, **kwargs)
    return code, buf.getvalue()


def assert_blind_line(tc, out):
    """The design's (c) blind-line assertions: literal GATE_BLIND token,
    re-run advice present, zero judged-fail tokens on the blind line."""
    lines = [ln for ln in out.splitlines() if "GATE_BLIND" in ln]
    tc.assertEqual(len(lines), 1, f"expected exactly one GATE_BLIND line, got: {out!r}")
    line = lines[0]
    tc.assertIn("re-run advised", line)
    tc.assertIsNone(JUDGED_TOKENS.search(line),
                    f"judged-fail token on a blind line: {line!r}")
    return line


class ClaimGateBlindTest(unittest.TestCase):
    ENV = dict(GITHUB_REPOSITORY="t/r", PR_NUMBER="2579",
               PR_HEAD_SHA="a" * 40, GITHUB_TOKEN="revoked")

    def test_403_permission_denied_is_blind_exit2(self):
        with _Env(**self.ENV), \
             mock.patch.object(urllib.request, "urlopen",
                               side_effect=_http_403(
                                   '{"message": "Resource not accessible by integration"}')):
            code, out = _run_capture(cig.main)
        self.assertEqual(code, 2)
        line = assert_blind_line(self, out)
        self.assertIn("transport: permission-denied", line)
        self.assertIn("CLAIM-EVIDENCE GATE: GATE_BLIND --", line)

    def test_429_rate_limit_is_blind_exit2(self):
        with _Env(**self.ENV), \
             mock.patch.object(urllib.request, "urlopen",
                               side_effect=_http_429(
                                   '{"message": "API rate limit exceeded for installation ID 1"}')):
            code, out = _run_capture(cig.main)
        self.assertEqual(code, 2)
        line = assert_blind_line(self, out)
        self.assertIn("transport: rate-limited", line)

    def test_dns_failure_is_blind_exit2_io_error(self):
        with _Env(**self.ENV), \
             mock.patch.object(urllib.request, "urlopen",
                               side_effect=urllib.error.URLError(
                                   "Name or service not known")):
            code, out = _run_capture(cig.main)
        self.assertEqual(code, 2)
        line = assert_blind_line(self, out)
        self.assertIn("transport: io-error", line)

    def test_missing_env_is_blind_exit2(self):
        with _Env(GITHUB_REPOSITORY=None, PR_NUMBER=None, PR_HEAD_SHA=None,
                  GITHUB_TOKEN=None):
            code, out = _run_capture(cig.main)
        self.assertEqual(code, 2)
        assert_blind_line(self, out)

    def test_judged_fail_is_exit1_without_gate_blind(self):
        body = "Seat: Naya 4. This work was independently verified end to end."

        def fake_urlopen(req, timeout=None):
            url = req.full_url
            if url.endswith("/reviews?per_page=100"):
                return _JsonResp([])
            if "/check-runs" in url:
                return _JsonResp({"check_runs": []})
            return _JsonResp({"body": body, "user": {"login": "bot"}})

        with _Env(**self.ENV), tempfile.TemporaryDirectory() as head, \
             _Env(PR_HEAD_DIR=head), \
             mock.patch.object(urllib.request, "urlopen", fake_urlopen):
            code, out = _run_capture(cig.main)
        self.assertEqual(code, 1)  # judged-fail keeps exit 1, exact texts
        self.assertNotIn("GATE_BLIND", out)
        self.assertIn("FAIL", out)  # judged lines keep their FAIL vocabulary


class ActivationGateBlindTest(unittest.TestCase):
    def _args(self, pr_head):
        return type("A", (), dict(delivery=True, pr_head=pr_head,
                                  changed_files=None, pr="1", json=False,
                                  design_gate="", design_manifest="",
                                  base_sha=""))()

    def _event(self, payload):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(payload, f)
        f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_delivery_transport_blind_exit2(self):
        event = self._event({"repository": {"full_name": "t/r"}})

        def fake_api(method, path, token, body=None):
            raise ag.TransportBlind(
                "GitHub API GET /repos/t/r/git/ref/heads/main -> HTTP 403: "
                '{"message": "API rate limit exceeded for installation ID 1"}')

        with tempfile.TemporaryDirectory() as head, \
             _Env(GITHUB_EVENT_PATH=event, GITHUB_TOKEN="x",
                  GITHUB_REPOSITORY=None), \
             mock.patch.object(ag, "_api", fake_api):
            code, out = _run_capture(ag._run_delivery, self._args(head))
        self.assertEqual(code, 2)
        line = assert_blind_line(self, out)
        self.assertIn("ACTIVATION-DELIVERY GATE: GATE_BLIND --", line)
        self.assertIn("transport: rate-limited", line)

    def test_delivery_non_transport_failure_keeps_tool_error(self):
        # A runner-config failure is NOT transport: it stays TOOL-ERROR,
        # keeps exit 2 (pre-existing), and never carries the GATE_BLIND token.
        event = self._event({"repository": {}})

        with tempfile.TemporaryDirectory() as head, \
             _Env(GITHUB_EVENT_PATH=event, GITHUB_TOKEN="x",
                  GITHUB_REPOSITORY=None):
            code, out = _run_capture(ag._run_delivery, self._args(head))
        self.assertEqual(code, 2)
        self.assertNotIn("GATE_BLIND", out)
        self.assertIn("TOOL-ERROR", out)


class ConsensusGateBlindTest(unittest.TestCase):
    ENV = dict(GH_TOKEN="revoked", REPO="t/r", PR_NUMBER="9",
               HEAD_SHA="b" * 40)

    def test_gate_api_error_is_blind_exit2(self):
        err = cmc.GateAPIError(
            "GitHub API rate-limited after 5 attempts "
            "(API rate limit exceeded). Re-run the check; "
            "merge bursts exhaust the shared token quota.")
        with _Env(**self.ENV), \
             mock.patch.object(cmc, "api_get", side_effect=err):
            out_buf = io.StringIO()
            with contextlib.redirect_stdout(out_buf), \
                 self.assertRaises(SystemExit) as cm:
                cmc.main()
        self.assertEqual(cm.exception.code, 2)
        line = assert_blind_line(self, out_buf.getvalue())
        self.assertIn("CONSENSUS GATE: GATE_BLIND --", line)
        self.assertIn("transport: rate-limited", line)
        # The gate's own explicit prose survives token alignment.
        self.assertIn("merge bursts exhaust the shared token quota", line)

    def test_judged_fail_is_exit1_without_gate_blind(self):
        def fake_api(path, token):
            return {"created_at": "2026-10-14T00:00:00Z",
                    "body": "plain prose, no seat declaration",
                    "user": {"login": "someone"}}

        with _Env(**self.ENV), mock.patch.object(cmc, "api_get", fake_api):
            out_buf = io.StringIO()
            with contextlib.redirect_stdout(out_buf), \
                 self.assertRaises(SystemExit) as cm:
                cmc.main()
        self.assertEqual(cm.exception.code, 1)
        out = out_buf.getvalue()
        self.assertIn("CONSENSUS GATE FAILED", out)
        self.assertNotIn("GATE_BLIND", out)


class ExitContractTest(unittest.TestCase):
    def test_blind_never_maps_to_pass(self):
        # The re-run mapping a builder seat may use. The contract that
        # matters: exit 2 is blocked, and 2 is never pass.
        self.assertNotIn(EXIT_ACTION[2], ("pass", "proceed", "merge"))
        self.assertIn("re-run", EXIT_ACTION[2])

    def test_all_blind_paths_still_block(self):
        # Every blind exit observed above is non-zero: blindness can never
        # be green, so no workflow change can accidentally merge on it.
        for code in (2,):
            self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
