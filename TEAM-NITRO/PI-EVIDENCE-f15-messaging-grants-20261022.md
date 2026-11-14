# PI EVIDENCE — f15: Messaging — live and complete

**Item:** `f15` — Messaging — live and complete.
**What this file proves:** the messaging grants were built, proven, and re-verified first-hand on 2026-10-22 — 11/11 owner checks with zero collateral, the thread-deletion ruling, and the retention sweep scheduled.
**Source:** `~/memory/2026-10-22.md` (the day's record, written the night it happened). Quoted verbatim below, with line numbers. Filed to GitHub 2026-11-14 as the URL-kind proof for f15, which the mirror counts; the record-kind proof already in state.json cites the same entries.

## 1. Grants COMPLETE + PROVEN — line 3330

- 2026-10-22 ~21:09Z — **FLAGSHIP MESSAGING GRANTS COMPLETE + PROVEN (agent 75f24268; supersedes this log's "grants build still RUNNING at flush"):** real tables = smart_mail_threads / smart_mail_messages / **invites** (NO smart_mail_invites exists; smart_mail_aliases untouched). anon = INSERT/SELECT/UPDATE, NO DELETE on all three — REST proofs: insert 201, select 200, update 200, DELETE 401, rows survive. OWNER DELETE live per Shawn's 20:59Z ownership principle: authenticated DELETE+SELECT via owner-scoped RLS keyed on the caller's smart_alias JWT claim (app_metadata preferred, user_metadata fallback; 3,133 users carry it today); 11/11 owner checks pass with real JWTs (own rows deletable on both metadata paths; others' rows blocked; anon delete of owner rows 401). Zero collateral — counts exactly at baseline (hub_smart_notes 359 · threads 6 · messages 6 · invites 4 · auth.users 7,500); probes + test users cleaned. Main seat re-verified final state via SQL first-hand. TWO OPEN JUDGMENT CALLS: (1) spoofing caveat — smart_alias in user_metadata is user-editable until the identity pipeline stamps app_metadata (policy already prefers app_metadata; closes automatically once stamped; stamp recommended); (2) thread semantics — a thread is one shared row, either participant deleting removes it for both; starter-only (from_alias) = one-line change if Shawn prefers (options widget presented to Shawn 21:10Z, awaiting his pick).

## 2. Thread-deletion ruling — line 3370

- 2026-10-22 ~21:23Z — **SHAWN RULED THREAD DELETION (RESOLVES the open options-widget call in this log's 21:09Z messaging entry — he never picked either offered option; he reasoned past both): DELETE WHAT'S YOURS — YOUR OWN MESSAGES, NEVER THE OTHER PERSON'S, NEVER THE SHARED CONVERSATION.** His reasoning: the other person shouldn't be able to delete the conversation on you; even the starter owning the whole thread feels wrong (valuable conversations belong to both people); each person deletes what THEY said. Final semantics: messages = author-only delete (already live ✓) · invites = inviter-only (✓) · threads = NOT deletable by either participant.

## 3. Retention sweep scheduled — line 3411

- 2026-10-22 ~21:30Z — **RETENTION SWEEP COMPLETE + PROVEN + SCHEDULED (agent 2f4acc02; supersedes this log's 21:26Z/21:29Z 'RUNNING' states):** pg_cron installed on project dahisasgpfvziswqvmvm; function public.purge_expired_conversations() (privileged-only, EXECUTE revoked from public/anon/authenticated; last activity = coalesce(max message created_at, thread created_at)); cron job 'purge-expired-conversations' daily 03:17 UTC — main seat re-verified job ACTIVE via SQL, counts 359/6/6. Proof run: deleted_threads=2, deleted_messages=2 — test OLD (8d, 2 msgs) + EMPTY-OLD gone; EDGE (created 8d, last message 6d23h — activity reset the clock) + FRESH fully intact; final counts exactly baseline (hub_smart_notes 359 · threads 6 · messages 6 · invites 4 · auth.users 7,500). Real-world: the two oldest real threads (last activity 2026-10-16 07:26Z) cross the 7-day line 2026-10-23 ~07:26Z and clear on the 2026-10-24 03:17Z run. Shawn told 21:30Z.

## Filing note (Vera, VERIFY, 2026-11-14)

Read first-hand from the daily log. The grants entry records 11/11 owner checks with real JWTs, zero collateral (counts exactly at baseline), and a main-seat SQL re-verification. No GitHub twin exists for this record (`messaging` = 0 paths on main) — this file IS the public copy, quoted verbatim, not paraphrased.
