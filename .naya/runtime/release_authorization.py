#!/usr/bin/env python3
"""Fail-closed release authorization gate for NayaPOWER."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / ".naya" / "control-plane" / "DEPLOYMENT-GOVERNANCE.json"
AUTH_PATH = ROOT / ".naya" / "control-plane" / "RELEASE-AUTHORIZATION.json"
KERNEL_PATH = ROOT / ".naya" / "control-plane" / "governance_kernel.py"
CANONICAL_PROJECT_ID = "prj_cHa9gwrtscCW8JuMDjcvw6DafaOK"


class Decision:
    """Dependency-free decision value returned by the release gate."""

    __slots__ = ("allowed", "reason")

    def __init__(self, allowed: bool, reason: str) -> None:
        self.allowed = allowed
        self.reason = reason

    def __repr__(self) -> str:
        return f"Decision(allowed={self.allowed!r}, reason={self.reason!r})"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _kernel_module():
    if not KERNEL_PATH.is_file():
        raise RuntimeError("canonical governance kernel is missing")
    spec = importlib.util.spec_from_file_location("naya_governance_kernel", KERNEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical governance kernel cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _kernel_gate(*, authorization: dict, commit_sha: str, target_environment: str) -> Decision:
    """Route release authorization through the canonical constitutional kernel."""
    try:
        kernel = _kernel_module()
        authorized_by = authorization.get("authorized_by")
        authority = {
            "authority_id": authorization.get("release_id"),
            "issuer": f"human:{authorized_by}",
            "holder": authorized_by,
            "actor": authorized_by,
            "purpose": "authorized-vercel-release",
            "permissions": ["release:vercel"],
            "scope": {
                "repository": "SoulSchoolAcademy/NayaPOWER",
                "environment": target_environment,
                "vercel_project_id": CANONICAL_PROJECT_ID,
            },
            "conditions": ["exact_commit_binding", "canonical_project_binding", "explicit_approval"],
            "issued_at": authorization.get("authorized_at"),
            "expires_at": authorization.get("expires_at"),
            "revoked_at": authorization.get("revoked_at"),
            "delegable": False,
            "delegation_scope": None,
            "evidence": authorization.get("verification", {}).get("evidence", []),
            "status": "ACTIVE",
        }
        decision = {
            "decision_id": authorization.get("release_id"),
            "mission": "Release exact NayaPOWER commit to canonical Vercel runtime",
            "actor": authorized_by,
            "request": f"deploy:{commit_sha}:{target_environment}",
            "purpose": "authorized-vercel-release",
            "authority": authority,
            "scope": authority["scope"],
            "boundaries": ["canonical_vercel_project_only", "exact_commit_only", "explicit_approval_only"],
            "evidence": authorization.get("verification", {}).get("evidence", []),
            "uncertainty": 2,
            "consequence": 4,
            "reversibility": 2,
            "risk": {"irreversibility": 4, "prohibited": False},
            "alternatives": ["do_not_release"],
            "value": "publish_authorized_verified_artifact",
            "required_permission": "release:vercel",
            "decision": "EXECUTE",
            "execution_plan": ["deploy exact verified commit to canonical Vercel project"],
            "verification_plan": ["exact commit", "runtime surface", "live runtime observation"],
            "stop_conditions": ["authorization mismatch", "kernel halt", "deployment failure", "runtime verification failure"],
            "receipt_requirements": ["release authorization", "deployment evidence", "runtime verification"],
            "learning_output": "release verification result",
        }
        risk = kernel.GovernanceKernel().gate(decision, authority)
        return Decision(True, f"canonical governance kernel accepted release at {risk.tier}")
    except Exception as exc:
        return Decision(False, f"canonical governance kernel denied release: {exc}")


def authorize(*, authorization: dict, commit_sha: str, target_environment: str) -> Decision:
    """ALLOW only when every release gate is explicitly satisfied."""
    if not isinstance(commit_sha, str) or not commit_sha:
        return Decision(False, "exact commit SHA is required")
    if target_environment not in {"preview", "production"}:
        return Decision(False, "target environment must be preview or production")
    if authorization.get("status") != "AUTHORIZED":
        return Decision(False, "release authorization is not AUTHORIZED")
    if authorization.get("repository") != "SoulSchoolAcademy/NayaPOWER":
        return Decision(False, "repository binding mismatch")
    if authorization.get("commit_sha") != commit_sha:
        return Decision(False, "exact commit SHA binding mismatch")
    if authorization.get("target_environment") != target_environment:
        return Decision(False, "target environment mismatch")
    if authorization.get("deployment_surface") != "vercel":
        return Decision(False, "deployment surface is not Vercel")
    if authorization.get("vercel_project_id") != CANONICAL_PROJECT_ID:
        return Decision(False, "Vercel project binding mismatch")
    if authorization.get("approval") != "EXPLICIT_APPROVAL_GRANTED":
        return Decision(False, "explicit approval is missing")
    verification = authorization.get("verification")
    if not isinstance(verification, dict) or verification.get("status") != "PASS":
        return Decision(False, "verification status is not PASS")
    evidence = verification.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return Decision(False, "verification evidence is required")
    for field in ("release_id", "release_reason", "authorized_by", "authorized_at", "expires_at"):
        value = authorization.get(field)
        if not isinstance(value, str) or not value or value.startswith("REQUIRED") or value.startswith("REPLACE_WITH"):
            return Decision(False, f"required authorization field missing: {field}")
    try:
        expires = datetime.fromisoformat(authorization["expires_at"].replace("Z", "+00:00"))
        if expires.tzinfo is None or expires <= datetime.now(timezone.utc):
            return Decision(False, "release authorization is expired")
    except ValueError:
        return Decision(False, "release authorization expiry is invalid")
    return _kernel_gate(authorization=authorization, commit_sha=commit_sha, target_environment=target_environment)


def current_template_decision(commit_sha: str, target_environment: str) -> Decision:
    return authorize(authorization=_load(AUTH_PATH), commit_sha=commit_sha, target_environment=target_environment)


def policy() -> dict:
    return _load(POLICY_PATH)
