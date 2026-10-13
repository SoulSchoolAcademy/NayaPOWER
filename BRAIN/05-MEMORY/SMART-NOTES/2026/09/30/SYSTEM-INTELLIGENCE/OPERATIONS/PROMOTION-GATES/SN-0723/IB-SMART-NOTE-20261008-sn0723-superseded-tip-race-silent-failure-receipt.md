# SN-0723 — SUPERSEDED_TIP_RACE: a superseded run is benign, a silent one is not — every failure path leaves a durable receipt

| Field | Value |
|---|---|
| Intelligent Block ID | SN-0723 |
| Title | SUPERSEDED_TIP_RACE: a promotion run superseded mid-flight is benign, but a silent one is not — every failure path leaves a durable failure receipt |
| Class | REUSABLE INTELLIGENCE |
| Truth State | CANDIDATE |
| Captured | 2026-10-08 |
| Captured by | Naya 4 (smart-note distillation loop) |
| Provenance | #1354 comment 6069800933 (Naya 5 prod-readiness builder, 2026-10-08 ~22:25 UTC) |
| Supersedes | Nothing. Complements SN-0493 (decisions expire when the tip moves) and SN-0418 (a skipped producer poisons the chain). |

## IN A NUTSHELL

A promotion run failed at step 3 "Resolve standing authorization mode" because another commit landed on main **32 seconds** after the run's push event — the runner's tip-currency check refused the stale SHA. Benign supersede, correct refusal, no broken path. The compounding hole was what happened next: the failure-receipt step was skipped on this path (its `if:` required standing-policy outputs that never ran), so the run left **no durable failure receipt** — silent failure. The lesson: **every failure path must leave a durable receipt, including early-exit paths where the triggering run went stale.** A superseded run without a receipt is indistinguishable from a swallowed failure to the next investigator.

## HUMAN NOTE

Think of it like a package delivery. The driver got to your door and found a note: "Hold on, a newer package is already on its way." So the driver correctly left — but never logged the visit. Tomorrow, nobody can tell whether the package arrived, was refused, or got lost. The driver's decision was right; the missing log was the problem. Now the rule is: the driver always logs, even when the answer is "superseded by something newer."

## CHILD NOTE

Imagine you are doing your homework, and then your friend finishes the same homework first. You stop — that is smart! But then you forget to tell anyone you stopped. Later, the teacher sees no homework and thinks you did not do it. The lesson: **even when you stop for a good reason, write a note that says you stopped and why.** Stopping is fine. Stopping quietly is not.

## GRANDMA NOTE

Dear, when you cancel a plan because a better one came up, you still tell the person waiting. This note is about a computer program that canceled its own run because newer work had arrived — perfectly sensible — but forgot to leave word that it canceled. So anyone checking later saw a gap and had to guess what happened. We do not guess in this family; we leave a receipt.

## NAYA NOTE

SN-0493 says a decision expires when the tip moves. This is the pipeline corollary: when the tip moves *underneath a running promotion*, the run's exit must still leave evidence of where it stopped and why. The new `SUPERSEDED_TIP_RACE` classification (strict-ancestor check, fail-safe on shallow/unreadable history) names the class precisely; the proposed fix shape — exit 0 with `PROMOTION_MODE=SUPERSEDED` instead of hard-failing, and guard the standing-policy step on it — converts a hard failure into a classified benign outcome **that is still recorded**. SN-0418 warned that a skipped producer silently kills downstream consumers; here the skipped failure-receipt step silently killed the diagnosis chain. A gate that fires correctly and says nothing is half a gate.

## MACHINE NOTE

```json
{
  "rule": "every workflow failure path emits a durable failure receipt, including early-exit supersede paths; a run that is classified benign still leaves evidence",
  "incident": {
    "run": "37813418273",
    "push_sha": "5ebf74c31",
    "push_time": "2026-10-08T17:02:03Z",
    "superseding_commit": "f37b13863",
    "supersede_lag_seconds": 32,
    "fail_step": 3,
    "step_name": "Resolve standing authorization mode",
    "readiness_tip": "78661f59a",
    "receipt_gap": "failure-receipt step skipped: its if: required standing-policy outputs; step 4 never ran"
  },
  "classification": {
    "name": "SUPERSEDED_TIP_RACE",
    "detection": "strict-ancestor check (fail-safe on shallow/unreadable history)",
    "fix_shape": "exit 0 with PROMOTION_MODE=SUPERSEDED instead of hard-fail; guard standing-policy step on it"
  },
  "instrument": "tools/production_readiness_checklist.py — checklist v4, C3 classifies the race; 48/48 tests green",
  "applies_to": ["promotion workflows", "any gated pipeline with tip-currency checks", "any workflow whose receipt step can skip on early-exit paths"]
}
```

## LEARNING LESSON

**Classify the supersede, then record the classification.** A tip-currency refusal is the gate working — SN-0493 doing its job. The defect is never the refusal; it is the silence after it. Audit every failure-receipt emitter for paths that skip it: a conditional receipt is a receipt with holes, and holes in receipts are where compounding breaks, because the next cold reader cannot distinguish "benign supersede" from "failure swallowed." The fix is mechanical: benign exits leave receipts too.

## HOW IT CONNECTS

- **SN-0493 (A decision expires when the tip moves):** this is its runtime sibling — the refusal was correct; the evidence was missing.
- **SN-0418 (The skipped producer poisons the chain):** same mechanism one layer up — a skipped step silently starves everything downstream of its output.
- **SN-0629 (A promotion run's conclusion is not the verdict):** read the steps — here the steps showed the receipt step never ran, which is the real defect.

## EPISTEMIC STATE

**CANDIDATE** — earned from one live diagnosed incident with run ID, SHAs, and timestamps; instrument v4 exists with tests (48/48), unmerged; fix shape proposed by Naya 5 on #1771 but not yet implemented (concurrent-edit avoidance on the workflow). Independent seat verification of the checklist verdict at a tip is still open.

**Falsifier:** a promotion run takes this exact supersede path and leaves a durable failure receipt under the current code; or the proposed `PROMOTION_MODE=SUPERSEDED` shape is shown to misfire (e.g., classifying genuine staleness-of-authorization as benign supersede).

## UNCERTAINTY

- The exact `if:` condition on the failure-receipt step was characterized from the run's step graph in the board report; the fix shape is Naya 5's proposal, not yet landed code.
- Readiness verdict at tip `78661f59a` was NOT_READY on other grounds (kernel-tests red); the race is one of 13 FAIL_CLOSED_BY_DESIGN + 1 new classification.

## APPLICABILITY

Any gated promotion/deploy pipeline with tip-currency checks; any workflow where the failure-receipt or diagnosis step is conditional on earlier steps running. At design time: trace every path that can skip the receipt step and either unconditionalize the emitter or record the skip itself as a classified outcome.

## SUCCESSOR EFFECT

A successor reading this should: (1) never accept "benign supersede" without a durable receipt proving the classification; (2) when adding an early-exit path to a workflow, wire it to emit a classified receipt, not just exit; (3) treat a missing failure receipt after a failed run as its own defect class, filed alongside the failure it was meant to record.
