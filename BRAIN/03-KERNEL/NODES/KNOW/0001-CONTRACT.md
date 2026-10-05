# KNOW Node Contract V1

**ID:** NAYA-KERNEL-KNOW

## Purpose

KNOW preserves and serves canonical semantic intelligence, events and memory. It owns canonical intelligence-object identity, meaning, lifecycle, provenance and durable reconstruction. PROVE owns epistemic claim assessment; CONNECT owns task/context applicability and relationship-aware selection.

## Inputs

- Canonical objects and events from intelligence layer
- Memory retrieval requests
- Classification and typing rules
- Provenance records
- Lifecycle state updates

## Outputs

- Canonical intelligence context
- Events and observations
- Checkpoints and state snapshots
- Current intelligence-object lifecycle/temporal summary
- Retrieval candidates with provenance, evidence references and uncertainty metadata

## MUST Rules

- Distinguish event from understanding.
- Preserve canonical identity and provenance.
- Preserve lifecycle state and lineage.
- Make durable intelligence retrievable.
- Classify all incoming material by type and epistemic state.
- Maintain indexes for efficient retrieval.

## MUST NOT Rules

- Treat raw logs, notes or database rows as intelligence automatically.
- Promote unclassified source material silently.
- Collapse knowledge type into epistemic state.
- Serve intelligence without provenance.
- Allow owner/scope-ineligible retrieval.
- Treat retrieval as truth, applicability, or authority.
- Promote final truth or task-level applicability; those belong to PROVE and CONNECT.

## Acceptance Criteria

- All canonical objects have stable identity and provenance.
- Intelligence is retrievable by semantic, structural, and contextual queries.
- Lifecycle state is accurate and current.
- Classification follows the canonical type system.
- Retrieval candidates include current lifecycle/temporal state, provenance and evidence references.
- Any applicability metadata is treated as candidate/context input until CONNECT resolves task-level applicability.

## Failure States

| Failure | Behavior |
|---|---|
| Object identity collision | Halt; resolve before proceeding |
| Provenance missing | Mark as UNVERIFIED; do not serve as canonical |
| Retrieval returns stale data | Trigger re-index; serve with STALE marker |
| Classification unknown | Mark as UNKNOWN; do not guess |
| Index corruption | Rebuild index; alert |
