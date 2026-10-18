"""w440 fix batch leg 1: test_backfill_apply_restamps_manifest.

Regression for the w440 finding — a schema migration that bypasses the
writer contract breaks the reader's anchor: the backfill's textual patch
mutated entries without re-stamping the manifest, leaving the freshness
anchor (check 7) silently stale.

The test enforces the writer contract: EVERY index-mutating migration
re-anchors corpus_manifest_hash in the same apply, on the post-mutation
entries. It proves the enforcement by the fail-leg pattern: seed a STALE
manifest (the pre-mutation shape) and assert the apply re-stamps it to the
post-mutation shape — an apply that skipped the restamp cannot pass.

Also proves the abort path: a deliberately failing apply (missing page)
refuses BEFORE any write lands — the index bytes on disk are untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

WORKTREE = Path(__file__).resolve().parents[1]  # repo root, never an absolute machine path
sys.path.insert(0, str(WORKTREE / "tools"))

import smart_note_v2 as m  # noqa: E402
import backfill_b51_index_hashes as bb  # noqa: E402

PAGES_DIR = ".naya/memory/smart-notes/pages"


def _make_corpus(tmp_path):
    """Temp repo layout: pages + index with a stale (pre-mutation) manifest."""
    pages = tmp_path / PAGES_DIR
    pages.mkdir(parents=True)
    (pages / "page1.md").write_text("# page one\n", encoding="utf-8")
    (pages / "page2.md").write_text("# page two\n", encoding="utf-8")
    entries = [
        {
            "intelligent_block_id": "IB-TEST-0001",
            "lifecycle_state": "ACTIVE",
            "projection_path": f"{PAGES_DIR}/page1.md",
            "title": "one",
        },
        {
            "intelligent_block_id": "IB-TEST-0002",
            "lifecycle_state": "ACTIVE",
            "projection_path": f"{PAGES_DIR}/page2.md",
            "title": "two",
        },
        {
            "intelligent_block_id": "IB-TEST-0003",
            "lifecycle_state": "RETIRED",
            "projection_path": None,
            "title": "retired",
        },
    ]
    # STALE seed: the manifest of the pre-mutation entries — exactly the
    # w440 failure shape (writer mutated without re-stamping).
    registry = {
        "schema": m.INDEX_SCHEMA,
        "entries": entries,
        "corpus_manifest_hash": m._corpus_manifest_hash(entries),
    }
    index_path = tmp_path / ".naya" / "memory" / "smart-notes" / "index.json"
    index_path.write_text(json.dumps(registry), encoding="utf-8")
    return index_path, tmp_path, registry


@pytest.fixture()
def corpus(tmp_path, monkeypatch):
    index_path, repo_root, registry = _make_corpus(tmp_path)
    # The validator resolves root at call time; re-point it at the temp
    # corpus (the function's own docstring blesses this for test harnesses).
    monkeypatch.setattr(m, "ROOT", repo_root)
    return index_path, repo_root, registry


def _reloaded(index_path):
    return json.loads(index_path.read_text(encoding="utf-8"))


def test_apply_restamps_manifest(corpus):
    """The w440 regression: a stale manifest must be re-anchored in the same apply."""
    index_path, repo_root, registry = corpus
    stale = registry["corpus_manifest_hash"]

    receipt = bb.apply(index_path, repo_root)

    after = _reloaded(index_path)
    recomputed = m._corpus_manifest_hash(after["entries"])
    assert after["corpus_manifest_hash"] == recomputed, (
        "apply mutated entries without re-stamping corpus_manifest_hash "
        "(writer contract violated: reader's anchor is stale)"
    )
    assert after["corpus_manifest_hash"] != stale, (
        "manifest unchanged by the apply — the migration left the pre-mutation anchor in place"
    )
    assert receipt["corpus_manifest_hash"] == after["corpus_manifest_hash"], (
        "receipt does not pin the post-mutation manifest"
    )
    # Pin-root enforcement: the receipt's tree_pin must anchor the INPUT
    # bytes the apply actually ran on (the harness root here). A pin
    # computed against the module REPO_ROOT silently resolves nothing in a
    # harness corpus and emits the empty-corpus pin (sha256 of "") —
    # a receipt that claims to anchor inputs it never covered.
    assert receipt["tree_pin"] == m._corpus_tree_pin(after["entries"], repo_root), (
        "receipt tree_pin does not anchor the corpus the apply ran on "
        "(wrong root → vacuous pin)"
    )


def test_apply_hashes_every_eligible_page(corpus):
    index_path, repo_root, _ = corpus
    receipt = bb.apply(index_path, repo_root)
    after = _reloaded(index_path)
    assert receipt["page_hashed"] == 2
    assert receipt["retired_unvalidatable"] == 1
    assert receipt["validator"] == "PASS"
    for e in after["entries"]:
        if e.get("projection_path"):
            assert isinstance(e.get("page_hash"), str) and e["page_hash"], e


def test_retired_entry_never_validated(corpus):
    index_path, repo_root, _ = corpus
    bb.apply(index_path, repo_root)
    after = _reloaded(index_path)
    retired = [e for e in after["entries"] if not e.get("projection_path")]
    assert len(retired) == 1
    assert retired[0]["index_validation"] == "RETIRED_UNVALIDATABLE"
    assert "page_hash" not in retired[0]


def test_abort_path_refuses_before_write(tmp_path, monkeypatch):
    """Fail leg: a broken corpus refuses BEFORE the write — disk bytes untouched."""
    index_path, repo_root, _ = _make_corpus(tmp_path)
    monkeypatch.setattr(m, "ROOT", repo_root)
    # Break the corpus: point an entry at a page that does not exist.
    registry = _reloaded(index_path)
    registry["entries"][0]["projection_path"] = f"{PAGES_DIR}/gone.md"
    index_path.write_text(json.dumps(registry), encoding="utf-8")
    before_bytes = index_path.read_bytes()

    with pytest.raises(SystemExit, match=r"BACKFILL_REFUSED:PROJECTION_ABSENT"):
        bb.apply(index_path, repo_root)

    assert index_path.read_bytes() == before_bytes, (
        "the refused apply wrote to the index before failing — "
        "the refusal must precede the write"
    )
