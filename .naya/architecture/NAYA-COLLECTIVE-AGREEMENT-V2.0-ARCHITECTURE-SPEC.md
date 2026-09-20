# 🔱 NAYA COLLECTIVE AGREEMENT v2.0 — ARCHITECTURE SPECIFICATION

**Status:** ARCHITECTURE BASELINE / IMPLEMENTATION SPECIFICATION
**Constitution baseline:** `.naya/codex/NAYA-COLLECTIVE-AGREEMENT-V2.0.md`
**Constitution blob SHA:** `d797704d3f9bd58eb5b814ce67fcaed9a1dcc4bd`
**Repository:** `SoulSchoolAcademy/NayaPOWER`
**Governance branch:** `main`
**Baseline commit:** `bc317a25f7d845c036ed09e532a4ab96366ccb37`
**Rule:** This document translates v2.0 into architecture and runtime controls. It does not amend, reinterpret, or rewrite the Constitution.

---

# 0. ARCHITECTURAL CONTRACT

The v2.0 Collective Agreement is the normative behavioral source. Architecture exists to make its commitments executable, observable, testable, recoverable, and resistant to self-assertion.

The implementation principle is:

> **Do not solve a governance weakness by silently changing the Constitution. Build the mechanism that makes the existing requirement operational.**

The architecture therefore has five layers:

1. **CONSTITUTION** — normative rules and authority.
2. **CONTROL PLANE** — live runtime state, authorization, risk, locks, gates, and audit.
3. **EVIDENCE PLANE** — immutable/append-only evidence and provenance.
4. **KNOWLEDGE PLANE** — canonical runtime briefing, mission state, Smart Notes, project state, and indexed context.
5. **EXECUTION PLANE** — repositories, applications, deployments, tools, agents, tests, and human-facing systems.

The control plane governs execution; the evidence plane proves what happened; the knowledge plane carries what the next Naya needs; the constitution defines what must be true.

---

# 1. VERIFIED SOURCE OF TRUTH

## 1.1 Constitutional baseline

The exact v2.0 text supplied by the governing human has been stored verbatim at:

`.naya/codex/NAYA-COLLECTIVE-AGREEMENT-V2.0.md`

GitHub reports blob SHA:

`d797704d3f9bd58eb5b814ce67fcaed9a1dcc4bd`

The establishing commit is:

`bc317a25f7d845c036ed09e532a4ab96366ccb37`

No semantic edits are permitted in this architecture phase.

## 1.2 Current runtime authority state

The currently existing canonical runtime constitution remains:

`.naya/codex/11-RUNTIME-CONSTITUTION.md`

Version: **V1.0**

Blob SHA observed from GitHub:

`06516033b7dd174560eac040786cf4f346657c70`

The canonical Context Boot Protocol currently instructs Naya to read that V1.0 constitution and the Runtime Completeness Laws. Therefore the repository now contains a v2.0 constitutional baseline while the existing boot path has not yet been migrated to v2.0.

This is intentionally preserved during architecture work.

**State:** V2.0 SOURCE LOCKED; V2.0 RUNTIME ACTIVATION NOT YET CLAIMED.

## 1.3 Current runtime state

The canonical Runtime Briefing currently establishes:

- canonical repository: `SoulSchoolAcademy/NayaPOWER`;
- canonical governance branch: `main`;
- MAXIS application repository: `SoulSchoolAcademy/Maxis`;
- MAXIS deployment project: Vercel `maxis`;
- NayaPOWER as governance repository, not MAXIS deployment source;
- current objective: complete and prove the next coherent MAXIS milestone;
- current continuity gate: fresh current-head NayaPOWER CI/boot evidence is required;
- current MAXESS browser gate: latest recorded gate is RED and needs a fresh green rerun;
- production parity: not yet proven for the current intended MAXIS source SHA;
- Naya Hub Phase 1 runtime: unproven unless superseded by current evidence.

The briefing explicitly requires the exact eleven orientation fields:

**WHERE → WHY → BUILDING → PROTECTED → BLOCKED → VERIFIED → UNKNOWN → THIS WEEK → NEXT ACTION → PROOF → LAST LEARNING**

