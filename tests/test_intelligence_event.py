from datetime import datetime, timezone

from intelligence.event import EventStore, IntelligenceEvent, EventState


def event(**overrides):
    data = {
        "event_id": "evt-1",
        "occurred_at": datetime(2026, 9, 26, 15, 30, tzinfo=timezone.utc),
        "event_type": "lesson",
        "topic": "continuity",
        "category": "system",
        "subject": "intelligent-event",
        "intelligence": {"insight": "Time is a retrieval dimension."},
        "nodes": ["KNOW", "CONNECT"],
        "source": "conversation",
        "state": EventState.DOCUMENTED,
    }
    data.update(overrides)
    return IntelligenceEvent(**data)


def test_event_embeds_time_and_semantic_dimensions_without_folder_encoding():
    e = event()
    assert (e.year, e.month, e.day) == (2026, 9, 26)
    assert e.topic == "continuity"
    assert e.category == "system"
    assert e.nodes == ("KNOW", "CONNECT")
    assert e.intelligence["insight"]


def test_store_retrieves_same_event_by_year_month_day_topic_category_and_node():
    store = EventStore()
    store.append(event())
    store.append(event(event_id="evt-2", occurred_at=datetime(2026, 9, 27, tzinfo=timezone.utc), topic="hub", nodes=["SELF"]))
    store.append(event(event_id="evt-3", occurred_at=datetime(2025, 9, 26, tzinfo=timezone.utc), category="project", topic="legacy", nodes=["SELF"]))

    assert [e.event_id for e in store.search(year=2026)] == ["evt-1", "evt-2"]
    assert [e.event_id for e in store.search(year=2026, month=9, day=26)] == ["evt-1"]
    assert [e.event_id for e in store.search(topic="continuity")] == ["evt-1"]
    assert [e.event_id for e in store.search(category="system")] == ["evt-1", "evt-2"]
    assert [e.event_id for e in store.search(node="CONNECT")] == ["evt-1"]


def test_store_preserves_one_provenance_chain_while_supporting_many_relationships():
    e = event(
        relationships={
            "derived_from": ["evt-source"],
            "reinforces": ["evt-prior"],
            "applies_to": ["hub"],
        },
        evidence=({"kind": "conversation", "ref": "turn-current"},),
    )
    store = EventStore()
    store.append(e)
    found = store.search(topic="continuity")[0]
    assert found.relationships["derived_from"] == ("evt-source",)
    assert found.relationships["reinforces"] == ("evt-prior",)
    assert found.evidence[0]["ref"] == "turn-current"


def test_event_state_is_explicit_and_not_inferred_from_storage():
    assert event(state=EventState.UNKNOWN).state is EventState.UNKNOWN
    assert event(state=EventState.VERIFIED).state is EventState.VERIFIED


def test_store_rejects_duplicate_canonical_event_ids():
    store = EventStore()
    store.append(event())
    try:
        store.append(event())
    except ValueError:
        return
    raise AssertionError("duplicate canonical event id must be rejected")
