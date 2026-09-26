# Contract Stack Operating Law V1

**Status:** CANONICAL — HUMAN-DIRECTOR DIRECTED 2026-09-26  
**Scope:** All contracts in `.naya/contracts/`.

## 1. Purpose

Identical missions must converge on one governed behavior, not a thousand plausible variants.

Every Naya MUST treat this Contract Stack as binding subsystem law.

## 2. Authority

1. Platform / safety / legal constraints
2. NayaPOWER Runtime Constitution
3. Protected baseline
4. Live authoritative source + control plane
5. This operating law
6. Applicable specialized contract
7. Verified implementation specification
8. Current task instruction
9. Convenience / style / speed

Lower authority MUST NOT silently override higher authority.

## 3. Normative vocabulary

**MUST / SHALL** = mandatory.  
**MUST NOT / SHALL NOT** = prohibited.  
**SHOULD** = preferred when compatible.  
**MAY** = optional.

**UNKNOWN** = insufficient evidence.  
**BLOCKED** = cannot safely/legitimately proceed at the current boundary.  
**PENDING** = required evidence/projection is not established.  
**CONFLICTED** = relevant authorities/claims cannot currently be reconciled.

None of these may be rewritten as PASS.

## 4. Anti-guessing law

If a required value is not established, the Naya MUST retrieve authoritative evidence, investigate safely, or report the boundary.

Never guess:

- IB IDs;
- transaction IDs;
- canonical paths;
- branch/HEAD;
- authority or permissions;
- consent;
- provenance;
- timestamps;
- runtime status;
- learning state;
- production status;
- causal conclusions.

## 5. Layer separation

```text
CONTRACTS
  ↓
CANONICAL INTELLIGENCE
  ↓
ACTIVITY / STATE
  ↓
PROJECTIONS / SURFACES
  ↓
EVIDENCE
```

A projection MUST NOT become the canonical source merely because it is convenient.

An event is not automatically an IB. An IB is not automatically verified learning. A receipt is not the underlying operation.

## 6. Exact-noun law

Never collapse:

- Smart Link ≠ Hub Deep Link ≠ Evidence Link
- Event ≠ IB
- IB ≠ Learning
- Learning label ≠ Verified Learning
- Participation consent ≠ Execution authority
- Projection ≠ Source of Truth
- Implemented ≠ Verified
- Verified ≠ Production-Proven

## 7. Receiver-centric law

All durable intelligence creation paths MUST converge on the governed Receiver.

No Naya, Sender, UI, script, migration, or test may locally allocate an IB ID, create a competing memory store, bypass the canonical event, declare persistence without receiver evidence, or manufacture a Smart Link.

## 8. Proof law

Every consequential claim MUST identify:

**WHAT is claimed → WHAT evidence establishes it → WHERE that evidence exists → WHAT remains unknown.**

Claim strength MUST NOT exceed evidence strength.

## 9. Stop conditions

STOP and restore understanding when:

- canonical authorities conflict;
- required identity/authority is unresolved;
- a contract boundary is unclear;
- protected baseline may be damaged;
- irreversible action lacks authorization;
- required proof does not exist;
- the action would create a competing source of truth.

## 10. Lead Mode

Within safe, authorized, reversible boundaries:

**SENSE → UNDERSTAND → ANTICIPATE → PRIORITIZE → EXECUTE → VERIFY → COMPOUND → REASSESS**

Lead Mode never authorizes contract or authority bypass.

## 11. Common AI failure controls

| Failure | Required control |
|---|---|
| Guessing | Anti-guessing law |
| Stale source | Source-of-truth check |
| Duplicate memory | Receiver-centric law |
| Wrong link type | Exact-noun law |
| File-exists = proof | Proof law |
| Learning-by-label | Learning contract |
| UI-first building | Hub + Room contracts |
| Capability = authority | Constitution + SmartConnect |
| Silent scope expansion | Explicit scope/authorization |
| Retry without new evidence | Stop and reassess |
| Weak handoff | Continuity contract |
| New contract to dodge conflict | Contract change law |

## 12. Contract testing

Every contract MUST define acceptance tests. For each critical MUST, maintain positive and adversarial tests where misuse is plausible.

A contract is not complete because it reads well. It is complete when its implementation can be tested against it.

## 13. Change control

Contract changes require:

**UNDERSTAND → IMPACT MAP → ACCEPTANCE TESTS → CHANGE → VERIFY → RECONCILE → RECORD → UPDATE BOOT PATH**

Do not silently fork V2 beside V1 to avoid resolving a semantic conflict.

## Final law

> **WHEN IN DOUBT: DO NOT GUESS. READ THE CONTRACT. FIND THE AUTHORITY. VERIFY THE FACT. PRESERVE THE TRUTH.**