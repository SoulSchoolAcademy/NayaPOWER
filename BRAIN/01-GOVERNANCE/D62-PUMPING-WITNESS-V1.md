# D62 — Minimal, Independently Verified Unbounded-Cycle Witnesses (AER-LIVE-7)

**Status:** CANDIDATE (machine form). **Source:** directive register #2175 comment 6102470813 (Naya 3's AER-LIVE intel, registered 2026-10-10). **Owner:** Naya 2 (build lane). **Machine form:** `drift_canary/pumping_witness.py` + `drift_canary/tests/test_pumping_witness.py`.

## The law

Assert an unbounded debt upper bound **only** from a minimized entry–cycle–exit certificate: an independently reachable entry, a positively debt-producing and arbitrarily repeatable cycle, and a valid exit after every finite repetition. **A short cycle is not proof of unboundedness.**

## Each part carries its own proof burden

- **Entry — independently reachable.** Replayed from the named verified boundary, never trusted. A mandatory reset inside the entry path means the entry is not reachable.
- **Cycle — debt-producing AND arbitrarily repeatable.** Every traversal must strictly raise the peak (gain > 0) **and** repeat without exhausting anything: budgets, tokens, revisions, termination. The dangerous false witness is the cycle that can repeat only twice — a self-loop on the scheduler state that quietly consumes a finite recovery token each traversal. The verifier finds the **minimal counterexample**: the first repetition that cannot complete (repetition 3 for the hidden two-token fixture).
- **Exit — valid after every finite repetition.** Replayed at sampled repetition counts (0…1000), always terminating at finite final debt. An exit that needs a resource the cycle exhausts — or that is never supplied — is unreachable.
- **Full-state closure or it doesn't count.** The cycle is modeled as a closed labeled transition system: same scheduler state, fixed debt delta, fixed per-traversal cost.

## Minimization preserves every constraint the proof depends on

Only minimized certificates are accepted — every cycle step debt-producing or resource-constraining (a zero-debt step carrying resource costs is load-bearing for repeatability and is kept by the minimizer), every entry step load-bearing, every resource claim consumed somewhere. `minimize_certificate` produces the minimal form; a non-minimal certificate is **refused with the redundant part named**, never silently repaired. Minimization never drops a defect: a mandatory-reset step is rejected as a defect, not repaired away.

## The independent verifier

`verify_pumping_witness` recomputes everything: minimization fixed-point, entry replay from the boundary, cycle gain, resource-exhaustion bound, reset scan, exit replays. `independent_verify` is the cold verifier: it reconstructs the certificate from serialized bytes alone and re-runs every check — the valid AER-LIVE-007 witness keeps its unbounded peak and finite final debt, reproducible from the certificate alone. Malformed bytes fail closed.

## The quantifiers stay separate

An unbounded peak (**for every bound, some history exceeds it**) is not a proven violation (**every history breaches it**). The verdict answers **UNRESOLVED** on the breach question even when the peak is proven unbounded — the witness can coexist with an undetermined verdict. `upgrade_to_breach` is the mechanical guard: it always raises `StarvationAccusationError`. **A pumping witness is never a starvation accusation.**

## AER-LIVE-007 — the case that makes it real

| Fixture | Naive checker (cycle-shape only) | Real verifier |
|---|---|---|
| valid | unbounded | ACCEPTED — peak proven, final debt finite, breach UNRESOLVED |
| two_token_defect | **unbounded (the bug)** | REJECTED — minimal counterexample at repetition 3 |
| mandatory_reset_defect | unbounded | REJECTED — reset inside the cycle |
| unreachable_exit_defect | unbounded | REJECTED — exit not reachable |

The naive checker's wrong answer on the two-token fixture is exactly the defect class D62 exists to catch: a self-loop that declares unboundedness while quietly consuming a finite resource.

## Composition

- **From D61:** D61's unbounded-debt engine exhibits a constructive U*S witness; D62 is the general certificate + verifier any such witness must survive. D61's module is not on main yet — shared verdict strings are PROVEN_UNBOUNDED / UNRESOLVED / BREACH / NO_BREACH (WITNESS_REJECTED is D62's own); no import coupling.
- **To D63/D64:** D63 (full-state invariants for repeatable cycle proofs) and D64 (dependency-ordered invariant verification) build on the certificate the D62 verifier accepts.
- **Witnesses are hypotheses:** every constructed history is defensible *within the stated model assumptions* — a hypothesis for bound computation, never an asserted fact, never an accusation.

## What this does NOT claim

- Not a verdict on whether starvation actually occurred (that needs real histories, not witnesses).
- Not physical realizability: the model proves possibility under stated assumptions, kept distinct from actual violation.
- Not the entry-boundary authority itself (the boundary is named and replayed from, not established here).
- Not wired into kernel/, KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
- No constitutional ratification is claimed. No production operation performed.
