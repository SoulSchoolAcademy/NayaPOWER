# OPERATIONS — Git / Issues / Handoffs / Deployment

## Git
GitHub is the durable engineering and institutional-memory surface. The default branch is the engineering source of truth unless canonical project state says otherwise.

## Issues
Preferred relay: SIGN-IN → READ CURRENT STATE → DECLARE ACTION → EXECUTE → UPDATE → EVIDENCE → BLOCKER/RESULT → SIGN-OUT

## Handoffs
Leave identity, authority, current state, evidence, unresolved items and exact next action so another Naya can continue without replaying the conversation.

## Worker contract
Consequential delegated work follows `../NAYA-UNIVERSAL-WORKER-PROTOCOL-V1.md`. A worker report is not proof: use WORKER → EVIDENCE → VERIFIER → SCORE → ACCEPT/REJECT, with the level of independence proportional to consequence. Machine-readable briefs use `../../.naya/specifications/NAYA-WORKER-CONTRACT-V1.schema.json`.

## Deployment
Deployment is not proof. Do not deploy around a failing proof. Production claims require production evidence.

## Credentials
Basic activation should work without a personal Supabase access token. Additional infrastructure is connected only when required, authorized and supported.
