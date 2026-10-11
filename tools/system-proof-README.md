# UD-07 — System Proof Harness (`tools/system_proof.py`)

**Prove the whole system, not just its parts.** Green components can
assemble into a broken system. This harness runs end-to-end scenarios
through a multi-node assembly and refuses invalid global executions —
naming the seam where they broke.

## Run

```bash
python3 tools/system_proof.py          # fixture demo (5 scenarios)
python3 tools/test_system_proof.py     # full adversarial suite (42 checks)
```

## The five obligation families (D17)

Every scenario run is judged on all five, independently:

| Family | Asks |
|---|---|
| `component` | Does each node run without error? |
| `interface` | Does each seam's contract hold on the real output? |
| `interaction` | Do cross-node invariants hold (joint context, auth freshness, plan finality)? |
| `environment` | Does the run's environment match the claim? |
| `composite-sufficiency` | End-to-end outcome correct **with** all families green? |

Certificate ladder: `COMPONENT_QUALIFIED` → `INTEGRATION_QUALIFIED` →
`TRANSFER_QUALIFIED` → `PRODUCTION_PROVEN`. Anything red →
`COMPOSITE_FAIL`.

## Adversarial fixtures (one failure = FAIL)

| Fixture | What it proves |
|---|---|
| `healthy` | Healthy system passes; no seam named |
| `malformed-output` | Parts pass, seam breaks → composite FAIL, seam named |
| `stale-auth` | Authorization revoked between LAW and ACT → refused at `LAW->ACT` |
| `late-lesson` | Lesson after plan finalization → refused at `KNOW->ACT` (no retroactive mutation) |
| `joint-context-mismatch` | Pairwise handoffs green, joint execution invalid → refused at `JOINT-CONTEXT` |

## Versioned obligations (D18)

`ObligationRegistry`: obligations carry versions + lifecycle states
(PROPOSED→ACTIVE→DEPRECATED→SUPERSEDED→RETIRED→WITHDRAWN). Change
classification decides treatment: editorial keeps proof; stronger needs
new proof; split/merge/interface/environment need targeted requalification.
History is append-only — yesterday's green never certifies tomorrow's
untested system.

## Migration engine (D19)

Splits/merges migrate EVIDENCE, never PASS labels. Per-item mappings:
`ENTAILS` / `PARTIALLY_SUPPORTS` / `DOES_NOT_SUPPORT` / `UNDETERMINED`.
A black-box end-to-end success can never prove internal invariants it
never observed. Merges additionally demand interaction proof.

## Interaction discovery (D20/D21)

`discover_interactions(system)` enumerates multi-party paths as
first-class obligations with shared-context invariants. Each carries a
positive witness AND a counterexample — a one-sided interaction proof
proves nothing. Core invariant: a valid KNOW→LAW handoff plus a valid
LAW→ACT handoff does NOT establish a valid KNOW→LAW→ACT execution.

## What this does NOT claim

The harness judges the obligations it is given. It does not discover
real-world hazards on its own. A PASS certifies the tested scenarios
only — not untested environments, futures, or hazards outside the
given obligations.
