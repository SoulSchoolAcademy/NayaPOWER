from __future__ import annotations

import copy
import hashlib
import importlib.util
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
PLANNER_SCRIPT = RUNTIME / "derived_intelligence_revalidation.py"
INVALIDATION_SCRIPT = RUNTIME / "intelligence_invalidation.py"
PLANNER_SPEC = importlib.util.spec_from_file_location("derived_intelligence_revalidation", PLANNER_SCRIPT)
PLANNER = importlib.util.module_from_spec(PLANNER_SPEC)
assert PLANNER_SPEC.loader
PLANNER_SPEC.loader.exec_module(PLANNER)
INVALIDATION_SPEC = importlib.util.spec_from_file_location("intelligence_invalidation", INVALIDATION_SCRIPT)
MODULE = importlib.util.module_from_spec(INVALIDATION_SPEC)
assert INVALIDATION_SPEC.loader
INVALIDATION_SPEC.loader.exec_module(MODULE)


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def fixture() -> tuple[dict, dict[str, dict]]:
    records = {
        "DERIVED-D": {"event_id": "DERIVED-D", "status": "SUPPORTED", "source_hash": sha("D")},
        "DERIVED-E": {"event_id": "DERIVED-E", "status": "SUPPORTED", "source_hash": sha("E")},
    }
    lineage_records = [
        {"event_id": "SOURCE-A", "status": "VERIFIED", "relationships": {"source_events": []}},
        {"event_id": "DERIVED-D", "status": "SUPPORTED", "relationships": {"source_events": ["SOURCE-A"]}},
        {"event_id": "DERIVED-E", "status": "SUPPORTED", "relationships": {"source_events": ["DERIVED-D"]}},
    ]
    plan = PLANNER.plan_revalidation_impact(
        [{"id": "SOURCE-A", "before_hash": sha("A-v1"), "after_hash": sha("A-v2")}],
        lineage_records,
    )
    return plan, records


def make_run(plan: dict | None = None, records: dict[str, dict] | None = None) -> MODULE.IntelligenceInvalidationRun:
    default_plan, default_records = fixture()
    return MODULE.IntelligenceInvalidationRun(
        plan if plan is not None else default_plan,
        records if records is not None else default_records,
        authority_ref="authority-decision-46",
        invalidator_id="invalidator-1",
        reason="foundational source revision changed",
        evidence_refs=["source-change-evidence-1"],
        idempotency_key="invalidation-batch-46",
    )


def recheck(outcome: str = "NEEDS_RECALCULATION") -> dict[str, dict]:
    return {
        candidate_id: {
            "outcome": outcome,
            "verifier_id": "recheck-verifier-1",
            "evidence_refs": [f"recheck-evidence-{candidate_id}"],
            "verification_record_ref": f"recheck-record-{candidate_id}",
        }
        for candidate_id in ("DERIVED-D", "DERIVED-E")
    }


