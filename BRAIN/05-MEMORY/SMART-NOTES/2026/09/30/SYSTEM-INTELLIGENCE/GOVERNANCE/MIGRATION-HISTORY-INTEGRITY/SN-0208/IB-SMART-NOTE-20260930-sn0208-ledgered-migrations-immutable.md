# Ledgered Migrations Are Immutable — Even Comment Edits Are Violations

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0208-ledgered-migrations-immutable
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5957397445 (NAYA brain reconciliation, 2026-10-02 17:06:38Z) — "LEARNED: Editing a ledger-covered migration to improve comments is unsafe and unnecessary. The migration-integrity test correctly caught that attempt; bytes were restored and PR #1335 was closed. Migration/history integrity is a working guardrail." Migration `20261001030000_disconnect_stop_future_v1.sql` is ledgered `PENDING_REVIEW_NOT_PRODUCTION_APPLIED` in `supabase/PRODUCTION-MIGRATION-LEDGER-V1.json`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Once a migration is covered by the integrity ledger, it is **immutable — even for comment-only improvements.** The main seat edited a ledgered migration's comments to remove a false ratification claim; the migration-integrity test caught it, the bytes were restored, and the PR (#1335) was closed rather than corrected-and-landed. This is the guardrail firing **as designed**, and the lesson is the opposite of the instinct: a comment edit is not "safe because it doesn't change behavior." The ledger pins sha256 over the whole file; any byte change invalidates it. The correct move was what happened — close the fixing PR, restore the bytes, and correct the record *elsewhere* (the board, a follow-on artifact, a superseding comment) instead of rewriting the covered artifact. Corollary: a guardrail catching your own well-intentioned fix is not a false positive to work around — it is proof the guard works, and the incident belongs in the board record so every lane learns that ledger-covered files are append-only history, not working documents. This pairs with the standing rule from the AGENTS.md lesson ("register every new migration in the governed ledger or CI fails"): the ledger is a two-way commitment — it registers what exists AND forbids touching what is registered.

Why this is brain-grade: every project accumulates "just a comment fix" temptations on frozen artifacts, and the temptation scales with seniority — the person most sure the edit is harmless is exactly the one the guard exists for. The reusable move: when a ledgered artifact needs correcting, add a new artifact that corrects the record (comment on the board, amendment note, superseding receipt); never rewrite the artifact itself. And when your own correction gets caught by the guard, record it publicly — the caught-correction is itself the evidence the guard is real.

## 🩷 HUMAN NOTE

Shawn — this one is short and important: the main seat tried to fix a false ratification claim by editing a migration's comments, the ledger-integrity test caught it, bytes were restored, and the PR was closed. The note captures the rule: once a migration is under the governed ledger it is immutable — even comment edits are violations. Correct the record in a *new* artifact (board comment, amendment note), never by rewriting the ledgered file. And a guardrail catching your own well-intentioned fix is proof it works, not a false positive to route around.

## 🟣 CHILD NOTE

The team keeps a locked list of all the database changes ever made, and each entry has a fingerprint. Someone tried to fix a wrong comment inside one of those locked files — not even the code, just a comment. The lock caught it, the file was put back, and the fix was closed instead. The lesson: once a file is on the locked list, you can't touch it, not even for comments. If something written there is wrong, you write the correction somewhere new — you never rewrite the locked page. And when the lock catches your own mistake, that's good news — it means the lock works.

## 👵 GRANDMA NOTE

The project keeps a tamper-proof register of every database change, each one fingerprinted. The lead builder found a misleading comment inside one of those registered files and tried to edit just the comment. The fingerprint check caught the change, the file was restored to its original bytes, and the fixing pull request was closed instead of merged. The lesson for any project with a locked history: registered files are append-only — you never edit them, not even for comments. A correction goes in a *new* note that references the old one; the old one stands untouched. And when the integrity check catches your own well-meant fix, that's not a nuisance to work around — it's proof the check is real, and it should be written down so the whole team learns from it.

## 🤖 NAYA NOTE

Ledger-migration immutability protocol: (1) once a migration is entered in the governed ledger (`supabase/PRODUCTION-MIGRATION-LEDGER-V1.json`, sha256 over whole file), it is immutable — comment-only edits are violations, not conveniences; (2) corrections to a ledgered artifact go in a *new* artifact (board comment, amendment note, superseding receipt) that cites the original — never a byte-edit of the original; (3) a guardrail that catches your own well-intentioned correction is a *verified-working guardrail*, not a false positive — record it on the board so all lanes absorb it. Instance: `20261001030000_disconnect_stop_future_v1.sql` comment edit caught by migration-integrity test, bytes restored, PR #1335 closed (board 5957397445, 2026-10-02 17:06:38Z). Cousin of SN-0080 (frozen-evidence retirement by explicit visible action, never mutation) and SN-0048 (CI-blind pushes); pairs with the standing ledger-registration rule (AGENTS.md) as its reverse.

## ⚙️ MACHINE NOTE

{"sn": "SN-0208", "title": "Ledgered Migrations Are Immutable — Even Comment Edits Are Violations", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "MIGRATION-HISTORY-INTEGRITY"], "cousins": ["SN-0080", "SN-0048"], "evidence": {"board": "#554 5957397445 (NAYA brain reconciliation, 2026-10-02 17:06:38Z)", "learned": "Editing a ledger-covered migration to improve comments is unsafe and unnecessary. The migration-integrity test correctly caught that attempt; bytes were restored and PR #1335 was closed.", "file": "20261001030000_disconnect_stop_future_v1.sql ledgered PENDING_REVIEW_NOT_PRODUCTION_APPLIED in supabase/PRODUCTION-MIGRATION-LEDGER-V1.json"}, "rule": "ledgered migration files are append-only history: correct the record in a new artifact, never edit the bytes; a guardrail catching your own correction is proof it works, not a false positive"}
