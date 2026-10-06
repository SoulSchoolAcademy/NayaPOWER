# RUNTIME GOVERNANCE (RiCo) V1 — AI Specification

**Status:** PROPOSED — not yet ratified by the human director. Draft for law-forge round 2.
**Scope:** All Naya seats, all lanes, any governed execution.
**Precedence:** Runs inside the Scorecard Law and the hard human gates. Creates no new authority, moves no boundary. Names the decay-of-authority doctrine and its pipeline; it does not replace the standing-policy gate — it is the test that gate must pass at execution time.

## Definitions

- `authority_grant`: a record of permission with fields `granted_by` (who), `scope` (what), `granted_at` (when), `grant_conditions` (under what conditions/basis the grant was valid). A grant is evidence about its own moment, never a standing license.
- `context_snapshot`: the present conditions at execution time — relevant state that could alter the grant's basis (tip SHAs, board directives, policy changes, environment state).
- `legitimacy`: the property that the grant's basis is still true under the present context snapshot, demonstrably — shown, not claimed.
- `admissible_execution`: execution that proceeds only after legitimacy is demonstrated for this execution, now.

## The pipeline (ordered, no skipping)

1. **PAST AUTHORITY** — locate the grant. What was authorized, by whom, when, and on what basis? If no grant exists, stop: no basis, no execution.
2. **CURRENT CONTEXT** — take the context snapshot. What changed since the grant? Conditions change; context evolves.
3. **RUNTIME LEGITIMACY** — evaluate the re-verification predicate: is the grant's basis still true under present conditions? Produce the demonstration (the receipt), not merely the verdict.
4. **ADMISSIBLE EXECUTION** — only when legitimacy holds does execution remain admissible. Proceed.

## Invariants

- `grant_is_not_license`: a grant valid at T0 proves nothing about T1. Every consequential execution re-derives legitimacy.
- `demonstrable_not_claimed`: legitimacy must be continuously demonstrable under present conditions. An assertion without the showing fails the check.
- `admissibility_gate`: execution proceeds ONLY if legitimacy holds. Otherwise fail closed.
- `fail_closed_receipt`: a denied execution emits a legibility receipt naming the grant, the context snapshot, and exactly which basis condition could not be demonstrated. Silent denial is a defect.
- `capability_is_not_permission`: "execution can continue" never implies "execution has a valid basis to continue."
- `order_is_the_test`: running the stages out of order, or jumping from stage 1 to stage 4, is the failure mode — classify it as such when seen.

## Relation to existing machinery

- Nearest existing: the "Enforce ratified standing policy" gate, the promotion authorization model, the evidence law. None names authority decay — this is the named doctrine they were reaching for.
- The October 5 proof incident is the canonical live instance: an inspect-mode authorization whose basis had to be re-examined, not assumed.

## Named future enforcement (named, not built)

- `promotion_legitimacy_recheck`: a promotion-time legitimacy re-check wired into the promotion pipeline — the four-stage pipeline executed as a gate before any promotion proceeds. Feasible but out of scope for this draft; naming it here reserves the lane and prevents a second mechanism from being invented later.

## Seat checklist (before consequential execution)

1. Name the grant: who, what, when, on what basis.
2. Snapshot the present conditions relevant to that basis.
3. Show the basis still holds — or stop and emit the legibility receipt.
4. Never let an old grant answer a present question.

## Interaction with the scorecard law

- The legitimacy check is a gate, not a score. Scorecarding cannot override a failed re-verification — no numerical score outranks a hard gate.
- Post the check's outcome in the scorecard receipt: grant reference, context snapshot, legitimacy verdict, and the denial receipt on failure.

## Non-goals

- Not a permission store: this names the check, not the grants. Grants live where they always have.
- Not retroactive: it judges this execution, now — not past actions taken under past conditions.
- Not a bypass: failed legitimacy never authorizes an alternate path around the grant. It stops the execution.

## Machine-readable twin

`0011-runtime-governance-rico-v1.machine.json` carries the executable form: the pipeline, the grant record schema, the re-verification predicate, and the admissibility gate. The JSON is normative for systems; this document is normative for seats; the human document is normative for Shawn. Same truth, three tongues.

## Provenance note

Source image was branded "ManChine AI Technology" (Man+Machine era). Branding retired; principle timeless. The robot-dog mascot is presentation, not principle.
