# NIGHT 02 — OSCAR ARCHITECTURE ATTACK

## DIRECT COMMAND

Oscar: do not agree with Stage 01. Attack it.

Your job is to find where Team Naya has confused names with capabilities, documents with implementations, implementations with verification, or projections with sources of truth.

### OBJECTIVE
Independently challenge the 01–58 evidence matrix and proposed domain architecture.

### REQUIRED ATTACKS
1. Find every claim marked VERIFIED that lacks independent evidence.
2. Find every implementation claim supported only by documentation.
3. Find duplicate systems hidden under different names.
4. Find competing authority sources.
5. Find competing Activity/event stores.
6. Find Hub code that behaves as a source of truth.
7. Find runtime paths that bypass governance.
8. Find execution paths that can complete without Activity evidence.
9. Find state transitions that can claim VERIFIED without independent verification.
10. Find circular dependencies that cannot bootstrap.
11. Find agents that could certify their own changes.
12. Find destructive cleanup assumptions.
13. Find missing rollback/recovery paths.
14. Find any stage whose success cannot be mechanically detected.

### ADVERSARIAL TESTS
Deliberately construct negative cases where possible:
- missing event
- false verification flag
- stale state
- missing successor
- unauthorized action
- duplicate event
- replayed execution
- conflicting authority
- failed test hidden behind a green summary
- live runtime serving an unexpected source SHA

### REQUIRED OUTPUT
For each finding:
`SEVERITY / CLAIM / EVIDENCE / WHY IT FAILS / REQUIRED REPAIR / TEST TO PROVE REPAIR`

### DECISION
Return exactly one:
- PASS
- PASS_WITH_REPAIRS
- FAIL

Do not permit Stage 03 to start if a P0 architectural contradiction affects the execution spine.

### RECEIPT
Record canonical event + Activity + state + evidence + one successor: **NIGHT 03 EXECUTION SPINE**.