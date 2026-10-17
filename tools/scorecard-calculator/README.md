# Scorecard Calculator v1 — the mechanical judge

`scorecard_calc.py` takes a work artifact (commit SHA and/or branch) plus the
builder's claim set (packet v1) and emits an honest scorecard JSON conforming
to `.naya/specifications/NAYA-SCORECARD-RECEIPT-AUTHORITY-V1.schema.json`.

**The judge's contract:** verify every citation against git at the ref,
apply the Human-Value evidence-rule caps downward only, never fabricate
attestation — unmeasurable is stated in `unmeasurable[]`, never scored.

## Quick start

```bash
# build a claim-set packet (packet v1: change_id, title, merge_sha, grader,
# harm_check, judgments[{dimension,score,evidence[],rationale}])
python3 tools/scorecard-calculator/scorecard_calc.py \
  --repo . --sha <merge-sha> --packet packet.json \
  --receipt-posted-comment-id <board-comment-id> \
  --judge "<your seat>" --out scorecard.json
echo $?   # 0 = scorecard emitted (incl. DISQUALIFIED); 2 = fail-safe, nothing emitted
```

## Agreement test (different-seat validation)

```bash
python3 tools/scorecard-calculator/test_calc.py [--repo REPO]
```

Re-runs the calculator against the three hand-written HV scorecards
(`tools/human_value/observatory/scorecards/HV-20261011-PR-{2188,2375,2383}.scorecard.json`)
and prints the agreement/divergence table. Pass = every per-dimension
divergence < 0.5 and all outputs receipt-schema-valid.

## Wiring

See `WIRING-PROPOSAL.md` — proposal only; no gate changes in this branch.
