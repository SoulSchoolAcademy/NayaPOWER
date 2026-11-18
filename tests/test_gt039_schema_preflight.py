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
    assert result["type_mismatches"] == {}
    assert result["required_not_null_mismatches"] == {"naya_notes": ["category"]}
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
    declared = preflight.declared_contracts()
    for table, cols in contracts.items():
        missing = cols - set(data["tables"][table])
        data["tables"][table] = sorted(set(data["tables"][table]) | cols)
        for col in missing:
            # Where source guards don't declare types, synthetic shape is only
            # diagnostic. Never apply these placeholders to real production.
            rule = declared.get(table, {}).get(col, {"udt_name": "text"})
            data["column_types"][table][col] = rule["udt_name"]
        for col, rule in declared.get(table, {}).items():
            if rule["not_null"] and col not in data["not_nullable"][table]:
                data["not_nullable"][table].append(col)
    result = preflight.evaluate(data, contracts)
    assert result["verdict"] == "SHAPE_COMPATIBLE_ONLY"
    assert result["missing"] == {}
    assert result["meaning"].endswith("NEVER production approval.")


@pytest.mark.parametrize("broken", ["tables", "kind", "captured_date_utc",
                                  "column_types", "not_nullable"])
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


def test_existing_source_column_type_drift_is_blocked() -> None:
    data = snapshot()
    data["column_types"]["smart_links"]["active"] = "text"  # expected boolean / bool
    result = preflight.evaluate(data, preflight.required_columns())
    assert result["verdict"] == "BLOCKED_SCHEMA_DRIFT"
    assert result["type_mismatches"]["smart_links.active"] == {
        "expected": "bool", "observed": "text"
    }


def test_required_not_null_mismatch_alone_still_blocks() -> None:
    data = snapshot()
    # Removing required NOT NULL from an existing field is not safe even
    # when every required name is present in an idealized schema.
    data["tables"] = {k: list(v) for k, v in data["tables"].items()}
    declared = preflight.declared_contracts()
    for table, cols in preflight.required_columns().items():
        for col in cols - set(data["tables"][table]):
            data["tables"][table].append(col)
            data["column_types"][table][col] = declared.get(table, {}).get(
                col, {"udt_name": "text"})["udt_name"]
        for col, rule in declared.get(table, {}).items():
            if rule["not_null"] and col != "category" and col not in data["not_nullable"][table]:
                data["not_nullable"][table].append(col)
    result = preflight.evaluate(data, preflight.required_columns())
    assert result["missing_column_count"] == 0
    assert result["type_mismatches"] == {}
    assert result["required_not_null_mismatches"] == {"naya_notes": ["category"]}
    assert result["verdict"] == "BLOCKED_SCHEMA_DRIFT"


def test_partial_type_metadata_fails_closed() -> None:
    data = snapshot()
    del data["column_types"]["smart_links"]["active"]
    with pytest.raises(preflight.PreflightError, match="METADATA_COLUMN_TYPES_INCOMPLETE"):
        preflight.evaluate(data, preflight.required_columns())


def test_non_nullable_metadata_cannot_name_nonexistent_field() -> None:
    data = snapshot()
    data["not_nullable"]["smart_mail_threads"].append("fake_field")
    with pytest.raises(preflight.PreflightError, match="METADATA_NULLABILITY_INVALID"):
        preflight.evaluate(data, preflight.required_columns())
