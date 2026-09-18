#!/usr/bin/env python3
"""Adversarial acceptance tests for the CCT -> Superbrain boundary."""
from __future__ import annotations

import unittest

from cct_intelligent_block import make_block
from cct_superbrain_coordination import CoordinationRejected, coordinate_next_action
from naya_claim import Claim

NOW = "2026-08-29T20:00:00Z"
BASE = "abc123"


def claim(*, work_id="W-1", owner="naya-a", base=BASE, status="IN_PROGRESS"):
    return Claim(work_id, owner, "T-1", "superbrain", (".naya/runtime/example.py",), base,
                 "tests pass", status, "2026-08-29T19:00:00Z", "2026-08-29T21:00:00Z")


def block(*, consumer="naya-a", verification="VERIFIED"):
    return make_block(block_id="IB-1", producer="naya-source", content={"next_best_action": "execute"},
                      evidence=[{"type": "VERIFIED", "ref": "E-1"}],
                      permissions={"consumers": [consumer], "purposes": ["execute"]}, verification=verification)


def action(*, work_id="W-1", block_id="IB-1"):
    return {"action_id": "A-1", "objective": "advance mission", "instruction": "run the next verified action",
            "acceptance": "record evidence", "claim_work_id": work_id, "block_id": block_id}


class CoordinationBoundaryTests(unittest.TestCase):
    def run_boundary(self, **kwargs):
        defaults = dict(block=block(), consumer="naya-a", claim=claim(), current_commit=BASE,
                        existing_claims=[], next_action=action(), now=NOW)
        defaults.update(kwargs)
        return coordinate_next_action(**defaults)

    def test_accepts_verified_bound_action(self):
        result = self.run_boundary()
        self.assertEqual(result["schema"], "naya/cct/superbrain-coordination/v1")
        self.assertEqual(result["claim_work_id"], "W-1")
        self.assertEqual(result["block_id"], "IB-1")
        self.assertEqual(result["base_commit"], BASE)

    def test_rejects_unverified_cct_block(self):
        with self.assertRaisesRegex(CoordinationRejected, "CCT block rejected"):
            self.run_boundary(block=block(verification="UNVERIFIED"))

    def test_rejects_unauthorized_consumer(self):
        with self.assertRaisesRegex(CoordinationRejected, "consumer is not authorized"):
            self.run_boundary(block=block(consumer="naya-b"))

    def test_rejects_stale_claim(self):
        with self.assertRaisesRegex(CoordinationRejected, "stale base commit"):
            self.run_boundary(claim=claim(base="old"))

    def test_rejects_conflicting_active_claim(self):
        with self.assertRaisesRegex(CoordinationRejected, "conflicting active claims"):
            self.run_boundary(existing_claims=[claim(work_id="W-2", owner="naya-b")])

    def test_rejects_action_bound_to_different_claim(self):
        with self.assertRaisesRegex(CoordinationRejected, "not bound to the active claim"):
            self.run_boundary(next_action=action(work_id="W-9"))

    def test_rejects_action_bound_to_different_cct_block(self):
        with self.assertRaisesRegex(CoordinationRejected, "not bound to the verified CCT block"):
            self.run_boundary(next_action=action(block_id="IB-9"))

    def test_rejects_incomplete_action(self):
        bad = action()
        del bad["instruction"]
        with self.assertRaisesRegex(CoordinationRejected, "missing required fields"):
            self.run_boundary(next_action=bad)

    def test_rejects_expired_claim_even_with_current_commit(self):
        expired = Claim("W-1", "naya-a", "T-1", "superbrain", (".naya/runtime/example.py",), BASE,
                        "tests pass", "IN_PROGRESS", "2026-08-29T18:00:00Z", "2026-08-29T19:00:00Z")
        with self.assertRaisesRegex(CoordinationRejected, "claim rejected: active claim is expired"):
            self.run_boundary(claim=expired)


if __name__ == "__main__":
    unittest.main(verbosity=2)
