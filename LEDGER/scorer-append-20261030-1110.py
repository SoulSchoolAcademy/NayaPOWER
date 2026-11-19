import json

rows = [
    {
        "tick": "t0776",
        "agent": "Team Naya Scorer",
        "lane": 9,
        "task": "PR #2591 second-seat review: DECLINED (self-review prohibition), fact-pack delivered",
        "receipt": "t0776-lane9.md",
        "score": 9.0,
        "note": "VERIFIED this tick on surviving bytes: receipt file exists (8233 bytes); its action-time claims are independently corroborated by ~/memory/2026-10-14.md line 3659, a separately written record naming the same receipt, the same re-pinned head 98426c3b6c8ff53fce4905232a5a6618e8f3abe0, the same CI states (Receipt gate SUCCESS 16:25Z flip, Team review FAILURE by design, claim-evidence/delivery-gate pre-existing failures), and the same evidence-handle resolutions. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, above the receipt self-score 8.5 because the decline was the correct call and the fact-pack is corroborated, not merely asserted. Why not 9.5: (1) the branch head and CI states cannot be re-proven 16 days later (both cited branches no longer resolve via ls-remote, expected post-merge deletion, so the branch/SHA leg rests on action-time record + log corroboration, not a live re-pin); (2) single-seat work, no second-seat check of the fact-pack; (3) whether the next reviewer actually used the fact-pack is unverified. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    },
    {
        "tick": "t0777",
        "agent": "Team Naya Scorer",
        "lane": 7,
        "task": "Second-seat probe of level-drill key-split fix: RED/GREEN + planted-variation controls, 10/10 actions",
        "receipt": "t0777-lane7.md",
        "score": 9.0,
        "note": "VERIFIED this tick in part on surviving bytes: receipt file exists and is internally consistent (action-time re-pin a8d01f0cde69722d9eb0b2a08362bb83458ebd9f claimed exact-match to the brief pin, pre-fix blob sha256 517ece163b... RED exit 1 on data literal, fixed tools/level_drill.py sha256 6b7cc5325d... GREEN exit 0, two planted-variation controls both caught, import-refusal control, third-pass re-pin UNMOVED, 10/10 attempted actions accounted). NOT PHANTOM on the receipt's own record. Score 9.0, GOOD, ONE MORE PASS, below the receipt self-score 9.5. Why not 9.5: (1) the branch/SHA leg could NOT be re-executed this tick - the cited branch no longer resolves via ls-remote 16 days later (expected post-merge deletion) and this workspace holds no git remote, so pins rest on the action-time record, not a live re-pin; (2) single-seat probe, no second-seat rebuild of the RED/GREEN controls; (3) the four remaining 'one-shell / seal-ordering / vocabulary / cold-script' items were explicitly deferred to future ticks, so the 10-count is attempted-now, not closed. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."
    },
]

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
# validate last lines parse
lines = open(path).read().strip().split("\n")
for ln in lines[-2:]:
    json.loads(ln)
print("last 2 lines parse OK; total lines:", len(lines))
