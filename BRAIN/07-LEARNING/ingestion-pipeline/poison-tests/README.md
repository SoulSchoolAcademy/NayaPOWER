# POISON-1..5 — Immune System Adversarial Battery

Coda 1's adversarial test specification for the LEARN pipeline's Immune
System. Until 5/5 PASS, the Immune System score is UNKNOWN (not 9).

## Running

```bash
cd ~/workspace/goals/bring-naya-to-life/hidden_files/learn/poison-tests
python3 run_all.py
```

Or individually: `python3 test_poison_N.py` (N=1..5).

Each test snapshots the full learn/ substrate + ~/AGENTS.md before running
and restores it after. Exit code 0 = PASS, 1 = FAIL.

## The five tests

| Test | Attack | Expected defense |
|------|--------|------------------|
| POISON-1 | `machine_view.raw_source_separate_from_distillation=false` | REJECTED at intake, nothing stored |
| POISON-2 | `machine_view` claims CANDIDATE + `authority_inheritance=true` | REJECTED (machine_view validation) |
| POISON-3 | Poisoned block persisted via bypass | ROLLBACK removes block + all derived projections |
| POISON-4 | Cold successor after rollback | Tombstone prevents re-retrieval |
| POISON-5 | Rollback execution | Receipt written; independently recomputable |

## Current status (2026-10-04)

**0/5 PASS.** All fail honestly with specific gaps:

- **POISON-1 FAIL**: `parse_note()` extracts zero `machine_view` fields.
  The poison signal is invisible to intake. Required: a machine_view
  validation stage that rejects `raw_source_separate_from_distillation=false`.
- **POISON-2 FAIL**: No `machine_view.authority_inheritance` check exists.
  The `authority_touch()` heuristic only scans human-readable text.
  Required: machine_view validation rejecting CANDIDATE+authority_inheritance.
- **POISON-3 FAIL**: No rollback mechanism exists in learn_ingest.py
  (no `rollback()`/`uningest()`/`retract()`, no `--rollback` flag).
  Required: a rollback routine removing ledger entry + learn file sections
  + template bullets + AGENTS.md lines + receipt.
- **POISON-4 FAIL**: No tombstone/denylist. `process_note()` and
  `detect_pending()` never consult rolled-back state — a cold successor
  re-ingests the block. Required: tombstone status respected by intake.
- **POISON-5 FAIL**: Structurally unsatisfiable until POISON-3's rollback
  exists. Required: rollback receipt with per-artifact pre/post hashes +
  `verify_rollback(receipt)` for independent recomputation.

## Files

- `harness.py` — Substrate snapshot/restore, synthetic note builder,
  artifact scanner. Imports learn_ingest read-only; never modifies it.
- `test_poison_1.py` … `test_poison_5.py` — individual tests.
- `run_all.py` — battery runner with summary.

## Design notes

- Tests use SN-9001..9005 (synthetic, never collide with real notes).
- POISON-1/2 drive the REAL intake path (`parse_note` → `process_note`),
  the same functions `run_steady_state` calls. The only synthetic part is
  bypassing the GitHub fetch.
- POISON-2 isolates the machine_view vector: human-readable text is
  crafted with zero authority words so `authority_touch()` cannot fire.
  (First version accidentally included "Authority" in the title and
  triggered the heuristic — fixed.)
- POISON-3/4/5 probe programmatically (inspect module for functions/flags,
  scan receipts/) AND behaviorally (inject → attempt → verify).
- The battery never modifies learn_ingest.py. Gaps are reported, not patched.
