import pytest

from tools import smart_note_v2 as mod


def test_migrate_preserving_fields_keeps_unknown_nested_governed_fields():
    existing = {
        "schema": "naya.smart-note-capture.v1",
        "title": "Original",
        "intelligence": {
            "essence": "Keep this",
            "provenance": {"director": "shawn", "ratification": "rat-1"},
            "future_governed_field": {"falsifier": "must remain", "measurement": {"unit": "seconds"}},
            "successor": {"continuity_key": "cold-1"},
            "unknown_nested": {"a": [1, {"b": True}]},
        },
        "future_top_level": {"owner_rule": "do not drop me"},
    }

    result = mod.migrate_preserving_fields(
        existing,
        {"schema": "naya.smart-note-capture.v2", "intelligence": {"essence": "Updated"}},
    )

    assert result["document"]["schema"] == "naya.smart-note-capture.v2"
    assert result["document"]["intelligence"]["essence"] == "Updated"
    assert result["document"]["intelligence"]["future_governed_field"] == existing["intelligence"]["future_governed_field"]
    assert result["document"]["intelligence"]["unknown_nested"] == existing["intelligence"]["unknown_nested"]
    assert result["document"]["future_top_level"] == existing["future_top_level"]


def test_migrate_preserves_omitted_fields_without_a_removal_manifest():
    existing = {"title": "Original", "intelligence": {"provenance": {"source": "x"}, "keep": 1}}

    result = mod.migrate_preserving_fields(existing, {"title": "Updated"})

    assert result["document"]["title"] == "Updated"
    assert result["document"]["intelligence"]["provenance"] == {"source": "x"}
    assert result["document"]["intelligence"]["keep"] == 1
    assert result["receipt"]["removed_paths"] == []


def test_migrate_records_explicit_authorized_nonprotected_removal():
    existing = {"title": "Original", "metadata": {"obsolete": True, "keep": 1}}

    result = mod.migrate_preserving_fields(
        existing,
        {"title": "Updated"},
        explicit_removals=[{
            "path": "metadata.obsolete",
            "reason": "replaced by v2 field",
            "authority": "director:shawn",
        }],
    )

    assert "obsolete" not in result["document"]["metadata"]
    assert result["document"]["metadata"]["keep"] == 1
    assert result["receipt"]["removed_paths"] == ["metadata.obsolete"]
    assert result["receipt"]["removals"][0]["authority"] == "director:shawn"


def test_migrate_never_allows_protected_governed_field_removal():
    existing = {"provenance": {"director": "shawn"}, "measurement": {"metric": "value"}}

    with pytest.raises(mod.PreservationMigrationError, match="PROTECTED_FIELD_REMOVAL"):
        mod.migrate_preserving_fields(
            existing,
            {},
            explicit_removals=[{
                "path": "provenance.director",
                "reason": "cleanup",
                "authority": "director:shawn",
            }],
        )


def test_migrate_receipt_is_machine_readable_and_lists_changes():
    result = mod.migrate_preserving_fields(
        {"title": "Old", "metadata": {"keep": 1}},
        {"title": "New", "metadata": {"added": 2}},
    )

    receipt = result["receipt"]
    assert receipt["schema"] == "naya.smart-note-migration-receipt.v1"
    assert receipt["changed_paths"] == ["title"]
    assert receipt["added_paths"] == ["metadata.added"]
    assert receipt["removed_paths"] == []
