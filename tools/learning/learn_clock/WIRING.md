# Wiring the learn-clock — a worker's guide

The clock measures; it does not change behavior. Put `emit()` calls at
the exact moment each stage becomes true — never earlier (that
manufactures green), never in bulk at the end (that manufactures
history).

**Status:** this is the wiring PLAN. No call sites are wired yet
(README.md, "What this package does NOT claim"). Wire one stage at a
time, with its evidence, in later chunks — never a bulk backfill.

## Where each emit belongs

| Stage | Emit when | Example call site |
|---|---|---|
| T0 EVENT | the failure/win/surprise is observed | the moment a test goes red, a 403 lands, a false fire is caught |
| T1 CAPTURED | a capture candidate exists | sign-out writes the win+why / failure+fix pair; the triage queue receives it |
| T2 TRIAGED | intake returns a verdict | the triage pass records PROMOTE / LOG / DROP with scores |
| T3 DISTILLED | the one-sentence principle + its enforcement are written | the Smart Note is filed with its enforcement named |
| T4 INJECTED | the principle is in a worker's live thinking context | the injection/broadcast pass includes it in a brief — being in a file doesn't count |
| T5 APPLIED | a worker is observed acting differently because of it | a sign-out names the changed decision and the lesson that changed it |
| T6 VERIFIED | control vs treatment proves it | a cold successor passes a held-out task the control failed — judged by a different seat (see the T6 guard below) |
| T7 COMPOUNDED | the machinery changed | the briefing, law, or checker is updated — or the lesson is rewritten/decayed on evidence |

Rule of thumb: **the emit goes next to the evidence, not next to the
claim.** T4's evidence is the brief the worker actually loaded; T6's
evidence is the judge's verdict. If you can't point at the evidence,
the stage didn't happen.

## The T6 judge-seat guard (F-2 contract — NOT in this branch yet)

T6 is the only stage with an identity gate, because self-verification
is not verification (the Inviolable). The guard is
`assert_independent_judge(doer_seat, scorer_seat, judge_seat)` in
`tools/lesson_verification.py`, implemented on branch
`naya5/eta-w146-learnclock-f2` (commit `1445cafd2d64...`). At the F-3
head this branch is built on, the guard does **not** exist — this
section documents the contract to wire against, not code present here.

- **Three seats, three origins.** `doer_seat` ← responses JSON
  `subject_seat` (who produced the responses). `scorer_seat` ← battery
  JSON `scorer_seat` (who authored the battery; set via
  `scaffold --scorer-seat`, defaults `""`). `judge_seat` ← verify CLI
  flag `--judge-seat`.
- **The rule.** All three must be non-empty strings (whitespace
  stripped; blank or non-string counts as missing), and
  `judge_seat != doer_seat` AND `judge_seat != scorer_seat`.
  Deliberately, `doer != scorer` is NOT asserted (battery
  self-authorship is a separate concern).
- **Failure is loud.** Missing identity →
  `SEAT_MISSING: <which> is required for T6 — no judge seat ⇒ no T6`.
  Collision →
  `SEAT_INDEPENDENCE_FAIL: judge_seat '<judge>' must differ from
  doer_seat '<doer>' and scorer_seat '<scorer>' — self-verification is
  not verification (Inviolable); no T6 emit.` Both raise
  `StructureError`, which the CLI maps to **exit 2**.
- **Gate placement.** In `cmd_verify`, `assert_independent_judge(...)`
  runs immediately before `cmd_score(args)` — after novelty + registry
  checks. A failing response + ineligible judge exits 2 with NO report
  file: scoring never runs. `cmd_score` asserts NOTHING
  (diagnostic-only); a score with no seat fields exits 0.
- **Two things the guard never confuses.**
  `--judge module:function` is the **scoring callable**, never a seat —
  a custom judge callable + `--judge-seat` coexist fine. `subject`
  (default `"unspecified"`) is **display-only**: the gate reads
  `subject_seat`, never `subject` — a display name equal to the judge
  seat passes, a `subject_seat` equal to the judge seat fails.
- **No T6 emit without a passing guard.** When the guard fails, there
  is no T6 — not a T6 with an asterisk. Fix the seats, re-run verify,
  emit T6 only on exit 0 with a passing response set.

