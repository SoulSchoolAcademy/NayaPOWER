#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path
import stewardship_runtime as s

BASE = {
    "operation_key": "github-actions:deploy",
    "objective": "Verify the intended release is healthy",
    "current_truth": "Previous release attempt failed",
    "proposed_action": "Investigate and execute the next justified step",
    "expected_effect": "The identified blocker is removed",
    "verification_plan": "Observe the target runtime and compare against acceptance criteria",
    "stop_condition": "Stop on equivalent repeated failure or missing evidence",
    "strategy": "inspect-source",
}

class StewardshipRuntimeTests(unittest.TestCase):
    def test_missing_intent_blocks(self):
        action = dict(BASE); action["objective"] = ""
        self.assertEqual(s.preflight(action)["decision"], "BLOCKED_PENDING_GOVERNANCE")

    def test_first_failures_require_diagnosis(self):
        ledger = {"schema":"naya-power-action-ledger/v1", "operations":{}}
        for expected in (1, 2):
            decision = s.failure_decision(BASE, ledger)
            self.assertEqual(decision["equivalent_failure_count"], expected)
            self.assertEqual(decision["decision"], "DIAGNOSE_BEFORE_RETRY")
            s.record_result(BASE, {"failure": True, "observed_result":"same blocker"}, ledger, Path(tempfile.mkdtemp())/"ledger.json")

    def test_three_failures_force_strategy_reassessment(self):
        ledger = {"schema":"naya-power-action-ledger/v1", "operations":{BASE["operation_key"]: []}}
        for _ in range(2):
            ledger["operations"][BASE["operation_key"]].append(dict(BASE, failure=True))
        decision = s.failure_decision(BASE, ledger)
        self.assertEqual(decision["decision"], "STRATEGY_REASSESSMENT_REQUIRED")

    def test_five_failures_stop_high_caution(self):
        ledger = {"schema":"naya-power-action-ledger/v1", "operations":{BASE["operation_key"]: [dict(BASE, failure=True) for _ in range(4)]}}
        self.assertEqual(s.failure_decision(BASE, ledger)["decision"], "STOP_HIGH_CAUTION")

    def test_ten_equivalent_failures_redline(self):
        ledger = {"schema":"naya-power-action-ledger/v1", "operations":{BASE["operation_key"]: [dict(BASE, failure=True) for _ in range(9)]}}
        self.assertEqual(s.failure_decision(BASE, ledger)["decision"], "STOP_REDLINE")

    def test_material_strategy_change_does_not_count_as_equivalent(self):
        ledger = {"schema":"naya-power-action-ledger/v1", "operations":{BASE["operation_key"]: [dict(BASE, failure=True) for _ in range(9)]}}
        changed = dict(BASE, strategy="runtime-diagnostic", diagnostic="inspect-runtime-logs")
        self.assertEqual(s.failure_decision(changed, ledger)["equivalent_failure_count"], 1)
        self.assertEqual(s.failure_decision(changed, ledger)["decision"], "DIAGNOSE_BEFORE_RETRY")

if __name__ == "__main__":
    unittest.main()
