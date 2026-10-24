"""Negative controls for one-network readiness: no network required."""
import copy
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "map-compiler"))
from surface_readiness import (QUALITY_DIMENSIONS, NORTH_STAR_DIMENSIONS,
                               NORTH_STAR_LEVELS, north_star_gate, load_registry,
                               grade_surface, audit_registry, probe_surface)

REGISTRY = ROOT / "HUB" / "NETWORK-SURFACE-REGISTRY.json"


class SurfaceReadinessTests(unittest.TestCase):
    def setUp(self):
        self.registry = load_registry(REGISTRY)
        self.item = copy.deepcopy(self.registry["surfaces"][0])

    def qualified_metadata(self):
        a = self.item["assessments"]
        a["dimension_scores"] = {d: 9.5 for d in QUALITY_DIMENSIONS}
        a["author_identity"] = "author"
        a["independent_verifier_identity"] = "distinct-authenticated-reviewer"
        a["source_sha"] = "a" * 40
        a["deployed_sha"] = "a" * 40
        a["freshness_at"] = "2026-10-23T22:50:00Z"
        a["verified_receipts"] = ["receipt-locator-needs-external-validation"]
        a["positive_real_user_test"] = True
        a["adversarial_negative_test"] = True
        a["north_star"]["score_by_level"] = {
            level:{axis:9.5 for axis in NORTH_STAR_DIMENSIONS}
            for level in NORTH_STAR_LEVELS
        }
        a["north_star"]["evidence_by_level"] = {
            level:["external-scope-proof-pending"] for level in NORTH_STAR_LEVELS
        }
        a["north_star"]["cohorts_tested"] = ["authorized-human", "cold-Naya"]
        a["experience_proof"].update({
            "human_task_success":True,
            "human_experience_score":9.5,
            "naya_task_success":True,
            "naya_experience_score":9.5,
            "network_continuity_verified":True,
            "useful_outcome_measured":True,
            "efficiency_vs_baseline_measured":True,
            "human_outcome_receipt":"external-human-receipt-placeholder",
            "naya_handoff_receipt":"external-naya-receipt-placeholder",
            "network_event_receipt":"external-network-receipt-placeholder",
            "outcome_value_measurement":"quantified-useful-outcome-placeholder",
            "cost_latency_measurement":"baseline-and-comparison-placeholder",
        })
        return a

    def test_inventory_covers_known_doors_but_not_all_apps(self):
        paths = {r["path"] for r in self.registry["surfaces"]}
        self.assertEqual(len(paths), 25)
        self.assertIn("/dashboard", paths)
        self.assertIn("/rooms/spaces", paths)
        self.assertIn("/projects/questions.json", paths)
        self.assertFalse(self.registry["coverage_complete"])

    def test_all_http_200_never_implies_nine_plus(self):
        r = audit_registry(self.registry, probe=lambda p:{
            "http_status":200,"reachable":True,"redirected":False,"effective_path":p})
        self.assertEqual(r["status"], "amber")
        self.assertEqual(r["public_reachable"], 25)
        self.assertEqual(r["unassessed"], 25)
        self.assertIsNone(r["official_9_plus_count"])

    def test_404_is_red_and_not_completed(self):
        r = audit_registry(self.registry, probe=lambda p:{
            "http_status":404 if p.endswith("questions.json") else 200,
            "reachable":not p.endswith("questions.json"),
            "redirected":False,"effective_path":p})
        self.assertEqual(r["status"], "red")
        self.assertEqual(r["public_reachable"], 24)

    def test_referral_redirect_does_not_prove_sign_up(self):
        r = audit_registry(self.registry, probe=lambda p:{
            "http_status":200,"reachable":True,
            "redirected":p=="/joinus","effective_path":"/" if p=="/joinus" else p})
        row = next(x for x in r["rows"] if x["id"] == "join")
        self.assertEqual(row["quality_gate"], "UNASSESSED")
        self.assertTrue(row["redirected"])

    def test_independent_metadata_still_requires_external_verifier(self):
        self.qualified_metadata()
        self.assertEqual(grade_surface(self.item), "READY_FOR_SHIP_REVIEW")
        self.item["assessments"]["governed_release_approval"] = "authoritative receipt claimed"
        self.assertEqual(grade_surface(self.item), "EXTERNAL_ACCEPTANCE_VALIDATION_REQUIRED")

    def test_same_author_identity_is_not_independent(self):
        a = self.qualified_metadata()
        a["independent_verifier_identity"] = "author"
        self.assertEqual(grade_surface(self.item), "UNVERIFIED")

    def test_stale_revision_is_not_accepted(self):
        a = self.qualified_metadata()
        a["deployed_sha"] = "b" * 40
        self.assertEqual(grade_surface(self.item), "UNVERIFIED")

    def test_missing_negative_control_not_accepted(self):
        a = self.qualified_metadata()
        a["adversarial_negative_test"] = None
        self.assertEqual(grade_surface(self.item), "UNVERIFIED")

    def test_weakest_dimension_blocks_nine_plus(self):
        a = self.qualified_metadata()
        a["dimension_scores"]["Honesty"] = 8.9
        self.assertEqual(grade_surface(self.item), "BELOW_9_5")

    def test_eight_perfect_scores_without_human_and_naya_experience_not_qualified(self):
        a = self.qualified_metadata()
        a["dimension_scores"] = {d: 10 for d in QUALITY_DIMENSIONS}
        a["experience_proof"]["human_experience_score"] = None
        self.assertEqual(grade_surface(self.item), "EXPERIENCE_UNASSESSED")

    def test_naya_cannot_operate_is_not_ten_star(self):
        a = self.qualified_metadata()
        a["experience_proof"]["naya_task_success"] = False
        self.assertEqual(grade_surface(self.item), "EXPERIENCE_UNVERIFIED")

    def test_wonderful_human_ui_not_enough_if_naya_experience_low(self):
        a = self.qualified_metadata()
        a["experience_proof"]["naya_experience_score"] = 8.8
        self.assertEqual(grade_surface(self.item), "BELOW_9_5")

    def test_experience_without_proven_value_and_efficiency_is_not_accepted(self):
        a = self.qualified_metadata()
        a["experience_proof"]["useful_outcome_measured"] = False
        self.assertEqual(grade_surface(self.item), "EXPERIENCE_UNVERIFIED")
        a["experience_proof"]["useful_outcome_measured"] = True
        a["experience_proof"]["efficiency_vs_baseline_measured"] = None
        self.assertEqual(grade_surface(self.item), "EXPERIENCE_UNVERIFIED")

    def test_isolated_excellent_page_without_cross_network_continuity_is_not_accepted(self):
        a = self.qualified_metadata()
        a["experience_proof"]["network_continuity_verified"] = False
        self.assertEqual(grade_surface(self.item), "EXPERIENCE_UNVERIFIED")

    def test_every_registered_surface_has_both_user_journeys(self):
        self.assertTrue(self.registry["ten_star_experience_contract"]["hard_gates_non_averageable"] if "hard_gates_non_averageable" in self.registry["ten_star_experience_contract"] else self.registry["quality_thresholds"]["hard_gates_non_averageable"])
        for row in self.registry["surfaces"]:
            self.assertTrue(row["human_journey"])
            self.assertTrue(row["naya_journey"])
            self.assertTrue(row["network_continuity_journey"])
            self.assertIsNone(row["assessments"]["experience_proof"]["human_experience_score"])

    def test_registry_reuses_canonical_smart_note_six_by_three(self):
        c = self.registry["north_star_operating_standard"]
        self.assertIn("SN-0843/",c["authority_ref"])
        self.assertEqual(tuple(c["six_dimensions"]),NORTH_STAR_DIMENSIONS)
        self.assertEqual(tuple(c["three_levels"]),NORTH_STAR_LEVELS)
        self.assertEqual(len(c["seven_question_loop"]),7)

    def test_individual_perfect_but_no_journey_is_unassessed(self):
        a = self.qualified_metadata()
        a["north_star"]["score_by_level"]["individual"] = {
            dim:10 for dim in NORTH_STAR_DIMENSIONS
        }
        a["north_star"]["score_by_level"]["journey"]["network_intelligence"] = None
        self.assertEqual(grade_surface(self.item), "NORTH_STAR_UNASSESSED")

    def test_component_and_journey_perfect_but_network_below_bar(self):
        a = self.qualified_metadata()
        for level in ("individual","journey"):
            a["north_star"]["score_by_level"][level] = {
                dim:10 for dim in NORTH_STAR_DIMENSIONS
            }
        a["north_star"]["score_by_level"]["network"]["trust_governance"]=8.5
        self.assertEqual(grade_surface(self.item),"BELOW_9_5")

    def test_each_north_star_dimension_blocks_when_weak_at_any_level(self):
        a = self.qualified_metadata()
        for level in NORTH_STAR_LEVELS:
            for dimension in NORTH_STAR_DIMENSIONS:
                with self.subTest(level=level,dimension=dimension):
                    a["north_star"]["score_by_level"][level][dimension]=9.0
                    self.assertEqual(grade_surface(self.item),"BELOW_9_5")
                    a["north_star"]["score_by_level"][level][dimension]=9.5

    def test_missing_independent_network_proof_not_nine_plus(self):
        a = self.qualified_metadata()
        a["north_star"]["evidence_by_level"]["network"] = []
        self.assertEqual(grade_surface(self.item),"NORTH_STAR_UNVERIFIED")

    def test_no_tested_human_or_naya_cohorts_not_nine_plus(self):
        a = self.qualified_metadata()
        a["north_star"]["cohorts_tested"] = []
        self.assertEqual(grade_surface(self.item),"NORTH_STAR_UNVERIFIED")

    def test_perfect_six_by_three_still_needs_external_acceptance(self):
        a = self.qualified_metadata()
        for level in NORTH_STAR_LEVELS:
            a["north_star"]["score_by_level"][level] = {
                d:10 for d in NORTH_STAR_DIMENSIONS
            }
        self.assertEqual(grade_surface(self.item),"READY_FOR_SHIP_REVIEW")
        a["governed_release_approval"] = "claimed"
        self.assertEqual(grade_surface(self.item),"EXTERNAL_ACCEPTANCE_VALIDATION_REQUIRED")

    def test_head_405_bounded_get_recovers_a_working_smartnote(self):
        class Response:
            status = 200
            headers = {}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def geturl(self): return "https://nayanet.live/s/sn0840"
        methods = []
        def special(req,timeout):
            methods.append(req.get_method())
            if req.get_method() == "HEAD":
                raise HTTPError(req.full_url, 405, "HEAD not supported", {}, None)
            self.assertEqual(req.headers.get("Range"), "bytes=0-0")
            return Response()
        r = probe_surface("/s/sn0840", opener=special)
        self.assertEqual(methods, ["HEAD","GET"])
        self.assertTrue(r["reachable"])
        self.assertTrue(r["head_unsupported_get_fallback"])

    def test_head_405_is_unknown_not_false_failure(self):
        def head_rejected(req,timeout):
            raise HTTPError(req.full_url,405,"No HEAD",{},None)
        r = probe_surface("/rooms/mail", opener=head_rejected)
        self.assertIsNone(r["reachable"])

if __name__ == "__main__":
    unittest.main()
