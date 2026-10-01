"""Canonical owner-scoped Activation Context for NayaPOWER.

Issue #1264 establishes two supported activation entrances:
- FORK_FIRST (preferred)
- INDEPENDENT_BOOTSTRAP (supported alternative)

Both MUST converge into this same context before any owner-specific projection,
persistence, authority, learning, graph, or NayaNET operation.

This object is deliberately small. It carries identity/routing facts; it does
not create authority, mint credentials, or infer ownership.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Mapping, Any


_REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class ActivationMode(str, Enum):
    FORK_FIRST = "FORK_FIRST"
    INDEPENDENT_BOOTSTRAP = "INDEPENDENT_BOOTSTRAP"


@dataclass(frozen=True)
class ActivationContext:
    human_owner_id: str
    naya_id: str
    owner_repo: str
    upstream_repo: str
    tenant_project_id: str
    authority_context: Mapping[str, Any]
    persistence_context: Mapping[str, Any]
    network_scope: str
    mode: ActivationMode

    def validate(self) -> "ActivationContext":
        required = {
            "human_owner_id": self.human_owner_id,
            "naya_id": self.naya_id,
            "owner_repo": self.owner_repo,
            "upstream_repo": self.upstream_repo,
            "tenant_project_id": self.tenant_project_id,
            "network_scope": self.network_scope,
        }
        missing = [
            name
            for name, value in required.items()
            if not isinstance(value, str) or not value.strip()
        ]
        if missing:
            raise ValueError("ACTIVATION_CONTEXT_REQUIRED:" + ",".join(sorted(missing)))

        try:
            mode = self.mode if isinstance(self.mode, ActivationMode) else ActivationMode(self.mode)
        except (TypeError, ValueError):
            raise ValueError("ACTIVATION_MODE_INVALID") from None
        object.__setattr__(self, "mode", mode)

        if not _REPO_RE.fullmatch(self.owner_repo):
            raise ValueError("OWNER_REPO_INVALID")
        if not _REPO_RE.fullmatch(self.upstream_repo):
            raise ValueError("UPSTREAM_REPO_INVALID")
        if self.owner_repo.casefold() == self.upstream_repo.casefold():
            raise ValueError("OWNER_REPO_MUST_BE_DISTINCT_FROM_UPSTREAM")
        if not isinstance(self.authority_context, Mapping):
            raise ValueError("AUTHORITY_CONTEXT_INVALID")
        if not isinstance(self.persistence_context, Mapping):
            raise ValueError("PERSISTENCE_CONTEXT_INVALID")

        return self

    @property
    def repository_target(self) -> str:
        """The only repository owner-specific projections may target."""
        return self.owner_repo
