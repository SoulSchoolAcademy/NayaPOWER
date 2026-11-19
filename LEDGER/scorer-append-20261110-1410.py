import json, datetime
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
row = {
    "tick": "gate-stall-20261110-1404",
    "agent": "Team Naya Scorer",
    "lane": 0,
    "task": "Lane-executor stall run 2026-11-10 14:04 PST: evaluate all 30 unclaimed briefs, claim none (28 exit 7 + 2 exit 2)",
    "receipt": "gate-stall-20261110-1404.md",
    "score": 8.5,
    "scored_at": now,
    "note": "VERIFIED this tick on workspace bytes: (1) the receipt's 30 blocked briefs (names + exit codes) match the live brief-queue/ set 30/30 exactly, and the list is IDENTICAL to the 13:01 receipt's list - delta zero is correctly stated; (2) cap compliance TRUE - prior stall receipt mtime 21:01:24Z vs this one 22:05:32Z = 64m08s, outside the 60-min window, and the '63 minutes old' recency claim is accurate (run 14:04 PST); (3) the 'four briefs carry explicit seat bars' count is consistent, and both exit-2 bar texts verified present in the brief files (brief-gap-gap-t1002-lane2.md CLAIMABILITY GATE bar; brief-gap-gap-gap-gap-t0172-lane1-lane1.md routing-prose bar). Score 8.5, REWORK. Why not 9.5: NO claim-sweep log exists for this run - newest log is claim-sweep-20261110-1303.log, the 13:01 run's late-arriving evidence, so the 30 script-attempt exit codes are unverifiable this run. This is the exact defect the 13:01 original 8.5 named, repeated; per that score's own rule ('then it clears 9.0'), the receipt clears 9.0 only when a matching sweep log arrives. The receipt's self-score of 9.0 is inflated by that gap. Secondary: 48th consecutive identical stall since 2026-11-08, no cleared work shipped - the queue's blockage is structural (every brief needs a second seat or a dispatcher stamp) and this seat cannot clear it alone. No gap-recycle: score below 9.0 (and queued=30 >= 30 throttles gap-recycling to zero anyway)."
}
with open("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl", "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended 1 score")
