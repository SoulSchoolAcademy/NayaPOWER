# SN-4574 — Supabase Filing Round — Complete, Checker Pass, Merged

**Category:** SUPABASE — the repo can almost rebuild the live database — 2026-11-21 ~13:27 MST

*Paired Naya Note: NN-20261121-supabase-filing-round-complete — the verbatim record of the completion.*

**Filed:** SN-4574 — Intelligence Loop run 475, 2026-11-21. Coordinator `3de2f6a4`, completed ~13:27 MST, as recorded in the curated memory. Branch `supabase/filing-20261121`, head `1fe638dc`, three clean merge commits. Lane: `~/workspace/team-nitro/supabase/filing-20261121/`.

## In a Nutshell

The biggest break from the Supabase inventory — the repo could not rebuild the live database — is now filed and merged: **143 filing units** (66 tables/views, 59 RPCs + 2 trigger fns + 2 drift corrections, +8 trigger helpers, +6 edge functions), checker PASS after three FAILs (11/11 triggers, 72/72 bodies byte-exact vs live, walk 1→11/11). The brief's "128" was wrong. `members` EXISTS live as a base table (settles M-15). Honest limit: no test-DB fresh apply was ever run — the one proof still owed before the rebuild is claimed proven end-to-end, now dispatched (coordinator `8cf19724`). DROP candidates (129 pieces) untouched — need Shawn's word.

## The Lesson

**SUPABASE FILING ROUND — COMPLETE, CHECKER PASS, MERGED (coordinator `3de2f6a4`, ~13:27 MST).** Branch `supabase/filing-20261121`, head `1fe638dc` (tree `21099866…`), created at main tip `56a90421`, three clean merge commits (tables `d3add794…`, functions `4804eae4…`, edge `1fe638dc…`). **FINAL TOTAL: 143 filing units** — 66 tables/views, 59 RPCs + 2 trigger fns + 2 drift corrections, +8 trigger helpers, +6 edge functions. The brief's "128" was wrong (mixed families, never included edge). Checker history: three FAILs then PASS (11/11 triggers, 72/72 bodies byte-exact vs live, walk 1→11/11). `members` EXISTS live as a base table (settles M-15). Dream-replay source recovered from git history and KEPT (filing ≠ deploying).

**HONEST LIMITS:** no test-DB fresh apply was ever run (out of scope; no local Postgres; live read-only) — a real fresh-apply run against a scratch project is the one proof still owed before the rebuild is claimed proven end-to-end; pgcrypto + `auth` schema unproven on a fresh project; two unowned sequences still unfiled; DROP candidates (129 pieces) untouched — need Shawn's word; nothing deleted or dropped; live was read-only throughout.

**FRESH-APPLY PROOF DISPATCHED (~13:27 MST, coordinator `8cf19724`)** to close the remaining proof.

## Why It Matters

The inventory's biggest break is closed on paper and in bytes: the repo now carries what live carries, byte-exact, checker-proven. What is still owed is the one proof that matters for the claim itself — a fresh apply against a scratch project — and it is dispatched, not assumed. And the DROP candidates stay untouched until Shawn's word — filing is not deleting. The "128" count is dead; 143 is the number.

## How to Use It

The rebuild claim stays unproven until the fresh-apply proof (coordinator `8cf19724`) lands. Do not claim the repo rebuilds live until then. Nothing is dropped without his word. The "128" count is never quoted again — 143 filing units.

## Owed from This Dictation

- Fresh-apply proof (coordinator `8cf19724`): real fresh apply against a scratch project, pgcrypto + `auth` schema proven.
- Two unowned sequences still unfiled.
- DROP candidates (129 pieces) — need Shawn's word before anything is dropped.
