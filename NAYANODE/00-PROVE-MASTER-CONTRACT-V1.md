# NayaPOWER PROVE — Master Node Contract V1

**STATUS:** CANONICAL ENGINEERING TARGET — AAA
**NODE:** NAYA-KERNEL-PROVE
**RESPONSIBILITY:** evidence, provenance, truth

## 1. Purpose
Why should this claim be believed, how strong is its evidence, and what remains unproven?

## 2. Six-language definition
- **Human:** Why should this claim be believed, how strong is its evidence, and what remains unproven?
- **Child:** This part of Naya makes sure the right thing happens for the right reason.
- **Grandma:** It keeps this part of Naya honest about what it knows, what it may do, and what really happened.
- **Naya:** I must know my exact job, trusted inputs, current state, authority boundary, evidence, unknowns, downstream requirement, refusal condition, and receipt.
- **AI:** Execute the node contract deterministically around explicit context, evidence, state transitions, and governed boundaries.
- **Machine:** Validate schema → validate dependencies → execute transition → validate output → emit receipt → expose evidence/gaps → fail closed.

## 3. Required functions
- collect_evidence
- validate_provenance
- assess_evidence_strength
- assess_claim_strength
- compare_strengths
- detect_conflict
- record_limitations
- select_verification_method
- construct_claim
- downgrade_claim
- invalidate_claim
- emit_proof_receipt

## 4. Inputs
- claim
- evidence references
- provenance chain
- verification method
- limitations

## 5. Outputs
- claim state
- evidence strength
- conflicts
- limitations
- proof receipt

## 6. Invariants
- Never create evidence
- Never upgrade a claim because it is useful
- Never omit material limitations.

## 7. State machine
UNINITIALIZED → ASSESSING → ASSESSED; conflicts remain explicit
Every transition records before-state, after-state, transition reason, execution ID, evidence references, and timestamp. Invalid transitions fail closed.

## 8. Inter-node contract
KNOW supplies sources. VERIFY supplies outcome observations. LEARN consumes only qualifying claims.

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