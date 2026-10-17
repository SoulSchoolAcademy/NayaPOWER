# Scorecard Calculator — Wiring Proposal (PROPOSAL ONLY)

**Status:** proposal. No gate, workflow, or merge-law change is included in
this branch. Gate changes are not wave-authorized; this document proposes the
wiring for a different seat to review and for Shawn's lane to ratify.

**What this plugs into:** the scorecard receipt flow the team already runs —
builder writes a claim set (the packet), a judge scores it honestly, the
receipt pins the merge head SHA, and the merge gate consumes it. Today the
judge is always a human seat. The calculator is a *mechanical first pass*:
it verifies every citation against git at the ref, applies the rubric's
evidence-rule caps with no exceptions, and emits a receipt-law-conformant
scorecard. It does not replace the human judge — it makes the human judge's
job checkable.

## 1. Who runs it

- **The VERIFY seat (or a lane-9 gate worker)** runs the calculator against a
  builder's claim set. The builder's seat (BUILD, or whoever shipped) supplies
  the packet; the verifying seat runs the judge. A seat never verifies its
  own work — the calculator is a tool of the *verifying* seat, never the
  builder's.
- **The agreement harness** (`test_calc.py`) is re-run by the second seat
  doing different-seat validation, and again by any seat before touching the
  calculator's code.

## 2. On what trigger

Three triggers, in priority order:

1. **Scorecard receipt submitted for a PR.** The builder posts their claim
   set; the verifying seat runs the calculator against the PR's head SHA.
   Calculator output and the human judge's scorecard both land in the wave
   log; any per-dimension divergence ≥ 0.5 blocks the receipt (the
   instrument's own agree/review band).
2. **Post-merge verification.** After merge, the calculator re-runs against
   the merge SHA (the `recheck`-style durability loop can call it at
   `durable_check_due_utc` + 7 days to catch rotted evidence).
3. **Calculator code changed.** `test_calc.py` re-runs the three HV subjects;
   the calculator's own receipts must still reproduce all three within 0.5.

## 3. What consumes its JSON output

- **The merge receipt gate** (a future rung alongside `check_scorecard_receipt_pin.py`):
  the gate reads the calculator's scorecard and requires
  `verdict != DISQUALIFIED`, `score >= <merge bar>`, and every deduction's
  evidence to be named. The calculator's JSON is the *machine-readable*
  companion to the human-readable board comment — same relationship the
  receipt-pin checker has to the PR body.
- **The evidence ledger** (`evidence_ledger[]`): consumed by the durability
  loop to re-verify citations at a later ref (HELD / ROTTED / drift).
- **The agreement table** (test output): consumed by the director's fold to
  measure whether the machine's judgment tracks the human seats'.
- **The `unmeasurable` list**: consumed by the verifying seat as their
  to-check list — exactly the claims the machine could not attest to, named
  so the human knows where their judgment still carries the weight.

## 4. Inputs and outputs, exactly

```
IN:  --repo REPO --sha SHA (or --branch BR) --packet PACKET.json
     --receipt-posted-comment-id N --judge <seat>
OUT: scorecard JSON (stdout or --out) — receipt-law frame + honest-score sidecar
EXIT: 0 = scorecard emitted (incl. DISQUALIFIED — a verdict was reached)
      2 = fail-safe: malformed input, unresolvable ref, missing receipt post,
          or output that fails receipt-schema validation — nothing emitted
```

- The packet is the builder's claim set in packet-v1 shape
  (`change_id, title, merge_sha, grader, harm_check, judgments[]` with
  `dimension/score/evidence/rationale`). The observatory scorecards'
  `evidence_ledger` regroups into this shape (see `test_calc.py`).
- `--receipt-posted-comment-id` is required and must be the real board
  comment where the receipt was posted. No id → no output (fail-closed):
  a private scorecard is not a gate.
- No network, no GitHub API: everything is verified against local git
  objects. The calculator never spends quota.

## 5. What the calculator does NOT do (by design)

- It never upgrades a score beyond what verified evidence supports; caps are
  one-directional (downward).
- It never runs tests or queries CI. Test *presence* is verified; test
  *passing* is UNMEASURED and listed. A future wiring step (API-budgeted,
  with Shawn's lane's sign-off) could feed CI results in as `receipt`
  evidence — that is a separate proposal.
- It never invents evidence, citations, line ranges, or counterfactual
  scores. The do-not-ship null option uses a stated NULL_BASELINE convention,
  flagged in the output.
- It never changes a gate. All wiring here is prose; the mechanical rung and
  any required-check click are ratification-gated decisions.

## 6. Open questions for the wiring decision (not answered here)

1. **Merge bar for the calculator's score:** the receipt law's learning-
   promotion bar is winner-mean ≥ 9.0; the general merge bar is honest score
   ≥ 9.5 with different-seat validation. Does the calculator's score feed the
   merge bar directly, or only advise the human judge? (Recommendation: advise
   first, measure agreement for a month, then decide.)
2. **Divergence handling:** calculator-vs-human divergence ≥ 0.5 blocks the
   receipt — does it also trigger a re-grade by a third seat?
3. **CI signal intake:** worth an API budget, or does attested CI evidence
   (the current practice) stay the human judge's call?
4. **Null-option scoring:** the NULL_BASELINE convention is honest but
   coarse — cost of inaction deserves a mechanical source before any
   promotion-authority use.
5. **Receipt-posted id plumbing:** the calculator needs the real board
   comment id at run time; the wave log / dispatcher should pass it in.
