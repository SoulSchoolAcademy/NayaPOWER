from pathlib import Path

FEED = Path("supabase/functions/naya-smart-feed/index.ts")

def test_collective_feed_reads_collective_wisdom_not_publications():
    source = FEED.read_text(encoding="utf-8")
    start = source.index("if(stream==='collective')")
    end = source.index("return json({ok:false,error:'INVALID_STREAM'}", start)
    body = source[start:end]
    assert "nayanet_collective_wisdom" in body
    assert "nayanet_intelligence_publications" not in body
    assert "wisdom_claim" in body

def test_collective_feed_preserves_identity_and_publication_boundaries():
    source = FEED.read_text(encoding="utf-8")
    start = source.index("if(stream==='collective')")
    end = source.index("return json({ok:false,error:'INVALID_STREAM'}", start)
    body = source[start:end]
    assert "contributor_identity:'private-by-default'" in body
    assert ".eq('identity_visibility','private')" in body
    assert ".eq('source_visibility','derived_only')" in body
    assert ".eq('public_publication','separate')" in body
    assert "owner_id" not in body
