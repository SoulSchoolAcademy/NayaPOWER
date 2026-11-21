# nayanet-invite-sender — live metadata record (source UNRECOVERABLE)

Filed: 2026-11-21, Supabase filing round, Seat 3 (Edge Functions).
Branch: `supabase/filing-20261121-edge`. Status: **UNRECOVERABLE — metadata only**.

No implementation is filed with this record. Nothing was invented. The source of
this live function could not be found anywhere searched (below). This record is
the filing for this function.

## Live state (Management API, 2026-11-21 — first-hand)

- Function id `fdd986d7-192d-40a1-82d4-04d4dc81be6e`, ACTIVE, **v6**
- Created 2026-10-20 04:34:53 UTC · updated 2026-10-20 06:10:15 UTC
- `verify_jwt: true`, `import_map: false`
- Entrypoint: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_fdd986d7-192d-40a1-82d4-04d4dc81be6e_5/source/index.ts`
  (hand-uploaded, not the repo deployment path)
- Live bundle digest (`ezbr_sha256`):
  `7fc062b30650f6fc0a971c933060a227419842243cd5a0d9aac3556a30f44d07`
- Spot-probed live 2026-11-10 (audit `~/workspace/team-nitro/SUPABASE-AUDIT-20261110.md`):
  answers auth-gated (exists); the probe did not establish behaviour.

## Known caller — verified in repo source (first-hand)

The Smart Match Cloudflare worker calls it with the **service-role key**:

- File: `~/workspace/team-nitro/smart-match/worker-before-port-update.js:779`
  (`const INVITE_FN_URL = SB_URL + '/functions/v1/nayanet-invite-sender'`)
- `GET /status/<invite-code>` — invite code status, via `apiJoinVisited`
  (worker line 803; the walk pings `/api/join/visited?invite=` on arrival)
- `POST /mark-joined { code }` — mark an invite joined, via `apiJoinMarkJoined`
  (worker line 811; called when an invite code rode along with a join)

Those are the only two `inviteFn()` call sites in the worker. What the function
stores, how invite codes are minted, what `/status/` returns beyond `status`,
and whether it sends anything itself are all **unverified** — the purpose
"sends invites — the Inviter / ambassador leg" is inferred from the name and
these two routes only.

## What was searched (all negative for source)

1. Management API `GET /projects/dahisasgpfvziswqvmvm/functions` + per-function
   metadata — metadata only, no source or bundle path offered.
2. GitHub code search, repo `SoulSchoolAcademy/NayaPOWER`, default branch —
   zero code hits (only today's four-part-bridge Naya Note + SN-4505, which
   only list the name).
3. `main` history: `GET /commits?path=supabase/functions/nayanet-invite-sender`
   — **0 commits ever touched that path**.
4. Pre-reset tree (parent of reset `b31f37fd`, commit `96a7ffaa`): absent from
   `supabase/functions/` and from `NAYANET/EXECUTION-BRIDGE/`.
5. All-branch sweep: `supabase/functions/` directory listing on 203 of 227 repo
   branches checked by filing time — no branch checked carries a directory of
   this name; the remaining 24 (walk-end/*, walkthrough/*,
   smart-messenger-icons/ultimate) are page/flow branches and were still being
   checked when this record was filed. (Sweep script:
   `~/workspace/team-nitro/supabase/filing-20261121/sweep_branches.py`.)
6. `supabase/config.toml` on `main`: not declared (none of the six is).
7. Local workspace + `~/memory/`: the caller above (smart-match worker) and the
   Nov 10 audit probe; no source file, no design note describing its routes.

## What would recover it

- The hand-upload (Oct 20 2026, `_5/source/index.ts`) predates the Inviter
  branches in the repo (`inviter/*`, Nov 20–21) — the source may live in the
  Smart Match worker's own history or the uploader's local copy, not in
  `NayaPOWER`. The worker file that calls it is the first place to look.
- **Deployed-bytes parity is NOT provable from here** even if a candidate source
  surfaces later: the live `ezbr_sha256` has no repo counterpart, and the
  Management API offers no bundle download.
