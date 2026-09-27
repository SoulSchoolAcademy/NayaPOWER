# NayaPOWER — Intelligence Evaluation Architecture v1

**Status:** EXECUTABLE EVALUATION CONTRACT  
**Purpose:** Umbrella contract for proving intelligence rather than describing architecture.  
**Relationship:** This contract governs the evaluation program; N9-001..N9-010 are the focused nine-node behavioral battery.

## 1. Core rule

A test instrument is itself untrusted until tested.

Neither the system under test nor the evaluator may promote a capability from:

`ASSERTED` → `PROVEN`

merely because a document, field, filename, schema, status, model response, or matching phrase says the capability exists.

Every positive evaluator result must identify **executed evidence**, not merely text that resembles evidence.

## 2. Evaluation hierarchy

The program has four layers:

1. **Architecture layer** — what is defined.
2. **Execution layer** — what actually ran.
3. **Behavior layer** — what behavior changed.
4. **Causal/generalization layer** — whether the architecture caused a durable improvement that survives held-out and cold tests.

A lower layer cannot prove a higher layer.

### Evidence ladder

`L0 ASSERTED`
→ `L1 STRUCTURALLY_PRESENT`
→ `L2 EXECUTED`
→ `L3 BEHAVIORALLY_OBSERVED`
→ `L4 VERIFIED`
→ `L5 CAUSALLY_ATTRIBUTED`
→ `L6 GENERALIZED`
→ `L7 COMPOUNDED`
→ `L8 COLD_SUCCESSOR_PROVEN`

The evaluator MUST report the highest evidence level actually supported. It MUST NOT collapse the ladder into a single green score.

## 3. The 14-test umbrella

The evaluation program retains the full 14-family examination:

1. Nine-kernel examination
2. Node intelligence
3. Node-to-node behavior
4. Brain reasoning
5. Governed action
6. Brutal verification
7. Self-optimization
8. Self-organization
9. Learning
10. Compounding
11. Cold Naya / cold successor
12. Adversarial resilience
13. Operational self-awareness
14. Twenty-question intelligence examination

N9-001..N9-010 are the executable proof battery for the nine-node brain. They do not replace the broader examination.

## 4. Mandatory test receipt

Every executed evaluation MUST record:

- test ID and fixture ID;
- source commit and runtime version;
- exact input and fixture hash;
- baseline/control condition;
- actual execution path;
- observed state before/after;
- evidence identifiers;
- authority decision;
- expected vs actual outcome;
- failures and uncertainties;
- reproducibility instructions;
- highest evidence level;
- causal claim, if any;
- confounders;
- **system-learning:** what the test taught us about the system itself;
- **evaluator-integrity:** how the instrument was validated against false positives.

## 5. Evaluator integrity gate

A test harness MUST have its own tests.

At minimum:

### Positive control
A fixture with known valid evidence MUST be recognized.

### Negative control
A fixture containing only assertions, filenames, schemas, or prose MUST NOT be recognized as behavioral proof.

### Mutation control
Deliberately remove or corrupt the evidence predicate. The evaluator MUST fail to pass the capability.

### Contradiction control
Supply authoritative evidence that conflicts with the apparent positive signal. The evaluator MUST surface `CONTRADICTED` or an equivalent fail-closed state.

### Stale-source control
Run against a known stale commit while a newer authoritative commit exists. The receipt MUST identify the source as stale rather than calling it current.

### Cold control
Run with zero conversation context. Any required answer must be reconstructible from explicitly permitted canonical sources.

A harness that fails its own integrity gate cannot issue PROVEN verdicts.

## 6. The 20 questions are not regex questions

The 20-question examination is an intelligence test, not a keyword-search test.

A question is **ANSWERABLE** only when the canonical evidence contains enough structured, executed evidence to answer the question itself.

A matching word such as `learning`, `authorization`, `behavior`, or `provenance` is not evidence.

Therefore:

- keyword presence MAY locate candidate evidence;
- keyword presence MUST NOT establish a PASS;
- filenames MUST NOT establish proof;
- a test file mentioning a capability MUST NOT establish that production executed it;
- a library with no executed caller MUST NOT establish runtime behavior;
- a CI workflow definition MUST NOT establish that the workflow actually passed on the tested source;
- a historical receipt MUST NOT establish current behavior unless its source/runtime applicability is verified.

## 7. Historical evidence

Historical receipts are valuable evidence but have a time boundary.

