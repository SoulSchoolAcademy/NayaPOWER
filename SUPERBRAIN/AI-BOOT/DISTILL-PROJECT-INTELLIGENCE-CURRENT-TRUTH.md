# 🔱 DISTILL — PROJECT INTELLIGENCE CURRENT TRUTH

**Project:** NayaNET  
**Substrate:** NayaPOWER  
**Authority:** canonical events + existing control plane + verified evidence  
**Role:** rebuildable derived context for every Naya

## ONE SENTENCE

Project Intelligence is the deterministic reconstruction of one project's authorized canonical experience into **current, historical, superseded, stale, conflicted, unknown, evidence, and causal-lineage views**. It is not a second memory store.

## SYSTEM 54 CONTRACT

`current[]` is the **current epistemic-claim view** of Project Intelligence. It is not the operational control-plane state and it is not a list of verified execution records.

- **Operational current state** belongs to `.naya/control-plane/STATE.json` (with BLOCKS/MAP/PROOF as the canonical operational control plane).
- **Project Intelligence `current[]`** contains claims resolved as current under this document's epistemic rules.
- **Verification is evidence about a record; currentness is a separate classification.** A record may be VERIFIED and still be HISTORICAL, SUPERSEDED, STALE, CONFLICTED, or otherwise not current.
- **Activity/execution records remain history** unless a separate canonical claim explicitly establishes a current epistemic state.
- Project state is carried separately in the reconstructed `project_state` field; it must never be inferred from `current[]`.

## CURRENT-TRUTH LAW

```
AUTHORIZED EVENTS
 → EXISTING SUBJECT
 → EFFECTIVE TIME ORDER
 → EXPLICIT SUPERSESSION
 → REMOVE SUPERSEDED / STALE FROM CURRENT
 → PRESERVE HISTORY
 → TEST ACTIVE COMPETING CLAIMS
 → USE EXISTING VERIFICATION / EVIDENCE / AUTHORITY
 → RESOLVE ONLY WHEN THE RECORD SUPPORTS RESOLUTION
 → OTHERWISE CONFLICTED / UNKNOWN
 → PROJECT CONTEXT
 → COLD NAYA
 → ONE NEXT ACTION
```

### Non-negotiable

1. Recency orders; it does not prove truth.
2. Explicit `supersedes` / `superseded_by` establishes lineage.
3. `SUPERSEDED` and `STALE` never become CURRENT.
4. Multiple unresolved active claims about the same existing `subject` are CONFLICTED.
5. A uniquely stronger candidate may become CURRENT only when its existing verification has explicit evidence and it strictly outranks competing active candidates; verification without evidence cannot resolve anything.
6. Equal-strength verified candidates remain CONFLICTED; recency is only a tie-breaker for deterministic ordering inside an already resolved class, never proof of truth.
7. Unknown remains UNKNOWN.
8. Unauthorized events never enter reconstruction.
9. Historical truth remains recoverable.
10. Every current claim carries evidence and causal lineage.
11. Canonical events remain the authority; reconstruction is rebuildable.

## COLD-NAYA PACKET

A cold Naya receives:

**WHO** project identity  
**WHY** mission / north star  
**CURRENT** resolved claims  
**HISTORY** historical + superseded + stale  
**CONFLICT** unresolved competing claims  
**UNKNOWN** unresolved uncertainty  
**PROOF** evidence / verification  
**LINEAGE** source / parent / relationship chain  
**STATE** current operational state  
**NEXT** exactly one next action  
**AUTHORITY** what may be executed

## CONTINUATION

The successor does not restart. It reads the reconstructed context, resolves live HEAD, verifies state, takes the one authorized next action, observes the actual outcome, records learning, and leaves a better successor state.

> **What is true now, why is it current, what proves it, what remains unresolved, and what is the next authorized thing to do?**
