from dataclasses import dataclass
import json
import os
from typing import Any, Callable
from urllib.parse import quote
from urllib.request import Request, urlopen


CANONICAL_BLOCK_FIELDS = (
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
    "supersedes_block_id",
    "superseded_by_block_id",
    "created_at",
    "updated_at",
    "schema_version",
)


@dataclass(frozen=True)
class IntelligentBlock:
    block_id: str
    intelligent_block_id: str
    owner_id: str
    owner_scope: str
    provenance: dict[str, Any]
    epistemic_state: str
    data: dict[str, Any]

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "IntelligentBlock":
        missing = [field for field in CANONICAL_BLOCK_FIELDS if field not in row]
        if missing:
            raise ValueError(f"canonical Intelligent Block is missing fields: {missing}")
        if not row["owner_id"] or not row["owner_scope"] or not row["provenance"]:
            raise ValueError("canonical Intelligent Block is missing owner, scope, or provenance")

        return cls(
            block_id=row["block_id"],
            intelligent_block_id=row["intelligent_block_id"],
            owner_id=row["owner_id"],
            owner_scope=row["owner_scope"],
            provenance=row["provenance"],
            epistemic_state=row["understanding_state"],
            data={field: row[field] for field in CANONICAL_BLOCK_FIELDS},
        )


class SupabaseIntelligentBlockReader:
    """Read-only adapter for canonical Intelligent Block persistence.

    Supabase/RLS remains the authorization boundary. The adapter requires an
    access token, filters by owner_id, and performs no persistence writes.
    """

    def __init__(
        self,
        *,
        url: str | None = None,
        access_token: str | None = None,
        api_key: str | None = None,
        request: Callable[[Request], bytes] | None = None,
    ) -> None:
        self._url = (url or os.environ.get("SUPABASE_URL", "")).rstrip("/")
        self._access_token = access_token or os.environ.get(
            "SUPABASE_USER_ACCESS_TOKEN",
            os.environ.get("SUPABASE_ACCESS_TOKEN", ""),
        )
        self._api_key = api_key or os.environ.get(
            "SUPABASE_PUBLISHABLE_KEY",
            os.environ.get("SUPABASE_API_KEY", ""),
        )
        self._request = request or self._default_request

    @staticmethod
    def _default_request(request: Request) -> bytes:
        with urlopen(request, timeout=10) as response:
            return response.read()

    def get_by_intelligent_block_id(
        self, *, intelligent_block_id: str, owner_id: str
    ) -> IntelligentBlock | None:
        if not self._url or not self._access_token or not self._api_key:
            raise RuntimeError(
                "Supabase URL, user access token, and publishable/API key "
                "are required for persistence retrieval"
            )
        if not intelligent_block_id or not owner_id:
            raise ValueError("intelligent_block_id and owner_id are required")

        select = quote(",".join(CANONICAL_BLOCK_FIELDS), safe=",")
        block_id = quote(intelligent_block_id, safe="")
        owner = quote(owner_id, safe="")
        endpoint = (
            f"{self._url}/rest/v1/nayanet_intelligent_blocks"
            f"?select={select}&intelligent_block_id=eq.{block_id}&owner_id=eq.{owner}&limit=1"
        )
        request = Request(
            endpoint,
            headers={
                "Authorization": f"Bearer {self._access_token}",
                "apikey": self._api_key,
                "Accept": "application/json",
            },
            method="GET",
        )
        rows = json.loads(self._request(request))
        if not isinstance(rows, list):
            raise RuntimeError("Supabase Intelligent Block retrieval returned a non-list payload")
        if not rows:
            return None
        if len(rows) != 1:
            raise RuntimeError("canonical Intelligent Block lookup returned multiple rows")
        return IntelligentBlock.from_row(rows[0])
