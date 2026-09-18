#!/usr/bin/env python3
"""Adversarial tests for the ONE Master Work Queue validator and selector."""
from __future__ import annotations

import json
import unittest

from validate_work_queue import candidates, load, select, validate

M1 = "TASK-NAYA-M1-MASTER-WORK-QUEUE"
M2 = "TASK-NAYA-M2-EXECUTION-SUPERVISOR"
M3 = "TASK-NAYA-M3-ACTIVITY-AUTOWRITE"
D1 = "TASK-NAYA-D1-CANONICAL-RUNTIME"


def mutate(queue, path, value):
    clone = json.loads(json.dumps(queue))
    node = clone
    parts = path.split(".")
    for part in parts[:-1]:
        node = node[int(part)] if part.isdigit() else node[part]
    last = parts[-1]
    if last.isdigit():
        node[int(last)] = value
    else:
        node[last] = value
    return clone


class MasterWorkQueueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = load()

    def task(self, task_id):
        return next(task for task in self.queue["tasks"] if task["task_id"] == task_id)

    def path(self, task_id):
        index = next(i for i, task in enumerate(self.queue["tasks"]) if task["task_id"] == task_id)
        return f"tasks.{index}"

    def test_canonical_queue_validates(self):
        self.assertEqual(validate(self.queue), [])

    def test_select_returns_exactly_one(self):
        result = select(self.queue)
        self.assertEqual(result["status"], "SELECTED")
        self.assertTrue(result["task_id"])
        self.assertTrue(result["next_action"])
        self.assertTrue(result["successor_action"])

    def test_select_chooses_the_unblocking_task(self):
        self.assertEqual(select(self.queue)["task_id"], M2)

    def test_complete_task_is_not_selected(self):
        self.assertNotEqual(select(self.queue)["task_id"], M1)

    def test_blocked_human_authority_task_is_not_selected(self):
        selected = select(self.queue)["task_id"]
        self.assertNotEqual(selected, D1)
        self.assertFalse(any(task["selector"]["blocked"] and task["task_id"] == selected for task in self.queue["tasks"]))

    def test_select_stops_cleanly_when_no_work_remains(self):
        clone = json.loads(json.dumps(self.queue))
        for task in clone["tasks"]:
            task["status"] = "COMPLETE"
            task["selector"]["blocked"] = False
            task["selector"]["executable"] = True
            task.pop("blocked_reason", None)
        self.assertEqual(validate(clone), [])
        result = select(clone)
        self.assertEqual(result["status"], "STOP_CLEANLY")
        self.assertEqual(result["candidate_count"], 0)

    def test_canonical_candidates_exclude_complete_and_blocked(self):
        ready_ids = {task["task_id"] for task in candidates(self.queue)}
        self.assertNotIn(M1, ready_ids)
        self.assertNotIn(D1, ready_ids)

    def test_duplicate_task_id_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M2)}.task_id", M1)
        self.assertTrue(any("duplicate task_id" in error for error in validate(mutated)))

    def test_missing_required_field_is_red(self):
        stripped = {k: v for k, v in self.task(M1).items() if k != "successor_action"}
        mutated = mutate(self.queue, self.path(M1), stripped)
        self.assertTrue(any("missing required field successor_action" in error for error in validate(mutated)))

    def test_unknown_dependency_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M2)}.dependencies", ["TASK-DOES-NOT-EXIST"])
        self.assertTrue(any("does not exist" in error for error in validate(mutated)))

    def test_dependency_cycle_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M1)}.dependencies", [M2])
        self.assertTrue(any("cycle" in error for error in validate(mutated)))

    def test_selector_factor_out_of_range_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M1)}.selector.risk", 1.5)
        self.assertTrue(any("selector.risk must be between 0 and 1" in error for error in validate(mutated)))

    def test_blocked_without_reason_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M3)}.status", "BLOCKED")
        self.assertTrue(any("blocked task requires blocked_reason" in error for error in validate(mutated)))

    def test_blocked_flag_status_mismatch_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M3)}.selector.blocked", True)
        self.assertTrue(any("requires status=BLOCKED" in error for error in validate(mutated)))

    def test_minimum_score_below_floor_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M1)}.minimum_score", 8.9)
        self.assertTrue(any("minimum_score must be >= 9.0" in error for error in validate(mutated)))

    def test_candidate_with_unmet_dependency_is_red(self):
        mutated = mutate(self.queue, f"{self.path(M3)}.status", "READY")
        self.assertTrue(any("requires completed dependencies" in error for error in validate(mutated)))

    def test_invalid_quality_policy_is_red(self):
        mutated = mutate(self.queue, "quality_policy.minimum_score", 8.0)
        self.assertTrue(any("minimum_score must be >= 9.0" in error for error in validate(mutated)))

    def test_invalid_schema_id_is_red(self):
        mutated = mutate(self.queue, "$schema", "naya/other/v1")
        self.assertTrue(any("invalid $schema" in error for error in validate(mutated)))

    def test_selector_is_deterministic(self):
        self.assertEqual(select(self.queue), select(self.queue))


if __name__ == "__main__":
    unittest.main()
