# NAYANET UNIVERSAL MEANINGFUL-OUTPUT PROMOTION CONTRACT V1

STATUS: CANONICAL WORKING CONTRACT
EFFECTIVE: 2026-09-23
MISSION RING: P0 — UNIVERSAL MEANINGFUL-OUTPUT PROMOTION
SCOPE: NayaPOWER / NayaNET

## Purpose

Generalize the verified Smart Note → intelligence_commit → Intelligent Block → index → checkpoint → retrieval rung without creating a second intelligence store, event model, authority system, Hub, or parallel persistence path.

The contract defines the common adapter boundary for meaningful Naya outputs. It does not claim that every existing surface is already promotion-capable or production-proven.

## Canonical architecture

SOURCE / OUTPUT
→ MEANINGFUL-OUTPUT ADAPTER
→ CANONICAL INTELLIGENT EVENT
→ EXISTING intelligence_commit / compound-intelligence boundary
→ INTELLIGENT BLOCK
→ VALIDATION
→ INTEGRATION / INDEX
→ CHECKPOINT
→ RETRIEVAL
→ APPLICABILITY
→ AUTHORIZATION
→ ACTION
→ OUTCOME
→ LEARNING
→ CORE INTELLIGENCE UPDATE

Historical events remain the temporal truth. Intelligent Blocks represent current understood meaning. The Hub remains a projection/action surface.

## Canonical adapter contract

Every adapter that claims promotion readiness MUST normalize a meaningful output into this conceptual shape:

- output_id — stable source/output identity
- output_class — controlled class name
- project_id — canonical project identity
- owner_scope — owner/privacy boundary
- source_ref — exact source identity/path/runtime reference where applicable
- occurred_at — when the meaningful output occurred
- recorded_at — when the canonical event was recorded
- title — human-readable meaning
- content — durable semantic payload
- meaning — concise reusable understanding
- evidence_refs — evidence supporting the claim
- provenance — origin + transformation lineage
- value_context — benefit/usefulness/relevance/consequence and uncertainty where known
- applicable_scope — where the understanding may safely be reused
- authority_ref — authority/consent reference when consequential
- idempotency_key — replay identity where the source operation supports replay
- desired_understanding_state — CAPTURED / CONTEXTUALIZED / INTERPRETED / VERIFIED / DISTILLED / APPLIED / LEARNED
- success_condition — exact condition required for the claimed promotion
- unknowns — material unresolved uncertainty
- next_use — intended future retrieval/use, when known

The adapter MUST NOT invent evidence, authority, outcome, learning, or verification state.

## Promotion rules

1. Meaningful does not mean merely emitted. The output must have a plausible human-value reason to preserve.
2. Promotion MUST use the existing canonical event/history substrate.
3. Promotion MUST preserve source identity and provenance.
4. Promotion MUST be owner/privacy scoped before persistence.
5. Promotion MUST be idempotent where the source operation can replay.
6. Promotion MUST distinguish event capture from block understanding.
7. A Block may be created only from a meaningful event/source bundle and must preserve source-event lineage.
8. Validation, integration, checkpoint, retrieval, applicability, authorization, action, outcome, and learning remain separately provable boundaries.
9. Projection surfaces such as Feed, Today, Reports, Library, Play, Activity, and Smart Ledger are representations of canonical state; they are not alternate intelligence authorities.
10. Share/publication, communication, relationship, and other consequential outputs must retain their own authority/consent boundary; being meaningful does not authorize broader disclosure or action.
11. A failure at one adapter must not trigger a parallel persistence implementation.
12. Universal promotion is NOT proven by one adapter or one output class.

## Evidence classification

Each output class is classified independently:

- DOCUMENTED — contract/source exists.
- IMPLEMENTED — adapter/source path exists.
- TESTED — runtime execution observed.
- VERIFIED — observed result maps directly to the class acceptance criterion.
- PRODUCTION_PROVEN — verified at the declared production scope with appropriate regression/security/privacy checks.
- UNKNOWN — insufficient evidence.
- BLOCKED — required authority/capability is unavailable.
- CONFLICTED — authoritative sources disagree.

## Evidence-backed output inventory — current main

