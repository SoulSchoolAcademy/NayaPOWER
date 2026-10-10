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

## Sixth cold run — 2026-10-09 ~09:55 UTC (39-event ledger, n=5 join)

Fresh clone @ `8f9ee42b` (branch `naya5/human-value-events-20261009`, rebased
onto live tip `925e4c348`), same procedure, no access to the originating
workspace:

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `8f9ee42b` | `8f9ee42b` | ✅ |
| `ledger_sha256` | `sha256:e1b8ed34…35db0f` | (same) | ✅ |
| `hv_per_day_total` | 5.7143 | 5.7143 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 39 | 39 | ✅ |
| `calibration.n` / MAE / signed bias | 5 / 0.1 / +0.1 | 5 / 0.1 / +0.1 | ✅ |
| overprediction | false | false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the n=5 measurement (DEC-005, predicted +7.0 at 09:45 UTC before
any ledger change, observed +7.0) is cold-recomputable at the pushed SHA. The
calibration series now reads MAE 0.5 → 0.25 → 0.1667 → 0.125 → 0.1 across five
real joins, signed bias shrinking in the same steps, zero overprediction
flags. /tmp clones removed after verification.

## Seventh cold-recompute proof — n=6 loop (2026-10-09 ~16:05 UTC)

Fresh clone of `naya5/human-value-events-20261009` @ `d8e987f076fa5913dcf9a82660a7701741477cbd`
(rebased onto live tip `3a60163c9`), same procedure, no access to the originating
workspace:

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `d8e987f0` | `d8e987f0` | ✅ |
| `ledger_sha256` | `sha256:deb7a79c…9a049114` | (same) | ✅ |
| `hv_per_day_total` | 6.7143 | 6.7143 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 46 | 46 | ✅ |
| `calibration.n` / MAE / signed bias | 6 / 0.0833 / +0.0833 | 6 / 0.0833 / +0.0833 | ✅ |
| overprediction | false | false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the n=6 measurement (DEC-006, predicted +7.0 at 15:50 UTC before
any ledger change, observed +7.0) is cold-recomputable at the pushed SHA. The
calibration series now reads MAE 0.5 → 0.25 → 0.1667 → 0.125 → 0.1 → 0.0833
across six real joins, signed bias shrinking in the same steps, zero
overprediction flags. /tmp/hv-cold removed after verification.

## Eighth cold-recompute proof — n=7 loop (2026-10-09 ~22:00 UTC)

Fresh clone of `naya5/human-value-events-20261009-2141` @ `5766dda2298dbd6035a8593f23b39518061d0ed2`
(on live tip `7b8f8be89768e1e79e3fe2dcfcd0b10b5e85291d`), same procedure, no access to the originating
workspace:

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `5766dda2` | `5766dda2` | ✅ |
| `ledger_sha256` | `sha256:370730d9…e6507e8e1d` | (same) | ✅ |
| `hv_per_day_total` | 8.2857 | 8.2857 | ✅ |
| `dai_per_day` | 0.2857 | 0.2857 | ✅ |
| `events_validated` | 57 | 57 | ✅ |
| `calibration.n` / MAE / overprediction | 7 / 0.0714 / false | 7 / 0.0714 / false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the n=7 measurement (DEC-007, predicted +7.0 at 21:47 UTC before
any ledger change, observed +7.0) is cold-recomputable at the pushed SHA. The
calibration series now reads MAE 0.5 → 0.25 → 0.1667 → 0.125 → 0.1 → 0.0833 → 0.0714
across seven real joins, zero overprediction flags. /tmp/hv-cold-2141 removed after verification.

**State note (unchanged):** PR #1939 (human-value events n=6) merged to main at
`0f033ac2e` with ZERO reviews — the independent-seat verification of the ledger
itself remains unmet; the cold-recompute proof above is reproducibility, not
independent human verification. DAI series is ~3.5 days of real data; trend
readable after 2+ weeks.

## Ninth cold-recompute proof — n=8 loop (2026-10-10 ~04:00 UTC)

Fresh clone of `naya5/human-value-events-20261010-0341` @ `b4be5ec6afcbf8afe78bf4fdf82355a0c833eb57`
(rebased onto live tip `8a41a18e2` before push — the DEC-007 carry-forward commits
`9c088e1e`/`3c94b318` and `0ca7c572` restored main's ledger from 46 to the verified 57-event state,
plus the n=8 accumulation `b4be5ec6`), same procedure, no access to the originating
workspace:

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `b4be5ec6` | `b4be5ec6` | ✅ |
| `ledger_sha256` | `sha256:70b2bf77…1dff48b` | (same) | ✅ |
| `hv_per_day_total` | 10.2856 | 10.2856 | ✅ |
| `dai_per_day` | 0.5714 | 0.5714 | ✅ |
| `events_validated` | 71 | 71 | ✅ |
| `calibration.n` / MAE / bias / overprediction | 8 / 0.0625 / +0.0625 / false | 8 / 0.0625 / +0.0625 / false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the n=8 measurement (DEC-008, predicted +7.0 at 03:50 UTC before
any ledger change, observed +7.0) is cold-recomputable at the pushed SHA. The
calibration series now reads MAE 0.5 → 0.25 → 0.1667 → 0.125 → 0.1 → 0.0833 → 0.0714 → 0.0625
across eight real joins, signed bias +0.0625 (the single 6.5 prediction at DEC-001 still
dominates the bias term), zero overprediction flags. /tmp/hv-cold-0341 removed after verification.

