"""Source-level contract for Decision Value Calculus V2.1 SmartLedger binding.

These tests prove repository semantics before deployment. They do not claim that
the pending migration has been applied to production.
"""
from __future__ import annotations

import json
from pathlib import Path

from pglast import parse_sql

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261001032000_decision_value_smart_ledger_v2_1.sql"
CONTRIBUTION_SCHEMA = ROOT / ".naya" / "specifications" / "NAYA-CONTRIBUTION-VALUE-V2.1.schema.json"


def source() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _function_body(name: str) -> str:
    text = source()
    marker = f"create or replace function public.{name}"
    start = text.index(marker)
    end = text.index("\n" + "$" * 2 + ";", start) + 4
    return text[start:end]


def test_migration_parses_and_creates_no_second_ledger_table():
    text = source()
    assert len(parse_sql(text)) == 18
    assert "create table" not in text.lower()
    assert "nayanet_smart_ledger" in text
    assert "nayanet_attach_value_receipt_v2_1" in text


def test_typed_receipt_validator_has_two_streams_and_three_assessment_states():
    body = _function_body("nayanet_value_receipt_v2_1_state")
    assert "'ALIGNMENT_DECISION'" in body
    assert "'CONTRIBUTION_VALUE'" in body
    assert "'ASSESSED'" in body
    assert "'VERIFIED_VALUE'" in body
    assert "VALUE_RECEIPT_SCHEMA_VERSION" in body
    assert "VALUE_RECEIPT_ENGINE_VERSION" in body
    assert "EVIDENCE_BEFORE_REWARD" in body


def test_contribution_receipt_validator_enforces_factors_privacy_and_verified_delta():
    body = _function_body("nayanet_value_receipt_v2_1_state")
    for factor in ("quality", "relevance", "verification_strength", "impact", "novelty"):
        assert factor in body
    assert "CONTRIBUTION_VALUE_FACTOR_RANGE" in body
    assert "CONTRIBUTION_VALUE_PRIVACY" in body
    assert "VERIFIED_CONTRIBUTION_REQUIRES_DELTA" in body
    assert "v_verification <> 'VERIFIED' and v_points <> 0" in body


def test_attach_is_owner_scoped_idempotent_and_conflicting_replay_fails_closed():
    body = _function_body("nayanet_attach_value_receipt_v2_1")
    assert "owner_id=p_owner_id" in body
    assert "source_table=p_source_table" in body
    assert "source_id=p_source_id" in body
    assert "for update" in body.lower()
    assert "if v_existing = p_receipt then" in body
    assert "VALUE_RECEIPT_ALREADY_ATTACHED" in body
    assert "privacy_classification" not in body, "value attachment must never widen privacy"


def test_value_writer_is_service_role_only():
    text = source()
    sig = "public.nayanet_attach_value_receipt_v2_1(uuid,text,text,jsonb)"
    assert f"revoke all on function {sig} from public,anon,authenticated;" in text
    assert f"grant execute on function {sig} to service_role;" in text


def test_execution_receipts_project_typed_v21_or_explicit_unassessed_state():
    projection = _function_body("nayanet_execution_value_projection_v2_1")
    trigger = _function_body("nayanet_execution_receipt_to_ledger")
    assert "assessment_state','UNASSESSED'" in projection
    assert "public.nayanet_value_receipt_v2_1_state(v_input)" in projection
    assert "DECISION-VALUE-CALCULUS-V2.1" in projection
    assert "public.nayanet_execution_value_projection_v2_1" in trigger


def test_future_smart_note_and_space_writers_stop_issuing_legacy_seed_points():
    note = _function_body("nayanet_smart_note_event_to_ledger")
    space = _function_body("nayanet_space_to_ledger")
    for body in (note, space):
        assert "assessment_state','UNASSESSED'" in body
        assert "legacy_seed_policy','NOT_REISSUED'" in body
        assert "base_points" not in body
        assert "NayaNET_V1_STARTING_MODEL" not in body


def test_historical_seed_migrations_remain_preserved_as_provenance():
    note_legacy = (ROOT / "supabase" / "migrations" / "20260919015207_smart_ledger_foundation_v1.sql").read_text(encoding="utf-8")
    space_legacy = (ROOT / "supabase" / "migrations" / "20260919015259_fix_smart_ledger_space_privacy_mapping.sql").read_text(encoding="utf-8")
    assert "'base_points',5" in note_legacy
    assert "'base_points',10" in space_legacy
    assert "NayaNET_V1_STARTING_MODEL" in note_legacy
    assert "NayaNET_V1_STARTING_MODEL" in space_legacy
    # New migration has no data backfill by legacy-engine predicate.
    assert "where value->>'value_engine'" not in source().lower()


def test_contribution_schema_is_strict_and_evidence_before_reward():
    schema = json.loads(CONTRIBUTION_SCHEMA.read_text(encoding="utf-8"))
    assert schema["properties"]["receipt_type"]["const"] == "CONTRIBUTION_VALUE"
    assert schema["properties"]["schema_version"]["const"] == "2.1"
    assert schema["properties"]["engine_version"]["const"] == "DECISION-VALUE-CALCULUS-V2.1"
    assert schema["properties"]["factors"]["additionalProperties"] is False
    assert set(schema["properties"]["factors"]["required"]) == {
        "quality", "relevance", "verification_strength", "impact", "novelty"
    }
    assert schema["properties"]["points_awarded"]["minimum"] == 0
    assert any(
        rule.get("then", {}).get("properties", {}).get("points_awarded", {}).get("const") == 0
        for rule in schema["allOf"]
    )


def test_pending_migration_ledger_declares_not_production_applied():
    ledger = json.loads((ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json").read_text(encoding="utf-8"))
    matches = [x for x in ledger["pending"] if x["version"] == "20261001032000"]
    assert len(matches) == 1
    entry = matches[0]
    assert entry["name"] == "decision_value_smart_ledger_v2_1"
    assert entry["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    assert entry["statement_count"] == 18