Source of inventory:
- NAYANET/HUB/src/app/routes.ts
- NAYANET/HUB/src/app/*.Surface.tsx
- NAYANET/HUB/public/assistant-runtime.js
- .naya/project-intelligence/INTELLIGENT-EVENT-V1.md
- .naya/project-intelligence/INTELLIGENT-BLOCK-V1.md
- P0-04 proof run 35913487739

### A. Capture / understanding outputs

| Output class | Existing surface/runtime | Canonical path | Current evidence |
|---|---|---|---|
| Smart Note / captured insight | SmartNoteSurface → captureSmartNote | v7-smart-note-canonical; bounded P0-04 also proves intelligence_commit promotion | VERIFIED at bounded owner/runtime scope |
| Direct cognitive event / Naya record | NayaAssistantRuntime.record; NayaNetCognition.recordPersistent | nayanet_record_cognition_event | IMPLEMENTED; not universal promotion-proven |
| Smart Feed action / interaction | Smart Feed + persistSmartFeedAction | nayanet cognitive record / naya-smart-feed | IMPLEMENTED; promotion-to-Block not universally proven |
| Learning evidence | recordLearningEvidence / learning runtime | learning_evidence + canonical learning functions | IMPLEMENTED; outcome/behavior loop is bounded |

### B. Consequential intelligence outputs

| Output class | Existing surface/runtime | Canonical path | Current evidence |
|---|---|---|---|
| Smart Share publication | SmartShareSurface → publishSmartFeed | naya-smart-feed + authority grant | PRODUCTION_PROVEN for governed Smart Share, but publication ≠ new Block |
| Smart Mail communication | SmartMailSurface → sendSmartMail / verifySmartMail | nayanet-smart-mail + authority grant + receipts | PRODUCTION_PROVEN at bounded relationship/security scope; universal output promotion not proven |
| Smart Space creation | SmartSpacesSurface → createSpace | canonical relationship/space runtime | IMPLEMENTED / bounded runtime proofs exist |
| Connection creation/revocation | ConnectionsSurface / canonical connection runtime | relationship RPC/runtime | IMPLEMENTED / bounded runtime proofs exist |
| Smart List creation/membership | SmartListsSurface | canonical list RPC/runtime | IMPLEMENTED / bounded runtime proofs exist |
| Dream replay / learning application | DreamSurface / runtime dreamReplay/applyLearning | naya-dream-replay / naya-learning-apply | IMPLEMENTED / bounded learning proofs exist |
| Naya Play playback | NayaPlaySurface | canonical event retrieval/playback | VERIFIED as bounded playback surface; playback is projection, not a new intelligence authority |

### C. Canonical projections / derived outputs

| Output class | Surface | Canonical source | Role |
|---|---|---|---|
| Personal Intelligence Feed | Feed / SmartFeedBoard | canonical cognition/intelligence index | Projection of owner-scoped intelligence |
| Collective Intelligence Feed | Collective surface | consented shared canonical intelligence | Projection; consent boundary remains authoritative |
| Activity | Activity feed | canonical meaningful events/receipts | Accountability/projection, not intelligence authority |
| Intelligence Today | Today | canonical events/intelligence | Human-facing time projection |
| Reports | ReportsSurface | nayanet_cognition_events | Derived time-horizon projection; no synthetic source records |
| Intelligence Library | Library | canonical intelligence/index | Retrieval/projection |
| Smart Ledger | Ledger | receipts/evidence lineage | Accountability/lineage projection, not intelligence |
| Settings / Identity | Settings/identity surfaces | runtime/session/governance | Control surface, not intelligence |

## Common ingress finding

The inventory shows that NayaNET already has multiple specialized front doors, but they do not all converge at the same semantic promotion boundary.

The strongest existing common primitives are:

1. authenticated NayaAssistantRuntime;
2. canonical cognition event recording;
3. nayanet-compound-intelligence / action:"intelligence_commit" for bounded capture→Block promotion;
4. nayanet_intelligent_blocks;
5. nayanet_intelligence_index;
6. checkpoint events;
7. receipts/evidence;
8. authorized retrieval.

Therefore the P0 target is an adapter normalization layer above these existing primitives, not a new persistence layer.

## First representative class

The first representative class is:

**Smart Note / meaningful captured insight.**

Reason:
- it already has a real human-facing source surface;
- it has an authenticated owner boundary;
- it has canonical event identity;
- P0-04 has directly verified event → provenance/validation → index → learning → checkpoint → Intelligent Block → fresh retrieval;
- it provides a concrete reference contract for other output classes.

This remains bounded proof until the same contract is exercised by additional output classes.

## Acceptance for universal promotion

Universal promotion is proven only when representative output classes from capture, interaction, learning, communication, relationship, and consequential action surfaces can each:

1. normalize through this contract;
2. produce a canonical meaningful event;
3. preserve provenance/evidence/owner scope;
4. promote to or deliberately decline Block creation with an explicit semantic reason;
5. integrate/checkpoint when applicable;
6. retrieve fresh;
7. preserve authority/consent boundaries;
8. record outcome/learning where the output claims those states;
9. leave one durable lineage;
10. demonstrate that the next Naya can understand the resulting state without conversational reconstruction.

## Explicit non-claims

This contract does NOT claim:

- arbitrary ChatGPT conversation capture;
- that every UI action deserves an Intelligent Block;
- that every projection is itself intelligence;
- that Smart Share/Mail/relationship operations should create duplicate Blocks automatically;
- universal Core Intelligence reconciliation;
- universal cold applicability or behavior change;
- universal collective promotion;
- model/provider portability;
- production parity across every Hub surface.

## Next proof boundary

Use this contract to route one additional representative output class through the canonical promotion decision:

**Direct Naya meaningful output → adapter normalization → intelligence_commit → Block/index/checkpoint/retrieval**

Do not redesign the canonical persistence substrate.

## Source-of-truth rule

This document is a working P0 contract and inventory. Runtime evidence and the canonical control plane remain authoritative over its claims. Update it when fresh proof changes class status.

