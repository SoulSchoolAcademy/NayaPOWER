# REPAIR RECEIPT — `repair/ai1-capability-carry` (Option A, branch-only)

**Branch:** `repair/ai1-capability-carry`
**Base SHA (origin/main):** `f648833b9e0a38296a3e13233058fe25ffc81082`
**Repair commit:** `<filled at commit time>`
**Date:** 2026-09-30
**Scope authorized:** code + tests + static verification ONLY.
**Explicitly NOT authorized / NOT done:** merge, deploy, production data
changes, re-commit of SN-013/SN-014, pre-registration v2 witnessing,
experiment execution, any Active Intelligence claim.

## Old writer behavior

The commit path (`nayanet-intelligence-commit-runtime` edge function →
`nayanet_intelligence_commit_runtime` bridge → `nayanet_intelligence_commit`
RPC) forwarded `p_event_id / p_title / p_content / p_category / p_topic /
p_target_id / p_authority_grant_id / p_project_id / p_connections` and persisted
`content = {lesson, topic, category}`, `applicable_scope = {target,
project_id}` — with **no** capability metadata. `deriveCapabilities` therefore
fell through to the bounded legacy regex, which matches doctrine text 0×, so
doctrine blocks were retained but never retrievable by purpose.

## New writer behavior

The capture may declare `capabilities: [...]`. The edge function validates it
against the bounded vocabulary (fail fast, HTTP 400) and forwards
`p_capabilities` to the runtime bridge, which threads it to the inner RPC. The
RPC validates server-side (fail closed: unknown/malformed rejects the commit)
and persists the validated, normalized, deduped array at
`content.capabilities` — the field `deriveCapabilities` already reads — plus a
`provenance.capability_declaration = {source: 'intelligence_commit_capture',
values: [...]}` record and a `declared_capabilities` entry on the immutable
commit receipt. Absent/empty → the block persists **byte-identical** to today.

## Capability vocabulary (verbatim, from the canonical file)

- `governance_triage` — "Intelligence that may inform governed triage decisions (act / read / ask / escalate / decline) under the 6→10 doctrine. Declaring this capability asserts relevance to governance triage, not correctness for any specific decision."
- `compounding_capture` — "Intelligence about capturing, preserving, and compounding learned intelligence across sessions and successors. Declaring this capability asserts relevance to compounding discipline, not universal applicability."

Canonical owner: `supabase/functions/nayanet-intelligence-commit-runtime/capability-vocabulary.ts`
(definition/addition/deprecation/validation/compatibility — see file header).
The SQL migration mirrors the set; the test suite asserts the mirror agreement.

**Canonical capability storage location = `content.capabilities`.**
The alternate field, `applicable_scope.capabilities`, is legacy-compatibility
read-only: the selector may union it internally, but the writer is forbidden
from writing it for new blocks (asserted by test AI1-WRITE-04).

## Two-block pilot results (TEST fixtures, full chain per capability)

| link | governance_triage | compounding_capture |
|---|---|---|
| capture → validate | `["governance_triage"]` accepted | `["compounding_capture"]` accepted |
| persisted `content.capabilities` | `["governance_triage"]` | `["compounding_capture"]` |
| `deriveCapabilities` (actual know.ts) | `["governance_triage"]` | `["compounding_capture"]` |
| `selectKnowContext` intended query | HIT, `IB-AI1-PILOT-GT` | HIT, `IB-AI1-PILOT-CC` |
| `retrieval_creates_authority` | `false` | `false` |
| cross-isolation | GT query never selects CC pilot | (asserted both directions) |
| fixture servability state | VERIFIED (test-only) | VERIFIED (test-only) |

Real commits land at CANDIDATE (unservable); the repair changes no states
(see §11 below).

## State-transition note

**This repair performs zero state transitions.** No block is moved
CANDIDATE→LEARNED or to any other state by this branch. Servability still
depends on the existing `SERVABLE_STATES` and the governed `nayanet-learning-verify`
promotion, revalidated against #1170 (immutable commit-receipt anchoring).
The honest answer to "is this block honestly eligible to be served before this
experiment?" is: a freshly committed block at CANDIDATE is **not** servable;
it becomes servable only through the existing governed promotion path —
never by state manipulation for retrieval convenience. The supersede RPC was
not invoked during this build.

---

## 15-item proof package (one decisive evidence pointer per item)

1. **Scope.** Branch-only: 8 files changed, all within writer/commit path +
   vocabulary + tests + repair docs. `git diff --cached --stat` on the branch.
2. **Diff.** `supabase/functions/nayanet-know-runtime/know.ts`: **0 lines
   changed** (selector frozen). Edge function: +15 lines (validate + forward).
   Migration: additive drop+recreate with trailing `p_capabilities text[]
   default null` (p_connections precedent). No workflow files touched.
