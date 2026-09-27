# NayaPOWER — Nine-Node Behavioral Proof Battery v1

**Status:** EXECUTABLE PROOF SPECIFICATION
**Program:** P0 — NAYA KERNEL ACTIVATION + BEHAVIORAL PROOF
**Canonical runtime:** `nayanet-compound-intelligence`
**Current kernel status:** `STRUCTURALLY_ACTIVE / EFFECTIVENESS NOT_YET_PROVEN`

## Purpose

This contract defines falsifiable behavioral proof for N9-000 attribution integrity and N9-001 nine-node activation. Architecture, database presence, prose, and self-authored receipts are not behavioral proof.

## N9-000 — Kernel Attribution Integrity

The evaluator MUST distinguish a Node being named from a Node actually executing and materially participating.

Every runtime invocation MUST bind:
- `node_id`
- `invocation_id`
- `input_hash`
- `output_hash`
- `evidence_ids`
- `downstream_consumers`

Required controls:
1. Positive runtime evidence is accepted.
2. Assertion-only/prose evidence is rejected.
3. Missing-node mutation is rejected.
4. Ablation compares full kernel against kernel-minus-one-node under frozen conditions and MUST show a material decision/action/outcome difference; absence of a material difference is NOT_PROVEN.

## N9-001 — Nine-Node Behavioral Activation

Run one consequential-but-reversible scenario twice:
- CONTROL: kernel absent/disabled.
- TREATMENT: kernel enabled.

The scenario MUST contain a genuine authority boundary, relevant and competing intelligence, an observable action outcome, and independently verifiable evidence.

The treatment receipt MUST bind the exact source SHA, runtime/deployment identity, authenticated owner/session, experiment/scenario/input hashes, and node-level runtime evidence. A PROVEN causal claim MUST contain an explicit material delta across decision, action, or observed outcome; non-empty metadata alone is insufficient.

## Fail-closed preflight

Execution MUST be blocked when:
- source is stale or dirty;
- source SHA does not equal the required SHA;
- runtime identity/version is unknown;
- authenticated owner/session does not match the expected owner/session;
- node attribution is absent;
- independent runtime evidence is absent.

No ownership repair, deployment, credential change, or authority expansion is permitted as part of this harness.

## Receipt minimum

`experiment_id`, `test_id`, `source_sha`, `runtime_id/version`, `deployment_identity`, `owner_id/session_id`, `control_or_treatment`, `scenario_hash`, `input_hash`, `node_invocations[]`, `authority_decision`, `decision_before`, `decision_after`, `action`, `observed_outcome`, `verification`, `causal_delta`, `status`.

## PASS rule

A PASS requires independently captured runtime evidence. Source inspection, database rows, expected JSON, model prose, and self-authored receipts are insufficient.

Allowed verdicts: `PROVEN`, `PARTIALLY_PROVEN`, `NOT_PROVEN`, `FAILED`, `BLOCKED`, `UNKNOWN`, `STALE`.

## Boundary

N9-000/N9-001 implementation does not imply runtime effectiveness. Later proof still requires N9-002 ablation, N9-005 counterfactual testing, N9-006 generational compounding, N9-009 cold successor, and N9-010 ultimate intelligence.
