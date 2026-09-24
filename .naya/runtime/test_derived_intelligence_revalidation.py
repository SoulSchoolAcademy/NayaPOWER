from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name("derived_intelligence_revalidation.py")
SPEC = importlib.util.spec_from_file_location("derived_intelligence_revalidation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source(event_id: str) -> dict:
    return {"event_id": event_id, "status": "VERIFIED", "source_hash": sha(event_id)}


def derived(event_id: str, parents: list[str]) -> dict:
    return {
        "event_id": event_id,
        "status": "SUPPORTED",
        "relationships": {"source_events": parents},
        "source_hash": sha(event_id),
    }


def changed(source_id: str, before: str = "v1", after: str = "v2") -> dict:
    return {"id": source_id, "before_hash": sha(before), "after_hash": sha(after)}


class DerivedIntelligenceRevalidationTests(unittest.TestCase):
    def test_direct_transitive_and_multi_parent_impact(self) -> None:
        records = [
            source("A"),
            source("B"),
            source("C"),
            derived("D", ["A", "B"]),
            derived("E", ["D", "C"]),
            derived("F", ["A", "C"]),
        ]
        plan = MODULE.plan_revalidation_impact([changed("A")], records)
        self.assertEqual(plan["status"], "COMPLETE")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], ["D", "E", "F"])
        candidate = next(item for item in plan["revalidation_candidates"] if item["id"] == "E")
        self.assertEqual(candidate["paths"][0]["nodes"], ["A", "D", "E"])
        self.assertEqual(candidate["paths"][0]["distance"], 2)

    def test_changed_source_may_be_known_without_full_record(self) -> None:
        plan = MODULE.plan_revalidation_impact([changed("A")], [derived("D", ["A"])])
        self.assertEqual(plan["status"], "COMPLETE")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], ["D"])

    def test_intelligent_block_event_alias_resolves_to_canonical_object(self) -> None:
        record = {
            "identity": {"object_id": "BLOCK-D", "event_id": "EVENT-D", "version": 1},
            "source_bundle": [{"source_id": "EVENT-A", "relationship": "DERIVED_FROM"}],
            "lifecycle": {"stage": "SUPPORTED"},
            "integrity": {"algorithm": "SHA-256", "content_hash": sha("BLOCK-D")},
        }
        plan = MODULE.plan_revalidation_impact([changed("EVENT-A")], [record])
        self.assertEqual(plan["status"], "COMPLETE")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], ["BLOCK-D"])
        self.assertEqual(plan["revalidation_candidates"][0]["paths"][0]["nodes"], ["EVENT-A", "BLOCK-D"])

    def test_multi_parent_deduplication_preserves_both_paths(self) -> None:
        plan = MODULE.plan_revalidation_impact(
            [changed("A"), changed("B")],
            [derived("D", ["A", "B"])],
        )
        self.assertEqual(plan["status"], "COMPLETE")
        self.assertEqual(len(plan["revalidation_candidates"]), 1)
        candidate = plan["revalidation_candidates"][0]
        self.assertEqual(candidate["changed_source_ids"], ["A", "B"])
        self.assertEqual(len(candidate["paths"]), 2)

    def test_missing_dependency_is_partial_not_guessed(self) -> None:
        plan = MODULE.plan_revalidation_impact([changed("A")], [derived("D", ["MISSING"])])
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], [])
        self.assertIn("DEPENDENCY_TARGET_MISSING", {item["code"] for item in plan["unresolved"]})

    def test_related_edge_is_not_dependency(self) -> None:
        record = {"event_id": "R", "status": "ACTIVE", "relationships": {"related": ["A"]}}
        plan = MODULE.plan_revalidation_impact([changed("A")], [record])
        self.assertEqual(plan["status"], "NO_KNOWN_DEPENDENTS")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], [])

    def test_supersession_is_historical_context_not_invalidation(self) -> None:
        record = {
            "event_id": "SUCCESSOR",
            "status": "ACTIVE",
            "relationships": [
                {"relationship_id": "R1", "relation": "SUPERSEDES", "source": "SUCCESSOR", "target": "A"}
            ],
        }
        plan = MODULE.plan_revalidation_impact([changed("A")], [record])
        self.assertEqual(plan["status"], "NO_KNOWN_DEPENDENTS")
        self.assertEqual(plan["lineage_context"][0]["relation"], "SUPERSEDES")
        self.assertEqual(plan["system46_actions_invoked"], [])

    def test_cycle_is_bounded_and_reported(self) -> None:
        records = [derived("A", ["B"]), derived("B", ["A"])]
        plan = MODULE.plan_revalidation_impact([changed("A")], records, max_depth=4)
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertIn("DEPENDENCY_CYCLE", {item["code"] for item in plan["unresolved"]})
        self.assertNotIn("A", plan["impacted_derived_intelligence_ids"])

    def test_max_depth_stops_expansion(self) -> None:
        records = [derived("A", []), derived("B", ["A"]), derived("C", ["B"])]
        plan = MODULE.plan_revalidation_impact([changed("A")], records, max_depth=1)
        self.assertEqual(plan["impacted_derived_intelligence_ids"], ["B"])
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertIn("MAX_DEPTH_TRUNCATED", {item["code"] for item in plan["unresolved"]})

    def test_authorization_filter_prevents_unauthorized_traversal(self) -> None:
        plan = MODULE.plan_revalidation_impact(
            [changed("PRIVATE-SOURCE")],
            [derived("D", ["PRIVATE-SOURCE"])],
            authorized_ids={"D"},
        )
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], [])
        self.assertIn("UNAUTHORIZED_DEPENDENCY", {item["code"] for item in plan["unresolved"]})
        self.assertNotIn("PRIVATE-SOURCE", json.dumps(plan["unresolved"], sort_keys=True))

    def test_output_is_deterministic_and_input_is_not_mutated(self) -> None:
        records = [source("A"), derived("D", ["A"])]
        original = copy.deepcopy(records)
        first = MODULE.plan_revalidation_impact([changed("A")], records)
        second = MODULE.plan_revalidation_impact([changed("A")], records)
        self.assertEqual(first, second)
        self.assertEqual(records, original)

    def test_hash_uncertainty_is_explicit(self) -> None:
        plan = MODULE.plan_revalidation_impact(
            [{"id": "A", "before_hash": None, "after_hash": sha("v2")}],
            [derived("D", ["A"])],
        )
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertEqual(plan["changed_sources"][0]["hash_state"], "UNKNOWN")
        self.assertEqual(plan["impacted_derived_intelligence_ids"], ["D"])
        self.assertIn("CHANGE_HASH_UNKNOWN", {item["code"] for item in plan["unresolved"]})

    def test_equal_hashes_cannot_be_called_changed(self) -> None:
        with self.assertRaisesRegex(MODULE.LineagePlanningError, "hashes are equal"):
            MODULE.plan_revalidation_impact(
                [{"id": "A", "before_hash": sha("same"), "after_hash": sha("same")}],
                [derived("D", ["A"])],
            )

    def test_plan_never_invokes_system46_actions(self) -> None:
        plan = MODULE.plan_revalidation_impact([changed("A")], [derived("D", ["A"])])
        self.assertEqual(plan["mode"], "PLAN_ONLY")
        self.assertEqual(plan["system46_actions_invoked"], [])
        for action in MODULE.SYSTEM46_ACTIONS:
            self.assertNotIn(action, plan["impacted_derived_intelligence_ids"])


if __name__ == "__main__":
    unittest.main()
