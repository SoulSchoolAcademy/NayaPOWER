# LAW → ACT freshness continuation

Evidence snapshot: canonical main `f2c39b83c468ae6e047fe526b47e7dbef9f10c19`.
This is a dated handoff, not a replacement genome, registry, authority system or runtime ledger.
Recheck main and TEAM NAYA #554 before acting. Later commits do not inherit this proof.

## What changed and why

The live ACT slice now exists. Its recorded deployment proof refers to source
`66e63c02f9590ec52fa14714a8897feb68d18aef`, run `36622283683`.
Both `law-to-act` and `independent-act-verification` jobs were independently fetched
and observed completed/success during this continuation. The proof is bounded to
`DOOR-AI / apply_retained_intelligence / naya_node_apply / NAYA-NODE-0001`.
It establishes a reread/recomputation of the retained-intelligence observation,
not arbitrary external action, universal nine-node binding or general learning.

Canonical proof: `BRAIN/06-PROOF/0007-ACT-LIVE-PROOF-36622283683-V1.json`.
Recorded authorized LAW receipt: `8812e1d2-1ebd-4067-b2be-e04112eab7ec`.
Recorded ACT receipt: `675cac2c-5091-4e18-9b7a-61664f688c10`.
Recorded missing-LAW refusal: `db8e344b-5718-438a-bf7c-e61ac8b0c382`.
These receipt IDs were read from canonical evidence; this continuation did not directly
query production rows or deploy a changed runtime.

ACT's `validateAct` previously skipped the age check when evaluation time was absent;
malformed dates yielded NaN, allowing comparisons to fail open. Failure-first tests
reported 13 passes / 2 failures, with `LAW_AND_LIVE_AUTHORITY_MATCH` where refusal was required.

The correction rejects absent, empty, malformed or future evaluation time, and
malformed non-null decision/live-grant expiry. Valid timestamps, null expiry,
the exact 900-second age boundary and expiry-at-now retain explicit tests.
The canonical ACT contract now states this requirement.

Actual entrypoint: `supabase/functions/nayanet-act-runtime/index.ts`, execute mode.
Guard: `supabase/functions/nayanet-act-runtime/act.ts`, `validateAct`.
The guard runs after the persisted LAW receipt/live grant reread, before `readBlock`.
The existing refusal path writes `nayanet_execution_receipts.action=act_node_refusal`.
OIDC issuer, audience, repository, workflow and main-ref checks are unchanged.

## Evidence boundary

- `node --test --test-isolation=none tests/*.test.mjs`: 65 passed.
- `/tmp/naya-organism-venv/bin/python -m pytest -q`: 249 passed, 3 skipped.
- `git diff --check`: passed.
- Actual HTTP handler exercised offline through VM; JWT verification and database transport mocked.
- Invalid time: HTTP 403, BLOCKED receipt, action_executed=false, observed=false,
  no `nayanet_intelligent_blocks` access. Mock receipt ID `offline-refusal` is not production evidence.
- Interrupted receipt persistence: error, no completed receipt or execution claim.
- Wrong OIDC workflow: no privileged read/write.
- No new production receipt, independent runtime verdict or deployed revision for this patch.
- Green repository tests establish source behavior only. Live proof of the correction is pending.

## Next failing rung — preserve, do not weaken

The canonical LAW evaluator still authorizes an otherwise matching ACTIVE grant whose
`expires_at` is `not-a-date`. An isolated behavioral probe expected refusal and exited 1.
ACT now refuses such decision evidence before its bounded effect, but this does not fix
other LAW consumers. Persisted grants use a timestamp column, so the malformed-input
probe alone does not establish a reachable production database bypass.

PR #1000 separately corrects LAW's undefined-project scope match and source-maps all nine.
It remains a draft at `82b09b28f19cb9648955389ed4e5ad109f2e3b3e`; its ACT mapping predates
the new main implementation and needs reconciliation before merge.
Do not apply this ACT-only correction as proof that #1000 or all LAW boundaries are closed.

Mission constraints, caller-provided same-note intent flags, replay, interrupted effects,
provenance loss, verifier independence and applicable responsibility ablation remain
distinct acceptance obligations. Existing executor tests cover wrong mission; that does
not prove every LAW/ACT consumer binds mission. Do not invent a second mission or authority model.

## Current fourteen-question reconstruction

