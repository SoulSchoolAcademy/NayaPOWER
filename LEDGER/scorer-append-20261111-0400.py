import json

row = {
    "tick": "lane-scorer-20261111-0400",
    "agent": "Team Naya Scorer",
    "lane": 0,
    "task": "Gate-stall run 2026-11-11 03:58 PST: evaluated all 30 queued gap follow-ups, 0 claimed, all refused by seat gate",
    "receipt": "gate-stall-20261111-0358.md",
    "score": 8.5,
    "note": "Verified this tick on live bytes: (1) receipt's 30 blocked briefs match the live brief-queue/ set 30/30 exactly, symdiff empty; (2) sweep log hidden_files/claim-sweep-20261111-0358.log exists, 29 attempts / 0 claimed / 27 x rc=7 parent-authorship / 2 x rc=2 explicit bars, plus 1 unattempted on its own-note bar (brief-gap-gate-stall-20261026-2230-lane0.md) as the receipt states; (3) delta claim verified: brief set identical to gate-stall-20261111-0253.md (30/30, symdiff empty), same refusal pattern. Score 8.5: the stall is the correct outcome under the seat gate and the receipt is honest, complete work (b1 ordering slip from the 02:53 run corrected and disclosed, outcome-neutral). Why not 9.5: no brief executed and the queue is frozen - this is the 9th consecutive identical stall, the second-seat unblock is still dispatcher-side and outstanding, so the run records a correct skip rather than shipped value. Matches the 8.5 precedent for the identical stall pattern (0253, 0153, 0048, 2343, 2241). No gap follow-up (below 9.0). No PHANTOM, no sub-7.0."
}

with open("twelve-lane-scores.jsonl", "a") as f:
    f.write(json.dumps(row) + "\n")

print("appended score 8.5 for gate-stall-20261111-0358.md")
