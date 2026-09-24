from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED = ROOT / "supabase/functions/naya-smart-feed/index.ts"
MIGRATION = ROOT / "supabase/migrations/20260924223000_harden_collective_publication_owner_boundary.sql"

def test_collective_feed_is_derived_only_and_fail_closed():
    source = FEED.read_text(encoding="utf-8")
    collective = source[source.index("if(stream==='collective')"):source.index("return json({ok:false,error:'INVALID_STREAM'}")]
    for marker in ("privacy_boundary:'derived-only'", "content:'NOT VERIFIED'", "source_event_id:null", "available_actions:[]", "truth_boundary:'Collective feed does not expose raw cognition events"):
        assert marker in collective
    assert "nayanet_cognition_events').select(fields).in('id',ids)" not in collective
    assert "publisher_identity:'private-by-default'" in collective

def test_collective_publication_update_cannot_repoint_to_another_owner_event():
    source = MIGRATION.read_text(encoding="utf-8")
    for marker in ("collective_publication_owner_update", "owner_id = (select auth.uid())", "e.user_id = (select auth.uid())", "e.id = intelligence_event_id"):
        assert marker in source
