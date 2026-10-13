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


def main() -> None:
    index_path = REPO_ROOT / ".naya" / "memory" / "smart-notes" / "index.json"
    registry = json.loads(index_path.read_text(encoding="utf-8"))
    entries = registry.get("entries")
    if not isinstance(entries, list):
        raise SystemExit("BACKFILL_REFUSED: index has no entries list")

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
        page = REPO_ROOT / pp
        if not page.is_file():
            raise SystemExit(
                f"BACKFILL_REFUSED:PROJECTION_ABSENT:"
                f"{e.get('intelligent_block_id')}: {pp}"
            )
        e["page_hash"] = m._page_file_hash(page)
        hashed += 1

    registry["corpus_manifest_hash"] = m._corpus_manifest_hash(entries)
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
        "validator": "PASS",
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
