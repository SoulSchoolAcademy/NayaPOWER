#!/usr/bin/env python3
"""Lane-scorer tick 2026-11-01 01:20 PDT: score gate-stall-20261101-0119.md."""
import json

row = {
    "tick": "20261101-0119",
    "agent": "Team Naya Scorer",
    "lane": "executor",
    "task": "gate-stall 01:19 PDT - 31-brief claim attempt, zero claimable, queue untouched",
    "receipt": "gate-stall-20261101-0119.md",
    "score": 9.0,
    "note": (
        "Verified by this scorer from live bytes: brief-queue root holds 31 brief-*.md "
        "(excluding lane-feed.md), twelve-lane-rotation.json queued = 31 with exact set match "
        "to disk, in_flight=[]; the receipt's listed 31 blocked briefs match the disk set exactly "
        "(29 x exit 7 parent-authorship + 2 x exit 2 seat/routing bar, counts re-derived from the "
        "receipt text), and the identical 31-brief set as the prior gate-stall-20261101-0019.md run. "
        "Stall-cap complies (prior receipt 00:19 PDT, 60 min 35 sec earlier by mtime). Receipt cites "
        "no git branch/SHA, so the branch/SHA leg does not apply; verification is the live "
        "queue/rotation check above. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: no brief was "
        "executed - the sweep only documents the structural single-seat stall, it does not clear "
        "it; the queue remains fully Clarity-blocked until a second seat claims or the dispatcher "
        "stamps a claimability gate. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero "
        "follow-ups filed."
    ),
}

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
existing = open(path).read()
assert "gate-stall-20261101-0119.md" not in existing or existing.count(
    '"receipt": "gate-stall-20261101-0119.md"'
) == 0, "already scored"
with open(path, "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended:", row["tick"], row["receipt"], "score", row["score"])