The canonical cold-start gate requires the briefing to be read before substantive execution and treats omission or material contradiction as RED.

---

# 2. PRIME RUNTIME MODEL

The runtime is modeled as a state machine rather than a prompt.

```text
BOOT
  ↓
CONTEXT RESTORED
  ↓
MISSION RESOLVED
  ↓
AUTHORITY RESOLVED
  ↓
RISK / REVERSIBILITY CLASSIFIED
  ↓
ACCESS VERIFIED
  ↓
PLAN AUTHORIZED
  ↓
EXECUTION
  ↓
OBSERVATION
  ↓
EVIDENCE CAPTURE
  ↓
VERIFICATION
  ↓
QUALITY GATE
  ↓
HUMAN-VALUE GATE
  ↓
HANDOFF
  ↓
LEARNING / STATE UPDATE
```

A runtime may not promote itself to a higher completion state merely by changing a label.

Minimum completion ladder:

`DOCUMENTED → ACTIVATED → CONTEXT ESTABLISHED → IMPLEMENTED → TESTED → INSPECTED → VERIFIED → LIVE VERIFIED → HUMAN-JOURNEY VERIFIED`

Failure/exception states remain first-class:

`UNKNOWN · BLOCKED · FAILED · PARTIAL · UNTESTED · ROLLBACK_REQUIRED · REJECTED · AUTHORIZED_DEVIATION · SUPERSEDED · CONFLICTED · STALE`

---

# 3. CONTROL-PLANE COMPONENTS

## 3.1 Identity Resolver

**Purpose:** establish which Naya runtime is operating and which environment it is operating within.

Inputs:
- session identity;
- repository;
- branch;
- task context;
- available tools;
- active governance version.

Outputs:
- `naya_identity`;
- `environment_id`;
- `session_id`;
- `capability_profile`;
- `governance_baseline`.

Rule: technical model identity remains distinct from operational Naya identity.

## 3.2 Authority Resolver

Resolves instructions using two separate dimensions:

**Conduct authority:** platform/safety → Constitution → protected baseline/system governance → task protocols → optimization.

**Reality authority:** current verified source → verified tool observation → current repository state → user-provided information → memory → inference.

The resolver must never infer authority merely from retrieval.

## 3.3 Mission / Intent Resolver

Stores:

- stated request;
- intended outcome;
- why it matters;
- success criteria;
- constraints;
- protected elements;
- dependencies;
- unresolved ambiguity.

If materially different interpretations exist, the state becomes `INTENT_CONFLICTED` until resolved or a low-risk declared assumption is explicitly accepted.

## 3.4 Risk / Consequence Classifier

Architecture must classify an action before execution.

Minimum categories:

- **L0 — informational/reversible:** explanation, analysis, drafting, local reasoning.
- **L1 — bounded reversible execution:** edits/tests/preparation with recoverable effects.
- **L2 — consequential controlled execution:** user-facing changes, shared-state writes, deployment preparation, data transformations, or changes with material downstream effect.
- **L3 — high-consequence execution:** irreversible deletion, financial/legal commitments, security-sensitive changes, production release, credential/permission changes, or equivalent high-impact action.

Classification is based on consequence, not on how technically difficult the task is.

The classifier is a control-plane mechanism; it does not alter the Constitution's language.

## 3.5 Authorization Gate

Every consequential action gets an authorization record containing:

- actor;
- role;
- requested action;
- target;
- risk level;
- reversibility;
- evidence available before action;
- authorization source;
- authorization timestamp;
- expiration/scope;
- resulting action receipt.

The gate must distinguish `RECOMMENDED`, `AUTHORIZED`, and `EXECUTED`.

## 3.6 Access Resolver

For every consequential operation record separately:

`CAPABILITY → TOOL → SESSION ACCESS → RESOURCE ACCESS → PERMISSION → ACTION → OBSERVATION`

No one of these states implies the next.

## 3.7 State Coordinator

Maintains the authoritative current runtime state and prevents incompatible concurrent writes.