class IntelligenceInvalidationTests(unittest.TestCase):
    def test_complete_proposal_flow_preserves_history(self) -> None:
        run = make_run()
        run.invalidate()
        run.recheck(
            {
                "DERIVED-D": {
                    "outcome": "CONFIRMED",
                    "verifier_id": "verifier-1",
                    "evidence_refs": ["recheck-d"],
                    "verification_record_ref": "verification-d",
                },
                "DERIVED-E": {
                    "outcome": "NEEDS_RECALCULATION",
                    "verifier_id": "verifier-1",
                    "evidence_refs": ["recheck-e"],
                    "verification_record_ref": "verification-e",
                },
            }
        )
        run.recalculate(
            {
                "DERIVED-E": {
                    "calculation_id": "calc-e-2",
                    "successor_content_sha256": sha("E-v2"),
                    "derivation_receipt_ref": "derivation-receipt-e-2",
                    "recalculator_id": "recalculator-1",
                    "evidence_refs": ["recalculation-evidence-e"],
                }
            }
        )
        run.supersede(
            {
                "DERIVED-E": {
                    "authority_ref": "authority-decision-46",
                    "evidence_refs": ["supersession-evidence-e"],
                    "supersession_receipt_ref": "supersession-receipt-e",
                }
            }
        )
        batch = run.export()
        self.assertEqual([receipt["action"] for receipt in batch["receipts"]], list(MODULE.ACTIONS))
        self.assertEqual(batch["status"], "PROPOSALS_READY")
        self.assertFalse(batch["persistence_performed"])
        self.assertFalse(batch["canonical_records_modified"])
        states = {item["id"]: item for item in batch["states"]}
        self.assertEqual(states["DERIVED-D"]["working_status"], "SUPPORTED")
        self.assertEqual(states["DERIVED-E"]["working_status"], "STALE")
        self.assertTrue(states["DERIVED-E"]["supersession"]["history_preserved"])
        self.assertEqual(states["DERIVED-E"]["supersession"]["successor_proposed_status"], "CANDIDATE")
        self.assertEqual(MODULE.validate_batch(batch), [])

    def test_partial_plan_is_refused(self) -> None:
        plan, records = fixture()
        plan["status"] = "PARTIAL"
        with self.assertRaisesRegex(MODULE.InvalidationError, "partial or empty"):
            make_run(plan, records)

    def test_missing_candidate_record_is_refused(self) -> None:
        plan, records = fixture()
        records.pop("DERIVED-E")
        with self.assertRaisesRegex(MODULE.InvalidationError, "candidate records missing"):
            make_run(plan, records)

    def test_missing_invalidation_evidence_is_refused(self) -> None:
        plan, records = fixture()
        with self.assertRaisesRegex(MODULE.InvalidationError, "evidence_refs"):
            MODULE.IntelligenceInvalidationRun(
                plan,
                records,
                authority_ref="authority-decision-46",
                invalidator_id="invalidator-1",
                reason="source changed",
                evidence_refs=[],
                idempotency_key="batch-46",
            )

    def test_invalidator_cannot_be_recheck_verifier(self) -> None:
        run = make_run()
        run.invalidate()
        results = recheck()
        results["DERIVED-D"]["verifier_id"] = "invalidator-1"
        with self.assertRaisesRegex(MODULE.InvalidationError, "must differ"):
            run.recheck(results)

    def test_recalculate_before_recheck_is_refused(self) -> None:
        run = make_run()
        run.invalidate()
        with self.assertRaisesRegex(MODULE.InvalidationError, "requires RECALCULATE"):
            run.recalculate({})

    def test_supersede_before_recalculate_is_refused(self) -> None:
        run = make_run()
        run.invalidate()
        run.recheck(recheck())
        with self.assertRaisesRegex(MODULE.InvalidationError, "requires SUPERSEDE"):
            run.supersede({})

    def test_invalid_successor_hash_is_refused(self) -> None:
        run = make_run()
        run.invalidate()
        run.recheck(recheck())
        with self.assertRaisesRegex(MODULE.InvalidationError, "SHA-256"):
            run.recalculate(
                {
                    candidate_id: {
                        "calculation_id": f"calc-{candidate_id}",
                        "successor_content_sha256": "invalid",
                        "derivation_receipt_ref": "derivation-receipt",
                        "recalculator_id": "recalculator-1",
                        "evidence_refs": ["recalculation-evidence"],
                    }
                    for candidate_id in ("DERIVED-D", "DERIVED-E")
                }
            )

    def test_recheck_results_must_match_candidates(self) -> None:
        run = make_run()
        run.invalidate()
        results = recheck()
        results.pop("DERIVED-E")
        with self.assertRaisesRegex(MODULE.InvalidationError, "match candidate IDs"):
            run.recheck(results)

    def test_output_is_deterministic_and_input_is_not_mutated(self) -> None:
        plan, records = fixture()
        original = copy.deepcopy(records)
        first = make_run(plan, records)
        second = make_run(plan, records)
        for run in (first, second):
            run.invalidate()
            run.recheck(recheck("CONFIRMED"))
            run.recalculate({})
            run.supersede({})
        self.assertEqual(first.export(), second.export())
        self.assertEqual(records, original)

    def test_blocked_recheck_remains_blocked(self) -> None:
        run = make_run()
        run.invalidate()
        run.recheck(recheck("BLOCKED"))
        run.recalculate({})
        run.supersede({})
        batch = run.export()
        self.assertEqual(batch["status"], "BLOCKED")
        self.assertEqual(batch["blocked_candidate_ids"], ["DERIVED-D", "DERIVED-E"])
        self.assertTrue(all(item["working_status"] == "STALE" for item in batch["states"]))
        self.assertEqual(MODULE.validate_batch(batch), [])

    def test_tampered_receipt_is_detected(self) -> None:
        run = make_run()
        run.invalidate()
        batch = run.export()
        batch["receipts"][0]["details"]["resulting_status"] = "ACTIVE"
        errors = MODULE.validate_batch(batch)
        self.assertIn("receipt 0 digest is invalid", errors)


if __name__ == "__main__":
    unittest.main()
