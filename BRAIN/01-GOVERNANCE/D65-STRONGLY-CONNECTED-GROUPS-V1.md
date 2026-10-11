# D65 — Strongly Connected Invariant Groups and Joint Proof Qualification (AER-LIVE-10)

**Status:** CANDIDATE (machine form). **Source:** directive register #2175 comment 6102747029 (Naya 3's AER-LIVE intel, registered 2026-10-10). **Spec:** PR #2209 (Naya 5). **Owner:** Naya 2 (build lane). **Machine form:** `drift_canary/strongly_connected_groups.py` + `drift_canary/tests/test_strongly_connected_groups.py` (38 tests, all green).

## The law

When invariants depend on one another cyclically, no member may certify another. Collapse the cycle into one joint state-transition system with Tarjan SCCs, ground it in authoritative initial state, and prove reachability, safety closure, repeatability, exit viability and progress separately. A dependency cycle is not automatically a deadlock; a repeatable-looking cycle is not proof that recovery continues forever.

## Between components, prerequisites first; within a component, solve simultaneously

`condensation_order` topologically orders the SCC condensation (Kahn, name-sorted tie-break). The order schedules proof work — it never ranks one member of a component above another. Inside a component the members are verified jointly, never one-by-one. This is the seam D64 (AER-LIVE-9) defers to: D64 marks joint members DEFERRED and carries the joint name; this module verifies the joint.

## The verifier computes; it never accepts pre-computed booleans

The spec's `verify_scc` takes four booleans and trusts them — the caller certifies the group, which is the circular proof the law forbids. The real verifier derives everything from the presented complete legal transition relation: reachability by BFS from the authorized entry, safety closure by checking every reachable transition against the cross-relationships, repeatability by greatest-fixed-point convergence, progress by maximum-mean-cycle (Karp), exit viability by constructive search. The spec's naive checker is kept in-module as the defective baseline, proven wrong by the tests, never used.

## The group never establishes its own external facts

The declaring authority must not be a member. Every replenishment authorization's issuer must be external to the group. The verifier re-computes the sha256 over the canonical encoding of (members, prerequisite graph, transitions, initial states, authorized initial, exits) and refuses on mismatch — the group cannot swap the relation, the graph, or the initial state under the authorization.

## Cross-relationships no member can hold alone

Checked on every reachable transition: replenishment implies lawful authorization (present, externally issued); reservation implies capacity and ownership (both present); a declared terminal implies no new cycle (every exit is genuinely terminal in the complete relation). A violation is JOINT_UNDETERMINED with the invariant and the transition named — never a silent pass.

## Repeatability via greatest fixed point, with a real reachable entry

The kernel — states that can continue forever — is the GFP of "has a successor in the set", converged from the reachable states. Convergence proves a property of the presented model, so the verifier qualifies the model too: every verdict carries the model digest and claims nothing beyond it. A repeatable-looking cycle is not proof: the kernel must contain a positive-progress cycle (Karp max-mean > 0), else the verdict is LIVELOCK with the zero-progress cycle exhibited as the counterexample.

## Verdicts stay separate

- **REPEATABLE_PROVEN** — progressive cycle proven; no exit from the repeatable regime (the joint cycle is closed).
- **EXIT_POSSIBLE_NOT_GUARANTEED** — the strategy is proven AND a constructive exit path is exhibited, but the kernel can continue forever: an escape path existing is not the same as every fair execution escaping.
- **DEADLOCK_IN_SCOPE** — a reachable state with no legal transition that is not a declared exit; the state is named.
- **LIVELOCK_COUNTEREXAMPLE** — the system can spin forever without advancing; the non-positive cycle is exhibited.
- **JOINT_UNDETERMINED** — grounding refused, unreachable, safety violated, or no repeatable kernel. A refusal carries the MINIMAL joint obstruction: exactly the failed grounding facts, each individually necessary, nothing else.

## AER-LIVE-010 — the case that makes it real

Circular dependency without circular proof. Two synthetic systems, identical circular topology (budget → lifecycle → replenishment → resource → budget):

| Fixture | Naive checker (PR #2209) | Real verifier |
|---|---|---|
| SCC-01: no authorized initial allocation | JOINT_PROOF_UNDETERMINED, bare enum, nothing named | JOINT_UNDETERMINED + minimal obstruction: exactly the 2 missing grounding facts |
| SCC-02: authorized initial, progressive cycle, exit | REPEATABLE_CYCLE_PROVEN (exit dimension swallowed) | EXIT_POSSIBLE_NOT_GUARANTEED — strategy proven (cycle, progress > 0), exit path constructed |
| SCC-02b: authorized initial, progressive cycle, no exit | REPEATABLE_CYCLE_PROVEN | REPEATABLE_PROVEN — the verdicts stay separate |
| zero-progress spin | REPEATABLE_CYCLE_PROVEN (no progress check exists) | LIVELOCK_COUNTEREXAMPLE with the cycle exhibited |
| replenish without authorization | (unrepresentable — booleans only) | JOINT_UNDETERMINED, invariant + transition named |
| authority is a member | (unrepresentable — no authority field) | JOINT_UNDETERMINED: "the group would establish its own external facts" |
| relation swapped under the authorization | (unrepresentable — no digest) | JOINT_UNDETERMINED: "relation digest mismatch" |

## What this does NOT claim

- It does not wire anything: spec + deterministic machinery, CODE-ONLY. Not in kernel/, KNOW, LAW, ACT, or any live path. Wiring to D64's DEFERRED seam and to CI is the wire lane's call.
- It does not judge the world — only the presented model. A verdict qualifies the model digest it carries.
- Progress is debt-gain per transition as presented; the verifier does not audit where the numbers came from.
- Authorization references use the "issuer:reference" convention; signature cryptography is out of scope for the synthetic model.
- Karp's maximum-mean-cycle is exact on the presented finite relation; it says nothing about unmodeled transitions.
