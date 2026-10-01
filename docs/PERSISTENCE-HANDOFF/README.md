# Disposable-DB Handoff — persistence seam write → fresh-read proof

**What this is:** the complete runnable package for the isolated persistence
boundary proof. Another worker can reproduce the 14/14 write → fresh-process
read evidence without the original author's computer or hidden context.

**What it is not:** a production migration, a deployment, or a second
persistence path. It exercises the existing `nayanet_record_ledger_event`
writer and the `kernel/persistence_seam.py` adapter against a disposable
local database.

## Prerequisites

- PostgreSQL 16 with `pgcrypto` available (local install or container).
- Python 3.10+ with `psycopg` (`pip install psycopg`).
- The repo checked out at the adapter commit under test.
- **No production credentials.** The target database must be disposable and
  local. Verify before writing (see §1).

## 1. Establish the disposable target (do this first)

```bash
# Create a disposable database and two owner roles. This is a LOCAL,
# throwaway database — never point these scripts at a production URL.
sudo -u postgres psql -v ON_ERROR_STOP=1 <<'EOF'
CREATE DATABASE naya_isolated_rt;
CREATE ROLE rt_owner_a LOGIN;
CREATE ROLE rt_owner_b LOGIN;
EOF
```

Target-identity check (not just a URL refusal): confirm the server is local
and the database is the disposable one before any write:

```bash
psql -U postgres -d naya_isolated_rt -tAc \
  "SELECT inet_server_addr(), current_database();"
# Expected: 127.0.0.1 (or local socket) | naya_isolated_rt
```

## 2. Apply the schema

```bash
psql -U postgres -d naya_isolated_rt -v ON_ERROR_STOP=1 \
  -f docs/PERSISTENCE-HANDOFF/isolated-schema.sql
# Expected exit code: 0. ON_ERROR_STOP=1 makes any failure fatal.
```

`isolated-schema.sql` is the ledger-relevant subset of the canonical
migration `20260919015207_smart_ledger_foundation_v1.sql`: the
`nayanet_smart_ledger` table, the `nayanet_record_ledger_event` writer, and
the owner-isolation RLS policy. Semantics are verbatim; only the
`p_learning_refs` default is normalized (`[]` instead of `{}` — the original
default is a type error against the `jsonb` column).

## 3. Run the boundary proof

```bash
python3 docs/PERSISTENCE-HANDOFF/isolated_roundtrip.py
# Expected exit code: 0 and "14/14 checks passed".
```

What it proves (each check is independent):
1. Receipt seal MATCH (kernel-produced `demo-001` receipt).
2. Adapter projection accepted (all boundary validations).
3. Verification stays honestly `UNVERIFIED`.
4. No invented execution/observation timestamps.
5. Canonical writer used.
6. Chain hash computed.
7. Identical replay returns the same row (idempotent).
8. Conflicting payload does NOT overwrite the existing row.
9. Fresh process reads the row (process boundary crossed).
10. 12-field reconstruction: 0 violations (substantive validation).
11. `receipt_hash` recomputes MATCH from the row.
12. `inputs_hash` recomputes MATCH from the preserved `inputs_state`.
13. Owner-B context sees 0 rows (RLS isolation).

The producer connection is terminated between write and read; the reader is
a separate OS process. A second dictionary or fixture reload is not
database persistence.

## 4. Fresh-reader entry point (for Coda 4 / independent consumers)

```bash
python3 docs/PERSISTENCE-HANDOFF/reconstruct-12field.py \
  --event-id <ledger_event_id> --owner <owner-uuid>
```

Prints the 12 contract fields reconstructed from the retrieved row and the
validation violations (empty = valid). Recompute both hashes from the
retrieved row alone:

```bash
python3 - <<'EOF'
import json, hashlib
from kernel.persistence_seam import verify_kernel_receipt, _sha256
row = ...  # retrieved row
receipt = row["value"]                      # verbatim kernel receipt
assert verify_kernel_receipt(receipt)["result"] == "MATCH"
assert _sha256(row["metadata"]["inputs_state"]) == receipt["inputs_hash"]
EOF
```

## 5. Cleanup

```bash
sudo -u postgres psql -v ON_ERROR_STOP=1 \
  -c "DROP DATABASE naya_isolated_rt;" \
  -c "DROP ROLE rt_owner_a;" \
  -c "DROP ROLE rt_owner_b;"
```

## 6. Explicit limitations

- The disposable schema is a **subset**: only the ledger writer path. V2.1
  typed-receipt functions are exercised separately (see directive move 8).
- The 14/14 proof used the `demo-001` kernel receipt at kernel `4e87d4a`,
  not the Demo-1 ACT receipt (`dec-demo1-live-001`) — the ACT receipt is a
  different family and is honestly refused by the adapter pending a joint
  contract extension with Naya 4.
- Owner isolation is proven at the RLS policy level with two login roles;
  production `auth.uid()` semantics are equivalent by policy definition,
  not re-proven here.
- `content_hash` shape-validity is not recomputation evidence; the
  recomputation proof is checks 11–12 above.
- The local `pg_hba.conf` trust change used during setup is a test-only
  weakening and must be reverted after the run.
