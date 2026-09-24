# GitHub Webhook P2 — Replay / Idempotency Repair

**Date:** 2026-09-24
**Status:** IMPLEMENTED + PRODUCTION_SCHEMA_VERIFIED / LIVE_WEBHOOK_PROOF_BLOCKED
**Repository:** SoulSchoolAcademy/NayaPOWER

## Finding

P1 established a concrete causal defect in the existing six-argument `nayanet_record_cognition_event` overload used by the inbound GitHub webhook: the cognition row was de-duplicated by `(user_id, project_id, event_id)`, but each replay could still create a fresh execution receipt and advance project cognition state.

## Repair

Migration `20260924222644_harden_cognition_event_replay_idempotency_v1` preserves the existing canonical persistence seam and adds an exact replay branch after the existing advisory transaction lock:

- find the canonical event by `(user_id, project_id, event_id)`;
- if its canonical receipt exists, return the existing event/state/receipt with `replayed=true`;
- do not create a second receipt;
- do not advance project cognition state;
- do not introduce a second event store or authority model.

The normal first-seen path remains unchanged apart from returning `replayed=false`.

## Evidence

- Repository migration commit: `7451968c14f9285a43b6a61dfe971e5630d3e564`
- Production migration: `20260924222644 / harden_cognition_event_replay_idempotency_v1`
- Production function read-back: replay branch present after migration.
- Existing unique index: `nayanet_cognition_events_user_id_project_id_event_id_key`.
- Live webhook endpoint remains fail-closed at the external credential boundary: HTTP 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED`.

## Truth boundary

**The causal repair is production-applied and source-backed. The live GitHub signed positive/replay journey is still NOT VERIFIED because the production webhook secret is not configured.**

The repair therefore must not be promoted to LIVE VERIFIED webhook behavior yet.

## Remaining holes

1. Authorized operator must configure `GITHUB_WEBHOOK_SECRET` without exposing it to chat/source/logs.
2. Run controlled signed positive delivery.
3. Run exact duplicate delivery and prove same event/receipt identity with no state/receipt increment.
4. Independently retrieve persisted event/receipt after the HTTP response.
5. Prove valid webhook event cannot mint or substitute for `intelligence_commit` authority.
6. Prove installation/repository isolation; installation ID is not currently persisted by the receiver.

## Single next action

**Configure `GITHUB_WEBHOOK_SECRET` in the authorized production secret-management/admin boundary, then execute the controlled signed webhook positive → exact replay → independent persistence/retrieval → authority-separation proof.**
