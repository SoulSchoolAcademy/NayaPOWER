#!/usr/bin/env python3
import json

row = {
    "tick": "lane-scorer-20261114-0240",
    "agent": "Team Naya Scorer",
    "lane": 9,
    "task": "gap-t0580b follow-up: cold-retrieve drill against live main tip, seal firing on moved seam",
    "receipt_file": "gap-t0580b-lane9.md",
    "score": 9.0,
    "scored_at_utc": "2026-11-14T10:42:00Z",
    "scorer": "lane-scorer",
    "note": (
        "Backlog sweep (fresh window empty; oldest unscored gap receipt, Oct 14). Verified first-hand in "
        "the rescue repo: commit ba62638704256b012c20e41fe7f53cc3b62b1b44 exists; "
        "tools/smart_note_v2.py at that commit hashes to fe6f2b4cec84b62f2431a6389cc88aa842a40e3c4aa268593d259b719e098851 "
        "exactly as the receipt quotes (SEAL_C pin mismatch confirmed, not asserted); the two file-touching "
        "commits at that tip are a5b7ff65f (B-51 validator) and 2e17cad9d (B-49/B-58 winner-read) exactly as "
        "cited. The receipt's honest refusal (seal exit 4, no number quoted against changed bytes) closes the "
        "gap's 'or' clause in bytes, and the t1052 HOLDS-OPEN closure argument is byte-grounded. NOT PHANTOM. "
        "Score 9.0, GOOD ONE MORE PASS (lane self-score 9.0). Why not 9.5: (1) the gap asked for a live-tip "
        "measurement and none exists - the deliverable is a refusal, not a number, until Lane 7 re-seals "
        "SEAL_C and re-anchors the band; (2) the sealed-instrument run itself (exit 4) was not re-executed by "
        "this scorer - its transcript rests on the receipt; (3) single-seat, and the B-51/B-49/B-58 diff "
        "attribution is read from commit subjects, not re-verified against board text. Gap-recycle: NO "
        "follow-up filed - the named gap (re-seal at ba626387) is a month stale, tip long moved; the re-seal "
        "belongs to the instrument owner's live work, not a stale-tip brief. Seen-key recorded as moot."
    ),
}
with open("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl", "a") as f:
    f.write(json.dumps(row) + "\n")
print("appended score row for lane-scorer-20261114-0240 lane 9")
