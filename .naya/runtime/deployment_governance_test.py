#!/usr/bin/env python3
"""Fail-closed regression tests for active NayaPOWER governance boundaries."""
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
BUILD_WORKFLOW = WORKFLOWS / "build-nayahub-intelligent.yml"
DEPLOY_WORKFLOW = WORKFLOWS / "deploy-nayanet-hub-canonical-v2.yml"
INTELLIGENCE_WORKFLOW = WORKFLOWS / "intelligence-promotion.yml"
KERNEL_MARKER = ".naya/control-plane/workflow_gate.py"
CANONICAL_PROJECT_ID = "prj_cHa9gwrtscCW8JuMDjcvw6DafaOK"
LEGACY_WORKFLOWS = (
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

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def deployment_allowed(*, authorization: dict, commit_sha: str, target: str) -> bool:
    return (authorization.get("status") == "AUTHORIZED" and authorization.get("repository") == "SoulSchoolAcademy/NayaPOWER" and authorization.get("commit_sha") == commit_sha and authorization.get("target_environment") == target and authorization.get("deployment_surface") == "vercel" and authorization.get("vercel_project_id") == CANONICAL_PROJECT_ID and authorization.get("approval") == "EXPLICIT_APPROVAL_GRANTED" and authorization.get("verification", {}).get("status") == "PASS" and bool(authorization.get("verification", {}).get("evidence")))

def kernel_release_authorization(*, authorization: dict, commit_sha: str, target: str):
    path = ROOT / ".naya" / "runtime" / "release_authorization.py"
    spec = importlib.util.spec_from_file_location("naya_release_authorization", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.authorize(authorization=authorization, commit_sha=commit_sha, target_environment=target)

def valid_authorization(commit_sha="a" * 40, target="preview"):
    now = datetime.now(timezone.utc)
    return {"status":"AUTHORIZED","repository":"SoulSchoolAcademy/NayaPOWER","commit_sha":commit_sha,"target_environment":target,"deployment_surface":"vercel","vercel_project_id":CANONICAL_PROJECT_ID,"release_id":"REL-KERNEL-TEST","release_reason":"kernel boundary regression test","verification":{"status":"PASS","evidence":["test evidence"]},"authorized_by":"test-human","authorized_at":now.isoformat(),"expires_at":(now+timedelta(hours=1)).isoformat(),"approval":"EXPLICIT_APPROVAL_GRANTED"}

def test_vercel_git_deployments_disabled():
    assert load(VERCEL)["git"]["deploymentEnabled"] is False

def test_release_contract_is_fail_closed_template():
    auth=load(AUTH); assert auth["status"]=="TEMPLATE"; assert auth["vercel_project_id"]==CANONICAL_PROJECT_ID; assert not deployment_allowed(authorization=auth,commit_sha="abc",target="production")

def test_denial_matrix():
    for field,value in (("commit_sha","wrong"),("vercel_project_id","wrong-project"),("approval","DENY"),("status","TEMPLATE")):
        auth=valid_authorization(commit_sha="abc123",target="production"); auth[field]=value
        assert not deployment_allowed(authorization=auth,commit_sha="abc123",target="production")

def test_kernel_allows_valid_and_denies_expired():
    auth=valid_authorization(target="production"); decision=kernel_release_authorization(authorization=auth,commit_sha=auth["commit_sha"],target="production"); assert decision.allowed
    auth["expires_at"]=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat(); decision=kernel_release_authorization(authorization=auth,commit_sha=auth["commit_sha"],target="production"); assert not decision.allowed

def test_active_hub_build_is_manual_and_kernel_gated():
    text=BUILD_WORKFLOW.read_text(encoding="utf-8"); normalized=text.lower()
    assert "workflow_dispatch:" in normalized and "approval:" in normalized and "explicit_approval_granted" in normalized
    assert KERNEL_MARKER in text and "git push" in normalized
    assert not any(line in {"push:","pull_request:","schedule:"} for line in (x.strip().lower() for x in text.splitlines()))

def test_active_hub_deploy_is_exact_sha_manual_and_kernel_gated():
    text=DEPLOY_WORKFLOW.read_text(encoding="utf-8"); normalized=text.lower()
    assert "workflow_dispatch:" in normalized and "commit_sha:" in normalized and "approval:" in normalized
    assert KERNEL_MARKER in text and "exact source sha" in normalized and "cloudflare/wrangler-action" in normalized
    assert not any(line in {"push:","pull_request:","schedule:","workflow_call:"} for line in (x.strip().lower() for x in text.splitlines()))

def test_intelligence_promotion_is_authorized_after_push_identification():
    text=INTELLIGENCE_WORKFLOW.read_text(encoding="utf-8").lower()
    assert "push:" in text and "workflow_dispatch:" in text and "github.event_name == 'workflow_dispatch'" in text
    assert "inputs.approval == 'explicit_approval_granted'" in text and KERNEL_MARKER in text and "git push" in text

def test_governance_workflow_never_executes_vercel():
    text=GOVERNANCE_WORKFLOW.read_text(encoding="utf-8").lower()
    assert not any(x in text for x in ("npx vercel deploy","npm exec vercel deploy","amondnet/vercel-action","vercel/action"))

def test_only_authorized_release_workflow_contains_vercel_deploy():
    offenders=[]
    for path in WORKFLOWS.glob("*.yml"):
        if path.resolve() in {AUTHORIZED_WORKFLOW.resolve(),GOVERNANCE_WORKFLOW.resolve(),DEPLOY_WORKFLOW.resolve()}: continue
        text=path.read_text(encoding="utf-8").lower()
        if "vercel@latest deploy" in text or "deploy --prod" in text: offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, offenders

def test_legacy_hub_workflows_are_non_mutating_and_retired():
    for name in LEGACY_WORKFLOWS:
        path=WORKFLOWS/name
        if not path.exists(): continue
        text=path.read_text(encoding="utf-8")
        assert "RETIRED" in text, name
        assert "contents: write" not in text and "git push" not in text and "cloudflare/wrangler-action" not in text and "workflow_call:" not in text, name

def test_policy_denies_default_deployment():
    policy=load(POLICY); assert policy["default"]["deployment"]=="DENY"; assert policy["default"]["preview_deployment"]=="DENY"; assert policy["default"]["production_deployment"]=="DENY"

if __name__ == "__main__":
    tests=[value for name,value in globals().items() if name.startswith("test_")]
    for test in tests: test(); print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} deployment-governance tests")
