# NayaPOWER — North-Star Acceptance Audit v3

**Historical acceptance run:** `36516790588`  
**Historical acceptance source:** `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`  
**Recovery execution source:** `335bdd82568e8041d3f6921a9ee4c7bf28e2c99f`  
**Recovery run:** `36632538416`  
**Governed deployment/proof run:** `36631960490`  
**Audit date:** 2026-09-29 UTC  
**Posture:** independent reconstruction from persisted GitHub/runtime evidence and authoritative Supabase records; no acceptance semantics weakened.

## Result

**Historical North-Star acceptance run `36516790588`: ACCEPTED under its existing bounded evidence contract.**

This closes the two independent-evidence gaps identified by v1/v2 without changing the underlying acceptance criteria:

1. historical checkpoint reconstructability — already closed in v2 through immutable `public.nayanet_checkpoint_receipts`;
2. corroborating execution-outcome records for the exact causal control/treatment receipts — now recovered by the independently authenticated causal verifier and independently reread from authoritative persistence.

This acceptance is bounded to the historical acceptance specimen and its evidence contract. It does not claim universal capability, unrestricted autonomy, or that every later repository revision automatically inherits production proof.

## Evidence preserved from v1/v2

The earlier independent audit established:
- all 18 historical acceptance jobs completed successfully;
- all 16 persisted artifacts matched GitHub artifact digests;
- Event → Intelligent Block → Lineage → Relationship → Index → Learning remained reconstructable;
- causal control/treatment behavior differed as claimed;
- independent verifier recomputed the causal result without trusting executor claims;
- learning was promoted and survived authoritative reread;
- cold successor reconstructed from authoritative state using identifiers rather than caller-supplied intelligence content;
- related-task reuse occurred;
- unrelated-task transfer was refused;
- graph context changed behavior under verified relationships;
- successor authority was not inherited.

v2 additionally established one immutable checkpoint receipt for checkpoint `a58dc3f0-5968-43dc-98ad-c31930777096`, closing the historical checkpoint evidence hole.

## #975 recovery

Issue #975 identified that these historical execution receipts had no corroborating rows in `public.nayanet_execution_outcomes`:

- control: `5b072812-699f-415d-b759-2ed509c36367`
- treatment: `109944fc-9868-45e3-a532-f40952aea3a1`

The recovery path was deliberately constrained:
- existing `nayanet-causal-verify` verifier;
- GitHub OIDC workflow identity;
- exact historical receipt IDs;
- independent recomputation from persisted causal receipts;
- idempotent CREATED/REPLAYED reread semantics;
- no manual SQL outcome fabrication;
- no second outcome pipeline.

The first live recovery attempt, run `36630484162`, correctly failed with HTTP 400. Live function inspection showed the deployed verifier did not yet contain `recover-learning-outcomes`.

The root cause was deployment configuration drift: canonical repository source contained the recovery mode, but `supabase/config.toml` omitted `nayanet-causal-verify` from the native GitHub Integration function set.

PR #1030 repaired only that deployment seam and its regression tests. Repository Kernel Tests and Collective Chain Readiness both passed before merge.

The exact source was then promoted through the governed production path. The native deployed `nayanet-causal-verify` was independently reread and contains both `recover-learning-outcomes` and `NAYANET_CAUSAL_OUTCOME_RECOVERY_V1`.

Governed production promotion `36631960490` completed SUCCESS, including canonical producer, canonical runtime proof, exact source/deployment revalidation, and durable promotion receipt.

## Recovery execution proof

Manual recovery run `36632538416` executed on exact source `335bdd82568e8041d3f6921a9ee4c7bf28e2c99f`.

The `historical-outcome-recovery` job completed SUCCESS:
- OIDC verifier identity minted;
- independent verifier recovery request succeeded;
- recovery artifact upload succeeded;
- normal CVO jobs were skipped for this recovery-only dispatch as intended.

## Authoritative Supabase reread

Independent read-only database reconstruction after recovery returned exactly **2** execution-outcome rows for the audited receipt pair.

### Treatment outcome
- receipt: `109944fc-9868-45e3-a532-f40952aea3a1`
- outcome type: `CAUSAL_TREATMENT_OUTCOME`
- verified: `true`
- verification method: `INDEPENDENT_RUNTIME_RECOMPUTATION_FROM_PERSISTED_CAUSAL_RECEIPTS`
- behavior: `PRESERVE_PROVENANCE_BEFORE_APPLY`
- provenance present: `true`
- treatment condition: `true`

### Control outcome
- receipt: `5b072812-699f-415d-b759-2ed509c36367`
- outcome type: `CAUSAL_CONTROL_OUTCOME`
- verified: `true`
- verification method: `INDEPENDENT_RUNTIME_RECOMPUTATION_FROM_PERSISTED_CAUSAL_RECEIPTS`
- behavior: `REQUIRE_DIRECT_CANONICAL_INTELLIGENCE`
- provenance present: `false`
- control condition: `true`

Both outcomes bind the same historical task, learning identity, source event and GitHub-OIDC workflow lineage.

A second compact authoritative reread independently returned:
- checkpoint rows for `a58dc3f0-5968-43dc-98ad-c31930777096`: **1**
- execution-outcome rows for the audited receipt pair: **2**
- target learning state: **ACTIVE**
- target Intelligent Block understanding state: **LEARNED**

## Acceptance disposition

| Boundary | v2 | v3 |
|---|---|---|
| Historical checkpoint independently reconstructable | VERIFIED | VERIFIED |
| Exact causal control/treatment execution outcomes persisted | MISSING | VERIFIED — 2/2 |
| Independent causal recomputation | VERIFIED | VERIFIED |
| Cold successor reconstruction / no inherited authority | VERIFIED | VERIFIED |
| Related reuse + unrelated refusal | VERIFIED | VERIFIED |
| Historical acceptance specimen | OPEN | **ACCEPTED** |

Therefore the historical North-Star acceptance specimen is now independently reconstructable under the existing evidence contract.

## Explicit limitations

This does not mean:
- every future `main` revision is automatically production-proven;
- every possible task generalizes;
- every NayaNET multi-owner interaction is proven;
- self-building or unrestricted self-optimization is proven;
- historical acceptance replaces current source/runtime parity checks.

Each later production claim still needs its own exact evidence.

## Next frontier

The next work must be chosen from current live evidence, not by continuing this historical issue after its acceptance gap is closed.

At the time of this audit, the separate `Current Truth Resolver` workflow is failing on current main and therefore represents a live continuity/truth-resolution hole that must be independently diagnosed before claiming deterministic cold-current-state resolution.

**#975 status after this audit: READY TO CLOSE ON EVIDENCE.**
