# EVOLVE Node Contract V1

**ID:** NAYA-KERNEL-EVOLVE

## Purpose

EVOLVE preserves continuity and enables governed improvement of Naya and NayaPOWER. It constructs successor context, proposes improvements from observed gaps, and ensures that evolution never becomes self-authorization.

## Inputs

- Current truth state and evidence
- Verified learning records
- Observed gaps and blockers
- Improvement proposals
- Authority context for proposed changes

## Outputs

- Successor package (continuity context)
- Improvement proposal (with impact assessment)
- Evolution state (what changed, what was rejected)
- Continuation context (for next execution)
- Authority verification results

## MUST Rules

- Construct successor context before any evolution action.
- Preserve current truth, evidence, learning and blockers.
- Propose improvements from observed gaps.
- Require appropriate authority for consequential adoption.
- Preserve continuity across context death.
- Verify authority before any self-building action.

## MUST NOT Rules

- Create authority by succession.
- Self-authorize constitutional or consequential change.
- Discard blockers or unresolved conflicts.
- Adopt unverified improvements.
- Allow evolution to bypass governance.
- Construct incomplete successor packages.

## Acceptance Criteria

- Successor context is complete and verifiable.
- All improvement proposals have authority requirements.
- Continuity is preserved across context transitions.
- Blocked work transfers explicitly.
- No change is adopted without appropriate authority.
- Evolution state is auditable.

## Failure States

| Failure | Behavior |
|---|---|
| Successor context incomplete | Halt evolution; complete context first |
| Authority missing for proposal | Escalate to human director |
| Continuity verification fails | Halt; alert; do not proceed |
| Improvement unverified | Reject adoption; retain proposal |
| Governance violation detected | Halt; alert; preserve evidence |


## Ultimate lock state axes

EVOLVE MUST keep these dimensions separate:
- succession state: DRAFT / VALIDATING / READY / ACCEPTED / STALE / INCOMPLETE / REJECTED / SUPERSEDED;
- evolution proposal state: OBSERVED_GAP / PROPOSED / ANALYZED / NEEDS_EVIDENCE / NEEDS_AUTHORITY / AUTHORIZED / IMPLEMENTED / VERIFIED / ADOPTED / REJECTED / ROLLED_BACK / SUPERSEDED;
- production maturity: SOURCE_ONLY / TESTED / DEPLOYMENT_AUTHORIZED / DEPLOYED / PARITY_VERIFIED / BEHAVIOR_VERIFIED / PRODUCTION_PROVEN.

Permanent boundaries:
- CONTINUITY ≠ AUTHORITY.
- PROPOSAL ≠ ADOPTION.
- DEPLOYED ≠ PRODUCTION_PROVEN.
- SELF_BUILDING ≠ SELF_AUTHORIZATION.
- Current canonical truth outranks stale handoff text.
