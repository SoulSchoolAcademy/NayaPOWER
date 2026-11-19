import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0822",
        "agent": "Team Naya Scorer",
        "lane": 11,
        "task": "Human-value instrument re-run on window t1062-t0822, HV3 re-affirmed, edge rows reclassified",
        "receipt": "t0822-lane11.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt file exists; instrument hidden_files/bin/hv_measure.py exists and runs on window t1062-t0822 (current corpus differs, 968 receipts now vs 714 on 2026-10-15, so the receipt's byte-identical SHA 3eec4057... cannot be re-derived — the /tmp run JSONs are gone); snapshot hidden_files/board-thread-snapshot.json still greps 0 correction_pairs, matching the HV3 PROVEN-UNMEASURABLE re-affirmation; audit hidden_files/lane-11/metric_audit_t1162.json exists and all four underlying receipts re-read for reclassification (t1142-lane4, t1142-lane9, t1152-lane2, t1052-lane5) exist. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the window-matching judgment audit for t1062-t0822 still does not exist — M2/M3/M4 legs remain fallback-sourced from audit t1322-t1402, the receipt's own hole #1; (2) the two byte-identical run JSONs are gone from /tmp, so determinism is trusted on the receipt's SHA record, not re-derived; (3) the author's 2026-10-19 correction struck the run-window attestation (future-knowledge claim withdrawn), leaving work evidence intact but the window claim void. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."
    },
    {
        "tick": "t0823",
        "agent": "Team Naya Scorer",
        "lane": 6,
        "task": "Second blind subject for the level-drill cold run (bottleneck #7)",
        "receipt": "t0823-lane6.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: sealed answers file hidden_files/level-drill-blind-answers-t0823-lane6.json exists and hashes EXACTLY as receipted (sha256 2e2bae4ce278dc05247f0787093b976727469676b04e3ddb251efb01818f3c77), with 8 scenario answers and provenance naming the instrument branch, head a8d01f0cde69722d9eb0b2a08362bb83458ebd9f, and the blindness/RED-differential proofs. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the instrument branch naya/lane9/level-drill-keysplit-t0730 is ABSENT from the remote today (full ls-remote grep finds no level-drill branch), so the blindness proof and RED differential cannot be re-run — the branch leg is lost, whether by merge or deletion; (2) the grader verdict that closes the loop is still owed by another seat, the receipt's own hole H1; (3) the session-command list is reconstructed, not machine-transcripted, by the receipt's own admission. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."
    },
    {
        "tick": "t0824",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Breaker #10 feature.smart_bars built end-to-end",
        "receipt": "t0824-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live remote bytes: git ls-remote returns refs/heads/naya4/t0824-lane12-smartbars at eefb77cca99ae666a5b21a694919f888f6ea3f40, exactly the receipt's pin; a depth-1 clone at that exact head contains HUB/design-system/tools/smart-builder/functions/feature_smart_bars.py, functions/tests/test_feature_smart_bars.py, registry.json, and resolver.py, and the registry at that head shows feature.smart_bars status built with feature.community still specified, matching the receipt's flip exactly (receipt paths omit the HUB/design-system/tools/smart-builder/ prefix). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the 213/213 suite and resolve() smoke were NOT re-run this tick, so the green-suite leg rests on the receipt's record; (2) single-seat build plus verification, the receipt's own named gap — no independent second seat reviewed the module. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
