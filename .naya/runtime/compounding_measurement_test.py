#!/usr/bin/env python3
"""Focused V1 proof: measurement attaches to the existing canonical Activity event."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from activity_event import build_activity_event, persist_activity_event
from compounding_measurement import SCHEMA, STATUS, build_compounding_measurement


class CompoundingMeasurementV1Tests(unittest.TestCase):
    def test_measurement_is_embedded_in_existing_activity_event(self):
        root = Path(tempfile.mkdtemp(prefix="compounding-measurement-v1-"))
        events = root / "events"
        index = events / "INDEX.json"
        evidence = ["receipt:verified", "proof:state-change"]

        event = build_activity_event(
            event_id="SE-20260919-130000-compounding-v1-test",
            claim_id="CL-COMP-001",
            action_id="ACT-COMP-001",
            decision_id="DEC-COMP-001",
            authority_id="AUTH-COMP-001",
            actor_id="NAYA-TEST",
            subject="Compounding measurement V1 test",
            summary="measurement is attached to canonical Activity",
            receipt_id="RCP-COMP-001",
            next_action="continue",
            successor="NEXT-COMP-001",
            evidence=evidence,
            run_id="RUN-COMP-001",
            session_id="NAYA-COMP-001",
        )
        measurement = build_compounding_measurement(
            event=event,
            execution=event["execution"],
            evidence=evidence,
            history=[
                {"at": "2026-09-19T13:00:00+00:00", "to": "CLAIMED"},
                {"at": "2026-09-19T13:00:02+00:00", "to": "VERIFIED"},
            ],
        )
        event["compounding_measurement"] = measurement
        result = persist_activity_event(event, events_root=events, index_path=index)
        self.assertEqual(result["status"], "CREATED")

        stored = json.loads((events / "2026/09/19/13/SE-20260919-130000-compounding-v1-test.json").read_text())
        self.assertEqual(stored["event_id"], event["event_id"])
        self.assertEqual(stored["compounding_measurement"]["schema"], SCHEMA)
        self.assertEqual(stored["compounding_measurement"]["status"], STATUS)
        self.assertEqual(stored["compounding_measurement"]["verified_state_change"]["verification_status"], "VERIFIED")
        self.assertEqual(stored["compounding_measurement"]["resource_usage"]["wall_time_ms"], 2000)
        self.assertFalse(stored["compounding_measurement"]["downstream_compounding"]["observed"])
        self.assertFalse(stored["compounding_measurement"]["promotion"]["compounded"])

    def test_missing_provenance_is_rejected(self):
        event = {
            "event_id": "SE-20260919-130001-compounding-v1-test",
            "effective_at": "2026-09-19T13:00:01+00:00",
        }
        with self.assertRaises(ValueError):
            build_compounding_measurement(
                event=event,
                execution={"action_id": "ACT-COMP-002", "run_id": "RUN-COMP-002"},
                evidence=[],
            )


if __name__ == "__main__":
    unittest.main()
