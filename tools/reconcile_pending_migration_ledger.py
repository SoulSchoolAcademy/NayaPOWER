#!/usr/bin/env python3
"""Detect or reconcile metadata drift in pending production migrations.

This tool NEVER applies migrations and NEVER changes production status. By
default it is read-only and exits non-zero when the governed ledger projection
does not match repository bytes. --write updates only sha256/bytes/
statement_count for entries already present in ledger["pending"].
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from pglast import parse_sql

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"

def metadata(path: Path) -> dict:
    data = path.read_bytes()
    text = data.decode("utf-8")
    return {
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "statement_count": len(parse_sql(text)),
    }

def reconcile(write: bool = False) -> int:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    drift = []
    for entry in ledger.get("pending", []):
        path = ROOT / entry["path"]
        if not path.is_file():
            drift.append({"version": entry.get("version"), "path": entry["path"], "error": "MISSING_FILE"})
            continue
        actual = metadata(path)
        expected = {k: entry.get(k) for k in actual}
        if expected != actual:
            drift.append({"version": entry.get("version"), "path": entry["path"], "expected": expected, "actual": actual})
            if write:
                entry.update(actual)

    print(json.dumps({"schema": "NAYAPOWER_PENDING_MIGRATION_DRIFT_V1", "write": write, "drift": drift}, indent=2))
    if write and drift:
        # Missing files are never repaired by metadata rewriting.
        if any("error" in item for item in drift):
            return 2
        LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        return 0
    return 1 if drift else 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="update metadata only for existing pending entries")
    args = parser.parse_args()
    raise SystemExit(reconcile(args.write))
