#!/usr/bin/env python3
"""Adversarial local checks for Superbrain truth/authority boundaries."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMOTE_PATH = ROOT / "tools" / "promote_intelligence.py"
RESTORE_PATH = ROOT / ".naya" / "runtime" / "restore_context.py"
STATE_PATH = ROOT / ".naya" / "control-plane" / "STATE.json"
START_PATH = ROOT / "START-HERE.md"
CONTRACT_PATH = ROOT / ".naya" / "SUPERBRAIN-COLD-START-AND-CONTINUITY-CONTRACT.md"

SPEC = importlib.util.spec_from_file_location("naya_promotion_engine", PROMOTE_PATH)
assert SPEC and SPEC.loader
engine = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(engine)


class SuperbrainAdversarialTests(unittest.TestCase):
    def test_canonical_identity_is_unambiguous(self):
        start = START_PATH.read_text(encoding="utf-8")
        self.assertIn("CANONICAL NAYA SUPERBRAIN / SHARED INTELLIGENCE REPOSITORY", start)
        self.assertIn("SoulSchoolAcademy/NayaPOWER", start)
        self.assertIn("MaxRESULTS remains the authoritative working repository for the MAXESS Results product", start)
        self.assertIn("It is **not** the NayaPOWER Superbrain", start)

    def test_state_never_claims_a_static_current_head(self):
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        current_head = state["current_head"]
        self.assertEqual(current_head["source"], "git:HEAD")
        self.assertEqual(current_head["mode"], "LIVE_RESOLUTION")
        self.assertTrue(current_head["recorded_head_is_not_authoritative"])

    def test_restore_has_explicit_reconciliation_boundary(self):
        restore = RESTORE_PATH.read_text(encoding="utf-8")
        self.assertIn("reconciliation_required", restore)
        self.assertIn('run_git(\'rev-parse\',\'HEAD\')', restore)
        self.assertIn("'observed_head'", restore)
        self.assertIn("'latest_handoff'", restore)
        self.assertIn("'reconciliation'", restore)

    def test_contract_requires_behavioral_acceptance(self):
        contract = CONTRACT_PATH.read_text(encoding="utf-8")
        self.assertIn("Acceptance is behavioral, not merely textual.", contract)
        self.assertIn("exactly one preferred executable next action", contract)
        self.assertIn("NOTE EVENT → PIS / PRIMARY INTELLIGENCE → RUNNING FEED / STATE PROJECTION → FUTURE NAYA RETRIEVAL", contract)

    def test_authority_home_is_not_auto_promoted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            engine.EVENT_DIR = root / "events"
            engine.RECEIPT_DIR = root / "receipts"
            engine.NAYA_DIR = root / "naya"
            engine.SHAWN_DIR = root / "shawn"
            engine.FEED_DIR = root / "feed"
            engine.HUB_PATH = root / "hub.md"
            engine.EVENT_DIR.mkdir(parents=True)
            engine.RECEIPT_DIR.mkdir(parents=True)
            engine.HUB_PATH.write_text("# Hub\n", encoding="utf-8")
            event = {
                "event_id": "ADVERSARIAL-001",
                "timestamp": "2026-08-30T19:00:00Z",
                "project": "ADVERSARIAL",
                "lesson": "A governance rule must not become canonical merely because an event was written.",
                "source": ["adversarial-test"],
                "evidence_state": "TESTED",
                "promotion_status": "PROPOSED",
                "candidate_homes": ["GUARDRAIL"],
                "what_happened": "Tested unauthorized promotion boundary.",
                "value": "Prevents memory from silently granting authority.",
                "evidence": ["tools/test_superbrain_adversarial.py"],
            }
            (engine.EVENT_DIR / "ADVERSARIAL-001.json").write_text(json.dumps(event) + "\n", encoding="utf-8")
            self.assertEqual(engine.main(), 0)
            receipt = json.loads((engine.RECEIPT_DIR / "LATEST-PROMOTION-RECEIPT.json").read_text(encoding="utf-8"))
            item = receipt["receipts"][0]
            self.assertEqual(item["promotion_status"], "PROMOTION_PROPOSAL_REQUIRES_AUTHORITY")
            self.assertIn("GUARDRAIL", item["authority_gated_homes"])
            self.assertFalse(item["verified"])
            self.assertIn("NO_FILE_WRITE_ALONE_COUNTS_AS_VERIFICATION", item["rule"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
