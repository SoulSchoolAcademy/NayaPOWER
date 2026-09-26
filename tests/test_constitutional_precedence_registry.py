from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
REGISTRY = REPO / ".naya" / "control-plane" / "CANONICAL-CONTRACT-REGISTRY.md"
STATE = REPO / ".naya" / "control-plane" / "STATE.json"


def _cc000_block(text: str) -> str:
    start = text.index("### CC-000:")
    end = text.index("### CC-001:", start)
    return text[start:end]


def test_constitutional_precedence_conflict_fails_closed():
    registry = _cc000_block(REGISTRY.read_text(encoding="utf-8"))
    state = STATE.read_text(encoding="utf-8")

    assert "CONFLICTED — HUMAN RATIFICATION BOUNDARY" in registry
    assert "precedence against the repository's existing Runtime Constitution remains unresolved" in registry
    assert ".naya/codex/11-RUNTIME-CONSTITUTION.md" in registry
    assert ".naya/codex/11-RUNTIME-CONSTITUTION.md" in state
    assert "None (supreme authority)" not in registry


def test_registry_does_not_claim_constitutional_supersession_without_record():
    registry = _cc000_block(REGISTRY.read_text(encoding="utf-8"))
    assert "No explicit supersession record" in registry
    assert "No machine or Naya inference may silently resolve this" in registry
