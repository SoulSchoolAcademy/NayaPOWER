#!/usr/bin/env python3
"""Scorer append for tick 20261030-2030: seat-stall-20261030-2027.md."""
import json, os

base = os.path.expanduser("~/workspace/goals/bring-naya-to-life/hidden_files")
entry = {
    "tick": "20261030-2027",
    "agent": "Team Naya Scorer",
    "lane": "executor",
    "task": "Seat-stall sweep 2026-10-30 20:27 PDT: 31-brief lane-executor queue sweep, all refused by claim gate",
    "receipt": "seat-stall-20261030-2027.md",
    "score": 9.0,
    "note": (
        "VERIFIED this tick on live bytes: receipt file exists (4867 bytes, sha256 09aa52ae24ffc9d7530a2993f8c69ea64c68bd11e6ffd2b767a240e37875ef36); "
        "brief-queue root holds exactly 31 brief-*.md files and twelve-lane-rotation.json queued=31 with EXACT set match across receipt, disk, and rotation "
        "(0 only-receipt, 0 only-disk, 0 only-rotation), in_flight=[]; brief-queue/claimed/ holds no brief files (only done/ subdir); "
        "prior stall receipt seat-stall-20261030-1920.md exists (~67 min earlier, within the one-per-hour stall cap pattern). "
        "Two sample dry-runs independently re-run this tick returned the claimed refusals exactly (brief-gap-t1556-lane11.md exit 7 parent-authorship refusal, "
        "'No mv, no touch'; brief-gap-gap-t1002-lane2.md exit 2 claimability-gate verdict barring 'clarity'), queue still 31 after both runs. "
        "Seat-stall receipts cite no git branch/SHA, so the branch/SHA leg does not apply; the receipt file itself is the artifact and matches its claims, "
        "including the seat-stall (not gate-stall) classification and the 29 exit 7 + 2 exit 2 pattern. NOT PHANTOM. "
        "Score 9.0, GOOD, ONE MORE PASS, matching the receipt's honest self-score 9.0. "
        "Why not 9.5: (1) it ships no cleared work and has zero delta vs the 19:20 stall - its value is bounded by a queue this seat cannot legally claim; "
        "(2) only 2 of 31 refusals were independently re-run this tick, the remaining 29 rest on the receipt's list (though the three-way set match is exact). "
        "GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    ),
}
path = os.path.join(base, "twelve-lane-scores.jsonl")
with open(path, "a") as f:
    f.write(json.dumps(entry) + "\n")
print("appended:", entry["tick"], entry["receipt"], entry["score"])
# validate last line parses
with open(path) as f:
    lines = f.readlines()
print("last line parses:", json.loads(lines[-1])["receipt"])
print("total score lines now:", len(lines))
