#!/usr/bin/env python3
"""INT-001 RED acceptance tests.

These tests intentionally target the missing machine-checkable Smart Link
verification boundary. The verifier module does not exist yet on the RED
commit; the test must fail before implementation.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))

from smart_link_verifier import classify_smart_link  # noqa: E402


def run():
    note = Path(
        ".naya/memory/smart-notes/2026/09/25/system/"
        "nayapower-daily-scorecard/IB-001061/smart-note.md"
    )
    assert classify_smart_link(
        repo_path=note,
        reported_ib="IB-001061",
        receiver_persisted=True,
        canonical_ref="main",
    ) == "VERIFIED"

    missing = Path(
        ".naya/memory/smart-notes/2026/09/25/system/"
        "not-present/IB-999999/smart-note.md"
    )
    assert classify_smart_link(
        repo_path=missing,
        reported_ib="IB-999999",
        receiver_persisted=True,
        canonical_ref="main",
    ) == "MISSING"

    conflicted = Path("tests/fixtures/int001-conflicted-smart-note.md")
    assert classify_smart_link(
        repo_path=conflicted,
        reported_ib="IB-001061",
        receiver_persisted=True,
        canonical_ref="main",
    ) == "CONFLICTED"

    pending = Path(
        ".naya/memory/smart-notes/2026/09/25/system/"
        "not-present/IB-888888/smart-note.md"
    )
    assert classify_smart_link(
        repo_path=pending,
        reported_ib="IB-888888",
        receiver_persisted=True,
        canonical_ref="main",
    ) == "PENDING"

    print("INT-001 RED/GREEN acceptance tests complete")


if __name__ == "__main__":
    run()