Core states:
- mission;
- plan;
- current action;
- active lock;
- observations;
- evidence;
- verification;
- blockers;
- unknowns;
- protected surfaces;
- next action;
- learning.

## 3.8 Concurrency Coordinator

Required because Team Naya can operate concurrently.

Mechanisms:

- per-resource lease/lock;
- optimistic version number on shared state;
- compare-and-swap on writes;
- immutable evidence events;
- conflict detection;
- deterministic conflict status;
- human escalation for unresolved material conflicts.

Two Nayas may read concurrently. Material writes to the same canonical state require a valid lease or conflict-safe transaction.

A stale writer cannot silently overwrite newer state.

## 3.9 Evidence Coordinator

Captures receipts as immutable evidence records rather than narrative claims.

Evidence record:

```yaml
id: evidence_<uuid>
timestamp: <iso8601>
actor: <naya/session/human>
action: <action>
target: <resource>
source: <tool/repository/runtime>
observed_result: <result>
artifact_ref: <canonical-ref|null>
commit_sha: <sha|null>
deployment_id: <id|null>
runtime_url: <url|null>
verification_scope: <scope>
verification_status: <state>
parent_evidence: [<id>]
```

The narrative response can point to this record. It is not the record itself.

## 3.10 Quality Gate

The quality gate consumes a scorecard and evidence set.

Important design decision:

> **The v2.0 numeric thresholds remain constitutional; the architecture must provide a measurement instrument rather than invent a new constitutional threshold.**

The scorecard engine therefore stores dimensions, weights, evidence, points lost, impact, correction, and retest results. The exact scoring rubric is an implementation artifact to be finalized and validated before being treated as authoritative.

Until the rubric exists, a decimal score must not be represented as objectively measured precision.

## 3.11 Handoff Generator

Produces a successor packet from canonical state, not from the model's memory.

Required v2.0 handoff fields:

- CURRENT STATE
- MISSION / WHY
- ACCOMPLISHED
- PROTECTED
- VERIFIED
- FAILED
- UNKNOWN
- BLOCKED
- SCORECARD
- PROOF / RECEIPTS
- CURRENT HUMAN-VALUE BOTTLENECK
- SINGLE NEXT ACTION
- READY-TO-RUN EXECUTION
- LAST LEARNING

The packet is versioned and linked to the evidence records that support it.

---

# 4. KNOWLEDGE-PLANE ARCHITECTURE

## 4.1 Canonical Runtime Briefing

The existing `.naya/memory/NAYAPOWER-RUNTIME-BRIEFING.md` remains the first cold-start orientation artifact.

It is context, not proof.

Current verified repository/runtime evidence outranks stale briefing content.

The architecture must enforce:

```text
READ BRIEFING
→ RESOLVE CURRENT HEAD
→ COMPARE
→ RECONCILE IF CONTRADICTED
→ ONLY THEN SUBSTANTIVE EXECUTION
```

## 4.2 Mission State

Mission State is the compact live representation of:

- current mission;
- objective;
- success criteria;
- protected baseline;
- current bottleneck;
- active work;
- next action;
- proof requirement;
- latest learning.

Mission State is mutable operational state and therefore requires versioning and evidence linkage.

## 4.3 Smart Notes

v2.0 requires durable intelligence but does not define a storage schema. Architecture therefore provides one without altering the Constitution.

Canonical Smart Note schema:

```yaml
id: note_<uuid>
created_at: <iso8601>
updated_at: <iso8601>
author: <actor>
type: insight|mistake|breakthrough|decision|idea|lesson|question|goal|win|opportunity|correction|architectural_discovery|process_improvement
status: active|superseded|conflicted|archived
importance: 1-5
scope: global|system|project|task
subject: <canonical subject>
content: <human-readable note>
source_refs: [<evidence-or-artifact-ref>]
related_notes: [<note-id>]
confidence_state: verified|observed|inferred|assumed|unknown|conflicted
valid_from: <iso8601>
valid_until: <iso8601|null>
supersedes: <note-id|null>
conflict_group: <id|null>
```

### Smart Note lifecycle

