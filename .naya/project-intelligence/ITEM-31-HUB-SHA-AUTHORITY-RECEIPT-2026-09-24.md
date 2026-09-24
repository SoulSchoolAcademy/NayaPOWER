# NayaPOWER — Hub SHA Authority Reconciliation Receipt

**Date:** 2026-09-24
**Item:** 31 successor boundary
**Status:** SOURCE AUTHORITY RESOLVED — DERIVED PROJECTION MECHANISM BLOCKED
**Branch:** `coda2/hub-sha-authority-receipt-20260924`
**Base main:** `b48aa8fd6fcc41660e22a99f357e4e2da8658c51`
**Canonical Hub source:** `NAYANET/HUB/index.html`
**Current source blob:** `eb825f34caecdb925bd3d7fe6a4390ce072025d7`
**Recorded prior checkpoint:** `7b1126a014b3b27026a0360dbc1b8226a9be9f50`
**Issue:** #554

## Authority determination

The current Hub source is authoritative. The recorded `7b1126a...` value is an authentic prior checkpoint, not the current source identity.

Evidence:

- PR #549 introduced the `7b1126a...` Hub checkpoint.
- Commit `b313d756dbfaf495f696ad42b58793247aaa2684` synchronized control-plane pointers to that checkpoint.
- PR #559 / merge `ad3e0118bdaf9086de3abcb5af68c263fdb66002` intentionally removed only the duplicate Hub entry gate and changed the source to `eb825f34...`.
- PR #561 / merge `ad2d2ba466fe60a3443611fb18dead428a57d800` advanced `.naya/control-plane/HUB-PRESERVATION.json` to `eb825f34...`.
- The canonical release run `35944908213` accepted the preservation gate and verified exact source/live parity and browser acceptance for the current Hub source.
- Current main `b48aa8fd...` carries the same Hub source blob.

The older visual/structural references remain historical preservation references; they do not override the active current source contract.

## Divergence surfaces

- `.naya/control-plane/STATE.json:38` records `7b1126a...`.
- `.naya/control-plane/MAP.json:67` and `:236` record `7b1126a...`.
- `.naya/control-plane/MAP.json:27` records an additional divergent authority value `ddffaf5a6ac5eccbca8d8a6c4b76ff26d3b70058`.
- `.naya/control-plane/BATON.json:22` records `7b1126a...`.
- `.naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md:17` records `7b1126a...`.
- Live `main:NAYANET/HUB/index.html` resolves to `eb825f34...`.

## Existing generation path

- `.naya/runtime/baton.py:29-85` is the canonical BATON builder. It derives the Hub blob at `:84` and writes only `.naya/control-plane/BATON.json` at `:190-193`.
- `.github/workflows/verify-next-action-handoff-cycle.yml:31-40` invokes the BATON builder, but only after a state-mutating next-action cycle; that cycle is currently blocked and is not a Hub identity reconciler.
- `.github/workflows/verify-control-plane-sync.yml` is verification-only and does not update Hub identity projections.
- `.github/workflows/assistant-cloudflare-hub-release.yml:76-133` validates the active Hub source and preservation checkpoint; it does not reconcile STATE/MAP/BATON/TEAM_NAYA.
- No existing canonical all-surface SHA projection generator was found.

The current Item 31 validator checks STATE, selected MAP values, BATON, and TEAM_NAYA at `scripts/validate-control-plane-freshness.py:315-339`, but does not check `MAP.authority.canonical_hub_source_sha` at `MAP.json:27`. A BATON-only rebuild would therefore be partial and could leave hidden divergence.

## No mutation

No Hub source, control-plane, validator, workflow, deployment, or historical evidence file was changed in this unit. No hash was replaced merely to satisfy validation.

## Blocker

Source authority is resolved, but the repository lacks an existing canonical mechanism that atomically projects the authoritative Hub blob into every derived identity surface. Updating only BATON would be incomplete; independently editing STATE, MAP, TEAM_NAYA, and the hidden MAP authority field would violate the one-authority/derived-artifact discipline.

## Exact successor action

Open a separately authorized control-plane Hub identity projection reconciliation unit that defines the atomic projection/receipt path from `HUB-PRESERVATION.json` and live `main` to all covered surfaces, then regenerate BATON through the existing builder and run the mainline freshness audit. Do not modify the Hub source or visual freeze in that unit.
