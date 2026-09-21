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

CURRENT_509_WORKFLOW_SURFACE = {
    "509-finish-smart-feed.yml",
    "509-sidebar-nav-audit.yml",
    "509-sidebar-nav-correction.yml",
    "509-smart-notes-board-presentation-fix.yml",
    "509-smart-notes-presentation-final.yml",
    "509-smart-notes-surgical-final-v3.yml",
    "deploy-509-c4-final-presentation-fix.yml",
    "deploy-509-c4-flow-repair-v2.yml",
    "deploy-509-c4-flow-repair.yml",
    "deploy-509-c4-nine-note-parser-v2.yml",
    "deploy-509-c4-nine-note-parser.yml",
    "deploy-509-c4-real-smart-feed-finalize.yml",
    "deploy-smart-feed-direct.yml",
}

CORE_GOVERNANCE_WORKFLOW_SURFACE = {
    "naya-control-plane.yml",
    "naya-memory-runtime.yml",
    "naya-power-adversarial-p0.yml",
    "naya-preflight-governance.yml",
    "nayapower-activity-feed-integrity.yml",
    "restore-509-exact.yml",
    "superbrain-current-main-behavioral-proof.yml",
    "verify-nayanet-hub-build-only.yml",
    "verify-primary-intelligence-system.yml",
}


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

    def test_assistant_lane_canonical_v2_is_not_falsely_claimed_current(self):
        """The missing Assistant/Cloudflare lane remains explicitly unknown, not silently replaced by the 509 lane."""
        self.assertFalse((WORKFLOWS / "deploy-nayanet-hub-canonical-v2.yml").exists())
        self.assertIn("deploy-smart-feed-direct.yml", CURRENT_509_WORKFLOW_SURFACE)
        self.assertIn("naya-control-plane.yml", CORE_GOVERNANCE_WORKFLOW_SURFACE)

    def test_current_workflow_surface_is_classified_without_requiring_a_stale_eight_workflow_snapshot(self):
        actual = {p.name for p in WORKFLOWS.glob("*.yml")}
        classified = CURRENT_509_WORKFLOW_SURFACE | CORE_GOVERNANCE_WORKFLOW_SURFACE
        self.assertEqual(actual, classified)

    def test_build_only_hub_verification_is_non_production_and_sha_bound(self):
        text = self.read("verify-nayanet-hub-build-only.yml")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("commit_sha:", text)
        self.assertIn("ref: ${{ steps.source.outputs.sha }}", text)
        self.assertIn('ACTUAL_SHA="$(git rev-parse HEAD)"', text)
        self.assertIn("npm install --no-audit --no-fund", text)
        self.assertIn("npm run typecheck", text)
        self.assertIn("npm run build", text)
        self.assertIn("VITE_RELEASE_COMMIT", text)
        self.assertIn("release-proof.txt", text)
        self.assertIn("actions/upload-artifact@v4", text)
        self.assertNotIn("cloudflare/wrangler-action", text)
        self.assertNotIn("EXPLICIT_APPROVAL_GRANTED", text)
        self.assertNotIn("deploy-nayanet-hub-canonical-v2.yml", text)

    def test_control_plane_contains_governance_and_cct_authority(self):
        text = self.read("naya-control-plane.yml")
        self.assertIn("Governance kernel self-test", text)
        self.assertIn("Execution-boundary self-test", text)
        self.assertIn("Cold Naya control-plane acceptance", text)
        self.assertIn("CCT-003 two-Naya exchange", text)
        self.assertIn("CCT-004 adversarial semantics", text)
        self.assertIn("CCT-005 value feedback", text)
        self.assertIn("paths:", text)

    def test_memory_runtime_is_scoped_to_memory_and_restore(self):
        text = self.read("naya-memory-runtime.yml")
        self.assertIn("Naya Power Memory + Restore Runtime", text)
        self.assertIn("Run Smart Note validator", text)
        self.assertIn("Run Restore Context tests", text)
        self.assertIn("Execute current Restore Context", text)
        self.assertNotIn("CCT-003 two-Naya exchange", text)
        self.assertNotIn("CCT-004 adversarial semantics", text)
        self.assertNotIn("CCT-005 value feedback", text)

    def test_activity_feed_integrity_is_exact_head_and_read_only(self):
        text = self.read("nayapower-activity-feed-integrity.yml")
        self.assertIn("SUPERBRAIN/NAYA-ACTIVITY-FEED.md", text)
        self.assertIn("SUPERBRAIN/NAYA-ACTIVITY/**", text)
        self.assertIn('ref: ${{ github.sha }}', text)
        self.assertIn("EXACT_HEAD=PASS", text)
        self.assertIn("contents: read", text)
        self.assertNotIn("contents: write", text)

    def test_adversarial_workflow_is_not_a_general_runtime_regression_runner(self):
        text = self.read("naya-power-adversarial-p0.yml")
        self.assertIn("tests/adversarial/**", text)
        self.assertIn("test_behavioral_bypasses.py", text)
        self.assertIn("Run behavioral bypass adversarial tests", text)
        self.assertIn("Run live P0 harness when explicitly requested", text)
        self.assertIn("if: github.event_name == 'workflow_dispatch'", text)
        self.assertNotIn(".naya/runtime/**", text)
        self.assertNotIn("Run canonical control-plane validator", text)
        self.assertNotIn("Validate Naya-to-Naya Activity Feed", text)

    def test_behavioral_proof_is_distinct_from_production_deployment(self):
        text = self.read("superbrain-current-main-behavioral-proof.yml")
        self.assertIn("Run current-main Superbrain behavioral suite", text)
        self.assertIn("Run A→B→C compounding proof independently", text)
        self.assertIn("EVIDENCE_CLASS=RUNTIME_TESTED_NOT_PRODUCTION_PROVEN", text)
        self.assertNotIn("cloudflare/wrangler-action", text)

    def test_pis_verification_is_projection_and_artifact_parity_only(self):
        text = self.read("verify-primary-intelligence-system.yml")
        self.assertIn("Build PIS projection", text)
        self.assertIn("PIS_PROJECTION=PASS", text)
        self.assertIn("PIS_PERSISTENT_ADAPTER_SOURCE=PASS", text)
        self.assertIn("PIS_ARTIFACT_PARITY=PASS", text)
        self.assertNotIn("cloudflare/wrangler-action", text)

    def test_registry_contains_exact_scoped_hub_grants(self):
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
        authorities = {item["authority_id"]: item for item in payload["authorities"]}
        self.assertEqual(
            authorities["HUMAN-SOULSCHOOLACADEMY-HUB-BUILD"]["scope"],
            "repo:SoulSchoolAcademy/NayaPOWER:path:index.html",
        )
        self.assertEqual(
            authorities["HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY"]["scope"],
            "public-runtime:sparkling-shape-7ae5:/",
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
            "--intent-understood",
            "--context-complete",
            "--quality-ready",
            "--evidence-ready",
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
            "--scope", "public-runtime:sparkling-shape-7ae5:/",
            "--evidence", "explicit deployment approval",
            "--intent-understood",
            "--context-complete",
            "--quality-ready",
            "--evidence-ready",
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
        for name in LEGACY_HUB_WORKFLOWS:
            self.assertFalse((WORKFLOWS / name).exists(), f"legacy workflow still present: {name}")

    def test_no_workflow_points_at_nonexistent_canonical_deployment(self):
        for path in WORKFLOWS.glob("*.yml"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "deploy-nayanet-hub-canonical.yml",
                text,
                msg=f"stale canonical deployment reference in {path.name}",
            )
