#!/usr/bin/env python3
"""check_circles.py — verify circle integrity: every hub exists, every member
exists, hub links every member, every member links back to the hub.
A link that doesn't come back is a dead end, and dead ends are bugs.
Reads hidden_files/circle-system.md for declared circles (machine block).
Exit 0 = all circles sound. Exit 1 = list every break.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path.home() / "workspace/goals/bring-naya-to-life/hidden_files"
GOAL = Path.home() / "workspace/goals/bring-naya-to-life"
DOC = BASE / "circle-system.md"

# candidate roots, in order: goal workspace, home workspace, repo checkout scratch
ROOTS = [GOAL, Path.home() / "workspace", Path("/tmp/sn-stage")]

def resolve(p: str):
    for r in ROOTS:
        cand = r / p
        if cand.is_file():
            return cand
    return None

def circles():
    text = DOC.read_text()
    out = []
    # machine block: ```circles ... ```
    m = re.search(r"```circles\n(.*?)```", text, re.S)
    if not m:
        return out
    return json.loads(m.group(1))

def links_in(path: Path):
    """Return set of link targets (paths/urls) found in a markdown file."""
    try:
        text = path.read_text()
    except OSError:
        return None
    targets = set()
    for mm in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        targets.add(mm.group(1).strip())
    return targets

def main():
    decls = circles()
    breaks = []
    for c in decls:
        if c.get("status") == "FORMING":
            print(f"CIRCLE {c['id']}: forming — skipped until hub lands")
            continue
        hub = resolve(c["hub"])
        if hub is None:
            breaks.append(f"{c['id']}: hub missing: {c['hub']}")
            continue
        hub_links = links_in(hub) or set()
        for member in c["members"]:
            mp = resolve(member)
            if mp is None:
                breaks.append(f"{c['id']}: member missing: {member}")
                continue
            ml = links_in(mp) or set()
            # hub -> member ?
            if not any(member in t or t.endswith(Path(member).name) for t in hub_links):
                breaks.append(f"{c['id']}: hub does not link member {member}")
            # member -> hub ?
            if not any(c["hub"] in t or t.endswith(Path(c["hub"]).name) for t in ml):
                breaks.append(f"{c['id']}: member does not link hub: {member}")
    if breaks:
        print("CIRCLE BREAKS:")
        for b in breaks:
            print(" -", b)
        return 1
    print("all circles sound")
    return 0

if __name__ == "__main__":
    sys.exit(main())
