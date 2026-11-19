import json

HF = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
OUT = HF + '/twelve-lane-scores.jsonl'

rows = [
    {
        "tick": "t0802",
        "agent": "Team Naya Scorer",
        "lane": 2,
        "task": "STALE BRIEF verified-done: EQ1-EQ4 retrieval-auth gate probe independently re-run, byte-identical results",
        "receipt": "t0802-lane2.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: probe hidden_files/retrieval-auth-gate-eq-probe-20261014-1910-lane4.py sha256 0ddabc02... matches the receipt pin exactly; results eq-probe-results-20261014-1910-lane4.json c9126f21... matches exactly; gap-followup-seen.json carries the scorer-20261014-1910-lane4 closure entry. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching the receipt self-score 9.0. Why not 9.5: (1) the probe was NOT re-executed this tick (SHA pins only), so the byte-identical re-run rests on the action-time record; (2) verification-only work, no new probe construction (the receipt's own gap); (3) single seat, and the staleness was discovered post-claim, not pre-claim. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0802",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Merge-readiness verdict on Hub-Supabase bridge branch (PR #2754): MERGE-READY at code level",
        "receipt": "t0802-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes, with time-decay: git ls-remote on SoulSchoolAcademy/NayaPOWER refs/heads/naya4/t0800-lane0-supabase-bridge returns bd1563c1..., NOT the receipt-certified head 8dad8451... (branch moved since, matching the t0800-lane0 score row). NOT PHANTOM: the receipt is specific, internally consistent, and its four-leg verdict structure (head cert, two-method conflict proof, 14/14 gate, live proof rows) is coherent. Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.5. Why not 9.5: (1) head moved, so current merge-readiness cannot be re-pinned at the certified head today - the verdict is historical, not live; (2) the board leg (#2721 comment 6245393485) and the live Supabase proof rows were NOT re-verified this tick (REST avoided per hard constraints); (3) single seat, and the tune-in miss stands as the receipt's own residual gap. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0808",
        "agent": "Team Naya Scorer",
        "lane": 11,
        "task": "HV observatory window 4 + hv_measure.py time-header parsing root fix with regression proof",
        "receipt": "t0808-lane11.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes, mixed: audit lane-11/metric_audit_t0808.json sha256 e89adb7d... matches the receipt pin exactly (11 rows, window t0791-t0808); instrument bin/hv_measure.py now hashes a83e2ab0... vs the receipt pin 663d1ec7... - the file evolved after receipt, so receipt-time instrument bytes are not re-pinnable (time-decay, not fabrication); /tmp regression proofs are gone, so the x2 byte-identical runs rest on the action-time record. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.5. Why not 9.5: (1) instrument SHA drift + ephemeral /tmp proofs mean the regression claim is receipt-attested, not re-verified today; (2) single-seat judgment audit (M2 8 / M3 5 / M4 9 on 11 rows); (3) the M1 board leg still reads the stale #2175 cache, not the live board (receipt's own named limitation, unfixed here); (4) class-#17 brief-head-before-sign-in recurrence. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0809",
        "agent": "Team Naya Scorer",
        "lane": 3,
        "task": "#2377 consolidation-repair owner named from live bytes + checklist delivered on #2537",
        "receipt": "t0809-lane3.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes, partially: receipt file exists and is internally consistent (merge-commit-first forensics, PR-head isolation, t0796-trap check, routing record line, board comment 6184852664, receipt_checker PASS all cohere). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.5. Why not 9.5: (1) the git-protocol legs (merge 01ba1f3a..., PR commit 1ae5d07c..., blob 0ff5e650...) were NOT re-fetched this tick (no clone made) and the board leg was NOT re-verified (REST avoided per hard constraints), so the attribution rests on the action-time record; (2) the PR-body Seat: line confirmation - the receipt's own named hole - remains owed by a seat with REST-read authority; (3) single seat, no independent corroboration of the attribution; (4) class-#17 recurrence owned in the receipt. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0810",
        "agent": "Team Naya Scorer",
        "lane": 1,
        "task": "Independent harness review of semantic-arm harness: 5 defects + falsified builder quote, verdict file",
        "receipt": "t0810-lane1.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: verdict hidden_files/harness-review-t0810-lane1.md sha256 f39bc2de... matches the receipt pin exactly; harness bin/semantic_arm_harness.py a7e72ce9... matches exactly; corpus pin file content aaf978c1... matches the receipt pin exactly. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.3. Why not 9.5: (1) the RED-first and edge probes (R1-R7, D1-D5) ran in /tmp at action time and were NOT re-executed this tick (SHA pins only); (2) single-seat review, no second-seat adoption check; (3) the receipt's own Pass-2 gaps (b) and (c) remain unclosed inside a review tick by design. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
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
print('appended', len(rows), 'rows; total score rows now', n)
