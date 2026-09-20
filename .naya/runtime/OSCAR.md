# Naya Power — Independent Oscar Runtime

Oscar is the independent adversarial challenge layer between builder verification and promotion.

## Boundary

```text
CLAIM
  ↓
EVIDENCE
  ↓
BUILDER VERIFICATION
  ↓
OSCAR CHALLENGE
  ↓
PROMOTION DECISION
```

Oscar deliberately does **not** import `evidence_runtime.py`. Its independence is structural: it evaluates the verification package through a separate implementation and can reject packages that the builder verifier accepts.

## Current deterministic checks

Oscar rejects:

- claims that are not presented as VERIFIED;
- missing evidence;
- forbidden evidence methods (`model_assertion`, `memory_assertion`, `user_assertion`, `retrieved_content`);
- non-PASS evidence;
- cross-claim evidence;
- missing commands, observed output, timestamps, or commit binding;
- evidence bound to the wrong commit;
- missing explicit coverage for any success criterion.

Oscar emits a machine-readable verdict with reasons and a `promotion_allowed` decision.

## Important boundary

This is **not** a semantic reasoning model. Deterministic Oscar can verify structural/provenance constraints and explicit machine-readable criterion coverage. It cannot independently determine whether arbitrary natural-language output semantically proves a criterion. That remains a future capability and must not be represented as implemented.

## CLI

```bash
python .naya/runtime/oscar.py CLAIM.json EVIDENCE.json --commit "$GITHUB_SHA"
```

A zero exit status means Oscar accepted the package. A non-zero exit status means promotion must be rejected.

## Tests

```bash
python .naya/runtime/test_oscar.py
```

The Claim Evidence CI workflow executes Oscar after builder verification and publishes the resulting machine-readable artifact.
