# NAYA EXECUTION

**Status:** CANONICAL EXECUTION LAYER

`.naya/execution/` holds the durable work input for Naya Power continuous execution.

## Master Work Queue

`WORK-QUEUE.json` is the ONE durable, priority-aware Master Work Queue. Every legitimate
mission/task is represented with the full field set (mission, objective, current state, why it
matters, dependencies, authority, constraints, protected boundaries, acceptance criteria, test
requirements, evidence requirements, quality scorecard, minimum/target score, risk,
rollback/repair, next action, successor action, autonomy level, status, and selector factors).

Authority:

1. It is **subordinate** to `.naya/codex/11-RUNTIME-CONSTITUTION.md`, the control plane
   (`MAP`/`STATE`/`BLOCKS`/`PROOF`/`GOVERNANCE-KERNEL`), and the governance kernel.
2. It is **not** a state database and does **not** define a competing state machine. Work item
   status uses the queue vocabulary; governed execution state remains owned by
   `.naya/runtime/execution_controller.py`.
3. The **only** selector is `.naya/runtime/priority_decision.py`. The queue feeds it; it never
   replaces it.

Quality policy: nothing knowingly below **9.0** passes; **9.5+** is the target; **10.0** is the
objective. A task that improves one thing while damaging another is a regression and must be
repaired or reverted before acceptance.

## Commands

```text
python .naya/execution/validate_work_queue.py validate    # structural + semantic gate
python .naya/execution/validate_work_queue.py select      # exactly one highest-value task
python .naya/execution/validate_work_queue.py self-test   # adversarial fail-closed proof
python .naya/execution/test_work_queue.py                 # adversarial unit tests
```

`select` returns `STOP_CLEANLY` when no legitimate executable unblocked work remains. It never
invents work to stay busy.

## Rules

- Fail closed. A malformed or ambiguous queue is RED, never silently repaired.
- `BLOCKED` requires a `blocked_reason`; human-authority tasks must remain `BLOCKED` until the
  human authorizes them.
- A `READY`/`IN_PROGRESS` task must have all dependencies `COMPLETE`.
- Selector factors are 0..1 and use the canonical formula in `priority_decision.py`.
- Queue changes are execution-layer changes. They do not by themselves authorize execution,
  deployment, or any protected-scope modification.
