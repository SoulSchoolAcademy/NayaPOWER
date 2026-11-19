import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0606",
        "agent": "Team Naya Scorer",
        "lane": 5,
        "task": "H-dc4 sealed arm - consequence-on-treatment-standing, verdict FALSIFIED (saturated)",
        "receipt": "t0606-lane5.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt t0606-lane5.md exists; auto-retrieval/t0606_h_dc4.py sha256 EXACT to receipt pin aac9bd12...; sealed-note-t0606-h-dc4.md sha256 EXACT to pin 95684a27...; results-t0606-h-dc4.json sha256 prefix de9acaa140d1dd36... matches live full hash; results JSON re-read: 72 pairs, delta_lift > 0 on all 72, delta_rank <= 0 on all 72, heartbeat holds, verdict FALSIFIED (saturated 72/72). NOT PHANTOM. SCORE 9.0 GOOD, ONE MORE PASS, agreeing with lane self-9.0. Why not 9.5: (1) designer = executor, no independent design seat touched H-dc4; (2) the SATURATED path fired on count alone, so the F1-F5 discrimination bars are untested, not failed; (3) anti-locality finding measured on one aggregator (max-pool) only, generalization untested. No git branch/SHA cited (worker-local battery), so the branch-head leg does not apply. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick. Backlog after this tick: 330 t-receipts lacking an independent (Team Naya Scorer) score (331 before).",
    },
    {
        "tick": "t0606",
        "agent": "Team Naya Scorer",
        "lane": 7,
        "task": "Journal-rot tree-wide pass - 12 lane journals verified, lane-11 gap fixed, 2 journals distilled",
        "receipt": "t0606-lane7.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt t0606-lane7.md exists; lane-journals/lane-11.md carries the t0605 entry with the provenance note 'Entry added 2026-10-13 by Lane 7 t0606 journal-rot pass' and the receipt's 68-row / 8.5-self-score / scorer-reconciled-9.0 details; lane-journals/lane-7.md carries the t0606 rot-pass entry recording the 12/12 check, the lane-6 tail-3 misread owned, and the 7 spot-checks all MATCH. Journal line counts have grown since (later passes), so the receipt's 225->172 / 203->172 distillation counts are action-time history, not current counts. NOT PHANTOM. SCORE 9.0 GOOD, ONE MORE PASS, agreeing with lane self-9.0. Why not 9.5: (1) the lane-6 near-miss was a verification defect in the lane's own tooling (tail-3 fabricated a gap; caught before any edit, but the defect happened); (2) distillation fact-loss on lane-3/lane-6 compressions has no second-seat verification; (3) score-file vs receipt-honest-score delta diff for lanes other than lane-11 was not audited. No git branch/SHA cited (journal maintenance), so the branch-head leg does not apply. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick. Backlog after this tick: 329 t-receipts lacking an independent score (330 before).",
    },
    {
        "tick": "t0607",
        "agent": "Team Naya Scorer",
        "lane": 9,
        "task": "Blind second-seat re-run of the t0602 provenance BAR corpus, 27/27 cells MATCH",
        "receipt": "t0607-lane9.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt t0607-lane9.md exists; auto-retrieval/blind-verdicts-t0607-lane9.json sha256 EXACT to receipt pin beb964a7...; its check_sha256 434e22a9... matches the receipted instrument pin prefix; re-read of the blind file: 3 briefs, all PASS, 27 check cells, all PASS. NOT PHANTOM. SCORE 9.0 GOOD, ONE MORE PASS, agreeing with lane self-9.0. Why not 9.5: (1) blinding was procedural, not informational - the lane-12 journal's t0602 sign-out pre-exposed '3/3 PASS' before the run, honestly named at sign-in; (2) the t0602 corpus is designer-labeled simulated markers, so the BAR's real test on live dispatcher-emitted markers is still owed; (3) C9 was not exercised (all briefs carry markers) and the instrument's spec pin is docstring-only, not asserted at runtime. No git branch/SHA cited (worker-local re-run), so the branch-head leg does not apply. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick. Backlog after this tick: 328 t-receipts lacking an independent score (329 before).",
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
