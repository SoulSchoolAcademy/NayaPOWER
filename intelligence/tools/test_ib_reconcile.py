#!/usr/bin/env python3
"""Negative-control tests for the IB canonical contract v1.1.

Proves the file-based <-> persisted mapping round-trips without losing:
owner, privacy/scope, evidence, relationships, applicability, truth state,
or successor effect. Also proves the failure modes fail LOUDLY (never silently).
"""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ib_reconcile import (
    CANONICAL_BLOCK_FIELDS,
    FILE_TO_PERSISTED_STATE,
    from_persisted_row,
    normalize_file_block,
    persisted_to_file_state,
    to_persisted_row,
    validate_v11,
)

# A realistic v1.0 file block (mirrors IB-0001 shape from the repo).
V10_BLOCK = {
    "id": "IB-0001",
    "schema_version": "1.0",
    "title": "Law One — Divine Oneness",
    "principle": "You are not separate from the team, the mission, or the people you serve.",
    "source": {"who": "Shawn", "when": "2026-10-11", "context": "Identity framing."},
    "evidence": [{"kind": "direct-word", "ref": "AGENTS.md: Law One", "note": "Root of all laws."}],
    "applicability": {
        "topics": ["identity", "ethics"],
        "situations": "Every decision.",
        "decisions": "Any choice affecting others.",
    },
    "verification_status": "APPLIED",
    "status_history": [{"status": "APPLIED", "at": "2026-10-11T20:30:00+00:00", "note": "Seed."}],
    "graduation": {"stage": "briefing", "next_step": "Keep injected.", "enforced_by": None},
    "supersedes": None,
    "superseded_by": None,
    "created_at": "2026-10-11T20:30:00+00:00",
    "updated_at": "2026-10-11T20:30:00+00:00",
}


def make_v11(**over):
    raw = copy.deepcopy(V10_BLOCK)
    raw.update(over)  # overrides apply BEFORE normalize so state derives correctly
    b = normalize_file_block(raw,
                             default_owner_id="owner-uuid-1234",
                             default_owner_scope="PRIVATE")
    b["intelligent_block_id"] = "IB-TEAM-20261011-law-one-divine-oneness"
    b["purpose"] = "Root identity law governing all decisions."
    b["authority_implications"] = "None — identity framing, no authority change."
    return b


class TestNormalize(unittest.TestCase):
    def test_legacy_id_alias_normalized(self):
        b = normalize_file_block(copy.deepcopy(V10_BLOCK))
        self.assertEqual(b["intelligent_block_id"], "IB-0001")
        self.assertNotIn("id", b)

    def test_legacy_supersession_aliases_normalized(self):
        b = normalize_file_block(copy.deepcopy(V10_BLOCK))
        self.assertIn("supersedes_block_id", b)
        self.assertIn("superseded_by_block_id", b)
        self.assertNotIn("supersedes", b)

    def test_provenance_seeded_from_source(self):
        b = normalize_file_block(copy.deepcopy(V10_BLOCK))
        self.assertEqual(b["provenance"]["source_who"], "Shawn")
        self.assertEqual(b["provenance"]["source_when"], "2026-10-11")

    def test_schema_version_bumped(self):
        b = normalize_file_block(copy.deepcopy(V10_BLOCK))
        self.assertEqual(b["schema_version"], "1.1")

    def test_empty_owner_preserved_for_loud_failure(self):
        # Must NOT invent an owner — validation must fail loudly.
        b = normalize_file_block(copy.deepcopy(V10_BLOCK), default_owner_id="")
        self.assertEqual(b["owner_id"], "")
        problems = validate_v11(b)
        self.assertTrue(any("owner_id" in p for p in problems))


