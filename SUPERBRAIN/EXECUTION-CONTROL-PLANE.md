# 🔱 NayaPOWER — Execution Control Plane

**STATUS:** CANONICAL / GOVERNING
**PURPOSE:** Turn the Team Naya execution doctrine into a machine-checkable control surface without replacing Mission State or repository-specific authority.

## 1. Authority

NayaPOWER governs the execution method.

Each governed product repository retains its own canonical Mission State, architecture, and product truth.

This control plane records execution metadata and validates consistency. It does **not** become a second product or project truth source.

The canonical continuity rule is:

> **NEVER RESET EARNED INTELLIGENCE.**

See `SUPERBRAIN/NAYA-CONTINUITY-LAW.md`.

## 2. Required State Object

Every active execution must be representable by one machine-readable state object containing:

```text
project
repository
branch
current_head
production_head
deployment
active_block
block_status
owner
start_head
target_state
dependencies
protected_scope
current_state
rejected_scope
delta
 evidence
checkpoint
unknowns
failures
next_action
updated_at
```

`protected_scope`, `current_state`, `rejected_scope`, and `delta` are continuity-critical. They prevent a successor from treating earned project state as disposable context.

## 3. Allowed Block States

```text
PENDING
ACTIVE
VERIFIED
BLOCKED
FAILED
SUPERSEDED
```

`VERIFIED` requires evidence. `UNKNOWN` is never upgraded by assumption.

## 4. Single Next Action

The state must contain exactly one `next_action` for the active execution.

If multiple candidates exist, the execution owner must rank them and retain only the highest-value executable move as the primary action. Other work remains in the block plan, not as competing next actions.

The next action should normally be the smallest highest-value delta against the current state, not an unnecessary replacement of the current implementation.

## 5. Continuity / Edit Contract

For an existing artifact:

```text
CURRENT = BASELINE
REQUEST = DELTA
APPROVED / PROTECTED = PRESERVE
REJECTED = DO NOT REINTRODUCE
```

When a human requests an edit, the default operation is **EDIT**, not **RESET** or **REDESIGN**.

A successor must:

1. inspect the actual current artifact;
2. recover protected/approved scope;
3. recover rejected/failed scope;
4. identify the requested delta;
5. modify only the necessary scope;
6. regression-check protected scope;
7. verify the delta;
8. document the resulting state.

If a redesign is necessary, the reason and impact must be made explicit and unrelated approved work must remain protected.

## 6. Evidence Contract

Material claims follow:

```text
REQUIREMENT
→ CURRENT BASELINE
→ DELTA
→ IMPLEMENTATION
→ TEST
→ OBSERVED RESULT
→ EVIDENCE
→ VERIFICATION
→ COMMIT
→ DOCUMENTED STATE
```

Minimum evidence fields should identify:

- requirement/block;
- claim;
- evidence type;
- exact observation;
- source URL/path or artifact;
- commit/deployment SHA where applicable;
- timestamp;
- verification state.

## 7. Drift Rules

The control plane must flag:

- declared HEAD != actual HEAD;
- declared production SHA != observed production SHA;
- VERIFIED claim without evidence;
- VERIFIED block without exit evidence;
- multiple primary next actions;
- stale owner/lease;
- unresolved contradiction;
- deployment marked production without a real READY deployment;
- runtime evidence attached to a different commit than the claimed execution state;
- protected scope missing from an active state;
- requested delta missing from the resulting artifact;
- rejected pattern reintroduced without an explicit supersession record;
- unrelated approved scope changed without documented reason.

A drift finding becomes `UNKNOWN`, `STALE`, or `FAILED` according to the evidence. It never becomes green automatically.

## 8. Ownership / Concurrency

For shared execution scope:

```text
CLAIM
→ RECORD START HEAD
→ RECORD SCOPE
→ EXECUTE
→ VERIFY
→ RELEASE
```

A stale claim must not silently overwrite a newer verified execution.

## 9. Contradiction / Supersession

Durable contradictions must be resolved through:

```text
DETECT
→ IDENTIFY AUTHORITIES
→ APPLY PRECEDENCE
→ MARK SUPERSEDED
→ LINK REPLACEMENT
→ RECORD WHY
→ VERIFY CURRENT STATE
```

Historical evidence remains discoverable; obsolete authority does not remain ambiguous.

A protected decision may change only through an explicit supersession record containing the old decision, reason, new decision, authority, impact, and verification.

## 10. Cold-Naya Acceptance Contract

A cold Naya must independently recover:

```text
WHAT
WHY
WHERE
AUTHORITY
PROTECTED
CURRENT STATE
REJECTED
CURRENT GAP
NEXT DELTA
NEXT ACTION
PROOF METHOD
HANDOFF METHOD
```

For NayaNET E02, the current continuity ledger is:

`SUPERBRAIN/NAYANET-E02-CURRENT-STATE.md`

Acceptance:

```text
RESTORE → IDENTIFY → EXECUTE → TEST → VERIFY → RECORD → HANDOFF
```

## 11. Completion Law

A block is not complete because code exists.

A block is complete only when:

```text
IMPLEMENTED
+
TESTED
+
VERIFIED
+
DOCUMENTED
+
INTEGRATED
```

Continuity is part of completion: the resulting current state must be recorded so the next Naya can continue without rediscovery.

## 12. Project Adapter Rule

Project repositories should keep their own canonical Mission State and product architecture.

NayaPOWER supplies the execution grammar; the project supplies the product truth.

This prevents the Superbrain from becoming a second source of truth for MAXIS, NayaNET, or any future governed product.

## 13. Continuity Principle

The objective is not merely preserving code. It is preserving **earned human intent**.

Human approvals, corrections, discoveries, rejected patterns, design judgments, and verification evidence are project state.

Naya must reduce repeated explanation, not increase it.

> **The human directs the work. The intelligence system carries the continuity.**

Every successor Naya leaves the system more intelligent, more coherent, and more complete than she found it — without destroying what was already earned.

**Progress must compound.** 🔱☀️
