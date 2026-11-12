"""Ensure the consensus gate recognizes the already-used Naya GPT-6 seat label."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_merge_consensus import author_seat_of, seat_of  # noqa: E402


def test_existing_naya_gpt6_seat_label_is_recognized():
    assert seat_of("Seat: Naya GPT-6") == "Naya Gpt-6"
    assert author_seat_of("Seat: Naya GPT-6") == "Naya Gpt-6"
