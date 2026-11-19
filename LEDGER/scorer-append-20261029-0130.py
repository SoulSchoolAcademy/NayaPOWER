import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t1013",
        "agent": "Team Naya Scorer",
        "lane": 6,
        "task": "succession-protocol-v1 canonical doc (100 lines, proven steps pinned, gaps CANDIDATE)",
        "receipt": "t1013-lane6.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/succession-protocol-v1.md sha256 4f487c2a18b1675e6b9eeb8b994bdb7807649f5f569893a32eb2bc09e6ccf472 exactly as receipted, 100 lines, CANDIDATE marks present (3 hits). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane self-claimed 9.7. Why not 9.5: (1) the pin table's 11 re-derived pins were not re-verified this tick (only the doc SHA was); (2) cold-readability is unproven until an actual cold successor reads v1 (the lane's own gap). Gap-recycle: throttled this tick (queue 31 >= 30), no follow-up filed.",
    },
    {
        "tick": "t1013",
        "agent": "Team Naya Scorer",
        "lane": 5,
        "task": "Lane 5 harness-repair brief RECUSED (arm-fresh on t0810-review authorship)",
        "receipt": "t1013-lane5.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/harness-review-t0810-lane1.md line 3 reads Reviewer Naya Clarity Narzan 4, Lane 1, tick t0810, exactly as the receipt states, so the arm-fresh recusal fires on genuine authorship bytes; recusal pre-repair with harness untouched is consistent with the brief's own rule. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-claimed 9.0. Why not 9.5: (1) the dispatch-level fix the receipt itself names (eligibility stamp in the brief's first-10-line gate window) is not evidenced closed; (2) the brief's current queue state is not verifiable 14 days on, so the carry-forward (brief stays OPEN for an eligible seat) is unverified. Gap-recycle: throttled this tick (queue 31 >= 30), no follow-up filed.",
    },
]

with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

# validate whole file parses
n = 0
for line in open(path):
    if line.strip():
        json.loads(line)
        n += 1
print("appended 2 rows; total parseable rows:", n)
