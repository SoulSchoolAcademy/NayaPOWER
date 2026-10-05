# VERIFY Node Contract V1

**ID:** NAYA-KERNEL-VERIFY

## Purpose

VERIFY determines what actually happened relative to what was intended. It compares expected outcomes with observed reality and makes acceptance decisions based on evidence.

## Inputs

- Expected outcome definition (from ACT)
- Observed outcome data
- Evidence artifacts
- Causality claims (if any)
- Acceptance criteria

## Outputs

- Outcome status (SUCCESS, FAILURE, INCONCLUSIVE, NOT_PROVEN)
- Acceptance decision (ACCEPTED, REJECTED, PENDING)
- Causal evidence status
- Unresolved gaps
- Verification receipt

## MUST Rules

- Compare expected and observed outcome systematically.
- Use evidence appropriate to the claim.
- Distinguish failure, inconclusive evidence and not-proven states.
- Address causality when causality is claimed.
- Produce verification receipts for all decisions.
- Preserve unresolved gaps explicitly.

## MUST NOT Rules

- Infer success from execution alone.
- Promote correlation to causation without adequate evidence.
- Mark inconclusive as failure or success.
- Ignore unresolved gaps.
- Accept outcomes without evidence.
- Collapse verification into execution.

## Acceptance Criteria

- Every outcome has an explicit status.
- Acceptance decisions trace to evidence.
- Causal claims have causal evidence.
- Unresolved gaps are explicitly recorded.
- Verification receipts are produced.
- Distinction between failure and not-proven is maintained.

## Failure States

| Failure | Behavior |
|---|---|
| Expected outcome undefined | Mark as NOT_PROVEN; request definition |
| Evidence insufficient | Mark as INCONCLUSIVE; do not accept or reject |
| Causality claimed without evidence | Mark causal claim as UNVERIFIED |
| Observation data missing | Mark as NOT_PROVEN; request data |
| Acceptance criteria ambiguous | Escalate; do not guess |

## Universal Verifier Method

Every agent, Naya, Coda, specialist, CI lane, or runtime acting as a verifier follows this method for consequential claims.

### 1. Measure before designing or repairing

Do not begin by proposing a fix, architecture, score, or explanation.

First establish whether the claim is true on the exact current evidence.

Prefer direct observation:
- exact revision / deployment / runtime identity;
- command actually executed;
- exit status;
- complete search/test scope;
- observed output;
- untouched comparison baseline where relevant.

A plausible inference is not a measurement.

### 2. Resolve evidence in source-precedence order

For repository claims, use this search order unless a stronger claim-specific source exists:

**CURRENT MAIN → RELEVANT OPEN/CLOSED PRS → RELEVANT BRANCHES → WORKFLOW/RUNTIME/PROOF EVIDENCE → HISTORICAL RECORD**

Rules:
- current `main` determines canonical source state;
- an open PR or branch may establish that substance exists, but does not make it canonical;
- a historical artifact may explain lineage but cannot prove current state;
- if `main` moves during verification, re-pin consequential conclusions before certification.

Never silently collapse **exists somewhere** into **exists on main**, or **implemented on a branch** into **canonical/verified**.

### 3. Separate the claim into independently testable parts

A verifier must distinguish at least:
- **substance** — is the underlying behavior/content real?
- **citation/provenance** — does the referenced artifact/revision actually resolve?
- **state** — CANDIDATE / IMPLEMENTED / VERIFIED / PRODUCTION-PROVEN / etc.;
- **scope/applicability** — does the proof cover the claim being made?
- **authority** — does the evidence grant or imply permission? Usually it does not.

One failed citation does not erase valid substance. Valid substance does not rescue a false citation or inflated state.

### 4. Give credit where evidence supports it

Verification is not adversarial theater.

When a compound claim is partly right:
- explicitly preserve the valid part;
- name the exact failing part;
- narrow rather than discard the claim;
- distinguish correction from condemnation.

The objective is the most accurate state map, not the largest defect count.

### 5. Falsify proportionally to consequence

Try to disprove the claim with the strongest practical counter-test.

For security, safety, authority, learning, rollback, poisoning, recovery, causality, or production claims, positive happy-path evidence is insufficient by itself.

A claimed defense that has never been attacked is **UNKNOWN / NOT_PROVEN**, not high-scoring security.

Where appropriate include:
- malformed input;
- stale/replayed state;
- wrong owner/scope/authority;
- forged or correlated evidence;
- poisoned intelligence;
- rollback/recovery;
- negative transfer;
- absent/deleted source;
- duplicate/reordered execution;
- cold-successor reread.

### 6. Refuse certification beyond evidence

If a required proof does not exist, say so directly.

Allowed verifier outcomes include:
- ACCEPTED / VERIFIED;
- REJECTED / CONTRADICTED;
- INCONCLUSIVE;
- NOT_PROVEN;
- UNKNOWN;
- BLOCKED;
- STALE.

Do not turn missing tests into a score.
Do not turn architecture into security proof.
Do not turn a builder report into independent verification.
Do not turn confidence into evidence.

**Refusal to certify an untested claim is correct verifier behavior.**

### 7. Negative claims require stronger discipline

Before publishing `NOT FOUND`, `ABSENT`, `NO TESTS`, `PRE-EXISTING`, or equivalent:

- record the exact revision;
- record the command/query;
- record the exit status or tool result;
- confirm the scope was complete enough to establish absence;
- compare an untouched baseline before calling a failure pre-existing.

Truncated, filtered, stale, or mis-scoped output cannot establish absence.

### 8. Correction is part of verification

If stronger evidence falsifies the verifier:
- retract or narrow the claim promptly;
- preserve the original provenance;
- state what changed and why;
- update the durable lesson when reusable.

A public correction increases system trust. Hiding or defending a disproven claim decreases it.

### 9. Certification output

Every consequential verification report should leave:

```
CLAIM
EXACT SOURCE / REVISION
MEASUREMENT METHOD
OBSERVED EVIDENCE
BASELINE / CONTROL (if applicable)
FALSIFICATION ATTEMPT
WHAT IS VALID
WHAT IS NOT VALID
TRUTH / PROOF STATE
SCOPE + LIMITATIONS
UNKNOWNS / BLOCKERS
ACCEPT / REJECT / INCONCLUSIVE / NOT_PROVEN
ONE NEXT PROOF ACTION
```

The verifier should make it possible for another cold verifier to reproduce the conclusion without trusting the report author.

### 10. Core verifier maxim

> **Measure first. Resolve the strongest current evidence. Credit what is true. Correct what is not. Attack claims proportional to consequence. Certify only what survives.**
