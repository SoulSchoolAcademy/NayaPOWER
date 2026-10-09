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

## Third cold run — 2026-10-08 ~16:10 UTC (18-event ledger, n=2 loop)

Same procedure, fresh clone @ `08946947` (branch `naya5/human-value-real-data-v1`,
rebased onto tip `aacbcc9a5`):

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `08946947` | `08946947` | ✅ |
| `ledger_sha256` | `sha256:d4aa6a07…f5b6f` | (same) | ✅ |
| `hv_per_day_total` | 2.7143 | 2.7143 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 18 | 18 | ✅ |
| `calibration.n` / MAE / bias | 2 / 0.25 / 0.25 | 2 / 0.25 / 0.25 | ✅ |
| test suite (real ledger + instrument) | 35 passed | 35 passed | ✅ |

**Verdict:** the second real prediction→observation join (n=2, DEC-002) is
cold-recomputable at the pushed SHA. MAE 0.5→0.25, signed bias +0.5→+0.25,
no overprediction — the calibration math a cold successor recomputes is the
same math the originating run reported. /tmp clones removed after verification.

## Fourth cold run — 2026-10-08 ~22:05 UTC (19-event ledger, n=3 loop)

Same procedure, fresh clone @ `961a4d35` (branch `naya5/human-value-real-data-v1`):

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `961a4d35e931747c94076d8a43487d0ebaa389c8` | (same) | ✅ |
| `ledger_sha256` | `sha256:e28ab77b…89d9b` | (same) | ✅ |
| `hv_per_day_total` | 2.8572 | 2.8572 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 19 | 19 | ✅ |
| `calibration.n` / MAE / bias | 3 / 0.1667 / 0.1667 | 3 / 0.1667 / 0.1667 | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the third real prediction→observation join (n=3, DEC-003) is
cold-recomputable at the pushed SHA. MAE 0.25→0.1667, signed bias
+0.25→+0.1667, no overprediction — the n>=3 recalibration floor is now
measurable by any cold successor from canonical repo bytes alone.
Run note: the first cold attempt of this run caught a stale era-pinned test
(`n == 2` hardcoded); the test was updated to pin the new floor
(`n >= 3`, LEARN_CANDIDATE proposes, never promotes) and both sides re-ran
green before this proof. /tmp clones removed after verification.

## Fifth cold run — 2026-10-09 03:48 UTC (29-event ledger, n=4 join)

Fresh clone @ `b60ebc6b` (branch `naya5/human-value-events-20261009`), same
procedure, no access to the originating workspace:

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `b60ebc6b` | `b60ebc6b` | ✅ |
| `ledger_sha256` | `sha256:90c7b3fe723f172cc2ddb7fe7540823df3a8de513da64db9d02130fe0ff8ceb3` | (same) | ✅ |
| `hv_per_day_total` | 4.2857 | 4.2857 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 29 | 29 | ✅ |
| `calibration.n` / MAE / signed bias | 4 / 0.125 / +0.125 | 4 / 0.125 / +0.125 | ✅ |
| overprediction | false | false | ✅ |
| test suite | 10 passed | 10 passed | ✅ |

**Verdict:** the n=4 measurement is cold-recomputable at the branch's final
state. The DEC-004 outcome event's `delta_v_actual: 7.0` stands: push +
cold-recompute proof verified; scorecard posts next.
