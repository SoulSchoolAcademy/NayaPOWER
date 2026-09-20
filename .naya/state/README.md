# NAYA STATE

**Status:** CANONICAL CONTRACT + MEASUREMENT LAYER

`.naya/state/` holds canonical operating contracts and the system measurement layer.

## Files

| File | Role |
| --- | --- |
| `excellence-operating-contract.v1.json` | The 16-dimension excellence contract and the 9.0 floor. |
| `maxis-living-sun-design.v1.json` | Design contract. |
| `NAYA-POWER-PROGRESS-INDEX-V1.schema.json` | Schema for the Naya Power Progress Index (weighted system checkpoints). |
| `CHECKPOINT-001.json` | The canonical progress index instance (currently the baseline checkpoint). |
| `validate_progress_index.py` | Fail-closed validator + independent adjudicator + self-test. |
| `test_progress_index.py` | Adversarial tests for the index and the acceptance law. |

## Naya Power Progress Index

Every checkpoint records an **exact HEAD + evidence + score + accepted/rejected status**. The index
authorizes nothing and executes nothing; it measures and adjudicates.

- `0.0–5.9` Failing · `6.0–7.9` Developing · `8.0–8.9` Strong but incomplete ·
  `9.0–9.4` Accepted · `9.5–9.9` Elite · `10.0` Objective achieved
- **Floor 9.0 · Target 9.5+ · Objective 10.0.** Nothing below 9.0 is accepted.
- A drop from an accepted/elite score is a **REGRESSION** and requires repair.

The measurement layer is deliberately separate from the builder. The declared score is recorded **and**
independently recomputed from the recorded weights and subsystem scores; divergence is surfaced, not
smoothed away. The verdict is derived mechanically from the floor.

## Commands

```text
python .naya/state/validate_progress_index.py validate     # structural + arithmetic + verdict gate
python .naya/state/validate_progress_index.py adjudicate   # recompute aggregates + verdict
python .naya/state/validate_progress_index.py self-test     # adversarial fail-closed proof
python .naya/state/test_progress_index.py                   # adversarial unit tests
```

## Current state

`CHECKPOINT-001.json` is the human-declared **baseline 6.70/10** at main
`94d2c561d4e6410c03a116f691186bead710b78c`, independently **rejected** (below the 9.0 floor).
The recorded weighted total is 6.40 and the unweighted mean is 6.00; the +0.30 divergence from the
declared figure is preserved as a measurement-integrity finding.

Truth rules carried from the control plane apply here: `RECORDED != CURRENT`, `UNKNOWN != GREEN`,
`VERIFIED != PRODUCTION_PROVEN`. A checkpoint is only current for the exact HEAD it binds.
