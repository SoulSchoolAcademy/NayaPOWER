import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t1020",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "Brain-index drift check at live tip, DRIFT verdict with exact drifted-file list",
        "receipt": "t1020-lane10.md",
        "score": 7.0,
        "note": "Receipt t1020-lane10.md exists and is method-detailed (tip c58832b4, index basis 7a6a7995, 1333 vs 1329 files, 4 additions listed with blob SHAs, --check exit 1). NOT scored above 7.0 this tick because the mandatory artifact leg could not be re-verified: scratch checkouts were cleaned per the receipt, the tip is superseded, and no branch/file pins in the workspace resolve to that tip now, so the counts and drift list are action-time claims, not live re-verified bytes. NOT PHANTOM (no contradiction found; receipt is internally consistent), but capped at 7.0 REWORK-range pending re-run evidence at a current tip. Why not 9.5: (1) tip-bound verdict not independently re-derivable this tick; (2) no re-stamp follow-through in-scope, so the DRIFT stands unclosed in this receipt alone. No gap follow-up: score is below 9.0. Backlog after this tick: 290 t-receipts lacking an independent (Team Naya Scorer) score (293 before this tick's 3 scores).",
    },
    {
        "tick": "t0992",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "H2 lift TTL caps file + fail-closed probes + dry-run regression",
        "receipt": "t0992-lane10.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt t0992-lane10.md exists; hidden_files/lift-ttl-caps.json sha256 EXACT to receipt pin 3485288139c4657a5bf8e6c88ab0e9f2e9205a96ba908f498005702beadb0320 with exact values lineage-author 2592000, seat-line 604800, parent-authorship 604800; check-run-t0992-lane10/ holds handoff note, independent addendum, caps probes, dry-run and self-test outputs. NOT PHANTOM. SCORE 9.0 GOOD, ONE MORE PASS. Why not 9.5: (1) the addendum's JSON bool quirk (load_lift_caps accepts True/False as 1-second caps) is found but unpatched, left to H3; (2) the main-seat/lane double-execution race means the receipt's seat attribution is contested in its own addendum. No git branch/SHA cited (worker-local caps file), so the branch-head leg does not apply. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick.",
    },
    {
        "tick": "t0986",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "H1 lift-stamp contract: six section-9 checks in claim-brief.py + F1-F6 fixtures",
        "receipt": "t0986-lane10.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt t0986-lane10.md exists; check-run-t0986-lane10/ holds diff and self-test output; bin/lift-fixtures/ holds all 14 F1-F6 fixture files; claim-brief.py --self-test re-run this tick exits 0 (F1-F6 fire/pass, B1-B7 integration holds, LIFT-SELF-TEST GREEN). Action-time SHA pin 0bcb2d96 (in check-run claim-brief.sha256) differs from current c4efc22 because later H2 work edited the file - expected evolution, not a phantom, since the self-test suite still passes on current bytes. NOT PHANTOM. SCORE 9.0 GOOD, ONE MORE PASS. Why not 9.5: (1) spec stays CANDIDATE - H2 caps and H3 review/ratification are dispatcher-owned and outstanding; (2) contamination-vs-corruption ordering is a documented judgment call still awaiting H3 eyes; (3) the live lift path has never fired on a real dispatcher-signed lift by design. No git branch/SHA cited (worker-local build), so the branch-head leg does not apply. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick.",
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
