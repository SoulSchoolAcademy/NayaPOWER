from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "NAYANET/HUB/index.html"

def test_hub_has_canonical_intelligent_block_deep_link_contract():
    source = HUB.read_text(encoding="utf-8")
    assert "NayaHubDeepLink" in source
    assert "intelligent_block_id" in source
    assert "location.search" in source
    assert "/hub" in source

def test_hub_deep_link_resolves_exact_ib_or_source_event_without_fallback_projection():
    source = HUB.read_text(encoding="utf-8")
    assert re.search(r"NayaHubDeepLink.*resolve|resolve.*NayaHubDeepLink", source, re.S)
    assert "data-event-id" in source
    assert "data-intelligence-id" in source
    assert "DEEP_LINK_NOT_FOUND" in source


def test_runtime_exposes_owner_scoped_intelligent_block_retrieval_and_listing():
    runtime = ROOT / "NAYANET/HUB/public/assistant-runtime.js"
    source = runtime.read_text(encoding="utf-8")
    assert "retrieveIntelligentBlock" in source
    assert "listIntelligentBlocks" in source
    assert "eq('intelligent_block_id'" in source
    assert "eq('owner_id',session.user.id)" in source

def test_deep_link_uses_authenticated_runtime_and_preserves_identity_provenance():
    source = HUB.read_text(encoding="utf-8")
    assert "retrieveIntelligentBlock" in source
    assert "data-intelligence-id" in source
    assert "data-event-id" in source
    assert "data-source-event-id" in source
    assert "owner_id" not in source
