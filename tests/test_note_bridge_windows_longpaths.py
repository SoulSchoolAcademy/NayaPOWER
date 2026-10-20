"""Fail-first proof: the canonical note bridge must read real long Windows paths."""
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from note_bridge_live import load_live_corpus, parse_note_file


@pytest.mark.skipif(os.name != "nt", reason="Windows MAX_PATH regression")
def test_long_win32_note_is_parsed_from_live_corpus_and_missing_stays_missing(tmp_path):
    root = tmp_path / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
    normal = (root / "2026" / "10" / "20"
              / ("CATEGORY-" + "a" * 72)
              / ("TOPIC-" + "b" * 72)
              / "SN-9916"
              / "IB-SMART-NOTE-20261020-sn9916-windows-long-path.md")
    assert len(str(normal)) >= 260
    extended = Path(chr(92) * 2 + "?" + chr(92) + str(normal))
    extended.parent.mkdir(parents=True, exist_ok=True)
    extended.write_text(
        "# Windows long-path memory\n\n"
        "| Smart Note | SN-9916 |\n\n"
        "## IN A NUTSHELL\n\n"
        "Existing intelligence must remain available through the ordinary "
        "note-bridge on Windows, even when the absolute path is long.\n",
        encoding="utf-8",
    )
    assert extended.is_file(), "control: the file physically exists"
    parsed = parse_note_file(str(normal))
    assert parsed is not None, "present Win32 long path must be parsed"
    assert parsed["id"] == "SN-9916"
    assert parsed["path"] == str(normal), "original path provenance stays unchanged"
    notes, report = load_live_corpus(root=str(root))
    assert report["total_files"] == 1, report
    assert report["parsed"] == 1 and report["failed"] == 0, report
    assert notes[0].id == "SN-9916"

    extended.write_bytes(b"")
    assert parse_note_file(str(normal)) is None, "empty note must not be fabricated"
    notes, report = load_live_corpus(root=str(root))
    assert not notes
    assert report["total_files"] == 1 and report["failed"] == 1, report

    extended.unlink()
    assert parse_note_file(str(normal)) is None, "genuine absence must not be fabricated"
    notes, report = load_live_corpus(root=str(root))
    assert report["total_files"] == 0 and report["parsed"] == 0, report
