"""Contract tests for canonical Project Intelligence retrieval.

Capability #2 must return provenance-bound intelligence, not merely matching
cognition rows. Authorization/project scoping remains fail-closed.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "supabase" / "functions" / "nayanet-compound-intelligence" / "index.ts"


def test_retrieve_contract_returns_provenance_bound_items():
    source = SOURCE.read_text(encoding="utf-8")
    assert 'schema: "NAYANET_PROJECT_INTELLIGENCE_RETRIEVE_V2"' in source
    assert "provenance:" in source
    assert "confidence:" in source
    assert "source_event_id:" in source
    assert "intelligent_block:" in source
    assert "index:" in source


def test_retrieve_contract_is_owner_and_project_scoped():
    source = SOURCE.read_text(encoding="utf-8")
    needle = '.eq("user_id", userId).eq("project_id", PROJECT)'
    assert needle in source
    assert '.eq("owner_id", userId)' in source
    assert '.eq("source_table", "nayanet_cognition_events")' in source


if __name__ == "__main__":
    tests = [
        test_retrieve_contract_returns_provenance_bound_items,
        test_retrieve_contract_is_owner_and_project_scoped,
    ]
    for test in tests:
        test()
    print("2 passed")
