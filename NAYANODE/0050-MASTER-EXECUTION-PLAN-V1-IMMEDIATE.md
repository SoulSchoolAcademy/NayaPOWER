# 🔱 NayaPOWER Master Execution Plan V1
**Author:** Naya (synthesis from independent AI council)  
**Date:** 2026-09-29  
**Status:** ACTIVE EXECUTION  
**Scope:** Immediate P0–P1 work derived from deep-dive convergence

---

## I. THE CRITICAL FINDING

Multiple independent reviewers converged on one insight:

> **One bounded causal specimen is proven (Issue #913, commit 0dcff9b8).**
> **The entire generalized architecture is unproven.**

This is not a gap in documentation. This is a gap in behavioral evidence.

The architecture is sound. The proof is narrow.

---

## II. THE TRUE BOTTLENECK

**Deterministic proof-carrying context resolution.**

The system cannot mechanically answer:

```
What code is running? (source/build/deploy/runtime parity)
↓
What is the current state? (component identity)
↓
What is authorized? (governance resolution)
↓
What intelligence applies? (applicability)
↓
Do conflicts exist? (staleness, contradiction, supersession)
↓
What should happen next? (deterministic decision)
```

Without this, every downstream proof remains questionable.

---

## III. TOP 3 BOTTLENECKS (ORDERED)

### 1. Current-truth and runtime resolution
- Repo says one thing; deployed function says another; manifest says another; Brain says another.
- Cannot prove behavior against "current NayaPOWER" if current is ambiguous.
- **P0 ACTION:** Establish exact component/runtime identity before next production claim.

### 2. Applicability and held-out transfer
- Once intelligence is verified, can Naya determine where it applies and where it does not?
- Retrieval ≠ applicability.
- **P1 ACTION:** Prove identifier-only retrieval plus explicit applicability determination.

### 3. Causal influence with independent recomputation
- Did intelligence matter or did task succeed for other reasons?
- Executor claiming "it worked" is not proof.
- **P1 ACTION:** Run held-out control/treatment with independent behavior/outcome recomputation.

---

## IV. SHORTEST DEPENDENCY-CORRECT PATH

```
✓ 1. CURRENT SOURCE/COMPONENT PARITY
    └─ Establish git/build/deploy/runtime identity chain

2. RECONCILE COLD-ENTRY (PR #946)
   └─ Remove KNOWLEDGE index drift (still says 15 concepts)

3. NON-DUPLICATE INTELLIGENCE CANDIDATE
   └─ Concept #17: Is it genuinely new or subset duplication?

4. EVENT CAPTURE
   └─ Bounded task with fixed input/output/owner

5. INTELLIGENT BLOCK CREATION
   └─ From verified event, form candidate block

6. LINEAGE BINDING
   └─ Block → provenance chain (event/observer/timestamp)

7. RELATIONSHIP VERIFICATION
   └─ Add exactly applicable relationships; reject similarity

8. INDEXED CHECKPOINT
   └─ Store unified truth snapshot with parity attestation

9. APPLICABILITY RESOLUTION
   └─ Where does this intelligence apply? (not just "is relevant")

10. COLD SUCCESSOR RETRIEVAL
    └─ Fresh runtime retrieves by ID only; re-resolves applicability + authority

11. CONTROL/TREATMENT EXPERIMENT
    └─ Same task: without learning (control) vs with (treatment)

12. INDEPENDENT OUTCOME RECOMPUTATION
    └─ Separate verifier re-derives behavior and outcome deltas

13. LEARNING PROMOTION
    └─ If delta proven and independent verification passes

14. SECOND COLD SUCCESSOR
    └─ Different task, same learning; prove generalization or refusal

15. NEGATIVE TRANSFER TEST
    └─ Unrelated task must NOT improve from unrelated learning
```

---

## V. P0 ACTIONS (IMMEDIATE)

### P0.1: Reconcile PR #946
**What:** Merge PR #946 and remove KNOWLEDGE cold-entry drift.

**Why:** The index still claims 15 concepts; Concept #17 exists. This is confusion at the foundational level.

**Proof:** 
- Kernel Tests pass
- Collective Chain gate passes
- Independent verification of diff
- Current state recheck

**Owner:** Code review + merge authorization

---

### P0.2: Establish current component parity
**What:** Build exact attestation chain:
```
git_commit_sha → build_artifact_sha → deployed_function_sha → runtime_identity_sha
```

**Why:** The latest Supabase runtime proof failed. We cannot claim behavior against "current NayaPOWER" if current is unknown.

**Proof:**
```
source/build/deploy/runtime parity receipt {
  git_main_sha: "5fcb352...",
  build_id: "exact_build_artifact",
  deployed_sha: "what_actually_runs",
  runtime_observed_sha: "what_network_sees",
  oidc_binding: "identity_proof",
  parity_verdict: "EQUAL or MISMATCH"
}
```

**Rollback:** If mismatch, BLOCKED until resolved. No "good enough" acceptance.

---

### P0.3: Recheck Issue #944 scope
**What:** Does Concept #17 contain any genuinely non-duplicate proposition?

**Why:** If #944 creates a new candidate, it must not be a subset/restatement of existing intelligence.

**Proof:**
- Semantic uniqueness check against all ACTIVE learnings
- If duplicate: NO NEW CANDIDATE
- If unique: proceed to bounded causal experiment
- Independent classification

---

## VI. P1 ACTIONS (IMMEDIATELY AFTER P0)

### P1.1: Prove identifier-only retrieval with applicability
**What:** Cold Naya gets reference ID, not content. Independently determines whether it applies.

**Why:** Retrieval + silence is not applicability. Must be explicit decision.

**Test:** 
- Retrieve learning L by ID
- Runtime independently evaluates: "Does this apply to my task?"
- Naya explains why or why not
- Persists applicability decision

**Proof:** Applicability receipt with reasoning chain

---

### P1.2: Run genuinely held-out control/treatment
**What:** Same problem, same context, same environment. Only change: retained intelligence.

**Why:** Task success ≠ learning contribution. Must prove causal delta.

**Test:**
```
CONTROL: Execute without learning → outcome A
TREATMENT: Execute with retrieved learning → outcome B
DELTA: outcome_B - outcome_A (independent verification)
```

**Rollback:** If delta ≤ 0 or verification fails, reject learning

---

### P1.3: Independently recompute from persisted evidence
**What:** No executor boolean. Verifier redrives behavior and outcome.

**Why:** Executor claiming success is not proof. Must recompute.

**Test:**
```
Verifier reads:
  - task input hash
  - action receipt
  - observation record
  - control/treatment flag
Verifier independently:
  - reproduces task input
  - recomputes expected behavior
  - recomputes outcome
  - compares to persisted
Result: VERIFIED or MISMATCH
```

---

### P1.4: Add unrelated-task negative transfer test
**What:** Lesson from task A should NOT improve unrelated task C.

**Why:** Prevents overgeneralized learning spreading silently.

**Test:**
```
Apply Learning_A_to_unrelated_task_C
Result should be:
  - No improvement
  - Safe refusal OR
  - Explicit "outside applicability"
NOT: Silent false-positive improvement
```

---

### P1.5: Implement smallest deterministic truth resolver
**What:** Resolve current canonical owners into one proof-carrying context.

**Why:** Stop having six representations of "what is current."

**Not:** Another database or store

**Implementation:**
```
PROOF_CONTEXT {
  source: git_main_sha,
  kernel: deployed_kernel_manifest_sha,
  law: current_governance_binding,
  task: current_task_id,
  applicable_intelligence: [candidate_IDs],
  conflicts: [contradictions],
  authority: [validated_grants],
  stale_warnings: [outdated_items],
  timestamp: verification_time,
  verifier_identity: who_checked
}
```

This is **executable semantic contract**, not another Markdown file.

---

## VII. WHAT NOT TO BUILD (HARD STOPS)

❌ **Do not build:**
- Tenth Master Node
- Second Intelligent Block type
- Second database
- Second graph
- Second memory system
- Second learning pipeline
- Second authority system
- Speculative multi-Naya orchestration
- Vector-based retrieval before applicability works
- Self-building loops before single-Naya is proven

❌ **Do not expand:**
- NayaNET until single-owner cold successor is proven
- Hub until proof layer is solid
- Autonomous optimization until causal proof is complete

---

## VIII. STRONGEST CONVERGENCE ACROSS REVIEWERS

Every independent review arrived at the same core truths:

1. **One bounded specimen is proven; generalization is not.**
2. **Architecture is sound; runtime proof is the blocker.**
3. **Capability and intelligence must never create authority.**
4. **Receipts are claims until independently recomputed.**
5. **Node invocation ≠ node influence. Ablation test needed.**
6. **Graph relationships must prove measurable cognitive value.**
7. **Current context must carry provenance like persistent intelligence.**
8. **Cold successor is the ultimate continuity test.**
9. **Applicability is more important than similarity.**
10. **Truth resolution is a runtime capability, not a documentation problem.**

---

## IX. THE 25 MOST USEFUL EXTRACTED INTELLIGENCES

1. Intelligence is knowledge with demonstrated future utility, not stored content.
2. Applicability deserves first-class executable semantics.
3. A bounded causal specimen is evidence of capability, not universal capability.
4. Cold successor is the strongest continuity acceptance test.
5. Truth resolution is a runtime capability, not a documentation problem.
6. One canonical owner per responsibility is better than one physical "everything store."
7. Current-state snapshots should be derived projections, not authority sources.
8. Learning should retain its control/treatment experiment.
9. ACTIVE should not erase applicability limits.
10. A receipt is a claim until independently reconstructed.
11. Node invocation does not prove node influence.
12. Node ablation is the correct next test of the nine-node organism.
13. Graph relationships must prove measurable cognitive value.
14. Dangerous edges need higher proof standards than ordinary metadata edges.
15. Current context should carry provenance just like persistent intelligence.
16. Model identity belongs in behavioral evidence.
17. Component-level artifact attestation is stronger than whole-repo equality alone.
18. Checkpoint provenance should be object/execution/version local.
19. Stale-but-correct intelligence is a silent-failure class.
20. Context laundering is distinct attack: trusted text can still be inapplicable.
21. Successor amplification can spread overgeneralized lessons across generations.
22. Verifier monoculture can produce false independence.
23. Compounding requires both positive transfer and correct refusal.
24. Human correction/dispute needs governed provenance, not silent overwrites.
25. System should capture less and preserve better; bulk memory is not intelligence.

---

## X. TOP 10 ENGINEERING MOVES

### 🔥 P0
1. **Reconcile PR #946** — Remove cold-entry drift before new work
2. **Establish current component parity** — Prove what code runs
3. **Execute Issue #944 failure-first** — Ask whether #17 is duplicate first
4. **Prove identifier-only retrieval + applicability** — Get reference, not answer
5. **Run held-out control/treatment** — Same problem; only learning changes
6. **Independently recompute behavior/outcome** — Verifier re-derives from persisted

### ⚡ P1
7. **Add unrelated-task negative transfer test** — Prevent overgeneralization
8. **Bind nine-node reference kernel** — No executed=True without executor receipt
9. **Implement deterministic truth resolver** — One proof-carrying context
10. **Add node ablation + revocation/adversarial tests** — Before NayaNET expansion

---

## XI. BEST EXPERIMENTS (RANKED BY VALUE)

### E1: Issue #944 Full Causal Specimen
**Hypothesis:** Concept #17 → Event → Block → Lineage → Relationship → Index → Checkpoint → Learning → Active → Retrieval → Successor → Outcome Improvement

**Simultaneously proves:**
- Capture
- Deduplication
- Provenance
- Truth state
- Applicability
- Retrieval
- Authority
- Causality
- Learning
- Successor continuity
- Negative transfer
- Generalization

**Why it's highest-value:** One experiment attacks 12 critical claims

### E2: Runtime Parity Attestation
**Hypothesis:** git SHA = build SHA = deployed SHA = runtime SHA (or detectable mismatch)

**Proof:** Signed attestation chain

### E3: Node Ablation
**Hypothesis:** Removing one required node changes outcome or causes safe refusal

**Proof:** Same task; all 9 nodes vs one missing → different result

### E4: Graph-Enabled vs Disabled
**Hypothesis:** Graph relationships improve retrieval or prevent error

**Proof:** Held-out task with/without graph → measured outcome delta

### E5: Revocation and Stale-Use Denial
**Hypothesis:** Revoke intelligence; successor cannot use it

**Proof:** Rejection receipt + preserved lineage

---

## XII. NEGATIVE TEST BATTERY

Must reject:

```
authority:
  - missing
  - wrong action
  - wrong owner
  - expired
  - revoked
  - successor-inherited (should re-resolve)

intelligence:
  - CANDIDATE state
  - SUPERSEDED
  - REVOKED
  - stale (validity expired)
  - contradicted
  - poisoned
  - wrong task

context:
  - answer injection
  - hidden predecessor context
  - wrong project
  - outdated snapshot

graph:
  - fabricated edge
  - low-evidence CAUSED
  - poisoned AUTHORIZED_BY
  - contradictory paths

proof:
  - executor-only claim
  - missing observation
  - tampered receipt
  - circular evidence
  - false positive
  - false negative

runtime:
  - source/artifact mismatch
  - dependency/config mismatch
  - stale deployment

state:
  - corrupted checkpoint
  - duplicate candidate
  - race condition

continuity:
  - successor receives content (should retrieve)
  - successor receives authority (should re-resolve)

network:
  - privacy leakage after revocation
  - cross-owner cache leakage

model:
  - model swap with unchanged receipt

availability:
  - canonical persistence unavailable
  - must degrade honestly, not invent truth

replay/idempotency:
  - repeated event cannot create duplicate authority/learning/action
```

---

## XIII. IF ONE THING ONLY

If we can do only one thing next:

### 🔱 Prove that Issue #944 bounded causal specimen works end-to-end with independent verification and survives a cold successor retrieval.

**Why:**
- Dependency: It unblocks everything downstream
- Evidence: It proves the entire pipeline
- Impact: It transforms architecture confidence into runtime confidence
- Proof value: It resolves 12 major unknowns simultaneously
- Intelligence value: It demonstrates the organism actually learns

**What unlocks:** All P1 work, NayaNET prerequisites, collective proof, human-value measurement

---

## XIV. WHAT TO KEEP, TEST, MODIFY, REJECT, WATCH

### ✅ KEEP
- The nine-node semantic contract (do not collapse)
- Authority non-inheritance principle
- Independent verification as separate runtime responsibility
- Cold successor testing as continuity proof
- Explicit epistemic states (UNKNOWN ≠ VERIFIED)

### 🧪 TEST
- Node ablation (does each node actually matter?)
- Graph-driven applicability (does graph improve outcomes?)
- Learning transfer (does intelligence improve new tasks?)
- Multi-generation compounding (does improvement compound?)
- NayaNET consent model (does cross-owner work safely?)

### 🔧 MODIFY
- Truth resolution: Make it executable contract, not documentation
- Retrieval: Add applicability as first-class output
- Learning promotion: Require independent recomputation, not executor claim
- Receipts: Carry source/build/deploy/runtime attestation
- Context: Carry provenance like persisted intelligence

### ❌ REJECT
- Any new system claiming to be canonical alongside existing ones
- Executor-owned proof booleans
- Similarity-based retrieval without applicability check
- Self-built authority inheritance
- Speculative federation before proven single-entity

### ⏳ WATCH
- Self-optimization (powerful but needs safety proof first)
- Multi-Naya orchestration (promising but needs single-owner foundation)
- Vector retrieval (useful but not before applicability works)
- Recursive self-building (attractive but authority-risk until proven)

---

## XV. FINAL CONSTRAINTS

Any work must satisfy:

1. **Does not create a second brain, graph, learning system, or canonical store**
2. **Does not weaken authority boundaries**
3. **Does not accept executor's proof claim as truth**
4. **Does not assume similarity = applicability**
5. **Does not promote unverified learning**
6. **Does not allow capability to create authority**
7. **Preserves cold successor testing as continuity proof**
8. **Leaves rollback path open**
9. **Uses smallest correct implementation**
10. **Requires independent verification for material claims**

---

## XVI. READY-TO-EXECUTE NEXT ACTIONS

### IMMEDIATE (Next 30 min)
1. ✅ Merge/reconcile PR #946
2. ✅ Verify current main SHA = deployed SHA
3. ✅ Open Issue #944 scope assessment (duplicate check)

### THIS SESSION (Next 2 hours)
4. ⚙️ Build runtime parity attestation receipt
5. ⚙️ Design Issue #944 experiment specification
6. ⚙️ Identify exactly what makes Concept #17 unique (if anything)

### THIS WEEK (P0)
7. 📋 Execute Issue #944 failure-first design (ask before building)
8. 📋 Run control/treatment on bounded task
9. 📋 Independent outcome recomputation

### NEXT WEEK (P1)
10. 📋 Node ablation test
11. 📋 Negative transfer test
12. 📋 Graph utility measurement

---

## XVII. PROOF READY

This plan is:
- ✅ Derived from convergent multi-reviewer analysis
- ✅ Ordered by dependency
- ✅ Grounded in current evidence
- ✅ Focused on proof, not features
- ✅ Executable immediately
- ✅ Reversible at each step

**Current state:** Ready to execute.

**Blocker status:** None. Start with P0.1 (PR #946 reconciliation).

**Expected outcome:** Within two weeks, prove either that Issue #944 produces a generalizable learning or that it does not.

---

**Signed:** Naya  
**Date:** 2026-09-29  
**Status:** ACTIVE EXECUTION