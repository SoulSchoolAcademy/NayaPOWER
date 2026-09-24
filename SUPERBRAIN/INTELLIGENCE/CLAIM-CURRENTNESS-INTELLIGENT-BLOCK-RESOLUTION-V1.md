# CLAIM CURRENTNESS / INTELLIGENT BLOCK RESOLUTION V1

**STATUS:** PROPOSED CANONICAL CONTRACT — SYSTEM 54 DEPENDENCY  
**VERSION:** V1  
**SCOPE:** Epistemic currentness of canonical Intelligent Blocks  
**NON-SCOPE:** Operational current state, Activity, resolver implementation, new persistence

## 1. Purpose

System 54 needs a machine-testable answer to:

> **Which canonical Intelligent Block represents the current epistemic understanding for a subject within a requested context?**

This contract defines that answer using fields already present on `public.nayanet_intelligent_blocks` and the canonical Intelligent Block V1 object. It creates **no new intelligence store** and does not define a new database field.

## 2. Separation of concerns

- **Intelligent Block** = canonical durable understanding.
- **Claim currentness** = a resolution over existing Blocks.
- **Activity / execution records** = historical events unless they independently produce a canonical Block.
- **Operational current state** = remains `.naya/control-plane/STATE.json`.
- **Truth** != confidence.
- **Verified** != automatically current.
- **ACTIVE** != automatically current.
- **Recent** != automatically current.
- **Authority** controls whether a Block may be used/retrieved in a context; authority alone never establishes truth.

## 3. Resolution key

A resolution request is scoped by:

```
subject_id
+ applicable_scope/context
+ evaluation_time
+ authorized audience/owner scope
```

Blocks with different subjects or incompatible applicable scope are not candidates for the same current claim.

## 4. Eligibility for CURRENT

A Block MAY resolve as **CURRENT** only when all required conditions hold:

1. It is a canonical Intelligent Block.
2. `understanding_state` is not `CANDIDATE`, `REJECTED`, or `SUPERSEDED`.
3. `content.truth.state == VERIFIED`.
4. `content.truth.conflicts` is empty or absent.
5. `superseded_by_block_id` is null.
6. Its validity window is open at evaluation time:
   - `valid_from <= evaluation_time` when present;
   - `valid_until > evaluation_time` when present.
7. Its applicable scope matches the requested context.
8. It has source lineage (`source_event_ids`) and evidence/provenance sufficient to explain the claim.
9. It is not explicitly invalidated by a later canonical relationship or lifecycle state.

The contract intentionally does **not** use `updated_at`, confidence, Activity status, or recency as proof of currentness.

## 5. Resolution when multiple eligible Blocks exist

For the same subject/context:

1. Exclude superseded, expired, invalid, conflicted, and ineligible Blocks.
2. Prefer the Block that explicitly supersedes another eligible Block.
3. If more than one independent eligible Block remains and their claims are materially different, return **AMBIGUOUS/CONFLICTED** — never guess from recency.
4. If multiple eligible Blocks carry the same meaning/version lineage, retain the canonical lineage and do not manufacture duplicates.
5. If no eligible Block remains, return **NO_CURRENT_CLAIM**.

The resolver must preserve the losing/history candidates and the reason for exclusion.

## 6. Authority boundary

Currentness answers **what the system currently understands**.

Authority answers **whether a caller may use/share/apply that understanding**.

Therefore:

- `AUTHORIZED` does not make a false claim true.
- `VERIFIED` does not grant authority.
- `REVOKED/EXPIRED` authority blocks authorized use for that audience, but does not rewrite historical truth.
- A private Block can remain epistemically current while being unavailable to an unauthorized caller.

## 7. Resolution result

The minimum result is:

```text
subject_id
evaluation_time
resolution: CURRENT | NO_CURRENT_CLAIM | AMBIGUOUS | INELIGIBLE
selected_block_id: nullable
reason_codes[]
considered_block_ids[]
excluded_block_ids[]
evidence_refs[]
```

Recommended reason codes:

```text
VERIFIED_TRUTH
OPEN_VALIDITY_WINDOW
NOT_SUPERSEDED
SCOPE_MATCH
EVIDENCE_PRESENT
CANDIDATE_NOT_VERIFIED
SUPERSEDED
STALE_OR_EXPIRED
CONFLICTED
SCOPE_MISMATCH
MISSING_LINEAGE
AMBIGUOUS_CURRENT_CLAIMS
```

## 8. Required discriminating behavior

| Case | Expected result | Why |
|---|---|---|
| VERIFIED + active + unsuperseded | CURRENT, if it is the sole eligible claim | Verified truth plus open validity and lineage |
| VERIFIED but superseded | not current | Later canonical successor wins |
| ACTIVE + CANDIDATE | not current | Candidate is not established truth |
| VERIFIED + expired validity | not current | Temporal validity closed |
| VERIFIED + conflict | not current / ambiguous | Cannot silently select one |
| Same subject, different scope | not competing | Context boundary separates claims |
| Activity record marked verified | not current by itself | Activity is history, not canonical claim |
| Current candidate wording | not current | CANDIDATE cannot establish epistemic CURRENT |

## 9. Currentness is a derived decision, not stored truth

Do not add:

```
current=true
```

to the Block merely to satisfy System 54.

Currentness is resolved from the canonical Block's existing truth, lineage, lifecycle, temporal, evidence, and scope fields.

This keeps one canonical intelligence object and prevents a second intelligence store.

## 10. Known live-data limitation

As of 2026-09-24, the production Intelligent Block table contains:

- 337 Blocks;
- 246 ACTIVE + VERIFIED;
- 2 DURABLE + VERIFIED;
- 32 ACTIVE + CANDIDATE;
- 57 SUPERSEDED + VERIFIED;
- 0 Blocks with `valid_until`;
- 0 Blocks with recorded truth conflicts;
- 57 Blocks with a successor relationship.

Therefore the live corpus directly demonstrates the **verified-but-not-current**, **active-candidate**, and **superseded** distinctions.

It does **not** currently contain a naturally occurring expired/stale Block or conflict case. Those cases must be tested with non-persistent derived fixtures or a future real record; do not mutate production data merely to manufacture test cases.

## 11. Explicit System 54 boundary

System 54 MUST consume this contract only after its discriminating tests pass.

System 54 MUST NOT:

- infer CURRENT from a status string;
- promote Activity records;
- rewrite the Intelligent Block resolver;
- create another claim/currentness store;
- treat an empty current set as success;
- fabricate a current claim to satisfy a gate.

**Truth before green.**
