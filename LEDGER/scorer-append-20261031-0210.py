import json

HF = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
OUT = HF + '/twelve-lane-scores.jsonl'

rows = [
    {
        "tick": "t0805",
        "agent": "Team Naya Scorer",
        "lane": 5,
        "task": "VOID fail-closed: blind level-drill brief refused on prior key contact (t0755 + t0761)",
        "receipt": "t0805-lane5.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt file exists; both cited contact receipts exist in twelve-lane-receipts/ and carry the key-contact markers (t0755-lane1.md contains level_drill_key and level_drill_grade; t0761-lane11.md is a VOID receipt mentioning the answer key). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below receipt self-score 9.4. Why not 9.5: (1) the board leg (#2537 comment 6184544713) was NOT re-verified this tick (REST avoided per hard constraints); (2) the void ships no run and no cleared work - its value is prevention, and the dispatcher eligibility gate that caused the void is still unmechanized (t0750 recurrence, receipt's own hole 1); (3) single seat, and the t0755 step-6 wording rests on the receipt's quotation, keyword-confirmed only. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0806",
        "agent": "Team Naya Scorer",
        "lane": 7,
        "task": "REGISTER-FLIP battery pre-reg frozen and sealed, K2 fail-closed (battery held)",
        "receipt": "t0806-lane7.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes, all four pins EXACT: pre-reg register-flip-prereg-t0806-lane7.md sha256 ccc5e2eecb1646128392b1e47b23aba7fd50de0c3c6bb469167f958ebaf656b0; spec register-flip-protocol-spec-t0770-lane8.md 91412fc298adf90a9f097b16bd8deef81f86f3a987483ec4c4e03f894309f7f9; design lane-1/surge-a-hypothesis-change-t0761.md 3b685b90c98f754c6151ba4ce8b7b951fa4a967c8a2746be948f3e0d56173efe; gate bin/value_calculus.py 25ddc96971a16f054a86a03025ec694f34b097f125b5db9ffcb805a850a78822. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below receipt self-score 9.2. Why not 9.5: (1) K2 positive doc set is a named failure, not a pin, so the battery is HELD and the brief's full done is unreached; (2) the 24-doc K1 derivation and the lexicon rule set were NOT re-run or independently re-implemented this tick (SHA pins only); (3) S0 situation bytes remain ephemeral (/tmp, receipt's own hole 2). GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0807",
        "agent": "Team Naya Scorer",
        "lane": 9,
        "task": "Battery v2 for semantic-arm harness: rank-sensitive metrics, tie-break pinned opposite to docs",
        "receipt": "t0807-lane9.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: battery batteries/t0412-v2-rank/ exists with runs/t0807-tfidf.json sha256 97f58ae49854c0e5 matching the receipt exactly; corpus.json sha256 b231f055fb95955260c901309727423275739b826e61374c454de22506a80d91 matching the receipt pin exactly; run file carries harness script prefix a7e72ce9, arm prefix 75d22842, corpus pin_verified true, matching the receipt; builder bin/build_t0412_v2_battery.py exists. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below receipt final self-score 9.2. Why not 9.5: (1) the harness run and the identical-text tie experiment were NOT re-executed this tick (SHA/pin verification only); (2) the false tie-break docstring in build_t0412_baseline_battery.py is still unfixed at receipt time and was not checked fixed today; (3) the lexical arm tie-break remains unverified (receipt's own named follow-up). GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
]

with open(OUT, 'a') as f:
    for r in rows:
        f.write(json.dumps(r) + '\n')

n = 0
for line in open(OUT):
    if line.strip():
        json.loads(line)
        n += 1
print('appended 3 rows; total score rows now', n)
