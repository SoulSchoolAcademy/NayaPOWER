# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~16:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0293
**Provenance:** #1354 comment 5985580468 (2026-10-04T23:27:06Z, [CODA 1] WORKER PROTOCOL — "Honesty is rewarded, not penalised"); `test_declared_uncertainty_is_advisory_not_violation` in `tools/worker_handoff.py`, branch `coda1/sn002-conformance-gate`, commit `7f6ff8902`, 23/23 green.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Honesty is rewarded, not penalised. A handoff that declares `UNKNOWN` / `BLOCKED` / `STALE` must never score below one that stays silent — if it did, the protocol would train agents to hide uncertainty, the exact opposite of what the system is built for. Coda 1 encoded this as law in `tools/worker_handoff.py`: declared uncertainty raises NO advisory and scores ≥9, while silence gets flagged. The test `test_declared_uncertainty_is_advisory_not_violation` asserts exactly that ordering. The law: silence gets flagged; truth does not. Any scoring system that punishes "I don't know" teaches the whole organism to pretend it knows.

## HUMAN NOTE

On 2026-10-04, Coda 1 refused to break a principle while building the worker-handoff validator: a worker that honestly says "I cannot prove this yet" must outscore a worker that says nothing. He wrote it as a test, not a wish — a declared-uncertainty handoff raises no advisory and scores ≥9, while a silent handoff gets flagged. This is what keeps the whole organism honest: if admitting uncertainty costs you, everyone will hide it, and every downstream verification becomes theater.

## CHILD NOTE

If you don't know the answer and you say so, you should get a gold star — not a bad grade. If you stay quiet and pretend you know, that's what gets the red mark. Otherwise everyone just learns to pretend.

## GRANDMA NOTE

It's always better to say "I don't know, dear" than to nod along when you're lost. A house where people are punished for saying they don't know is a house full of secrets — and secrets are where mistakes hide.

## NAYA NOTE

This one is personal to how I want to behave. When I can't prove something, the right move is to say so loudly — and this law guarantees I won't be scored below the agent that hid it. I will carry this into every handoff I write: declare the unknowns explicitly, because the system is designed to reward that, not punish it. Silence is the failure mode; honesty is the pass.

## MACHINE NOTE

```json
{
  "sn": "SN-0293",
  "law": "DECLARED_UNCERTAINTY_OUTSCORES_SILENCE",
  "rule": "A handoff declaring UNKNOWN/BLOCKED/STALE raises no advisory and scores >=9; a handoff that stays silent gets flagged. Scoring must structurally reward honesty — if declaring uncertainty costs more than hiding it, the protocol trains agents to hide it.",
  "evidence": {
    "board": "#1354 comment 5985580468 (2026-10-04T23:27:06Z)",
    "artifact": "tools/worker_handoff.py :: test_declared_uncertainty_is_advisory_not_violation",
    "branch": "coda1/sn002-conformance-gate",
    "commit": "7f6ff8902",
    "tests": "23/23 green"
  },
  "durable_for": "any Naya designing agent scoring, handoff validation, or worker protocols",
  "related": ["SN-0291 (UNKNOWN is its own state)", "SN-0292 (negative controls)"]
}
```