**State note (unchanged):** no independent seat has yet cold-recomputed the ledger
per this file and posted a verdict on #1604 — reproducibility is proven, independent
human verification of the ledger itself remains the binding 8.0 gate. DAI series is
~4 days of real data (0.5714/day this window: two genuine attention demands — #2068
awaiting Shawn's click, prod-readiness C10 awaiting his word); trend readable after 2+ weeks.

## Tenth cold-recompute proof — n=9 loop (2026-10-10 ~09:55 UTC)

Fresh clone of `naya5/human-value-events-20261010-0341` @ `05643642f0c4119cd18a8741e60a57fecb4b67ee`
(rebased onto live tip `fe25661c5` before push — the n=9 accumulation `05643642`:
DEC-009 pre-registered, PR #2108 merged-verified outcome, join closed at honest
+6.5), same procedure, no access to the originating workspace:

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `05643642` | `05643642` | ✅ |
| `ledger_sha256` | `sha256:f6df6368…64e8fb66` | (same) | ✅ |
| `hv_per_day_total` | 10.5713 | 10.5713 | ✅ |
| `dai_per_day` | 0.5714 | 0.5714 | ✅ |
| `events_validated` | 73 | 73 | ✅ |
| `calibration.n` / MAE / bias / overprediction | 9 / 0.1111 / 0.0 / false | 9 / 0.1111 / 0.0 / false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the n=9 measurement (DEC-009, predicted +7.0 at 09:44 UTC before
any ledger change, observed +6.5) is cold-recomputable at the pushed SHA. The
calibration series now reads MAE 0.5 → 0.25 → 0.1667 → 0.125 → 0.1 → 0.0833 → 0.0714 → 0.0625 → 0.1111
across nine real joins, signed bias back to 0.0 (the single early under-prediction
error +0.5 and this window's thin-window miss −0.5 cancel), zero overprediction
flags. This is the loop working as designed: the +7.0 prediction was "consistent
with prior loops"; the window's thin material (1 verified outcome vs 11 in DEC-008)
was observed honestly at +6.5 instead of rubber-stamped, and the calibration
absorbed the miss. /tmp/hv-cold-0941 removed after verification.

**State note (unchanged):** no independent seat has yet cold-recomputed the ledger
per this file and posted a verdict on #1604 — reproducibility is proven, independent
human verification of the ledger itself remains the binding 8.0 gate. DAI series is
~5 days of real data (0.5714/day, flat this window: zero new human-attention demands —
the brain-index red and the draft→ready tooling failure were both team-handled,
#2068's wait for Shawn's click is a continuing demand, not a new one); trend
readable after 2+ weeks.

## Eleventh cold-recompute proof — n=9 loop at rebased head (2026-10-10 ~16:00 UTC)

Fresh clone of `naya5/human-value-events-20261010-0341` @ `45c8035d337fd88db5a4389523bf5aade0ef530a`
(rebased onto live tip `7281ede6b` — the #2142 tune-in-template merge; no ledger
changes since the tenth proof), same procedure, no access to the originating
workspace. Clone at `~/workspace/_scratch/hv-cold-1541` (fresh checkout;
`/tmp` is a 512M tmpfs and filled mid-clone — scratch removed after verification).

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `45c8035d3` | `45c8035d3` | ✅ |
| `ledger_sha256` | `sha256:f6df6368…64e8fb66` | (same) | ✅ |
| `hv_per_day_total` | 10.5713 | 10.5713 | ✅ |
| `dai_per_day` | 0.5714 | 0.5714 | ✅ |
| `events_validated` | 73 | 73 | ✅ |
| `calibration.n` / MAE / bias / overprediction | 9 / 0.1111 / 0.0 / false | 9 / 0.1111 / 0.0 / false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the rebase onto the live tip preserved the ledger byte-for-byte; the
n=9 measurement remains cold-recomputable at the rebased head. Merge rehearsal
(worktree @ `7281ede6b` + `git merge --no-commit --no-ff`): true delta is exactly
the branch's 3 ledger files — no main-as-reversions artifact. Full pytest on the
merged tree: 25 failed, all reproducing identically on pristine `7281ede6b`
(control worktree) — pre-existing main redness (`tools/test_activation_checklist.py`
expects ref `origin/brain-build/operating-code-v2`, absent here); zero failures
from this branch. Merge gate honestly blocked on main's redness (Naya 4's #2062
repair lane), not on this branch. Push deferred: GitHub API 403'd 15:55 UTC
post-sign-in; push + DEC-010 window close resume post-reset.

**State note (unchanged):** no independent seat has yet cold-recomputed the ledger
per this file and posted a verdict on #1604 — reproducibility is proven,
independent human verification of the ledger itself remains the binding 8.0 gate.
DAI series is ~5 days of real data; trend readable after 2+ weeks.

## Twelfth cold-recompute proof — n=10 loop (2026-10-10 ~16:05 UTC)

Fresh clone of `naya5/human-value-events-20261010-0341` @ `d3aba03508c85a3f56d8e41af66ea20b0023293c`
(DEC-010: pre-registered 16:02:44Z at +7.0, 18 verified window events appended,
join closed at honest +7.0), same procedure, no access to the originating workspace.
Clone at `~/workspace/_scratch/hv-cold-1602` (fresh checkout; scratch removed after verification).

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `d3aba0350` | `d3aba0350` | ✅ |
| `ledger_sha256` | `sha256:1953a48b…23e5eb7b28` | (same) | ✅ |
| `hv_per_day_total` | 13.2857 | 13.2857 | ✅ |
| `dai_per_day` | 0.5714 | 0.5714 | ✅ |
| `events_validated` | 92 | 92 | ✅ |
| `calibration.n` / MAE / bias / overprediction | 10 / 0.1 / 0.0 / false | 10 / 0.1 / 0.0 / false | ✅ |
| test suite (real ledger + instrument) | 36 passed | 36 passed | ✅ |

**Verdict:** the n=10 measurement (DEC-010, predicted +7.0 at 16:02:44Z before any
ledger change, observed +7.0) is cold-recomputable at the pushed SHA. The window
was genuinely rich — 18 verified outcome events including Shawn's ratification of
Operating Code V2 landing on main (#2087, API-verified merged), the 45-law operating
law (#2122), the tune-in template (#2142, on the live tip), the amendment loader
(#2129), the gate console (#2127), four gate-hold releases (#2092/#2096/#2098/#2099),
four enforcement-gate/learning-loop merges (#2094/#2095/#2114/#2115/#2116), the #2113
revert, #2117, #2120 — plus the 308-branch graveyard cleanup. DAI flat at 0.5714:
zero new human-attention demands (#2068's wait for Shawn's click is a continuing
demand, already recorded; WS-9/WS-4 blockers and CI reds are team-handled). MAE
improved 0.1111 → 0.1, bias 0.0, zero overprediction flags across ten real joins.
Excluded with reasons (anti-inflation): Naya 4's driver self-completions, Naya 5's
own CI-heal/hourly-report items, Shawn's direction relays (coordination, not outcome),
the token fix (asserted in live plan, no durable feed evidence found on #1354/#1604).

**State note (unchanged):** no independent seat has yet cold-recomputed the ledger
per this file and posted a verdict on #1604 — reproducibility is proven, independent
human verification of the ledger itself remains the binding 8.0 gate. DAI series is
~5 days of real data; trend readable after 2+ weeks.

## Thirteenth cold-recompute proof — n=11 loop (2026-10-10 ~22:05 UTC)

Same procedure, fresh clone @ `b2546fc4f1675915dbbc52fc821bf3a676eaa078`
(branch `naya5/human-value-events-20261010-0341`, rebased onto live tip
`cfbd81cca6`; the rebase collapsed the branch's prior ledger commits into one
tree-identical commit — ledger bytes byte-for-byte identical across the rebase,
verified by hash before/after):

| Check | Originating worktree | Cold clone | Match |
|---|---|---|---|
| HEAD | `b2546fc4` | `b2546fc4` | ✅ |
| `ledger_sha256` | `sha256:dddd6c21a22c40a8056f7ca0b5899510489f252334d5d5e8837a5ce4da08f433` | (same) | ✅ |
| `hv_per_day_total` | 14.4285 | 14.4285 | ✅ |
| `dai_per_day` | 0.5714 (flat — zero new human-attention demands) | 0.5714 | ✅ |
| `events_validated` | 102 | 102 | ✅ |
| `calibration.n` / MAE / bias | 11 / 0.0909 / 0.0 | 11 / 0.0909 / 0.0 | ✅ |
| test suite | 36 passed | 36 passed | ✅ |

**Anti-inflation note (new this run):** DEC-011 scored two of Shawn's own merges
(#2173, #2187 — mission-state snapshots without a brain-index re-stamp, the 7th
and 8th drift occurrences) at **−3.0** durable value instead of hiding them:
verified rework (repair lanes dispatched, CI red at the exact tip). The loop's
value is in the honesty — a ledger that only ever goes up is a decoration, not
an instrument. Predicted aggregate +4.0 → observed +4.0; all 9 per-decision
components verified as predicted at 21:50Z. Calibration bias stays 0.0, MAE
improved 0.1 → 0.0909, no overprediction. (Encoding discipline: per-decision
signed signals live in the prediction record and the join event only — a
mid-run encoding put delta_v_actual on two outcome events and briefly
double-counted the join; caught and corrected before push. One decision, one
observation row.)

**State note (unchanged):** no independent seat has yet cold-recomputed the ledger
per this file and posted a verdict on #1604 — reproducibility is proven, independent
human verification of the ledger itself remains the binding 8.0 gate. DAI series is
~5 days of real data; trend readable after 2+ weeks.
