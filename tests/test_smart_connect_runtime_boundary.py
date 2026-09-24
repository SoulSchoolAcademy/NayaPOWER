from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "supabase" / "migrations" / "20260924180000_smart_connect_participation_collective_wisdom_v1.sql").read_text(encoding="utf-8")
FUNCTION = (ROOT / "supabase" / "functions" / "nayanet-compound-intelligence" / "index.ts").read_text(encoding="utf-8")


def test_smart_connect_has_exactly_seven_doors():
    doors = ["github_app", "mcp", "rest_openapi", "webhooks", "sdk", "a2a", "mcp_apps"]
    assert all(f"'{door}'" in MIGRATION for door in doors)
    assert MIGRATION.count("door text") == 1


def test_connection_is_participation_not_publication_or_authority():
    assert "wisdom_sharing text not null default 'default'" in MIGRATION
    assert "identity_visibility text not null default 'private'" in MIGRATION
    assert "'publication','NOT_GRANTED'" in MIGRATION
    assert "'authority','UNCHANGED'" in MIGRATION
    assert "consent_state" not in MIGRATION


def test_denied_collective_learning_requires_smart_connect():
    assert "SMART_CONNECT_PARTICIPATION_REQUIRED" in MIGRATION
    gate = "if not v_participation then raise exception 'SMART_CONNECT_PARTICIPATION_REQUIRED'; end if;"
    assert gate in MIGRATION


def test_collective_wisdom_is_derived_and_identity_private():
    assert "source_visibility text not null default 'derived_only'" in MIGRATION
    assert "identity_visibility text not null default 'private'" in MIGRATION
    assert "public_publication text not null default 'separate'" in MIGRATION
    assert "-'identity'-'owner_id'-'raw_content'" in MIGRATION
    assert "nayanet_collective_wisdom_feed" in MIGRATION
    assert "owner_id" not in MIGRATION.split("create view public.nayanet_collective_wisdom_feed", 1)[1].split("grant select", 1)[0]


def test_intelligence_commit_authority_is_unchanged_and_participation_is_a_separate_gate():
    assert "if (!authorityGrantId) throw new Error('AUTHORITY_GRANT_ID_REQUIRED');" in FUNCTION
    assert "await validateIntelligenceCommitAuthority(client, authorityGrantId);" in FUNCTION
    assert "SMART_CONNECT_PARTICIPATION_REQUIRED" in FUNCTION
    assert "nayanet_collective_wisdom_for_event" in FUNCTION
    assert "case " + '"smart_connect"' + ": result=await smartConnect(client,user.id,body); break;" in FUNCTION


def test_no_per_event_learning_permission_was_reintroduced():
    assert 'consent_state' not in FUNCTION.split('async function share', 1)[0]
    assert 'smart_share' not in FUNCTION.lower()
    assert "smart connect participation" in FUNCTION.lower()
