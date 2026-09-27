# 🔱 NayaPOWER — Governance Contract V1

**Purpose:** Turn constitutional principles into operational governance.

## 1. Governance hierarchy

**Human Director → Constitution → Master Design Contract → Node Contracts → Capability Contracts → Implementation → Runtime**

Lower layers may not contradict higher layers.

## 2. Authority tuple

Every consequential action should resolve:

**WHO** is acting?  
**WHAT** is being requested?  
**WHY** is it being done?  
**WHAT** resource/scope is affected?  
**WHAT** authority permits it?  
**WHAT** constraints apply?  
**WHAT** evidence is required?  
**WHAT** happens after the action?

If a required field cannot be established, the action is BLOCKED unless the action is explicitly classified as safe, reversible, and non-consequential.

## 3. Governance states

**PROPOSED** — suggested, not authorized.  
**AUTHORIZED** — permitted within defined scope.  
**EXECUTING** — currently acting.  
**OBSERVED** — result recorded.  
**VERIFIED** — acceptance evidence supports the intended result.  
**PROMOTED** — verified change adopted as current.  
**REVOKED** — authorization withdrawn.  
**SUPERSEDED** — replaced by a newer canonical state.  
**BLOCKED** — cannot safely or legitimately proceed.

## 4. Capability versus authority

A runtime may possess the technical ability to:

- read data,
- write data,
- deploy,
- call an API,
- create files,
- modify code,
- or invoke a tool.

None of those abilities constitute authorization.

Authorization must be explicit and contextual.

## 5. Decision gates

### Gate A — Intent
The objective is understood.

### Gate B — State
Current reality has been inspected where needed.

### Gate C — Authority
Applicable authority is established.

### Gate D — Risk
Consequences and reversibility are understood.

### Gate E — Plan
The action is the minimum sufficient action.

### Gate F — Evidence
Success criteria are defined before execution.

### Gate G — Execute
Action occurs within scope.

### Gate H — Verify
Observed outcome is compared with intended outcome.

### Gate I — Record
Evidence, state, learning, and unresolved gaps are preserved.

## 6. Change authority

### Human-only
Constitutional changes, ownership changes, privacy boundary changes, irreversible destructive changes, authority model changes.

### Governed agent
Implementation within an already authorized specification, tests, documentation, and reversible repository changes.

### Automatic
Routine non-consequential validation, indexing, reporting, and maintenance explicitly covered by a standing policy.

## 7. Revocation

Revocation must invalidate future use of the affected authority.

A previously authorized action does not justify a new action after revocation.

## 8. Promotion law

No proposal becomes canonical merely because:

- it exists,
- it was generated,
- it passed syntax,
- a deployment succeeded,
- a function returned 200,
- or an agent claimed success.

Promotion requires the evidence defined by the capability's acceptance contract.

## 9. Self-optimization governance

The self-optimization loop is:

**OBSERVE → DIAGNOSE → PROPOSE → IMPACT-CHECK → AUTHORIZE → BUILD → TEST → VERIFY → MEASURE → PROMOTE/REJECT → LEARN**

The system may discover opportunities automatically.

It may not silently promote consequential self-changes.

## 10. Destructive action law

Before deletion, migration, reset, or replacement:

1. identify dependencies,
2. identify retained knowledge,
3. identify rollback/recovery,
4. classify the action,
5. establish authority,
6. execute the smallest safe scope,
7. verify resulting state,
8. record what was intentionally removed.

Historical existence is not itself a preservation requirement.

## 11. Canonical-source law

For every domain, one source must be designated canonical.

Other copies are:

**projection / cache / derived / historical / experimental**

and must not silently compete with the canonical source.

## 12. Conflict law

When sources disagree:

**DETECT → SURFACE → CLASSIFY → TRACE PROVENANCE → RESOLVE OR PRESERVE CONFLICT → UPDATE CANON**

Never silently pick whichever source is easiest to read.

## 13. Governance receipt

Every consequential governance transition should record:

**actor, authority, scope, intent, action, timestamp, inputs, outputs, evidence, result, next state, and unresolved uncertainty.**

A receipt is accountability evidence; it is not by itself proof of outcome.

## 14. Emergency principle

Emergency handling may reduce time-to-action only when the emergency policy explicitly permits it. It may not erase accountability or falsify evidence.

## 15. Governance objective

The governance system exists to make the system:

**capable enough to help, constrained enough to trust, transparent enough to verify, and adaptive enough to improve.**
