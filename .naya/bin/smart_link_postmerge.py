#!/usr/bin/env python3
"""Post-merge Smart-Link backfill (D1: auto-PR, human merges).

Called by .github/workflows/smart-link-postmerge.yml on push to main.
For each new projection path given on argv: generate the Smart Link
(verified against main, which now contains the file), merge the fragment
into the index, and print a summary. The workflow then opens the PR.

Never pushes to main. Never merges itself.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from smart_link import (  # noqa: E402
    GitHubVerifier, backfill, generate, load_index, utcnow,
)

INDEX = Path(".naya/memory/smart-notes/index.json")


def main(argv: list[str]) -> int:
    if not argv:
        print("no projection paths given; nothing to do")
        return 0
    index = load_index(INDEX)
    verifier = GitHubVerifier()
    # main SHA for the stamp: read from the checked-out tree
    import subprocess
    rev = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                         text=True).stdout.strip()
    added = 0
    for path in argv:
        path = path.strip()
        if not path:
            continue
        try:
            frag = generate(path, index, verifier=verifier, rev=rev)
        except ValueError as ex:
            print(f"SKIP {path}: {ex}", file=sys.stderr)
            continue
        # merge fragment into a new or existing entry
        ent = next((e for e in index["entries"]
                    if e.get("projection_path") == path), None)
        if ent is None:
            ent = {"smart_note_id": "SN-?",
                   "title": Path(path).stem,
                   "projection_path": path,
                   "truth_state": "CANDIDATE",
                   "scope": "PRIVATE"}
            index["entries"].append(ent)
        ent.update(frag)
        added += 1
        print(f"LINKED {path} -> {frag['smart_link']}")
    INDEX.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(f"done: {added} linked, rev {rev[:8]}, at {utcnow()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
