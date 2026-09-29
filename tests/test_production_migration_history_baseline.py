"""Production Supabase migration-history parity contract.

The active migration directory is governed by the production-ledger manifest.
Historical repository migrations displaced by reconciliation remain preserved
outside the active Supabase migration path.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"
MANIFEST = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
PATTERN = re.compile(r"^(\d{14})_(.+)\.sql$")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_active_migration_directory_matches_governed_ledger_manifest():
    ledger = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert ledger["schema"] == "naya.supabase.production-migration-ledger.v1"
    assert ledger["source_project_ref"] == "dahisasgpfvziswqvmvm"
    applied = ledger["production_applied"]
    pending = ledger["pending"]
    assert ledger["production_applied_count"] == len(applied) == 143

    entries = applied + pending
    versions = [entry["version"] for entry in entries]
    assert len(versions) == len(set(versions)), "duplicate governed migration versions"

    expected = {Path(entry["path"]).name: entry for entry in entries}
    actual = {path.name: path for path in MIGRATIONS.glob("*.sql")}
    assert set(actual) == set(expected), (
        f"active migration set drift: missing={sorted(set(expected)-set(actual))}, "
        f"unexpected={sorted(set(actual)-set(expected))}"
    )

    for name, path in actual.items():
        match = PATTERN.match(name)
        assert match, f"malformed active migration filename: {name}"
        entry = expected[name]
        assert match.group(1) == entry["version"]
        assert match.group(2) == entry["name"]
        assert _sha256(path) == entry["sha256"], f"migration content drift: {name}"


def test_pre_reconciliation_repository_lineage_is_preserved_exactly():
    ledger = json.loads(MANIFEST.read_text(encoding="utf-8"))
    legacy = ledger["legacy_repository_snapshot"]
    assert ledger["legacy_repository_snapshot_count"] == len(legacy) == 95
    assert len({entry["original_path"] for entry in legacy}) == len(legacy)
    for entry in legacy:
        archived = ROOT / entry["archive_path"]
        assert archived.is_file(), f"missing archived source migration: {archived}"
        assert _sha256(archived) == entry["sha256"], (
            f"archived source migration changed: {entry['archive_path']}"
        )
