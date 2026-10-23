"""Negative controls for one-network readiness: no network required."""
import copy
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "map-compiler"))
from surface_readiness import QUALITY_DIMENSIONS, load_registry, grade_surface, audit_registry, probe_surface

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

    def test_head_405_is_unknown_not_false_failure(self):
        def head_rejected(req,timeout):
            raise HTTPError(req.full_url,405,"No HEAD",{},None)
        r = probe_surface("/rooms/mail", opener=head_rejected)
        self.assertIsNone(r["reachable"])

if __name__ == "__main__":
    unittest.main()