For every historical result, record:

`evidence_head`  
`current_head`  
`runtime_version`  
`applicability_status`

Allowed applicability states:

`CURRENT`, `REVALIDATED`, `STALE`, `UNKNOWN`.

A historical PASS with `STALE` or `UNKNOWN` applicability MUST NOT promote current capability.

## 8. Killer test

The killer test is:

> Find a problem for which persisted, connected, learned intelligence materially changes performance; demonstrate the difference against a frozen control; reproduce it on held-out cases; then show a cold successor benefits on a related but different task.

Required causal chain:

`CONTROL`
vs
`PERSISTED_INTELLIGENCE`
→ observed delta
→ causal controls
→ held-out generalization
→ generational inheritance
→ cold successor improvement.

The killer test is **not** satisfied by three database records, a Smart Note, a checkpoint, or a narrative saying that learning occurred.

## 9. Self-organization is a separate capability

Repository organization, branch count, worktree count, or document count is not by itself evidence that the intelligence system can self-organize.

Self-organization must be tested behaviorally with a messy corpus containing:

- duplicates;
- contradictions;
- related concepts;
- stale and current items;
- incomplete facts;
- interpretations;
- noise;
- outcomes and failures.

The critical relationship/taxonomy MUST NOT be supplied in advance.

PASS requires useful emergent organization that preserves provenance, uncertainty, contradiction, applicability, and lineage.

## 10. Learning requires behavioral change

A new learning record is not learning.

Learning requires:

`OUTCOME`
→ `LESSON`
→ `PERSIST`
→ `RETRIEVE`
→ `CHANGE`
→ `MEASURED_IMPROVEMENT`

If behavior does not change, learning is not proven.

If behavior changes but no improvement is measured, learning may be present but compounding/effectiveness is not proven.

## 11. Promotion gates

No capability may jump directly from structural presence to effectiveness.

Required progression:

`STRUCTURALLY_ACTIVE`
→ `EXECUTED`
→ `BEHAVIORALLY_PROVEN`
→ `VERIFIED`
→ `CAUSALLY_ATTRIBUTED`
→ `GENERALIZED`
→ `COMPOUNDED`
→ `COLD_SUCCESSOR_PROVEN`
→ `EFFECTIVENESS_PROVEN`

Promotion requires explicit evidence and evaluator-integrity PASS.

## 12. Tester self-correction

If a harness produces a positive result and later inspection shows that the predicate was satisfied by a filename, regex, assertion, stale artifact, test-only caller, or non-executed library, the evaluator MUST:

1. downgrade the result;
2. record the false-positive mechanism;
3. add a regression test;
4. rerun the affected question;
5. preserve the original result as superseded evidence rather than deleting it.

This is a required learning loop for the tester itself.

## 13. Meta-learning

Every battery run MUST answer:

> **What did we learn about the system itself?**

Examples:

- a gate can report GREEN while missing a semantic authority conflict;
- a learning module exists but has no production caller;
- a measurement library exists but is not executable;
- a historical proof is stale against current HEAD;
- a cold test proves continuity only for the surfaces it actually exercises.

Meta-learning becomes reusable intelligence only after it is captured with provenance and changes a later test or implementation.

## 14. Current priority sequence

The evaluation program should now execute in this order:

1. Reconcile the constitutional-authority gate against current `origin/main`.
2. Prove the authority detector with positive, negative, mutation, contradiction, and stale-source controls.
3. Repair the cold 20-question harness so **no question can PASS from keyword presence alone**.
4. Add machine-readable evaluator-integrity receipts.
5. Run N9-001 and N9-003.
6. Run N9-004.
7. Run N9-002 ablation.
8. Run N9-005 counterfactual.
9. Run N9-007 self-diagnosis.
10. Run N9-008 self-optimization.
11. Run N9-006 generational held-out evaluation.
12. Run N9-009 cold successor.
13. Run N9-010 ultimate intelligence / killer test.
14. Add and execute the separate self-organization test.

## 15. Non-negotiable final rule

The system does not become more intelligent because the repository contains better explanations of intelligence.

The evaluator does not become better because the evaluator contains better explanations of testing.

**Both must demonstrate changed behavior under controlled conditions.**

The final question is therefore not:

> "Does the architecture look like intelligence?"

It is:

> **"What changed in the world because the architecture persisted, connected, verified, learned, and compounded experience — and can another cold Naya reproduce that result?"**
