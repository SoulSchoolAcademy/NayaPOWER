#!/usr/bin/env python3
"""GT-039 read-only *shape* preflight against a supplied metadata-only catalog.

Derives required fields from existing canonical migration SQL, not a second
hand-maintained contract. It does not connect to Supabase, read any customer
record, modify a database, or authorize a migration.

Provide fresh metadata (table/column name, type and nullable status ONLY) from
information_schema. The versioned fixture is historical test evidence, never
a substitute for current deployment checks.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations"
REQUIRED_LIVE_TABLES = frozenset(
    {"smart_notes", "smart_mail_threads", "smart_mail_messages",
     "invites", "naya_notes", "smart_links"}
)
GUARD_MIGRATIONS = (
    "20261022203000_person_timeline_v1.sql",
    "20261022214500_universal_search_v1.sql",
)
CREATE_CONTRACTS = {
    "20261022201500_smart_links_v1.sql": {"smart_links": {"owner_id"}},
    "20261022204500_naya_notes_v1.sql": {"naya_notes": {"owner_id", "text"}},
}
GUARD = re.compile(
    r"for\s+col\s+in\s+select\s+\*\s+from\s+\(values"
    r"(?P<pairs>.*?)\)\s*as\s+t\s*\(\s*tbl\s*,\s*colname\s*\)\s*loop",
    re.IGNORECASE | re.DOTALL,
)
PAIR = re.compile(r"\(\s*'([a-z_]+)'\s*,\s*'([a-z_]+)'\s*\)", re.I)
COLUMN = re.compile(r"(?m)^\s*([a-z_]+)\s+(?:uuid|text|boolean|timestamptz|integer|jsonb)\b", re.I)
DECLARED_COLUMN = re.compile(r"(?m)^\s*([a-z_]+)\s+(uuid|text|boolean|timestamptz|integer|jsonb)\b([^\n]*)", re.I)
UDT = {"boolean": "bool", "integer": "int4"}


class PreflightError(ValueError):
    pass


def required_columns(root: Path = MIGRATION) -> dict[str, set[str]]:
    result = {table: set() for table in REQUIRED_LIVE_TABLES}
    for filename in GUARD_MIGRATIONS:
        source = (root / filename).read_text(encoding="utf-8")
        match = GUARD.search(source)
        if not match:
            raise PreflightError(f"SOURCE_GUARD_MISSING: {filename}")
        pairs = PAIR.findall(match.group("pairs"))
        if not pairs:
            raise PreflightError(f"SOURCE_GUARD_EMPTY: {filename}")
        for table, column in pairs:
            if table in result:
                result[table].add(column)
    for filename, tables in CREATE_CONTRACTS.items():
        source = (root / filename).read_text(encoding="utf-8")
        for table, cols in tables.items():
            match = re.search(
                rf"\bcreate\s+table\s+if\s+not\s+exists\s+public\.{table}\s*\("
                r"(?P<body>.*?)\n\s*\)\s*;",
                source, re.I | re.S,
            )
            if not match:
                raise PreflightError(f"SOURCE_TABLE_CONTRACT_MISSING: {filename}:{table}")
            body = match.group("body")
            declared = set(COLUMN.findall(body))
            for col in cols:  # Non-optional authority/shape anchors; removing one must fail.
                if col not in declared:
                    raise PreflightError(f"SOURCE_COLUMN_CONTRACT_MISSING: {filename}:{table}.{col}")
            if not declared:
                raise PreflightError(f"SOURCE_TABLE_EMPTY: {filename}:{table}")
            result[table].update(declared)
    if any(not fields for fields in result.values()):
        raise PreflightError("SOURCE_CONTRACT_INCOMPLETE")
    return result


def declared_contracts(root: Path = MIGRATION) -> dict[str, dict[str, dict]]:
    """Only types and NOT NULL constraints *actually declared* in create-table SQL."""
    result: dict[str, dict[str, dict]] = {}
    for filename, tables in CREATE_CONTRACTS.items():
        sql = (root / filename).read_text(encoding="utf-8")
        for table in tables:
            match = re.search(
                rf"\bcreate\s+table\s+if\s+not\s+exists\s+public\.{table}\s*\("
                r"(?P<body>.*?)\n\s*\)\s*;", sql, re.I | re.S
            )
            if not match:
                raise PreflightError(f"SOURCE_TABLE_CONTRACT_MISSING: {filename}:{table}")
            cols = {
                name: {"udt_name": UDT.get(typ.lower(), typ.lower()),
                       "not_null": bool(re.search(r"\bnot\s+null\b", tail, re.I))}
                for name, typ, tail in DECLARED_COLUMN.findall(match.group("body"))
            }
            if not cols or not CREATE_CONTRACTS[filename][table] <= cols.keys():
                raise PreflightError(f"SOURCE_DECLARATIONS_INCOMPLETE: {filename}:{table}")
            result[table] = cols
    return result


def parse_snapshot(source: dict) -> dict[str, set[str]]:
    if not isinstance(source, dict) or source.get("kind") != "information_schema_column_contracts":
        raise PreflightError("METADATA_KIND_MISSING")
    if not isinstance(source.get("captured_date_utc"), str):
        raise PreflightError("METADATA_CAPTURE_DATE_MISSING")
    tables = source.get("tables")
    if not isinstance(tables, dict):
        raise PreflightError("METADATA_TABLES_MISSING")
    absent = sorted(REQUIRED_LIVE_TABLES - tables.keys())
    if absent:
        raise PreflightError("METADATA_REQUIRED_TABLES_MISSING: " + ", ".join(absent))
    type_map = source.get("column_types")
    non_null = source.get("not_nullable")
    if not isinstance(type_map, dict) or not isinstance(non_null, dict):
        raise PreflightError("METADATA_TYPES_OR_NULLABILITY_MISSING")
    result = {}
    for table in REQUIRED_LIVE_TABLES:
        cols = tables[table]
        if (not isinstance(cols, list) or not cols or
                any(not isinstance(c, str) or not re.fullmatch(r"[a-z_]+", c) for c in cols)):
            raise PreflightError(f"METADATA_INVALID_COLUMNS: {table}")
        result[table] = set(cols)
        if not isinstance(type_map.get(table), dict) or set(type_map[table]) != result[table]:
            raise PreflightError(f"METADATA_COLUMN_TYPES_INCOMPLETE: {table}")
        if any(not isinstance(v, str) or not re.fullmatch(r"[a-z0-9_]+", v)
               for v in type_map[table].values()):
            raise PreflightError(f"METADATA_COLUMN_TYPES_INVALID: {table}")
        nn = non_null.get(table)
        if not isinstance(nn, list) or len(nn) != len(set(nn)) or not set(nn) <= result[table]:
            raise PreflightError(f"METADATA_NULLABILITY_INVALID: {table}")
    return result


def evaluate(metadata: dict, contracts: dict[str, set[str]]) -> dict:
    actual = parse_snapshot(metadata)
    declared = declared_contracts()
    type_drift = {}
    nullability_drift = {}
    for table, columns in sorted(declared.items()):
        for col, rule in sorted(columns.items()):
            if col not in actual[table]:
                continue  # Already BLOCKED as a missing column.
            actual_type = metadata["column_types"][table][col]
            if actual_type != rule["udt_name"]:
                type_drift[f"{table}.{col}"] = {
                    "expected": rule["udt_name"], "observed": actual_type}
            if rule["not_null"] and col not in metadata["not_nullable"][table]:
                nullability_drift.setdefault(table, []).append(col)
    missing = {
        table: sorted(columns - actual[table])
        for table, columns in sorted(contracts.items())
        if columns - actual[table]
    }
    return {
        "verdict": "BLOCKED_SCHEMA_DRIFT" if (missing or type_drift or nullability_drift)
                   else "SHAPE_COMPATIBLE_ONLY",
        "missing_column_count": sum(map(len, missing.values())),
        "affected_tables": len(set(missing) | set(nullability_drift)
                               | {name.split(".")[0] for name in type_drift}),
        "missing": missing,
        "type_mismatches": type_drift,
        "required_not_null_mismatches": nullability_drift,
        "captured_date_utc": metadata["captured_date_utc"],
        "meaning": "Metadata-only prerequisite shape check; NEVER production approval.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--catalog-json", type=Path, required=True,
                    help="Metadata-only table/column/type/nullability snapshot; use fresh information_schema.columns.")
    args = ap.parse_args()
    try:
        catalog = json.loads(args.catalog_json.read_text(encoding="utf-8"))
        result = evaluate(catalog, required_columns())
    except (OSError, json.JSONDecodeError, PreflightError) as exc:
        print(json.dumps({"verdict": "UNKNOWN_FAIL_CLOSED", "error": str(exc)}, sort_keys=True))
        return 3
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["verdict"] == "BLOCKED_SCHEMA_DRIFT" else 0


if __name__ == "__main__":
    raise SystemExit(main())