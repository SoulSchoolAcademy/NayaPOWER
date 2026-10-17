# D51 — The Living Ledger / Smart Net (first machine slice)

**Status:** CANDIDATE (machine form). **Source:** directive register, #2175 comment 6102054179 (Shawn's vision, registered 2026-10-10). **Owner:** Naya 2 (build lane). **Machine form:** `living_ledger/receipt.py` + `living_ledger/chain.py` + `living_ledger/tests/` (all green).

## The law

Every action that matters emits a receipt — actor, action, evidence, timestamp, scope. No action without tracking, receipt, and evidence. Receipts append to one shared hash-chained ledger, and the chain is verifiable by anyone holding the events: a tampered link fails loudly, never silently.

## What already exists (not rebuilt)

- **The chained ledger:** `nayanet_smart_ledger` (Supabase) with `chain_seq`, `previous_chain_hash`, `event_hash`, and the `nayanet_record_ledger_event()` writer — hash-chained and idempotent. Building a second ledger would be a duplicate mechanism; this slice feeds that ledger, it does not replace it.
- **The room contract:** `HUB/ROOMS/06-LEDGER.md` specifies the living surface (one page, every tracked action with its evidence, live, chain-verifiable). This slice does not build the page — that is a separate, larger slice.
- **Domain receipts:** `CanaryReceipt`, `LivenessReceipt`, and siblings are domain-specific. This slice unifies them into one envelope; it does not replace them.

## The gaps this slice closes

1. **No canonical D51 receipt in Python.** Nothing carried (actor, action, evidence, timestamp, scope) as one envelope. `LivingReceipt` is that envelope. It refuses to construct without evidence — a receipt with no evidence is not a receipt, it is a claim.
2. **Nothing proves the chain.** "Chain-verifiable" was words. `verify_chain` re-computes every link with the exact `nayanet_smart_ledger_hash` construction and reports the first break with the event index, the expected hash, and the actual hash. Tamper → `HASH_MISMATCH`. Dropped or reordered link → `LINK_BROKEN`. It works on provided event lists; it performs zero database reads.

## The envelope

`LivingReceipt(actor, action, evidence, timestamp, scope, metadata)`:

- `actor` — who acted (`naya2/build-lane`, `shawn`, …). Non-empty, or construction refuses.
- `action` — what was done, a verb phrase (`merged PR #2293`, `recorded learning event`). Non-empty, or construction refuses.
- `evidence` — the proof references. Non-empty tuple, or construction refuses. This is the D51 hard rule: no evidence, no receipt.
- `timestamp` — ISO-8601 UTC. Malformed, or construction refuses.
- `scope` — one of `self` / `team` / `collective` / `public`. Maps to the ledger's privacy classification (`PRIVATE` / `SHARED` / `COLLECTIVE` / `PUBLIC`); anything else refuses.
- `receipt_id` — deterministic sha256 over the canonical envelope encoding. Same action twice yields the same id: idempotent by construction, matching the ledger's `(owner_id, source_table, source_id)` uniqueness.

`to_ledger_params(owner_id)` maps the envelope exactly onto `nayanet_record_ledger_event()` arguments (`p_event_type`, `p_event_at`, `p_source_table='living_ledger'`, `p_source_id=receipt_id`, `p_evidence_refs`, `p_metadata` carrying actor/scope, `p_privacy_classification` from scope). It builds the call — it does not execute it. Execution stays behind the human-only database gate.

## The verifier

`verify_chain(events)`:

- Recomputes `event_hash` per event as `sha256(owner_id|event_type|event_at|source_table|source_id|parent_ledger_event_id|previous_chain_hash|evidence_refs|metadata)` — the exact field order and `|` separators of `nayanet_smart_ledger_hash`.
- Checks each event's `previous_chain_hash` equals its predecessor's `event_hash` (genesis event: empty/None allowed exactly once, at index 0).
- Checks `chain_seq` strictly increases when present.
- Verdicts: `CHAIN_VALID`, `HASH_MISMATCH`, `LINK_BROKEN`, `SEQ_REGRESSION`, `EMPTY_CHAIN`. Every failure names the event index and both hashes — the break is exhibited, never implied.

**Canonical encoding note (honest boundary):** Postgres renders `jsonb::text` and `timestamptz::text` in its own dialect (key ordering, spacing, `+00` offsets). The Python canonical encoding uses compact JSON (sorted keys) and ISO-8601. A chain exported from Postgres verifies in Python only if the exporter normalizes to this canonical encoding first; `normalize_postgres_event()` documents the known divergences. Byte-parity with a live Postgres row is asserted nowhere — that claim would require a live database read, which is a human-only gate.

## The cases that make it real

| Fixture | Expected |
|---|---|
| Well-formed receipt, evidence present | constructs; `to_ledger_params` maps every field |
| Receipt with empty evidence | refuses at construction (`ValueError`) |
| Malformed timestamp | refuses at construction |
| Unknown scope | refuses at construction |
| Two identical actions | identical `receipt_id` (idempotent) |
| Valid 3-event chain | `CHAIN_VALID` |
| Evidence tampered on event 1 | `HASH_MISMATCH` at index 1, expected vs actual shown |
| Event 1 dropped (0 → 2) | `LINK_BROKEN` at index 1 |
| Events reordered | `LINK_BROKEN` or `HASH_MISMATCH` — never a silent pass |
| Forged `event_hash` | `HASH_MISMATCH` |
| `chain_seq` not increasing | `SEQ_REGRESSION` |
| Empty event list | `EMPTY_CHAIN` (not a pass) |

## What this does NOT claim

- It does not build the living surface page. The HUB room contract specifies it; the page is a separate slice.
- It does not write to any database. `to_ledger_params` builds the stored-procedure call; execution is human-only.
- It does not read the production ledger. The verifier works on event lists handed to it.
- It does not replace domain receipts. `CanaryReceipt`, `LivenessReceipt`, et al. keep their shapes; the envelope unifies them at the ledger boundary.
- It does not assert byte-parity with Postgres `::text` rendering. The canonical encoding is documented; cross-system verification needs the normalizer.
- CODE-ONLY: spec + deterministic machinery. Not in kernel/, KNOW, LAW, ACT, or any live path. Wiring is the wire lane's call.
