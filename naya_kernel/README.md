# naya_kernel — nine-node kernel scaffold

**CANDIDATE — NOT RATIFIED — NOT MERGED.** Stubs only; no node is implemented.

## What this is

The structural target for closing **GAP-A**: `Kernel.decide()` must exercise all
nine nodes' gates in pipeline order (SELF → LAW → ACT → KNOW → PROVE → CONNECT
→ VERIFY → LEARN → EVOLVE), with the nine-node manifest and gate script present.
Today the kernel exercises SELF+LAW only; this package is the shape the full
kernel will fill.

## Layout

- `node_base.py` — the strict interface every node implements: `manifest_entry()`,
  `gate()` (PASS/FAIL/NEED_EVIDENCE), `persisted_transitions()`, `evidence_hooks()`,
  `authority_checks()`, `cold_reconstruct()`.
- `nodes/` — nine stub modules, each quoting its spec's contractual responsibility
  in the docstring; every method raises `NotImplementedError`.
- `kernel.py` — `Kernel.decide()` skeleton (GAP-A closure point).
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
