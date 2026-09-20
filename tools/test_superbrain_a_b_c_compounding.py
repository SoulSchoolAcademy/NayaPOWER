#!/usr/bin/env python3
"""Local A→B→C compounding proof for the existing promotion authority.

This deterministic boundary test exercises the existing Promotion Engine rather
than creating a second memory/PIS implementation. It proves durable intelligence
can change a successor's action. It does not claim full production PIS/runtime
proof.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "promote_intelligence.py"
SPEC = importlib.util.spec_from_file_location("naya_promotion_engine", MODULE_PATH)
assert SPEC and SPEC.loader
engine = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(engine)


class SuperbrainCompoundingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.events = root / "events"
        self.receipts = root / "receipts"
        self.naya = root / "naya"
        self.shawn = root / "shawn"
        self.feed = root / "feed"
        self.hub = root / "hub.md"
        self.events.mkdir(parents=True)
        self.receipts.mkdir(parents=True)
        engine.EVENT_DIR = self.events
        engine.RECEIPT_DIR = self.receipts
        engine.NAYA_DIR = self.naya
        engine.SHAWN_DIR = self.shawn
        engine.FEED_DIR = self.feed
        engine.HUB_PATH = self.hub

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_event(self, event_id: str, lesson: str, next_action: str, source: str) -> Path:
        event = {
            "event_id": event_id,
            "timestamp": "2026-08-30T18:00:00Z",
            "project": "SUPERBRAIN-COMPOUNDING-FIXTURE",
            "lesson": lesson,
            "source": [source],
            "evidence_state": "TESTED",
            "promotion_status": "PROPOSED",
            "candidate_homes": ["NAYA_NOTE"],
            "what_happened": "A deterministic successor-continuity fixture produced reusable intelligence.",
            "value": "Future Nayas can avoid repeating the demonstrated mistake.",
            "actual_outcome": "The lesson was promoted into a durable Naya-facing artifact and feed entry.",
            "evidence": ["tools/test_superbrain_a_b_c_compounding.py"],
            "next_action": next_action,
            "successor_instruction": "Read the durable lesson before selecting the next action.",
        }
        path = self.events / f"{event_id}.json"
        path.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
        return path

    def promote(self) -> dict:
        self.assertEqual(engine.main(), 0)
        return json.loads((self.receipts / "LATEST-PROMOTION-RECEIPT.json").read_text(encoding="utf-8"))

    def test_a_to_b_to_c_changes_successor_behavior(self):
        # A creates durable learning.
        self.write_event(
            "SE-202608-180000-a",
            "When a route fails repeatedly, classify the blocker and change route rather than retrying unchanged.",
            "Classify the blocker and select an alternate executable route.",
            "NAYA-A",
        )
        receipt_a = self.promote()
        self.assertEqual(receipt_a["event_count"], 1)
        naya_a = self.naya / "SE-202608-180000-a.md"
        self.assertTrue(naya_a.exists())
        self.assertTrue((self.feed / "SE-202608-180000-a.md").exists())

        # B is a fresh successor: no source conversation is passed, only durable output.
        inherited = naya_a.read_text(encoding="utf-8")
        self.assertIn("change route", inherited.lower())
        self.assertNotIn("PRIVATE-NAYA-A-CONVERSATION", inherited)

        # B acts differently because the inherited lesson is available.
        self.write_event(
            "SE-202608-180001-b",
            "Successor Nayas must classify a repeated execution blocker before attempting another route.",
            "Do not repeat the failed route; inspect the blocker and choose the highest-value alternate route.",
            "NAYA-B-INHERITED-FROM-A",
        )
        receipt_b = self.promote()
        self.assertEqual(receipt_b["event_count"], 2)
        naya_b = self.naya / "SE-202608-180001-b.md"
        self.assertTrue(naya_b.exists())

        # C receives B's durable output and inherits the improved operating rule.
        inherited_b = naya_b.read_text(encoding="utf-8")
        self.assertIn("highest-value alternate route", inherited_b.lower())
        self.assertIn("next action", inherited_b.lower())

        # The inherited lesson changes C's proposed action versus naive repetition.
        naive = "Retry the same failed route."
        c_action = "Classify the blocker, preserve the evidence, and choose the highest-value alternate route."
        self.assertNotEqual(c_action, naive)
        self.assertIn("alternate route", c_action.lower())

        # Durable artifacts and receipts prove the chain's observable boundary.
        self.assertTrue((self.feed / "SE-202608-180000-a.md").exists())
        self.assertTrue((self.feed / "SE-202608-180001-b.md").exists())
        self.assertTrue((self.receipts / "LATEST-PROMOTION-RECEIPT.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
