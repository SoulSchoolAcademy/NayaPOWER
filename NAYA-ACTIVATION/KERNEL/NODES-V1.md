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
| SELF | NAYA-KERNEL-SELF | naya4/nine-node-kernel-v1 | 245fe52e8a8d17b7a670cace2a5c8ff358d6d184 | tests/test_nodes/test_self_node.py | 37/37 pass | 2026-09-30 ~19:55 PDT |
| LAW | NAYA-KERNEL-LAW | naya4/nine-node-kernel-v1 | 245fe52e8a8d17b7a670cace2a5c8ff358d6d184 | tests/test_nodes/test_law_node.py | 27/27 pass | 2026-09-30 ~19:55 PDT |
| ACT | NAYA-KERNEL-ACT | naya4/nine-node-kernel-v1 | 245fe52e8a8d17b7a670cace2a5c8ff358d6d184 | tests/test_nodes/test_act_node.py | 32/32 pass | 2026-09-30 ~19:55 PDT |

Kernel-wide at that SHA: `tests/test_nodes/` 111/111 pass, `tests/test_kernel.py`
5/5 pass. Verified in an ephemeral /tmp worktree (clean public clone, no seat
credentials), read-only; worktree removed after the run.

## Pending nodes (scaffold stubs)

KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE — 2 acceptance tests each on the
scaffold baseline; not yet implemented as candidates. `Kernel.decide()` raises
`NotImplementedError` until all nine gates are built. No wiring for a stub:
activation binds only verified-green nodes.

## Standing open questions (carried, not decided here)

- Pipeline slot 8 is unassigned (manifest: LEARN claims 9th, EVOLVE is "last").
- Spec fidelity beyond each node's own documented contract is UNVERIFIED:
  no node-spec PDFs have landed in `~/workspace/user/files/` as of 19:55 PDT,
  and no reconciled spec is named on #554 — code matches its stated contract
  (1017-line ACT implementation, 32 genuine acceptance tests), not an
  independently published spec.

## What this unlocks

- Morning cold-acceptance receipt can instantiate SELF, LAW, ACT today;
  the full nine-node receipt awaits KNOW/PROVE/CONNECT/VERIFY/LEARN/EVOLVE.
- When a node lands and verifies green, append its row here on the next
  `activation/nine-node-wiring` revision (before 05:00 PDT per the watch);
  after that, wire in the morning report instead of new PRs.

Lane: `activation/*` only. No touch on `naya_kernel/`, `naya4/*`, or main.
Sign-in/out on issue #554.
