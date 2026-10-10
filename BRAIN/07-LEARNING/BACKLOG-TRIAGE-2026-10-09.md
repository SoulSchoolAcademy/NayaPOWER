# Backlog Triage — 36 CANDIDATE rows (2026-10-09)

Triage by Learning Builder B. Supabase read-only; no rows touched.
Disposition requires Shawn's per-statement DB approval (statements below, NOT executed).

## Group A — 13 rows, target_id = 'NAYA-NODE-0001' (2026-09-28 → 2026-10-07)

Independent doer+scorer analysis, 2026-10-09: **0 of 13 verifiable as designed**
(1 definitional tautology, 4 honest nulls, 5 non-experiments, 3 definitional
token changes). Named examples:
- `de0b794b` — treatment "applied the lesson", control did not. No named task,
  no external outcome, no falsifiable criterion. INCONCLUSIVE; redesign required.
- `367a6ae3` — both arms returned `REQUIRE_DIRECT_CANONICAL_INTELLIGENCE`,
  `behavioral_change: false`. INCONCLUSIVE as verification; NOT SUPPORTED.

**Disposition: RETIRE.** Every row fails the admission contract
(`tools/learning_admission_gate.py`): no falsifiable experimental contract at
capture. Verification cannot be bolted on afterwards.

## Group B — 23 rows, target_id LIKE 'smart-note:%' (2026-10-07 → 2026-10-08)

provenance=USER, verification_method=PENDING_OUTCOME_VERIFICATION,
source=v7-smart-note-canonical. Claims: "Almost there", "Should work now",
"Getting closer", "Testing again", "End-to-end proof that the deployed capture
chain works", "Coda 1 capture-proof run", …

**Disposition: RETIRE.** These are chain-test utterances swept into the
candidate table during a capture-chain testing session — not falsifiable
learning claims. They fail every admission rule (no falsifiable claim, no
named task, no pre-registered criterion, no measurement design). Proven:
`tests/test_learning_admission_gate.py::test_chain_test_artifact_rejected`.

Note on the Verification Law: retiring the CANDIDATE classification does not
touch the underlying smart notes. If any utterance was a Shawn-directed
"smart note this" capture, the instant-activation path (Builder A's lane)
applies to the note itself — a learning-experiment candidacy that was never
designed is a separate classification, and it is that classification being
retired. Retirement is a status change only; fully reversible.

## Prepared statements (NOT executed — awaiting Shawn's word)

```sql
-- Statement 1: retire the 13 unverifiable NAYA-NODE-0001 candidates (hits exactly 13 rows)
UPDATE learning_evidence
SET status = 'RETIRED',
    observed_value = coalesce(observed_value, '{}'::jsonb) || '{"retirement_reason": "Fails admission contract: no falsifiable experimental contract at capture (independent analysis 2026-10-09: 0/13 verifiable as designed)", "retired_by": "learning-admission-law"}'::jsonb
WHERE status = 'CANDIDATE' AND target_id = 'NAYA-NODE-0001';

-- Statement 2: retire the 23 chain-test artifacts (hits exactly 23 rows)
UPDATE learning_evidence
SET status = 'RETIRED',
    observed_value = coalesce(observed_value, '{}'::jsonb) || '{"retirement_reason": "Chain-test artifact, not a falsifiable learning claim; fails all admission rules", "retired_by": "learning-admission-law"}'::jsonb
WHERE status = 'CANDIDATE' AND target_id LIKE 'smart-note:%';
```

Row-count verification (read-only, 2026-10-09): Statement 1 matches 13 rows,
Statement 2 matches 23 rows, total 36 = all current CANDIDATE rows. No ACTIVE
row is touched by either statement.

## Queue state after triage

Empty. All 36 backlog rows retire; the verification queue
(`BRAIN/07-LEARNING/VERIFICATION-QUEUE/queue.json`) starts clean. New
candidates enter only through the admission gate, then enqueue with a 48h SLA.
