"""Repair pass for the 16 path-clobbered notes (2026-11-09, wiring fix).

The hook's regular run re-appended local-copy blocks (github_path
empty) AFTER the live-tree backfill, and boxstore's last-wins made
the empty path win - the box stopped naming 16 real Nov 9 notes.

The clobber rule is now fixed in organize_hook.append_blocks (a
pathless block never supersedes a pathed one). This script repairs
the CURRENT state: it asks the completeness gate for the missing
paths, removes exactly those paths from the watermark's live_tree,
and saves the watermark - so the next --live-tree backfill re-fetches
and re-appends them pathed. Nothing else is touched.
"""
import json
import sys

sys.path.insert(0, "/home/hatch/workspace/team-nitro/smart-box")
sys.path.insert(0, "/home/hatch/workspace/project-intelligence")
import box_source  # noqa: E402
import organize_hook  # noqa: E402

WM = "/home/hatch/workspace/nitro-smart-box/.organize-watermark-shawn.json"
STATE = "/home/hatch/workspace/factory-pipeline/.sync-state.json"

with open(STATE, encoding="utf-8") as handle:
    state = json.load(handle)
state_paths = sorted(state["files"].keys())
_complete, missing = box_source.box_is_complete_for_state(
    "shawn", state_paths)
print("state paths:", len(state_paths))
print("gate missing:", len(missing))
for path in missing:
    print("  ", path)
mark = organize_hook.load_watermark(WM)
live = mark.get("live_tree", {})
removed = [p for p in missing if p in live]
for path in removed:
    del live[path]
mark["live_tree"] = live
organize_hook.save_watermark(WM, mark)
print("removed from live_tree watermark:", len(removed))
print("live_tree entries now:", len(live))
