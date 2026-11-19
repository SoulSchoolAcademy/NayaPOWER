import json, os
p = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {"tick": "t0612", "agent": "Team Naya Scorer", "lane": 3,
     "task": "SURGE slice (c) query-side schema-coverage analysis",
     "receipt": "t0612-lane3.md", "score": 9.0,
     "note": "VERIFIED this tick on live bytes, pin-exact: hidden_files/surge/querylog-needs-t0612.md sha256 636b3b82e6b4ac58616821573722079560bc4ccc09c3e1059ea056de795c669a matches receipt pin, 13790 bytes as claimed. NOT PHANTOM. The ask-world log pin (57f0c922...) no longer matches live bytes (now 60358 bytes) because the shared log has grown by later appends since action time; the action-time pin is corroborated by t0613-lane7's independent re-pin of the identical sha. Score 9.0, GOOD, ONE MORE PASS, above lane self-score 8.5 because the deliverable is complete (two-layer coverage finding + two falsified brief premises recorded). Why not 9.5: (1) v1's 6 failing lint checks not enumerated by name (receipt's own gap); (2) writer-side contract H3 is a shape proposal, not executable text; (3) no second-seat re-run of the lint; counts inherited, not re-derived this tick. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. Backlog: t-pattern receipts lacking an independent Team Naya Scorer score 268 before this tick, 265 after (t0612 lanes 3, 10 and t0613 lane 7 scored). No PHANTOM, no lane below 7.0 this tick."},
    {"tick": "t0612", "agent": "Team Naya Scorer", "lane": 10,
     "task": "Brain-index drift verification at the moved tip",
     "receipt": "t0612-lane10.md", "score": 9.0,
     "note": "VERIFIED this tick: action-time tip pin e47a650e2f05935cb57b02f0f368452b346148e1 confirmed as a preserved commit via the commits API (merge of PR #2512, 2026-10-13T08:09Z), consistent with the receipt's 'PRs #2501-#2512 merged' account; current HEAD has since moved to e445a597d. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane self-score 9.0. Why not 9.5: (1) --check exit 0 and 13/13 freshness suite not re-run this tick - execution inherited, tip existence verified; (2) #2385 base staleness noted but unadjudicated (receipt's own gap); (3) freshness gate still advisory-only, recurrence #16 structurally open. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."},
    {"tick": "t0613", "agent": "Team Naya Scorer", "lane": 7,
     "task": "Demand-source map for the ask-world log",
     "receipt": "t0613-lane7.md", "score": 9.0,
     "note": "VERIFIED this tick on live bytes, pin-exact: hidden_files/retrieval/demand-source-map-t0613.md sha256 2f7deb8d1ce6548aa6707016940b56638e8a34127e7b8d140fbb9b3cafa712fd matches receipt pin, 6688 bytes as claimed. NOT PHANTOM. The log pin (57f0c922...) drift is the same later-appends explanation as t0612-lane3, corroborated at action time by this receipt's own re-pin. Score 9.0, GOOD, ONE MORE PASS, above lane self-score 8.5 because the S1-synthetic/S2-self-packet split is a genuine load-bearing finding with a stated evidence bar and a named re-arm path. Why not 9.5: (1) S1 seed-loop producer unattributed (receipt's own gap); (2) lane-5/lane-3 feed correlations rest on session-timing inference, not an agent tag; (3) single-seat verdict, no second-seat check of the RESTORABLE bar; (4) run-clock jump caveat on sign-in times. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."},
]
with open(p, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
