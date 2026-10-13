# intelligence/tools/learn — practice harness for hyper-speed learning

Piano practice for principles: scenario drills drawn from REAL past
violations, rubric-scored responses, groove ledger with recency decay,
spaced repetition. Owned by the LEARN lane (Naya Alpha).

## Files

| File | Role |
|---|---|
| `exercise.py` | EXERCISE v1.1 harness — `score_response` heuristic rubric (v1.1: verb-sense redo-verb matching), groove-ledger math, `due`/`round`/`status`/`test` commands |
| `violation-bank.json` | Drill scenarios: real past violations, one per scenario, with pass/fail signals and correct behavior |
| `test_verb_sense_guard.py` | 8-check guard pinning the P-008 rubric artifact (2026-10-13): the pre-fix rubric scored semantically rich responses FLAT; v1.1 passes them while still biting on minimized redo |
| `check_learn_artifacts_present.py` | P-013 presence gate: fails loudly (nonzero exit, named files) if any artifact is absent from the repo tree — a tip move that loses the artifacts must not silently "pass" |

## Running

```bash
python intelligence/tools/learn/check_learn_artifacts_present.py
python intelligence/tools/learn/test_verb_sense_guard.py
python intelligence/tools/learn/exercise.py --principles <principle-ledger.json> test
```

The practice commands (`due`/`round`/`status`) need a principle ledger;
pass `--principles <file>` pointing at the canonical ledger (the goal
workspace's `daily-learning-review/principle-ledger.json`) — the harness
carries no default and fails with a clear message otherwise.

## CI

`kernel-tests.yml` runs the presence check and the guard on every PR.
`exercise.py test` is local-only (it needs a principle ledger).

## Provenance

Authored in the goal workspace 2026-10-12/13 by Naya Alpha (LEARN lane):
the P-008 EXERCISE artifact, the verb-sense rubric fix, and the wave-32
retention drill that found the artifacts were authored but never committed.
Mechanized into the repo 2026-10-13 as the P-013 follow-up: authored is not
enforced — the presence gate makes non-mechanization a loud failure.
