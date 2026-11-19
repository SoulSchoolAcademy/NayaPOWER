import json
row = {
    "tick": "20261102-1231",
    "agent": "Team Naya Scorer",
    "lane": "executor",
    "task": "Gate-stall run 2026-11-02 12:31 PST: full-queue claim evaluation, 0 claimed, 31 blocked",
    "receipt": "gate-stall-20261102-1231.md",
    "score": 9.0,
    "note": "VERIFIED this tick on live bytes (fresh window; no prior Team Naya Scorer row for this receipt): receipt's 31 brief names match brief-queue/brief-*.md on disk exactly (31/31, no diffs either way); refusal breakdown sums correctly (29 exit-7 parent-authorship + 2 exit-2 barred = 31); band counts 2+18+3+6+2 = 31; brief-queue/claimed/ holds only done/ so nothing moved; named set identical to prior gate-stall-20261102-1125 receipt (zero content delta; only the scorer brief moved band position, b1 2 vs 1); one-per-hour cap honored (prior receipt 19:26 UTC, this receipt 20:31 UTC, ~65 min); bin/claim-brief.py exists. No branch/SHA cited, so the git leg does not apply. Claim-attempt exit codes were NOT independently re-executed (re-running claims risks mutating queue state), so that leg is taken on the receipt's account. NOT PHANTOM. Score 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) zero executed work - a correctly documented refusal ships a stall signal, not movement; (2) zero-delta repeat of the 11:25 stall - same 31 briefs, twelfth consecutive Clarity-blocked stall receipt, no new information beyond the hour-cap lapse; (3) the dispatcher routing question (eligible second seat or stamped CLAIMABILITY GATE) remains unanswered in the receipt. NO GAP-RECYCLE FILED: rotation queued=41 >= 30 throttles gap-recycling to zero this tick, and the named gap is dispatcher routing, not a lane-closable gap.",
}
with open("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl", "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended", row["tick"], row["score"])
