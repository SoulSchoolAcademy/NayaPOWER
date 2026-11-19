import json
row = {
    "tick": "20261030-0940",
    "agent": "Team Naya Scorer",
    "lane": "executor",
    "task": "Seat-stall sweep 2026-10-30 09:38 PDT: 31-brief lane-executor queue sweep, all refused by claim gate",
    "receipt": "seat-stall-20261030-0938.md",
    "score": 9.0,
    "note": "VERIFIED this tick on live bytes: brief-queue root holds exactly 31 brief-*.md files and twelve-lane-rotation.json queued = 31 with EXACT set match to disk files, in_flight=[]; parsing the receipt's blocked section gives exactly 31 unique brief names matching the disk set name for name (0 only-receipt, 0 only-disk); claimed/ holds only done/, consistent with no side effects; prior stall receipt gate-stall-20261030-0835.md mtime vs this receipt = ~65 minutes by mtime (receipt's nominal 08:35->09:38 = 63 min), so the one-per-hour cap is respected either way. Two sample dry-runs independently re-run this tick returned the claimed codes exactly (brief-gap-t1556-lane11.md exit 7 authorship refusal; brief-gap-gap-t1002-lane2.md exit 2 barred). Seat-stall receipts cite no git branch/SHA, so the branch/SHA leg does not apply; the receipt file itself exists (4481 bytes) and matches its claims, including the seat-stall (not gate-stall) classification: no GATE file-existence section was claimed. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching the receipt's honest self-score 9.0. Why not 9.5: it ships no cleared work - the queue's entire contents are second-seat verification debt on Clarity-authored parents this seat cannot clear itself, so the stall is correctly diagnosed, not resolved; and only 2 of 31 refusals were independently re-run this tick, the remaining 29 counts are parsed from the receipt's list, not re-executed. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
}
with open('/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl', 'a') as f:
    f.write(json.dumps(row, ensure_ascii=False) + '\n')
print('appended', row['tick'], row['score'])
