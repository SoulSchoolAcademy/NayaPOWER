# LEARN Node — Ingestion Pipeline + POISON Battery

Workspace-local intelligence ingestion pipeline for NayaPOWER's LEARN node.
Staged from Naya 4's workspace for review per Naya 2's request (issue #1354).

## What this is

- `learn_ingest.py` — Ingests Smart Notes from branch `naya4/smart-notes-2026-09-30`
  into the briefing substrate. Includes the four POISON fixes (Immune System).
- `poison-tests/` — Adversarial test battery (POISON-1..5). Run: `python3 run_all.py`
- `substrate/` — Current ingested intelligence (doctrine, laws, lessons, etc.)

## POISON fixes (Immune System 6/10 measured)

1. Machine-view validation at intake (rejects poisoned `machine_view` flags)
2. `rollback(sn_id)` + `--rollback` CLI (removes block + all projections)
3. Tombstone (`ROLLED_BACK` status, intake refuses re-ingestion)
4. `verify_rollback(receipt)` (independently recomputable from receipt data)

Battery: 5/5 PASS. Canary: PASS. 267 ledger entries verified clean.

## Not included

Runtime state (`receipts/`, `ledger.json`, `conflicts.md`, `ingestion-log.md`)
is regenerable and excluded to keep the branch lean. Available in workspace.

## Status

CANDIDATE — staged for review. Not merged to main. Only Shawn merges.
