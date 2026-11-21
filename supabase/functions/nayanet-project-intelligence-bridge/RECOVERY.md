# nayanet-project-intelligence-bridge — source recovery record

Filed: 2026-11-21, Supabase filing round, Seat 3 (Edge Functions).
Branch: `supabase/filing-20261121-edge`. Status: **FILED (recovered source)**.

## What was recovered

`index.ts` in this directory is the file as it stood in repo history — byte-identical
to the source blob, verified by sha256 (see below). Nothing was invented, rewritten,
or reformatted.

- **Source commit:** `ffd6e883` (2026-09-25T03:49:32Z) — "fix(oidc): bind bridge owners
  to workflow runs (#697)"
- **Source path then:** `supabase/functions/nayanet-project-intelligence-bridge/index.ts`
- **Source blob sha:** `ea9c24516c1cd65a8dc39371791a6c2febb84323`
- **Size:** 9,799 B · **sha256:** `88ca8d31ba9ddcb760488a3bcfef27335b73187e2392f2708599199571ad79ef`
- **History:** added `91d2ccda` (2026-09-21), modified `f91caa1f`, `68fb7829`,
  `ffd6e883` (2026-09-25). Removed from `main` by the reset commit `b31f37fd`
  ("reset: establish 2026-09-26 Nine-Node clean start", 2026-09-27). It was never
  re-added to `main` after the reset.
- **Original directory contents:** `index.ts` only (no `deno.json`, no helpers).

## What it does (read from the recovered source, not assumed)

POST only. Verifies a GitHub Actions OIDC token (audience
`nayanet-project-intelligence-bridge`, repo `SoulSchoolAcademy/NayaPOWER`,
`refs/heads/main`, allow-listed workflow refs via
`NAYANET_BRIDGE_ALLOWED_WORKFLOW_REFS`), consumes a one-time owner binding
(`nayanet_consume_bridge_owner_binding`), then persists a
`NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1` packet to
`nayanet_project_intelligence_bridge`, projects it as a `nayanet_cognition_events`
row, and requires the canonical `nayanet_intelligence_index` row to exist
(written by the cognition-event trigger). Idempotent on `idempotency_key`
(replays return `ACCEPTED` + `replay: true`). Gateway `verify_jwt: false` live —
it does its own OIDC auth in code.

## Live state (Management API, 2026-11-21)

- Function id `92a75eeb-2d31-46b8-b297-b8db691cdf22`, ACTIVE, **v17**
- Created 2026-09-21 16:08:54 UTC · updated 2026-09-21 17:13:04 UTC
- `verify_jwt: false`, `import_map: false`
- Entrypoint: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_92a75eeb-2d31-46b8-b297-b8db691cdf22_4/source/index.ts`
  (hand-uploaded, not the repo deployment path)
- Live bundle digest (`ezbr_sha256`):
  `84cc5b23ddb38301eceb16633665dc3388a68d50953b9dd0914d9be905f0c40d`

## Parity limit — read this before trusting the filing

- The live function was last updated **2026-09-21 17:13 UTC**, but the repo source
  kept changing until **2026-09-25** (`ffd6e883`). The filed source is NEWER than
  the deployed bundle by four days. It is the last known repo source, not a
  proven copy of the deployed bytes.
- **Deployed-bytes parity is NOT provable from here.** The live `ezbr_sha256` has
  no repo counterpart to compare against, and the Management API offers no
  bundle download. Do not claim the filed source equals the deployed v17 bytes.
- Also mentioned (not source): `BRAIN/90-OPERATIONS/2026-10-23-MOST-INTELLIGENT-SYSTEM-ASSESSMENT-V1.*`
  (three forms) names the bridge; the Oct 19 inventory lists it with no description.
