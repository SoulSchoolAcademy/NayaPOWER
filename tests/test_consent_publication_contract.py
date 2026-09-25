from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOUND = ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts"
SMART_FEED = ROOT / "supabase/functions/naya-smart-feed/index.ts"
PUBLICATION_MIGRATION = ROOT / "supabase/migrations/20260925010000_require_explicit_consensus_publication_rpc_v1.sql"
CONSENT_MIGRATION = ROOT / "supabase/migrations/20260925020000_require_explicit_smart_connect_consent_v1.sql"
ATTACK4 = ROOT / ".github/workflows/verify-attack4-live-intelligence-receipt.yml"
UAI = ROOT / ".github/workflows/verify-uai-authority-parity-live.yml"


def test_publication_paths_use_authority_and_consent_rpc():
    compound = COMPOUND.read_text(encoding="utf-8")
    smart_feed = SMART_FEED.read_text(encoding="utf-8")
    assert "nayanet_publish_intelligence" in compound
    assert 'consentState !== "explicit"' in compound
    assert 'from("nayanet_intelligence_publications").upsert' not in compound
    assert "nayanet_publish_intelligence" in smart_feed
    assert "nayanet_revoke_intelligence_publication" in smart_feed
    assert "p_consent_state:'explicit'" in smart_feed
    assert "from('nayanet_intelligence_publications').upsert" not in smart_feed
    assert "from('nayanet_intelligence_publications').update" not in smart_feed


def test_publication_migration_revokes_direct_mutation_and_revalidates_authority():
    source = PUBLICATION_MIGRATION.read_text(encoding="utf-8")
    for marker in (
        "nayanet_publish_intelligence",
        "nayanet_validate_authority_grant",
        "smart_feed_publish",
        "EXPLICIT_CONSENT_REQUIRED",
        "PUBLISH_AUTHORITY_REQUIRED",
        "revoke insert,update,delete on table public.nayanet_intelligence_publications from anon, authenticated",
        "nayanet_revoke_intelligence_publication",
    ):
        assert marker in source
    assert "'status','SHARED_BY_EXPLICIT_CONSENT'" in source


def test_smart_connect_requires_explicit_participation_consent():
    source = CONSENT_MIGRATION.read_text(encoding="utf-8")
    for marker in (
        "consent_state text not null default 'pending'",
        "SMART_CONNECT_CONSENT_REQUIRED",
        "SMART_CONNECT_BINDING_CONSENT_REQUIRED",
        "create trigger nayanet_smart_connect_consent_boundary",
        "p_consent_state text",
        "consent_state='explicit'",
        "consent_state='revoked'",
    ):
        assert marker in source
    assert "tg_op='UPDATE'" in source


def test_smart_connect_proofs_pass_consent_explicitly():
    attack4 = ATTACK4.read_text(encoding="utf-8")
    uai = UAI.read_text(encoding="utf-8")
    assert attack4.count("p_consent_state:'explicit'") == 2
    assert '"p_consent_state":"explicit"' in uai
    assert "body:JSON.stringify({p_door:'mcp',p_consent_state:'explicit'})" in attack4
