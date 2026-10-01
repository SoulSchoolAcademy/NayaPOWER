# NAYA-ACTIVATION / KERNEL / NODE BINDINGS V1

**CANDIDATE — NOT RATIFIED — NOT MERGED.**
This file binds the activation protocol's kernel responsibilities
(`SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE`)
to their independently verified candidate implementations.
Provisional: superseded when a node is ratified, merged, or superseded by a
newer verified SHA. Verified by Naya 2 (independent verifier lane —
builders don't self-certify; read-only verification of `naya4/*`).

## Verified-green nodes

| Responsibility | Node ID | Branch | Verified SHA | Suite | Result | Verified |
|---|---|---|---|---|---|---|
| SELF | NAYA-KERNEL-SELF | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_self_node.py | 37/37 pass | 2026-09-30 ~22:52 PDT |
| LAW | NAYA-KERNEL-LAW | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_law_node.py | 27/27 pass | 2026-09-30 ~22:52 PDT |
| ACT | NAYA-KERNEL-ACT | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_act_node.py | 32/32 pass | 2026-09-30 ~22:52 PDT |
| KNOW | NAYA-KERNEL-KNOW | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_know_node.py | 53/53 pass | 2026-09-30 ~22:52 PDT |
| PROVE | NAYA-KERNEL-PROVE | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_prove_node.py | 34/34 pass | 2026-09-30 ~22:52 PDT |
| CONNECT | NAYA-KERNEL-CONNECT | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_connect_node.py | 49/49 pass | 2026-09-30 ~22:52 PDT |
| VERIFY | NAYA-KERNEL-VERIFY | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_verify_node.py | 75/75 pass | 2026-09-30 ~22:52 PDT |
| LEARN | NAYA-KERNEL-LEARN | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_learn_node.py | 58/58 pass | 2026-09-30 ~22:52 PDT |
| EVOLVE | NAYA-KERNEL-EVOLVE | naya4/nine-node-kernel-v1 | 31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194 | tests/test_nodes/test_evolve_node.py | 63/63 pass | 2026-09-30 ~22:52 PDT |

Kernel-wide at that SHA: `tests/test_nodes/` **457/457 pass** (was 450/450 at
94340120ad). Kernel nine-node integration battery
(`tests/test_nodes/test_kernel_nine_node.py`): **22/22 pass** — covers the
13-edge runtime-graph traversal, per-edge fail-fast/fail-closed, LOCK minimum
routes as required subset, in-code table ↔ seed-file drift guard, and
hash-bound decision receipts. Full collectible repo suite: **964 passed, 3
skipped** (4 test files fail collection on the missing undeclared `pglast`
dependency — pre-existing environment gap, unrelated to `naya_kernel`).
Verified in an ephemeral /tmp worktree (clean public clone at the exact SHA,
no seat credentials), read-only; worktree removed after the run.

**`Kernel.decide()` — canonical 13-edge runtime graph VERIFIED (GAP-A closed).**
`naya_kernel/kernel.py` `RUNTIME_EDGES` traverses the canonical 13-edge
runtime graph (copied from
`BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json`; the 13
`REL-KERNEL-*` edge IDs and types match the seed 1:1, independently
re-checked this run; the seed's 9 `REL-VALUE-CALCULUS-*` edges are correctly
excluded from the runtime graph). `LOCK_MINIMUM_ROUTES` (11 routes) enforced
as the required subset. A gate is consulted only when every required upstream
gate PASSed (`GATE_REQUIREMENTS`; VERIFY requires ACT+PROVE+CONNECT;
EVOLVE requires LAW+LEARN). First non-PASS short-circuits (fail-fast);
`gate_all()` evaluates all without short-circuit for audit visibility.
Decision receipts are hash-bound (`decision-<id>`, `receipt_hash` over the
body; `verify_decision_receipt()` re-derives the hash — independently
exercised this run). `cold_reconstruct()` verifies each receipt hash and
lists mismatches — mismatched receipts are never trusted and their verdict
fields do not feed counts (Shawn's 21:04 PDT hardening). Activation binds
decide() at this SHA.

Spec-fidelity spot-review (adversarial, this run): the two functional
reconciliation commits are spec-faithful —
- `d86741b36` "Re-topologize Kernel.decide() onto the canonical 13-edge
  runtime graph": executable communication is no longer one mandatory linear
  call stack; the in-code table is drift-guarded against the seed file by
  test (test passes; manual 1:1 edge check also done). No gate weakened:
  per-edge fail-fast/fail-closed preserved; EVOLVE→SELF and ACT→KNOW
  correctly recorded as non-gate edges (next-cycle / write path).
- `7e72b2737` "Reconcile KNOW to the Ultimate Lock": KNOW's applicability
  exclusion removed — declared applicability now rides through as a
  non-steering `applicability_note` (`steering_decision=false`,
  `decided_by=NAYA-KERNEL-CONNECT`); epistemic claim/evidence assessment
  moved to PROVE (ingest of SUPPORTED/LEARNED/VERIFIED and REUSABLE
  promotion requires a well-formed `prove_receipt_ref` naming
  `NAYA-KERNEL-PROVE`); `truth_deltas` renamed `state_deltas` — KNOW is
  never the final truth authority. Matches the Ultimate Lock and
  `00-KNOW-MASTER-CONTRACT-V1.md` invariants ("Never promote final truth
  or task-level applicability; PROVE and CONNECT own those
  responsibilities"). **No discrepancy found at this depth.** Re-verified
  2026-09-30 ~22:22 PDT at `94340120ad6bae091a33a6111a88e429cc6ab9a4`
  ("HARDEN: remove remaining stale 'calculus unratified' premises
  (LAW/VERIFY)" — FLAG-001 step 4): diff is tightly scoped to removing
  stale CANDIDATE-calculus premises across connect/evolve/law/learn/verify
  nodes + node_base.py + manifest.json and binding the RATIFIED Decision
  Value Calculus V2.1 (CALCULUS_V21_SPEC_HASH pinned); the hard-coded spec
  blob SHA was independently checked against live main at a726a837 —
  exact match. LEARN/EVOLVE now allow autonomous promotion under the
  ratified calculus (condition 0 satisfied by ratification — intended
  ratified-law behavior, not a weakened gate). Deeper semantic
  qualification belongs to the dedicated qualification lane, not this
  watch. All code is CANDIDATE — not ratified, not merged, not deployed.

Re-verified 2026-09-30 ~22:52 PDT at `31864c25d46ce8ccbe0cfa47ca66e7c9c9bca194`
("HARDEN: spec-cited docstrings for public non-interface ops (LEARN
register_cvo/register_evidence/clear_harm_window/regress, KNOW expire_sweep,
CONNECT apply_transition) (candidate)"): the three new commits since
94340120ad are docstring-only — all 8 changed node source files are
AST-identical to 94340120ad ignoring docstrings (independently checked by
AST strip-and-compare), plus `manifest.json` status `SCAFFOLD` → `CANDIDATE`
and README state-accuracy. The 7 new `test_manifest_state.py` guard tests
assert the CANDIDATE status with the NOT RATIFIED / NOT MERGED banner —
evidence-law honesty, no behavioral change. decide() 13-edge topology
unchanged. All code is CANDIDATE — not ratified, not merged, not deployed.

## Pending nodes

None — all nine node responsibilities now bind verified-green candidate
implementations.

## Standing open questions (carried, not decided here)

- Pipeline slot 8 is unassigned (manifest: LEARN claims 9th, EVOLVE is "last").
- All nine verified nodes are CANDIDATE implementations of candidate specs;
  ratification is Shawn's, human-only.
- EVOLVE's spec open questions Q7–Q10 (mission immutability class, CORE-class
  succession, successor re-demonstration, personality-trait evolutions) are
  director decisions pending.

## What this unlocks

- Morning cold-acceptance receipt can instantiate all nine nodes and fire one
  decision through `Kernel.decide()` — the full nine-node acceptance path is
  clear at this SHA.
- Further revisions land on this branch before 05:00 PDT per the watch; after
  that, wiring batches into the morning report.

Lane: `activation/*` only. No touch on `naya_kernel/`, `naya4/*`, or main.
Sign-in/out on issue #554.
