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
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def test_active_migration_directory_matches_governed_ledger_manifest():
    ledger = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert ledger["schema"] == "naya.supabase.production-migration-ledger.v1"
    assert ledger["source_project_ref"] == "dahisasgpfvziswqvmvm"
    assert ledger["hash_semantics"] == "UTF8_TEXT_LF_NORMALIZED_SHA256"
    applied = ledger["production_applied"]
    pending = ledger["pending"]
    assert ledger["production_applied_count"] == len(applied)
    assert ledger["production_applied_count"] >= 143, "production migration ledger must not shrink below the reconstructed baseline"

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


def test_active_migrations_have_no_byte_order_mark_or_leading_invisible_characters():
    """Supabase's migration runner rejects a UTF-8 BOM: a file starting with
    EF BB BF fails with `syntax error at or near "alter"` and fails the
    production deployment check closed (observed 2026-09-30 on
    20260929210000_nayanet_action_idempotency_atomicity.sql)."""
    offenders = []
    for path in sorted(MIGRATIONS.glob("*.sql")):
        raw = path.read_bytes()
        if raw[:3] == b"\xef\xbb\xbf":
            offenders.append(f"{path.name}: UTF-8 BOM")
        elif raw[:1] in (b"\xff", b"\xfe", b"\x00"):
            offenders.append(f"{path.name}: unexpected leading byte {raw[:1]!r}")
    assert not offenders, (
        "migrations with leading invisible characters (Supabase will reject): "
        + "; ".join(offenders)
    )
