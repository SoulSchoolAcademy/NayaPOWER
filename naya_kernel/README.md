# naya_kernel — nine-node kernel

**CANDIDATE — NOT RATIFIED — NOT MERGED.** Tested candidate code on this
branch only; NOT production, NOT merged, NOT ratified.

## What this is

The nine-node decision graph closing **GAP-A**: `Kernel.decide()`
traverses the canonical 13-edge runtime graph (per the Ultimate Lock;
executable communication is not one mandatory linear call stack),
exercising all nine nodes' gates with per-edge fail-fast/fail-closed
semantics in the topological evaluation order
(SELF → LAW → KNOW → ACT → PROVE → CONNECT → VERIFY → LEARN → EVOLVE),
with the nine-node manifest present. A FAILing gate halts the whole decision
globally; a NEED_EVIDENCE gate edge-blocks only its downstream edges while
independent branches continue; `gate_all()` evaluates every gate without
short-circuit for
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
  `Kernel.gate_all()` (every gate, no short-circuit; emits a hash-bound
  AUDIT receipt — verifiable, but never counted as a decision verdict).
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

## Slot numbering — resolved

The manifest's old scaffold-era ordering left slot 8 unassigned (LEARN at 9,
EVOLVE at "last"). The slot gap was scaffold numbering drift, not a spec
claim — no LEARN/EVOLVE spec text declares pipeline-responsibility
numbering. Resolved: the manifest's `gate_order` now mirrors the kernel's
canonical `EVALUATION_ORDER` exactly — LEARN = 8, EVOLVE = 9, slots 1–9
contiguous (guard test in `tests/test_nodes/test_manifest_state.py`).

## Layering boundary — ACT deliberation vs execution (A-ACT-4)

The kernel implements the **execution half** of the ACT contract, not the
deliberative half. The five deliberative functions named in the master
contract — `plan_action`, `select_minimum_sufficient_action`,
`define_expected_outcome`, `define_proof_requirements`, `observe` (as a
deliberative callable) — have **no kernel implementation, by design**.
Deliberation lives in the agent layer: the layer that produces the
decision receipt's `winner` (tool_id, params, bounds) has already planned,
selected, and defined the expected outcome and proof requirements before
ACT is ever consulted. The kernel's ACT consumes that receipt — it
admits the decision verb, claims the execution under an idempotency key,
invokes only registered tools within the granted authority envelope,
observes the effects, and emits a hash-bound receipt a cold successor
can trust. ACT never re-scores, never overrides the verb, never grants
authority (`authority_checks()` declares validations only).

Do not read the spec's function list as claiming kernel implementations
that exist nowhere: the deliberative five are agent-layer
responsibilities; the kernel owns execution. If spec wording implies
otherwise, that is a spec-side wording issue for the spec lane, not a
kernel gap — the boundary is recorded here so neither side silently
assumes the other implements them.
