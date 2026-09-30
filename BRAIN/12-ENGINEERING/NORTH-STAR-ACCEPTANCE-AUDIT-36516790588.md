# NayaPOWER — Canonical North-Star Acceptance Audit

**Acceptance run:** `36516790588`  
**Acceptance source revision:** `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Audit date:** 2026-09-29 UTC  
**Audit posture:** independent reconstruction from persisted GitHub artifacts and authoritative Supabase records; workflow assertions are treated as claims, not proof.

## Executive finding

**Result: PARTIAL / NOT YET ACCEPTED as a fully independent North-Star acceptance.**

The persisted evidence independently reconstructs the core chain through fresh learning, causal behavioral change, promotion, retained-learning reread, cold successor retrieval, related-task reuse, unrelated-task refusal, graph-context behavior, independent verifier recomputation, and non-inherited authority.

However, two material evidence boundaries prevent a clean full acceptance:

1. **Historical checkpoint is no longer independently reconstructable from the authoritative current database.** The run's persisted artifacts identify checkpoint `a58dc3f0-5968-43dc-98ad-c31930777096` at revision 800 and show its state tied to the fresh lesson. The authoritative `nayanet_project_cognition_state` table is a single mutable row and now contains a later checkpoint state at revision 823, with a different learning/block/lineage/event. No separate checkpoint table exists. Therefore the historical checkpoint rung is supported by the run's persisted receipt/artifact, but cannot be independently re-read from current authoritative state.

2. **No rows exist in `nayanet_execution_outcomes` for the control/treatment execution receipts used by the causal learning proof.** The causal proof is therefore independently reconstructable from `nayanet_execution_receipts` plus the learning/block/lineage/index records, but it does not have a second persisted execution-outcome ledger corroborating those two receipts.

These are evidence-boundary findings, not claims that the underlying behavior did not occur.

## Source / deployment boundary

- Run `36516790588` checked out and executed against `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`.
- The deployed CONNECT runtime independently reported `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`.
- The generated deployed-runtime observation records the same revision and a digest of the actual runtime response.
- The current `main` has advanced: `38a2bd9ade375144e3ed6b1a67c4a0842d3244a1` is two commits ahead of `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`. Therefore **the acceptance run is historically valid only for c9**, and must not be represented as proof that current main is deployed.
- The current workflow file itself is unchanged between c9 and current main (same blob SHA), but current main also contains kernel and migration-ledger changes. This is why the historical source/deployment boundary is preserved explicitly.

## GitHub artifact integrity

All 16 persisted artifacts exposed by run `36516790588` were downloaded and their local SHA-256 digests matched the GitHub artifact metadata digests exactly.

| Artifact | GitHub digest matched | Evidence role |
|---|---|---|
| `naya-cold-runtime-1` | YES | cold runtime 1 |
| `naya-cold-runtime-2` | YES | cold runtime 2 |
| `cold-successor-receipt` | YES | first cold successor |
| `cold-successor-receipt-verified` | YES | independent successor verification |
| `live-connect-runtime-receipt` | YES | deployed runtime + parity |
| `causal-learning-experiment` | YES | candidate + control/treatment |
| `causal-verification` | YES | CVO |
| `causal-learning-experiment-receipt` | YES | independent causal reconstruction |
| `learning-promotion` | YES | promotion + lock-in |
| `independent-retained-learning-reread` | YES | fresh authoritative reread |
| `cold-graph-behavior-pair` | YES | graph OFF/ON behavior |
| `cold-graph-independent-verification` | YES | graph recomputation |
| `active-learning-generalization` | YES | related holdout + negative transfer |
| `independent-active-learning-generalization` | YES | independent recomputation |
| `cold-successor-generalization` | YES | successor related/unrelated reuse |
| `active-learning-generalization-successor-proof` | YES | independent successor generalization proof |

## 18-job acceptance chain

The run contains 18 completed-success jobs. The audit below does not treat those conclusions as sufficient proof; it maps each job to independently inspected source and/or persisted state.

| Job | Independent audit result |
|---|---|
| `contract` | **SUPPORTED.** c9 source tests explicitly bind canonical Naya identity, owner binding, token-rotation stability, and GitHub OIDC workflow binding. |
| `cold-runtime-1` | **SUPPORTED.** Persisted receipt has canonical Naya/block/owner, retained lesson, OIDC identity. |
| `cold-runtime-2` | **SUPPORTED.** Same canonical identity and behavior with a different OIDC JTI. |
| `independent-verification` | **SUPPORTED.** c9 verifier recomputes required fields and requires different JTIs; persisted inputs satisfy the contract. |
| `live-connect` | **SUPPORTED.** Actual runtime response + generated observation report c9; CONNECT is connected, but consequential behavior is blocked by LAW and no mutation/RLS/credential change occurred. |
| `independent-connect-verification` | **SUPPORTED.** c9 verifier contract independently checks the persisted response. |
| `learning-influence-experiment` | **SUPPORTED.** Current authoritative receipts reproduce the exact control/treatment delta and source lineage. |
| `independent-learning-influence-verification` | **SUPPORTED.** Final causal receipt records authoritative reread/recomputation with executor claims explicitly untrusted. |
| `cold-graph-control-treatment` | **SUPPORTED.** Authoritative receipts show OFF = direct-canonical requirement and ON = verified contextual intelligence. |
| `independent-cold-graph-verification` | **SUPPORTED.** Persisted verifier artifact records pair reread, verified treatment relationships, and independent reconstruction. |
| `learning-promotion` | **SUPPORTED WITH CHECKPOINT CAVEAT.** Learning is currently ACTIVE, block is DURABLE/LEARNED, relationship is VERIFIED, index is DURABLE; historical checkpoint itself is no longer independently rereadable. |
| `independent-retained-learning-reread` | **SUPPORTED WITH CHECKPOINT CAVEAT.** Learning, block, relationship, lineage, index, and causal evidence survive in authoritative state; checkpoint ID is historical and current state has moved on. |
| `cold-successor` | **SUPPORTED.** Successor receives only learning_id/task_id, uses no local state or caller-supplied intelligence content, reconstructs from authoritative state, and derives behavior from the retained lesson. |
| `cold-successor-verification` | **SUPPORTED.** Independent verifier recomputes behavior and authority boundary; successor grant count = 0 and blocked by IDENTITY_SCOPE. |
| `active-learning-generalization` | **SUPPORTED.** Related holdout materially reuses provenance capability; unrelated arithmetic task refuses transfer. |
| `independent-active-learning-generalization` | **SUPPORTED.** Independent recomputation records related delta, stable unrelated outcome, and negative-transfer refusal. |
| `cold-successor-generalization` | **SUPPORTED.** Cold successor reconstructs retained learning for a related task and refuses unrelated transfer, with no inherited authority. |
| `cold-successor-generalization-verification` | **SUPPORTED.** Final persisted successor-generalization proof independently records no inherited authority and zero successor grants. |

## Exact authoritative reconstruction

### Fresh intelligence persistence

Current Supabase records independently agree on the following chain:

`event → Intelligent Block → lineage → relationship → index → learning evidence`

- Event: `aa735543-4f00-45ec-a9db-9bd6055e24d9`
- Event key: `NAYA-FLOW-LESSON-7ccdf73c3c0049b4812599c28ba74386`
- Commit receipt: `32ff7884-e44b-46fc-84d2-682cd6f00161`
- Intelligent Block: `IB-NAYA-FLOW-LESSON-7ccdf73c3c0049b4812599c28ba74386`
- Block row: `0fad29cb-6f9f-40f4-97ec-360758883a07`
- Lineage: `c7401602-90ee-4e8d-ae16-c34f3e4e9aa0`
- Relationship: `cb5cc82a-c4a1-41cf-ad33-aceffbc10004`
- Index: `ce6f92cb-5aa4-4b92-bcf7-0d8e67b91f53`
- Learning: `65b93cdb-3981-4504-badd-a38861ffb971`
- Owner: `adfdf0b8-5558-41d1-9fed-ec51abf4fe2f`
- Learning status: `ACTIVE`
- Block status: `DURABLE`
- Block understanding state: `LEARNED`
- Relationship epistemic state: `VERIFIED`
- Index status: `DURABLE`

The exact lesson persisted is: **“Preserve provenance before applying retained intelligence.”**

### Authority boundary

Two current authority grants exist for the owner:

- `ab66924e-aa3b-4c57-a029-20e96a6a8afc`: `naya_node_apply`, target `NAYA-NODE-0001`.
- `0e082400-de6d-485e-9ebc-51b34f5debdc`: `intelligence_commit`, target `NAYA-NODE-0001`, consequential actions explicitly false.

The successor proofs independently report:
- authority inherited = false
- retrieval creates authority = false
- knowledge creates authority = false
- successor grant count = 0
- consequential action authorized = false
- execution = false
- blocked by `IDENTITY_SCOPE`

The durable successor handoff row also has `authority_inherited = false` and requires fresh authorization.

### Causal learning

Authoritative control/treatment receipts agree with the persisted causal receipt:

- Control: `5b072812-699f-415d-b759-2ed509c36367`
  - behavior: `REQUIRE_DIRECT_CANONICAL_INTELLIGENCE`
  - provenance preserved: false
  - retained intelligence used: false
- Treatment: `109944fc-9868-45e3-a532-f40952aea3a1`
  - behavior: `PRESERVE_PROVENANCE_BEFORE_APPLY`
  - provenance preserved: true
  - retained intelligence used: true
  - source event bound to the fresh lesson
  - Intelligent Block bound to the fresh lesson

The persisted independent-verification basis says the verifier recomputed the outcome from authoritative state, did not trust the executor claim, found the same task input, same learning, same source event, a behavioral delta, and an outcome delta of `provenance_preserved = 1`.

### Generalization and negative transfer

Authoritative receipts show:

- Related held-out task `NAYA-0001-PROVENANCE-HELDOUT-002`:
  - control: `REQUIRE_DIRECT_CANONICAL_INTELLIGENCE`
  - treatment: `PRESERVE_PROVENANCE_BEFORE_APPLY`
  - applicability true
  - provenance preserved only under treatment
- Unrelated arithmetic task `NAYA-0001-UNRELATED-ARITHMETIC-001`:
  - both conditions return `NO_APPLICABLE_RETAINED_INTELLIGENCE`
  - arithmetic result remains 12
  - applicability false

The independent generalization artifact recomputes the same result and explicitly records negative-transfer refusal.

### Graph behavior

Authoritative graph receipts show:

- Graph OFF: `REQUIRE_DIRECT_CANONICAL_INTELLIGENCE`
- Graph ON: `APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE`
- ON selected two VERIFIED relationships:
  - KNOW → `IB-NAYA-NODE-0001-0001`
  - PROVE → `IB-NAYA-NODE-0001-0001`

The independent graph verifier rereads the persisted pair and independently confirms the behavioral delta and verified treatment relationships.

## Cold successor boundary

The successor artifacts are unusually strong on the authority boundary:

- caller supplies only `learning_id` + task identifier
- intelligence content is not accepted as caller input
- local state is not used
- reconstruction is from authoritative state
- related task behavior is materially attributable to retrieved retained intelligence
- unrelated transfer is refused
- no successor authority grant is created
- consequential execution remains blocked by identity scope

This establishes a real cold retrieval/reuse boundary for this bounded proof. It does **not** establish universal generalization or unrestricted autonomous capability.

## Current-state drift discovered by the audit

The current `nayanet_project_cognition_state` row is now:

- revision: 823
- latest event: `204e6117-62fc-4f98-b31f-0efee45574c8`
- learning: `bcfd22b2-0acc-4880-ac12-9d235dcc82d7`
- Intelligent Block: `IB-NAYA-FLOW-LESSON-9a7d39bce1414c5da7a203bf16b93ede`
- lineage: `37d05370-361f-4b82-b587-84a3eeb2eba1`

That row was updated after the acceptance run. The historical checkpoint `a58dc3f0-5968-43dc-98ad-c31930777096` is not separately persisted in a checkpoint table. This is the primary reason the audit does not certify the checkpoint rung as independently reconstructed today.

## Acceptance disposition

**Do not label run `36516790588` as a fully independently proven North-Star acceptance yet.**

What is independently supported is substantial: persisted intelligence, provenance, causal behavioral change, promotion, retained reread, cold successor reconstruction, related-task reuse, unrelated refusal, graph-context behavior, OIDC identity separation, and non-inherited authority.

What remains unclosed is evidence durability/reconstructability at the historical checkpoint boundary, plus the absence of a corroborating execution-outcome row for the causal control/treatment receipts.

## Canonical next action

**Make the historical checkpoint independently reconstructable and add/restore an immutable persisted checkpoint receipt (or equivalent durable checkpoint record) for the exact learning `65b93cdb-3981-4504-badd-a38861ffb971`, then rerun the independent North-Star audit without changing the acceptance semantics.**

No new brain, second database, token loop, or parallel proof lane is authorized by this audit.
