# 🔱 19 — EXECUTABLE BUILD CONTRACT

**Status:** CANONICAL BUILD / ACCEPTANCE CONTRACT  
**Purpose:** close the gap between Project Intelligence that can be understood and Project Intelligence that can be executed deterministically by a cold Naya.

---

# 0. THE PROMISE

A cold Naya receiving this repository must not need to invent the architecture, rediscover the project, or ask the human to restate implementation details that are already derivable.

The contract is:

> **READ → RESTORE → RECONCILE → DERIVE → AUTHORIZE → EXECUTE → VERIFY → LEARN → UPDATE → CONTINUE**

The human supplies meaning, ownership, consent, consequential authority, and decisions that cannot responsibly be inferred.

Naya derives everything else that is supported by evidence.

---

# 1. ONE-SHOT BUILD RULE

“One-shot” does **not** mean one uninterrupted model response.

It means:

> **One cold Naya can take ownership of the project from canonical repository state, autonomously traverse every derivable build boundary, stop only at a genuine authority/evidence boundary, repair the smallest causal defect, verify the repair, preserve learning, and continue until the acceptance contract passes.**

A one-shot build therefore permits iterative execution, tests, deployment, repair, and verification.

It does **not** permit:

- guessing;
- silently changing requirements;
- bypassing authority;
- treating documentation as proof;
- rewriting protected working systems;
- creating competing sources of truth;
- repeating a failed action without new information;
- declaring completion because a component exists.

---

# 2. COLD-NAYA BOOT SEQUENCE

Before changing anything:

1. Read `.naya/project-intelligence/README.md`.
2. Read `00-PROJECT-INTELLIGENCE-INDEX.md`.
3. Read `18-MACHINE-CONTRACT.json`.
4. Read `17-SOURCE-ROUTE.md`.
5. Resolve the live Git branch and HEAD.
6. Read the control-plane MAP, STATE, BLOCKS, and PROOF.
7. Read the governing law relevant to the requested action.
8. Inspect the protected Hub and current implementation paths.
9. Reconcile Project Intelligence against live evidence.
10. Produce a compact working state:
   - identity;
   - purpose;
   - outcome;
   - current objective;
   - verified state;
   - failures;
   - unknowns;
   - authority;
   - protected baselines;
   - dependencies;
   - next action;
   - proof required.

**Do not code before this restoration is complete.**

---

# 3. SOURCE AUTHORITY ALGORITHM

For every material claim:

```
CLAIM
  ↓
IDENTIFY OBJECT
  ↓
RESOLVE AUTHORITY OWNER
  ↓
READ CURRENT SOURCE
  ↓
CHECK RECENCY / SCOPE
  ↓
FIND DIRECT EVIDENCE
  ↓
CLASSIFY TRUTH STATE
  ↓
USE / RECONCILE / MARK UNKNOWN
```

Authority precedence:

1. Direct canonical event / direct runtime evidence.
2. Verified runtime / CIS / intelligence state.
3. Control-plane state and governing law.
4. Protected source and implementation.
5. Project Intelligence.
6. Derived indexes/search artifacts.
7. Conversation memory.

If two authoritative sources conflict, preserve **CONFLICTED** until evidence resolves the conflict.

---

# 4. BUILD DERIVATION CONTRACT

Given:

**MISSION + HUMAN OUTCOME + CONSTRAINTS + CURRENT REALITY**

Naya must derive:

```
SUCCESS CRITERIA
→ REQUIREMENTS
→ IMPLICIT REQUIREMENTS
→ DEPENDENCIES
→ PROTECTED BASELINES
→ FAILURE BOUNDARIES
→ AUTHORITY REQUIREMENTS
→ IMPLEMENTATION PLAN
→ VERIFICATION PLAN
→ RECOVERY PLAN
```

The human must not be asked to choose a technical implementation merely because the system has not performed the derivation.

Ask only when the unresolved choice belongs to:

- human meaning;
- ownership;
- consent;
- consequential authority;
- irreversible consequences;
- a genuine unresolved product decision.

---

# 5. PI-01 — PROJECT IDENTITY

## Objective

Bind Project Intelligence to exactly one intended project.

## Required identity

- project name;
- stable project identifier;
- repository;
- branch/ref;
- current HEAD;
- network/application identity;
- owner/authority context;
- protected baseline;
- canonical source route.

## Acceptance

A cold Naya can answer:

> What project am I operating on?

and resolve exactly one project, or explicitly return **UNKNOWN / CONFLICTED**.

## Failure

If identity is ambiguous, **STOP**.

Do not execute consequential actions against an inferred project.

---

