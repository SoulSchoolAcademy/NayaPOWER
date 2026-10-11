# UD-19 Overlap Arbiter — when work overlaps, the math decides

**Plain words:** when two lanes' work overlaps or conflicts, nobody pulls rank.
Each product gets independently scorecarded (each seat scores the other's,
never its own), the numbers pick the winner, and the decision lands in a
receipt that cites evidence — never authority. The receipt is the only thing
that authorizes the merge or action.

## The protocol

1. **Claims.** Each lane registers its work product: claimant, artifact id,
   work key (what work this is), content hash, location (branch/PR/path).
2. **Overlap trigger.** `find_overlaps()` groups claims by work key; groups
   with 2+ distinct claimants need arbitration. (The advisory PR-file watch
   in `enforcement/warn_overlapping_prs.py` is separate and unchanged.)
3. **Cross-scorecard.** Independent scorers score each artifact with
   evidenced dimension scores via `cross_score()`. The claimant may never
   score their own artifact — refused with `SELF_JUDGE`. Scores without
   cited evidence are refused as inflation.
4. **Arbitration.** `arbitrate()` with an independent verifier (never a
   claimant — `SELF_VERIFY` refused):
   - highest verified cross-score total wins;
   - a tie (gap < 0.5) goes to better evidence quality;
   - a remaining tie requires a recorded Intelligence-Question answer,
     else `TIEBREAK_MISSING`;
   - reasoning must explain in words and may never cite rank
     (`RANK_NOT_EVIDENCE`);
   - evidence cited for two different artifacts by one scorer is flagged
     `DUPLICATE_EVIDENCE` in the receipt.
5. **Receipt.** Winner, margin, cross-scores, reasoning, evidence refs,
   resolution (`ADVANCE_WINNER` / `MERGE_BOTH` / `COMPOSE_PARTS`), and the
   preserved losers (id, hash, location — history is kept, never erased).
   Every receipt carries a does-not-claim boundary.

## Decision rule

```
a* = argmax over artifacts of (mean independent cross-score total)
tie  -> max evidence quality
tie  -> recorded Intelligence-Question answer (verifier's judgment, in words)
```

## Ego guards (all refused, machine-readable codes)

| code | meaning |
|---|---|
| `SELF_JUDGE` | claimant scored their own artifact |
| `SELF_VERIFY` | verifier is a claimant in the overlap |
| `SCORE_WITHOUT_EVIDENCE` | score with no/thin/empty evidence, or artifact with no cross-score |
| `RANK_NOT_EVIDENCE` | reasoning cites rank, or is too thin to explain |
| `DUPLICATE_EVIDENCE` | same evidence string cited twice (within a claim: refused; across artifacts: flagged) |
| `TIEBREAK_MISSING` | full tie with no recorded IQ answer |

## Run the proof

```
python3 tools/test_overlap_arbiter.py   # 9 adversarial cases, all green
```

## What this does NOT claim

The arbiter judges the decision procedure, not the truth of the evidence —
fabricated-but-plausible evidence cites pass the format checks; that is why
scorers must be genuinely independent seats and receipts stay auditable.
Rank-pattern detection in reasoning is heuristic, not semantic proof.
