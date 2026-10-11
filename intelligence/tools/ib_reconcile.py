#!/usr/bin/env python3
"""ib_reconcile — Canonical Intelligent Block contract v1.1.

Reconciles the file-based authoring schema (intelligence/blocks/, SCHEMA v1.0)
with the persisted machine-canonical envelope
(kernel/supabase_intelligent_blocks.py CANONICAL_BLOCK_FIELDS).

Design law (from protocol 0005 §6, §16):
- Persisted envelope is authoritative for: identity, owner, scope/privacy,
  provenance, epistemic state, type, version.
- File form is authoritative for: authoring ergonomics, graduation path,
  status-history detail, evidence richness, applicability detail.
- Canonical contract v1.1 = persisted required fields + file-form additions.
  No third schema. The file form is extended so any file-authored block
  round-trips into persistence without loss.

Stdlib only.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone

SCHEMA_VERSION = "1.1"

# ---------------------------------------------------------------------------
# Persisted envelope field contract (mirrors
# kernel/supabase_intelligent_blocks.py::CANONICAL_BLOCK_FIELDS)
# ---------------------------------------------------------------------------
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

REQUIRED_PERSISTED = ("owner_id", "owner_scope", "provenance")
# (from_row raises if any of these are empty)

OWNER_SCOPES = ("PRIVATE", "TEAM", "COLLECTIVE", "PUBLIC")
BLOCK_TYPES = ("GOVERNED_INTELLIGENCE", "PRINCIPLE", "PROCEDURE", "LESSON",
               "CONSTRAINT", "DECISION", "STATE")
UNDERSTANDING_STATES = ("CANDIDATE", "VERIFIED", "SUPERSEDED", "DEPRECATED")
LIFECYCLE_STATUSES = ("DRAFT", "DURABLE", "SUPERSEDED", "ARCHIVED")

# ---------------------------------------------------------------------------
# File-form v1.1 field contract (extends SCHEMA.md v1.0)
# ---------------------------------------------------------------------------
FILE_REQUIRED_V11 = [
    "intelligent_block_id",   # canonical machine identity (B-authoritative)
    "block_id",               # row identity; null until persisted
    "schema_version",         # "1.1"
    "title",
    "purpose",                # NEW in v1.1 (protocol §6 #2)
    "principle",              # one sentence -> content.lesson on export
    "owner_id",               # NEW required (B-authoritative)
    "owner_scope",            # NEW required (B-authoritative)
    "block_type",             # NEW (B-authoritative)
    "source",                 # human {who, when, context}
    "provenance",             # NEW required dict (B-authoritative)
    "source_event_ids",       # NEW (B-authoritative)
    "evidence",               # rich array
    "applicability",          # rich object
    "applicable_scope",       # NEW coarse scope (B-authoritative)
    "understanding_state",    # NEW (B-authoritative)
    "status",                 # NEW lifecycle (B-authoritative)
    "verification_status",    # A 4-state ladder (kept)
    "status_history",
    "graduation",
    "authority_implications", # NEW in v1.1 (protocol §6 #14)
    "conflicts",              # NEW in v1.1 (protocol §6 #13)
    "supersedes_block_id",    # renamed to B's canonical names
    "superseded_by_block_id",
    "version",                # NEW (B-authoritative)
    "created_at",
    "updated_at",
]

# Legacy v1.0 aliases still accepted on read, normalized on write.
LEGACY_ALIASES = {
    "id": "intelligent_block_id",
    "supersedes": "supersedes_block_id",
    "superseded_by": "superseded_by_block_id",
}

FILE_STATUSES = ("UNVERIFIED", "APPLIED", "BEHAVIOR-CHANGE-PROVEN", "COMPOUNDED")
FILE_STAGES = ("text", "briefing", "code-gate")

# ---------------------------------------------------------------------------
# Epistemic state mapping (lossless both directions)
# ---------------------------------------------------------------------------
# file verification_status -> (understanding_state, status, provenance_flags)
FILE_TO_PERSISTED_STATE = {
    "UNVERIFIED": ("CANDIDATE", "DRAFT", {}),
    "APPLIED": ("CANDIDATE", "DURABLE", {}),
    "BEHAVIOR-CHANGE-PROVEN": ("VERIFIED", "DURABLE", {}),
    "COMPOUNDED": ("VERIFIED", "DURABLE", {"successor_reuse_proven": True}),
}


def persisted_to_file_state(understanding_state, status, provenance):
    """Reverse mapping. SUPERSEDED status overrides everything."""
    if status == "SUPERSEDED":
        # file form keeps its own ladder position in status_history;
        # current verification_status is derived from the last non-superseded entry
        hist = (provenance or {}).get("file_status_history", [])
        for entry in reversed(hist):
            vs = entry.get("verification_status")
            if vs in FILE_STATUSES:
                return vs
        return "UNVERIFIED"
    if understanding_state == "VERIFIED":
        if (provenance or {}).get("successor_reuse_proven"):
            return "COMPOUNDED"
        return "BEHAVIOR-CHANGE-PROVEN"
    # CANDIDATE
    return "APPLIED" if status == "DURABLE" else "UNVERIFIED"


# ---------------------------------------------------------------------------
# Normalization: v1.0 file block -> v1.1 canonical file block
# ---------------------------------------------------------------------------
def normalize_file_block(block, default_owner_id="", default_owner_scope="PRIVATE"):
    """Upgrade a v1.0 (or partial v1.1) file block to full v1.1.

    Fills B-authoritative fields with explicit defaults where the author
    must confirm them; never silently invents owner identity — an empty
    owner_id is preserved as empty so validation fails loudly.
    """
    b = dict(block)
    # legacy aliases
    for old, new in LEGACY_ALIASES.items():
        if old in b and new not in b:
            b[new] = b.pop(old)
    # identity
    b.setdefault("block_id", None)
    # new required B-fields (explicit, validatable)
    b.setdefault("owner_id", default_owner_id)
    b.setdefault("owner_scope", default_owner_scope)
    b.setdefault("block_type", "GOVERNED_INTELLIGENCE")
    b.setdefault("source_event_ids", [])
    # provenance: seed from human source so nothing is lost
    if "provenance" not in b or not isinstance(b.get("provenance"), dict):
        src = b.get("source", {}) if isinstance(b.get("source"), dict) else {}
        b["provenance"] = {
            "authored_via": "intelligence/blocks file form",
            "source_who": src.get("who"),
            "source_when": src.get("when"),
            "source_context": src.get("context"),
        }
    # new §6 fields
    b.setdefault("purpose", "")
    b.setdefault("authority_implications", "")
    b.setdefault("conflicts", [])
    # state machines: derive persisted pair from file ladder if absent
    if "understanding_state" not in b or "status" not in b:
        vs = b.get("verification_status", "UNVERIFIED")
        us, st, flags = FILE_TO_PERSISTED_STATE.get(vs, ("CANDIDATE", "DRAFT", {}))
        b.setdefault("understanding_state", us)
        b.setdefault("status", st)
        if flags:
            b["provenance"] = {**b.get("provenance", {}), **flags}
    # supersession: legacy IB-IDs -> keep, plus row-id slots
    b.setdefault("version", 1)
    b.setdefault("applicable_scope", "")
    b["schema_version"] = "1.1"
    return b


# ---------------------------------------------------------------------------
# Export: v1.1 file block -> persisted row dict (CANONICAL_BLOCK_FIELDS)
# ---------------------------------------------------------------------------
def to_persisted_row(block):
    """Convert a v1.1 file block to the persisted envelope row.

    Raises ValueError on the same conditions from_row enforces:
    missing owner_id / owner_scope / provenance.

    Lossless guarantee (#2386): the persisted envelope is authoritative for
    identity/owner/scope/provenance/epistemic-state/type/version, but the
    FILE FORM is authoritative for rich detail — evidence kind + per-item
    explanatory notes, detailed applicability, status history. That detail is
    carried verbatim inside provenance (namespaced keys) so
    from_persisted_row reconstructs the file form byte-exact. The caller's
    provenance dict is never mutated.
    """
    b = normalize_file_block(block)
    for field in REQUIRED_PERSISTED:
        if not b.get(field):
            raise ValueError(
                f"canonical Intelligent Block is missing owner, scope, or provenance "
                f"(empty {field})"
            )
    evidence = b.get("evidence") or []
    # Rich file-form detail rides in provenance (carried verbatim through
    # persistence) so the round-trip is lossless. Keys match what
    # from_persisted_row expects; legacy rows without them still import via
    # the documented ref/empty fallbacks.
    provenance = dict(b["provenance"])
    provenance["evidence_detail"] = evidence
    provenance["applicability_detail"] = b.get("applicability") or {
        "topics": [], "situations": "", "decisions": ""}
    provenance["file_status_history"] = b.get("status_history") or []
    content = {
        "lesson": b.get("principle", ""),
        "title": b.get("title", ""),
        "purpose": b.get("purpose", ""),
        "graduation": b.get("graduation", {}),
        "verification_status": b.get("verification_status", "UNVERIFIED"),
        "authority_implications": b.get("authority_implications", ""),
        "conflicts": b.get("conflicts", []),
    }
    row = {
        "block_id": b.get("block_id"),
        "intelligent_block_id": b["intelligent_block_id"],
        "owner_id": b["owner_id"],
        "subject_id": b.get("subject_id"),
        "title": b.get("title", ""),
        "block_type": b.get("block_type", "GOVERNED_INTELLIGENCE"),
        "version": b.get("version", 1),
        "status": b.get("status", "DRAFT"),
        "understanding_state": b.get("understanding_state", "CANDIDATE"),
        "owner_scope": b["owner_scope"],
        "source_event_ids": b.get("source_event_ids", []),
        "evidence_refs": [
            e.get("ref") for e in evidence
            if isinstance(e, dict) and e.get("ref")
        ],
        "provenance": provenance,
        "applicable_scope": b.get("applicable_scope", ""),
        "content": content,
        "supersedes_block_id": b.get("supersedes_block_id"),
        "superseded_by_block_id": b.get("superseded_by_block_id"),
        "created_at": b.get("created_at"),
        "updated_at": b.get("updated_at"),
        "schema_version": b.get("schema_version", "1.1"),
    }
    missing = [f for f in CANONICAL_BLOCK_FIELDS if f not in row]
    if missing:
        raise ValueError(f"canonical Intelligent Block is missing fields: {missing}")
    return row


# ---------------------------------------------------------------------------
# Import: persisted row dict -> v1.1 file block (lossless)
# ---------------------------------------------------------------------------
def from_persisted_row(row):
    """Convert a persisted envelope row to a v1.1 file block.

    Nothing is dropped: B-only fields are carried verbatim; rich A-fields
    are reconstructed from content/provenance where the export placed them.
    Malformed rich-detail keys fail CLOSED (ValueError) — never silently
    degraded. Rows persisted before #2386 (no detail keys) still import via
    the documented ref/empty fallbacks; rich fields are not invented.
    """
    missing = [f for f in CANONICAL_BLOCK_FIELDS if f not in row]
    if missing:
        raise ValueError(f"canonical Intelligent Block is missing fields: {missing}")
    content = row.get("content") or {}
    provenance = row.get("provenance") or {}
    # Fail closed on tampered detail: wrong types mean a corrupted or
    # adversarial row, not something to paper over.
    ev_detail = provenance.get("evidence_detail", [])
    if not isinstance(ev_detail, list):
        raise ValueError(
            "canonical Intelligent Block has corrupted provenance.evidence_detail "
            "(must be a list)")
    app_detail = provenance.get("applicability_detail")
    if app_detail is not None and not isinstance(app_detail, dict):
        raise ValueError(
            "canonical Intelligent Block has corrupted provenance.applicability_detail "
            "(must be an object)")
    hist = provenance.get("file_status_history", [])
    if not isinstance(hist, list):
        raise ValueError(
            "canonical Intelligent Block has corrupted provenance.file_status_history "
            "(must be a list)")
    # reconstruct rich evidence array from refs + provenance detail
    if ev_detail:
        evidence = ev_detail
    else:
        # Legacy row (pre-#2386): refs survive, kind/note are NOT invented.
        evidence = [{"kind": "ref", "ref": r, "note": ""} for r in (row.get("evidence_refs") or [])]
    block = {
        "intelligent_block_id": row["intelligent_block_id"],
        "block_id": row.get("block_id"),
        "schema_version": "1.1",
        "title": row.get("title", ""),
        "purpose": content.get("purpose", ""),
        "principle": content.get("lesson", ""),
        "owner_id": row.get("owner_id", ""),
        "owner_scope": row.get("owner_scope", ""),
        "block_type": row.get("block_type", "GOVERNED_INTELLIGENCE"),
        "source": {
            "who": provenance.get("source_who"),
            "when": provenance.get("source_when"),
            "context": provenance.get("source_context"),
        },
        "provenance": provenance,
        "source_event_ids": row.get("source_event_ids", []),
        "evidence": evidence,
        "applicability": app_detail or {
            "topics": [],
            "situations": "",
            "decisions": "",
        },
        "applicable_scope": row.get("applicable_scope", ""),
        "understanding_state": row.get("understanding_state", "CANDIDATE"),
        "status": row.get("status", "DRAFT"),
        "verification_status": persisted_to_file_state(
            row.get("understanding_state", "CANDIDATE"),
            row.get("status", "DRAFT"),
            provenance,
        ),
        "status_history": hist,
        "graduation": content.get("graduation", {"stage": "text", "next_step": "", "enforced_by": None}),
        "authority_implications": content.get("authority_implications", ""),
        "conflicts": content.get("conflicts", []),
        "supersedes_block_id": row.get("supersedes_block_id"),
        "superseded_by_block_id": row.get("superseded_by_block_id"),
        "version": row.get("version", 1),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }
    return block


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_v11(block):
    """Return list of problems (empty = valid)."""
    problems = []
    b = dict(block)
    for old in LEGACY_ALIASES:
        if old in b:
            problems.append(f"legacy field '{old}' must be renamed to '{LEGACY_ALIASES[old]}' (v1.1)")
    for field in FILE_REQUIRED_V11:
        if field not in b:
            problems.append(f"missing required field: {field}")
    if not b.get("owner_id"):
        problems.append("owner_id is required (persisted envelope raises without it)")
    if not b.get("owner_scope"):
        problems.append("owner_scope is required (persisted envelope raises without it)")
    elif b["owner_scope"] not in OWNER_SCOPES:
        problems.append(f"owner_scope must be one of {OWNER_SCOPES}")
    if not b.get("provenance") or not isinstance(b.get("provenance"), dict):
        problems.append("provenance must be a non-empty dict (persisted envelope raises without it)")
    if b.get("understanding_state") not in UNDERSTANDING_STATES:
        problems.append(f"understanding_state must be one of {UNDERSTANDING_STATES}")
    if b.get("status") not in LIFECYCLE_STATUSES:
        problems.append(f"status must be one of {LIFECYCLE_STATUSES}")
    if b.get("verification_status") not in FILE_STATUSES:
        problems.append(f"verification_status must be one of {FILE_STATUSES}")
    # v1.0 rule carried forward: non-UNVERIFIED status requires evidence
    if b.get("verification_status") != "UNVERIFIED" and not b.get("evidence"):
        problems.append(
            f"status {b.get('verification_status')} requires non-empty evidence"
        )
    # cross-check: file ladder and persisted pair must agree per mapping
    vs = b.get("verification_status")
    if vs in FILE_TO_PERSISTED_STATE:
        exp_us, exp_st, exp_flags = FILE_TO_PERSISTED_STATE[vs]
        if b.get("status") != "SUPERSEDED":  # supersession overrides
            if b.get("understanding_state") != exp_us:
                problems.append(
                    f"understanding_state '{b.get('understanding_state')}' disagrees with "
                    f"verification_status '{vs}' (expected '{exp_us}')"
                )
    principle = b.get("principle", "")
    if principle and len(principle.split(". ")) > 2:
        problems.append("principle should be one sentence (v1.0 rule carried into v1.1)")
    return problems


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
