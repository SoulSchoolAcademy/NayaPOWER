# Learn-clock — the measurement instrument for near-instant learning

Shawn's target: a live failure becomes a verified behavior change in a
cold successor within **60 minutes**. This package makes "near-instant"
a number. It measures; it does not change behavior.

- **Learning latency = T6 − T0** (minutes). Target: ≤ 60.
- **Fail-closed:** no T6, no claim. `meets_target()` is `False` until T6
  exists. Missing stages are reported, never silently skipped.
- **T6 or it didn't happen.** Filing a note (T3) is not learning.

## Files in this package

| File | What it is | Lines |
|---|---|---|
| `learn_clock.py` | The clock: append-only JSONL, in-order stages, metrics | 149 |
| `learn_hook.py` | The CLI wiring between live work and the clock | 146 |
| `test_learn_clock.py` | 16-test battery for the clock | 187 |
| `test_learn_hook.py` | 7-test battery for the hook (incl. the F-3 pins) | 115 |
| `README.md` | This file | — |
| `WIRING.md` | Where each `emit()` belongs, the T6 guard, bootstrap | — |

Line counts from the F-3 commit (`aa01c1ec0`); tests: **23 passed**
(16 clock + 7 hook) on that commit's tree.

## The eight stages (all UTC)

| Stage | Name | Means |
|---|---|---|
| T0 | EVENT | The failure / win / surprise is observed |
| T1 | CAPTURED | A capture candidate exists (note, sign-out pair) |
| T2 | TRIAGED | Intake verdict: PROMOTE / LOG / DROP, with scores |
| T3 | DISTILLED | One-sentence principle + its enforcement named |
| T4 | INJECTED | The principle is in a worker's live thinking context |
| T5 | APPLIED | A worker is observed acting differently because of it |
| T6 | VERIFIED | Control vs treatment proves it (different seat judges) |
| T7 | COMPOUNDED | The machinery changed (briefing / law / checker) |

T7 is recorded but never moves the latency number (latency = T6 − T0).

## Quick start — the hook CLI (the normal path)

Run from the repo root. The hook writes to the repo log paths (below).

```sh
python3 tools/learning/learn_clock/learn_hook.py t0 --title "push wrote through a symlink" --evidence "wave log + broken python"
# prints the lesson id, e.g. LESSON_ID=LC-20261014-001
python3 tools/learning/learn_clock/learn_hook.py t1 LC-20261014-001 --evidence "sign-out win+why filed"
# ... t2 .. t7 as each stage becomes true, with --evidence every time
```

- `--evidence` is **required** for every emit (fail-closed).
- Stages must arrive **in order**; out-of-order, duplicate, or
  timestamp-regressed emits raise `OutOfOrderError` (the hook exits
  loudly instead of writing).
