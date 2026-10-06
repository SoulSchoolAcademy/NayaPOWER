# PROVENANCE-CHAIN EXTENSION V1 — AI Operating Specification

**Status:** PROPOSED — awaiting Human Director ratification.
**Scope:** Proposed extension to the ACT/LAW machine contracts. Adds a required input, not new states or new nodes. Does not override any ratified contract.
**Precedence:** On conflict with ACT/LAW ratified contracts, those contracts win. This spec specifies *what* provenance must be carried and how chain failures resolve.

## 1. The extended chain (exact)

`INTENT → PROVENANCE → UNDERSTANDING → AUTHORITY → DECISION → ACTION → EVIDENCE → RESULT → LEARNING → MEMORY → NEXT_ACTION`

PROVENANCE sits between INTENT and UNDERSTANDING: understanding must come after the source is known. An intent with unknown source is data, never instruction.

## 2. Provenance record (exact schema — machine twin carries the JSON schema)

Every delegated intent carries one record, updated at each hop:

- `originator` — who first formed the intent (actor identity, bound)
- `authorizer` — who granted authority for it (actor identity, bound), with grant scope and expiry
- `modifications` — ordered list; each: `hop_actor`, `what_changed`, `authority_invoked`, `timestamp`
- `transmissions` — ordered hop list; each: `from → to`, `timestamp`, `channel`
- `executor` — who executed it (bound identity)
- `authority_accompaniment` — the authority present at each hop, so non-expansion is checkable

## 3. Chain rules (exact predicates)

- `provenance_required`: no provenance record → the intent is UNKNOWN-provenance → cannot authorize action. This is a fail-closed rule, not a warning.
- `provenance_walkable`: every hop must resolve to a bound identity and a stated authority. An unwalkable hop → the whole chain is unwalkable → UNKNOWN-provenance.
- `authority_non_expansion`: `authority_at_hop_n ⊆ authority_at_hop_(n-1)`. Violation → refuse the intent, record the attempt as evidence.
- `modification_attributed`: any change to the intent across a hop must appear in `modifications`. Silent modification → the record is corrupt → fail closed.
- `collective_resolves`: a chain ending at COLLECTIVE must name the mechanism that produced the intent. Unresolvable → not an authority.

## 4. ACT/LAW integration (how the extension attaches)

- **ACT:** each state transition (PLANNED → AUTHORIZED → EXECUTING → COMPLETED/FAILED/ROLLED_BACK) gains a required input: the provenance record for the intent being executed. ACT's states and transitions are unchanged.
- **LAW:** authorization gains a precondition — the authorization is valid only against a walkable, non-expanding provenance chain. LAW's permission/consent/scope model is unchanged.
- **PROVE:** provenance verification is PROVE's natural home (provenance + truth limits) — cited, not redefined.

## 5. The Smart Ledger (conceptual anchor)

The extended chain, persisted across executions, is the Smart Ledger: "the memory of intelligence in action." Each entry: the full chain for one intent, from originator to learning. The ledger is how a cold successor, or an auditor, answers: *where did this instruction come from, and who was allowed to give it?*

## 6. Failure handling

- Provenance loss at any point → fail closed (halt; do not proceed on the intent).
- Authority expansion detected → refuse the intent; record the attempt as evidence (reputation input for the delegating actor).
- Corrupt record (silent modification) → quarantine the intent; escalate.

## 7. Cite, don't duplicate

- `NAYANODE/00-ACT-MASTER-CONTRACT-V1.md` — state machine, invariants, acceptance battery (provenance-loss detection).
- `BRAIN/03-KERNEL/NODES/LAW/0001-CONTRACT.md` — permission/consent/scope.
- `BRAIN/10-INTERFACES/0004-INTELLIGENCE-IDENTITY-TRUST-PROTOCOL-V1` — the envelope PROVENANCE field uses this record format.
- `BRAIN/03-KERNEL/NODES/PROVE/` — provenance + truth limits home (cited).

## 8. Enforcement status

Not enforceable until ratified. Named CI follow-ups: provenance-record schema check on governed actions; a chain-walk battery (valid passes; broken/modified/unknown-source fails closed). Proposals, not faked enforcement.
