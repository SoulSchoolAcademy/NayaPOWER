#!/usr/bin/env python3
"""Fail-closed regression tests for NayaPOWER deployment governance."""
from __future__ import annotations

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
CANONICAL_PROJECT_ID = "prj_cHa9gwrtscCW8JuMDjcvw6DafaOK"


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
    auth = {
        "status": "AUTHORIZED",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "commit_sha": "abc123",
        "target_environment": "production",
        "deployment_surface": "vercel",
        "vercel_project_id": CANONICAL_PROJECT_ID,
        "approval": "EXPLICIT_APPROVAL_GRANTED",
        "verification": {"status": "PASS", "evidence": ["tests passed"]},
    }
    assert not deployment_allowed(authorization=auth, commit_sha="different", target="production")


def test_wrong_vercel_project_is_denied():
    auth = {
        "status": "AUTHORIZED",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "commit_sha": "abc123",
        "target_environment": "production",
        "deployment_surface": "vercel",
        "vercel_project_id": "wrong-project",
        "approval": "EXPLICIT_APPROVAL_GRANTED",
        "verification": {"status": "PASS", "evidence": ["tests passed"]},
    }
    assert not deployment_allowed(authorization=auth, commit_sha="abc123", target="production")


def test_authorized_release_is_permitted():
    auth = {
        "status": "AUTHORIZED",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "commit_sha": "abc123",
        "target_environment": "production",
        "deployment_surface": "vercel",
        "vercel_project_id": CANONICAL_PROJECT_ID,
        "approval": "EXPLICIT_APPROVAL_GRANTED",
        "verification": {"status": "PASS", "evidence": ["tests passed"]},
    }
    assert deployment_allowed(authorization=auth, commit_sha="abc123", target="production")


def test_only_the_canonical_release_workflow_may_contain_vercel_deploy_command():
    forbidden_markers = ("vercel deploy", "vercel@latest deploy", "deploy --prod")
    offenders = []
    for path in WORKFLOWS.glob("*.yml"):
        # The governance workflow contains scanner literals but has no deployment capability.
        if path.resolve() in {AUTHORIZED_WORKFLOW.resolve(), GOVERNANCE_WORKFLOW.resolve()}:
            continue
        text = path.read_text(encoding="utf-8").lower()
        if any(marker in text for marker in forbidden_markers):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f"Vercel deployment bypass candidates found: {offenders}"


def test_governance_workflow_does_not_execute_vercel():
    text = GOVERNANCE_WORKFLOW.read_text(encoding="utf-8").lower()
    # It may contain literal scanner patterns, but must not contain an executable
    # Vercel deployment invocation or a Vercel deployment action.
    executable_markers = (
        "npx vercel deploy",
        "npm exec vercel deploy",
        "yarn vercel deploy",
        "pnpm vercel deploy",
        "vercel@latest deploy",
        "amondnet/vercel-action",
        "vercel/action",
    )
    assert not any(marker in text for marker in executable_markers)


def test_canonical_release_workflow_contains_the_only_deployment_boundary():
    text = AUTHORIZED_WORKFLOW.read_text(encoding="utf-8").lower()
    assert "workflow_dispatch" in text
    assert "commit_sha" in text
    assert "release_id" in text
    assert "explicit_approval_granted" in text
    assert "release_authorization.py" in text
    assert "vercel_project_id" in text
    assert "vercel@latest deploy" in text


def test_mutating_repository_workflows_require_explicit_dispatch():
    """Repository-mutating bridge workflows must never react automatically to pushes/PRs."""
    for path in (MAXESS_BRIDGE_WORKFLOW, INTEGRATED_RESULTS_WORKFLOW):
        text = path.read_text(encoding="utf-8")
        normalized = text.lower()
        assert "workflow_dispatch:" in normalized, f"manual dispatch missing: {path}"
        assert "approval:" in normalized, f"explicit approval input missing: {path}"
        assert "explicit_approval_granted" in normalized, f"approval gate missing: {path}"
        assert "if: inputs.approval == 'explicit_approval_granted'" in normalized, f"job gate missing: {path}"
        assert "git push" in normalized, f"mutation boundary unexpectedly absent: {path}"
        # The YAML must not contain an automatic push or pull-request event trigger.
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
