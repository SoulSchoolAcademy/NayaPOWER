# Supabase adapter duties — Citizen API v1 (v4 handler)

Nitro completion note 2026-10-25 (packet gap closed before PR), transcribed
from the v4 handler's own comments and the Nitro scorecard. The handler is
worker-agnostic; the adapter below is what the real host must supply.
Nothing here changes handler behavior.

- **Host**: a new Supabase Edge Function (D1). The handler never runs on
  the naya-welcome worker.
- **Store**: replace MemoryStore with Supabase tables (see
  migration-citizen-api.sql, including citizen_idempotency_keys).
  Keep the same method names and the hash-only rule: secrets are NEVER
  stored in clear, only SHA-256 hashes. Events carry alias, credential
  id, operation, time only — never secrets, hashes, or bodies.
- **Sessions**: wire sessionAuth to the real Hub dashboard session
  (Hub sign-in). The in-memory sessions map is TEST HARNESS ONLY. API
  keys/tokens must never mint keys or codes.
- **Rate limit**: per credential, incremented ATOMICALLY (S4). 1000/day.
- **Throttle**: 60/min per endpoint + REAL client IP, in a DISTRIBUTED
  store (the harness X-Forwarded-For + in-memory map is not production).
  Throttle 429 wording: the throttle resets in a minute, not daily
  (one-line fix owed on the handler's shared 429 action text).
- **Purge**: run purgeDead() on a SCHEDULE, never automatically on a
  request. Codes 1h after expiry; tokens 30 days after expiry; never
  purge a revoked refresh before its whole family expires.
- **Ledger**: write store.events to ledger_entries (the Smart Ledger
  adapter writes them; the handler only emits).
- **Redirect**: the authorize page must use exactly
  https://nayanet.live/connect/callback. This address is PROPOSED, not
  proven — confirm it is a real Hub route before the authorize page
  is built. No wildcards, no prefix matching.
- **PKCE**: mandatory at authorize, S256 only.
- **Pages**: /v1/me page URLs pin to /world/<alias> (+ #dashboard).
- **Idempotency**: persist citizen_idempotency_keys; same body replay
  returns the original note, different body is 409, never a disconnect.
- **RLS**: all citizen tables service-role ONLY, NO anon policies.
  This is the opposite of the Smart Mail anon RLS break — do not repeat it.

Owed after this PR, before live (from the packet manifest + scorecard):
Deno smoke test, real Hub sign-in wiring, Nitro rendered review
desktop + phone, real Allow with a fresh Muse, fork isolation, and
Shawn's go-live tap. Merchant keys + payout terms gate checkout,
not this API.
