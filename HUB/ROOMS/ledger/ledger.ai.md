# Smart Ledger — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/ledger`. **Accent:** gold — hairlines and seals ONLY (never washes, never body text). **Build order:** 5.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. `hub/ledger?filter=`.

## Component tree

1. `LedgerHero` — title, tagline, `StandingStrip` (balances/positions, plain numbers).
2. `FilterPills` — ALL / ACTIONS / DECISIONS / SHARES / CONNECTIONS / SYSTEM.
3. `LiveTimeline` — `ReceiptCard`s, chronological: time, event title, source, authority, result, receipt id, lifecycle badge.
4. `ProofDrawer` — per receipt: evidence chain, timestamps, authority record.
5. `VerifyButton` — re-check affordance per receipt.

## Data bindings

- Receipts ← governed record store (append-only). Standing strip ← value positions (proven only).
- Every receipt binds: `receipt_id`, `event`, `source`, `authority`, `result`, `lifecycle_state`, `evidence_ids`.

## States

- `live` / `catching_up` / `offline` (cached with stamp). `empty`: "No recorded activity yet." Verify: `verifying` → `sealed` / `gap_found`.

## Interactions

- Receipt tap → proof drawer inline. Verify → live re-check → re-seal or honest gap report.
- Explain → Naya narrates the receipt in plain words.
- Filter → timeline re-queries by type.

## Design tokens

Gold restraint is law here: 1px hairlines, seal chips, Verify button edge. Everything else white-on-obsidian, tabular numerals for the standing strip.

## Acceptance

Append-only proven by test (no edit path in UI); lifecycle states on every receipt; Verify re-checks for real; empty state honest; 9.0+.
