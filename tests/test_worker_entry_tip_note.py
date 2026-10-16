"""TIP NOTE parser regression tests (worker_entry.py, t2702 follow-up).

The 2026-10-15 ~19:03Z defect: a pass note quoted "## TIP NOTE" in prose and
split("## TIP NOTE") treated the quote as a section boundary, freezing the
entry gate tip at a stale prose SHA and misfiring WORK_AVAILABLE on every
run. The 09:29Z fix preferred the "(machine contract)" marker as a substring
anywhere in the section; the 09:31Z hardening anchors the heading AND the
marker to the heading line itself. These tests pin that behavior, including
the cases the substring-marker version still got wrong.

11 tests, all deterministic, no network.
Run: python3 -m pytest tests/test_worker_entry_tip_note.py -q
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load():
    spec = importlib.util.spec_from_file_location(
        "worker_entry", ROOT / "tools" / "worker_entry.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = _load()

STALE = "9f80e8eccfbe8256ec7ce069c61cd38cc86430ce"
LIVE = "e19a75d60f33972efee09718199b7be6643f356c"


def _read(text, tmp_path):
    p = tmp_path / "LIVE-PLAN.md"
    p.write_text(text)
    return mod.read_tip_from_plan(str(p))


def test_contract_marker_beats_prose_quote_after(tmp_path):
    """Prose quote AFTER the contract: mid-line "## TIP NOTE" mention must not
    become a section; the marked contract heading wins."""
    text = (
        "## TIP NOTE (machine contract — advanced by the director pass)\n"
        f"tip: {LIVE}\n"
        "\n"
        "## PASS NOTE (2026-10-15 ~19:03Z): the \"## TIP NOTE\" contract was\n"
        f"frozen at {STALE} while the live tip moved on.\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_contract_marker_beats_prose_quote_before(tmp_path):
    """Prose quote BEFORE the contract: same guarantee, position-independent."""
    text = (
        "## PASS NOTE (2026-10-15 ~19:03Z): the \"## TIP NOTE\" contract was\n"
        f"frozen at {STALE} while the live tip moved on.\n"
        "\n"
        "## TIP NOTE (machine contract — advanced by the director pass)\n"
        f"tip: {LIVE}\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_prose_marker_in_body_does_not_hijack(tmp_path):
    """The hardening case: a prose section whose BODY mentions the
    "(machine contract)" phrase must not steal the parse from the real
    contract heading. The 09:29Z substring version failed this."""
    text = (
        "## PASS NOTE: the \"## TIP NOTE\" machine contract below froze at\n"
        f"{STALE} — the machine contract marker is just prose here.\n"
        "\n"
        "## TIP NOTE (machine contract — advanced by the director pass)\n"
        f"tip: {LIVE}\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_indented_heading_like_line_is_not_a_boundary(tmp_path):
    """A line that merely looks like a heading but is indented (prose quote
    on its own line) must not delimit a section."""
    text = (
        "Some pass note quoting the heading on its own line:\n"
        "  ## TIP NOTE (machine contract)\n"
        f"  tip: {STALE}\n"
        "\n"
        "## TIP NOTE (machine contract — advanced by the director pass)\n"
        f"tip: {LIVE}\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_no_marker_falls_back_to_last_heading(tmp_path):
    """Without any marker, the last heading wins (contract appended last)."""
    text = (
        "## TIP NOTE\n"
        f"tip: {STALE}\n"
        "\n"
        "## TIP NOTE\n"
        f"tip: {LIVE}\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_first_marker_wins_among_marked(tmp_path):
    """If two headings carry the marker (should not happen), the first wins —
    deterministic, no silent last-write surprise."""
    text = (
        "## TIP NOTE (machine contract)\n"
        f"tip: {LIVE}\n"
        "\n"
        "## TIP NOTE (machine contract)\n"
        f"tip: {STALE}\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_no_headings_returns_none(tmp_path):
    assert _read(f"tip: {LIVE}\nno headings here\n", tmp_path) is None


def test_section_cut_at_next_heading(tmp_path):
    """A SHA in a LATER section must not leak into the TIP NOTE parse."""
    text = (
        "## TIP NOTE (machine contract)\n"
        "no sha in this section\n"
        "\n"
        "## OTHER SECTION\n"
        f"tip: {STALE}\n"
    )
    assert _read(text, tmp_path) is None


def test_midline_double_hash_does_not_cut_section(tmp_path):
    """A mid-line '##' mention inside the contract body must not truncate the
    section (the 09:29Z split('##') version cut here and lost the SHA)."""
    text = (
        "## TIP NOTE (machine contract)\n"
        "see ## Evidence for the receipts\n"
        f"tip: {LIVE}\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_short_sha_fallback(tmp_path):
    text = (
        "## TIP NOTE (machine contract)\n"
        "tip: e19a75d\n"
    )
    assert _read(text, tmp_path) == "e19a75d"


def test_forty_hex_preferred_over_short(tmp_path):
    text = (
        "## TIP NOTE (machine contract)\n"
        f"tip: {LIVE} (short e19a75d)\n"
    )
    assert _read(text, tmp_path) == LIVE


def test_missing_file_returns_none(tmp_path):
    assert mod.read_tip_from_plan("/nonexistent-dir-xyz/LIVE-PLAN.md") is None
