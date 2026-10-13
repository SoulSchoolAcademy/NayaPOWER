"""Fail-closed acceptance tests for the brain index reader (B-51 class).

B-51 (Shawn, P0): "a wrong answer with no error signal is worse than no
answer at all, because it teaches confidently." The reader used to accept
whatever bytes sat on disk for BRAIN/NAYAPOWER-BRAIN-INDEX.json. These tests
prove the guard now refuses instead:

  FRESH    - corpus bytes == manifest blob SHAs, receipt files == committed
             tree: the index was regenerated against exactly this corpus.
  STALE    - a corpus file drifted from the manifest (regen needed).
  TAMPERED - the index/receipt files on disk differ from the committed tree
             (hand-edited index, never regenerate-and-commit).

Red-first: these were written before kernel/brain_index_guard.py existed, so
the first run fails on the missing module (the open wound: no guard at all).
"""

import json
import subprocess
from pathlib import Path

import pytest

from kernel.brain_index_guard import (
    StaleBrainIndexError,
    TamperedBrainIndexError,
    UnverifiableBrainIndexError,
    inspect_index,
    load_index_failclosed,
)

RECEIPTS = (
    "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
    "BRAIN/REAL-TREE.json",
    "BRAIN/REAL-TREE.md",
)


def _git(root: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def make_fixture(root: Path) -> Path:
    """Minimal git checkout: one corpus file + the three receipt files committed."""
    (root / "BRAIN").mkdir(parents=True)
    corpus = root / "BRAIN" / "11-KNOWLEDGE-0001.md"
    corpus.write_text("canonical knowledge v1\n", encoding="utf-8")
    (root / "BRAIN/REAL-TREE.md").write_text("tree receipt\n", encoding="utf-8")
    (root / "BRAIN/NAYAPOWER-BRAIN-INDEX.json").write_text('{"nine_nodes": []}\n', encoding="utf-8")
    blob = _git(root, "hash-object", "--", str(corpus))
    manifest = {
        "receipt_basis_commit": "fixture",
        "files": [{"path": "BRAIN/11-KNOWLEDGE-0001.md", "blob_sha": blob, "size": corpus.stat().st_size}],
    }
    (root / "BRAIN/REAL-TREE.json").write_text(json.dumps(manifest), encoding="utf-8")
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "fixture")
    # stamp the real basis commit now that HEAD exists
    manifest["receipt_basis_commit"] = _git(root, "rev-parse", "HEAD")
    (root / "BRAIN/REAL-TREE.json").write_text(json.dumps(manifest), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "manifest")
    # honest FRESH state: the manifest's basis is the commit that carries it
    manifest["receipt_basis_commit"] = _git(root, "rev-parse", "HEAD")
    (root / "BRAIN/REAL-TREE.json").write_text(json.dumps(manifest), encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "manifest", "--amend", "--no-edit")
    return root


def test_fresh_fixture_passes_and_loads(tmp_path):
    root = make_fixture(tmp_path)
    receipt = inspect_index(root)
    assert receipt["verdict"] == "FRESH"
    assert len(receipt["corpus_fingerprint"]) == 64
    assert len(receipt["receipt_basis_commit"]) == 40
    # the fixture's basis is the corpus commit, not the manifest commit: the
    # receipt distinguishes "regenerated against exactly this commit" from
    # "regenerated against an older corpus" without either being stale.
    assert receipt["basis_matches_head"] is False
    assert load_index_failclosed(root) == {"nine_nodes": []}


def test_mutated_corpus_is_stale_not_silent(tmp_path):
    """The forgery probe: corpus moves under a committed index -> refuse loudly."""
    root = make_fixture(tmp_path)
    with (root / "BRAIN/11-KNOWLEDGE-0001.md").open("a", encoding="utf-8") as fh:
        fh.write("forged addition\n")
    with pytest.raises(StaleBrainIndexError) as exc:
        inspect_index(root)
    assert "BRAIN/11-KNOWLEDGE-0001.md" in str(exc.value)
    with pytest.raises(StaleBrainIndexError):
        load_index_failclosed(root)


def test_hand_edited_index_is_tampered_not_stale(tmp_path):
    """Index edited on disk without regen+commit -> TAMPERED, distinct from STALE."""
    root = make_fixture(tmp_path)
    with (root / "BRAIN/NAYAPOWER-BRAIN-INDEX.json").open("a", encoding="utf-8") as fh:
        fh.write('{"forged": true}\n')
    with pytest.raises(TamperedBrainIndexError) as exc:
        inspect_index(root)
    assert "BRAIN/NAYAPOWER-BRAIN-INDEX.json" in str(exc.value)
    with pytest.raises(TamperedBrainIndexError):
        load_index_failclosed(root)


def test_deleted_corpus_file_is_stale(tmp_path):
    root = make_fixture(tmp_path)
    (root / "BRAIN/11-KNOWLEDGE-0001.md").unlink()
    with pytest.raises(StaleBrainIndexError):
        inspect_index(root)


def test_non_git_directory_fails_closed(tmp_path):
    (tmp_path / "BRAIN").mkdir()
    with pytest.raises(UnverifiableBrainIndexError):
        inspect_index(tmp_path)


def test_reader_refuses_stale_corpus_through_load_and_validate(tmp_path):
    """The wire-in: load_and_validate_brain itself refuses, not just the guard."""
    from kernel.brain_registry import load_and_validate_brain

    root = make_fixture(tmp_path)
    with (root / "BRAIN/11-KNOWLEDGE-0001.md").open("a", encoding="utf-8") as fh:
        fh.write("forged addition\n")
    report = load_and_validate_brain(root)
    assert report["ok"] is False
    assert report["guard_verdict"] == "REFUSED"
    assert any("brain_index_refused:StaleBrainIndexError" in e for e in report["errors"])


def test_reader_refuses_tampered_index_through_load_and_validate(tmp_path):
    from kernel.brain_registry import load_and_validate_brain

    root = make_fixture(tmp_path)
    with (root / "BRAIN/NAYAPOWER-BRAIN-INDEX.json").open("a", encoding="utf-8") as fh:
        fh.write('{"forged": true}\n')
    report = load_and_validate_brain(root)
    assert report["ok"] is False
    assert report["guard_verdict"] == "REFUSED"
    assert any("brain_index_refused:TamperedBrainIndexError" in e for e in report["errors"])
