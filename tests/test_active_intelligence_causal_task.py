from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"


def test_active_intelligence_candidate_has_predeclared_causal_task():
    source = RUNTIME.read_text(encoding="utf-8")
    assert "active_intelligence_discipline" in source
    assert "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-001" in source
    assert "Persistence alone is memory, not proof of active intelligence." in source
    assert "Retrieved intelligence does not grant authority" in source
    assert "REQUIRE_TRUTH_AND_AUTHORITY_BOUNDARIES_BEFORE_APPLY" in source
    assert 'outcome_key: "governed_autonomy_applied"' in source


def test_unknown_lesson_still_has_no_applicable_capability():
    source = RUNTIME.read_text(encoding="utf-8")
    assert "NAYA-0001-NO-APPLICABLE-CAPABILITY" in source
    assert "NO_APPLICABLE_RETAINED_INTELLIGENCE" in source