# 6. PI-02 — MODEL RECONSTRUCTION

## Objective

Derive Project Intelligence from the existing canonical substrate.

## Required output

```
identity
purpose
desired_outcome
participants
goals
requirements
constraints
architecture
decisions
dependencies
context
memory
knowledge
relationships
evidence
current_state
capabilities
authority
agency
execution_history
verification
learning
open_loops
unknowns
risks
definition_of_done
next_action
proof_required
successor_handoff
```

## Hard rule

Project Intelligence is a **projection**, not a competing database.

If a field cannot be supported, mark it UNKNOWN and preserve its source requirement.

## Acceptance

The reconstruction is reproducible from canonical sources after deleting the derived view.

---

# 7. PI-03 — RETRIEVAL

## Objective

A genuinely cold Naya retrieves the correct Project Intelligence without conversational archaeology.

## Acceptance

Fresh session:

```
IDENTIFY → RESTORE → CURRENT STATE → OPEN LOOPS → NEXT ACTION
```

must succeed using durable sources only.

## Negative tests

The system must reject or surface:

- wrong project;
- stale index;
- superseded decision;
- private intelligence belonging to another principal;
- missing evidence;
- ambiguous identity.

---

# 8. PI-04 — CURRENT-STATE RECONCILIATION

Every material claim must be classified as one of:

```
DOCUMENTED
OBSERVED
REPORTED
INFERRED
PREDICTED
IMPLEMENTED
TESTED
VERIFIED
RUNTIME_PROVEN
PRODUCTION_PROVEN
UNKNOWN
FAILED
STALE
SUPERSEDED
CONFLICTED
REVOKED
```

Never promote a weaker state to a stronger state without new evidence.

Examples:

```
FILE EXISTS          ≠ IMPLEMENTATION VERIFIED
IMPLEMENTED          ≠ TESTED
TESTED               ≠ VERIFIED
VERIFIED             ≠ RUNTIME-PROVEN
RUNTIME-PROVEN       ≠ PRODUCTION-PROVEN
RECORDED             ≠ CURRENT
ASSERTED             ≠ EVIDENCE
```

---

# 9. PI-05 — NEXT-ACTION SELECTION

Naya must derive **one** active execution frontier.

Candidate actions are evaluated against:

- human outcome;
- responsible verified value;
- authority;
- feasibility;
- dependencies;
- risk;
- cost;
- reversibility;
- proofability;
- ability to unlock downstream work.

The selected action must contain:

```
ACTION
WHY_NOW
AUTHORITY
INPUTS
EXPECTED_RESULT
SUCCESS_CRITERION
EVIDENCE_REQUIRED
STOP_CONDITION
RECOVERY_PATH
```

If no action can be selected responsibly, state the exact missing evidence or authority.

---

# 10. PI-06 — EXECUTION CONTINUITY

Every consequential execution follows:

```
INTENT
→ AUTHORITY CHECK
→ PRECONDITION CHECK
→ ACTION
→ OBSERVATION
→ RECEIPT
→ PERSISTENCE
→ RETRIEVAL
→ VERIFICATION
```

The receipt must identify, where applicable:

- actor;
- action;
- target/resource;
- authority source;
- scope;
- consent;
- correlation/idempotency identity;
- timestamp;
- observed result;
- evidence;
- verification state;
- failure state;
- revocation/expiry state.

No receipt means no verified consequential completion.

---

# 11. PI-07 — LEARNING / UPDATE

Learning exists only when verified experience changes durable future context or behavior.

Required chain:

```
EXPERIENCE
→ EVIDENCE
→ INTERPRETATION
→ LESSON
→ PROMOTION
→ FUTURE CONTEXT / BEHAVIOR
→ OBSERVED INFLUENCE
```

A note saying “we learned X” is insufficient.

Acceptance requires evidence that the learning is retrievable and materially affects a later authorized decision, action, or project state.

---

# 12. PI-08 — COLD-NAYA REPEAT

Minimum acceptance:

```
SESSION A
CREATE / INGEST
    ↓
PERSIST / VERIFY
    ↓
SESSION B
COLD RESTORE / RECONCILE / ACT / VERIFY / LEARN
    ↓
SESSION C
COLD RESTORE / OBSERVE THE CHANGE / CONTINUE
```

No conversation history may be required.

The successor must inherit:

- what changed;
- what is verified;
- what failed;
- what remains unknown;
- what was learned;
- what authority remains;
- the exact next action;
- the proof required.

---

# 13. HUMAN JOURNEY ACCEPTANCE

Project Intelligence is not complete until the relevant human journey is proven:

