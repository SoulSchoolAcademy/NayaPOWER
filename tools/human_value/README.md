# Human Value Instrument v1

Canonical, cold-recomputable measurement of verified human value for NayaPOWER.
If you are a successor reading this cold: start at `CONTRACT.md`, then run the
example below. You need nothing from any originating workspace.

## Quick start

```bash
# Recompute the example measurement (deterministic — same bytes, same numbers)
python3 tools/human_value/compute_hv.py \
  --ledger tools/human_value/examples/example-events.jsonl \
  --receipts tools/human_value/examples/example-receipts.json

# Verify against a pinned ledger hash (fail closed on byte drift)
python3 tools/human_value/compute_hv.py \
  --ledger <your-ledger.jsonl> \
  --expect-ledger-sha256 sha256:<pinned>

# Custom window / as-of (as_of defaults to the latest event date, never wall-clock)
python3 tools/human_value/compute_hv.py \
  --ledger <ledger> --window-days 30 --as-of 2026-10-31
```

## Files

- `CONTRACT.md` — the measurement contract (five laws, metrics, cold checklist)
- `schema.py` — strict event validation; violations fail closed (no credit)
- `compute_hv.py` — deterministic HV/day + DAI + ledger hash + calibration join
- `real_outcome_loop.py` — prediction→observation join feeding the kernel's
  `calibration_summary` / `build_recalibration_receipt`
- `examples/` — synthetic demonstration corpus (labeled SYNTHETIC; not real data)
- `ledgers/` — REAL data: `real-events.jsonl` (verified public-evidence events),
  `decision-predictions.json` (pre-registered calculus predictions; the
  prediction side of the real-outcome loop)
- `../../tests/test_human_value_instrument.py` — the proof this works
- `../../tests/test_human_value_real_ledger.py` — the proof the real ledger
  validates, recomputes deterministically, and joins to its predictions

## Real-data quick start

```bash
# First real measurement (deterministic — same bytes, same numbers)
python3 tools/human_value/compute_hv.py \
  --ledger tools/human_value/ledgers/real-events.jsonl \
  --receipts tools/human_value/ledgers/decision-predictions.json
```

## Observatory — the live loop (`observatory.py`)

The ledger grows by observation, not by hand-editing. The observatory is the
loop that keeps measurement running live:

```bash
# 1. SCAN — draft every merge since the watermark (mechanical only: SHAs,
#    diffstats, PR links). Drafts are deliberately NOT ledgerable — the
#    machine observes, it never credits.
python3 tools/human_value/observatory.py scan --repo . --base <LAST_MERGE> \
  --watermark-out tools/human_value/observatory/watermark.json

# 2. GRADE — a seat grades a draft's change with instrument.py (judgment
#    with cited evidence; this is the human/seat step, never automated).

# 3. PROMOTE — the explicit lane act. A REAL VALUE+ scorecard becomes one
#    ledger event; the ledger recomputes deterministically, a trend snapshot
#    is appended, a promotion receipt is written. THIN / NO VALUE /
#    DISQUALIFIED and duplicate event_ids are refused, fail closed.
python3 tools/human_value/observatory.py promote \
  --ledger tools/human_value/ledgers/real-events.jsonl \
  --scorecard <SCORECARD.json> --event-id HV-20261012-PR-9001 \
  --recorded-at 2026-10-12 --confirm

# 4. REPORT — regenerate the pinned live report (deterministic bytes).
python3 tools/human_value/observatory.py report \
  --ledger tools/human_value/ledgers/real-events.jsonl \
  --receipts tools/human_value/ledgers/decision-predictions.json \
  --out tools/human_value/OBSERVATORY-REPORT.md
```

`observatory/drafts/` (grading queue), `observatory/receipts/` (promotion
provenance), `observatory/scorecards/` (graded scorecards),
`observatory/watermark.json` (observation cursor — operational, not a
measurement), `ledgers/trend.jsonl` (one snapshot per promotion — the raw
material of the 30-day trend), `OBSERVATORY-REPORT.md` (the pinned live
report, regenerated — never hand-edited).

## Recording a real event

**Ledger placement law** (learned 2026-10-08 from the dead-workspace failure):
- **Non-sensitive ledgers** (public evidence only — `feed_comment`, `url`,
  `smart_note`, `receipt` pointers; no private human data) are canonical **in
  this repo** under `tools/human_value/ledgers/`. Cold successors recompute
  from these. Anything that lives only in a workspace can die with it.
- **Sensitive ledgers** (anything touching private human data) live **outside**
  this repo (e.g. a goal's `hidden_files/`); the repo holds only derived
  measures + `content_hash` pins, never raw private bytes.

Append one JSON object per line to the ledger:

```json
{"schema_version": "1", "event_id": "HV-20261008-001",
 "recorded_at": "2026-10-08", "value_type": "useful_outcome",
 "value_units": 1, "unit_description": "human-requested outcome delivered end to end",
 "evidence": [{"kind": "feed_comment", "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1604#issuecomment-XXXX"}],
 "decision_id": "DEC-20261008-001", "delta_v_actual": 7.5}
```

## Lane ownership

Human Value lane (Naya 5). Feed: #1604. The Decision Value Calculus
(`kernel/value_calculus.py`) remains the single decision/selection seam —
this instrument is its observed-outcome evidence supplier, not a competitor.
