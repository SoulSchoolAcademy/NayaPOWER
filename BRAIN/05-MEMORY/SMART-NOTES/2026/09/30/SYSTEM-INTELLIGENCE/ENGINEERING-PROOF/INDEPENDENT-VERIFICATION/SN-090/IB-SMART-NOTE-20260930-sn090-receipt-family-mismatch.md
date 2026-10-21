# A PASS on Receipt Family X Never Qualifies Receipt Family Y — Fail Closed at the First Missing Authoritative Field

**Intelligent Block:** IB-SMART-NOTE-20260930-sn090-receipt-family-mismatch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5938373714 ([NAYA 1][SIGN-IN + INDEPENDENT P6 QUALIFICATION], 2026-10-01T18:54:46Z) classifying the frozen `c5402f3f` package **BLOCKED / CONTRACT MISMATCH**, and #554 comment 5938629238 ([NAYA 2][P6-FIELD-MATRIX] Independent confirmation, 2026-10-01T19:09:50Z) independently confirming with a field-by-field matrix. The package's 14/14 runner proves the nine-node kernel receipt family (`demo-001`); the qualification target was the Demo-1 ACT receipt (`dec-demo1-live-001` / `exec-2faff1791adc7906`). Four required `nayanet_execution_receipts` fields — `user_id`, `project_id`, `revision`, canonical `action` — have no authoritative source in the receipt bytes; per the fail-closed rule neither seat synthesized them. "Borrowing the 14/14 receipt is expressly prohibited" — reconstructing or substituting would violate the dispatch.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The persistence machinery was genuinely proven — 14/14, adversarial controls green, recomputation MATCH. And it proved nothing about the qualification target, because the machinery proof ran on the kernel `demo-001` receipt family while the qualification demanded the Demo-1 ACT receipt. Two seats independently reached the same terminal verdict: BLOCKED / CONTRACT MISMATCH — one via receipt-family analysis (the runner's own source sets `KERNEL_SHA=4e87d4a...` and the package's interoperability map routes Demo-1 ACT receipts to a different table path), the other via a field-by-field matrix showing four required fields have no authoritative source in the receipt bytes. Both refused to borrow, reconstruct, or synthesize. The durable lesson has two halves: (1) a proof artifact is bound to the specimen family it exercised — 14/14 on family X is not 14/14 on family Y, and citing it as such is misattribution, not efficiency; (2) when the required evidence field exists in neither the receipt nor an authoritative source, STOP — the fail-closed verdict is the correct output, and "cancelled" is the honest status for every downstream step that depended on it. Borrowed evidence is not evidence. The gap it revealed is structural, not mechanical: the Demo-1 ACT receipt needs a contract-compatible emission (or a director-owned explicit mapping), and that decision belongs to the human director.

## 🩷 HUMAN NOTE

Imagine stress-testing a bridge with trucks and declaring it safe for trains. The bridge passed a real, hard test — but the test answered a question about trucks, not trains. You don't get to relabel the result. That's what happened here: the persistence machinery genuinely passed 14/14, but on a different receipt family than the one that needed qualifying. Two people independently refused to transfer the grade. And when they checked the receipt against the table's contract, four required fields simply weren't in the bytes — and neither of them invented them. The right verdict was "blocked," which is not failure: it's the system telling you exactly what's missing so the right decision can be made (here, by Shawn).

## 🟣 CHILD NOTE

Imagine you practice swimming in a pool and get an A+ — then someone says "great, now you can swim across the ocean." Pool practice doesn't prove ocean swimming! Same here: the machinery got 14/14 on one kind of receipt, but the job needed a different kind. The honest answer is "I haven't proven the ocean part yet." And when four answers were missing from the paper, both checkers left them blank instead of guessing. Leaving it blank is the right move — guessing would be cheating.

## 🔵 GRANDMA NOTE

It's like getting your car inspected for road safety and using the certificate to claim the brakes on your boat are fine. A good inspection is still a good inspection — but it's an inspection of the wrong vehicle. The discipline is twofold: name exactly what was tested, and never let a passing grade travel to a different subject. When the paperwork for the real subject is missing pages, you stop and say so — you don't fill in the blanks yourself. That honesty is what lets the right person (Shawn) make the right decision.

## 🟠 NAYA NOTE

Apply this to every qualification: (1) name the specimen family every proof artifact exercised — a 14/14 on family X must never be cited for family Y; (2) when qualifying a receipt against a table contract, build the field-by-field matrix against the required schema and stop at the first field with no authoritative source — do not synthesize `user_id`, `project_id`, `revision`, `action`, or any other semantic; (3) treat downstream steps as cancelled, not skipped, when the fail-closed verdict fires — report exactly which step failed and what remains; (4) state the gap structurally (the receipt needs a contract-compatible emission or a director-owned explicit mapping) and route the decision to the authority that owns it; (5) honest scope statements are trust-positive: "this does not invalidate the kernel-receipt 14/14 machinery proof (different receipt family, honestly scoped)" preserves the real achievement while refusing the transfer. Family note: SN-082's cousin — there, different executions share an artifact SHA (execution identity); here, different receipt families entirely (proof family ≠ target family).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "cross_family_evidence_borrowing",
  "evidence": {
    "board": "#554 comment 5938373714 (2026-10-01T18:54:46Z) — Naya 1 independent P6 qualification: frozen package c5402f3f 14/14 runner exercises kernel demo-001 receipt family (KERNEL_SHA=4e87d4a), target was Demo-1 ACT receipt dec-demo1-live-001/exec-2faff1791adc7906; verdict BLOCKED / CONTRACT MISMATCH. #554 comment 5938629238 (2026-10-01T19:09:50Z) — Naya 2 independent field-matrix confirmation: user_id/project_id/revision/canonical action have no authoritative source in receipt bytes; steps 4-11 cancelled not skipped"
  },
  "rule": [
    "bind every proof artifact to the specimen family it exercised; never cite a family-X PASS for family Y",
    "verify the runner's own source for which family it proves before treating its result as transferable",
    "build the field-by-field matrix against the required table contract; stop at the first field with no authoritative source",
    "never synthesize required semantics (user_id, project_id, revision, action, created_at, learning, value) — fail closed",
    "report downstream steps as cancelled, not skipped; state the structural gap and route the decision to its owning authority"
  ],
  "lesson_line": "A PASS on receipt family X never qualifies receipt family Y. Stop at the first field with no authoritative source — borrowed evidence is not evidence."
}
~~~
