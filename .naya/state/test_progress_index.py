#!/usr/bin/env python3
"""Adversarial tests for the Naya Power Progress Index measurement layer."""
from __future__ import annotations

import json
import unittest

from validate_progress_index import adjudicate, load, validate


def clone(index):
    return json.loads(json.dumps(index))


def checkpoint(index):
    return index["checkpoints"][0]


class ProgressIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = load()

    def test_canonical_index_validates(self):
        self.assertEqual(validate(self.index), [])

    def test_baseline_is_developing_and_rejected(self):
        record = adjudicate(self.index)["checkpoints"][0]
        self.assertEqual(record["band"], "Developing")
        self.assertFalse(record["accepted"])
        self.assertLess(record["adjudicated_score"], record["floor"])

    def test_arithmetic_is_independent_of_the_declaration(self):
        record = adjudicate(self.index)["checkpoints"][0]
        self.assertAlmostEqual(record["weight_sum"], 105, places=4)
        self.assertAlmostEqual(record["weighted_total"], 6.0952, places=4)
        self.assertAlmostEqual(record["unweighted_mean"], 6.00, places=4)
        self.assertAlmostEqual(record["declared_system_score"], 6.70, places=4)
        self.assertAlmostEqual(record["divergence"], 0.6048, places=4)

    def test_weight_sum_anomaly_is_recorded_not_hidden(self):
        subtotal = sum(item["weight_pct"] for item in checkpoint(self.index)["subsystems"])
        self.assertEqual(subtotal, 105)
        self.assertFalse(checkpoint(self.index)["aggregate"]["weight_sum_valid"])
        notes = " ".join(checkpoint(self.index)["known_risks"] + checkpoint(self.index)["unknowns"]).lower()
        self.assertIn("weight", notes)

    def test_weight_sum_validity_lie_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["aggregate"]["weight_sum_valid"] = True
        self.assertTrue(any("weight_sum_valid must be False" in error for error in validate(mutated)))

    def test_exactly_one_baseline_checkpoint(self):
        self.assertEqual(len(self.index["checkpoints"]), 1)
        self.assertEqual(checkpoint(self.index)["kind"], "BASELINE")
        self.assertEqual(checkpoint(self.index)["sequence"], 1)

    def test_accepting_below_floor_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["verdict"]["accepted"] = True
        self.assertTrue(any("accepted must be False" in error for error in validate(mutated)))

    def test_weighted_total_lie_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["aggregate"]["weighted_total"] = 9.9
        self.assertTrue(any("weighted_total must equal" in error for error in validate(mutated)))

    def test_divergence_lie_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["aggregate"]["divergence"] = 0.0
        self.assertTrue(any("divergence must equal" in error for error in validate(mutated)))

    def test_subsystem_status_mismatch_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["subsystems"][2]["status"] = "Developing"
        self.assertTrue(any("status must be Failing" in error for error in validate(mutated)))

    def test_verdict_status_mismatch_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["verdict"]["status"] = "Accepted"
        self.assertTrue(any("verdict.status must be Developing" in error for error in validate(mutated)))

    def test_non_hex_baseline_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["baseline_reference"]["main_head"] = "94d2c5"
        self.assertTrue(any("baseline_reference.main_head must be a 40-hex commit" in error for error in validate(mutated)))

    def test_ancestor_contradiction_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["execution_head"]["relation_to_baseline"]["is_ancestor"] = True
        self.assertTrue(any("is_ancestor must be true exactly when behind == 0" in error for error in validate(mutated)))

    def test_wrong_subsystem_count_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["subsystems"].pop()
        self.assertTrue(any("exactly 10 subsystems" in error for error in validate(mutated)))

    def test_weights_not_one_hundred_is_red(self):
        mutated = clone(self.index)
        checkpoint(mutated)["subsystems"][0]["weight_pct"] = 14
        self.assertTrue(any("weight_sum must equal" in error for error in validate(mutated)))

    def test_lowered_floor_is_red(self):
        mutated = clone(self.index)
        mutated["acceptance_law"]["floor"] = 8.0
        self.assertTrue(any("floor must be 9.0" in error for error in validate(mutated)))

    def test_top_gaps_are_recorded(self):
        ids = {item["id"] for item in checkpoint(self.index)["highest_value_improvements"]}
        self.assertEqual(ids, {"P0-A", "P0-B", "P0-C"})

    def test_adjudication_is_deterministic(self):
        self.assertEqual(adjudicate(self.index), adjudicate(self.index))


if __name__ == "__main__":
    unittest.main()
