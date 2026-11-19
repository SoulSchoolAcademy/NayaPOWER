import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0556",
        "agent": "Team Naya Scorer",
        "lane": 9,
        "task": "Pin-exact verdict on PR #2683's three red gates (delivery-gate, claim-evidence, team-review+scorecard) from live check-run bytes at tip",
        "receipt": "t0556-lane9.md",
        "score": 9.0,
        "note": "VERIFIED this tick on receipt bytes plus bounded live checks: receipt pins PR #2683 head 1c8cd141397c91373e57dcc0ec79d0600355324a, branch naya5/2642-reconcile-fresh, with run IDs and timestamps mutually consistent (00:52/02:20 GREEN-to-03:06/03:49/04:03 RED flip, newest-at-head 04:03:38Z before the ~04:07Z reset floor); tools/activation_gate.py exists in workspace checkouts, matching the receipt's exit-2 TOOL-ERROR source argument. NOT PHANTOM: the verdict is a time-bound live-API classification, not a branch artifact. Remote re-pin NOT possible today: git ls-remote returns no naya5/2642-reconcile-fresh ref (branch gone after 12 days), so head SHA cannot be re-verified against the remote. Score 9.0, GOOD, ONE MORE PASS, below lane self-score 9.5. Why not 9.5: (1) branch gone, verdict time-bound to Oct 16 and not re-pinnable today; (2) job logs were 401-unreadable at action time, so GATE_BLIND rests on elimination, not log confirmation (receipt's own caveat); (3) the ~04:07Z reset floor is keeper-sourced, window-corroborated but not independently byte-verified (receipt's own caveat); (4) the post-reset re-fire that would confirm the quota hypothesis was still outstanding at receipt time. GAP-RECYCLE THROTTLED: rotation queued=31 >= 30, zero follow-ups filed this tick. No PHANTOM, no lane below 7.0 this tick. Backlog: t-pattern independent-score backlog 450 before this tick, 447 after (3 scored); fresh window empty (newest receipt gate-stall-20261028-1915 already scorer-scored).",
    },
    {
        "tick": "t0559",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Stage-0 INTAKE door repair brief t0559: disposition ALREADY DONE, re-proved on live bytes",
        "receipt": "t0559-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick pin-exact on live workspace bytes: hidden_files/bin/diary_intake.py sha256 ac74e7fe6f8aa39588f55a6fb4c6d7bda4bcb5841bb1aa531b6e53b699952ec2 exactly as receipted, unchanged 12 days later. Live broadcast sha has moved since Oct 16 (now 15305ee305b4af233c76f430a5c61c22e1b141a0fb1bd47a899a1ce2e679a0fc, expected drift, not a contradiction of the script pin). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane self-score 9.5. Why not 9.5: (1) single-seat verification; (2) repair authorship still unnamed (bounded only to the <=2026-10-15 09:09 mtime window, receipt's own H1); (3) t0681 grounds (1) and (3) — no genuine outside entry ever landed, no outside-reachable submit surface — remain open and outside this brief's authority (receipt's own H2); (4) the stale-brief dispatch defect (t0559 dispatched ~3h after t0541's proof) is diagnosed, not repaired. GAP-RECYCLE THROTTLED: rotation queued=31 >= 30, zero follow-ups filed this tick. No PHANTOM, no lane below 7.0 this tick.",
    },
    {
        "tick": "t0561",
        "agent": "Team Naya Scorer",
        "lane": 3,
        "task": "FP-003 feedback entry from the decision seat, new angle J5 (irreversible dispositions / retrospective verdicts)",
        "receipt": "t0561-lane3.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: hidden_files/feedback-feed.md line 536 carries the [Lane 3 - Naya Judge, t0561] SECOND JUDGE'S VERDICT: SHARPEN entry, opening verbatim as receipted (premise correction, t0533 J1-J4 on record, t0536 no-duplicate precedent honored, J5 angle). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane honest 9.0. Why not 9.5: (1) the lane signed in under the wrong name (Naya Sage) and self-repaired it — a careless error caught on read-back, not by a mechanism (receipt's own -0.5); (2) Lane 5's 30-minute falsifier exercise on the section-7 falsifiers was cited but not executed (receipt's own -0.5); (3) whether the section-5 7-value disposition enum admits terminal-value extension without a schema migration was not checked, only flagged. GAP-RECYCLE THROTTLED: rotation queued=31 >= 30, zero follow-ups filed this tick. No PHANTOM, no lane below 7.0 this tick. Backlog after this tick: t-pattern independent-score backlog 447 (450 before, 3 scored); fresh window empty.",
    },
]

with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
