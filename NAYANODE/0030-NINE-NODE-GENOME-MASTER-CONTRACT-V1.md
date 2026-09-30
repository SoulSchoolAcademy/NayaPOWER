# NayaPOWER Nine-Node Genome — Master Contract V1

**STATUS:** CANONICAL ENGINEERING CONTRACT
**TARGET:** AAA / 10-star
**KERNEL:** SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE

## 1. Purpose

This is the qualification bar for the nine responsibilities that make up the NayaPOWER kernel. It is not a claim that every responsibility is already production-proven. Implementation and runtime evidence must earn each status.

## 2. Life-cycle proof ladder

SPECIFIED → IMPLEMENTED → LOADED → INVOKED → INFLUENTIAL → APPLIED → OUTCOME_OBSERVED → VERIFIED → LEARNED → COMPOUNDED → SUCCESSOR_RETAINED → EVOLVED

No state may be inferred from the previous state.

## 3. Universal node contract

Every node MUST expose: stable identity/version; input schema; output schema; state machine; preconditions/postconditions; invariants; dependencies; authority context where relevant; provenance; execution/correlation ID; deterministic receipt; failure taxonomy; negative-path behavior; evidence; performance measurements; compatibility information.

Every node MUST fail closed when required identity, substrate, authority, provenance, or contract integrity is missing.

Every node MUST NOT invent identity, manufacture authority, convert UNKNOWN to VERIFIED, hide conflicts, treat retrieval as authorization, treat execution as verification, promote candidate learning without evidence, or silently inherit predecessor permissions.

## 4. Canonical message envelope

{ message_id, execution_id, source_node, target_node, contract_version, timestamp, identity_context, authority_context, truth_context, provenance, payload }

The envelope transports context; it does not replace a node-specific contract.

## 5. Canonical receipt

A consequential transition records receipt_id, execution_id, node_id, node_version, input/output hashes, state_before/state_after, decision, evidence references, authority reference, provenance references, gaps, and timestamp.

A receipt proves that an execution record exists. It does not automatically prove the truth of its claims.

## 6. Cross-node dependency law

| Node | Primary dependencies | Forbidden self-authority |
|---|---|---|
| SELF | identity substrate, checkpoint | cannot grant authority |
| LAW | SELF, governance substrate | cannot execute |
| ACT | SELF, LAW, action substrate | cannot verify outcome |
| KNOW | SELF, persistence/retrieval | cannot authorize use |
| PROVE | KNOW, evidence substrate | cannot manufacture evidence |
| CONNECT | KNOW, PROVE, graph substrate | cannot create trust from similarity |
| VERIFY | ACT, PROVE, observations | cannot claim unsupported causality |
| LEARN | VERIFY, KNOW | cannot promote unverified candidates |
| EVOLVE | LEARN, LAW, VERIFY, SELF | cannot inherit authority silently |

## 7. Universal test battery

1. happy path
2. schema validation
3. state transition validation
4. missing dependency
5. malformed input
6. identity conflict
7. authority boundary
8. provenance loss
9. stale/superseded data
10. replay/idempotency
11. concurrency where applicable
12. receipt integrity
13. real runtime invocation
14. behavioral influence/counterfactual
15. live substrate proof
16. independent verification
17. cold successor continuity

## 8. AAA release gate

A node is AAA-qualified only when implementation matches the contract, negative paths are tested, real runtime invocation is demonstrated, receipts are inspectable, evidence supports every claimed state, critical gaps are exposed, security boundaries are tested, performance is measured, and a cold successor can continue safely.

## 9. Failure semantics

BLOCKED = required preconditions absent.
FAILED = execution attempted and failed.
DEFERRED = evidence or authority is insufficient.
INCONCLUSIVE = observations do not establish the claim.
VERIFIED = the declared verification contract was satisfied.
PRODUCTION-PROVEN = the actual production boundary was exercised and independently evidenced.

## 10. Kernel birth test

The kernel is behaviorally alive only when controlled evidence shows durable intelligence → retrieval → governed influence → changed behavior → real outcome → independent verification → promoted learning → later held-out improvement → cold successor reuse.

Anything below this is a partial capability, not completion.