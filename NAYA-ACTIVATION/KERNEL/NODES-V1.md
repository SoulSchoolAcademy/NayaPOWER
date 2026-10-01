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
| SELF | NAYA-KERNEL-SELF | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_self_node.py | 37/37 pass | 2026-09-30 ~20:55 PDT |
| LAW | NAYA-KERNEL-LAW | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_law_node.py | 27/27 pass | 2026-09-30 ~20:55 PDT |
| ACT | NAYA-KERNEL-ACT | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_act_node.py | 32/32 pass | 2026-09-30 ~20:55 PDT |
| KNOW | NAYA-KERNEL-KNOW | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_know_node.py | 50/50 pass | 2026-09-30 ~20:55 PDT |
| PROVE | NAYA-KERNEL-PROVE | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_prove_node.py | 34/34 pass | 2026-09-30 ~20:55 PDT |
| CONNECT | NAYA-KERNEL-CONNECT | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_connect_node.py | 49/49 pass | 2026-09-30 ~20:55 PDT |
| VERIFY | NAYA-KERNEL-VERIFY | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_verify_node.py | 75/75 pass | 2026-09-30 ~20:55 PDT |
| LEARN | NAYA-KERNEL-LEARN | naya4/nine-node-kernel-v1 | d5353d8f2ac321d20ddfd04aae54ca81dbfe27c0 | tests/test_nodes/test_learn_node.py | 58/58 pass | 2026-09-30 ~20:55 PDT |

Kernel-wide at that SHA: `tests/test_nodes/` 367/367 pass. Verified in an
ephemeral /tmp worktree (clean public clone at the exact SHA, no seat
credentials), read-only; worktree removed after the run.

Spec-fidelity spot-review (adversarial, LEARN this run): LEARN implements the
reconciled `specs/LEARN-NODE-SPEC-CANDIDATE.md` (Naya 4's merge of the
NODE_8 LEARN PDF — builder sign-in on #554, 2026-09-30 ~20:35 PDT). Verified
present in code: VERIFIED_PASS-only bounded intake, LearningKey dedupe,
duplicate + contradiction reconciliation, promotionEligible V^P^R^A^B^N^C +
condition-0 calculusVersion gating, seven hard refusals, self-dealing block,
CORE-class/governance/identity → BRIEF routing, propose-only calibration,
hash-bound receipts, validity envelopes, generalization ceiling,
holdout-contamination fields, inert investigation placeholders. The node is
CANDIDATE code — not ratified, not merged, not deployed.

## Pending nodes (scaffold stubs)

EVOLVE — 2 stub acceptance tests only; not yet implemented as a candidate.
No wiring for a stub: activation binds only verified-green nodes.

`Kernel.decide()` exists at this SHA but exercises only the SELF and ACT
gates — full nine-node wiring (GAP-A closure) is the builder's sequenced-next
unit tonight, per their #554 sign-in. No activation binding on decide() until
it is verified to run all nine gates.

## Standing open questions (carried, not decided here)

- Pipeline slot 8 is unassigned (manifest: LEARN claims 9th, EVOLVE is "last").
- All eight verified nodes are CANDIDATE implementations of candidate specs;
  ratification is Shawn's, human-only.

## What this unlocks

- Morning cold-acceptance receipt can instantiate SELF, LAW, ACT, KNOW, PROVE,
  CONNECT, VERIFY, LEARN; EVOLVE awaits implementation.
- The full nine-node acceptance receipt awaits EVOLVE implementation plus the
  `Kernel.decide()` nine-gate wiring.
- Further revisions land on this branch before 05:00 PDT per the watch; after
  that, wiring batches into the morning report.

Lane: `activation/*` only. No touch on `naya_kernel/`, `naya4/*`, or main.
Sign-in/out on issue #554.
