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

# Rich-detail provenance keys the exporter stamps (t922, #2386).
DETAIL_KEYS = ("evidence_detail", "applicability_detail", "file_status_history")
# Honest marker for fallback-derived detail (t982 legacy-row re-export heal).
# Meaning: "the emitted rich-detail keys were populated from ref-only
# fallback content, not from authored rich detail." Absent on modern rows.
DETAIL_SOURCE_KEY = "detail_source"
LEGACY_FALLBACK = "legacy-fallback"


def _is_ref_only(evidence):
    """True when every evidence entry carries nothing but a ref.

    This is exactly the shape from_persisted_row produces for legacy rows
    (kind "ref", empty note) — i.e. content equivalent to a pre-#2386 row,
    with no authored kind/note detail to preserve.
    """
    return all(
        isinstance(e, dict) and e.get("kind") == "ref" and not e.get("note")
        for e in (evidence or [])
    )

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
        # gap-t922 (c): history entries carry the DOCUMENTED shape
        # {"status", "at", "note"} (SCHEMA.md; written by ib.py create/promote
        # and seed_blocks) where "status" IS the verification-ladder value.
        # The "verification_status" key is accepted first for forward
        # compatibility, but no writer emits it — reading only that key made
        # this branch dead code that always returned UNVERIFIED. A "status"
        # that is not a ladder rung (lifecycle word, junk) is skipped: the
        # path degrades, never invents.
        hist = (provenance or {}).get("file_status_history", [])
        for entry in reversed(hist):
            vs = entry.get("verification_status")
            if vs not in FILE_STATUSES:
                vs = entry.get("status")
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

    Legacy-row re-export heal (t982): when the rich-detail keys were NOT in
    the source block's provenance AND the evidence is ref-only fallback
    content, the emitted detail is reconstructed, not authored — it is
    marked provenance["detail_source"] = "legacy-fallback" so no consumer
    mistakes it for authored rich detail. Modern rows (keys present) get no
    marker; a marker already present is carried verbatim, never recomputed.
    Hand-authored rich detail on first export is never mislabeled.
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
    src_provenance = b.get("provenance") or {}
    provenance = dict(src_provenance)
    provenance["evidence_detail"] = evidence
    provenance["applicability_detail"] = b.get("applicability") or {
        "topics": [], "situations": "", "decisions": ""}
    provenance["file_status_history"] = b.get("status_history") or []
    if DETAIL_SOURCE_KEY not in src_provenance:
        if (not all(k in src_provenance for k in DETAIL_KEYS)
                and _is_ref_only(evidence)):
            provenance[DETAIL_SOURCE_KEY] = LEGACY_FALLBACK
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
    A non-string provenance.detail_source also fails closed.
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
    detail_source = provenance.get(DETAIL_SOURCE_KEY)
    if detail_source is not None and not isinstance(detail_source, str):
        raise ValueError(
            "canonical Intelligent Block has corrupted provenance.detail_source "
            "(must be a string)")
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


# ---------------------------------------------------------------------------
# System ownership — Shawn's locked decision (2026-10-11 ~22:34Z)
# ---------------------------------------------------------------------------
# "Naya is locking that in for owner." Naya — the collective system — owns the
# 20 seed Intelligent Blocks and all future blocks. No per-block human owner:
# a per-block owner recreates the bottleneck the system exists to remove.
# Operational authority flows through the verification/promotion gates of
# OWNERSHIP_AUTHORITY_PATH below — executable checks, not prose. Each gate is
# a real function exercised by tests (positive + negative); the path is the
# machine-readable record of HOW Naya exercises ownership.
OWNER_NAYA = "NAYA"

SYSTEM_OWNERSHIP_DECISION = {
    "owner_id": OWNER_NAYA,
    "decided_by": "Shawn",
    "decided_at": "2026-10-11T22:34:00+00:00",
    "decision": (
        "Naya (the collective system) owns the 20 seed Intelligent Blocks and "
        "all future blocks. No per-block human owner (bottleneck). Operational "
        "authority flows through the system's verification/promotion gates."
    ),
    "recorded_in": "intelligence/tools/ib_reconcile.py (this module)",
}


def validate_system_owned(block):
    """Seed-corpus ownership rule. Returns a problem string, or None if clean.

    Every block authored under intelligence/blocks/ is system-owned: owner_id
    must be exactly OWNER_NAYA. Empty fails loudly (never invent, never leave
    pending); any other value fails as a per-block-owner bottleneck.
    """
    owner = (block or {}).get("owner_id")
    if not owner:
        return (
            "owner_id is empty: system-owned blocks must declare "
            f"owner_id='{OWNER_NAYA}' (never invent, never leave pending)"
        )
    if owner != OWNER_NAYA:
        return (
            f"owner_id '{owner}' is a per-block owner: only '{OWNER_NAYA}' may own "
            "seed-corpus blocks (Shawn 2026-10-11 — per-block owners are bottlenecks)"
        )
    return None


