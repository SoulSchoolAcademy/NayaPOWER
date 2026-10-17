# Proof

**Brain-level status: PROPOSED pending Human-Director ratification. Individual files carry their own status declarations (see file headers).**

Owns evidence, provenance, verification, causal acceptance, replay, regression, and production-proof boundaries.

Implementation is not verification.

## Contents (9 files + this README = 10)

| File | Purpose |
|---|---|
| [0001-PROOF-CONTRACT-V1.md](./0001-PROOF-CONTRACT-V1.md) | Core proof and evidence rules |
| [0006-LAW-LIVE-PROOF-36620001626-V1.json](./0006-LAW-LIVE-PROOF-36620001626-V1.json) | Machine receipt: LAW live proof run 36620001626 (historical) |
| [0006-LAW-LIVE-PROOF-36620001626-V1.md](./0006-LAW-LIVE-PROOF-36620001626-V1.md) | Human projection of the LAW live proof receipt |
| [0007-ACT-LIVE-PROOF-36622283683-V1.json](./0007-ACT-LIVE-PROOF-36622283683-V1.json) | Machine receipt: ACT live proof run 36622283683 (historical) |
| [0007-ACT-LIVE-PROOF-36622283683-V1.md](./0007-ACT-LIVE-PROOF-36622283683-V1.md) | Human projection of the ACT live proof receipt |
| [2026-09-29-KNOW-HANDLER-FRESHNESS-PROOF.md](./2026-09-29-KNOW-HANDLER-FRESHNESS-PROOF.md) | Dated KNOW handler freshness source-proof (historical) |
| [2026-09-29-STANDING-PROMOTION-ACTIVATION.md](./2026-09-29-STANDING-PROMOTION-ACTIVATION.md) | Dated standing-promotion activation record (historical) |
| [2026-09-29-STANDING-PROMOTION-ENFORCEMENT-PROOF.md](./2026-09-29-STANDING-PROMOTION-ENFORCEMENT-PROOF.md) | Dated standing-promotion enforcement proof (historical) |
| [2026-09-30-ACT-CONCURRENT-IDEMPOTENCY-PROOF.md](./2026-09-30-ACT-CONCURRENT-IDEMPOTENCY-PROOF.md) | Dated ACT concurrent-idempotency point-in-time proof (historical) |

> **Note (2026-09-30):** the dated `2026-09-2*` / `2026-09-30-*` files are point-in-time evidence snapshots. Their embedded SHAs describe the main revision at the time of writing — see live main for current. They are preserved as historical evidence, not current claims.

## Tip-pinned proof by construction (2026-10-07)

Every green `live-law-proof.yml` run commits its own proof receipt into this
directory (`0006-LAW-LIVE-PROOF-<run_id>-V1.json`, schema
`naya.law.live-proof.v1`, `source_main` = the exact main SHA the proof ran
against) via the `publish-tip-proof` job, built by the fail-closed
`scripts/build_law_tip_proof.py` — the negative control (capability without
authority MUST be refused) is re-validated before anything lands, and the
brain index is regenerated in the same commit. [`LATEST-LAW-LIVE-PROOF.json`](./LATEST-LAW-LIVE-PROOF.json)
is the registry pointer to the newest receipt. Historical hand-committed
receipts above remain as history; the by-construction series is the current
claim.

## Key Principles

- Proof states: `CLAIMED → SUPPORTED → VERIFIED → PRODUCTION-PROVEN`
- Claim strength must never exceed evidence strength
- Unknown is not verified; implemented is not verified; verified is not production-proven
- Conflicts must be surfaced, not resolved by fiat
- Correlation does not imply causation without adequate evidence
