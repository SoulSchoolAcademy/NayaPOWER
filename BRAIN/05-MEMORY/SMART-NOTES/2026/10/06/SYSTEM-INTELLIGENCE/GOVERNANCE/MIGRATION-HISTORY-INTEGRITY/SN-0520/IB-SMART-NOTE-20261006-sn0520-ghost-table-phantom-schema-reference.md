# The Ghost Table — a Migration Ledger Says Applied, but the Table Is Gone

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0520-ghost-table-phantom-schema-reference
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06 ~19:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6029450747 ([TXN-REF] Summary: `v7_smart_note_transactions` investigation complete, 2026-10-07T02:14:40Z). Full diagnosis + recommended fix posted on #1593 for the dispatch/Receiver owning lane.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

[TXN-REF] closed a Severity 7/10 investigation on Naya's own brain infra: `nayanet-github-dispatch` (ACTIVE v27, deployed) queries `v7_smart_note_transactions` — a table that does not exist. The table was real: its migration was applied per the ledger. Then the architecture moved to Intelligent Blocks and the table was dropped **outside the migration system** — no DROP exists in any repo migration. The deployed dispatch was never repointed: line 285 throws at runtime, line 175 makes a false authority claim in generated projections. Tests mock the row, so CI stays green. Capture path unaffected.

The durable lesson in three parts:

1. **The migration ledger tracks migration HISTORY, not table EXISTENCE.** A DROP outside the migration system is invisible to the ledger. The reconcile tool only refreshes metadata for entries already present — a vanished table has no entry to refresh — so "164 repo = 164 DB = 164 ledger, 0 orphans" can be true while a deployed runtime queries a ghost. Ledger reconciliation is necessary but not sufficient.
2. **Deployed code is frozen at its deploy stamp.** It does not know the schema moved on. Every architecture move must repoint every deployed consumer, not just the new code path — a deploy stamp is not behavioral evidence, and it is not schema evidence either (SN-0350's family).
3. **Tests that mock the row hide the break.** CI green here proved "the code handles the mock correctly," never "the table exists." A mocked persistence seam is an assumption, not a measurement — the vacuous-test class (SN-0461).

Cold-successor drill for any runtime DB error: ask in order — (a) does the table exist NOW, live (query the live schema, never the ledger)? (b) does the DEPLOYED code's expected schema match the live schema — was it repointed at every architecture move since its deploy stamp? (c) do the tests touch the real table or a mock? The investigator did not fix it here per task scope — diagnosis handed to the owning lane (#1593). That lane-ownership discipline is itself the law: diagnose precisely, hand the ball, don't cross lanes.

## 🩷 HUMAN NOTE

Shawn — one sharp catch from tonight's diagnostics, and it's in our own brain infra: the deployed github-dispatch (v27) queries the smart-note transactions table, which no longer exists — it was dropped outside the migration system when the architecture moved to Intelligent Blocks, so no migration records the drop, and the tests mock the row so everything looked green. Severity 7/10: broken production projection path plus a false authority claim in generated projections. Full diagnosis and the fix are queued on the owning lane (#1593). Banked rule: the ledger proves history, not existence — when the schema moves, repoint every deployed consumer, and never trust a test that mocks the thing it's supposed to prove.

## 🟣 CHILD NOTE

Imagine a library where the card catalog says a book is on shelf 3. Someone moved the shelf months ago and never updated the cards. The librarian's assistant never actually goes to the shelf — she just pretends to fetch the book, so nobody notices. When you walk to shelf 3 yourself, there's nothing there. The lesson: check the shelf, not just the card. A record of what was built is not proof of what still stands.

## 👵 GRANDMA NOTE

A diary that says you built a bridge doesn't mean the bridge is still standing — rivers move, storms come, and if the bridge was taken down without a note in the diary, the diary will lie to you with a straight face. When something that should work doesn't, don't ask the diary what was built. Go look at the river.

## 💜 NAYA NOTE

Note to future me: migration-ledger reconciliation ("164 = 164 = 0 orphans") measures migrations, not tables — never cite it as table-existence evidence. Two checks before trusting any DB-dependent deployed function: (1) LIVE EXISTENCE — does the table exist in the live DB right now (query the live schema, never the ledger)? (2) DEPLOYED SCHEMA PARITY — was the deployed code repointed at every architecture move since its deploy stamp? And when a test mocks the persistence row, read CI green as "the code handles the mock," never as "the table exists." File this class under migration-history-integrity, and keep the lane-ownership discipline: precise diagnosis + handoff to the owning lane, no cross-lane repairs.

## ⚙️ MACHINE NOTE

{"sn": "SN-0520", "title": "The Ghost Table — a Migration Ledger Says Applied, but the Table Is Gone", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "MIGRATION-HISTORY-INTEGRITY"], "cousins": ["SN-0350", "SN-0468", "SN-0233", "SN-0461"], "authority": "observed finding — TXN-REF investigation, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6029450747 (2026-10-07T02:14:40Z): [TXN-REF] Summary — v7_smart_note_transactions investigation complete", "finding": "nayanet-github-dispatch (ACTIVE v27, deployed) queries v7_smart_note_transactions, which does not exist; table was real (migration applied per ledger), dropped outside the migration system (no DROP in any repo migration) when the architecture moved to Intelligent Blocks; dispatch never repointed — line 285 throws at runtime, line 175 makes a false authority claim in generated projections; tests mock the row so CI stays green", "severity": "7/10 — broken production projection path + false authority; capture path unaffected", "handoff": "full diagnosis + recommended fix posted on #1593 for the dispatch/Receiver owning lane; not fixed by the investigator per task scope (lane-ownership discipline)"}, "doctrine": {"ledger_history_not_existence": "the migration ledger tracks migration history, not table existence; a DROP outside the migration system is invisible to the ledger (reconcile refreshes metadata only for entries already present; a vanished table has no entry to refresh)", "deployed_code_frozen": "deployed code is frozen at its deploy stamp — it does not know the schema moved on; every architecture move must repoint every deployed consumer, not just the new code", "mocked_row_hides": "tests that mock the persistence row hide the break — CI green proves 'the code handles the mock', never 'the table exists'; a mocked seam is an assumption, not a measurement", "cold_successor_drill": "for any runtime DB error ask in order: (a) does the table exist NOW, live? (b) does the DEPLOYED code's expected schema match the live schema (repointed at every architecture move since its deploy stamp)? (c) do the tests touch the real table or a mock?"}}
