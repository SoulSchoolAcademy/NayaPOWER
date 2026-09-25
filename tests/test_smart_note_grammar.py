from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "NAYANET" / "509-AAA-SMART-NOTES-01-09-CANONICAL.md"

CANONICAL_SECTIONS = [
    "IN A NUTSHELL",
    "HUMAN NOTE",
    "CHILD",
    "GRANDMA NOTE",
    "NAYA NOTE",
    "MACHINE NOTE",
    "ADAPTIVE LEARNING",
    "WHAT IT MEANS",
    "WHAT'S IN IT FOR YOU?",
]

EXPECTED_SUBJECT_BY_NUMBER = {n: f"NAYA-POWER-{n:02d}" for n in range(1, 10)}
EXPECTED_STATUS = "CANONICAL INTELLIGENCE - V1"

NOTE_RE = re.compile("^## SMART NOTE (\\d{2})\\s+\u2014\\s+(.*)$", re.MULTILINE)
SECTION_RE = re.compile(r"^### (.+)$", re.MULTILINE)
SUBJECT_ID_RE = re.compile(r"^Subject ID: (\S+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status: (.+)$", re.MULTILINE)
NOTES_TEMPLATE = (
    "## SMART NOTE {number} \u2014 TITLE\nSubject ID: {subject}\nStatus: {status}\n{sections}"
)

HTML_CONSUMER_SECTION_ALIASES = {
    "nutshell": ["nutshell"],
    "human": ["human note", "human"],
    "child": ["child"],
    "grandma": ["grandma note", "grandma"],
    "naya": ["naya note", "naya"],
    "machine": ["machine note", "machine"],
    "learning": ["adaptive learning", "learning"],
    "meaning": ["what it means", "meaning"],
    "benefits": ["what's in it for you?", "what's in it for you", "benefits"],
}


def read_source() -> str:
    assert SOURCE.is_file(), f"missing canonical source: {SOURCE}"
    return SOURCE.read_text(encoding="utf-8")


def parse_notes(text: str) -> list[dict]:
    notes: list[dict] = []
    current: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        head = NOTE_RE.match(line)
        if head:
            if current is not None:
                notes.append(current)
            current = {
                "number": int(head.group(1)),
                "title": head.group(2),
                "head": [],
                "sections": [],
            }
            continue
        if current is None:
            continue
        section = SECTION_RE.match(line)
        if section:
            current["sections"].append({"name": section.group(1), "body": []})
        elif current["sections"]:
            current["sections"][-1]["body"].append(raw)
        else:
            current["head"].append(raw)
    if current is not None:
        notes.append(current)
    for note in notes:
        head_text = "\n".join(note["head"])
        subject = SUBJECT_ID_RE.search(head_text)
        status = STATUS_RE.search(head_text)
        note["subject_id"] = subject.group(1) if subject else None
        note["status"] = status.group(1) if status else None
        note["bodies"] = {
            section["name"]: "\n".join(section["body"]).strip()
            for section in note["sections"]
        }
    return notes


def flag_issues(text: str) -> list[str]:
    notes = parse_notes(text)
    issues: list[str] = []
    if not notes:
        return ["grammar produced no notes"]
    if len(notes) != 9:
        issues.append(f"expected 9 notes, found {len(notes)}")
    if [note["number"] for note in notes] != [n for n in range(1, 10)]:
        issues.append(
            f"note numbers not sequential 01..09: {[note['number'] for note in notes]}"
        )
    for note in notes:
        number = note["number"]
        if number not in EXPECTED_SUBJECT_BY_NUMBER:
            issues.append(f"note number out of range: {number}")
            continue
        if note["subject_id"] != EXPECTED_SUBJECT_BY_NUMBER[number]:
            issues.append(f"note {number:02d} Subject ID mismatch: {note['subject_id']}")
        if note["status"] != EXPECTED_STATUS:
            issues.append(f"note {number:02d} Status mismatch: {note['status']}")
        names = [section["name"] for section in note["sections"]]
        if names != CANONICAL_SECTIONS:
            issues.append(f"note {number:02d} section set/order invalid: {names}")
        seen: set[str] = set()
        for name in names:
            if name in seen:
                issues.append(f"note {number:02d} duplicate section: {name}")
            seen.add(name)
        for name in CANONICAL_SECTIONS:
            if not note["bodies"].get(name):
                issues.append(f"note {number:02d} empty required section: {name}")
        for name in names:
            if name not in CANONICAL_SECTIONS:
                issues.append(f"note {number:02d} unknown section: {name}")
    return issues


def _canonical() -> str:
    text = read_source()
    assert NOTE_RE.search(text), "no Smart Note headings at all"
    assert SECTION_RE.search(text), "no section headings at all"
    assert SUBJECT_ID_RE.search(text), "no Subject ID lines at all"
    assert STATUS_RE.search(text), "no Status lines at all"
    return text


def _synthetic(template: str = NOTES_TEMPLATE) -> str:
    return "\n\n".join(
        template.format(
            number=f"{n:02d}",
            subject=EXPECTED_SUBJECT_BY_NUMBER[n],
            status=EXPECTED_STATUS,
            sections="\n".join(
                f"### {name}\nBody {name} {n:02d}." for name in CANONICAL_SECTIONS
            ),
        )
        for n in range(1, 10)
    )


def test_legacy_509_reference_corpus_is_parseable():
    text = _canonical()
    assert parse_notes(text), "legacy 509 reference corpus must parse into notes"


