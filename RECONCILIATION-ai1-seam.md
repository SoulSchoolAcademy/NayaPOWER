# AI1 Seam Reconciliation — pin 8cb4f109 → f648833b9e0a38296a3e13233058fe25ffc81082

**Basis:** fresh clone at `f648833b9e0a38296a3e13233058fe25ffc81082` (origin/main, 2026-09-30).
**Old basis:** `8cb4f109683940b93dd51ed257b9629a666c161a` (reviewer's original analysis pin).
**Method:** `git diff <old> <new>` on every file in the writer→selector seam, plus
inspection of #1166, #1167, #1168, #1170 and the GitHub PR record for #1125.
No production reads were performed; production-sourced claims are marked CARRIED.

## Classification key

- **STILL TRUE** — verified byte-identical or semantically identical at the new pin.
- **CHANGED** — materially different at the new pin; the repair must account for it.
- **SUPERSEDED** — the old claim is replaced by a newer one.
- **UNKNOWN** — cannot be determined from the repository at the new pin.
- **CARRIED** — production-sourced, not re-verifiable from the repo; unaffected by
  main movement (no writer/selector change touches it).

## Reconciliation table

| # | Original claim (old pin) | Status | Evidence at f648833b |
|---|---|---|---|
| C1 | `selectKnowContext` filters candidates by `required_capability ∈ deriveCapabilities(block)` | **STILL TRUE** | `git diff 8cb4f10..f648833 -- supabase/functions/nayanet-know-runtime/know.ts` is **empty**. Filter at know.ts:277 unchanged. |
| C2 | `deriveCapabilities` reads `applicable_scope.capabilities[]` + `content.capabilities[]` (deduped, stringified); falls back to a bounded legacy regex | **STILL TRUE** | know.ts:234–248 byte-identical. Legacy fallback remains a single regex → `"provenance_preservation"` only. |
| C3 | Commit writer persists `content={lesson,topic,category}` and `applicable_scope={target,project_id}` with **no** capability metadata | **STILL TRUE** | Edge function `nayanet-intelligence-commit-runtime/index.ts` byte-identical between pins; forwards `p_event_id/p_title/p_content/p_category/p_topic/p_target_id/p_authority_grant_id/p_project_id/p_connections` — **no `p_capabilities`**. Inner RPC `nayanet_intelligence_commit` last defined in `20260930191233…v2.sql`, builds `jsonb_build_object('lesson',p_content,'topic',p_topic,'category',p_category)` — unchanged. |
| C4 | Legacy regex matches 0× in the SN-013 doctrine text | **STILL TRUE** | Regex unchanged (C2); doctrine text is production data, unchanged by main movement. |
| C5 | Commits land at `understanding_state='CANDIDATE'`; KNOW serves only `VERIFIED/DISTILLED/APPLIED/LEARNED` → CANDIDATE is unservable | **STILL TRUE** | `SERVABLE_STATES` unchanged; RPC still writes `'CANDIDATE'` (20260930191233). The repair does **not** change any state. |
| C6 | `nayanet-learning-verify` can promote eligible blocks CANDIDATE→LEARNED | **CHANGED** (strengthened, same mechanism) | #1170 reworked the promotion path: when the mutable checkpoint row has advanced past the block's checkpoint, learning-verify now reconstructs the historical checkpoint from the **immutable `intelligence_commit` execution receipt** (`checkpoint_provenance: "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT"`), and lock-in additionally accepts `historicalReceiptLockIn` (receipt `learning[]` entry verified). The promotion remains the only governed CANDIDATE→LEARNED path; no code path manufactures `LEARNED` for retrievability. |
| C7 | SN-013 = `IB-SMART-NOTE-20260930-sn013-decision-efficiency` (hash `2a534acea…`); SN-014 = `IB-SMART-NOTE-20260930-sn014-compounding-imperative` (hash `318b7a06…`) | **CARRIED** | Production-sourced identities; not re-verifiable from the repo. No writer/selector movement affects them. Re-commit/promotion remain explicitly unauthorized. |
| C8 | Analysis basis `8cb4f109` | **SUPERSEDED** | New basis `f648833b9e0a38296a3e13233058fe25ffc81082`. |
| C9 | The seam is the **writer→selector capability contract**, not another Brain subsystem | **STILL TRUE** | Both endpoints byte-identical; the barrier reproduces exactly at the new pin. |
| C10 | Open selector PR / #1125 dedupe commitment | **CHANGED** | #1125 is a **draft PR** titled `[GOVERNANCE BLOCKED] feat(know): Graph V2 selector gates into retrieval` — state open, draft, governance-blocked (verified via GitHub API 2026-09-30). The repair does not touch `know.ts` and therefore does not interact with #1125. |

## New findings at f648833b (not in the original brief)

| # | Finding | Relevance |
|---|---|---|
| N1 | **#1166** (`2ff9e002d`, "prove active intelligence on an applicable causal task") added **heuristic** capability inference (`lesson.includes(…) → "active_intelligence_discipline"`) inside `nayanet-cold-runtime-proof/index.ts` — a **proof harness**, not the canonical path. It does not persist capabilities, does not change `deriveCapabilities`/`selectKnowContext`, and introduces a harness-local string (`active_intelligence_discipline`) that is **not** part of any canonical vocabulary. | Must **not** be duplicated. The repair uses **explicit declared** capabilities only (10-point contract §6: no heuristic inference where explicit metadata exists). Materially different task, different strings, different layer — kept separate. |
| N2 | **#1170** added a heuristic `deriveGraphApplicability` branch in `nayanet-learning-verify/index.ts` keyed on lesson-text regex (same active-intelligence lesson). | Heuristic, learning-verify-local. Not the commit path; not reused by the repair. |
| N3 | **No canonical capability-vocabulary owner exists on current main.** Searched `BRAIN/00-SPEC/`, `BRAIN/04-INTELLIGENCE/`, `BRAIN/11-KNOWLEDGE/`, `KNOWLEDGE/`, `.naya/project-intelligence/`, all `*.sql`, and the machine-contract schema: the only bounded vocabularies are `EDGE_VOCABULARY` (22 relationship types — explicitly out of scope) and the legacy `"provenance_preservation"` regex. | The repair therefore creates the **smallest canonical bounded seam**: one vocabulary file owned by the writer/commit contract, mirrored (not duplicated) in the SQL writer, with a test asserting the two agree — following the repo's R1 precedent (`tests/know-writer-roundtrip.test.mjs` "migration vocabulary matches the canonical 22-type contract"). |
| N4 | **Correction:** `isEligibleBlock`'s gates (`SERVABLE_STATUS`, `SERVABLE_STATES`, `superseded_by_block_id` exclusion, non-empty `provenance`/`evidence_refs`, owner match, scope-target match) are **byte-identical at both pins** — they are long-standing, not new in #1166/#1170. | The amendment's four precision negatives map directly onto these existing gates. No new selector behavior is needed or introduced. |
| N5 | Test convention: `node --test tests/*.test.mjs` (CI: `.github/workflows/kernel-tests.yml`); existing `tests/know-writer-roundtrip.test.mjs` already imports the **actual** `know.ts` and asserts writer-stamped row shapes round-trip through `selectKnowContext`. | The repair's tests follow this exact convention — no new test framework. |

## Net effect on the repair

- The seam, the barrier, and the Option A shape are **unchanged** by main movement.
- The repair stays confined to: vocabulary contract + commit RPC migration +
  runtime-bridge threading + edge-function forwarding + tests. `know.ts` untouched.
- #1170's immutable-receipt anchoring is **reused by reference, not duplicated**:
  the repair records the capability declaration in the block `provenance` and in the
  commit receipt `evidence`, so the declaration itself becomes historically
  reconstructible through the receipt #1170 made canonical.
- #1166's heuristic inference pattern is **explicitly not** copied into the writer.

## Field canonicalization

**Canonical capability storage location = `content.capabilities`.**

The alternate field, `applicable_scope.capabilities`, exists in the selector's
read union (`structuredCapabilities`) for legacy compatibility only. Its
defined semantic role: **read-path legacy compatibility; forbidden for new
writes.** The writer has ONE canonical representation (`content.capabilities`);
the selector may union two sources internally, but the writer never writes the
alternate field (asserted by test AI1-WRITE-04).

## Vocabulary ownership

No canonical owner existed on current main (N3). The repair establishes the
smallest bounded seam, owned by the writer/commit contract:

| aspect | owner |
|---|---|
| definition | `supabase/functions/nayanet-intelligence-commit-runtime/capability-vocabulary.ts` — changed only by governed repo PR |
| addition | Human-Director-approved PR extending the bounded set AND regenerating the SQL mirror AND updating the mirror-agreement test. No autonomous addition; capture authors must not mint production capabilities (writer rejects unknown names) |
| deprecation | removal from the bounded set by PR; already-persisted blocks stay selector-visible (opaque matching); new writes with the removed name are rejected |
| validation | writer-side, two layers: edge function (fail fast, 400) + SQL writer (fail closed, commit rejected) |
| compatibility | test asserts the SQL mirror contains exactly the module's values |

## #1166 vs #1170 — traced answers

**#1166** (`2ff9e002d`, "prove active intelligence on an applicable causal task"):
implements (a) an active-intelligence causal task inside the
`nayanet-cold-runtime-proof` **proof harness** — including heuristic lesson-text
→ capability inference (`lesson.includes(…) → "active_intelligence_discipline"`)
and a harness-local task registry; (b) a runtime-parity comparison fix
(deployable source vs repo drift). It does NOT touch `know.ts`, does NOT
persist capabilities, and its capability strings are harness-local.

**#1170** (`f648833b`, "durable historical checkpoint reconstruction"):
implements (a) historical checkpoint reconstruction in `nayanet-learning-verify`
from the **immutable `intelligence_commit` execution receipt**
(`checkpoint_provenance: "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT"`,
`historicalReceiptLockIn`); (b) generalized ACTIVE reuse / successor proof for
SN-015 (learning-verify + causal-learning-experiment + cold-runtime-proof +
tests); (c) producer-dispatch binding fixes; (d) workflow changes
(`live-intelligence-commit-proof.yml`, `live-supabase-runtime-proof.yml`).

**Overlap:** both add a heuristic regex branch keyed on the active-intelligence
lesson text — #1166 in the proof harness (task routing), #1170 in
learning-verify (`deriveGraphApplicability`: task_classes
`active_intelligence_sensitive / learning_reuse / contextual_retrieval`).
Different domains, no conflict; **neither is authoritative for capability
vocabulary** — both are local heuristics.

**Duplicates:** none that the repair inherits. The repair reuses neither
heuristic; it introduces explicit declared capabilities instead (per the
10-point contract §6).

**What survives into the repair branch:** #1170's immutable-receipt anchoring,
by reference — the repair records the capability declaration in block
`provenance` AND in the commit receipt `evidence.declared_capabilities`, so the
declaration itself is historically reconstructible through the receipt #1170
made canonical. #1166's machinery is not reused (different task, heuristic
layer, harness-local).

