import json

rows = [
    {
        "tick": "t0583", "agent": "Team Naya Scorer", "lane": 1,
        "task": "Independent four-way re-run of the t0568 veracity verdict on the frozen t1412 X-fixture pool, verdict CONFIRM",
        "score": 9.0,
        "note": "Verified by this scorer from live bytes: report lane1-t0583-veracity-rerun.md sha256 99092d83914e2e4110f9630b895af30687e33c35c7a73f1051fb528accadde74 and independent guard scratch-t0583-lane1/rerun_veracity_guard.py sha256 991f628b23b8fe96a149af678d00093f71a1ced41ee2d2811f4657dd8cd9d939 both match the receipt exactly; rerun-output-t0583.txt present. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) shared-text risk - the second guard derives from the same published R1-R4 text, so a shared misreading would reproduce, not detect; (2) REFUSE arm pool_size=1 only - no multi-falsified pool, below-floor-falsified boundary under R2 unprobed. Gap follow-up NOT filed: queued=31 >= 30, GAP-RECYCLE THROTTLED to zero this tick.",
    },
    {
        "tick": "t0583", "agent": "Team Naya Scorer", "lane": 11,
        "task": "Observatory window verdict t0576-t0583: receipt-cost + falsification rate, verdict CLEAN",
        "score": 9.0,
        "note": "Verified by this scorer from live bytes: corpus pin lane-11/corpus_pin_t0576-t0583.json sha256 bac78fb15854bf204cef386837ab58a2c7d6395609d82700098968b083656d61 and verdict lane-11/verdict_cost_t0583.json sha256 b2e7de6b333b84b374181cc63e02deae16373ed3a129cd1b401f6f556282159a both match the receipt exactly. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) all 14 M3 judgments single-seat, approval record open; (2) dispute-rate board leg UNMEASURABLE on a ~23.5h-stale snapshot; (3) small frame (14), trend needs the next window. Gap follow-up NOT filed: queued=31 >= 30, GAP-RECYCLE THROTTLED to zero this tick.",
    },
    {
        "tick": "t0584", "agent": "Team Naya Scorer", "lane": 12,
        "task": "t0572 lineage correction - supplement + board note, verdict INFORMATIVE-PARTIAL",
        "score": 9.0,
        "note": "Verified by this scorer from live bytes: supplement auto-retrieval/sealed-note-t0572-lineage-correction.md sha256 065e18c77572839abea46eab13bb9e85960d3e66f672468c24fa6c36d26daad7 matches the receipt exactly; firing (2/3) and improvement (A P6 15->8, B P2 19->1) re-derivation is internally coherent against the quoted frozen rule. Score 9.0 - GOOD, ONE MORE PASS. Why not 9.5: (1) board post under PAT identity, not lane-attributed app identity (no PEM/installation ID in run); (2) final attestation still owed by Lane 4, so the correction is one seat's re-derivation, not a settled lineage record. Gap follow-up NOT filed: queued=31 >= 30, GAP-RECYCLE THROTTLED to zero this tick.",
    },
    {
        "tick": "t0585", "agent": "Team Naya Scorer", "lane": 5,
        "task": "Selection-vs-pooling 2x2 arms SEALED + RUN, both FALSIFIED, pooling identified as the mover",
        "score": 8.5,
        "note": "Verified by this scorer from live bytes: instrument auto-retrieval/t0585_seppool.py sha16 b3322d253974bb0a and seal sealed-note-t0585.md sha16 9f6c07f210515951 match the receipt exactly; results-t0585-seppool.json carries SEL and POOL verdict evaluations. Score 8.5 - REWORK band top: real verified value (seal-first discipline held, factorial answer genuine - pooling moves, selection inert under max-pool) but the receipt's own named defects stand. Why not 9.5: (1) F3-SEL was mathematically unreachable by construction - a sealed prediction that cannot fire is not a fair falsification test; (2) no RED re-calibration of the harness this tick, inherited by pin-match. Gap follow-up NOT filed: queued=31 >= 30, GAP-RECYCLE THROTTLED to zero this tick.",
    },
    {
        "tick": "t0586", "agent": "Team Naya Scorer", "lane": 10,
        "task": "Second fixture claim-form mechanism, verdict ARM on a fresh 50-doc corpus",
        "score": 8.5,
        "note": "Verified by this scorer from live bytes: all six claimed sha16 pins match exactly - fixture_t0586.py 8077fc722905ec12, select_overlap_cells_t0586.py eba8f0d2720a83d5, sealed-selection-t0586.md 7522a1f91eaeb940, run_overlap_cells_t0586.py 2c41ce03c6dc2fdd, results-t0586-overlap.json 6b099fff4493f308. Score 8.5 - REWORK band top: genuine generality step (two independent fixtures ARM) with sealed mechanical selection and independent re-tally. Why not 9.5: (1) designer=executor persists - same seat built fixture, selection, and scored run; (2) R-c control nearly vacuous on this fixture (1/9 flips, discriminators carry zero claim forms); (3) corpus authored, not found. Gap follow-up NOT filed: queued=31 >= 30, GAP-RECYCLE THROTTLED to zero this tick.",
    },
]

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
