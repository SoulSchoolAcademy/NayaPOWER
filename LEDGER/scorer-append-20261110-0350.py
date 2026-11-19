import json, datetime
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
rows = [
    {
        "tick": "t0537-lane12",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Sealed cold-retrieve drill re-run with page-cache isolation on byte-identical tip; verdict CONFIRMED vs t0472 baseline",
        "receipt": "t0537-lane12.md",
        "score": 9.0,
        "scored_at": now,
        "note": "VERIFIED this tick on live bytes: run record hidden_files/auto-retrieval/cold-drill-t0537-lane12.md sha256 ead87a17... MATCHES receipt; results json f84d724d... MATCHES; instrument cold_drill_t0537_lane12.py 7dd61a99... MATCHES; tip dbe06f9e exists as a commit. Drill 15/15 gate-COLD, cold median 0.996s vs t0472 1.065s / t0530 1.019s, clustering within 7% across three independent runs on the byte-identical tip. NOT PHANTOM. Score 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) the gate RED demonstration was NOT re-run this tick - it leans on t0530's bytes on the byte-identical tip, sound but not fresh; (2) single frozen query, multi-query AUDIT-P0 battery still open (Lane 5 owner); (3) t0472 residuals #1-#3 stated, not closed. NO GAP-RECYCLE FILED: rotation queued=31 >= 30 throttles gap-recycling to zero this tick."
    },
    {
        "tick": "t0537-lane2",
        "agent": "Team Naya Scorer",
        "lane": 2,
        "task": "Dual-view bi-encoder semantic arm vs t0532 battery; FALSIFIED 1/3, P2 winmine control holds",
        "receipt": "t0537-lane2.md",
        "score": 9.0,
        "scored_at": now,
        "note": "VERIFIED this tick on live bytes: results hidden_files/auto-retrieval/results-t0537-semantic.json sha256 f0e745ee... MATCHES receipt; instrument t0537_semantic.py 9eaa0975... MATCHES. Arm run honestly FALSIFIED (1/3 tasks clear >=2/3) under the RED-certified battery, with positive calibration shown (battery fails t0432 and t0442 in two distinct shapes, so it discriminates and is not a blanket rejector); P2 winmine control holds, P5 byte-identical across two fresh-process runs. NOT PHANTOM. Score 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) doer=scorer, non-blind instrument - declared but a gap is a gap; (2) P5 used two fresh processes on one checkout, not two independent checkouts - partial by the battery's letter; (3) N=3 tasks, single seat, no second-seat verification of the battery evaluation. NO GAP-RECYCLE FILED: rotation queued=31 >= 30 throttles gap-recycling to zero this tick."
    },
    {
        "tick": "t0537-lane9",
        "agent": "Team Naya Scorer",
        "lane": 9,
        "task": "Retrieval-authorization-gate wiring packet branch (refusal contract + 18 tests + RED demo), AWAITING-SHAWN, no merge",
        "receipt": "t0537-lane9.md",
        "score": 9.0,
        "scored_at": now,
        "note": "VERIFIED this tick on live bytes: branch naya/nine-retrieval-auth-wire-packet-t0537 EXISTS on remote; pinned SHA 9a7c60247b58fb82ed8bbdd24206d2b0f7bc6c55 EXISTS as a commit and all 4 packet files are present at that SHA (git ls-tree: refusal_point, test_refusal_predicate, red_demo_refusal, retrieval-auth-wire-packet doc); base tip dbe06f9e exists as a commit. HEAD DRIFT NOTED: branch head has since moved to 99a2f832 (pinned commit is not its ancestor - later force-push/rebase), so the SHA no longer matches the live head; the receipt was accurate when filed (pinned via ls-remote at the time) and every cited artifact still exists at the pinned SHA, so NOT PHANTOM. Refusal suite 18/18 + gate suite 25/25 claims are taken on the receipt's account (not re-executed this tick). Score 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) single-seat proof - no independent seat reproduced the refusal suite or reviewed the contract; (2) M3 corpus-stamping designed, not executable code - stamping authority decision still open; (3) sign-in posted after the brief-claim mv (owned in receipt). NO GAP-RECYCLE FILED: rotation queued=31 >= 30 throttles gap-recycling to zero this tick."
    },
]
with open("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl", "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows), "scores")
