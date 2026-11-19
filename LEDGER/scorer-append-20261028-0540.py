import json
row = {
    "tick": "distill-daily-20261028",
    "agent": "Team Naya Scorer",
    "lane": 0,
    "task": "Daily distillation 2026-10-28: fresh verification of mission-state drift (main vs naya/mission-state) + handoff, no landing",
    "receipt": "distill-daily-20261028.md",
    "score": 9.0,
    "note": "VERIFIED this tick on live bytes + git protocol: evidence files exist with SHA256 EXACT match to receipt pins - main doc 65382e118aebed72502651e626643766406e5f665d1146c3dff27ce30665bef2 (23 lines) and branch doc 2d3a59150bc8dafdaf2d530ad5c707621fbe14a9bb6e3b6e48272e7cb1972768 (16 lines); work clone HEAD 57bf31e9d8eb7d0d28db15fdde3316bdc6119a2a and fresh ls-remote HEAD match receipt main tip exactly; drift diff file present (15017 bytes). NOT PHANTOM. Score 9.0 GOOD, ONE MORE PASS, above lane honest 8.0 because the stale-snapshot catch (receipt head 46e83fc newer than brief 04a76c4) is itself verified value. Why not 9.5: (1) landing + branch retirement still owed by design - merge-protected seat, scored process + dock must carry it; (2) branch head has already moved again since execution (ls-remote now e5a2c23e, not receipt 46e83fc), so the handoff target must be re-derived at landing time, proving the receipt mirror lesson; (3) queue-evaluation claim (29 exit-7 refusals etc.) not independently re-verified by this scorer (bounded read). GAP-RECYCLE THROTTLED - rotation queued=31 >= 30, zero follow-ups filed this tick. No PHANTOM, no lane below 7.0 this tick."
}
path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
with open(path, "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended ok")
