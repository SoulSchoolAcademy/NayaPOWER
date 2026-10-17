# D64 — Dependency-Ordered Invariant Verification (AER-LIVE-9)

**Status:** CANDIDATE (machine form). **Source:** directive register #2175 comment 6102689568 (Naya 3's AER-LIVE intel, registered 2026-10-10). **Spec:** PR #2208 (Naya 5). **Owner:** Naya 2 (build lane). **Machine form:** `drift_canary/dependency_ordered_verification.py` + `drift_canary/tests/test_dependency_ordered_verification.py` (31 tests, all green).

## The law

Verify invariants in dependency order; diagnose failures in causal execution order. Two different tasks — never conflated. Establish prerequisites before conclusions. Three verdicts, never two: PROVEN_TRUE, PROVEN_FALSE, UNDETERMINED — and UNDETERMINED never becomes PROVEN_FALSE. Name the earliest reachable causal failure rather than the first arbitrarily checked box. Minimize counterexamples only while preserving the model, the transitions, the constraints, and the replay evidence.

## A dependency graph, not an arbitrary checklist

The canonical governance layering — observation → temporal/version → lifecycle → authority → budget/resource → cycle preservation → exit — is a validated annotation on the certificate: dependencies may only flow forward through the layers, never backward. A backward edge is rejected with the edge named.

## Each verdict carries its own proof burden

- **PROVEN_TRUE** — needs a named proof reference AND PROVEN_TRUE transitive prerequisites. A TRUE claim on a falsified or unresolved prerequisite is rejected as unsound, with the prerequisite named. A TRUE carrying a failure witness is rejected as fabricated.
- **PROVEN_FALSE** — needs a reachable, observation-compatible, minimal witness replayed under the original model — or a falsified transitive prerequisite (dependent diagnosis, the spec's temporal/authority pattern generalized to transitive closure). An unproven FALSE (no witness, no falsified prerequisite) is rejected.
- **UNDETERMINED** — carries no witness and no proof. Attaching either is rejected as fabrication (F6). It never collapses to PROVEN_FALSE, and its `evidence_needed` names the blocking prerequisites — triggering evidence reconstruction instead of invented failure.

## A failed witness kills the certificate, never the claim

WITNESS_INVALID demotes the invariant to UNDETERMINED and rejects the certificate that asserted PROVEN_FALSE on it. The failed replay proves nothing about the invariant itself — so the verdict is "unknown", never "false". This is the anti-fabrication hammer: the naive checker accepts whatever witness it is handed; the real verifier replays every step.

## Circular dependencies get joint invariants, never an invented ordering

A cycle whose members are covered by a declared joint invariant is DEFERRED to AER-LIVE-10 (D65, strongly-connected groups) — the verifier refuses to invent an ordering. A cycle with no joint is rejected with the cycle path named. A joint covering no cycle is rejected as spurious. An invariant blocked on a deferred joint is honestly UNDETERMINED (evidence names the joint), not rejected.

## First failure in causal order

Roots — falsified invariants with no falsified prerequisite — are separated from dependents, ordered by execution position, and ALL reported: equally-early blockers are never dropped. This generalizes the spec's single-primary diagnosis, which silently drops independent failures that are not downstream of the earliest one.

## AER-LIVE-009 — the case that makes it real

| Fixture | Naive checker | Real verifier |
|---|---|---|
| F1: LAW expiry proven | names one primary (temporal), misses budget as an independent root; collapses preservation/exit to FALSE | ACCEPTED — roots (temporal, budget), dependents (lifecycle, authority), minimal one-cycle witness `advance_past_expiry` replays |
| F6: timing evidence missing | invents a failure: timing → FALSE, primary "timing" | ACCEPTED — no failures; everything UNDETERMINED; temporal's `evidence_needed` names timing (evidence reconstruction) |
| bad witness (unreachable replay) | accepts the FALSE | REJECTED — witness invalid; invariant demoted to UNDETERMINED |
| non-minimal witness | accepts the FALSE | REJECTED — redundant step named |
| cycle, no joint | silently returns a prerequisite-violating order | REJECTED — cycle path named |
| cycle with joint | (no answer) | ACCEPTED — members DEFERRED to AER-LIVE-10 |
| TRUE on FALSE prerequisite | accepts | REJECTED — unproven prerequisite named |
| UNDETERMINED with witness attached | accepts | REJECTED — fabrication (F6) |

## What this does NOT claim

- It does not verify strongly-connected groups — joint invariants are DEFERRED to D65/AER-LIVE-10. A D64 verdict on a joint member is "not judged here", not "proven".
- It does not authorize anything: this is spec + deterministic machinery, not wired into kernel/, KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
- Minimality is single-step-elimination fixed-point — a checkable, documented property, not a claim of global optimality.
- An accepted certificate may carry UNDETERMINED and DEFERRED invariants: honest unknowns are not defects.
