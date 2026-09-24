#!/usr/bin/env python3
"""Portable, independently verifiable authorization (NAYA POWER TEST #12).

The UniversalExecutionGate remains the ONE authority issuer. This module does
NOT create a second authority system and does NOT mint, expand, delegate, or
modify authority. It makes the gate-issued `ExecutionAuthorization` portable
across a process boundary so that an independent GitHub Actions runner can
verify it WITHOUT the issuer's in-process `_issued` set.

Provenance model (Ed25519 asymmetric signature, smallest sufficient mechanism):

  ISSUER (human-controlled tooling): holds the PRIVATE signing key,
          calls gate.authorize(...) -> signs the portable artifact.
  VERIFIER (the GitHub runner):       holds ONLY the PINNED PUBLIC key,
          recomputes the binding hash, re-reads the canonical registry,
          and checks signature + expiry + revocation at time of use.

  VERIFIER CANNOT ISSUE NEW AUTHORITY: the pinned public key cannot sign.
  A workflow token / GITHUB_TOKEN / provider secret provides capability only.

The runtime default pin is UNSET (None): verification fails closed until the
human provisions a public key pin. Tests pass explicit keypairs. Nothing here
is wired to a live workflow, and signing keys never live in this repository.

Deterministic hashing is NOT provenance; the in-process `_issued` set is NOT
portable. A valid signature over a fresh gate credential IS both.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Tuple

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
        Ed25519PublicKey,
    )
except Exception:  # pragma: no cover - verification requires cryptography
    InvalidSignature = type("InvalidSignature", (Exception,), {})
    Ed25519PrivateKey = None
    Ed25519PublicKey = None

_RUNTIME_DIR = Path(__file__).resolve().parent
_GOVERNANCE_DIR = _RUNTIME_DIR.parents[1] / "governance"
_REGISTRY_PATH = _GOVERNANCE_DIR / "authority-registry.json"
_GATE_PATH = _RUNTIME_DIR / "universal_execution_gate.py"
_BOUNDARY_PATH = _RUNTIME_DIR / "release_execution_boundary.py"

# In-repo public key pin (provisioned by the human only). UNSET = fail closed.
VERIFIER_PUBLIC_KEY_PEM: Optional[str] = None
VERIFIER_PUBLIC_KEY_HEX: Optional[str] = None
PIN_PATH = _RUNTIME_DIR / "portable-authorization-public-key.hex"

SCHEMA = "naya/portable_authorization/v1"
MAX_ARTIFACT_TTL_MINUTES = 30
DEFAULT_EXPIRES_IN_SECONDS = 15 * 60


def _load_by_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


GATE = _load_by_path("naya_portable_authorization_gate", _GATE_PATH)
BOUNDARY = _load_by_path("naya_portable_authorization_boundary", _BOUNDARY_PATH)

GovernanceState = GATE.GovernanceState
_LOAD_REGISTRY = GATE.load_registry
_BINDING_HASH = GATE._execution_binding_hash
_GRANT_FINGERPRINT = GATE.grant_fingerprint

DEPLOY_PERMISSION = BOUNDARY.DEPLOY_PERMISSION
DEPLOYMENT_SURFACES = BOUNDARY.DEPLOYMENT_SURFACES
DEFAULT_REPOSITORY = BOUNDARY.DEFAULT_REPOSITORY
RELEASE_ACTION_TYPES = BOUNDARY.RELEASE_ACTION_TYPES
RELEASE_ENVIRONMENTS = BOUNDARY.RELEASE_ENVIRONMENTS
REPO_MUTATION_ACTION_TYPES = BOUNDARY.REPO_MUTATION_ACTION_TYPES
REPO_WRITE_PERMISSION = BOUNDARY.REPO_WRITE_PERMISSION
INTELLIGENCE_COMMIT_ACTION_TYPE = "INTELLIGENCE_COMMIT"
INTELLIGENCE_COMMIT_PERMISSION = "intelligence_commit"
INTELLIGENCE_COMMIT_TARGET = "NayaNET"
BOUNDARY_DECISION = BOUNDARY.BoundaryDecision
DEPLOY_TARGET = BOUNDARY.deploy_target
REPO_MUTATION_TARGET = BOUNDARY.repo_mutation_target


def _canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _parse_iso(value: Any) -> Tuple[Optional[datetime], bool]:
    if value is None or not str(value).strip():
        return None, True
    text = str(value).replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None, True
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed, False


def load_verifier_public_key() -> Optional[str]:
    """Return the pinned verifier public key (hex) if the human provisioned one."""
    if VERIFIER_PUBLIC_KEY_HEX:
        return VERIFIER_PUBLIC_KEY_HEX
    if not PIN_PATH.is_file():
        return None
    try:
        raw = PIN_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    text = raw.splitlines()[-1] if raw.splitlines() else ""
    if len(text) == 64 and all(ch in "0123456789abcdef" for ch in text.lower()):
        return text.lower()
    return None


def generate_keypair() -> Tuple[str, str]:
    """ISSUER-SIDE ONLY. Generates a fresh Ed25519 keypair (private hex, public hex).

    Private keys must never be stored in this repository or passed to a runner.
    The PUBLIC hex is the value that gets pinned for verifiers.
    """
    private_hex = os.urandom(32).hex()
    private_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_hex))
    public_hex = private_key.public_key().public_bytes_raw().hex()
    return private_hex, public_hex


def _sign(private_key_hex: str, message: bytes) -> str:
    private_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_key_hex))
    return private_key.sign(message).hex()


def _verify_signature(public_key_hex: str, message: bytes, signature_hex: str) -> bool:
    public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
    public_key.verify(bytes.fromhex(signature_hex), message)
    return True


def registry_revision(registry: Any) -> str:
    """Deterministic content hash of every registry grant (audit field only)."""
    grants = []
    for aid in sorted(registry.authorities):
        authority = registry.authorities[aid]
        grants.append([
            authority.authority_id,
            authority.principal_id,
            authority.purpose,
            authority.scope,
            sorted(authority.granted_actions),
            authority.expires_at,
            bool(authority.revoked),
        ])
    return hashlib.sha256(_canonical_json(grants).encode("utf-8")).hexdigest()


def _context_fields(artifact_authorization: Mapping[str, Any]) -> Tuple[str, str, frozenset, str, str]:
    repository = str(artifact_authorization.get("repository", ""))
    commit_sha = str(artifact_authorization.get("commit_sha", ""))
    change_set = frozenset(str(item) for item in artifact_authorization.get("change_set", []) or [])
    environment = str(artifact_authorization.get("environment", ""))
    deployment_surface = str(artifact_authorization.get("deployment_surface", ""))
    return repository, commit_sha, change_set, environment, deployment_surface


def issue_portable_authorization(
    *,
    execution_authorization: Any,
    registry: Any,
    gate: Any,
    commit_sha: str,
    private_key_hex: str,
    repository: str = DEFAULT_REPOSITORY,
    change_set: Iterable[str] = (),
    environment: str = "",
    deployment_surface: str = "",
    worker_name: Optional[str] = None,
    project_id: Optional[str] = None,
    now: Optional[str] = None,
    expires_in_seconds: int = DEFAULT_EXPIRES_IN_SECONDS,
) -> dict[str, Any]:
    """Sign a gate-issued ExecutionAuthorization into a portable artifact.

    Requires the credential to be bound to the EXACT canonical target for the
    provided context (release or mutation), with the exact permission/action_type.
    The signature is over the canonical JSON of the whole authorization object.
    """
    issued_at = now or datetime.now(timezone.utc).isoformat()
    parsed, bad = _parse_iso(issued_at)
    if bad or parsed is None:
        raise ValueError("issued_at must be a valid ISO timestamp")
    if execution_authorization is None:
        raise ValueError("a gate-issued ExecutionAuthorization is required")
    if gate is None:
        raise ValueError("the UniversalExecutionGate that issued the authorization is required")
    gate_ok, gate_reasons = gate.verify(execution_authorization, now=issued_at)
    if not gate_ok:
        raise ValueError("execution authorization was not issued by the supplied UniversalExecutionGate: " + "; ".join(gate_reasons))
    if execution_authorization.governance_state != GovernanceState.AUTHORIZED.value:
        raise ValueError("execution authorization is not AUTHORIZED")
    if int(expires_in_seconds) <= 0 or int(expires_in_seconds) > MAX_ARTIFACT_TTL_MINUTES * 60:
        raise ValueError("expires_in_seconds must be within the artifact TTL policy")

    expected_hash = _BINDING_HASH(
        execution_authorization.authority_id,
        execution_authorization.decision_id,
        execution_authorization.action_id,
        execution_authorization.action_type,
        execution_authorization.target,
        execution_authorization.actor_id,
        execution_authorization.scope,
        execution_authorization.permission,
    )
    if expected_hash != execution_authorization.binding_hash:
        raise ValueError("execution authorization binding_hash is inconsistent with its fields")

    authority = registry.resolve(execution_authorization.authority_id)
    if authority is None:
        raise ValueError("authority_id is not present in the canonical registry")
    authority_fingerprint = _GRANT_FINGERPRINT(authority)

    action_type = execution_authorization.action_type
    if action_type in REPO_MUTATION_ACTION_TYPES:
        paths = sorted(str(item) for item in change_set)
        if not paths:
            raise ValueError("change_set is required for a repository-mutation artifact")
        expected_target = REPO_MUTATION_TARGET(repository=repository, target_paths=paths)
        if execution_authorization.target != expected_target:
            raise ValueError("credential is not bound to this exact change-set")
        if execution_authorization.permission != REPO_WRITE_PERMISSION:
            raise ValueError("repo-mutation artifact requires the repo_write permission")
        environment = deployment_surface = ""
    elif action_type == INTELLIGENCE_COMMIT_ACTION_TYPE:
        if commit_sha == "":
            raise ValueError("intelligence-commit artifact requires the exact source commit SHA")
        if execution_authorization.target != INTELLIGENCE_COMMIT_TARGET:
            raise ValueError("credential is not bound to the canonical NayaNET intelligence target")
        if execution_authorization.permission != INTELLIGENCE_COMMIT_PERMISSION:
            raise ValueError("intelligence-commit artifact requires the intelligence_commit permission")
        paths = []
        environment = deployment_surface = ""
    elif action_type in RELEASE_ACTION_TYPES:
        if environment not in RELEASE_ENVIRONMENTS:
            raise ValueError("release artifact requires preview or production environment")
        if deployment_surface not in DEPLOYMENT_SURFACES:
            raise ValueError("release artifact requires cloudflare or vercel surface")
        if not commit_sha or not isinstance(commit_sha, str):
            raise ValueError("release artifact requires the exact commit SHA")
        paths = []
        expected_target = DEPLOY_TARGET(
            deployment_surface=deployment_surface,
            environment=environment,
            repository=repository,
            commit_sha=commit_sha,
            worker_name=worker_name,
            project_id=project_id,
        )
        if execution_authorization.target != expected_target:
            raise ValueError("credential is not bound to this exact deploy target")
        if execution_authorization.permission != DEPLOY_PERMISSION:
            raise ValueError("release artifact requires the deploy_public_runtime permission")
    else:
        raise ValueError(f"action_type {action_type!r} is not a portable release or mutation action")

    expires_at = (parsed + timedelta(seconds=int(expires_in_seconds))).isoformat()
    authorization = {
        "authority_id": execution_authorization.authority_id,
        "decision_id": execution_authorization.decision_id,
        "action_id": execution_authorization.action_id,
        "action_type": action_type,
        "target": execution_authorization.target,
        "actor_id": execution_authorization.actor_id,
        "scope": execution_authorization.scope,
        "permission": execution_authorization.permission,
        "governance_state": GovernanceState.AUTHORIZED.value,
        "risk_tier": execution_authorization.risk_tier,
        "validated_at": execution_authorization.validated_at,
        "binding_hash": execution_authorization.binding_hash,
        "repository": repository,
        "commit_sha": commit_sha,
        "change_set": paths,
        "environment": environment,
        "deployment_surface": deployment_surface,
        "worker_name": str(worker_name or ""),
        "project_id": str(project_id or ""),
        "issued_at": issued_at,
        "expires_at": expires_at,
        "authority_fingerprint": authority_fingerprint,
        "registry_revision": registry_revision(registry),
    }
    message = _canonical_json(authorization).encode("utf-8")
    return {
        "schema": SCHEMA,
        "authorization": authorization,
        "signature": _sign(private_key_hex, message),
    }


def verify_portable_authorization(
    *,
    artifact: Any,
    public_key_hex: str,
    registry: Any,
    now: Optional[str] = None,
) -> Tuple[bool, Tuple[str, ...]]:
    """Independent, stateless verification (no issuer memory required).

    A fresh process that has NEVER seen the issuer's `_issued` set can fully
    verify provenance here: Ed25519 signature over the canonical artifact +
    binding-hash recomputation + current registry authority-of-record checks.
    """
    reasons: list[str] = []
    now_iso = now or datetime.now(timezone.utc).isoformat()
    if Ed25519PublicKey is None:
        return False, ("cryptography library is unavailable to the verifier",)
    if isinstance(artifact, dict):
        pass
    elif isinstance(artifact, str):
        try:
            artifact = json.loads(artifact)
        except json.JSONDecodeError:
            return False, ("artifact is not valid JSON",)
    else:
        return False, ("artifact is not a portable authorization",)

    if artifact.get("schema") != SCHEMA:
        return False, (f"unsupported portable authorization schema {artifact.get('schema')!r}",)
    authorization = artifact.get("authorization")
    signature = artifact.get("signature")
    if not isinstance(authorization, dict) or not isinstance(signature, str):
        return False, ("portable authorization is missing its authorization or signature",)

    try:
        _verify_signature(public_key_hex, _canonical_json(authorization).encode("utf-8"), signature)
    except (ValueError, InvalidSignature, TypeError):
        return False, ("signature verification failed",)

    sources = {
        "authority_id": authorization.get("authority_id"),
        "decision_id": authorization.get("decision_id"),
        "action_id": authorization.get("action_id"),
        "action_type": authorization.get("action_type"),
        "target": authorization.get("target"),
        "actor_id": authorization.get("actor_id"),
        "scope": authorization.get("scope"),
        "permission": authorization.get("permission"),
    }
    if any(not str(value) for value in sources.values()):
        reasons.append("portable authorization missing identity fields")
    else:
        expected_hash = _BINDING_HASH(
            str(sources["authority_id"]),
            str(sources["decision_id"]),
            str(sources["action_id"]),
            str(sources["action_type"]),
            str(sources["target"]),
            str(sources["actor_id"]),
            str(sources["scope"]),
            str(sources["permission"]),
        )
        if expected_hash != authorization.get("binding_hash"):
            reasons.append("binding_hash does not match authorization fields")

    if authorization.get("governance_state") != GovernanceState.AUTHORIZED.value:
        reasons.append("governance_state is not AUTHORIZED")

    issued_at, bad_issued = _parse_iso(authorization.get("issued_at"))
    expires_at, bad_expires = _parse_iso(authorization.get("expires_at"))
    validated_at, bad_validated = _parse_iso(authorization.get("validated_at"))
    current, bad_now = _parse_iso(now_iso)
    if any((bad_issued, bad_expires, bad_validated)) or current is None:
        reasons.append("artifact timelines are invalid")
    elif bad_now:
        reasons.append("now is not a valid ISO timestamp")
    else:
        assert issued_at is not None and expires_at is not None and validated_at is not None and current is not None
        if validated_at != issued_at:
            reasons.append("validated_at does not match issued_at")
        if current < issued_at:
            reasons.append("artifact is not yet valid")
        if current >= expires_at:
            reasons.append("artifact has expired")
        if (expires_at - issued_at) > timedelta(minutes=MAX_ARTIFACT_TTL_MINUTES):
            reasons.append("artifact TTL exceeds the configured maximum")

    if "validated_at" in authorization and authorization.get("validated_at"):
        _, invalid = _parse_iso(authorization["validated_at"])
        if invalid:
            reasons.append("validated_at is not a valid ISO timestamp")

    resolved = registry.resolve(str(authorization.get("authority_id", "")))
    if resolved is None:
        reasons.append("authority_id is not present in the canonical registry")
    else:
        fingerprint_ok = True
        try:
            fingerprint_ok = _GRANT_FINGERPRINT(resolved) == authorization.get("authority_fingerprint")
        except Exception:
            fingerprint_ok = False
        if not fingerprint_ok:
            reasons.append("canonical grant was modified or revoked after issuance (fingerprint mismatch)")
        current_permits = True
        try:
            current_permits = resolved.permits(
                actor_id=str(authorization.get("actor_id", "")),
                action=str(authorization.get("permission", "")),
                scope=str(authorization.get("scope", "")),
                now=now_iso,
            )
        except Exception:
            current_permits = False
        if not current_permits:
            reasons.append("authority no longer permits this actor/action/scope at time of use")

    return (not reasons), tuple(dict.fromkeys(reasons))


def portable_boundary_release(
    *,
    artifact: Any,
    public_key_hex: str,
    registry: Any,
    commit_sha: str,
    target_environment: str,
    deployment_surface: str,
    repository: str = DEFAULT_REPOSITORY,
    worker_name: Optional[str] = None,
    project_id: Optional[str] = None,
    now: Optional[str] = None,
) -> BoundaryDecision:
    """Runner-side release boundary: portable verify + EXACT target binding."""
    if target_environment not in RELEASE_ENVIRONMENTS:
        return BOUNDARY_DECISION(False, "target environment must be preview or production")
    if deployment_surface not in DEPLOYMENT_SURFACES:
        return BOUNDARY_DECISION(False, "deployment surface must be cloudflare or vercel")
    if not isinstance(commit_sha, str) or not commit_sha:
        return BOUNDARY_DECISION(False, "exact commit SHA is required")
    if not repository:
        return BOUNDARY_DECISION(False, "repository binding is required")

    ok, reasons = verify_portable_authorization(
        artifact=artifact, public_key_hex=public_key_hex, registry=registry, now=now,
    )
    if not ok:
        return BOUNDARY_DECISION(False, "portable verification failed: " + "; ".join(reasons))
    authorization = artifact["authorization"]

    expected_target = DEPLOY_TARGET(
        deployment_surface=deployment_surface,
        environment=target_environment,
        repository=repository,
        commit_sha=commit_sha,
        worker_name=worker_name,
        project_id=project_id,
    )
    if authorization.get("target") != expected_target:
        return BOUNDARY_DECISION(
            False,
            "portable credential was not issued for this exact deploy target "
            f"(expected {expected_target!r})",
        )
    if authorization.get("action_type") not in RELEASE_ACTION_TYPES:
        return BOUNDARY_DECISION(
            False,
            f"artifact action_type {authorization.get('action_type')!r} is not a release action",
        )
    if authorization.get("permission") != DEPLOY_PERMISSION:
        return BOUNDARY_DECISION(
            False,
            f"artifact permission {authorization.get('permission')!r} is not {DEPLOY_PERMISSION!r}",
        )
    return BOUNDARY_DECISION(
        True,
        "release authorized by a valid gate-issued portable authorization bound to the exact target",
        approval_required_for=expected_target,
    )


def portable_boundary_repo_mutation(
    *,
    artifact: Any,
    public_key_hex: str,
    registry: Any,
    target_paths: Iterable[str],
    repository: str = DEFAULT_REPOSITORY,
    now: Optional[str] = None,
) -> BoundaryDecision:
    """Runner-side repository-mutation boundary: portable verify + EXACT change-set."""
    if not repository:
        return BOUNDARY_DECISION(False, "repository binding is required")

    ok, reasons = verify_portable_authorization(
        artifact=artifact, public_key_hex=public_key_hex, registry=registry, now=now,
    )
    if not ok:
        return BOUNDARY_DECISION(False, "portable verification failed: " + "; ".join(reasons))
    authorization = artifact["authorization"]

    expected_target = REPO_MUTATION_TARGET(repository=repository, target_paths=target_paths)
    if authorization.get("target") != expected_target:
        return BOUNDARY_DECISION(
            False,
            "portable credential was not issued for this exact change-set "
            f"(expected {expected_target!r})",
        )
    embedded = frozenset(str(item) for item in authorization.get("change_set", []) or [])
    requested = frozenset(str(item) for item in target_paths)
    if embedded != requested:
        return BOUNDARY_DECISION(
            False,
            f"portable credential change-set {sorted(embedded)} does not match "
            f"requested change-set {sorted(requested)}",
        )
    if authorization.get("action_type") not in REPO_MUTATION_ACTION_TYPES:
        return BOUNDARY_DECISION(
            False,
            f"artifact action_type {authorization.get('action_type')!r} is not a mutation action",
        )
    if authorization.get("permission") != REPO_WRITE_PERMISSION:
        return BOUNDARY_DECISION(
            False,
            f"artifact permission {authorization.get('permission')!r} is not {REPO_WRITE_PERMISSION!r}",
        )
    return BOUNDARY_DECISION(
        True,
        "repository mutation authorized by a valid gate-issued portable authorization "
        "bound to the exact change-set",
        approval_required_for=expected_target,
    )


def default_registry_path() -> Path:
    return _REGISTRY_PATH


__all__ = [
    "SCHEMA",
    "MAX_ARTIFACT_TTL_MINUTES",
    "DEFAULT_EXPIRES_IN_SECONDS",
    "VERIFIER_PUBLIC_KEY_HEX",
    "PIN_PATH",
    "GATE",
    "BOUNDARY",
    "BOUNDARY_DECISION",
    "DEPLOY_PERMISSION",
    "REPO_WRITE_PERMISSION",
    "INTELLIGENCE_COMMIT_ACTION_TYPE",
    "INTELLIGENCE_COMMIT_PERMISSION",
    "INTELLIGENCE_COMMIT_TARGET",
    "DEFAULT_REPOSITORY",
    "load_verifier_public_key",
    "generate_keypair",
    "registry_revision",
    "issue_portable_authorization",
    "verify_portable_authorization",
    "portable_boundary_release",
    "portable_boundary_repo_mutation",
    "default_registry_path",
]