class TestToPersisted(unittest.TestCase):
    def test_all_canonical_fields_present(self):
        row = to_persisted_row(make_v11())
        missing = [f for f in CANONICAL_BLOCK_FIELDS if f not in row]
        self.assertEqual(missing, [])

    def test_owner_privacy_provenance_survive(self):
        row = to_persisted_row(make_v11())
        self.assertEqual(row["owner_id"], "owner-uuid-1234")
        self.assertEqual(row["owner_scope"], "PRIVATE")
        self.assertTrue(row["provenance"])
        self.assertEqual(row["provenance"]["source_who"], "Shawn")

    def test_principle_lands_in_content_lesson(self):
        row = to_persisted_row(make_v11())
        self.assertEqual(row["content"]["lesson"], V10_BLOCK["principle"])

    def test_evidence_refs_derived(self):
        row = to_persisted_row(make_v11())
        self.assertIn("AGENTS.md: Law One", row["evidence_refs"])

    def test_state_mapping_applied(self):
        row = to_persisted_row(make_v11())  # verification_status=APPLIED
        self.assertEqual(row["understanding_state"], "CANDIDATE")
        self.assertEqual(row["status"], "DURABLE")

    def test_graduation_preserved_in_content(self):
        row = to_persisted_row(make_v11())
        self.assertEqual(row["content"]["graduation"]["stage"], "briefing")

    def test_empty_owner_raises_like_from_row(self):
        b = make_v11(owner_id="")
        with self.assertRaises(ValueError):
            to_persisted_row(b)

    def test_empty_provenance_raises_like_from_row(self):
        b = make_v11(provenance={})
        with self.assertRaises(ValueError):
            to_persisted_row(b)

    def test_empty_scope_raises_like_from_row(self):
        b = make_v11(owner_scope="")
        with self.assertRaises(ValueError):
            to_persisted_row(b)


class TestRoundTrip(unittest.TestCase):
    def _roundtrip(self, **over):
        original = make_v11(**over)
        row = to_persisted_row(original)
        back = from_persisted_row(row)
        return original, back

    def test_identity_survives(self):
        o, b = self._roundtrip()
        self.assertEqual(b["intelligent_block_id"], o["intelligent_block_id"])
        self.assertEqual(b["title"], o["title"])
        self.assertEqual(b["principle"], o["principle"])

    def test_owner_privacy_survive(self):
        o, b = self._roundtrip()
        self.assertEqual(b["owner_id"], o["owner_id"])
        self.assertEqual(b["owner_scope"], o["owner_scope"])

    def test_provenance_survives(self):
        o, b = self._roundtrip()
        self.assertEqual(b["provenance"]["source_who"], "Shawn")
        self.assertEqual(b["provenance"]["source_context"], "Identity framing.")

    def test_evidence_refs_survive(self):
        o, b = self._roundtrip()
        refs = [e.get("ref") for e in b["evidence"]]
        self.assertIn("AGENTS.md: Law One", refs)

    def test_state_survives(self):
        o, b = self._roundtrip()
        self.assertEqual(b["understanding_state"], o["understanding_state"])
        self.assertEqual(b["status"], o["status"])
        self.assertEqual(b["verification_status"], o["verification_status"])

    def test_graduation_and_new_fields_survive(self):
        o, b = self._roundtrip()
        self.assertEqual(b["graduation"]["stage"], "briefing")
        self.assertEqual(b["purpose"], o["purpose"])
        self.assertEqual(b["authority_implications"], o["authority_implications"])

    def test_supersession_chain_survives(self):
        o, b = self._roundtrip(supersedes_block_id="row-uuid-0009",
                              superseded_by_block_id=None)
        self.assertEqual(b["supersedes_block_id"], "row-uuid-0009")
        self.assertIsNone(b["superseded_by_block_id"])

    def test_successor_effect_flag_survives(self):
        # COMPOUNDED sets successor_reuse_proven in provenance; must survive.
        o, b = self._roundtrip(verification_status="COMPOUNDED")
        row = to_persisted_row(o)
        self.assertTrue(row["provenance"].get("successor_reuse_proven"))
        back = from_persisted_row(row)
        self.assertEqual(back["verification_status"], "COMPOUNDED")

    def test_double_roundtrip_stable(self):
        o, b = self._roundtrip()
        row2 = to_persisted_row(b)
        b2 = from_persisted_row(row2)
        self.assertEqual(b2["intelligent_block_id"], b["intelligent_block_id"])
        self.assertEqual(b2["principle"], b["principle"])
        self.assertEqual(b2["verification_status"], b["verification_status"])


