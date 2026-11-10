# SN-2632: The Supabase Audit — 6 Out of 10, and the One Open Door

## Hook
Supabase is the live memory of NayaNET — and the audit counted everything: 21 functions, 97 tables, 187,175 rows. It is not 10 out of 10 yet, and the reason is one open door anyone can walk through.

## Nutshell
The engine runs and the data flows: all 21 edge functions are live, the notes sync is current to today, and the archive lock from October still holds. But six tables have no lock on the door at all — including the seat-keys table, which anyone holding the public key can read and rewrite — the search engine was never deployed, the citizen-pages table still does not exist, and no daily report has landed in 18 days. Score: 6 out of 10. The full audit is filed at TEAM-NITRO/SUPABASE-AUDIT-20261110.md.

## Human
Think of Supabase as the house where NayaNET keeps everything it remembers: every Smart Note, every mail message, every click, every ledger entry. The audit walked every room and counted what is in it. Most rooms are locked. Six are not — and one of those rooms holds the keys to the house. The search engine, the one thing that would let you ask Naya a question and get an answer from everything she knows, was built but never switched on. And the table where a new citizen's page would be written does not exist yet, so the walkthrough collects answers with nowhere to put them.

## Child
Supabase is like a big school where all of Naya's memories live in different classrooms. Almost every classroom has a locked door. But six classrooms have no lock at all, and one of them keeps the spare keys! Also, the library's search machine was built but never plugged in, and the classroom for new students' pages was never built. So the school works, but it is not finished or fully safe yet.

## Grandma
Dear, the computer system that remembers everything for Naya was checked from top to bottom today. It is working well — all the notes and letters are safe and up to date. But a few cupboard doors were found unlocked, including the one where the spare keys are kept, so those need locking straight away. And two things that were promised are still missing: the clever search that finds any note you ask for, and the place where a new person's page gets written. Nothing is lost — it just needs finishing.

## Naya
**What I learned:** an audit that only checks the tables someone named will miss the tables nobody named — the November 3 inventory checked 15 tables and found the system healthy; this audit checked all 97 and found the open door. Count everything, every time; the list scrolls, and what scrolls past is where the gap lives.
**How it applies:** before any "healthy" verdict, enumerate the full surface from the live system (Management API list, `pg_tables`), not from a remembered list. A partial inventory is a claim, not a measurement.
**Score:** 6/10 — healthy bones, one open door, two missing pieces. The fixes are named by hand in the audit: Shawn holds the locks (RLS, grants, the pages table, the service-key report run); a seat deploys the search engine and dedupes the notes once the delete grant lands.
