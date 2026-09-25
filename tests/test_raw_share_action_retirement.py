from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "supabase/functions/nayanet-compound-intelligence/index.ts"

def test_compound_intelligence_share_action_is_fail_closed():
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("async function share(")
    end = source.index("async function supersede", start)
    block = source[start:end]
    assert "SMART_SHARE_RETIRED_USE_SMART_CONNECT_DERIVED_PUBLICATION" in block
    assert "nayanet_intelligence_publications" not in block
    assert "SHARED_BY_EXPLICIT_CONSENT" not in block
