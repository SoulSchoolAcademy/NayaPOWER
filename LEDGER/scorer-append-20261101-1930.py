import json
row = {
    "tick": "20261101-1930",
    "agent": "Team Naya Scorer",
    "lane": "executor",
    "task": "Gate-stall run 2026-11-01 19:24 PST: full-queue claim evaluation, 0 claimed, 31 blocked",
    "receipt": "gate-stall-20261101-1924.md",
    "score": 9.0,
    "note": "VERIFIED this tick on live bytes (fresh window; no prior Team Naya Scorer row): receipt file exists; brief-queue/ holds exactly the 31 brief names listed in the receipt (31/31, no diffs either way; the one other top-level .md is lane-feed.md, not a brief); refusal breakdown sums correctly (29 exit-7 parent-authorship + 2 barred = 31); stall delta zero vs prior scored receipt gate-stall-20261101-1823.md (same 31-brief set, same order); one-per-hour cap honored (prior stall receipt mtime 61.9 min before this receipt). bin/claim-brief.py exists as cited. No branch/SHA cited, so the git leg does not apply. NOT PHANTOM. Score 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) zero executed work - a correctly documented refusal ships a stall signal, not movement; (2) the queue is a standing stall with no new information beyond the inventory; (3) the dispatcher routing question (eligible second seat or stamped CLAIMABILITY GATE) remains unanswered in the receipt. GAP-RECYCLE: none filed - score is 9.0 but the named gap is dispatcher routing, not a lane-closable gap, and rotation queued=41 >= 30 throttles gap-recycling to zero this tick."
}
with open("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl", "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended", row["tick"], row["receipt"], row["score"])
