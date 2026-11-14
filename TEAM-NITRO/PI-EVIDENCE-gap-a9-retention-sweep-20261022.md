# PI EVIDENCE — gap-a9: Conversation retention sweep (ruled 21:26Z)

**Item:** `gap-a9` — Conversation retention sweep.
**What this file proves:** Shawn ruled the 7-day retention on 2026-10-22 21:26Z, and the sweep was built, proven, and scheduled the same night — pg_cron job `purge-expired-conversations`, daily 03:17 UTC, job ACTIVE re-verified via SQL, proof run deleted 2 threads / 2 messages with counts exactly at baseline.
**Source:** `~/memory/2026-10-22.md`. Quoted verbatim below, with line numbers. Filed to GitHub 2026-11-14 as the URL-kind proof for gap-a9; the record-kind proof already in state.json cites the same entries.

## 1. The ruling — line 3374

- 2026-10-22 ~21:26Z — **SHAWN'S HOUSEKEEPING RULE: CONVERSATIONS LIVE ABOUT A WEEK, THEN THE SYSTEM CLEARS THEM.** His words: 'we don't keep the conversations forever — they last like a week or something.' Form chosen (his principle, main seat's mechanics, stated to him): a Smart Mail conversation clears **7 days after its last message** — quiet conversations expire, active ones keep living (each new message restarts the week); thread AND its messages go together. This is a SYSTEM retention sweep, distinct from participant delete rights (own messages only per the 21:23Z ruling). Invites are NOT conversations — excluded (own lifecycle). Build dispatched same minute (agent 2f4acc02): database-side daily purge (public.purge_expired_conversations() + pg_cron if available; otherwise the function + an external caller), proof owed on three test threads (8-day-old dies, fresh survives, 6d23h survives), counts reconcile, zero collateral outside threads+messages. RUNNING at flush.

## 2. The sweep COMPLETE + PROVEN + SCHEDULED — line 3411

- 2026-10-22 ~21:30Z — **RETENTION SWEEP COMPLETE + PROVEN + SCHEDULED (agent 2f4acc02; supersedes this log's 21:26Z/21:29Z 'RUNNING' states):** pg_cron installed on project dahisasgpfvziswqvmvm; function public.purge_expired_conversations() (privileged-only, EXECUTE revoked from public/anon/authenticated; last activity = coalesce(max message created_at, thread created_at)); cron job 'purge-expired-conversations' daily 03:17 UTC — main seat re-verified job ACTIVE via SQL, counts 359/6/6. Proof run: deleted_threads=2, deleted_messages=2 — test OLD (8d, 2 msgs) + EMPTY-OLD gone; EDGE (created 8d, last message 6d23h — activity reset the clock) + FRESH fully intact; final counts exactly baseline (hub_smart_notes 359 · threads 6 · messages 6 · invites 4 · auth.users 7,500). Real-world: the two oldest real threads (last activity 2026-10-16 07:26Z) cross the 7-day line 2026-10-23 ~07:26Z and clear on the 2026-10-24 03:17Z run. Shawn told 21:30Z.

## Filing note (Vera, VERIFY, 2026-11-14)

Read first-hand from the daily log. No GitHub twin exists for this record (`purge`/`retention` = 0 paths on main) — this file IS the public copy, quoted verbatim, not paraphrased.
