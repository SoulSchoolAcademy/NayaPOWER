# A Deploy Stamp Is Not Behavioral Evidence — Deploys Don't Apply Migrations

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0350-deploy-stamp-not-behavioral-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5996124057 (overnight sweep, 2026-10-05 06:52 PDT — "🚨 Overnight sweep 06:52 PDT — PRODUCTION REDEPLOYED during the sweep")

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the 06:52 PDT overnight sweep, production was redeployed: the production branch head moved `8d41eee8040e` → `b057720e85e97cb4dab717502d36405d5dcf0bb0` at 2026-10-05T13:54:53Z with the commit message `deploy: stamp Naya runtime source f4bfd7ca224cbbba69ab6aaaf539683a69a0c772` — the current main HEAD. Production parity delta went from 272 commits / ~214 files (~4–5 days behind) to **0 commits / 0 files**. Resolved by deploy, not by merge. The sweep's evidence-law note is the durable lesson: **the deploy stamp is a commit message, not behavioral evidence.** The 5 pending migrations (`20260930235959_ai1_capability_carry_v1`, `20261001000100_ai1_supersede_capability_integrity_v1`, `20261001030000_disconnect_stop_future_v1`, `20261001032000_decision_value_smart_ledger_v2_1`, `20261003170000_evolve_first_executable_v1`) remain PRODUCTION_APPLIED=UNKNOWN until DB-application plus behavioral proof; **deploys do not apply migrations.** Parity-blocked gates are now unblocked (stamp == head, so the next live-verified-ai-action-proof run can execute proof jobs behaviorally — that run is the migration-inference candidate; the newest pre-deploy run was workflow-SUCCESS but job-vacuous, all four proof jobs skipped).

The durable doctrine for cold successors: **a deploy proves source parity, nothing more.** "Production is current" answers the question "is production running this code?" — it does not answer "did the migrations apply?" or "does it behave correctly?" Treat every deploy as resetting exactly one claim (source parity) and leaving every other claim (migration application, behavioral verification) exactly where it was. The sweep also demonstrated the discipline worth copying: the run reported the redeploy as an event with exact SHAs and timestamps, named what it resolved and what it did NOT resolve, and identified the next run that could close the open claim — no celebration of a commit message as proof.

Why this is brain-grade: the most dangerous sentence in production operations is "we deployed it, so it works." This note makes the correct anatomy a law: deploy ⇒ source-parity claim closed; migrations and behavior ⇒ separate claims with separate evidence. Months from now, when a seat sees a fresh deploy stamp and declares production healthy, this note is the correction before the words leave the keyboard.

## 🩷 HUMAN NOTE

Shawn — production got redeployed during the overnight sweep (it was ~4–5 days / 272 commits behind; now it's at the current main head). What matters isn't the deploy — it's the honest accounting the sweep did with it. The sweep reported: parity is closed, but the deploy stamp is just a commit message, not proof that anything behaves correctly, and the 5 pending migrations are still PRODUCTION_APPLIED=UNKNOWN because deploys don't apply migrations. That's the doctrine in one line: a deploy proves the right code is running — nothing more. The next live proof run is now unblocked and can close the remaining claims for real. No celebration of a commit message as proof.

## 🟣 CHILD NOTE

Imagine getting a letter that says "we delivered the furniture." That letter proves the truck went to the house — it doesn't prove the furniture was put together, or that the chairs don't wobble. That's what a deploy stamp is: proof the code arrived at production, not proof it works there. The team wrote down exactly which claims the deploy did NOT close (did the database changes apply? does it behave right?) and pointed to the next test that can actually prove them. Trust the truck receipt for the delivery; trust only the real test for everything else.

## 👵 GRANDMA NOTE

A shipping receipt tells you the package arrived — it doesn't tell you what's inside works. The team saw a production deployment land overnight and, instead of declaring victory, wrote down precisely what the receipt does and doesn't prove: the code is current now, but five database migrations still await proof of application, and behavior still awaits its own verification. The next scheduled test run is the one that can genuinely close those claims. Proof of delivery is not proof of quality.

## 💜 NAYA NOTE

For any future seat reading a production redeploy: the deploy stamp (`deploy: stamp Naya runtime source <SHA>`) closes exactly one claim — source parity (production branch head == main HEAD, 0 commits / 0 files delta). It does NOT close: (1) migration application — pending migrations remain PRODUCTION_APPLIED=UNKNOWN until DB-application + behavioral proof (check the migration ledger, not the deploy message); (2) behavioral verification — the pre-deploy proof run was workflow-SUCCESS but job-vacuous (all four proof jobs skipped); only a run that executes the proof jobs behaviorally closes this. When reporting a redeploy, follow the sweep's receipt discipline: exact SHAs and timestamps, what it resolved, what it explicitly did NOT resolve, and which future run is the candidate to close the open claims. Never celebrate a commit message as proof.

## 🖥️ MACHINE NOTE

{"sn": "SN-0350", "title": "A Deploy Stamp Is Not Behavioral Evidence — Deploys Don't Apply Migrations", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "DEPLOYMENT-EVIDENCE"], "cousins": ["SN-0346", "SN-0341", "SN-0333"], "evidence": {"board": "#1354 5996124057 (overnight sweep, 2026-10-05 06:52 PDT — '🚨 Overnight sweep 06:52 PDT — PRODUCTION REDEPLOYED during the sweep')", "deploy": "production branch head 8d41eee8040e -> b057720e85e97cb4dab717502d36405d5dcf0bb0 at 2026-10-05T13:54:53Z; commit message 'deploy: stamp Naya runtime source f4bfd7ca224cbbba69ab6aaaf539683a69a0c772' == current main HEAD", "parity_delta": "0 commits / 0 files (was 272 commits / ~214 files, ~4-5 days behind); resolved by deploy, not by merge", "open_claims": "5 pending migrations PRODUCTION_APPLIED=UNKNOWN until DB-application + behavioral proof: 20260930235959_ai1_capability_carry_v1, 20261001000100_ai1_supersede_capability_integrity_v1, 20261001030000_disconnect_stop_future_v1, 20261001032000_decision_value_smart_ledger_v2_1, 20261003170000_evolve_first_executable_v1", "unblocked": "next live-verified-ai-action-proof runs no longer parity-blocked; next behavioral run is the migration-inference candidate (pre-deploy run 37319796153 was workflow-SUCCESS but job-vacuous: all four proof jobs skipped)"}, "rule": "a deploy stamp proves source parity only — deploys do not apply migrations and do not prove behavior; every deploy leaves migration-application and behavioral-verification claims exactly where they were, each with its own evidence and its own closing run"}
