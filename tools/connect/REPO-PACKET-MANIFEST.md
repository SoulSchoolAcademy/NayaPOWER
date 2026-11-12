# Repo packet — Citizen API v1, v4 (PR-ready, NOT PUSHED)

**Status: PREPARED ONLY.** This manifest is the landing packet for
Resolve's 10x item 10. It is NOT pushed to GitHub in this turn.
Pushing needs: Shawn's tap to push as a branch + PR, and a
different-seat review at the exact head before any merge. Power
never self-merges. A push without that trail would violate the
same rule Resolve cited for item 10.

## Files in the packet (workspace, production/)
- citizen-api.js — v4 handler (v3 adopted + E2-E9)
- test-production.mjs — v4 suite, all passed in Node (see SCORECARD Loop 7)
- migration-citizen-api.sql — v3 + v4 idempotency table
- supabase-adapter-NOTES.md — adapter duties, updated for v4
- REPO-PACKET-MANIFEST.md — this file

## Companion files (workspace, connect-nayanet/)
- DECISIONS.md (D1-D6), SCORECARD.md (Loops 1-7),
  api-spec-v1-DRAFT.md, connect-sheet-DRAFT.md,
  NITRO-REVIEW-PACKET.md, FORK-VERIFICATION-NOTES.md,
  FORK-ISOLATION-TEST-PLAN.md, PIECE-1-HARVEST-NOTES.md

## PR description (proposed, for the PR body)
Citizen API v1: Allow-first, key fallback, fork path (owner, unproven
until isolation test). Hash-only secrets, token families with reuse
detection (refined), PKCE mandatory at authorize, redirect exact-match,
session-gated issuance, ledger events, idempotent notes, connections
inventory, aggregate usage, purge rules. NOT deployed, NOT live,
checkout test-mode only, no mail ops, no Smart Mail privacy claims.
Owed after this PR, before live: Deno smoke, real Hub sign-in wiring,
Nitro rendered review desktop+phone, real Allow with fresh Muse,
fork isolation, Shawn go-live tap.

## Review checklist for the different seat
- [ ] Run test-production.mjs unchanged, confirm all pass
- [ ] Run an independent probe past the test horizon (second replay,
      older generation, idempotency conflict, throttle, purge)
- [ ] Confirm migration applies to a clean schema (family, gen,
      revoke_reason, replays, idempotency table present)
- [ ] Confirm no secrets, no hashes, no bodies in events or logs
- [ ] Confirm redirect URI is the confirmed Hub address before merge
