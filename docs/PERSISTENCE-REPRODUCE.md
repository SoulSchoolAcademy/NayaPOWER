# Reproduce — persistence seam package

All commands are read-only except where marked. No credentials are in this package.

## 1. Adapter unit tests (no database)

```bash
# from the repo root at the package commit
python -m pytest tests/test_persistence_seam.py -q
```

Expected: all 15 tests pass (pytest-discoverable; also runs under the repo's
normal `python -m pytest -q`). Covers: valid payload, missing metadata,
invalid types, hash-mismatch tamper, source/config shape, ownership shape,
forced UNVERIFIED at insert, successor parent shape, lineage threading,
idempotency-key shape, seal validation (numeric/null/malformed receipt_hash
rejected), receipt vocabulary (verdict/timestamp/decision_id types),
input-commitment (inputs_hash recomputation; legacy labeled absent-legacy),
interop against Naya 4's real `seam-verify-001` receipt
(tests/fixtures/seam-verify-001.json), contract-record validation.

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

## 3. Isolated database exercise (NOT run by Naya 2 — no local Postgres here)

Reproducible setup, using only repo files:

```bash
# 1. Start Postgres 16 with pgcrypto available
docker run -d --name naya-seam-test -e POSTGRES_PASSWORD=test -p 5433:5432 postgres:16

# 2. Prepare the database
psql -h localhost -p 5433 -U postgres -c "CREATE SCHEMA extensions;"
psql -h localhost -p 5433 -U postgres -c "CREATE EXTENSION pgcrypto WITH SCHEMA extensions;"

# 3. Apply all migrations in order (pinned SHA: a726a8376559609a3620f948ec7bfcabdba50abb)
for f in $(ls supabase/migrations/*.sql | sort); do
  psql -h localhost -p 5433 -U postgres -d postgres -v ON_ERROR_STOP=1 -f "$f"
done
# NOTE: the two external history versions (20260930233038, 20260930233137) have no
# repo files; their SQL is recoverable from production
# supabase_migrations.schema_migrations.statements (read-only) if needed.

# 4. Exercise the seam function (as service_role equivalent = postgres superuser here)
psql -h localhost -p 5433 -U postgres -d postgres <<'EOF'
-- owner isolation: authenticated callers are checked via auth.uid();
-- here we call as superuser (auth.uid() IS NULL, like service_role).
SELECT ledger_event_id, event_hash, status
FROM public.nayanet_record_ledger_event(
  '12345678-1234-1234-1234-123456789abc',  -- p_owner_id (must be a real auth.users id in prod)
  'DECISION', 'naya_kernel_decision', 'dec-001',
  now(), NULL, 'PRIVATE', 'RECORDED', '[]'::jsonb, '{"state":"UNVERIFIED"}'::jsonb,
  '{"decision_id":"dec-001"}'::jsonb, '{}'::jsonb, '[]'::jsonb, '{}'::jsonb, NULL
);
-- duplicate write returns the SAME row (idempotency), no second row:
SELECT count(*) FROM public.nayanet_smart_ledger
WHERE owner_id='12345678-1234-1234-1234-123456789abc' AND source_id='dec-001';
EOF

# 5. Tear down
docker rm -f naya-seam-test
```

**Limitation (stated, not hidden):** Naya 2 has no local Postgres and no authorized
disposable cloud environment, so step 3–4 above is published but not executed by Naya 2.
Static schema/constraint mapping is documented in `docs/PERSISTENCE-SEAM-SPEC-V1.md`
and is not represented as DB integration. Any seat with Docker can run it.

## 4. What "done" looks like for the DB exercise

- `nayanet_record_ledger_event` inserts one row; duplicate call returns the same
  `ledger_event_id` (no second row).
- `LEDGER_OWNER_MISMATCH` fires when an authenticated caller passes a different
  `p_owner_id` than `auth.uid()`.
- `event_hash` recomputes deterministically from the stored row
  (`nayanet_smart_ledger_hash` over the same inputs).
- After migration `20261001032000` is applied, the three V2.1 functions exist and
  `nayanet_validate_v2_1_value_receipt` accepts/rejects per its rules.
