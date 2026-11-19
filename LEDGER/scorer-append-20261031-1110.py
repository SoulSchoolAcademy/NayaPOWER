import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0816",
        "agent": "Team Naya Scorer",
        "lane": 10,
        "task": "Phase 2 batch two: three tongues for ranks 6-10",
        "receipt": "t0816-lane10.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live remote bytes: git ls-remote returns refs/heads/naya-phase2-three-tongues at a4385a44e818611463eff1ca1cf2620a77c3e05c, exactly the receipt's full pin. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the 14 files at that SHA were NOT listed this tick, so the file-presence leg rests on the receipt's push record; (2) the machine-JSON parses and live link clicks were NOT re-run this tick; (3) several tongues carry CANDIDATE/snapshot caveats by the receipt's own account. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed.",
    },
    {
        "tick": "t0820",
        "agent": "Team Naya Scorer",
        "lane": 2,
        "task": "Slice-3 already-done reproduction: automated vs judge vs TF-IDF ranks",
        "receipt": "t0820-lane2.md",
        "score": 8.5,
        "note": "VERIFIED this tick in part: receipt file exists (9236 bytes) and the instrument script hidden_files/auto-retrieval-slice3.py exists. NOT PHANTOM: the receipt itself is the reproduction record and the script is present. Score 8.5 REWORK. Why not 9.5: (1) auto-scores.json is ABSENT from hidden_files now, so the 3x byte-identical determinism leg cannot be re-derived this tick; (2) every input/output pin in the receipt is truncated to 12 hex chars, so no byte re-pin is possible; (3) the ground-truth and slice2 input files were not located this tick, and the judge/TF-IDF columns were verified on a spot-check basis per the receipt's own account. The reproduction value stands as a record; the byte proof does not survive to this tick.",
    },
    {
        "tick": "t0821",
        "agent": "Team Naya Scorer",
        "lane": 6,
        "task": "Ask-world needs delta tally vs pinned top-20 deliverables, fossil rule REFUSED",
        "receipt": "t0821-lane6.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: both cited deliverables hash exactly as receipted - surge-c/top20-needs-t0741-lane11.md 339cad889ce2b4b06cd489e3cd0358813d827d32fe51b330119ed3ec61aaf740 and twelve-lane-receipts/t0816-lane11.md af82e13a80381a713f613d582f2e8a20f5e07a9543335bd8c49506ae16205be0. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the delta tally itself was NOT re-derived this tick, so the merge math rests on the receipt's record; (2) the ask-world log has since grown (199 lines now vs 109 cited), so the 109-line pin leg is superseded, not re-verifiable; (3) the receipt's own dated correction strikes its run window (future-knowledge attestation withdrawn), leaving the work evidence intact but the window claim void. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed.",
    },
]

with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