## Concrete example (hypothetical lesson `LC-DEMO-001`)

A worker's push fails: the git-database push script wrote through a
symlink and clobbered a system binary.

- `emit("LC-DEMO-001", 0)` — T0, the moment the failure is observed
  (push died, python broken team-wide).
- `emit("LC-DEMO-001", 1)` — T1, the sign-out's failure+fix pair is
  filed ("ls -la before redirecting into any path").
- `emit("LC-DEMO-001", 2)` — T2, triage verdicts PROMOTE (recurrence
  risk: every worker pushes).
- `emit("LC-DEMO-001", 3)` — T3, the distilled note names its
  enforcement: "spawn briefs carry the no-system-paths rule; violation
  = whole-team outage."
- `emit("LC-DEMO-001", 4)` — T4, the next wave's spawn briefs actually
  contain the rule (check the brief text, not the note file).
- `emit("LC-DEMO-001", 5)` — T5, a worker's sign-out shows she checked
  `ls -la` before a redirect and says the lesson is why.
- `emit("LC-DEMO-001", 6)` — T6, a cold successor given the same push
  task checks paths first while a control (no lesson) does not —
  judged by a different seat, through the T6 guard above.
  `latency("LC-DEMO-001")` now reads the learning latency;
  `meets_target("LC-DEMO-001")` says whether it beat 60 minutes.
- `emit("LC-DEMO-001", 7)` — T7, the dispatcher brief template carries
  the rule permanently, or later evidence rewrites it.

```python
from tools.learning.learn_clock.learn_clock import (
    emit, latency, meets_target, status)

emit("LC-DEMO-001", 0)          # T0 — the failure is observed
# ... capture, triage, distill ...
emit("LC-DEMO-001", 3)          # T3 — principle + enforcement filed
# ... injection, application ...
emit("LC-DEMO-001", 6)          # T6 — cold successor verified (guard passed)
print(latency("LC-DEMO-001"))   # minutes, T6 − T0
print(meets_target("LC-DEMO-001"))  # True only if ≤ 60 and T6 exists
print(status("LC-DEMO-001"))    # hit vs missing stages
```

**Do not run the snippet above as-is** — it emits to the real repo
log. Rehearse with `LearnClock(tmp_path / "lc.jsonl")` or the hook's
test seams. The snippet shows the call shape, not a demo to execute.

## Retroactive bootstrap (the spec's step 1)

For the last real lessons, reconstruct from evidence with explicit
timestamps — oldest first, in order:

```python
emit("LC-TMPFS-001", 0, ts="2026-10-12T14:02:00+00:00")
emit("LC-TMPFS-001", 1, ts="2026-10-12T14:20:00+00:00")
# ... through T6 as the evidence supports
```

Or via the hook CLI: `learn_hook.py t0 --title ... --evidence ... --ts
"2026-10-12T14:02:00+00:00"`, then `t1..t6` with their own `--ts`.

Expect hours, not minutes — that's the honest baseline. The clock's
job is to make the number visible, then drive it down. T6 or it didn't
happen.

**F-3 note:** on retroactive `--ts`, the hook meta log's `ts` is the
EVENT time (== the clock row's `ts`), and `written_ts` records the
append time. Before F-3, meta rows carried mint-time. When reading old
meta rows, trust the clock JSONL for event times.

## What NOT to wire

- **No bulk backfill.** Emits stamped in bulk at the end manufacture
  history. One stage, at its moment, with its evidence.
- **No T6 without the guard.** A T6 emit whose verify run skipped the
  guard (or ran on the pre-guard code) is not a T6. Re-verify through
  `cmd_verify` with `--judge-seat` set, then emit.
- **No T4 from a file.** A principle sitting in a file is not
  injected. T4 needs the principle inside a worker's live thinking
  context — the brief text, the broadcast — with the brief as evidence.
- **No emit on the real log for demos, tests, or rehearsals.** Tmp
  paths and test seams exist for exactly this. The real log is the
  permanent record.
- **No scratch paths.** The scratch instrument home
  (`~/workspace/_scratch/learn-clock/`) and its `from learn_clock
  import ...` form are superseded. Repo imports, repo log paths,
  always.
