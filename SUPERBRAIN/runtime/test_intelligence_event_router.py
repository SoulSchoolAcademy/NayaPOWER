from datetime import datetime, timezone

from intelligence_event_router import (
    DeliveryReceipt,
    EventType,
    IntelligenceEvent,
    Visibility,
    build_briefing,
    canonical_record_paths,
    daily_path,
    delivery_state,
    should_propagate,
)


def event(**overrides):
    base = dict(
        event_id="evt-001",
        event_type=EventType.INTELLIGENCE_CREATED,
        occurred_at="2026-09-21T14:00:00-07:00",
        source_naya_id="NAYA-001",
        source_surface="NayaPOWER",
        mission="NayaNET",
        summary="A material intelligence record was created.",
        why_it_matters="Future Nayas need the new learning.",
        required_awareness=True,
        authority_state="UNCHANGED",
        evidence_state="OBSERVED",
        visibility=Visibility.PRIVATE,
    )
    base.update(overrides)
    return IntelligenceEvent(**base)


def test_daily_layout_is_year_month_day_not_hour():
    assert daily_path("2026-09-21T23:59:59-07:00", "ACTIVITY.md") == (
        ".naya/INTELLIGENCE/2026/09/21/ACTIVITY.md"
    )


def test_all_daily_surfaces_share_one_day():
    paths = canonical_record_paths("2026-09-21T14:00:00-07:00")
    assert set(paths) == {"smart_notes", "activity", "notifications", "briefings"}
    assert all("/2026/09/21/" in value for value in paths.values())


def test_event_validation_requires_timezone():
    try:
        event(occurred_at="2026-09-21T14:00:00").validate()
    except ValueError as exc:
        assert "timezone" in str(exc)
    else:
        raise AssertionError("timezone-less event should fail closed")


def test_material_events_propagate():
    assert should_propagate(event())


def test_briefing_preserves_event_identity_and_structure():
    briefing = build_briefing(
        event(),
        what_changed="New intelligence entered the daily record.",
        who_needs_to_know=("LIVE_NAYAS", "INTELLIGENCE_HUB"),
        recommendation="Use this context during the next restoration.",
    )
    assert briefing.event_id == "evt-001"
    assert briefing.who_needs_to_know == ("LIVE_NAYAS", "INTELLIGENCE_HUB")


def test_delivery_is_idempotent_by_event_identity():
    receipts = (
        DeliveryReceipt("evt-001", "LIVE_NAYAS", "DELIVERED"),
        DeliveryReceipt("evt-001", "INTELLIGENCE_HUB", "DELIVERED"),
    )
    assert delivery_state(receipts) == "DELIVERED"


def test_partial_delivery_stays_visible():
    receipts = (
        DeliveryReceipt("evt-001", "LIVE_NAYAS", "DELIVERED"),
        DeliveryReceipt("evt-001", "INTELLIGENCE_HUB", "FAILED"),
    )
    assert delivery_state(receipts) == "PARTIAL"