# ---------------------------------------------------------------------------
# Ownership authority path — how Naya (the system) exercises ownership
# ---------------------------------------------------------------------------
# Each entry: (gate_name, check_function, what_it_exercises).
# A check takes (block, ctx=None) and returns None (pass) or a problem string.
# ctx carries cross-file state the check needs, e.g. {"registry": REGISTRY.json}.
def check_ownership_locked(block, ctx=None):
    "Gate 1: the block declares the system as its owner, exactly."
    return validate_system_owned(block)


def check_envelope_identity(block, ctx=None):
    "Gate 2: the block round-trips through the persisted envelope with owner + identity intact."
    try:
        row = to_persisted_row(block)
        back = from_persisted_row(row)
    except ValueError as e:
        return f"envelope round-trip raised: {e}"
    if back.get("owner_id") != OWNER_NAYA:
        return f"round-trip lost system owner: {back.get('owner_id')!r}"
    if back.get("intelligent_block_id") != block.get("intelligent_block_id"):
        return "round-trip lost block identity"
    return None


def check_epistemic_consistency(block, ctx=None):
    "Gate 3: verification_status ladder position agrees with understanding_state + status."
    vs = block.get("verification_status")
    if vs not in FILE_TO_PERSISTED_STATE:
        return f"verification_status {vs!r} is not on the ladder"
    if block.get("status") == "SUPERSEDED":
        return None  # supersession overrides the mapping
    exp_us, exp_st, _ = FILE_TO_PERSISTED_STATE[vs]
    if block.get("understanding_state") != exp_us:
        return (
            f"understanding_state {block.get('understanding_state')!r} disagrees with "
            f"verification_status {vs!r} (expected {exp_us!r})"
        )
    if block.get("status") != exp_st:
        return (
            f"status {block.get('status')!r} disagrees with "
            f"verification_status {vs!r} (expected {exp_st!r})"
        )
    return None


def check_ladder_evidence(block, ctx=None):
    "Gate 4: any ladder rung above UNVERIFIED is backed by evidence (receipts, not claims)."
    if block.get("verification_status") != "UNVERIFIED" and not block.get("evidence"):
        return "verification ladder requires non-empty evidence above UNVERIFIED"
    return None


def check_graduation(block, ctx=None):
    "Gate 5: the block sits on the text->briefing->code-gate path; code-gate names its enforcer."
    g = block.get("graduation") or {}
    stage = g.get("stage")
    if stage not in FILE_STAGES:
        return f"graduation.stage {stage!r} not in {FILE_STAGES}"
    if stage == "code-gate" and not g.get("enforced_by"):
        return "code-gate graduation claims must name enforced_by"
    return None


def check_registry_consistency(block, ctx=None):
    "Gate 6: REGISTRY.json indexes the block with matching state and the system owner."
    reg = (ctx or {}).get("registry") or {}
    entries = {e.get("id"): e for e in reg.get("blocks", [])}
    bid = block.get("intelligent_block_id") or block.get("id")
    entry = entries.get(bid)
    if entry is None:
        return f"block {bid!r} missing from REGISTRY.json"
    if entry.get("title") != block.get("title"):
        return f"registry title {entry.get('title')!r} != block {block.get('title')!r}"
    if entry.get("verification_status") != block.get("verification_status"):
        return "registry verification_status disagrees with block"
    if entry.get("graduation_stage") != (block.get("graduation") or {}).get("stage"):
        return "registry graduation_stage disagrees with block"
    if entry.get("owner_id") != OWNER_NAYA:
        return f"registry owner_id {entry.get('owner_id')!r} != '{OWNER_NAYA}'"
    return None


OWNERSHIP_AUTHORITY_PATH = (
    ("ownership-locked", check_ownership_locked,
     "owner_id is exactly NAYA — the system owns the block; no per-block human owner"),
    ("envelope-identity", check_envelope_identity,
     "file block round-trips through the persisted envelope with owner + identity intact"),
    ("epistemic-consistency", check_epistemic_consistency,
     "verification_status ladder position agrees with understanding_state + status"),
    ("verification-ladder-evidence", check_ladder_evidence,
     "any rung above UNVERIFIED is backed by evidence"),
    ("graduation-path", check_graduation,
     "block sits on the text->briefing->code-gate path; code-gate names its enforcer"),
    ("registry-integrity", check_registry_consistency,
     "REGISTRY.json indexes the block with matching state and the system owner"),
)


def run_authority_path(block, ctx=None):
    """Exercise the full ownership authority path.

    Returns [(gate_name, problem_or_None), ...]. All None = the system
    exercises ownership cleanly through every gate.
    """
    return [(name, check(block, ctx)) for name, check, _ in OWNERSHIP_AUTHORITY_PATH]
