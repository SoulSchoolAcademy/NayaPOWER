from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PROTOCOL = ROOT / ".naya/operations/NAYA-UNDERSTANDING-FIDELITY-EXECUTION-PROTOCOL-V1.md"
TEAM = ROOT / ".naya/TEAM-NAYA/00-START-HERE-FOR-EVERY-NAYA.md"
BOOTSTRAP = ROOT / ".naya/memory/BOOTSTRAP.md"
CONTINUOUS = ROOT / ".naya/operations/NAYA-CONTINUOUS-EXECUTION-PROMPT-2026-09-25.md"
CONTINUATION = ROOT / ".naya/operations/NAYA-CONTINUATION-PROMPT-2026-09-25.md"
STATE = ROOT / ".naya/control-plane/STATE.json"
BATON = ROOT / ".naya/control-plane/BATON.json"
SMART_NOTE_CONTRACT = ROOT / ".naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md"


def test_understanding_protocol_is_discoverable_from_canonical_surfaces():
    assert PROTOCOL.exists()
    protocol = PROTOCOL.read_text(encoding="utf-8")
    assert "SOURCE-FIDELITY LAW" in protocol
    assert "UNDERSTANDING GATE" in protocol
    assert "NO-SKIM RULE" in protocol
    assert "SCORECARD INTEGRITY" in protocol
    assert "EXECUTION LAW" in protocol
    assert "HANDOFF LAW" in protocol

    for path in (STATE, BATON):
        text = path.read_text(encoding="utf-8")
        assert "NAYA-UNDERSTANDING-FIDELITY-EXECUTION-PROTOCOL-V1.md" in text

    assert "NAYA-UNDERSTANDING-FIDELITY-EXECUTION-PROTOCOL-V1.md" in CONTINUOUS.read_text(encoding="utf-8")
    assert "NAYA-UNDERSTANDING-FIDELITY-EXECUTION-PROTOCOL-V1.md" in CONTINUATION.read_text(encoding="utf-8")


def test_smart_note_identity_is_not_semantically_split():
    team = TEAM.read_text(encoding="utf-8")
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    contract = SMART_NOTE_CONTRACT.read_text(encoding="utf-8")

    assert "Smart Note ≠ Intelligent Block" not in team
    assert "Smart Note = Intelligent Block" in team
    assert "Smart Note = Intelligent Block" in bootstrap
    assert "Smart Note = Intelligent Block" in contract


def test_protocol_requires_fidelity_before_canonical_claims():
    protocol = PROTOCOL.read_text(encoding="utf-8")
    assert "FIDELITY NOT VERIFIED" in protocol
    assert "A canonical artifact must preserve meaning, not merely topic." in protocol
    assert "do not silently replace a score" in protocol
    assert "Do not stop at:" in protocol
