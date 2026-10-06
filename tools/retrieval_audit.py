#!/usr/bin/env python3
"""Retrieval registry hygiene audit (read-only).

Reports defects in the retrieval corpus that .naya/memory/smart-notes/index.json
describes, without changing anything:

  - entries whose projection_path is missing on disk
  - entries whose projection_path resolves to a TOMBSTONE file
  - duplicate smart_note_id values across entries
  - Smart Note files under BRAIN/05-MEMORY/SMART-NOTES not covered by the registry
  - truth-state distribution

Usage: python3 tools/retrieval_audit.py [--root /path/to/repo]
Exit 0 always; the report is JSON on stdout. A non-empty "defects" list means
the retrieval corpus needs attention, not that the audit failed.
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
DEFAULT_ROOT = HERE.parents[1]
NOTE_GLOB_ROOT = DEFAULT_ROOT / "BRAIN" / "05-MEMORY" / "SMART-NOTES"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DEFAULT_ROOT))
    ap.add_argument("--json", action="store_true", help="emit JSON report (default)")
    args = ap.parse_args()
    root = Path(args.root)
    registry_path = root / ".naya" / "memory" / "smart-notes" / "index.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    entries = registry.get("entries", [])

    defects = {"missing_projection": [], "tombstone_projection": [],
               "duplicate_smart_note_id": [], "unindexed_note_files": []}

    seen_ids = Counter()
    indexed_paths = set()
    for e in entries:
        sid = e.get("smart_note_id") or e.get("intelligent_block_id")
        seen_ids[sid] += 1
        pp = e.get("projection_path")
        if not pp:
            defects["missing_projection"].append({"entry": sid, "reason": "no projection_path"})
            continue
        p = root / pp
        indexed_paths.add(p.resolve() if p.exists() else p)
        if not p.exists():
            defects["missing_projection"].append({"entry": sid, "path": pp})
        elif "<!-- TOMBSTONE" in p.read_text(encoding="utf-8", errors="replace")[:2000]:
            defects["tombstone_projection"].append({"entry": sid, "path": pp})

    for sid, n in seen_ids.items():
        if n > 1:
            defects["duplicate_smart_note_id"].append({"smart_note_id": sid, "entries": n})

    on_disk = set()
    if NOTE_GLOB_ROOT.exists():
        # NOTE_GLOB_ROOT is resolved against DEFAULT_ROOT; rebase for --root
        glob_root = root / "BRAIN" / "05-MEMORY" / "SMART-NOTES"
        for f in glob_root.rglob("IB-SMART-NOTE-*.md"):
            on_disk.add(f.resolve())
    for f in sorted(on_disk - indexed_paths):
        try:
            rel = str(f.relative_to(root))
        except ValueError:
            rel = str(f)
        defects["unindexed_note_files"].append(rel)

    report = {
        "registry": str(registry_path),
        "entry_count": len(entries),
        "truth_state_distribution": dict(Counter(
            str(e.get("truth_state", "MISSING")) for e in entries)),
        "lifecycle_distribution": dict(Counter(
            str(e.get("lifecycle_state", "ACTIVE")) for e in entries)),
        "note_files_on_disk": len(on_disk),
        "defects": defects,
        "defect_count": sum(len(v) for v in defects.values()),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
