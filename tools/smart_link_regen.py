#!/usr/bin/env python3
"""Smart-Link regen: keep .naya/memory/smart-notes/index.json smart_links truthful.

For every index entry with a smart_link:
  1. Extract the repo path from the .../blob/main/<path> URL.
  2. Check the path exists in the git tree at --rev (default HEAD).
  3. If missing, attempt a renumber-aware repair (never invent):
       a. superseded_by_capture_id names a successor capture
          (e.g. IB-SMART-NOTE-20261004-sn0599-....json) -> derive the new
          SN number -> the successor file is <same stem>.md under /SN-<num>/.
       b. slug-stem fallback: strip date/sn-number tokens from the entry's
          intelligent_block_id, search SMART-NOTES .md paths for the stem;
          repair only on exactly one hit.
     Ambiguous or unlocatable -> smart_link_status='BROKEN', old link kept,
     reported for a human lane. Nothing is fabricated.
  4. Re-stamp smart_link_verified_at / smart_link_verified_rev for every
     resolving link.

Usage:
    python3 tools/smart_link_regen.py [--rev SHA] [--root PATH] [--write]
                                      [--receipt-out PATH]

    --rev         git rev to verify against (default: HEAD of the repo)
    --root        repo root (default: derived from this file's location)
    --write       write the repaired index back (default: dry run)
    --receipt-out write the regen receipt JSON (for the auto-merge gate's
                  smart_link_regen_receipt pr_state field)

Exit codes: 0 = no drift (all green, stamps already at --rev);
            1 = changes written (dry-run would change, or --write applied);
            2 = unrecoverable broken links remain (human lane needed).

Merge protocol: the merging lane runs this at the new main tip after every
merge touching BRAIN/05-MEMORY/SMART-NOTES/ or the index; exit 1 -> open an
auto-PR with the result (auto-PR beats human memory per smart_link.py D1).
The auto-merge gate (tools/auto_merge_gate.py, P11) requires a fresh receipt
for any smart-note-touching PR.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

INDEX_REL = Path(".naya/memory/smart-notes/index.json")
SMART_NOTES_PREFIX = "BRAIN/05-MEMORY/SMART-NOTES/"
BLOB_PREFIX = "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/"
CAPTURE_RE = re.compile(r"IB-SMART-NOTE-(\d{8})-sn(\d+)-(.+)\.json$")
STEM_NUM_RE = re.compile(r"^IB-SMART-NOTE(?:-SMART-NOTE)?-\d{8}-sn\d+-(.+)$")


def _git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr[:300]}")
    return p.stdout


def tree_paths(root: Path, rev: str) -> set[str]:
    out = _git(root, "ls-tree", "-r", "--name-only", "-z", rev)
    return {p for p in out.split("\0") if p}


def path_from_link(link: str) -> str | None:
    if not link or not link.startswith(BLOB_PREFIX):
        return None
    return link[len(BLOB_PREFIX):]


def successor_lookup(entry: dict, tree: set[str]) -> tuple[str | None, bool]:
    """Rule (a): follow the entry's own supersession record to the new file.

    Returns (path_or_None, attempted). When the record names a successor but
    the file is absent from the tree, that is KNOWN-ABSENT: the note did not
    move somewhere guessable, it is gone -> BROKEN, never stem-guessed.
    """
    cap = entry.get("superseded_by_capture_id") or ""
    m = CAPTURE_RE.match(cap)
    if not m:
        return None, False
    _date, num, _stem = m.groups()
    want_name = cap[: -len(".json")] + ".md"
    cands = [p for p in tree
             if p.startswith(SMART_NOTES_PREFIX)
             and f"/SN-{num}/" in p
             and p.endswith("/" + want_name)]
    if len(cands) == 1:
        return cands[0], True
    return None, True  # named successor absent (or ambiguous): do not guess


def stem_candidate(entry: dict, tree: set[str]) -> str | None:
    """Rule (b): slug-stem search; repair only on an unambiguous single hit."""
    bid = entry.get("intelligent_block_id") or ""
    m = STEM_NUM_RE.match(bid)
    if not m:
        return None
    stem = m.group(1)
    if len(stem) < 8:
        return None
    cands = [p for p in tree
             if p.startswith(SMART_NOTES_PREFIX)
             and p.endswith(".md")
             and stem in p]
    return cands[0] if len(cands) == 1 else None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--root", default=None)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--receipt-out", default=None)
    a = ap.parse_args(argv)

    here = Path(__file__).resolve()
    root = Path(a.root).resolve() if a.root else here.parents[1]
    rev = _git(root, "rev-parse", a.rev).strip()
    tree = tree_paths(root, rev)
    index_path = root / INDEX_REL
    idx = json.loads(index_path.read_text())
    ents = idx["entries"]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    repaired, already_ok, broken = [], [], []
    changed = False

    for e in ents:
        link = e.get("smart_link")
        if not link:
            continue
        p = path_from_link(link)
        if p and p in tree:
            already_ok.append(e["intelligent_block_id"])
        else:
            newp, attempted = successor_lookup(e, tree)
            if not attempted:
                newp = stem_candidate(e, tree)
            if newp:
                old = link
                e["smart_link"] = BLOB_PREFIX + newp
                if e.get("smart_link_status") == "BROKEN":
                    e["smart_link_status"] = "ACTIVE_AUTH_GATED"
                repaired.append({"id": e["intelligent_block_id"],
                                 "sn": e.get("smart_note_id"),
                                 "old": old, "new": e["smart_link"]})
                changed = True
            else:
                e["smart_link_status"] = "BROKEN"
                broken.append({"id": e["intelligent_block_id"],
                               "sn": e.get("smart_note_id"),
                               "link": link})
                changed = True
        # re-stamp every resolving link at this rev
        if path_from_link(e.get("smart_link") or "") in tree:
            if (e.get("smart_link_verified_rev") != rev
                    or not e.get("smart_link_verified_at")):
                e["smart_link_verified_rev"] = rev
                e["smart_link_verified_at"] = now
                changed = True

    receipt = {
        "tool": "tools/smart_link_regen.py",
        "rev": rev,
        "verified_at": now,
        "result": "green" if not repaired else "repaired",
        "checked": len(already_ok) + len(repaired) + len(broken),
        "ok": len(already_ok),
        "repaired": repaired,
        "broken_count": len(broken),
        "broken": broken,
    }
    if a.receipt_out:
        Path(a.receipt_out).write_text(json.dumps(receipt, indent=1) + "\n")

    if changed and a.write:
        index_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n")

    print(json.dumps({k: v for k, v in receipt.items() if k != "broken"},
                     indent=1)[:2000])
    if broken:
        print("UNRECOVERABLE (human lane needed):", file=sys.stderr)
        for b in broken:
            print(f"  {b['sn']} {b['id']}", file=sys.stderr)
        return 2
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
