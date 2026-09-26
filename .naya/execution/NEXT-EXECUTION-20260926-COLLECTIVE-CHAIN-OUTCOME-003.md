# 🔱 COLLECTIVE-CHAIN-OUTCOME-003 — EXECUTABLE SUCCESSOR

## Mission
Complete the existing real Collective Intelligence Chain proof without bypassing the independent-outcome law.

## Current verified boundary
Run 36259399548 on main failed at the first intelligence_commit because the proof supplied no authority_grant_id. That failure was expected by the current authority contract.

Repair PR #784 added a fresh proof-owner source event and bounded intelligence_commit grant. Run 36259399548 on the repaired branch then failed later at:
**INDEPENDENT_OUTCOME_ID_REQUIRED**
Run 36259467103 reached this boundary only after successful capture, retrieval, connection, reconciliation, learning candidate creation, and the authority boundary.

## Authoritative contract
learning_verify requires:
- evidence_id
- verification_method
- outcome_id
- source_event_id matching the learning evidence
- a row in nayanet_execution_outcomes owned by the same member
- verified=true
- verifier_id != the learner
- non-empty evidence
- finite verified_value
- receipt_id matching the independent outcome

Therefore do NOT weaken learning_verify and do NOT invent an outcome row.

## Execute
1. Read live main and the existing collective-chain workflow.
2. Inspect the already-proven independent-outcome mechanism in:
   - scripts/run-controlled-paired-policy-experiment.mjs
   - scripts/verify-proof7-compounding-loop.mjs
   - the current nayanet_execution_outcomes migrations/functions
3. Reuse the existing canonical outcome mechanism rather than creating a new outcome system.
4. Extend the collective-chain proof with the smallest compatible independent-outcome path:
   - create/use a second authenticated verifier identity;
   - execute one governed action whose result can be independently observed;
   - record the outcome through the existing canonical outcome boundary;
   - verify outcome_id, receipt_id, verifier_id, evidence, verified_value and ownership;
   - pass outcome_id + receipt_id + source_event_id into learning_verify.
5. Preserve the lesson semantics: the verified lesson must influence a later governed decision without changing authority.
6. Continue the chain:
   lesson → retrieve → connect → reconcile → learning candidate → independent outcome → verified learning → apply → behavior change → observed outcome → improved checkpoint → fresh retrieval.
7. Run the workflow from the clean branch.
8. If it fails, diagnose the first deterministic boundary and repair only that boundary.
9. Update registry/topology/Project Intelligence evidence and the control plane only after proof is real.
10. Post Issue #554 UPDATE and SIGN-OUT, leaving exactly one successor.

## Hard stops
- Do not relax INDEPENDENT_OUTCOME_ID_REQUIRED.
- Do not self-verify the outcome.
- Do not insert a fabricated outcome.
- Do not use service-role authority to fake an independent verifier.
- Do not create a second outcome model.
- Do not claim PROVEN from the workflow source.
- Do not alter constitutional authority.

## Acceptance
PASS only when the workflow itself produces and independently verifies a canonical outcome and then proves learning promotion, later applicability/behavior change, observed outcome, improved checkpoint, and fresh retrieval.

## One successor
After this action, recalculate the top 10 and write the complete next execution prompt before ending the wave.
