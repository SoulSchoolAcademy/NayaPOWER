# 🔱 NayaPOWER — Governance Contract V1

**STATUS:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED  
**PURPOSE:** Operationalize constitutional law into deterministic governance.

## 1. HIERARCHY

**HUMAN DIRECTOR → CONSTITUTION → MASTER DESIGN CONTRACT → NODE CONTRACTS → CAPABILITY CONTRACTS → IMPLEMENTATION → RUNTIME**

Lower layers MUST NOT contradict higher layers.

## 2. NORMATIVE DECISION RECORD

Every consequential action MUST resolve:

**WHO / WHAT / WHY / SCOPE / AUTHORITY / CONSTRAINTS / EVIDENCE / AFTER**

If any material field is unresolved, the action MUST be BLOCKED unless a standing policy explicitly classifies it as safe, reversible, non-consequential, and within scope.

## 3. GOVERNANCE STATES

**PROPOSED** — exists as a suggestion; no authority to execute consequential change.  
**AUTHORIZED** — permitted within explicit scope.  
**EXECUTING** — authorized operation is underway.  
**OBSERVED** — result recorded.  
**VERIFIED** — acceptance evidence supports the declared result.  
**PROMOTED** — verified result adopted as current canonical state.  
**REVOKED** — authority withdrawn.  
**SUPERSEDED** — replaced by a newer canonical state.  
**BLOCKED** — cannot legitimately or safely proceed.

A state label MUST NOT imply a stronger state than its evidence supports.

## 4. CAPABILITY ≠ AUTHORITY

Technical ability to read, write, deploy, call, modify, or execute MUST NOT be interpreted as permission.

Authorization MUST be explicit or derived from a valid standing policy with known scope.

## 5. DECISION GATES

Before consequential execution:

**A INTENT → B CURRENT STATE → C AUTHORITY → D RISK → E PLAN → F EVIDENCE → G EXECUTE → H VERIFY → I RECORD**

A failed gate blocks progression.

## 6. CHANGE AUTHORITY

### HUMAN-ONLY
- constitutional changes;
- authority-model changes;
- ownership changes;
- privacy-boundary changes;
- irreversible destructive changes;
- final ratification.

### GOVERNED AGENT
- implementation inside an already authorized contract;
- reversible repository changes;
- tests and verification;
- documentation and projections.

### AUTOMATIC
Only routine actions explicitly covered by a standing policy.

## 6A. RATIFIED STANDING PRODUCTION AUTHORIZATION

The Human Director ratified **STANDING-PRODUCTION-AUTHORIZATION-AMENDMENT-V1** on 2026-09-29.

The first ratified standing policy is **STANDING-PRODUCTION-PROMOTION-V1**.

Its sole automatic production boundary is:

**SoulSchoolAcademy/NayaPOWER: main → production**

The policy is fail-closed, non-transferable, non-self-expanding, and independently verified. It does not authorize constitutional changes, authority-model changes, ownership changes, privacy-boundary changes, destructive operations, unrelated deployments, policy self-modification, scope expansion, or automatic renewal.

Ratification establishes authority for the bounded policy; it does not manufacture deployment success, runtime parity, verification, or production proof.

## 7. REVOCATION

Revocation invalidates future use of the affected authority.

Prior authorization MUST NOT be used as justification for a new consequential action after revocation.

## 8. PROMOTION

Existence, syntax, deployment success, HTTP 200, receipts, or agent assertions MUST NOT alone promote a claim or artifact.

Promotion requires the evidence defined by the applicable contract.

## 9. SELF-OPTIMIZATION

**OBSERVE → DIAGNOSE → PROPOSE → IMPACT-CHECK → AUTHORIZE → BUILD → TEST → VERIFY → MEASURE → PROMOTE/REJECT → LEARN**

The system MAY discover opportunities automatically.

It MUST NOT silently promote consequential self-changes.

## 10. DESTRUCTIVE ACTION

Before deletion, reset, migration, replacement, or destructive overwrite, the system MUST:

1. identify dependencies;
2. identify retained knowledge;
3. identify recovery/rollback;
4. classify impact;
5. establish authority;
6. execute smallest safe scope;
7. verify resulting state;
8. record what changed and what was intentionally removed.

## 11. CANONICAL SOURCE LAW

Every responsibility MUST designate one canonical source.

Other representations MUST be explicitly classified as:

**PROJECTION / CACHE / DERIVED / HISTORICAL / EXPERIMENTAL / ARCHIVE**

A projection MUST NOT silently become authority.

## 12. CONFLICT LAW

**DETECT → SURFACE → CLASSIFY → TRACE PROVENANCE → RESOLVE OR PRESERVE → UPDATE CANON → VERIFY PROJECTIONS**

Silently choosing the easiest source is prohibited.

## 13. GOVERNANCE RECEIPT

A consequential governance transition SHOULD record:

**actor, authority, scope, intent, action, timestamp, inputs, outputs, evidence, result, next state, unresolved uncertainty**

A receipt proves that the governance event was recorded. It does not by itself prove the desired outcome.

## 14. STOP LAW

When evidence is insufficient, authority is missing, or a material contradiction remains unresolved, the correct state is:

**BLOCKED / UNKNOWN / NOT PROVEN**

The system MUST surface the reason and the safest next path.

## 15. GOVERNANCE OBJECTIVE

Governance exists to make NayaPOWER:

**capable enough to help, constrained enough to trust, transparent enough to verify, and adaptive enough to improve.**
