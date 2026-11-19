import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0842",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Long-text regime probe: 24 LONG docs, pre-registered falsification fired, regime FALSIFIED",
        "receipt": "t0842-lane12.md",
        "score": 8.5,
        "note": "VERIFIED this tick on live remote bytes: git ls-remote refs/heads/naya4/t0842-lane12-longtext-probe = 22564d9765c7b514a86d857043080e3ad6e16fb2, exactly the receipt pin; that commit tree contains verification/t0842-longtext-probe/PREREG.md, probe_docs.json (+sha256 sidecar) and probe_verdict.json (+sha256 sidecar). NOT PHANTOM. Score 8.5, REWORK band, agreeing with the lane's own 3-pass 8.5. Why not 9.5: (1) 4-query probe, not the 12-query battery the brief wanted; (2) single-seat - authoring plus margin computation uncorroborated, and the different-arm incoherence proof still unratified by a second seat; (3) elaboration-style lengthening only, so longer-texts-as-a-class is not exhausted, and F1-F7 on long texts unmeasured; (4) the original run-window attestation was struck by the author's 2026-10-19 correction (future-knowledge claim withdrawn; work evidence unaffected). No gap follow-up: 8.5 is below the 9.0-9.4 recycle band, and the queue throttle (31 >= 30) would block filing anyway."
    },
    {
        "tick": "t0845",
        "agent": "Team Naya Scorer",
        "lane": 12,
        "task": "Battery arm now swappable: --arm refactor, TF-IDF arm, GREEN selftest 6/6",
        "receipt": "t0845-lane12.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: hidden_files/arms/tfidf-cos-t0845/arm.py sha256 0c544e5e132a87e9bd780b4bbcabadafbd50f7a0bdae8ae8de7902ee7c0ab1a2, byte-exact to the receipt; sealed verdict hidden_files/v2-pilot-12q/pilot12_verdict.json ebeef7378b656c8f5376d8ab9250edd4c65c9a5fbc58cc9b89990d35bf655ed1, byte-exact; TF-IDF verdict 2a056a2a889d8b37ab049c51ad833327645bf6471a616c00eeb9f05370c1da7c, byte-exact. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) the refactored runner hidden_files/run_pilot12_battery.py now hashes d58357940cc7648e9e3fe4e2e245c8bc7e69d92b5268ce55fd16d59c7b9ff162, NOT the receipt's dc228b5f - the runner has been edited since, so the refactor leg rests on the receipt's record plus the still-exact arm/verdict pins; (2) full --arm semantic-t0426 was not run end-to-end post-refactor (selftest covers margins, not subprocess cold-ranks); (3) single-seat refactor, unreviewed; (4) the push done-item remains unfulfillable (untracked working tree), honestly named not faked. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0883",
        "agent": "Team Naya Scorer",
        "lane": 3,
        "task": "Exit-7 verdicts: 12 refusals classified GENUINE/FALSE-POSITIVE with stamp text",
        "receipt": "t0883-lane3.md",
        "score": 9.3,
        "note": "VERIFIED this tick on live bytes: hidden_files/exit7-verdicts-t0883.md sha256 98802e1fc3efbc20461fce9daa492ddf14399c78f4b18734ea3488dc7b252485, matching the receipt's full hash; file carries 12 '###' rows (3 GENUINE, 9 FALSE-POSITIVE per the receipt) with the four-line header naming the dispatcher as addressee. NOT PHANTOM. Score 9.3, GOOD, ONE MORE PASS (above bare 9.0 because the process deviation is owned in-file and the 1420 close call is flagged with its flip condition). Why not 9.5: (1) the 9 recommended stamps are still unapplied - verdicts are recommendatory only, queue unmoved, and stamping sits with the dispatcher; (2) the full-brief read happened pre-sign-in (class-#17 deviation, sanctioned only for the first 25 lines); (3) the 1420-lane5 FP ruling rests on unstated-bar fail-open, the receipt's own closest call. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed. No PHANTOM, no lane below 7.0 this tick."
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