3. **Tests.** `node --test tests/*.test.mjs` → **221 pass, 0 fail** (CI command
   from `.github/workflows/kernel-tests.yml`). New: `tests/ai1-capability-carry.test.mjs`
   (29 tests: vocabulary, writer carry, derivation, eligibility chain,
   selection incl. 4 precision negatives + superseded regression + injection
   resistance, 2 pilots + cross-isolation). Updated:
   `tests/intelligence_commit_handler.test.mjs` (exact RPC-body contract now
   pins `p_capabilities`; real vocabulary module injected into the offline VM;
   +3 fail-closed forwarding tests).
4. **Writer payload.** Edge function forwards `p_capabilities: capabilities`
   (validated array or null) in the named-arg RPC body — asserted byte-exact by
   the handler test (`p_capabilities: null` default; normalized/deduped array
   when declared).
5. **Persisted object.** `content = {lesson, topic, category}` plus
   `capabilities` ONLY when declared; `provenance.capability_declaration`
   records `{source: 'intelligence_commit_capture', values}`; receipt
   `evidence.declared_capabilities` mirrors it. Absent → no `capabilities` key
   (test AI1-WRITE-02 deep-equals the pre-repair shape).
6. **Derived capability.** Actual `deriveCapabilities` (imported from know.ts,
   not reimplemented) returns `["governance_triage"]` for the persisted shape
   (AI1-DERIVE-01); doctrine-like text without carried capabilities derives
   `[]` — the bounded legacy fallback is NOT the causal path (AI1-DERIVE-02).
7. **Selector candidate.** Actual `selectKnowContext` over writer-shaped rows:
   eligible + matching capability → HIT with the intended `selected_block_id`
   (AI1-SELECT-01, AI1-PILOT-01/02/03).
8. **Servability.** Eligibility chain tested per-condition via the actual
   `isEligibleBlock` (AI1-ELIG-01: id, owner, status, state, supersession,
   provenance, evidence, scope-target each independently observable). A
   CANDIDATE block with a matching capability → MISS (AI1-SELECT-04): the
   repair manufactures no servability.
9. **Negative cases.** Wrong capability → MISS (AI1-SELECT-02); superseded →
   excluded (AI1-SELECT-03 regression); non-servable state → excluded
   (AI1-SELECT-04); wrong owner → excluded (AI1-SELECT-05); unknown name
   cannot produce a selectable block — writer rejects (AI1-SELECT-06,
   AI1-VOCAB-02); capability words in lesson prose do not select —
   no heuristic inference (AI1-SELECT-07).
10. **Backward compatibility.** Untagged blocks persist byte-identical
    (AI1-WRITE-02); untagged blocks retrieve exactly as before — MISS for the
    new capabilities, legacy `provenance_preservation` path intact
    (AI1-SELECT-08, AI1-DERIVE-03); full pre-existing suite still green.
11. **State semantics.** Zero state changes in branch (this receipt, §State-transition
    note). CANDIDATE→LEARNED remains solely via `nayanet-learning-verify`,
    revalidated against #1170's immutable-receipt reconstruction; the repair
    neither invokes it nor alters its preconditions.
12. **Runtime implications.** Deployed edge function gains one validated
    optional field; RPC gains one trailing optional parameter with default —
    existing callers unaffected. No new tables, no new RPCs, no new authority
    checks, no selector behavior change. `retrieval_creates_authority` remains
    `false` on every HIT: capability metadata creates zero authority.
13. **No production impact.** No merge (branch only), no deploy workflow trigger
    (deploy workflow fires on `main` push only), no data writes, no re-commit,
    no promotion, no execution. Verified: branch is the only ref created.
14. **Source/revision binding.** Base `f648833b9e0a38296a3e13233058fe25ffc81082`
    (origin/main 2026-09-30); reconciliation of the old pin `8cb4f109` in
    `RECONCILIATION-ai1-seam.md` (all seam claims STILL TRUE; #1166/#1170/#1125
    reconciled; run 36773534374 classified as retrieval-stage, not KNOW,
    evidence). Failure matrix in `FAILURE-MATRIX-ai1.md`. v2 draft (procedure
    only) in `V2-DRAFT-PROPOSAL.md`.
15. **Remaining UNKNOWNs.** (a) The plpgsql migration has not executed against
    a live database in this environment (no DB available; branch-only scope
    forbids it) — logic is minimal, mirrors existing patterns, and is
    reviewer-verified on read; live deploy-time verification remains. (b) Real
    v2 block ids/hashes require governed re-commit (draft procedure only).
    (c) Production HIT proof requires the setup probe after deploy + promotion
    (separate gates).

## Anti-patterns observed (none present)

No synthetic fallback (actual know.ts + actual vocabulary module imported); no
silent artifact skips (all writes asserted); no expected-value substitution
(assertions run the real functions); no fixture-declared behavior (fixtures
labeled test-only; SQL non-execution stated openly); no manual selection (the
real selector chooses); no alternate retrieval path (only selectKnowContext);
no post-hoc threshold changes (no thresholds in the repair); no state
inflation (servable fixtures labeled; CANDIDATE negative proves the gate).
