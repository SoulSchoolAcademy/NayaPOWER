"""Negative controls for the Smart Note publication uniqueness guard."""
import importlib.util
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "tools" / "check_smart_note_unique_ids.py"
spec = importlib.util.spec_from_file_location("note_unique", P)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

ROOT = "BRAIN/05-MEMORY/SMART-NOTES/2026/10/23/"
A = ROOT + "LEARNING/lessons/SN-1852/IB-SMART-NOTE-20261023-sn1852-first.md"
B = ROOT + "SYSTEM/lessons/SN-1852/IB-SMART-NOTE-20261023-sn1852-second.md"
C = ROOT + "SYSTEM/lessons/SN-1853/IB-SMART-NOTE-20261023-sn1853-another.md"
PAD = ROOT + "SYSTEM/lessons/SN-01852/IB-SMART-NOTE-20261023-sn01852-padded.md"


def test_duplicate_added_is_denied():
    assert g.check([A, B], [B]) == {1852: sorted([A, B])}


def test_zero_padding_cannot_evade_collision():
    assert g.check([A, PAD], [PAD]) == {1852: sorted([A, PAD])}


def test_distinct_numbers_allowed():
    assert not g.check([A, C], [C])


def test_legacy_untouched_duplicate_is_not_new_blocker():
    assert not g.check([A, B, C], [C])


def test_updates_same_path_are_not_duplicate_publications():
    assert not g.check([A], [A])


def test_arbitrary_non_note_files_ignored():
    assert not g.check([A, "BRAIN/OTHER/SN-1852/x.md"], ["BRAIN/OTHER/SN-1852/x.md"])
