#!/usr/bin/env python3
"""Adversarial regression test for the P0-01 execution/activity boundary."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"
spec = importlib.util.spec_from_file_location("execution_controller_activity_gate", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class ActivityGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.state_original = module.STATE
        self.events_original = module.ACTIVITY_EVENTS_ROOT
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        module.STATE = root / "EXECUTION-STATE.json"
        module.ACTIVITY_EVENTS_ROOT = root / "events"

    def tearDown(self) -> None:
        module.STATE = self.state_original
        module.ACTIVITY_EVENTS_ROOT = self.events_original
        self.temp.cleanup()

    def _reach_verified(self) -> None:
        module.transition(
            "CLAIMED",
            claim_id="EXEC-P0-01-TEST",
            block_id="B-P0-01-TEST",
            owner="Naya-Test",
            scope=["runtime/activity-gate"],
            start_head="test-head",
        )
        module.transition("EXECUTING")
        module.transition("OBSERVED", observation="test observation")
        module.transition(
            "VERIFIED",
            evidence=["receipt:p0-01-test"],
            verification={"status": "VERIFIED", "method": "unit-test"},
        )

    def test_missing_activity_event_blocks_terminal_completion(self) -> None:
        self._reach_verified()
        with self.assertRaisesRegex(AssertionError, "Activity Feed event not found"):
            module.transition(
                "HANDED_OFF",
                next_action="continue",
                handoff={"current_state": "VERIFIED"},
                activity_event_id="SE-20990101-000001-missing",
            )
        self.assertEqual(module.load()["status"], "VERIFIED")

    def test_unposted_activity_event_blocks_terminal_completion(self) -> None:
        self._reach_verified()
        event_id = "SE-20990101-000002-unposted"
        event_dir = module.ACTIVITY_EVENTS_ROOT / "2099/01/01/00"
        event_dir.mkdir(parents=True)
        (event_dir / f"{event_id}.json").write_text(
            json.dumps(
                {
                    "event_id": event_id,
                    "execution_id": "EXEC-P0-01-TEST",
                    "event_type": "execution-milestone",
                    "verification": {"status": "VERIFIED", "feed_posted": False},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(AssertionError, "not verified as feed_posted"):
            module.transition(
                "HANDED_OFF",
                next_action="continue",
                handoff={"current_state": "VERIFIED"},
                activity_event_id=event_id,
            )
        self.assertEqual(module.load()["status"], "VERIFIED")

    def test_feed_posted_event_allows_completion_and_validation(self) -> None:
        self._reach_verified()
        event_id = "SE-20990101-000003-posted"
        event_dir = module.ACTIVITY_EVENTS_ROOT / "2099/01/01/00"
        event_dir.mkdir(parents=True)
        (event_dir / f"{event_id}.json").write_text(
            json.dumps(
                {
                    "event_id": event_id,
                    "execution_id": "EXEC-P0-01-TEST",
                    "event_type": "execution-milestone",
                    "verification": {"status": "VERIFIED", "feed_posted": True},
                }
            )
            + "\n",
            encoding="utf-8",
        )
        module.transition(
            "HANDED_OFF",
            next_action="continue",
            handoff={"current_state": "VERIFIED"},
            activity_event_id=event_id,
        )
        result = module.validate()
        self.assertEqual(result["status"], "GREEN")
        self.assertEqual(result["execution_status"], "HANDED_OFF")


if __name__ == "__main__":
    unittest.main(verbosity=2)
