"""Owner-scoped, read-only access to canonical NayaNET intelligence.

The runtime intentionally uses an authenticated user access token. A service-role
credential is never accepted as the identity used for retrieval.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class CanonicalMemoryError(RuntimeError):
    """Raised when canonical retrieval cannot safely establish intelligence."""


@dataclass(frozen=True)
class HttpResponse:
    status: int
    body: Any


class HttpTransport(Protocol):
    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: Any | None = None,
    ) -> HttpResponse: ...


class UrllibTransport:
    """Minimal standard-library HTTPS transport for the runtime boundary."""

    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: Any | None = None,
    ) -> HttpResponse:
        payload = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(url, data=payload, method=method, headers=headers)
        try:
            with urlopen(request, timeout=20) as response:
                raw = response.read().decode("utf-8")
                return HttpResponse(response.status, json.loads(raw) if raw else None)
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                parsed = raw
            return HttpResponse(exc.code, parsed)
        except URLError as exc:
            raise CanonicalMemoryError(f"canonical retrieval transport failure: {exc}") from exc


@dataclass(frozen=True)
class CanonicalMemoryConfiguration:
    supabase_url: str
    anon_key: str
    access_token: str

    def __post_init__(self) -> None:
        for name, value in (
            ("supabase_url", self.supabase_url),
            ("anon_key", self.anon_key),
            ("access_token", self.access_token),
        ):
            if not isinstance(value, str) or not value.strip():
                raise CanonicalMemoryError(f"{name} is required")
        if self.access_token.strip() == self.anon_key.strip():
            raise CanonicalMemoryError(
                "access token must be an authenticated user token, not the publishable/anon key"
            )

    @classmethod
    def from_environment(cls) -> "CanonicalMemoryConfiguration":
        supabase_url = os.getenv("NAYAPOWER_SUPABASE_URL") or os.getenv("SUPABASE_URL") or ""
        anon_key = os.getenv("NAYAPOWER_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_ANON_KEY") or ""
        access_token = (
            os.getenv("NAYAPOWER_ACCESS_TOKEN")
            or os.getenv("NAYA_ACCESS_TOKEN")
            or ""
        )
        return cls(
            supabase_url=supabase_url,
            anon_key=anon_key,
            access_token=access_token,
        )


@dataclass(frozen=True)
@dataclass(frozen=True)
class RetrievedRelationship:
    """Validated owner-scoped graph relationship used only as retrieval context."""

    relationship_id: str
    source_id: str
    target_id: str
    relationship_type: str
    provenance: dict[str, Any]
    epistemic_state: str

    @classmethod
    def from_payload(cls, payload: Any) -> "RetrievedRelationship":
        if not isinstance(payload, dict):
            raise CanonicalMemoryError("canonical relationship returned a non-object payload")
        required = (
            "relationship_id",
            "source_id",
            "target_id",
            "relationship_type",
            "provenance",
            "epistemic_state",
        )
        missing = [field for field in required if field not in payload]
        if missing:
            raise CanonicalMemoryError(
                f"canonical relationship missing required fields: {', '.join(missing)}"
            )
        for field in required[:4] + ("epistemic_state",):
            if not str(payload[field]).strip():
                raise CanonicalMemoryError(
                    f"canonical relationship {field} must be non-empty"
                )
        if not isinstance(payload["provenance"], dict) or not payload["provenance"]:
            raise CanonicalMemoryError(
                "canonical relationship provenance must be a non-empty object"
            )
        return cls(
            relationship_id=str(payload["relationship_id"]),
            source_id=str(payload["source_id"]),
            target_id=str(payload["target_id"]),
            relationship_type=str(payload["relationship_type"]),
            provenance=payload["provenance"],
            epistemic_state=str(payload["epistemic_state"]),
        )

    def is_verified_support_for(self, block_id: str) -> bool:
        return (
            self.target_id == block_id
            and self.relationship_type == "VERIFIED_BY"
            and self.epistemic_state == "VERIFIED"
            and bool(self.provenance)
        )


class RetrievedIntelligentBlock:
    """Validated machine view of a canonical persisted Intelligent Block."""

    block_id: str
    intelligent_block_id: str
    owner_id: str
    subject_id: str
    title: str
    block_type: str
    version: int
    status: str
    understanding_state: str
    owner_scope: str
    source_event_ids: tuple[str, ...]
    evidence_refs: tuple[Any, ...]
    provenance: dict[str, Any]
    applicable_scope: dict[str, Any]
    content: dict[str, Any]
    schema_version: str

    @classmethod
    def from_payload(cls, payload: Any) -> "RetrievedIntelligentBlock":
        if isinstance(payload, list):
            if len(payload) != 1:
                raise CanonicalMemoryError(
                    f"canonical retrieval returned {len(payload)} rows; expected exactly one"
                )
            payload = payload[0]
        if not isinstance(payload, dict):
            raise CanonicalMemoryError("canonical retrieval returned a non-object payload")

        required = (
            "block_id",
            "intelligent_block_id",
            "owner_id",
            "subject_id",
            "title",
            "block_type",
            "version",
            "status",
            "understanding_state",
            "owner_scope",
            "source_event_ids",
            "evidence_refs",
            "provenance",
            "applicable_scope",
            "content",
            "schema_version",
        )
        missing = [field for field in required if field not in payload]
        if missing:
            raise CanonicalMemoryError(
                f"canonical Intelligent Block missing required fields: {', '.join(missing)}"
            )

        status = str(payload["status"])
        if status in {"DELETED", "SUPERSEDED"}:
            raise CanonicalMemoryError(
                f"canonical Intelligent Block status {status} is not live"
            )

        try:
            version = int(payload["version"])
        except (TypeError, ValueError) as exc:
            raise CanonicalMemoryError("canonical Intelligent Block version is invalid") from exc
        if version <= 0:
            raise CanonicalMemoryError("canonical Intelligent Block version must be positive")

        source_event_ids = payload["source_event_ids"]
        if not isinstance(source_event_ids, list) or not source_event_ids:
            raise CanonicalMemoryError("canonical Intelligent Block source_event_ids are required")

        evidence_refs = payload["evidence_refs"]
        if not isinstance(evidence_refs, list):
            raise CanonicalMemoryError("canonical Intelligent Block evidence_refs must be an array")

        provenance = payload["provenance"]
        applicable_scope = payload["applicable_scope"]
        content = payload["content"]
        for name, value in (
            ("provenance", provenance),
            ("applicable_scope", applicable_scope),
            ("content", content),
        ):
            if not isinstance(value, dict) or not value:
                raise CanonicalMemoryError(
                    f"canonical Intelligent Block {name} must be a non-empty object"
                )

        for field in (
            "block_id",
            "intelligent_block_id",
            "owner_id",
            "subject_id",
            "schema_version",
        ):
            if not str(payload[field]).strip():
                raise CanonicalMemoryError(
                    f"canonical Intelligent Block {field} must be non-empty"
                )

        return cls(
            block_id=str(payload["block_id"]),
            intelligent_block_id=str(payload["intelligent_block_id"]),
            owner_id=str(payload["owner_id"]),
            subject_id=str(payload["subject_id"]),
            title=str(payload["title"]),
            block_type=str(payload["block_type"]),
            version=version,
            status=status,
            understanding_state=str(payload["understanding_state"]),
            owner_scope=str(payload["owner_scope"]),
            source_event_ids=tuple(str(value) for value in source_event_ids),
            evidence_refs=tuple(evidence_refs),
            provenance=provenance,
            applicable_scope=applicable_scope,
            content=content,
            schema_version=str(payload["schema_version"]),
        )

    def is_applicable_to(self, task_target: str | None) -> bool:
        if not task_target:
            return False
        target = self.applicable_scope.get("target")
        return target == task_target

    def evidence_key(self) -> str:
        return f"{self.intelligent_block_id}@v{self.version}"


class SupabaseCanonicalMemory:
    """Read-only canonical memory adapter using Supabase's owner-scoped RPC."""

    def __init__(
        self,
        configuration: CanonicalMemoryConfiguration,
        *,
        transport: HttpTransport | None = None,
    ) -> None:
        self.configuration = configuration
        self.transport = transport or UrllibTransport()

    def retrieve_relationships(self, intelligent_block_id: str) -> tuple[RetrievedRelationship, ...]:
        """Read owner-scoped relationships targeting one canonical block."""

        if not isinstance(intelligent_block_id, str) or not intelligent_block_id.strip():
            raise CanonicalMemoryError("intelligent_block_id is required")

        from urllib.parse import urlencode

        base = self.configuration.supabase_url.rstrip("/")
        params = urlencode(
            {
                "target_id": f"eq.{intelligent_block_id}",
                "select": "relationship_id,source_id,target_id,relationship_type,provenance,epistemic_state",
                "order": "created_at.asc",
            }
        )
        url = f"{base}/rest/v1/nayanet_brain_relationships?{params}"
        response = self.transport.request(
            "GET",
            url,
            headers={
                "apikey": self.configuration.anon_key,
                "Authorization": f"Bearer {self.configuration.access_token}",
                "Accept": "application/json",
            },
        )
        if response.status < 200 or response.status >= 300:
            detail = (
                response.body.get("message")
                if isinstance(response.body, dict)
                else response.body
            )
            raise CanonicalMemoryError(
                f"canonical relationship retrieval rejected ({response.status}): "
                f"{detail or 'unknown error'}"
            )
        if not isinstance(response.body, list):
            raise CanonicalMemoryError("canonical relationship retrieval returned a non-array payload")

        relationships = tuple(
            RetrievedRelationship.from_payload(payload)
            for payload in response.body
        )
        mismatched = [
            relationship.relationship_id
            for relationship in relationships
            if relationship.target_id != intelligent_block_id
        ]
        if mismatched:
            raise CanonicalMemoryError(
                "canonical relationship target mismatch: " + ",".join(mismatched)
            )
        return relationships


    def retrieve_block(self, block_id: str) -> RetrievedIntelligentBlock:
        if not isinstance(block_id, str) or not block_id.strip():
            raise CanonicalMemoryError("block_id is required")

        base = self.configuration.supabase_url.rstrip("/")
        url = f"{base}/rest/v1/rpc/nayanet_retrieve_intelligent_block"
        response = self.transport.request(
            "POST",
            url,
            headers={
                "apikey": self.configuration.anon_key,
                "Authorization": f"Bearer {self.configuration.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body={"p_block_id": block_id},
        )
        if response.status < 200 or response.status >= 300:
            detail = (
                response.body.get("message")
                if isinstance(response.body, dict)
                else response.body
            )
            raise CanonicalMemoryError(
                f"canonical retrieval rejected ({response.status}): {detail or 'unknown error'}"
            )
        return RetrievedIntelligentBlock.from_payload(response.body)
