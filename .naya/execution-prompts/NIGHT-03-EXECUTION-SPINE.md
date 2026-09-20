# NIGHT 03 — BUILD THE EXECUTION SPINE

## DIRECT COMMAND

Naya Runtime + Naya Gov + Naya Event: build the smallest real governed execution spine. Do not build cosmetic Hub features until this works.

### TARGET
Implement/prove:
`RESTORE → PREFLIGHT → GOVERN → SELECT → EXECUTE → OBSERVE → VERIFY → CANONICAL EVENT → ACTIVITY → STATE → HANDOFF`

### START WITH EXISTING CODE
Inspect before editing:
- `.naya/runtime/execution_controller.py`
- `.naya/runtime/universal_execution_gate.py`
- `.naya/runtime/activity_event.py`
- `.naya/runtime/canonical_event_store.py`
- `.naya/runtime/evidence_runtime.py`
- `.naya/runtime/project_execution_contract.py`
- `.naya/governance/governance_kernel.py`
- authority registry/control-plane files

### REQUIRED IMPLEMENTATION
1. Create durable execution identity before consequential execution.
2. Load current mission/state.
3. Run machine-readable preflight.
4. Resolve authority using the exact machine-readable Authority Registry.
5. Reject unauthorized actions.
6. Execute only after the gate passes.
7. Observe the real result.
8. Verify independently where required.
9. Create the canonical Activity event at the actual execution boundary; do not merely require an actor-supplied event ID.
10. Project the event to Activity using the existing canonical architecture.
11. Update current state.
12. Write exactly one successor handoff.
13. Make completion impossible when required evidence is missing.

### TESTS
Create adversarial tests for:
- no preflight
- no authority
- missing Activity event
- fake Activity event
- mismatched execution ID
- unverified result
- duplicate execution
- replay
- missing successor
- valid execution

### IMPORTANT
Do not create a second event store or Activity database. Extend the existing canonical substrate.

### ACCEPTANCE
A substantive execution cannot reach VERIFIED/HANDED_OFF without its own canonical evidence chain.

### RECEIPT
Record implementation files, tests, exact passing/failing cases, canonical event, Activity, state, and successor: **NIGHT 04 INTELLIGENCE COMPOUNDING**.