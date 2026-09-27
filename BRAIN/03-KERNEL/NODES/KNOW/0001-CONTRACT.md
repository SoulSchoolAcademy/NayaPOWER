# KNOW Node Contract V1

**ID:** NAYA-KERNEL-KNOW

## Purpose

KNOW preserves and serves canonical semantic intelligence, events and memory. It is the knowledge organ of the kernel, responsible for maintaining the intelligence substrate.

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
- Current knowledge state summary
- Retrieval results with provenance

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
- Allow retrieval without authorization check.

## Acceptance Criteria

- All canonical objects have stable identity and provenance.
- Intelligence is retrievable by semantic, structural, and contextual queries.
- Lifecycle state is accurate and current.
- Classification follows the canonical type system.
- Retrieval results include epistemic state.

## Failure States

| Failure | Behavior |
|---|---|
| Object identity collision | Halt; resolve before proceeding |
| Provenance missing | Mark as UNVERIFIED; do not serve as canonical |
| Retrieval returns stale data | Trigger re-index; serve with STALE marker |
| Classification unknown | Mark as UNKNOWN; do not guess |
| Index corruption | Rebuild index; alert |
