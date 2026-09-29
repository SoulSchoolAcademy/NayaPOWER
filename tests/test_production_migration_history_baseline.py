"""Failure-first guard for Supabase production migration-history parity.

Live Supabase production currently records 143 applied migrations, while the
repository's active migration directory has drifted to a different version
lineage. Native GitHub deployment refuses that divergence.

This test is intentionally red before the canonical history repair.
It never mutates production migration metadata.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"
PATTERN = re.compile(r"^(\d{14})_(.+)\.sql$")

PRODUCTION_MIGRATION_COUNT = 143
PRODUCTION_ANCHORS = {
    "20260827011050",
    "20260902035216",
    "20260928172457",
    "20260928180632",
}


def _active_versions():
    versions = []
    malformed = []
    for path in sorted(MIGRATIONS.glob("*.sql")):
        match = PATTERN.match(path.name)
        if not match:
            malformed.append(path.name)
            continue
        versions.append(match.group(1))
    return versions, malformed


def test_active_migration_versions_match_production_history_shape():
    versions, malformed = _active_versions()
    assert not malformed, f"malformed active migration filenames: {malformed}"
    assert len(versions) == len(set(versions)), "duplicate active migration versions exist"
    assert len(versions) == PRODUCTION_MIGRATION_COUNT, (
        f"expected {PRODUCTION_MIGRATION_COUNT} production-history versions, got {len(versions)}"
    )
    assert PRODUCTION_ANCHORS <= set(versions), (
        f"missing production-history anchors: {sorted(PRODUCTION_ANCHORS - set(versions))}"
    )
