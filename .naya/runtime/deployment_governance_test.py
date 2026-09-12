#!/usr/bin/env python3
"""Fail-closed regression tests for NayaPOWER deployment governance."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / ".naya" / "control-plane" / "DEPLOYMENT-GOVERNANCE.json"
AUTH = ROOT / ".naya" / "control-plane" / "RELEASE-AUTHORIZATION.json"
VERCEL = ROOT / "vercel.json"
WORKFLOWS = ROOT / ".github" / "workflows"
AUTHORIZED_WORKFLOW = WORKFLOWS / "authorized-vercel-release.yml"
GOVERNANCE_WORKFLOW = WORKFLOWS / "deployment-governance.yml"
MAXESS_BRIDGE_WORKFLOW = WORKFLOWS / "apply-maxess-result-bridge.yml"
INTEGRATED_RESULTS_WORKFLOW = WORKFLOWS / "build-integrated-results.yml"
AISCORE_BRIDGE_WORKFLOW = WORKFLOWS / "build-aiscore-app-bridge.yml"
NAYANET_HUB_PATCH_WORKFLOW = WORKFLOWS / "2026-09-08-10-05-apply-nayanet-hub-surgical-patch.yml"
INTELLIGENCE_PROMOTION_WORKFLOW = WORKFLOWS / "intelligence-promotion.yml"
CANONICAL_PROJECT_ID = "prj_cHa9gwrtscCW8JuMDjcvw6DafaOK"
KERNEL_MARKER = ".naya/control-plane/workflow_gate.py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def deployment_allowed(*, authorization: dict, commit_sha: str, target: str) -> bool:
    return (
        authorization.get("status") == "AUTHORIZED"
        and authorization.get("repository") == "SoulSchoolAcademy/NayaPOWER"
        and authorization.get("commit_sha") == commit_sha
        and authorization.get("target_environment") == target
        and authorization.get("deployment_surface") == "vercel"
        and authorization.get("vercel_project_id") == CANONICAL_PROJECT_ID
        and authorization.get("approval") == "EXPLICIT_APPROVAL_GRANTED"
        and authorization.get("verification", {}).get("status") == "PASS"
        and bool(authorization.get("verification", {}).get("evidence"))
    )


def kernel_release_authorization(*, authorization: dict, commit_sha: str, target: str):
    module_path = ROOT / ".naya" / "runtime" / "release_authorization.py"
    spec = importlib.util.spec_from_file_location("naya_release_authorization", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.authorize(authorization=authorization, commit_sha=commit_sha, target_environment=target)


def valid_kernel_authorization(commit_sha="a" * 40, target="preview"):
    now = datetime.now(timezone.utc)
    return {
        "status": "AUTHORIZED",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "commit_sha": commit_sha,
        "target_environment": target,
        "deployment_surface": "vercel",
        "vercel_project_id": CANONICAL_PROJECT_ID,
        "release_id": "REL-KERNEL-TEST",
        "release_reason": "kernel boundary regression test",
        "verification": {"status": "PASS", "evidence": ["test evidence"]},
        "authorized_by": "test-human",
        "authorized_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=1)).isoformat(),
        "approval": "EXPLICIT_APPROVAL_GRANTED",
    }


def test_vercel_git_deployments_disabled():
    assert load(VERCEL)["git"]["deploymentEnabled"] is False


def test_release_contract_is_fail_closed_template():
    auth = load(AUTH)
    assert auth["status"] == "TEMPLATE"
    assert auth["vercel_project_id"] == CANONICAL_PROJECT_ID
    assert not deployment_allowed(authorization=auth, commit_sha="abc", target="production")


def test_documentation_change_does_not_authorize_deployment():
    assert not deployment_allowed(authorization=load(AUTH), commit_sha="docs", target="preview")


def test_smart_note_change_does_not_authorize_deployment():
    assert not deployment_allowed(authorization=load(AUTH), commit_sha="smart-note", target="preview")


def test_naya_governance_change_does_not_authorize_deployment():
    assert not deployment_allowed(authorization=load(AUTH), commit_sha="governance", target="production")


def test_normal_commit_does_not_authorize_deployment():
    assert not deployment_allowed(authorization=load(AUTH), commit_sha="ordinary", target="production")


def test_wrong_commit_is_denied_even_when_other_fields_are_valid():
    auth = valid_kernel_authorization(commit_sha="abc123")
    assert not deployment_allowed(authorization=auth, commit_sha="different", target="production")


def test_wrong_vercel_project_is_denied():
    auth = valid_kernel_authorization(commit_sha="abc123", target="production")
    auth["vercel_project_id"] = "wrong-project"
    assert not deployment_allowed(authorization=auth, commit_sha="abc123", target="production")


def test_authorized_release_is_permitted_by_legacy_boundary():
    auth = valid_kernel_authorization(commit_sha="abc123", target="production")
    assert deployment_allowed(authorization=auth, commit_sha="abc123", target="production")


def test_authorized_release_is_also_permitted_by_canonical_kernel():
    auth = valid_kernel_authorization(commit_sha="a" * 40, target="production")
    decision = kernel_release_authorization(authorization=auth, commit_sha="a" * 40, target="production")
    assert decision.allowed, decision.reason
    assert "canonical governance kernel" in decision.reason


def test_kernel_denies_expired_release_authorization():
    auth = valid_kernel_authorization()
    auth["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    decision = kernel_release_authorization(authorization=auth, commit_sha=auth["commit_sha"], target=auth["target_environment"])
    assert not decision.allowed
    assert "expired" in decision.reason


def test_kernel_denies_missing_release_authority():
    auth = valid_kernel_authorization()
    auth.pop("authorized_by")
    decision = kernel_release_authorization(authorization=auth, commit_sha=auth["commit_sha"], target=auth["target_environment"])
    assert not decision.allowed


def test_known_repository_mutation_workflows_cross_the_canonical_kernel():
    for path in (
        MAXESS_BRIDGE_WORKFLOW,
        INTEGRATED_RESULTS_WORKFLOW,
        AISCORE_BRIDGE_WORKFLOW,
        NAYANET_HUB_PATCH_WORKFLOW,
        INTELLIGENCE_PROMOTION_WORKFLOW,
    ):
        text = path.read_text(encoding="utf-8")
        assert KERNEL_MARKER in text, f"canonical kernel gate missing: {path}"
        assert "EXPLICIT_APPROVAL_GRANTED" in text, f"explicit approval missing: {path}"


def test_intelligence_promotion_cannot_mutate_on_automatic_push():
    text = INTELLIGENCE_PROMOTION_WORKFLOW.read_text(encoding="utf-8").lower()
    assert "push:" in text
    assert "github.event_name == 'workflow_dispatch'" in text
    assert "inputs.approval == 'explicit_approval_granted'" in text
    assert "git push" in text


def test_only_the_canonical_release_workflow_may_contain_vercel_deploy_command():
    forbidden_markers = ("vercel deploy", "vercel@latest deploy", "deploy --prod")
    offenders = []
    for path in WORKFLOWS.glob("*.yml"):
        if path.resolve() in {AUTHORIZED_WORKFLOW.resolve(), GOVERNANCE_WORKFLOW.resolve()}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        if any(marker in text for marker in forbidden_markers):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f"Vercel deployment bypass candidates found: {offenders}"


def test_governance_workflow_does_not_execute_vercel():
    text = GOVERNANCE_WORKFLOW.read_text(encoding="utf-8").lower()
    executable_markers = (
        "npx vercel deploy", "npm exec vercel deploy", "yarn vercel deploy",
        "pnpm vercel deploy", "vercel@latest deploy", "amondnet/vercel-action", "vercel/action",
    )
    assert not any(marker in text for marker in executable_markers)


def test_canonical_release_workflow_contains_the_only_deployment_boundary():
    text = AUTHORIZED_WORKFLOW.read_text(encoding="utf-8").lower()
    assert "workflow_dispatch" in text
    assert "commit_sha" in text
    assert "release_id" in text
    assert "explicit_approval_granted" in text
    assert "release_authorization.py" in text
    assert "governance-kernel" in text
    assert "vercel_project_id" in text
    assert "vercel@latest deploy" in text


def test_mutating_repository_workflows_require_explicit_dispatch():
    """Repository-mutating workflows must never react automatically to pushes/PRs."""
    for path in (
        MAXESS_BRIDGE_WORKFLOW,
        INTEGRATED_RESULTS_WORKFLOW,
        AISCORE_BRIDGE_WORKFLOW,
        NAYANET_HUB_PATCH_WORKFLOW,
    ):
        text = path.read_text(encoding="utf-8")
        normalized = text.lower()
        assert "workflow_dispatch:" in normalized, f"manual dispatch missing: {path}"
        assert "approval:" in normalized, f"explicit approval input missing: {path}"
        assert "explicit_approval_granted" in normalized, f"approval gate missing: {path}"
        assert "if: inputs.approval == 'explicit_approval_granted'" in normalized, f"job gate missing: {path}"
        assert "git push" in normalized, f"mutation boundary unexpectedly absent: {path}"
        lines = [line.strip().lower() for line in text.splitlines()]
        assert not any(line in {"push:", "pull_request:"} for line in lines), f"automatic trigger remains: {path}"


def test_policy_preserves_connection_but_denies_default_deployment():
    policy = load(POLICY)
    assert policy["default"]["deployment"] == "DENY"
    assert policy["default"]["preview_deployment"] == "DENY"
    assert policy["default"]["production_deployment"] == "DENY"


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} deployment-governance tests")
