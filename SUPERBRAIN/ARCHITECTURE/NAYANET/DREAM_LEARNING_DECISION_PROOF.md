# NayaNET Dream → Learning → Later Decision Proof

This contract closes the first adaptive-learning boundary without creating a second identity, memory, authority, or execution system.

## Verified path

1. Authenticated human history is recorded in `nayanet_cognition_events` and receives the existing execution receipt.
2. `naya-dream-replay` creates an immutable, deterministic `SIMULATED` replay using that preserved history.
3. `learning_evidence` records the reusable claim and its provenance.
4. `naya-learning-apply` promotes that evidence into the canonical `learner_states` row, retaining lineage to the replay.
5. `naya-decision-context` reads only the canonical learner state and returns a deterministic later decision context.
6. The later decision is persisted as a cognition event with evidence ID, replay ID, policy version, influence flag, and authority invariants.
7. A fresh retrieval proves the decision remains traceable.

## Authority boundary

Learning changes what context is available to a later decision. It does not grant authority, authorize an action, or change production policy.

## What this proves

A real preserved human event can influence a later governed decision through:

`human history → verified receipt → Dream replay → learning evidence → learner state → later decision context → persisted proof`

The proof records **what changed**, **why it changed**, **which evidence supported it**, and **that authority remained unchanged**.

## What remains separate

This does not claim model-weight self-improvement. The decision boundary is deterministic and auditable first. A future Naya reasoning model can consume this governed context without becoming the authority source.
