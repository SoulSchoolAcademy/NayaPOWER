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
| SELF | NAYA-KERNEL-SELF | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_self_node.py | 37/37 pass | 2026-09-30 ~21:22 PDT |
| LAW | NAYA-KERNEL-LAW | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_law_node.py | 27/27 pass | 2026-09-30 ~21:22 PDT |
| ACT | NAYA-KERNEL-ACT | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_act_node.py | 32/32 pass | 2026-09-30 ~21:22 PDT |
| KNOW | NAYA-KERNEL-KNOW | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_know_node.py | 50/50 pass | 2026-09-30 ~21:22 PDT |
| PROVE | NAYA-KERNEL-PROVE | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_prove_node.py | 34/34 pass | 2026-09-30 ~21:22 PDT |
| CONNECT | NAYA-KERNEL-CONNECT | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_connect_node.py | 49/49 pass | 2026-09-30 ~21:22 PDT |
| VERIFY | NAYA-KERNEL-VERIFY | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_verify_node.py | 75/75 pass | 2026-09-30 ~21:22 PDT |
| LEARN | NAYA-KERNEL-LEARN | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_learn_node.py | 58/58 pass | 2026-09-30 ~21:22 PDT |
| EVOLVE | NAYA-KERNEL-EVOLVE | naya4/nine-node-kernel-v1 | 842af91ced2dac4e7e3dd49c06d8ae734e3e5748 | tests/test_nodes/test_evolve_node.py | 63/63 pass | 2026-09-30 ~21:22 PDT |

Kernel-wide at that SHA: `tests/test_nodes/` **440/440 pass** (was 367/367 at
d5353d8f). Kernel + organism battery (`tests/test_kernel.py`,
`tests/test_nine_node_organism_v1.py`,
`tests/test_nodes/test_kernel_nine_node.py`,
`tests/test_nodes/test_learn_node.py`): **81/81 pass** (was 69/69).
Verified in an ephemeral /tmp worktree (clean public clone at the exact SHA,
no seat credentials), read-only; worktree removed after the run.

**`Kernel.decide()` — nine-gate wiring VERIFIED (GAP-A closed).**
`naya_kernel/kernel.py` `GATE_ORDER` runs SELF → LAW → ACT → KNOW → PROVE →
CONNECT → VERIFY → LEARN → EVOLVE in pipeline order; `decide()` evaluates each
gate, first non-PASS short-circuits; `gate_all()` evaluates all without
short-circuit for full audit visibility. Decision receipts are hash-bound
(`decision-<id>`, `receipt_hash` over the body). `cold_reconstruct()` verifies
each receipt hash and lists mismatches — mismatched receipts are never
trusted and their verdict fields do not feed counts (Shawn's 21:04 PDT
hardening, 5 edge-case tests). Activation binds decide() at this SHA.

Spec-fidelity spot-review (adversarial, EVOLVE this run): EVOLVE implements
the reconciled `specs/EVOLVE-NODE-SPEC-CANDIDATE.md` (Naya 4's merge of the
NODE_9 EVOLVE PDF — builder sign-in on #554, 2026-09-30 ~20:35 PDT).
Verified present in `naya_kernel/nodes/evolve_node.py`: MISSION on the
immutable surface (ORDERING_LAW MISSION-first; MISSION_DRIFT refusal —
`M_t+1 = M_t` unless the Human Director explicitly ratifies), three state
axes never collapsing, stale-proposal rule (`STALE_PROPOSAL` →
REBASE/RE-EVALUATE), bounded `impact_closure` transitive-dependency analysis,
blast-radius taxonomy (context, never permission), `SuccessorKey` idempotency
+ compare-and-swap version promotion, Cold-14 continuity questions,
SHA256-canonicalized package hashes, PROHIBITED classes (mission redefinition
among them), director-set autonomous envelope, class-specific freshness,
armed-and-receipted rollback, independent replayability,
anti-self-ratification via `deciding_config_hash` binding. **No discrepancy
found at this depth.** Deeper semantic qualification belongs to the dedicated
qualification lane, not this watch. The node is CANDIDATE code — not ratified,
not merged, not deployed.

## Pending nodes

None — all nine node responsibilities now bind verified-green candidate
implementations. (EVOLVE was a scaffold stub at d5353d8f; implemented at
3709f3ce, verified this run.)

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
