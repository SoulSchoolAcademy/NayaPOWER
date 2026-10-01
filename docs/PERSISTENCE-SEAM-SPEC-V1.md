# Persistence Seam Spec V1 — kernel receipts → governed ledger

**Status:** PROPOSED (Naya 2, 2026-10-01). For Naya 4's agreement before wiring.
**Canonical authority:** `NAYANODE/0101-PERSISTENCE-CONTRACT-V1.md` (12 required fields). This spec
implements the seam *under* that contract. It does not replace it.
**Withdrawn:** Naya 2's earlier `naya-receipt-contract/1` draft (#554/5934427074) is withdrawn as a
competing format. Its lineage/verification content is folded here as seam convention.

## 1. The three layers (do not conflate)

| Layer | What | Producer | Where it lives |
|---|---|---|---|
| Common persistence metadata | The 12 contract fields | Seam | `nayanet_smart_ledger` columns |
| Execution evidence | Kernel decision receipt | `naya_kernel` | `value` jsonb |
| Typed value receipt | V2.1 `ALIGNMENT_DECISION` / `CONTRIBUTION_VALUE` | Calculator / assessor | `value` jsonb, validated by `nayanet_validate_v2_1_value_receipt` on every write |

## 2. Existing write path (verified live 2026-10-01 — extend, don't duplicate)

```
kernel receipt (dict)
  → kernel/persistence_seam.py :: project_kernel_receipt()   [NEW, this package]
  → nayanet_record_ledger_event(...)                          [EXISTS, SECURITY DEFINER]
  → nayanet_smart_ledger row                                  [EXISTS]
```

Alternative existing path: `INSERT INTO nayanet_execution_receipts` → trigger
`nayanet_execution_receipt_to_smart_ledger` → same function. Kernel decision receipts use the
direct function path (`source_table='naya_kernel_decision'`), not the execution-receipts table.

## 3. Field map — contract → producer → validation → storage

| # | Contract field | Meaning | Type | Producer | Validation | Ledger storage |
|---|---|---|---|---|---|---|
| 1 | `object_id` | Durable identity | uuid | Seam (DB `gen_random_uuid()`) | PK | `ledger_event_id` |
| 2 | `owner_id` | Data owner (auth identity) | uuid | Seam from `auth.uid()`; **never the kernel** | `LEDGER_OWNER_MISMATCH` in function; FK `auth.users`; RLS read `auth.uid()=owner_id` | `owner_id` |
| 3 | `owner_scope` | Visibility | enum | Seam from request context (default `PRIVATE`) | CHECK `PRIVATE/SHARED/COLLECTIVE/PUBLIC` | `privacy_classification` |
| 4 | `created_at` | Record creation | timestamptz | DB `now()` | NOT NULL | `created_at` |
| 5 | `updated_at` | Last mutation | timestamptz | — | **GAP:** no column (append-only). Convention: `metadata.updated_at` | `metadata` |
| 6 | `schema_version` | Contract version | text | DB hardcoded | NOT NULL | `schema_version` = `'1.0.0'` |
| 7 | `provenance` | How this came to be | jsonb object | Kernel supplies `{node_id, kernel_version, kernel_sha, config_hash}`; seam adds `{received_at, adapter_version}` | must be object | `metadata` (+ function adds `assessment_state`, `value_receipt_type`, `value_receipt_hash`) |
| 8 | `truth_state` | Epistemic state | enum | — | **GAP:** no column. Carried by `status` + `verification` jsonb | `status`, `verification` |
| 9 | `status` | Lifecycle | enum | Seam (initial `RECORDED`) | CHECK `RECORDED/VERIFIED/QUALIFIED/SUPERSEDED/BLOCKED/FAILED` | `status` |
| 10 | `superseded_by` | Forward supersession pointer | uuid/null | — | **GAP:** no forward column. Derivable: `SELECT … WHERE supersedes_ledger_event_id = X` | (reverse query) |
| 11 | `lineage` | Backward chain | object | Seam: `p_parent_ledger_event_id`; DB resolves `previous_chain_hash` | self-FK; hash chain | `parent_ledger_event_id`, `previous_chain_hash`, `event_hash` |
| 12 | `content_hash` | Integrity of content | hex(64) | DB: `nayanet_smart_ledger_hash(...)` | recomputed in-function | `event_hash` |

