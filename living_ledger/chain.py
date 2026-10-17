"""D51 hash-chain verifier.

Recomputes every link with the exact `nayanet_smart_ledger_hash`
construction and reports the first break with the event index and both
hashes. Works on event lists handed to it; performs zero database reads.

Canonical encoding (Python):
  sha256(owner_id|event_type|event_at|source_table|source_id|
         parent_ledger_event_id|previous_chain_hash|evidence_refs|metadata)
  - fields joined by "|", None renders as ""
  - evidence_refs / metadata render as compact JSON with sorted keys
  - event_at renders as ISO-8601 (datetimes are normalized to UTC first)

Postgres `::text` diverges (jsonb key ordering/spacing, timestamptz
`+00` rendering). `normalize_postgres_event()` converts a Postgres-shaped
row toward this canonical form; byte-parity with a live row is asserted
nowhere - that would require a live database read (human-only gate).
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

_HASH_FIELDS = (
    "owner_id",
    "event_type",
    "event_at",
    "source_table",
    "source_id",
    "parent_ledger_event_id",
    "previous_chain_hash",
    "evidence_refs",
    "metadata",
)


def _render_field(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    if isinstance(value, datetime):
        moment = value
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        return moment.astimezone(timezone.utc).isoformat()
    return str(value)


def canonical_event_hash(event: Mapping[str, Any]) -> str:
    """sha256 over the canonical encoding of the hash fields."""
    try:
        joined = "|".join(_render_field(event.get(name)) for name in _HASH_FIELDS)
    except (TypeError, ValueError) as exc:
        raise ValueError("event fields are not renderable: %s" % (exc,))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def normalize_postgres_event(row: Mapping[str, Any]) -> dict:
    """Normalize a Postgres-shaped ledger row toward the canonical form.

    Known divergences handled: timestamptz rendered with a space and `+00`
    suffix is converted to ISO-8601; jsonb text is re-parsed so key order
    and spacing no longer matter. Returns a new dict; the input is
    untouched. Divergences this does NOT cover are documented, not hidden:
    non-UTC timestamptz offsets are normalized to UTC (the DB stores an
    absolute instant; the canonical form names it in UTC).
    """
    normalized = dict(row)
    event_at = normalized.get("event_at")
    if isinstance(event_at, str):
        text = event_at.strip()
        # Postgres: "2026-10-11 10:50:28+00" -> ISO-8601.
        if " " in text and "T" not in text:
            head, _, tail = text.rpartition(" ")
            text = head + "T" + tail
            if text.endswith("+00"):
                text = text[:-3] + "+00:00"
        normalized["event_at"] = text
    for name in ("evidence_refs", "metadata"):
        value = normalized.get(name)
        if isinstance(value, str):
            try:
                normalized[name] = json.loads(value)
            except ValueError:
                pass  # leave as-is; the hash will simply not match
    return normalized


@dataclass(frozen=True)
class ChainVerdict:
    verdict: str  # CHAIN_VALID | HASH_MISMATCH | LINK_BROKEN |
                  # SEQ_REGRESSION | EMPTY_CHAIN
    index: int = -1
    expected: str = ""
    actual: str = ""
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.verdict == "CHAIN_VALID"


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return int(value.strip())
    return None


def verify_chain(events: Sequence[Mapping[str, Any]]) -> ChainVerdict:
    """Verify a ledger event list, oldest first.

    Checks, in order per event: the stored `event_hash` recomputes;
    `previous_chain_hash` equals the predecessor's `event_hash`
    (genesis: empty/None exactly once, at index 0); `chain_seq`
    strictly increases when present on both neighbors.
    The first break is reported with index and both hashes.
    """
    items = list(events)
    if not items:
        return ChainVerdict(verdict="EMPTY_CHAIN", detail="no events to verify")
    previous_hash: str | None = None
    previous_seq: int | None = None
    for index, event in enumerate(items):
        if not isinstance(event, Mapping):
            return ChainVerdict(
                verdict="HASH_MISMATCH", index=index,
                detail="event is not a mapping",
            )
        stored = event.get("event_hash")
        if not isinstance(stored, str) or not stored:
            return ChainVerdict(
                verdict="HASH_MISMATCH", index=index,
                detail="missing event_hash",
            )
        try:
            expected = canonical_event_hash(event)
        except ValueError as exc:
            return ChainVerdict(
                verdict="HASH_MISMATCH", index=index, actual=stored,
                detail=str(exc),
            )
        if expected != stored:
            return ChainVerdict(
                verdict="HASH_MISMATCH", index=index,
                expected=expected, actual=stored,
                detail="stored event_hash does not recompute",
            )
        link = event.get("previous_chain_hash")
        link_text = "" if link is None else str(link)
        if index == 0:
            if link_text != "":
                return ChainVerdict(
                    verdict="LINK_BROKEN", index=index,
                    expected="", actual=link_text,
                    detail="genesis event must not point at a predecessor",
                )
        else:
            if previous_hash is None or link_text != previous_hash:
                return ChainVerdict(
                    verdict="LINK_BROKEN", index=index,
                    expected=previous_hash or "", actual=link_text,
                    detail="previous_chain_hash does not match predecessor",
                )
        seq = _as_int(event.get("chain_seq"))
        if seq is not None and previous_seq is not None and seq <= previous_seq:
            return ChainVerdict(
                verdict="SEQ_REGRESSION", index=index,
                detail="chain_seq %r does not increase after %r"
                       % (seq, previous_seq),
            )
        previous_hash = stored
        if seq is not None:
            previous_seq = seq
    return ChainVerdict(
        verdict="CHAIN_VALID",
        detail="all %d event(s) verified" % (len(items),),
    )
