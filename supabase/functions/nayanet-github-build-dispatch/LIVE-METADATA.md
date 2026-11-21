# nayanet-github-build-dispatch — live metadata record (source UNRECOVERABLE)

Filed: 2026-11-21, Supabase filing round, Seat 3 (Edge Functions).
Branch: `supabase/filing-20261121-edge`. Status: **UNRECOVERABLE — metadata only**.

No implementation is filed with this record. Nothing was invented. The source of
this live function could not be found anywhere searched (below). This record is
the filing for this function.

## Live state (Management API, 2026-11-21 — first-hand)

- Function id `a2eb0a31-6f59-45bf-9db1-cd796a54df49`, ACTIVE, **v17**
- Created 2026-09-12 23:55:30 UTC · updated 2026-09-12 23:55:30 UTC
  (created and last updated in the same second — 17 deployments since, same bytes
  or re-deploys; the version count is a deployment count, not a change count)
- `verify_jwt: true`, `import_map: true`
- Entrypoint: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_a2eb0a31-6f59-45bf-9db1-cd796a54df49_1/source/index.ts`
  (hand-uploaded, not the repo deployment path)
- Import map: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_a2eb0a31-6f59-45bf-9db1-cd796a54df49_1/source/deno.json`
  (the only one of the six with an import map — it had a `deno.json` when uploaded)
- Live bundle digest (`ezbr_sha256`):
  `439686f6bd28e1962cfbddbe11ef18833f141f2596db4fb2863a05c15d014d6b`

## Purpose (relayed report only — NOT verified from source)

The 2026-10-19 inventory report (relayed to Shawn, addressed to "Naya 6";
recorded in `~/memory/2026-10-19.md`) says: **"verify-hub-build workflow only —
NOT a general Smart Factory build service."** No source exists to verify what it
verifies, how it authenticates the workflow, or what it returns. Treat the
purpose as a name, not a proof.

## Known callers

- **None found.** No workflow named `verify-hub-build` (or `verify_hub_build`)
  exists on `main` or in the pre-reset tree, and no file on `main` references this
  function (code search: zero hits outside today's four-part-bridge Naya Note,
  which only lists it). The Oct 19 report's "Hub build-verification workflow"
  caller cannot be located. Whether any workflow still calls it is UNKNOWN.

## What was searched (all negative)

1. Management API `GET /projects/dahisasgpfvziswqvmvm/functions` + per-function
   metadata — metadata only, no source or bundle path offered.
2. GitHub code search, repo `SoulSchoolAcademy/NayaPOWER`, default branch —
   zero code hits (only `BRAIN/05-MEMORY/NAYA-NOTES/2026/11/21/NN-20261121-the-four-part-bridge-flow-like-water.md`
   and its paired Smart Note SN-4505, both from today, which only list the name).
3. `main` history: `GET /commits?path=supabase/functions/nayanet-github-build-dispatch`
   — **0 commits ever touched that path**.
4. Pre-reset tree (parent of reset `b31f37fd`, commit `96a7ffaa`): the function
   is absent from `supabase/functions/` and from `NAYANET/EXECUTION-BRIDGE/`.
5. All-branch sweep: `supabase/functions/` directory listing on 203 of 227 repo
   branches checked by filing time — no branch checked carries a directory of
   this name; the remaining 24 (walk-end/*, walkthrough/*,
   smart-messenger-icons/ultimate) are page/flow branches and were still being
   checked when this record was filed. (Sweep script:
   `~/workspace/team-nitro/supabase/filing-20261121/sweep_branches.py`.)
6. `supabase/config.toml` on `main`: the function is not declared (none of the
   six sourceless functions is).
7. `~/memory/` (Oct 19 inventory + Oct 20 webhook investigation): only the
   relayed one-line purpose above; no source location, no caller workflow name.

## What would recover it

- The machine or person who hand-uploaded it (entrypoint `_1/source/index.ts`,
  Sep 12 2026) may hold the original file; no uploader identity is recorded
  anywhere reachable from here.
- The calling workflow, if it still exists under another name, would name the
  function URL; it was not found on `main`. A GitHub-side search of workflow
  run history for calls to `/functions/v1/nayanet-github-build-dispatch` is a
  follow-on for another round (not run here — read-only, and outside this seat).
- **Deployed-bytes parity is NOT provable from here** even if a candidate source
  surfaces later: the live `ezbr_sha256` has no repo counterpart, and the
  Management API offers no bundle download.
