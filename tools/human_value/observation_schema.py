"""Observed-human-experience schema v2 — extends the Human Value schema v1.

The core distinction (see the design doc
`hidden_files/human-value/observed-experience-instrument-v1.md`):

    Seat-graded value is a hypothesis. Observed human experience is the
    evidence. The instrument only credits evidence.

Schema v2 = schema v1 fields + the observer/evidence seam:
`observation_kind`, `subject`, `observed_by`, `observed_at`, `collected_at`,
`verbatim_hash`, `authorship`, `collector_inference`, `promotion`, `supersedes`.

Validation FAILS CLOSED on: unknown/missing evidence, `authorship: uncertain`
with a promotion, assessor == builder (or collector), self-observation without
a direct human statement, CORRECTED events not typed `attention_demanded`,
bad verbatim hashes, `collected_at` before `observed_at`, and unknown fields.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Mapping, Sequence

from tools.human_value.schema import (
    BENEFICIARIES,
    EVIDENCE_KINDS,
    OPTIONAL_FIELDS as V1_OPTIONAL_FIELDS,
    REQUIRED_FIELDS as V1_REQUIRED_FIELDS,
    SCHEMA_VERSION as V1_SCHEMA_VERSION,
    VALUE_TYPES,
    SchemaError,
    validate_event as validate_v1_event,
    validate_evidence as validate_v1_evidence,
)

SCHEMA_V2_VERSION = "2"

OBSERVATION_KINDS = (
    "stated",    # the human's own words assert the experience (verbatim quote)
    "revealed",  # the human's action demonstrates the experience (counted acts)
    "corrected", # the human overrode/corrected/rejected system output (negative)
)

AUTHORSHIP = (
    "direct",     # authorship is mechanically grounded (API, verbatim quote, marker)
    "inferred",   # collector inferred authorship; labeled, review surface only
    "uncertain",  # cannot attribute; FAILS CLOSED — no promotion, ever
)

# v1: Shawn, the director, is the only human in the loop. Other humans are v2+.
SUBJECTS = ("human_self",)

CHANNELS = ("c1", "c2", "c3")  # team feeds / direct messages / repo actions

OBSERVATORY_PATH_HINTS = (
    "tools/human_value/",
    "observation",
    "observe.py",
    "observation_schema.py",
)

REQUIRED_V2_FIELDS = (
    "observation_kind",
    "subject",
    "observed_by",
    "observed_at",
    "collected_at",
    "verbatim_hash",
    "authorship",
    "collector_inference",
    "promotion",  # candidate_id string, or null for a standalone observation
)

OPTIONAL_V2_FIELDS = (
    "supersedes",          # event_id of a prior event this CORRECTED event amends
    "observatory_subject", # bool: the observed artifact IS the observatory
)

ALL_V2_FIELDS = (
    tuple(V1_REQUIRED_FIELDS)
    + tuple(V1_OPTIONAL_FIELDS)
    + tuple(REQUIRED_V2_FIELDS)
    + tuple(OPTIONAL_V2_FIELDS)
)

VERBATIM_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

# ---------------------------------------------------------------------------
# candidates (pending-candidates.jsonl)
# ---------------------------------------------------------------------------

CANDIDATE_REQUIRED = (
    "candidate_id",
    "graded_value_type",
    "graded_units",
    "graded_by",
    "graded_at",
    "expires_at",
    "status",
)

CANDIDATE_OPTIONAL = (
    "schema_version",
    "pr",
    "capability",   # capability tag for capability-level matching (design §2.3)
    "built_by",
    "note",
    "decision_id",
)

CANDIDATE_STATUSES = ("pending", "promoted", "unobserved")

# ---------------------------------------------------------------------------
# sweeps (observation-sweeps.jsonl)
# ---------------------------------------------------------------------------

SWEEP_REQUIRED = (
    "sweep_id",
    "swept_at",
    "watermark_start",
    "watermark_end",
    "channels",
    "observations_found",
    "promotions_proposed",
    "null_sweep",
    "collector",
)

SWEEP_OPTIONAL = ("note",)


def _check_no_unknown(raw: Mapping[str, Any], allowed: Sequence[str], what: str) -> None:
    unknown = [k for k in raw if k not in allowed]
    if unknown:
        raise SchemaError(f"{what}: unknown field(s) {unknown} — fail closed")


def _parse_ts(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise SchemaError(f"{field}: must be a non-empty ISO-8601 string")
    text = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        raise SchemaError(f"{field}: not parseable as ISO-8601: {value!r}")


def looks_like_self_observation(evidence: Sequence[Mapping[str, Any]]) -> bool:
    """Heuristic: does any evidence pointer target the observatory itself?"""
    for item in evidence or []:
        ref = str(item.get("ref", ""))
        if any(hint in ref for hint in OBSERVATORY_PATH_HINTS):
            return True
    return False


def validate_candidate(raw: Any) -> dict:
    """Validate one pending-candidate record. Fail closed."""
    if not isinstance(raw, Mapping):
        raise SchemaError("candidate: must be a JSON object")
    _check_no_unknown(raw, CANDIDATE_REQUIRED + CANDIDATE_OPTIONAL, "candidate")
    missing = [k for k in CANDIDATE_REQUIRED if k not in raw]
    if missing:
        raise SchemaError(f"candidate: missing required field(s) {missing}")
    if raw.get("schema_version", V1_SCHEMA_VERSION) != V1_SCHEMA_VERSION:
        raise SchemaError("candidate: schema_version must be '1'")
    if raw["graded_value_type"] not in VALUE_TYPES:
        raise SchemaError(f"candidate: unknown graded_value_type {raw['graded_value_type']!r}")
    if not isinstance(raw["graded_units"], (int, float)) or not (raw["graded_units"] > 0):
        raise SchemaError("candidate: graded_units must be a positive number (a prior, not a measurement)")
    if not str(raw["candidate_id"]).strip():
        raise SchemaError("candidate: candidate_id must be non-empty")
    if raw["status"] not in CANDIDATE_STATUSES:
        raise SchemaError(f"candidate: unknown status {raw['status']!r}")
    _parse_ts(raw["graded_at"], "candidate.graded_at")
    _parse_ts(raw["expires_at"], "candidate.expires_at")
    return dict(raw)


def validate_sweep(raw: Any) -> dict:
    """Validate one observation-sweep record (the NULL sweep log). Fail closed."""
    if not isinstance(raw, Mapping):
        raise SchemaError("sweep: must be a JSON object")
    _check_no_unknown(raw, SWEEP_REQUIRED + SWEEP_OPTIONAL, "sweep")
    missing = [k for k in SWEEP_REQUIRED if k not in raw]
    if missing:
        raise SchemaError(f"sweep: missing required field(s) {missing}")
    channels = raw["channels"]
    if not isinstance(channels, list) or not channels or any(c not in CHANNELS for c in channels):
        raise SchemaError("sweep: channels must be a non-empty list of c1/c2/c3")
    if not isinstance(raw["observations_found"], int) or raw["observations_found"] < 0:
        raise SchemaError("sweep: observations_found must be a non-negative int")
    if not isinstance(raw["promotions_proposed"], int) or raw["promotions_proposed"] < 0:
        raise SchemaError("sweep: promotions_proposed must be a non-negative int")
    if not isinstance(raw["null_sweep"], bool):
        raise SchemaError("sweep: null_sweep must be a bool")
    if raw["null_sweep"] and raw["observations_found"] != 0:
        raise SchemaError("sweep: null_sweep=true requires observations_found=0")
    _parse_ts(raw["swept_at"], "sweep.swept_at")
    _parse_ts(raw["watermark_start"], "sweep.watermark_start")
    _parse_ts(raw["watermark_end"], "sweep.watermark_end")
    return dict(raw)


def validate_event_v2(raw: Any, candidate: Mapping[str, Any] | None = None) -> dict:
    """Validate one observed-experience event (schema v2). Fail closed.

    `candidate`: the matched candidate record (or None for a standalone
    observation). When given, enforces assessor != builder != collector at
    promote time.
    """
    if not isinstance(raw, Mapping):
        raise SchemaError("event: must be a JSON object")
    _check_no_unknown(raw, ALL_V2_FIELDS, "event")

    if raw.get("schema_version") != SCHEMA_V2_VERSION:
        raise SchemaError("event: schema_version must be '2'")

    # Units are counts of observed things, never ratings. Check the RAW value
    # before the v1 seam normalizes numbers to float.
    raw_units = raw.get("value_units")
    if isinstance(raw_units, bool) or not isinstance(raw_units, int) or raw_units < 1:
        raise SchemaError("event: value_units must be an int >= 1 (counts of observed things, never ratings)")

    # v1 core first (evidence presence, value types, units explainability).
    # The v1 seam sees only v1 fields, with the v1 schema version asserted.
    v1_payload = {k: v for k, v in raw.items() if k in V1_REQUIRED_FIELDS + V1_OPTIONAL_FIELDS}
    v1_payload["schema_version"] = V1_SCHEMA_VERSION
    base = validate_v1_event(v1_payload)
    base["value_units"] = raw_units  # restore the int the v1 seam normalized away

    missing = [k for k in REQUIRED_V2_FIELDS if k not in raw]
    if missing:
        raise SchemaError(f"event: missing required v2 field(s) {missing}")

    kind = raw["observation_kind"]
    if kind not in OBSERVATION_KINDS:
        raise SchemaError(f"event: unknown observation_kind {kind!r}")

    if raw["subject"] not in SUBJECTS:
        raise SchemaError(f"event: unknown subject {raw['subject']!r} (v1 observes human_self only)")

    if not str(raw["observed_by"]).strip():
        raise SchemaError("event: observed_by (collector seat) must be non-empty")

    authorship = raw["authorship"]
    if authorship not in AUTHORSHIP:
        raise SchemaError(f"event: unknown authorship {authorship!r}")

    promotion = raw["promotion"]
    if promotion is not None and not str(promotion).strip():
        raise SchemaError("event: promotion must be a candidate_id string or null")
    # Fail closed: uncertain authorship can never promote.
    if authorship == "uncertain" and promotion is not None:
        raise SchemaError("event: authorship 'uncertain' cannot carry a promotion — fail closed")

    if not VERBATIM_HASH_RE.match(str(raw["verbatim_hash"])):
        raise SchemaError("event: verbatim_hash must look like 'sha256:<64 hex>'")

    if not str(raw["collector_inference"]).strip():
        raise SchemaError("event: collector_inference must be non-empty (inference is labeled, never hidden)")

    observed_at = _parse_ts(raw["observed_at"], "event.observed_at")
    collected_at = _parse_ts(raw["collected_at"], "event.collected_at")
    if collected_at < observed_at:
        raise SchemaError("event: collected_at cannot precede observed_at")

    value_type = base["value_type"]
    # CORRECTED is the negative observation class: it always measures
    # attention_demanded, and only it does. Mechanical, no judgment calls.
    if kind == "corrected" and value_type != "attention_demanded":
        raise SchemaError("event: observation_kind 'corrected' requires value_type 'attention_demanded'")
    if kind != "corrected" and value_type == "attention_demanded":
        raise SchemaError("event: value_type 'attention_demanded' requires observation_kind 'corrected'")

    units = base["value_units"]
    assert isinstance(units, int) and units >= 1  # guaranteed by the raw check above

    # Self-observation: the observatory's own activity is never evidence of
    # human value. The only exception is a DIRECT human statement about the
    # observatory (stated kind, direct authorship, verbatim preserved) backed
    # by a human-grounded evidence pointer — a bare receipt to an observatory
    # file is the collector asserting value for its own work, and fails closed.
    observatory_subject = bool(raw.get("observatory_subject", False)) or looks_like_self_observation(
        base["evidence"]
    )
    if observatory_subject:
        human_grounded = any(
            item.get("kind") in ("feed_comment", "content_hash", "smart_note", "url")
            for item in base["evidence"]
        )
        if not (authorship == "direct" and kind == "stated" and human_grounded):
            raise SchemaError(
                "event: self-observation requires a DIRECT human statement "
                "(authorship=direct, observation_kind=stated, human-grounded evidence) — fail closed"
            )

    supersedes = raw.get("supersedes")
    if supersedes is not None and not str(supersedes).strip():
        raise SchemaError("event: supersedes must be an event_id string or null")

    # Assessor != builder != collector (promote-time mechanical check).
    if candidate is not None:
        assessed_by = str(candidate.get("graded_by", "")).strip()
        built_by = str(candidate.get("built_by", "")).strip()
        collector = str(raw["observed_by"]).strip()
        if assessed_by and assessed_by == collector:
            raise SchemaError("promote: assessor (graded_by) == collector (observed_by) — fail closed")
        if built_by and built_by in (collector, assessed_by):
            raise SchemaError("promote: builder == collector or assessor — fail closed")

    event = dict(base)
    for field in REQUIRED_V2_FIELDS + OPTIONAL_V2_FIELDS:
        if field in raw:
            event[field] = raw[field]
    if "observatory_subject" not in event:
        event["observatory_subject"] = observatory_subject
    return event


def validate_observation_ledger(raw_events: Sequence[Any]) -> list[dict]:
    """Validate a full observed-events.jsonl ledger. Fail closed on any row."""
    return [validate_event_v2(e) for e in raw_events]


def project_to_schema(raw: Mapping[str, Any]) -> dict:
    """Project a collector's working observation onto the schema v2 fields.

    Collectors carry review-only fields (verbatim_quote for human review,
    fixture labels, artifact/pr match hints). The ledger carries only schema
    fields. Projection is explicit and logged — never silent acceptance of
    unknown fields at the signed promote step, which stays strict.
    """
    return {k: v for k, v in raw.items() if k in ALL_V2_FIELDS}


def fold_candidates(records: Sequence[Mapping[str, Any]]) -> dict[str, dict]:
    """Fold append-only candidate records to latest-status-per-candidate_id.

    The ledger is append-only: a promotion or expiry appends a status-update
    record; the latest record per candidate_id wins. Silent overwrite is
    impossible because every state change is a new line.
    """
    folded: dict[str, dict] = {}
    for rec in records:
        validated = validate_candidate(rec)
        folded[validated["candidate_id"]] = validated
    return folded


def expired_candidates(folded: Mapping[str, dict], as_of: str) -> list[str]:
    """Candidate ids that are pending and past expires_at as of `as_of`."""
    as_of_dt = _parse_ts(as_of, "as_of")
    expired = []
    for cid, cand in folded.items():
        if cand["status"] == "pending" and _parse_ts(cand["expires_at"], "expires_at") < as_of_dt:
            expired.append(cid)
    return sorted(expired)
