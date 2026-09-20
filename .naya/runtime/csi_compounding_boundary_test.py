#!/usr/bin/env python3
import unittest
from csi_compounding_boundary import build_compounding_change

BASE = {
    "event_id": "INT-TEST-001",
    "lesson": "Verified evidence must remain linked to the execution.",
    "source": ["exec-1", "ev-1"],
    "evidence_state": "VERIFIED",
    "promotion_status": "VERIFIED",
}

class CSICompoundingBoundaryTests(unittest.TestCase):
    def test_valid_learning_creates_measurable_change(self):
        c = build_compounding_change(BASE, baseline="No provenance check", expected_improvement="Require provenance", measurement="100% of future changes carry source")
        self.assertEqual(c["state"], "PROPOSED_FUTURE_EXECUTION_CHANGE")
        self.assertEqual(c["source_event_id"], "INT-TEST-001")

    def test_unvalidated_cannot_compound(self):
        with self.assertRaises(ValueError): build_compounding_change({**BASE, "evidence_state":"IMPLEMENTED"}, baseline="x", expected_improvement="y", measurement="z")

    def test_unpromoted_cannot_compound(self):
        with self.assertRaises(ValueError): build_compounding_change({**BASE, "promotion_status":"WRITTEN"}, baseline="x", expected_improvement="y", measurement="z")

    def test_noise_lesson_rejected(self):
        with self.assertRaises(ValueError): build_compounding_change({**BASE, "lesson":""}, baseline="x", expected_improvement="y", measurement="z")

    def test_missing_provenance_rejected(self):
        with self.assertRaises(ValueError): build_compounding_change({**BASE, "source":[]}, baseline="x", expected_improvement="y", measurement="z")

    def test_duplicate_input_is_not_multiplied(self):
        a = build_compounding_change(BASE, baseline="x", expected_improvement="y", measurement="z")
        b = build_compounding_change(BASE, baseline="x", expected_improvement="y", measurement="z")
        self.assertEqual(a, b)

    def test_baseline_required(self):
        with self.assertRaises(ValueError): build_compounding_change(BASE, baseline="", expected_improvement="y", measurement="z")

    def test_measurement_required(self):
        with self.assertRaises(ValueError): build_compounding_change(BASE, baseline="x", expected_improvement="y", measurement="")

    def test_no_canonical_authority_created(self):
        c = build_compounding_change(BASE, baseline="x", expected_improvement="y", measurement="z")
        self.assertEqual(c["authority"], "CSI_BOUNDARY_ONLY")
        self.assertNotIn("canonical", c)
        self.assertNotIn("verification", c)

if __name__ == "__main__": unittest.main()