`CAPTURE → VALIDATE → DEDUPLICATE → LINK → PUBLISH → REUSE → SUPERSEDE/ARCHIVE`

Deduplication should use canonical subject + semantic similarity + source overlap. Exact duplicates are merged; materially different claims are retained as separate notes unless evidence proves one supersedes the other.

Conflicting notes are never silently merged. They enter `CONFLICTED`, retain provenance, and require resolution by stronger evidence or authorized human decision.

Retention should be relevance-based rather than time-only. High-importance canonical lessons remain active; obsolete operational notes are superseded/archived rather than silently deleted.

## 4.4 Retrieval Index

Index fields:

- canonical name;
- type;
- scope;
- status;
- authority;
- timestamp;
- currentness;
- source;
- dependencies;
- task route;
- tags.

Retrieval must rank authoritative/current material ahead of historical memory and untrusted external content.

---

# 5. EVIDENCE-PLANE ARCHITECTURE

## 5.1 Claim Provenance

Every consequential claim maps to:

```text
CLAIM
  ↓
SOURCE / TOOL
  ↓
OBSERVED RESULT
  ↓
INTERPRETATION
  ↓
SUCCESS CRITERION
  ↓
EVIDENCE TIER
  ↓
CLAIM STATUS
```

The architecture must support one-to-many source evidence and many-to-one claim aggregation.

## 5.2 Evidence tiers

Implementation-level tiers:

- **T0 — assertion only:** no evidence; never sufficient for verified consequential claims.
- **T1 — static observation:** source/file inspection.
- **T2 — automated execution:** test/build/tool result.
- **T3 — runtime observation:** actual running environment.
- **T4 — production-parity/live evidence:** intended deployed environment verified.
- **T5 — human journey evidence:** fresh human completed the intended outcome.

A higher tier does not erase lower-tier provenance; it extends it.

## 5.3 Receipt integrity

Every receipt must be either:

- generated directly by the tool/action system;
- fetched from a canonical source;
- or explicitly marked unverified.

A model-generated SHA, URL, deployment ID, database ID, or permission claim is not evidence merely because it has plausible syntax.

---

# 6. HUMAN AUTHORITY MODEL

v2.0 uses the term "governing human". The architecture must resolve that role without rewriting the Constitution.

Identity model:

```text
HUMAN
├── GOVERNING / OPERATOR
│   ├── authorize consequential exceptions
│   ├── resolve governance conflicts
│   ├── approve releases
│   └── authorize constitutional amendment workflow
│
└── END USER / LEARNER
    ├── receive service and dignity protections
    ├── express intent/preferences
    └── cannot silently grant operator-level governance authority
```

The architecture must not infer operator status merely because a person typed a request.

Role assignment must be explicit and auditable.

If operator identity is unavailable for an action requiring it, the runtime enters `AUTHORIZATION_REQUIRED` rather than guessing.

---

# 7. CHILD / VULNERABLE-USER HANDLING

The architecture must support a safety profile for minors and other vulnerable users where the product context requires it.

This is an implementation control, not a constitutional amendment.

Minimum runtime behavior:

- identify when a product/workflow is intended for or may involve minors;
- apply the stricter applicable safety policy;
- prevent operator-style authority from being inferred from end-user interaction;
- log safety-relevant decisions;
- route safety conflicts to higher-priority platform/safety controls;
- never use pedagogical convenience to override safety.

No age-sensitive data should be inferred or persisted beyond what the applicable product and privacy design legitimately requires.

---

# 8. INSTRUCTION TRUST BOUNDARY

Every input is classified before it can influence execution authority:

`CONSTITUTIONAL → SYSTEM GOVERNANCE → PROTECTED BASELINE → AUTHORIZED HUMAN → TASK → REFERENCE MATERIAL → EXTERNAL CONTENT → UNTRUSTED DATA`

External content is data, not authority.

Quoted text is not automatically an instruction to Naya.

Retrieved documents can inform a decision but cannot silently elevate themselves into governance.

---

# 9. CONCURRENCY / MULTI-NAYA PROTOCOL

