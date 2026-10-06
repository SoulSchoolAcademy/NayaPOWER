-- IDEMPOTENCY STRUCTURAL ENFORCEMENT: duplicates become impossible at the database level.
--
-- Context (2026-10-06, Naya 4): 19 true duplicate receipt pairs found in
-- production nayanet_execution_receipts (same token_jti = same workflow
-- execution, content-identical, 0.3-2.1s apart). Root cause: idempotency_key
-- was NULL on all 1,603 rows — the column existed but no code populated it.
-- PR #1624 repairs the code path to populate the key on write.
--
-- This migration encodes Shawn's law — "there are never duplicates, we always
-- distill" — as a database constraint. The law is the constraint, not just
-- the code: no code path, retry storm, or future bug can write a duplicate
-- key once this index exists. Code populates; the database refuses.
--
-- Design: partial unique index on non-null keys only. Legacy NULL rows are
-- untouched (the 1,603 historical NULLs remain queryable; the 19 true
-- duplicates are removed by a separate director-gated dedup, not here).
-- Any future INSERT with an already-seen non-null idempotency_key fails
-- with a unique-violation instead of silently doubling the receipt.
--
-- Idempotent: IF NOT EXISTS — safe to re-run.

CREATE UNIQUE INDEX IF NOT EXISTS nayanet_execution_receipts_idempotency_key_uidx
  ON public.nayanet_execution_receipts (idempotency_key)
  WHERE idempotency_key IS NOT NULL;