def test_legacy_reference_count_is_nine():
    notes = parse_notes(_canonical())
    assert len(notes) == 9, len(notes)


def test_legacy_reference_numbers_are_sequential_01_to_09():
    notes = parse_notes(_canonical())
    assert [note["number"] for note in notes] == list(range(1, 10))


def test_legacy_reference_identity_present_per_note():
    for note in parse_notes(_canonical()):
        assert note["subject_id"] == EXPECTED_SUBJECT_BY_NUMBER[note["number"]]
        assert note["status"] == EXPECTED_STATUS


def test_legacy_reference_identity_block_precedes_content_sections():
    for note in parse_notes(_canonical()):
        head_text = "\n".join(note["head"])
        assert f"Subject ID: {note['subject_id']}" in head_text
        assert f"Status: {note['status']}" in head_text


def test_legacy_reference_sections_present_complete():
    for note in parse_notes(_canonical()):
        names = [section["name"] for section in note["sections"]]
        assert set(names) == set(CANONICAL_SECTIONS), names


def test_legacy_reference_section_order_is_stable():
    for note in parse_notes(_canonical()):
        names = [section["name"] for section in note["sections"]]
        assert names == CANONICAL_SECTIONS, names


def test_legacy_reference_no_empty_sections():
    for note in parse_notes(_canonical()):
        for name in CANONICAL_SECTIONS:
            assert note["bodies"][name].strip(), (note["number"], name)


def test_legacy_reference_no_duplicate_or_unknown_sections():
    for note in parse_notes(_canonical()):
        names = [section["name"] for section in note["sections"]]
        assert len(set(names)) == len(names), names
        assert all(name in CANONICAL_SECTIONS for name in names)


def test_legacy_reference_grammar_consistent_across_all_notes():
    parsings = parse_notes(_canonical())
    first = [section["name"] for section in parsings[0]["sections"]]
    for note in parsings[1:]:
        names = [section["name"] for section in note["sections"]]
        assert names == first, names


def test_html_consumer_semantic_keys_resolvable():
    aliases = {
        key: {alias for alias in value}
        for key, value in HTML_CONSUMER_SECTION_ALIASES.items()
        if key != "nutshell"
    }
    for note in parse_notes(_canonical()):
        names = {name.lower() for name in note["bodies"]}
        for key, candidates in aliases.items():
            assert candidates & names, f"note {note['number']:02d} missing semantic key {key}"


def test_html_consumer_nutshell_alias_divergence_recorded():
    aliases = {alias for alias in HTML_CONSUMER_SECTION_ALIASES["nutshell"]}
    assert "in a nutshell" not in aliases
    for note in parse_notes(_canonical()):
        assert "IN A NUTSHELL" in note["bodies"]


def test_fail_closed_wrong_note_count():
    text = _synthetic() + "\n\n## SMART NOTE 10 \u2014 EXTRA\nSubject ID: NAYA-POWER-10\nStatus: CANONICAL INTELLIGENCE - V1\n### IN A NUTSHELL\nBody."
    issues = flag_issues(text)
    assert any("expected 9 notes" in issue for issue in issues)


def test_fail_closed_missing_required_section():
    text = _synthetic()
    broken = text.replace("### HUMAN NOTE\nBody HUMAN NOTE 01.", "### HUMAN NOTE", 1)
    issues = flag_issues(broken)
    assert any("empty required section: HUMAN NOTE" in issue for issue in issues)


def test_fail_closed_unknown_section():
    text = _synthetic()
    broken = text.replace(
        "Body IN A NUTSHELL 01.",
        "Body IN A NUTSHELL 01.\n### RANDOM SECTION\nSneaky extra.",
        1,
    )
    issues = flag_issues(broken)
    assert any("unknown section: RANDOM SECTION" in issue for issue in issues)


def test_fail_closed_duplicate_section():
    text = _synthetic()
    broken = text.replace(
        "### IN A NUTSHELL\nBody IN A NUTSHELL 01.",
        "### IN A NUTSHELL\nBody IN A NUTSHELL 01.\n### IN A NUTSHELL\ndup",
        1,
    )
    issues = flag_issues(broken)
    assert any("duplicate section: IN A NUTSHELL" in issue for issue in issues)


def test_fail_closed_out_of_order_sections():
    standard = _synthetic()
    swapped = ["IN A NUTSHELL", "CHILD", "HUMAN NOTE"] + CANONICAL_SECTIONS[3:]
    first_block = (
        "## SMART NOTE 01 \u2014 TITLE\nSubject ID: NAYA-POWER-01\nStatus: CANONICAL INTELLIGENCE - V1\n"
        + "\n".join(f"### {name}\nBody {name} 01." for name in swapped)
    )
    tail = standard[standard.index("## SMART NOTE 02 \u2014 TITLE"):]
    broken = first_block + "\n\n" + tail
    issues = flag_issues(broken)
    assert any("section set/order invalid" in issue for issue in issues)


def test_fail_closed_missing_identity():
    text = _synthetic().replace("Subject ID: NAYA-POWER-01\n", "", 1)
    issues = flag_issues(text)
    assert any("Subject ID mismatch" in issue for issue in issues)


def test_fail_closed_non_sequential_numbers():
    text = _synthetic().replace(
        "## SMART NOTE 04 \u2014 TITLE", "## SMART NOTE 06 \u2014 TITLE", 1
    )
    issues = flag_issues(text)
    assert any("not sequential" in issue for issue in issues)