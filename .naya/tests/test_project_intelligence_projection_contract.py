"""Contract tests for canonical Project Intelligence projection (capability #3)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "supabase" / "functions" / "nayanet-compound-intelligence" / "index.ts"


def test_project_returns_explicit_projection_evidence():
    source = SOURCE.read_text(encoding="utf-8")
    assert "NAYANET_PROJECT_INTELLIGENCE_PROJECT_V2" in source
    assert "projection_evidence:" in source
    assert "source_event_id:" in source
    assert "index_id:" in source
    assert "projected_at:" in source


if __name__ == "__main__":
    test_project_returns_explicit_projection_evidence()
    print("1 passed")
