"""Production authority-grant -> canonical Authority adapter.

The production grant UUID is the authority-of-record. This module does not
mint authority; it deterministically translates a live DB grant into the
existing canonical Authority model consumed by UniversalExecutionGate.
"""
from __future__ import annotations

import json
from pathlib import Path
import importlib.util
from typing import Any, Mapping


_KERNEL_PATH = Path(__file__).resolve().parents[1] / "governance" / "governance_kernel.py"
_spec = importlib.util.spec_from_file_location("naya_production_authority_kernel", _KERNEL_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError("canonical governance kernel cannot be loaded")
_kernel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_kernel)

Authority = _kernel.Authority
AuthorityRegistry = _kernel.AuthorityRegistry


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def production_grant_to_authority(grant: Mapping[str, Any]) -> Authority:
    required = ("grant_id", "subject_id", "mission_id", "scope", "actions", "status")
    missing = [key for key in required if grant.get(key) in (None, "")]
    if missing:
        raise ValueError("production authority grant missing required fields: " + ", ".join(missing))
    if str(grant["status"]) not in {"ISSUED", "ACTIVE"}:
        raise ValueError("production authority grant is not active")
    actions = frozenset(str(item) for item in (grant.get("actions") or []))
    if not actions:
        raise ValueError("production authority grant has no actions")
    scope = grant["scope"]
    if not isinstance(scope, Mapping):
        raise ValueError("production authority grant scope must be an object")
    return Authority(
        authority_id=str(grant["grant_id"]),
        principal_id=str(grant["subject_id"]),
        purpose=str(grant["mission_id"]),
        scope=_canonical_json(scope),
        granted_actions=actions,
        expires_at=grant.get("expires_at"),
        revoked=str(grant.get("status")) == "REVOKED",
    )


def production_registry_from_grant(grant: Mapping[str, Any]) -> AuthorityRegistry:
    authority = production_grant_to_authority(grant)
    return AuthorityRegistry(authorities={authority.authority_id: authority})
