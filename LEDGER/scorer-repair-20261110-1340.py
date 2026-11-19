#!/usr/bin/env python3
"""Repair malformed line 8329 of twelve-lane-scores.jsonl (2026-11-10 ~13:40 PST).

Line 8329 held TWO JSON objects concatenated with no newline, so neither
parsed for any line-based reader (find-unscored.py, ledger_writer.py):
  A: {"tick":"gate-stall-20261110-1301", ... "score":8.5} -- the ONLY score
     for receipt gate-stall-20261110-1301.md (fresh, filed 13:01 PST today).
  B: {"tick":"t0539-lane5", ... "score":9.0} -- a DUPLICATE. Receipt
     t0539-lane5.md already has a valid, fuller score row
     (tick "t0539", lane 5, score 9.0) elsewhere in the file.
     B never parsed, never entered any ledger/stat.

Repair: replace line 8329 with ONE row for the 1301 receipt.
Score amended 8.5 -> 9.0: the original 8.5 (REWORK) named exactly one gap --
no claim-sweep log, exit codes unverifiable. That gap is CLOSED this tick:
claim-sweep-20261110-1303.log arrived after scoring (mtime 21:06:44Z) and
verifies 30 attempt lines, 28x exit 7 + 2x exit 2, same two exit-2 briefs,
named set == receipt list 30/30, with an explicit totals line. The original
scorer's own rule was "then it clears 9.0" -- the amendment follows it.
Object B is set aside (its full text is preserved in the repair note);
restoring it would double-count t0539-lane5.md in the ledger.
The original 8.5 row text is also preserved in the repair note for audit.
"""
import json
from pathlib import Path

HIDDEN = Path("/home/hatch/workspace/goals/bring-naya-to-life/hidden_files")
SCORES = HIDDEN / "twelve-lane-scores.jsonl"
NOTE = HIDDEN / "ledger" / "scorer-repair-20261110-1340.md"

lines = SCORES.read_text().splitlines(keepends=True)
assert len(lines) == 8334, f"expected 8334 lines, got {len(lines)}"
bad = lines[8328]  # 0-based index for line 8329
idx = bad.find('}{"tick"')
assert idx > 0, "concatenation boundary not found"
obj_a = bad[: idx + 1]
obj_b = bad[idx + 1 :]
a = json.loads(obj_a)
b = json.loads(obj_b)
assert a["tick"] == "gate-stall-20261110-1301" and a["score"] == 8.5, a
assert b["tick"] == "t0539-lane5" and b["score"] == 9.0, b
# Confirm B is a true duplicate: a valid row for the same receipt exists.
valid_dup = False
for ln in lines:
    try:
        j = json.loads(ln)
    except Exception:
        continue
    if (j.get("agent") == "Team Naya Scorer" and j.get("receipt") == "t0539-lane5.md"
            and j.get("lane") == 5 and j.get("score") == 9.0):
        valid_dup = True
assert valid_dup, "no valid duplicate row for t0539-lane5.md; refusing to drop B"

amended_note = (
    "VERIFIED this tick on workspace bytes: (1) queue holds exactly the receipt's "
    "30 briefs (31 .md files = 30 briefs + lane-feed.md, which is not a brief); "
    "blocked-brief list (name + exit code) is IDENTICAL to the 11:57 receipt's list, "
    "28x exit 7 + 2x exit 2, same two exit-2 bars; (2) cap compliance TRUE - prior "
    "stall receipt mtime 19:57:42Z vs this one 21:01:24Z = 63m42s, outside the 60-min "
    "window, and the '64 minutes old' recency claim is accurate; (3) the 'four briefs "
    "carry explicit seat bars' count is now consistent (was the self-contradicting "
    "'five... six in total'), and both exit-2 bar texts verified in the brief files; "
    "(4) delta vs the immediate prior receipt is correctly stated as zero change. "
    "AMENDED 2026-11-10 ~13:40 PST: the original 8.5 (REWORK) named one gap - no "
    "claim-sweep log, exit codes unverifiable. That gap is now CLOSED: "
    "claim-sweep-20261110-1303.log arrived after scoring (mtime 21:06:44Z) and verifies "
    "30 attempt lines, 28x exit 7 + 2x exit 2, same two exit-2 briefs, named set == "
    "receipt list 30/30, with an explicit totals line. Per the original scorer's own "
    "rule ('then it clears 9.0'), score is 9.0, GOOD ONE MORE PASS. Why not 9.5: (1) no "
    "cleared work shipped - the queue's blockage is structural (every brief needs a "
    "second seat or a dispatcher stamp) and this seat cannot clear it alone; (2) a repeat "
    "identical stall with no new blockage, in a run stretching back to 2026-11-08; "
    "(3) the evidence log arrived after the receipt was filed, so the receipt as filed "
    "was unverifiable at filing time. No gap-recycle: queued=30 >= 30 throttles "
    "gap-recycling to zero this tick. This row was restored from malformed line 8329 "
    "(two JSON objects concatenated, no newline) - see ledger/scorer-repair-20261110-1340.md."
)
amended = {
    "tick": "gate-stall-20261110-1301",
    "agent": "Team Naya Scorer",
    "lane": 0,
    "task": "Lane-executor stall run 2026-11-10 13:01 PST: evaluate all 30 unclaimed briefs, claim none (28 exit 7 + 2 exit 2)",
    "receipt": "gate-stall-20261110-1301.md",
    "score": 9.0,
    "note": amended_note,
}
lines[8328] = json.dumps(amended) + "\n"
SCORES.write_text("".join(lines))

# Verify: whole file parses now, and the 1301 row is visible at 9.0.
n_ok = 0
seen = None
for ln in SCORES.read_text().splitlines():
    if not ln.strip():
        continue
    j = json.loads(ln)
    n_ok += 1
    if j.get("tick") == "gate-stall-20261110-1301":
        seen = j
assert seen is not None and seen["score"] == 9.0 and seen["agent"] == "Team Naya Scorer"

NOTE.write_text(
    "# Scorer repair 2026-11-10 ~13:40 PST (lane-scorer tick)\n\n"
    "Line 8329 of twelve-lane-scores.jsonl held two JSON objects concatenated "
    "with no newline, so neither parsed for any line-based reader "
    "(find-unscored.py, ledger_writer.py).\n\n"
    "## Restored (amended 8.5 -> 9.0)\n\n"
    "The gate-stall-20261110-1301 score, the only score for that receipt. The "
    "original 8.5 (REWORK) named one gap: no claim-sweep log, exit codes "
    "unverifiable. claim-sweep-20261110-1303.log arrived after scoring "
    "(mtime 21:06:44Z) and verifies 30 attempt lines, 28x exit 7 + 2x exit 2, "
    "same two exit-2 briefs, named set == receipt list 30/30, totals line present. "
    "Per the original scorer's own rule ('then it clears 9.0'), the restored row "
    "scores 9.0. Original 8.5 row text, preserved for audit:\n\n```json\n"
    + obj_a.strip() + "\n```\n\n"
    "## Set aside (duplicate, not restored)\n\n"
    "The second object on that line, a duplicate t0539-lane5 score (9.0). The "
    "receipt already carries a valid, fuller score row (tick \"t0539\", lane 5, "
    "9.0); restoring the duplicate would double-count it in the ledger. "
    "Full text:\n\n```json\n" + obj_b.strip() + "\n```\n\n"
    f"Post-repair: {n_ok} parseable rows; 1301 row visible at 9.0.\n"
)
print(f"REPAIRED: parseable rows={n_ok} seen_1301_score={seen['score']}")
