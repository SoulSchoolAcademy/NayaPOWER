import json
base = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files"
rows = [
    {"tick": "t0648", "agent": "Team Naya Scorer", "lane": 4,
     "task": "EXECUTE sealed H-dc6 instrument (t0648)",
     "receipt": "t0648-lane4.md", "score": 9.0,
     "note": "VERIFIED this tick, hash-exact on live bytes: auto-retrieval/results-t0633-h-dc6.json sha256 f897f3da59cecdd9e6176c9c759e4175556dc0d91e96dff4f93a8237da7e5ff2 matches the receipt exactly, and verdict-t0633-h-dc6.md opens with RETRACT (winner ablation flips 1/3 < 2/3) with the instrument pin b6e6e7338 matching the receipt, confirming the clean sealed execution (EQ-D0 PASS, heartbeat PASS) and the correctly applied frozen verdict rule. No git branch/SHA is cited for this work, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: single seat with no independent re-verification of the frozen rule's Python against the design prose, and the 'why only 1/72' mechanism reading is the executor's inference, not the instrument's. GAP-RECYCLE THROTTLED this tick (rotation queued=42 >= 30): zero follow-ups filed."},
    {"tick": "t0648", "agent": "Team Naya Scorer", "lane": 5,
     "task": "Stage 0 [WINMINE] - mine 3+ repeatable success patterns from 9.5/10 receipts",
     "receipt": "t0648-lane5.md", "score": 9.0,
     "note": "VERIFIED this tick, hash-exact on live bytes: winmine-success-patterns-t0648.md sha256 a2ad03a326a0de617de0bed0e74d990832592f4b491cc58859272f63b498fadf matches the receipt exactly, with 4 patterns each carrying receipt citations and a behavior delta, and a re-parse check that all 6 cited 9.5 receipts resolve in the jsonl. No git branch/SHA is cited, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: only 6 of the 24 nine-point-five receipts were mined, so the remaining 18 may hold unseen patterns; and with zero sub-7.0 rows the differential half (what loses points) could not be mined from scores alone. GAP-RECYCLE THROTTLED this tick (rotation queued=42 >= 30): zero follow-ups filed."},
    {"tick": "t0649", "agent": "Team Naya Scorer", "lane": 6,
     "task": "Pin-verified determination of BRAIN/CURRENT-MISSION-STATE.md as canonical (SURGE (a) Stage-0 hole-3 close-out)",
     "receipt": "t0649-lane6.md", "score": 9.0,
     "note": "VERIFIED this tick on live bytes: lane-6/t0649-mission-state-pin.md exists (4214 bytes) carrying the FOUND verdict with tip 4f0c9aa8, blob 015dfefe and content sha256 115e2d2e as cited in the receipt, falsifying the brief's 'file absent' premise and closing the t0644 Hole 3 at live bytes. No git branch/SHA is cited for this work itself, so the branch leg does not apply beyond the pinned tip. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: single seat - no independent second seat re-derived the tree entry, blob SHA, or content sha256; and the pin file carries a preview plus pins, not the full 525 KB bytes. GAP-RECYCLE THROTTLED this tick (rotation queued=42 >= 30): zero follow-ups filed."},
    {"tick": "t0650", "agent": "Team Naya Scorer", "lane": 9,
     "task": "Kernel byte-verdict (GREEN/RED) at the live main tip, twice-pinned",
     "receipt": "t0650-lane9.md", "score": 8.5,
     "note": "VERIFIED this tick as far as the historic record allows: receipt file exists with a twice-pinned tip 582e5e5f, instrument green (mjs 11/11, pytest battery 60/1), tree-wide replay 6 failed / 2925 passed, and a RED verdict correctly split into introduced freshness drift (routed to the regen owner) versus pre-existing environment-coupled compound_scale drift (routed to Lane 2), plus the gate-by-design promote-and-prove classification. Live re-running of the 216s tree-wide battery was not done this tick, so counts are inherited from the receipt, not re-derived; no branch for this work is cited, so the branch leg does not apply. NOT PHANTOM. Score 8.5, REWORK tier, matching lane self-score 8.5. Why not 9.5: the CI failing set is named from a local replay rather than CI log bytes (401 on this credential, honestly flagged); the claim-before-sign-in exemption recurred; and no second seat verified the introduced/inherited classification. No gap-recycle: score is below 9.0."},
    {"tick": "t0651", "agent": "Team Naya Scorer", "lane": 11,
     "task": "Hand-read the 78 zero-keyword-floor rows; falsification floor 32.4% becomes a 48.8% rate",
     "receipt": "t0651-lane11.md", "score": 8.5,
     "note": "VERIFIED this tick, hash-exact on live bytes: lane-11/metric_audit_t0651.json sha256 c801497c31a9797eb255fd7d5dfe4b2818fcbdb99f4fb72e35a122c4cba67eb3 matches the receipt exactly, and the rate arithmetic checks: (55 + 28) / 170 = 83/170 = 48.8% on the fully hand-read frame, with 78/78 floor rows judged and 0 UNJUDGEABLE. No git branch/SHA is cited, so the branch leg does not apply. NOT PHANTOM. Score 8.5, REWORK tier, matching lane self-score 8.5. Why not 9.5: single-seat judgments throughout with no second-seat spot-check of the 28 new TRUE rows (a check the FP-001 gate consumer is owed); claim-before-sign-in recurrence #17, owned in the receipt; and the t0645 pin-file SHA citation discrepancy is named but not reconciled. No gap-recycle: score is below 9.0."},
]
with open(base + "/twelve-lane-scores.jsonl", "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
