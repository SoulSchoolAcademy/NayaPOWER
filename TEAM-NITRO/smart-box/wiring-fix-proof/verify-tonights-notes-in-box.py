"""Verify tonight's new notes (SN-2574..SN-2599) are retrievable
from shawn's box (2026-11-09, wiring fix + embedding amendment).

For each SN: find its path(s) in the live-tree watermark, then check
the box's current blocks for a block with that SN's id whose
where.github_path names the live-tree path. A note is IN when the
box's current block for its id names the real GitHub path - that is
what "the notes live in the Box" means, and it is what the
completeness gate checks. SN-2596 has two paths (a numbering
collision the noting seat is resolving) - both are reported.
A note not yet in the live tree at all is PENDING (the noting seat
has not filed it), not a box failure.
"""
import json
import re
import sys

sys.path.insert(0, "/home/hatch/workspace/team-nitro/smart-box")
import boxstore  # noqa: E402

WM = "/home/hatch/workspace/nitro-smart-box/.organize-watermark-shawn.json"
BOXES = "/home/hatch/workspace/nitro-smart-box/boxes"

mark = json.load(open(WM, encoding="utf-8"))
live = mark.get("live_tree", {})
boxstore.BOXES_ROOT = BOXES
blocks = boxstore.read_blocks("shawn")
# Index the box's CURRENT blocks by the path they name - a note is
# IN when some current block names its live-tree path. (Ids derive
# from the note's SN line when it has one, so the id cannot be
# rebuilt from the filename alone.)
by_path = {}
for block in blocks.values():
    path = (block.get("where") or {}).get("github_path") or ""
    if path:
        by_path[path] = block

results = []
for num in range(2574, 2600):
    sn = "SN-%d" % num
    paths = sorted(p for p in live
                   if re.search(r"sn%04d-" % num, p, re.I)
                   or "/%s/" % sn in p)
    if not paths:
        results.append((sn, "PENDING", "not in the live tree yet"))
        continue
    for path in paths:
        block = by_path.get(path)
        if block is None:
            results.append((sn, "FAIL", "no block names %s" % path))
        else:
            results.append((sn, "IN",
                            "%s (%s)" % (path, block["id"])))

fails = [r for r in results if r[1] == "FAIL"]
pendings = [r for r in results if r[1] == "PENDING"]
ins = [r for r in results if r[1] == "IN"]
for sn, status, detail in results:
    print("%s %s %s" % (sn, status, detail))
print("IN: %d  FAIL: %d  PENDING: %d" % (len(ins), len(fails),
                                        len(pendings)))
