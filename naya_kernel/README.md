# naya_kernel — nine-node kernel

**CANDIDATE — NOT RATIFIED — NOT MERGED.** Tested candidate code on this
branch only; NOT production, NOT merged, NOT ratified.

## What this is

The nine-node decision pipeline closing **GAP-A**: `Kernel.decide()`
exercises all nine nodes' gates in pipeline order
(SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE),
with the nine-node manifest present. The first non-PASS gate short-circuits
(fail-fast); `gate_all()` evaluates every gate without short-circuit for
full audit visibility.

## Layout

- `node_base.py` — the strict interface every node implements: `manifest_entry()`,
  `gate()` (PASS/FAIL/NEED_EVIDENCE), `persisted_transitions()`, `evidence_hooks()`,
  `authority_checks()`, `cold_reconstruct()`.
- `nodes/` — the nine implemented node modules, each built against its
  candidate spec; every gate is covered by `tests/test_nodes/test_<node>.py`.
- `kernel.py` — `Kernel.decide()` (GAP-A closure: all nine gates in pipeline
  order, first non-PASS short-circuits, hash-bound decision receipt) and
  `Kernel.gate_all()` (every gate, no short-circuit).
- `manifest.json` — nine-node manifest skeleton, all versions `0.1.0-candidate`.

## How the overnight build loop fills it in

1. Ratify each node spec (morning package → Shawn's decision).
2. Implement each stub against its ratified spec; the smoke tests in
   `tests/test_nodes/` turn red→green as each node lands.
3. Implement `Kernel.decide()` to iterate all nine gates and emit decision receipts.
4. Nothing here merges to main or deploys without Shawn's explicit word.

## Open question

LEARN's spec declares itself the *ninth* pipeline responsibility and EVOLVE the
*last*, leaving the eighth slot unassigned. The overnight review should resolve
whether slot 8 is reserved, unnamed, or a spec numbering error.
