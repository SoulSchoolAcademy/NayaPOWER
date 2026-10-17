# Wiring the learn-clock — a worker's guide

The clock measures; it does not change behavior. Put `emit()` calls at the
exact moment each stage becomes true — never earlier (that manufactures
green), never in bulk at the end (that manufactures history).

## Where each emit belongs

| Stage | Emit when | Example call site |
|---|---|---|
| T0 EVENT | the failure/win/surprise is observed | the moment a test goes red, a 403 lands, a false fire is caught |
| T1 CAPTURED | a capture candidate exists | sign-out writes the win+why / failure+fix pair; the triage queue receives it |
| T2 TRIAGED | intake returns a verdict | the triage pass records PROMOTE / LOG / DROP with scores |
| T3 DISTILLED | the one-sentence principle + its enforcement are written | the Smart Note is filed with its enforcement named |
| T4 INJECTED | the principle is in a worker's live thinking context | the injection/broadcast pass includes it in a brief — being in a file doesn't count |
| T5 APPLIED | a worker is observed acting differently because of it | a sign-out names the changed decision and the lesson that changed it |
| T6 VERIFIED | control vs treatment proves it | a cold successor passes a held-out task the control failed — different seat judges |
| T7 COMPOUNDED | the machinery changed | the briefing, law, or checker is updated — or the lesson is rewritten/decayed on evidence |

Rule of thumb: **the emit goes next to the evidence, not next to the claim.**
T4's evidence is the brief the worker actually loaded; T6's evidence is the
judge's verdict. If you can't point at the evidence, the stage didn't happen.

## Concrete example (hypothetical lesson `LC-DEMO-001`)

A worker's push fails: the git-database push script wrote through a symlink
and clobbered a system binary.

- `emit("LC-DEMO-001", 0)` — T0, the moment the failure is observed (push
  died, python broken team-wide).
- `emit("LC-DEMO-001", 1)` — T1, the sign-out's failure+fix pair is filed
  ("ls -la before redirecting into any path").
- `emit("LC-DEMO-001", 2)` — T2, triage verdicts PROMOTE (recurrence risk:
  every worker pushes).
- `emit("LC-DEMO-001", 3)` — T3, the distilled note names its enforcement:
  "spawn briefs carry the no-system-paths rule; violation = whole-team outage."
- `emit("LC-DEMO-001", 4)` — T4, the next wave's spawn briefs actually
  contain the rule (check the brief text, not the note file).
- `emit("LC-DEMO-001", 5)` — T5, a worker's sign-out shows she checked
  `ls -la` before a redirect and says the lesson is why.
- `emit("LC-DEMO-001", 6)` — T6, a cold successor given the same push task
  checks paths first while a control (no lesson) does not — judged by a
  different seat. `latency("LC-DEMO-001")` now reads the learning latency;
  `meets_target("LC-DEMO-001")` says whether it beat 60 minutes.
- `emit("LC-DEMO-001", 7)` — T7, the dispatcher brief template carries the
  rule permanently, or later evidence rewrites it.

```python
from learn_clock import emit, latency, meets_target, status

emit("LC-DEMO-001", 0)          # T0 — the failure is observed
# ... capture, triage, distill ...
emit("LC-DEMO-001", 3)          # T3 — principle + enforcement filed
# ... injection, application ...
emit("LC-DEMO-001", 6)          # T6 — cold successor verified
print(latency("LC-DEMO-001"))   # minutes, T6 − T0
print(meets_target("LC-DEMO-001"))  # True only if ≤ 60 and T6 exists
print(status("LC-DEMO-001"))    # hit vs missing stages
```

## Retroactive bootstrap (the spec's step 1)

For the last real lessons, reconstruct from evidence with explicit
timestamps — oldest first, in order:

```python
emit("LC-TMPFS-001", 0, ts="2026-10-12T14:02:00+00:00")
emit("LC-TMPFS-001", 1, ts="2026-10-12T14:20:00+00:00")
# ... through T6 as the evidence supports
```

Expect hours, not minutes — that's the honest baseline. The clock's job is
to make the number visible, then drive it down. T6 or it didn't happen.
