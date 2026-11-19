import json
rows = [
    {
        "tick": "t0551",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Hub room wiring-status ledger: 12 canonical rooms surveyed, all LOCAL-ONLY",
        "receipt": "t0551-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/hub-room-wiring-status-20261016.md exists (5265 bytes, header names t0551 Lane 12) with 12 room rows all LOCAL-ONLY plus the 05-CONNECT WATCH row, matching the receipt's verdict taxonomy and head pin 83806f4d0e335b223ba2f849fd19a7a7915fdcc6; fresh git ls-remote HEAD is now 5e62373967530d9ce066a51a408db162f6e44165, head moved since the Oct 16 survey as expected. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane self-score 9.5. Why not 9.5: (1) the working-copy-to-repo-tree correspondence gap the receipt itself names is still unclosed, so the ledger cites working-copy bytes, not repo bytes; (2) the 05-CONNECT door-badge WATCH still awaits the second-seat ruling; (3) the live-board post was not re-verified by this scorer this tick (bounded read). GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed, gaps not added to gap-followup-seen.json. No PHANTOM, no lane below 7.0 this tick."
    },
    {
        "tick": "t0552",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "First v0.1 SMARTBLOCK draft contracts for top-3 asked lanes (10/5/1), UNWIRED-DRAFT",
        "receipt": "t0552-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/auto-retrieval/smartblock-drafts-t0552.md exists (16727 bytes) with header matching the receipt exactly - log SHA 5398dda9a59d9d66da9a86490a43666ed391e8235ef2070dbb10835160eafa4f, 115 lines, top-3 lane 10:9 / lane 5:9 / lane 1:8, and 3 lane-status-packet blocks marked UNWIRED-DRAFT; source log hidden_files/auto-retrieval/ask-world-queries.jsonl now at 199 lines (grew since the Oct 16 pin, expected drift, not a contradiction). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane self-score 9.5. Why not 9.5: (1) the recount/checker scripts lived in /tmp and are gone, so independent re-execution from surviving bytes is impossible - only receipt-sealed logic remains; (2) the official check_smartblock.py lint was never run on the drafts, only a mirror checker, leaving the one-file-three-blocks schema hole unresolved; (3) blocks are contract-only UNWIRED-DRAFT with no live payload. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed, gaps not added to gap-followup-seen.json. No PHANTOM, no lane below 7.0 this tick."
    },
]
path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
with open(path, "a") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")
print("appended", len(rows), "rows ok")