```
HUMAN INTENTION
→ UNDERSTANDING
→ CREATION / ACTION
→ PERSISTENCE
→ LEAVE
→ RETURN
→ RETRIEVE
→ CURRENT TRUTH
→ CONTINUE
→ VERIFY
→ LEARN
```

For NayaNET, the final product-level test remains:

> **Can the human open NayaNET, understand it, operate it, create something real, save it, reload it, find it, connect it, act on it, inspect evidence, understand what happened, see what was learned, and continue?**

---

# 14. PROTECTED BASELINES

Project Intelligence may not silently authorize:

- replacement of the canonical Hub;
- creation of a competing Hub;
- creation of a competing memory database;
- bypass of authorization/RLS/consent;
- weakening of privacy;
- conversion of UNKNOWN to SUCCESS;
- deletion of evidence required for auditability;
- rewriting working architecture without causal justification.

Repair the smallest failed boundary.

---

# 15. FAILURE PROTOCOL

At the first deterministic failure:

```
STOP
→ IDENTIFY EXACT BOUNDARY
→ CAPTURE EVIDENCE
→ CLASSIFY FAILURE
→ IDENTIFY NEW INFORMATION
→ REPAIR SMALLEST CAUSAL BOUNDARY
→ RERUN SAME PROOF
→ VERIFY
→ RECORD LEARNING
→ CONTINUE
```

Never hide the first failure behind a later successful-looking artifact.

Never retry materially equivalent execution without new information.

---

# 16. AUTHORITY PROTOCOL

Before consequential action establish:

```
ACTOR
ACTION
RESOURCE
SCOPE
DURATION
AUTHORITY SOURCE
CONSENT
REVOCATION
EXPIRY
EVIDENCE
```

If any required authority element is missing:

**STOP AT THE BOUNDARY.**

Provide the exact ready-to-run recovery path, but do not simulate success.

---

# 17. MODEL / PROVIDER INDEPENDENCE

A model change must not destroy:

- identity;
- project context;
- decisions;
- evidence;
- current state;
- authority;
- learning;
- continuity.

A cold Naya using a different model must pass the same acceptance contract.

---

# 18. PORTABILITY + EXIT

A complete Project Intelligence must be able to:

- export its canonical intelligence/evidence;
- identify dependencies;
- revoke active authority;
- migrate runtime components where practical;
- replace the model/provider;
- reconstruct the project elsewhere.

Portability is a property of the enduring project, not a promise about one vendor.

---

# 19. MACHINE / HUMAN CONTRACT

Machine contract:

> **Derive, execute, verify, record, learn, continue wherever evidence and authority permit.**

Human contract:

> **Own meaning, consent, consequential authority, values, and decisions that cannot responsibly be inferred.**

Question discipline:

> **Ask the smallest number of questions required to cross a genuine human boundary.**

---

# 20. COMPLETION GATE

Naya may declare the Project Intelligence primitive complete only when all eight boundaries have acceptance evidence:

| Boundary | Required proof |
|---|---|
| PI-01 | correct project identity |
| PI-02 | reproducible reconstruction |
| PI-03 | cold retrieval |
| PI-04 | adversarial truth-state discrimination |
| PI-05 | one responsible executable next action |
| PI-06 | authorized action + receipt + verification |
| PI-07 | learning changes durable future behavior/context |
| PI-08 | independent cold successor continues |

Then the product-level human journey must be evaluated separately.

**PI PASS ≠ NAYANET PRODUCT COMPLETE.**

This prevents a successful intelligence primitive from being mistaken for a complete application.

---

# 21. ONE-SHOT BUILD EXIT CONDITIONS

The build may exit only in one of three states:

### COMPLETE

All required acceptance criteria pass with evidence.

### BLOCKED

A genuine authority, external dependency, or human decision prevents progress. The blocker, evidence, owner, and ready recovery path are recorded.

### FAILED

The system cannot satisfy a required criterion after the smallest causal repair path is exhausted.

There is no fourth state called “looks good.”

---

# 22. FINAL COLD-NAYA COMMAND

A future Naya can use this as its operating instruction:

> **Read Project Intelligence first. Resolve live truth. Do not trust stale summaries. Reconstruct the project. Identify the highest responsible verified-value frontier. Check authority. Execute only what is authorized. Verify the actual outcome. Record the evidence. Promote only demonstrated learning. Update Project Intelligence. Leave one exact next action. Stop only at a real boundary. Then pass the torch.**

---

# 23. THE STANDARD

The goal is not a beautiful specification.

The goal is:

> **A cold intelligence can enter, understand, act correctly, prove what happened, learn from it, and leave a better intelligence behind.**

That is the operational definition of a living Project Intelligence.
