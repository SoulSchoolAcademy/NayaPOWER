#!/usr/bin/env python3
"""
Successor reconstruction contract — NAYANET_SUCCESSOR_RECONSTRUCTION_V1.

A cold successor must independently reconstruct 14 elements from authoritative
state only:
  WHO / WHAT / WHY / SUCCESS / CURRENT TRUTH / PROVEN / UNKNOWN /
  AUTHORITY / HISTORY / LEARNING / NEXT / PROOF / RECORD / CONTINUATION

This module is READ-side only. It does not write to any store.

It provides:
  1. SUCCESSOR_HANDOFF_V1 — the canonical schema for the `successor` payload
     written by nayanet_create_successor_handoff into
     nayanet_project_cognition_state.state. Until the writer populates it,
     the primary cold-restore surface cannot carry 7 of the 14 elements.
  2. audit(...) — gap matrix: element x structure x PRESENT/PARTIAL/MISSING.
  3. reconstruct(...) — builds the 14-element reconstruction with provenance.
  4. validate_handoff(...) — fail-closed schema check for handoff payloads.
  5. CLI — `python -m tools.successor_reconstruction --audit <json>`
     exits 0 when fully reconstructable, 1 with the gap report otherwise.

No second brain, no duplicate store. One contract, one checker.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

SCHEMA_VERSION = "NAYANET_SUCCESSOR_RECONSTRUCTION_V1"
HANDOFF_SCHEMA_VERSION = "NAYANET_SUCCESSOR_HANDOFF_V1"

ELEMENTS = [
    "who",
    "what",
    "why",
    "success",
    "current_truth",
    "proven",
    "unknown",
    "authority",
    "history",
    "learning",
    "next",
    "proof",
    "record",
    "continuation",
]

# ---------------------------------------------------------------------------
# Extraction rules.
#
# Each element maps to a list of (structure, json_path, strength) candidates,
# tried in order.  "strong" = the element is genuinely carried;
# "weak" = an opaque pointer or generic restatement exists but a cold
# successor cannot reconstruct the element from it alone.
#
# json_path uses dot notation into the supplied structure dicts.
# Structures: "cognition_state" (the state jsonb + row columns),
#             "checkpoint_receipt" (nayanet_checkpoint_receipts row),
#             "checkpoint_event" (NAYANET_INTELLIGENCE_CHECKPOINT_V1 event).
# ---------------------------------------------------------------------------
EXTRACTION_RULES: dict[str, list[tuple[str, str, str]]] = {
    "who": [
        ("cognition_state", "state.successor.director", "strong"),
        ("cognition_state", "user_id", "weak"),
        ("checkpoint_event", "actor", "weak"),
    ],
    "what": [
        ("checkpoint_event", "title", "strong"),
        ("checkpoint_event", "content", "strong"),
        ("checkpoint_receipt", "checkpoint_type", "strong"),
        ("cognition_state", "project_id", "weak"),
    ],
    "why": [
        ("cognition_state", "state.successor.why", "strong"),
        ("checkpoint_event", "metadata.what_changed", "strong"),
    ],
    "success": [
        ("cognition_state", "state.successor.success_criteria", "strong"),
        ("cognition_state", "status", "weak"),
        ("checkpoint_receipt", "status", "weak"),
    ],
    "current_truth": [
        ("cognition_state", "state", "strong"),
        ("cognition_state", "revision", "strong"),
        ("checkpoint_receipt", "state", "strong"),
    ],
    "proven": [
        ("cognition_state", "state.successor.proven", "strong"),
        ("checkpoint_event", "metadata.evidence_refs", "strong"),
        ("checkpoint_receipt", "content_hash", "weak"),
    ],
    "unknown": [
        ("cognition_state", "state.successor.unknown", "strong"),
        ("checkpoint_event", "metadata.unknown", "strong"),
    ],
    "authority": [
        ("cognition_state", "state.successor.authority", "strong"),
        ("checkpoint_event", "metadata.authority_scope", "strong"),
    ],
    "history": [
        ("checkpoint_receipt", "revision", "strong"),
        ("checkpoint_receipt", "source_receipt_id", "strong"),
        ("checkpoint_event", "metadata.source_event_ids", "strong"),
        ("checkpoint_event", "parent_event_id", "strong"),
        ("cognition_state", "state.last_event_id", "weak"),
    ],
    "learning": [
        ("cognition_state", "state.successor.learning", "strong"),
        ("checkpoint_event", "metadata.learned", "strong"),
        ("checkpoint_receipt", "learning_id", "weak"),
    ],
    "next": [
        ("cognition_state", "state.successor.next_actions", "strong"),
        ("checkpoint_event", "metadata.next_use", "weak"),
    ],
    "proof": [
        ("checkpoint_event", "metadata.evidence_refs", "strong"),
        ("checkpoint_receipt", "source_receipt_id", "strong"),
        ("checkpoint_receipt", "content_hash", "strong"),
        ("cognition_state", "state.receipt_id", "weak"),
    ],
    "record": [
        ("cognition_state", "state.successor.record", "strong"),
        ("checkpoint_receipt", "checkpoint_id", "strong"),
        ("checkpoint_receipt", "recorded_at", "strong"),
        ("checkpoint_event", "metadata.checkpointed_at", "strong"),
    ],
    "continuation": [
        ("cognition_state", "state.successor.continuation", "strong"),
        ("cognition_state", "state.successor", "weak"),
        ("checkpoint_event", "metadata.successor_relevance", "weak"),
    ],
}

# ---------------------------------------------------------------------------
# Canonical successor-handoff schema (NAYANET_SUCCESSOR_HANDOFF_V1).
#
# This is the contract for the `successor` jsonb payload accepted by
# nayanet_create_successor_handoff. Every field maps 1:1 onto a
# reconstruction element, so a populated handoff makes structure A
# (the primary cold-restore surface) fully reconstructable on its own.
# ---------------------------------------------------------------------------
HANDOFF_REQUIRED_FIELDS: dict[str, str] = {
    "handoff_id": "record",
    "director": "who",
    "predecessor": "who",
    "what": "what",
    "why": "why",
    "success_criteria": "success",
    "current_truth": "current_truth",
    "proven": "proven",
    "unknown": "unknown",
    "authority": "authority",
    "history": "history",
    "learning": "learning",
    "next_actions": "next",
    "proof": "proof",
    "record": "record",
    "continuation": "continuation",
}

HANDOFF_LIST_FIELDS = {
    "success_criteria",
    "proven",
    "unknown",
    "learning",
    "next_actions",
}

HANDOFF_STRING_FIELDS = {
    "handoff_id",
    "what",
    "why",
    "continuation",
}

HANDOFF_OBJECT_FIELDS = {
    "director",
    "predecessor",
    "current_truth",
    "authority",
    "history",
    "proof",
    "record",
}


def _get_path(obj: dict, path: str):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _substantive(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return len(value.strip()) > 0
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def audit_element(element: str, structures: dict[str, dict]) -> dict:
    """Return {status, sources, value} for one element.

    PRESENT: a strong source carries a substantive value.
    PARTIAL: only weak sources carry values.
    MISSING: no source carries a substantive value.
    """
    rules = EXTRACTION_RULES[element]
    strong_hits: list[str] = []
    weak_hits: list[str] = []
    value = None
    for struct_name, path, strength in rules:
        struct = structures.get(struct_name) or {}
        v = _get_path(struct, path)
        if _substantive(v):
            label = f"{struct_name}.{path}"
            if strength == "strong":
                strong_hits.append(label)
                if value is None:
                    value = v
            else:
                weak_hits.append(label)
                if value is None:
                    value = v
    if strong_hits:
        status = "PRESENT"
    elif weak_hits:
        status = "PARTIAL"
    else:
        status = "MISSING"
    return {
        "status": status,
        "sources": strong_hits + weak_hits,
        "value": value,
    }


def audit(structures: dict[str, dict]) -> dict[str, dict]:
    """Full gap matrix: element -> {status, sources, value}."""
    return {el: audit_element(el, structures) for el in ELEMENTS}


def reconstruct(structures: dict[str, dict]) -> dict:
    """Build the 14-element reconstruction with provenance and a verdict."""
    matrix = audit(structures)
    counts = {"PRESENT": 0, "PARTIAL": 0, "MISSING": 0}
    for el in ELEMENTS:
        counts[matrix[el]["status"]] += 1
    missing = [el for el in ELEMENTS if matrix[el]["status"] == "MISSING"]
    return {
        "schema": SCHEMA_VERSION,
        "reconstructed_at": datetime.now(timezone.utc).isoformat(),
        "elements": matrix,
        "score": counts,
        "missing": missing,
        # Fail-closed: a cold successor cannot reconstruct what is absent.
        "reconstructable": len(missing) == 0,
    }


def validate_handoff(handoff: dict) -> dict:
    """Fail-closed schema check for a nayanet_create_successor_handoff payload.

    Returns {valid, errors[], warnings[], element_coverage}.
    """
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(handoff, dict):
        return {
            "valid": False,
            "errors": ["handoff must be a JSON object"],
            "warnings": [],
            "element_coverage": {},
        }
    if handoff.get("schema_version") != HANDOFF_SCHEMA_VERSION:
        errors.append(
            "schema_version must be %r, got %r"
            % (HANDOFF_SCHEMA_VERSION, handoff.get("schema_version"))
        )
    for field, element in HANDOFF_REQUIRED_FIELDS.items():
        if field not in handoff:
            errors.append(f"missing required field {field!r} (element {element})")
            continue
        v = handoff[field]
        if field in HANDOFF_STRING_FIELDS and not (
            isinstance(v, str) and v.strip()
        ):
            errors.append(f"field {field!r} must be a non-empty string")
        elif field in HANDOFF_OBJECT_FIELDS and not (
            isinstance(v, dict) and len(v) > 0
        ):
            errors.append(f"field {field!r} must be a non-empty object")
        elif field in HANDOFF_LIST_FIELDS and not isinstance(v, list):
            errors.append(f"field {field!r} must be a list")
    # Authority must never be inherited through a handoff.
    authority = handoff.get("authority")
    if isinstance(authority, dict):
        if authority.get("inherits_authority") is True:
            errors.append(
                "authority.inherits_authority must never be true: "
                "a successor does not inherit authority"
            )
        if "scope" not in authority:
            warnings.append("authority.scope not stated; default-deny applies")
    # An empty unknown list is a claim, not a fact — flag it.
    if isinstance(handoff.get("unknown"), list) and len(handoff["unknown"]) == 0:
        warnings.append(
            "unknown is empty: asserting 'no known unknowns' — "
            "verify this is deliberate"
        )
    coverage = {}
    for field, element in HANDOFF_REQUIRED_FIELDS.items():
        v = handoff.get(field)
        coverage[element] = "PRESENT" if _substantive(v) else "MISSING"
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "element_coverage": coverage,
    }


def _load_json_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit cold-successor reconstructability of checkpoint state."
    )
    parser.add_argument(
        "--audit",
        metavar="JSON",
        help="JSON file with {cognition_state, checkpoint_receipt, checkpoint_event}",
    )
    parser.add_argument(
        "--validate-handoff",
        metavar="JSON",
        help="JSON file with a successor handoff payload to schema-check",
    )
    args = parser.parse_args(argv)

    if args.validate_handoff:
        result = validate_handoff(_load_json_file(args.validate_handoff))
        print(json.dumps(result, indent=2, default=str))
        return 0 if result["valid"] else 1

    if args.audit:
        structures = _load_json_file(args.audit)
        result = reconstruct(structures)
        print(json.dumps(result, indent=2, default=str))
        if not result["reconstructable"]:
            print(
                "FAIL CLOSED: missing elements: " + ", ".join(result["missing"]),
                file=sys.stderr,
            )
            return 1
        print("RECONSTRUCTABLE: all 14 elements present", file=sys.stderr)
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