class TestStateMapping(unittest.TestCase):
    def test_all_file_states_map(self):
        for vs, (us, st, _flags) in FILE_TO_PERSISTED_STATE.items():
            b = make_v11(verification_status=vs)
            # re-derive: normalize already set the pair from the ladder
            row = to_persisted_row(b)
            self.assertEqual(row["understanding_state"], us, vs)
            self.assertEqual(row["status"], st, vs)

    def test_reverse_mapping_roundtrips(self):
        for vs in ("UNVERIFIED", "APPLIED", "BEHAVIOR-CHANGE-PROVEN", "COMPOUNDED"):
            us, st, flags = FILE_TO_PERSISTED_STATE[vs]
            prov = dict(flags)
            self.assertEqual(persisted_to_file_state(us, st, prov), vs)

    def test_superseded_overrides(self):
        # A SUPERSEDED row keeps its file ladder position from history.
        prov = {"file_status_history": [{"verification_status": "COMPOUNDED"}]}
        self.assertEqual(persisted_to_file_state("VERIFIED", "SUPERSEDED", prov), "COMPOUNDED")

    def test_mismatched_state_caught_by_validation(self):
        b = make_v11()
        b["understanding_state"] = "VERIFIED"  # but verification_status=APPLIED
        problems = validate_v11(b)
        self.assertTrue(any("disagrees" in p for p in problems))


class TestRoundTripLosslessRichFields(unittest.TestCase):
    """#2386 (Naya 5 finding): the exporter must emit every field the
    importer expects. Rich file-form fields — evidence kind/type, per-item
    explanatory notes, detailed applicability, status history — must survive
    export -> import byte-exact, not degrade to refs/empty fallbacks."""

    def _roundtrip(self, **over):
        original = make_v11(**over)
        row = to_persisted_row(original)
        back = from_persisted_row(row)
        return original, row, back

    def test_exporter_carries_evidence_detail(self):
        _, row, _ = self._roundtrip()
        detail = row["provenance"].get("evidence_detail")
        self.assertIsInstance(detail, list)
        self.assertEqual(len(detail), 1)
        self.assertEqual(detail[0]["kind"], "direct-word")
        self.assertEqual(detail[0]["ref"], "AGENTS.md: Law One")
        self.assertEqual(detail[0]["note"], "Root of all laws.")

    def test_evidence_type_and_note_roundtrip_byte_exact(self):
        o, _, b = self._roundtrip()
        self.assertEqual(b["evidence"], o["evidence"])
        self.assertEqual(
            json.dumps(b["evidence"], sort_keys=True),
            json.dumps(o["evidence"], sort_keys=True),
        )

    def test_applicability_detail_roundtrip_byte_exact(self):
        o, row, b = self._roundtrip()
        self.assertIn("applicability_detail", row["provenance"])
        self.assertEqual(
            json.dumps(b["applicability"], sort_keys=True),
            json.dumps(o["applicability"], sort_keys=True),
        )
        self.assertEqual(b["applicability"]["topics"], ["identity", "ethics"])
        self.assertEqual(b["applicability"]["situations"], "Every decision.")
        self.assertEqual(b["applicability"]["decisions"], "Any choice affecting others.")

    def test_status_history_roundtrip_byte_exact(self):
        o, row, b = self._roundtrip()
        self.assertIn("file_status_history", row["provenance"])
        self.assertEqual(
            json.dumps(b["status_history"], sort_keys=True),
            json.dumps(o["status_history"], sort_keys=True),
        )
        self.assertEqual(b["status_history"][0]["note"], "Seed.")
        self.assertEqual(b["status_history"][0]["status"], "APPLIED")

    def test_roundtrip_is_fixed_point(self):
        # export -> import -> export -> import must be stable (idempotent).
        o, row1, b1 = self._roundtrip()
        row2 = to_persisted_row(b1)
        b2 = from_persisted_row(row2)
        for key in ("evidence", "applicability", "status_history", "provenance"):
            self.assertEqual(
                json.dumps(b2[key], sort_keys=True),
                json.dumps(b1[key], sort_keys=True),
                key,
            )
        self.assertEqual(
            json.dumps(row2["provenance"], sort_keys=True),
            json.dumps(row1["provenance"], sort_keys=True),
        )

    def test_exporter_does_not_mutate_caller_provenance(self):
        o = make_v11()
        before = copy.deepcopy(o["provenance"])
        to_persisted_row(o)
        self.assertEqual(o["provenance"], before)


