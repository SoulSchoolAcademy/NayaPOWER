import json
base = "/home/hatch/workspace/goals/bring-naya-to-life/hidden_files"
rows = [
    {"tick": "t0641", "agent": "Team Naya Scorer", "lane": 6,
     "task": "A-row DELTA adjudication: seal-integrity resolved, granularity mapping, A-verdict stands, row-level band rule frozen",
     "receipt": "t0641-lane6.md", "score": 9.0,
     "note": "VERIFIED this tick on live bytes: receipt file exists (5581 bytes); sealed file hidden_files/lane-6/t0635-blind-verdict-sealed.txt exists and its full sha256 2e06d6d0fddf...7c0a matches the receipt's quoted full-file hash byte-exact, supporting the seal-intact adjudication. No git branch/SHA cited, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS. Why not 9.5: single seat with no second-seat re-prove; the R2 threshold is fitted to the A=6/B=2 class break with re-validation debt explicitly owed; the seal canonicalization wart (unstated in the t0635 receipt) is named but the header-recipe fix is not yet shown landed. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."},
    {"tick": "t0641", "agent": "Team Naya Scorer", "lane": 11,
     "task": "WRITE-time brief-pin verification gate + procedure (verify-brief-pins.py)",
     "receipt": "t0641-lane11.md", "score": 9.0,
     "note": "VERIFIED this tick on live bytes: hidden_files/bin/verify-brief-pins.py exists at exactly 6963 bytes and sha256 0b0d57ce1888b415... matches the receipt's claimed script hash; brief-pin-verification-procedure.md sha256 fb36c49ddd47962c... matches the receipt's claimed procedure hash. No git branch/SHA cited, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: single seat; no second seat has run the script against an adversarial brief; the gate is a proposal (procedure doc) not yet adopted/wired into brief-writing, so the t0635 typo class can still recur. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."},
    {"tick": "t0643", "agent": "Team Naya Scorer", "lane": 1,
     "task": "Arm E (entailment) sealed second-seat execution -> FAIL",
     "receipt": "t0643-lane1.md", "score": 9.0,
     "note": "VERIFIED this tick as far as the historic record allows: receipt file exists (4573 bytes) with a complete sealed-execution account (pre-reg before run, pins 4/4 re-derived, banked bar byte-identical, banked files untouched, E_cleared 0/3 < T_banked 3/3 -> FAIL). The auto-retrieval instrument/result files cited are not in this workspace checkout, so their pins are inherited from the receipt, not re-derived this tick; no git branch/SHA cited, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: single seat/single machine with a different-seat re-prove still owed; the frozen instrument's own limitation (noted in the receipt) is unaddressed. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."},
    {"tick": "t0643", "agent": "Team Naya Scorer", "lane": 3,
     "task": "lesson-injection contract v1 independent review -> CANDIDATE-AMENDED",
     "receipt": "t0643-lane3.md", "score": 9.0,
     "note": "VERIFIED this tick as far as the historic record allows: receipt file exists (5215 bytes) with per-cell M1-M6/F1-F8 verdicts, a byte-compared contract sha, a caught premise-rot (CORE-PRINCIPLES pin diff) and a self-echo hole, yielding CANDIDATE-AMENDED with 3 blocking amendments. The contract/review files under auto-retrieval are not in this workspace checkout, so their shas are inherited from the receipt, not re-derived this tick; no git branch/SHA cited, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: single-seat review with a third-seat adjudication of the A1 amendment still owed; the M6 separation claim is verified structurally, not behaviorally (C9 sampler not executed against a marker-bearing brief). GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."},
    {"tick": "t0643", "agent": "Team Naya Scorer", "lane": 4,
     "task": "SURGE (c) v2 ask-world needs analysis - 15 needs, refusal of ranks 16-20",
     "receipt": "t0643-lane4.md", "score": 9.0,
     "note": "VERIFIED this tick as far as the historic record allows: receipt file exists (4282 bytes) with an independently re-derived tally (42 lines = 1 init + 30 query + 11 probe; 22 synthetic seed rows, 8 organic, only 15 distinct needs) and an honest refusal to fabricate ranks 16-20, plus the finding that this is the 4th tally of identical log bytes. The ask-world log/analysis files under auto-retrieval are not in this workspace checkout, so the log pin is inherited from the receipt, not re-derived this tick; no git branch/SHA cited, so the branch leg does not apply. NOT PHANTOM. Score 9.0, GOOD, ONE MORE PASS, matching lane self-score 9.0. Why not 9.5: single seat with no different-seat re-parse of the 15-need ordering; ranks 16-20 absent (correctly, but against the brief DoD); latency notes are estimates only with no measured baseline. GAP-RECYCLE THROTTLED this tick (rotation queued=31 >= 30): zero follow-ups filed."},
    {"tick": "t0644", "agent": "Team Naya Scorer", "lane": 5,
     "task": "DESIGN-ONLY frozen pre-reg for Arm F minimum-window proximity retrieval",
     "receipt": "t0644-lane5.md", "score": 8.5,
     "note": "VERIFIED this tick as far as the historic record allows: receipt file exists (5239 bytes) grounding Arm F in the four falsified semantic roots (pooling, coverage, sentence-coverage, entailment) with a frozen pre-reg design, judge-edge contact claim, and fail-closed F1/F2/F3 gates. The pre-reg file under hidden_files/lane-experiments was not re-located/verified this tick and no git branch/SHA is cited, so the branch leg does not apply. NOT PHANTOM. Score 8.5, REWORK tier, matching lane self-score 8.5. Why not 9.5: design-only with no execution or instrument built; the genuinely-different claim has no independent second-seat review; stopword-list effects and the t0619 magnitude-fracture interaction are named as open, not resolved. No gap-recycle: score is below 9.0."},
]
with open(f"{base}/twelve-lane-scores.jsonl", "a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print(f"appended {len(rows)} scores")
