from pathlib import Path
import json
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"
REGISTRY = ROOT / ".naya" / "governance" / "authority-registry.json"
ADAPTER = ROOT / ".naya" / "control-plane" / "workflow_gate.py"

LEGACY_HUB_WORKFLOWS = (
    "2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml",
    "2026-09-08-canonical-hub-release-dispatch.yml",
    "2026-09-08-nuclear-right-rail-fix.yml",
    "2026-09-08-repair-main-feed-and-strip-garbage.yml",
    "2026-09-08-surgical-right-rail-removal.yml",
    "deploy-canonical-hub-vercel.yml",
    "deploy-canonical-nayanet-live.yml",
    "deploy-current-nayanet-hub.yml",
    "deploy-nayanet-hub.yml",
    "deploy-v7-intelligent-hub.yml",
    "nayanet-feed-v5-apply.yml",
    "refine-nayahub-v7.yml",
    "v7-intelligent-hub-build.yml",
)


class NayaExecutionBoundaryTests(unittest.TestCase):
    def read(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def run_adapter(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ADAPTER), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_canonical_hub_deployment_is_human_dispatched_kernel_gated_and_sha_bound(self):
        text = self.read("deploy-nayanet-hub-canonical-v2.yml")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("workflow_call:", text)
        self.assertNotIn("schedule:", text)
        self.assertIn("commit_sha:", text)
        self.assertIn("approval:", text)
        self.assertIn("Enforce canonical NayaPOWER governance kernel", text)
        self.assertIn("--permission \"deploy_public_runtime\"", text)
        self.assertIn("--scope \"public-runtime:aged-art-7c12:/\"", text)
        self.assertIn("EXACT_SOURCE_SHA=PASS", text)
        self.assertNotIn("on:\n  push:", text)

    def test_intelligent_hub_builder_is_kernel_gated_and_human_dispatched(self):
        text = self.read("build-nayahub-intelligent.yml")
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("workflow_call:", text)
        self.assertNotIn("schedule:", text)
        self.assertIn("approval:", text)
        self.assertIn("Enforce canonical NayaPOWER governance kernel", text)
        self.assertIn("--permission \"repo_write\"", text)
        self.assertIn("--scope \"repo:SoulSchoolAcademy/NayaPOWER:path:index.html\"", text)
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
        text = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("load_authority_registry", text)
        self.assertIn("resolve_authority", text)
        self.assertIn("authority.purpose == purpose", text)
        self.assertNotIn("authority_id=f\"workflow:", text)

    def test_build_authority_is_executable(self):
        result = self.run_adapter(
            "--actor", "SoulSchoolAcademy",
            "--purpose", "build and mutate the canonical NayaNET Intelligent Hub artifact",
            "--permission", "repo_write",
            "--request", "build_nayanet_intelligent_hub",
            "--mission", "make NayaPOWER governance operationally capable of safely building the Intelligent Hub",
            "--uncertainty", "1",
            "--consequence", "5",
            "--irreversibility", "2",
            "--scope", "repo:SoulSchoolAcademy/NayaPOWER:path:index.html",
            "--evidence", "explicit workflow_dispatch approval",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('"status": "AUTHORIZED"', result.stdout)

    def test_deploy_authority_is_executable_and_high_risk_verified(self):
        result = self.run_adapter(
            "--actor", "SoulSchoolAcademy",
            "--purpose", "deploy the canonical NayaNET Intelligent Hub public runtime",
            "--permission", "deploy_public_runtime",
            "--request", "deploy_nayanet_hub_canonical",
            "--mission", "make NayaPOWER operationally capable of safely governing Intelligent Hub production deployment",
            "--uncertainty", "3",
            "--consequence", "8",
            "--irreversibility", "8",
            "--scope", "public-runtime:aged-art-7c12:/",
            "--evidence", "explicit deployment approval",
            "--evidence", "exact source SHA verified",
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn('"status": "AUTHORIZED"', result.stdout)
        self.assertIn('"risk_tier": "HIGH"', result.stdout)

    def test_unregistered_scope_is_denied(self):
        result = self.run_adapter(
            "--actor", "SoulSchoolAcademy",
            "--purpose", "deploy the canonical NayaNET Intelligent Hub public runtime",
            "--permission", "deploy_public_runtime",
            "--request", "forged_request",
            "--mission", "attempt an unregistered deployment",
            "--uncertainty", "3",
            "--consequence", "8",
            "--irreversibility", "8",
            "--scope", "public-runtime:UNREGISTERED:/",
            "--evidence", "forged authority test",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("explicit authority resolution failed", result.stdout)

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

    def test_all_legacy_hub_workflows_are_non_mutating(self):
        for name in LEGACY_HUB_WORKFLOWS:
            path = WORKFLOWS / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIn("RETIRED", text, msg=f"legacy workflow not marked retired: {name}")
            self.assertNotIn("contents: write", text, msg=f"legacy workflow still has write power: {name}")
            self.assertNotIn("git push", text, msg=f"legacy workflow can push: {name}")
            self.assertNotIn("cloudflare/wrangler-action", text, msg=f"legacy workflow can deploy: {name}")
            self.assertNotIn("workflow_call:", text, msg=f"legacy workflow can be invoked: {name}")


if __name__ == "__main__":
    unittest.main()
