from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "NAYANET" / "509-AAA-SMART-NOTES-01-09-CANONICAL.md"

EXPECTED_IDS = [f"NAYA-POWER-{n:02d}" for n in range(1, 10)]
EXPECTED_STATUS = "CANONICAL INTELLIGENCE - V1"

HEADING_RE = re.compile(r"^## SMART NOTE (\d{2}) ", re.MULTILINE)
SUBJECT_ID_RE = re.compile(r"^Subject ID: (NAYA-POWER-\d{2})$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status: (.+)$", re.MULTILINE)


def read_source() -> str:
    assert SOURCE.is_file(), f"missing canonical source: {SOURCE}"
    return SOURCE.read_text(encoding="utf-8")


def parse_blocks(text: str) -> list[tuple[str, list[str]]]:
    blocks: list[tuple[str, list[str]]] = []
    current_number: str | None = None
    current_lines: list[str] = []
    for raw in text.splitlines():
        match = HEADING_RE.match(raw.strip())
        if match:
            if current_number is not None:
                blocks.append((current_number, current_lines))
            current_number = match.group(1)
            current_lines = []
        elif current_number is not None:
            current_lines.append(raw)
    if current_number is not None:
        blocks.append((current_number, current_lines))
    return blocks


def subject_ids_in(text: str) -> list[str]:
    return [m.group(1) for m in SUBJECT_ID_RE.finditer(text)]


def statuses_in(text: str) -> list[str]:
    return [m.group(1) for m in STATUS_RE.finditer(text)]


def _assert_fail_closed_guards() -> str:
    text = read_source()
    assert HEADING_RE.search(text), "no Smart Note headings at all"
    assert SUBJECT_ID_RE.search(text), "no Subject ID lines at all"
    assert STATUS_RE.search(text), "no Status lines at all"
    return text


def test_exactly_nine_smart_note_blocks():
    blocks = parse_blocks(_assert_fail_closed_guards())
    assert len(blocks) == 9, f"expected 9 Smart Note blocks, found {len(blocks)}"


def test_block_ordering_is_01_to_09():
    blocks = parse_blocks(_assert_fail_closed_guards())
    numbers = [number for number, _ in blocks]
    assert numbers == [f"{n:02d}" for n in range(1, 10)], numbers


def test_exactly_nine_subject_id_lines():
    ids = subject_ids_in(_assert_fail_closed_guards())
    assert len(ids) == 9, f"expected 9 Subject ID lines, found {len(ids)}"


def test_exactly_nine_status_lines():
    statuses = statuses_in(_assert_fail_closed_guards())
    assert len(statuses) == 9, f"expected 9 Status lines, found {len(statuses)}"


def test_subject_ids_are_exact_expected_set():
    ids = subject_ids_in(_assert_fail_closed_guards())
    assert set(ids) == set(EXPECTED_IDS), ids


def test_no_duplicate_subject_ids():
    ids = subject_ids_in(_assert_fail_closed_guards())
    assert len(set(ids)) == len(ids), f"duplicate Subject IDs: {ids}"


def test_no_missing_subject_ids():
    ids = subject_ids_in(_assert_fail_closed_guards())
    missing = [expected for expected in EXPECTED_IDS if expected not in set(ids)]
    assert not missing, f"missing Subject IDs: {missing}"


def test_each_smart_note_holds_matching_subject_id():
    blocks = parse_blocks(_assert_fail_closed_guards())
    expected_by_number = {f"{n:02d}": f"NAYA-POWER-{n:02d}" for n in range(1, 10)}
    for number, lines in blocks:
        expected = expected_by_number[number]
        assert any(
            line.strip() == f"Subject ID: {expected}" for line in lines
        ), f"Smart Note {number} missing Subject ID {expected}"


def test_each_smart_note_holds_canonical_status():
    blocks = parse_blocks(_assert_fail_closed_guards())
    for number, lines in blocks:
        assert any(
            line.strip() == f"Status: {EXPECTED_STATUS}" for line in lines
        ), f"Smart Note {number} missing Status {EXPECTED_STATUS}"