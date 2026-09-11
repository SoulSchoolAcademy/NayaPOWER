# 🔱 NAYA POWER RUNTIME ARCHITECTURE / MACHINE CONTRACT

**Version:** 1.0  
**Status:** Executable Vertical Slice — PRE-LOCK  
**Repository:** `SoulSchoolAcademy/NayaPOWER`  
**Purpose:** Define the smallest provider-neutral constitutional runtime that can be executed, tested, observed, and extended without turning the constitution into a prompt pile.

---

## 1. NORTH STAR

> **Naya Power is the executable constitutional operating layer that connects human-readable principles, machine-readable contracts, runtime enforcement, verification, evidence, and adaptive learning to produce maximum responsible, verified, useful value.**

Naya Power is **not** the documents, JSON, code, or model individually.

The model supplies reasoning/candidate generation. Naya Power governs the decision boundary, execution eligibility, evidence discipline, verification state, and learning handoff.

---

## 2. DESIGN LAW

### 2.1 Permission precedes optimization

An action is first evaluated for legitimacy, authority, and protected-boundary compliance.

`INELIGIBLE ACTIONS NEVER ENTER VALUE OPTIMIZATION.`

A prohibited action cannot become permissible because its predicted benefit is larger.

### 2.2 Human life is non-compensable

Human life and other explicitly protected boundaries are not scalar variables in the value equation.

`PROTECTED BOUNDARY VIOLATION → INELIGIBLE / REFUSE`

No amount of benefit, reward, urgency, popularity, intelligence, or delegated authority may buy back eligibility.

### 2.3 Capability does not create authority

Model intelligence, confidence, reward, or self-improvement does not create permission.

`CAPABILITY ≠ AUTHORITY`

### 2.4 Unknown remains unknown

Missing authorization, evidence, context, or verification cannot be converted into certainty by model confidence.

`UNKNOWN ≠ VERIFIED`

### 2.5 Learning does not rewrite the Constitution

Verified experience may improve procedures, preferences, retrieval, and future decision quality. It cannot silently mutate constitutional boundaries.

`LEARNED ≠ ADOPTED`

Governance-sensitive changes require an explicit proposal and authority path.

---

## 3. RUNTIME PIPELINE

The vertical slice implements this minimum loop:

```text
REQUEST
  ↓
UNDERSTAND
  ↓
LEGITIMIZE
  ↓
AUTHORIZE
  ↓
CONSTRAIN
  ↓
ASSESS RISK / EVIDENCE
  ↓
FILTER INELIGIBLE OPTIONS
  ↓
VALUE ELIGIBLE OPTIONS
  ↓
CHOOSE / REFUSE / ESCALATE
  ↓
RECEIPT
```

The broader Naya operating loop remains:

```text
SEE → UNDERSTAND → THINK → CHOOSE → ACT → VERIFY → LEARN → IMPROVE
```

The existing Promotion Engine remains responsible for durable intelligence promotion; this kernel does not duplicate it.

---

## 4. MACHINE CONTRACT

### Request

A runtime request contains:

- `request_id`
- `mission`
- `context`
- `authority`
- `candidates[]`
- `constitution_version`

### Candidate

Each candidate action contains:

- `id`
- `description`
- `expected_benefit` — normalized comparison score, 0–100
- `necessary_cost` — normalized comparison score, 0–100
- `risk_loss` — normalized expected-loss score, 0–100
- `authorization` — `approved`, `denied`, or `unknown`
- `boundary_violations[]`
- `evidence_state` — `UNKNOWN`, `IMPLEMENTED`, `TESTED`, `VERIFIED`, `RUNTIME-PROVEN`, `PRODUCTION-PROVEN`
- `reversible` — boolean
- `governance_sensitive` — boolean

### Receipt

Every evaluation returns a deterministic receipt containing:

- request identity
- constitution version
- candidate eligibility decisions
- value calculation for eligible candidates
- final decision
- reason
- verification state
- timestamp

The receipt records what the kernel actually evaluated. It does not claim that an external action occurred or was verified unless an external verifier supplies that evidence.

---

## 5. DECISION CALCULUS

For eligible actions only:

`V(a) = expected_benefit(a) - necessary_cost(a) - risk_loss(a)`

Then:

`a* = argmax V(a)`

This scalar is **only a comparison mechanism among already-eligible actions**.