| Question | Current answer |
|---|---|
| Who are we? | Shawn directs NayaPOWER; Naya is a durable operating intelligence, distinct from human ownership and temporary runtime credentials. SELF anchors that identity; credentials never constitute inherited authority. |
| What are we building? | One governed intelligence organism spanning capture, provenance, retrieval, authorized action, independent verification, justified learning and successor continuity. The nine responsibilities share existing persistence, graph and authority. |
| Why? | Preserve useful understanding across sessions and improve later decisions while reducing repeated human explanation. |
| Success? | A cold successor reconstructs current truth, retrieves applicable intelligence, acts within fresh authority, independently proves an improvement and leaves usable continuity. |
| True now? | Canonical main contains SELF/LAW/ACT bounded slices; ACT's source and recorded bounded live proof are new. PR #1000 is still draft. Universal binding and arbitrary-IB Hub projection remain unproven. |
| Proven? | Recorded bounded LAW/ACT live jobs pass; this correction has failure-first evaluator and actual-handler offline proof. These evidence classes are not interchangeable. |
| Unknown? | Full nine-node causal operation, general VERIFY binding, arbitrary-IB Hub cards, exact-current-main production parity and multi-generation generalization remain unresolved at this snapshot. |
| Authority? | Existing human direction permits source inspection, bounded tests and reviewable corrections. The canonical queue reserves production promotion for explicit DEPLOY and checkpoint policy acceptance for Shawn. Capability/retrieval never grants authority. |
| History? | SN-001 established format, SN-002 explained the river, SN-003 recorded continuation; LAW and ACT bounded proofs followed. Historical receipts constrain claims to their exact source and specimen. |
| Learned? | Optional timestamp fields plus NaN comparisons can remove a freshness gate. Presence and parseability must be checked before calculating age. This is a verified engineering finding, not automatically promoted runtime learning. |
| Next? | Reconcile the existing LAW correction and latest ACT source, then test malformed grant expiry at LAW's actual handler boundary without production mutation. |
| Proof method? | Failure-first behavioral test, actual handler refusals/effect tracing, persisted receipt reread, fresh independent recomputation, exact deployed revision and applicable ablation. |
| Record? | Existing canonical contracts/code/tests, this dated handoff, PR evidence and TEAM NAYA #554. Runtime facts belong in the existing canonical river/receipts. |
| Successor? | Fetch fresh main, check outstanding PRs and board claims, retain these exact limits, execute the one next action below and leave source/test/runtime distinctions intact. |

## Prioritized ten work items

This is a dated prioritization beneath the existing execution queue, not a replacement queue.

| Rank | Work | Why / acceptance boundary |
|---|---|---|
| 1 | Human checkpoint-policy decision, #978/#980 | Existing open security finding; accept/reject the concrete owner-read/privileged-write proposal before applying it. No fresh production advisor query in this continuation. |
| 2 | Reconcile and review LAW scope + ACT freshness corrections | Close demonstrated guards; refresh #1000 against ACT main, failure-first LAW expiry handler proof. |
| 3 | Governed exact-revision promotion and fresh proof | Requires explicit DEPLOY; record actual deployed revision, corrected refusals, canonical receipts and independent reread. |
| 4 | #975 independent outcome recovery | Use existing verifier and exact causal receipt pair; reread actual outcome rows, never manually fabricate outcomes. |
| 5 | #810 bounded acceptance and applicable ablation | Existing verifier is a starting point; prove responsibility changes behavior without requiring all nine for every capture. |
| 6 | KNOW next bounded seam | Relevant owner-scoped retrieval through actual access boundary; provenance/privacy/conflict failures before use. |
| 7 | PROVE/CONNECT integration | Source-bound evidence, typed existing graph relationships, applicability and reconciliation; no inferred authority. |
| 8 | VERIFY→LEARN causal promotion | Independent observations, replay/interruption/provenance loss and durable justified learning; captured notes cannot self-promote. |
| 9 | EVOLVE/cold successor transfer | Fresh authority, held-out related improvement, unrelated refusal and A→B→C continuation. |
| 10 | Arbitrary-IB Hub + human-value/two-owner proof | Same IB projected owner-safely, consent/revocation preserved, observable usability/value; no Hub redesign. |

## Evidence scorecard

Scores are deliberately not invented from issue activity or green unit tests.
The earlier reported numerical scores are estimates, not audited acceptance.

| Area | Auditable status at this snapshot | Missing evidence for a numerical readiness score |
|---|---|---|
| Organism engine | Bounded live LAW/ACT proof; universal binding NOT_PROVEN | Nine-responsibility black-box acceptance with applicable ablation |
| Setup/identity | Canonical identity/OIDC implementation; binding preserved by patch | Fresh exact-revision cold boot and identity continuity evidence |
| Sender | Existing implementation/evidence not re-exercised here | Current deployed sender receipt and authorized handoff |
| Receiver | Existing implementation/evidence not re-exercised here | Current owner-bound intake/projection and independent reread |
| Hub | Arbitrary-IB projection NOT_PROVEN | New arbitrary IB visibly projected as the same canonical object |
| Production readiness | NOT_ESTABLISHED for this source correction | Security acceptance, explicit promotion, deployed revision and current audit |
| Work performed | Failure reproduced, minimal correction, tests green, handoff | CI/review and independent deployed verdict still pending |

## Exactly one next executable action

**Fetch fresh main and PR #1000, then add a failure-first LAW HTTP-handler test for
malformed matching-grant expiry, recording whether that input is reachable through the
canonical persistence adapter.** If the adapter excludes malformed timestamps, keep
the evaluator's fail-closed requirement distinct from a production vulnerability claim.
Reconcile source overlap before any further correction. Stop at an unresolved authority
or source conflict; never bypass OIDC or broaden grants to make the test pass.

After source review, live exercise remains gated by the existing explicit DEPLOY rule.
This handoff creates no authorization to alter checkpoint RLS or production state.
