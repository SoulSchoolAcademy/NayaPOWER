# AI1 Production Dispatch Package V1

**Status:** PREPARED / NOT EXECUTED  
**Prepared from canonical main:** `2a7651e95e3d8aee5723324d90aa5234569b542e`  
**Important:** do **not** promote that SHA for AI1. This preparation pass found a real migration dependency inversion on main. The production candidate must be the exact main SHA **after** the repair in this package is merged and all required gates are green.

## Why the prior exact SHA is no longer the deploy candidate

The earlier package target `6b4a429472113bdd5b5186d0b9222f44463b273d` is no longer current main. Main advanced through Brain index regeneration, receipt refresh, and pointer-integrity hardening to `2a7651e95e3d8aee5723324d90aa5234569b542e`.

During dispatch preparation, the two pending AI1 migrations were found in this filename order:

1. `20260930214500_ai1_supersede_capability_integrity_v1.sql`
2. `20260930235959_ai1_capability_carry_v1.sql`

But the first file explicitly declares that it **depends on** the second. A normal ordered migration runner would therefore apply them in the opposite of the declared dependency order.

This package repairs the filename to:

1. `20260930235959_ai1_capability_carry_v1.sql`
2. `20261001000100_ai1_supersede_capability_integrity_v1.sql`

and adds a regression test so the inversion cannot silently return.

## Canonical production authority

The repository contains ratified `STANDING-PRODUCTION-PROMOTION-V1` with `automatic_execution: true` for the narrow existing main→production mechanism. Therefore a new per-deploy human click is **not inherently required** when all standing-policy preconditions are satisfied.

If standing promotion blocks, it must fail closed. A manual dispatch is a separate path and requires:
- `confirm=DEPLOY`
- exact 40-hex `source_sha`
- that SHA must still equal resolved `origin/main`.

No stale SHA may be reused after main moves.

## Exact deployment order

For the eventual exact post-merge main SHA `S`:

1. Resolve `origin/main == S`.
2. Require exact-S Kernel Tests PASS.
3. Require exact-S Collective Chain Readiness Gate PASS.
4. Require no unresolved production blocker under the standing policy.
5. Build the provenance-stamped production deployment commit from `S`.
6. Advance `production` non-force to that deployment commit.
7. Require a **new successful Supabase GitHub Integration deployment check** for that deployment commit.
8. Supabase migration execution must see pending migrations in this order:
   - `20260930235959_ai1_capability_carry_v1.sql`
   - `20261001000100_ai1_supersede_capability_integrity_v1.sql`
9. Only after the schema/RPC migrations are applied may the updated `nayanet-intelligence-commit-runtime` function be treated as production-usable with `p_capabilities` on commit/supersede calls.
10. Revalidate source/deployment ownership and dispatch the existing producer/proof workflows bound to `expected_source_sha=S`.
11. Prove the parity equation:
   `canonical_main_sha == authorized_source_sha == deployed_source_revision == verified_runtime_source`.
12. Only after parity, proceed to the AI1 setup-proof chain below.

## Post-deploy AI1 setup-proof chain — NOT the causal experiment

After deployment parity is proven:

1. Create fresh governed v2 SN-013 and SN-014 intelligence commits through the canonical full commit path with their bounded capability metadata.
2. Independently reread Event → Block → Lineage → Relationship → Index → Checkpoint → receipt for each.
3. Recompute the v2 registry content hash from the independently reread persisted `nayanet_intelligent_blocks.content` object. Do not substitute the runtime raw-lesson `content_hash`.
4. Freeze/witness preregistration v2 with the new real block identities/hashes while preserving v1 byte-for-byte.
5. Promote only through the existing governed learning verifier.
6. Independently reread the promoted block and evidence.
7. Run the production KNOW setup probe against the exact required capability.
8. Require the intended treatment block to return **HIT** and all wrong-capability/owner/state/supersession controls to fail as preregistered.
9. Stop. A successful setup probe does **not** authorize the causal experiment.

## Explicit stop conditions

Stop immediately and classify the rung if any of these occurs:

- main changes after source candidate resolution;
- either required CI gate is missing, pending, or failed;
- production blocker/policy check is not ALLOW;
- pending migration order differs from the order above;
- Supabase deployment check is absent or non-success;
- deployed runtime source cannot be independently tied to exact source SHA;
- runtime sends an RPC argument not present in deployed SQL;
- fresh v2 commit does not produce the complete persisted lineage chain;
- independent reread disagrees with executor output;
- registry content hash cannot be recomputed from persisted content;
- learning state is manually flipped or bypasses the canonical verifier;
- KNOW setup probe returns MISS, wrong block, wrong capability, or ambiguous selection;
- any authority, owner, privacy, or Graph V2 boundary must be widened to continue.

**UNKNOWN ≠ PASS. BLOCKED ≠ PASS. IMPLEMENTED ≠ PRODUCTION-PROVEN.**

## Brain self-map parallel track

The Brain generator now exists at `tools/regenerate_brain_index.py`. This package wires its `--check` mode into required Kernel Tests so future BRAIN structural drift fails CI instead of silently rotting the index.

This is the intended compounding pattern:

`manual repair → generator → CI drift guard → future failure becomes automatic signal`.

## One next consequential action

Review this repair PR. If accepted, merge it only when you are comfortable allowing the repository's already-ratified standing production policy to evaluate the new exact main SHA. Do **not** run the AI1 causal experiment from this package.