## 9.1 Shared-state write protocol

```text
READ VERSION N
→ ACQUIRE RESOURCE LEASE
→ RECHECK VERSION N
→ APPLY MINIMAL CHANGE
→ WRITE VERSION N+1
→ EMIT EVIDENCE EVENT
→ RELEASE LEASE
```

If version changed between read and write:

`ABORT WRITE → RELOAD → DIFF → RECONCILE`

## 9.2 Conflicting verification

Two Nayas cannot both make a shared claim `VERIFIED` from incompatible evidence.

Conflict state:

`CONFLICTED → PRESERVE BOTH EVIDENCE SETS → IDENTIFY AUTHORITY → RESOLVE → RECORD RESOLUTION`

## 9.3 Work partitioning

Each active Naya receives:

- mission slice;
- owned resources;
- read/write scope;
- dependency list;
- expected outputs;
- proof requirements;
- expiration/lease time.

No Naya owns the whole system merely because it is currently active.

---

# 10. COLD-START / FAILURE-OF-CONTEXT PROTOCOL

The v2.0 cold-start sequence is implemented as a gated state machine.

### Normal path

`READ CONSTITUTION → READ RUNTIME BRIEFING → RESOLVE LIVE STATE → IDENTIFY MISSION → IDENTIFY PROTECTION → IDENTIFY VERIFIED/UNKNOWN/BLOCKED → SELECT ONE NEXT ACTION`

### Recovery path when context is unavailable

If canonical runtime state cannot be retrieved:

1. mark `CONTEXT_UNAVAILABLE`;
2. do not declare current state verified;
3. do not perform consequential writes;
4. identify what can safely be investigated;
5. restore the smallest authoritative context required;
6. escalate to the governing human if required authority remains unavailable.

This closes the cold-start hole without changing the Constitution.

---

# 11. FAILURE AND RECOVERY ENGINE

Every failed action produces a structured event:

```yaml
failure_id: fail_<uuid>
state: FAILED|PARTIAL|BLOCKED|UNKNOWN|ROLLBACK_REQUIRED
first_evidence: <evidence-id>
root_cause: <identified-or-unknown>
protected_state: <ref>
repair_plan: <ref>
retest_plan: <ref>
result: <ref>
learning_ref: <note-id|null>
```

Recovery sequence:

`CLASSIFY → CONTAIN → PRESERVE → ROOT CAUSE → REPAIR → RETEST → VERIFY → LEARN`

A failed attempt remains in history even after a successful repair. The system must never erase failure evidence merely because the final result is good.

---

# 12. QUALITY / 10.0 ARCHITECTURE

v2.0 establishes:

- target 10.0;
- AAA at 9.5+;
- conditional 9.0–9.49;
- below 9.0 as failure absent explicit exception authority.

The architecture must make those values measurable rather than rhetorical.

## Proposed scorecard instrument

Dimensions should be configured per work type, but the engine must support at least:

1. human outcome / usefulness;
2. correctness / truth;
3. functional completeness;
4. clarity / information architecture;
5. usability / interaction quality;
6. accessibility where applicable;
7. performance / reliability;
8. architecture / maintainability;
9. verification strength;
10. continuity / handoff quality.

Each dimension requires:

- score;
- weight;
- evidence;
- points lost;
- materiality;
- defect/root cause;
- correction;
- retest result.

Aggregation:

`weighted_score = Σ(dimension_score × dimension_weight) / Σ(weights)`

However, this formula is an architecture proposal, not a constitutional amendment. It becomes authoritative only after it is formally approved as the implementation rubric.

Hard-stop defects may block release independently of the numeric aggregate.

---

# 13. RELEASE GATE

A consequential release requires the following machine-checkable states:

```text
AUTHORITY_RESOLVED
AND
PROTECTION_ESTABLISHED
AND
RISK_CLASSIFIED
AND
ACCESS_CONFIRMED
AND
IMPLEMENTED
AND
TESTED
AND
INSPECTED
AND
SCORED
AND
MATERIAL_DEFECTS_RESOLVED
AND
RETESTED
AND
VERIFIED
AND
REQUIRED_INDEPENDENT_REVIEW_COMPLETE
AND
REQUIRED_HUMAN_AUTHORIZATION_PRESENT
→ RELEASE ELIGIBLE
```

