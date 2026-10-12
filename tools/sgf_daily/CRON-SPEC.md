# CRON SPEC — "She Goes Forever" daily cold-Naya acceptance run

**For:** a credentialed seat (the Team Naya dispatcher, or a lane agent with cron
authority) to install. Installing a cron is a credentialed action — this document
is the complete install artifact; no guesswork required.

## Schedule

- **Cadence:** daily, 06:30 Pacific. Chosen to land before the team's morning
  brief cycle and after any overnight tip churn settles.
- **Wall-time budget:** 30–60 min per run (two subagent spawns dominate; mechanical
  phases are seconds).
- **Cost:** 2 subagent spawns/day ≈ two lane-dispatch briefs. Git protocol only
  for repo reads; zero GitHub Actions minutes; zero REST except on alert.

## Command (the daily loop)

The installing seat (an agent with subagent-spawn authority) runs, in order:

```bash
D=~/workspace/goals/bring-naya-to-life/hidden_files/lane-6/sgf-daily
# 1. SEAL — selects the slot, writes brief, seals BEFORE any agent is spawned.
$D/run_daily.sh --phase seal
#    -> prints the cold-successor spawn prompt (brief path + evidence output path)
# 2. Spawn ONE fresh subagent with the brief ONLY. Wait for successor/evidence.json.
# 3. NORMALIZE — builds the blinded evidence and prints the scorer spawn prompt.
$D/run_daily.sh --phase normalize --run-dir <printed run dir>
# 4. Spawn a DIFFERENT fresh subagent with claim + rubric + blinded evidence ONLY.
#    Save its JSON output to <run dir>/scorer/scores.json.
# 5. SCORE — mechanical checks + machine-computed verdict.
$D/run_daily.sh --phase score --run-dir <run dir> --scorer-scores <run dir>/scorer/scores.json
```

Step 5 refuses to run on missing evidence/scores and refuses to score a run whose
seal does not predate the successor's first write (M5). A failed phase = the run
is recorded as INVALID/failed in the run dir, not silently retried with the same
spawn (three-try circuit breaker applies to spawns, not phases).

## Evidence path

`~/workspace/goals/bring-naya-to-life/hidden_files/lane-6/sgf-daily/run-<date>-<task>/`
(see README.md for the per-file contract). The runner refuses to finish `--phase
score` unless all nine artifacts exist and are non-empty.

## History-ledger handoff (Lane 1 sign-off required)

Each run produces `pending-history.jsonl` (one JSON line: date, task, kind,
mech_pass_rate, blinded_q, daily_score, capability_verdict). The installing seat:

1. Sends the line to the spec owner (Naya Verity, Lane 1) with the run dir path —
   lane feed #2175, one comment.
2. On her sign-off, appends the line to
   `hidden_files/lane-1/she-goes-forever/sgf_history.jsonl` and increments that
   lane's `rotation_counter` so the production rotation advances exactly one slot
   per completed run.
3. Until that handoff exists, the runner itself NEVER writes Lane 1's files.

This keeps spec ownership with Lane 1 while the daily machine runs unattended.

## Failure alerting

| Condition | Action |
|---|---|
| verdict == **CAPABILITY-DRIFT** | Post to #2175 the same hour: run dir, which check failed (M2? M3? blinded_q?), the evidence rows. This is the mission's early-warning light — never batch it. |
| drift_7d drops ≥ 1.5 vs previous 7-run window | Weekly trend post to #2175 (computed from `sgf_history.jsonl`). |
| Run INVALID (seal breach, empty evidence, missing scores) | Record INVALID in the run dir + one #2175 line; re-run next day (same slot, counter not consumed). Never invent scores. |
| A task needs production telemetry / credentials / destructive ops / Shawn's word | Mark **SKIPPED-GATED** in the run dir; do not work around it; note the gate in the #2175 sign-out. |

## Gates this spec never crosses

The runner never: runs Lane 6's full B→C acceptance (PARKED — Shawn's word),
touches production deploy paths/credentials/money/destructive ops, changes
authority/privacy/consent posture, or marks anything ratified/deployed. If a slot
is SGF-INELIGIBLE by these rules, the seat records SKIPPED-GATED and moves on.

## Rollback

Disable the schedule; the last good run dir and the canonical history ledger are
untouched. No state is created anywhere except the run dir and the one appended
history line per completed run.