class TestTamperedDetailFailsClosed(unittest.TestCase):
    """Adversarial: malformed rich-detail in a persisted row fails LOUDLY."""

    def _row(self):
        return to_persisted_row(make_v11())

    def test_tampered_evidence_detail_raises(self):
        row = self._row()
        row["provenance"]["evidence_detail"] = {"not": "a list"}
        with self.assertRaises(ValueError):
            from_persisted_row(row)

    def test_tampered_applicability_detail_raises(self):
        row = self._row()
        row["provenance"]["applicability_detail"] = ["not", "a", "dict"]
        with self.assertRaises(ValueError):
            from_persisted_row(row)

    def test_tampered_status_history_raises(self):
        row = self._row()
        row["provenance"]["file_status_history"] = "definitely-not-a-list"
        with self.assertRaises(ValueError):
            from_persisted_row(row)

    def test_missing_evidence_detail_degrades_to_refs_loudly_documented(self):
        # Legacy rows persisted before this fix have no evidence_detail;
        # the importer still works, but rich fields are NOT silently
        # invented — refs survive, kind/note come back empty.
        row = self._row()
        del row["provenance"]["evidence_detail"]
        back = from_persisted_row(row)
        self.assertEqual([e.get("ref") for e in back["evidence"]],
                         ["AGENTS.md: Law One"])
        self.assertEqual(back["evidence"][0]["note"], "")


class TestNegativeControls(unittest.TestCase):
    """Adversarial: prove the mapping cannot silently corrupt."""
    def test_tampered_provenance_detected(self):
        o = make_v11()
        row = to_persisted_row(o)
        row["provenance"] = {}  # attacker wipes provenance
        with self.assertRaises(ValueError):
            # re-export path enforces non-empty provenance
            to_persisted_row(from_persisted_row({**row, "provenance": {"x": 1},
                                                "owner_id": "", "owner_scope": "",
                                                "block_id": None, "subject_id": None,
                                                "version": 1, "source_event_ids": [],
                                                "evidence_refs": [], "applicable_scope": "",
                                                "created_at": "", "updated_at": "",
                                                "schema_version": "1.1",
                                                "title": "", "block_type": "",
                                                "content": {}, "status": "",
                                                "understanding_state": "",
                                                "supersedes_block_id": None,
                                                "superseded_by_block_id": None,
                                                "intelligent_block_id": "x"}))

    def test_missing_canonical_field_raises(self):
        row = to_persisted_row(make_v11())
        del row["owner_id"]
        with self.assertRaises(ValueError):
            from_persisted_row(row)

    def test_invalid_scope_rejected(self):
        b = make_v11(owner_scope="EVERYONE")
        problems = validate_v11(b)
        self.assertTrue(any("owner_scope" in p for p in problems))

    def test_legacy_fields_rejected_on_write(self):
        b = make_v11()
        b["id"] = "IB-0001"  # legacy field snuck back in
        problems = validate_v11(b)
        self.assertTrue(any("legacy field" in p for p in problems))


if __name__ == "__main__":
    unittest.main(verbosity=2)
