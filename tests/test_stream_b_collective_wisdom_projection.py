import re
from pathlib import Path

MIGRATION = Path("supabase/migrations/20260924150000_verified_learning_collective_wisdom_projection_v1.sql")
COMPOUND = Path("supabase/functions/nayanet-compound-intelligence/index.ts")

def test_verified_learning_projection_contract():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "nayanet_project_verified_learning_to_collective_wisdom" in sql
    assert "v_learning.status <> 'ACTIVE'" in sql
    assert "nayanet_collective_wisdom_for_event" in sql
    assert "v_learning.claim" in sql
    assert "v_source.id" in sql
    assert "verification_method" in sql
    assert "set epistemic_state='VERIFIED'" in sql
    assert "execution authority and publication are not consulted" in sql

def test_projection_provenance_excludes_identity_and_raw_content():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "'identity'" not in sql
    assert "'raw_content'" not in sql
    assert "source_event_id" in sql
    assert "learning_id" in sql

def test_compound_capture_does_not_directly_publish_collective_wisdom():
    source = COMPOUND.read_text(encoding="utf-8")
    commit = source[source.index("async function commitIntelligence"):source.index("async function health")]
    assert "nayanet_collective_wisdom_for_event" not in commit

def test_learning_verification_is_the_projection_boundary():
    source = COMPOUND.read_text(encoding="utf-8")
    start = source.index("async function learningVerify")
    end = source.index("async function successor", start)
    body = source[start:end]
    assert 'status: "ACTIVE"' in body
    assert "learning_id" not in body or "evidence_id" in body
    # Fail-first contract: the verifier must eventually invoke the canonical
    # verified-learning projection after ACTIVE promotion.
    assert "nayanet_project_verified_learning_to_collective_wisdom" in body
