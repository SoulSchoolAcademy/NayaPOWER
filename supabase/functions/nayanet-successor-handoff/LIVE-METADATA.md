# nayanet-successor-handoff — live metadata record (source UNRECOVERABLE)

Filed: 2026-11-21, Supabase filing round, Seat 3 (Edge Functions).
Branch: `supabase/filing-20261121-edge`. Status: **UNRECOVERABLE — metadata only**.

No implementation is filed with this record. Nothing was invented. The source of
this live function could not be found anywhere searched (below). This record is
the filing for this function.

## Live state (Management API, 2026-11-21 — first-hand)

- Function id `00c1bd69-1f11-4493-8f20-1a0bdffb1b4a`, ACTIVE, **v15**
- Created 2026-09-21 16:49:31 UTC · updated 2026-09-21 18:21:30 UTC
- `verify_jwt: true`, `import_map: false`
- Entrypoint: `file:///tmp/user_fn_dahisasgpfvziswqvmvm_00c1bd69-1f11-4493-8f20-1a0bdffb1b4a_2/source/index.ts`
  (hand-uploaded, not the repo deployment path)
- Live bundle digest (`ezbr_sha256`):
  `729592d082e1622eb895c1015d17059697323b6b4fd6952a930e7882c9a52d79`

## Purpose (registry + report only — NOT verified from source)

- The 2026-10-19 inventory report lists it in the learning/verification/
  continuity layer as handing "the machine's intelligence to a successor Naya".
- The runtime registry (`BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json`, EVOLVE
  node, `phantom_binding_reconciliation`) says: **"nayanet-successor-handoff is
  not present on current main and is no longer claimed as an active runtime
  entrypoint. Restore it only if future evidence establishes it as the
  canonical seam."** Note the tension: the registry un-claims it as an
  entrypoint while the function is ACTIVE live at v15. The registry speaks
  about `main`; the live deployment speaks for itself. Which one is right about
  whether it should exist is a decision for the coordinator, not this seat.

## Known callers

- **None found.** No workflow, page, worker, or function in the repo calls this
  slug. The successor flow it supposedly serves is exercised live by
  `nayanet-cold-runtime-proof` (cold-successor modes) — whether that proof or
  anything else invokes this function is UNKNOWN.

## Related artifact — NOT the deployed source (do not mistake it for one)

`supabase/functions/nayanet-pi-successor-handoff/index.ts` existed in the
pre-reset tree (commit `96a7ffaa`, blob `298335c73f44f191d6d6815e3da992ac76cfd3e4`,
1,549 B, sha256 `28202802a1761adbb00984ada0f9d6d8e4203505eda5e0efe23f9b1dac591a05`).
It is a **different slug** (`nayanet-pi-successor-handoff`, not
`nayanet-successor-handoff`): a thin delegate that forwards the request body
plus `action: "successor_handoff"` to `nayanet-compound-intelligence` — a
function that is itself neither on `main` nor live. It is filed here as a
lead only, NOT as this function's source: the slugs differ, the delegate
target does not exist live, and nothing ties the live v15 bundle to it.
Its source is NOT copied into this directory, to avoid presenting a look-alike
as the real thing.

## What was searched (all negative for source)

1. Management API `GET /projects/dahisasgpfvziswqvmvm/functions` + per-function
   metadata — metadata only, no source or bundle path offered.
2. GitHub code search, repo `SoulSchoolAcademy/NayaPOWER`, default branch —
   exactly one hit: the registry file above (a mention, never source).
3. `main` history: `GET /commits?path=supabase/functions/nayanet-successor-handoff`
   — **0 commits ever touched that path**.
4. Pre-reset tree (parent of reset `b31f37fd`, commit `96a7ffaa`): no directory
   of this exact name (only the `nayanet-pi-successor-handoff` relative above).
5. All-branch sweep: `supabase/functions/` directory listing on 203 of 227 repo
   branches checked by filing time — no branch checked carries a directory of
   this exact name; the remaining 24 (walk-end/*, walkthrough/*,
   smart-messenger-icons/ultimate) are page/flow branches and were still being
   checked when this record was filed. (Sweep script:
   `~/workspace/team-nitro/supabase/filing-20261121/sweep_branches.py`.)
6. `supabase/config.toml` on `main`: not declared (none of the six is).

## What would recover it

- The hand-upload (Sep 21 2026, `_2/source/index.ts`) is the only known
  provenance; no uploader identity is recorded anywhere reachable from here.
- If the live v15 bundle is the `pi-` delegate renamed, the pi source above is
  the lead — but that is a hypothesis, not a recovery, and it must be proven
  (e.g. by a controlled call observing the delegate's behaviour) before anyone
  files it as source.
- **Deployed-bytes parity is NOT provable from here** even if a candidate source
  surfaces later: the live `ezbr_sha256` has no repo counterpart, and the
  Management API offers no bundle download.
