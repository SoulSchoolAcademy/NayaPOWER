from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "capabilities" / "system-truth-ledger.v1.json"
SPEC_PATH = ROOT / "60 SYSTEM UPDATES FOR NAYA,md"
VALID_CLASSIFICATIONS = {
    "VERIFIED_MECHANISM",
    "VERIFIED_PRODUCTION",
    "BLOCKED",
    "NOT_TESTED",
    "UNKNOWN",
}
REQUIRED_FIELDS = {
    "number",
    "title",
    "classification",
    "mechanism_status",
    "production_status",
    "dedicated_branch",
    "head",
    "base",
    "source_evidence",
    "local_tests",
    "ci_runs",
    "artifacts",
    "issue_receipt",
    "blocker",
    "next_action",
    "evidence_notes",
}


class SystemTruthLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        cls.systems = cls.ledger["systems"]
        cls.by_number = {row["number"]: row for row in cls.systems}
        cls.spec = SPEC_PATH.read_text(encoding="utf-8")

    def test_scope_is_exactly_41_through_60(self) -> None:
        self.assertEqual(self.ledger["schema"], "naya-system-truth-ledger/v1")
        self.assertEqual([row["number"] for row in self.systems], list(range(41, 61)))
        self.assertEqual(len(self.by_number), 20)

    def test_every_row_has_typed_evidence_fields(self) -> None:
        for row in self.systems:
            with self.subTest(system=row["number"]):
                self.assertEqual(set(row), REQUIRED_FIELDS)
                self.assertIn(row["classification"], VALID_CLASSIFICATIONS)
                self.assertIn(row["mechanism_status"], VALID_CLASSIFICATIONS)
                self.assertIn(row["production_status"], VALID_CLASSIFICATIONS)
                self.assertIsInstance(row["source_evidence"], dict)
                self.assertIsInstance(row["local_tests"], list)
                self.assertIsInstance(row["ci_runs"], list)
                self.assertIsInstance(row["artifacts"], list)
                self.assertIsInstance(row["issue_receipt"], dict)
                self.assertTrue(row["blocker"])
                self.assertTrue(row["next_action"])
                self.assertTrue(row["evidence_notes"])

    def test_dedicated_receipts_have_exact_identity(self) -> None:
        for row in self.systems:
            if row["dedicated_branch"] is not None:
                with self.subTest(system=row["number"]):
                    self.assertRegex(row["dedicated_branch"], r"^coda3/")
                    self.assertRegex(row["head"], r"^[0-9a-f]{40}$")
                    self.assertRegex(row["base"], r"^[0-9a-f]{40}$")
                    self.assertIsNotNone(row["issue_receipt"]["sign_in"])
                    self.assertIsNotNone(row["issue_receipt"]["sign_out"])

    def test_ci_and_artifact_evidence_is_typed(self) -> None:
        for row in self.systems:
            for run in row["ci_runs"]:
                self.assertIsInstance(run["run"], int)
                self.assertIsInstance(run["job"], int)
                self.assertIn(run["conclusion"], {"PASS", "FAIL", "FAIL_EXPECTED"})
            for artifact in row["artifacts"]:
                self.assertIsInstance(artifact["id"], int)
                self.assertRegex(artifact["sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(artifact["independent_inspection"])

    def test_canonical_numbering_corrections_are_preserved(self) -> None:
        self.assertEqual(self.by_number[47]["classification"], "NOT_TESTED")
        self.assertEqual(self.by_number[47]["title"], "CAUSAL MODEL")
        self.assertIsNone(self.by_number[47]["dedicated_branch"])
        self.assertEqual(self.by_number[50]["title"], "DISTRIBUTED NAYA")
        self.assertEqual(self.by_number[50]["source_evidence"]["classification"], "MISLABELED_AS_SYSTEM_60")
        self.assertEqual(self.by_number[60]["title"], "THE ULTIMATE NAYAPOWER LOOP")
        self.assertEqual(self.by_number[60]["classification"], "BLOCKED")
        self.assertEqual(
            self.by_number[60]["issue_receipt"]["mislabeled_pair"]["scope"],
            "MISLABELED_SYSTEM_50_EVIDENCE",
        )

    def test_no_full_system_is_overclaimed_as_production(self) -> None:
        self.assertNotIn("VERIFIED_PRODUCTION", {row["classification"] for row in self.systems})
        self.assertEqual(self.by_number[41]["mechanism_status"], "VERIFIED_PRODUCTION")
        self.assertEqual(self.by_number[41]["classification"], "BLOCKED")
        self.assertEqual(self.by_number[42]["classification"], "NOT_TESTED")
        self.assertEqual(self.by_number[56]["classification"], "NOT_TESTED")
        self.assertEqual(self.by_number[58]["classification"], "NOT_TESTED")

    def test_canonical_spec_contains_each_number(self) -> None:
        for number in range(41, 61):
            self.assertRegex(self.spec, rf"(?m)^{number}\. ")


if __name__ == "__main__":
    unittest.main()
