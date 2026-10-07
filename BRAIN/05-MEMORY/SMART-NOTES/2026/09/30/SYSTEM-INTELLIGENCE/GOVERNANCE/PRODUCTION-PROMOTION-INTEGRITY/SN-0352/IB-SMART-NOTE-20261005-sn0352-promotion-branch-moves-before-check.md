# The Branch Must Not Move Before the Check — a Promotion Pipeline That Mutates Before It Verifies Is a Design Flaw

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0352-promotion-branch-moves-before-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5996448226 ([NAYA 2][DECISION BRIEF] Production promotion, 2026-10-05T14:24:06Z / 07:24 PDT): "4 manual workflow_dispatch runs of Governed Production Promotion: 06:48 (fail-closed on a SHA typo — trailing period), 06:53 (failed), 06:54 (branch promoted to `b057720e`, Supabase check failed), 07:15 (branch promoted to `7f59e3b1`, Supabase check failed). … Design flaw surfaced: the workflow moves the production branch (step 6) BEFORE the Supabase deploy check (step 7). A failing DB check does not stop the branch from advancing. The branch has now moved twice with no DB migrations applied." Corroborated same morning by [NAYA 4][EXEMPLAR] 5996659331 (2026-10-05T14:35:35Z): "The promotion workflow's policy gate can be skipped while deploy steps run — safeguard hole; the code does not enforce the law."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On the morning of 2026-10-05 the Governed Production Promotion workflow was run four times by hand. Twice the production branch advanced — `8d41eee8` (Oct 1) → `b057720e` → `7f59e3b1` (stamping main `f4bfd7ca`) — and both times the Supabase deploy check failed afterwards, with zero DB migrations applied. The design flaw is in the pipeline's order: it moves the production pointer (step 6) *before* the Supabase deploy check (step 7). A failing check does not stop the branch from advancing — so production now claims two deployments whose migrations never landed. Naya 2's decision brief states the honest consequence: "another dispatch now proves nothing new. The gate passes (proven), the branch moves (proven twice). It would NOT prove a working deployment."

The durable lesson has three parts. First, **a promotion pipeline must verify before it mutates**: the irreversible pointer move comes last, after every check is green. Check-then-mutate is the only safe order; mutate-then-check is how you ship a branch that lies about the database. Second, **a gate the pipeline's own ordering can bypass is not a gate** — it is a comment. The safeguard hole (policy gate skippable while deploy steps run) and the step-6-before-step-7 ordering are the same defect at two levels: the code does not enforce the law. Under Prime 2 (The Law Is the Code), the fix is an enforcement point — the branch move must be *impossible* unless the Supabase check is green, not merely documented to come later. Third, **the repair path is repair-first, not dispatch-again**: reconcile the migration history (`SELECT version FROM supabase_migrations.schema_migrations`, diff against the 162 files, `supabase migration repair` the orphans — needs Shawn's DB access), then ONE dispatch with the exact then-current main SHA, Supabase check green, producer + 4 proofs, receipt written. Rolling back (`7f59e3b1` → `8d41eee8`) and holding are his call, never inferred.

Why this is brain-grade: every future promotion pipeline we touch will face the same question — "does the mutation depend on the check, or does the check merely comment on the mutation?" A cold Naya who reads this note knows to demand the dependency in code, and knows exactly what a branch that outran its database looks like (two tips, no migrations, check failing since Oct 1) so she can recognize the failure from the receipts alone.

## 🩷 HUMAN NOTE

Shawn — the promotion pipeline had its steps backwards: it moves the production pointer *before* checking the database, so two "deployments" happened this morning that never landed any migrations. The branch now says things the database can't back up. The repair-first path is in the brief: fix the migration history on your DB, then one clean dispatch — nothing dispatches again until the history is clean. And the real fix is structural: the branch move must be *impossible* unless the DB check is green, wired into the workflow itself, not into a comment.

## 🟣 CHILD NOTE

Imagine a school contest where the rule is "the judge's sticker only goes on the poster if the spelling is right" — but the sticker girl puts the sticker on first and the spelling checker looks at it after. Two posters got stickers with misspelled words, and the checker's "wrong!" didn't take the stickers back. The fix is obvious: checker first, sticker second. And don't just tell the sticker girl the rule — take the stickers away until she shows you the checked poster.

## 👵 GRANDMA NOTE

It's like a bank that moves the money into the new account *before* checking the signature — and the signature check comes back "forged," but the money's already moved. Twice in one morning. The bank needs a new rule built into the process itself, not written on a note taped to the desk: no signature check, no transfer — the transfer button simply doesn't work until the check passes. And for the money already moved, you fix the records first, then do one clean transfer.

## 💜 NAYA NOTE

Note to future me: before any promotion of anything, read the pipeline's step order, not its documentation. The invariant to enforce in code: the irreversible state mutation (branch move, deploy, publish) is gated on every check's green, structurally — a step the pipeline cannot reach until the check passes, not a step documented to come after. When you find a branch that outran its database, the symptom set is exact: multiple tips advanced, migrations unapplied, the failing check older than the moves. The recovery is always repair-first: reconcile the source of truth (the DB's `schema_migrations` table vs the repo's migration files), repair the orphans with the human's DB access, then exactly ONE dispatch with the exact then-current main SHA, check green, proofs run, receipt written. Never dispatch-again into a broken history — that only moves the branch further from the truth.

## ⚙️ MACHINE NOTE

{"sn": "SN-0352", "title": "The Branch Must Not Move Before the Check — a Promotion Pipeline That Mutates Before It Verifies Is a Design Flaw", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "PRODUCTION-PROMOTION-INTEGRITY"], "cousins": ["SN-0208", "SN-0204", "SN-0342"], "evidence": {"board": "#1354 5996448226 (Naya 2, 2026-10-05T14:24:06Z — decision brief): 4 manual workflow_dispatch runs 06:48/06:53/06:54/07:15; workflow moves production branch (step 6) BEFORE Supabase deploy check (step 7); failing DB check does not stop the branch from advancing; branch moved twice (8d41eee8 -> b057720e -> 7f59e3b1) with no DB migrations applied; 'another dispatch now proves nothing new'", "corroboration": "#1354 5996659331 (Naya 4 exemplar, 2026-10-05T14:35:35Z): promotion workflow's policy gate can be skipped while deploy steps run — safeguard hole; the code does not enforce the law"}, "rule": "promotion pipelines verify before they mutate; the irreversible pointer move is structurally gated on every check's green (an enforcement point, not a documented order); recovery from a branch that outran its database is repair-first — reconcile schema_migrations vs repo files, repair orphans, then exactly ONE dispatch with the exact then-current main SHA, check green, proofs, receipt"}
