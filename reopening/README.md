# Reopening Protocol — SPEC

**Principle (Shawn, 2026-10-10):** "A resolution is the best supported interpretation at a particular time — not an eternal declaration of truth."

The temporal review lifecycle for interpretations. Extends the error-defense
spec (`naya5/error-defense-falsification`); does not duplicate it.

## The four objects

| Object | Mutability | Purpose |
|---|---|---|
| `SourceRecord` | immutable | What was actually said. Corrections link; never edit. |
| `InterpretationSet` | versioned | Plausible meanings + evidence. New meanings = new version. |
| `ResolutionReceipt` | immutable | Why THIS meaning won, at THIS time, under THIS policy. |
| `ApplicabilityAssessment` | reassessed | Can it guide THIS decision NOW? Judged under current policy. |

## The five states

`RESOLVED → CHALLENGED → REOPENED → REQUALIFIED | UNRESOLVED`

- **CHALLENGED** changes nothing by itself — eligibility is untouched until
  the reopen threshold is met.
- **REOPENED** applies risk-based containment only to materially dependent uses.
- **REQUALIFIED** issues a NEW receipt superseding the prior (history preserved).
- **UNRESOLVED** holds consequential use; the review stays open, nothing deleted.

Illegal transitions raise (`CHALLENGED → REQUALIFIED` is impossible by construction).

## The three decisions (separate questions)

1. **Admit?** — concrete, non-duplicate, evidenced basis? (`admit_challenge`)
2. **Contain?** — could continued reliance cause material harm? (`determine_containment`)
3. **Requalify?** — old meaning / new meaning / no single meaning? (`requalify`)

## The ten triggers

`triggers.REGISTRY` — each with required evidence shape and mandated response.
A challenge naming a trigger without its evidence is `INSUFFICIENT`.

## Policy versioning

P1 receipt stays valid as history. Current applicability is judged under the
current policy (`assess_applicability`). `retroactivity_rule` defaults to
`prospective`; retroactive effect only when the authoritative policy declares it.

## Idempotency

Challenge ids are content-derived (`derive_challenge_id`). Same challenge
twice = one incident (`ChallengeRegistry.register` → `DUPLICATE`).

## Descendant tracing

`trace_impact`: independently-supported descendants recalculate via their own
evidence; historical cites are preserved; only sole-basis material dependents
are restricted pending review.

## What this does NOT do

- Not wired into `kernel/` — spec + tests only. Wiring needs Shawn's word.
- Does not replace memory-record lifecycle (`memory_metabolism`) or the
  error-defense promotion gate — it governs the *temporal review* of
  *interpretations*, a layer neither covers.
- A challenge never grants permission to change production, delete evidence,
  or override LAW.
