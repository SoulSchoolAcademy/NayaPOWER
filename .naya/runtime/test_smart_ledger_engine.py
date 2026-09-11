import unittest

from smart_ledger_engine import (
    calculate_value,
    create_ledger_event,
    create_smart_note,
    determine_level,
    generate_smart_link,
    run_vertical_slice,
    verify_event,
)


class SmartLedgerEngineTests(unittest.TestCase):
    def test_end_to_end_vertical_slice(self):
        result = run_vertical_slice("A useful insight", "This is durable intelligence.", cumulative_points_before=45)
        self.assertEqual(result["ledger_event"]["event_type"], "SMART_NOTE_CREATED")
        self.assertEqual(result["ledger_event"]["status"], "verified")
        self.assertEqual(result["value_event"]["points"], 5)
        self.assertEqual(result["member"]["level"], 2)
        self.assertEqual(result["member"]["name"], "Emerging Member")
        self.assertEqual(result["smart_link"]["target_type"], "ledger_event")

    def test_value_requires_verification(self):
        note = create_smart_note("Test", "Content")
        event = create_ledger_event(note)
        with self.assertRaises(ValueError):
            calculate_value(event)

    def test_verification_requires_evidence(self):
        note = create_smart_note("Test", "Content")
        event = create_ledger_event(note)
        verified, receipt = verify_event(event)
        self.assertEqual(verified.status, "verified")
        self.assertEqual(receipt["verification_state"], "verified")

    def test_level_boundaries(self):
        self.assertEqual(determine_level(0)["level"], 1)
        self.assertEqual(determine_level(49)["level"], 1)
        self.assertEqual(determine_level(50)["level"], 2)
        self.assertEqual(determine_level(74999)["level"], 9)
        self.assertEqual(determine_level(75000)["level"], 10)

    def test_integrity_chain_changes_when_parent_changes(self):
        first = create_smart_note("First", "One")
        first_event = create_ledger_event(first)
        second = create_smart_note("Second", "Two")
        second_event = create_ledger_event(second, previous=first_event)
        self.assertEqual(second_event.previous_integrity_hash, first_event.integrity_hash)
        self.assertNotEqual(first_event.integrity_hash, second_event.integrity_hash)

    def test_smart_link_is_safe_reference(self):
        link = generate_smart_link("ledger_event", "ledger_123", access_class="authorized")
        self.assertEqual(link["target_ref"], "ledger_123")
        self.assertNotIn("actor_ref", link)


if __name__ == "__main__":
    unittest.main()
