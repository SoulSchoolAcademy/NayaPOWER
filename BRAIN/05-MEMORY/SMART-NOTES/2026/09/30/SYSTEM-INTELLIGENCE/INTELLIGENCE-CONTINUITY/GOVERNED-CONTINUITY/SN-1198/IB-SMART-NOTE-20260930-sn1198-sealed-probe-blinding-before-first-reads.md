# A Sealed Acceptance Probe's Blinding Rule Must Fire Before Any First-Reads in the Brief — the Brief Must Not Contaminate Its Own Executor

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1198-sealed-probe-blinding-before-first-reads
**Smart Note:** SN-1198
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A sealed/blinded acceptance probe is worthless if the executor is contaminated before the blinding rule fires. On 2026-10-13, the t0568 sealed cold-retrieve acceptance probe was NOT executed: the brief's own "First reads" contaminated the executor seat before §7's assignment rule could fire — and the frozen driver was missing, the sealed corpus tip unreachable, and no blinded scorer existed. The seal was preserved by the HOLD, and the bytes are intact (MANIFEST 8/8 OK) — but a probe whose executor saw the material is no probe at all.

## HUMAN NOTE

Blinding is order-of-operations, not intention. The mechanism:

1. **The assignment rule fires first.** §7's assignment rule decides WHO the executor seat is and WHAT it may read — before any content enters the brief.
2. **Then the brief is constructed** so the executor's first reads exclude the sealed corpus.
3. **Preconditions are verified before dispatch:** frozen driver present, sealed corpus tip reachable, blinded scorer named. A probe missing any of these does not "run and adapt" — it HOLDS.

What happened at t0568: the brief's "First reads" section read the sealed material into the executor's context before §7's assignment rule fired. Contamination is irreversible once read — there is no unreading. Lane 9 broadcast the HOLD (owed from t0634), preserved the seal, and templated the repair (sealed-probe-blinding-checklist, CANDIDATE).

Rule: **blinding fires before first-reads; a brief that pre-reads contaminating material burns its own blinded executor.** The checklist is a dispatch gate, not documentation.

## CHILD NOTE

If you're doing a surprise quiz, you can't peek at the answers first. Decide who takes the quiz, and make sure they don't see the answers before they start. If anything goes wrong, stop — don't pretend the quiz still counts.

## GRANDMA NOTE

You can't fairly test someone if they've already seen the test. Set up the rules first, hand them the test second. If the rules can't be set up properly, you wait — you don't fake it.

## NAYA NOTE

Sealed acceptance probes are the cold-successor standard's load-bearing experiment: they measure whether intelligence actually retrieved and applied, versus reconstructed from contaminated context. The contamination boundary is absolute — an executor that has seen the material cannot produce an uncontaminated result, and no scorecard can recover that. The HOLD is the correct output of a broken blinding setup, not a failure to execute. Template the blinding checklist as a dispatch precondition: executor assigned → first-reads constrained → frozen driver → corpus reachability → blinded scorer → then and only then dispatch.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "rule": "blinding_rule_fires_before_first_reads",
  "dispatch_gate": [
    "executor_seat_assigned (blinding rule)",
    "first_reads_constrained_against_sealed_corpus",
    "frozen_driver_present",
    "sealed_corpus_tip_reachable",
    "blinded_scorer_named"
  ],
  "failure_mode": "brief_first_reads_contaminate_executor_before_assignment_rule_fires -> HOLD, seal preserved, probe NOT counted",
  "master_nodes": ["PROVE", "VERIFY", "LAW"]
}
~~~

## 🟡 WHAT IT MEANS

Experimental integrity is a gate, not a wish. When the gate can't be built, HOLD — a contaminated probe is worse than no probe, because it wears the costume of evidence.

## 🧾 PROOF / PROVENANCE

- Lane 9 (Naya Smith) t0640 HOLD broadcast, board #2175 comment 6148601855 (2026-10-13T15:04:50Z): "the t0568 sealed cold-retrieve acceptance probe was NOT executed — the brief's own 'First reads' contaminated the executor seat before §7's assignment rule could fire; frozen driver missing; sealed corpus tip unreachable; no blinded scorer. Seal bytes intact (MANIFEST 8/8 OK), seal preserved by the HOLD."
- Receipt: `hidden_files/twelve-lane-receipts/t0634-lane9.md`; repair template (CANDIDATE): `hidden_files/sealed-probe-blinding-checklist-t0640.md`

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Covers the t0568 sealed cold-retrieve probe specifically and blinded acceptance probes generally. The checklist template remains CANDIDATE — its dispatch-gate status is proposed, not yet ratified by Shawn.

## ➜ NEXT ACTION / SUCCESS CONDITION

The blinding checklist is wired as a dispatch precondition for future sealed probes; any probe whose executor was pre-contaminated is HOLDed and recorded, never scored.
