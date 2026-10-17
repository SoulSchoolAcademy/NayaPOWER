#!/usr/bin/env python3
"""Local tests for RATE_LIMIT_RESET capture (Kappa w207 spec, Lambda w212 impl).

The gates failed blind on installation-403 rate limits (w209 GATE_BLIND at
07:16:40Z): GitHub returns X-RateLimit-Reset (epoch seconds) on 403s and both
HTTP layers discarded the headers before failing closed. These tests prove the
capture fires — by mocking urllib at the seam, never touching live CI.

Contract: on a 403 carrying X-RateLimit-Reset, the layer prints exactly
    RATE_LIMIT_RESET epoch=<N> path=<p> status=403
and STILL fails closed (GateBlind / RuntimeError). Every other failure shape
is unchanged: no emit, same raise.
"""

import io
import os
import sys
import unittest
import urllib.error
from contextlib import redirect_stdout
from email.message import Message
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import activation_gate as ag  # noqa: E402
import ci_claim_evidence_gate as ceg  # noqa: E402

_EPOCH = 1760518800  # a fixed reset clock for the assertion
_PATH = "/repos/SoulSchoolAcademy/NayaPOWER/git/ref/heads/main"


def _http_error(code, reset=None):
    hdrs = Message()
    if reset is not None:
        hdrs["X-RateLimit-Reset"] = str(reset)
    return urllib.error.HTTPError(
        "https://api.github.com" + _PATH, code, "msg", hdrs,
        io.BytesIO(b'{"message":"rate limited"}'))


def _emit_lines(captured):
    return [ln for ln in captured.getvalue().splitlines()
            if ln.startswith("RATE_LIMIT_RESET")]


class ClaimEvidenceCaptureTest(unittest.TestCase):
    def _run(self, exc):
        with patch.object(ceg.urllib.request, "urlopen", side_effect=exc):
            buf = io.StringIO()
            with redirect_stdout(buf):
                with self.assertRaises(ceg.GateBlind):
                    ceg.api_get(_PATH, token="deadbeef")
            return buf

    def test_403_with_reset_emits_and_fails_closed(self):
        buf = self._run(_http_error(403, _EPOCH))
        self.assertEqual(
            _emit_lines(buf),
            [f"RATE_LIMIT_RESET epoch={_EPOCH} path={_PATH} status=403"])

    def test_403_without_header_no_emit_still_blind(self):
        self.assertEqual(_emit_lines(self._run(_http_error(403))), [])

    def test_non403_with_header_no_emit_still_blind(self):
        self.assertEqual(_emit_lines(self._run(_http_error(404, _EPOCH))), [])

    def test_nonhttp_failure_no_emit_still_blind(self):
        buf = io.StringIO()
        with patch.object(ceg.urllib.request, "urlopen",
                          side_effect=urllib.error.URLError("socket down")):
            with redirect_stdout(buf):
                with self.assertRaises(ceg.GateBlind):
                    ceg.api_get(_PATH, token="deadbeef")
        self.assertEqual(_emit_lines(buf), [])


class DeliveryGateCaptureTest(unittest.TestCase):
    def _run(self, exc):
        with patch.object(ag.urllib.request, "urlopen", side_effect=exc):
            buf = io.StringIO()
            with redirect_stdout(buf):
                with self.assertRaises(RuntimeError) as ctx:
                    ag._api("GET", _PATH, "deadbeef")
            return buf, str(ctx.exception)

    def test_403_with_reset_emits_and_fails_closed(self):
        buf, msg = self._run(_http_error(403, _EPOCH))
        self.assertEqual(
            _emit_lines(buf),
            [f"RATE_LIMIT_RESET epoch={_EPOCH} path={_PATH} status=403"])
        self.assertIn("HTTP 403", msg)  # original RuntimeError shape preserved

    def test_403_without_header_no_emit_still_raises(self):
        buf, _ = self._run(_http_error(403))
        self.assertEqual(_emit_lines(buf), [])

    def test_non403_with_header_no_emit_still_raises(self):
        buf, _ = self._run(_http_error(422, _EPOCH))
        self.assertEqual(_emit_lines(buf), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
