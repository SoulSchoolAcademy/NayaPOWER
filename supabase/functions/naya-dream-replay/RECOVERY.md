# naya-dream-replay — source recovery record

Filed: 2026-11-21, Supabase filing round, Seat 3 (Edge Functions).
Branch: `supabase/filing-20261121-edge`. Status: **FILED (recovered source)**.

## ⚠️ Flag on the brief — read first

The seat brief ordered this function **metadata-only** ("a DROP candidate (no
source, no caller, no flow): metadata only, never an implementation"). That
premise turned out to be wrong on the first point: **the source DOES exist in
repo history** (below), and the recovered source shows exactly what it does.
Per the sense check (do not obey a brief past the sense of the page) and the
harvest law (harvest, never invent), the recovered source is filed here
alongside the metadata record — it is a recovery of bytes that existed, not an
implementation written for this round. **Nothing is deployed, nothing is
deleted, nothing is re-activated by this filing.** The DROP candidacy itself
is unchanged and still needs the coordinator's / Shawn's word. If the
coordinator holds to metadata-only, strike `index.ts` from this branch and
keep `LIVE-METADATA.md` + this file.

## What was recovered

`index.ts` in this directory is the file as it stood in repo history — byte-identical
to the source blob, verified by sha256 (see below). Nothing was invented, rewritten,
or reformatted.

- **Source as of:** parent of the reset, commit `96a7ffaa8728f65da2d02eb2b7c7c8cf504e88fd`
  (2026-09-26 tree, immediately before the reset deleted it)
- **Source path then:** `supabase/functions/naya-dream-replay/index.ts`
- **Source blob sha:** `178784f990ddb80d0bb53fe9e25da46ee0501851`
- **Size:** 7,209 B · **sha256:** `145df9790eca942f0c46db87a2b8a7fa2ce7e86e2ba4af1e5bcf70e4c6bd0b82`
- **History:** added `b79065e7` (2026-09-18T22:31:15Z) — "feat: add canonical Naya
  Dream replay function source"; last modified `dc11aea8` (2026-09-19T02:06:15Z) —
  "fix: handle scalar Dream receipt evidence safely". Removed from `main` by the
  reset commit `b31f37fd` (2026-09-27). Never re-added to `main` after the reset.
- **Original directory contents:** `index.ts` only (no `deno.json`, no helpers).

## What it does (read from the recovered source, not assumed)

POST only, user-JWT authenticated (gateway `verify_jwt: true` live, and the code
refuses anonymous callers with `AUTHENTICATED_USER_REQUIRED`). Given a
`project_id` (default `NayaNET`) and an `idempotency_key` (required, or
`x-idempotency-key` header), it reads the caller's latest
`nayanet_cognition_events` row (optionally one `event_id`) plus their last 20
`nayanet_execution_receipts`, computes a **SIMULATED** replay — baseline
`HISTORY_ONLY_V1` vs counterfactual `HISTORY_PLUS_VERIFIED_RECEIPT_V1` under
`NAYANET_DREAM_SCORE_V1` (task score + responsible value
`benefit - harm - cost - risk_adjusted_loss`; `policy_improvement: NOT_PROVEN`) —
and writes one row to `nayanet_dream_replays` (idempotent on `idempotency_key`;
duplicate returns the existing replay). It performs no execution, grants no
authority, and changes no production policy (`execution_performed: false`,
`authority_granted: false`).

## Callers

None found in the repo (no code-search hit for the slug outside today's
four-part-bridge note; no workflow, page, or worker calls it). It is a
user-JWT endpoint, so any authenticated user could call it directly — but no
in-repo caller exists. "No caller" stands; "no flow" does not — the flow is the
simulated dream replay above, and it serves the learning/verification/continuity
layer, not a citizen-facing Vault flow.

## Live state (Management API, 2026-11-21)

- Function id `a60ccf2e-7e8e-4df4-b3a7-a35bb48986ee`, ACTIVE, **v18**
- Created 2026-09-18 20:54:02 UTC · updated 2026-09-19 02:06:18 UTC
- `verify_jwt: true`, `import_map: false`
- Entrypoint: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_a60ccf2e-7e8e-4df4-b3a7-a35bb48986ee_4/source/index.ts`
  (hand-uploaded, not the repo deployment path)
- Live bundle digest (`ezbr_sha256`):
  `04266dcda23d3584e1a43d3adba8bb7ba59edc01678833b3e2b743b7f392463d`

## Parity limit

- The live last-update (2026-09-19 02:06 UTC) matches the last repo source change
  (`dc11aea8`, 2026-09-19 02:06:15Z) to the minute — consistent with the deployed
  bundle being this source, but **deployed-bytes parity is NOT provable from
  here**: the live `ezbr_sha256` has no repo counterpart to compare against, and
  the Management API offers no bundle download. Do not claim the filed source
  equals the deployed v18 bytes.
