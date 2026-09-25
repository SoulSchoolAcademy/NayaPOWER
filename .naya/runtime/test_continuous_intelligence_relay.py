#!/usr/bin/env python3
"""
Comprehensive test suite for Continuous Intelligence Relay
Tests: Activity → Learning → Playback → Baton automation chain
"""
from __future__ import annotations
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

from continuous_intelligence_relay import (
    relay_from_execution_receipt,
    extract_learning_from_event,
    create_learning_candidate,
    update_playback_lineage,
    rebuild_baton,
    update_activity_board,
    load_json,
    save_json,
)


class TestContinuousIntelligenceRelay(unittest.TestCase):
    """Test the continuous intelligence relay automation chain"""

    def setUp(self):
        """Set up isolated temp environment for each test"""
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="cir-test-"))
        
        # Override paths to use temp directory
        import continuous_intelligence_relay as cir
        cir.ROOT = self.tmp_dir
        cir.PI = self.tmp_dir / ".naya" / "project-intelligence"
        cir.CONTROL_PLANE = self.tmp_dir / ".naya" / "control-plane"
        cir.STATE = self.tmp_dir / ".naya" / "control-plane" / "STATE.json"
        cir.BLOCKS = self.tmp_dir / ".naya" / "control-plane" / "BLOCKS.json"
        cir.MAP = self.tmp_dir / ".naya" / "control-plane" / "MAP.json"
        cir.PROOF = self.tmp_dir / ".naya" / "control-plane" / "PROOF.json"
        cir.BATON = self.tmp_dir / ".naya" / "control-plane" / "BATON.json"
        cir.ACTIVITY_BOARD = self.tmp_dir / "NAYA" / "ACTIVITY" / "00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md"
        
        # Create directory structure
        cir.CONTROL_PLANE.mkdir(parents=True, exist_ok=True)
        cir.PI.mkdir(parents=True, exist_ok=True)
        cir.ACTIVITY_BOARD.parent.mkdir(parents=True, exist_ok=True)
        
        # Create minimal control plane files
        cir.save_json(cir.STATE, {
            "single_next_action": "Test next action from STATE"
        })
        cir.save_json(cir.BLOCKS, {"active_block": {"id": "TEST", "status": "VERIFIED"}})
        cir.save_json(cir.MAP, {"mission": "Test mission"})
        cir.save_json(cir.PROOF, {"current_evidence": {}})
        cir.save_json(cir.BATON, {
            "$schema": "naya/control-plane/baton/v1",
            "status": "CANONICAL",
            "evidence": [],
            "next_action": {"action": "Initial action", "status": "BLOCKED"}
        })

    def tearDown(self):
        """Clean up temp directory"""
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_extract_learning_from_event_positive(self):
        """Test learning extraction from learning-worthy event"""
        event = {
            "observed_result": "Verified learning improved policy from 0 to 1 on held-out case",
            "event_id": "test-event-001",
            "receipt_id": "test-receipt-001",
        }
        
        learning = extract_learning_from_event(event)
        
        self.assertIsNotNone(learning)
        self.assertEqual(learning["claim"], event["observed_result"])
        self.assertEqual(learning["source_event_id"], event["event_id"])
        self.assertEqual(learning["source_receipt_id"], event["receipt_id"])
        self.assertEqual(learning["status"], "CANDIDATE")
        self.assertEqual(learning["level"], "E1_UNDERSTANDS")

    def test_extract_learning_from_event_negative(self):
        """Test no learning extracted from non-learning event"""
        event = {
            "observed_result": "Routine execution completed successfully",
            "event_id": "test-event-002",
        }
        
        learning = extract_learning_from_event(event)
        self.assertIsNone(learning)

    def test_extract_learning_various_keywords(self):
        """Test learning extraction catches various keywords"""
        keywords = ["learning", "verified", "improved", "discovered", "confirmed"]
        
        for kw in keywords:
            event = {"observed_result": f"Event with {kw} in result", "event_id": "test"}
            learning = extract_learning_from_event(event)
            self.assertIsNotNone(learning, f"Should detect '{kw}' keyword")

    def test_create_learning_candidate(self):
        """Test learning candidate creation and persistence"""
        learning = {
            "claim": "Test learning claim",
            "source_event_id": "test-event-001",
            "source_receipt_id": "test-receipt-001",
            "level": "E1_UNDERSTANDS",
            "provenance": "RUNTIME_OBSERVATION",
            "status": "CANDIDATE",
            "verification_method": "AUTOMATIC_EXTRACTION",
        }
        
        import continuous_intelligence_relay as cir
        evidence_id = create_learning_candidate(learning)
        
        self.assertTrue(evidence_id.startswith("learning-test-event-001-"))
        self.assertIn("evidence_id", learning)
        self.assertEqual(learning["evidence_id"], evidence_id)
        
        # Verify file was created
        learning_file = cir.PI / f"{evidence_id}.json"
        self.assertTrue(learning_file.exists())
        
        # Verify content
        saved = cir.load_json(learning_file)
        self.assertEqual(saved["claim"], "Test learning claim")

    def test_update_playback_lineage(self):
        """Test playback lineage update"""
        event = {
            "event_id": "test-event-001",
            "event_type": "TEST_EVENT",
            "action": "test_action",
            "status": "SUCCESS",
            "receipt_id": "test-receipt-001",
            "next_action": "Continue test",
        }
        
        import continuous_intelligence_relay as cir
        update_playback_lineage(event)
        
        lineage_path = cir.CONTROL_PLANE / "PLAYBACK_LINEAGE.json"
        self.assertTrue(lineage_path.exists())
        
        lineage = cir.load_json(lineage_path)
        self.assertEqual(len(lineage["lineage"]), 1)
        self.assertEqual(lineage["lineage"][0]["event_id"], "test-event-001")
        self.assertEqual(lineage["latest_event_id"], "test-event-001")

    def test_rebuild_baton(self):
        """Test baton rebuild with event and learning"""
        event = {
            "event_id": "test-event-001",
            "action": "test_action",
            "status": "SUCCESS",
            "receipt_id": "test-receipt-001",
            "next_action": "New next action from event",
        }
        learning = {
            "evidence_id": "learning-test-001",
            "claim": "Test learning",
            "status": "CANDIDATE",
        }
        
        import continuous_intelligence_relay as cir
        rebuild_baton(event, learning)
        
        baton = cir.load_json(cir.BATON)
        
        # Check evidence updated
        evidence_kinds = [e["kind"] for e in baton["evidence"]]
        self.assertIn("activity_event", evidence_kinds)
        self.assertIn("learning_candidate", evidence_kinds)
        
        # Check next action updated
        self.assertEqual(baton["next_action"]["action"], "New next action from event")
        self.assertIn("Derived from event", baton["next_action"]["reason"])

    def test_update_activity_board(self):
        """Test activity board update"""
        event = {
            "event_type": "TEST_EVENT",
            "event_id": "test-event-001",
            "action": "test_action",
            "status": "SUCCESS",
            "receipt_id": "test-receipt-001",
        }
        learning = {
            "claim": "Test learning claim",
            "status": "CANDIDATE",
            "evidence_id": "learning-test-001",
        }
        
        import continuous_intelligence_relay as cir
        update_activity_board(event, learning)
        
        board_content = cir.ACTIVITY_BOARD.read_text(encoding="utf-8")
        self.assertIn("TEST_EVENT", board_content)
        self.assertIn("test-event-001", board_content)
        self.assertIn("Test learning claim", board_content)
        self.assertIn("CANDIDATE", board_content)

    def test_full_relay_chain(self):
        """Test the complete relay chain: receipt → event → learning → lineage → baton → board"""
        mock_receipt = {
            "id": "test-receipt-001",
            "revision": 1,
            "action": "intelligence_commit",
            "expected_result": "Learning captured as Intelligent Block",
            "observed_result": "Verified learning improved policy from 0 to 1 on held-out case",
            "status": "SUCCESS",
            "evidence": {"event_id": "test-event-001"},
            "learning": [{"type": "policy_improvement", "before": 0, "after": 1}],
            "authority_grant_id": "test-grant-001",
            "authority_source_event_id": "test-source-001",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        
        result = relay_from_execution_receipt(mock_receipt)
        
        # Verify result structure
        self.assertEqual(result["status"], "RELAYED")
        self.assertIn("event", result)
        self.assertIn("learning", result)
        self.assertIsNotNone(result["learning"])
        
        # Verify event structure
        event = result["event"]
        self.assertEqual(event["action"], "intelligence_commit")
        self.assertEqual(event["status"], "SUCCESS")
        self.assertEqual(event["receipt_id"], "test-receipt-001")
        self.assertEqual(event["next_action"], "Test next action from STATE")
        
        # Verify learning extracted
        learning = result["learning"]
        self.assertEqual(learning["claim"], "Verified learning improved policy from 0 to 1 on held-out case")
        self.assertEqual(learning["status"], "CANDIDATE")
        
        # Verify files created
        import continuous_intelligence_relay as cir
        
        # Learning file
        learning_file = cir.PI / f"{learning['evidence_id']}.json"
        self.assertTrue(learning_file.exists())
        
        # Playback lineage
        lineage_path = cir.CONTROL_PLANE / "PLAYBACK_LINEAGE.json"
        self.assertTrue(lineage_path.exists())
        lineage = cir.load_json(lineage_path)
        self.assertEqual(len(lineage["lineage"]), 1)
        
        # Baton updated
        baton = cir.load_json(cir.BATON)
        self.assertTrue(any(e["kind"] == "activity_event" for e in baton["evidence"]))
        self.assertTrue(any(e["kind"] == "learning_candidate" for e in baton["evidence"]))
        self.assertEqual(baton["next_action"]["action"], "Test next action from STATE")
        
        # Activity board
        board_content = cir.ACTIVITY_BOARD.read_text(encoding="utf-8")
        self.assertIn("EXECUTION_COMPLETED", board_content)
        self.assertIn("learning-execution-receipt", board_content)

    def test_relay_idempotent_on_same_receipt(self):
        """Test that relaying the same receipt produces consistent results"""
        mock_receipt = {
            "id": "test-receipt-002",
            "revision": 1,
            "action": "test_action",
            "expected_result": "Test",
            "observed_result": "Verified learning improved outcome",
            "status": "SUCCESS",
            "evidence": {"event_id": "test-event-002"},
            "learning": [],
            "authority_grant_id": "test-grant-002",
            "authority_source_event_id": "test-source-002",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        
        # First relay
        result1 = relay_from_execution_receipt(mock_receipt)
        
        # Second relay (same receipt)
        result2 = relay_from_execution_receipt(mock_receipt)
        
        # Learning evidence ID should be different (timestamp-based) but claim same
        self.assertEqual(result1["learning"]["claim"], result2["learning"]["claim"])
        
        # Lineage should have 2 entries
        import continuous_intelligence_relay as cir
        lineage = cir.load_json(cir.CONTROL_PLANE / "PLAYBACK_LINEAGE.json")
        self.assertEqual(len(lineage["lineage"]), 2)

    def test_no_learning_for_non_learning_events(self):
        """Test that routine events don't generate learning candidates"""
        mock_receipt = {
            "id": "test-receipt-003",
            "revision": 1,
            "action": "routine_action",
            "expected_result": "Routine completed",
            "observed_result": "Routine execution completed successfully",
            "status": "SUCCESS",
            "evidence": {"event_id": "test-event-003"},
            "learning": [],
            "authority_grant_id": "test-grant-003",
            "authority_source_event_id": "test-source-003",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        
        result = relay_from_execution_receipt(mock_receipt)
        
        # Should not extract learning
        self.assertIsNone(result["learning"])
        
        # But should still update baton and board
        import continuous_intelligence_relay as cir
        baton = cir.load_json(cir.BATON)
        self.assertTrue(any(e["kind"] == "activity_event" for e in baton["evidence"]))
        self.assertFalse(any(e["kind"] == "learning_candidate" for e in baton["evidence"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)