#!/usr/bin/env python3
"""One-time backfill for the B-51 fail-closed index validator (2026-10-13).

Computes page_hash for every retrieval-eligible index entry from working-tree
bytes and writes corpus_manifest_hash over the full entry list, then commits
the regenerated index atomically. Entries with no projection_path cannot be
bound to a page: they are explicitly retired (marked, never deleted) instead
of being silently left unvalidatable.

Uses the module's own hash functions (single hashing authority). Fails LOUD
(BACKFILL_REFUSED) if any eligible entry's page is missing — the backfill
never blesses a broken corpus.

Usage: python3 tools/backfill_b51_index_hashes.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import smart_note_v2 as m  # noqa: E402


def _diff_census(before_entries, after_entries, hashed, retired):
    """Diff census after a backfill-class apply (w428 leg 221).

    Every corpus entry must have been VISITED (hashed or retired) and its
    bytes must have CHANGED. A silently skipped entry is not a no-op — it
    is a shortfall: the apply is refused, never trusted. JSON round-trips
    are not byte-safe, so the census runs on the exact bytes, not the
    writer's format claims.
    """
    before_c = [json.dumps(e, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False) for e in before_entries]
    after_c = [json.dumps(e, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False) for e in after_entries]
    changed = sum(1 for b, a in zip(before_c, after_c) if b != a)
    total = len(after_entries)
    return {
        "total_entries": total,
        "hashed": hashed,
        "retired_unvalidatable": retired,
        "changed": changed,
        "coverage_ok": total > 0 and (hashed + retired) == total and changed == total,
    }


def apply(index_path, repo_root):
    """Run the backfill apply against index_path (testable entry point).

    Mutates entries in place, re-anchors corpus_manifest_hash in the SAME
    apply (writer contract), writes the registry atomically, then proves
    the regenerated index against the validator on the same bytes. Any
    refusal raises SystemExit(BACKFILL_REFUSED:...) BEFORE the write lands.

    Returns the receipt dict (also printed by main()).
    """
    registry = json.loads(index_path.read_text(encoding="utf-8"))
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("BACKFILL_REFUSED: index has no entries list")
    before_entries = [dict(e) for e in entries]  # pre-apply shape, for the census

    hashed, retired = 0, 0
    for e in entries:
        pp = e.get("projection_path")
        if not pp:
            e["index_validation"] = "RETIRED_UNVALIDATABLE"
            e["index_validation_reason"] = (
                "B-51 fail-closed backfill 2026-10-13: no projection_path, "
                "so no page can be bound. Entry kept for provenance; it is "
                "never scored and never validated."
            )
            retired += 1
            continue
        page = repo_root / pp
        if not page.is_file():
            raise SystemExit(
                f"BACKFILL_REFUSED:PROJECTION_ABSENT:"
                f"{e.get('intelligent_block_id')}: {pp}"
            )
        e["page_hash"] = m._page_file_hash(page)
        hashed += 1

    # The writer contract: an index-mutating migration re-anchors the
    # corpus_manifest_hash in the same apply, on the post-mutation entries.
    # A migration that mutates entries without re-stamping breaks the
    # reader's freshness anchor (w440).
    registry["corpus_manifest_hash"] = m._corpus_manifest_hash(entries)

    # Diff census BEFORE the write: an apply that does not cover the whole
    # corpus is refused before it lands (leg 205's shape, leg 221's content).
    census = _diff_census(before_entries, entries, hashed, retired)
    if not census["coverage_ok"]:
        raise SystemExit(
            "BACKFILL_REFUSED:DIFF_CENSUS_SHORTFALL:"
            f"visited={hashed + retired} changed={census['changed']} "
            f"total={len(entries)}"
        )

    m._atomic_write_json(index_path, registry)

    # The validator is the acceptance gate for this migration: the regenerated
    # index must pass it in the same process, or the backfill did not land.
    reloaded = json.loads(index_path.read_text(encoding="utf-8"))
    m._validate_index_against_corpus(reloaded)

    receipt = {
        "backfill": "b51-failclosed-index-validation",
        "date": "2026-10-13",
        "total_entries": len(entries),
        "page_hashed": hashed,
        "retired_unvalidatable": retired,
        "corpus_manifest_hash": registry["corpus_manifest_hash"],
        "tree_pin": m._corpus_tree_pin(entries, REPO_ROOT),
        "diff_census": census,
        "validator": "PASS",
    }
    return receipt


def main() -> None:
    index_path = REPO_ROOT / ".naya" / "memory" / "smart-notes" / "index.json"
    receipt = apply(index_path, REPO_ROOT)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
