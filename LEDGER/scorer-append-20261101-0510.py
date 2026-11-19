#!/usr/bin/env python3
"""Lane-scorer tick 2026-11-01 05:10 PDT: backlog sweep, oldest unscored first.
Fresh window (last ~2h) was empty: all 5 receipts since 03:10 PDT already scored.
Scored here: the two oldest unscored gap receipts, both verified from live bytes.
Queued briefs = 41 (>= 30), so GAP-RECYCLE THROTTLED: zero follow-ups filed.
"""
import json

rows = [
    {
        "tick": "20261015-0040",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "gap-scorer 0040 lane12 - refusal of second-seat tag-provenance sweep (exit 7) + self-reported void of false-token claim",
        "receipt": "gap-scorer-20261015-0040-lane12.md",
        "score": 9.0,
        "note": (
            "Verified by this scorer from live bytes: parent receipt t0817-lane12.md exists; "
            "both cited re-derivation artifacts hash byte-exact to the receipt pins "
            "(sweep script b34ba4eb...676, report f06ad7b5...1d00986d94d); the addendum honestly "
            "voids the false-token claim (claim via a foreign --seat token), returns the brief "
            "unclaimed, and re-labels the sweep as a script-level cross-check, never a second-seat "
            "verification. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: the run itself committed "
            "the token bypass it documents (self-caught and voided, but a real integrity lapse), "
            "and the underlying gap - an eligible non-Clarity second-seat re-run of the tag-provenance "
            "sweep - remains open. GAP-RECYCLE THROTTLED this tick (queued 41 >= 30): zero follow-ups filed."
        ),
    },
    {
        "tick": "20261015-0450",
        "agent": "Team Naya Scorer",
        "lane": 1,
        "task": "gap-lane-scorer 0450 lane1 - t0541 zero-finding re-run on frozen retrieval battery",
        "receipt": "gap-lane-scorer-20261015-0450-lane1.md",
        "score": 9.0,
        "note": (
            "Verified by this scorer from live bytes: frozen battery "
            "hidden_files/retrieval/retrieval-hitrate-t0541.py hashes byte-exact to the receipt pin "
            "(df496220...3d75f); --selftest reproduced 5/5 PASS now (phantom->WRONG, renamed->WRONG, "
            "marker->AUTO, no-marker->MANUAL, low-overlap->UNJUDGEABLE); marker census over the current "
            "brief-queue finds 0 auto-retrieved markers, consistent with the receipt's zero finding. "
            "Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: the receipt's own named holes - this run's "
            "measurement JSON was inspected, not pinned to disk; the original 30-brief corpus is gone, "
            "so this is a same-instrument/different-window re-derivation; and the denominator thinned "
            "(6 principles vs 46), so a per-wave denominator definition from the surge owners is still owed. "
            "GAP-RECYCLE THROTTLED this tick (queued 41 >= 30): zero follow-ups filed."
        ),
    },
]

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
existing_receipts = set()
for line in open(path):
    try:
        j = json.loads(line)
    except Exception:
        continue
    if j.get("agent") == "Team Naya Scorer" and j.get("receipt"):
        existing_receipts.add(j["receipt"])
for row in rows:
    assert row["receipt"] not in existing_receipts, "already scored: " + row["receipt"]
with open(path, "a") as f:
    for row in rows:
        f.write(json.dumps(row) + "\n")
print("appended", len(rows), "rows")
for row in rows:
    print(row["tick"], row["receipt"], "score", row["score"])
