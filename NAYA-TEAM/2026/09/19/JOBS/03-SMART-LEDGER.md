# JOB 03 — SMART LEDGER
## Mission
Make Smart Ledger the human-readable durable consequence/evidence surface for NayaNET actions and intelligence changes.

## Current known state
Live evidence includes 96 Smart Ledger rows, 125 execution receipts, and 124 cognition events. Historical production closure proved real execution → receipt → cognition → Ledger. Current execution outcomes table has 0 rows and must not be treated as proven observation data.

## Job
Connect the existing Ledger UI to canonical production consequences without creating another event store.

## Build
- Map Ledger UI regions in the canonical Hub.
- Map every supported Ledger row to its canonical source/event/receipt.
- Preserve provenance and lineage.
- Present truthful lifecycle state: recorded, observed, verified where evidence exists.
- Link actions to receipts/cognition/intelligence where authorized.
- Enforce owner/visibility filtering before presentation.
- Prove unauthorized evidence is not exposed.
- Test reload, replay/idempotency semantics, and duplicate prevention where applicable.
- Explicitly identify the execution-outcome gap; do not manufacture observed/verified status from a receipt alone.
- Prove Cloudflare parity.

## Acceptance
A user can inspect a real consequence and reconstruct what happened, from authorized action through receipt/cognition/Ledger. Claims unsupported by observation remain unverified.

## Handoff
Update report/checklist/activity and coordinate with Feed, Mail, Share, Spaces, Today, and Reports where Ledger is their consequence source.
