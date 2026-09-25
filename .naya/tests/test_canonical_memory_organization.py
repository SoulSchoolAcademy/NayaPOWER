#!/usr/bin/env python3
"""Regression tests for the canonical Smart Note filesystem boundary."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / ".naya" / "runtime" / "canonical_memory_organization.py"

spec = importlib.util.spec_from_file_location("canonical_memory_organization", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_valid_projection_is_accepted():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / ".naya/memory/smart-notes/2026/09/25/system/channel-constitution/IB-000123/smart-note.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "# SMART NOTE\n\n**Intelligent Block ID:** IB-000123\n\n"
            "## IN A NUTSHELL\n\nA canonical intelligence object.\n"
            "## DATE / TIME\n\n2026-09-25\n"
            "## WHAT\n\nWhat\n## WHY IT MATTERS\n\nWhy\n"
            "## HUMAN\n\nHuman\n## CHILD\n\nChild\n## GRANDMA\n\nGrandma\n"
            "## NAYA\n\nNaya\n## MACHINE\n\nMachine\n## WHAT WE LEARNED\n\nLesson\n"
            "## CONNECTIONS\n\nConnections\n## HOW TO APPLY\n\nApply\n"
            "## WHAT IT ULTIMATELY MEANS\n\nMeaning\n"
            "## WHAT'S IN IT FOR YOU / US\n\nValue\n## NEXT ACTION\n\nNext\n",
            encoding="utf-8",
        )
        errors = module.audit(root)
        assert errors == []


def test_smart_note_outside_canonical_namespace_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / "SUPERBRAIN/NIA-COMMUNICATION/2026/09/25/CHANNEL-CONSTITUTION.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "# SMART NOTE — Channel Constitution\n\n"
            "**Intelligent Block ID:** IB-000999\n\n"
            "## IN A NUTSHELL\n\nThis is canonical intelligence.\n",
            encoding="utf-8",
        )
        errors = module.audit(root)
        assert any("canonical Smart Note artifact outside" in error for error in errors)


def test_smart_note_md_outside_canonical_namespace_is_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / ".naya/memory/notes/2026/09/25/smart-note.md"
        path.parent.mkdir(parents=True)
        path.write_text("# SMART NOTE\n", encoding="utf-8")
        errors = module.audit(root)
        assert any("smart-note.md outside canonical Smart Note root" in error for error in errors)


if __name__ == "__main__":
    test_valid_projection_is_accepted()
    test_smart_note_outside_canonical_namespace_is_rejected()
    test_smart_note_md_outside_canonical_namespace_is_rejected()
    print("PASS — canonical Smart Note filesystem boundary regression GREEN")


def test_canonical_projection_identity_is_read_from_ib_path_segment():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / ".naya/memory/smart-notes/2026/09/25/system/channel-constitution/IB-000123/smart-note.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "# SMART NOTE\n\n**Intelligent Block ID:** IB-000123\n\n"
            + "".join(f"## {h}\n\nvalue\n" for h in module.HEADINGS),
            encoding="utf-8",
        )
        errors = module.audit(root)
        assert errors == []
