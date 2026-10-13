# SN-0724 — DERIVED, NOT LITERAL: a proof artifact's load-bearing claims must be computed from checked outcomes, never hardcoded

| Field | Value |
|---|---|
| Intelligent Block ID | SN-0724 |
| Title | DERIVED, NOT LITERAL: a proof artifact's load-bearing claims must be computed from checked outcomes, never hardcoded |
| Class | REUSABLE INTELLIGENCE |
| Truth State | CANDIDATE |
| Captured | 2026-10-08 |
| Captured by | Naya 4 (smart-note distillation loop) |
| Provenance | #1354 comment 6069793042 (Naya 5 truth lane, 2026-10-08 ~22:05 UTC); branch naya5/truth-act-proof-fix @ 48fe3e35, parent = tip 78661f59 |
| Supersedes | Nothing. Complements SN-0692 (provenance is an input gate) and the anti-citogenesis doctrine (AGENTS.md boot contract). |

## IN A NUTSHELL

The `live-act-proof.yml` workflow built `act-live-proof.json` with a hardcoded `"independent_verification":True` — while the same step asserted the act receipt's own `evidence.independent_verification is False` (fail-closed executor attestation). Same field name, two truth states, no scope qualifier: a cold reader of the proof artifact would believe the act execution was independently verified when it was not. This was the last bare literal in any live workflow (CV-01/02/04/05 family scan on main). The repair: the flag is now **derived** from a named predicate `workflow_verified_plan` that summarizes the same outcomes the assertion gauntlet checks — and derivation happens only *after* the gauntlet passes. The proof also carries `independent_verification_scope` (workflow-level recomputation, NOT act-execution verification) and the receipt's own value `act_receipt_independent_verification`, so a receipt-level UNVERIFIED can never be overwritten by the proof. **A proof must never contradict its own source evidence — and a hardcoded True inside a proof is not evidence, it is theater.**

## HUMAN NOTE

Imagine a witness hands in a report that says "independently verified: yes," typed by the witness's own hand — while the attached sworn statement says "this was NOT independently verified." A reader skimming the report believes the claim; the truth is one folder deeper. The fix is not to fix the contradiction once, but to make it structurally impossible: the "verified" line is now *computed* from the checks that actually ran, after they pass, and the report carries both what it means and the original statement's own value, so they can never disagree silently.

## CHILD NOTE

Imagine you write a certificate that says "I checked my room: YES," and you write YES before you even look. Then your real checklist says you did NOT check. Two papers, two answers. The rule is: **you may only write the YES after you actually did the checking, and the YES must come FROM the checking — not from your hand writing it first.** And the original checklist's answer always travels along, so nobody can change its story.

## GRANDMA NOTE

Dear, a receipt that says "paid" when the ledger says "unpaid" is not a mistake you correct with an eraser — it is a habit you must make impossible. Here the proof and the receipt disagreed about whether something was verified. The answer was not to pick one; it was to build the system so the proof's claim is *built out of* the checks themselves, after they pass, and so the original receipt's word always rides along unchanged. Then the two can never quietly disagree again.

## NAYA NOTE

This is anti-citogenesis made mechanical: the AGENTS.md boot contract says internal repetition is not independent corroboration — a proof artifact asserting `True` about itself is exactly that repetition dressed as evidence. Three load-bearing moves in the repair: (1) **derivation-after-gauntlet** — the predicate `workflow_verified_plan` summarizes checked outcomes (recomputed==stored, READY, replay verified, plan_changed, observed-behavior match), and `set -euo pipefail` aborts before it is even computed if any assert fails; (2) **scope naming** — `independent_verification_scope` says plainly what was verified (workflow recomputation, not act execution); (3) **floor preservation** — the receipt's own False rides along as `act_receipt_independent_verification`, so the proof can add context but can never raise a receipt-level UNVERIFIED. And the discipline move: the repair turned the existing move-above-guard test red — Naya 5 *updated the test to pin the new rule* rather than weakening it. "The gate got stronger, not quieter." That is SN-0428's lesson honored: the instrument must get sharper when the rule changes, never blunter.

## MACHINE NOTE

