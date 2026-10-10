# Reproduce — persistence seam package

All commands are read-only except where marked. No credentials are in this package.

## 1. Adapter unit tests (no database)

```bash
# from the repo root at the package commit
python -m pytest tests/test_persistence_seam.py -q
```

Expected: all 24 tests pass (pytest-discoverable; also runs under the repo's
normal `python -m pytest -q`). Covers: valid payload, missing metadata,
invalid types, hash-mismatch tamper, source/config shape, ownership shape,
forced UNVERIFIED at insert, successor parent shape, lineage threading,
idempotency-key shape, seal validation (numeric/null/malformed receipt_hash
rejected), receipt vocabulary (verdict/timestamp/decision_id types),
input-commitment (inputs_hash recomputation; legacy labeled absent-legacy),
interop against Naya 4's real `seam-verify-001` receipt
(tests/fixtures/seam-verify-001.json), detached snapshots (caller mutation
cannot invalidate projected evidence; non-JSON values rejected), substantive
contract-record validation (timestamps, vocabularies, lineage, provenance).

## 2. Boundary validator (ad-hoc)

```bash
python3 - <<'EOF'
from kernel.persistence_seam import project_kernel_receipt, verify_kernel_receipt
# receipt: any dict produced by naya_kernel Kernel.decide()
# owner_id: the authenticated user's uuid (auth.uid())
params = project_kernel_receipt(receipt, owner_id='<uuid>', kernel_sha='<40-hex>')
print(params['p_source_id'], params['p_verification'])
EOF
```

## 3. Isolated database exercise (EXECUTED 2026-10-01 — 14/14 PASS)

The full runnable handoff lives in `docs/PERSISTENCE-HANDOFF/` (README,
schema, proof runner, reconstruction code). Summary of the executed run:

```bash
# 1. Disposable local Postgres 16; two login roles (rt_owner_a, rt_owner_b)
# 2. Target-identity check: inet_server_addr()=127.0.0.1, db=naya_isolated_rt
# 3. Schema: docs/PERSISTENCE-HANDOFF/isolated-schema.sql
#    (ledger subset of 20260919015207, ON_ERROR_STOP=1; p_learning_refs
#    default normalized [] — the migration's {} is a jsonb type error)
psql -U postgres -d naya_isolated_rt -v ON_ERROR_STOP=1 \
  -f docs/PERSISTENCE-HANDOFF/isolated-schema.sql
# 4. Boundary proof (write → terminate producer → fresh process → read):
python3 docs/PERSISTENCE-HANDOFF/isolated_roundtrip.py
# Expected: exit 0, "14/14 checks passed"
```

**Evidence (2026-10-01):** receipt seal MATCH; projection accepted;
verification honestly UNVERIFIED; no invented timestamps; canonical writer;
chain hash; identical replay → same row; conflicting payload → no overwrite;
fresh-process read; 12-field reconstruction 0 violations; receipt_hash and
inputs_hash recompute MATCH from the row alone; owner B sees 0 rows.
Proof log: `roundtrip-proof-2026-10-01.txt` (sha256
`7dcd265ecb4eb137b2b57f3b9667a62651bd5328915b3800a1a1673f4773013f`);
written ledger row `79404825-97a5-407c-a350-5820e51f50f3`.

**Limitations (stated, not hidden):** the disposable schema is the ledger
writer subset (V2.1 typed-receipt functions exercised separately); the proof
used the `demo-001` kernel receipt, not the Demo-1 ACT receipt (different
family, honestly refused pending a joint contract extension); owner isolation
proven at RLS policy level with two login roles.

## 4. What "done" looks like for the DB exercise

- `nayanet_record_ledger_event` inserts one row; duplicate call returns the same
  `ledger_event_id` (no second row).
- `LEDGER_OWNER_MISMATCH` fires when an authenticated caller passes a different
  `p_owner_id` than `auth.uid()`.
- `event_hash` recomputes deterministically from the stored row
  (`nayanet_smart_ledger_hash` over the same inputs).
- After migration `20261001032000` is applied, the three V2.1 functions exist and
  `nayanet_validate_v2_1_value_receipt` accepts/rejects per its rules.
