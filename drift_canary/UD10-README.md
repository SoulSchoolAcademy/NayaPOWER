# UD-10 — Say "we don't know" instead of inventing answers

An incident is a set of possibilities, not one confident story.

## What this builds

**D31 — incident verdict with four independent dimensions** (`d31_incident.py`,
vendored byte-identical from draft PR #2211, which itself stacks the D29/D30
machinery also vendored here):
- `IncidentVerdict` has **NO `failure_reason` field** (test-asserted). Anyone
  wanting one confident story must compute it from evidence — the module
  refuses to do it for them.
- Four dimensions never collapsed: observability (per source/event/interval;
  absence is evidence only inside covered scope), evidence state
  (claim-level verdicts, false-corroboration detection), blocker state
  (AND/OR minimal blocking sets; repairs recognized only with authenticating
  witness), causal state (competing revisable hypotheses).
- `Hypothesis.promote_to_verified_lesson()` raises `PermissionError` while
  unresolved — mechanically, not by convention.

**D42 — possible-histories engine** (`d42_possible_histories.py`, new):
- `H(O)` = concrete histories consistent with admissible observations.
- Verdicts: `SAFETY_ESTABLISHED_IN_SCOPE` (all safe) /
  `VIOLATION_ESTABLISHED` (all violate) / `AMBIGUOUS_BOTH_POSSIBLE` /
  `INSUFFICIENT_MODEL_OR_OBSERVABILITY` /
  `INCONSISTENT_OBSERVATIONS_OR_MODEL` (never a vacuous PASS).
- `MayViolate` / `MustViolate` with the nonempty-guard: an empty history set
  never yields a universal claim.
- Evidence-monotonic refinement: new observations shrink `H(O)`, never grow
  it, never invent facts. Contradictory evidence raises
  `InconsistentEvidenceError` — flagged, not silently resolved.
- Hard refusals: timeout ⇒ nothing; ack ⇒ no effect; missing receipt ⇒
  nothing outside covered-complete scope.
- Safety policy while ambiguous: inspect/reconcile permitted; certification,
  LEARN promotion, and blind retry withheld. Handoffs carry every remaining
  world.
- `diagnose()` takes observations only — indistinguishable observations
  cannot produce different diagnoses (answer-key leakage structurally
  impossible).

## Sharpest case: RFD-AMB-001

Two sealed worlds, identical observations (request sent, revocation
committed, effect receipt missing). World L: effect before revocation.
World V: effect after revocation against the fence. The worker stays
`AMBIGUOUS_BOTH_POSSIBLE` in both. Staged trusted evidence narrows to legal
(2A) or violation (2B); removing it returns to ambiguity.

## What this does NOT claim

- The engine is fixture-scale: histories are explicitly enumerated with a
  hard cap (`MAX_HISTORIES`). Oversized spaces return
  `INSUFFICIENT_MODEL_OR_OBSERVABILITY` instead of silently sampling. It is
  not a production trace analyzer.
- Vendored D29/D30/D31 code is byte-identical to draft branches
  `naya4/d30-causal-trace` and `naya4/d31-incident`. At merge time these
  land in dependency order (or this branch rebases onto them) — until then
  this branch is self-contained so the UD-10 acceptance gate runs on the
  real machinery.
- An established violation may be learned from (`may_promote_to_learn`
  is True for `VIOLATION_ESTABLISHED`): established knowledge, even bad
  news, is learnable. Ambiguity never is.
