"""Regression controls for metadata-only GT-039 prerequisite shape audit.

The recorded live metadata is a historical fixture. It must remain BLOCKED;
no test asserts production safety, migration approval, or fixes missing fields.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import preflight_gt039_schema as preflight  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "gt039_live_columns_20261111.json"


def snapshot() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_historical_live_schema_is_blocked_on_exact_source_contract() -> None:
    result = preflight.evaluate(snapshot(), preflight.required_columns())
    assert result["verdict"] == "BLOCKED_SCHEMA_DRIFT"
    assert result["missing_column_count"] == 13
    assert result["affected_tables"] == 6
    assert result["missing"] == {
        "invites": ["owner_alias"],
        "naya_notes": ["owner_id", "text"],
        "smart_links": ["owner_id", "updated_at"],
        "smart_mail_messages": ["direction", "thread_key"],
        "smart_mail_threads": ["owner_alias", "participants", "status", "thread_key"],
        "smart_notes": ["author_name", "sender_name"],
    }


def test_adding_all_missing_columns_is_only_shape_compatibility() -> None:
    data = snapshot()
    contracts = preflight.required_columns()
    for table, cols in contracts.items():
        data["tables"][table] = sorted(set(data["tables"][table]) | cols)
    result = preflight.evaluate(data, contracts)
    assert result["verdict"] == "SHAPE_COMPATIBLE_ONLY"
    assert result["missing"] == {}
    assert result["meaning"].endswith("NEVER production approval.")


@pytest.mark.parametrize("broken", ["tables", "kind", "captured_date_utc"])
def test_invalid_or_incomplete_catalog_fails_closed(broken: str) -> None:
    data = snapshot()
    data.pop(broken)
    with pytest.raises(preflight.PreflightError):
        preflight.evaluate(data, preflight.required_columns())


def test_missing_required_table_fails_closed() -> None:
    data = snapshot()
    del data["tables"]["smart_links"]
    with pytest.raises(preflight.PreflightError, match="METADATA_REQUIRED_TABLES_MISSING"):
        preflight.evaluate(data, preflight.required_columns())


def test_guard_removal_fails_closed(tmp_path: Path) -> None:
    for name in (*preflight.GUARD_MIGRATIONS, *preflight.CREATE_CONTRACTS):
        shutil.copy(preflight.MIGRATION / name, tmp_path / name)
    sql = tmp_path / preflight.GUARD_MIGRATIONS[0]
    sql.write_text(sql.read_text(encoding="utf-8").replace("for col in", "for entry in", 1),
                   encoding="utf-8")
    with pytest.raises(preflight.PreflightError, match="SOURCE_GUARD_MISSING"):
        preflight.required_columns(tmp_path)


def test_create_table_contract_removal_fails_closed(tmp_path: Path) -> None:
    for name in (*preflight.GUARD_MIGRATIONS, *preflight.CREATE_CONTRACTS):
        shutil.copy(preflight.MIGRATION / name, tmp_path / name)
    sql = tmp_path / "20261022201500_smart_links_v1.sql"
    original = sql.read_text(encoding="utf-8")
    assert "owner_id uuid" in original
    sql.write_text(original.replace("owner_id uuid", "legacy_owner_uuid uuid", 1), encoding="utf-8")
    with pytest.raises(preflight.PreflightError, match="SOURCE_COLUMN_CONTRACT_MISSING"):
        preflight.required_columns(tmp_path)
