# SN-4565 — Schema Packet — Stopped at Gate 1, Decision Owed to Shawn

**Category:** LAW — the apply stopped at Gate 1; the decision is his, not the machine's — 2026-11-21 ~13:11 MST

*Paired Naya Note: NN-20261121-schema-packet-stopped-at-gate-1-decision-owed — the verbatim record of the Gate 1 stop.*

**Filed:** SN-4565 — Intelligence Loop run 474, 2026-11-21. Apply coordinator's stop, ~13:11 MST, as recorded in the curated memory. Follows SN-4561 (his tap). Report: `~/workspace/team-nitro/dashboard/schema-packet-apply-20261121/GATE-1-REPORT.md`.

## In a Nutshell

Apply coordinator `20cf668f` STOPPED — chain is RED on production: `naya_notes.owner_id` missing, `object_links` 5 columns missing, alias-binding trigger blocked. Nothing applied, nothing written, production untouched. Baseline verified (ledger_entries 30 rows, LE-20261022-030, ed5fe433…). THE DEADLOCK: the repairs that close the red chain ARE filed on main, byte-identical (tip `dc7cbcba…`), but they only reach production through the deploy itself — under a literal "never dispatch while red," the check can never go green. The Preview step is the real chain test (preview failure = production untouched). DECISION OWED: (a) hold the stop — apply waits indefinitely; or (b) authorize the dispatch with Preview as the gate (`governed-supabase-production-deploy.yml`, confirm=DEPLOY, source_sha = main tip at dispatch; must time to a quiet tip — main moves every few minutes and the workflow fails closed on a HEAD race). TWO NEW FINDINGS: (1) Divergence 3 closed out-of-band — 4 columns appeared on production Nov 13–21 with NO migration recording them; live schema and recorded chain have drifted, route/actor unknown. (2) The governed pipeline runs on PUSH too, not just dispatch — latest run (44944437696) failed at step 3 on a HEAD race, never reached Supabase, production untouched.

## The Lesson

**SCHEMA PACKET — STOPPED AT GATE 1, DECISION OWED TO SHAWN (apply coordinator, 2026-11-21 ~13:11 MST):**

**THE STOP.** The chain is RED on production: `naya_notes.owner_id` missing, `object_links` 5 columns missing, alias-binding trigger blocked. The coordinator stopped. Nothing applied, nothing written, production untouched. The stop worked as designed — a red chain does not deploy.

**THE DEADLOCK.** The repairs that close the red chain ARE filed on main, byte-identical (tip `dc7cbcba…`) — but they only reach production through the deploy itself. Under a literal "never dispatch while red," the check can never go green: the deploy is blocked by the red it exists to fix. The Preview step is the real chain test (preview failure = production untouched) — the gate that can actually tell red from green before anything lands.

**THE DECISION, OWED TO HIM.** (a) Hold the stop — the apply waits indefinitely; or (b) authorize the dispatch with Preview as the gate (`governed-supabase-production-deploy.yml`, confirm=DEPLOY, source_sha = main tip at dispatch; must time to a quiet tip — main moves every few minutes and the workflow fails closed on a HEAD race). The machine does not choose. He does.

**FINDING 1 — DIVERGENCE 3 CLOSED OUT-OF-BAND.** 4 columns appeared on production Nov 13–21 with NO migration recording them; live schema and recorded chain have drifted, route/actor unknown. Somebody or something changed production outside the chain — and the chain does not know.

**FINDING 2 — THE PIPELINE RUNS ON PUSH TOO.** The governed pipeline runs on PUSH, not just dispatch — latest run (44944437696) failed at step 3 on a HEAD race, never reached Supabase, production untouched. A push can trip the pipeline the same way a dispatch can.

## Why It Matters

His tap (SN-4561) said "do it" — and the machine stopped at the first gate because the chain is red. Both are right: the tap authorizes the apply, the gate refuses a red deploy. The deadlock is the question neither the tap nor the gate can answer alone: when the fix for the red chain is the deploy itself, who decides the deploy goes? That decision is his — and it is owed, not assumed. Meanwhile the out-of-band drift is the deeper warning: production changed without a migration, so the chain's picture of production is already wrong in a way no gate can see.

## How to Use It

Bring him the decision: (a) hold the stop, or (b) authorize the dispatch with Preview as the gate, timed to a quiet tip. Do not dispatch while the decision is owed. Investigate the out-of-band drift (4 columns, Nov 13–21, route/actor unknown) and the push-triggered pipeline run — both belong in the record before the next apply.

## His Words, As Recorded

> "Apply coordinator 20cf668f STOPPED — chain is RED on production: naya_notes.owner_id missing, object_links 5 columns missing, alias-binding trigger blocked. Nothing applied, nothing written, production untouched."

— apply coordinator's stop, 2026-11-21 ~13:11 MST, as recorded in the curated memory. Report: `~/workspace/team-nitro/dashboard/schema-packet-apply-20261121/GATE-1-REPORT.md`.

## Owed from This Dictation

- Decision owed to Shawn: (a) hold the stop, or (b) authorize dispatch with Preview as the gate.
- Nothing applied; production untouched; baseline verified (30 rows, LE-20261022-030).
- Out-of-band drift (4 columns, Nov 13–21) — route/actor unknown, investigate.
- Governed pipeline runs on PUSH too — latest run failed at step 3 on a HEAD race.
