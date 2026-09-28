# Daily Intelligence Report Contract V1

**Status:** CANONICAL ENGINEERING CONTRACT  
**Purpose:** one durable, addressable Daily Intelligence Report per reporting period.

## 1. Identity

Required:

- `report_id` — immutable stable identifier.
- `report_type` — `DAILY_INTELLIGENCE`.
- `reporting_period` — explicit start/end or date.
- `schema_version`.
- `status`.

## 2. Required sections

Every Daily report contains:

1. Date / reporting period
2. Executive state
3. What changed
4. Major accomplishments
5. Verified evidence
6. Important discoveries
7. Current intelligence / graph state
8. Open gaps / blockers
9. Decisions locked
10. Top-10 priorities
11. Exactly one next action
12. Evidence / receipt references
13. Provenance / source boundary
14. Report status

## 3. Epistemic separation

Every material claim is classified as one of:

- `FACT` — directly supported by identified evidence.
- `INTERPRETATION` — reasoned synthesis; not itself proof.
- `UNKNOWN` — not established.
- `PROPOSED_ACTION` — intended next work, not completed work.

Do not convert an interpretation or proposal into a fact by presentation.

## 4. Evidence law

The report may only claim what its cited evidence supports.

```
IMPLEMENTED ≠ VERIFIED
VERIFIED ≠ PRODUCTION-PROVEN
BLOCKED ≠ PASS
UNKNOWN ≠ VERIFIED
RETRIEVAL ≠ AUTHORIZATION
```

A report is a projection of canonical intelligence and must not manufacture evidence, authority, learning, causality, or production status.

## 5. Human view / machine view

The Markdown and JSON representations MUST share the same:

- `report_id`
- reporting period
- status
- source boundary
- evidence references
- next action

The JSON is the machine contract. The Markdown is the human projection.

## 6. Publication

Publishing a report creates a durable `REPORT_PUBLISHED` event containing:

- event identity;
- report identity;
- publication timestamp;
- report revision;
- source commit;
- report content hash;
- publication status;
- provenance.

The event is suitable for downstream Activity Feed and Hub projection.

## 7. Correction / supersession

Published reports are immutable records.

If a material correction is required:

```
OLD REPORT
   ↓
SUPERSEDING REPORT
   ↓
SUPERSEDES relationship
```

Never silently rewrite history.

## 8. Rollups

Weekly and Monthly reports are derived projections:

```
DAILY → WEEKLY → MONTHLY
```

Every rollup preserves explicit source-report IDs. A rollup never deletes or replaces the underlying Daily record.

## 9. Retrieval

The report index must support retrieval by:

- date;
- report ID;
- status;
- period;
- source lineage;
- predecessor/successor report;
- evidence reference.

## 10. Security / authority

Reports do not grant authority.

Private intelligence remains private by default. Publication is a projection operation governed by the same ownership, consent, and access boundaries as the underlying intelligence.

## 11. Acceptance

The Daily report system is considered minimally established when:

- one real Daily report exists;
- its human and machine views agree;
- the report is addressable from an index;
- provenance and evidence are explicit;
- exactly one next action is present;
- a durable publication event identifies the report;
- tests validate the contract;
- no second intelligence store is introduced.
