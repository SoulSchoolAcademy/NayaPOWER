import json
row = {
    "tick": "t0600",
    "agent": "Team Naya Scorer",
    "lane": 1,
    "task": "D2-gap verdict: per-class floor calibration FALSIFIED (section-addressed stays)",
    "receipt": "t0600-lane1.md",
    "score": 9.0,
    "note": "VERIFIED this tick on live workspace bytes: hidden_files/scratch-t0600-lane1/verdict-t0600-lane1.md sha256 d4640bbf... matches receipt pin exactly; results-t0600-lane1.json c50e27f2... matches exactly; prereg-t0600.json f71ba4fe... matches exactly. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane honest 9.0. Why not 9.5: (1) E4 relevance classification is a single-seat judgment - blinded second-seat rating of the raw winners is owed and named in the receipt; (2) the distribution summary was computed during dry-fire exploration before the formal pre-reg freeze, so E1-E3 are observed-not-predicted rather than true blind predictions; (3) verdict is time-bounded to pinned tip bdfb5868a1ef while origin had already moved twice since t0595, so re-baseline on the new tip is owed before further seam measurements. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed, gap not added to gap-followup-seen.json. No PHANTOM, no lane below 7.0 this tick. Backlog: independent-score backlog 466 before this tick, 465 after (1 scored this tick). Fresh window empty after this score."
}
path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
with open(path, "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended ok")