The architecture does not weaken v2.0's conditional language; it turns the applicable obligations into explicit gate predicates.

---

# 14. INDEPENDENT REVIEW

For consequential releases, independent review should be an actual separate actor/process rather than the same Naya repeating its own conclusion.

Minimum independence controls:

- different session identity;
- isolated review context where practical;
- read-only access to target evidence;
- explicit adversarial review objective;
- independent findings record;
- no ability for the reviewed Naya to rewrite the review record.

The architecture can support automated and human reviewers as well as another Naya.

Where independence cannot be established, the result is not represented as independently reviewed.

---

# 15. DEATH TEST AS A REAL TEST

v2.0's Death Test is implemented in two layers.

### Layer A — static handoff validator

Checks that all required handoff fields exist, are current, and point to canonical state/evidence.

### Layer B — cold-successor acceptance test

A fresh Naya/session is given only the canonical entry context and asked to recover:

- truth;
- protection;
- accomplishment;
- failures;
- unknowns;
- proof;
- current bottleneck;
- next action.

The test passes only if the successor can identify the intended next action without relying on the predecessor's hidden conversational context.

This converts a metaphorical thought experiment into an executable continuity test without changing its constitutional wording.

---

# 16. NO-SURPRISE / HUMAN-VALUE GATE

Before exposing consequential human-facing work, the control plane must ask:

- Is the intended human outcome explicit?
- Is the main journey executable?
- Are material edge states covered?
- Has actual runtime behavior been observed where required?
- Are accessibility requirements covered where applicable?
- Are known defects disclosed?
- Does the human need to understand internal infrastructure to receive the intended value?

If internal complexity has leaked into the user journey, the human-value gate fails even if engineering tests pass.

---

# 17. GOVERNANCE VERSIONING

The architecture separates three concepts:

1. **CONSTITUTION SOURCE** — exact normative text.
2. **RUNTIME ACTIVATION** — which constitutional version the boot path currently enforces.
3. **IMPLEMENTATION SPECIFICATION** — architecture that operationalizes the activated/baselined rules.

A constitutional activation transition must be explicit and auditable.

Required transition record:

```yaml
from_version: <version>
to_version: <version>
source_sha: <sha>
old_runtime_ref: <path>
new_runtime_ref: <path>
compatibility_review: <ref>
implementation_migration: <ref>
approval: <human-authorization-ref>
activation_commit: <sha>
rollback_plan: <ref>
```

No architecture commit may silently cause a constitutional version transition.

---

# 18. MACHINE-READABLE CONTRACT

The implementation should expose a machine-readable control contract separate from the human-readable Constitution.

Illustrative shape:

```yaml
naya_runtime:
  constitution:
    source: .naya/codex/NAYA-COLLECTIVE-AGREEMENT-V2.0.md
    version: "2.0"
    sha256: <content-hash>
    activation_state: source_locked_not_runtime_activated

  boot:
    runtime_briefing: required
    required_fields:
      - WHERE
      - WHY
      - BUILDING
      - PROTECTED
      - BLOCKED
      - VERIFIED
      - UNKNOWN
      - THIS_WEEK
      - NEXT_ACTION
      - PROOF
      - LAST_LEARNING

  authority:
    conduct:
      - platform_safety
      - constitution
      - system_governance
      - authorized_human
      - task
      - recommendation
    reality:
      - verified_source
      - verified_observation
      - repository_state
      - user_information
      - memory
      - inference

  states:
    completion:
      - documented
      - activated
      - context_established
      - implemented
      - tested
      - inspected
      - verified
      - live_verified
      - human_journey_verified
    failure:
      - unknown
      - blocked
      - failed
      - partial
      - untested
      - rollback_required
      - rejected
      - authorized_deviation
      - superseded
      - conflicted
      - stale

  controls:
    authorization_required_for: [consequential]
    evidence_required_for: [consequential_claim]
    concurrent_shared_writes: lease_plus_version_check
    fabricated_receipts: forbidden
    silent_governance_override: forbidden
    context_failure: no_consequential_write
```

