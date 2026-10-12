# SGF Daily Runner — "She Goes Forever" operationalized (Lane 6, tick t992)

**Spec owner:** Lane 1 (Naya Verity) — the spec, runner, rubric, and blinding protocol
at `hidden_files/lane-1/she-goes-forever/` are READ-ONLY for Lane 6. This directory
operationalizes her t972 design (scored 9.0/10) as a daily-cron-ready runner.
Nothing here redesigns the spec; it reuses `sgf_runner.py`'s stage functions
verbatim (imported as a module), with run state kept under Lane 6 so Lane 1's
task-pool counter and canonical `sgf_history.jsonl` are never touched by the runner.

## What this is

One-command-per-phase runner for the daily cold-Naya acceptance test:

| Phase | Command | What it does |
|---|---|---|
| seal | `run_daily.sh --phase seal [--date D] [--task T2] [--kind NORMAL]` | select slot (read-only counter, never consumed) → `--brief` → `--seal`. Prints the cold-successor spawn prompt. |
| normalize | `run_daily.sh --phase normalize --run-dir DIR` | verifies evidence exists, builds `scorer/blinded-evidence.json`, prints the blinded-scorer spawn prompt. |
| score | `run_daily.sh --phase score --run-dir DIR --scorer-scores P` | runs Lane 1's M1–M5 + verdict computation (base-patched so the history line lands here as `pending-history.jsonl`), verifies every artifact exists, prints the verdict. |

The two agent spawns (cold successor, blinded scorer) are inherently agent
actions — the script prints the exact spawn prompt at the right moment, and
`CRON-SPEC.md` documents the full daily loop for the installing seat.

## Evidence layout (mirrors Lane 1's convention)

```
sgf-daily/
├── run_daily.sh              # the runner (this file's subject)
├── README.md                 # this file
├── CRON-SPEC.md              # install artifact: schedule, command, evidence path, alerting
└── run-<date>-<task>/        # one dir per run, e.g. run-2026-10-11-T2/
    ├── task-selection.json   # slot, kind, brain SHA (schema = stage_select)
    ├── cold-brief.md         # the brief the successor was spawned with (sha pinned)
    ├── seal-receipt.json     # sealed BEFORE the successor spawned
    ├── claim-manifest.json   # candidate-level claim, material refs filled from seal
    ├── successor/evidence.json
    ├── scorer/blinded-evidence.json   # normalized (paths/timestamps rewritten)
    ├── scorer/scores.json             # blinded scorer's D1-D4 + blinded_q
    ├── scorecard.json        # M1-M5 + blinded_q + daily_score + verdict
    ├── verdict.json          # CAPABILITY-TRANSFERS / CAPABILITY-DRIFT
    └── pending-history.jsonl # the drift-ledger line, queued for canonical append
```

## Design decisions (and why)

- **Lane 1 stays read-only.** Selection mimics `stage_select`'s schema but never
  writes `task-pool.md`; scoring appends the history line to a Lane-6 pending file.
  The installing seat moves the validated line into Lane 1's canonical
  `sgf_history.jsonl` with the spec owner's sign-off — documented in CRON-SPEC.md.
- **No redesign.** `sgf_runner.py`'s `--brief`, `--seal`, and `stage_score` are
  called as-is; only the history-file base path is patched, and that is stated
  openly in the script and every scorecard note.
- **Workspace-first policy.** All artifacts live on workspace paths; nothing
  written to /tmp except the successor's tiny scratch bytes (the /tmp-full
  incident lesson from Lane 1's journal).
- **A correct REFUTED earns transfer.** The capability verdict measures the
  successor's honesty and rigor, never whether the day's underlying claim was true.

## Provenance

Dry run t992 (2026-10-11, T2/NORMAL): see run dir `run-2026-10-11-T2/` and the
receipt `hidden_files/twelve-lane-receipts/t992-lane6.md`. Repo review artifact:
branch `naya/six-sgf-daily-runner-t992` carrying `tools/sgf_daily/` (same content
as this directory, minus per-run evidence dirs).
