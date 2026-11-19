import json
row = {
    "tick": "20261103-0859",
    "agent": "Team Naya Scorer",
    "lane": "executor",
    "task": "Gate-stall run 2026-11-03 08:59 PST: full-queue claim evaluation, 0 claimed, 31 blocked",
    "receipt": "gate-stall-20261103-0859.md",
    "score": 9.0,
    "note": "VERIFIED this tick on live bytes (fresh window; no prior Team Naya Scorer row for this receipt): receipt's 31 brief names match brief-queue/brief-*.md on disk exactly (31/31, no diffs either way, verified by set comparison); refusal breakdown sums correctly (29 exit-7 parent-authorship + 2 barred = 31); zero mission-sequence brief-t files; claimed/ holds only the distill brief plus done/, so nothing moved; named set identical to prior gate-stall-20261103-0753 receipt (zero delta, verified by set comparison); one-per-hour cap honored (prior receipt mtime 15:54 UTC to this receipt 16:59 UTC, 65.5 min, past the 60-minute boundary). No branch/SHA cited, so the git leg does not apply. Claim-attempt exit codes were NOT independently re-executed (re-running claims risks mutating queue state), so that leg is taken on the receipt's account. NOT PHANTOM. Score 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) zero executed work - a correctly documented refusal ships a stall signal, not movement; (2) zero-delta repeat of the 07:53 stall - same 31 briefs, same refusal pattern, no new information beyond the hourly record; (3) the dispatcher routing question (eligible second seat or stamped CLAIMABILITY GATE) remains unanswered in the receipt. NO GAP-RECYCLE FILED: rotation queued=41 >= 30 throttles gap-recycling to zero this tick, and the named gap is dispatcher routing, not a lane-closable gap. Note rotation queued (41) diverges from on-disk briefs (31) by 10 stale entries, pre-existing, not created by this run."
}
with open("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl", "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended", row["receipt"], row["score"])
