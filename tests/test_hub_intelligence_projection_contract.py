from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "NAYANET" / "HUB" / "index.html"


def test_hub_is_canonical_read_only_intelligence_projection():
    source = HUB.read_text(encoding="utf-8")
    assert "NAYA-HUB-CANONICAL-PROJECTION-V1" in source
    assert "nayanet_intelligent_blocks" in source
    assert "nayanet_cognition_events" in source
    assert "RLS remains the authorization boundary" in source
    assert "service_role" not in source
    assert '.in("understanding_state",["VERIFIED","LEARNED"])' in source
    assert '.in("status",["DURABLE","RELEASED"])' in source
    assert '.eq("owner_scope","PRIVATE")' in source


def test_hub_preserves_sender_receiver_provenance_for_display():
    source = HUB.read_text(encoding="utf-8")
    for marker in (
        "source_event_ids",
        "provenance",
        "learning_id",
        "verification_runtime",
        "authority_grant_id",
        "COPY LESSON",
    ):
        assert marker in source


def test_hub_does_not_create_a_second_intelligence_pipeline():
    source = HUB.read_text(encoding="utf-8")
    assert ".insert(" not in source
    assert ".upsert(" not in source
    assert ".update(" not in source
    assert "intelligence_commit" not in source
