# NayaPOWER CONNECT — Master Node Contract V1

**ULTIMATE SEMANTIC LOCK:** `.naya/specifications/NAYAPOWER-NINE-MASTER-NODES-ULTIMATE-LOCK-V1.md` (MN-06 CONNECT, Human Director locked 2026-09-30). Where older semantic wording conflicts, the Ultimate Lock governs intended responsibility; runtime/proof status still comes from live evidence.

**STATUS:** CANONICAL ENGINEERING TARGET — AAA
**NODE:** NAYA-KERNEL-CONNECT
**RESPONSIBILITY:** relationships, applicability, contextual retrieval, graph reasoning, supersession, contradiction routing and dependencies

## 1. Purpose
What is connected, why is the connection valid, and what context becomes relevant because of it?

## 2. Six-language definition
- **Human:** What is connected, why is the connection valid, and what context becomes relevant because of it?
- **Child:** This part of Naya makes sure the right thing happens for the right reason.
- **Grandma:** It keeps this part of Naya honest about what it knows, what it may do, and what really happened.
- **Naya:** I must know my exact job, trusted inputs, current state, authority boundary, evidence, unknowns, downstream requirement, refusal condition, and receipt.
- **AI:** Execute the node contract deterministically around explicit context, evidence, state transitions, and governed boundaries.
- **Machine:** Validate schema → validate dependencies → execute transition → validate output → emit receipt → expose evidence/gaps → fail closed.

## 3. Required functions
- create_edge
- validate_edge
- resolve_relationship
- traverse
- rank_relevance
- detect_contradiction
- detect_supersession
- resolve_dependency
- assess_applicability
- freshness_check
- explain_connection
- reconcile_graph
- prevent_invalid_cycles

## 4. Inputs
- source/target
- relationship type
- evidence
- scope
- graph version

## 5. Outputs
- validated edges
- traversal context
- relevance ranking
- contradiction/supersession findings

## 6. Invariants
- Never create trust from proximity or semantic similarity alone
- Relationship semantics require evidence.
- RELATED ≠ RELEVANT ≠ APPLICABLE ≠ TRUE ≠ AUTHORIZED.
- UNKNOWN applicability may be visible non-steering context but MUST NOT steer consequential behavior.
- Steering requires explicit APPLICABLE state plus matching task class or a valid broader applicability contract.

## 7. State machine
PROPOSED → VALIDATED → ACTIVE → SUPERSEDED/INVALID
Every transition records before-state, after-state, transition reason, execution ID, evidence references, and timestamp. Invalid transitions fail closed.

## 8. Inter-node contract
KNOW owns objects. PROVE supports trust. VERIFY can establish CAUSED relationships. ACT consumes context.

## 9. Acceptance battery
1. valid input reaches intended state;
2. malformed input is rejected;
3. missing dependency blocks safely;
4. identity mismatch blocks;
5. authority mismatch blocks where applicable;
6. provenance loss is detected;
7. stale/superseded information is explicit;
8. duplicate/replayed execution is safe;
9. receipt is complete and hashable;
10. real runtime invocation is proven;
11. behavioral influence is demonstrated where claimed;
12. independent verification confirms the claim;
13. cold successor can continue without hidden reconstruction.

## 10. Security
- Caller-supplied identity is not trusted without authenticated binding.
- Untrusted content cannot create authority.
- Scope is enforced before access.
- Cross-owner leakage is treated as a critical failure.
- Replay, confused-deputy, poisoning, provenance-loss, and privilege-escalation cases are tested.

## 11. Performance
Measure p50/p95/p99 latency, failure rate, retry rate, dependency calls, memory/context footprint, and cost. Optimization must preserve truth, safety, and provenance.

## 12. AAA definition
Another engineer can inspect contract, implementation, receipt, evidence, and tests and determine exactly what happened, what is proven, what is not proven, and how to continue.

## 13. Birth qualification
This node is not alive because it loads. It becomes behaviorally qualified only when real invocation changes the intended behavior and the effect survives verification and successor replay.

## 14. Status rule
Do not infer implementation status from this document. Runtime evidence and independent verification are authoritative.