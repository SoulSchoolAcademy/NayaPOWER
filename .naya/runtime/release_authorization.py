#!/usr/bin/env python3
"""Fail-closed release authorization for NayaPOWER.

Unified with the ONE UniversalExecutionGate: this module is a thin
compatibility layer over `release_execution_boundary`. It never mints an
Authority. The ONLY accepted source of power is an ExecutionAuthorization
issued by the UniversalExecutionGate (registry + canonical governance kernel).

Release conditions (surface, environment, project, worker, commit, repository)
are CONDITIONS, never authority. Caller-declared "authorization"/"approval"
strings are accepted as release metadata at most and are irrelevant to the
decision.
"""
from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / ".naya" / "control-plane" / "DEPLOYMENT-GOVERNANCE.json"
AUTH_PATH = ROOT / ".naya" / "control-plane" / "RELEASE-AUTHORIZATION.json"
CANONICAL_PROJECT_ID = "prj_cHa9gwrtscCW8JuMDjcvw6DafaOK"


def _boundary_module():
    """Load the ONE release execution boundary by its canonical path."""
    path = Path(__file__).resolve().parent / "release_execution_boundary.py"
    name = "naya_release_execution_boundary_canonical"
    if name in sys.modules:
        return sys.modules[name]
    if not path.is_file():
        raise RuntimeError("release execution boundary is missing")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("release execution boundary cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


BOUNDARY = _boundary_module()


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


def authorize(
    *,
    execution_authorization=None,
    gate=None,
    commit_sha: str,
    target_environment: str,
    deployment_surface: str = "vercel",
    repository: str = "SoulSchoolAcademy/NayaPOWER",
    worker_name=None,
    project_id: str = CANONICAL_PROJECT_ID,
) -> Decision:
    """ALLOW a release ONLY for the exact gate-issued ExecutionAuthorization."""
    if execution_authorization is None or gate is None:
        return Decision(
            False,
            "a gate-issued ExecutionAuthorization and the UniversalExecutionGate are required",
        )
    try:
        result = BOUNDARY.authorize_release(
            gate=gate,
            execution_authorization=execution_authorization,
            commit_sha=commit_sha,
            target_environment=target_environment,
            deployment_surface=deployment_surface,
            repository=repository,
            worker_name=worker_name,
            project_id=project_id,
        )
    except (TypeError, ValueError) as exc:
        return Decision(False, f"release conditions are invalid: {exc}")
    if not result.allowed:
        return Decision(False, result.reason)
    return Decision(True, result.reason)


def current_template_decision(commit_sha: str, target_environment: str) -> Decision:
    """The checked-in template declares nothing the gate issued, so it fails closed."""
    try:
        template = _load(AUTH_PATH)
    except (OSError, ValueError):
        template = {}
    if not template:
        return Decision(False, "release authorization template is missing")
    authorization = template.get("authorization", template)
    if authorization.get("repository") != "SoulSchoolAcademy/NayaPOWER":
        return Decision(False, "repository binding mismatch")
    if authorization.get("commit_sha") and authorization.get("commit_sha") != commit_sha:
        return Decision(False, "exact commit SHA binding mismatch")
    if authorization.get("deployment_surface") not in ("cloudflare", "vercel", None):
        return Decision(False, "deployment surface is invalid")
    if authorization.get("vercel_project_id", CANONICAL_PROJECT_ID) != CANONICAL_PROJECT_ID:
        return Decision(False, "Vercel project binding mismatch")
    try:
        target = BOUNDARY.deploy_target(
            deployment_surface=authorization.get("deployment_surface", "vercel"),
            environment=target_environment,
            repository="SoulSchoolAcademy/NayaPOWER",
            commit_sha=commit_sha,
            worker_name=authorization.get("worker_name"),
            project_id=authorization.get("vercel_project_id", CANONICAL_PROJECT_ID),
        )
    except (TypeError, ValueError):
        return Decision(False, "template declares an invalid release target")
    return Decision(False, f"template is not gate-issued; declared target is {target}")


def policy() -> dict:
    return _load(POLICY_PATH)


__all__ = ["Decision", "authorize", "current_template_decision", "policy"]