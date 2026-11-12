# Learning Promotion Receipt — Schema V1

**Status:** CANDIDATE (not ratified) · **Owner:** Learning team (#1865) · **Created:** 2026-10-08

## Purpose

Every `learning_evidence` CANDIDATE row gets a decisive verdict. No limbo: a row is
PROMOTEd, DROPped, or HELD with a recorded reason. This ledger is the verdict record;
it does **not** write to the database. Status changes in Supabase remain a separate
governed action.

## Verdicts

| Verdict | Meaning | When |
|---|---|---|
| `PROMOTE` | Lesson is valid, evidence-backed, **and** clears the Standing Promotion Law gates (trial proof, no negative transfer, **independent** verification, immutable audit receipt). | All four gates evidenced. |
| `DROP` | Row leaves the candidate queue. | Stale, duplicate, or not-a-lesson (e.g. chat chatter captured as a lesson). Dropping a row is not calling it false — it is refusing to promote noise. |
| `HOLD` | Valid lesson, evidence present, but a promotion gate is still open. Decisive, not limbo: names the blocking gate and the next step. | e.g. paired control/treatment receipts exist but independent causal verification is pending. |

## Why HOLD exists

Promoting without independent verification repeats the exact error Naya 1 challenged on
2026-10-08 (manual CANDIDATE→ACTIVE flips with improvised receipts, later deleted).
A HOLD receipt is the honest middle: the lesson is real, the evidence is recorded,
the gate is named, and promotion waits for the verifier — never for the builder's
own judgment.

## Receipt fields

- `schema`: `learning-promotion-receipt/v1`
- `lesson_id` / `lesson_id_short`: the `learning_evidence` row UUID
- `claim_summary`: human-readable lesson gist
- `evidence`: `source_event_id`, `provenance`, `verification_method`, `row_created_at`,
  `observed_value_sha16` (integrity fingerprint of the row's evidence payload),
  `paired_control_treatment` (bool)
- `assessed_by` / `assessed_at`: who verdict­ed and when
- `verdict`: `PROMOTE` | `DROP` | `HOLD`
- `verdict_reason`: the decisive reasoning
- `next_step`: what unblocks a HOLD, or `None` for DROP

## Ledger files

One JSON file per assessment run: `receipts-YYYY-MM-DD.json`, with a `summary` block
(counts per verdict) and the full `receipts` array.
