#!/usr/bin/env python3
"""Dependency-free tests for the canonical Note Event -> CCT boundary."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for name in ("cct_intelligent_block", "cct_note_event_promotion"):
    path = ROOT / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

cct = sys.modules["cct_intelligent_block"]
promotion = sys.modules["cct_note_event_promotion"]


class NoteEventPromotionTests(unittest.TestCase):
    def event(self):
        return {
            "event_id": "SE-20260829-120000-cct-proof",
            "type": "learning",
            "subject": "CCT",
            "learning": {"lesson": "verified reusable intelligence"},
            "why_it_matters": "enables safe reuse",
            "next_best_action": "consume and validate",
            "provenance": {"source": "NAYA-A", "kind": "runtime"},
            "evidence": [{"kind": "test", "id": "proof-1", "result": "PASS"}],
            "verification": {"status": "VERIFIED", "receipt": "receipt-1"},
        }

    def test_verified_event_promotes_to_authorized_block(self):
        block = promotion.promote_note_event(self.event(), producer="NAYA-A", consumers=["NAYA-B"])
        decision = cct.verify_block(block, consumer="NAYA-B")
        self.assertTrue(decision.allowed)
        self.assertEqual(block["provenance"]["origin"], "NAYA-A")
        self.assertEqual(block["content"]["event_id"], self.event()["event_id"])

    def test_unverified_event_fails_closed(self):
        event = self.event()
        event["verification"]["status"] = "SUPPORTED"
        with self.assertRaises(promotion.PromotionRejected):
            promotion.promote_note_event(event, producer="NAYA-A", consumers=["NAYA-B"])

    def test_missing_evidence_fails_closed(self):
        event = self.event(); event["evidence"] = []
        with self.assertRaises(promotion.PromotionRejected):
            promotion.promote_note_event(event, producer="NAYA-A", consumers=["NAYA-B"])

    def test_missing_consumer_authorization_fails_closed(self):
        with self.assertRaises(promotion.PromotionRejected):
            promotion.promote_note_event(self.event(), producer="NAYA-A", consumers=[])

    def test_consumer_not_in_explicit_scope_is_denied(self):
        block = promotion.promote_note_event(self.event(), producer="NAYA-A", consumers=["NAYA-B"])
        self.assertFalse(cct.verify_block(block, consumer="NAYA-C").allowed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
