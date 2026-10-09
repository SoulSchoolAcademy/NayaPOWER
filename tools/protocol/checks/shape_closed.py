#!/usr/bin/env python3
"""Fail Closed on Shape — the validator's meta-law (2026-10-09).

"Absence is the cheapest exploit." A record that passes SYNTAX (valid
JSON, right keys) can still carry NOTHING: required fields missing,
None, empty strings. Every downstream check then validates a ghost —
the law fires on empty air and the violation walks through.

This module enforces SHAPE, not just syntax: required fields must be
PRESENT, CORRECTLY TYPED, and (for text/collections) NON-EMPTY.
A shape failure fails the record outright — it never silently defaults,
never coerces, never proceeds.

Sibling checks (two_layer, blocker_surfacing) import validate_shape()
and run it FIRST: shape before substance, always.

Record:
    {
      "schema": {
        "required": ["field1", "field2"],      # must be present and not None
        "types": {"field1": "str",             # str | int | float | bool |
                  "field2": "list"},           # list | dict
        "non_empty": ["field1", "field2"],     # str/list/dict with content
        "min_length": {"field1": 40},          # minimum len() for str/list
        "allowed": {"status": ["a", "b"]},     # enum membership
      },
      "data": { ... the record under test ... }
    }

Usage:
    python3 tools/protocol/checks/shape_closed.py \\
        --record '{"schema": {...}, "data": {...}}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

TYPES = {
    "str": str,
    "int": int,
    "float": (float, int),
    "bool": bool,
    "list": list,
    "dict": dict,
}


def _type_ok(tname: str, value) -> bool:
    """Type acceptance with the bool quirk closed.

    Python's isinstance(True, int) is True — a bool would silently pass
    an "int" or "float" gate. A bool is not a number for shape purposes:
    True is not 1 here. Reject bool for int/float explicitly.
    """
    if isinstance(value, bool) and tname in ("int", "float"):
        return False
    return isinstance(value, TYPES[tname])


def validate_shape(data: dict, schema: dict) -> tuple[bool, list[str]]:
    """Validate data against a shape schema. Returns (ok, reasons)."""
    reasons: list[str] = []
    if not isinstance(data, dict):
        return False, ["data is not a JSON object — shape check cannot proceed"]
    if not isinstance(schema, dict):
        return False, ["schema is not a JSON object — fail closed, cannot validate"]

    ok = True
    required = schema.get("required", []) or []
    types = schema.get("types", {}) or {}
    non_empty = schema.get("non_empty", []) or []
    min_length = schema.get("min_length", {}) or {}
    allowed = schema.get("allowed", {}) or {}

    # 1. Presence — absence is the exploit.
    for field in required:
        if field not in data:
            ok = False
            reasons.append(
                f"field {field!r} is ABSENT — absence is the cheapest "
                "exploit; the record fails closed on shape"
            )
        elif data[field] is None:
            ok = False
            reasons.append(
                f"field {field!r} is None — a required field present-as-None "
                "is absence in disguise; fail closed"
            )
    for field in required:
        if field in data and data[field] is not None:
            reasons.append(f"field {field!r} present")

    # 2. Type — a str where a list belongs is a silent lie.
    for field, tname in types.items():
        if field not in data or data[field] is None:
            continue  # presence already failed above
        if tname not in TYPES:
            ok = False
            reasons.append(f"schema error: unknown type {tname!r} for {field!r}")
            continue
        if not _type_ok(tname, data[field]):
            ok = False
            bool_note = (
                " — a bool is not a number (isinstance quirk closed)"
                if isinstance(data[field], bool)
                else ""
            )
            reasons.append(
                f"field {field!r} is {type(data[field]).__name__}, "
                f"not {tname} — wrong shape, fail closed{bool_note}"
            )
            continue
        reasons.append(f"field {field!r} is {tname}")

    # 3. Non-empty — an empty string is not content.
    for field in non_empty:
        if field not in data or data[field] is None:
            continue
        val = data[field]
        if isinstance(val, str) and not val.strip():
            ok = False
            reasons.append(
                f"field {field!r} is an empty/blank string — "
                "emptiness is not content; fail closed"
            )
        elif isinstance(val, (list, dict)) and len(val) == 0:
            ok = False
            reasons.append(
                f"field {field!r} is an empty {type(val).__name__} — "
                "emptiness is not content; fail closed"
            )

    # 4. Minimum length — a one-word layer is not a layer.
    for field, minlen in min_length.items():
        if field not in data or data[field] is None:
            continue
        try:
            size = len(data[field])
        except TypeError:
            continue
        if size < minlen:
            ok = False
            reasons.append(
                f"field {field!r} has length {size} < {minlen} — "
                "too thin to carry the meaning the law requires; fail closed"
            )

    # 5. Enum membership — unknown types fail closed, never default.
    for field, members in allowed.items():
        if field not in data or data[field] is None:
            continue
        if data[field] not in members:
            ok = False
            reasons.append(
                f"field {field!r} is {data[field]!r}, not in "
                f"{list(members)!r} — unknown values fail closed, "
                "they are never silently defaulted"
            )

    return ok, reasons


def check(record: dict) -> dict:
    details: dict = {"law": "FAIL-CLOSED-SHAPE", "law_status": "RATIFIED"}
    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)
    ok, reasons = validate_shape(record.get("data", {}),
                                 record.get("schema", {}))
    return result(ok, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed shape check")
    parser.add_argument("--record", required=True,
                        help="JSON record with schema+data (or @file)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "FAIL-CLOSED-SHAPE"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
