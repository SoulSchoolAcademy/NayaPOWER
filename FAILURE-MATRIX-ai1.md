# AI1 Failure Matrix — boundary × expectation × failure-meaning

**Purpose:** when a future retrieval does not produce the expected HIT, this
matrix identifies the **first broken edge** instead of auto-misdiagnosing every
MISS as a capability failure.

**Three failure kinds** (Director's classification):

- **CAPABILITY failure** — purpose unknown: the block carries no usable purpose
  metadata, the query names a purpose the writer never declared, or the
  declaration was rejected/mangled before persistence.
- **ELIGIBILITY failure** — purpose known, but the block is refused by
  state, status, supersession, provenance, evidence, owner, or scope-target.
- **RETRIEVAL failure** — the block is eligible AND purpose-compatible, yet the
  query still misses. This is the only kind that indicts the selector itself.

**Reading rule:** walk the boundaries in order. The FIRST boundary whose check
fails names the failure kind. A later boundary can only break if all earlier
ones hold. `NO EFFECT ≠ INVALID`; a correctly-classified failure is a
diagnostic, not a defect.

| # | Boundary | Expectation (check) | If broken → first-broken-edge meaning | Kind |
|---|---|---|---|---|
| 1 | Capture→writer | The capture declares `capabilities`; the writer accepts only bounded names. Check: `validateCapabilities` returns the expected array; unknown/malformed rejects the commit. | Declaration rejected or absent at the door: typo'd name, non-array, empty. Nothing was persisted with the intended purpose. | **CAPABILITY** |
| 2 | Writer→DB | The persisted row carries `content.capabilities = [<declared>]` and `provenance.capability_declaration = {source: 'intelligence_commit_capture', values: [...]}`; the commit receipt `evidence.declared_capabilities` matches. | Write-path mangling: field dropped, renamed, or stored in the wrong location (e.g. `applicable_scope`). The DB row does not reflect the capture. | **CAPABILITY** |
| 3 | DB→deriveCapabilities | `deriveCapabilities(persistedRow)` returns the declared capability. Check against the actual `know.ts` export. | Derivation gap: the row shape the writer stamps is not the shape the selector reads (schema drift), or the legacy fallback is masking the miss. | **CAPABILITY** |
| 4 | derive→selector (capability compatibility) | The derived set includes `required_capability` (exact string match). | Purpose mismatch, not a defect: the block is about X, the query asks for Y. Expected behavior is MISS. | **CAPABILITY** |
| 5 | selector→eligibility | `isEligibleBlock` holds: id present, owner match, status ∈ {ACTIVE,DURABLE,RELEASED}, understanding_state ∈ {VERIFIED,DISTILLED,APPLIED,LEARNED}, not superseded, provenance non-empty, evidence_refs non-empty, scope-target match. Each condition is separately observable (see tests AI1-ELIG-01). | Purpose known but refused. Sub-classify by the exact failing gate: **state** (e.g. CANDIDATE — the honest pre-promotion condition), **supersession**, **provenance**, **evidence**, **owner**, **scope**. | **ELIGIBILITY** |
| 6 | selector→KNOW result | `selectKnowContext` returns HIT with `selected_block_id` = the intended block. | Eligible + purpose-compatible yet MISS (or wrong block selected). This — and only this — is selector-indicting. | **RETRIEVAL** |
| 7 | KNOW→bind | The setup probe captures the authenticated HIT object: expected vs actual block id, expected vs returned hash, `hit_object_hash`. (Harness: `runs/setup-probe-HIT.json`; runbook `--bind`.) | Retrieval provenance broken: the object the experiment will consume is not the object KNOW returned, or hashes disagree. Expectation ≠ observation until this check passes. | **RETRIEVAL** |
| 8 | bind→consumer | The exact bound object (hash-verified at ingest, never trusted from stored fields) is injected into the consumer prompt. | Exposure broken: consumer reasoned over a different object than the HIT. | **RETRIEVAL** |
| 9 | consumer→decision→score | The decision artifact is produced from the injected input; scoring is condition-blind against the frozen rubric. | Attribution broken: score reflects treatment knowledge rather than decision quality, or the artifact does not derive from the input. | **RETRIEVAL** (evidence-chain) |

**Scope note:** boundaries 1–6 are closed by this repair's tests (see
`tests/ai1-capability-carry.test.mjs`: AI1-WRITE-*, AI1-DERIVE-*, AI1-ELIG-01,
AI1-SELECT-*). Boundaries 7–9 belong to the experiment harness/runbook phases
(setup probe, `--bind`/`--ingest`, blind scoring) and are defined here so the
first broken edge is never misattributed to the writer↔selector seam.

**Anti-misdiagnosis examples:**

- A treatment MISS where the block is at CANDIDATE is an **ELIGIBILITY (state)**
  outcome at boundary 5 — not a capability failure, not a selector defect. The
  honest next step is the governed learning-verify promotion, never a state edit.
- A MISS where `deriveCapabilities` returns `[]` for a doctrine block is a
  **CAPABILITY** outcome at boundary 1–3 — the writer never carried the purpose.
- A MISS where derivation returns the capability and all eligibility gates pass
  is a **RETRIEVAL** outcome at boundary 6 — the only case that reopens the
  selector for inspection (and the selector is frozen for this repair).