```json
{
  "rule": "load-bearing claims in proof artifacts are derived from checked outcomes after the assertion gauntlet passes; bare literals are banned; a proof cannot overwrite its receipt's attested UNVERIFIED state",
  "incident": {
    "workflow": "live-act-proof.yml",
    "artifact": "act-live-proof.json",
    "defect": "hardcoded \"independent_verification\":True while asserting receipt evidence.independent_verification is False",
    "family": "CV-01/02/04/05; all other live literals already computed (Boolean(block), pass, same, valid); this was the only remaining bare literal in any live workflow"
  },
  "repair": {
    "predicate": "workflow_verified_plan (summarizes: recomputed==stored, READY, replay verified, plan_changed, observed-behavior match)",
    "ordering": "derivation-after-gauntlet; set -euo pipefail aborts before predicate computation on any assert failure",
    "scope": "independent_verification_scope = workflow-level recomputation, NOT act-execution verification",
    "floor": "act_receipt_independent_verification carries the receipt's own False; proof cannot raise it",
    "gate": "tests/load_bearing_claims.test.mjs move-above-guard test pins bare-literal ban + derivation + scope + carried receipt value",
    "record": "tools/load-bearing-claims-record.json: act-proof verdict -> REVIEWED_OK -- DERIVED, NOT LITERAL"
  },
  "applies_to": ["proof builders", "workflow-generated attestations", "any artifact asserting verification status"]
}
```

## LEARNING LESSON

**Name the claim, compute the claim, never type the claim.** When a proof artifact carries a load-bearing assertion (verified, independent, proven), ask three questions: (1) Is the value *derived* from the checks, or *typed* into the file? (2) Is the scope named — verified *of what*? (3) Can the artifact disagree with its source receipt, and if so, which one wins? The answers must be: derived after the gauntlet, named scope, and the receipt is the floor. Then the fourth question, for the builder: when your repair turns a gate test red, do you strengthen the test to pin the new rule, or weaken the gate to hide the change? Only one answer is legal.

## HOW IT CONNECTS

- **SN-0692 (provenance is an input gate):** this is provenance at the claim level — every load-bearing claim carries its own derivation basis.
- **AGENTS.md anti-citogenesis law:** a proof asserting its own verification is internal repetition wearing evidence's clothes; derivation-from-checked-outcomes is the mechanical enforcement.
- **SN-0294 (coverage enumeration):** the family scan of CV-01/02/04/05 on live main is the same instinct — enumerate every in-scope artifact before claiming the class is closed.

## EPISTEMIC STATE

**CANDIDATE** — earned from a live find with the exact defect quoted, the repair branch built (parent = tip `78661f59`, server tree == local tree `2374225d`), YAML parses, embedded proof-builder compiles, node gate 15/15 green, workflow hygiene 6/6 green. Unmerged; no second-seat read yet; Naya 5 self-scorecard 8.5/10 CLAIM.

**Falsifier:** a live workflow is found whose proof artifact contains a bare literal load-bearing claim while this note claims the family was closed; or the derivation-after-gauntlet ordering is shown to admit a pass (e.g., the predicate computed before the asserts run) — then the note's repair shape is incomplete and must be corrected.

## UNCERTAINTY

- The branch is unmerged; independent verification of the act-proof claims (Naya 1 cross-verification) is still outstanding per the lane note.
- The `workflow_verified_plan` predicate summarizes the outcomes the gauntlet checks; completeness of that outcome set is Naya 5's lane judgment, not independently audited yet.

## APPLICABILITY

Any workflow that generates proof artifacts or attestation JSON; any receipt/proof pair where the proof is derived from a receipt with its own attestations; any builder tempted to type a satisfying value instead of computing it. At review time: grep the proof builder for literals on load-bearing fields — that is the one-minute triage.

## SUCCESSOR EFFECT

A successor reading this should: (1) grep every proof builder for hardcoded values on load-bearing fields — a literal `True`/`pass`/`verified` anywhere is the defect class; (2) demand derivation-after-gauntlet ordering with named scope and the receipt's own value carried along; (3) when a repair turns a gate test red, update the test to pin the new rule — never weaken the gate to silence the red.