- `t0` mints the lesson id (`LC-YYYYMMDD-NNN`); never pass an id to `t0`.
- `--ts "<ISO UTC>"` is for **retroactive reconstruction only** (the
  spec's bootstrap step). Live emits use now. See WIRING.md.

## Quick start — the Python API

Repo-root imports (the scratch-era `from learn_clock import ...` is stale
for the repo home — do not use it):

```python
from tools.learning.learn_clock.learn_clock import LearnClock, OutOfOrderError

clock = LearnClock()                       # default: repo log (below)
clock.emit("LC-DEMO-001", 0)                # T0 — the failure is observed
# ... stages 1..6 as each becomes true ...
print(clock.latency("LC-DEMO-001"))         # minutes, T6 − T0; None until T6
print(clock.meets_target("LC-DEMO-001"))    # True only if ≤ 60 and T6 exists
print(clock.lags("LC-DEMO-001"))            # capture / injection / verification lag
print(clock.status("LC-DEMO-001"))          # hit vs missing stages
```

Module-level functions (`emit`, `status`, `latency`, `lags`,
`meets_target`) wrap a default `LearnClock()` on the repo log.

**Demo discipline:** never rehearse against the real log. Pass an
explicit tmp path — `LearnClock(tmp_path / "lc.jsonl")` — or use the
hook's test seams (`main(..., clock_path=..., meta_log=...)`). A demo
emit on the real log is a false lesson in the permanent record.

## Log paths — runtime data, never in the code tree

| Log | Default path (repo-relative) | Rows |
|---|---|---|
| Clock | `BRAIN/07-LEARNING/learn-clock/learn-clock.jsonl` | `{lesson_id, stage, stage_name, ts}` |
| Meta | `BRAIN/07-LEARNING/learn-clock/learn-lessons.jsonl` | `{lesson_id, stage, stage_name, ts, written_ts, title, evidence}` |

- Both paths are computed from the file location (`parents[3]`), never
  from the current working directory and never from scratch.
- The `BRAIN/07-LEARNING/learn-clock/` directory does **not** exist in
  the repo — it is created on first emit (`mkdir(parents=True)`).
  Runtime data is never committed.
- `ts` is the **event time** (== the clock row's `ts`, including on
  retroactive `--ts` — the F-3 fix). `written_ts` is the **append time**.
  Rows written before the F-3 fix carried `ts` == write time; the clock
  JSONL is authoritative for event times on those rows.
- Scratch JSONL data was **not** carried into the repo. The repo log
  starts empty.

## Secondary metrics

- `capture_lag` = T1 − T0 (is capture automatic yet?)
- `injection_lag` = T4 − T3 (does the machinery carry it?)
- `verification_lag` = T6 − T5 (can we prove it?)
- Each is `None` when unmeasurable.

## History — F-1 → F-2 → F-3, as actually built

- **F-1 — the instrument.** `learn_clock.py` + the 16-test battery,
  built in scratch (`~/workspace/_scratch/learn-clock/`), 16-test
  battery (16/16 green per the w140 graduation packet).
  The T5 application-receipt instrument — the E2 witness for the
  retrieval → application binding — lives separately at
  `tools/learning_application_receipt.py` (already on main; not part of
  this package). Its T5 chunk was validated by a different seat
  (Alpha, w145, ACCEPT 9.5/10, per the w146 F-2 receipt's record of
  w145).
- **F-2 — the T6 judge-seat guard.** Implemented in
  `tools/lesson_verification.py` on branch
  `naya5/eta-w146-learnclock-f2` (commit
  `1445cafd2d6408b9d793c61c54603512af86be4a`, local-only at F-4 time;
  different-seat validation ACCEPT 9.5/10, Alpha w147). **It is NOT in
  this branch and NOT in this package** — at the F-3 head,
  `tools/lesson_verification.py` contains zero seat-guard symbols
  (verified by grep). WIRING.md documents the guard's contract so the
  wiring is ready when it lands; it does not claim the guard is here.
- **F-3 — the carry (this package).** Commit `aa01c1ec0` carried
  `learn_clock.py` + `learn_hook.py` + both batteries from scratch into
  `tools/learning/learn_clock/` (4 files, +597), repointing
  `DEFAULT_LOG` / `META_LOG` to `BRAIN/07-LEARNING/learn-clock/`.
  **No logic changed in the carry** except the paths, the F-3 hook
  meta-`ts` fix (below), and test seams (`main(clock_path, meta_log)`,
  `_meta_write(meta_log)`) so tests never touch the real log.
- **F-3 fix (the reason F-3 exists).** Before F-3, the hook meta log
  ignored retroactive `--ts`: `_meta_write()` always stamped wall-clock
  `now`, so bootstrap meta rows carried mint-time while the clock JSONL
  carried the true retroactive stamp. The fix: meta `ts` == the clock
  row's event `ts` (`event_ts=rec["ts"]`), with `written_ts` recording
  the append time. Three of the seven hook tests pin the fix and fail
  against pre-fix behavior (negative control verified in the F-3
  commit).

## What this package does NOT claim

- **No emit() wiring.** No T0–T7 call sites exist anywhere. Graduation
  ships the instrument; wiring ships the behavior. WIRING.md is the
  wiring plan, not wiring.
- **No F-2.** See F-2 above: the guard is a separate branch, not here.
- **No graduation PR, no merge.** This branch is docs + carry only.
- **No spec file in the repo.** `learn_clock.py`'s docstring cites
  `learn-clock-spec.md`, but no such file exists in the repo tree at
  the F-3 head — the spec lives in the goal working files
  (`hidden_files/learn-clock-spec.md`). That dangling reference is a
  known doc defect, reported in the F-4 receipt, not fixed here
  (docs-only mission; the code docstring is untouched).

## Tests

```sh
python3 -m pytest tools/learning/learn_clock/ -q   # 23 passed
```

The clock battery pins: known latency (45 min), `None` before T6,
out-of-order / duplicate / regression rejection, bad-stage rejection,
missing-stage status, target true/false incl. custom minutes,
concurrent lessons, retroactive bootstrap (260 min → target `False`),
secondary lags, T7-beyond-latency, emit receipt shape, module-level API.
The hook battery pins: meta `ts` == clock `ts` on retroactive and live
emits, `written_ts` > retroactive `ts`, both default logs under the
repo path (never scratch), missing-`--evidence` rejection (exit 2),
sequential `LC-YYYYMMDD-NNN` ids.
