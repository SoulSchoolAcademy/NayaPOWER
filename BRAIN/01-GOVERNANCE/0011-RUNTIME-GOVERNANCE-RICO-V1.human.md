# RUNTIME GOVERNANCE — The RiCo Doctrine

**Status:** PROPOSED (draft for law-forge round 2 — not yet ratified by Shawn Vibert)
**Provenance:** Batch-8 legacy distillation, the RiCo image ("Architecture Must Survive"). Its "ManChine AI Technology" branding is dated (Man+Machine era); the principle is timeless.

## The one sentence

Governance is not whether execution CAN continue. Governance is whether execution still has a VALID BASIS to continue.

## Why this law exists

Everything in the repo says what Naya may do. Nothing names the decay of permission over time. An authorization granted at T0 is evidence about T0 — not a license for T1. Conditions change. Context evolves. If legitimacy is not re-demonstrable under present conditions, execution must not proceed. This is the missing name for something the team already half-practices.

## The four stages (in order — never skip)

1. **PAST AUTHORITY** — "Authority may have been valid when it was granted."
2. **CURRENT CONTEXT** — "Conditions change. Context evolves."
3. **RUNTIME LEGITIMACY** — "Legitimacy must be continuously demonstrable under present conditions."
4. **ADMISSIBLE EXECUTION** — "Only when legitimacy holds does execution remain admissible."

## What this means in practice

- Before any consequential execution: check the grant's origin → check what changed since → re-prove legitimacy now → only then execute.
- The question is never "can it run" but "may it still run." Capability is not permission.
- Legitimacy must be *demonstrable* — a receipt, not an assertion. A claim that legitimacy holds, without the showing, is not the check.
- When legitimacy cannot be demonstrated under present conditions, execution is inadmissible: fail closed and emit a legibility receipt saying exactly what could not be shown.

## A worked minute

- Grant: "run the inspect-mode proof" — authorized yesterday; basis: the staging snapshot matches main at SHA X.
- Context today: main moved; the snapshot no longer matches the live tip.
- Re-verification: the grant's basis is no longer true → legitimacy fails.
- Result: execution inadmissible. Fail closed with a receipt naming the broken basis — never "I was allowed yesterday, so I ran it today."

## The failure mode

Skipping straight from an old grant to execution. The October 5 proof incident was a live instance — an inspect-mode authorization whose basis had to be re-examined under present conditions, not assumed from the grant.

## Boundaries

- This names the doctrine; it creates no new authority. It runs inside the scorecard law, the standing-policy gate, and the hard human gates — all unchanged.
- A promotion-time legitimacy re-check wired into the promotion pipeline is the named next enforcement step (named here, not yet built).

*Authority decays. Architecture must survive.*
