# Claim → Evidence → Verification Runtime

The evidence layer prevents unsupported claims from becoming `VERIFIED` state.

## Contract

A **claim** states what is asserted and how success is defined. An **evidence record** records an observed result, method, command, commit, environment, and provenance. Verification is a runtime decision over those records.

`CLAIM ≠ EVIDENCE ≠ VERIFICATION`

A claim may be `VERIFIED` only when it has at least one passing evidence record whose commit matches the verification target. Model assertions, memory assertions, user assertions, and retrieved content are explicitly prohibited as evidence-producing methods.

## Commands

```text
python .naya/runtime/evidence_runtime.py validate
python .naya/runtime/evidence_runtime.py verify <claim_id>
```

For deterministic verification against a known revision:

```text
python .naya/runtime/evidence_runtime.py validate --commit <sha>
python .naya/runtime/evidence_runtime.py verify <claim_id> --commit <sha>
```

## Evidence freshness

Evidence is tied to the commit it observed. Historical evidence remains useful as historical evidence, but it cannot silently promote a changed current repository to `VERIFIED`.

## CI rule

CI must generate or validate evidence from the exact checkout under test. A green workflow is evidence only when its success criteria, observed output, and commit identity are recorded or deterministically reproducible.
