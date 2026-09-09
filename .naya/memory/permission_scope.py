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


def access_class(event: Mapping) -> Access:
    permissions = _permissions(event)
    raw = permissions.get("access", event.get("visibility", Access.PRIVATE.value))
    try:
        return Access(str(raw).upper())
    except ValueError:
        return Access.PRIVATE


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
    denied. Public access is still limited by explicit scope when an event has one.
    Cross-project access requires an explicit grant (or the principal's own project).
    """
    principal = request.principal
    principal_id = _norm(principal.principal_id)
    requested_scope = _norm(request.scope) or _norm(principal.scope)
    requested_project = _norm(request.project) or _norm(principal.project)
    stored_scope = event_scope(event)
    stored_project = event_project(event)

    if not principal_id or not requested_scope or not stored_scope:
        return False

    grants = explicit_grants(event)
    access = access_class(event)
    same_scope = requested_scope == stored_scope
    same_project = bool(requested_project and stored_project and requested_project == stored_project)
    principal_granted = principal_id in grants
    scope_granted = stored_scope in principal.grants
    project_granted = bool(stored_project and f"project:{stored_project}" in principal.grants)

    if access is Access.PRIVATE:
        return same_scope and (same_project or principal_granted or scope_granted or project_granted)

    if access is Access.SHARED:
        return same_scope and (same_project or principal_granted or scope_granted or project_granted)

    # PUBLIC is not a bypass for an explicit scope boundary.
    return same_scope or principal_granted or scope_granted or project_granted


def filter_authorized(request: AuthorizationRequest, events: Iterable[Mapping]) -> list[Mapping]:
    """Filter candidates before ranking/context assembly."""
    return [event for event in events if authorize(request, event)]