The kernel never computes a compensating value for protected human-life boundaries.

### Uncertainty rule

If an action is materially dependent on unknown authorization, unknown evidence, or an unresolved governance boundary, it is not eligible for autonomous selection.

The kernel returns `ESCALATE` when the uncertainty cannot be safely resolved by the supplied contract.

---

## 6. HARD BOUNDARIES

The first executable boundary set is:

1. `HUMAN_LIFE_PROTECTED`
2. `NONCONSENSUAL_HARM_PROHIBITED`
3. `UNAUTHORIZED_EXTERNAL_ACTION_PROHIBITED`
4. `GOVERNANCE_MUTATION_REQUIRES_AUTHORITY`
5. `FABRICATED_VERIFICATION_PROHIBITED`
6. `SELF_AUTHORIZATION_PROHIBITED`

These are machine policy identifiers, not a claim that a small deterministic kernel can solve every real-world safety problem. The purpose of this slice is to make the boundary **executable and testable**.

---

## 7. AUTHORITY RULES

| Condition | Runtime result |
|---|---|
| `authorization=approved`, no boundary violation | Eligible |
| `authorization=denied` | Ineligible |
| `authorization=unknown` | Ineligible; escalate if material |
| boundary violation present | Refuse / ineligible |
| governance-sensitive + not approved | Escalate |
| verification claim without evidence | Invalid contract |

---

## 8. VERIFICATION LAW

The runtime distinguishes:

`IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ RUNTIME-PROVEN ≠ PRODUCTION-PROVEN`

The kernel may prove that **its own decision procedure executed and produced a receipt**.

It may not infer that a downstream action succeeded merely because a function returned.

This preserves the repository's existing evidence law and Promotion Engine boundary.

---

## 9. LEARNING HANDOFF

The kernel emits a structured decision receipt suitable for later promotion into the existing canonical intelligence system.

The intended compound loop is:

`ACTION → OBSERVATION → RECEIPT → VERIFICATION → LEARNING → RULE → FUTURE PREFLIGHT`

Constitutional changes are never auto-promoted by this kernel.

---

## 10. FIRST VERTICAL SLICE

The first slice intentionally does **not** call an LLM, database, vector store, or external tool.

It proves the smallest meaningful constitutional runtime:

1. Load machine contract.
2. Validate request shape.
3. Reject protected-boundary violations.
4. Reject unknown/denied authority.
5. Refuse governance mutation without authority.
6. Score eligible actions.
7. Select highest responsible eligible value.
8. Produce an auditable receipt.
9. Run deterministic self-tests.

This is deliberate. We first prove the governing kernel before adding model/tool complexity.

---

## 11. NON-GOALS OF V1

V1 does not claim to provide:

- general intelligence
- AGI or superintelligence
- perfect moral reasoning
- complete natural-language safety understanding
- independent factual verification of arbitrary external claims
- autonomous real-world authority
- production safety certification

Those require additional runtime layers and evidence.

---

## 12. SUCCESS GATE

The vertical slice is successful when the exact committed implementation can demonstrate:

- safe eligible action selected by value;
- prohibited human-harm action rejected even when its stated benefit is higher;
- unknown authorization escalated rather than guessed;
- governance-sensitive mutation escalated without approval;
- fabricated verification rejected;
- receipt contains constitutional version and eligibility evidence;
- all deterministic self-tests pass.

Only after that evidence exists should the kernel be connected to a model adapter and real tools.

---

## 13. RELATIONSHIP TO EXISTING NAYAPOWER

This runtime is an **execution kernel**, not a replacement for the existing architecture.

It complements:

- Activation Engine — activation and durable document identity;
- Canonical Event Store — authoritative memory/event persistence;
- Promotion Engine — intelligence promotion and deduplication;
- Adaptive Learning — learning and compounding;
- Oscar/adversarial validation — independent challenge;
- Repository Operating Standard — cold-start/source/state/evidence discipline.

The architectural direction is:

```text
HUMAN PRINCIPLES (.md)
        ↓
MACHINE CONTRACT (.json)
        ↓
RUNTIME KERNEL (.py)
        ↓
TESTS
        ↓
RECEIPT / EVIDENCE
        ↓
CANONICAL MEMORY / PROMOTION
        ↓
LEARNING
```

**The purpose is not to create more documents. The purpose is to make the governing intelligence executable.**
