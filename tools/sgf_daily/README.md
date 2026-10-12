# SGF Daily Runner — "She Goes Forever" operationalized (Lane 6, tick t992)

**Spec owner:** Lane 1 (Naya Verity) — the spec, runner, rubric, and blinding protocol
at `hidden_files/lane-1/she-goes-forever/` are READ-ONLY for Lane 6. This directory
operationalizes her t972 design (scored 9.0/10) as a daily-cron-ready runner.
`--brief`/`--seal` reuse `sgf_runner.py`'s stage functions verbatim (imported
as a module); `--score` runs the Lane-6 vendored scoring port
(`sgf_daily_score.py`, pin-verified) so the t0172 M6 swallower-veto rides in
the runner's own bytes. Run state is kept under Lane 6 so Lane 1's task-pool
counter and canonical `sgf_history.jsonl` are never touched by the runner.

## What this is

One-command-per-phase runner for the daily cold-Naya acceptance test:

| Phase | Command | What it does |
|---|---|---|
| seal | `run_daily.sh --phase seal [--date D] [--task T2] [--kind NORMAL]` | select slot (read-only counter, never consumed) → `--brief` → `--seal`. Prints the cold-successor spawn prompt. |
| normalize | `run_daily.sh --phase normalize --run-dir DIR` | verifies evidence exists, builds `scorer/blinded-evidence.json`, prints the blinded-scorer spawn prompt. |
| score | `run_daily.sh --phase score --run-dir DIR --scorer-scores P` | runs the vendored M1–M6 scoring port (pin-verified so the history line lands here as `pending-history.jsonl`), verifies every artifact exists, prints the verdict. |

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
- **No redesign.** `sgf_runner.py`'s `--brief` and `--seal` stages are
  called as-is; the `--score` stage runs the Lane-6 vendored port
  (`sgf_daily_score.py`), pinned to Lane-1 source sha256
  `6326d8c1b42cbb2e1c3aad1f093d992e39a5bdaee7326b04ade2dcc7bd8c78ff` and
  carrying the t0172 M6 swallower-veto. `run_daily.sh --phase score` refuses
  to run unless the vendored file matches its baked-in pin — the daily
  instrument never scores on bytes it did not test.
- **CT-4 double-negative cross-check rides on the branch.**
  `ct4_cross_check.py` implements CTA-PROTOCOL-v2 §4 CT-4 as executable bytes:
  TWO independent remote reads (targeted ref lookup AND full-listing filter)
  must both agree on a branch's absence before PHANTOM_CAUGHT; disagreement
  refuses as UNABLE_TO_VERIFY (this is what v1's single lookup could not
  distinguish from a transient failure). The v2 G2 anti-elision rule is
  exposed as `assert_rows_elision_free()` for successor-recorded rows — a
  catch on elided rows is UNPROVEN_CATCH, never trusted.
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
