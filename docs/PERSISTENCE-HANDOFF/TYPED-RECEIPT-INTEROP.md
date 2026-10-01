# Typed-Receipt Interoperability Map (Move 8)

**Principle:** each receipt keeps its legitimate meaning, identity, producer,
and proof level. No fields are manufactured to route one family through
another family's path.

## The five distinct artifacts

| # | Artifact | Producer | Path to ledger | Proof level |
|---|----------|----------|----------------|-------------|
| 1 | Kernel.decide() receipt | naya_kernel (`nine-node-kernel-v1`) | `kernel/persistence_seam.py` adapter → `nayanet_record_ledger_event` (direct) | `receipt_hash` recomputed by adapter; `inputs_hash` recomputed from preserved state |
| 2 | ACT execution receipt | Naya 4's runtime (`dec-demo1-live-001` family) | `nayanet_execution_receipt_to_ledger()` trigger fn → `nayanet_record_ledger_event` | Execution status → ledger status mapping (SUCCESS→VERIFIED, etc.) |
| 3 | Typed value receipt (ALIGNMENT_DECISION / CONTRIBUTION_VALUE) | Decision Value Calculus V2.1 | `nayanet_attach_value_receipt_v2_1` | `nayanet_value_receipt_v2_1_state` → ASSESSED / VERIFIED_VALUE / REJECTED |
| 4 | Database ledger event | `nayanet_record_ledger_event` (SECURITY DEFINER) | — (it IS the ledger) | `event_hash` chain; idempotency on (owner, source_table, source_id) |
| 5 | Independent verification result | Fresh consumer (Coda 4) | Read-only | Recomputation from the row alone |

## Boundary agreement (Naya 4)

- **Kernel receipts** (family `naya-receipt-contract/1`, with `decision_id`,
  `kernel_version`, `verdict`) → the adapter. This is the only family the
  adapter accepts.
- **ACT execution receipts** (family `dec-demo1-live-001`, missing the
  kernel fields) → the execution-receipt table → trigger →
  `nayanet_record_ledger_event`. The adapter's honest REFUSAL of
  `dec-demo1-live-001` is correct routing, not a gap: it belongs to path 2,
  not path 1. No joint contract extension is needed to *store* it; one would
  only be needed if we wanted the adapter to *validate* it (we don't —
  that's the trigger's job).
- **Typed value receipts** → the V2.1 functions. Verified live in the
  disposable DB: `nayanet_value_receipt_v2_1_state` returns ASSESSED for a
  valid ALIGNMENT_DECISION, raises `VALUE_RECEIPT_TYPE_UNSUPPORTED` /
  `ALIGNMENT_DECISION_REQUIRED_FIELDS` for invalid input.

## What recomputation means per artifact (not conflated)

- `receipt_hash` recomputation: adapter re-hashes the kernel receipt body
  with the kernel's canonicalization. Proves the receipt is intact.
- `inputs_hash` recomputation: fresh consumer re-hashes the preserved
  `inputs_state` from the row. Proves the inputs are intact. (Needs the
  state — hence cold-recomputation closure.)
- Ledger event/hash-chain verification: `event_hash` recomputed from the
  stored row via `nayanet_smart_ledger_hash`. Proves the ledger entry is
  intact and chained.
- Value Calculus result recomputation: needs candidate/baseline/profile
  evidence (Coda 1 / Naya 4). Preserving input bytes is necessary but not
  sufficient — the calculator's result is not reconstructed from bytes
  alone. Open coordination item.
- Observed outcome verification: never at insert time (UNVERIFIED, empty
  outcome). A separate verification event, not a field on the receipt.

## V2.1 disposable-DB evidence (2026-10-01)

- Migration `20261001032000` applied to `naya_isolated_rt` (needed
  `service_role` created first — same role-existence class as the `anon`
  grant fix).
- `nayanet_value_receipt_v2_1_state`: valid ALIGNMENT_DECISION → ASSESSED;
  bogus type → `VALUE_RECEIPT_TYPE_UNSUPPORTED`; missing fields →
  `ALIGNMENT_DECISION_REQUIRED_FIELDS`.
- The three trigger functions exist; no `CREATE TRIGGER` in the migration —
  trigger attachment is a separate step (not done here; no production
  application under this directive).
