#!/usr/bin/env python3
"""TDD guardrails for the canonical Smart Note / Intelligent Block identity boundary."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from smart_note_transaction import (
    IB_ID_RE,
    _allocate_ib_id,
    canonical_smart_note_path,
    validate_note,
)


class CanonicalSmartNoteIdentityTests(unittest.TestCase):
    def test_local_identity_allocation_is_forbidden(self):
        with self.assertRaises(RuntimeError):
            _allocate_ib_id()

    def test_canonical_identity_is_receiver_issued(self):
        self.assertTrue(IB_ID_RE.fullmatch("IB-000860"))
        self.assertFalse(IB_ID_RE.fullmatch("IB:600a0bf0-bcf5-417b-b322-0f3b3802f109"))
        self.assertFalse(IB_ID_RE.fullmatch("SN-20260925-SOMETHING"))

    def test_repository_path_is_projection_of_authoritative_ib_identity(self):
        path = canonical_smart_note_path(
            "2026-09-25T14:00:25+00:00",
            "Canonical Smart Note",
            category="system",
            ib_id="IB-000860",
            root=Path("/tmp/naya-memory"),
        )
        self.assertEqual(
            str(path),
            "/tmp/naya-memory/2026/09/25/system/canonical-smart-note/IB-000860/smart-note.md",
        )

    def test_invalid_or_missing_identity_cannot_resolve_canonical_path(self):
        for value in ("", "IB-860", "IB:EVENT", "SN-001"):
            with self.assertRaises(ValueError):
                canonical_smart_note_path(
                    "2026-09-25T14:00:25+00:00",
                    "Canonical Smart Note",
                    ib_id=value,
                    root=Path("/tmp/naya-memory"),
                )

    def test_canonical_contract_requires_all_human_sections(self):
        note = {
            "in_a_nutshell": "summary",
            "date_time": "2026-09-25T14:00:25Z",
            "what": "what",
            "why_it_matters": "why",
            "human": "human",
            "child": "child",
            "grandma": "grandma",
            "naya": "naya",
            "machine": "machine",
            "learning": "learning",
            "how_it_connects": "connections",
            "how_to_use": "apply",
            "ultimate_meaning": "meaning",
            "value": "value",
            "next_action": "one action",
            "evidence": ["receipt"],
        }
        validate_note(note)

        missing = dict(note)
        del missing["ultimate_meaning"]
        with self.assertRaises(ValueError):
            validate_note(missing)


if __name__ == "__main__":
    unittest.main()
