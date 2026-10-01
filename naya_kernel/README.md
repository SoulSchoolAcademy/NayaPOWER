# naya_kernel — nine-node kernel

**CANDIDATE — NOT RATIFIED — NOT MERGED.** Tested candidate code on this
branch only; NOT production, NOT merged, NOT ratified.

## What this is

The nine-node decision graph closing **GAP-A**: `Kernel.decide()`
traverses the canonical 13-edge runtime graph (per the Ultimate Lock;
executable communication is not one mandatory linear call stack),
exercising all nine nodes' gates with per-edge fail-fast/fail-closed
semantics
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
- `kernel.py` — `Kernel.decide()` (GAP-A closure: all nine gates traversed
  on the canonical 13-edge runtime graph, per-edge fail-fast/fail-closed;
  order, first non-PASS short-circuits, hash-bound decision receipt) and
  `Kernel.gate_all()` (every gate, no short-circuit).
- `manifest.json` — nine-node manifest: per-node implementation status,
  the 13-edge runtime graph topology, the Ultimate Lock reconciliation
  record, and the ratified V2.1 calculus binding; all versions
  `0.1.0-candidate`.

## How the overnight build loop filled it in

1. Each node spec reached the CANDIDATE bar overnight; ratification is
   Shawn's word (morning package).
2. All nine node modules implemented against their candidate specs; the
   per-node tests in `tests/test_nodes/` are green (NOT ratified/merged/
   deployed — tested candidate code on this branch only).
3. `Kernel.decide()` traverses the canonical 13-edge runtime graph and
   emits hash-bound decision receipts; the 9/9-green demo receipt is
   recorded in the goal workspace (`hidden_files/node-build-demo-receipt.json`).
4. Nothing here merges to main or deploys without Shawn's explicit word.

## Open question

LEARN's spec declares itself the *ninth* pipeline responsibility and EVOLVE the
*last*, leaving the eighth slot unassigned. The overnight review should resolve
whether slot 8 is reserved, unnamed, or a spec numbering error.
