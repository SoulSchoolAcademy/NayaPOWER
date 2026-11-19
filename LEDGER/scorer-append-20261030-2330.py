import json

HF = '/home/hatch/workspace/goals/bring-naya-to-life/hidden_files'
OUT = HF + '/twelve-lane-scores.jsonl'

rows = [
    {
        "tick": "20261030-2330",
        "agent": "Team Naya Scorer",
        "lane": 9,
        "task": "Gap follow-up scorer-20261014-1905: pre-claim claimability gate mechanized (claim-brief.py, --self-test 4/4)",
        "receipt": "gap-scorer-20261014-1905-lane9.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: receipt file exists; gap-followup-seen.json entry scorer-20261014-1905-lane9 -> CLOSED with matching receipt path; brief-gap-scorer-20261014-1905-lane9.md present in brief-queue/done/; bin/claim-brief.py present and --self-test GREEN today (expanded suite incl. F1-F6 lift-stamp). NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: (1) original script pin drifted - receipt SHA cd46c7bb82b5ca0162b824714ecb8b9958392766d75c436e4f4b550384474fea vs live c4efc2229c72e595eeffb610af9d0b59978ed820b7817e09390b62fc7e34f4ba (later extensions), so action-time bytes not re-pinnable; (2) adoption gap still dispatcher-owned - script available, not mandatory in the claim block; (3) gate-dialect canonicalization still owed; (4) single seat, and the run itself used the old raw-mv order it was curing. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "20261030-2330",
        "agent": "Team Naya Scorer",
        "lane": 1,
        "task": "t0796 forensics root fix: parameterized all 8 live push-script copies via fail-closed seat_identity helper, proof on live commit objects",
        "receipt": "t0796-lane1.md",
        "score": 9.0,
        "note": "VERIFIED in part on live bytes: receipt file exists; bin/seat_identity.py present (era-consistent 2026-10-15) and --self-test PASS fail-closed + round-trip today. NOT PHANTOM on the action-time record. Git legs could NOT be re-executed this tick: proof branch d3813117bce4a8126b6465e31e8a277575fc2bc7, dangling probe commit 3576161f8a177d99f60d29a8a7c0eef60529f1ae, and the 8-file parameterization/grep sweep rest on the action-time record (no git remote in this workspace, REST avoided per budget law). Score 9.0, GOOD, ONE MORE PASS, below receipt self-score 9.5. Why not 9.5: (1) repo proof legs not re-pinnable today; (2) cross-seat proof synthetic, not a second real seat; (3) stale-copy consolidation still dispatcher-owned; (4) class-#17 sign-in-after-read recurred in the run itself. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "20261030-2330",
        "agent": "Team Naya Scorer",
        "lane": 2,
        "task": "t0802 STALE BRIEF VERIFIED-DONE: retrieval-auth EQ1-EQ4 gap already closed, independent re-run reproduces byte-identical results",
        "receipt": "t0802-lane2.md",
        "score": 9.0,
        "note": "VERIFIED this tick on live bytes: probe SHA 0ddabc02afce3e79c355bd111c531482364831f1952e28dc38b593db316c4702 and results SHA c9126f21a37d2cf89829019e31f5bb9d0a13ddf3d294cdd9306a03f910df8ac8 both match the receipt exactly (same pins re-verified at the 2300 tick for the parent receipt); gap-followup-seen.json entry scorer-20261014-1910-lane4 -> CLOSED; brief-t0802-lane2.md present in brief-queue/done/. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching receipt self-score 9.0. Why not 9.5: (1) verification-only work - no new probe construction; (2) staleness discovered post-claim, not pre-claim; (3) dispatcher supersede-watch (auto-retire closed-gap briefs) still open; (4) single seat. GAP-RECYCLE THROTTLED (rotation queued=31 >= 30): zero follow-ups filed."
    },
]

with open(OUT, 'a') as f:
    for r in rows:
        f.write(json.dumps(r) + '\n')

# validate: whole file still parses
n = 0
for line in open(OUT):
    if line.strip():
        json.loads(line)
        n += 1
print('appended 3 rows; total score rows now', n)
