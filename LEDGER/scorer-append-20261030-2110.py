#!/usr/bin/env python3
"""Scorer append for tick 20261030-2110: backlog sweep, oldest-first t0748/t0765/t0766."""
import json, os

base = os.path.expanduser("~/workspace/goals/bring-naya-to-life/hidden_files")
entries = [
    {
        "tick": "t0748",
        "agent": "Team Naya Scorer",
        "lane": 6,
        "task": "Verdict-instability adjudication: FM#61 candidate root-caused to API-blind fail-closed transport",
        "receipt": "t0748-lane6.md",
        "score": 9.0,
        "note": (
            "VERIFIED in part on live bytes: receipt file exists (7875 bytes); brief brief-t0748-lane6.md sits in brief-queue/done/ (not claimed/); "
            "receipt is internally consistent (7 quoted log lines with job ids, line numbers, identical head 7847be0603474a404de51575815284808b0d77ce across the (a) runs, "
            "falsifier test applied to both instances, holes named not hidden). NOT PHANTOM on the action-time record. "
            "The board leg could NOT be re-verified this tick: #2537 comment 6167590868 and the 7 job logs were not re-pulled (REST avoided per budget law; logs are 16 days old), "
            "so the quoted lines rest on the action-time record, not a live re-pin; no branch/SHA is cited, so the git leg does not apply. "
            "Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.5. "
            "Why not 9.5: (1) the re-pinned #2576 body's 'Receipt gate green x2' claim stays unreconciled (receipt's own hole 1); "
            "(2) the claim-gate 403s as rate-limit (vs permission) is inference from same-batch corroboration, not header-proven (hole 2); "
            "(3) no body-hash logging, so 'body identical' in (b) rests on same-head plus no-edit evidence, not a hash (hole 3); "
            "(4) board/log legs not re-verified this tick. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
        ),
    },
    {
        "tick": "t0765",
        "agent": "Team Naya Scorer",
        "lane": 11,
        "task": "First independent measurement of genuine human-value events: honest count 0",
        "receipt": "t0765-lane11.md",
        "score": 9.0,
        "note": (
            "VERIFIED this tick on live bytes: receipt file exists (8238 bytes); value-ledger.md sha256 230b98135cba12be8d41208b1c9cb4339536a167c8351e696d116a0a3639df64 "
            "byte-matches the receipt pin prefix 230b98135cba12be exactly; value-counts-timeseries.md carries the t0765 row (0 events, same ledger_sha16, Mu's-five caveat stated); "
            "instrument human-value-instrument-v1.md and seed value-ledger-seed-t0690.md both exist; brief brief-t0765-lane11.md sits in brief-queue/done/. NOT PHANTOM. "
            "Score 9.0, GOOD, ONE MORE PASS, matching the receipt self-score 9.0. "
            "Why not 9.5: (1) single-seat closeout of a timed-out worker's measurement - no independent second-seat re-run of the zero; "
            "(2) Mu's-five board-side status is UNVERIFIED beyond the 100 most recent #2537 comments - the full 1,198-comment scan is owed, not assumed (receipt says so itself); "
            "(3) the time-series is initialized, not yet proven as a delta mechanism; (4) no human-outcome collection channel exists, flagged as NEEDS without an assigned owner. "
            "GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
        ),
    },
    {
        "tick": "t0766",
        "agent": "Team Naya Scorer",
        "lane": 1,
        "task": "Class-#17 violation detector built, proven live (28 violations), controls + regression battery",
        "receipt": "t0766-lane1.md",
        "score": 9.0,
        "note": (
            "VERIFIED this tick on live bytes: receipt file exists (6411 bytes); violation-detector-class17.py sha256 "
            "085f592e2f4e8152bdc592c0bad6c26f545983ac330a16cf9fc3485fcef62635 byte-matches the receipt pin exactly (64/64); "
            "python3 -m py_compile passes clean; next-class note violation-detector-next-class-note-t0766.md exists (1958 bytes); "
            "brief brief-t0766-lane1.md sits in brief-queue/done/. NOT PHANTOM. "
            "Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.5. "
            "Why not 9.5: (1) the 28/28 live catch, positive/negative/fail-closed controls and 8/8+4/4 regression battery rest on the action-time record - not re-run this tick "
            "(the feed has since grown, so a re-run would not reproduce 28/28); (2) second-seat review of the 8 patterns is owed, not done (receipt's own item 9, NOT LANDED); "
            "(3) the excuse-cluster taxonomy is surfaced, not classified (item 10, NOT LANDED); (4) the timestamp heuristic stays a heuristic, documented but unproven against fresh mislabelings. "
            "GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
        ),
    },
]
path = os.path.join(base, "twelve-lane-scores.jsonl")
with open(path, "a") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")
print("appended:", [(e["tick"], e["receipt"], e["score"]) for e in entries])
with open(path) as f:
    lines = f.readlines()
for e in entries:
    assert json.loads(lines[-3 + entries.index(e)])["receipt"] == e["receipt"]
print("all new lines parse; total score lines now:", len(lines))
