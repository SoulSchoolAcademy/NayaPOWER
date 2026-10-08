# Cold-recompute proof — real-events ledger v1

**Gate under test (continuity gate 8.0, items 2–4):** a cold successor with no
access to the originating workspace retrieves the canonical source, recomputes
the same HV/DAI numbers from cited evidence, and any byte drift fails closed.

## Procedure (exactly as run 2026-10-08)

```bash
rm -rf /tmp/hv-cold-proof
git clone --branch naya5/human-value-real-data-v1 \
  https://github.com/SoulSchoolAcademy/NayaPOWER.git /tmp/hv-cold-proof
cd /tmp/hv-cold-proof
python3 tools/human_value/compute_hv.py \
  --ledger tools/human_value/ledgers/real-events.jsonl \
  --receipts tools/human_value/ledgers/decision-predictions.json
```

## Result

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `de955893` | `de955893` | ✅ |
| `ledger_sha256` | `sha256:fd75825efd1f89e4d7133ba1d67a8f309699f74085269a3aa3af68bc3fac9cd5` | (same) | ✅ |
| `hv_per_day_total` | 1.0 | 1.0 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 6 | 6 | ✅ |
| `calibration.n` | 0 (no joined observations yet) | 0 | ✅ |

**Verdict:** the real measurement is cold-recomputable. Same bytes → same
numbers, with no access to the originating workspace. The 2026-10-06 failure
(dead workspace, documented-only numbers) cannot recur for this ledger: the
producing bytes are canonical repo bytes on a pushed branch.