This contract is implementation data, not a second constitution. It must be generated/validated against the constitutional source so that drift is detectable.

---

# 19. OBSERVABILITY / AUDIT LOG

The system must persist an audit trail for consequential runtime events.

Event types:

- `BOOT`
- `CONTEXT_READ`
- `AUTHORITY_RESOLVED`
- `MISSION_RESOLVED`
- `RISK_CLASSIFIED`
- `AUTHORIZATION_GRANTED`
- `ACTION_STARTED`
- `ACTION_COMPLETED`
- `OBSERVATION_CAPTURED`
- `EVIDENCE_CAPTURED`
- `VERIFICATION_COMPLETED`
- `SCORECARD_CREATED`
- `DEFECT_FOUND`
- `REPAIR_COMPLETED`
- `RETEST_COMPLETED`
- `REVIEW_COMPLETED`
- `RELEASE_AUTHORIZED`
- `RELEASE_COMPLETED`
- `HANDOFF_CREATED`
- `STATE_CONFLICT`
- `GOVERNANCE_CONFLICT`
- `EXCEPTION_GRANTED`
- `LEARNING_CAPTURED`

Audit records are append-only. Corrections create new events; they do not rewrite historical evidence.

---

# 20. ARCHITECTURE / REPOSITORY LAYOUT

Recommended implementation layout:

```text
.naya/
├── codex/
│   ├── NAYA-COLLECTIVE-AGREEMENT-V2.0.md          # exact normative source
│   ├── 11-RUNTIME-CONSTITUTION.md                 # current legacy/runtime constitution
│   └── 12-RUNTIME-COMPLETENESS-LAWS.md            # current runtime extension
│
├── architecture/
│   └── NAYA-COLLECTIVE-AGREEMENT-V2.0-ARCHITECTURE-SPEC.md
│
├── control-plane/
│   ├── authority/
│   ├── authorization/
│   ├── risk/
│   ├── concurrency/
│   ├── state/
│   └── gates/
│
├── evidence/
│   ├── claims/
│   ├── receipts/
│   ├── reviews/
│   └── audit/
│
├── memory/
│   ├── NAYAPOWER-RUNTIME-BRIEFING.md
│   ├── MISSION-STATE.md
│   ├── SMART-NOTES/
│   └── INDEX.json
│
└── tests/
    ├── constitution-conformance/
    ├── cold-start/
    ├── authority/
    ├── evidence/
    ├── concurrency/
    ├── failure-recovery/
    ├── release-gates/
    └── human-journey/
```

This layout is architectural guidance, not permission to create all directories immediately. Apply smallest-sufficient-change.

---

# 21. CONFORMANCE TEST SUITE

The architecture is not complete until it can be tested.

## Constitution conformance

- exact v2.0 source hash is stable;
- machine-readable representation maps to the same source version;
- no hidden semantic edits;
- required constitutional concepts are represented in control predicates.

## Boot / continuity

- canonical Runtime Briefing is first read;
- missing briefing = RED;
- stale/contradicted briefing triggers reconciliation;
- context retrieval failure blocks consequential writes;
- cold successor can recover the current mission and next action.

## Truth / evidence

- fabricated receipt is rejected;
- unverified receipt is labeled unverified;
- deployment is not treated as runtime proof;
- runtime proof is not treated as human-journey proof;
- claim provenance is inspectable.

## Authority

- end-user cannot silently become governing human;
- unauthorized consequential action is blocked;
- governance conflict becomes explicit;
- recommendation is not recorded as authorization.

## Concurrency

- stale writer cannot overwrite newer state;
- concurrent evidence remains independently preserved;
- conflicting verification enters `CONFLICTED`;
- lease expiry is safe.

## Quality

- scorecard requires evidence;
- material defect creates repair/retest path;
- below-floor result blocks release absent explicit exception;
- independent review is distinguishable from self-review.

## Handoff

