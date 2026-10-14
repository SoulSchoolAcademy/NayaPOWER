# learn-clock

The learning-latency instrument for the Super-brain mission (GRAND-TODO
bottleneck #1: LEARN 5 → 10).

**What it does:** measures the clock from event to compounding. `emit()`
records T0–T7 stage transitions to an append-only JSONL ledger;
`latency()` returns T6−T0 in minutes; `meets_target()` is fail-closed
(True only when T6 exists and latency ≤ 60); `status()` shows missing
stages.

**Files:**
- `learn_clock.py` — the instrument (`emit`, `latency`, `meets_target`, `status`)
- `learn_hook.py` — hook adapter for capture paths
- `test_learn_clock.py` — 16 tests, all green
- `WIRING.md` — worker's guide: where each `emit()` belongs in live paths

**State (2026-10-14):** built and unit-verified. Not yet wired into live
capture paths — that is the next chunk (bottleneck #1). The `.jsonl`
ledgers are runtime state and are deliberately NOT committed; each
deployment initializes its own ledger.

**Law:** the emit goes next to the evidence, never earlier, never in bulk.
WIRING.md is the contract.
