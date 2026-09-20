#!/usr/bin/env python3
"""Release/Deployment & repository-mutation execution boundary for NayaPOWER.

This module is a VALIDATION-ONLY layer. It deliberately:

  * does NOT mint, expand, delegate, or create authority of any kind;
  * consumes the ONE UniversalExecutionGate and the ExecutionAuthorization it
    issued (derived from the human-controlled authority registry + canonical
    governance kernel);
  * treats release conditions (environment / project / worker / commit / paths)
    as CONDITIONS to verify, never as authority;
  * refuses caller-declared "authorization"/"approval" strings, receipts,
    claims, secrets, and execution state on every path.

The exact target (surface, runtime, environment, repository, commit) is bound
into the gate credential's `target` field, so a credential issued for the
canonical worker/commit can never authorize a different worker, environment,
project, commit, or repository mutation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable, Optional

RELEASE_ENVIRONMENTS = frozenset({"preview", "production"})
DEPLOYMENT_SURFACES = frozenset({"cloudflare", "vercel"})
RELEASE_ACTION_TYPES = frozenset({"deploy", "deploy_public_runtime", "release"})
REPO_MUTATION_ACTION_TYPES = frozenset({"repository_write", "repo_write", "file_write", "write"})
DEPLOY_PERMISSION = "deploy_public_runtime"
REPO_WRITE_PERMISSION = "repo_write"

DEFAULT_REPOSITORY = "SoulSchoolAcademy/NayaPOWER"


def deploy_target(
    *,
    deployment_surface: str,
    environment: str,
    repository: str,
    commit_sha: str,
    worker_name: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    """Canonical, exact deploy target string bound into the credential."""
    if deployment_surface not in DEPLOYMENT_SURFACES:
        raise ValueError("deployment surface must be cloudflare or vercel")
    surface_id = worker_name if deployment_surface == "cloudflare" else (project_id or "")
    if not surface_id:
        raise ValueError("worker_name (cloudflare) or project_id (vercel) is required")
    return (
        f"{deployment_surface}-runtime:{surface_id}"
        f":environment:{environment}:repository:{repository}:commit:{commit_sha}"
    )


def repo_mutation_target(*, repository: str, target_paths: Iterable[str]) -> str:
    """Canonical, exact change-set target string bound into the credential."""
    paths = sorted(str(path) for path in target_paths)
    if not paths:
        raise ValueError("target_paths is required")
    return f"repo:{repository}:paths:{','.join(paths)}"


@dataclass(frozen=True)
class BoundaryDecision:
    """Fail-closed result of a release/mutation boundary check."""

    allowed: bool
    reason: str
    approval_required_for: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _verify_credential(execution_authorization: Any, gate: Any) -> BoundaryDecision:
    if gate is None:
        return BoundaryDecision(False, "no UniversalExecutionGate supplied; release cannot be verified")
    if execution_authorization is None:
        return BoundaryDecision(False, "no gate-issued ExecutionAuthorization supplied")
    ok, reasons = gate.verify(execution_authorization)
    if not ok:
        return BoundaryDecision(False, "gate verification failed: " + "; ".join(reasons))
    return BoundaryDecision(True, "")


def authorize_release(
    *,
    gate: Any,
    execution_authorization: Any,
    commit_sha: str,
    target_environment: str,
    deployment_surface: str,
    repository: str = DEFAULT_REPOSITORY,
    worker_name: Optional[str] = None,
    project_id: Optional[str] = None,
) -> BoundaryDecision:
    """ALLOW a release/deployment ONLY for the exact gate-bound target."""
    if not isinstance(commit_sha, str) or not commit_sha:
        return BoundaryDecision(False, "exact commit SHA is required")
    if target_environment not in RELEASE_ENVIRONMENTS:
        return BoundaryDecision(False, "target environment must be preview or production")
    if deployment_surface not in DEPLOYMENT_SURFACES:
        return BoundaryDecision(False, "deployment surface must be cloudflare or vercel")
    if not repository:
        return BoundaryDecision(False, "repository binding is required")

    verified = _verify_credential(execution_authorization, gate)
    if not verified.allowed:
        return verified

    expected_target = deploy_target(
        deployment_surface=deployment_surface,
        environment=target_environment,
        repository=repository,
        commit_sha=commit_sha,
        worker_name=worker_name,
        project_id=project_id,
    )
    if execution_authorization.target != expected_target:
        return BoundaryDecision(
            False,
            "credential was not issued for this exact deploy target "
            f"(expected {expected_target!r})",
        )
    if execution_authorization.action_type not in RELEASE_ACTION_TYPES:
        return BoundaryDecision(
            False,
            f"credential action_type {execution_authorization.action_type!r} "
            f"is not a release action",
        )
    if execution_authorization.permission != DEPLOY_PERMISSION:
        return BoundaryDecision(
            False,
            f"credential permission {execution_authorization.permission!r} "
            f"is not {DEPLOY_PERMISSION!r}",
        )
    return BoundaryDecision(
        True,
        "release authorized by gate-issued ExecutionAuthorization bound to the exact target",
        approval_required_for=execution_authorization.target,
    )


def authorize_repo_mutation(
    *,
    gate: Any,
    execution_authorization: Any,
    target_paths: Iterable[str],
    repository: str = DEFAULT_REPOSITORY,
) -> BoundaryDecision:
    """ALLOW a repository mutation ONLY for the exact gate-bound change-set."""
    if not repository:
        return BoundaryDecision(False, "repository binding is required")

    verified = _verify_credential(execution_authorization, gate)
    if not verified.allowed:
        return verified

    expected_target = repo_mutation_target(repository=repository, target_paths=target_paths)
    if execution_authorization.target != expected_target:
        return BoundaryDecision(
            False,
            "credential was not issued for this exact change-set "
            f"(expected {expected_target!r})",
        )
    if execution_authorization.action_type not in REPO_MUTATION_ACTION_TYPES:
        return BoundaryDecision(
            False,
            f"credential action_type {execution_authorization.action_type!r} "
            f"is not a repository mutation action",
        )
    if execution_authorization.permission != REPO_WRITE_PERMISSION:
        return BoundaryDecision(
            False,
            f"credential permission {execution_authorization.permission!r} "
            f"is not {REPO_WRITE_PERMISSION!r}",
        )
    return BoundaryDecision(
        True,
        "repository mutation authorized by gate-issued ExecutionAuthorization bound to the exact change-set",
        approval_required_for=expected_target,
    )


__all__ = [
    "BoundaryDecision",
    "deploy_target",
    "repo_mutation_target",
    "authorize_release",
    "authorize_repo_mutation",
    "RELEASE_ENVIRONMENTS",
    "DEPLOYMENT_SURFACES",
    "RELEASE_ACTION_TYPES",
    "REPO_MUTATION_ACTION_TYPES",
    "DEPLOY_PERMISSION",
    "REPO_WRITE_PERMISSION",
    "DEFAULT_REPOSITORY",
]