"""Windows MAX_PATH corpus read/validation contract: real presence and refusal.

A registered projection must not be called missing solely because the
Windows checkout root is long. This tests the existing canonical Smart
Note retrieval validator and page hashing, not a new retrieval engine.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "smart_note_v2_windows_projection", ROOT / "tools" / "smart_note_v2.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


@pytest.mark.skipif(os.name != "nt", reason="Win32 MAX_PATH specific")
def test_corpus_validator_reads_long_valid_projection_and_refuses_bad_or_missing(tmp_path):
    rel = (
        Path("BRAIN/05-MEMORY/SMART-NOTES")
        / ("topic-" + "x" * 65)
        / ("subcategory-" + "y" * 65)
        / "IB-WINDOWS-VALIDATION.md"
    )
    native = tmp_path / rel
    assert len(str(native)) >= 260
    extended = Path("\\\\?\\" + str(native))
    extended.parent.mkdir(parents=True, exist_ok=True)
    payload = b"Canonical long-path Smart Note\\n"
    extended.write_bytes(payload)
    assert extended.is_file(), "control needs a genuinely existing file"

    expected = hashlib.sha256(payload).hexdigest()
    entry = {
        "intelligent_block_id": "IB-WINDOWS-VALIDATION",
        "projection_path": rel.as_posix(),
        "page_hash": expected,
        "lifecycle_state": "ACTIVE",
    }

    def registry():
        return {
            "schema": mod.INDEX_SCHEMA,
            "entries": [entry.copy()],
            "corpus_manifest_hash": mod._corpus_manifest_hash([entry]),
        }

    assert mod._page_file_hash(native) == expected
    mod._validate_index_against_corpus(registry(), root=tmp_path)

    entry["page_hash"] = "0" * 64
    with pytest.raises(SystemExit, match="INDEX_CORRUPT:PAGE_HASH_MISMATCH"):
        mod._validate_index_against_corpus(registry(), root=tmp_path)

    entry["page_hash"] = expected
    extended.unlink()
    with pytest.raises(SystemExit, match="INDEX_CORRUPT:PROJECTION_ABSENT"):
        mod._validate_index_against_corpus(registry(), root=tmp_path)
