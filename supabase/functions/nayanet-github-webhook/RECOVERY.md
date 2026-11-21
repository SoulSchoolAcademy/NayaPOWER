# nayanet-github-webhook — source recovery record

Filed: 2026-11-21, Supabase filing round, Seat 3 (Edge Functions).
Branch: `supabase/filing-20261121-edge`. Status: **FILED (recovered source)**.

## What was recovered

`index.ts` in this directory is the file as it stood in repo history — byte-identical
to the source blob, verified by sha256 (see below). Nothing was invented, rewritten,
or reformatted.

- **Source commit:** `7f120a74828fffc2628a285ddb52d2f227281110`
  (2026-09-25T05:38:20Z) — "fix(sender): preserve renderable GitHub events for Hub Feed"
- **Source path then:** `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts`
  (not under `supabase/functions/` at that time)
- **Source blob sha:** `4d34eb233682b62cf4e40a53e2890bf78fab4ef9`
- **Size:** 6,160 B · **sha256:** `c03000ce254bcc36e3e865fc04ce649d7f6a7038ebf39c43b0d004db8a38d292`
- **History:** added `271c415a` (2026-09-18), hardened through Sep 24 (`da74234e`,
  `86c332bc`), last version `7f120a74` (2026-09-25). Removed from `main` by the
  reset commit `b31f37fd` (2026-09-27). Never re-added to `main` after the reset.
  The activation branches that carried it (`activation/awesome-code-boot-v1`,
  `activation/nine-node-wiring-v1`, per the Oct 20 black-box map) no longer exist
  as branches; the source survives only by commit SHA.
- **Known drift (from the Oct 20 investigation, still visible in this source):**
  the normalizer sets `metadata.source = "github_webhook"` but no top-level
  `source` on the event object, so the RPC's `p_event->>'source'` projection
  coalesces to `'nayanet-hub'` — a GitHub event is mislabelled hub-origin.
  One-line fix, NOT applied here: this filing recovers, it does not repair.

## What it does (read from the recovered source, not assumed)

POST only. Requires `x-github-delivery` and `x-hub-signature-256: sha256=<64 hex>`;
verifies HMAC-SHA256 over the exact raw body with `GITHUB_WEBHOOK_SECRET`
(constant-time compare, fail-closed: 503 when the secret is absent, 401 on
mismatch). Normalizes the delivery into a canonical cognition event
(`event_id = "github:<delivery>"`, `schema_version "2.0.0"`), resolves the owner
via RPC `nayanet_resolve_github_webhook_owner` (installation id + repository),
then persists via RPC `nayanet_record_cognition_event` with
`p_action = "github_webhook_received"`. Returns `PERSISTED` or `REPLAYED`.
Gateway `verify_jwt: false` live — it does its own HMAC auth in code.

## Live state (Management API, 2026-11-21)

- Function id `a597bbe4-8ed8-4afc-acc9-cda06a171e9f`, ACTIVE, **v16**
- Created 2026-09-18 21:42:22 UTC · updated 2026-09-24 23:04:08 UTC
- `verify_jwt: false`, `import_map: false`
- Entrypoint: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_a597bbe4-8ed8-4afc-acc9-cda06a171e9f_4/source/index.ts`
  (hand-uploaded, not the repo deployment path)
- Live bundle digest (`ezbr_sha256`):
  `36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072`

## Parity signal — and its limit

- The live `ezbr_sha256` **exactly equals** the deployed-bundle digest recorded
  2026-09-24 for the v4 deployment in the production boundary doc
  (`.naya/project-intelligence/GITHUB-WEBHOOK-P1-CREDENTIAL-BOUNDARY-2026-09-24.md`,
  corroborated by the Oct 20 black-box map,
  `~/workspace/team-nitro/webhook-map/WEBHOOK-BLACKBOX-MAP.md`). That is the
  strongest parity signal available for any of the six functions — but it is a
  digest match against a second-hand record, not a recomputation from the source
  here, and the live version is now v16 (re-deploys of identical bytes bump the
  version without changing the hash). **Deployed-bytes parity is still NOT proven
  from here;** the Management API offers no bundle download.
- The GitHub webhook that should deliver to this function (repo Settings →
  Webhooks) was unverifiable from here (hooks:read → 403); the delivery URL,
  subscribed events, and whether deliveries currently flow are UNKNOWN.
