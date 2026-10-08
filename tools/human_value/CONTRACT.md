# Human Value Measurement Contract v1

**Status:** canonical instrument (repo bytes). Replaces the lost 2026-10-06 local
instrument, whose producing bytes lived in a deleted workspace — the exact
failure this contract prevents.

## The question

**Did a human's life get measurably better?** "Task done" ≠ "mission complete."
Only observed, evidenced human outcomes count.

## What counts as human value (the four outcomes)

| value_type | Meaning |
|---|---|
| `cognitive_load_reduced` | human attention/effort the system absorbed instead of demanding |
| `rework_avoided` | work that did not have to be redone |
| `error_prevented` | mistakes caught before they cost a human |
| `useful_outcome` | a human got something they actually wanted |

Plus the service-quality counter-metric:

| value_type | Meaning | Trend target |
|---|---|---|
| `attention_demanded` | times the human had to intervene/correct the system (DAI input) | **DOWN** |

## The five laws of a valid measurement

1. **Evidence or it didn't happen.** Every event carries ≥1 durable evidence
   pointer. No evidence → no credit, fail closed. Evidence kinds: `feed_comment`
   (GitHub issue comment URL), `smart_note` (IB-… id), `receipt` (repo path),
   `content_hash` (`sha256:<hex>`), `url`.
2. **Private stays private.** Raw human data never enters a ledger. Ledgers hold
   derived measures + pointers; private bytes are pinned by `content_hash` and
   kept outside the repo.
3. **Units are human-comprehensible.** `value_units` must be explainable in one
   sentence (`unit_description`); minutes returned, cycles avoided, outcomes
   delivered. No abstract points.
4. **Deterministic recomputation.** Same ledger bytes → same report, for any
   successor, with no access to the originating workspace. `as_of` defaults to
   the latest event date (never wall-clock); the report pins `ledger_sha256`;
   `--expect-ledger-sha256` fails closed on byte drift.
5. **Prediction meets observation.** Events may carry `decision_id` +
   `delta_v_actual` (calculus scale [-10,10]). Joined to the decision receipt's
   `delta_v_predicted`, the kernel's `calibration_summary` closes the
   real-outcome loop: PREDICT → ACT → OBSERVE → CALIBRATE → RECALIBRATE-CANDIDATE.
   Recalibration candidates propose; they never promote.

## Metrics

- **HV/day** = Σ value_units per type over trailing 7 days ÷ 7. Total and per-type.
- **DAI/day** = `attention_demanded` units per day. Healthy system: trending down.
- **Calibration**: n joined observations, MAE, signed bias, overprediction flag,
  confidence multiplier (kernel math).

## What this is not

- Not a second decision engine. The Decision Value Calculus remains the one
  scoring seam; this instrument supplies the observed-outcome evidence it learns from.
- Not a survey. Sentiment is not measured; outcomes are.
- Not retroactive credit. Events are recorded when observed, with evidence that
  already exists — never manufactured to lift a number.

## Cold-successor checklist (8.0 gate)

1. `git clone` at the pinned SHA; read `tools/human_value/README.md`.
2. `python3 tools/human_value/compute_hv.py --ledger <ledger> --receipts <receipts>`.
3. Compare `ledger_sha256` and every number against the posted report.
4. Any mismatch fails closed and is visible. A recomputation that matches is
   proof; a claim without one is documentation.