- all required state fields present;
- proof references resolve;
- single next action is executable;
- successor test can operate without hidden predecessor context.

---

# 22. IMPLEMENTATION ORDER

Do not build everything at once.

### Phase 0 — source lock
**DONE**

Exact v2.0 source is stored and verified.

### Phase 1 — architecture foundation

Build:
1. constitutional source registry;
2. runtime activation-state registry;
3. claim/evidence model;
4. state model;
5. authority/authorization model;
6. conformance test harness.

### Phase 2 — continuity controls

Build:
1. Runtime Briefing validator;
2. cold-start gate;
3. mission-state store;
4. handoff generator;
5. cold-successor test.

### Phase 3 — execution controls

Build:
1. risk/consequence classifier;
2. access resolver;
3. authorization gate;
4. failure/recovery engine;
5. concurrency coordinator.

### Phase 4 — quality controls

Build:
1. scorecard engine;
2. evidence-backed scoring;
3. independent review workflow;
4. release gate;
5. human-value gate.

### Phase 5 — intelligence continuity

Build:
1. Smart Note schema;
2. deduplication;
3. conflict lifecycle;
4. relevance ranking;
5. learning promotion.

### Phase 6 — constitutional activation

Only after the architecture is complete, tested, reviewed, and authorized:

1. complete v2.0 conformance mapping;
2. reconcile v1.0 runtime references;
3. update boot/activation references;
4. migrate machine-readable representation;
5. run full acceptance suite;
6. record explicit activation authorization;
7. activate v2.0;
8. verify cold start against the activated version.

This phase is intentionally outside the current architecture completion boundary.

---

# 23. CURRENT BLOCKERS

1. **V2.0 is source-locked but not yet the runtime-activated constitution.** The existing boot protocol still names the V1.0 runtime constitution.
2. **Fresh current-head NayaPOWER CI/boot evidence is still required.** The Runtime Briefing explicitly records this.
3. **Current MAXIS browser/runtime gate remains unproven/RED in the recorded state.**
4. **The v2.0 score thresholds lack a formally approved measurement rubric.** Architecture specifies the instrument shape but does not silently make the proposed formula constitutional.
5. **Governing-human identity/role enforcement is not yet demonstrated as a runtime control.**
6. **Concurrent multi-Naya state control is specified here but not yet proven implemented.**
7. **Smart Note lifecycle controls are specified here but not yet proven implemented.**

These are architecture/implementation states, not reasons to rewrite v2.0 during this phase.

---

# 24. ARCHITECTURAL ACCEPTANCE CRITERIA

Architecture is complete when all of the following are true:

- v2.0 exact source is immutable and addressable by canonical path + content hash;
- every v2.0 article/appendix has an identified runtime mechanism, test, or explicit human-only control;
- consequential actions have machine-checkable risk and authorization gates;
- consequential claims have provenance and evidence records;
- completion states cannot be silently promoted;
- cold-start failure has a safe degraded path;
- shared state has concurrency controls;
- Smart Notes have lifecycle and conflict handling;
- governing-human authority is explicit and auditable;
- independent review is a real separate control for required releases;
- quality scoring is evidence-backed;
- Death Test is executable, not merely rhetorical;
- handoff is generated from canonical state;
- audit records are durable;
- conformance tests exist for every control;
- constitutional activation remains a separate, explicit, authorized step.

---

# 25. THE ARCHITECTURAL PRINCIPLE

The central design requirement is:

> **The Constitution says what Naya must do. The architecture makes it difficult for Naya to merely say she did it.**

Therefore:

**RULE → STATE → GATE → ACTION → OBSERVATION → EVIDENCE → VERIFICATION → AUDIT → HANDOFF**

The desired end state is not a larger prompt.

It is a runtime in which:

- authority is explicit;
- reality is observable;
- actions leave receipts;
- unknowns remain unknown;
- failures remain visible;
- concurrent work cannot silently corrupt shared state;
- quality claims are measurable;
- successors can actually recover the system;
- and the human is protected from being the default integration test.

**END OF ARCHITECTURE SPECIFICATION v2.0 BASELINE**