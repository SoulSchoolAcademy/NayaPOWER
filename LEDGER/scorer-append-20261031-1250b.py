import json
path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0948",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "SB-D2 writer-side origin markers re-dispatch: verify hole closed, do not rebuild",
        "receipt": "t0948-lane10.md",
        "score": 9.3,
        "note": "VERIFIED this tick on live bytes: hidden_files/bin/ask-world.py sha256 2139f493ab23fa8e8ebe1271f13a674625f30e01f145bb631ab03f32b1132cbb and hidden_files/bin/check-origin-markers.py sha256 2c4776c2230bfe7b583c2636b2aa89fa22354a3c69565299305ceb50f90d435d, both exactly matching the receipt cites; fresh check run this tick: OK 50/50 rows carry valid origin_marker, and independent read of hidden_files/auto-retrieval/ask-world-queries.jsonl shows 0 marker-less in the last 50 with tail format_version 3. NOT PHANTOM. Score 9.3, GOOD, ONE MORE PASS. Why not 9.5: (1) verification-only by design - the hole was already closed by t0903, so this tick ships confirmation, not a new artifact; (2) the log has grown 191 rows at receipt time to 199 now, so today's 50-row window is a later window than the receipt's, re-proven but not byte-identical to it; (3) single-seat re-verification, no second-seat confirmation. The lane correctly did NOT rebuild on a premise-rotted re-dispatch. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
