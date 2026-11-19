import json

rows = [
    {
        "tick": "t0605",
        "agent": "Team Naya Scorer",
        "lane": 2,
        "task": "blinded recount of Mason's t0598 pooling arm",
        "receipt": "t0605-lane2.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live workspace bytes: instrument arm_poolmax_recount_t0605.py sha16 EXACT to receipt pin f28e453e83b49c18; blinded verdict results-t0605-poolmax-recount.json sha16 EXACT to pin 190447280d7a52d3; sealed note exists. No git branch/SHA cited (worker-local battery), so the branch-head leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane self-9.0. Why not 9.5: doer=scorer single seat (blinded vs designer but not vs itself); N=3 tasks eternal confound with GUARD-RR threshold single-calibrated; per-doc score cells are recount-only, not directly compared to Mason's file. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick.",
    },
    {
        "tick": "t0605",
        "agent": "Team Naya Scorer",
        "lane": 8,
        "task": "adversarial bypass audit of the retrieval-auth gate candidate",
        "receipt": "t0605-lane8.md",
        "score": 9.0,
        "note": "VERIFIED this tick: probe script and results-t0605-bypass.json exist; results sha16 EXACT to receipt pin fc685b907dc0e174; git ls-remote in the recon mirror returns branch naya/five-retrieval-auth-gate-t942 at EXACTLY e654f16e8a49e9a26309fd852695a0bef202673d, the receipted head. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, agreeing with lane self-9.0. Why not 9.5: all 10 probes are synthetic fixtures against the candidate module with no live retrieve() seam integration; single seat with no independent re-run of the probe battery. GAP-RECYCLE THROTTLED this tick (queued 31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick.",
    },
    {
        "tick": "t0605",
        "agent": "Team Naya Scorer",
        "lane": 11,
        "task": "SURGE evidence ledger t0538-t0604: CONFIRMED, FALSIFIED, and still-not-built",
        "receipt": "t0605-lane11.md",
        "score": 8.5,
        "note": "VERIFIED this tick on live workspace bytes: ledger surge-evidence-ledger-t0605.json exists with 68 rows (61 arm + 7 context), lineage 47 single / 12 second / 2 blinded-second / 7 context, and its receipt_sha_list_sha256 field EXACTLY matches the receipted 391ff2aafbdcdbf222c9090737d4cd7849870fc10183bc0ec9688171eef5e28c. Whole-file sha256 differs from the receipted f6cc9083... because a later extension (2026-10-15 lane-11 follow-up) re-extracted holed rows and recomputed counts (now FALSIFIED 13 / ARM 8 vs receipted 11 / 6) - drift explained by the receipt's own extend-never-rewrite rule, not fabrication. NOT PHANTOM. Score 8.5, REWORK tier, agreeing with lane honest self-8.5. Why not 9.5: 8 of 68 rows carried verdict-not-re-extracted holes at action time; single-seat lineage on 47/61 arm rows; sub-goal verdicts are prose over quoted verdicts, not independent re-measurements. No gap-recycle (score below 9.0). No PHANTOM, no lane below 7.0 this tick.",
    },
]

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