Seam-managed extras: `event_type='DECISION'`, `source_table='naya_kernel_decision'`,
`source_id` = kernel `decision_id`, `event_at` = kernel `issued_at`, `evidence_refs=[]`,
`verification={'state':'UNVERIFIED'}`, `outcome={}`, `learning_refs=[]`.

## 4. Boundary answers (Naya 4's question, 5934391765)

- **Who assigns `object_id`?** The seam/database (`ledger_event_id`, `gen_random_uuid()` at insert).
  The kernel's `receipt_id` / `decision_id` travel as `source_id`, never as `object_id`.
- **Who assigns `owner_id`?** The seam, from `auth.uid()` of the authenticated caller, passed as
  `p_owner_id`. The function raises `LEDGER_OWNER_MISMATCH` if they differ. The kernel never sees
  owner identity. Seat labels ("naya-2") are worker descriptions, not security identities.
- **Does the kernel emit `inputs_hash`?** **Yes** (current kernel `123fc98e`;
  earlier `4e87d4a` introduced it, `seal()` line 370 hashes the full evaluated
  state). It emits `receipt_hash` (SHA-256 over the canonical receipt body
  *including* `issued_at` and `inputs_hash`) and `issued_at`. Legacy receipts
  without `inputs_hash` are labeled `input_commitment: "absent-legacy"` and
  never receive the recomputation qualification.
- **Does the kernel emit `executed_at`?** Not by that name. `issued_at` is the execution timestamp
  (receipt created at the end of `decide()`). The seam records `received_at` in provenance; it must
  not invent `executed_at` or `observed_at`.
- **Direct emission vs adapter wrapping?** **Adapter wrapping.** The kernel emits its native receipt
  unchanged; the seam validates `receipt_hash` with the kernel's own canonicalization, then projects
  onto the function parameters. No kernel changes required.

## 5. Enforcement evidence (all verified live against production, read-only, 2026-10-01)

| Claim | Evidence | Verdict |
|---|---|---|
| Idempotent writes | Pre-insert SELECT + `unique_violation` handler returning existing row + `UNIQUE(owner_id, source_table, source_id)` | **DB-ENFORCED** (triple) |
| Owner-isolated reads | RLS policy `nayanet_smart_ledger_select_own`: `auth.uid() = owner_id` (SELECT, authenticated) | **DB-ENFORCED** |
| Owner-isolated writes | `LEDGER_OWNER_MISMATCH` raised in `nayanet_record_ledger_event` when `auth.uid()` ≠ `p_owner_id` | **DB-ENFORCED** (service_role bypasses by design — `auth.uid()` is null) |
| Value-receipt validation | `nayanet_validate_v2_1_value_receipt(p_value)` called on every write | **DB-ENFORCED** |
| Hash-chain integrity | `nayanet_smart_ledger_hash(...)` computed in-function; `previous_chain_hash` linked | **DB-ENFORCED** |
| Status / privacy vocabularies | CHECK constraints | **DB-ENFORCED** |
| Lineage referential integrity | Self-FKs on `parent_ledger_event_id`, `supersedes_ledger_event_id`, `qualified_by_ledger_event_id` | **DB-ENFORCED** |
| Source identity (`repo_sha` = actual) | — | **SEAM CHECK ONLY**, not DB-enforced |
| `updated_at`, `truth_state`, `superseded_by` columns | — | **GAPS** (conventions documented above) |

## 6. Corrections to earlier Naya 2 claims

1. `naya-receipt-contract/1` — withdrawn as a competing format (this spec replaces it).
2. "owner_id is the RLS boundary" — true for reads; writes are enforced by `LEDGER_OWNER_MISMATCH`
   inside the SECURITY DEFINER function, not by an INSERT RLS policy (none exists; authenticated
   writes go through the function, which checks).
3. "Database-enforced outcome rules" — the V2.1 *receipt validation* is enforced on every write;
   the UNVERIFIED→VERIFIED_PASS *lifecycle* is seam convention in `verification` jsonb, not a CHECK.
4. Static schema mapping is not DB integration — stated as such; the DB setup for live exercise is
   in `docs/PERSISTENCE-REPRODUCE.md`.

## 7. v2 hardening (2026-10-01, after independent review)

Independent review of the v1 package reproduced four seal/boundary bypasses
and one CI failure. All are fixed in `persistence-seam-v2`; RED evidence was
published on PR #1243 before the fix (comment 5935447995).

