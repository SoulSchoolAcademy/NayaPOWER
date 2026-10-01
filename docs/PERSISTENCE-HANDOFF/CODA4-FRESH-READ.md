# Fresh-Read Package for Coda 4 (Move 9)

**Purpose:** you independently retrieve the persisted proof row and
recompute both hashes — not relying on Naya 2's "MATCH" output.

## Identifiers

- **Ledger event:** `79404825-97a5-407c-a350-5820e51f50f3`
- **Owner:** `11111111-1111-1111-1111-111111111111` (owner A)
- **Source:** `naya_kernel_decision` / `demo-001`
- **Adapter:** `persistence-seam-v3` — PR #1243 @ `23186d4b`
  (`kernel/persistence_seam.py`)
- **Kernel:** `4e87d4a5810f6b0b5b72e254f3d37ddf69826c87`
- **Database:** `naya_isolated_rt` (disposable, local Postgres 16)

## Approved owner context

Read as `rt_owner_a` with `app.uid` set to the owner UUID (RLS applies).
You should see exactly 1 row for this event. Reading as `rt_owner_b`
must show 0 rows for owner A's data.

```bash
psql -U rt_owner_a -d naya_isolated_rt -c \
  "SET app.uid='11111111-1111-1111-1111-111111111111'; \
   SELECT ledger_event_id, event_hash, status \
   FROM public.nayanet_smart_ledger \
   WHERE ledger_event_id='79404825-97a5-407c-a350-5820e51f50f3';"
```

## Retrieved row evidence

The full row (15 columns) is in `coda4-row.json` alongside this package —
but prefer a live read via the command above. Verify the live row matches
the file.

## Independent recomputation commands

```bash
python3 - <<'EOF'
import json, sys
sys.path.insert(0, '<repo>/naya2/persistence-integration-package')
from kernel.persistence_seam import verify_kernel_receipt, _sha256

row = json.load(open('coda4-row.json'))
receipt = row['value']  # verbatim kernel receipt, as stored

# 1. Receipt seal: recompute from the row alone.
vr = verify_kernel_receipt(receipt)
assert vr['result'] == 'MATCH', vr
print('receipt_hash: MATCH')

# 2. Inputs hash: recompute from the preserved state in the row alone.
state = row['metadata']['inputs_state']
assert _sha256(state) == receipt['inputs_hash']
print('inputs_hash: MATCH')

# 3. Honest verification state: still UNVERIFIED, no invented outcome.
assert row['verification']['state'] == 'UNVERIFIED'
assert row['value'].get('observed_outcome') is None
print('verification: honestly UNVERIFIED')
EOF
```

Expected: all three print. If any assertion fails, the proof is broken —
report it, don't adjust.

## Lifecycle and supersession expectations

- `status` = `RECORDED`. This row has not been superseded
  (`superseded_by` is null; no successor names it as parent).
- A child row exists (`dec-child-001`, parent = this event) from the
  lineage qualification — it does not supersede this row; it threads from
  it. Backward reconstruction: child's `previous_chain_hash` =
  this row's `event_hash`.
- 12-field reconstruction of this row must yield 0 violations under the
  hardened `validate_contract_record` (tz-aware timestamps, V1 status
  vocabulary, V2.1 truth-state vocabulary).

## What this does NOT prove (keep separate)

- This is **database retrieval proof**, not KNOW restoration. Your CS-01
  and receipt-integrity findings require Naya 4's runtime repair; this
  persisted row does not close them.
- Owner isolation here is RLS-read-level with two login roles (see the
  Move 5 finding on write-time caller binding).
