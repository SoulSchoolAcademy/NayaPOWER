from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"
REGISTRY = ROOT / ".naya" / "governance" / "authority-registry.json"


class NayaExecutionBoundaryTests(unittest.TestCase):
    def read(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def test_canonical_hub_deployment_is_kernel_gated_and_sha_bound(self):
        text = self.read("deploy-nayanet-hub-canonical-v2.yml")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("commit_sha:", text)
        self.assertIn("approval:", text)
        self.assertIn("Enforce canonical NayaPOWER governance kernel", text)
        self.assertIn("--permission \"deploy_public_runtime\"", text)
        self.assertIn("--scope \"public-runtime:aged-art-7c12:/\"", text)
        self.assertIn("EXACT_SOURCE_SHA=PASS", text)
        self.assertNotIn("on:\n  push:", text)

    def test_intelligent_hub_builder_is_kernel_gated(self):
        text = self.read("build-nayahub-intelligent.yml")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("approval:", text)
        self.assertIn("Enforce canonical NayaPOWER governance kernel", text)
        self.assertIn("--permission \"repo_write\"", text)
        self.assertNotIn("on:\n  push:", text)

    def test_governance_validator_is_not_a_deployment_authority(self):
        text = self.read("naya-governance-gate.yml")
        self.assertNotIn("cloudflare/wrangler-action", text)
        self.assertNotIn("canonical_release:", text)
        self.assertIn("NO_PARALLEL_DEPLOYMENT_AUTHORITY=PASS", text)

    def test_registry_contains_exact_scoped_hub_grants(self):
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
        authorities = {item["authority_id"]: item for item in payload["authorities"]}
        self.assertEqual(
            authorities["HUMAN-SOULSCHOOLACADEMY-HUB-BUILD"]["scope"],
            "repo:SoulSchoolAcademy/NayaPOWER:path:index.html",
        )
        self.assertEqual(
            authorities["HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY"]["scope"],
            "public-runtime:aged-art-7c12:/",
        )
        self.assertEqual(
            authorities["HUMAN-SOULSCHOOLACADEMY-HUB-BUILD"]["granted_actions"],
            ["repo_write"],
        )
        self.assertEqual(
            authorities["HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY"]["granted_actions"],
            ["deploy_public_runtime"],
        )
        self.assertFalse((ROOT / ".naya" / "governance" / "workflow-authorities.json").exists())

    def test_adapter_resolves_preexisting_authority_and_never_mints_one(self):
        text = (ROOT / ".naya" / "control-plane" / "workflow_gate.py").read_text(encoding="utf-8")
        self.assertIn("load_authority_registry", text)
        self.assertIn("resolve_authority", text)
        self.assertIn("authority.purpose == purpose", text)
        self.assertNotIn("authority_id=f\"workflow:", text)

    def test_no_known_obsolete_mutating_workflow_remains(self):
        self.assertFalse((WORKFLOWS / "nayanet-welcome-executor.yml").exists())
        self.assertFalse((WORKFLOWS / "deploy-nayanet.yml").exists())

    def test_no_workflow_points_at_nonexistent_canonical_deployment(self):
        for path in WORKFLOWS.glob("*.yml"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "deploy-nayanet-hub-canonical.yml",
                text,
                msg=f"stale canonical deployment reference in {path.name}",
            )

    def test_current_hub_aliases_are_non_mutating(self):
        for name in ("deploy-nayanet-hub.yml", "deploy-current-nayanet-hub.yml"):
            text = self.read(name)
            self.assertNotIn("cloudflare/wrangler-action", text)
            self.assertNotIn("git push", text)
            self.assertIn("RETIRED", text)


if __name__ == "__main__":
    unittest.main()
