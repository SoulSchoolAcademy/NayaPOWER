# Intelligence Lifecycle V1

**Status:** CANONICAL SPECIFICATION — transition receipt law defined

```
EXPERIENCE
→ CAPTURE
→ DISTILL
→ STRUCTURE
→ CONNECT
→ PROVE
→ PRESERVE
→ RETRIEVE
→ APPLY
→ ACT
→ OUTCOME
→ VERIFY
→ LEARN
→ COMPOUND
→ SUCCESSOR
→ EVOLVE
```

Every durable transition must preserve lineage and explicit status.

## Transition receipt

Each durable transition MUST be attributable to:

- subject/object identity;
- source state;
- target state;
- actor/runtime identity;
- authority context when required;
- evidence references;
- timestamp;
- result;
- failure reason when not completed.

## Truth-state separation

The lifecycle MUST preserve these distinctions:

```
EVENT ≠ INTERPRETATION
INTERPRETATION ≠ LEARNING
LEARNING ≠ VERIFIED LEARNING
RETRIEVAL ≠ AUTHORIZATION
ACTION ≠ OUTCOME
OUTCOME ≠ VERIFICATION
VERIFICATION ≠ PRODUCTION PROOF
SUCCESSOR CONTEXT ≠ INHERITED AUTHORITY
```

## Failure law

A failed or blocked transition remains a first-class event/receipt where operationally relevant. It MUST NOT be rewritten as success.

## Completion law

A lifecycle stage is complete only when its acceptance condition is satisfied. A downstream stage cannot retroactively prove an upstream stage that was never evidenced.

## Canonical runtime target

The eventual living runtime must make the lifecycle observable as one lineage:

```
INTENT
→ RETRIEVE
→ GOVERN
→ ACT
→ OBSERVE
→ VERIFY
→ LEARN
→ VALUE
→ HANDOFF
```

The BRAIN documents the contract; runtime evidence determines which stages are actually live.
