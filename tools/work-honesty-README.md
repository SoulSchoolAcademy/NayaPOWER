# Work-Honesty Tracker (UD-08)

**Plain words:** authorized work must actually move, and progress claims must be
honest. This is the machinery that tracks a work item from authorization to
verified outcome — and refuses to mark it done without proof. No motion
mistaken for movement.

## The state machine

```
AUTHORIZED -> IN_PROGRESS -> CLAIMED_DONE -> VERIFIED_DONE
     any live state -> BLOCKED -> IN_PROGRESS   (unblock with evidence)
```

`STALLED`, `STARVED`, `UNVERIFIED_CLAIM`, `DEADLOCK_CYCLE`, `LIVELOCK_SUSPECT`
are **computed audit flags**, never worker-set states. A correct refusal
(`BLOCKED`) is never a stall.

## Transition evidence (every step)

| Transition | Requires |
|---|---|
| authorize | an authority source (no authority, no work) |
| start | doer identity + a first action (a pulse is not evidence) |
| claim_done | the artifact itself: content hash + pointer. No artifact → refused |
| verify PASS/FAIL | an **independent** verifier (seat AND session differ from doer's) + verification evidence |
| block | a named blocker + owner (optionally `blocked_by_item` for waits-for edges) |
| unblock | evidence the blocker is gone |

Refusals carry machine-readable codes: `NO_ARTIFACT`, `SELF_VERIFICATION`,
`NO_VERIFICATION_EVIDENCE`, `BLOCKED_CANNOT_COMPLETE`, `INVALID_TRANSITION`,
etc. A refusal is a verdict, not an exception to hide.

## What counts as progress

Only obligation-state changes (the `transitions` list). Heartbeats, notes, and
activity logs are recorded but earn **zero** progress credit — a thousand
logged actions with no discharged obligation is zero progress.

The audit report keeps **progress** and **fairness** in separate sections:
selections (service opportunity) are reported side by side with advancements,
never merged. A fair scheduler with broken workers must not be confusable
with a broken scheduler with lucky workers.

## Audit flags

- **STALLED** — `IN_PROGRESS` with no evidence movement past the window.
- **STARVED** — `AUTHORIZED` but never started past the window.
- **UNVERIFIED_CLAIM** — `CLAIMED_DONE` languishing without verification.
- **DEADLOCK_CYCLE** — cycle in the item-level waits-for graph.
- **LIVELOCK_SUSPECT** — repeated claim/verify-FAIL loops past threshold.

## Run the tests

```
python3 test_work_honesty.py   # 22/22 adversarial cases
```

## Scope note

This module is the work-honesty tracker: item-level states, evidence gates,
stale/deadlock/livelock detection. The full D22–D28 fairness machinery
(scheduler fairness layers, model checker + runtime harness, assumption
audit) remains follow-up work, explicitly out of this change.
