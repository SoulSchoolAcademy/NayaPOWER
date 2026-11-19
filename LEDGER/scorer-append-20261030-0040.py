import json

path = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-scores.jsonl"
rows = [
    {
        "tick": "t0673",
        "agent": "Team Naya Scorer",
        "lane": 5,
        "task": "Reproduce t0671 constant-slot bias, prove weight-table fix in sandbox, measure quality cost, route dispatcher decision",
        "receipt": "t0673-lane5.md",
        "score": 9.0,
        "note": "VERIFIED on live bytes: sandbox SHAs match the receipt exactly (matcher_repro.py c17f0235e27f..., fair_test.py b6bc60bcf593..., lessons-before.jsonl ca6b1bafd84c..., lessons-after.jsonl 59f5dfdddb34c...). No git branch/SHA is cited for this work itself, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane pass-3 self-score 9.0. Why not 9.5: (1) mission tag sets are reverse-engineered, not the dispatcher's actual judgments; (2) the 9/6/3 quality estimate is a rubric projection, not a live A/B; (3) the live bias is still in the store by decision, so the loop is unclosed; (4) the preregister-conservative 8-injection tie is flagged but uninvestigated. GAP-RECYCLE: t0673-lane5 already in gap-followup-seen.json ('filed'), and queue throttle applies (rotation queued=31 >= 30): zero follow-ups filed this tick.",
    },
    {
        "tick": "t0673",
        "agent": "Team Naya Scorer",
        "lane": 8,
        "task": "Wordable packet for learning-authority 5 rows (Stage 1 item 4)",
        "receipt": "t0673-lane8.md",
        "score": 9.0,
        "note": "VERIFIED on live bytes: packet hidden_files/wordable-packet-learning-authority-5-rows-t0673.md sha256 e63a4152dc2f... matches the receipt's full pin exactly; row snapshot 5b594493eb89... and scope snapshot 4a2489af0504... match the receipt's prefixes; verifier file hidden_files/repo/supabase/functions/nayanet-learning-verify/index.ts exists and carries the learning_lock_in constant the poisoning claim rests on. No git branch/SHA is cited for this work itself, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, below lane pass-3 self-score 9.5. Why not 9.5: (1) the live DB rows are not re-derivable at this tick - only the Oct 17 snapshots survive, and the only-live grant expired 2026-10-21, so the file evidence is historical; (2) single seat, no second-seat re-derivation, which is the receipt's own named next action; (3) the production request pattern (which block IDs the runtime sends) is unverified, so the poisoning's bite frequency is unproven. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed.",
    },
]
with open(path, "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print("appended", len(rows))
