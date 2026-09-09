"""Deterministic deny-by-default scope and permission enforcement.

This module is intentionally small and independent of retrieval ranking. Callers
must authorize a request before loading/ranking/delivering memory candidates.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping, Optional


class Access(str, Enum):
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"
    PUBLIC = "PUBLIC"


@dataclass(frozen=True)
class Principal:
    principal_id: str
    scope: Optional[str] = None
    project: Optional[str] = None
    grants: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class AuthorizationRequest:
    principal: Principal
    scope: Optional[str] = None
    project: Optional[str] = None


def _norm(value: Optional[str]) -> Optional[str]:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _permissions(event: Mapping) -> Mapping:
    value = event.get("permissions")
    return value if isinstance(value, Mapping) else {}


def access_class(event: Mapping) -> Optional[Access]:
    permissions = _permissions(event)
    if "access" not in permissions and "visibility" not in event:
        return None
    raw = permissions.get("access", event.get("visibility"))
    try:
        return Access(str(raw).upper())
    except (TypeError, ValueError):
        return None


def event_scope(event: Mapping) -> Optional[str]:
    permissions = _permissions(event)
    return _norm(permissions.get("scope", event.get("scope")))


def event_project(event: Mapping) -> Optional[str]:
    return _norm(event.get("project"))


def explicit_grants(event: Mapping) -> frozenset[str]:
    permissions = _permissions(event)
    grants = permissions.get("grants", event.get("authorized_principals", []))
    if isinstance(grants, str):
        grants = [grants]
    if not isinstance(grants, Iterable) or isinstance(grants, (bytes, Mapping)):
        return frozenset()
    return frozenset(str(x) for x in grants)


def authorize(request: AuthorizationRequest, event: Mapping) -> bool:
    """Return True only when the event is explicitly within authorized scope.

    Missing identity, requested scope, event scope, or permission information is
    denied. Public access is not a bypass for scope or project isolation.
    Cross-scope access requires an explicit ``scope:<scope>`` grant, while
    cross-project access requires an explicit project/principal grant.
    """
    principal = request.principal
    principal_id = _norm(principal.principal_id)
    requested_scope = _norm(request.scope) or _norm(principal.scope)
    requested_project = _norm(request.project) or _norm(principal.project)
    stored_scope = event_scope(event)
    stored_project = event_project(event)
    access = access_class(event)

    if not principal_id or not requested_scope or not stored_scope or not stored_project or access is None:
        return False

    grants = explicit_grants(event)
    same_scope = requested_scope == stored_scope
    same_project = bool(requested_project and requested_project == stored_project)
    principal_granted = principal_id in grants
    principal_scope_granted = f"scope:{stored_scope}" in principal.grants
    principal_project_granted = f"project:{stored_project}" in principal.grants
    event_scope_granted = f"scope:{requested_scope}" in grants
    event_project_granted = f"project:{requested_project}" in grants if requested_project else False

    explicit_scope_grant = principal_scope_granted or event_scope_granted
    explicit_project_grant = principal_project_granted or event_project_granted
    explicit_principal_grant = principal_granted

    scope_allowed = same_scope or explicit_scope_grant
    project_allowed = same_project or explicit_project_grant or explicit_principal_grant

    if access in (Access.PRIVATE, Access.SHARED, Access.PUBLIC):
        return scope_allowed and project_allowed

    return False


def filter_authorized(request: AuthorizationRequest, events: Iterable[Mapping]) -> list[Mapping]:
    """Filter candidates before ranking, relationship expansion, or context assembly."""
    return [event for event in events if authorize(request, event)]