## Run 36773534374 (live-intelligence-commit-proof.yml)

- Workflow "Live Intelligence Commit Proof", head `f5c808375` (#1168),
  `workflow_dispatch`, conclusion **failure** (2026-09-30T20:34:06Z).
- Failed at job `cold-successor-held-out`, step 5:
  "Cold retrieve this run's exact Smart Note from machine registry and
  canonical runtime".
- The run executed **pre-#1170** code (#1170 merged 20:52 UTC, after the run
  started). #1170's message includes "fix(smart-note): reconstruct missing
  expected artifact deterministically" — the project itself identified
  missing-expected-artifact as a failure mode and repaired it after this run.
- **Classification:** retrieval-STAGE failure evidence. The step retrieves
  "this run's exact Smart Note **from machine registry** and canonical
  runtime" — the named sources include the workflow's own machine registry
  (artifact availability), not just the KNOW selector. The available evidence
  is consistent with a workflow-artifact availability failure at the retrieval
  stage; it does **not** establish a KNOW selector failure (no selector MISS
  evidence is available from run metadata). It is independent production
  evidence that the retrieval stage is the weak link — **not** labeled a KNOW
  failure. No diagnosis beyond this is invented.

## State semantics (revalidated against #1170)

"Is this block honestly eligible to be served before this experiment?"
**No** — for a freshly committed block. The current state machine:

- Commits land at `CANDIDATE` (unservable; `SERVABLE_STATES` unchanged).
- The only governed CANDIDATE→LEARNED path is `nayanet-learning-verify`:
  candidate-mode re-validation of the persisted event→block→lineage→
  relationship→index→checkpoint chain, a `learning_evidence` row, then a
  verify-mode call with evidence + method from the authorized OIDC workflow.
- #1170 strengthened this path (immutable commit-receipt anchoring,
  `IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT`) but did not change what LEARNED means:
  "provenance re-validated + verification attested" — NOT "behaviorally
  validated", NOT "retrieval-enabled for convenience".
- This repair performs **zero** state transitions and invokes neither the
  learning-verify nor the supersede RPC. Repair now; production revision later;
  separate phases.
