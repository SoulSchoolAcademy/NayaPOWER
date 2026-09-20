#!/usr/bin/env python3
import unittest
from naya_claim import Claim, authorize_write, conflicts, validate_claim

NOW = "2026-08-29T22:00:00+00:00"
LATER = "2026-08-29T23:00:00+00:00"


def claim(work_id="A", owner="NAYA-A", scope="cct-003", files=("a.py",), base="abc"):
    return Claim(work_id, owner, "CCT-003", scope, tuple(files), base, "tests pass", "IN_PROGRESS", NOW, LATER)


class ClaimTests(unittest.TestCase):
    def test_valid_claim(self):
        self.assertEqual(validate_claim(claim(), now=NOW)[0], True)

    def test_expired_claim_fails_closed(self):
        expired = Claim("A", "NAYA-A", "CCT-003", "cct-003", ("a.py",), "abc", "tests pass", "IN_PROGRESS", "2026-08-29T20:00:00+00:00", "2026-08-29T21:00:00+00:00")
        self.assertFalse(validate_claim(expired, now=NOW)[0])

    def test_overlapping_active_claim_conflicts(self):
        self.assertEqual(conflicts(claim("B", "NAYA-B"), [claim()], now=NOW), ["A"])

    def test_disjoint_claim_is_safe(self):
        # A different scope and file set is genuinely disjoint. Same-scope claims
        # intentionally conflict even when they touch different files.
        self.assertEqual(conflicts(claim("B", "NAYA-B", scope="cct-004", files=("b.py",)), [claim()], now=NOW), [])

    def test_stale_base_commit_fails_closed(self):
        allowed, reason = authorize_write(claim(), current_commit="different", existing=[], now=NOW)
        self.assertFalse(allowed)
        self.assertEqual(reason, "stale base commit")

    def test_conflicting_claim_blocks_write(self):
        allowed, reason = authorize_write(claim("B", "NAYA-B"), current_commit="abc", existing=[claim()], now=NOW)
        self.assertFalse(allowed)
        self.assertIn("A", reason)

    def test_done_claim_cannot_write(self):
        done = Claim("A", "NAYA-A", "CCT-003", "cct-003", ("a.py",), "abc", "tests pass", "DONE", NOW, LATER)
        allowed, _ = authorize_write(done, current_commit="abc", existing=[], now=NOW)
        self.assertFalse(allowed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