1. **Seal bypass (RED-1).** v1 invoked the verifier only when `receipt_hash`
   was a string, so `receipt_hash=123` skipped verification entirely. v2
   rejects missing/null/non-string/malformed hashes and ALWAYS verifies a
   well-formed hash (must be 64-char lowercase hex).
2. **Receipt vocabulary (RED-2/3/4).** v1 accepted resealed receipts with
   `verdict="BOGUS"`, `issued_at="banana"`, `decision_id=123`. v2 enforces:
   `verdict` ∈ {PASS, FAIL, NEED_EVIDENCE} (canonical `GateVerdict` from
   `naya_kernel/node_base.py`); `issued_at` must parse as ISO-8601;
   `receipt_id`/`decision_id`/`kernel_version` must be non-empty strings.
3. **Input commitment.** Receipts without `inputs_hash` are labeled
   `input_commitment: "absent-legacy"` in provenance; verified receipts carry
   `"recomputed-match"`. A legacy receipt never receives the recomputation
   qualification. **Cold-recomputation closure (v3):** when `inputs_state` is
   submitted, the exact evaluated state is preserved verbatim in
   `p_metadata.inputs_state` alongside the receipt — so a fresh consumer
   retrieving the row can independently recompute `inputs_hash` from the row
   alone. Without this, only the write-time commitment would survive and the
   consumer could not re-verify. Privacy posture is unchanged (row already
   PRIVATE to the owner; receipt already stored verbatim).
4. **Provenance honesty.** `kernel_sha`/`config_hash` are shape-checked
   caller-supplied LABELS, preserved in provenance as claims — never as
   independently established source/config provenance. Shape is not isolation:
   `owner_id` uuid format ≠ owner isolation; idempotency-key determinism ≠
   safe replay; parent uuid format ≠ lineage authorization. Those are
   database properties, proven only by DB evidence.
5. **CI.** Test file renamed `tests/persistence_seam.test.py` →
   `tests/test_persistence_seam.py` (pytest discovery) and imports via
   `from kernel.persistence_seam import ...` instead of a `sys.path` hack —
   the dependency guard no longer misclassifies `persistence_seam` as an
   undeclared third-party distribution. Guard not weakened.

## 8. v3 hardening (2026-10-01, coordinator review — master directive moves 3–4)

Independent review reproduced two more defect classes. Both fixed in
`persistence-seam-v3`; RED tests published before the fix.

6. **Snapshot aliasing (RED-2).** `dict(receipt)` was a shallow copy and
   `p_metadata["inputs_state"]` aliased the caller's object: mutating the
   caller's `inputs_state` after projection changed the projected state, and
   mutating nested receipt content broke the projected seal. v3 detaches
   BOTH through strict canonical JSON (`_detached_snapshot`) BEFORE
   validation — validation and hashing run on the snapshots, the exact
   objects that will be serialized. Caller mutation after projection cannot
   invalidate already-validated evidence; projection mutation cannot reach
   back into producer objects. Non-JSON-native values (sets, bytes,
   NaN/Infinity) are REJECTED at the boundary, not silently stringified.
   Canonical hashing rules (`_canon`/`_sha256`) are unchanged.
7. **Substantive contract validation (RED-3).** `validate_contract_record()`
   checked presence only — `created_at="banana"`, `schema_version=123`,
   `truth_state="MADE_UP"`, `status="MADE_UP"`, `superseded_by="not-a-uuid"`
   returned zero violations. v3 validates meanings against the canonical
   contracts: tz-aware ISO-8601 timestamps with time (date-only and naive
   rejected — the producer emits tz-aware; the ledger stores timestamptz);
   `schema_version` semver; `status` ∈ the V1 migration's check-constraint
   vocabulary (RECORDED, VERIFIED, QUALIFIED, SUPERSEDED, BLOCKED, FAILED);
   `truth_state` ∈ the V2.1 assessment vocabulary (UNASSESSED, ASSESSED,
   VERIFIED_VALUE, REJECTED); `superseded_by` null-or-uuid; lineage shape
   (parent null-or-uuid, chain_seq null-or-int, previous_chain_hash
   null-or-64hex); provenance requires `source_table` + `source_id`.
   Explicit limitation: shape-valid `content_hash` is not recomputation
   evidence — recomputation is proven by the write→fresh-read path.
8. **Timestamp boundary.** `_parse_timestamp` now enforces the producer's
   contract: a date-only value such as `2026-10-01` is rejected as
   `issued_at`, as are naive datetimes. This applies to adapter input and
   to `created_at`/`updated_at` in contract records.
