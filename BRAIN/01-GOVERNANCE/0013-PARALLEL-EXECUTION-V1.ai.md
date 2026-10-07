# THE PARALLEL EXECUTION LAW — AI Specification

**Status:** DIRECTOR-RATIFIED (Shawn Vibert, 2026-10-06)
**Law ID:** PARALLEL-EXECUTION-V1 · `BRAIN/01-GOVERNANCE/0013-PARALLEL-EXECUTION-V1`
**Replaces:** nothing. **Amends:** nothing. **Constrains:** every execution plan by every seat.

## 1. Definitions

- **Task:** a unit of work with declared inputs, outputs, and completion criteria.
- **Dependency (A→B):** B cannot correctly start until A's outputs exist. Must be proven, not assumed. Temporal habit ("we always do A first") is NOT a dependency.
- **Lane:** an independent execution context (worker, process, seat) that can proceed without waiting on another lane.
- **Parallelizable(A, B):** true iff (a) no dependency A→B or B→A, (b) no exclusive-resource contention (same file locked for write, same rate-limited credential, same human gate), (c) concurrent execution preserves correctness of both.
- **Capacity:** the real concurrent-execution ceiling: CPU cores, RAM, API rate limits, human attention. Measured, not guessed.
- **Join:** the synchronization point where all lanes' results are collected and independently verified.

## 2. The rule (exact)

For every plan: `lanes = maximal set of parallelizable tasks sized to capacity`. Every task whose dependencies are met MUST be dispatched immediately on its own lane. Sequential execution of parallelizable tasks is a defect.

## 3. Procedure

1. Enumerate all tasks with inputs/outputs/completion criteria.
2. Build the dependency DAG. Challenge every edge: is the dependency real?
3. Compute the ready set (all tasks with no unmet dependencies). Dispatch ALL of them concurrently, up to capacity.
4. As tasks complete, recompute the ready set and dispatch. Never let a ready task wait for an unrelated task.
5. On lane failure: isolate it. Other lanes continue. The join verifies each lane independently; a failed lane is reported with its evidence, never hidden, never blocking healthy lanes silently.
6. Record in the scorecard: planned parallelism vs executed parallelism; any sequentialization of parallelizable work is named as a defect with its cause.

## 4. Capacity sizing

- `workers = min(ready_tasks, floor(available_capacity / per_task_cost))`.
- per_task_cost is measured (RAM per model load, seconds per file), never assumed.
- If capacity < 2, the law still applies: the plan must SHOW the parallelism it would use at capacity, and the scorecard must record capacity as the binding constraint.

## 5. Common violations

- Running N independent bakes/renders/tests one after another in a single loop.
- One agent doing five lanes sequentially instead of spawning five lanes.
- "Waiting for the full result" when partial lanes are already actionable.
- Claiming a dependency that is actually just ordering habit.

## 6. Interaction with other laws

- **Scorecard Law:** the execution scorecard must include the parallelism check. A plan that scores 9.0 but ran parallelizable work sequentially is not 9.0.
- **Evidence law:** each lane's output is verified independently. Parallelism never merges evidence.
- **Human gates:** a human gate is a real dependency (exclusive resource: the human's decision). It serializes correctly and is never "parallelized around."

## 7. Amendment path

Amendments follow the standard law-amendment procedure (loader refuses invalid amendment records). Until amended, every implementation honors this law.
