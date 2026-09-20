# TEAM NAYA MASTER SYSTEM PROMPT — OSCAR AUDIT RESULT V1

**Target:** `SUPERBRAIN/NIA-COMMUNICATION/TEAM-NAYA-MASTER-SYSTEM-PROMPT-AAA-V1.md`  
**Target commit:** `363fa2a640d802f6eb233db0de6797199c14d6b0`  
**Independent audit posture:** Oscar / verifier lens  
**Audit date:** 2026-09-17

# RESULT

## AUDIT STATUS: PASS_WITH_REPAIRS

The prompt is structurally strong and substantially aligned with the Runtime Constitution, authority registry, and current Team Naya operating model.

It is **NOT YET AUTHORITATIVE** because one material authority-hierarchy conflict was found and must be repaired before promotion.

---

# 1. WHAT PASSED

### Human authority
PASS.

The prompt correctly identifies Shawn as the human authority and explicitly states that agents, tools, prompts, workflows, memory, or prior Nayas cannot mint authority.

### Capability vs authority
PASS.

The prompt explicitly states:

`CAPABILITY DOES NOT CREATE AUTHORITY.`

This agrees with the Authority Registry hard rule `CAPABILITY != AUTHORITY`.

### Truth / evidence discipline
PASS.

The prompt preserves the required distinctions between claim, evidence, testing, independent verification, live verification, and acceptance.

### Builder ≠ Judge
PASS.

The prompt explicitly assigns Oscar/Verifier and Adversary roles and rejects self-verification as sufficient independent proof.

### Activity architecture
PASS WITH IMPLEMENTATION-GAP LANGUAGE.

The prompt correctly describes automatic execution-boundary Activity as the target architecture rather than falsely claiming that the runtime already provides it.

It also explicitly prohibits creating a second event store, Activity database, message bus, memory system, queue, or governance kernel.

This agrees with the current P0 execution architecture.

### Cold-Naya orientation
PASS.

The prompt directs cold Naya to:

`START-HERE/COLD-NAYA-OPERATING-INDEX.md`

and requires truth restoration before consequential work.

### Failure / blocked behavior
PASS.

The prompt requires truthful failure reporting, repair, retest, independent verification, and productive behavior while blocked.

### Perpetual operation
PASS.

The prompt explicitly defines perpetual Naya Power as governed self-continuity rather than uncontrolled background autonomy.

### Cleanup discipline
PASS.

The cleanup rules preserve recoverability and prohibit deleting valuable history merely for aesthetic reasons.

### Intelligent Hub boundary
PASS.

The Hub is correctly defined as a projection of canonical Superbrain state rather than a competing source of truth.

---

# 2. MATERIAL CONFLICT FOUND

## SOURCE-OF-TRUTH / AUTHORITY HIERARCHY

The Master Prompt currently says:

```text
EXTERNAL HARD CONSTRAINTS
↓
CONSTITUTION
↓
EXPLICIT CURRENT HUMAN AUTHORITY
↓
GOVERNANCE ACTS
↓
ARCHITECTURE
↓
ACTIVATION
↓
OPERATIONAL LAWS
↓
DOMAIN STANDARDS
↓
CURRENT MISSION STATE
↓
SMART NOTES / HISTORICAL INTELLIGENCE
↓
ASSUMPTIONS
```

The canonical Authority Registry defines the actual precedence as:

```text
0 EXTERNAL_HARD_CONSTRAINTS
1 NAYA_POWER_CONSTITUTION
2 EXPLICIT_CURRENT_HUMAN_AUTHORITY
3 GOVERNANCE_ACT_AND_AUTHORITY_REGISTRY
4 MASTER_SYSTEM_ARCHITECTURE
5 MASTER_ACTIVATION_AND_LEAD_MODE
6 CANONICAL_OPERATIONAL_LAWS
7 DOMAIN_STANDARDS
8 CURRENT_MISSION_STATE
9 SMART_NOTES_AND_HISTORICAL_INTELLIGENCE
10 ASSUMPTIONS_AND_CONVENIENCE
```

The difference is not merely cosmetic: the canonical registry is the authoritative machine-readable authority source, and its exact names/order should not be paraphrased in a way that could create a competing hierarchy.

## REQUIRED REPAIR

Replace the prompt's generalized hierarchy with the exact Authority Registry precedence, and state explicitly:

> The machine-readable Authority Registry is authoritative for authority precedence. This prompt may explain the hierarchy but may not redefine it.

Also preserve the Registry's hard rule:

`HUMAN_AUTHORITY > RUNTIME_AUTONOMY_WITHIN_CONSTITUTIONAL_AND_EXTERNAL_CONSTRAINTS`

---

# 3. SECONDARY OBSERVATION

The prompt says:

> “Shawn Vibert is the human authority and final decision-maker.”

This is directionally correct but should be interpreted within the external/platform constraints and constitutional boundaries already established by the Authority Registry and Runtime Constitution.

Recommended wording for V1.1:

> **Shawn Vibert is the explicit current human authority and final mission decision-maker within applicable external constraints and Naya Power constitutional boundaries.**

This removes any possibility that the prompt could be read as granting human authority power to override platform safety or constitutional constraints.

---

# 4. UNSUPPORTED CLAIMS

NONE MATERIAL.

The prompt correctly avoids claiming that automatic Activity emission or full perpetual execution already exists.

It describes those capabilities as target architecture.

The prompt also does not promote the reconstructed 100-question framework to historical canonical status.

---

# 5. DUPLICATE-SYSTEM RISK

PASS.

The prompt explicitly prohibits competing event stores, queues, memory systems, governance kernels, and Activity stores.

That is consistent with the current architecture.

---

# 6. SAFETY / AUTONOMY RISK

PASS AFTER REPAIR.

The prompt correctly defines perpetual power as governed continuity rather than unrestricted autonomous operation.

No autonomous background claim should be added during V1.1 repair.

---

# 7. REQUIRED V1.1 REPAIRS

1. Replace the generalized authority hierarchy with the exact Authority Registry precedence.
2. State that the Authority Registry controls precedence and the prompt cannot redefine it.
3. Qualify the Shawn human-authority statement by external constraints and constitutional boundaries.
4. Re-run static validation.
5. Re-run Oscar audit.
6. Only then promote V1.1 to canonical Team Naya master prompt.

---

# 8. FINAL RECOMMENDATION

**AUTHORITATIVE AFTER REPAIRS**

Do **not** mark V1 as canonical yet.

The artifact is valuable and substantially correct, but the hierarchy conflict must be repaired first.

---

# 9. ONE NEXT ACTION

Create **TEAM-NAYA-MASTER-SYSTEM-PROMPT-AAA-V1.1.md** with the two authority corrections above, run the static validator, then perform a second Oscar audit against the exact V1.1 artifact.

Only a clean second audit may promote the prompt to canonical status.

**Builder ≠ Judge.**
