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

## Result (final branch state — re-verified after the outcome event)

Second cold run, same procedure, fresh clone @ `6cc7d0e9` (7-event ledger):

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `6cc7d0e9` | `6cc7d0e9` | ✅ |
| `ledger_sha256` | `sha256:864ba35dfa75c743353450943aa3713869b79913d35281b4cd6743ca946aefb1` | (same) | ✅ |
| `hv_per_day_total` | 1.1429 | 1.1429 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 7 | 7 | ✅ |
| `calibration.n` / MAE | 1 / 0.5 | 1 / 0.5 | ✅ |
| test suite | 34 passed | 34 passed | ✅ |

(First cold run @ `de955893`, 6-event ledger: HV/day 1.0, DAI 0.2857,
`sha256:fd75825e…`, calibration n=0 — all matched identically.)

**Verdict:** the real measurement is cold-recomputable at the branch's final
state. Same bytes → same numbers, with no access to the originating
workspace. The 2026-10-06 failure (dead workspace, documented-only numbers)
cannot recur for this ledger: the producing bytes are canonical repo bytes
on a pushed branch.
