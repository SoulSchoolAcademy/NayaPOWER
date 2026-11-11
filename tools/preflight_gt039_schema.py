#!/usr/bin/env python3
"""GT-039 read-only *shape* preflight against a supplied metadata-only catalog.

Derives required fields from existing canonical migration SQL, not a second
hand-maintained contract. It does not connect to Supabase, read any customer
record, modify a database, or authorize a migration.

Provide fresh metadata (table_name, column_name ONLY) from information_schema,
using the query shown in --help. The versioned fixture is historical test
evidence, never a substitute for current deployment checks.
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


def parse_snapshot(source: dict) -> dict[str, set[str]]:
    if not isinstance(source, dict) or source.get("kind") != "information_schema_columns":
        raise PreflightError("METADATA_KIND_MISSING")
    if not isinstance(source.get("captured_date_utc"), str):
        raise PreflightError("METADATA_CAPTURE_DATE_MISSING")
    tables = source.get("tables")
    if not isinstance(tables, dict):
        raise PreflightError("METADATA_TABLES_MISSING")
    absent = sorted(REQUIRED_LIVE_TABLES - tables.keys())
    if absent:
        raise PreflightError("METADATA_REQUIRED_TABLES_MISSING: " + ", ".join(absent))
    result = {}
    for table in REQUIRED_LIVE_TABLES:
        cols = tables[table]
        if (not isinstance(cols, list) or not cols or
                any(not isinstance(c, str) or not re.fullmatch(r"[a-z_]+", c) for c in cols)):
            raise PreflightError(f"METADATA_INVALID_COLUMNS: {table}")
        result[table] = set(cols)
    return result


def evaluate(metadata: dict, contracts: dict[str, set[str]]) -> dict:
    actual = parse_snapshot(metadata)
    missing = {
        table: sorted(columns - actual[table])
        for table, columns in sorted(contracts.items())
        if columns - actual[table]
    }
    return {
        "verdict": "BLOCKED_SCHEMA_DRIFT" if missing else "SHAPE_COMPATIBLE_ONLY",
        "missing_column_count": sum(map(len, missing.values())),
        "affected_tables": len(missing),
        "missing": missing,
        "captured_date_utc": metadata["captured_date_utc"],
        "meaning": "Metadata-only prerequisite shape check; NEVER production approval.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--catalog-json", type=Path, required=True,
                    help="Metadata-only snapshot; use a fresh SELECT from information_schema.columns.")
    args = ap.parse_args()
    try:
        catalog = json.loads(args.catalog_json.read_text(encoding="utf-8"))
        result = evaluate(catalog, required_columns())
    except (OSError, json.JSONDecodeError, PreflightError) as exc:
        print(json.dumps({"verdict": "UNKNOWN_FAIL_CLOSED", "error": str(exc)}, sort_keys=True))
        return 3
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
