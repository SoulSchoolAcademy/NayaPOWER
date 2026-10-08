"""Human Value event schema v1 — strict, fail-closed validation.

A measurement only exists if it can be recomputed by a cold successor from
canonical bytes. This schema is the contract between the recorder and every
future recomputation. Unknown fields, missing evidence, or malformed values
FAIL CLOSED: the event gets no credit and the run exits non-zero.
"""

from __future__ import annotations

from datetime import date
import math
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = "1"

VALUE_TYPES = (
    "cognitive_load_reduced",   # human attention/effort the system absorbed instead
    "rework_avoided",           # work that did not have to be redone
    "error_prevented",          # mistakes caught before they cost a human
    "useful_outcome",           # a human got something they actually wanted
    "attention_demanded",       # the human had to intervene (DAI input; trend target: DOWN)
)

EVIDENCE_KINDS = (
    "feed_comment",   # GitHub issue comment URL (the durable team feed)
    "smart_note",     # canonical smart-note id (IB-...)
    "receipt",        # repo-relative path to a receipt/artifact file
    "content_hash",   # "sha256:<hex>" pinning private bytes kept outside the repo
    "url",            # any other durable public URL
)

BENEFICIARIES = ("human_self", "human_other", "team", "public")

REQUIRED_FIELDS = (
    "schema_version",
    "event_id",
    "recorded_at",
    "value_type",
    "value_units",
    "unit_description",
    "evidence",
)

OPTIONAL_FIELDS = (
    "beneficiary",
    "decision_id",       # links to a value_calculus decision receipt
    "delta_v_actual",    # observed outcome in calculus scale [-10, 10]
    "note",
)

ALLOWED_FIELDS = frozenset(REQUIRED_FIELDS + OPTIONAL_FIELDS)


class SchemaError(ValueError):
    """A single schema violation. The event gets no credit."""


def _is_finite_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def validate_evidence(evidence: Any, event_id: str) -> list[dict]:
    if not isinstance(evidence, list) or not evidence:
        raise SchemaError(f"{event_id}: 'evidence' must be a non-empty list "
                          f"(no evidence = no credit)")
    out = []
    for i, item in enumerate(evidence):
        if not isinstance(item, Mapping):
            raise SchemaError(f"{event_id}: evidence[{i}] must be an object")
        kind = item.get("kind")
        ref = item.get("ref")
        if kind not in EVIDENCE_KINDS:
            raise SchemaError(f"{event_id}: evidence[{i}].kind must be one of "
                              f"{list(EVIDENCE_KINDS)}")
        if not isinstance(ref, str) or not ref.strip():
            raise SchemaError(f"{event_id}: evidence[{i}].ref must be a non-empty string")
        if kind == "content_hash" and not ref.startswith("sha256:"):
            raise SchemaError(f"{event_id}: evidence[{i}].ref for content_hash "
                              f"must look like 'sha256:<hex>'")
        extra = set(item.keys()) - {"kind", "ref"}
        if extra:
            raise SchemaError(f"{event_id}: evidence[{i}] has unknown fields {sorted(extra)}")
        out.append({"kind": kind, "ref": ref})
    return out


def validate_event(raw: Any) -> dict:
    """Validate one event. Returns the normalized event or raises SchemaError."""
    if not isinstance(raw, Mapping):
        raise SchemaError("event must be a JSON object")
    event_id = raw.get("event_id", "<missing-id>")
    unknown = set(raw.keys()) - ALLOWED_FIELDS
    if unknown:
        raise SchemaError(f"{event_id}: unknown fields {sorted(unknown)} "
                          f"(strict schema v{SCHEMA_VERSION})")
    for field in REQUIRED_FIELDS:
        if field not in raw:
            raise SchemaError(f"{event_id}: missing required field '{field}'")
    if raw["schema_version"] != SCHEMA_VERSION:
        raise SchemaError(f"{event_id}: schema_version must be {SCHEMA_VERSION!r}")
    if not isinstance(event_id, str) or not event_id.strip():
        raise SchemaError("<missing-id>: event_id must be a non-empty string")
    try:
        recorded = date.fromisoformat(raw["recorded_at"])
    except (ValueError, TypeError):
        raise SchemaError(f"{event_id}: recorded_at must be YYYY-MM-DD")
    if raw["value_type"] not in VALUE_TYPES:
        raise SchemaError(f"{event_id}: value_type must be one of {list(VALUE_TYPES)}")
    units = raw["value_units"]
    if not _is_finite_number(units) or units < 0:
        raise SchemaError(f"{event_id}: value_units must be a finite number >= 0")
    if not isinstance(raw["unit_description"], str) or not raw["unit_description"].strip():
        raise SchemaError(f"{event_id}: unit_description must be a non-empty string")
    evidence = validate_evidence(raw["evidence"], event_id)

    event: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "recorded_at": recorded.isoformat(),
        "value_type": raw["value_type"],
        "value_units": float(units),
        "unit_description": raw["unit_description"].strip(),
        "evidence": evidence,
    }
    if "beneficiary" in raw:
        if raw["beneficiary"] not in BENEFICIARIES:
            raise SchemaError(f"{event_id}: beneficiary must be one of {list(BENEFICIARIES)}")
        event["beneficiary"] = raw["beneficiary"]
    if "decision_id" in raw:
        if not isinstance(raw["decision_id"], str) or not raw["decision_id"].strip():
            raise SchemaError(f"{event_id}: decision_id must be a non-empty string")
        event["decision_id"] = raw["decision_id"]
    if "delta_v_actual" in raw:
        actual = raw["delta_v_actual"]
        if not _is_finite_number(actual) or not -10.0 <= actual <= 10.0:
            raise SchemaError(f"{event_id}: delta_v_actual must be within [-10, 10]")
        event["delta_v_actual"] = float(actual)
    if "note" in raw:
        if not isinstance(raw["note"], str):
            raise SchemaError(f"{event_id}: note must be a string")
        event["note"] = raw["note"]
    return event


def validate_ledger(raw_events: Sequence[Any]) -> list[dict]:
    """Validate a full ledger. Raises SchemaError on the first violation.

    Duplicate event_ids fail closed — the whole ledger is rejected, because a
    recomputation cannot tell which copy the original measurement counted.
    """
    events = [validate_event(raw) for raw in raw_events]
    seen: dict[str, int] = {}
    for i, e in enumerate(events):
        if e["event_id"] in seen:
            raise SchemaError(f"duplicate event_id {e['event_id']!r} "
                              f"(lines {seen[e['event_id']]} and {i})")
        seen[e["event_id"]] = i
    return events
